# -*- coding: utf-8 -*-
"""P2 隔离断言脚本（A1–A10）——规格来源＝P1规格件 v1.2 §4。

每次链路运行后执行；输出全 PASS/FAIL 逐项日志，入 P3 汇整。

自命中规避（§3 注，A4 既有手法之扩用）：本脚本位于 verify/ 子树，而 A2 要求
标记串于 entity/∪verify/ 命中数==0、A4 要求关键字集于 entity/ 命中数==0。
故一切被检字符串均以拼接形态构造，源码中不出现完整字面量。

状态三值：PASS / FAIL / PENDING。PENDING＝该断言之触点尚未到达（例如连接尚未
发生时之 A8），非通过亦非失败；不得以 PENDING 充抵 PASS。
"""

import hashlib
import json
import os
import platform
import re
import sys

# --------------------------------------------------------------------------
# 拼接形态常量（防自命中）
# --------------------------------------------------------------------------

MARK = "_pro" + "be_"                                   # 外部数据标记串
DATA_SOURCE_KEY = "_data_source"
DATA_SOURCE_VALUE = "external" + MARK + "NOT_FOR_ENTITY"
KD_PARAMS_FILENAME = "kd_params" + MARK + ".json"

FORBIDDEN_KEYWORDS = ["IB" + "KR", "Quant" + "Connect", "https" + "://"]

ORDER_SIDE_APIS = [
    "placeOrder", "cancelOrder", "reqGlobalCancel", "exerciseOptions",
    "whatIfOrder", "bracketOrder", "oneCancelsAll",
    "MarketOrder", "LimitOrder", "StopOrder", "StopLimitOrder",
]

# 85-1a 核证值（engine v1.3 逐字节复用锚）
ENGINE_SHA256 = "d88a955e45dddaa5a11f02c9237cb5e178bdfca6335a670ecdf21414dca682cf"
# §4A 照录块锚值（A10）——v1.3（AGENTS.md v1.1，20260812 增第6条凭据纪律）
AGENTS_SHA256 = "ccc753477b66900cd67dd73d830182e092799272f8f68c6b3202d7ec4c5320e7"

# A11 flex 凭据闸（§4B，v1.3 新增）
FLEX_ENV_VARS = ("IB_FLEX_TOKEN", "IB_FLEX_QUERY_ID")
FLEX_GATE = "require_flex_credentials"
FLEX_CALL_MARKER = "@FLEX_CALL_POINT"

PAPER_PORTS = (7497, 4002)
PAPER_ACCT_PREFIXES = ("DU", "DF")

# q/r 数值字面量赋值形态（A9）
QR_FIELDS = ("dividend_yield", "risk_free_rate")
QR_ASSIGN_PATTERNS = [
    re.compile(r"\b(" + "|".join(QR_FIELDS) + r")\s*=\s*[-+]?[0-9.]"),
    re.compile(r"[\"'](" + "|".join(QR_FIELDS) + r")[\"']\s*:\s*[-+]?[0-9.]"),
]

ASSEMBLE_MARKER = "@LOT_ASSEMBLY_POINT"
GATE_CALL = "require_kd_params"

# --------------------------------------------------------------------------
# 路径
# --------------------------------------------------------------------------

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTITY = os.path.join(ROOT, "entity")
VERIFY = os.path.join(ROOT, "verify")
PROBE = os.path.join(ROOT, "probe")

MANIFEST = os.path.join(PROBE, "data_manifest.json")
CONN_LOG = os.path.join(VERIFY, "connection_log.json")
FP_LOG = os.path.join(VERIFY, "engine_fingerprint_log.json")
ASSERT_LOG = os.path.join(VERIFY, "assert_log.json")

HARNESS_FILES = [
    os.path.join(ENTITY, "probe_harness.py"),
    os.path.join(PROBE, "probe_run.py"),
    os.path.join(PROBE, "probe_flex.py"),   # §4B 新增，纳入 A7 只读扫描射程
]


# --------------------------------------------------------------------------
# 工具
# --------------------------------------------------------------------------

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def walk_files(root):
    out = []
    if not os.path.isdir(root):
        return out
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for fn in filenames:
            out.append(os.path.join(dirpath, fn))
    return out


def read_text(path):
    """文本读取；二进制或解码失败返回 None（不参与字符串命中统计，另行登记）。"""
    try:
        with open(path, "rb") as f:
            raw = f.read()
        if b"\x00" in raw:
            return None
        return raw.decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def count_hits(text, needle):
    return text.count(needle)


def redact(s):
    """断言输出自身落在 verify/ 子树内（assert_log.json），若把含标记串之文件名
    原样写入，下一轮 A2 将对本脚本之输出自命中。故一切外发文本先行遮蔽。
    遮蔽只作用于输出面，不影响检测面。"""
    return str(s).replace(MARK, "_pr" + "*be_")


# --------------------------------------------------------------------------
# 断言实现
# --------------------------------------------------------------------------

def a1_dirs():
    """目录三分在场：三目录存在且顶层无第四实体目录。"""
    expected = {"entity", "verify", "probe"}
    present = set()
    extra = []
    for name in os.listdir(ROOT):
        if os.path.isdir(os.path.join(ROOT, name)):
            if name in expected:
                present.add(name)
            elif name.startswith("."):
                extra.append(name + "(点目录)")
            else:
                extra.append(name)
    missing = sorted(expected - present)
    ok = (not missing) and (not extra)
    return ("PASS" if ok else "FAIL",
            "三分在场=%s 缺=%s 第四实体目录=%s" % (sorted(present), missing, extra))


def a2_blacklist():
    """黑名单零渗透：manifest 每一哈希于 entity/∪verify/ 无同哈希文件；
    标记串于 entity/∪verify/ 命中数==0（文件名与内容双面）。"""
    detail = []
    ok = True

    scanned = walk_files(ENTITY) + walk_files(VERIFY)

    # (a) 哈希面
    if os.path.isfile(MANIFEST):
        with open(MANIFEST, "r", encoding="utf-8") as f:
            man = json.load(f)
        black = set()
        for rec in man.get("entries", []):
            if rec.get("sha256"):
                black.add(rec["sha256"].lower())
        collide = []
        for p in scanned:
            try:
                if sha256_file(p).lower() in black:
                    collide.append(os.path.relpath(p, ROOT))
            except OSError:
                pass
        detail.append("manifest哈希数=%d 同哈希渗透=%s" % (len(black), collide))
        if collide:
            ok = False
    else:
        detail.append("manifest未生成(尚无外部载荷)")

    # (b) 标记串面
    name_hits = [os.path.relpath(p, ROOT) for p in scanned if MARK in os.path.basename(p)]
    content_hits = []
    for p in scanned:
        t = read_text(p)
        if t is None:
            continue
        n = count_hits(t, MARK)
        if n:
            content_hits.append("%s×%d" % (os.path.relpath(p, ROOT), n))
    detail.append("标记串文件名命中=%s 内容命中=%s" % (name_hits, content_hits))
    if name_hits or content_hits:
        ok = False

    return ("PASS" if ok else "FAIL", "；".join(detail))


def a3_key_marker():
    """键名标记在场：probe/ 下每一 *MARK*.json 含 _data_source 且值正确。"""
    targets = []
    for p in walk_files(PROBE):
        b = os.path.basename(p)
        if b.endswith(".json") and MARK in b:
            targets.append(p)
    if not targets:
        return ("PENDING", "probe/ 下尚无标记 json（外部载荷未落地）")
    bad = []
    for p in targets:
        try:
            with open(p, "r", encoding="utf-8") as f:
                obj = json.load(f)
        except (OSError, ValueError) as e:
            bad.append("%s(不可解析:%s)" % (os.path.basename(p), e))
            continue
        if not isinstance(obj, dict) or obj.get(DATA_SOURCE_KEY) != DATA_SOURCE_VALUE:
            bad.append("%s(%s缺位或值不符)" % (os.path.basename(p), DATA_SOURCE_KEY))
    return ("PASS" if not bad else "FAIL",
            "受检=%d 不合格=%s" % (len(targets), bad))


def a4_forbidden_scan():
    """forbidden 扫描：entity/ 下关键字集命中数==0（probe/ 豁免）。"""
    hits = []
    for p in walk_files(ENTITY):
        t = read_text(p)
        if t is None:
            continue
        for kw in FORBIDDEN_KEYWORDS:
            n = count_hits(t, kw)
            if n:
                hits.append("%s:%s×%d" % (os.path.relpath(p, ROOT), kw, n))
    return ("PASS" if not hits else "FAIL",
            "entity/受检文件=%d 命中=%s" % (len(walk_files(ENTITY)), hits))


def a5_engine_fingerprint():
    """引擎逐字复用。"""
    p = os.path.join(ENTITY, "engine.py")
    if not os.path.isfile(p):
        return ("FAIL", "entity/engine.py 不在场")
    got = sha256_file(p)
    return ("PASS" if got == ENGINE_SHA256 else "FAIL",
            "实测=%s 锚值=%s" % (got, ENGINE_SHA256))


def a6_zero_write(record=True):
    """零写入可证（M6）：逐次实测指纹入日志，全部相等且等于锚值。
    本函数每次调用追加一条实测记录——「运行前后两次实测」由链路前后各跑一次
    本脚本自然承载，双值同入日志。"""
    p = os.path.join(ENTITY, "engine.py")
    if not os.path.isfile(p):
        return ("FAIL", "entity/engine.py 不在场")
    got = sha256_file(p)

    log = {"anchor": ENGINE_SHA256, "measurements": []}
    if os.path.isfile(FP_LOG):
        try:
            with open(FP_LOG, "r", encoding="utf-8") as f:
                log = json.load(f)
        except ValueError:
            pass
    if record:
        log.setdefault("measurements", []).append(
            {"seq": len(log.get("measurements", [])) + 1,
             "sha256": got,
             "phase": os.environ.get("P2_PHASE", "unspecified")})
        with open(FP_LOG, "w", encoding="utf-8") as f:
            json.dump(log, f, ensure_ascii=False, indent=2)

    vals = [m["sha256"] for m in log.get("measurements", [])]
    ok = bool(vals) and all(v == ENGINE_SHA256 for v in vals)
    return ("PASS" if ok else "FAIL",
            "实测序列n=%d 相异值=%s 全等锚值=%s"
            % (len(vals), sorted(set(vals)), ok))


def a7_readonly():
    """只读纪律：harness 源码中下单侧 API 名命中数==0。"""
    present = [p for p in HARNESS_FILES if os.path.isfile(p)]
    if not present:
        return ("PENDING", "harness 尚未生成")
    hits = []
    for p in present:
        t = read_text(p) or ""
        for api in ORDER_SIDE_APIS:
            n = count_hits(t, api)
            if n:
                hits.append("%s:%s×%d" % (os.path.relpath(p, ROOT), api, n))
    return ("PASS" if not hits else "FAIL",
            "受检=%s 命中=%s" % ([os.path.relpath(p, ROOT) for p in present], hits))


def a8_paper():
    """paper账户：端口白名单 ＋ managedAccounts 前缀校验。"""
    if not os.path.isfile(CONN_LOG):
        return ("PENDING", "连接尚未发生（无 connection_log.json）")
    with open(CONN_LOG, "r", encoding="utf-8") as f:
        c = json.load(f)
    port = c.get("port")
    accts = c.get("managed_accounts") or []
    bad_port = port not in PAPER_PORTS
    bad_accts = [a for a in accts if not str(a).upper().startswith(PAPER_ACCT_PREFIXES)]
    ok = (not bad_port) and bool(accts) and (not bad_accts)
    return ("PASS" if ok else "FAIL",
            "port=%s(白名单%s) accounts=%s 非paper格式=%s"
            % (port, list(PAPER_PORTS), accts, bad_accts))


def a9_qr_gate():
    """q/r赋值闸：数值字面量零命中 ＋ 闸在场且位于组装 lot 之前 ＋ SystemExit 分支在场。"""
    detail = []
    ok = True

    # (a) 数值字面量赋值（entity/∪probe/ 全部 .py）
    hits = []
    for p in walk_files(ENTITY) + walk_files(PROBE):
        if not p.endswith(".py"):
            continue
        t = read_text(p)
        if t is None:
            continue
        for ln, line in enumerate(t.splitlines(), 1):
            for pat in QR_ASSIGN_PATTERNS:
                if pat.search(line):
                    hits.append("%s:%d" % (os.path.relpath(p, ROOT), ln))
    detail.append("字面量赋值命中=%s" % (hits,))
    if hits:
        ok = False

    # (b) 闸在场且序位在组装点之前
    gate_files = [p for p in HARNESS_FILES if os.path.isfile(p)]
    if not gate_files:
        detail.append("harness 尚未生成")
        return ("PENDING", "；".join(detail))

    checked = False
    for p in gate_files:
        t = read_text(p) or ""
        if ASSEMBLE_MARKER not in t:
            continue
        checked = True
        rel = os.path.relpath(p, ROOT)
        i_gate = t.find(GATE_CALL + "(")
        i_asm = t.find(ASSEMBLE_MARKER)
        has_exit = "SystemExit" in t
        good = (i_gate != -1) and (i_gate < i_asm) and has_exit
        detail.append("%s: %s位置=%d 组装点=%d SystemExit=%s → %s"
                      % (rel, GATE_CALL, i_gate, i_asm, has_exit,
                         "OK" if good else "NG"))
        if not good:
            ok = False
    if not checked:
        detail.append("未发现组装点标记（%s），闸序位不可判" % ASSEMBLE_MARKER)
        return ("PENDING", "；".join(detail))

    return ("PASS" if ok else "FAIL", "；".join(detail))


def a10_agents_md():
    """AGENTS.md 在场且同源。"""
    p = os.path.join(ROOT, "AGENTS.md")
    if not os.path.isfile(p):
        return ("FAIL", "工作目录根 AGENTS.md 不在场")
    got = sha256_file(p)
    return ("PASS" if got == AGENTS_SHA256 else "FAIL",
            "实测=%s 锚值=%s" % (got, AGENTS_SHA256))


def a11_flex_gate():
    """flex凭据闸（§4B）：凭据值零落盘 ＋ 闸在场且位于 FlexQuery 调用前 ＋
    SystemExit 分支在场 ＋ manifest／摩擦记录无凭据值。

    本脚本自身不含凭据值——从运行时环境变量取，仅用于**反查是否有文件落了值**。
    """
    detail = []
    ok = True
    flex_file = os.path.join(PROBE, "probe_flex.py")

    # (a) 凭据值字面量零命中：entity/∪probe/∪verify/ 全面（含 manifest、摩擦记录）
    secrets = [v for v in (os.environ.get(k) for k in FLEX_ENV_VARS) if v]
    if not secrets:
        detail.append("环境变量未注入，值字面量面不可判")
        if not os.path.isfile(flex_file):
            return ("PENDING", "；".join(detail + ["probe_flex.py 未生成"]))
        ok = False          # 无法证否即不得判 PASS
    else:
        hits = []
        for p in walk_files(ENTITY) + walk_files(PROBE) + walk_files(VERIFY):
            t = read_text(p)
            if t is None:
                continue
            for s in secrets:
                if s in t:
                    hits.append(os.path.relpath(p, ROOT))
        detail.append("受检环境变量=%d 值字面量命中=%s"
                      % (len(secrets), sorted(set(hits))))
        if hits:
            ok = False

    # (b) 闸在场、序位在 FlexQuery 调用前、SystemExit 分支在场
    if not os.path.isfile(flex_file):
        detail.append("probe/probe_flex.py 未生成")
        return ("PENDING", "；".join(detail))
    t = read_text(flex_file) or ""
    i_gate = t.find(FLEX_GATE + "(")
    i_call = t.find(FLEX_CALL_MARKER)
    has_exit = "SystemExit" in t
    good = (i_gate != -1) and (i_call != -1) and (i_gate < i_call) and has_exit
    detail.append("probe_flex.py: %s位置=%d 调用点=%d SystemExit=%s → %s"
                  % (FLEX_GATE, i_gate, i_call, has_exit,
                     "OK" if good else "NG"))
    if not good:
        ok = False

    return ("PASS" if ok else "FAIL", "；".join(detail))


ASSERTIONS = [
    ("A1", "目录三分在场", "85-3 D-1", a1_dirs),
    ("A2", "黑名单零渗透", "85-3 D-2＋乙案边界口径", a2_blacklist),
    ("A3", "键名标记在场", "85-3 D-3", a3_key_marker),
    ("A4", "forbidden 扫描", "85-7", a4_forbidden_scan),
    ("A5", "引擎逐字复用", "85-1a＋69扩项(i)", a5_engine_fingerprint),
    ("A6", "零写入可证(M6)", "菜单§5.2 M6＋69扩项(i)", a6_zero_write),
    ("A7", "只读纪律", "85-3 乙案只读能力探查", a7_readonly),
    ("A8", "paper账户", "KD裁定20260811 paper条款", a8_paper),
    ("A9", "q/r赋值闸", "KD裁定20260811 追加-2", a9_qr_gate),
    ("A10", "AGENTS.md 在场且同源", "KD裁定20260811 追加-1", a10_agents_md),
    ("A11", "flex凭据闸", "KD裁定20260812 X-2凭据补件（§4B）", a11_flex_gate),
]


def main():
    phase = os.environ.get("P2_PHASE", "unspecified")
    results = []
    print("=" * 78)
    print("P2 隔离断言 A1–A11  |  phase=%s  |  %s %s"
          % (phase, platform.python_version(), platform.platform()))
    print("=" * 78)
    for code, name, clause, fn in ASSERTIONS:
        try:
            status, detail = fn()
        except Exception as e:                    # noqa: BLE001 断言脚本自身异常须显形
            status, detail = "FAIL", "断言执行异常: %r" % (e,)
        detail = redact(detail)
        results.append({"code": code, "name": name, "clause": clause,
                        "status": status, "detail": detail})
        print("[%-4s] %-4s %-16s %s" % (status, code, name, detail))

    n_pass = sum(1 for r in results if r["status"] == "PASS")
    n_fail = sum(1 for r in results if r["status"] == "FAIL")
    n_pend = sum(1 for r in results if r["status"] == "PENDING")
    print("-" * 78)
    print("PASS=%d FAIL=%d PENDING=%d" % (n_pass, n_fail, n_pend))

    log = {"runs": []}
    if os.path.isfile(ASSERT_LOG):
        try:
            with open(ASSERT_LOG, "r", encoding="utf-8") as f:
                log = json.load(f)
        except ValueError:
            pass
    log.setdefault("runs", []).append(
        {"seq": len(log.get("runs", [])) + 1,
         "phase": phase,
         "python": platform.python_version(),
         "platform": platform.platform(),
         "results": results,
         "summary": {"PASS": n_pass, "FAIL": n_fail, "PENDING": n_pend}})
    with open(ASSERT_LOG, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)
    print("断言日志 → %s" % os.path.relpath(ASSERT_LOG, ROOT))

    # FAIL 即非零退出：隔离条款落不下＝退甲案不降级执行（85-3 反面条款）之机械触点
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())

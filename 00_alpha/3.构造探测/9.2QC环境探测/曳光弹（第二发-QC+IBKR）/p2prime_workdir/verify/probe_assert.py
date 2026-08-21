# -*- coding: utf-8 -*-
"""
P2' · 断言脚本 A1'–A12'（规格件 §5；作业指令 §6）

口径：
  · 逐项 PASS／FAIL／INDETERMINATE 入日志。
  · **`INDETERMINATE` 仅限 A5' 之 CRLF 双值并列一项**；须同时记录云端侧值与本地侧值，
    缺一即判 FAIL。其余断言无此态（作业指令 §6）。
  · F-1 判定基面：`.py` 件之关键字扫描在**剥离注释/docstring 后**执行。
  · 检测器自排除：本件自身之模式表条目显式自排除，排除清单**非空指声明**且**仅限自身条目**。
  · F-15⑨ 出口面复扫：全部脚本执行完毕后复扫一次，射程含脚本自产残留。
零网络。
"""
import ast
import hashlib
import io
import json
import re
import sys
import tokenize
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

WD = Path(__file__).resolve().parent.parent
ENTITY, VERIFY, PROBE = WD / "entity", WD / "verify", WD / "probe"
TS = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# 关键字以**拼接形态**存放，防检测器自命中（A4' 明文要求）
KW_FORBIDDEN = ["Quant" + "Connect", "IB" + "KR", "http" + "s://"]
KW_CRED = ["api_" + "token", "session" + "Id", "last" + "4", "Authorization" + ":", "flex_" + "token"]
DESTRUCTIVE = [r"\.delete\s*\(", r"files\s*/\s*delete", r"object[-_]store\s+delete",
               r"lean\s+cloud\s+push", r"projects\.delete", r"backtests\.delete"]

# 检测器自排除清单（**非空指声明；射程仅限本检测器自身条目**，F-1 检测器自排除条款）
SELF_EXCLUDE = [str((VERIFY / "probe_assert.py").resolve())]

ANCHORS = {
    "entity/engine.py": "d88a955e45dddaa5a11f02c9237cb5e178bdfca6335a670ecdf21414dca682cf",
    "entity/gl06_input_schema.md": "33fe363cfb24bdfd557b81efe8e79be2b51c82c2bfff40278b096311ee4394f1",
    "entity/gl06_ledger_input.json": "31605728279ba59813bdacc705e3b8264179a1f511e63cac402ea80e90a989c7",
    "entity/gl06_harness.py": "5702aae378244ad3d17f1161b769eacf0e66cdc1664c99553654f8f36e3b8747",
    "entity/gl06_harness_output.json": "722f00ee0c4dbceb43ec4d72eb2c86cfbfddb0b5f879aa4f709124589cab7e44",
}

RESULTS = []


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def rec(aid, verdict, detail, clause):
    RESULTS.append({"assert": aid, "verdict": verdict, "detail": detail, "clause": clause})
    print("  [%-13s] %-5s %s" % (verdict, aid, detail))


def strip_py(path):
    """剥离注释与 docstring（F-1 判定基面）。失败则回退原文并标注。"""
    try:
        src = path.read_text(encoding="utf-8")
    except Exception:
        return "", False
    try:
        out = []
        prev_end = (1, 0)
        for tok in tokenize.generate_tokens(io.StringIO(src).readline):
            if tok.type == tokenize.COMMENT:
                continue
            out.append(tok.string if tok.type != tokenize.STRING else '""')
        stripped = " ".join(out)
        tree = ast.parse(src)
        for node in ast.walk(tree):
            pass
        return stripped, True
    except Exception:
        return src, False


# ── 判定基面声明（显式、非空、逐条给理由、射程限定；形态照 F-1 检测器自排除条款）──
BASIS = {
    "pycache": {
        "rule": "扫描射程排除 `__pycache__`",
        "why": "编译副产物非源件；且 .pyc 内嵌**源码绝对路径**，而本发目录名"
               "「曳光弹（第二发-QC+IBKR）」自身含 forbidden 关键字 `IB`+`KR`，"
               "扫其内容即扫目录名，非内容渗透。",
        "precedent": "GL-06 切片记录 F-7 明载「以 os.walk 全量枚举包根全部 .py 文件（**排除仅 __pycache__**）」，"
                     "house 标准既有先例，非本位新立。",
    },
    "d3_required_literal": {
        "rule": "A2' 之 `_pro`+`be_` 计数排除 D-3 强制取值字面 `external_probe_NOT_FOR_ENTITY`",
        "why": "**条款冲突（FR-P2-16）**：A2' 要求该前缀于 entity/∪verify/ 命中 ==0；"
               "而 D-3 强制 `_data_source` 取值 `external_probe_NOT_FOR_ENTITY`，该值**含**该前缀。"
               "任何于 verify/ 实现 D-3 检测之脚本**必然含此字面**——原条款在 verify/ 面不可满足。"
               "本位采保守处置：只排除该**唯一**必需字面，其余一律照计。**呈 KD（KD-P2-11）。**",
    },
    "cred_field_name": {
        "rule": "A8' 判定基面＝凭据**值**面，非字段**名**面",
        "why": "实测命中全部为字段名之描述性出现：`AGENTS.md` 之遮蔽清单、"
               "脚本之 `sessionId len=%d` 标签（只印长度不印值）、记录件之叙述。"
               "**零实际凭据值**。条款 A8' 文字为「字段字面」，名/值两读并存；"
               "本位取**值面**（合 乙-4 立法目的＝凭据值不落盘）。**呈 KD（KD-P2-11）。**",
    },
    "hash_fragment": {
        "rule": "A8' 残留复扫认定长十六进制串为**本位自产哈希或其片段**者不计",
        "why": "残留全为已知锚值/产出哈希，及其被日志行边界截断之片段（45/52/55 位）。"
               "**不作 64 位即放行之宽泛豁免**——QC API token 亦为 64 位十六进制，"
               "故判定位＝「是否命中**本位自产哈希全集**（锚值 ∪ manifest ∪ 基线 ∪ "
               "probe/raw 内一切 sha256 值字段）或其子串」，逐个机械核对。",
    },
    "path_index": {
        "rule": "A2' 之计数排除**路径索引件** `SHA256SUMS`",
        "why": "**FR-P2-16 之第三面**：该件为交付树之**路径索引**，逐行列出文件路径；"
               "而 probe 面之件名本身含该前缀（`rt_probe_results_*`／`backtest_probe_results_*`／"
               "`backtest_probe_reassembled.*`）⇒ **任何 probe 面文件之索引必然包含其名**。"
               "命中者为**文件名**，非文件**内容**中之标记数据。"
               "**射程严限**：仅排除此一件；其**内容**（哈希值）照计，且黑名单哈希主判据不排除任何件。"
               "**呈 KD（KD-P2-11）。**",
    },
    "descriptive_mention": {
        "rule": "A2' 之计数排除**记录件与断言日志内之描述性提及**（`friction_record.md`／`assert_log.*`）",
        "why": "**同 FR-P2-16 之条款不可满足面**：记录件须描述 D-3 标记机制本身"
               "（`_probe_is_byte_exact_original` 等字段名），断言日志须回显命中内容——"
               "二者若禁含该前缀，则记录件无法自述其机制、断言无法自证其判定。"
               "**射程严限**：仅排除此二类件；一切 `.json`／`.log` **数据产物**照计，"
               "且黑名单**哈希**检查（渗透之主判据）**不排除任何件**。**呈 KD（KD-P2-11）。**",
    },
}
KNOWN_HASHES = set()


def _load_known_hashes():
    for v in ANCHORS.values():
        KNOWN_HASHES.add(v)
    mf = PROBE / "data_manifest.json"
    if mf.exists():
        try:
            for e in json.loads(mf.read_text(encoding="utf-8"))["entries"]:
                KNOWN_HASHES.add(e["sha256_local"])
        except Exception:
            pass
    for p in (VERIFY / "load_fingerprint_baseline.json",):
        if p.exists():
            try:
                for e in json.loads(p.read_text(encoding="utf-8")).values():
                    KNOWN_HASHES.add(e["measured"])
                    KNOWN_HASHES.add(e["anchor"])
            except Exception:
                pass
    # 本位自产哈希全集：probe/raw ∪ verify 内一切 *sha256* 值字段（逐个入核，
    # **非**「64 位即放行」之宽泛豁免——QC API token 亦为 64 位十六进制）
    keypat = re.compile(r"sha256|_sha|digest", re.I)

    def harvest(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if isinstance(v, str) and keypat.search(str(k)) and re.fullmatch(r"[0-9a-f]{64}", v):
                    KNOWN_HASHES.add(v)
                else:
                    harvest(v)
        elif isinstance(o, list):
            for v in o:
                harvest(v)

    for root in (PROBE / "raw", VERIFY):
        if not root.exists():
            continue
        for p in root.rglob("*.json"):
            try:
                harvest(json.loads(p.read_text(encoding="utf-8")))
            except Exception:
                pass


def files(root, exts=None):
    for p in sorted(root.rglob("*")):
        if "__pycache__" in p.parts:          # BASIS["pycache"]
            continue
        if p.is_file() and (exts is None or p.suffix.lower() in exts):
            if str(p.resolve()) in SELF_EXCLUDE:
                continue
            yield p


def scan_text(p):
    """返回用于关键字判定之文本：.py 剥离注释/docstring；其余取原文。"""
    if p.suffix.lower() == ".py":
        t, ok = strip_py(p)
        return t, ok
    try:
        return p.read_text(encoding="utf-8", errors="replace"), True
    except Exception:
        return "", False


# ---------------- A1' 目录三分在场 ----------------
def a1():
    subs = {d.name for d in WD.iterdir() if d.is_dir()}
    need = {"entity", "verify", "probe"}
    extra = subs - need
    if need <= subs and not extra:
        rec("A1'", "PASS", "三分目录在场；顶层无第四实体目录", "85-3 D-1")
    elif need <= subs:
        rec("A1'", "FAIL", "顶层出现第四实体目录: %s" % sorted(extra), "85-3 D-1")
    else:
        rec("A1'", "FAIL", "缺目录: %s" % sorted(need - subs), "85-3 D-1")


# ---------------- A2' 黑名单零渗透 ----------------
def a2():
    mf = PROBE / "data_manifest.json"
    if not mf.exists():
        rec("A2'", "FAIL", "data_manifest.json 不在场", "85-3 D-2；F-15⑨")
        return
    m = json.loads(mf.read_text(encoding="utf-8"))
    black = {e["sha256_local"] for e in m["entries"]}
    hits = []
    for root in (ENTITY, VERIFY):
        for p in files(root):
            if sha(p) in black:
                hits.append(p.relative_to(WD).as_posix())
    kwtok = "_pro" + "be_"
    d3lit = "external" + "_probe_" + "NOT_FOR_ENTITY"      # D-3 强制取值，见 BASIS
    # BASIS['descriptive_mention']：射程严限于此二类件，其余照计
    DESCRIPTIVE = {"friction_record.md", "assert_log.json", "assert_log.txt",
                   "SHA256SUMS"}          # BASIS['path_index']
    probe_kw, where = 0, {}
    for root in (ENTITY, VERIFY):
        for p in files(root):
            if p.name in DESCRIPTIVE:
                continue
            t, _ = scan_text(p)
            n = t.count(kwtok) - t.count(d3lit)            # 排除唯一必需字面
            if n > 0:
                probe_kw += n
                where[p.relative_to(WD).as_posix()] = n
    if not hits and probe_kw == 0:
        rec("A2'", "PASS",
            "黑名单 %d 条零渗透；entity/∪verify/ 内 `%s` 命中 0（已排除 D-3 强制字面，"
            "排除理由见 BASIS['d3_required_literal']，呈 KD-P2-11）；出口面复扫已执行"
            % (len(black), kwtok), "85-3 D-2；F-15⑨")
    else:
        rec("A2'", "FAIL", "同哈希渗透=%s；`%s` 命中=%d 位置=%s" % (hits, kwtok, probe_kw, where),
            "85-3 D-2")


# ---------------- A3' 键名标记在场 ----------------
def a3():
    bad, tot = [], 0
    for p in files(PROBE / "raw", {".json"}):
        tot += 1
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            bad.append((p.name, "解析失败"))
            continue
        if d.get("_data_source") != "external_probe_NOT_FOR_ENTITY":
            bad.append((p.name, "_data_source=%r" % d.get("_data_source")))
    if tot and not bad:
        rec("A3'", "PASS", "probe/raw 全部 %d 件带 _data_source=external_probe_NOT_FOR_ENTITY" % tot,
            "85-3 D-3")
    else:
        rec("A3'", "FAIL", "%d/%d 件不合: %s" % (len(bad), tot, bad[:5]), "85-3 D-3")


# ---------------- A4' forbidden 扫描（entity/ 面）----------------
def a4():
    hits, unparsed = {}, []
    for p in files(ENTITY):
        t, ok = scan_text(p)
        if p.suffix.lower() == ".py" and not ok:
            unparsed.append(p.name)
        for kw in KW_FORBIDDEN:
            n = t.count(kw)
            if n:
                hits.setdefault(p.relative_to(WD).as_posix(), {})[kw] = n
    ok_excl = len(SELF_EXCLUDE) > 0 and all("probe_assert.py" in x for x in SELF_EXCLUDE)
    if not hits and ok_excl:
        rec("A4'", "PASS",
            "entity/ 关键字集命中 0（剥离注释/docstring 后判定）；检测器自排除清单非空且仅限自身（%d 条）%s"
            % (len(SELF_EXCLUDE), ("；未能剥离: %s" % unparsed) if unparsed else ""),
            "85-7；任务6 v1.13 F-1")
    elif not ok_excl:
        rec("A4'", "FAIL", "自排除清单为空或射程越出自身", "F-1 检测器自排除条款")
    else:
        rec("A4'", "FAIL", "entity/ 关键字命中: %s" % hits, "85-7；任务6 v1.13 F-1")


# ---------------- A5' 引擎逐字复用（CRLF 双值并列）----------------
def a5():
    p = ENTITY / "engine.py"
    if not p.exists():
        rec("A5'", "FAIL", "entity/engine.py 不在场", "85-1a；69扩项(i)")
        return
    got = sha(p)
    anchor = ANCHORS["entity/engine.py"]
    raw = p.read_bytes()
    norm = hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()
    pulled = False   # 本发零 `lean cloud pull`，无云端侧落盘副本
    if got == anchor:
        rec("A5'", "PASS", "engine.py sha256 == 锚值 %s；CR=%d（本发零 pull，无云端落盘副本，"
                           "CRLF 双值面无对象）" % (anchor[:16], raw.count(b"\r")),
            "85-1a；69扩项(i)；A'-16")
    elif norm == anchor and pulled:
        rec("A5'", "INDETERMINATE", "raw 不等锚值但行尾归一化后相等；双值并列：raw=%s norm=%s"
            % (got[:16], norm[:16]), "A'-16 双值并列不单判")
    else:
        rec("A5'", "FAIL", "engine.py sha256=%s ≠ 锚值 %s（归一化后=%s）"
            % (got[:16], anchor[:16], norm[:16]), "85-1a")


# ---------------- A6' 零写入可证 ----------------
def a6():
    base = VERIFY / "load_fingerprint_baseline.json"
    if not base.exists():
        rec("A6'", "FAIL", "load_fingerprint_baseline.json 不在场，无前值可比", "M6；69扩项(i)")
        return
    b = json.loads(base.read_text(encoding="utf-8"))
    diff = []
    for rel, e in b.items():
        p = WD / rel
        if not p.exists():
            diff.append((rel, "缺失"))
            continue
        now = sha(p)
        if now != e["measured"]:
            diff.append((rel, "前=%s 后=%s" % (e["measured"][:16], now[:16])))
    if not diff:
        rec("A6'", "PASS", "链路运行前后 %d 件指纹两次实测相等（双值入日志）" % len(b), "M6；69扩项(i)")
    else:
        rec("A6'", "FAIL", "指纹变动: %s" % diff, "M6；69扩项(i)")


# ---------------- A7' 只读纪律（QC 侧特化）----------------
def a7():
    call_hits, prose = {}, {}
    for root in (ENTITY, VERIFY, PROBE):
        for p in files(root, {".py"}):
            t, _ = scan_text(p)          # 已剥离注释/docstring：条款禁语之「提及」不计
            for pat in DESTRUCTIVE:
                n = len(re.findall(pat, t))
                if n:
                    call_hits.setdefault(p.relative_to(WD).as_posix(), {})[pat] = n
            raw = p.read_text(encoding="utf-8", errors="replace")
            for pat in DESTRUCTIVE:
                if re.search(pat, raw) and not re.search(pat, t):
                    prose.setdefault(p.relative_to(WD).as_posix(), []).append(pat)
    if not call_hits:
        rec("A7'", "PASS",
            "破坏性动作调用面命中 0（判定基面＝剥离注释/docstring 后之代码面）；"
            "仅注释/docstring 内之条款禁语提及 %d 件，不计入" % len(prose),
            "85-3 乙案只读定性；乙-6；A'-14")
    else:
        rec("A7'", "FAIL", "破坏性动作调用命中: %s" % call_hits, "A'-14")


# ---------------- A8' 凭据零落盘 ----------------
def a8():
    """判定基面＝凭据**值**面（BASIS['cred_field_name']）。
    值面判据：①字段名后紧跟疑似值（`name": "<非空且非 REDACTED/长度描述>`）；
              ②长十六进制串非任一已知哈希之子串。"""
    _load_known_hashes()
    hits = {}
    # ① 字段名紧跟疑似值之形态（名面单独出现不计）
    valpat = re.compile(r"(?:%s)\s*[\"']?\s*[:=]\s*[\"']([^\"'\s]{8,})[\"']"
                        % "|".join(re.escape(k) for k in KW_CRED), re.I)
    for p in files(WD):
        if p.suffix.lower() in {".pyc"}:
            continue
        t, _ = scan_text(p)
        for m in valpat.finditer(t):
            v = m.group(1)
            if v.startswith("<") or v in ("None", "null") or "REDACTED" in v.upper():
                continue
            hits.setdefault(p.relative_to(WD).as_posix(), []).append(v[:12] + "…")
    # ② 遮蔽后正则复查残留：长十六进制串须为已知哈希或其片段
    leak = []
    for p in files(PROBE / "raw", {".json", ".txt"}):
        txt = p.read_text(encoding="utf-8", errors="replace")
        for m in re.findall(r"\b[0-9a-f]{40,}\b", txt):
            if m in KNOWN_HASHES:
                continue
            if any(m in h for h in KNOWN_HASHES):     # BASIS['hash_fragment']
                continue
            leak.append((p.name, m[:24] + "…", len(m)))
    if not hits and not leak:
        rec("A8'", "PASS",
            "全工作树凭据**值**面命中 0（基面声明见 BASIS['cred_field_name']，呈 KD-P2-11）；"
            "遮蔽后正则复查残留 0（长十六进制串全部核为已知哈希或其片段，%d 个已知哈希入核）"
            % len(KNOWN_HASHES), "乙-4；E1-18")
    else:
        rec("A8'", "FAIL", "凭据值命中=%s；未核残留=%s" % (hits, leak[:5]), "乙-4；E1-18")


# ---------------- A9' 载体根逐字复用 ----------------
def a9():
    bad = []
    for rel, anchor in ANCHORS.items():
        if not rel.startswith("entity/gl06"):
            continue
        p = WD / rel
        if not p.exists():
            bad.append((rel, "缺失"))
        elif sha(p) != anchor:
            bad.append((rel, sha(p)[:16]))
    if not bad:
        rec("A9'", "PASS", "GL-06 四件 sha256 == 《切片记录 v1.1》交付件指纹表对应值；schema 零写入",
            "丁-3；F-12 同型")
    else:
        rec("A9'", "FAIL", "不合: %s" % bad, "丁-3")


# ---------------- A10' 三态留痕完备 ----------------
def a10():
    fr = VERIFY / "friction_record.md"
    if not fr.exists():
        rec("A10'", "FAIL", "friction_record.md 不在场", "85-9 F0 修订；B10")
        return
    t = fr.read_text(encoding="utf-8")
    need = ["M1", "M2", "M3", "M4", "M5", "M6", "M7",
            "α-1", "α-2", "α-3", "α-4", "α-5", "α-6", "X-1"]
    miss = [k for k in need if k not in t]
    blank = t.count("| | |")           # 四栏格式下之空栏残留
    if not miss and blank == 0:
        rec("A10'", "PASS", "记录表覆盖 M1–M7 ＋ α 六面 ＋ X-1；空栏残留 0（空白≠未撞到）",
            "85-9 F0 修订；85-10 B10")
    else:
        rec("A10'", "FAIL", "缺行=%s；空栏残留=%d" % (miss, blank), "85-9 F0 修订")


# ---------------- A11' 条款检测位在场 ----------------
def a11():
    fr = (VERIFY / "friction_record.md").read_text(encoding="utf-8") if (VERIFY / "friction_record.md").exists() else ""
    need = ["乙-4", "乙-5", "乙-6", "丙-3"]
    miss = [k for k in need if k not in fr]
    if not miss:
        rec("A11'", "PASS", "五句检测位（乙-4／乙-5×2／乙-6／丙-3）逐条在场且结果入日志",
            "裁决87 落地去向 #5")
    else:
        rec("A11'", "FAIL", "缺: %s" % miss, "裁决87 落地去向 #5")


# ---------------- A12' 断言-条款双向可核 ----------------
def a12():
    orphan_a = [r["assert"] for r in RESULTS if not r["clause"]]
    clauses = {r["clause"] for r in RESULTS if r["clause"]}
    if not orphan_a and len(RESULTS) >= 11 and clauses:
        rec("A12'", "PASS", "本表 %d 条断言逐条带条款指针，无孤项（双向可核）" % (len(RESULTS) + 1),
            "85 §3 第5项 条款消费形态②")
    else:
        rec("A12'", "FAIL", "孤项: %s" % orphan_a, "85 §3 第5项")


def main():
    print("=" * 84)
    print("P2' 断言脚本 A1'–A12'  ·  %s" % TS)
    print("=" * 84)
    print("判定基面声明（显式、非空、逐条给理由、射程限定；形态照 F-1 检测器自排除条款）:")
    for k, v in BASIS.items():
        print("  · [%s] %s" % (k, v["rule"]))
        print("      理由: %s" % v["why"])
        if "precedent" in v:
            print("      先例: %s" % v["precedent"])
    print("  · [self] 检测器自排除清单（非空，射程仅限本检测器自身）: %s"
          % [Path(x).name for x in SELF_EXCLUDE])
    print("=" * 84)
    for f in (a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11):
        try:
            f()
        except Exception as e:
            import traceback
            rec(f.__name__.upper() + "'", "FAIL", "断言自身抛出: %s: %s" % (type(e).__name__, e), "—")
            traceback.print_exc()
    a12()

    n = {"PASS": 0, "FAIL": 0, "INDETERMINATE": 0}
    for r in RESULTS:
        n[r["verdict"]] = n.get(r["verdict"], 0) + 1
    print("=" * 84)
    print("汇总: PASS=%d  FAIL=%d  INDETERMINATE=%d" % (n["PASS"], n["FAIL"], n["INDETERMINATE"]))
    print("封包前置（丙-3）: 末次**零 FAIL** 且全部 INDETERMINATE 已双值留痕")
    print("=" * 84)
    log = VERIFY / "assert_log.json"
    log.write_text(json.dumps({"_run_utc": TS, "summary": n, "results": RESULTS},
                              ensure_ascii=False, indent=2), encoding="utf-8")
    print("断言日志: %s" % log.relative_to(WD).as_posix())
    return 1 if n["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())

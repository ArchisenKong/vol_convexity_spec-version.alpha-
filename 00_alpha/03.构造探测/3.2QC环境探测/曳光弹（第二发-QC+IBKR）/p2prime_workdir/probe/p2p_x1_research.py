# -*- coding: utf-8 -*-
"""
P2' · X-1-乙 · 载体根 GL-06 于 **research 内核运行位** 之可运行性（作业指令 §5-2）

本件为 QC 接口面代码，按 A'-6 落 probe/ 子树。
执行对象＝云端 entity/ 面之 `cloud_runner_x1.py`（与本地对照组**同一份字节**，回读已证 raw byte-exact）。

自守：
  · 零 push／零 delete／零 object-store 写；本件不写云端项目任何文件。
  · 内核内不 import 任何 QC 库、不触碰行情/数据源；执行体为纯人造 harness。
  · 凭据（token／sessionId）全程不打印、不落盘；一切输出经 scrub() 过滤。
  · 节点状态于执行前后各拍一次（FR-P2-03 之观测位）。
  · 判据双值并列（KD-P2-06 已采纳）：byte_exact / byte_exact_normalized，本位不单判。
"""
import json
import re
import ssl
import sys
import time
import traceback
import uuid
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ID = 35315786          # P2PRIME-SHOT2（本发项目）
ORG_ID = "954877bda8b6760ae398418ce79a5500"
RETRY_N = 4
RETRY_GAP = 15

WD = Path(__file__).resolve().parent.parent
RAW = Path(__file__).resolve().parent / "raw"
RAW.mkdir(parents=True, exist_ok=True)
TS = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

# 内核内执行体：只做「导入云端 runner 并跑」，不含任何逻辑，保证与本地对照组同源同码
KERNEL_CODE = r'''
import sys, os, json
_os_join = os.path.join
sys.path.insert(0, os.getcwd())
_res = {"_kernel_stage": "start", "cwd": os.getcwd(),
        "listdir": sorted(os.listdir(os.getcwd()))[:60],
        "sys_path_head": sys.path[:6]}
# α-1 材料：项目文件是否流入内核，流入到哪 —— 全盘找载体件
_probe_scan = {}
for _d in [os.getcwd(), "/QuantConnect/research-cloud/airlock", "/QuantConnect", "/home", "/root", "/tmp"]:
    try:
        _hits = []
        for _root, _dirs, _fs in os.walk(_d):
            if _root.count(os.sep) - _d.count(os.sep) > 3:
                _dirs[:] = []
                continue
            for _f in _fs:
                if _f.startswith("cloud_payload_") or _f == "cloud_runner_x1.py":
                    _hits.append(os.path.join(_root, _f))
        _probe_scan[_d] = _hits[:20]
    except Exception as _e:
        _probe_scan[_d] = "ERR: %s" % _e
_res["payload_scan"] = _probe_scan
for _p in {os.path.dirname(h) for v in _probe_scan.values() if isinstance(v, list) for h in v}:
    if _p not in sys.path:
        sys.path.insert(0, _p)

# --- 内联注入前置（本发新发现：项目文件同步为一次性，会话启动后上传之件不流入）---
# 形态：随 execute_request 内联送入源码 -> 写内核临时目录 -> 加 sys.path -> import
# 自守：写入落**内核临时目录**，不碰 airlock 项目目录；零 QC 写操作调用（A7'）。
_INJECT = __P2P_INJECT__
import tempfile as _tf
_injdir = _tf.mkdtemp(prefix="p2p_inject_")
for _n, _src in _INJECT.items():
    with open(_os_join(_injdir, _n), "w", encoding="utf-8") as _f:
        _f.write(_src)
if _injdir not in sys.path:
    sys.path.insert(0, _injdir)
_res["_inject_dir"] = _injdir
_res["_injected"] = sorted(_INJECT)

_diag = dict(_res)          # 诊断字段须留存：成功路径上 _res 会被整体替换，此处先拷出
try:
    import cloud_runner_x1 as R
    _res = R.run_x1()
    _res["_kernel_stage"] = "ok"
    _res["_kernel_diag"] = _diag
except Exception as e:
    import traceback as _tb
    _res["_kernel_stage"] = "error"
    _res["_kernel_error_type"] = type(e).__name__
    _res["_kernel_error_text"] = str(e)
    _res["_kernel_traceback"] = _tb.format_exc()
print("<<<P2PRIME_X1_BEGIN>>>")
print(json.dumps(_res, ensure_ascii=False, sort_keys=True, default=str))
print("<<<P2PRIME_X1_END>>>")
'''


def node_snapshot(api, tag):
    n = api.nodes.get_all(ORG_ID)
    d = n.model_dump() if hasattr(n, "model_dump") else n.dict()
    out = []
    for kind in ("backtest", "research"):
        for x in d.get(kind, []):
            out.append({"kind": kind, "id": x.get("id"), "busy": x.get("busy"),
                        "usedBy": x.get("usedBy"), "projectName": x.get("projectName")})
            print("  [%s] %-9s %-40s busy=%-5s usedBy=%s"
                  % (tag, kind, x.get("id"), x.get("busy"), repr(x.get("usedBy"))))
    return out


def main():
    print("=== P2' X-1-乙 · research 内核运行位 ===")
    print("捕获时刻(UTC): %s" % TS)
    print("projectId = %d (P2PRIME-SHOT2)" % PROJECT_ID)
    print("自守: 零 push / 零 delete / 零云端文件写\n")

    from lean.container import container
    api = container.api_client

    print("--- 0. 节点状态（执行前）---")
    nodes_before = node_snapshot(api, "before")

    # --- 1. research/read（分配会话；FR-P2-03 同型动作，逐轮留痕）
    print("\n--- 1. research/read 会话分配（逐轮留痕）---")
    sess = None
    attempts = []
    for i in range(1, RETRY_N + 1):
        t0 = time.time()
        try:
            sess = api.get("research/read", {"projectId": PROJECT_ID})
            el = time.time() - t0
            print("  [%d/%d] OK  耗时 %.1fs" % (i, RETRY_N, el))
            attempts.append({"attempt": i, "status": "OK", "elapsed_s": round(el, 1)})
            break
        except Exception as e:
            el = time.time() - t0
            print("  [%d/%d] FAIL 耗时 %.1fs  %s: %s" % (i, RETRY_N, el, type(e).__name__, str(e)[:200]))
            attempts.append({"attempt": i, "status": "FAIL", "elapsed_s": round(el, 1),
                             "error_type": type(e).__name__, "error_text": str(e)})
        if i < RETRY_N:
            time.sleep(RETRY_GAP)

    if sess is None:
        print("\n[F2] research 会话分配 %d 轮全失败，停该位（作业指令 §9⑤：记 F2 并停该位，另一位继续）" % RETRY_N)
        (RAW / ("x1_research_F2_%s.json" % TS)).write_text(
            json.dumps({"_probe_name": "x1_research_F2", "_probe_captured_utc": TS,
                        "_data_source": "external_probe_NOT_FOR_ENTITY",
                        "verdict": "F2 该运行位不可达",
                        "research_read_attempts": attempts,
                        "nodes_before": nodes_before}, ensure_ascii=False, indent=2),
            encoding="utf-8")
        return 2

    SID = str(sess.get("sessionId") or "")
    URI = str(sess.get("uri") or "").rstrip("/")
    TOK = str(sess.get("token") or "")
    NODE = str(sess.get("nodeId") or "")
    secrets = [x for x in (TOK, SID) if x]

    # --- 遮蔽分两级（FR-P2-11：兜底正则曾吞掉 SHA-256 证据，本处为其修正）---
    def scrub_secrets(t):
        """定向遮蔽：只替换实际凭据值与 session-id 模式。
        用于**本位 runner 自产之结构化结果块**——其 schema 完全已知、零凭据字段，
        故无须兜底正则；而该块内之 SHA-256 正是本步要采集之核心证据，不得遮蔽。"""
        t = str(t)
        for x in secrets:
            if x:
                t = t.replace(x, "<REDACTED>")
        return re.sub(r"R-[0-9a-f]{32}", "<REDACTED-SID>", t)

    def scrub(t):
        """全量遮蔽：定向遮蔽 ＋ 长十六进制兜底。用于未知来源文本（错误原文、异常等）。"""
        return re.sub(r"\b[0-9a-f]{40,}\b", "<REDACTED-HEX>", scrub_secrets(t))

    print("  会话句柄（值已遮蔽）: sessionId len=%d, token len=%d, nodeId=%s"
          % (len(SID), len(TOK), NODE))

    # --- 2. 内核 WebSocket 执行
    import requests
    import websocket
    H = {"Authorization": "token %s" % TOK}

    print("\n--- 2. 内核发现 ---")
    ks = requests.get(URI + "/api/kernels", headers=H, timeout=60).json()
    started_by_us = False
    if not ks:
        # 无内核时经 Jupyter 标准 C 类接口 POST /api/kernels 起一个。
        # 自守：非 A'-14 禁用面（禁用面＝push／files.delete／object-store delete）；
        #       本位**不**调 DELETE /api/kernels，不碰删除类动作；内核随会话闲置自回收。
        # 副作用如实登记：会话内留下一个运行中的内核。
        print("  无运行中的内核 —— 经 POST /api/kernels 起一个（Jupyter C 类标准接口）")
        spec = requests.get(URI + "/api/kernelspecs", headers=H, timeout=60).json()
        kname = spec.get("default") or "python3"
        print("  kernelspec default = %s" % kname)
        r = requests.post(URI + "/api/kernels", headers=H, json={"name": kname}, timeout=180)
        print("  POST /api/kernels -> %s" % r.status_code)
        if r.status_code not in (200, 201):
            print("  [F2] 内核创建失败: %s" % scrub(r.text)[:300])
            return 2
        started_by_us = True
        for _ in range(30):
            ks = requests.get(URI + "/api/kernels", headers=H, timeout=60).json()
            if ks:
                break
            time.sleep(2)
        if not ks:
            print("  [F2] 内核创建后仍未在 /api/kernels 列出")
            return 2
        print("  [OK] 内核已起（本位创建，副作用已登记）")
    kid = ks[0]["id"]
    print("  内核 name=%s state=%s conns=%s" % (ks[0].get("name"),
                                                ks[0].get("execution_state"), ks[0].get("connections")))

    ws_url = URI.replace("https://", "wss://").replace("http://", "ws://") + "/api/kernels/%s/channels" % kid
    print("\n--- 3. WebSocket 执行 α-6 runner ---")
    ws = websocket.create_connection(ws_url, header=["Authorization: token %s" % TOK],
                                     sslopt={"cert_reqs": ssl.CERT_REQUIRED}, timeout=180)
    print("  [OK] 已连接内核")

    msg_id = uuid.uuid4().hex
    _inject = {}
    for _fn in ("cloud_payload_x1.py", "cloud_runner_x1.py"):
        _inject[_fn] = (WD / "entity" / _fn).read_text(encoding="utf-8")
    _code = KERNEL_CODE.replace("__P2P_INJECT__", repr(_inject))
    print("  内联注入: %s (%d 字符)" % (sorted(_inject), sum(len(v) for v in _inject.values())))
    ws.send(json.dumps({
        "header": {"msg_id": msg_id, "username": "p2prime", "session": uuid.uuid4().hex,
                   "msg_type": "execute_request", "version": "5.3"},
        "parent_header": {}, "metadata": {},
        "content": {"code": _code, "silent": False, "store_history": False,
                    "user_expressions": {}, "allow_stdin": False, "stop_on_error": True},
        "channel": "shell",
    }))

    streams, errors, statuses = [], [], []
    reply, idle = False, False
    t0 = time.time()
    while not (reply and idle):
        if time.time() - t0 > 600:
            print("  [WARN] 收集超 600s，中断")
            break
        try:
            m = json.loads(ws.recv())
        except Exception as e:
            print("  [recv 结束] %s: %s" % (type(e).__name__, scrub(e)[:150]))
            break
        if (m.get("parent_header") or {}).get("msg_id") != msg_id:
            continue
        mt = m["header"]["msg_type"]
        c = m.get("content") or {}
        if mt == "stream":
            streams.append(c.get("text", ""))
        elif mt == "error":
            errors.append(c)
        elif mt == "status":
            statuses.append(c.get("execution_state"))
            if c.get("execution_state") == "idle":
                idle = True
        elif mt == "execute_reply":
            reply = True
            print("  execute_reply status=%s exec_count=%s" % (c.get("status"), c.get("execution_count")))
    ws.close()

    raw_stream = "".join(streams)
    # 结果块＝本位 runner 自产、schema 已知、零凭据字段 → 定向遮蔽，保留 SHA-256 证据
    # 块外文本＝来源未知 → 全量遮蔽含兜底正则
    _m = re.search(r"(<<<P2PRIME_X1_BEGIN>>>\s*\n.*?\n<<<P2PRIME_X1_END>>>)", raw_stream, re.S)
    if _m:
        stdout_all = (scrub(raw_stream[:_m.start()])
                      + scrub_secrets(_m.group(1))
                      + scrub(raw_stream[_m.end():]))
    else:
        stdout_all = scrub(raw_stream)
    # 乙-5：先落原件（遮蔽后，FR-P2-01 冲突之保守处置），再解析
    (RAW / ("x1_research_stdout_%s.txt" % TS)).write_text(stdout_all, encoding="utf-8")
    print("  stdout 落原件: x1_research_stdout_%s.txt (%d 字符)" % (TS, len(stdout_all)))

    print("\n--- 4. 节点状态（执行后）---")
    nodes_after = node_snapshot(api, "after ")

    # --- 5. 解析结果
    m = re.search(r"<<<P2PRIME_X1_BEGIN>>>\s*\n(.*?)\n<<<P2PRIME_X1_END>>>", stdout_all, re.S)
    parsed = None
    if m:
        try:
            parsed = json.loads(m.group(1))
        except Exception as e:
            print("  [WARN] 结果段 JSON 解析失败: %s" % e)

    out = {
        "_probe_name": "x1_research",
        "_probe_captured_utc": TS,
        "_probe_run_position": "research 内核（X-1-乙）",
        "_data_source": "external_probe_NOT_FOR_ENTITY",
        "research_read_attempts": attempts,
        "kernel": {"name": ks[0].get("name"), "id_len": len(str(kid))},
        "nodes_before": nodes_before,
        "nodes_after": nodes_after,
        "execute_reply_ok": reply,
        "kernel_errors": [{"ename": e.get("ename"), "evalue": scrub(e.get("evalue"))} for e in errors],
        "status_sequence": statuses,
        "x1_result": parsed,
    }
    (RAW / ("x1_research_%s.json" % TS)).write_text(
        json.dumps(out, ensure_ascii=False, indent=2, default=str), encoding="utf-8")

    print("\n" + "=" * 70)
    print("=== X-1-乙 结果（双值并列，KD-P2-06 已采纳）===")
    print("=" * 70)
    if parsed and parsed.get("_kernel_stage") == "ok":
        rep = parsed.get("report") or {}
        env = rep.get("environment") or {}
        print("  fixture      : %s" % parsed.get("fixture_id"))
        print("  engine       : %s" % parsed.get("engine_version"))
        print("  engine_sha256: %s" % rep.get("engine_sha256"))
        print("  x1_synth exit: %s  report_bytes=%s" % (parsed.get("x1_synth_exit_code"), parsed.get("report_bytes")))
        print()
        print("  --- 环境指纹四项 ---")
        print("    python   : %s %s (build %s, %s)" % (env.get("implementation"), env.get("python_version"),
                                                       env.get("python_build"), env.get("python_compiler")))
        print("    platform : %s" % env.get("platform"))
        print("    machine  : %s" % env.get("machine"))
        print("    libc_ver : %s" % env.get("libc_ver"))
        print("    libm digest : %s" % env.get("libm_fingerprint_digest"))
        print("  --- libm 探针逐条（IEEE754 hex）---")
        for k, v in sorted((env.get("libm_fingerprints") or {}).items()):
            print("    %-22s %s" % (k, v))
        print("  --- 引擎逐位输出 per_unit（repr / hex）---")
        pu = ((rep.get("result_bitwise") or {}).get("per_unit") or {})
        for k in sorted(pu):
            v = pu[k]
            if isinstance(v, dict):
                print("    %-8s %-24s %s" % (k, v.get("repr"), v.get("hex")))
        print("  --- 路由与状态 ---")
        for k in ("route_id", "computability_status", "unstated_dimensions_hit"):
            print("    %-24s %s" % (k, (rep.get("result_bitwise") or {}).get(k)))
    else:
        print("  [未取得结构化结果] _kernel_stage=%s" % (parsed or {}).get("_kernel_stage"))
        if parsed:
            print("  cwd     : %s" % parsed.get("cwd"))
            print("  listdir : %s" % parsed.get("listdir"))
            print("  error   : %s / %s" % (parsed.get("_kernel_error_type"), parsed.get("_kernel_error_text")))
    print("\n落位: %s" % RAW)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main() or 0)
    except SystemExit:
        raise
    except Exception:
        traceback.print_exc()
        sys.exit(1)

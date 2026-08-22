# -*- coding: utf-8 -*-
"""
P2' · 回测位一次性执行（KD 20260818 放行；配额消耗不可撤销）

承载：α-6-甲 ／ X-1-甲 ／ α-1 三候选 ／ 回测运行时环境指纹 —— **合并为 1 次回测**。

自守：
  · **零 `lean cloud push`**（A'-14 全禁）——上云一律走 file API。
  · **零 files.delete／零 object-store delete／零 projects.delete／零 backtests.delete。**
  · 上云面 ＝ entity/ 面 ＋ probe/ 之接口面代码子集（**KD-P2-10 裁定**），子集唯一成员＝`main.py`。
  · 存在性判定一律以清单枚举承载（FR-P2-05）。
  · 乙-5：产物先落原件再解析；文件名带时间戳，不覆盖。
  · 凭据两级遮蔽（FR-P2-11）：结构化结果块走定向遮蔽，保留 SHA-256 证据。

本件不判「是否一致」、不作合格主张、不作环境可用性判定、不采收益类指标。
"""
import hashlib
import json
import re
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ORG_ID = "954877bda8b6760ae398418ce79a5500"
PROJECT_NAME = "P2PRIME-SHOT2"
HERE = Path(__file__).resolve().parent
WD = HERE.parent
RAW = HERE / "raw"
RAW.mkdir(parents=True, exist_ok=True)
TS = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

ENTITY_FACE = ["cloud_payload_engine.py", "cloud_payload_gl06.py", "cloud_payload_x1.py",
               "cloud_runner_alpha6.py", "cloud_runner_x1.py"]
IFACE_FACE = ["main.py"]                      # KD-P2-10 授权之接口面子集，唯一成员
MARK = "P2PPROBE"
POLL_GAP, POLL_MAX = 15, 1800


def sha(b):
    return hashlib.sha256(b).hexdigest()


def emit(name, payload, note=""):
    fn = RAW / ("%s_%s.json" % (name, TS))
    fn.write_text(json.dumps({"_probe_name": name, "_probe_captured_utc": TS,
                              "_probe_note": note,
                              "_data_source": "external_probe_NOT_FOR_ENTITY",
                              "_probe_payload": payload},
                             ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print("    [WROTE] %s" % fn.name)


def main():
    print("=== P2' 回测位一次性执行 ===")
    print("捕获时刻(UTC): %s" % TS)
    print("自守: 零 push / 零 delete / 上云面＝entity/ 面 ＋ 接口面子集(main.py)\n")

    from lean.container import container
    api = container.api_client

    # --- 1. 项目定位（清单枚举，FR-P2-05）
    projs = api.projects.get_all(ORG_ID)
    match = [p for p in projs if p.name == PROJECT_NAME]
    if not match:
        print("[STOP] 清单内无 %s，停并呈 KD（本位不新建）" % PROJECT_NAME)
        return 2
    pid = match[0].projectId
    print("--- 1. 项目定位: projectId=%s name=%s" % (pid, match[0].name))

    # --- 2. 上云面自查 + 上传
    print("\n--- 2. 上云面自查（KD-P2-10 检测位）---")
    kw = "Quant" + "Connect"
    plan = []
    for n in ENTITY_FACE:
        p = WD / "entity" / n
        t = p.read_text(encoding="utf-8")
        hits = t.count(kw)
        print("  [entity   ] %-28s %6d chars  %s命中=%d" % (n, len(t), kw, hits))
        if hits:
            print("  [STOP] entity/ 面出现接口面字面，A4' 自查失败")
            return 2
        plan.append((n, t))
    for n in IFACE_FACE:
        p = HERE / n
        t = p.read_text(encoding="utf-8")
        # 检测位 2：接口面件须 零凭据字面（token/session/card 类）
        bad = [w for w in ("api_token", "sessionId", "last4", "credentials") if w in t]
        face = re.search(r'_P2P_FACE\s*=\s*"(\w+)"', t)
        print("  [interface] %-28s %6d chars  _P2P_FACE=%s  凭据字面=%s"
              % (n, len(t), face.group(1) if face else "**缺**", bad or "无"))
        if bad or not face or face.group(1) != "interface":
            print("  [STOP] 接口面件自查失败")
            return 2
        plan.append((n, t))

    print("\n--- 3. 上传（file API；零 push）---")
    present = {f.name for f in api.files.get_all(pid)}
    for n, t in plan:
        (api.files.update if n in present else api.files.create)(pid, n, t)
        print("  [OK] %-28s %s (%d chars)" % (n, "更新" if n in present else "新建", len(t)))

    back = {f.name: (f.content or "") for f in api.files.get_all(pid)}
    fid = {}
    for n, t in plan:
        cb, lb = back.get(n, "").encode("utf-8"), t.encode("utf-8")
        fid[n] = {"byte_exact_raw": cb == lb,
                  "byte_exact_normalized": cb.replace(b"\r\n", b"\n") == lb.replace(b"\r\n", b"\n"),
                  "local_sha256": sha(lb), "cloud_sha256": sha(cb)}
        print("  回读 %-28s raw=%s norm=%s" % (n, fid[n]["byte_exact_raw"], fid[n]["byte_exact_normalized"]))
    emit("backtest_upload_fidelity", {"projectId": pid, "files": fid}, "上传回读保真（双值并列）")

    # --- 4. 编译
    print("\n--- 4. compiles.create ---")
    t0 = time.time()
    comp = api.compiles.create(pid)
    cid = comp.compileId
    print("  [OK] compileId=%s state=%s 耗时%.1fs" % (cid, getattr(comp, "state", "?"), time.time() - t0))
    for _ in range(40):
        c = api.compiles.get(pid, cid)
        st = str(getattr(c, "state", ""))
        if "InQueue" not in st and "BuildRequest" not in st:
            break
        time.sleep(3)
    logs = list(getattr(c, "logs", []) or [])
    print("  编译状态: %s  日志 %d 行" % (getattr(c, "state", "?"), len(logs)))
    for ln in logs[:20]:
        print("    %s" % str(ln)[:200])
    emit("backtest_compile", {"compileId": cid, "state": str(getattr(c, "state", "")),
                              "logs": [str(x) for x in logs]}, "编译留痕，全量日志")
    if "Error" in str(getattr(c, "state", "")):
        print("  [F2] 编译失败，**未发回测，零配额消耗**")
        return 2

    # --- 5. 发回测（**配额消耗，不可撤销**）
    print("\n--- 5. backtests.create（配额消耗，不可撤销）---")
    name = "p2prime-shot2-probe-%s" % TS
    bt = api.backtests.create(pid, cid, name)
    bid = bt.backtestId
    print("  [OK] backtestId=%s name=%s" % (bid, name))

    print("\n--- 6. 轮询完成 ---")
    t0 = time.time()
    while time.time() - t0 < POLL_MAX:
        bt = api.backtests.get(pid, bid)
        done = bool(getattr(bt, "completed", False))
        prog = getattr(bt, "progress", None)
        print("  +%4ds  completed=%-5s progress=%s error=%s"
              % (int(time.time() - t0), done, prog, str(getattr(bt, "error", "") or "")[:80]), flush=True)
        if done:
            break
        time.sleep(POLL_GAP)

    # --- 7. 产物取回（A 类端点；乙-5 先落原件）
    print("\n--- 7. 产物取回 ---")
    d = bt.model_dump() if hasattr(bt, "model_dump") else bt.dict()
    (RAW / ("backtest_raw_%s.json" % TS)).write_text(
        json.dumps(d, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print("  原件落盘: backtest_raw_%s.json" % TS)
    print("  completed=%s  error=%s" % (d.get("completed"), str(d.get("error") or "")[:200]))
    print("  stacktrace=%s" % str(d.get("stacktrace") or "")[:300])

    # 日志全量（探针输出在此）
    raw_logs = []
    try:
        r = api.get("backtests/read", {"projectId": pid, "backtestId": bid})
        (RAW / ("backtest_read_raw_%s.json" % TS)).write_text(
            json.dumps(r, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        print("  backtests/read 顶层键: %s" % sorted(r.keys())[:20])
        rg = (r.get("backtest") or {}).get("researchGuide") or r.get("researchGuide")
        print("  researchGuide（配额）: %s" % json.dumps(rg, ensure_ascii=False))
    except Exception as e:
        print("  [WARN] backtests/read: %s: %s" % (type(e).__name__, str(e)[:200]))

    for src in ("logs", "Logs"):
        v = d.get(src)
        if v:
            raw_logs = v if isinstance(v, list) else str(v).splitlines()
            break
    if not raw_logs:
        try:
            lg = api.get("backtests/read/log", {"projectId": pid, "backtestId": bid, "format": "json"})
            raw_logs = (lg.get("logs") or lg.get("log") or "")
            if isinstance(raw_logs, str):
                raw_logs = raw_logs.splitlines()
            print("  日志经 backtests/read/log 取得 %d 行（B 类端点）" % len(raw_logs))
        except Exception as e:
            print("  [WARN] backtests/read/log: %s: %s" % (type(e).__name__, str(e)[:200]))

    (RAW / ("backtest_logs_%s.txt" % TS)).write_text("\n".join(str(x) for x in raw_logs), encoding="utf-8")
    print("  日志原件落盘: backtest_logs_%s.txt (%d 行)" % (TS, len(raw_logs)))

    # --- 8. 探针输出重组
    print("\n--- 8. 探针分片重组 ---")
    buf, out = {}, {}
    for ln in raw_logs:
        s = str(ln)
        i = s.find(MARK + "|")
        if i < 0:
            continue
        parts = s[i:].split("|")
        if len(parts) >= 4 and parts[2] == "BEGIN":
            buf[parts[1]] = {"n": int(parts[3]), "frag": {}}
        elif len(parts) >= 3 and parts[2] == "END":
            b = buf.get(parts[1])
            if b:
                txt = "".join(b["frag"].get(k, "") for k in sorted(b["frag"]))
                try:
                    out[parts[1]] = json.loads(txt)
                except Exception as e:
                    out[parts[1]] = {"_reassemble_error": str(e), "_len": len(txt),
                                     "_frags": len(b["frag"]), "_expected": b["n"]}
        elif len(parts) >= 4 and parts[2].isdigit():
            b = buf.setdefault(parts[1], {"n": None, "frag": {}})
            b["frag"][parts[2]] = "|".join(parts[3:])
    for tag in ("ENV", "A1_I_IMPORT", "A1_II_OBJSTORE", "A6_JIA", "X1_JIA", "A1_III_ADDDATA"):
        r = out.get(tag)
        st = "(未取得)" if r is None else r.get("status", "?")
        print("  %-16s %s" % (tag, st))
    emit("backtest_probe_results", {"projectId": pid, "backtestId": bid, "results": out},
         "六探测项重组结果")
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

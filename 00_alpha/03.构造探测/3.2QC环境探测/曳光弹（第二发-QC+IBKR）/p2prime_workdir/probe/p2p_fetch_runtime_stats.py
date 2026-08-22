# -*- coding: utf-8 -*-
"""
P2' · 经 runtimeStatistics 取回探针结果（只读，零配额消耗）

通道：`backtests/read` → `backtest.runtimeStatistics`（**A 类端点**，lean 库已发布）。
成因：日志通道 free 档实测 **10kb/回测 且 10kb/天**（截断告示原文），今日已耗尽。
本件同时采集该通道之**开销材料**（键数、单值长度、总字节）——α-4 射程内。

乙-5：先落原件再解析。凭据面：本通道零凭据字段，仍执行残留复扫。
"""
import glob
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lean.container import container

PID = 35315786
RAW = Path(__file__).resolve().parent / "raw"
TS = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
api = container.api_client

bid = sys.argv[1] if len(sys.argv) > 1 else None
if not bid:
    # 取本项目最新一次回测
    f = sorted(glob.glob(str(RAW / "backtest_raw_*.json")))[-1]
    bid = json.load(open(f, encoding="utf-8")).get("backtestId")
print("=== 取回 runtimeStatistics ===")
print("  projectId=%s backtestId=%s" % (PID, bid))

r = api.get("backtests/read", {"projectId": PID, "backtestId": bid})
bt = r.get("backtest") or {}
(RAW / ("rt_read_raw_%s.json" % TS)).write_text(
    json.dumps(r, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
print("  原件落盘: rt_read_raw_%s.json" % TS)
print("  status=%s completed=%s hasInitializeError=%s error=%s"
      % (bt.get("status"), bt.get("completed"), bt.get("hasInitializeError"),
         str(bt.get("error") or "")[:150]))

rs = bt.get("runtimeStatistics") or {}
p2p = {k: v for k, v in rs.items() if k.startswith("P2P_")}
print("\n--- 通道开销材料（α-4）---")
print("  runtimeStatistics 键总数 : %d" % len(rs))
print("  其中 P2P_* 键数          : %d" % len(p2p))
if p2p:
    lens = [len(str(v)) for v in p2p.values()]
    print("  P2P_* 单值长度 min/max   : %d / %d" % (min(lens), max(lens)))
    print("  P2P_* 载荷总字节         : %d" % sum(lens))
print("  非 P2P 键（QC 自带）      : %s" % sorted(set(rs) - set(p2p)))

# --- runtimeStatistic 单值上限探针（本轮 RTLIM 项之实证）
print("\n--- RTLIM 单值上限实证 ---")
for n in (100, 200, 400, 800, 1600):
    k = "P2P_LIMPROBE_%d" % n
    if k in rs:
        got = len(str(rs[k]))
        print("  写入 %4d 字符 -> 回读 %4d 字符  %s" % (n, got, "完整" if got == n else "**被截断**"))
    else:
        print("  写入 %4d 字符 -> **键不在场**" % n)

# --- 分片重组
print("\n--- 分片重组 ---")
tags = sorted({m.group(1) for k in p2p if (m := re.match(r"P2P_([A-Z0-9]+)_(?:HDR|\d{3})$", k))})
out = {}
for tag in tags:
    hdr = p2p.get("P2P_%s_HDR" % tag)
    frags = {k[-3:]: v for k, v in p2p.items() if re.match(r"P2P_%s_\d{3}$" % tag, k)}
    txt = "".join(frags[i] for i in sorted(frags))
    exp_n, exp_len = (hdr.split("/") + [None, None])[:2] if hdr else (None, None)
    ok = "?"
    try:
        out[tag] = json.loads(txt)
        ok = "OK"
    except Exception as e:
        out[tag] = {"_reassemble_error": str(e), "_got": len(txt),
                    "_expected_len": exp_len, "_frags": len(frags), "_expected_frags": exp_n}
        ok = "**失败**"
    print("  %-8s HDR=%-12s 实收%2d片/%5d字符  重组=%s" % (tag, hdr, len(frags), len(txt), ok))
for k in p2p:
    if k.endswith("_ERR"):
        print("  [ERR] %s = %s" % (k, p2p[k]))

(RAW / ("rt_probe_results_%s.json" % TS)).write_text(
    json.dumps({"backtestId": bid, "results": out,
                "channel_cost": {"keys_total": len(rs), "keys_p2p": len(p2p),
                                 "payload_bytes": sum(len(str(v)) for v in p2p.values())}},
               ensure_ascii=False, indent=2, default=str), encoding="utf-8")

# 凭据残留复扫（本通道零凭据字段，仍执行）
blob = json.dumps(out, ensure_ascii=False, default=str)
leaks = [w for w in ("api_token", "sessionId", "last4", "Authorization") if w in blob]
print("\n  凭据残留复扫: %s" % (leaks or "零残留"))
print("  落位: %s" % RAW)

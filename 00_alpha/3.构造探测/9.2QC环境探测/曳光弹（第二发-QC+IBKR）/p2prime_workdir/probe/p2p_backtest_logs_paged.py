# -*- coding: utf-8 -*-
"""P2' · 回测日志分页取回（只读，零配额）。start/end ＝ **行号**（非时间戳），单页 ≤200 行。"""
import json, sys
from datetime import datetime, timezone
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lean.container import container

PID, BID = 35315786, "64c64125a2ee96a7ea50dc14f38add25"
RAW = Path(__file__).resolve().parent / "raw"
TS = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
PAGE, MAXPAGE = 200, 200
api = container.api_client

allrows, start, pages = [], 0, 0
while pages < MAXPAGE:
    try:
        d = api.get("backtests/read/log", {"projectId": PID, "backtestId": BID,
                                           "start": start, "end": start + PAGE, "query": ""})
    except Exception as e:
        print("  [FAIL] start=%d  %s: %s" % (start, type(e).__name__, str(e)[:180]))
        break
    rows = d.get("logs") or d.get("log") or []
    if isinstance(rows, str):
        rows = rows.splitlines()
    n = len(rows)
    print("  [OK] start=%-6d 取回 %3d 行  (length=%s)" % (start, n, d.get("length")))
    allrows.extend(rows)
    pages += 1
    if n < PAGE:
        break
    start += PAGE

p = RAW / ("backtest_logs_paged_%s.txt" % TS)
p.write_text("\n".join(str(x) for x in allrows), encoding="utf-8")
print("\n日志原件落盘: %s  共 %d 行, %d 页" % (p.name, len(allrows), pages))
hits = [r for r in allrows if "P2PPROBE" in str(r)]
print("P2PPROBE 分片行数: %d" % len(hits))
for r in allrows[:6]:
    print("   ", str(r)[:150])

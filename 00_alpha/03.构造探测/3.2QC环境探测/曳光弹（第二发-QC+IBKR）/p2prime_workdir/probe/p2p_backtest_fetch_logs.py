# -*- coding: utf-8 -*-
"""P2' · 回测日志取回（只读，零配额消耗）。逐候选试端点，全量错误原文留痕。"""
import json, sys, glob
from datetime import datetime, timezone
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lean.container import container

PID, BID = 35315786, "64c64125a2ee96a7ea50dc14f38add25"
RAW = Path(__file__).resolve().parent / "raw"
TS = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
api = container.api_client

print("=== 原件字段面盘点（F1-18：pydantic 丢字段，故直取裸 API）===")
r = api.get("backtests/read", {"projectId": PID, "backtestId": BID})
bt = r.get("backtest") or {}
print("  backtest 顶层键 (%d): %s" % (len(bt), sorted(bt.keys())))
(RAW / ("backtest_read_full_%s.json" % TS)).write_text(
    json.dumps(r, ensure_ascii=False, indent=2, default=str), encoding="utf-8")

CANDS = [
    ("backtests/read/log", {"projectId": PID, "backtestId": BID, "start": 0, "end": 99999999}),
    ("backtests/read/log", {"projectId": PID, "backtestId": BID, "start": 0}),
    ("backtests/read/log", {"projectId": PID, "backtestId": BID, "start": 0, "format": "json"}),
    ("backtests/read/logs", {"projectId": PID, "backtestId": BID, "start": 0}),
]
logs = None
for ep, params in CANDS:
    try:
        d = api.get(ep, params)
        keys = sorted(d.keys()) if isinstance(d, dict) else type(d).__name__
        print("\n[OK  ] %s %s\n       键: %s" % (ep, {k: v for k, v in params.items() if k not in ("projectId", "backtestId")}, keys))
        for k in ("logs", "log", "Logs"):
            if isinstance(d, dict) and d.get(k):
                logs = d[k]
                print("       -> 命中字段 %r，类型 %s" % (k, type(logs).__name__))
                break
        (RAW / ("backtest_logendpoint_%s_%s.json" % (ep.replace("/", "_"), TS))).write_text(
            json.dumps(d, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        if logs:
            break
    except Exception as e:
        print("\n[FAIL] %s %s\n       %s: %s" % (ep, {k: v for k, v in params.items() if k not in ("projectId", "backtestId")}, type(e).__name__, str(e)[:200]))

if isinstance(logs, str):
    logs = logs.splitlines()
logs = logs or []
p = RAW / ("backtest_logs_full_%s.txt" % TS)
p.write_text("\n".join(str(x) for x in logs), encoding="utf-8")
print("\n=== 日志原件落盘: %s (%d 行) ===" % (p.name, len(logs)))
for ln in logs[:8]:
    print("   ", str(ln)[:160])

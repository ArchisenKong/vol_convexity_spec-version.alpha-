# -*- coding: utf-8 -*-
"""P2' · research 会话到场监视（只读轮询）；到场即触发 α-6-乙。零写入、零配额消耗。"""
import subprocess, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lean.container import container

ORG = "954877bda8b6760ae398418ce79a5500"
PID = 35315786
GAP, MAX_S = 10, 540
HERE = Path(__file__).resolve().parent

api = container.api_client
t0 = time.time()
i = 0
while time.time() - t0 < MAX_S:
    i += 1
    n = api.nodes.get_all(ORG)
    d = n.model_dump() if hasattr(n, "model_dump") else n.dict()
    r = (d.get("research") or [{}])[0]
    busy = r.get("busy")
    try:
        api.get("research/read", {"projectId": PID})
        sess = True
        err = ""
    except Exception as e:
        sess = False
        err = str(e)[:60]
    print("  [%02d] +%4ds  node.busy=%-5s  research/read=%-5s  %s"
          % (i, int(time.time() - t0), busy, "OK" if sess else "FAIL", "" if sess else err), flush=True)
    if sess:
        print("\n[会话到场] 立即触发 α-6-乙\n", flush=True)
        sys.exit(subprocess.run([sys.executable, "-u", str(HERE / "p2p_alpha6_research.py")]).returncode)
    time.sleep(GAP)
print("\n[超时] %ds 内会话未到场，未触发。本轮零动作、零写入。" % MAX_S)
sys.exit(3)

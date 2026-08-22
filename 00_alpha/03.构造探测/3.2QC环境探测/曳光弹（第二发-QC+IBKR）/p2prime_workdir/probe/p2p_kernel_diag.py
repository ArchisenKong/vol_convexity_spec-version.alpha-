# -*- coding: utf-8 -*-
"""P2' · research 会话内核面只读诊断。零写入、零 POST、零配额。凭据全程遮蔽。"""
import json, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lean.container import container
import requests

PID = 35315786
api = container.api_client
s = api.get("research/read", {"projectId": PID})
SID, URI, TOK = str(s.get("sessionId") or ""), str(s.get("uri") or "").rstrip("/"), str(s.get("token") or "")
secrets = [x for x in (TOK, SID) if x]

def scrub(t):
    t = str(t)
    for x in secrets:
        t = t.replace(x, "<REDACTED>")
    t = re.sub(r"R-[0-9a-f]{32}", "<REDACTED-SID>", t)
    return re.sub(r"\b[0-9a-f]{40,}\b", "<REDACTED-HEX>", t)

H = {"Authorization": "token %s" % TOK}
for path in ("/api/status", "/api/kernelspecs", "/api/kernels", "/api/sessions", "/api/terminals", "/api/contents"):
    try:
        r = requests.get(URI + path, headers=H, timeout=60)
        print("[%s] GET %s" % (r.status_code, path))
        if r.status_code == 200:
            j = r.json()
            if path == "/api/kernelspecs":
                print("     default:", j.get("default"))
                for k, v in (j.get("kernelspecs") or {}).items():
                    print("     spec: %-22s display=%s" % (k, (v.get("spec") or {}).get("display_name")))
            elif path == "/api/contents":
                for it in (j.get("content") or []):
                    print("     %-9s %-30s %s" % (it.get("type"), it.get("name"), it.get("size")))
            elif isinstance(j, list):
                print("     list, %d 项" % len(j))
                for it in j:
                    print("     ", scrub(json.dumps({k: it.get(k) for k in ("id","name","path","kernel","execution_state","connections") if k in it}, ensure_ascii=False))[:300])
            else:
                print("     ", scrub(json.dumps(j, ensure_ascii=False))[:400])
        else:
            print("     ", scrub(r.text)[:200])
    except Exception as e:
        print("[ERR] GET %s  %s: %s" % (path, type(e).__name__, scrub(e)[:150]))
    print()

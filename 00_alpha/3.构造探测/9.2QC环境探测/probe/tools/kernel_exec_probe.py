"""
E25 · Research 内核编程执行（任务书外，执行人已授权）

目标：经 research/read 取得的会话句柄，通过 Jupyter 内核 WebSocket 协议
      在云端 research 内核中执行代码并取回输出。

仅通道探测。执行的代码不含任何交易或策略逻辑，不计算收益指标。

凭据纪律：token 与 sessionId 全程不打印，所有输出经 scrub() 过滤。
"""
import json
import re
import ssl
import uuid

PROJECT_ID = 35174460

# 探测代码：与 E19/E20 同族的固定载荷，便于跨通道比对
PROBE_CODE = r'''
import os, sys, platform, hashlib, json
PAYLOAD = (
    "probe-marker-E25\n"
    "line2-ascii\n"
    "line3-中文与全角：测试　保真\n"
    'line4-special: {"json":true} [1,2,3] <tag/> & % $ # @ ! ~ ` ^\n'
    "line5-long: " + "0123456789" * 8 + "\n"
)
b = PAYLOAD.encode("utf-8")
print("cwd            :", os.getcwd())
print("python         :", sys.version.split()[0])
print("payload bytes  :", len(b))
print("payload sha256 :", hashlib.sha256(b).hexdigest())
import pandas as pd
df = pd.DataFrame({"a": range(5), "b": [x*1.5 for x in range(5)]})
print("dataframe sum  :", float(df["b"].sum()))
df
'''


def main():
    from lean.container import container
    api = container.api_client
    s = api.get("research/read", {"projectId": PROJECT_ID})
    SID = str(s["sessionId"])
    URI = str(s["uri"]).rstrip("/")
    TOK = str(s["token"])

    secrets = [x for x in (TOK, SID) if x]

    def scrub(t):
        t = str(t)
        for x in secrets:
            t = t.replace(x, "<REDACTED>")
        t = re.sub(r"R-[0-9a-f]{32}", "<REDACTED-SID>", t)
        t = re.sub(r"\b[0-9a-f]{40,}\b", "<REDACTED-HEX>", t)
        return t

    import requests
    H = {"Authorization": f"token {TOK}"}

    kernels = requests.get(URI + "/api/kernels", headers=H, timeout=30).json()
    if not kernels:
        print("[FAIL] 无运行中的内核")
        return
    kid = kernels[0]["id"]
    print("内核 name=%s state=%s conns=%s" % (
        kernels[0].get("name"), kernels[0].get("execution_state"),
        kernels[0].get("connections")))
    print()

    ws_url = URI.replace("https://", "wss://").replace("http://", "ws://")
    ws_url += f"/api/kernels/{kid}/channels"

    import websocket
    print("=== 连接内核 WebSocket ===")
    ws = websocket.create_connection(
        ws_url,
        header=[f"Authorization: token {TOK}"],
        sslopt={"cert_reqs": ssl.CERT_REQUIRED},
        timeout=60,
    )
    print("[OK] 已连接")
    print()

    msg_id = uuid.uuid4().hex
    sess_uuid = uuid.uuid4().hex
    req = {
        "header": {"msg_id": msg_id, "username": "probe", "session": sess_uuid,
                   "msg_type": "execute_request", "version": "5.3"},
        "parent_header": {},
        "metadata": {},
        "content": {"code": PROBE_CODE, "silent": False, "store_history": False,
                    "user_expressions": {}, "allow_stdin": False,
                    "stop_on_error": True},
        "channel": "shell",
    }
    ws.send(json.dumps(req))
    print("=== 已发送 execute_request，收集输出 ===")
    print()

    collected = {"stream": [], "execute_result": [], "display_data": [],
                 "error": [], "status": []}
    reply_ok = False
    idle = False

    while not (reply_ok and idle):
        try:
            raw = ws.recv()
        except Exception as e:
            print("[recv 结束]", type(e).__name__, scrub(e)[:150])
            break
        try:
            m = json.loads(raw)
        except Exception:
            continue
        if (m.get("parent_header") or {}).get("msg_id") != msg_id:
            continue
        mt = m["header"]["msg_type"]
        c = m.get("content") or {}

        if mt == "stream":
            collected["stream"].append(c.get("text", ""))
        elif mt == "execute_result":
            collected["execute_result"].append(c.get("data", {}))
        elif mt == "display_data":
            collected["display_data"].append(c.get("data", {}))
        elif mt == "error":
            collected["error"].append(c)
        elif mt == "status":
            st = c.get("execution_state")
            collected["status"].append(st)
            if st == "idle":
                idle = True
        elif mt == "execute_reply":
            reply_ok = True
            print("execute_reply status:", c.get("status"),
                  " execution_count:", c.get("execution_count"))

    ws.close()

    print()
    print("=" * 70)
    print("stdout（stream）")
    print("=" * 70)
    print(scrub("".join(collected["stream"])))

    print("=" * 70)
    print("execute_result / display_data 的 MIME 类型与体积")
    print("=" * 70)
    for label in ("execute_result", "display_data"):
        for d in collected[label]:
            for mime, val in d.items():
                n = len(val) if isinstance(val, str) else len(json.dumps(val))
                print(f"  [{label}] {mime:28} {n} 字节")

    if collected["error"]:
        print("=" * 70)
        print("error")
        print("=" * 70)
        for e in collected["error"]:
            print(" ", e.get("ename"), scrub(e.get("evalue"))[:200])

    print()
    print("=" * 70)
    print("汇总")
    print("=" * 70)
    print(json.dumps({
        "stream 段数": len(collected["stream"]),
        "execute_result 数": len(collected["execute_result"]),
        "display_data 数": len(collected["display_data"]),
        "error 数": len(collected["error"]),
        "status 序列": collected["status"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

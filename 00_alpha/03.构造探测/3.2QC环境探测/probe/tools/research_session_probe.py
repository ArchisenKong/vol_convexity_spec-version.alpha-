"""
E24 · Research 会话编程访问探测（任务书外，执行人追加，执行人已授权）

目标：research/read 返回的 uri + token 是否可用于编程访问运行中的 research 会话。

凭据纪律（本脚本从设计起即内建遮蔽，修正 endpoint_probe.py 的缺陷）：
  - token 与 sessionId 一律不打印。
  - 所有输出经 scrub() 过滤，凡出现 token / sessionId 处替换为占位符。
  - 不写出任何含凭据的文件。
"""
import json
import re

PROJECT_ID = 35174460

from lean.container import container  # noqa: E402

api = container.api_client
sess = api.get("research/read", {"projectId": PROJECT_ID})

SESSION_ID = str(sess.get("sessionId") or "")
URI = str(sess.get("uri") or "").rstrip("/")
TOKEN = str(sess.get("token") or "")
NODE_ID = str(sess.get("nodeId") or "")

_SECRETS = [s for s in (TOKEN, SESSION_ID) if s]


def scrub(text):
    t = str(text)
    for s in _SECRETS:
        t = t.replace(s, "<REDACTED>")
    t = re.sub(r"R-[0-9a-f]{32}", "<REDACTED-SESSION-ID>", t)
    t = re.sub(r"\b[0-9a-f]{40,}\b", "<REDACTED-HEX>", t)
    return t


print("=== research/read 会话句柄（值已遮蔽）===")
print("  sessionId : <REDACTED>（长度 %d）" % len(SESSION_ID))
print("  token     : <REDACTED>（长度 %d）" % len(TOKEN))
print("  nodeId    :", NODE_ID)
print("  uri host  :", scrub(URI).split("//")[-1].split("/")[0] if URI else "(空)")
print()

import requests  # noqa: E402

# 两种 Jupyter 认证方式都试
AUTHS = [
    ("Authorization 头", {"Authorization": f"token {TOKEN}"}, {}),
    ("token 查询参数", {}, {"token": TOKEN}),
]

ENDPOINTS = [
    ("GET", "/api/status", "Jupyter 服务状态"),
    ("GET", "/api/kernelspecs", "可用内核规格"),
    ("GET", "/api/kernels", "运行中的内核"),
    ("GET", "/api/sessions", "运行中的会话"),
    ("GET", "/api/contents", "文件树根"),
    ("GET", "/api/contents/research.ipynb", "notebook 内容（关键：是否含 outputs）"),
    ("GET", "/api/terminals", "终端"),
    ("GET", "/lab/api/settings", "JupyterLab 设置"),
]

results = {}

for auth_label, headers, params in AUTHS:
    print("#" * 70)
    print(f"# 认证方式：{auth_label}")
    print("#" * 70)
    for method, path, note in ENDPOINTS:
        url = URI + path
        try:
            r = requests.request(method, url, headers=headers, params=params,
                                 timeout=30, allow_redirects=False)
            body = scrub(r.text)
            print(f"[{r.status_code}] {method} {path}   —— {note}")
            ct = r.headers.get("content-type", "")
            if r.status_code == 200:
                results[(auth_label, path)] = r.status_code
                if "json" in ct:
                    try:
                        j = r.json()
                        if isinstance(j, dict):
                            print(f"        JSON dict, 键: {list(j.keys())[:12]}")
                            if path.endswith(".ipynb"):
                                content = j.get("content") or {}
                                cells = content.get("cells") or []
                                print(f"        cells: {len(cells)}")
                                tot = 0
                                for i, c in enumerate(cells):
                                    outs = c.get("outputs") or []
                                    tot += len(outs)
                                    if outs:
                                        kinds = [o.get("output_type") for o in outs]
                                        print(f"          cell[{i}] outputs={len(outs)} 类型={kinds}")
                                print(f"        >>> outputs 总数: {tot} <<<")
                        elif isinstance(j, list):
                            print(f"        JSON list, {len(j)} 项")
                            for it in j[:3]:
                                if isinstance(it, dict):
                                    print(f"          {[k for k in it.keys()][:8]}")
                    except Exception as e:
                        print("        JSON 解析失败:", scrub(e)[:150])
                else:
                    print(f"        content-type={ct}, {len(r.content)} 字节")
                    print("        前 200 字符:", body[:200].replace("\n", " "))
            else:
                print(f"        {body[:200]}")
        except Exception as e:
            print(f"[ERR] {method} {path}   {type(e).__name__}: {scrub(e)[:200]}")
        print()

print("#" * 70)
print("# 汇总：HTTP 200 的端点")
print("#" * 70)
if results:
    for (a, p), code in results.items():
        print(f"  [{a}] {p}")
else:
    print("  无一返回 200")

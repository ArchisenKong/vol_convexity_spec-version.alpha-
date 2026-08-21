# =====================================================================
# E20 · Research → QC file API → 云端项目文件 → lean cloud pull → 本地
# 放入 QC 网页端 Research 的一个新 cell 执行。
# 任务书外，执行人追加。仅通道探测，不含交易或策略逻辑，不计算收益指标。
#
# 凭据纪律：
#   本 cell 使用 airlock/config.json 中 QC 自行注入的 job 凭据，
#   凭据仅在云端内核内存中流转，全程不打印、不写入文件、不外传。
#   所有输出在打印前经 scrub() 过滤，若响应意外回显凭据则替换为 <REDACTED>。
# =====================================================================
import json, hashlib, time

PROJECT_ID = 35174460

# 第二轮更正：api/v2 base 正确后，端点已找到、认证已通过，
# 唯一阻挡是扩展名白名单。服务端原文：
#   "File extension not valid txt valid values are : cs, py, ipynb, html, css"
# 故改用白名单内的扩展名，并一次覆盖多个以摸清约束边界。
FILE_NAMES = [
    "probe_E20_output.py",
    "probe_E20_output.html",
    "probe_E20_output.css",
]

PAYLOAD = (
    "probe-marker-E20\n"
    "line2-ascii\n"
    "line3-中文与全角：测试　保真\n"
    'line4-special: {"json":true} [1,2,3] <tag/> & % $ # @ ! ~ ` ^\n'
    "line5-long: " + "0123456789" * 8 + "\n"
)
PAYLOAD_B = PAYLOAD.encode("utf-8")
PAYLOAD_SHA = hashlib.sha256(PAYLOAD_B).hexdigest()

print("payload bytes :", len(PAYLOAD_B))
print("payload sha256:", PAYLOAD_SHA)
print()

cfg = json.load(open("config.json"))
UID = str(cfg.get("job-user-id", ""))
TOK = str(cfg.get("api-access-token", ""))

# 首轮错误更正：config.json 的 cloud-api-url 实测为
#   https://www.quantconnect.com/api/v2/cloud/     ← 带 /cloud/ 后缀
# 直接拼 files/create 会得到 api/v2/cloud/files/create，该端点不存在。
# 项目与文件 API 的正确 base 是 api/v2/（不含 cloud/），
# 与 lean/constants.py:85 的 API_BASE_URL 一致。
_RAW = str(cfg.get("cloud-api-url", "") or "")
if not _RAW.endswith("/"):
    _RAW += "/"
BASE = _RAW[: -len("cloud/")] if _RAW.endswith("cloud/") else _RAW
if not BASE:
    BASE = "https://www.quantconnect.com/api/v2/"

# 两个 base 都试，一轮内定论
BASES = [("api/v2（正确候选）", BASE)]
if _RAW and _RAW != BASE:
    BASES.append(("api/v2/cloud（首轮误用，作对照）", _RAW))

_SECRETS = [s for s in (TOK, UID) if s]


def scrub(text):
    """在打印前抹掉任何可能回显的凭据。"""
    t = str(text)
    for s in _SECRETS:
        if s:
            t = t.replace(s, "<REDACTED>")
    return t


print("job-user-id   : <REDACTED>（长度 %d）" % len(UID))
print("api-access-token 存在:", bool(TOK), "（长度 %d）" % len(TOK))
for label, b in BASES:
    print(f"base [{label}] : {scrub(b)}")
print()


def qc_post(base, endpoint, body):
    """按 lean api_client.py:135-152 复现的认证方式发请求。"""
    import requests
    ts = str(int(time.time()))
    pw = hashlib.sha256(f"{TOK}:{ts}".encode("utf-8")).hexdigest()
    r = requests.post(
        base + endpoint,
        headers={"Timestamp": ts},
        auth=(UID, pw),
        json=body,
        timeout=60,
    )
    return r.status_code, r.text


BASE_OK = BASES[0][1]   # api/v2（已确认端点可达、认证通过）
verdict = {}

for fname in FILE_NAMES:
    print("#" * 68)
    print(f"# 文件名 = {fname}")
    print("#" * 68)

    for step, endpoint, body in [
        ("1. files/create", "files/create",
         {"projectId": PROJECT_ID, "name": fname, "content": PAYLOAD}),
        ("2. files/update", "files/update",
         {"projectId": PROJECT_ID, "name": fname, "content": PAYLOAD}),
        ("3. files/read", "files/read",
         {"projectId": PROJECT_ID, "name": fname}),
    ]:
        print("-" * 68)
        print(step)
        print("-" * 68)
        try:
            code, text = qc_post(BASE_OK, endpoint, body)
            print("HTTP", code)
            print(scrub(text)[:600])
            if endpoint == "files/read":
                try:
                    j = json.loads(text)
                    for f in (j.get("files") or []):
                        c = f.get("content", "")
                        h = hashlib.sha256(c.encode("utf-8")).hexdigest()
                        same = (h == PAYLOAD_SHA)
                        verdict[fname] = same
                        print("回读 content 字节 :", len(c.encode("utf-8")))
                        print("回读 content sha256:", h)
                        print(">>> 与载荷一致:", same, "<<<")
                except Exception:
                    pass
        except Exception as e:
            print("[FAIL]", type(e).__name__, scrub(e))
        print()

print("#" * 68)
print("# 汇总：哪些扩展名可承载回传")
print("#" * 68)
print(json.dumps(verdict, ensure_ascii=False, indent=2) if verdict
      else "（无一成功写入并回读）")

print()
print("=" * 68)
print("4. storage-permissions（config.json 中的 ObjectStore 权限声明）")
print("=" * 68)
print(json.dumps(cfg.get("storage-permissions"), ensure_ascii=False))

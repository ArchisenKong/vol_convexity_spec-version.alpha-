# =====================================================================
# E19 · Research 输出回传路径探测 · 放入 QC 网页端 Research 的一个 cell 执行
# 任务书外，执行人追加。仅通道探测，不含交易或策略逻辑，不计算收益指标。
# =====================================================================
import os, sys, json, hashlib, platform

MARKER = "probe-marker-E19"
PAYLOAD = (
    "probe-marker-E19\n"
    "line2-ascii\n"
    "line3-中文与全角：测试　保真\n"
    'line4-special: {"json":true} [1,2,3] <tag/> & % $ # @ ! ~ ` ^\n'
    "line5-long: " + "0123456789" * 8 + "\n"
)
PAYLOAD_B = PAYLOAD.encode("utf-8")
PAYLOAD_SHA = hashlib.sha256(PAYLOAD_B).hexdigest()

print("=" * 68)
print("A. 环境指纹")
print("=" * 68)
print("cwd            :", os.getcwd())
print("python         :", sys.version.split()[0])
print("platform       :", platform.platform())
print("libc           :", platform.libc_ver())
print("payload bytes  :", len(PAYLOAD_B))
print("payload sha256 :", PAYLOAD_SHA)

print()
print("=" * 68)
print("B. cwd 目录内容（判断 research 内核是否就在云端项目目录里）")
print("=" * 68)
try:
    for name in sorted(os.listdir(".")):
        p = os.path.join(".", name)
        kind = "DIR " if os.path.isdir(p) else "FILE"
        size = os.path.getsize(p) if os.path.isfile(p) else "-"
        print(f"  {kind} {name}  ({size})")
except Exception as e:
    print("  [FAIL]", type(e).__name__, e)

print()
print("=" * 68)
print("C. 多路径写入测试（哪条能落进云端项目）")
print("=" * 68)
candidates = [
    ("cwd 同级",            f"probe_E19_cwd.txt"),
    ("cwd/子目录",          f"probe_E19_sub/probe_E19_nested.txt"),
    ("上一级",              f"../probe_E19_parent.txt"),
    ("/tmp",                f"/tmp/probe_E19_tmp.txt"),
    ("显式 .ipynb 同名前缀", f"probe_E19_output.json"),
]
write_results = {}
for label, path in candidates:
    try:
        d = os.path.dirname(path)
        if d:
            os.makedirs(d, exist_ok=True)
        data = PAYLOAD_B if not path.endswith(".json") else json.dumps(
            {"marker": MARKER, "sha256": PAYLOAD_SHA, "bytes": len(PAYLOAD_B)},
            ensure_ascii=False, indent=2).encode("utf-8")
        with open(path, "wb") as f:
            f.write(data)
        back = open(path, "rb").read()
        ok = hashlib.sha256(back).hexdigest()
        write_results[label] = {"path": path, "wrote": len(data), "readback_sha256": ok}
        print(f"  [OK]   {label:22} -> {path}  ({len(data)} 字节, 回读 sha256 {ok[:16]}…)")
    except Exception as e:
        write_results[label] = {"path": path, "error": f"{type(e).__name__}: {e}"}
        print(f"  [FAIL] {label:22} -> {path}  {type(e).__name__}: {e}")

print()
print("=" * 68)
print("D. ObjectStore 写入（云端侧，验证方向性）")
print("=" * 68)
try:
    qb = QuantBook()  # noqa: F821  QC 研究环境内置
    qb.object_store.save_bytes("probe_E19_from_research", PAYLOAD_B)
    print("  [OK]   object_store.save_bytes 成功，key = probe_E19_from_research")
    got = qb.object_store.read_bytes("probe_E19_from_research")
    print("  [OK]   同环境内回读成功，", len(got), "字节，sha256",
          hashlib.sha256(bytes(got)).hexdigest()[:16], "…")
except Exception as e:
    print("  [FAIL]", type(e).__name__, e)

print()
print("=" * 68)
print("E. 浏览器下载链接（对照 E17 执行人报告的方式）")
print("=" * 68)
try:
    import base64
    from IPython.display import display, HTML, FileLink
    b64 = base64.b64encode(PAYLOAD_B).decode()
    display(HTML(
        f'<a download="probe_E19_download.txt" '
        f'href="data:text/plain;base64,{b64}">'
        f'▼ 点此下载 probe_E19_download.txt （{len(PAYLOAD_B)} 字节, sha256 {PAYLOAD_SHA[:16]}…）</a>'
    ))
    print("  [OK]   base64 data URI 锚点已生成（上方链接）")
    try:
        display(FileLink("probe_E19_cwd.txt"))
        print("  [OK]   IPython FileLink 已生成")
    except Exception as e:
        print("  [FAIL] FileLink:", type(e).__name__, e)
except Exception as e:
    print("  [FAIL]", type(e).__name__, e)

print()
print("=" * 68)
print("F. 汇总（请连同上方全部输出一起截图回传）")
print("=" * 68)
print(json.dumps({"payload_sha256": PAYLOAD_SHA,
                  "payload_bytes": len(PAYLOAD_B),
                  "writes": write_results}, ensure_ascii=False, indent=2))

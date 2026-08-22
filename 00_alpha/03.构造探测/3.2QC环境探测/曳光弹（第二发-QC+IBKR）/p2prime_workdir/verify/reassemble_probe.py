# -*- coding: utf-8 -*-
"""P2' · 回测探针分片重组（本地，零网络）。"""
import glob, json, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
MARK = "P2PPROBE"
f = sorted(glob.glob("probe/raw/backtest_logs_paged_*.txt"))[-1]
rows = open(f, encoding="utf-8").read().splitlines()
buf, out, order = {}, {}, []
for s in rows:
    i = s.find(MARK + "|")
    if i < 0:
        continue
    parts = s[i:].split("|")
    tag = parts[1]
    if len(parts) >= 4 and parts[2] == "BEGIN":
        buf[tag] = {"n": int(parts[3]), "total": int(parts[4]) if len(parts) > 4 else None, "frag": {}}
        order.append(tag)
    elif len(parts) >= 3 and parts[2] == "END":
        b = buf.get(tag)
        if b:
            txt = "".join(b["frag"][k] for k in sorted(b["frag"]))
            try:
                out[tag] = json.loads(txt)
            except Exception as e:
                out[tag] = {"_reassemble_error": str(e), "_got_chars": len(txt),
                            "_expected_chars": b["total"], "_frags": len(b["frag"]), "_expected_frags": b["n"]}
    elif len(parts) >= 4 and parts[2].isdigit():
        buf.setdefault(tag, {"n": None, "total": None, "frag": {}})["frag"][parts[2]] = "|".join(parts[3:])

print("=== 分片到场盘点 ===")
for tag in ("ENV", "A1_I_IMPORT", "A1_II_OBJSTORE", "A6_JIA", "X1_JIA", "A1_III_ADDDATA"):
    b = buf.get(tag)
    if not b:
        print("  %-16s **BEGIN 标未出现——该项输出未进入日志**" % tag)
    else:
        print("  %-16s 期望%s片/%s字符  实收%d片  重组=%s"
              % (tag, b["n"], b["total"], len(b["frag"]),
                 "OK" if tag in out and "_reassemble_error" not in out[tag] else "**失败/缺**"))
print()
json.dump(out, open("probe/derived/backtest_probe_reassembled.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2, default=str)
for tag, r in out.items():
    print("=" * 76)
    print("=== %s  status=%s" % (tag, r.get("status")))
    print("=" * 76)
    if r.get("status") == "error":
        print("  %s: %s" % (r.get("error_type"), r.get("error_text")))
        continue
    res = r.get("result") or r
    if tag == "ENV":
        for k in ("python_version", "python_compiler", "implementation", "platform", "machine", "libc_ver", "cwd"):
            print("  %-18s %s" % (k, res.get(k)))
        print("  sys_path_head      %s" % json.dumps(res.get("sys_path_head"), ensure_ascii=False)[:200])
    else:
        print(json.dumps(res, ensure_ascii=False, indent=2)[:2500])

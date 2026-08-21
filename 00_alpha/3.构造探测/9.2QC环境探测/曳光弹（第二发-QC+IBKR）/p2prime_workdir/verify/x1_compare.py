# -*- coding: utf-8 -*-
"""X-1 两位逐位比对（第一发本地基准 vs 本发 QC research 内核）。
本件只产比对**素材**：逐字段列同/异、给 ULP 距离。**不判「是否一致」之结论、不作合格主张、
不作环境可用性判定**（85-9 反面条款；DOC-25 兑现点不变更）。零网络。"""
import glob, json, struct, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

A = json.load(open("verify/x1_env_report_shot1.json", encoding="utf-8"))          # 第一发本地
f = sorted(glob.glob("probe/raw/x1_research_2*.json"))[-1]
B = json.load(open(f, encoding="utf-8"))["x1_result"]["report"]                    # 本发 QC research

def ulp(h1, h2):
    try:
        a, b = float.fromhex(h1), float.fromhex(h2)
    except Exception:
        return None
    ia = struct.unpack("<q", struct.pack("<d", a))[0]
    ib = struct.unpack("<q", struct.pack("<d", b))[0]
    if ia < 0: ia = -(ia & 0x7fffffffffffffff) 
    if ib < 0: ib = -(ib & 0x7fffffffffffffff)
    return abs(ia - ib)

print("=" * 92)
print("X-1 逐位比对素材 · 第一发本地(甲基准) vs 本发 QC research 内核(乙)")
print("=" * 92)
print("  比对件 B: %s" % f)
print()
print("  engine_sha256  A=%s" % A["engine_sha256"])
print("                 B=%s   %s" % (B["engine_sha256"], "同" if A["engine_sha256"] == B["engine_sha256"] else "**异**"))
print("  fixture lot_id A=%s  B=%s  %s" % (A["fixture"]["lot_id"], B["fixture"]["lot_id"],
      "同" if A["fixture"] == B["fixture"] else "**异**"))
print()
ea, eb = A["environment"], B["environment"]
print("-" * 92)
print("环境面")
print("-" * 92)
for k in ("implementation", "python_version", "python_compiler", "platform", "machine", "libc_ver"):
    print("  %-18s A: %-42s B: %s" % (k, ea.get(k), eb.get(k)))
print("  %-18s A: %s" % ("libm digest", ea["libm_fingerprint_digest"]))
print("  %-18s B: %s   %s" % ("", eb["libm_fingerprint_digest"],
      "同" if ea["libm_fingerprint_digest"] == eb["libm_fingerprint_digest"] else "**异**"))
print()
print("-" * 92)
print("libm 探针逐条（IEEE754 hex）")
print("-" * 92)
pa, pb = ea["libm_fingerprints"], eb["libm_fingerprints"]
nsame = ndiff = 0
for k in sorted(set(pa) | set(pb)):
    x, y = pa.get(k), pb.get(k)
    same = x == y
    nsame += same; ndiff += (not same)
    d = "" if same else ("  ULP距离=%s" % ulp(x, y))
    print("  %-22s %-26s %-26s %s%s" % (k, x, y, "同" if same else "**异**", d))
print("  -> 同 %d / 异 %d" % (nsame, ndiff))
print()
print("-" * 92)
print("引擎逐位输出 per_unit（repr / IEEE754 hex）")
print("-" * 92)
qa = A["result_bitwise"]["per_unit"]; qb = B["result_bitwise"]["per_unit"]
nsame = ndiff = 0
for k in sorted(set(qa) | set(qb)):
    va, vb = qa.get(k) or {}, qb.get(k) or {}
    ha, hb = va.get("hex"), vb.get("hex")
    same = (va.get("repr") == vb.get("repr")) and (ha == hb)
    nsame += same; ndiff += (not same)
    print("  %-8s %s" % (k, "同" if same else "**异**"))
    print("           A  %-24s %s" % (va.get("repr"), ha))
    print("           B  %-24s %s%s" % (vb.get("repr"), hb, "" if same else "   ULP距离=%s" % ulp(ha, hb)))
print("  -> 同 %d / 异 %d" % (nsame, ndiff))
print()
print("-" * 92)
print("路由与状态（非浮点面）")
print("-" * 92)
for k in ("route_id", "computability_status", "unstated_dimensions_hit", "lot_id",
          "instrument_class", "exercise_style"):
    x, y = A["result_bitwise"].get(k), B["result_bitwise"].get(k)
    print("  %-24s A=%-34s B=%-34s %s" % (k, x, y, "同" if x == y else "**异**"))
print()
print("=" * 92)
print("本件只产比对素材。不判「是否一致」之结论、不作合格主张、不作环境可用性判定。")
print("DOC-25 兑现点不变更（85-6 A11）。总体判定归 KD。")
print("=" * 92)

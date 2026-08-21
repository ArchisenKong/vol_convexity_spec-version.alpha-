# -*- coding: utf-8 -*-
"""X-1 三位比对：甲＝第一发本地 ／ 乙＝QC research 内核 ／ 丙＝QC 回测运行时。
只产比对素材；不判「是否一致」之结论、不作合格主张、不作环境可用性判定。DOC-25 兑现点不变更。"""
import glob, json, struct, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

A = json.load(open("verify/x1_env_report_shot1.json", encoding="utf-8"))
B = json.load(open(sorted(glob.glob("probe/raw/x1_research_2*.json"))[-1], encoding="utf-8"))["x1_result"]["report"]
C = json.load(open(sorted(glob.glob("probe/raw/rt_probe_results_*.json"))[-1], encoding="utf-8"))["results"]["X1C"]["result"]

def ulp(h1, h2):
    try:
        a, b = float.fromhex(h1), float.fromhex(h2)
    except Exception:
        return None
    f = lambda x: struct.unpack("<q", struct.pack("<d", x))[0]
    ia, ib = f(a), f(b)
    ia = -(ia & 0x7fffffffffffffff) if ia < 0 else ia
    ib = -(ib & 0x7fffffffffffffff) if ib < 0 else ib
    return abs(ia - ib)

ea, eb = A["environment"], B["environment"]
print("=" * 100)
print("X-1 三位比对素材   甲=第一发本地(Win)  乙=QC research 内核  丙=QC 回测运行时")
print("=" * 100)
print("\n--- 环境面 ---")
rows = [("python", ea["python_version"], eb["python_version"], C["pv"]),
        ("compiler", ea["python_compiler"], eb["python_compiler"], C["pc"]),
        ("platform", ea["platform"], eb["platform"], C["pf"]),
        ("libc", str(ea["libc_ver"]), str(eb["libc_ver"]), str(C["lc"])),
        ("libm digest", ea["libm_fingerprint_digest"][:24] + "…",
         eb["libm_fingerprint_digest"][:24] + "…", C["ld"][:24] + "…")]
for k, x, y, z in rows:
    print("  %-12s 甲 %-46s\n  %-12s 乙 %-46s\n  %-12s 丙 %-46s  乙丙同=%s" % (k, x, "", y, "", z, y == z))
print("\n  engine_sha 三位同 = %s" % (A["engine_sha256"] == B["engine_sha256"] == C["esha"]))

print("\n--- libm 探针（7 条）---")
pa, pb, pc = ea["libm_fingerprints"], eb["libm_fingerprints"], C["lm"]
for k in sorted(pa):
    x, y, z = pa[k], pb.get(k), pc.get(k)
    print("  %-22s 甲 %-24s 乙 %-24s 丙 %-24s | 甲乙%s 乙丙%s"
          % (k, x, y, z, "同" if x == y else "异(%sULP)" % ulp(x, y), "同" if y == z else "异"))
print("  libm digest: 甲乙%s  乙丙%s" % (
    "同" if ea["libm_fingerprint_digest"] == eb["libm_fingerprint_digest"] else "**异**",
    "同" if eb["libm_fingerprint_digest"] == C["ld"] else "**异**"))

print("\n--- 引擎逐位输出 per_unit ---")
qa, qb = A["result_bitwise"]["per_unit"], B["result_bitwise"]["per_unit"]
for k in sorted(qa):
    ha, hb = qa[k]["hex"], qb[k]["hex"]
    hc = (C["pu"].get(k) or [None, None])[1]
    ab = "同" if ha == hb else "**异(%sULP)**" % ulp(ha, hb)
    bc = "同" if hb == hc else "**异(%sULP)**" % ulp(hb, hc)
    ac = "同" if ha == hc else "**异(%sULP)**" % ulp(ha, hc)
    print("  %-8s 甲 %-26s\n  %-8s 乙 %-26s\n  %-8s 丙 %-26s  甲乙=%s 乙丙=%s 甲丙=%s"
          % (k, ha, "", hb, "", hc, ab, bc, ac))

print("\n--- 路由与状态 ---")
for k, ck in (("route_id", "rt"), ("computability_status", "cs"), ("unstated_dimensions_hit", "ud")):
    x, y, z = A["result_bitwise"].get(k), B["result_bitwise"].get(k), C.get(ck)
    print("  %-24s 甲=%-32s 乙=%-32s 丙=%-32s 三位同=%s" % (k, x, y, z, x == y == z))
print("\n" + "=" * 100)
print("本件只产比对素材。不判结论、不作合格主张、不作环境可用性判定。DOC-25 兑现点不变更。总体判定归 KD。")
print("=" * 100)

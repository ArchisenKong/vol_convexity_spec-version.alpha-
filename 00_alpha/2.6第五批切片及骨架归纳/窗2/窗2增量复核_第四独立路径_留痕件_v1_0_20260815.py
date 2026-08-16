# 增量复核会话·第四独立路径（自声明面反推重写，零 import 被测实现/harness/复算器）
import json, sys
sys.dont_write_bytecode = True
D = json.load(open('pkg_v1_1/entity/roll_record_declaration.json', encoding='utf-8'))
INP = json.load(open('pkg_v1_1/entity/synthetic_input.json', encoding='utf-8'))
REQ = D["record_required_refs"]; SUB = D["required_action_subtype"]
IDOM = set(D["position_ref_coordinate_key"]["domain"]); ODOM = set(D["ledger_origin_domain"])

def V(c, cont, key): return {"code": c, "locus": {"container": cont, "key": key}}

def p1(r):
    out = []
    for f in REQ:
        if f not in r or r[f] in (None, ""): out.append(V("R10", "record", f))
    if r.get("action_subtype") != SUB: out.append(V("R11", "record", "action_subtype"))
    for l in r.get("position_lots_declared", []):
        if l.get("instrument_type") not in IDOM:
            out.append(V("R12", "position_lots_declared", l["lot_id"]))
    decl = [l["lot_id"] for l in r.get("position_lots_declared", [])]
    clo, opn = r.get("closing_lots", []), r.get("opening_lots", [])
    bad = sorted({x for x in clo + opn if x not in decl})
    dup = sorted({x for x in (clo, opn) for x in x if (clo + opn).count(x) > 1 and
                  (clo.count(x) > 1 or opn.count(x) > 1)})
    for x in bad + [d for d in dup if d not in bad]: out.append(V("R03", "record", x))
    if not clo: out.append(V("R01", "record", "closing_lots"))
    if not opn: out.append(V("R01", "record", "opening_lots"))
    inter = sorted(set(clo) & set(opn))
    if inter: out.append(V("R02", "record", inter[0]))
    return out

def p2(r):
    out = []
    clo, opn = set(r.get("closing_lots", [])), set(r.get("opening_lots", []))
    mp = r.get("ledger_migration_map", [])
    dom = {m["from_lot"] for m in mp}; tgt = {m["to_lot"] for m in mp}
    sym = sorted(dom ^ clo)
    if sym: out.append(V("R04", "ledger_migration_map", sym[0]))
    for m in mp:
        if m["to_lot"] not in opn: out.append(V("R05", "ledger_migration_map", m["to_lot"]))
    org = r.get("ledger_origin", {})
    for lid in sorted(opn):
        o = org.get(lid)
        if o not in ODOM: out.append(V("R06", "ledger_origin", lid))
        elif o == "migrated" and lid not in tgt: out.append(V("R06", "ledger_origin", lid))
        elif o == "new_capital" and lid in tgt: out.append(V("R06", "ledger_origin", lid))
    b, a = r.get("function_roles_before", {}), r.get("function_roles_after", {})
    rsym = set(b) ^ set(a)
    if rsym:
        out.append(V("R07", "function_roles", min(rsym))); return out
    for role in sorted(b):
        if len(b[role]) == 0: out.append(V("R08", "function_roles_before", role))
        if len(a[role]) == 0: out.append(V("R08", "function_roles_after", role))
        if not set(b[role]) <= clo: out.append(V("R09", "function_roles_before", role))
        if not set(a[role]) <= opn: out.append(V("R09", "function_roles_after", role))
    return out

def check(r):
    v = p1(r) or p2(r)
    v = sorted(v, key=lambda x: (x["code"], x["locus"]["container"], x["locus"]["key"]))
    return {"record_id": r["record_id"], "verdict": "not_closed" if v else "closed", "violations": v}

mine = {r["record_id"]: check(r) for r in INP["records"]}
RUN = {x["record_id"]: x for x in json.load(open('pkg_v1_1/entity/outputs/run_output.json', encoding='utf-8'))["results"]}
ok = 0; diff = []
for rid in sorted(mine, key=lambda s: (s[0], int(s[1:]))):
    m, o = mine[rid], RUN[rid]
    same = (m["verdict"] == o["verdict"]) and (m["violations"] == o["violations"])
    ok += same
    print("%-4s %-11s %s %s" % (rid, m["verdict"], "MATCH" if same else "DIFF",
          "" if same else "mine=%s | run=%s" % (json.dumps(m["violations"], ensure_ascii=False),
                                               json.dumps(o["violations"], ensure_ascii=False))))
    if not same: diff.append(rid)
print("-"*62)
print("第四独立路径对表：%d/%d 一致；差异件=%s" % (ok, len(mine), diff or "无"))

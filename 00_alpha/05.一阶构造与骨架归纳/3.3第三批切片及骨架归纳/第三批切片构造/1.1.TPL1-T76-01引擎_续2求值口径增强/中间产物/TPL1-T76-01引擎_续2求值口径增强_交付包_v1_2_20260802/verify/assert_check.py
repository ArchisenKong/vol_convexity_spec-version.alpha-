"""
TPL1-T76-01 引擎 · D段合格断言脚本

判据基线一律**程序化解析自本包内源文件**（entity/input_schema.md 之三个声明块），
不使用任何人工转抄常量（T3-03 缺陷F1 教训：断言基线须独立解析源markdown）。
包自足：不读取 /mnt/project/ 或任何包外路径（W-13(6) 教训）。

失败即以**非零退出码**退出（裁决28-B(ii)，经裁决30-A 溯及既往，本包为存量义务）。

v1.1 修复面（裁决48 §4，逐项）：
  · Q-6 日志写出时序——进程启动即清空日志、逐断言即时写出并 flush，
    失败/中断运行不再残留上一次绿日志。
  · D-3 step0(ii) 与 A6 扫描面扩至**全部交付脚本**（含 verify/negative_control.py）。
  · D-4 扫描模式数据件以指纹钉定（基线载于 input_schema.md §8.1 声明面，
    非脚本内写死常量）。
  · Q-3 route_table **值层**对表（A3-b2），非仅键集。
  · 48-2 A9 组声明-实现一致性断言（六例形态：ACT/365 分母／per_lot 缩放式含
    side_sign／raw 量纲三项／期货桩零持有成本），源级与行为级双层、engine 与
    independent 双侧，基线一律取自 §5.1 CONVENTION_DECLARATION。
"""

import ast
import datetime
import hashlib
import json
import os
import re
import sys
from fractions import Fraction

from mpmath import mp, mpf, fabs

mp.dps = 60

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
E = lambda *p: os.path.join(PKG, "entity", *p)
V = lambda *p: os.path.join(HERE, *p)

TOL_B = mpf("1e-12")
CONTAINERS = ("base_valuation", "scenario_revaluation", "time_shift_revaluation")

FAILS = []
LOG = []

# --------------------------------------------------------------------------
# 日志写出时序（Q-6 订正，裁决48 §4）
# 旧形态：全部断言跑完后一次性写出 → 运行中途异常退出时磁盘留存上一次绿日志，
#         失败运行与绿日志并存（外审 SM5 实证）。
# 新形态：进程一启动即清空日志并写入运行头，逐断言即时写出并 flush。
#         任何中途退出（含判据基线解析失败之 SystemExit、未捕获异常）之后，
#         磁盘上只可能留下本次运行之部分日志，绝不可能留下上一次之绿日志。
# --------------------------------------------------------------------------
LOG_PATH = V("assert_check_log.txt")
_LOG_FH = open(LOG_PATH, "w", encoding="utf-8")
_LOG_FH.write("# assert_check 运行开始（日志已清空；逐断言即时写出）\n")
_LOG_FH.flush()


def _emit(line):
    _LOG_FH.write(line + "\n")
    _LOG_FH.flush()


def check(cond, name, detail=""):
    line = "%s  %s%s" % ("PASS" if cond else "FAIL", name,
                         ("  | " + detail) if detail else "")
    LOG.append(line)
    _emit(line)
    if not cond:
        FAILS.append(name)
    return cond


def read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


# --------------------------------------------------------------------------
# 判据基线：独立解析 entity/input_schema.md
# --------------------------------------------------------------------------
SCHEMA = read(E("input_schema.md"))


def parse_block(tag):
    m = re.search(r"```\s*\n%s\n(.*?)```" % re.escape(tag), SCHEMA, re.S)
    if not m:
        raise SystemExit("判据基线解析失败：声明块 %s 未在 input_schema.md 中找到" % tag)
    return [ln.strip() for ln in m.group(1).strip().split("\n") if ln.strip()]


DECL_TOPLEVEL = set(parse_block("OUTPUT_TOPLEVEL_DECLARATION"))
DECL_RECORD = set(parse_block("RECORD_KEY_DECLARATION"))
DECL_COMPONENT = set(parse_block("COMPONENT_KEY_DECLARATION"))

DECL_ROUTE = {}
for line in parse_block("ROUTE_DECLARATION"):
    cols = [c.strip() for c in line.split("|")]
    while len(cols) < 4:
        cols.append("")
    DECL_ROUTE[cols[0]] = {
        "route_id": cols[1],
        "computability_status": cols[2],
        "unstated_dimensions_hit": [d for d in cols[3].split(",") if d],
    }

# 计算约定声明面（§5.1，裁决48-2 兑现）——声明-实现一致性断言之判据基线
DECL_CONV = {}
for line in parse_block("CONVENTION_DECLARATION"):
    k, _, v = line.partition("|")
    DECL_CONV[k.strip()] = v.strip()

# 检测器完整性声明面（§8.1，D-4 兑现）
DECL_FP = {}
for line in parse_block("DETECTOR_FINGERPRINT_DECLARATION"):
    cols = [c.strip() for c in line.split("|")]
    DECL_FP[cols[0]] = (cols[1], cols[2])

B1_CLAUSE = ("以下为已言明最小面，未言明维度（美式行权、股息、期货保证金形态、"
             "day count等）不构成规格封闭，留引擎切片撞墙")

HARNESS_OUT = json.loads(read(E("harness_output.json")))
INDEP = json.loads(read(V("independent_expected.json")))
INPUT = json.loads(read(E("input_data.json")))


# --------------------------------------------------------------------------
# step 0 · 前置合规断言（先于数值比对）
# --------------------------------------------------------------------------
def strip_code(src):
    """剥离注释与docstring，仅留实际代码。"""
    out_lines = []
    for ln in src.split("\n"):
        out_lines.append(re.sub(r"#.*$", "", ln))
    stripped = "\n".join(out_lines)
    try:
        tree = ast.parse(stripped)
    except SyntaxError:
        return stripped
    spans = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef,
                             ast.ClassDef)):
            doc = ast.get_docstring(node, clean=False)
            if doc:
                first = node.body[0]
                spans.append((first.lineno, first.end_lineno))
    lines = stripped.split("\n")
    for a, b in spans:
        for i in range(a - 1, b):
            lines[i] = ""
    return "\n".join(lines)


PATTERNS = json.loads(read(V("scan_patterns.json")))
FORBIDDEN_KEYWORDS = PATTERNS["forbidden_datasource_keywords"]
FORBIDDEN_IMPORT_RE = re.compile(PATTERNS["forbidden_import_regex"], re.M)

# 扫描面（D-3 订正，裁决48 §4）：**全部交付脚本**（entity/ ＋ verify/ 两侧之
# 可执行 .py 件，含 verify/negative_control.py——外审 S5 实证其此前完全逃逸）。
# verify/scan_patterns.json 为模式数据件，按构造排除（否则模式表逐条自命中）；
# 其内容之钉定改由 §8.1 指纹断言承担（D-4）。
# 续2新增 verify/regression_check.py（F-1封闭规则：实际交付之任何其他脚本自动入面，
# 任务包§3 F-1）——本脚本亦为可执行交付脚本，纳入扫描与措辞审计两面。
# 续2续修复新增 verify/build_provenance.py（同一封闭规则自动入面）。
SCANNED = ["entity/engine.py", "entity/harness.py",
           "verify/independent_recompute.py", "verify/assert_check.py",
           "verify/negative_control.py", "verify/regression_check.py",
           "verify/build_provenance.py"]
SCAN_EXCLUDED = ["verify/scan_patterns.json"]

raw_hits, stripped_hits = {}, {}
for rel in SCANNED:
    src = read(os.path.join(PKG, rel))
    st = strip_code(src)
    raw_hits[rel] = [k for k in FORBIDDEN_KEYWORDS if k in src]
    hits = [k for k in FORBIDDEN_KEYWORDS if k in st]
    hits += [m.group(1) for m in FORBIDDEN_IMPORT_RE.finditer(st)]
    stripped_hits[rel] = hits

check(INPUT.get("_data_source") == "synthetic_hand_constructed",
      "step0(i) input 为人造构造",
      "_data_source=%r" % INPUT.get("_data_source"))
check(HARNESS_OUT.get("_data_source") == "synthetic_hand_constructed",
      "step0(i-b) 输出承载人造标记")
check(all(not v for v in stripped_hits.values()),
      "step0(ii) 剥离注释/docstring后零数据源接入命中（扫描面＝全部交付脚本%d件）"
      % len(SCANNED),
      "剥离后=%s；剥离前留痕=%s" % (stripped_hits, {k: v for k, v in raw_hits.items() if v}))

# step0(ii-b) · 检测器完整性：模式数据件内容以指纹钉定（D-4，裁决48 §4）
fp_ok, fp_detail = True, []
for rel, (algo, want) in DECL_FP.items():
    with open(os.path.join(PKG, rel), "rb") as fh:
        got = hashlib.new(algo, fh.read()).hexdigest()
    fp_detail.append("%s %s=%s" % (rel, algo, got))
    if got != want:
        fp_ok = False
check(fp_ok, "step0(ii-b) 外置数据件指纹＝§8.1声明面钉定值（含scan_patterns.json与"
      "baseline_v1_1_reference.json两件，续2续修复F-5双钉补齐，D-3封堵；检测器/判据"
      "基线锚均不可被静默削弱或改写）",
      "；".join(fp_detail))

indep_src = read(V("independent_recompute.py"))
indep_code = strip_code(indep_src)
check(("import engine" not in indep_code) and ("from engine" not in indep_code)
      and ("harness_output" not in indep_code) and ("import harness" not in indep_code),
      "step0(iii) 独立复算未import被测模块、未读harness产物",
      "剥离前 'harness' 字样命中%d处（均落在docstring独立性自述内）"
      % indep_src.count("harness"))


# --------------------------------------------------------------------------
# A1 · 输出形态封闭（裁决39-B / 38-2 第三可检层次）
# --------------------------------------------------------------------------
top = set(HARNESS_OUT.keys())
check(top == DECL_TOPLEVEL, "A1 输出顶层键集＝declaration声明集",
      "多出=%s；缺失=%s" % (sorted(top - DECL_TOPLEVEL), sorted(DECL_TOPLEVEL - top)))

rec_ok, comp_ok = True, True
for c in CONTAINERS:
    for r in HARNESS_OUT[c]:
        if set(r.keys()) != DECL_RECORD:
            rec_ok = False
        for layer in ("per_unit", "per_lot"):
            if set(r[layer].keys()) != DECL_COMPONENT:
                comp_ok = False
check(rec_ok, "A1-b 每条记录键集＝RECORD_KEY_DECLARATION")
check(comp_ok, "A1-c per_unit/per_lot 分量键集＝COMPONENT_KEY_DECLARATION")


# --------------------------------------------------------------------------
# A2 · 契约① 供给物语义类型：5全集 raw Greeks ＋ V(t)
# --------------------------------------------------------------------------
need = {"delta", "gamma", "vega", "theta", "rho", "value"}
check(DECL_COMPONENT == need, "A2 契约①分量声明＝5全集＋V(t)")
numeric_ok = all(isinstance(r[l][k], (int, float))
                 for c in CONTAINERS for r in HARNESS_OUT[c]
                 for l in ("per_unit", "per_lot") for k in need)
check(numeric_ok, "A2-b 全部分量为实产数值（非占位null）")


# --------------------------------------------------------------------------
# A3 · 契约② 品种感知路由身份
# --------------------------------------------------------------------------
GAP_DOMAIN = {"spot", "spot_etf", "futures", "index",
              "european_option", "american_option"}
check(set(DECL_ROUTE.keys()) == GAP_DOMAIN,
      "A3 路由声明覆盖缺口原文六品种域", "声明=%s" % sorted(DECL_ROUTE))
check(set(HARNESS_OUT["route_table"].keys()) == GAP_DOMAIN,
      "A3-b 输出 route_table 覆盖六品种域（未静默收窄）")

# A3-b2 · route_table **值层**对表（Q-3 兑现，裁决48 §4）
# 旧形态 A3-b 仅检键集，route_table 之 computability_status／unstated_dimensions_hit
# 可被集体改标而不被检出（外审 SM6 实证）。本断言逐路由三字段与声明块对表。
rt_bad = []
for ic in sorted(GAP_DOMAIN):
    got = HARNESS_OUT["route_table"].get(ic, {})
    want = DECL_ROUTE[ic]
    for f in ("route_id", "computability_status", "unstated_dimensions_hit"):
        if got.get(f) != want[f]:
            rt_bad.append("%s.%s: 输出=%r 声明=%r" % (ic, f, got.get(f), want[f]))
check(not rt_bad, "A3-b2 route_table 逐路由值层与ROUTE_DECLARATION对表（三字段）",
      "不符=%s" % (rt_bad if rt_bad else "无"))

route_ok, status_ok, exercised = True, True, set()
for c in CONTAINERS:
    for r in HARNESS_OUT[c]:
        d = DECL_ROUTE[r["instrument_class"]]
        exercised.add(r["instrument_class"])
        if r["route_id"] != d["route_id"]:
            route_ok = False
        if (r["computability_status"] != d["computability_status"]
                or r["unstated_dimensions_hit"] != d["unstated_dimensions_hit"]):
            status_ok = False
check(route_ok, "A3-c 逐笔 route_id 与路由声明一致（路由身份可辨识）")
check(status_ok, "A3-d 逐笔可算性标注与未言明维度标注与声明一致（降格标注在场）")
check(exercised == GAP_DOMAIN, "A3-e 人造input实跑覆盖全部六品种",
      "实跑=%s" % sorted(exercised))
check(len({d["route_id"] for d in DECL_ROUTE.values()}) == 4,
      "A3-f 四条互异求值路径在场")


# --------------------------------------------------------------------------
# A4 · 契约④ 已言明最小面 ＋ 45-B1 条款措辞逐字在场
# --------------------------------------------------------------------------
check(B1_CLAUSE in SCHEMA, "A4 45-B1条款措辞逐字载于 input_schema.md")
check(B1_CLAUSE in read(E("engine.py")), "A4-b 45-B1条款措辞逐字载于 engine.py")
eng = read(E("engine.py"))
m = re.search(r"STATED_FACE_FIELDS = \((.*?)\)", eng, re.S)
consumed = set(re.findall(r'"([a-z_]+)"', m.group(1)))
# A4-c基线（续2续修复D-5②，M22封堵）：改为独立解析 §2 声明面（原形态为脚本内
# 写死allowed集合，与schema行38同源声明脱钩，故schema声明面漂移零区分力——
# 外审变异M22逃逸实证。现基线程序化取自 input_schema.md §2 之
# "本实体求值路径实际消费之字段集"声明行，非脚本内写死常量。
m4c = re.search(
    r"本实体求值路径实际消费之字段集\*\*（STATED_FACE_FIELDS，[^）]*）：\s*\n(.*?)\n\n",
    SCHEMA, re.S)
if not m4c:
    raise SystemExit("判据基线解析失败：§2 STATED_FACE_FIELDS 声明行未在 input_schema.md 中找到")
allowed = set(re.findall(r"`([a-z_]+)`", m4c.group(1)))
check(consumed == allowed,
      "A4-c 求值消费字段集＝schema §2声明面（程序化解析非写死集合；M22封堵，D-5②）",
      "engine消费=%s；schema声明=%s" % (sorted(consumed), sorted(allowed)))
excluded = {"underlying", "leg_type", "open_interest"}
check(not (consumed & excluded), "A4-d 坐标/保留字段未进入求值路径")


# --------------------------------------------------------------------------
# A11/A12 · C07/C08口径（裁决57-5扩域裁定，48-2通道之外延；源级机械核验）
#
# 立法背景：外审M22/C07/C08逃逸例证实，DECL_ROUTE（schema声明）与engine.py之
# UNSTATED_DIMENSIONS/COMPUTABILITY若被同步协同篡改（如C07/C08两侧同标），
# 既有A3-b2（route_table值层对表，declaration vs harness_output）与A3-c/A3-d
# （逐笔一致性）对此类"两侧协同同改"逃逸无区分力——两侧同改后彼此仍自洽。
# 本组断言之基线取自**engine.py路由派发函数体本身**（_DISPATCH链追索，是否
# 源级消费`lot["dividend_yield"]`），该基线不与UNSTATED_DIMENSIONS/
# COMPUTABILITY两声明字典同源，故可作为独立于"协同篡改"之判据锚。裁决57-5：
# 该核验技术上可机械化（源级追索_DISPATCH链），扩入48-2"可建而未建之
# 声明-实现一致性断言通道"定义域，不落35-A固有上限。
# --------------------------------------------------------------------------
m_disp = re.search(r"_DISPATCH\s*=\s*\{(.*?)\}", eng, re.S)
DISPATCH_MAP = dict(re.findall(r'"([a-zA-Z_]+)"\s*:\s*(_eval_\w+)', m_disp.group(1)))


def _func_body(name, src):
    mm = re.search(r"^def %s\(.*?\n(?:(?: {4}.*)?\n)*" % re.escape(name), src, re.M)
    return mm.group(0) if mm else ""


def _consumes_dividend_yield(func_name, src, seen=None):
    """源级追索：函数体是否直接消费lot["dividend_yield"]，或委派给消费它的函数。"""
    seen = seen if seen is not None else set()
    if not func_name or func_name in seen:
        return False
    seen.add(func_name)
    body = _func_body(func_name, src)
    if ('lot["dividend_yield"]' in body) or ("lot['dividend_yield']" in body):
        return True
    return any(_consumes_dividend_yield(callee, src, seen)
               for callee in re.findall(r"(_eval_\w+)\(", body) if callee != func_name)


q_carry_bad, closed_face_bad = [], []
for ic, route in sorted(DECL_ROUTE.items()):
    fn = DISPATCH_MAP.get(route["route_id"])
    consumes_q = _consumes_dividend_yield(fn, eng)
    hit = route["unstated_dimensions_hit"]
    # A11〔C07口径〕：源级实际消费q，则该路由不得仍将dividend_carry标为未言明维度
    #（"标注去留 vs 实际是否消费"须一致——防两侧协同回标而机械面零检出）。
    if consumes_q and ("dividend_carry" in hit):
        q_carry_bad.append("%s（route_id=%s，派发函数=%s）：源级消费dividend_yield，"
                           "但unstated_dimensions_hit仍标dividend_carry" % (ic, route["route_id"], fn))
    # A12〔C08口径〕：computability_status=closed_on_stated_face 依三分判别§3自身
    # 定义须以零unstated_dimensions_hit为前提，不得宣称闭合而仍留任一未言明维度
    #（含day_count_convention——防升标闭合态而遗留维度未消解）。
    if route["computability_status"] == "closed_on_stated_face" and hit:
        closed_face_bad.append("%s：标注closed_on_stated_face但unstated_dimensions_hit=%s非空"
                               % (ic, hit))

check(not q_carry_bad,
      "A11〔续2续修复，57-5，C07口径〕路由dividend_carry标注与_DISPATCH链源级"
      "q消费实况一致（源级消费q者不得仍标该维度未言明）",
      "不符=%s" % (q_carry_bad or "无"))
check(not closed_face_bad,
      "A12〔续2续修复，57-5，C08口径〕closed_on_stated_face标注以零"
      "unstated_dimensions_hit为前提（不得宣称闭合而遗留未言明维度，含day_count_convention）",
      "不符=%s" % (closed_face_bad or "无"))


# --------------------------------------------------------------------------
# A5 · 契约⑤ 数据源边界：输入面零 vendor 派生量
# --------------------------------------------------------------------------
VENDOR_KEYS = {"delta", "gamma", "vega", "theta", "rho", "model_price",
               "theo_price", "vendor_iv", "greeks", "mark_price_model"}
in_keys = set()
for lot in INPUT["lots"]:
    in_keys |= set(lot.keys())
check(not (in_keys & VENDOR_KEYS), "A5 输入面与vendor派生量键名集之交为空",
      "输入键=%s" % sorted(in_keys))


# --------------------------------------------------------------------------
# A6 · 契约⑥ 措辞审计（审计表行94 证伪证据形态）
# --------------------------------------------------------------------------
CLAIM_PATTERNS = PATTERNS["truth_claim_patterns"]
NEG_MARKERS = PATTERNS["negation_markers"]
NEG_WIN = PATTERNS["negation_window_chars"]
audited = ["entity/engine.py", "entity/harness.py", "entity/input_schema.md",
           "verify/independent_recompute.py", "verify/assert_check.py",
           "verify/negative_control.py", "verify/regression_check.py",
           "verify/build_provenance.py"]
           # D-3 订正：扩至全部交付脚本；续2新增regression_check.py同步纳入；
           # 续2续修复新增build_provenance.py同步纳入
affirmative, negated = [], []
for rel in audited:
    txt = read(os.path.join(PKG, rel))
    for pat in CLAIM_PATTERNS:
        for mm in re.finditer(re.escape(pat), txt):
            ctx = txt[max(0, mm.start() - NEG_WIN):mm.start()]
            (negated if any(n in ctx for n in NEG_MARKERS) else affirmative
             ).append("%s::%s::…%s|%s" % (rel, pat, ctx[-10:].replace("\n", " "), pat))
check(not affirmative, "A6 措辞审计：零肯定式真理源/获利合法性宣称",
      "否定语境命中%d处（留痕）；肯定式=%s；扫描排除件=%s" % (len(negated), affirmative, SCAN_EXCLUDED))


# --------------------------------------------------------------------------
# A7 · 数值比对（成分级容差分派）＋ 量纲否定式判别
# --------------------------------------------------------------------------
rows = [["container", "lot_id", "layer", "component", "harness",
         "independent", "tol_subcaliber", "rel_diff", "verdict"]]
n_a = n_b = n_bad = 0
worst = mpf(0)

for c in CONTAINERS:
    hmap = {r["lot_id"]: r for r in HARNESS_OUT[c]}
    for ir in INDEP[c]:
        hr = hmap[ir["lot_id"]]
        kind = ir["numeric_kind"]
        for layer in ("per_unit", "per_lot"):
            for k in sorted(DECL_COMPONENT):
                hv = hr[layer][k]
                iv = ir[layer][k]
                if kind == "exact_rational":
                    ok = Fraction(str(hv)) == Fraction(iv)
                    rel, sub = "0" if ok else "nonzero", "(a) bit-exact"
                    n_a += 1
                else:
                    h, i = mpf(str(hv)), mpf(iv)
                    if i == 0:
                        ok, r_ = (h == 0), mpf(0)
                    else:
                        r_ = fabs(h - i) / fabs(i)
                        ok = r_ <= TOL_B
                    worst = max(worst, r_)
                    rel, sub = mp.nstr(r_, 6), "(b) rel<=1e-12"
                    n_b += 1
                if not ok:
                    n_bad += 1
                rows.append([c, ir["lot_id"], layer, k, repr(hv), iv, sub,
                             rel, "OK" if ok else "OUT"])

check(n_bad == 0, "A7 全量分量比对（%d项：(a)%d ／ (b)%d）" % (n_a + n_b, n_a, n_b),
      "越限%d项；(b)类最大相对diff=%s" % (n_bad, mp.nstr(worst, 6)))

with open(V("comparison_table.tsv"), "w", encoding="utf-8") as fh:
    for r in rows:
        fh.write("\t".join(str(x) for x in r) + "\n")

# 量纲否定式判别：若产出为 vega/100、theta/365、rho/100 形态，本组断言须失败
neg_ok = True
for c in CONTAINERS:
    hmap = {r["lot_id"]: r for r in HARNESS_OUT[c]}
    for ir in INDEP[c]:
        if ir["numeric_kind"] != "transcendental":
            continue
        hr = hmap[ir["lot_id"]]
        for k, factor in (("vega", 100), ("theta", 365), ("rho", 100)):
            i = mpf(ir["per_unit"][k])
            if i == 0:
                continue
            scaled = mpf(str(hr["per_unit"][k])) * factor
            if fabs(scaled - i) / fabs(i) <= TOL_B:
                neg_ok = False
check(neg_ok, "A7-b 量纲否定式判别：产出非 vega/100、theta/日、rho/100 缩放形态")


# --------------------------------------------------------------------------
# A8 · 重估形态自洽（同签名再次求值，零新增接口参数）
# --------------------------------------------------------------------------
lens = {c: len(HARNESS_OUT[c]) for c in CONTAINERS}
check(len(set(lens.values())) == 1 and lens["base_valuation"] == len(INPUT["lots"]),
      "A8 三容器逐笔齐备（情景重估／时点推移覆盖全部lot）", str(lens))
sig = re.search(r"def evaluate_lot\((.*?)\)", eng).group(1)
check(sig.strip() == "lot", "A8-b 引擎签名未因重估需求增参",
      "evaluate_lot(%s)" % sig)

opt_moved = all(
    mpf(str(next(r for r in HARNESS_OUT["time_shift_revaluation"]
                 if r["lot_id"] == lid)["per_unit"]["value"]))
    != mpf(str(next(r for r in HARNESS_OUT["base_valuation"]
                    if r["lot_id"] == lid)["per_unit"]["value"]))
    for lid in ("L05", "L06", "L07", "L08"))
check(opt_moved, "A8-c 时点推移使期权估值变动（T-24 V(t0)/V(t1) 消费面可用）")


# --------------------------------------------------------------------------
# A9 · 声明-实现一致性断言（裁决48-2 兑现）
#
# 覆盖面钉死＝48-2 所限定之六例形态（外审逃逸例 C1／C2／C4／C7／C8b／C10）：
#   ACT/365 分母、per_lot 缩放式（含 side_sign）、raw 量纲（vega per 1.0σ／
#   theta 年计／rho per 1.0r／零缩放）、期货桩"不引入持有成本"。
#   **不扩至 C3（情景构造式两侧同形）**——该例维持归数值比对方法固有上限（35-A）。
#
# 基线一律取自 entity/input_schema.md §5.1 CONVENTION_DECLARATION（程序化解析），
# 断言施于 entity/engine.py 与 verify/independent_recompute.py **双侧**：
#   源级层——两侧实现之字面量/表达式与声明对表；
#   行为级层——两侧产物（harness_output.json ／ independent_expected.json）
#             须满足由声明值参数化之恒等式。
# 两层皆以声明面为锚，故两侧协同同改任一项仍 FAIL。
# --------------------------------------------------------------------------
DEN = int(DECL_CONV["day_count_denominator"])
SIGN_MAP = {"long": int(DECL_CONV["side_sign_long"]),
            "short": int(DECL_CONV["side_sign_short"])}
SCALE_FACTORS = [f.strip() for f in
                 DECL_CONV["per_lot_scaling_factors"].split(",") if f.strip()]
OPT_ROUTES = set(r.strip() for r in
                 DECL_CONV["option_identity_routes"].split(",") if r.strip())
LIN_ROUTES = set(r.strip() for r in
                 DECL_CONV["linear_identity_routes"].split(",") if r.strip())

indep_code_src = read(V("independent_recompute.py"))

# --- A9-a 源级 · day count 分母双侧对表 -----------------------------------
m_eng = re.search(r"DAY_COUNT_DENOMINATOR\s*=\s*(\d+)", eng)
m_ind = re.search(r"mpf\(_dte\([^\n]*?\)\)\s*/\s*(\d+)", indep_code_src)
den_eng = int(m_eng.group(1)) if m_eng else None
den_ind = int(m_ind.group(1)) if m_ind else None
check(den_eng == DEN and den_ind == DEN,
      "A9-a〔C1〕day count 分母：engine.py／independent_recompute.py 双侧＝声明值",
      "声明=%s；engine=%s；independent=%s" % (DEN, den_eng, den_ind))

# --- A9-b 源级 · per_lot 缩放因子集双侧对表 -------------------------------
def _scale_expr(src):
    mm = re.search(r"^\s*scale\s*=\s*(.+)$", src, re.M)
    return mm.group(1) if mm else ""


def _has_factor(expr, f):
    if f == "side_sign":
        return bool(re.search(r"_side_sign|\bsign\b", expr))
    return f in expr


sc_eng, sc_ind = _scale_expr(eng), _scale_expr(indep_code_src)
miss = [(side, f) for side, ex in (("engine", sc_eng), ("independent", sc_ind))
        for f in SCALE_FACTORS if not _has_factor(ex, f)]
check(not miss,
      "A9-b〔C4〕per_lot 缩放因子集：双侧 scale 表达式含全部声明因子%s" % SCALE_FACTORS,
      "缺失=%s；engine: %s；independent: %s" % (miss or "无", sc_eng, sc_ind))


# --- 行为级层：市场坐标重建（自 input_data.json，非取自被测中间量）--------
def _dte_ck(expiry, vd):
    a = datetime.date(*[int(x) for x in expiry.split("-")])
    b = datetime.date(*[int(x) for x in vd.split("-")])
    return (a - b).days


LOTS = {l["lot_id"]: l for l in INPUT["lots"]}
_sh, _ts = INPUT["scenario_shock"], INPUT["time_shift"]
CTX = {"base_valuation": (INPUT["valuation_date"], 1.0, 0.0),
       "scenario_revaluation": (INPUT["valuation_date"],
                                1.0 + _sh["spot_shock_pct"],
                                _sh["vol_shock_points"]),
       "time_shift_revaluation": (_ts["valuation_date_t1"], 1.0, 0.0)}

INDEP_MAP = {c: {r["lot_id"]: r for r in INDEP[c]} for c in CONTAINERS}
HARN_MAP = {c: {r["lot_id"]: r for r in HARNESS_OUT[c]} for c in CONTAINERS}


def _rel(a, b):
    a, b = mpf(str(a)), mpf(str(b))
    if b == 0:
        return mpf(0) if a == 0 else mpf("1e99")
    return fabs(a - b) / fabs(b)


def _both_sides(container, lot_id):
    """返回 (被测侧 per_unit, 独立侧 per_unit) 之 (标签, 分量字典) 二元组序列。"""
    return (("engine", HARN_MAP[container][lot_id]["per_unit"]),
            ("independent", INDEP_MAP[container][lot_id]["per_unit"]))


# --- A9-1〔C1/rho〕rho = T·(S·delta − V)，反解分母与声明对表 ---------------
bad_rho, bad_den = [], []
for c, (vd, sfac, vadd) in CTX.items():
    for lid, L in LOTS.items():
        if DECL_ROUTE[L["instrument_class"]]["route_id"] not in OPT_ROUTES:
            continue
        S = mpf(str(L["spot"])) * mpf(str(sfac))
        T = mpf(_dte_ck(L["expiry"], vd)) / DEN
        for tag, u in _both_sides(c, lid):
            V_, d, rh = mpf(str(u["value"])), mpf(str(u["delta"])), mpf(str(u["rho"]))
            pred = T * (S * d - V_)
            if _rel(rh, pred) > TOL_B:
                bad_rho.append("%s/%s/%s rel=%s" % (c, lid, tag,
                                                    mp.nstr(_rel(rh, pred), 4)))
            base = S * d - V_
            if base != 0:
                den_implied = mpf(_dte_ck(L["expiry"], vd)) / (rh / base)
                if _rel(den_implied, mpf(DEN)) > mpf("1e-9"):
                    bad_den.append("%s/%s/%s 反解分母=%s"
                                   % (c, lid, tag, mp.nstr(den_implied, 8)))
check(not bad_rho and not bad_den,
      "A9-1〔C1+rho量纲〕rho＝T·(S·δ−V) 双侧成立，且由产出反解之 day count 分母＝声明值%d" % DEN,
      "恒等式越限=%s；分母不符=%s" % (bad_rho or "无", bad_den or "无"))

# --- A9-2〔C7〕vega = gamma·S²·σ·T（钉定 vega per 1.0σ）--------------------
bad_vega = []
for c, (vd, sfac, vadd) in CTX.items():
    for lid, L in LOTS.items():
        if DECL_ROUTE[L["instrument_class"]]["route_id"] not in OPT_ROUTES:
            continue
        S = mpf(str(L["spot"])) * mpf(str(sfac))
        sig = mpf(str(L["implied_vol"])) + mpf(str(vadd))
        T = mpf(_dte_ck(L["expiry"], vd)) / DEN
        for tag, u in _both_sides(c, lid):
            pred = mpf(str(u["gamma"])) * S * S * sig * T
            if _rel(mpf(str(u["vega"])), pred) > TOL_B:
                bad_vega.append("%s/%s/%s rel=%s"
                                % (c, lid, tag,
                                   mp.nstr(_rel(mpf(str(u["vega"])), pred), 4)))
check(not bad_vega,
      "A9-2〔C7〕vega＝γ·S²·σ·T 双侧成立（vega_unit＝%s，非 per 1%% 缩放）"
      % DECL_CONV["vega_unit"], "越限=%s" % (bad_vega or "无"))

# --- A9-3〔C8b〕BS-PDE（续2推广，含q）：theta + ½σ²S²γ + (r−q)Sδ − rV = 0 ------
# q逐笔取自该lot声明值（非全局CONVENTION_DECLARATION标量，见schema§5.1续2订正说明）；
# q=0时代数退化至增强前原式，故本断言同时覆盖q=0与q≠0两种情形，无需分支。
bad_theta = []
for c, (vd, sfac, vadd) in CTX.items():
    for lid, L in LOTS.items():
        if DECL_ROUTE[L["instrument_class"]]["route_id"] not in OPT_ROUTES:
            continue
        S = mpf(str(L["spot"])) * mpf(str(sfac))
        sig = mpf(str(L["implied_vol"])) + mpf(str(vadd))
        r_ = mpf(str(L["risk_free_rate"]))
        q_ = mpf(str(L["dividend_yield"]))
        for tag, u in _both_sides(c, lid):
            th, g = mpf(str(u["theta"])), mpf(str(u["gamma"]))
            d, V_ = mpf(str(u["delta"])), mpf(str(u["value"]))
            resid = th + sig * sig * S * S * g / 2 + (r_ - q_) * S * d - r_ * V_
            if fabs(resid) / fabs(th) > TOL_B:
                bad_theta.append("%s/%s/%s rel=%s"
                                 % (c, lid, tag, mp.nstr(fabs(resid) / fabs(th), 4)))
check(not bad_theta,
      "A9-3〔C8b〕BS-PDE 残差双侧为零（含q推广形态；theta_unit＝%s，非按日计）"
      % DECL_CONV["theta_unit"], "越限=%s" % (bad_theta or "无"))

# --- A9-6〔续2〕q承接位声明-实现一致性（源级）--------------------------------
q_field = DECL_CONV["dividend_yield_field"]
eng_has_q = ('lot["%s"]' % q_field) in eng or ("lot['%s']" % q_field) in eng
ind_has_q = (('lot["%s"]' % q_field) in indep_code_src
             or ("lot['%s']" % q_field) in indep_code_src)
check(eng_has_q and ind_has_q,
      "A9-6〔续2〕q承接位（%s）双侧源码消费在场（声明-实现一致性，源级）" % q_field,
      "engine=%s；independent=%s" % (eng_has_q, ind_has_q))

# --- A9-4〔C2〕per_lot ＝ per_unit × multiplier × quantity × side_sign -----
bad_scale = []
for c in CONTAINERS:
    for lid, L in LOTS.items():
        sign = SIGN_MAP[L["side"]]
        factor = mpf(int(L["multiplier"]) * int(L["quantity"]) * sign)
        for tag, rec in (("engine", HARN_MAP[c][lid]),
                         ("independent", INDEP_MAP[c][lid])):
            for k in sorted(DECL_COMPONENT):
                pu, pl = mpf(str(rec["per_unit"][k])), mpf(str(rec["per_lot"][k]))
                if _rel(pl, pu * factor) > TOL_B:
                    bad_scale.append("%s/%s/%s/%s" % (c, lid, tag, k))
check(not bad_scale,
      "A9-4〔C2〕per_lot 逐分量＝per_unit×multiplier×quantity×side_sign 双侧成立"
      "（side_sign: long=%d／short=%d，含 V(t)）"
      % (SIGN_MAP["long"], SIGN_MAP["short"]),
      "不符=%s" % (bad_scale or "无"))

# --- A9-5〔C10〕期货桩零持有成本：per_unit 与标的报价恒等，五希腊(1,0,0,0,0) --
bad_carry = []
for c, (vd, sfac, vadd) in CTX.items():
    for lid, L in LOTS.items():
        if DECL_ROUTE[L["instrument_class"]]["route_id"] not in LIN_ROUTES:
            continue
        S = mpf(str(L["spot"])) * mpf(str(sfac))
        for tag, u in _both_sides(c, lid):
            if _rel(mpf(str(u["value"])), S) > TOL_B:
                bad_carry.append("%s/%s/%s value≠spot" % (c, lid, tag))
            if _rel(mpf(str(u["delta"])), mpf(1)) > TOL_B:
                bad_carry.append("%s/%s/%s delta≠1" % (c, lid, tag))
            for k in ("gamma", "vega", "theta", "rho"):
                if mpf(str(u[k])) != 0:
                    bad_carry.append("%s/%s/%s %s≠0" % (c, lid, tag, k))
check(not bad_carry,
      "A9-5〔C10〕线性/期货桩路由零持有成本（futures_stub_carry＝%s）：双侧 per_unit"
      "＝(spot,1,0,0,0,0)" % DECL_CONV["futures_stub_carry"],
      "不符=%s" % (bad_carry or "无"))


# --------------------------------------------------------------------------
# A10 · 产物新鲜度（续2续修复新增，D-4/E-1封堵）
#
# 外审E-1实证：engine.py注入两处实质变异后不重跑harness.py/independent_recompute.py/
# regression_check.py，直接跑本脚本——40/40 PASS，exit=0。此前全链无任何机制核证
# harness_output.json／independent_expected.json／regression_q0_output.json
# 系当前源码/输入之产出（无源件指纹回写、无产出时序核验、无构建序强制）。
#
# 判据基线＝verify/build_provenance.json（由verify/build_provenance.py在
# harness.py／independent_recompute.py／regression_check.py全部产出**之后**
# 一次性生成，记录当时engine.py/input_data.json/independent_recompute.py三份
# 源码-输入之SHA256，与harness_output.json/independent_expected.json/
# regression_q0_output.json三份产物之SHA256）。核验：当前重算之六项SHA256须与
# 钉定值逐一一致。任一失配即证明"源已变而产物未随动"（E-1型陈旧产物通道）或
# "产物遭直接篡改"。independent_expected.json锚取其自身生成脚本
# （independent_recompute.py）而非engine.py——维持D段②"不import被测模块"之
# 独立性纪律，设计选择详见verify/build_provenance.py docstring与本根裁定登记。
# --------------------------------------------------------------------------
PROV_PATH = V("build_provenance.json")
check(os.path.exists(PROV_PATH),
      "A10前置：verify/build_provenance.json 在场（产物新鲜度钉定件）")
PROV = json.loads(read(PROV_PATH))

PROV_TARGETS = [
    ("engine_py_sha256",                E("engine.py")),
    ("input_data_sha256",               E("input_data.json")),
    ("independent_recompute_py_sha256", V("independent_recompute.py")),
    ("harness_output_sha256",           E("harness_output.json")),
    ("independent_expected_sha256",     V("independent_expected.json")),
    ("regression_q0_output_sha256",     V("regression_q0_output.json")),
]
prov_bad = []
for key, path in PROV_TARGETS:
    with open(path, "rb") as fh:
        got = hashlib.sha256(fh.read()).hexdigest()
    want = PROV.get(key)
    if got != want:
        prov_bad.append("%s：钉定=%s 当前=%s" % (key, want, got))
check(not prov_bad,
      "A10 产物新鲜度：engine.py/input_data.json/independent_recompute.py三份源码-输入"
      "与harness_output.json/independent_expected.json/regression_q0_output.json三份"
      "产物之当前SHA256均与build_provenance.json钉定值一致（源变而产物未随动，或产物"
      "遭直接篡改，即此处失配——D-4/E-1封堵）",
      "失配=%s" % (prov_bad or "无"))


# --------------------------------------------------------------------------
# S-1 · 增量封闭（续2新增，任务包§3语义层判据；机械前哨＝regression_check.py
# 产出之双件：q=0退化回归 ＋ 底版-增强版diff面清单）。regression_check.py须
# 已先行运行产出 regression_q0_output.json 与 baseline_diff_table.tsv，本节
# 读取其产出并纳入主断言链（而非仅作构造侧留痕自查，任务包§3明定S-1含"断言"）。
# --------------------------------------------------------------------------
Q0_PATH = V("regression_q0_output.json")
BASELINE_PATH = V("baseline_v1_1_reference.json")
DIFF_TABLE_PATH = V("baseline_diff_table.tsv")

check(os.path.exists(Q0_PATH) and os.path.exists(BASELINE_PATH),
      "S-1 前置：regression_check.py 产出件与回归基准参照件均在场",
      "q0产出=%s；基准参照=%s" % (os.path.exists(Q0_PATH), os.path.exists(BASELINE_PATH)))

Q0_OUT = json.loads(read(Q0_PATH))
BASELINE_REF = json.loads(read(BASELINE_PATH))

s1_q0_bad = []
for c in CONTAINERS:
    bmap = {r["lot_id"]: r for r in BASELINE_REF[c]}
    for r in Q0_OUT[c]:
        b = bmap[r["lot_id"]]
        for layer in ("per_unit", "per_lot"):
            for k in sorted(DECL_COMPONENT):
                if r[layer][k] != b[layer][k]:
                    s1_q0_bad.append("%s/%s/%s/%s q0=%r baseline=%r"
                                     % (c, r["lot_id"], layer, k, r[layer][k], b[layer][k]))
check(not s1_q0_bad,
      "S-1a q=0退化回归：强制q=0之增强引擎产出与v1.1原始产出逐字节一致",
      "不符=%s" % (s1_q0_bad or "无"))

# S-1b 变更面封闭：非期权路由（spot/spot_etf/index/futures）逐笔逐分量须与
# baseline v1.1 零变动（实际交付harness_output.json，真实q值，非q0变体）
OPTION_IC = {"european_option", "american_option"}
s1_scope_bad = []
for c in CONTAINERS:
    bmap = {r["lot_id"]: r for r in BASELINE_REF[c]}
    for r in HARNESS_OUT[c]:
        if r["instrument_class"] in OPTION_IC:
            continue
        b = bmap[r["lot_id"]]
        for layer in ("per_unit", "per_lot"):
            for k in sorted(DECL_COMPONENT):
                if r[layer][k] != b[layer][k]:
                    s1_scope_bad.append("%s/%s/%s/%s" % (c, r["lot_id"], layer, k))
check(not s1_scope_bad,
      "S-1b 变更面封闭：非期权路由（spot/spot_etf/index/futures）与baseline v1.1零变动",
      "不符=%s" % (s1_scope_bad or "无"))

check(os.path.exists(DIFF_TABLE_PATH),
      "S-1c 底版-增强版diff面清单件已产出（人工可核验件，见 baseline_diff_table.tsv）")


# --------------------------------------------------------------------------
# 收尾
# --------------------------------------------------------------------------
report = "\n".join(LOG)
_emit("")
_emit("失败项：%s" % (FAILS if FAILS else "无"))
_emit("# assert_check 运行结束（断言数=%d，失败=%d）" % (len(LOG), len(FAILS)))
_LOG_FH.close()
print(report)
print("\n失败项：%s" % (FAILS if FAILS else "无"))
sys.exit(1 if FAILS else 0)

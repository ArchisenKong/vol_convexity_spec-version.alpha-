"""
T3-17 wing effectiveness -- verify/assert_check.py
模板三 D段合格断言：step0前置合规 -> 独立实现数值比对 -> 附加断言。

本脚本为T3-17 v2.0重生成之修复载体，对应旧切片(v1.0)外审缺陷 D1/D2/O2 逐条修复：
  D1修复：附加断言基线改为程序化解析T3源文（不复用任何转录常量）——见 assert_source_anchors_parsed_from_live_text()。
  D2修复：附加断言集新增期望band序列钉点、期望trigger序列钉点、window/floor两处严格边界钉点、
          min()合成双方向governance钉点，取代旧版"仅验枚举合法性/仅验单点"的弱断言（不可被协同变异绕过）。
  O2修复：判定失败以非零退出码终止（sys.exit(1)），不仅由stdout/日志承载。

判据出处字段命名（裁决28-H）：本文件全部判据出处引用使用"判据源文位置"等中性命名，不使用"权威定义源"类表述。
"""

import json
import os
import re
import sys
import tokenize
import io

FAILURES = []   # 每条失败断言的具体归因（W-9(3)：不写死单一失败原因）
PASSES = []


def record(ok, label, detail=""):
    if ok:
        PASSES.append(label)
    else:
        FAILURES.append(f"{label} :: {detail}")


# ------------------------------------------------------------------
# step0(i) -- input确为人造
# ------------------------------------------------------------------
def step0_i(input_data):
    record(
        input_data.get("_data_source") == "synthetic_hand_constructed",
        "step0(i) _data_source字段值",
        f"实得={input_data.get('_data_source')!r}"
    )


# ------------------------------------------------------------------
# step0(ii) -- 静态扫描集统一三部分（W-8），剥离注释/docstring后判定
# ------------------------------------------------------------------
FORBIDDEN_IMPORT_PATTERN = re.compile(
    r"^\s*(import\s+(requests|urllib|socket|yfinance|ibapi|ib_insync|pandas_datareader)\b"
    r"|from\s+(requests|urllib|socket|yfinance|ibapi|ib_insync|pandas_datareader)\b)",
    re.MULTILINE,
)
FORBIDDEN_KEYWORD_PATTERN = re.compile(
    r"IBKR|QuantConnect|http://|https://|urlopen|requests\.|socket\.",
)


def strip_comments_and_docstrings(src: str) -> str:
    """剥离注释与docstring后仅留代码文本（W-8(c)口径：判定在剥离后文本上执行）。"""
    out = []
    try:
        tokens = tokenize.generate_tokens(io.StringIO(src).readline)
        prev_toktype = tokenize.INDENT
        for tok in tokens:
            toktype, tokstr, start, end, line = tok
            if toktype == tokenize.COMMENT:
                continue
            if toktype == tokenize.STRING and prev_toktype in (tokenize.INDENT, tokenize.NEWLINE, tokenize.NL, 0):
                # 粗略docstring判定：紧跟缩进/换行的字符串字面量视为docstring，剥离
                continue
            out.append(tokstr)
            prev_toktype = toktype
    except tokenize.TokenizeError:
        return src
    return " ".join(out)


def scan_file_for_forbidden(path):
    with open(path, "r", encoding="utf-8") as fh:
        raw = fh.read()
    stripped = strip_comments_and_docstrings(raw)
    import_hits = FORBIDDEN_IMPORT_PATTERN.findall(stripped)
    keyword_hits = FORBIDDEN_KEYWORD_PATTERN.findall(stripped)
    raw_hits = FORBIDDEN_KEYWORD_PATTERN.findall(raw)  # 剥离前留痕展示用
    return {
        "path": path,
        "stripped_import_hits": import_hits,
        "stripped_keyword_hits": keyword_hits,
        "raw_keyword_hits_for_trace_only": raw_hits,
    }


def step0_ii():
    # 硬性判据对象（本包字面口径）：harness + 独立复算两文件
    required_scope = ["../entity/harness.py", "independent_recompute.py"]
    for p in required_scope:
        res = scan_file_for_forbidden(p)
        ok = (len(res["stripped_import_hits"]) == 0 and len(res["stripped_keyword_hits"]) == 0)
        record(ok, f"step0(ii) 硬性扫描（{p}）", str(res))

    # 主动扩展（非本包硬性判据；规避T3-18外审O1同型缺口，声明为额外自查，不计入硬性判据分母）
    extra_scope = ["assert_check.py"]
    for p in extra_scope:
        res = scan_file_for_forbidden(p)
        ok = (len(res["stripped_import_hits"]) == 0 and len(res["stripped_keyword_hits"]) == 0)
        record(ok, f"step0(ii)-额外自查（{p}，非硬性判据，主动扩展避免T3-18 O1同型缺口）", str(res))


# ------------------------------------------------------------------
# step0(iii) -- independent_recompute.py 零harness耦合
# ------------------------------------------------------------------
def step0_iii():
    with open("independent_recompute.py", "r", encoding="utf-8") as fh:
        raw = fh.read()
    stripped = strip_comments_and_docstrings(raw)
    harness_import = bool(re.search(r"\bimport\s+harness\b|\bfrom\s+harness\b", stripped))
    harness_output_read = "harness_output.json" in stripped
    record(not harness_import, "step0(iii) 复算未import harness模块（剥离后）", f"命中={harness_import}")
    record(not harness_output_read, "step0(iii) 复算未读取harness_output.json（剥离后）", f"命中={harness_output_read}")


# ------------------------------------------------------------------
# D1修复：断言基线程序化解析T3源文（不得复用转录常量）
# ------------------------------------------------------------------
SOURCE_CANDIDATE_PATHS = [
    "/mnt/project/3_波动率凸性操作方法论主文档_T0_frozen_clean_20260615.md",
    "../../3_波动率凸性操作方法论主文档_T0_frozen_clean_20260615.md",
    "./3_波动率凸性操作方法论主文档_T0_frozen_clean_20260615.md",
]

REQUIRED_ANCHOR_TERMS = [
    "wing effectiveness", "moneyness band", "Vega", "Gamma", "响应比",
    "wing_responsiveness_floor", "wing_dullness_window",
    "低于槽位水平", "持续超过槽位窗口", "wing dullness",
    "Phase 3", "repair candidate",
]


def locate_source_file():
    for p in SOURCE_CANDIDATE_PATHS:
        if os.path.isfile(p):
            return p
    return None


def assert_source_anchors_parsed_from_live_text():
    """D1修复核心：真实打开T3现行文件、用正则程序化定位"判据一"段落、
    断言全部锚定关键词在场——不得以任何一侧的人工转录常量替代（判据(i)，裁决28-B）。
    若找不到源文件，直接判该断言不通过并终止（不得静默回退到内嵌副本，
    否则重犯D1"复用转录常量"之同型缺陷）。
    """
    path = locate_source_file()
    if path is None:
        record(False, "D1修复 源文件定位",
               f"候选路径均未找到：{SOURCE_CANDIDATE_PATHS}；拒绝静默回退到内嵌副本")
        return

    with open(path, "r", encoding="utf-8") as fh:
        full_text = fh.read()

    m = re.search(r"判据一｜(.*?)(?=判据二｜)", full_text, re.S)
    record(m is not None, "D1修复 程序化定位判据一段落（正则：判据一｜...至判据二｜）", f"path={path}")
    if not m:
        return
    para = m.group(1)

    missing = [term for term in REQUIRED_ANCHOR_TERMS if term not in para]
    record(len(missing) == 0, "D1修复 判据一段落锚定关键词全部在场（程序化解析，非人工转录）",
           f"缺失={missing}" if missing else "全部命中")

    # 槽位标识符须与input_data.json人造声明的槽位名逐字一致（跨文件一致性核验）
    with open("../entity/input_data.json", "r", encoding="utf-8") as fh:
        input_data = json.load(fh)
    slot_names_in_input = {k for k in input_data["slots"].keys() if not k.startswith("_")}
    slot_names_expected = {"wing_responsiveness_floor", "wing_dullness_window"}
    record(slot_names_in_input == slot_names_expected,
           "D1修复 input声明槽位名与判据一段落锚定槽位名集合一致",
           f"input声明={slot_names_in_input}")


# ------------------------------------------------------------------
# 数值比对：harness_output.json vs independent_output.json 逐分量bit-exact
# ------------------------------------------------------------------
COMPONENT_FIELDS = [
    "moneyness_band_position", "stressed_vega", "stressed_gamma",
    "vega_response_ratio", "gamma_response_ratio", "combined_response_ratio",
    "below_floor", "consecutive_below_count", "wing_dullness_triggered",
]


def load_outputs():
    with open("../entity/harness_output.json", "r", encoding="utf-8") as fh:
        h = json.load(fh)
    with open("independent_output.json", "r", encoding="utf-8") as fh:
        v = json.load(fh)
    return h, v


def numeric_comparison(h, v):
    total = 0
    mismatches = []
    for wing in ["put", "call"]:
        hp = {p["t"]: p for p in h["wings"][wing]}
        vp = {p["t"]: p for p in v["wings"][wing]}
        if hp.keys() != vp.keys():
            record(False, f"数值比对 {wing}翼期数集合一致", f"harness={sorted(hp.keys())} vs 独立={sorted(vp.keys())}")
            continue
        for t in sorted(hp.keys()):
            for field in COMPONENT_FIELDS:
                total += 1
                if hp[t][field] != vp[t][field]:
                    mismatches.append((wing, t, field, hp[t][field], vp[t][field]))
    record(len(mismatches) == 0, f"数值比对 全量{total}项bit-exact（diff=0）",
           f"不符项={mismatches}" if mismatches else f"共{total}项，0不符")


# ------------------------------------------------------------------
# D2修复：附加断言——期望band序列/期望trigger序列/边界钉点/min()双方向钉点
# ------------------------------------------------------------------
EXPECTED_BAND = {
    "put":  ["below", "within", "within", "within", "within", "within", "within", "above", "within"],
    "call": ["below", "within", "within", "within", "within", "within", "within", "within", "within"],
}
EXPECTED_TRIGGERED = {
    "put":  [False, False, False, True, False, False, False, False, False],
    "call": [False, False, False, False, False, False, False, False, False],
}
EXPECTED_BELOW_FLOOR = {
    "put":  [True, True, True, True, False, True, True, True, False],
    "call": [False, False, True, True, False, False, False, True, False],
}
EXPECTED_COUNT = {
    "put":  [1, 2, 3, 4, 0, 1, 2, 3, 0],
    "call": [0, 0, 1, 2, 0, 0, 0, 1, 0],
}
# 双Greek合成governance钉点（governing greek）：min()取值来源方向，逐期人工独立核验值
EXPECTED_GOVERNING = {
    "put":  ["gamma", "vega", "gamma", "vega", "vega", "vega", "vega", "gamma", "gamma"],
    "call": ["vega", "gamma", "vega", "gamma", "gamma", "tie", "tie", "gamma", "vega"],
}


def additional_assertions(h):
    wings = h["wings"]

    # (a) 两翼在场
    record({"put", "call"} <= set(wings.keys()), "附加断言(a) 两翼在场", f"实得keys={list(wings.keys())}")

    for wing in ["put", "call"]:
        periods = wings[wing]
        # (b) 每翼9期、每期9字段齐备
        record(len(periods) == 9, f"附加断言(b) {wing}翼期数=9", f"实得={len(periods)}")
        for p in periods:
            missing_fields = [f for f in COMPONENT_FIELDS if f not in p]
            record(len(missing_fields) == 0, f"附加断言(b) {wing}翼t={p.get('t')}字段齐备", f"缺失={missing_fields}")

        # (c) band位置枚举合规
        bad_enum = [p["t"] for p in periods if p["moneyness_band_position"] not in ("below", "within", "above")]
        record(len(bad_enum) == 0, f"附加断言(c) {wing}翼band枚举合规", f"越界t={bad_enum}")

        # (d) 期望band序列钉点（D2修复：取代仅验枚举合法性——堵M10型band标签互换协同变异）
        actual_band = [p["moneyness_band_position"] for p in sorted(periods, key=lambda x: x["t"])]
        record(actual_band == EXPECTED_BAND[wing], f"附加断言(d) {wing}翼期望band序列钉点",
               f"期望={EXPECTED_BAND[wing]} 实得={actual_band}")

        # (e) 期望below_floor序列钉点
        actual_below = [p["below_floor"] for p in sorted(periods, key=lambda x: x["t"])]
        record(actual_below == EXPECTED_BELOW_FLOOR[wing], f"附加断言(e) {wing}翼期望below_floor序列钉点",
               f"期望={EXPECTED_BELOW_FLOOR[wing]} 实得={actual_below}")

        # (f) 期望consecutive_below_count序列钉点
        actual_count = [p["consecutive_below_count"] for p in sorted(periods, key=lambda x: x["t"])]
        record(actual_count == EXPECTED_COUNT[wing], f"附加断言(f) {wing}翼期望count序列钉点",
               f"期望={EXPECTED_COUNT[wing]} 实得={actual_count}")

        # (g) 期望wing_dullness_triggered序列钉点（D2修复核心：取代旧版仅钉单点t5——
        #     堵M7型">"→">="协同变异：本断言逐期钉住，任一期偏离即FAIL）
        actual_trig = [p["wing_dullness_triggered"] for p in sorted(periods, key=lambda x: x["t"])]
        record(actual_trig == EXPECTED_TRIGGERED[wing], f"附加断言(g) {wing}翼期望triggered序列钉点",
               f"期望={EXPECTED_TRIGGERED[wing]} 实得={actual_trig}")

        # (h) min()双方向governance钉点
        from fractions import Fraction as F
        actual_gov = []
        for p in sorted(periods, key=lambda x: x["t"]):
            vr, gr = F(p["vega_response_ratio"]), F(p["gamma_response_ratio"])
            if vr == gr:
                actual_gov.append("tie")
            elif vr < gr:
                actual_gov.append("vega")
            else:
                actual_gov.append("gamma")
        record(actual_gov == EXPECTED_GOVERNING[wing], f"附加断言(h) {wing}翼min()合成方向钉点（双方向覆盖核验）",
               f"期望={EXPECTED_GOVERNING[wing]} 实得={actual_gov}")

    # (i) O3(a)修复核验：put t1即below_floor（首期边界覆盖，不再是M6语义中性存活的空白点）
    put_t1 = next(p for p in wings["put"] if p["t"] == 1)
    record(put_t1["below_floor"] is True, "附加断言(i) O3(a)修复：put t1首期即below_floor", f"实得={put_t1['below_floor']}")

    # (j) O3(b)修复核验：above分支在两翼中至少出现一次
    all_bands = [p["moneyness_band_position"] for w in ("put", "call") for p in wings[w]]
    record("above" in all_bands, "附加断言(j) O3(b)修复：above分支至少出现一次", f"命中次数={all_bands.count('above')}")

    # (k) 严格边界钉点：floor精确相等不计入below（call t2、t7，combined恰=7/10）
    call_t2 = next(p for p in wings["call"] if p["t"] == 2)
    call_t7 = next(p for p in wings["call"] if p["t"] == 7)
    from fractions import Fraction as F
    record(F(call_t2["combined_response_ratio"]) == F(7, 10) and call_t2["below_floor"] is False,
           "附加断言(k) floor严格边界：call t2 combined恰=floor且below_floor=False（'低于'非'不高于'）",
           f"combined={call_t2['combined_response_ratio']} below_floor={call_t2['below_floor']}")
    record(F(call_t7["combined_response_ratio"]) == F(7, 10) and call_t7["below_floor"] is False,
           "附加断言(k) floor严格边界：call t7 combined恰=floor且below_floor=False",
           f"combined={call_t7['combined_response_ratio']} below_floor={call_t7['below_floor']}")

    # (l) window严格边界钉点（读法#5"超过"=严格大于）：put t3 count==window(3)未触发；put t4 count==window+1(4)触发
    put_t3 = next(p for p in wings["put"] if p["t"] == 3)
    put_t4 = next(p for p in wings["put"] if p["t"] == 4)
    record(put_t3["consecutive_below_count"] == 3 and put_t3["wing_dullness_triggered"] is False,
           "附加断言(l) window严格边界：put t3 count==window(3且未触发，非'达到即触发'的>=粘滞误读)",
           f"count={put_t3['consecutive_below_count']} triggered={put_t3['wing_dullness_triggered']}")
    record(put_t4["consecutive_below_count"] == 4 and put_t4["wing_dullness_triggered"] is True,
           "附加断言(l) window严格边界：put t4 count==window+1(4)触发",
           f"count={put_t4['consecutive_below_count']} triggered={put_t4['wing_dullness_triggered']}")

    # (m) 非粘滞钉点：put t5恢复后count清零、triggered回落（触发后不粘滞永久锁定）
    put_t5 = next(p for p in wings["put"] if p["t"] == 5)
    record(put_t5["consecutive_below_count"] == 0 and put_t5["wing_dullness_triggered"] is False,
           "附加断言(m) 非粘滞：put t4触发后，t5恢复即count清零/triggered回落",
           f"count={put_t5['consecutive_below_count']} triggered={put_t5['wing_dullness_triggered']}")

    # (n) call翼全程未触发（健康翼负例：验证机制不会无条件产生触发信号）
    call_never_triggered = all(p["wing_dullness_triggered"] is False for p in wings["call"])
    record(call_never_triggered, "附加断言(n) call翼负例：全程9期均未触发（健康翼不应被误判dullness）",
           f"触发次数={sum(1 for p in wings['call'] if p['wing_dullness_triggered'])}")

    # (o) tie案例核验：call t6 vega_ratio==gamma_ratio（min()相等分支）
    from fractions import Fraction as F
    call_t6 = next(p for p in wings["call"] if p["t"] == 6)
    record(F(call_t6["vega_response_ratio"]) == F(call_t6["gamma_response_ratio"]) == F(1),
           "附加断言(o) min()相等分支核验：call t6 vega_ratio==gamma_ratio==1",
           f"vega={call_t6['vega_response_ratio']} gamma={call_t6['gamma_response_ratio']}")


# ------------------------------------------------------------------
# 主流程
# ------------------------------------------------------------------
def main():
    with open("../entity/input_data.json", "r", encoding="utf-8") as fh:
        input_data = json.load(fh)

    step0_i(input_data)
    step0_ii()
    step0_iii()

    step0_ok = (len(FAILURES) == 0)
    if not step0_ok:
        write_log(step0_only=True)
        print(f"\n判定：不通过（step0前置合规未过，短路不入后续断言）。失败{len(FAILURES)}项，见assert_log.txt")
        sys.exit(1)

    assert_source_anchors_parsed_from_live_text()   # D1修复
    h, v = load_outputs()
    numeric_comparison(h, v)
    additional_assertions(h)                        # D2修复

    write_log(step0_only=False)

    if FAILURES:
        print(f"\n判定：不通过。失败{len(FAILURES)}项，见assert_log.txt")
        sys.exit(1)
    else:
        print(f"\n判定：通过（PASS）。{len(PASSES)}项断言全部通过，见assert_log.txt")
        sys.exit(0)


def write_log(step0_only):
    with open("assert_log.txt", "w", encoding="utf-8") as fh:
        fh.write(f"T3-17 v2.0 assert_check.py 运行日志\n")
        fh.write(f"通过项（{len(PASSES)}）：\n")
        for p in PASSES:
            fh.write(f"  [PASS] {p}\n")
        fh.write(f"失败项（{len(FAILURES)}）：\n")
        for f_ in FAILURES:
            fh.write(f"  [FAIL] {f_}\n")
        fh.write(f"\n总判定：{'不通过' if FAILURES else '通过（PASS）'}\n")
        if step0_only:
            fh.write("（step0前置合规未过，短路未执行后续数值比对与附加断言）\n")


if __name__ == "__main__":
    main()

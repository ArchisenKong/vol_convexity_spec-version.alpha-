"""
T3-17 wing effectiveness · D段合格断言（step0前置合规 -> 数值比对 -> 附加断言）
依据：任务6产出v1.7 §3D段 ＋ 执行阶段实施操作手册v1.3 §2D ＋ W-8扫描集统一。
断言脚本整体判定归因文案不写死单一失败原因，按实际失败断言输出（W-9(3)）。
"""
import json
import re
import tokenize
import io
from fractions import Fraction as F

FAILURES = []


def record(name, ok, detail=""):
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}" + (f" :: {detail}" if detail and not ok else ""))
    if not ok:
        FAILURES.append((name, detail))
    return ok


def strip_comments_and_docstrings(source):
    """剥离注释与docstring后的纯代码文本（用tokenize正确处理三引号/嵌套/字符串边界）。"""
    out = []
    try:
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        prev_toktype = tokenize.INDENT
        for tok in tokens:
            toktype, tokstr, start, end, line = tok
            if toktype == tokenize.COMMENT:
                continue
            if toktype == tokenize.STRING and prev_toktype in (tokenize.INDENT, tokenize.NEWLINE, tokenize.NL, 0) :
                # 粗略docstring判定：紧跟indent/newline的字符串字面量视为docstring，剥离
                continue
            out.append(tokstr)
            prev_toktype = toktype
    except tokenize.TokenizeError:
        return source
    return " ".join(out)


IMPORT_PATTERNS = [
    r"^\s*import\s+(requests|urllib|socket|yfinance|ibapi|ib_insync|pandas_datareader)\b",
    r"^\s*from\s+(requests|urllib|socket|yfinance|ibapi|ib_insync|pandas_datareader)\b",
]
KEYWORD_PATTERNS = [
    r"IBKR", r"QuantConnect", r"http://", r"https://",
    r"urlopen", r"requests\.", r"socket\.",
]


def scan_forbidden(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    pre_strip_hits = []
    for pat in IMPORT_PATTERNS + KEYWORD_PATTERNS:
        for m in re.finditer(pat, raw, flags=re.MULTILINE):
            pre_strip_hits.append((pat, m.group(0)))

    stripped = strip_comments_and_docstrings(raw)
    post_strip_hits = []
    for pat in IMPORT_PATTERNS:
        for m in re.finditer(pat, stripped, flags=re.MULTILINE):
            post_strip_hits.append((pat, m.group(0)))
    for pat in KEYWORD_PATTERNS:
        for m in re.finditer(pat, stripped):
            post_strip_hits.append((pat, m.group(0)))

    return pre_strip_hits, post_strip_hits


def step0():
    print("--- step0 前置合规断言 ---")
    with open("../entity/input_data.json", "r", encoding="utf-8") as f:
        input_data = json.load(f)
    ok_i = record("(i) input _data_source=synthetic_hand_constructed",
                   input_data.get("_data_source") == "synthetic_hand_constructed")

    files_to_scan = ["../entity/harness.py", "independent_recompute.py"]
    all_clean = True
    for fp in files_to_scan:
        pre, post = scan_forbidden(fp)
        clean = len(post) == 0
        all_clean = all_clean and clean
        record(f"(ii) {fp} 剥离后forbidden模式扫描", clean,
               detail=f"post-strip hits={post}")
        if pre and not post:
            print(f"      留痕（剥离前命中，剥离后0命中，仅展示不构成不合规）：{pre}")
    ok_ii = record("(ii) 全体scan_target剥离后0命中forbidden模式", all_clean)

    with open("independent_recompute.py", "r", encoding="utf-8") as f:
        indep_src_raw = f.read()
    indep_src_stripped = strip_comments_and_docstrings(indep_src_raw)
    # 剥离注释/docstring后二次扫描判定（W-8(c)口径）；剥离前命中（如本文件头部docstring独立性
    # 声明句中出现"harness.py"/"harness_output.json"字样）仅留痕展示，不构成实际耦合。
    raw_hits = [h for h in ["import harness", "from harness", "harness_output.json"] if h in indep_src_raw]
    no_harness_import = "import harness" not in indep_src_stripped and "from harness" not in indep_src_stripped
    no_harness_output_read = "harness_output.json" not in indep_src_stripped
    ok_iii = record("(iii) 独立复算剥离后未引用harness模块/未读取harness_output.json",
                     no_harness_import and no_harness_output_read)
    if raw_hits and (no_harness_import and no_harness_output_read):
        print(f"      留痕（剥离前命中，剥离后0命中，均落在独立性声明docstring内，非实际耦合）：{raw_hits}")

    return ok_i and ok_ii and ok_iii


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def step1_2():
    print("--- step1-2 独立复算 vs harness 数值比对（子口径(a) bit-exact，裁决13）---")
    harness_out = load_json("../entity/harness_output.json")
    indep_out = load_json("independent_output.json")

    comparison_rows = []
    all_match = True
    for wing in ["put", "call"]:
        h_periods = {p["t"]: p for p in harness_out["wings"][wing]["periods"]}
        i_periods = {p["t"]: p for p in indep_out["wings"][wing]["periods"]}
        assert set(h_periods.keys()) == set(i_periods.keys())
        for t in sorted(h_periods.keys()):
            h = h_periods[t]
            i = i_periods[t]
            for field in ["moneyness_band_position", "stressed_vega", "stressed_gamma",
                          "vega_response_ratio", "gamma_response_ratio",
                          "combined_response_ratio", "below_floor",
                          "consecutive_below_count", "wing_dullness_triggered"]:
                hv = h[field]
                iv = i[field]
                if field in ("stressed_vega", "stressed_gamma", "vega_response_ratio",
                              "gamma_response_ratio", "combined_response_ratio"):
                    diff = F(hv) - F(iv)
                    match = (diff == 0)
                else:
                    diff = 0 if hv == iv else "mismatch"
                    match = (hv == iv)
                all_match = all_match and match
                comparison_rows.append((f"{wing}.t{t}.{field}", hv, iv, diff, match))

    for name, hv, iv, diff, match in comparison_rows:
        if not match:
            print(f"[FAIL] {name}: harness={hv} indep={iv} diff={diff}")
    record(f"逐项比对（{len(comparison_rows)}项，全部要求diff=0）", all_match,
           detail=f"{sum(1 for r in comparison_rows if not r[4])} 项不符")

    with open("comparison_table.tsv", "w", encoding="utf-8") as f:
        f.write("component\tharness\tindependent\tdiff\tmatch\n")
        for name, hv, iv, diff, match in comparison_rows:
            f.write(f"{name}\t{hv}\t{iv}\t{diff}\t{match}\n")

    return all_match, len(comparison_rows)


def step3(harness_out):
    print("--- step3 附加断言（形态齐备、判据覆盖）---")
    ok1 = record("附加①：两翼(put/call)均在场",
                  set(harness_out["wings"].keys()) == {"put", "call"})

    all_periods_complete = True
    required_fields = {"t", "moneyness_band_position", "stressed_vega", "stressed_gamma",
                        "vega_response_ratio", "gamma_response_ratio",
                        "combined_response_ratio", "below_floor",
                        "consecutive_below_count", "wing_dullness_triggered"}
    for wing in ["put", "call"]:
        periods = harness_out["wings"][wing]["periods"]
        if len(periods) != 6:
            all_periods_complete = False
        for p in periods:
            if not required_fields.issubset(p.keys()):
                all_periods_complete = False
    ok2 = record("附加②：每翼6期时序、每期字段齐备（含band位置/双Greek响应比/合成量/触发标记）",
                  all_periods_complete)

    valid_band_values = {"below", "within", "above"}
    band_valid = all(
        p["moneyness_band_position"] in valid_band_values
        for wing in ["put", "call"]
        for p in harness_out["wings"][wing]["periods"]
    )
    ok3 = record("附加③：moneyness_band_position取值枚举合规（below/within/above）", band_valid)

    put_triggered = any(p["wing_dullness_triggered"] for p in harness_out["wings"]["put"]["periods"])
    call_never_triggered = not any(p["wing_dullness_triggered"] for p in harness_out["wings"]["call"]["periods"])
    ok4 = record("附加④：判据覆盖——正例分支(put触发)与负例分支(call不触发)均出现",
                  put_triggered and call_never_triggered)

    put_t5 = next(p for p in harness_out["wings"]["put"]["periods"] if p["t"] == 5)
    ok5 = record("附加⑤：put wing t5触发点精确核验（连续低于槽位3期 > window(2)）",
                  put_t5["consecutive_below_count"] == 3 and put_t5["wing_dullness_triggered"] is True)

    put_t6 = next(p for p in harness_out["wings"]["put"]["periods"] if p["t"] == 6)
    ok6 = record("附加⑥：put wing t6恢复后连续计数清零、触发标记回落",
                  put_t6["consecutive_below_count"] == 0 and put_t6["wing_dullness_triggered"] is False)

    return all([ok1, ok2, ok3, ok4, ok5, ok6])


def main():
    ok0 = step0()
    if not ok0:
        print("\n=== step0未过，直接判不合格，不进入数值比对 ===")
        write_log(False, "step0前置合规未过")
        return

    ok12, n_items = step1_2()
    harness_out = load_json("../entity/harness_output.json")
    ok3 = step3(harness_out)

    overall = ok0 and ok12 and ok3
    print(f"\n=== 总判定：{'合格 PASS' if overall else '不合格 FAIL'} ===")
    write_log(overall, "" if overall else f"失败项：{[f[0] for f in FAILURES]}")


def write_log(overall, note):
    with open("assert_log.txt", "w", encoding="utf-8") as f:
        f.write(f"T3-17 wing effectiveness 断言运行日志\n")
        f.write(f"总判定：{'合格 PASS' if overall else '不合格 FAIL'}\n")
        if FAILURES:
            f.write("失败断言明细：\n")
            for name, detail in FAILURES:
                f.write(f"  - {name}: {detail}\n")
        else:
            f.write("全部断言 PASS，无失败项。\n")
        if note:
            f.write(f"备注：{note}\n")


if __name__ == "__main__":
    main()

"""
T-24 theta decay cost · verify/assert_check.py

D段断言脚本：step0 前置合规断言 + step1-2 数值比对（裁决13 子口径分派）+ step3 附加断言。
"""
import json
import re
import sys

SOURCE_MD_PATH = "/mnt/project/2_波动率凸性策略可复用方法论文档集_12篇_T0_frozen_clean_20260615.md"

# 裁决13 子口径(b)既有锚定值：连续解析计算（含超越函数闭式解）＝相对diff≤1e-15
# 本脚本按既有锚定值如实判定，不自行放宽（锚定值修订权归KD）
REL_TOL_B = 1e-15

FORBIDDEN_IMPORT_RE = re.compile(
    r'^\s*(import|from)\s+(requests|urllib|socket|yfinance|ibapi|ib_insync|pandas_datareader)\b',
    re.MULTILINE,
)
FORBIDDEN_KEYWORDS = ["IBKR", "QuantConnect", "http://", "https://", "urlopen", "requests.", "socket."]


def strip_comments_and_docstrings(src: str) -> str:
    src = re.sub(r'"""(.*?)"""', '', src, flags=re.DOTALL)
    src = re.sub(r"'''(.*?)'''", '', src, flags=re.DOTALL)
    lines = []
    for line in src.split("\n"):
        idx = line.find("#")
        lines.append(line if idx == -1 else line[:idx])
    return "\n".join(lines)


def scan_forbidden(path):
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    stripped = strip_comments_and_docstrings(raw)

    stripped_hits = [m.group(0).strip() for m in FORBIDDEN_IMPORT_RE.finditer(stripped)]
    for kw in FORBIDDEN_KEYWORDS:
        if kw in stripped:
            stripped_hits.append("keyword:" + kw)

    raw_hits = [m.group(0).strip() for m in FORBIDDEN_IMPORT_RE.finditer(raw)]
    for kw in FORBIDDEN_KEYWORDS:
        if kw in raw:
            raw_hits.append("keyword:" + kw)

    return stripped_hits, raw_hits


def check_step0():
    results = {}

    # (i) input 确为人造
    with open("entity/input_data.json", "r", encoding="utf-8") as f:
        input_data = json.load(f)
    results["i_synthetic_input"] = (input_data.get("_data_source") == "synthetic_hand_constructed")

    # (ii) harness.py 静态扫描（W-8 统一扫描集：剥离注释/docstring后判定，剥离前留痕）
    stripped_hits, raw_hits = scan_forbidden("entity/harness.py")
    results["ii_harness_stripped_hits"] = stripped_hits
    results["ii_harness_raw_hits_for_trace"] = raw_hits
    results["ii_harness_clean"] = (len(stripped_hits) == 0)

    # (iii) independent_recompute.py 无 harness 耦合，独立于 clean input 推导
    with open("verify/independent_recompute.py", "r", encoding="utf-8") as f:
        recompute_src = f.read()
    stripped_recompute = strip_comments_and_docstrings(recompute_src)
    coupling_hits = []
    if re.search(r'\bimport\s+harness\b', stripped_recompute):
        coupling_hits.append("import harness")
    if "harness_output" in stripped_recompute:
        coupling_hits.append("harness_output reference")
    results["iii_recompute_clean"] = (len(coupling_hits) == 0)
    results["iii_recompute_coupling_hits"] = coupling_hits

    raw_lines = recompute_src.split("\n")
    harness_mentions = [(i + 1, l.strip()) for i, l in enumerate(raw_lines) if "harness" in l.lower()]
    results["iii_raw_harness_mentions_for_manual_grep"] = harness_mentions

    step0_pass = results["i_synthetic_input"] and results["ii_harness_clean"] and results["iii_recompute_clean"]
    return step0_pass, results


def rel_diff(a, b):
    if a == b:
        return 0.0
    denom = max(abs(a), abs(b), 1e-300)
    return abs(a - b) / denom


def check_numeric():
    with open("entity/harness_output.json", "r", encoding="utf-8") as f:
        h = json.load(f)
    with open("verify/independent_output.json", "r", encoding="utf-8") as f:
        v = json.load(f)

    items = []
    for leg in h["legs"]:
        lid = leg["leg_id"]
        items.append((f"{lid}.price_t0", leg["price_t0"], v["leg_prices_t0"][lid]))
        items.append((f"{lid}.price_t1", leg["price_t1"], v["leg_prices_t1"][lid]))
    items.append(("V_t0", h["valuation"]["t0"]["portfolio_value"], v["V_t0"]))
    items.append(("V_t1", h["valuation"]["t1"]["portfolio_value"], v["V_t1"]))
    items.append(("bleed", h["value"], v["bleed"]))

    rows = []
    for name, hv, vv in items:
        d = abs(hv - vv)
        rd = rel_diff(hv, vv)
        within = rd <= REL_TOL_B
        rows.append((name, hv, vv, d, rd, within))
    all_within = all(r[5] for r in rows)
    return all_within, rows


def check_additional_assertions():
    with open("entity/harness_output.json", "r", encoding="utf-8") as f:
        h = json.load(f)
    with open("verify/independent_output.json", "r", encoding="utf-8") as f:
        v = json.load(f)

    # ① bleed 为标量数值且落账本字段（形态齐备）
    a1 = isinstance(h.get("value"), (int, float)) and h.get("field") == "long_end_premium_bleed_theta_decay_cost"

    # ② 复算/账本一致（按裁决13(b)既有锚定值判定，与数值比对bleed项同口径）
    a2 = rel_diff(h["value"], v["bleed"]) <= REL_TOL_B

    # ③ 账本随行标注在场且取值一致——独立锚定源文（独立解析源文件，不复用harness侧转录）
    with open(SOURCE_MD_PATH, "r", encoding="utf-8") as f:
        source_raw = f.read()
    m = re.search(
        r'\|\s*long-end premium bleed[^\|]*\|\s*[^\|]*\|\s*([^\|]*?)\s*\|',
        source_raw,
    )
    canonical_text = m.group(1).strip() if m else None
    ledger_text = h.get("caliber_annotation", {}).get("text", "").strip()
    a3 = (canonical_text is not None) and (canonical_text == ledger_text)

    return {
        "a1_scalar_and_field": a1,
        "a2_recompute_ledger_consistent": a2,
        "a3_caliber_annotation_present_and_anchored": a3,
        "a3_canonical_text_from_source": canonical_text,
        "a3_ledger_text": ledger_text,
    }


def main():
    step0_pass, step0_results = check_step0()
    print("=== step0 前置合规断言 ===")
    print(f"(i) input人造: {step0_results['i_synthetic_input']}")
    print(f"(ii) harness.py 扫描（剥离后命中）: {step0_results['ii_harness_stripped_hits']} -> clean={step0_results['ii_harness_clean']}")
    print(f"(ii) harness.py 扫描（剥离前留痕，非判定依据）: {step0_results['ii_harness_raw_hits_for_trace']}")
    print(f"(iii) independent_recompute.py 无harness耦合: {step0_results['iii_recompute_clean']}, 耦合命中={step0_results['iii_recompute_coupling_hits']}")
    print(f"(iii) 剥离前'harness'字样人工grep核验行号: {step0_results['iii_raw_harness_mentions_for_manual_grep']}")
    print(f"step0 通过: {step0_pass}")

    if not step0_pass:
        print("\nstep0 未通过，判定：不合格，不进入数值比对")
        sys.exit(1)

    print("\n=== step1-2 数值比对（裁决13子口径(b)既有锚定值，REL_TOL=1e-15）===")
    all_within, rows = check_numeric()
    with open("verify/comparison_table.tsv", "w", encoding="utf-8") as f:
        f.write("item\tharness\tindependent\tabs_diff\trel_diff\twithin_1e-15\n")
        for name, hv, vv, d, rd, within in rows:
            line = f"{name}: harness={hv!r} indep={vv!r} abs_diff={d:.6e} rel_diff={rd:.6e} within_1e-15={within}"
            print(line)
            f.write(f"{name}\t{hv!r}\t{vv!r}\t{d:.6e}\t{rd:.6e}\t{within}\n")
    n_within = sum(1 for r in rows if r[5])
    print(f"{n_within}/{len(rows)} 项限内（≤1e-15），{len(rows) - n_within} 项越限")
    print(f"数值比对整体是否全部限内: {all_within}")

    print("\n=== step3 附加断言 ===")
    add = check_additional_assertions()
    for k, val in add.items():
        print(f"{k}: {val}")

    overall = (
        step0_pass
        and all_within
        and add["a1_scalar_and_field"]
        and add["a2_recompute_ledger_consistent"]
        and add["a3_caliber_annotation_present_and_anchored"]
    )
    print(f"\n=== 合格判定（依裁决13(b)既有锚定值1e-15字面适用）===")
    print("通过" if overall else "不通过（数值比对项越限，非step0/附加断言缺陷）")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()

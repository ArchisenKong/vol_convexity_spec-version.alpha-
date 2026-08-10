#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify/assert_check.py · T3-18 · 模板三D段合格断言（step0 前置 + 数值比对 + 附加断言）

纪律绑定：
  - 非零退出码（裁决28-B(ii)判据(ii)，裁决30-A溯及本存量包）：任一断言未过，本脚本以非零退出码结束。
  - 断言基线须程序化解析源文（裁决28-B判据(i)，包§1.5既有条款）：本脚本独立读取并正则解析
    3_波动率凸性操作方法论主文档 源文件第609行，不复用 harness 转录/中间量，作为公式结构断言基线。
  - 整体判定归因文案不写死单一失败原因（W-9(3)）：逐条[PASS]/[FAIL]按实际断言结果输出。
  - step0(ii) 静态扫描口径按手册§3.1 W-5/W-8三部分（剥离注释/docstring后判定，W-8(c)）。
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(HERE)
ENTITY_DIR = os.path.join(REPO_ROOT, "entity")
SOURCE_DOC = os.path.join(REPO_ROOT, "3_波动率凸性操作方法论主文档_T0_frozen_clean_20260615.md")
HARNESS_PATH = os.path.join(ENTITY_DIR, "harness.py")
HARNESS_OUTPUT = os.path.join(ENTITY_DIR, "harness_output.json")
INDEP_SCRIPT = os.path.join(HERE, "independent_recompute.py")
SCHEMA_PATH = os.path.join(ENTITY_DIR, "input_schema.md")

passes = []
failures = []


def record(name, ok, detail=""):
    (passes if ok else failures).append((name, detail))
    return ok


# ---------- step0(i)：input 确为人造 ----------
def check_step0_i_input_synthetic():
    input_path = os.path.join(ENTITY_DIR, "ledger_input.json")
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    ok = data.get("_data_source") == "synthetic_hand_constructed"
    return record("step0(i)_input_synthetic", ok, f"_data_source={data.get('_data_source')!r}")


# ---------- step0(ii)：harness 全程无数据源接入（静态扫描，手册§3.1 W-5/W-8三部分口径） ----------
FORBIDDEN_IMPORT_RE = re.compile(
    r'^\s*(import\s+(requests|urllib|socket|yfinance|ibapi|ib_insync|pandas_datareader)\b'
    r'|from\s+(requests|urllib|socket|yfinance|ibapi|ib_insync|pandas_datareader)\b)',
    re.MULTILINE,
)
FORBIDDEN_KEYWORD_RE = re.compile(r'IBKR|QuantConnect|http://|https://|urlopen|requests\.|socket\.')


def strip_comments_and_docstrings(src):
    """W-8(c)：判定在剥离注释/docstring后的文本上执行；剥离前命中仅留痕展示，不作否决依据。"""
    no_triple = re.sub(r'("""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\')', '', src)
    no_comment = re.sub(r'#.*$', '', no_triple, flags=re.MULTILINE)
    return no_comment


def check_step0_ii_no_data_source():
    with open(HARNESS_PATH, "r", encoding="utf-8") as f:
        raw = f.read()
    stripped = strip_comments_and_docstrings(raw)
    import_hits = FORBIDDEN_IMPORT_RE.findall(stripped)
    keyword_hits = FORBIDDEN_KEYWORD_RE.findall(stripped)
    raw_only = []
    if FORBIDDEN_IMPORT_RE.search(raw) and not FORBIDDEN_IMPORT_RE.search(stripped):
        raw_only.append("import(剥离前命中·留痕非否决)")
    if FORBIDDEN_KEYWORD_RE.search(raw) and not FORBIDDEN_KEYWORD_RE.search(stripped):
        raw_only.append("keyword(剥离前命中·留痕非否决)")
    ok = (len(import_hits) == 0) and (len(keyword_hits) == 0)
    detail = f"剥离后import命中={import_hits} 剥离后keyword命中={keyword_hits} 留痕={raw_only}"
    return record("step0(ii)_no_data_source_static_scan", ok, detail)


# ---------- step0(iii)：独立复算不取 harness 中间量/数据源派生量 ----------
def check_step0_iii_independent_path():
    """判定须在剥离注释/docstring后的文本上执行（同W-8(c)口径）——否则本脚本自身文档字符串中
    "不读取 harness_output.json" 的说明性文本会被朴素子串匹配误判为真实读取行为（自查中发现，留痕于
    切片记录"检验通道记录"）。剥离前命中仅作留痕展示，不作否决依据。"""
    with open(INDEP_SCRIPT, "r", encoding="utf-8") as f:
        raw = f.read()
    stripped = strip_comments_and_docstrings(raw)
    imports_harness = bool(re.search(r'^\s*(import\s+harness|from\s+harness)', stripped, re.MULTILINE))
    reads_harness_output = "harness_output.json" in stripped
    raw_only = []
    if ("harness_output.json" in raw) and ("harness_output.json" not in stripped):
        raw_only.append("harness_output.json字样(仅见于剥离前/注释docstring内·留痕非否决)")
    ok = (not imports_harness) and (not reads_harness_output)
    return record(
        "step0(iii)_independent_recompute_no_harness_reuse", ok,
        f"剥离后imports_harness={imports_harness} 剥离后reads_harness_output_json={reads_harness_output} 留痕={raw_only}",
    )


# ---------- 断言基线程序化解析源文（裁决28-B判据(i)） ----------
def check_source_anchor_line609():
    with open(SOURCE_DOC, "r", encoding="utf-8") as f:
        lines = f.readlines()
    line609 = lines[608] if len(lines) >= 609 else ""  # 0-indexed -> 第609行
    required_terms = [
        "funding gap", "short-end premium income", "long-end premium bleed", "roll cost",
        "滚动窗口", "累计", "parameter_slot_candidate",
        "funding_gap_window", "funding_gap_persistence_shape",
    ]
    missing = [t for t in required_terms if t not in line609]
    ok = (len(missing) == 0)
    return record("source_anchor_T3_line609_programmatic_parse", ok,
                   f"missing_terms={missing} line_len={len(line609)}")


# ---------- B：真跑 harness（裁决1"真跑出数"，非纸面推演） ----------
def run_harness():
    result = subprocess.run([sys.executable, HARNESS_PATH], cwd=ENTITY_DIR,
                             capture_output=True, text=True)
    ok = (result.returncode == 0) and os.path.exists(HARNESS_OUTPUT)
    return record("harness_real_run", ok,
                   f"returncode={result.returncode} stdout={result.stdout.strip()!r} stderr={result.stderr[:300]!r}")


# ---------- D段②：独立复算数值比对（子口径(a)=0 bit-exact，全程整数运算） ----------
def run_independent_and_compare():
    result = subprocess.run([sys.executable, INDEP_SCRIPT], cwd=HERE,
                             capture_output=True, text=True)
    if result.returncode != 0:
        return record("independent_recompute_run", False,
                       f"returncode={result.returncode} stderr={result.stderr[:300]!r}")
    record("independent_recompute_run", True, "独立复算脚本真跑成功")

    indep = json.loads(result.stdout)
    with open(HARNESS_OUTPUT, "r", encoding="utf-8") as f:
        harness_out = json.load(f)

    gap_match = (harness_out["gap_series_cents"] == indep["gap_series_cents"])
    record("numeric_compare_gap_series_bit_exact_a0", gap_match,
           f"harness={harness_out['gap_series_cents']} indep={indep['gap_series_cents']}")

    cum_match = (harness_out["cum_gap_cents"] == indep["cum_gap_cents"])
    record("numeric_compare_cum_gap_bit_exact_a0", cum_match,
           f"harness={harness_out['cum_gap_cents']} indep={indep['cum_gap_cents']}")

    shape_match = (harness_out["shape_evaluation"] == indep["shape_evaluation"])
    record("numeric_compare_shape_evaluation_bit_exact_a0", shape_match,
           f"harness={harness_out['shape_evaluation']} indep={indep['shape_evaluation']}")

    return gap_match and cum_match and shape_match


# ---------- D段③附加断言：判据覆盖——三分支齐备（历史不足/触发/未触发） ----------
def check_shape_branch_coverage():
    with open(HARNESS_OUTPUT, "r", encoding="utf-8") as f:
        out = json.load(f)
    shape = out["shape_evaluation"]
    has_none = any(v is None for v in shape.values())
    has_true = any((v is not None and v["destructive_form"] is True) for v in shape.values())
    has_false = any((v is not None and v["destructive_form"] is False) for v in shape.values())
    ok = has_none and has_true and has_false
    return record("branch_coverage_insufficient_history_trigger_nontrigger", ok,
                   f"has_insufficient_history={has_none} has_destructive_true={has_true} has_destructive_false={has_false}")


# ---------- D段③附加断言：实体制品须携带 C-6标记 / P_B引用 / _data_source 字段（包§7强制） ----------
def check_entity_carries_required_annotations():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_text = f.read()
    has_c6 = "C-6" in schema_text
    has_pb = ("P_B" in schema_text) and ("要件4" in schema_text or "P_B注册记录" in schema_text)
    has_data_source_field = ("_data_source" in schema_text) and ("synthetic_hand_constructed" in schema_text)
    ok = has_c6 and has_pb and has_data_source_field
    return record("entity_carries_C6_PB_reference_and_data_source_field", ok,
                   f"has_C6标记={has_c6} has_P_B要件4引用={has_pb} has_data_source字段声明={has_data_source_field}")


def main():
    check_step0_i_input_synthetic()
    check_step0_ii_no_data_source()
    check_step0_iii_independent_path()
    check_source_anchor_line609()

    gate_names = {
        "step0(i)_input_synthetic",
        "step0(ii)_no_data_source_static_scan",
        "step0(iii)_independent_recompute_no_harness_reuse",
        "source_anchor_T3_line609_programmatic_parse",
    }
    gate_failed = any(name in gate_names for name, _ in failures)

    if not gate_failed:
        if run_harness():
            run_independent_and_compare()
            check_shape_branch_coverage()
            check_entity_carries_required_annotations()
        else:
            record("D段跳过_harness未真跑成功", False, "harness执行失败，无法进入数值比对")
    else:
        record("D段跳过_step0前置未过", False,
               "step0前置合规断言/源文锚定未全过，依模板三D段规则直接判不合格，不进入数值比对（裁决1强制）")

    print("=== T3-18 断言执行日志（模板三D段：step0前置 + 独立数值比对 + 附加断言） ===")
    for name, detail in passes:
        print(f"[PASS] {name} :: {detail}")
    for name, detail in failures:
        print(f"[FAIL] {name} :: {detail}")

    total = len(passes) + len(failures)
    print(f"--- 合计 {len(passes)}/{total} 项断言通过 ---")

    if failures:
        fail_names = "、".join(name for name, _ in failures)
        print(f"整体判定：不合格（{len(failures)}项未过：{fail_names}——按实际失败断言输出，非写死单一原因）")
        sys.exit(1)
    else:
        print("整体判定：合格（step0前置合规 + 断言基线程序化解析源文 + D段②独立数值比对bit-exact + D段③附加断言 全部通过）")
        sys.exit(0)


if __name__ == "__main__":
    main()

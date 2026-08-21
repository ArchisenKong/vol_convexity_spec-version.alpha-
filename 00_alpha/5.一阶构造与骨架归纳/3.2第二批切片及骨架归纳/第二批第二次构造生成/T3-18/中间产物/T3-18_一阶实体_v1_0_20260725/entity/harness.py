#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
harness.py · T3-18 funding relation failure · 一次性 harness
（模板三B段，裁决1："一次性harness真跑出数"；不建常设pipeline，不接任何数据源）

输入：同目录 ledger_input.json（人造构造，_data_source=synthetic_hand_constructed）。
输出：同目录 harness_output.json（真跑捕获，非纸面推演）。

算法边界（entity/input_schema.md §4 三分判别落地口径）：
  ① funding_gap_t = income_t - bleed_t - roll_cost_t
     —— 类一·语义即裁，T3§5.5行609原文直给公式结构，当场裁定写入实现，非桩。
  ② cum_gap_t = 窗口 funding_gap_window 内 funding_gap 之滚动求和
     —— 聚合形式（滚动窗口求和）类一·语义即裁（原文"滚动窗口内累计"文本无歧义）；
        窗口长度数值 = funding_gap_window 槽位（parameter_slot_candidate），本根桩值。
  ③ 破坏形态判定（持续性负值 AND 斜率不收敛）
     —— 类三候选，funding_gap_persistence_shape 槽位内容之操作化候选之一，
        待Phase B证伪，不外推为规范。
"""
import json
import os

INPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ledger_input.json")
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "harness_output.json")


def load_input(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_gap_series(periods):
    """funding_gap_t = income_t - bleed_t - roll_cost_t（T3§5.5行609，类一定案）"""
    gaps = []
    for p in periods:
        g = p["income_cents"] - p["bleed_cents"] - p["roll_cost_cents"]
        gaps.append(g)
    return gaps


def compute_cum_gap(gaps, window):
    """滚动窗口内累计 funding gap（滚动窗口求和，类一定案）。
    window = funding_gap_window 槽位桩值。首个可算评估点 t=window（1-indexed）。
    评估点之前（历史不足）不产出（非"值为0"，是"尚不可算"，不得混淆——独立复算/断言同守此边界）。
    """
    cum = {}
    n = len(gaps)
    for t in range(window, n + 1):
        window_sum = sum(gaps[t - window:t])
        cum[t] = window_sum
    return cum


def evaluate_shape(cum_gap, persistence_periods, baseline_cents, slope_threshold_cents):
    """
    funding_gap_persistence_shape 槽位候选操作化实现——候选之一，待Phase B证伪。
    破坏形态 = 持续性负值 AND 斜率不收敛（T3§5.5行609："累计gap呈持续性负值且斜率不收敛超过槽位窗口"）：
      (a) 持续性负值：评估点 t 前溯 persistence_periods 个累计值全部 < baseline
      (b) 斜率不收敛：以 persistence_periods 窗口两端点做割线（secant）
          delta = cum_gap[t] - cum_gap[t-persistence_periods+1]；delta <= slope_threshold 视为未收敛
          （除法经移项消去，避免引入非精确有理运算，保子口径(a)=0 bit-exact可判性——见W-4容差指令）
    历史不足（窗口内任一评估点缺失）返回 None（"尚不可判"，非"未触发"，两态不得混淆）。
    """
    results = {}
    for t in sorted(cum_gap.keys()):
        window_start = t - persistence_periods + 1
        needed = list(range(window_start, t + 1))
        if any(s not in cum_gap for s in needed):
            results[t] = None
            continue
        window_vals = [cum_gap[s] for s in needed]
        persistent_negative = all(v < baseline_cents for v in window_vals)
        delta = cum_gap[t] - cum_gap[window_start]
        slope_nonconvergent = delta <= slope_threshold_cents
        destructive = persistent_negative and slope_nonconvergent
        results[t] = {
            "persistent_negative": persistent_negative,
            "slope_nonconvergent": slope_nonconvergent,
            "destructive_form": destructive,
            "delta": delta,
        }
    return results


def main():
    data = load_input(INPUT_PATH)
    periods = data["periods"]
    window = data["slots"]["funding_gap_window"]["value"]
    shape_slot = data["slots"]["funding_gap_persistence_shape"]
    persistence_periods = shape_slot["persistence_periods"]
    baseline_cents = shape_slot["baseline_cents"]
    slope_threshold_cents = shape_slot["slope_threshold_cents"]

    gaps = compute_gap_series(periods)
    cum_gap = compute_cum_gap(gaps, window)
    shape_results = evaluate_shape(cum_gap, persistence_periods, baseline_cents, slope_threshold_cents)

    output = {
        "_data_source": "synthetic_hand_constructed",
        "gap_series_cents": gaps,
        "cum_gap_cents": {str(k): v for k, v in cum_gap.items()},
        "shape_evaluation": {str(k): v for k, v in shape_results.items()},
    }
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2, sort_keys=True)
    print(f"harness: wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

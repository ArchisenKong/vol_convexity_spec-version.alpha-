#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify/independent_recompute.py · T3-18 · 模板三D段②独立复算

路径独立声明（D段②硬性要求：不复用B的代码/思路）：
  - 累计gap改用前缀和(prefix sum)技术复算，不使用 harness 之滑动窗口切片求和写法；
  - 持久性判据改用 max(window)<baseline 表达（harness 用 all(v<baseline for v in window)）；
  - 斜率判据改用 not(delta>threshold) 表达（harness 用 delta<=threshold，逻辑等价、写法独立）；
  - 不 import harness、不读取 harness_output.json、不取 harness 任何中间量
    （step0(iii) 断言由本行为满足，assert_check.py 对本文件源码做静态核验）。

仅依赖 entity/ledger_input.json（人造input），不接任何数据源。
结果以 JSON 写至 stdout，供 assert_check.py 以子进程方式调用并比对。
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(HERE, "..", "entity", "ledger_input.json")


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def independent_gap_series(periods):
    """funding_gap_t = income_t - bleed_t - roll_cost_t（同一文本依据T3§5.5行609，独立重写实现）"""
    out = []
    for pd in periods:
        out.append(pd["income_cents"] - pd["bleed_cents"] - pd["roll_cost_cents"])
    return out


def prefix_sums(gaps):
    """前缀和数组：prefix[0]=0，prefix[i]=sum(gaps[0:i])——与harness滑动切片求和为不同算法路径"""
    prefix = [0]
    acc = 0
    for g in gaps:
        acc += g
        prefix.append(acc)
    return prefix


def independent_cum_gap(prefix, window, n):
    """cum_gap[t] = prefix[t] - prefix[t-window]（前缀和差分，t为1-indexed评估期）"""
    out = {}
    for t in range(window, n + 1):
        out[t] = prefix[t] - prefix[t - window]
    return out


def independent_shape(cum_gap, persistence_periods, baseline, slope_threshold):
    out = {}
    for t in sorted(cum_gap.keys()):
        lo = t - persistence_periods + 1
        needed = range(lo, t + 1)
        if any(s not in cum_gap for s in needed):
            out[t] = None
            continue
        vals = [cum_gap[s] for s in needed]
        persistent_negative = (max(vals) < baseline)
        delta = cum_gap[t] - cum_gap[lo]
        slope_nonconvergent = not (delta > slope_threshold)
        out[t] = {
            "persistent_negative": persistent_negative,
            "slope_nonconvergent": slope_nonconvergent,
            "destructive_form": persistent_negative and slope_nonconvergent,
            "delta": delta,
        }
    return out


def main():
    data = load(INPUT_PATH)
    periods = data["periods"]
    window = data["slots"]["funding_gap_window"]["value"]
    shape_slot = data["slots"]["funding_gap_persistence_shape"]
    persistence_periods = shape_slot["persistence_periods"]
    baseline = shape_slot["baseline_cents"]
    slope_threshold = shape_slot["slope_threshold_cents"]

    gaps = independent_gap_series(periods)
    prefix = prefix_sums(gaps)
    cum_gap = independent_cum_gap(prefix, window, len(periods))
    shape = independent_shape(cum_gap, persistence_periods, baseline, slope_threshold)

    result = {
        "gap_series_cents": gaps,
        "cum_gap_cents": {str(k): v for k, v in cum_gap.items()},
        "shape_evaluation": {str(k): v for k, v in shape.items()},
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()

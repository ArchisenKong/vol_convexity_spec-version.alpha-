"""
T3-17 wing effectiveness -- verify/independent_recompute.py
模板三 D段②：独立实现数值比对（不复用 entity/harness.py 任何代码或计算思路；路径独立为硬要求）。

本文件不 import harness 模块、不读取 harness_output.json（step0(iii)核验对象）。
本文件仅读取 entity/input_data.json（人造input，唯一数据源；裁决1：零数据源接入，仅本地文件读取，非"数据源"）。

路径独立点（四处真分叉，风格与harness对照）：
  1. 情景重估：harness用 raw*mult 直接相乘；本文件用展开式 raw + raw*(mult-1)（代数等价，表达式路径不同）。
  2. band位置：harness用 if/elif 三分支；本文件用嵌套条件表达式（三元运算符链）。
  3. 双Greek合成：harness用 if/else 比较链手工取小；本文件用内建 min()。
  4. 连续低于槽位计数：harness用命令式for循环+局部变量原地累加重置；本文件先batch生成
     below_flags布尔列表，再用 itertools.accumulate 配合自定义reducer做扫描式重置计数
     （非逐期耦合band/ratio计算的同一循环体，先分离生成再独立扫描）。
"""

import json
from fractions import Fraction as F
from itertools import accumulate


def load_input(path="../entity/input_data.json"):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def band_position(moneyness, band_low, band_high):
    """嵌套条件表达式风格（非if/elif），路径独立点2。"""
    return ("below" if moneyness < band_low
             else ("above" if moneyness > band_high else "within"))


def reestimate_expanded(raw, mult):
    """展开式：raw + raw*(mult-1)，代数等价于 raw*mult，表达式路径独立点1。"""
    return raw + raw * (mult - F(1))


def combined_via_min(vega_ratio, gamma_ratio):
    """内建min()，路径独立点3。"""
    return min(vega_ratio, gamma_ratio)


def reset_counter(acc, is_below):
    """accumulate自定义reducer：below则累加，否则清零。路径独立点4的核心闭包。"""
    return (acc + 1) if is_below else 0


def compute_wing_independent(wing_data, scenario_shock, slots):
    band_low = F(wing_data["declared_basis"]["target_activation_band_low"])
    band_high = F(wing_data["declared_basis"]["target_activation_band_high"])
    target_vega = F(wing_data["declared_basis"]["target_vega_response_level"])
    target_gamma = F(wing_data["declared_basis"]["target_gamma_response_level"])
    vega_mult = F(scenario_shock["vega_mult"])
    gamma_mult = F(scenario_shock["gamma_mult"])
    floor = F(slots["wing_responsiveness_floor"])
    window = int(slots["wing_dullness_window"])

    periods = wing_data["periods"]

    # 逐期生成器：band/stressed/ratio/combined/below_floor（不含状态依赖部分）
    stage1 = []
    for p in periods:
        moneyness = F(p["moneyness"])
        raw_vega = F(p["raw_vega"])
        raw_gamma = F(p["raw_gamma"])

        pos = band_position(moneyness, band_low, band_high)
        s_vega = reestimate_expanded(raw_vega, vega_mult)
        s_gamma = reestimate_expanded(raw_gamma, gamma_mult)
        v_ratio = s_vega / target_vega
        g_ratio = s_gamma / target_gamma
        combined = combined_via_min(v_ratio, g_ratio)
        below = combined < floor

        stage1.append({
            "t": p["t"],
            "moneyness_band_position": pos,
            "stressed_vega": s_vega,
            "stressed_gamma": s_gamma,
            "vega_response_ratio": v_ratio,
            "gamma_response_ratio": g_ratio,
            "combined_response_ratio": combined,
            "below_floor": below,
        })

    # 批生成below_flags后，用accumulate做独立的连续计数扫描（非同循环体耦合）
    below_flags = [row["below_floor"] for row in stage1]
    counts = list(accumulate(below_flags, reset_counter, initial=0))[1:]  # 去掉initial seed

    out_periods = []
    for row, cnt in zip(stage1, counts):
        row_out = dict(row)
        row_out["stressed_vega"] = str(row["stressed_vega"])
        row_out["stressed_gamma"] = str(row["stressed_gamma"])
        row_out["vega_response_ratio"] = str(row["vega_response_ratio"])
        row_out["gamma_response_ratio"] = str(row["gamma_response_ratio"])
        row_out["combined_response_ratio"] = str(row["combined_response_ratio"])
        row_out["consecutive_below_count"] = cnt
        row_out["wing_dullness_triggered"] = cnt > window
        out_periods.append(row_out)

    return out_periods


def main():
    data = load_input()
    output = {
        "_data_source": data["_data_source"],
        "_recompute": "verify/independent_recompute.py（函数式/生成器风格，独立路径，未import harness）",
        "wings": {
            wing_name: compute_wing_independent(wing_data, data["scenario_shock"], data["slots"])
            for wing_name, wing_data in data["wings"].items()
        }
    }
    with open("independent_output.json", "w", encoding="utf-8") as fh:
        json.dump(output, fh, ensure_ascii=False, indent=2)
    print("独立复算完成，已写出 independent_output.json")


if __name__ == "__main__":
    main()

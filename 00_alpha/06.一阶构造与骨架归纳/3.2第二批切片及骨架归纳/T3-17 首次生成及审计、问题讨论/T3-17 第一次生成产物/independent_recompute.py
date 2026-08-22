"""
T3-17 wing effectiveness · D段②独立复算（核验夹具，不属归纳消费物）
路径独立纪律（任务6 v1.7 D段②）：不复用 entity/harness.py 的代码/思路，另写实现。
本文件直读 entity/input_data.json（clean人造input），不触碰 entity/harness_output.json 任何中间量。
风格：函数式/生成器表达式 + itertools.accumulate 状态累积（与 harness.py 命令式for循环+手工重置计数
在计算核心表达式层面分叉，非仅取字段/循环外壳分叉）。
不接任何数据源（IBKR/QuantConnect/历史行情/实时行情/文件数据源）——本文件不 import requests/urllib/
socket/yfinance/ibapi/ib_insync/pandas_datareader，不发起任何网络访问。
"""
import json
from fractions import Fraction as F
from itertools import accumulate


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def band_position(m, lo, hi):
    # 集合成员式判定（非 if/elif 链）：三态映射为函数式条件表达式
    return "below" if m < lo else ("above" if m > hi else "within")


def stressed_value(raw, coef, delta_iv):
    # 展开式：raw + raw*coef*delta_iv （代数等价于 raw*(1+coef*delta_iv)，但表达式路径不同）
    return raw + raw * coef * delta_iv


def response_ratios(entry, band_lo, band_hi, target_vega, target_gamma, vega_coef, gamma_coef, delta_iv):
    m = F(entry["moneyness"])
    rv = F(entry["raw_vega"])
    rg = F(entry["raw_gamma"])
    sv = stressed_value(rv, vega_coef, delta_iv)
    sg = stressed_value(rg, gamma_coef, delta_iv)
    vr = sv / target_vega
    gr = sg / target_gamma
    return {
        "t": entry["t"],
        "band": band_position(m, band_lo, band_hi),
        "stressed_vega": sv,
        "stressed_gamma": sg,
        "vega_ratio": vr,
        "gamma_ratio": gr,
        "combined": min(vr, gr),  # 内建min，非harness的if/else比较链
    }


def consecutive_below_scan(below_flags):
    """
    用 itertools.accumulate 对 below_flags(bool列表) 做"遇False清零、遇True累加"的扫描，
    与 harness.py 手工 for 循环内 if/else 累加+重置在实现路径上分叉（accumulate的
    reduce式状态传递 vs 显式局部变量重置）。
    """
    def step(acc, flag):
        return acc + 1 if flag else 0
    return list(accumulate(below_flags, step, initial=0))[1:]


def run(input_path):
    data = load(input_path)
    delta_iv = F(data["scenario"]["delta_IV_vol_pts"])
    vega_coef = F(data["scenario"]["vega_sensitivity_coef_per_vol_pt"])
    gamma_coef = F(data["scenario"]["gamma_sensitivity_coef_per_vol_pt"])
    floor = F(data["slots"]["wing_responsiveness_floor"])
    window = int(data["slots"]["wing_dullness_window"])

    out = {"wings": {}}
    for wing_name, wing in data["wings"].items():
        band_lo = F(wing["target_activation_band"][0])
        band_hi = F(wing["target_activation_band"][1])
        target_vega = F(wing["target_response_level"]["vega"])
        target_gamma = F(wing["target_response_level"]["gamma"])

        # 生成器表达式一次性算出全部逐期比值结构（非for循环累加）
        rows = [response_ratios(e, band_lo, band_hi, target_vega, target_gamma,
                                 vega_coef, gamma_coef, delta_iv)
                for e in wing["timeseries"]]

        below_flags = [r["combined"] < floor for r in rows]
        consec = consecutive_below_scan(below_flags)

        periods = []
        for r, cnt in zip(rows, consec):
            periods.append({
                "t": r["t"],
                "moneyness_band_position": r["band"],
                "stressed_vega": str(r["stressed_vega"]),
                "stressed_gamma": str(r["stressed_gamma"]),
                "vega_response_ratio": str(r["vega_ratio"]),
                "gamma_response_ratio": str(r["gamma_ratio"]),
                "combined_response_ratio": str(r["combined"]),
                "below_floor": r["combined"] < floor,
                "consecutive_below_count": cnt,
                "wing_dullness_triggered": cnt > window,
            })
        out["wings"][wing_name] = {"periods": periods}
    return out


if __name__ == "__main__":
    result = run("../entity/input_data.json")
    with open("independent_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("independent recompute complete -> independent_output.json")

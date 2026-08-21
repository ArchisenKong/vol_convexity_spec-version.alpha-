"""
T3-17 wing effectiveness · 一次性harness（B段）
裁决1强制：一次性夹具，不建常设pipeline/数据接口/持久服务。
本文件不接任何数据源（IBKR/QuantConnect/历史行情/实时行情/文件数据源）——
全部输入读取自本地人造 entity/input_data.json（人造，非外部数据源）。
风格：命令式 for 循环（与 verify/independent_recompute.py 的函数式风格路径独立，见D段②）。
"""
import json
from fractions import Fraction as F


def load_input(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def frac(s):
    return F(s)


def moneyness_band_position(moneyness, band_lo, band_hi):
    if moneyness < band_lo:
        return "below"
    elif moneyness > band_hi:
        return "above"
    else:
        return "within"


def run(input_path):
    data = load_input(input_path)

    delta_iv = frac(data["scenario"]["delta_IV_vol_pts"])
    vega_coef = frac(data["scenario"]["vega_sensitivity_coef_per_vol_pt"])
    gamma_coef = frac(data["scenario"]["gamma_sensitivity_coef_per_vol_pt"])
    vega_mult = 1 + vega_coef * delta_iv
    gamma_mult = 1 + gamma_coef * delta_iv

    floor = frac(data["slots"]["wing_responsiveness_floor"])
    window = int(data["slots"]["wing_dullness_window"])

    output = {"scenario_multipliers": {"vega_mult": str(vega_mult), "gamma_mult": str(gamma_mult)},
              "wings": {}}

    for wing_name, wing in data["wings"].items():
        band_lo = frac(wing["target_activation_band"][0])
        band_hi = frac(wing["target_activation_band"][1])
        target_vega = frac(wing["target_response_level"]["vega"])
        target_gamma = frac(wing["target_response_level"]["gamma"])

        periods = []
        consecutive_below = 0

        # 命令式 for 循环：逐期顺序处理，consecutive_below 为跨迭代累积状态
        for entry in wing["timeseries"]:
            t = entry["t"]
            moneyness = frac(entry["moneyness"])
            raw_vega = frac(entry["raw_vega"])
            raw_gamma = frac(entry["raw_gamma"])

            band_pos = moneyness_band_position(moneyness, band_lo, band_hi)

            stressed_vega = raw_vega * vega_mult
            stressed_gamma = raw_gamma * gamma_mult

            vega_ratio = stressed_vega / target_vega
            gamma_ratio = stressed_gamma / target_gamma

            # TPL1-T317-01 桩：min合成（worst-of，确定性最简）
            if vega_ratio < gamma_ratio:
                combined_ratio = vega_ratio
            else:
                combined_ratio = gamma_ratio

            below_floor = combined_ratio < floor

            if below_floor:
                consecutive_below += 1
            else:
                consecutive_below = 0

            dullness_triggered = consecutive_below > window

            periods.append({
                "t": t,
                "moneyness_band_position": band_pos,
                "stressed_vega": str(stressed_vega),
                "stressed_gamma": str(stressed_gamma),
                "vega_response_ratio": str(vega_ratio),
                "gamma_response_ratio": str(gamma_ratio),
                "combined_response_ratio": str(combined_ratio),
                "below_floor": below_floor,
                "consecutive_below_count": consecutive_below,
                "wing_dullness_triggered": dullness_triggered,
            })

        output["wings"][wing_name] = {"periods": periods}

    return output


if __name__ == "__main__":
    result = run("input_data.json")
    with open("harness_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("harness run complete -> harness_output.json")

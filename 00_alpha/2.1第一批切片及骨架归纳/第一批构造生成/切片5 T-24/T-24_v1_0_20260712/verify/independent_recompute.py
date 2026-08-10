"""
T-24 theta decay cost · verify/independent_recompute.py

D段 step1：自 clean 人造 input（entity/input_data.json）独立推导期望值。
不 import 一次性执行夹具模块、不读取其产出文件、不取任何中间量派生量（step0(iii)强制要求）。
实现路径独立：标准正态 CDF 走 erfc 入口（非 erf 入口）；聚合改用字典/列表推导式 + sum()，
非命令式 for 循环原地累加；d1/d2 计算拆为独立辅助函数。
"""
import json
import math

INPUT_PATH = "entity/input_data.json"
OUTPUT_PATH = "verify/independent_output.json"


def norm_cdf_erfc(x):
    # 标准正态 CDF，走 erfc 入口（libm 入口二，与 erf 入口数学等价但计算路径不同）
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def _d1_d2(S, K, tau, sigma, r):
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * tau) / (sigma * math.sqrt(tau))
    return d1, d1 - sigma * math.sqrt(tau)


def price_leg(option_type, S, K, tau, sigma, r):
    if tau <= 0:
        intrinsic = (S - K) if option_type == "call" else (K - S)
        return max(intrinsic, 0.0)
    d1, d2 = _d1_d2(S, K, tau, sigma, r)
    if option_type == "call":
        return S * norm_cdf_erfc(d1) - K * math.exp(-r * tau) * norm_cdf_erfc(d2)
    return K * math.exp(-r * tau) * norm_cdf_erfc(-d2) - S * norm_cdf_erfc(-d1)


def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    legs = data["position"]["legs"]
    mkt = data["market_params"]
    S, sigma, r = mkt["spot"], mkt["volatility_annual"], mkt["risk_free_rate_annual"]

    tp = data["time_points"]
    basis = tp["day_count_basis"]
    tau0 = tp["tau0_days_to_expiry"] / basis
    tau1 = tp["tau1_days_to_expiry"] / basis

    # 字典推导式，非命令式累加循环（与一次性执行夹具的分叉点）
    leg_prices_t0 = {
        leg["leg_id"]: price_leg(leg["option_type"], S, leg["strike"], tau0, sigma, r)
        for leg in legs
    }
    leg_prices_t1 = {
        leg["leg_id"]: price_leg(leg["option_type"], S, leg["strike"], tau1, sigma, r)
        for leg in legs
    }

    leg_notionals_t0 = {
        leg["leg_id"]: leg["quantity_contracts"] * leg["contract_multiplier"] * leg_prices_t0[leg["leg_id"]]
        for leg in legs
    }
    leg_notionals_t1 = {
        leg["leg_id"]: leg["quantity_contracts"] * leg["contract_multiplier"] * leg_prices_t1[leg["leg_id"]]
        for leg in legs
    }

    V0 = sum(leg_notionals_t0.values())
    V1 = sum(leg_notionals_t1.values())
    bleed = V0 - V1

    out = {
        "leg_prices_t0": leg_prices_t0,
        "leg_prices_t1": leg_prices_t1,
        "leg_notionals_t0": leg_notionals_t0,
        "leg_notionals_t1": leg_notionals_t1,
        "V_t0": V0,
        "V_t1": V1,
        "bleed": bleed,
    }
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print("独立复算完成，bleed=%.15f" % bleed)


if __name__ == "__main__":
    main()

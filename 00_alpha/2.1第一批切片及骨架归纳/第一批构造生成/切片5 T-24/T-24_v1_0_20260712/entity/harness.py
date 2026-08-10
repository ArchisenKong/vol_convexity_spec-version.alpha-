"""
T-24 theta decay cost · entity/harness.py

一次性 harness：喂入 entity/input_data.json，对长端 wing 持仓在 t0/t1 两个估值时点分别
经定价重估桩得出持仓价值，bleed = V(t0) - V(t1)，落账本字段（entity/harness_output.json）。
不建常设 pipeline，不接任何数据源。

定价重估桩：Black-Scholes 无股息解析解（确定性、可复算、最简，不承诺逼真；
真实供给方＝品种感知自算 Greeks/定价引擎，登记 TPL1-T76-01，缺实现型，引用不重登，裁决14模式）。

公式结构（类一定案，落档见切片记录 KD 登记项）：bleed = V(t0) - V(t1)，重估差。
"""
import json
import math

INPUT_PATH = "entity/input_data.json"
OUTPUT_PATH = "entity/harness_output.json"

# harness 侧对 T2/00A §4 行86（第三列）分账约束原文的独立转录，供 verify/assert_check.py
# 独立解析源文件后比对（不得复用本转录作为断言基准，任务包§2 D段附加断言③）
CALIBER_ANNOTATION_TEXT = "可以作为长端凸性成本表达；不得与短端 premium income 混账。"
CALIBER_ANNOTATION_POINTER = "T2/00A §4 行86 第三列"


def norm_cdf(x):
    # 标准正态 CDF，走 erf 入口（libm 入口一）
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bsm_price(option_type, S, K, tau, sigma, r):
    if tau <= 0:
        if option_type == "call":
            return max(S - K, 0.0)
        else:
            return max(K - S, 0.0)
    d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * tau) / (sigma * math.sqrt(tau))
    d2 = d1 - sigma * math.sqrt(tau)
    if option_type == "call":
        return S * norm_cdf(d1) - K * math.exp(-r * tau) * norm_cdf(d2)
    elif option_type == "put":
        return K * math.exp(-r * tau) * norm_cdf(-d2) - S * norm_cdf(-d1)
    else:
        raise ValueError("unknown option_type: %s" % option_type)


def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data.get("_data_source") == "synthetic_hand_constructed"

    legs = data["position"]["legs"]
    mkt = data["market_params"]
    S = mkt["spot"]
    sigma = mkt["volatility_annual"]
    r = mkt["risk_free_rate_annual"]

    tp = data["time_points"]
    basis = tp["day_count_basis"]
    tau0 = tp["tau0_days_to_expiry"] / basis
    tau1 = tp["tau1_days_to_expiry"] / basis

    leg_results = []
    V0_total = 0.0
    V1_total = 0.0

    # 命令式 for 循环逐腿累加（B段实现风格；与独立复算侧生成器+sum()分叉，D段②独立性要求）
    for leg in legs:
        opt = leg["option_type"]
        K = leg["strike"]
        qty = leg["quantity_contracts"]
        mult = leg["contract_multiplier"]

        price_t0 = bsm_price(opt, S, K, tau0, sigma, r)
        price_t1 = bsm_price(opt, S, K, tau1, sigma, r)

        notional0 = qty * mult * price_t0
        notional1 = qty * mult * price_t1

        V0_total += notional0
        V1_total += notional1

        leg_results.append({
            "leg_id": leg["leg_id"],
            "option_type": opt,
            "strike": K,
            "price_t0": price_t0,
            "price_t1": price_t1,
            "notional_value_t0": notional0,
            "notional_value_t1": notional1,
        })

    bleed = V0_total - V1_total

    ledger = {
        "object_id": "T-24",
        "field": "long_end_premium_bleed_theta_decay_cost",
        "value": bleed,
        "unit": "currency",
        "valuation": {
            "t0": {"tau_days": tp["tau0_days_to_expiry"], "portfolio_value": V0_total},
            "t1": {"tau_days": tp["tau1_days_to_expiry"], "portfolio_value": V1_total},
        },
        "legs": leg_results,
        "caliber_annotation": {
            "text": CALIBER_ANNOTATION_TEXT,
            "pointer": CALIBER_ANNOTATION_POINTER,
        },
        "income_side_reference": data["income_side_reference"],
        "pricing_model_stub": {
            "type": "BSM_no_dividend_closed_form",
            "status": "占位桩（确定性、可复算、最简，不承诺逼真）",
            "supply_side_gap": "TPL1-T76-01（缺实现型，引用不重登，裁决14模式）",
        },
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)

    print("harness 完成，bleed=%.15f" % bleed)


if __name__ == "__main__":
    main()

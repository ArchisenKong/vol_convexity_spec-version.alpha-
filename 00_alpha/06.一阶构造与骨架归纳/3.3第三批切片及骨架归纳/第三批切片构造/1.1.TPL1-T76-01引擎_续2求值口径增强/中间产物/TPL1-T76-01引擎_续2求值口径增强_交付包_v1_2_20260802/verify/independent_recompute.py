"""
TPL1-T76-01 引擎 · 独立复算路径

独立性声明（任务6产出 v1.7 D段② 口径：判据为"实现路径独立"）：
  1. 数据源独立——本脚本只读 entity/input_data.json（人造 input），
     不 import entity 侧任何模块，不读取 entity/harness_output.json。
  2. 计算核心分叉——
     · 期权分支：估值以 mpmath（60位十进制精度）之 ncdf 独立实现；五希腊
       一律由估值函数之高精度数值微分求得（delta=∂V/∂S、gamma=∂²V/∂S²、
       vega=∂V/∂σ、theta=−∂V/∂T、rho=∂V/∂r），**不使用任何解析希腊公式**。
       与被测侧"闭式解析希腊公式 ＋ math.erf"构成两条结构不同的推导路径。
     · 线性分支：以 fractions.Fraction 精确有理数实现，零浮点。
     · 日期差：使用 datetime.date 序日，与被测侧手写 Rata Die 整数式分叉。
  3. 期望值自 clean 人造 input 独立推导，不取被测侧任何中间量。

数据源纪律：零网络、零行情接口。
"""

import datetime
import json
import os
from fractions import Fraction

from mpmath import mp, mpf, ncdf, exp, log, sqrt, diff

mp.dps = 60

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
IN_PATH = os.path.join(PKG, "entity", "input_data.json")
OUT_PATH = os.path.join(HERE, "independent_expected.json")

DIGITS = 40
GREEKS = ("delta", "gamma", "vega", "theta", "rho")
COMPONENTS = ("value",) + GREEKS

LINEAR = {"spot", "spot_etf", "index", "futures"}
OPTION = {"european_option", "american_option"}


def _dte(expiry, valuation_date):
    a = datetime.date(*[int(x) for x in expiry.split("-")])
    b = datetime.date(*[int(x) for x in valuation_date.split("-")])
    return (a - b).days


def _bs_value(S, K, r, sig, T, cp, q):
    """含连续股息收益率q之欧式估值；mpmath 独立实现（续2）。
    q=0 时代数化简至增强前（无股息）形态——本函数结构与 entity/engine.py 之
    _eval_bs_dividend_yield 分叉：闭式解析五希腊公式 vs 本侧五希腊全部由估值函数
    高精度数值微分求得，零解析希腊公式（独立性声明同模块docstring）。
    q 为冻结参数，不参与微分——契约①5希腊全集不含∂V/∂q（无第六希腊）。"""
    S, K, r, sig, T, q = (mpf(str(x)) for x in (S, K, r, sig, T, q))
    d1 = (log(S / K) + (r - q + sig * sig / 2) * T) / (sig * sqrt(T))
    d2 = d1 - sig * sqrt(T)
    if cp == "call":
        return S * exp(-q * T) * ncdf(d1) - K * exp(-r * T) * ncdf(d2)
    return K * exp(-r * T) * ncdf(-d2) - S * exp(-q * T) * ncdf(-d1)


def _option_components(lot, valuation_date):
    S = lot["spot"]
    K = lot["strike"]
    r = lot["risk_free_rate"]
    sig = lot["implied_vol"]
    cp = lot["option_type"]
    q = lot["dividend_yield"]
    T = mpf(_dte(lot["expiry"], valuation_date)) / 365

    val = _bs_value(S, K, r, sig, T, cp, q)
    delta = diff(lambda x: _bs_value(x, K, r, sig, T, cp, q), mpf(str(S)))
    gamma = diff(lambda x: _bs_value(x, K, r, sig, T, cp, q), mpf(str(S)), 2)
    vega = diff(lambda x: _bs_value(S, K, r, x, T, cp, q), mpf(str(sig)))
    theta = -diff(lambda x: _bs_value(S, K, r, sig, x, cp, q), T)
    rho = diff(lambda x: _bs_value(S, K, x, sig, T, cp, q), mpf(str(r)))
    return {"value": val, "delta": delta, "gamma": gamma,
            "vega": vega, "theta": theta, "rho": rho}, "transcendental"


def _linear_components(lot):
    """线性标的与期货占位桩：恒等承接，精确有理。"""
    S = Fraction(str(lot["spot"]))
    return ({"value": S, "delta": Fraction(1), "gamma": Fraction(0),
             "vega": Fraction(0), "theta": Fraction(0), "rho": Fraction(0)},
            "exact_rational")


def _fmt(x):
    if isinstance(x, Fraction):
        return "%.*e" % (DIGITS - 1, float(x)) if x.denominator != 1 else str(x)
    return mp.nstr(x, DIGITS, strip_zeros=False)


def _evaluate(lot, valuation_date):
    ic = lot["instrument_class"]
    if ic in LINEAR:
        comps, kind = _linear_components(lot)
    elif ic in OPTION:
        comps, kind = _option_components(lot, valuation_date)
    else:
        raise ValueError("品种值域外: %r" % (ic,))

    sign = 1 if lot["side"] == "long" else -1
    scale = int(lot["multiplier"]) * int(lot["quantity"]) * sign

    per_unit = {k: _fmt(comps[k]) for k in COMPONENTS}
    per_lot = {k: _fmt(comps[k] * (Fraction(scale) if kind == "exact_rational"
                                   else mpf(scale)))
               for k in COMPONENTS}
    return {"lot_id": lot["lot_id"], "numeric_kind": kind,
            "per_unit": per_unit, "per_lot": per_lot}


def main():
    with open(IN_PATH, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    v0 = data["valuation_date"]
    shock = data["scenario_shock"]
    tshift = data["time_shift"]

    base, scen, tsh = [], [], []
    for lot in data["lots"]:
        base.append(_evaluate(lot, v0))

        s_lot = dict(lot)
        s_lot["spot"] = lot["spot"] * (1.0 + shock["spot_shock_pct"])
        if lot["implied_vol"] is not None:
            s_lot["implied_vol"] = lot["implied_vol"] + shock["vol_shock_points"]
        scen.append(_evaluate(s_lot, v0))

        tsh.append(_evaluate(lot, tshift["valuation_date_t1"]))

    out = {"_source": "independent_recompute (mpmath dps=60 数值微分 ／ Fraction 精确有理)",
           "_reads": "entity/input_data.json only",
           "base_valuation": base,
           "scenario_revaluation": scen,
           "time_shift_revaluation": tsh}
    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("独立复算完成：%d lots × 3 情形 × 12 分量" % len(base))


if __name__ == "__main__":
    main()

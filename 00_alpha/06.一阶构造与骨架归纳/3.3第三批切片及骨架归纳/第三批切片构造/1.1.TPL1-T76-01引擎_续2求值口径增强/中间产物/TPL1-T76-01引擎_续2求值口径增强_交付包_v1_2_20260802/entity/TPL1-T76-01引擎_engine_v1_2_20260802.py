"""
TPL1-T76-01 引擎 · 一阶实体本体（被测对象）

身份：品种感知自算 Greeks/定价引擎之阶段A一阶实体。
边界：本模块只做 per-lot 层求值（per_unit 与 per_lot 两层）。node 级聚合＝T-76 本职
      （裁决14），本模块不做；腿级聚合＝GK-31 本职，本模块不做。

数据源纪律（契约⑤）：本模块零网络、零文件读取、零行情接口。全部市场坐标由调用方
以已言明面字段传入；Greeks 与估值一律自算，不消费任何 vendor 派生量。

已言明最小面声明（裁决45-B1 条款措辞逐字随附）：
以下为已言明最小面，未言明维度（美式行权、股息、期货保证金形态、day count等）不构成规格封闭，留引擎切片撞墙

未言明维度之当前处置：不就地定义。各路由以确定性占位桩承接并在输出中逐笔标注
（computability_status / unstated_dimensions_hit），缺口另行登记于撞墙清单。
占位桩不 claim 语义等价——桩产出与真实定价结果在当前样本上的任何数值关系，
均不构成桩正确性宣称。

定价模型之地位：本模块所路由之模型为计算用途之仪表计算器，不承载定价真理宣称，
不用于裁决任何交易的获利合法性。

── 续2 引擎求值口径增强（KD裁定52-2，欧式分支引入连续股息收益率 q）──────────
本次增强＝欧式期权定价分支由无股息 BS 闭式解，推广为含连续股息收益率 q 之
BS 闭式解（q 承接位＝新增已言明字段 `dividend_yield`，人造声明输入，裁决1
`_data_source` 纪律同§9）。q=0 时公式代数化简至与增强前逐字节一致（回归可证，
见 verify/regression_check.py）。定价模型族地位不变（仍属 TPL3-T7601-01 类三·
阶段B校准项——"连续股息收益率参数化"为52-2既裁之q承接方式本身，非模型族
再选择；GBM闭式解族之内部参数化增强，非换族）。
线性持仓（spot/spot_etf/index）之股息/持有成本处置＝范围裁定不建模（裁决52-2
①，TPL1-T7601-01该分量已闭合），本次增强不触及 `_eval_linear`。
期货持有成本形态（TPL1-T7601-02）、美式早行权溢价（TPL1-T7601-03）维持 open，
本次增强不宣称覆盖；美式桩因承接欧式分支而随之消费 q（如实呈报，见撞墙清单
候选写回），不构成对03之闭合宣称。
day count 分母（TPL1-T7601-04）本次不改动（KD裁定前按桩纪律续用现值 ACT/365）。
"""

import math

# ---------------------------------------------------------------------------
# 已言明最小面（契约④）：本引擎消费之字段集，锚＝T-76 input_schema v2.2
#   §2 字段表（行17–33）＋ §3 行46（valuation_date 权威源，Q-9订正，裁决48 §4）
#   ＋ §4 桩接口段（行60–79）。三段锚定面，非仅两段（续2续修复订正，D-5②）。
# 未列字段（underlying / leg_type / open_interest / lot_id 之外的坐标与保留字段）
# 不进入求值路径。
# `dividend_yield`（续2新增）不在上述T-76锚定面内——该字段承接45-B1所列未言明
# 维度（股息）之q参数化处置（裁决52-2②直接指定），系本根自行取用之已言明字段
# （工程取用，不外推为跨根命名规范，形态先例同 `instrument_class`），非对
# T-76锚定面本身之扩展。
# ---------------------------------------------------------------------------
STATED_FACE_FIELDS = (
    "lot_id",
    "instrument_class",   # 路由键（本根取用，值域取自 TPL1-T76-01 缺口描述原文）
    "option_type",
    "side",
    "strike",
    "expiry",
    "spot",
    "risk_free_rate",
    "implied_vol",
    "multiplier",
    "quantity",
    "valuation_date",
    "dividend_yield",     # 续2新增：q承接位（人造声明输入，仅期权路由消费）
)

# 品种值域＝撞墙清单_T-76 v2.3 缺口描述原文所列六类，逐项映射为路由键
INSTRUMENT_CLASSES = (
    "spot",              # 现货
    "spot_etf",          # 现货ETF
    "futures",           # 期货
    "index",             # 指数
    "european_option",   # 欧式期权
    "american_option",   # 美式期权
)

ROUTE_TABLE = {
    "spot":             "linear_underlying",
    "spot_etf":         "linear_underlying",
    "index":            "linear_underlying",
    "futures":          "linear_underlying_futures_stub",
    "european_option":  "bs_dividend_yield_closed_form",   # 续2改名（原 bs_no_dividend_closed_form）：
                                                            # 旧名于q≠0后失实，改名避免声明-实现名实不符
    "american_option":  "american_via_european_stub",
}

# 各品种命中之未言明维度（45-B1 列示面 ＋ 构造中撞到之同型维度）
#
# 标注语义（裁决48 §3 既裁，乙·求值路径特征级命中）：
#   `unstated_dimensions_hit` ＝「该求值路径之计算是否进入该维度」。
#   线性恒等求值不含时间投影，股息维度不进入计算 → spot / spot_etf / index
#   三条线性路由均不标 dividend_carry；期货路由（结算/持有成本形态本身未言明）
#   维持命中——TPL1-T7601-02（期货结算形态）不入续2范围，futures 分支零改动。
#   经济层之股息现金流缺口（含线性持仓 bleed 漏分红之实况）由撞墙清单
#   TPL1-T7601-01 之缺口描述全域承载，不由本标注承载。
#
# 续2订正（路由声明兑现，KD裁定52-2②）：european_option / american_option 两路由
# 之 dividend_carry 去标——q 承接位已建成，该求值路径之计算已进入股息维度（q≠0
# 时纳入定价与希腊求值）。美式桩因承接同一函数而随之消费 q，如实去标（§2.3边界：
# 不构成对 TPL1-T7601-03 早行权缺口之闭合宣称，early_exercise 维持命中）。
# day_count_convention 两路由均维持命中——TPL1-T7601-04 本次仅呈候选，未经KD裁定。
UNSTATED_DIMENSIONS = {
    "spot":             (),
    "spot_etf":         (),
    "index":            (),
    "futures":          ("futures_settlement_form", "dividend_carry"),
    "european_option":  ("day_count_convention",),
    "american_option":  ("early_exercise", "day_count_convention"),
}

# 三态可算性标注（降格标注，三分判别 §3 处置要求）
COMPUTABILITY = {
    "spot":             "closed_on_stated_face",
    "spot_etf":         "closed_on_stated_face",
    "index":            "closed_on_stated_face",
    "futures":          "placeholder_stub",
    "european_option":  "computed_with_open_dimensions",
    "american_option":  "placeholder_stub",
}

GREEK_KEYS = ("delta", "gamma", "vega", "theta", "rho")

# day count 占位取值：ACT/365（未言明维度之确定性占位桩，不外推）
DAY_COUNT_DENOMINATOR = 365


# --------------------------- 基础数值原语 ---------------------------------

def _norm_cdf(x):
    """标准正态 CDF；erf 入口。"""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _norm_pdf(x):
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def _side_sign(side):
    if side == "long":
        return 1
    if side == "short":
        return -1
    raise ValueError("side 越出已言明值域 enum{long,short}: %r" % (side,))


def _dte_days(expiry, valuation_date):
    """dte = (expiry - valuation_date).days，整数天（T-76 §3 已言明口径）。
    不引入日历库：两日期以 yyyy-mm-dd 给出，按公历序日差计算。"""
    def _ord(d):
        y, m, dd = (int(t) for t in d.split("-"))
        # 公历序日（Rata Die），纯整数运算
        if m <= 2:
            y -= 1
            m += 12
        return (365 * y + y // 4 - y // 100 + y // 400
                + (153 * (m - 3) + 2) // 5 + dd)
    return _ord(expiry) - _ord(valuation_date)


# --------------------------- 路由分支实现 ---------------------------------

def _eval_linear(lot):
    """线性标的路由（现货／现货ETF／指数）：恒等映射。
    per-unit 估值＝标的报价本身；delta＝1；其余四希腊为 0（精确值，非近似）。
    本路由之求值不含时间投影，股息/持有成本维度不进入计算——三条线性路由
    据裁决48 §3 之求值路径特征级口径均标为 closed_on_stated_face、零维度命中。
    该零命中标注仅就求值路径而言，不构成"线性持仓无股息经济影响"之主张；
    经济层缺口见撞墙清单 TPL1-T7601-01。"""
    return {
        "value": float(lot["spot"]),
        "delta": 1.0,
        "gamma": 0.0,
        "vega": 0.0,
        "theta": 0.0,
        "rho": 0.0,
    }


def _eval_futures_stub(lot):
    """期货路由：确定性占位桩。
    结算/保证金形态未言明（45-B1 明列），本分支不引入任何持有成本或结算约定，
    以标的报价恒等承接。桩不 claim 语义等价：本分支与线性标的路由在阶段A数值重合，
    不构成'期货＝现货'之语义主张。"""
    return {
        "value": float(lot["spot"]),
        "delta": 1.0,
        "gamma": 0.0,
        "vega": 0.0,
        "theta": 0.0,
        "rho": 0.0,
    }


def _eval_bs_dividend_yield(lot):
    """欧式期权路由：含连续股息收益率 q 之 Black-Scholes-Merton 闭式解。
    定价模型族选型＝类三（阶段B校准项，TPL3-T7601-01）：本分支仍属 GBM 闭式解族，
    q 为该族内之参数化增强（续2，KD裁定52-2），非换族；候选之一，声明值不外推，
    待阶段B以回测/实盘数据证伪。

    q 承接位＝`dividend_yield`（续2新增已言明字段，人造声明输入）。q=0 时本公式
    代数化简至增强前（无股息）闭式解逐字节一致（d1/d2 中 −q 项为0，disc_q=e^0=1.0
    精确成立），回归可证——见 verify/regression_check.py（S-1 机械前哨）。

    量纲＝raw（T-76 schema 行80 口径）：delta/gamma 逐份额原始解析值；
    vega 按 sigma 变化 1.0 计；theta 按年计；rho 按 r 变化 1.0 计；零行业缩放。
    q 不新增第六希腊（无 epsilon＝∂V/∂q）——契约①之5全集＋V(t)边界不变，
    q 仅作为定价输入影响既有5希腊之数值，不扩展供给物语义类型。"""
    S = float(lot["spot"])
    K = float(lot["strike"])
    r = float(lot["risk_free_rate"])
    sig = float(lot["implied_vol"])
    q = float(lot["dividend_yield"])
    dte = _dte_days(lot["expiry"], lot["valuation_date"])
    if dte <= 0:
        raise ValueError("dte<=0 落在本分支已言明面之外（到期/已到期形态未言明）")
    T = dte / DAY_COUNT_DENOMINATOR

    sqrtT = math.sqrt(T)
    d1 = (math.log(S / K) + (r - q + 0.5 * sig * sig) * T) / (sig * sqrtT)
    d2 = d1 - sig * sqrtT
    disc_r = math.exp(-r * T)
    disc_q = math.exp(-q * T)
    nd1 = _norm_pdf(d1)

    if lot["option_type"] == "call":
        value = S * disc_q * _norm_cdf(d1) - K * disc_r * _norm_cdf(d2)
        delta = disc_q * _norm_cdf(d1)
        theta = (-(S * disc_q * nd1 * sig) / (2.0 * sqrtT)
                 - r * K * disc_r * _norm_cdf(d2)
                 + q * S * disc_q * _norm_cdf(d1))
        rho = K * T * disc_r * _norm_cdf(d2)
    elif lot["option_type"] == "put":
        value = K * disc_r * _norm_cdf(-d2) - S * disc_q * _norm_cdf(-d1)
        delta = disc_q * (_norm_cdf(d1) - 1.0)
        theta = (-(S * disc_q * nd1 * sig) / (2.0 * sqrtT)
                 + r * K * disc_r * _norm_cdf(-d2)
                 - q * S * disc_q * _norm_cdf(-d1))
        rho = -K * T * disc_r * _norm_cdf(-d2)
    else:
        raise ValueError("option_type 越出已言明值域 enum{call,put}: %r"
                         % (lot["option_type"],))

    gamma = disc_q * nd1 / (S * sig * sqrtT)
    vega = S * disc_q * nd1 * sqrtT
    return {"value": value, "delta": delta, "gamma": gamma,
            "vega": vega, "theta": theta, "rho": rho}


def _eval_american_stub(lot):
    """美式期权路由：确定性占位桩，承接路径＝欧式含股息收益率闭式解。
    早行权维度未言明（45-B1 明列），本分支不计算早行权溢价——早行权溢价通常
    随 q>0（尤其美式put）而非零，本桩不承接该效应，不 claim 语义等价。
    续2订正：本分支因承接欧式分支而随之消费 q（如实呈报，不静默）——
    dividend_carry 已从本路由 unstated_dimensions_hit 去标（q 已进入计算），
    early_exercise 维持命中（本桩产出不构成'美式价值＝欧式价值'之主张，
    亦不构成对早行权溢价大小或方向的任何断言，含 q>0 情形）。"""
    return _eval_bs_dividend_yield(lot)


_DISPATCH = {
    "linear_underlying":              _eval_linear,
    "linear_underlying_futures_stub": _eval_futures_stub,
    "bs_dividend_yield_closed_form":  _eval_bs_dividend_yield,
    "american_via_european_stub":     _eval_american_stub,
}


# --------------------------- 引擎入口 -------------------------------------

def evaluate_lot(lot):
    """品种感知求值：喂一笔 lot（已言明最小面字段），出 per-unit 与 per-lot 两层
    raw Greeks 5全集 ＋ 估值 V(t)。

    情景重估与时点推移不另设参数：调用方以冲击后的市场坐标（spot / implied_vol /
    risk_free_rate / valuation_date）构造同形 lot 再次调用本函数即得重估结果。
    """
    ic = lot["instrument_class"]
    if ic not in ROUTE_TABLE:
        raise ValueError("instrument_class 越出品种值域: %r" % (ic,))
    route = ROUTE_TABLE[ic]
    per_unit = _DISPATCH[route](lot)

    scale = int(lot["multiplier"]) * int(lot["quantity"]) * _side_sign(lot["side"])
    per_lot = {k: per_unit[k] * scale for k in ("value",) + GREEK_KEYS}

    return {
        "lot_id": lot["lot_id"],
        "instrument_class": ic,
        "route_id": route,
        "computability_status": COMPUTABILITY[ic],
        "unstated_dimensions_hit": list(UNSTATED_DIMENSIONS[ic]),
        "per_unit": per_unit,
        "per_lot": per_lot,
    }

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
day count 分母（TPL1-T7601-04）本次不改动（**丙类修复订正，D-4／70-A2**：原注"KD裁定前
按桩纪律续用现值"为裁决57-6 前之陈述残留，已失实——ACT/365 经 57-6 裁定为阶段A权威
口径、经裁决58 闭合落写，非占位桩；本行陈述随之订正，取值本身零变动）。

── 续3 引擎美式切片（TPL1-T7601-03 兑现；KD裁定 A-0/A-0'/A-1/A-2/A-2'/A-3 ＋ §6）──
本次兑现＝美式期权（可提前行权合约）之估值与五希腊求值供给，且早行权溢价对欧式
结果之差异可被识别（撞墙清单 TPL1-T7601-03 条目缺口描述原文＝功能需求唯一权威）。
置换现行 `american_via_european_stub` 确定性占位桩。

三分判别拆分与归类（KD裁定 A-0，受控文本 v1.1 §1 之 D6#1 三层拆分先例）：
  甲·结构层「须承载提前行权价值、且差异可识别」＝**类一**（03 条目缺口描述原文
     "该结果与欧式结果之差异（早行权溢价）可被识别"排除欧式闭式解承接候选）
     → 定案写入实现，非桩。
  乙·算法族（BSM近似 / BAW / CRR / 其他）＝**类三·阶段B校准项**
     → 新立 TPL3-T7601-02。类一测试判"裁不了"（查过：契约六条、缺口描述原文、
     45-B1、翻译审计表现行版之「宪-EP-05 定价模型批判」「宪-EP-06 定价认识论」两行
     （**丙类修复订正，D-5采β形态**：弃行号锚改词锚，grep 可定位唯一字符串，
     上游台账再版不再断链），全候选与全部权威文本相容）；类二测试亦不成立
     ——引擎自身即终端供给方，再挂类二即自指循环。阶段A 跑具体版本＝CRR 二叉树，
     **候选之一，声明值不外推，待阶段B以回测/实盘数据证伪**；不留白。
  丙·步数 N ＝**类二·缺定义型**（KD裁定 A-2）→ 供给方＝消费方之精度要求（node级
     聚合/腿级聚合尚未提出精度要求），登记 PROBE-02。N 非类三——N→∞ 极限良定义、
     收敛性在阶段A 可自证（收敛研究随 verify 交付），不需经验数据裁定。
     阶段A 声明值＝500，声明值不外推。

行权风格字段（KD裁定 §6，授权源＝裁决71-4）：新增 `exercise_style` **必填**独立字段，
不由 `instrument_class` 推导。`ROUTE_TABLE` 键由单键改为
`(instrument_class, exercise_style)` **二元组**——一致性校验因而内建于路由查表本身
（非法组合不在表中即 raise），无需另设校验步。品种值域六类维持不动（锚＝撞墙清单
_T-76 v2.3 缺口描述原文），未静默收窄。

早行权溢价之输出（S-1 兑现）：record 级新增 `early_exercise_premium` 键（per_unit /
per_lot 两层，非美式路由取 null）。**同离散基线**（KD裁定 B-1）——溢价＝同一格点参数
下"允许提前行权"与"不允许提前行权"两次倒推之差，**不取欧式闭式解为减数**：跨口径
基线会把树截断误差混入溢价读数（探针实测：小溢价用例污染 4～9%，恒等零域污染 100%）。
契约①之 5全集＋V(t) 边界不变——溢价为估值分解量，非第六希腊（形态先例＝续2 之
q 不新增 epsilon）。

美式路由之希腊求法（KD裁定 D-1）：delta / gamma / theta 取**格点原生**，vega / rho 取
声明步长中心差分。spot-bump 差分 gamma **禁用**——固定 N 下树值对 S 呈锯齿，探针实测
差分 gamma 与格点 gamma 偏离达 11.3 倍（C1 坐标：0.000774 vs 0.009549）。

离散分红形态（KD裁定 A-3）：本分支之 q 为**连续**股息收益率。真实 equity/ETF 分红为
离散现金事件，美式提前行权之最优时点由离散除息事件驱动，连续 q 将其抹平。该近似
之充分性只能由实盘/回测判定 → 新立 **TPL3-T7601-03**（类三·阶段B校准项）。
TPL1-T7601-01 之闭合（裁决58）字面限定于欧式分支，本条不翻转其闭合。
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
    "exercise_style",     # 续3新增：行权风格（必填独立字段，路由第二轴；KD裁定§6）
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

# 行权风格值域（续3新增，KD裁定§6）：期权类取 enum{european,american}，
# 非期权类退化取 None（退化形态先例＝strike/implied_vol 之 null 退化）。
EXERCISE_STYLES = ("european", "american", None)

# 路由表（续3：单键→二元组，KD裁定§6之(ii-全)，含扩范围明授）
# 键＝(instrument_class, exercise_style)。两轴均为 input 必填声明字段，均不推导。
# 非法组合（如 ("european_option","american")）不在表中，查表即 raise——
# 一致性校验内建于路由本身，不另设校验步。
# 当前期权域两轴共变（european_option↔european、american_option↔american），系
# instrument_class 值域锚定于撞墙清单_T-76 v2.3 六品种原文所致，非设计选择；
# 该结构冗余如实登记（施工过程发现事项），不以静默收窄品种域消除之。
ROUTE_TABLE = {
    ("spot",            None):        "linear_underlying",
    ("spot_etf",        None):        "linear_underlying",
    ("index",           None):        "linear_underlying",
    ("futures",         None):        "linear_underlying_futures_stub",
    ("european_option", "european"):  "bs_dividend_yield_closed_form",   # 续2改名（原 bs_no_dividend_closed_form）：
                                                                          # 旧名于q≠0后失实，改名避免声明-实现名实不符
    ("american_option", "american"):  "american_crr_binomial",           # 续3：置换 american_via_european_stub
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
# day_count_convention 两路由维持命中——**续3订正（R-2残留第三处，搭车项5／70-A2）**：
# 原注"本次仅呈候选，未经KD裁定"为裁决57-6 前之陈述残留，已失实；04 条目经 57-6
# 裁定 ACT/365 为阶段A权威口径并经裁决58 闭合落写。本标签之去留（标签语义重定）
# 为待裁二选一，撞墙清单引擎「已知开口登记」明写"呈KD裁定后同批落"，本版维持不动。
# 续3订正（03 兑现之直接后果，KD裁定 A-0'）：`american_option` 路由之
# `early_exercise` **去标**——早行权维度已进入该求值路径之计算（CRR 逐节点提前行权
# 判定），标注口径同裁决48 §3 之乙·求值路径特征级命中。形态先例＝续2 对
# `dividend_carry` 之去标处置。去标不构成"美式定价已完备"之主张：算法族与离散分红
# 形态两项类三（TPL3-T7601-02 / -03）如实 open，由 computability_status 与撞墙清单
# 承载，不由本标注承载。
# `day_count_convention` 两期权路由命中标签**本版维持不动**——该项（撞墙清单引擎
# v1.3「已知开口登记」之 route_table 标签语义重定）原文即为待裁二选一
# 「是否随之重定（去标／升 closed_on_stated_face）」，且明写"呈KD裁定后同批落"；
# KD 本轮未就该二选一作裁定，故本版维持现状并随包呈裁，不由构造会话自决。
UNSTATED_DIMENSIONS = {
    ("spot",            None):        (),
    ("spot_etf",        None):        (),
    ("index",           None):        (),
    ("futures",         None):        ("futures_settlement_form", "dividend_carry"),
    ("european_option", "european"):  ("day_count_convention",),
    ("american_option", "american"):  ("day_count_convention",),
}

# 三态可算性标注（降格标注，三分判别 §3 处置要求）
# 续3订正（KD裁定 A-0'）：`american_option` 由 `placeholder_stub` 升
# `computed_with_open_dimensions`——本路由求值规则已非占位桩，而是真实计算（CRR
# 二叉树，逐节点提前行权判定），其模型族属类三 open（TPL3-T7601-02），形态与
# `european_option` 分支完全平行（该分支之 GBM 闭式解族亦为类三 TPL3-T7601-01）。
# `futures` 维持 `placeholder_stub`（TPL1-T7601-02 显式后置，裁决72-7）。
COMPUTABILITY = {
    ("spot",            None):        "closed_on_stated_face",
    ("spot_etf",        None):        "closed_on_stated_face",
    ("index",           None):        "closed_on_stated_face",
    ("futures",         None):        "placeholder_stub",
    ("european_option", "european"):  "computed_with_open_dimensions",
    ("american_option", "american"):  "computed_with_open_dimensions",
}

GREEK_KEYS = ("delta", "gamma", "vega", "theta", "rho")

# day count 分母：ACT/365。**权威值非占位桩**（裁决57-6 裁定为阶段A权威口径；
# 续3 订正——v1.2 之"占位取值不外推"注为 57-6 前之陈述残留，属撞墙清单 R-2 登记项，
# 本窗搭车订正，KD裁定搭车项5/70-A2）。
DAY_COUNT_DENOMINATOR = 365

# ── 续3 美式求值声明面（全部为声明值，程序化解析对表见 verify/assert_check.py）──
# 步数 N：类二·缺定义型之阶段A声明值（KD裁定 A-2/A-2'）。供给方＝消费方精度要求，
# 登记 PROBE-02。**声明值不外推**。收敛性由 verify 侧收敛研究自证，非经验数据裁定。
CRR_STEPS = 500

# vega / rho 之中心差分声明步长（delta/gamma/theta 走格点原生，不用差分——KD裁定 D-1）。
# 步长数值＝构造自由度（裁决17(a) 口径：幅度值＝数据）；其"作为声明离散近似量"之
# 容差归属＝F-11（逐对象标定，界值登记于 schema 声明块）。
CRR_BUMP_VOL = 1e-3      # 绝对，作用于 implied_vol
CRR_BUMP_RATE = 1e-4     # 绝对，作用于 risk_free_rate


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


def _crr_lattice(S, K, r, q, sig, T, otype, american, n_steps):
    """CRR 二叉树倒推求解。返回 dict：
      value              树根值
      delta_lat/gamma_lat/theta_lat   格点原生希腊（KD裁定 D-1）
      n_exercise_nodes   提前行权绑定节点计数（离散不变量／事件类派生量）
      max_exercise_excess 绑定处 intrinsic−continuation 之最大超出量（噪声免疫诊断量）

    离散化＝Cox-Ross-Rubinstein：u=e^{σ√dt}、d=1/u、p=(e^{(r−q)dt}−d)/(u−d)，
    逐层贴现 e^{−r·dt}。`american=True` 时每节点取 max(继续持有, 内在价值)。
    模型族地位＝类三 TPL3-T7601-02（候选之一，声明值不外推，待阶段B证伪）。

    `american=False` 之欧式模式**不是**欧式闭式解分支之替身——其唯一用途为
    同离散基线（S-1 溢价之减数，KD裁定 B-1），使截断误差在相减时同向消去。"""
    dt = T / n_steps
    sd = sig * math.sqrt(dt)
    u = math.exp(sd)
    d = 1.0 / u
    p = (math.exp((r - q) * dt) - d) / (u - d)
    disc = math.exp(-r * dt)
    if not (0.0 < p < 1.0):
        raise ValueError(
            "CRR 风险中性概率越出 (0,1)：p=%r（步数/参数组合越出本分支已言明面）" % (p,))

    # 上行因子幂表：ef[k + n] = u^k，避免逐节点重算 exp
    ef = [math.exp(sd * k) for k in range(-n_steps, n_steps + 1)]

    def node_spot(i, j):          # i 步、j 次上行
        return S * ef[(2 * j - i) + n_steps]

    if otype == "call":
        def intrinsic(x):
            return x - K
    elif otype == "put":
        def intrinsic(x):
            return K - x
    else:
        raise ValueError("option_type 越出已言明值域 enum{call,put}: %r"
                         % (otype,))

    V = [max(intrinsic(node_spot(n_steps, j)), 0.0) for j in range(n_steps + 1)]
    n_ex = 0
    max_ex = 0.0
    keep = {}
    for i in range(n_steps - 1, -1, -1):
        V = [disc * (p * V[j + 1] + (1.0 - p) * V[j]) for j in range(i + 1)]
        if american:
            out = []
            for j in range(i + 1):
                iv = intrinsic(node_spot(i, j))
                if iv > V[j]:
                    n_ex += 1
                    if iv - V[j] > max_ex:
                        max_ex = iv - V[j]
                    out.append(iv)
                else:
                    out.append(V[j])
            V = out
        if i <= 2:
            keep[i] = (list(V), [node_spot(i, j) for j in range(i + 1)])

    v0 = V[0]
    V1, S1 = keep[1]
    V2, S2 = keep[2]
    # 格点原生 delta：第1层两节点之差商
    delta = (V1[1] - V1[0]) / (S1[1] - S1[0])
    # 格点原生 gamma：第2层三节点之二阶差商（spot-bump 差分禁用，KD裁定 D-1）
    d_up = (V2[2] - V2[1]) / (S2[2] - S2[1])
    d_dn = (V2[1] - V2[0]) / (S2[1] - S2[0])
    gamma = (d_up - d_dn) / (0.5 * (S2[2] - S2[0]))
    # 格点原生 theta：中间节点（S 复归原位）与树根之差商，按年计（theta_unit）
    theta = (V2[1] - v0) / (2.0 * dt)
    return {"value": v0, "delta_lat": delta, "gamma_lat": gamma,
            "theta_lat": theta, "n_exercise_nodes": n_ex,
            "max_exercise_excess": max_ex,
            # 微修窗 E-1α（裁决78）：回显字段须来自实际执行路径之返回值，
            # 不得由同名常量直接回显——"回显"与"实际离散化"不可脱钩。
            "n_steps_used": n_steps}


def _american_inputs(lot, vol=None, rate=None):
    """自 lot 抽出 CRR 入参（供本体与 vega/rho 差分共用，避免两处口径漂移）。
    **无 spot 形参**——delta/gamma 走格点原生，spot-bump 差分经 KD裁定 D-1 禁用；
    形参不在场即从源级排除该路径之可能。"""
    dte = _dte_days(lot["expiry"], lot["valuation_date"])
    if dte <= 0:
        raise ValueError("dte<=0 落在本分支已言明面之外（到期/已到期形态未言明）")
    return (float(lot["spot"]),
            float(lot["strike"]),
            float(lot["risk_free_rate"]) if rate is None else rate,
            float(lot["dividend_yield"]),
            float(lot["implied_vol"]) if vol is None else vol,
            dte / DAY_COUNT_DENOMINATOR,
            lot["option_type"])


def _eval_american_crr(lot):
    """美式期权路由：CRR 二叉树，逐节点提前行权判定（TPL1-T7601-03 兑现）。

    量纲＝raw（同欧式分支，T-76 schema 行80 口径）：delta/gamma 逐份额原始值；
    vega 按 sigma 变化 1.0 计；theta 按年计；rho 按 r 变化 1.0 计；零行业缩放。

    希腊求法（KD裁定 D-1）：delta/gamma/theta 格点原生；vega/rho 声明步长中心差分。
    **spot-bump 差分 gamma 禁用**——固定 N 下树值对 S 呈锯齿，探针实测偏离达 11.3 倍。

    早行权溢价（S-1）：同离散基线，＝本树（允许提前行权）− 同参数欧式模式树。
    不以欧式闭式解为减数（KD裁定 B-1）。"""
    S, K, r, q, sig, T, otype = _american_inputs(lot)
    am = _crr_lattice(S, K, r, q, sig, T, otype, True, CRR_STEPS)
    eu = _crr_lattice(S, K, r, q, sig, T, otype, False, CRR_STEPS)

    def _val(vol=None, rate=None):
        a = _american_inputs(lot, vol, rate)
        return _crr_lattice(a[0], a[1], a[2], a[3], a[4], a[5], a[6],
                            True, CRR_STEPS)["value"]

    vega = (_val(vol=sig + CRR_BUMP_VOL) - _val(vol=sig - CRR_BUMP_VOL)) \
        / (2.0 * CRR_BUMP_VOL)
    rho = (_val(rate=r + CRR_BUMP_RATE) - _val(rate=r - CRR_BUMP_RATE)) \
        / (2.0 * CRR_BUMP_RATE)

    return {"value": am["value"],
            "delta": am["delta_lat"], "gamma": am["gamma_lat"],
            "vega": vega, "theta": am["theta_lat"], "rho": rho,
            "_eep": am["value"] - eu["value"],
            "_lattice_diag": {
                "n_exercise_nodes": am["n_exercise_nodes"],
                "max_exercise_excess": am["max_exercise_excess"],
                "european_mode_n_exercise_nodes": eu["n_exercise_nodes"],
                "european_mode_value": eu["value"],
                # E-1α（裁决78）：取美式树实际步数返回值，非常量回显
                "crr_steps": am["n_steps_used"]}}


_DISPATCH = {
    "linear_underlying":              _eval_linear,
    "linear_underlying_futures_stub": _eval_futures_stub,
    "bs_dividend_yield_closed_form":  _eval_bs_dividend_yield,
    "american_crr_binomial":          _eval_american_crr,
}


# --------------------------- 引擎入口 -------------------------------------

def evaluate_lot(lot):
    """品种感知求值：喂一笔 lot（已言明最小面字段），出 per-unit 与 per-lot 两层
    raw Greeks 5全集 ＋ 估值 V(t)。

    情景重估与时点推移不另设参数：调用方以冲击后的市场坐标（spot / implied_vol /
    risk_free_rate / valuation_date）构造同形 lot 再次调用本函数即得重估结果。
    """
    ic = lot["instrument_class"]
    if ic not in INSTRUMENT_CLASSES:
        raise ValueError("instrument_class 越出品种值域: %r" % (ic,))
    if "exercise_style" not in lot:
        raise ValueError(
            "exercise_style 为必填字段，缺位（KD裁定§6：必填独立字段，不由 "
            "instrument_class 推导）：lot_id=%r" % (lot.get("lot_id"),))
    es = lot["exercise_style"]
    if es not in EXERCISE_STYLES:
        raise ValueError("exercise_style 越出已言明值域 enum{european,american}∪{null}: %r"
                         % (es,))
    key = (ic, es)
    if key not in ROUTE_TABLE:
        # 一致性校验内建于路由查表（KD裁定§6之(ii-全)）：非法组合无路由即拒绝，
        # 不就地推导、不静默回退。
        raise ValueError(
            "(instrument_class, exercise_style) 组合无路由，越出已言明面: %r" % (key,))
    route = ROUTE_TABLE[key]
    per_unit_raw = _DISPATCH[route](lot)

    # 溢价与格点诊断为求值副产物，不入 per_unit/per_lot 分量键集
    # （契约①之 5全集＋V(t) 边界不变；形态先例＝续2 之 q 不新增第六希腊）。
    eep_unit = per_unit_raw.pop("_eep", None)
    lattice_diag = per_unit_raw.pop("_lattice_diag", None)
    per_unit = per_unit_raw

    scale = int(lot["multiplier"]) * int(lot["quantity"]) * _side_sign(lot["side"])
    per_lot = {k: per_unit[k] * scale for k in ("value",) + GREEK_KEYS}

    if eep_unit is None:
        eep = None
    else:
        # 溢价为估值分解量，与 V(t) 同施 side_sign（§5 缩放式之一致外延）
        eep = {"per_unit": eep_unit, "per_lot": eep_unit * scale}

    return {
        "lot_id": lot["lot_id"],
        "instrument_class": ic,
        "exercise_style": es,
        "route_id": route,
        "computability_status": COMPUTABILITY[key],
        "unstated_dimensions_hit": list(UNSTATED_DIMENSIONS[key]),
        "per_unit": per_unit,
        "per_lot": per_lot,
        "early_exercise_premium": eep,
        "lattice_diagnostics": lattice_diag,
    }

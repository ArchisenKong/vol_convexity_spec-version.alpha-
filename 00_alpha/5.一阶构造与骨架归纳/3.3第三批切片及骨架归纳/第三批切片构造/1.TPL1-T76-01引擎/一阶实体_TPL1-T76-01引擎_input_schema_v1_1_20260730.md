# 一阶实体 · TPL1-T76-01引擎 · input schema 与算法declaration · v1.0 · 20260730

> **身份**：TPL1-T76-01（品种感知自算Greeks/定价引擎）之阶段A一阶实体。第三批首根（裁决43-E3）。
> **授权链**：切片任务包_TPL1-T76-01引擎_v1_0_candidate_20260730（KD已确认）＋裁决1（构造链）＋裁决45 §5（1级契约六条）＋裁决13/19（容差）＋裁决21(a)（三分判别）＋裁决24-A7 O1（目录结构）＋裁决28-B(ii)（非零退出码）＋裁决39-B（输出形态封闭，第三批起转施工侧判据）。
> **会话身份**：切片构造会话。零自审、零裁决——本文件全部判断均为构造侧呈报，实体边界与范围疑义一律呈KD。

---

## §1 对象语义与边界

TPL1-T76-01引擎＝**品种感知的自算Greeks/定价供给物**：按品种路由适用定价模型，per-lot Greeks 与估值 V(t) 由自有统一算法计算，以消除回测（QC）与实盘（IBKR）数据源间的Greeks口径差异。

**供给方定位（契约⑥，既裁24-E3）**：仪表计算器，非定价真理源。Phase B设计受宪法定价认识论章约束（消费通道＝翻译审计表_v1_4_定案 行94/行95 对照区，C4②成对引用）。本实体不承载任何"应然价格/正确定价"宣称，不以模型输出裁决获利合法性。

**下边界（不做什么）**：
- 不做 node 级聚合（T-76 本职，裁决14）；不做腿级聚合（GK-31 本职）。本实体止于 per-lot 两层（per_unit / per_lot）。
- 不承载 identity/target review 判定或 target 变更之自动执行位（审计表行96，宪-ID-02，人工域，pipeline出口外）。
- 不消费任何 vendor 派生量（Greeks/理论价/模型IV）作输入（契约⑤）。

**情景重估之形态（构造中反推浮现，非预先设计）**：T3-03 §3.4／GK-14 §2.6／T3-17 §3 之情景重估消费面、T-24 §4① 之 V(t0)/V(t1) 重估差消费面，**均不要求本实体新增任何接口参数**——以冲击后（或时点推移后）的市场坐标构造同形 lot 再次调用同一签名即得重估结果。模块划分_v1_0 M1 接口形态所列"情景冲击"入参面，在已言明面上收敛为市场坐标字段本身。此为构造侧呈报观察，不自裁。

---

## §2 已言明最小面（契约④）

**原文锚**：一阶实体_T-76_input_schema_v2_2_20260714.md §2 字段表（行17–33）＋ §4 桩接口段（行60–79）。指针引用，不转写。

**锚定区间之补充（Q-9 订正，裁决48 §4）**：上列两区间不覆盖 `valuation_date` 之权威源——该字段之权威定义在 **T-76 schema §3 行46**（`dte = (expiry - valuation_date).days`，整数天口径）。本实体求值路径消费 `valuation_date`（见 STATED_FACE_FIELDS），故锚定面为〔§2 行17–33〕＋〔§3 行46〕＋〔§4 行60–79〕三段，非原表述之两段。

**45-B1 条款措辞（逐字随附）**：

以下为已言明最小面，未言明维度（美式行权、股息、期货保证金形态、day count等）不构成规格封闭，留引擎切片撞墙

**本实体求值路径实际消费之字段集**（STATED_FACE_FIELDS，engine.py 同名常量）：
`lot_id` / `instrument_class` / `option_type` / `side` / `strike` / `expiry` / `spot` / `risk_free_rate` / `implied_vol` / `multiplier` / `quantity` / `valuation_date`

**未进入求值路径**：`underlying` / `leg_type` / `open_interest`（T-76 坐标轴与保留字段，非定价输入）。

**新增字段一项**：`instrument_class`（路由键）。已言明面无路由键槽位——T-76 `option_type: enum{call,put}` 为强制枚举，GK-31 之 `instrument_type: enum{linear,option}` 为二值域，均不足以承载契约②所要求之六品种路由。本根取用 `instrument_class`，值域逐项取自撞墙清单_T-76 v2.3 缺口描述原文所列六品种。**本根工程取用，不外推为跨根命名规范**（形态先例＝T-76 schema §1 同型声明）；是否升为常设接口＝骨架/模块层归纳反推之事（裁决14），本根不预裁。**呈KD**：字段名与值域取用之追认。

`instrument_class=spot/spot_etf/index` 之 lot 其 `expiry`/`strike`/`implied_vol` 退化取 `null`，`option_type` 退化取 `"NA"`（退化形态先例＝GK-31 schema §1 点3 之 linear 节点退化处置）。

---

## §3 品种路由声明（契约②）

```
ROUTE_DECLARATION
spot | linear_underlying | closed_on_stated_face |
spot_etf | linear_underlying | closed_on_stated_face |
index | linear_underlying | closed_on_stated_face |
futures | linear_underlying_futures_stub | placeholder_stub | futures_settlement_form,dividend_carry
european_option | bs_no_dividend_closed_form | computed_with_open_dimensions | dividend_carry,day_count_convention
american_option | american_via_european_stub | placeholder_stub | early_exercise,dividend_carry,day_count_convention
```

（四列＝品种｜route_id｜可算性标注｜命中之未言明维度；空第四列表示零命中。）

**`unstated_dimensions_hit` 之标注语义（裁决48 §3 既裁，乙·求值路径特征级命中）**：该字段＝「该求值路径之计算是否进入该维度」。线性恒等求值不含时间投影，股息维度不进入计算，故 `spot`／`spot_etf`／`index` 三条线性路由均零命中；`european_option`／`american_option`（时间投影在场）与 `futures`（结算/持有成本形态本身未言明）维持各自命中。**该零命中标注仅就求值路径而言，不构成"线性持仓无股息经济影响"之主张**——经济层股息现金流缺口（含线性持仓 bleed 漏分红之实况）由撞墙清单 TPL1-T7601-01 之缺口描述全域承载，信息零丢失。

**可算性三态口径**（降格标注，三分判别 §3 处置要求）：
- `closed_on_stated_face`：求值规则在已言明面上闭合，零未言明维度命中。
- `computed_with_open_dimensions`：求值规则本身在已言明面上可执行，但存在未建模的未言明维度（其影响未计入）。
- `placeholder_stub`：求值规则本身即占位桩——该路由之正确求值方式未言明，本根以确定性最简路径承接。

**桩纪律（三分判别 §3）**：`futures` 分支与 `linear_underlying` 在阶段A数值重合，`american_option` 分支与 `bs_no_dividend_closed_form` 在阶段A数值重合。**两处数值重合均不构成语义等价宣称**，亦不构成对期货持有成本、或对早行权溢价之大小/方向的任何断言。

**构造侧核心呈报（按裁决48 §3 订正后口径）**：契约②要求六品种路由，而已言明最小面**对 3/6 品种（`spot`／`spot_etf`／`index`）闭合**；其余三品种（`futures`／`european_option`／`american_option`）各命中至少一项未言明维度。此即45-B1所预期之"留引擎切片撞墙"实况，缺口逐项登记于撞墙清单，未静默收窄品种域。契约②之"覆盖"经裁决48 §3 判**满足**（路由身份在场、六品种实跑全覆盖、SM8变异反证品种域未静默收窄）；闭合度低系45-B1预期形态，非契约②违反。

---

## §4 量纲口径（契约③）

**契约本体＝T-76 schema 原文，指针入包不转写**（45-JP1/B2）：一阶实体_T-76_input_schema_v2_2_20260714.md **行80**。人读辅助件＝QT-002（读法辅助，非规范载体）。

**本实体之口径实现与可证伪化**：五希腊按其偏导定义直接产出，零缩放。断言基线不取自上述源文之人工转抄，而由独立复算路径按偏导定义**独立生成**（verify/independent_recompute.py：delta=∂V/∂S、gamma=∂²V/∂S²、vega=∂V/∂σ、theta=−∂V/∂T、rho=∂V/∂r，T 以年为单位）。量纲断言另附**否定式判别**：若产出为 vega/100、theta/365 或 rho/100 形态，断言应失败——该否定式核验使量纲断言具备区分力而非同义反复。

---

## §5 输出形态声明（裁决39-B，输出形态封闭）

**顶层键集声明**（harness_output.json 顶层键集须**恰等于**下列集合，无未声明键、无静默删键）：

```
OUTPUT_TOPLEVEL_DECLARATION
_data_source
_declaration_ref
route_table
base_valuation
scenario_revaluation
time_shift_revaluation
```

**per-lot 记录键集声明**（`base_valuation` / `scenario_revaluation` / `time_shift_revaluation` 三容器内每条记录）：

```
RECORD_KEY_DECLARATION
lot_id
instrument_class
route_id
computability_status
unstated_dimensions_hit
per_unit
per_lot
```

**分量键集声明**（`per_unit` 与 `per_lot` 各自，契约①之 5全集＋V(t)）：

```
COMPONENT_KEY_DECLARATION
value
delta
gamma
vega
theta
rho
```

`per_lot` 分量＝`per_unit` 分量 × `multiplier` × `quantity` × `side_sign`（已言明面 T-76 §4 **行76** 之 position 缩放式；**估值 V(t) 同施 side_sign** ——空头持仓估值为负，与 T-24 §4① 之 bleed＝V(t0)−V(t1) 消费面方向一致。此为本根对行76式之一致外延，**呈KD追认**）。

---

## §5.1 计算约定声明面（裁决48-2 兑现；声明-实现一致性断言之判据基线）

本块承载「已在本 schema 内成文、但此前无对应断言」之计算约定，供 `verify/assert_check.py` 程序化解析后对 `entity/engine.py` 与 `verify/independent_recompute.py` **双侧**对表。范围钉死＝裁决48-2 所限定之六例形态（C1／C2／C4／C7／C8b／C10 所违反者），**不扩至情景构造式（C3，维持35-A固有上限口径）**。

```
CONVENTION_DECLARATION
day_count_denominator | 365
side_sign_long | 1
side_sign_short | -1
per_lot_scaling_factors | multiplier,quantity,side_sign
vega_unit | per_1.0_sigma
theta_unit | per_year
rho_unit | per_1.0_r
industry_scaling | none
futures_stub_carry | none
option_identity_routes | bs_no_dividend_closed_form,american_via_european_stub
linear_identity_routes | linear_underlying,linear_underlying_futures_stub
```

**各行之出处与可证伪化形态**：

| 声明行 | 出处 | 断言形态（脚本侧） |
|---|---|---|
| `day_count_denominator` | §6 表行10（ACT/365 占位取值，不外推） | 源级：两侧实现之分母字面量对表；行为级：由产出反解 T（rho 恒等式）再折算分母 |
| `side_sign_long` / `side_sign_short` | §5 缩放式（"空头持仓估值为负"） | 行为级：逐笔 `per_lot ＝ per_unit × multiplier × quantity × side_sign` 双侧核验 |
| `per_lot_scaling_factors` | §5 缩放式（T-76 §4 行76） | 源级：两侧 `scale` 表达式之因子集对表；行为级：同上 |
| `vega_unit` / `theta_unit` / `rho_unit` / `industry_scaling` | §4 量纲口径（契约③，指针锚＝T-76 schema 行80） | 行为级：三条闭式恒等式（见下）双侧核验；另有 A7-b 否定式判别 |
| `futures_stub_carry` | §3 桩纪律（期货分支"不引入任何持有成本或结算约定"） | 行为级：期货路由 per_unit 与标的报价逐笔恒等，五希腊取 (1,0,0,0,0) |

**行为级恒等式（仅施于 `option_identity_routes` 所列路由；模型族依赖经声明面显式限定，不构成对类三成分6之判据级固化）**：

1. `rho = T · (S · delta − V)` ——对 call/put 同式成立；反解 T 后与 `day_count_denominator` 折算对表，同时钉定 `rho_unit`。
2. `vega = gamma · S² · σ · T` ——钉定 `vega_unit`（若产出为 per 1% 形态则不成立）。
3. `theta + ½σ²S²·gamma + r·S·delta − r·V = 0`（Black-Scholes 偏微分方程，`theta ＝ ∂V/∂t`）——钉定 `theta_unit`（若产出为按日计则不成立）。

三式为无股息欧式闭式解之解析恒等式，**属计算约定之可证伪化手段，不构成对定价模型族之选定**（成分6 之类三地位不变；恒等式适用面由 `option_identity_routes` 声明行界定，阶段B 换族时随声明面同步改写）。

---

## §6 三分判别套用全表（裁决21(a)受控文本 v1.1；双重引用纪律遵行）

前置分流（数据/机制刀口）：`scenario_shock` 幅度值（−5%、+3 vol pts）、`time_shift.days_forward`、以及全部 S/K/σ/r/持仓明细取值＝**数据**（人造input构造自由度，裁决17(a)口径），不入三分。

| # | 计算成分 | 判别 | 实质依据（双重引用之实质侧） | 处置 |
|---|---|---|---|---|
| 1 | 品种路由结构（按品种选取求值路径） | **类一** | 缺口描述原文"按品种（现货/现货ETF/期货/指数/欧式/美式期权）路由适用定价模型"（撞墙清单_T-76 v2.3）＋契约②（裁决45 §5） | 定案写入实现，非桩 |
| 2 | 供给物语义类型（5全集raw Greeks＋V(t)） | **类一** | 契约①（45-IC4/45-IC2） | 定案写入实现 |
| 3 | raw 量纲口径 | **类一** | 契约③；原文锚＝T-76 schema 行80（指针） | 定案写入实现 |
| 4 | per_lot 缩放式（×multiplier×quantity×side_sign） | **类一**（结构） | 已言明面 T-76 §4 **行76** | 定案；V(t) 同施 side_sign 之外延呈KD追认 |
| 5 | 线性标的求值规则（V＝标的报价，Δ=1，其余为0） | **类一（条件性定案）** | **条件＝零持有成本占位下之恒等映射**。在该条件下无模型自由度；查过：缺口描述原文、契约六条、审计表行94/95——均未与恒等映射矛盾。`rho=0`／`theta=0` 系该占位条件之直接后果，**非对成分7 之独立处置**，故与成分7 之类二登记无层次交叉（Q-13 订正，裁决48 §3） | 定案写入实现；条件由成分7（类二）承载，成分7 闭合时本行随之复核 |
| 6 | **定价模型族选型**（欧式分支之标的动力学假设：GBM闭式解 vs 其他） | **类三** | 类一测试判"裁不了"：查过契约六条、缺口描述原文、审计表行94（EP-05 不授权栏行125：不禁用BSM类模型作仪表计算器/换算工具——**许可而非选定**）、行95（EP-06 派生量＝观测仪表）；全候选与全部权威文本相容 | 阶段A跑具体版本＝无股息BS闭式解，**候选之一，声明值不外推，待阶段B以回测/实盘数据证伪**；不留白 |
| 7 | **股息/持有成本维度** | **类二·缺定义型** | 45-B1 明列为未言明维度；全项目文本无权威计算定义 | 确定性占位＝零调整分支；模板一登记 TPL1-T7601-01 |
| 8 | **期货结算/保证金形态** | **类二·缺定义型** | 45-B1 明列 | 确定性占位＝恒等承接（不引入持有成本）；模板一登记 TPL1-T7601-02 |
| 9 | **美式早行权定价** | **类二·缺实现型** | 45-B1 明列；求值方式无权威定义 | 确定性占位＝欧式闭式解路径承接，不claim语义等价；模板一登记 TPL1-T7601-03 |
| 10 | **day count 约定**（T＝dte/分母） | **类二·缺定义型** | 45-B1 明列；约定属规范选择，非经验裁定，故非类三 | 确定性占位＝ACT/365（同T-76 §4 桩既有取值，不外推）；模板一登记 TPL1-T7601-04 |
| 11 | dte 整数天口径（(expiry−valuation_date).days） | **类一** | T-76 schema §3 已言明口径 | 定案写入实现 |
| 12 | IV 之输入身份（市场报价坐标 vs 模型派生量） | **类一** | 审计表行95（EP-06 行135：IV作为市场报价的坐标仍可读，被否定的是其模型本体论地位） | 定案：可作输入；**呈KD**——缺口描述原文之行情枚举（价格、期限、到期日、bid/ask、类型等）未列IV，边界确认请KD追认 |

**否定结论义务留痕**（受控文本 §2）：成分6之类一测试判"裁不了"，已查文本见上表；成分7/8/9/10之类一测试同判"裁不了"（查过：契约六条、缺口描述原文、45-B1条款、审计表行94/95/96），进类二测试后指向待建供给方/待裁定义。

---

## §7 容差口径与成分级分派（裁决13/19 ＋ QT-001）

- 子口径(a) 离散/精确有理计算＝**bit-exact（diff=0）**（裁决13）。
- 子口径(b) 连续解析计算（超越函数路径）＝**相对 diff ≤ 1e-12**（裁决19）。
- **QT-001 成分级（非族级）分派**（期权波动率工程笔记 v1.2 行19/26，裁决34-F2）：分派作用于数值成分本身，非计算上下文。本根实况：`linear_underlying` / `linear_underlying_futures_stub` 路由之全部12分量（per_unit＋per_lot）落 (a)，与期权路由分量同处三容器之内，仍逐分量按 (a) 比对；期权路由分量落 (b)。

---

## §8 缺口引用与登记指针

本体缺口 TPL1-T76-01（撞墙清单_T-76 v2.3 行12–24，open）＝本切片对象自身，引用不重登。构造中新撞四条（TPL1-T7601-01～04）登记于 `撞墙清单_TPL1-T76-01引擎_v1_0_20260730.md`，模板一。DOC-11 随行注记：估值输出 V(t) 已在1级契约（45-IC2），清单缺口描述非范围上限。

---

## §8.1 检测器完整性声明（D-4 兑现，裁决48 §4）

`verify/scan_patterns.json` 承载 step0(ii) 之数据源关键词集与 bare-import 正则、A6 之宣称模式集/否定标记集/窗口参数。该件按构造排除于扫描面（否则模式表逐条自命中），其内容此前不受任何断言约束（外审 S7 实证：删关键词后 step0(ii) 仍全绿）。

**处置＝指纹断言钉定**（裁决48 §4 二选一之后者）。指纹值载于本声明面而非脚本内常量，以维持"判据基线一律程序化解析自本包内源文件、零人工转抄常量"之既有形态（避免新增写死常量，Q-8 张力不加剧）。

```
DETECTOR_FINGERPRINT_DECLARATION
verify/scan_patterns.json | sha256 | f17de0f5544f377daba514e690aa347a6a37f5c20c12746f507f9a0555ebc74c
```

模式表内容任何变动（含删关键词、放宽正则、缩小窗口）均使指纹失配而 FAIL；模式表之正当再版须同批改写本声明行，改写动作因而落入人读可见面。

---

## §9 数据源纪律声明（契约⑤）

`entity/` 与 `verify/` 全部代码零网络、零行情接口、零外部数据源读取；输入面仅消费行情类字段与持仓静态属性，Greeks 与估值一律自算。输入记录中不存在任何 vendor Greeks / 理论价字段（断言可证伪：输入键集与 vendor 派生量键名集之交为空）。

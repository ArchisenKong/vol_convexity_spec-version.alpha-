# T3-03 input schema · v1.1 · 20260711

> **v1.1修订（裁决17落地）**：§3.4 情景变换规则由"人造声明输入"改标**降格占位桩**——定案形态＝重估（类一，源文语义裁定：T2/00A§4行81"情景下重估"＋GK行398"固定参数Gamma不足…co-move情景下重估"＋GK§2.3.1行232），本根线性近似仅为占位；重估实现＝缺实现型缺口，供给方引用 TPL1-T76-01（不重登）。情景幅度值（−5%/+3pt）维持数据定性（input构造自由度）。§4.1 同步替换。数值与A/B产物零变动（除裁决C空格修复：governance_input.aggregation_scope 补锚原文）。

## §1 raw ledger 维度取用裁定（本根工程裁定，不外推）

维度字段最小充分集：`leg_id / tenor_days / side / option_type / moneyness / delta / gamma / vega / theta / rho`。

- 不单独保留 lot 级细粒度：`leg_id` 代表已完成 lot 聚合后的持仓单位。理由：Q4 判据只需六 slice 状态值＋标注，非 lot 级可追溯性；`leg_id` 足以充当 raw ledger 的原始节点标识。若后续对象需要 lot 级颗粒度，需回到本处扩展，本裁定不外推为跨根规范（同型先例：T-76 input_schema §1 lot_id 处置）。
- `expiry` 以 `tenor_days`（30 / 90）代表 tenor bucket，不另建日历日期字段——本根测试目的不需日历精度。
- 全部 Greeks 值取**持仓级（position-level，已含方向符号）**，非单腿裸期权级：short 头寸的 gamma/vega 符号相对 long 头寸反转，theta 符号相应反转（short 端正 theta = 卖方获得时间价值）。此为标准持仓 Greeks 符号约定，非本根发明。

## §2 raw ledger 人造数据（4 legs，短端卖权利金＋长端买保护结构）

| leg_id | tenor_days | side | option_type | moneyness | delta | gamma | vega | theta | rho |
|---|---|---|---|---|---|---|---|---|---|
| L1 | 30 | short | put | 0.90 | +2.00 | -0.15 | -80.0 | +120.0 | +15.0 |
| L2 | 30 | short | call | 1.10 | -1.80 | -0.12 | -70.0 | +100.0 | -12.0 |
| L3 | 90 | long | put | 0.80 | -1.25 | +0.04 | +75.0 | -25.0 | -15.0 |
| L4 | 90 | long | call | 1.20 | +1.10 | +0.035 | +70.0 | -22.5 | +14.0 |

`_data_source: synthetic_hand_constructed`（见 `input_data.json`）。全部数值为手工构造有理数，无任何数据源接入。

## §3 聚合声明（各派生 slice 所需，人造构造；结构性字段名锚 T3§13.2 与 T2/00A§4 行77-82，取值为本根声明）

### 3.1 proxy Greeks 声明
- 压缩范围：按 `tenor_days` 分桶（30D / 90D），指标子集限定 `{delta, gamma, vega}`（本根声明范围，不含 theta/rho）。

### 3.2 diagnostic Greeks 声明
- diagnostic unit：`gamma_center`（gamma 幅值加权 moneyness 均值）、`vega_concentration`（最大 tenor 桶 |vega| 占总 |vega| 比例）。
- 来源节点：全部 4 legs。
- 解释范围：跨 tenor 全组合。
- **计算规则来源＝本会话占位声明，非方法论权威定义**（见 §4.2 撞墙登记 TPL1-T303-02）。

### 3.3 risk-equivalent Greeks 声明
- 等价规则：30D-tenor 桶 Vega/Gamma 按声明比例 `r=1/2` 折算为 90D-tenor-equivalent 单位（`90D等效值 = 30D桶值×1/2 + 90D桶值×1`）。
- 聚合范围：跨两个 tenor 桶，指标子集 `{gamma, vega}`。
- 适用假设：假定平坦期限结构衰减比 1:2（30D:90D），期限结构倒挂时不适用（声明性假设，未经真实波动率曲面校验）。
- **等价比例规则来源＝本会话占位声明，非方法论权威定义**（见 §4.2 撞墙登记 TPL1-T303-01）。

### 3.4 scenario-stressed Greeks 声明（S1）〔v1.1 裁决17改标〕
- 情景：价格冲击 ΔS = spot×(-5%)，spot 声明为 100，故 ΔS_dollar = -5；IV 冲击 +3 vol pts，声明 vega 敏感系数 2%/vol pt，故 vega 乘子 = 1 + 0.02×3 = 1.06。
- 节点范围：全部 4 legs；声明字段范围限定 `{delta, vega}`（gamma/theta/rho 不在本情景声明覆盖范围内）。
- 情景幅度值（−5%、+3 vol pts）＝数据（人造 input 构造自由度，裁决17）。
- 作用规则（**降格占位桩，裁决17**；定案形态＝重估，本根以固定参数线性近似占位，替换时点＝TPL1-T76-01 闭合）：
  - `stressed_delta_leg = raw_delta_leg + raw_gamma_leg × ΔS_dollar`（桩：固定参数一阶近似；源文 GK行398 明示 co-move 情景下固定参数 Gamma 不足，须重估——本式非定案形态）；
  - `stressed_vega_leg = raw_vega_leg × 1.06`（桩：固定响应系数 2%/vol pt 属作用规则成分，非幅度值；定案形态下由重估自然携带）。

### 3.5 governance input 声明
- 进入范围：`risk_equivalent.vega_90D_equiv`、`risk_equivalent.gamma_90D_equiv`、`scenario_stressed.delta_total_S1`、`scenario_stressed.vega_total_S1` 四项。
- lineage：均回指 `[L1, L2, L3, L4]` ＋ 各自声明版本号（`declaration_ref`）。

## §4 B段计算路线选择与撞墙登记指针

- **路线选择**：全程采用 Python `fractions.Fraction` 精确有理数运算，不引入超越函数（sqrt/exp/log 等），故全部六 slice 分量适用容差子口径 **(a) bit-exact（裁决13）**，无需子口径 (b)。
- **§4.1 情景成分（scenario-stressed）〔v1.1 依裁决17替换〕**：拆分三段——幅度值＝数据不登记；作用规则形态＝类一当场裁定为重估（源文行号见头部修订记录），线性近似降格为占位桩；重估实现＝类二缺实现，供给方＝TPL1-T76-01，**引用不重登**。原"预授权人造声明、不登记"判定作废（任务包§3该预授权文本本身系包生成缺陷，已随裁决17订正）。
- **§4.2 撞墙登记**（依裁决14/16 同构教训，机制成分实质决定输出数值且方法论无权威定义时不得判零登记）：
  - **TPL1-T303-01**：risk-equivalence rule（跨 tenor 等价折算比例）的权威计算定义缺失。GK§2.3.1（行228-232）自查结论：仅边界陈述（合法/非法用途），不构成计算规则。登记模板一，占位＝声明比例 r=1/2（桩，非实体算法要件，边界裁定留外审）。
  - **TPL1-T303-02**：diagnostic 解释规则（gamma center / vega concentration 等状态如何从 raw 计算）的权威计算定义缺失。全项目文档检索（00A/T3/GK/B-2/YAML Taxonomy Bridge）均只见状态标签枚举，无计算公式。登记模板一，占位＝声明公式（gamma 幅值加权均值 / 最大占比集中度，桩，非实体算法要件，边界裁定留外审）。
  - 详见 `撞墙清单_T3-03_v1_0_20260711.md`。

## §5 T-19 承接字段取值（六角色语义直接取值源＝T3§13.2表 / T2/00A§4 行77-82）

三字段（`source_phase` / `aggregation_scope` / `allowed_usage`）逐 slice 取值见切片记录附表，全部为源文原文摘录，非本根另造。T-19 六角色字段语义在本根全部套得动，无回传登记项。

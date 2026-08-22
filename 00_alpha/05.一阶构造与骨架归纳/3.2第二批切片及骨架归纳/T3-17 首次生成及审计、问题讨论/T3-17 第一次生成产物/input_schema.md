# T3-17 input schema · v1.0 · 20260718

对象：T3-17｜失效判据一：wing effectiveness（双翼有效性）。权威定义源＝T3§5.5行607；形状/数值分层＝T3§5.5行613-614。

## §1 实体-上游边界析出（C1，本根裁定登记#1）

**实体算法要件（T3-17自有机制）**：
1. moneyness band 位置判定——将当前 moneyness 与声明的 `target_activation_band` 区间比较，输出三态（below / within / above）。结构由 line 607"位置"语义直接决定，类一。
2. 情景响应比计算——`情景压力值 / 目标响应水平`，逐 Greek（vega、gamma）分别计算。结构类一（line 607 定义句直接给出比值关系）。
3. 双 Greek 响应比合成为单一 responsiveness 量——**结构类二，见 §4 缺口 TPL1-T317-01**。
4. 槽位比较与持续窗口判定——responsiveness 量 < `wing_responsiveness_floor` 的连续计数是否超过 `wing_dullness_window`，超过则 `wing_dullness` 触发。比较/计数结构类一（line 607"响应比低于槽位水平且持续超过槽位窗口"直接给出判据形状）；槽位**数值**类三。

**上游输入（非本根机制，声明性/桩性/校准性）**：
- T3-22 状态时序本身（moneyness、raw vega、raw gamma）——本切片人造代理，T3-22 对象未构造。
- `target_activation_band`、`target_response_level`——建仓/roll 治理动作声明产物，本切片作为已声明输入接收，不在 T3-17 内部生成。
- 情景定义（ΔS、ΔIV）——数据（input构造自由度，裁决17口径）。
- 情景作用规则（重估）——**结构类一定案为重估**（T2/00A§4行81＋GK行398＋GK§2.3.1行232，同 T3-03/GK-14 引用），**实现类二缺实现，供给方 TPL1-T76-01（引用不重登）**；本根以线性近似降格占位（§3）。
- 槽位数值（floor、window）——类三，阶段B校准（§2）。

本根裁定：不外推为跨根规范（同型先例：T3-03 §1、GK-14 §1、T-24 §1、TC-33 裁定登记#4）。

## §2 槽位数值（类三，阶段B校准占位，任务5 Step2 v1.2行100 Q3已确认"字段已登记定义、取值待赋"）

`wing_responsiveness_floor = 3/5`；`wing_dullness_window = 2`（连续超过2期即触发，第3个连续周期触发）。取值为阶段A候选之一，待阶段B证伪（受控文本§4处置口径），不登记模板一/二（同型先例：T-76 schema§3 H1注记、GK-14 w_τ）。

## §3 情景重估桩（C4桩纪律，供给方TPL1-T76-01引用不重登）

情景：ΔS_dollar = −5（spot声明100、−5%）；ΔIV = +3 vol pts（幅度值＝数据，input_data.json §scenario）。

作用规则（**降格占位桩**；定案形态＝重估，替换时点＝TPL1-T76-01闭合）：
- `stressed_vega_leg = raw_vega_leg × (1 + 2/100 × 3) = raw_vega_leg × 53/50`（桩：固定响应系数2%/vol pt，沿用T3-03 §3.4声明值，属作用规则成分非幅度值）；
- `stressed_gamma_leg = raw_gamma_leg × (1 + 3/100 × 3) = raw_gamma_leg × 109/100`（桩：固定响应系数3%/vol pt，**本根新声明**——T3-03桩未覆盖gamma情景响应，本值为本根工程裁定，不外推，供后续根/归纳复用参考非契约）。
- 桩不claim语义等价：桩与真值在当前样本数值重合不构成桩正确性宣称（C4纪律，GK-14 §2.3行33同源条款）。
- 声明字段范围：仅 {vega, gamma}，价格冲击ΔS对vega/gamma的二阶影响（vanna/speed类）不在本桩覆盖范围内（本根简化声明，理由同T3-03 §3.4"gamma/theta/rho不在情景声明覆盖范围内"限定模式，此处对称地限定"价格冲击对vega/gamma的二阶交叉项不覆盖"）。

## §4 双Greek响应比合成缺口（TPL1-T317-01，本会话主动自查登记）

全项目检索（T3§5.5行607、任务5 Step1/Step2/Step3、任务3收录清单）均只见"scenario-stressed Vega/Gamma相对基准情景的响应比"（单数"响应比"），未见任一处规定当 Vega 响应比与 Gamma 响应比不一致时如何合成为单一可与槽位比较的量。此为机制成分（决定 wing_dullness 是否触发的实质计算步骤），方法论无权威定义，依裁决14/16同构教训主动自查登记（不判零登记，同型先例＝TPL1-T303-01/02施工阶段自查登记）。

- **占位处理（桩）**：`combined_response_ratio(wing, t) = min(vega_response_ratio(wing, t), gamma_response_ratio(wing, t))`——确定性最简、worst-of保守合成，不claim为权威合成规则。
- 详见 `撞墙清单_T3-17_v1_0_20260718.md`。

## §5 B段计算路线选择与容差子口径

全程 `fractions.Fraction` 精确有理数运算：响应系数、目标响应水平、槽位、moneyness 边界全部为人造有理数；情景乘子固定有理数；比值、min比较、计数比较均为 `+ - × ÷` 与比较运算，无 sqrt/exp/log 等超越函数。适用容差子口径 **(a) bit-exact（裁决13）**，无需子口径(b)（同型先例：T3-03 §4、TC-33 §3、GK-14 §5）。

## §6 T3-22 代理时序输入结构（人造，覆盖Q4判据最小输入）

每翼（put/call）6期时序，字段：`t`（期号）、`moneyness`（有理数）、`raw_vega`、`raw_gamma`。构造意图：PUT翼 t1-t2健康、t3-t5响应比连续3期低于槽位（超槽位窗口2，第3期t5触发wing_dullness）、t6经roll恢复；CALL翼全程健康（负例对照，验证判据非全触发型）。`_data_source: synthetic_hand_constructed` 显式字段（骨架C6档二字段规范化候选，KD采纳20260718；先例＝TC-33 schema§5、T3-03 schema§2行22）。

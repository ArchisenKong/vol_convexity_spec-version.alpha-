# entity/input_schema.md · GL-09 正Carry时间占比状态量 · v1.1 · 20260808

> **v1.1（20260808，四4 GL-09 修复会话）**：按《修复会话开启文本 四4 GL-09 v1.0》§2 落地——甲-1（§1 三口径并存）／甲-2（§2 期切分未定义面声明）／甲-3（§3 消费面枚举补 `_dte_days`、TPL1-T7601-04 改闭合）／甲-4（§4③④ 重写为六槽位表）／甲-5·甲-6（§7 防线1/4）／甲-7（§12 层上界订正与字段面分列）／乙-4（§14 F4 块 21→26 键）；连带更新＝§2 字段表两槽位行、§6 输出面两键、§10 六槽位与乙-7 事后钉表标注。**修复会话零裁决、零自审**。
> **性质**：呈报态（构造会话产出，修复会话续产，候KD收讫落档，49-D）。本会话零裁决、零自审、零自评本根合格判定之终局效力。
> **构造会话身份**：切片构造会话（施工），独立新session、chat环境，授权源＝《任务包_四4_GL-09_v1_0_定案_20260805》。不自审、不裁决、不生成后续任务包（任务包§0）。排程＝甲案线3，并行硬约束下未读取、未依赖、未引用线1（四1∪四2）／线2（四3）会话之任何中间或最终产物；引擎相关引用一律取已收口版（续2 v1.2）。

---

## §0 对象与Q4判据锚定

**GL-09 ＝ 正Carry时间占比状态量**（一阶实体·取值形态；任务3产出v1.4 行307收录行；任务5_Step2增量产出v1.0 GL-09行阶次判定＝一阶实体ᵃ）。

**源文锚（判据级消费，GL行511–515，八份思想层源文之一，非T0三件套、无翻译层、不在翻译审计表审计域；C4②成对义务不命中，开工无审计表前置闸门——任务包§2.2）**：

> 《QQQAI杠铃结构交流_20260718-20250101_.md》
> 行511「**答：**」／行513「总体上是保持正 Carry 的即可，不用严格时时刻刻都要保持正 Theta。」／行515「一言以蔽之，以正 Carry 占 90%+ 时间下的正凸性，是最重要的。」
> （行号经 `verify/assert_check.py` 之 `source_anchor_check` 程序化实读核证，28-B(i)；不可定位即不通过，禁静默回退内嵌副本。）

**收录行既载之核心语义拆解**（任务3产出v1.4 行307）：**Carry口径 ≠ 时时正Theta**。

**Q4可算判据（权威转抄，任务5_Step2增量产出_v1.0 GL-09行，裁决51已裁态；本schema不新造对象级判据）**：

> Q0否→Q1是→Q3否→Q4是ᵃ→Q5是→Q6是→一阶实体ᵃ。Q0：时间占比度量单体。Q1：逐日Carry符号序列→占比统计，可核验；"Carry口径≠时时正Theta"为口径限定语（度量定义之一部分，非约束他物）。Q4ᵃ：喂账本Carry时序，出占比值与阈值比较；取值"90%"＝类三候选槽位。Q5：账本。

**Q0既裁边界（本schema/harness据此不实现任何下游处置逻辑）**：占比未达某水平时之处置动作（减仓/告警/roll调整等）——源文未定义，本根不补白、不代裁；harness止步于"占比量＋与源文参考锚之比较结果"，不产出任何动作。

**哲学准入记录**（任务5_Step3增量产出_v1_0_20260731 GL-09行，裁决51已裁态）：C-1~C-5全不命中——判据对象＝**历史**时间占比统计（已实现Carry序列），非未来占比预测；Carry口径限定语（≠时时正Theta）恰为类型澄清，非禁形；无禁形、不含P_B靶子、**C-6不标记**。C-1边界自查之误用形态见 §7（本schema强制收录，72-4注）。

---

## §1 语义硬约束（宪-ST-06 口径界定，强制明写；随包携带义务①，任务包§5）

**"Carry"** 于本根界定为：**组合层净时间价值现金流量（net time-value cashflow，extrinsic premium 成分）**——短端卖出腿之时间价值收入与长端保护腿之时间价值消耗于同一期间内之净额，**非瞬时 ∂V/∂t 之 Greeks 读数**（非希腊字母意义之 theta）。

**该界定之射程涵盖三种测算口径（裁决落地·新14；TPL3-GL09-01 槽位①-甲）**——本界定为**口径族层界定**，不锁定其中任一测算实现：

| 口径 | 测算形态 | 本根 |
|---|---|---|
| (i) | 模型估值时间价值差：`ΔEV = EV(t₁) − EV(t₀)`，其中 `EV = V_model − intrinsic` | **本根采纳** |
| (ii) | 账本入账现金流（已入账之权利金收支净额） | GL-06 形态 |
| (iii) | **extrinsic 成分之市值变动 ＋ 已平仓腿之 extrinsic 实现差** | 31-L 优先候选 |

**口径(iii) 之三项性质显式声明（新14）**：①**仍为时间价值成分口径**——其两个加项（未平仓腿之 extrinsic 市值变动、已平仓腿之 extrinsic 实现差）均以 extrinsic premium 成分为被测量，未引入 intrinsic 成分或 Greeks 成分，故落在宪-ST-06 "时间价值（extrinsic premium）现金流"之射程内；②**两侧同源**——短端与长端两侧均按同一 extrinsic 成分口径计量，满足宪-ST-06 可比性/一致性原则之"同一比较内口径同源"；③**不依赖定价模型**——市值变动取自市场成交/报价面，实现差取自实际平仓价，两者均非模型输出，故该口径**不引入 Greeks 引擎依赖**（与口径(i) 之关键分野，L3 合规性后果见 §4③ 附注1）。

**"Theta"** 于本根仅以**瞬时 ∂V/∂t 之 Greeks 口径读数**出现，且仅作**口径分离之对照诊断量**（§8），不参与占比量之定义与计算。

界定依据＝宪-ST-06 既裁口径（"本条'Theta'＝时间价值（extrinsic premium）现金流的代指……原型行文以'Theta'代指该收支流，非希腊字母瞬时Theta（∂V/∂t）"）＋宪-ST-06 可比性/一致性原则（"一切供血/消耗/性价比类比较须同一比较内口径同源——现金流类比较用时间价值成分口径〔ATM/OTM取全额、ITM取其期权价值中的时间价值成分〕，Greeks类度量用Greeks口径"）。此界定为KD既裁口径，非本schema自行创设；先例形态＝GL-06 schema §1（同族对象，同一条款落写）。

**ITM 时间价值成分提取（宪-ST-06 明文之落写）**：逐腿时间价值 `EV_unit = V_unit − intrinsic_unit`，其中 `intrinsic_unit = max(S−K,0)`（call）／`max(K−S,0)`（put）。ATM/OTM 之 `intrinsic_unit = 0`，`EV_unit = V_unit`（取全额）；ITM 腿据此扣除内在价值，仅留时间价值成分。人造持仓时序内 P3／P4（短端put实值）与 P8（短端call实值）三期刻意构造为 ITM 形态，使该提取步进入数值比对射程（非空转声明；`verify/assert_check.py` `A10_itm_extraction_effective`）。

**口径同源纪律（宪-ST-06 强制，任务包§5"对象核心命中"）**：本根之两口径量（时间价值现金流口径之 Carry 占比量／Greeks 口径之 Theta 读数占比量）**不进入任何同一个比值、差额或阈值比较**；`entity/harness.py` 不构造任何跨口径合成量（`contrast_diagnostic.no_cross_caliber_composite` 为该声明之输出侧载体，`assert_check.py` `A11_caliber_separation` 核证）。两者之**非同一性核证**（两占比量取值不等）为**口径区分之可指认性证据**，非供血/消耗/性价比类比较——本条界分呈KD裁定（§13 呈裁项4，A档）。

---

## §2 账本schema（人造input，`entity/ledger_input.json`）

输入形态＝**人造持仓时序 ＋ 人造行情坐标**（任务包§2.4；裁决1全程强制：不接IBKR／QuantConnect／历史行情／实时行情／任何文件数据源）。

| 字段 | 定义 |
|---|---|
| `_data_source` | 固定值 `synthetic_hand_constructed`（骨架C6档二字段规范化候选；先例＝GL-06／T3-18／TC-33／T3-03） |
| `slots.carry_measurement_caliber` | **（v1.1 新增，槽位①-甲）** Carry 之测算口径。本根取 `model_valuation_time_value_difference`＝口径(i)。`parameter_slot_candidate`，候选空间见 §1 三口径表与 §4③ 落地表 |
| `slots.carry_coordinate_regime` | 期间Carry之坐标推移形态（槽位①-乙）。本根取 `frozen_market_coordinates_time_advance_only`（期内 S/σ/r 冻结、仅推进日历时点）。`parameter_slot_candidate`，**仅在 ①-甲 取口径(i) 下有意义**，候选空间与登记建议见 §4③ |
| `slots.time_base_unit` | 时间基计量单位。本根取 `calendar_day`（整数日）。`parameter_slot_candidate`，见 §4④ |
| `slots.positivity_boundary` | "正Carry"之正的边界语义。本根取 `strict_greater_than_zero`（类一定案，见 §4②） |
| `slots.period_segmentation_rule` | **（v1.1 新增，槽位⑤）** 期切分规则。本根取 `position_structure_change_point_aligned`（期边界与持仓结构变更点重合之如实标注；**规则本身未成文**）。`parameter_slot_candidate`，见本节"期切分规则之如实声明"段与 §4③ 落地表 |
| `slots.aggregation_horizon` | 占比之聚合视界。本根取 `full_sample_cumulative`（全样本累计，单一占比量）。`parameter_slot_candidate`，见 §4④ |
| `source_reference_anchor.positive_carry_time_share_pct` | 源文参考锚取值＝90。**类三候选槽位**（Step2既裁"取值'90%'＝类三候选槽位"）；**非验收阈值、非合格判据组成部分**，见 §7 |
| `source_reference_anchor.comparator` | `greater_equal`（源文"90%+"含端点，类一定案，见 §4⑤） |
| `expected_pin.*` | 乙-2 期望值钉表节（与人造input同轮写定），见 §10 |
| `market_constants.risk_free_rate` / `.dividend_yield` | 行情坐标常量（r＝0.04、q＝0.0）。数据层构造自由度，不登记模板一/二 |
| `periods[].period_id` / `.t_start` / `.t_end` / `.duration_days` | 期标识与时间基。`duration_days` 为**声明值**，与由日期序差导出之 `duration_days_derived` 逐期核证一致（F-4） |
| `periods[].spot` / `.implied_vol` | 该期之人造行情坐标（期内冻结，见 §4③） |
| `periods[].boundary_construction` | 二值。`true` 标识刻意构造之边界期（本根仅 P5） |
| `periods[].legs[]` | 该期持有之持仓明细：`lot_id`／`instrument_class`／`option_type`／`side`／`strike`／`expiry`／`multiplier`／`quantity`。字段面取自引擎已言明最小面（`STATED_FACE_FIELDS`），行情坐标与 `valuation_date`／`dividend_yield` 由 harness 于调用时注入 |

**期切分规则之如实声明（新5，强制）**：本根 9 期之期切分为**构造自由度**，其期边界与**持仓结构变更点重合**（每期内持仓明细恒定，期边界处发生腿的增删或换约）。**该重合为如实标注之事实，切分规则本身未成文**——源文对"时间"之切分粒度与切分依据全无约束语，本根亦不就地创设规则。**实盘接入时期切分属未定义面**：实盘持仓变更为连续事件流，何为一"期"（持仓变更事件驱动／固定日历粒度／到期日驱动／其他）尚无权威供给，占比量之分子分母随该规则改换而改变。该面登记为 TPL3-GL09-01 槽位⑤（`ledger_input.json` `slots.period_segmentation_rule` 为其制品侧载体），**本根不补白、不代裁**。

**人造持仓时序设计（9期，累计38日，构造自由度，不外推）**：常态双翼书＝短端卖出双腿（call K=102／put K=98，短期限）＋长端买入双翼（put K=85／call K=118，长期限）。

- **非等长期**：期时长为 1／3／7／2／1／4／4／9／7 日——刻意构造为非等长，使"时长加权占比"与"等权期数占比"两候选取值分离（本根实测 31/38 ≠ 2/3），令加权形态进入可击落射程。
- **P5 恰零边界期**（`boundary_construction: true`）：完全对冲书＝同契约（put K=90、同到期）多空各5张。两节点之组合时间价值恒等为 `0.0`（IEEE754 下 x−x 精确为 0.0），期间 Carry 精确等于 `0.0`。用于断言实现采用严格 `> 0` 而非 `≥ 0` 语义（§4②）。
- **P9 口径背离期**：短端平值双腿（K=100）临近到期、长端双翼重仓。期初瞬时组合 Theta 读数为负（−3386.69），而期间 Carry 为正（+132.30）——源文行513"总体上保持正Carry即可，不用严格时时刻刻保持正Theta"之**可算实例**。
- **P4／P7 负Carry期**；**P3／P4／P8 ITM期**（§1 提取路径）。

---

## §3 随行指针与消费面声明（本根不就地裁口径）

1. **短端 premium（时间价值收入）口径与宪-ST-06 时间价值成分口径之同源性** → 治理册槽位候选信号 **#7**（ST-06/ST-08测算口径族，Phase B定）。本根不做同源性核验，随行携带指针（先例＝GL-06 schema §3①／T3-18 schema §2①）。
2. **长端保护成本时间价值消耗口径** → **TPL3-T24-01**（open，裁决记录D6登记；宪-ST-06不授权栏"长端日均消耗口径与已登记之TPL3-T24-01同域，走该既有登记不另立"）。**引用不重登**（一阶实体_T-24_input_schema.md §4–§7先例；GL-06 schema §3②同型处置）。
3. **day count 分母**（引擎侧 ACT/365）→ **TPL1-T7601-04**（**闭合**——ACT/365 经**裁决57-6**裁定为阶段A权威口径；闭合落写见《撞墙清单_TPL1-T76-01引擎 v1.3》头注修订②）。引用不重登。**本根之 day count 面有权威供给，非开口**（E-①(i) 之实质要求以权威供给满足，非以缺口登记满足）。

**输入域契约面（上游引用之性质界定）**：

- **T-24**（成本度量 bleed，M5；一阶实体_T-24_input_schema.md＋切片记录_T-24 v1.0，已收口，读不改）：共享"长端时间价值消耗"域语义与 TPL3-T24-01 指针；**本根不消费 T-24 之 harness 输出**。
- **T3-18**（供血关系失效之现金流域结构；T3-18_input_schema v1.1＋切片记录 v1.2，已收口，读不改）：共享账本现金流域结构参考；**本根不消费 T3-18 之 harness 输出**。
- **GL-06**（Theta收入配比判据，比值维度；schema v1.1＋切片记录 v1.1，已收口，读不改）：**互补维度契约**——GL-06 承载**比值维度**（短端时间价值收入 ÷ 长端日均消耗之倍数比较），本根承载**时间占比维度**（净Carry为正之时间份额）。两者共用宪-ST-06 之时间价值现金流口径，但**度量对象不同、不重叠、互不代行**（反面陈述见 §9①）；**本根不消费 GL-06 之 harness 输出**。
- 上述三者均为**语义关联与口径同源参照，非数据依赖边**（GL-06 schema §3同型处置）。

**引擎契约面（本根**触发**消费，与GL-06先例分歧点，如实声明）**：

- 消费形态＝**调用**（非声明值接收）。任务包§2.4"取何供给形态（调用/声明值接收）归构造会话判断呈KD"——本根判断＝调用，理由：任务包§2.1／§2.4 明定输入为"人造持仓时序＋人造行情坐标"，Carry 须由持仓与行情坐标经求值导出，声明值接收形态不满足该输入面。呈KD裁定（§13 呈裁项3，A档）。
- 消费对象＝ `entity/engine.py`（TPL1-T76-01 引擎续2求值口径增强 v1.2 之**逐字节复用件**）之两个调用点，**枚举完备**（D-3 落地；消费面枚举不限于判据链消费量）：
  - `evaluate_lot()`：取 `per_unit.value`（估值 V）与 `per_lot.theta`（Theta读数）。**判据链消费量**。
  - `engine._dte_days(t_end, t_start)`（`entity/harness.py` `compute_gl09` 内）：取期间日数 `duration_days_derived`，与账本声明值 `duration_days` 逐期核证一致（A8 之"两独立日期算法一致"结构）。**辅助核验路径消费量，不入判据链之数值面**。该调用消费引擎之私有函数（下划线前缀），如实声明；引擎侧未就该函数作稳定性承诺，故其**再版敏感性**随 F-12 触发式重验义务一并覆盖。
- **装载核证（裁决69扩项(i)）**：`entity/engine.py` 与《切片记录_TPL1-T76-01引擎_续2求值口径增强 v1.2》指纹列声明之 `entity/engine.py` SHA256 逐字节一致＝`e31fbcfeacebeb196f7e1d63f41089e7e0a7deb3cc9a9a8b44941af31e194e99`。本会话对 `/mnt/project/` 与工作区内之引擎源码**零写入**。
- **F-12 逐字复用之机械核证**：本根宣称"逐字节复用"，故以整文件 SHA256 重算比对承载该 claim，不以文字声明承载（`assert_check.py` `A14_engine_verbatim_reuse`）。**触发式重验义务**：引擎再版或 #8 对照批触碰时重验（登记于撞墙清单，条目形态比照 TPL-FW03A-02 先例）。
- 路由面＝ `european_option` → `bs_dividend_yield_closed_form`（`computability_status = computed_with_open_dimensions`；`unstated_dimensions_hit = ["day_count_convention"]`）。本根不消费 `futures`／`american_option` 桩路由。

---

## §4 核心公式三层三分判别（《计算成分三分判别受控文本》v1.1 落地口径；乙-7 单向回引条款号；双重引用＝受控文本程序性纪律＋成分实质依据）

| # | 计算成分 | 判别 | 依据（双重引用） | 处置 |
|---|---|---|---|---|
| ① | **Carry 之口径归属**（时间价值现金流口径 vs 瞬时 ∂V/∂t 之 Greeks 口径） | **类一**（语义即裁，当场定案） | 受控文本 §2；实质依据＝宪-ST-06 口径界定（"'Theta'＝时间价值（extrinsic premium）现金流的代指……非希腊字母瞬时Theta"）＋源文行513本身（"保持正 Carry……不用严格时时刻刻保持正 Theta"——两词并置且被明确区分，取"Carry＝瞬时Theta"之候选与该句矛盾）。**否定结论义务不触发**（测试成立） | 裁A，定案写入 `entity/harness.py`（`_evaluate_node` 之 EV 口径路径）＋ `verify/independent_recompute.py`（同口径、独立实现路径） |
| ② | **"正Carry"之"正"的边界语义**（`> 0` vs `≥ 0`） | **类一**（语义即裁） | 受控文本 §2；实质依据＝汉语"正"之语义为严格大于零（"非负"另有专词），源文行513／515两处均作"正 Carry"而未作"非负 Carry"，候选 `≥ 0` 与该措辞矛盾。**查过并记录**：源文行511–515全段、宪-ST-06 条款全文、GL-06/S6-11 同族既裁文本，均无将零计入"正"之相容读法 | 裁A，定案写入 `_is_positive_carry`（`carry_value > 0.0`）；P5 恰零边界期为其可击落载体（NC-1 变异注入实证） |
| ③ | **Carry 之测算口径 ＋ 期间坐标推移形态**（槽位①-甲／①-乙） | **类三**（阶段B校准项） | 受控文本 §4；实质依据＝源文对"Carry"之测算方式与期间计量方式全无约束语，全部候选与权威文本相容（口径(i)(ii)(iii) 三者均落在宪-ST-06"时间价值成分"射程内，见 §1） | 阶段A跑 ①-甲＝口径(i)、①-乙＝候选(a)，标注"候选之一，待Phase B证伪，不外推为规范"，不留白。**登记形态＝ TPL3-GL09-01 六槽位族条目**（下表逐字落写；比照 TPL3-GL06-01 先例）。**是否登记、编号、指针挂靠均由KD裁定**；本根不自行裁定登记与否 |
| ④ | **时间基单位／聚合视界／参考锚取值／期切分规则**（槽位②③④⑤） | **类三**（阶段B校准项） | 受控文本 §4；实质依据＝源文"占 90%+ 时间"未指明时间基粒度、未指明统计视界、未指明期切分依据，参考锚数值亦无权威文本可排除候选，全部候选相容 | 阶段A跑 `calendar_day` ＋ `full_sample_cumulative` ＋ `9/10` ＋ 本根实际期切分形态，标注候选之一不外推。并入下表 **TPL3-GL09-01** 六槽位族条目，呈KD裁定 |
| ⑤ | **参考锚比较子方向**（`≥` vs `>`） | **类一**（语义即裁） | 受控文本 §2；实质依据＝源文"90%+"之"+"字面含端点，候选 `>` 与之矛盾 | 裁A，定案写入 harness（`ratio >= ref_thr`）。**注**：该比较之**取值90**属⑥；该比较之**结果**不进入合格判据（§7） |
| ⑥ | **参考锚取值"90%"** | **类三**（阶段B校准项） | 受控文本 §4；实质依据＝任务5_Step2增量产出 GL-09行既裁"取值'90%'＝类三候选槽位"；数值本身无权威文本可排除候选 | 阶段A候选值＝9/10（源文字面值），标注"候选之一，待Phase B证伪，不外推为规范"，不留白。**并入 TPL3-GL09-01 族条目第四槽位**，呈KD。**误用防线见 §7** |
| ⑦ | **逐腿估值 V 之定价模型族** | **数据/机制刀口下之上游既裁项**（本根不重判） | 受控文本 §1（数据/机制刀口）＋ §5 KD既裁项三分表处置条款（IND3-14→65-29：经KD直接裁定之成分进入三分表**仅作登记与承接，不重走判别测试路径**）；实质依据＝引擎侧既裁（TPL3-T7601-01 类三·阶段B校准项，裁决52-2） | 本根**引用不重登**：消费引擎求值结果为值，模型族选型不在本根范围 |

### §4③④ 落地表 · TPL3-GL09-01 六槽位族（定案形态）

| # | 槽位 | 阶段A取值 | 候选空间 |
|---|---|---|---|
| **①-甲** | **测算口径** | 模型估值时间价值差〔口径(i)〕 | (i) 模型估值时间价值差〔本根采纳〕／(ii) 账本入账现金流〔GL-06 形态〕／(iii) extrinsic 成分之市值变动＋已平仓腿之 extrinsic 实现差〔31-L 优先候选，经新14 定形〕 |
| **①-乙** | 坐标推移形态 | `frozen_market_coordinates_time_advance_only` | (a) 期内 S/σ/r 冻结仅推进时点〔采纳〕／(b) 实际坐标推移／(c) 分解式。**仅在 ①-甲 取口径(i) 下有意义** |
| **②** | 时间基计量单位 | `calendar_day` | 日历日〔采纳〕／交易日／小时／分钟 |
| **③** | 占比之聚合视界 | `full_sample_cumulative` | 全样本累计〔采纳〕／滚动窗口／日历分段 |
| **④** | 源文参考锚取值 | `9/10` | 数值无权威文本可排除候选 |
| **⑤** | **期切分规则** | 本根实际形态（人造声明，边界与持仓结构变更点重合） | 持仓变更事件驱动／固定日历粒度／到期日驱动 |

**①-甲 附注1｜L3 合规性**：口径(i) **不入 L3 合格叙述链**（《合格判据链骨架》L3 形态铁律2："断言对象＝账本与约束，非Greeks；Greeks引擎为诊断仪表，不入L3合格叙述链"；口径(i) 依赖定价模型）；口径(ii)(iii) 合规。**L1→L3 存在强制换口径断点。**

**①-甲 附注2｜换装联动**：口径(iii) 与**零轴基准不相容**（裁决31-L 注记②："MTM口径下判据形态由市场路径主导〔暴跌窗口 gap 大幅转正、vol crush 窗口深负〕，零轴基准易误触发，须与历史分布基准候选配套评估"）。换装 ①-甲 至口径(iii) 须**同批重议 `positivity_boundary` 之类一定案**（即本表 §4② 之 `strict_greater_than_zero`）。此为**类三槽位换装推翻类一定案**之形态，既往各根未出现。

**①-甲 附注3｜参考锚口径未核证**：④ 之 `9/10` 口径归属**源文未记载**；其与实测占比之比较为**跨口径未核证比较**，仅承载 Step2 Q4 判据面之形式要求，不构成可比结论。制品侧载体＝ `harness_output.json` `state_quantity.reference_anchor_caliber = unstated_in_source` ＋ `threshold_comparison_caliber_verified = false`。

**④ 联动注记**：取值与 ①-甲 耦合。**换装 ①-甲 之任一口径，④ 之候选值须重取，不得沿用 9/10。** 阶段A候选值 9/10 仅对口径(i) 之形式比较有效，不构成任何口径下的目标水平。

**族条目指针**：挂 **#7**（ST-06/ST-08 测算口径族，含"分子分母构造"）＋ **#12**（bleed 治理消费口径，指针→TPL3-T24-01＋31-L 注记），**引用不重登**。

**已知副作用如实登记（槽位组合敏感性）**：①-甲取口径(i) × ①-乙取候选(a) 之组合下，期内 S 冻结 ⇒ intrinsic 期内恒定 ⇒ `ΔEV ≡ ΔV`，故 ITM 提取步对**期间Carry之数值**无影响；该步之非空转性由逐腿 `ev_unit` 进入数值比对射程承载（§1末段）。**换 ①-乙 为候选(b) 该副作用即刻消失；换 ①-甲 为口径(ii)/(iii) 该步骤本身不存在**（口径(ii)(iii) 不经模型估值路径提取 intrinsic）。

---

## §5 H/P/W标注（O-S3i-1 随行义务，任务包§5"本根命中"；撞到即记，登记观察非判据缺陷）

源文引用段（GL行511–515）自行完成 H/P/W 标注（八份思想层源文无原生 H/P/W 标注可携带，递延义务见 Step3增量产出 §3 O-S3i-1；通道形态承 GL-06 schema §5 首批走通先例）：

- **H层锚点（硬核/身份承诺）**：行515"以正 Carry 占 90%+ 时间下的**正凸性**，是**最重要**的"之**优先序断言**——"正凸性为第一位"已由宪-ST-06 收为结构存续之第一要求（"以正Carry占90%以上时间为前提的正凸性，是结构存续的第一要求"）。该优先序为**结构层承诺**，非本源文自行创设之身份断言，标 H 层。
- **P层（可证伪/可修正/可替换之辅助假设）**：行513"总体上……不用严格时时刻刻"之**宽严度设定**，与行515之**具体占比水平"90%+"**——两者均为从业者操作性准则，可被证伪、修正、替换，符合 P 层定义。具体占比取值即 P 层参数，随 §4⑥ 类三槽位处置。
- **W层（当前状态/路径弱判断/人工裁量输入）**：**不适用**——本源文段无当前状态量、无路径弱判断、无人工裁量输入成分需标注。

**标注结果呈KD裁定分类是否成立**（任务包§6呈裁项1；GL-06 先例＝呈KD登记项形态）。

---

## §6 输出形态（模板三 C 段；对象Q4判据"出什么"为准）

`entity/harness_output.json` 之交付面：

- **状态量（本根交付物）**：`state_quantity.positive_carry_time_share` ＝ {`numerator_days`／`denominator_days`／`exact_fraction`（既约有理数字符串）／`decimal`／`caliber`}。本根实测＝ **31/38**（≈0.8158）。
- **Q4判据"与阈值比较"面**：`state_quantity.share_meets_reference_threshold`（本根实测＝ `false`）＋ `reference_threshold_exact`（9/10）＋ 状态标注两项（§7）＋ **（v1.1 新增）`reference_anchor_caliber = unstated_in_source` 与 `threshold_comparison_caliber_verified = false`**——参考锚之口径归属源文未记载，该比较为**跨口径未核证比较**，仅承载 Step2 Q4 判据面之形式要求，不构成可比结论（§4③ 落地表 ①-甲 附注3）。
- **逐期支持性数值**：`periods[]` 之 `tv_pos_start`／`tv_pos_end`／`carry`／`carry_positive`／`carry_sign_margin`／`theta_reading_start`／`theta_reading_end`／逐腿明细（`value_unit`／`intrinsic_unit`／`ev_unit`／`signed_scale`／`tv_pos`／`theta_per_lot`／`route_id`／`computability_status`／`unstated_dimensions_hit`）。
- **对照诊断量（非交付状态量）**：`contrast_diagnostic`（§8）／`discrimination_contrast`（等权期数占比，仅证时长加权之区分力）。
- **非信号声明**：`non_signal_declaration` 字段（§9②）。

---

## §7 误用/失效条件声明（**强制**，任务包§2.3／§5；C-1 边界自查留痕承接，裁决72-4注）

**既留痕之误用形态（原样收录）**：将源文"预期90%时间为正"当作**构造目标**或**合格判据**——该形态经 Step3 增量产出 GL-09行 C-1 边界自查留痕在案（"若被误用为'预期90%时间为正'即C-1命中，该误用形态记入任务6'误用/失效条件声明'素材"）。

**本根之防线（逐条可检）**：

1. 源文"90%+"＝**思想层期望性陈述**，非验收阈值、非预测承诺。该占比水平＝**宪-ST-06 不变量之参数位**（数值归参数挂接，既裁拆分线 20260723·轮③），**非本切片 L1 合格判据组成部分**。`ledger_input.json` 之 `source_reference_anchor._status` 与 harness 输出之 `reference_threshold_status = source_reference_anchor_not_acceptance_criterion` 为该定性之制品侧载体。
2. **本切片合格判定不以任何实测占比达到90%为条件**。合格对象＝占比量之**定义、可算性与可复现性**，非占比取值本身（任务包§2.3／§4）。
3. **形式化实证**：本根人造input **刻意构造为占比 31/38 ≈ 81.58% < 90%**，`share_meets_reference_threshold = false`，而 `verify/assert_check.py` 全项通过、退出码 0——"合格与占比达标解耦"由此成为可复现之实测事实而非文字承诺（`A18_threshold_decoupling`）。
4. **判据面纯净性**：`assert_check.py` 之合格判定链**不消费参考锚**（`A18` 判据面自扫描核证 `9/10`／`0.9` 字面**零出现于判定路径**）。参考锚之实测比较结果**仅作输出面事实记录，不进入任何断言**。
5. **失效条件（本根状态量在何种情形下不成立/不可用）**：①坐标推移形态改换（§4③候选(b)/(c)）时，Carry 数值与符号序列可变，占比量随之改变——本根取值仅对候选(a)成立；②时间基/聚合视界改换（§4④）同理；③本根为**历史已实现序列之统计**，不构成对未来占比之任何预测或承诺（C-1 不命中之边界即在此）；④占比量为 diagnostic 地位，不承载定价真理宣称、不裁决任何交易之获利合法性（宪-EP-06 仪表推论）。

---

## §8 仪表读数身份标注（随包携带义务②＝§5.4常设纪律；对照表§3③）

本根**消费**模型派生量：`entity/engine.py` 之 `per_lot.theta`（瞬时 ∂V/∂t）与 `per_unit.value`（模型估值 V）。据 §5.4 常设纪律"命中即施加"：

- 该两量为**仪表读数**（instrument reading），**非定价真理源**；由其导出之 `EV_unit`／`tv_pos`／`carry`／`theta_reading_*` 同一仪表身份随行，不因经过差分、聚合或符号判定而升格为真理判定。
- 输出侧载体＝ `contrast_diagnostic.positive_theta_reading_time_share.instrument_reading_note`（`assert_check.py` `A12_instrument_reading_tag` 核证在场）。
- 引擎侧契约⑥（"定价模型之地位：本模块所路由之模型为计算用途之仪表计算器，不承载定价真理宣称，不用于裁决任何交易的获利合法性"）随 `entity/engine.py` 逐字节复用件之模块 docstring 原文携带。
- 本根输出之符号序列、占比量与两口径对照均为**观察与诊断量**（宪-EP-06 仪表推论）。

---

## §9 反面陈述段（**F-13 在场判据**，任务包§2.5；下边界"不做什么"显式化）

1. **不代行 GL-06 之比值维度**：GL-06 ＝ 短端时间价值收入 ÷ 长端日均消耗之**倍数比较判据**；本根 ＝ 净Carry为正之**时间份额状态量**。两者为已裁并立之互补相邻对象（裁决72-4定位语；GL-06 schema §7"本根不吸收其语义"之镜像面）。本根**不产出任何倍数/比值量**、**不吸收 GL-06 语义**、**不代建、不合并**。
2. **不产出交易信号或动作建议**：本根输出为状态量/诊断量（diagnostic 地位）。不产出买卖方向、不产出仓位调整建议、不产出 roll 触发、不产出告警动作。输出侧载体＝ `non_signal_declaration` 字段。
3. **不承诺任何占比水平之达成**：见 §7。本根不预测未来占比、不将 90% 作为目标或验收线。
4. **不代行动作/生命周期域**：供血族之**动作面**归第五批设计窗 **W-23**（任务包§5"W-23后置面"），显式后置。本根不定义占比恶化时之处置动作、不定义生命周期状态迁移。
5. **不代行同族之另两根**：**S6-11**（收入超开支1倍+，阈值1）为并立相邻对象，本根不吸收其语义、如实登记边界（GL-06 schema §7 同型处置）。
6. **不裁决、不修改**：T-24／T3-18／GL-06 之全部产物、翻译审计表、自由度治理册、骨架、模块划分（任务包§2.5）。本会话对上述件**只读**。
7. **不代行 M1 引擎本职**：本根不实现、不修改、不重判定价模型；引擎为逐字节复用之上游收口件（§3）。

---

## §10 钉表顺序留痕（F-10，最低形态＝文字声明三处一致）

**先钉表后跑数**：`entity/ledger_input.json`（含9期人造持仓时序、行情坐标、**六槽位**声明〔v1.1；原四槽位〕、参考锚与 `expected_pin` 期望值钉表节）为本次构造会话交付面之**首个写定文件**，先于 `entity/harness.py` 与 `verify/independent_recompute.py` 之任何执行动作写定；该文件 `_pin_note` 字段载同一声明。第三处声明见切片记录"检验通道记录·F-10钉表顺序留痕"节。

**如实标注（不作过度声明）**：人造input之设计参数（各期时长、持仓数量、行权价、坐标取值）之选定过程使用了**非交付之一次性试算脚本**（构造自由度设计用途），该脚本不进入交付面、不产生任何期望值钉表条目。`expected_pin` 全部条目与人造input同轮写定，先于交付件之比对断言执行。本声明为**文字声明形态**，非程序化时序证据（受控文本v1.1处置条款：成本收益不成立；撞到伪造实证再升格）。

**钉表粒度（乙-2）**：凡进入合格判定叙述链之期望值逐值钉表——占比量精确值、分子/分母、等权对照值、边界期恰零、口径背离期形态、负Carry期集、ITM期集、参考锚比较结果，共9项，全部载于 `expected_pin`；可独立复算者标复算来源（`_recompute_source`），本表无"不可证"项。

**v1.1 增补（乙-7）与其性质之如实标注**：`expected_pin.carry_sign_margin_by_period` 逐期钉 9 值，纳入 `A23` 核证射程（bit-exact），用以承载 `carry_sign_margin` 之防篡改（该量为**单路径量**，独立复算路径不产出该量，故不能以两路径比对承载）。**该子表不承载本节之「先钉表后跑数」时序声明**——其值系自修复会话之不变量验收基线逐值转录，属**事后钉表**，仅承载"钉定后不得漂移"之功能。性质就地标注于 `_carry_sign_margin_pin_provenance` 字段，不与上列 9 项同轮钉表条目混同。

---

## §11 外置数据件双钉声明面（F-5）与钉定排除件防线声明（手册v1.8 §3.1d）

**F-5 双钉（指纹断言 ＋ 声明面）**：

| 外置数据件 | 声明面（本节即声明面） | SHA256 |
|---|---|---|
| `verify/scan_patterns.json` | step0(ii) 扫描模式表（import七库＋关键字七项＋71-9反混淆三条）＋ F-7 全包域封闭规则（os.walk 发现面、排除面限 `__pycache__` 目录名精确匹配、双向比对）＋ 检测器自排除清单（**空集**，71-7）＋ 独立路径禁读清单三项 | `70918293f9f7ff9f0126b547d4004cbe1fd1836f8aaca992243623c7bc39fcd2` |
| `verify/nc_payload.txt` | 负向对照 NC-4 之数据源注入载荷（`import requests` ＋ URL 常量 ＋ 调用）。**外置于 .txt 以免污染 .py 扫描集**——若内嵌于交付脚本，将迫使扫描器自排除面扩至检测器自身之外，构成 71-7 所指开口 | `fc4b06f2d78b6a2765ed7f35d95154174b584928e1a4683424f9d512ddbc4d48` |
| `entity/engine.py` | M1 引擎逐字节复用件（§3；F-12 机械核证对象） | `e31fbcfeacebeb196f7e1d63f41089e7e0a7deb3cc9a9a8b44941af31e194e99` |

**双钉之免疫射程声明（手册§3.1d）**：双钉之设计目标＝**单面篡改检出**（改数不改声明／改声明不改数）；**协同篡改（多面一致改）不在免疫射程**，需第三独立面方可覆盖。本根不宣称协同免疫；是否加第三面按对象风险逐处裁，本根未加，如实声明。

**钉定排除件之防线位置声明（手册§3.1d，禁默示"排除即无防"或"断言全覆盖"）**：`verify/build_provenance.json` 为新鲜度钉定件自身，属**时序循环/自指类排除件**——其内容篡改**无 `assert_check.py` 脚本内通道**。其防线位于断言脚本之外，为两条：①**重生成幂等**（`build_provenance.py --verify` 重算并逐键比对，不一致即非零退出）；②**权威记录逐字转载对照**（该件 SHA256 入《切片记录_GL-09》之交付件指纹列，外审/增量复核以记录面对照）。

---

## §12 容差口径声明（W-4两子口径，裁决13/19；F-11 适用性）

本根计算面分两层，容差分派逐层独立：

- **连续解析层**（逐腿 `value_unit`／`ev_unit`／`tv_pos`／期间 `carry`／`theta_*`）：含超越函数闭式解（`erf`/`erfc`/`exp`/`log`/`sqrt`），C3 分派判据（超越函数在场性）判定属**连续解析计算**，分派**子口径(b)＝相对 diff ≤ 1e-12**（裁决13设立子口径、裁决19修订锚定值）。**本根实测上界＝6.475663e-13**（命中位＝P8 `legs_at_t_end.P8_S_PUT.value_unit`），在限内，距子口径(b) 上限 1e-12 之余量约 1.54 倍。**字段面最大值分列**（该层射程全九字段，逐字段最大相对 diff）：`value_unit` 6.475663e-13（P8 `legs_at_t_end.P8_S_PUT`）／`ev_unit` 6.475663e-13（同位）／`tv_pos` 6.475663e-13（同位）／`carry` **3.950941e-13**（P4，差值型输出之 cancellation 放大形态，同 T-24 REG-T24-01 已裁机理）／`tv_pos_end` 2.038552e-13（P3）／`tv_pos_start` 3.935432e-14（P8）／`theta_reading_start` 7.180336e-16（P4）／`theta_per_lot` 4.933461e-16（P8 `legs_at_t_end.P8_S_PUT`）／`theta_reading_end` 3.994932e-16（P7）。**层上界 ≠ `carry` 字段面最大值**——旧版本节以 `carry` 面最大值 3.95e-13 充作层上界，属射程误标（D-1）；本值经 §14 F-4 机读块键 `continuous_analytic_layer_max_rel_diff` 与 `A13` 之实测重算逐字节绑定，杜绝声明面单向漂移（X8 同源逃逸之补口）。
- **离散不变量层**（逐期 `carry_positive` 布尔向量、`duration_days`、占比之分子/分母/既约分数字符串、`share_meets_reference_threshold`）：整数与精确有理数（`fractions.Fraction`）运算，无超越函数，分派**子口径(a)＝0（bit-exact）**。本根实测两独立路径 **0 差异**。
- **符号判定稳健性（本根自设诊断，非新造判据）**：离散层之 bit-exact 可复现性以"符号不落在浮点噪声底"为前提。故输出逐期 `carry_sign_margin ＝ |carry| / max(|tv₀|,|tv₁|,|carry|)`，非边界期实测最小值＝**2.08e-3**（P4），高于子口径(b)上限 1e-12 约 **9个数量级**；边界期 P5 之 margin 恰为 0.0（设计如此，Carry 精确为 0.0，非噪声）。`assert_check.py` `A9_sign_margin` 核证。

**F-11 适用性（显式注记，非默认省略）**：F-11 射程＝被测量本身为**声明离散近似**（如声明步长下之差分导数）者。本根之 `carry` 为**期间时间价值之精确差**（模型量在两声明时点之差），非对任何瞬时量之离散近似——`theta_reading_*` 为引擎侧解析导数，本根未对其作任何差分近似。故 **F-11 不命中**，容差沿用裁决13/19 原框架分层分派如上。

**F-6 适用性**：源文非 T3 锚定词表 607-A/607-B 覆盖范围（本根源文＝八份思想层源文之一，非T0三件套），**F-6 不适用**，`assert_check.py` 显式断言留痕。

---

## §13 本根裁定登记与呈裁项索引

全部裁定语句汇总与呈KD逐项裁定形态见《切片记录_GL-09 v1.0》"本根裁定登记"节（本schema不重复承载，指针唯一）。其中标 **A档**（逐项呈，55-3a）者四项：①Carry 口径界定（§1）；②坐标推移形态类三处置与 TPL3-GL09-01 登记建议（§4③④⑥）；③引擎消费形态＝调用（§3）；④两口径量非同一性核证与宪-ST-06 口径同源纪律之界分（§1末段）。

---

## §14 F-4 机读声明块（断言脚本严格解析，禁兜底）

<!-- F4_DECLARATIONS
carry_measurement_caliber: model_valuation_time_value_difference
carry_coordinate_regime: frozen_market_coordinates_time_advance_only
period_segmentation_rule: position_structure_change_point_aligned
time_base_unit: calendar_day
positivity_boundary: strict_greater_than_zero
aggregation_horizon: full_sample_cumulative
reference_threshold_pct: 90
reference_threshold_comparator: greater_equal
reference_threshold_exact: 9/10
reference_threshold_status: source_reference_anchor_not_acceptance_criterion
reference_anchor_caliber: unstated_in_source
threshold_comparison_caliber_verified: false
st06_scope_marker: time_value_cashflow_extrinsic_premium_not_instantaneous_dVdt
risk_free_rate: 0.04
dividend_yield: 0.0
period_count: 9
total_days: 38
positive_carry_numerator_days: 31
positive_carry_share_exact: 31/38
engine_source_sha256: e31fbcfeacebeb196f7e1d63f41089e7e0a7deb3cc9a9a8b44941af31e194e99
scan_patterns_sha256: 70918293f9f7ff9f0126b547d4004cbe1fd1836f8aaca992243623c7bc39fcd2
nc_payload_sha256: fc4b06f2d78b6a2765ed7f35d95154174b584928e1a4683424f9d512ddbc4d48
continuous_analytic_layer_max_rel_diff: 6.475663e-13
source_anchor_file: QQQAI杠铃结构交流_20260718-20250101_.md
source_anchor_line_start: 511
source_anchor_line_end: 515
-->

本块与 §1/§2/§11/§12 散文声明同义；`verify/assert_check.py` `A13_f4_strict_declaration` 对本块逐键严格解析并与 `entity/ledger_input.json` 实际槽位值、实际文件指纹、harness 实际输出、**连续解析层实测上界之当场重算值**精确比对（零 OR 兜底、零宽松匹配）；`continuous_analytic_layer_max_rel_diff` 一键另与 §12 散文之同一字面串双向绑定（散文改而机读块不改、或反之，均即刻断言失败）；并断言 §1 宪-ST-06 口径界定段之三锚短语（"净时间价值现金流"／"extrinsic premium"／"非瞬时"）在场——删除或改写该段即断言失败。源文锚两键由 `source_anchor_check` 程序化核证（28-B(i)）。

# entity/input_schema.md · GK-31可算部分（策略腿映射五对象·腿级Greeks观察量归集）· v1.1 · 20260728

> **v1.1修复说明**（GK-31修复会话，授权源＝GK31外审报告与KD裁定落地_v1_0_20260728.md 裁决37）：
> §3尾部追加GK·852口径限定注记（37-C4裁定原文逐字转抄）；§4三分判别表补GK·816/GK·827两行
> 范围裁定处置行（37-B4）与GK·852同步补行（37-C4）。除以上并正，其余全文与v1.0一致，
> 不触发数值重跑（裁决37-A第2条：本次为文档层并正，不改任何A-D数值）。

## §1 坐标继承与字段声明（含A9档二检验发现）

node级raw Greeks账本坐标键继承T-76节点坐标系（六维：leg_type × side × option_type × tenor_bucket × moneyness_bucket × scenario；裁决14：T-76实体算法要件＝bucket派生＋坐标归属＋node级聚合，node级raw Greeks为上游输入之聚合事实）。GK-31不重算per-lot→node聚合（该聚合为T-76本职，同GK-14先例——本根直接消费node级raw Greeks账本作为人造input）。

**A9档二检验结论（骨架首批v1.0区一A9档二："T-76坐标系＝全项目坐标标准"检验义务，本切片为天然触点）**：

**采用＋扩展（半继承半自建），非全盘采用、非全盘自建**：

1. **直接采用不变部分**：side{long,short}、scenario{base}、tenor_bucket桶函数分段边界（0-30D/31-60D/61-90D/91-180D/180D+）、moneyness_bucket桶函数分段边界（low/atm/high，0.95/1.05分界）——结构与数值均零改动。
2. **扩展点一（leg_type值域）**：T-76 `leg_type: enum{core,hedge}`（二值）无法覆盖GK-31五腿结构，本根扩展为5值枚举`{core_position, near_financing_leg, far_convexity_leg, mid_gamma_leg, tail_protection_enhancement}`。值域扩展，坐标轴地位不变（仍是节点身份键之一）。
3. **扩展点二（新增instrument_type维度）**：T-76 `option_type: enum{call,put}`为强制枚举，无NA/线性工具槽位。GK-31核心仓位腿（GK§11.2"spot/futures/forward Delta口径"）持仓非期权，T-76坐标系原生无法承载。本根**新增第七维**`instrument_type: enum{linear,option}`；`instrument_type=linear`节点的`option_type`/`moneyness_bucket`退化取值`"NA"`，`tenor_bucket`对spot取"NA"、对futures/forward按既有桶函数正常取值（无需新函数）。
4. **发现的性质**：T-76坐标系"结构范式"（多维笛卡尔积节点身份键+桶函数思路）可直接复用，但其**取值域**（尤其leg_type、option_type两轴）系T-76自身对象范围内的工程裁定（"该取用为本根工程裁定，不构成骨架归纳阶段的跨对象命名标准"——T-76 input_schema §1原文），本非承诺覆盖全项目对象类型。GK-31的扩展需求**印证**该原文自身声明的"不外推"边界——即"T-76坐标系＝全项目坐标标准"命题现应判**外推不成立（部分）**：结构范式可外推，具体取值域不可无扩展地外推。本发现回传骨架第二轮归纳消费（裁决22(a)复用检验回传通道），本切片不代骨架裁定，仅如实记录处置与检验结果。

## §2 字段schema

| 字段 | 类型 | 说明 |
|---|---|---|
| node_id | string | 节点唯一标识，本根工程裁定 |
| leg_type | string, enum（见coordinate_declaration） | 坐标轴，本根扩展5值（§1点2） |
| instrument_type | string, enum{linear,option} | 坐标轴，本根新增维度（§1点3） |
| side | string, enum{long,short} | 坐标轴，继承T-76；side_sign: long=+1, short=-1 |
| option_type | string, enum{call,put,NA} | 坐标轴，继承T-76并扩展NA值 |
| tenor_bucket | string | 坐标轴，继承T-76桶函数；linear/spot取NA |
| moneyness_bucket | string | 坐标轴，继承T-76桶函数；linear取NA |
| scenario | string, enum{base} | 坐标轴，继承T-76，本根固定base |
| raw_delta/raw_gamma/raw_vega/raw_theta/raw_rho | 有理数（本根取整数） | node级raw Greeks账本五分量，满足裁决13子口径(a)全程bit-exact |

## §3 GK-31实体算法要件：腿级Greeks观察量归集

**Q4判据**（任务5 Step2 §3）："喂持仓，出腿级Greeks量集，判据＝与node级复算一致＋腿归属唯一"。

**腿归属唯一（结构性保证）**：每条node记录仅含一个`leg_type`字段取值，不存在双腿标注结构；聚合遍历按`leg_type`单键分组，无节点可被计入两腿。此为schema层面结构性保证，非运行时判断。

**核心算法**（对g∈{delta,gamma,vega,theta,rho}，leg∈5腿域）：

```
leg_greek[g][leg] = Σ_{n: leg_type(n)=leg} raw_g(n)
```

**leg-specific观察量（三分判别后确定的可算范围，见§4）**：
- `near_financing_leg`：附加联合旗标 `positive_theta_with_short_gamma = (theta_agg>0) AND (gamma_agg<0)`、`short_vega_flag = (vega_agg<0)`——直接反映GK§11.3"positive Theta是否伴随short Gamma/jump risk""short Vega/skew exposure"之可算部分（联合布尔判定，非新增固定参数——判定条件为聚合值自身符号，非外部阈值）。
- `far_convexity_leg`：附加`vega_by_tenor`（按tenor_bucket分列vega_agg子和，复用既有坐标维度）、`wing_delta_by_moneyness`（按moneyness_bucket分列delta_agg子和，复用既有坐标维度）——反映GK§11.4"long Vega的tenor/surface/skew exposure"之tenor可算子集、"wing Delta激活/钝化"之raw值部分（钝化/激活**标签**本身不计算，见§4）。
- `tail_protection_enhancement`：附加`by_option_type`（put=左尾、call=右尾两侧全量Greeks子和，复用既有坐标维度）——反映GK§11.6左尾"down Delta/down Gamma/put wing Vega"、右尾"up Delta/up Gamma/call wing Vega"及"theta cost/convexity rent"（右尾theta子和）。

  **口径限定（GK·852）**：`by_option_type`分列＝左右尾观察的**单维可算投影**，非左右尾功能定义本身。左右尾功能定义＝组合在状态空间下响应函数共同体现（GK·852功能定义句），其完整刻画需多Greek联合响应与情景机制，超出本根Level-0范围，范围裁定不登记；下游消费本分列时不得将put/call单轴视同左右尾完整定义。〔37-C4裁定原文逐字转抄，不改写〕
- `core_position`：gamma/vega/theta三分量本根声明恒为0（线性工具无二阶/时间价值维度——工具类型决定的范围裁定，非能力缺失，不登记）；delta/rho子和体现"spot/futures/forward Delta口径一致性"（三种子工具共用同一`delta=quantity×side_sign`公式，口径本身即为一致性观察点）与"Rho/financing/basis对持有成本影响"（futures/forward贡献非零rho，spot贡献0，如实反映"直接持有资产无融资敏感度、展期/远期工具有"）。
- `mid_gamma_leg`：仅输出全量五分量聚合作为基线；GK§11.5具名六项诊断量（gamma center/up-down asymmetry/Delta bleed/rebalancing cost diagnostic/vol-stressed Delta/post-hedge payoff shape）均不在本根计算范围，逐项三分判别见§4，TPL1-GK31-01回溯锚点标注见切片记录。

## §4 三分判别受控文本v1.1程序性纪律套用（逐机制成分）

判别顺序：类一测试（是否已有权威计算规则/结构支撑）→类二测试（候选池检索有无待建供给方）→类三（阶段B校准）。双重引用纪律：受控文本+实质依据并列。

| 成分 | 出处 | 类一测试 | 处置 |
|---|---|---|---|
| 五腿leg_greek聚合公式（Σ raw_g） | 本根算法要件 | 通过——加总结构无歧义，Q4判据字面即"腿级Greeks量集" | 类一已定，直接计算 |
| positive_theta_with_short_gamma联合旗标 | GK§11.3行812（判据一子问题） | 通过——判定条件即聚合值符号本身，非外部阈值参数 | 类一已定，直接计算 |
| vega_by_tenor/wing_delta_by_moneyness/by_option_type子分列 | GK§11.4行828、GK§11.6行855-857 | 通过——复用§1既有坐标维度（tenor_bucket/moneyness_bucket/option_type），非新造schema，同GK-14"复用T-76既有坐标维度非新造"先例处置模式 | 类一已定，直接计算 |
| **gamma center**（GK§11.5行840，中期Gamma leg） | GK§11.5 | **不通过（结构性）**——全项目检索确认该量已在**T3-03**处以同名对象登记为**TPL1-T303-02**四标签之一（`gamma_center`＝gamma幅值加权moneyness均值，占位声明公式，权威计算定义缺失，见撞墙清单_T3-03_v1_3现行状态open） | **交叉消费，不新登**——GK-31（中期Gamma leg）判定为TPL1-T303-02"gamma_center"子标签**第二消费方**（原单消费方＝T3-03）。本根不计算该量数值，随行携带TPL1-T303-02指针；此为本根施工阶段主动核出的消费关系，裁决36-E原文两随行指针未列此项，呈KD补记 |
| **wing Delta激活/钝化**（GK§11.4行826，远端凸性腿） | GK§11.4 | **不通过（结构性）**——同名"wing dullness"概念已登记TPL1-T303-02，现行状态open（裁决24-A6'续挂，20260721） | **引用不重登**，裁决36-E已列为随行指针①，本根照单携带。仅输出raw wing Delta值（§3 wing_delta_by_moneyness），钝化/激活标签本身不判定 |
| **Delta bleed**（GK§11.5行842，中期Gamma leg） | GK§11.5 | **不通过**——TPL3-T24-01（类三，Phase B校准项）已登记 | **引用不重登**，裁决36-E已列为随行指针②，本根照单携带，不计算数值 |
| **up/down Gamma asymmetry**（GK§11.5行841） | GK§11.5 | 不通过——需上/下行情景冲击态Gamma对比，本根scenario固定base（同T-76/GK-14范围限定），无冲击机制 | **范围裁定，不登记**——scenario机制未建为本根A层范围限定（非缺定义），同T-76/GK-14对scenario-shocked形态的处置模式；如需计算需另建scenario-shock供给（候选：比照TPL1-T76-01模式登记，本根不代登记） |
| **rebalancing cost diagnostic**（GK§11.5行843） | GK行616"边界：支持rebalancing cost diagnostic；不支持固定对冲频率"；GK行914"不固定交易成本模型" | 不通过——源文明文禁止固定成本模型/对冲频率，任何本根发明的数值公式即违反该边界声明 | **边界禁止直接计算，不登记**——非缺定义型缺口（缺口需"待建"，此处是"禁固定"），本根不产出数值，不构成TPL登记对象（登记模板一"缺口"隐含"应存在待建供给方"，而本项是方法论主动禁止固定，性质不同） |
| **vol-stressed Delta**（GK§11.5行844） | GK§11.5；GK行620"DdeltaDvol...波动率冲击后重新测量" | 不通过——需Vanna（∂Delta/∂vol）或冲击重估机制，本根五分量Greek集不含Vanna，无重估供给 | **范围裁定，不登记**——本根Level-0 Greek集（delta/gamma/vega/theta/rho）不含二阶交叉项，超出本根计算能力范围（非缺定义，是工具集范围边界）；背景参考GK-09"Delta形态族"（任务3产出行212，未入40节点判定域，非本项目当前活跃对象） |
| **post-hedge payoff shape**（GK§11.5行845） | GK§11.5 | 不通过——payoff曲线构造非Greeks聚合量，对象类型不同 | **范围裁定，不登记**——categorically非"Greeks观察量"（同GK-14对correlation matrix"范围裁定非能力缺失，不登记"处置模式） |
| skew exposure/event matrix/locked downside Delta/asymptotic upside Delta（GK§11.6左右尾各项） | GK§11.6行855-856 | 不通过——需波动率曲面/情景冲击数据，本根仅flat implied_vol、无surface/skew建模 | **范围裁定，不登记**——数据构造自由度限定内，同型GK-14对scenario_set"未冻结不外推"处置 |
| 双向三项（surface deformation/liquidity/execution lag/post-action legality，GK§11.6行857） | GK§11.6 | 不适用——裁决36-D已定性为**非Greeks可算量**，不入GK-31可算归集面 | **既有裁定排除，不登记**——沿裁决36-D，非本根三分判别对象 |
| **左右尾功能定义本身（GK·852功能定义句）vs `by_option_type`单维投影** | GK§11.6行852 | 不通过——左右尾功能定义＝组合在状态空间下响应函数共同体现，需多Greek联合响应与情景机制 | **口径限定，范围裁定不登记**——`by_option_type`分列仅为单维可算投影，非功能定义本身；下游消费不得将put/call单轴视同左右尾完整定义（口径文本见§3尾部腿段注记）；37-C4修复版补行，§3/§4同步 |
| **中期Gamma leg腿实体地位**（是否为T-36母结构既有要件升级 vs 第五要件新增） | GK行835/340/425 | 不通过——**KD已单独裁定为"未定"并登记TPL1-GK31-01**（裁决36-B，20260727） | **引用不重登，随行标注**——本根以该腿为归集对象照常开工（36-B消费方处置原文），切片记录随行标注TPL1-GK31-01作回溯锚点，不自行改读 |
| 核心仓位"Delta与标的Beta暴露的关系""对冲后是否改变核心仓位的功能承担"（GK§11.2行800-801） | GK§11.2 | 不适用——文本为治理判断/关系陈述，非数值量定义，与"Greeks观察量"范畴不同 | **范围裁定，不登记**——非缺口，是量与非量的类别区分（同核心仓位rho/delta计算之外的部分） |
| 近端融资腿"near-expiry binary risk""event state matrix"（GK§11.3行813-815） | GK§11.3 | 不通过——前者需DTE固定阈值（违GK§11.6行860"不设定DTE...固定参数"跨条通用边界声明）；后者"命名工程对象未固化形状"（裁决36-C已认定） | **范围裁定/既有裁定排除，不登记**——event state matrix沿裁决36-C（消费方触发时再登，本根未触发）；near-expiry阈值化违反固定参数禁令，本根不发明阈值 |
| **近端融资腿"financing / cash account / premium ledger分账"（GK·816）** | GK§11.3行816 | 不适用——分账为账务处理机制，非Greeks观察量本身（类别区分，非阶次不足） | **类别区分，范围裁定不登记**——premium ledger分账职责属账务/账本层（TC-04/T-23分账语义邻域），非本根"腿级Greeks观察量归集"对象范围；37-B4修复版补行 |
| **远端凸性腿"long Gamma的price band与expiry"（GK·827）** | GK§11.4行827 | 不通过——需价格带（price band）机制，本根未建 | **范围裁定不登记**——price band为独立机制对象，本根Level-0五分量聚合不含该机制，非缺定义型缺口（是"机制未建"非"待建供给方缺失"）；37-B4修复版补行 |

## §5 撞墙登记指针（引用不重登，详见撞墙清单）

- **TPL1-T76-01**：node级raw Greeks的per-lot/真实定价来源（品种感知自算Greeks引擎），上游桩，裁决14口径，引用不重登。
- **TPL1-T303-02**：wing dullness子标签（远端凸性腿钝化/激活）＝裁决36-E随行指针①，引用不重登；**gamma_center子标签**（中期Gamma leg）＝本根施工阶段自查发现的**第二消费方关系**，引用不重登，呈KD知悉（裁决36-E原文未列此项）。
- **TPL3-T24-01**：Delta bleed口径（中期Gamma leg）＝裁决36-E随行指针②，引用不重登，Phase B校准。
- **TPL1-GK31-01**：中期Gamma leg腿实体归属未定（裁决36-B，20260727），本根随行标注作回溯锚点，不自行改读，照常开工（消费方处置原文）。

## §6 容差口径声明

裁决13子口径(a)：离散/精确有理计算＝0（bit-exact）。理由：全部node级raw Greeks账本为人造整数，leg级聚合仅为加法运算（`fractions.Fraction`有理数`+`），无sqrt/exp/log等超越函数，无浮点舍入风险。

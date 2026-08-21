# B-2 Volatility Positioning × Greeks Governance × Coupling Taxonomy Bridge

> **document_id**：`B-2_Volatility_Positioning_Greeks_Governance_Coupling_Taxonomy_Bridge`  
> **canonical_name**：`B-2_Volatility_Positioning_Greeks_Governance_Coupling_Taxonomy_Bridge_v1_3_20260616`  
> **alias**：`B-2_PGC_Bridge`  
> **version**：`v1.3`  
> **status**：`frozen`（Part A + Part B + Part C 已全部内容化；阶段2内容化完成）  
> **date**：`20260616`  
> **lineage**：`v1.0-skeleton`（SHA256 `82d44f60...`）→ `v1.1`（Part A 内容化，SHA256 `4c083da4...`）→ `v1.2`（Part B 内容化，SHA256 `975890ad46017d1830cce1b4444ea5daf74b5869b3e86b26eb2ce42dcbe33002`）→ `v1.3`（+ Part C 内容化）  
> **task_id**：`TP-SPINE2-B21`（Part A 内容化）+ `TP-SPINE2-B22`（Part B 内容化）+ `TP-SPINE2-B23`（Part C 内容化）  
> **reference_shelf**：Greeks / Trading Concepts 采用 `交叉一致性修正版_20260616` 作本批核验基准；原 v0.1.2-freeze 保留为 lineage 锚。  
> **R6_status**：`settled`（待阶段2批3完成旧 spine delta 重锚后转 `closed`）  
> **scope_lock**：本版冻结 Part A / Part B / Part C 的方法论级承接；不定义字段、schema、typed container、状态机、算法、代码、生产参数、硬数值、治理阈值或自动执行规则。

# Part A｜Volatility Convexity Positioning

> 承担：目标风险形状、positioning thesis、收益/成本/失效路径，以及 TC residual-risk 语义。

## A.1 Positioning Thesis / Exposure-Shape Domain

> 承担：定义本策略希望维护的 volatility / convexity 风险形状、各功能承担者的责任，以及该目标在何种路径、成本与失效条件下仍可成立。本节是目标形状与责任声明的 canonical 家，不负责报告当前组合实际提供了多少 Greeks 或 convexity supply。

### Thesis 与责任声明

Positioning thesis 必须把波动率观点写成结构性暴露命题，而非市场方向句或单一 long-vol / short-vol 标签。它需要说明目标 payoff 形状希望在哪些价格路径、波动率路径、曲面形变与期限迁移中获得有利响应，哪些负凸性与成本属于有意承担，哪些左尾保护、右尾参与和 optionality 责任不得因局部账本改善而消失。该命题只能形成诊断基准与治理输入，不能直接授权动作。承接自 `T3 §1.3`、`T3 §§2.1–2.4`、`D17`；以 Greeks 主文档 §§2–3 作核验基准，后者不作为本节语义权威。

### Exposure shape 与 convexity responsibility

Exposure shape 表达目标风险响应在方向、路径、期限、翼侧、曲面与成本之间应保持的关系。A.1 只向 Part B 声明所需的 convexity responsibility，例如左尾和右尾分别需要何种情景承担、期限错位和翼侧错位为何会破坏目标形状；当前组合的实际 Vega 供给、分解与审计归 Part B。由此，A.1 是需求与责任的提出方，不是实际供给的计算方或批准方。承接自 `T3 §§2.2–3.5`、`D18`。

### 收益、成本与失效解释

`realized path convexity` 与 `convexity rent` 在本 Bridge 中归 A.1。前者描述目标结构希望从路径展开中获得的凸性响应，后者描述为保留该响应而支付、收取和分账的经济代价；二者共同构成 positioning thesis 的收益—成本基础，而非某一 TC 残差的附属项。A.2.6 负责检验分布、skew 与 path-vol 假设是否使 realized path convexity 失真，A.2.8 负责在最差路径中压力验证，但不另行定义这两个对象。归属依据为 `T3 §§4.1、4.3`、`T3 §§5.1–5.3`、`D17` 与 `D20` 的单一 canonical 家原则。

**承接概念**：
- **Volatility positioning thesis**：声明策略希望维护的风险形状、受益路径、成本路径、失败路径与结构责任；只能作为 Phase 3 诊断和 Part C 耦合的上游基准。承接自 `T3 §§2.1–2.4`。
- **Exposure shape**：描述左尾、右尾、局部凸性、期限结构、skew、spot-vol 与 vol-of-vol 等暴露之间的目标关系，不将其压缩为单一净 Greek。承接自 `T3 §§2.3、3.1–3.5`。
- **Convexity responsibility declaration**：向 Part B 声明何处需要 convexity、由何种功能承担以及何种错位不可接受；不接收或定义实际 `convexity_supply_vega`。承接自 `D18`。
- **Realized path convexity**：目标组合在路径展开中应出现的有利非线性响应，必须与 coverage、funding、执行可行性和对象身份共同守约。承接自 `T3 §4.1`。
- **Convexity rent**：为获得和维持目标凸性支付的 premium bleed、roll 与维护成本，以及用于支持该成本的 premium / funding 账本关系；不得与 Greeks Theta 或无风险 carry 混同。承接自 `T3 §4.3`、`T3 §§5.1–5.3`。
- **Positioning failure modes**：至少包括 thesis-drift、proxy-failure 与 coupling-break。前者指目标命题被路径或成本条件证伪，第二类指压缩观察替代了真实暴露，第三类指目标形状虽仍被陈述但已与母结构、账本或治理状态脱节。承接自 `T3 §§6.1–6.5`。

**域边界**：
- 与 Part B 的边界：A.1 定义所需风险形状与责任，Part B 描述当前组合实际持有的五维 Greeks 状态及 `convexity_supply_vega`；需求声明不得被误写为供给事实。
- 与 A.2.7 的边界：dynamic hedge residual 的 canonical 家是 A.2.7；A.1 只把其可能侵蚀目标形状列为失败来源。
- 与 Part C 的边界：A.1 不比较目标与实际状态，不封装 candidate package，也不作治理裁决。
- 不承接：字段化 exposure envelope、具体腿位选择、阈值、期限、行权价、比例、参数或执行触发器。

**不变式**：
- Positioning thesis 不得退化为方向预测、单一 volatility label 或单一 Greek 目标。
- `realized path convexity` 与 `convexity rent` 的定义只在 A.1 出现；其他节只进行条件检验或压力引用。
- `convexity_supply_vega` 始终归 Part B；A.1 的责任声明不能替代实际供给、coverage 或治理裁决。
- 任何局部 cashflow、Theta 或净 Greek 改善，都不能自动证明 exposure shape 仍然守约。

## A.2 Trading Concepts Residual-Risk / Path-Execution Domain

> 承接：TC 独立 canonical 承接域（D20）。下设八章一级骨架（A.2.1–A.2.8）。

### A.2.1 Substitutability / Proxy / Stacking Residual

> 承担：判断理论等价、代理关系与临时堆叠在真实工具、期限、融资、流动性和结算条件下是否仍成立，并识别由此迁移出的 residual risk。

可替代性是复制、对冲、套利与交割关系成立的前提，不是工具名称相似或局部 Greek 接近即可成立。弱可替代关系必须保留工具身份、期限与交割差异；proxy 和 stacking 只能把主要风险临时转移或压低，无法消除 basis、correlation、liquidity、funding、settlement 与 hedge-quality decay。承接自 `TC 主文档 §3`（核验基准）、`T3 §0.3`、`T3 §19.4`、`D20-item1`。

**承接概念**：
- **Substitutability boundary**：检验两个 underlying、衍生工具或交割对象在经济功能、期限、结算和融资条件上是否具有足够等价性；不足时，理论复制关系只能作为有限条件下的近似。
- **Proxy residual**：代理工具降低主风险后仍保留的 basis、相关性、期限、流动性、结算和对象身份差异；proxy 只提供观察或候选输入。
- **Stacking residual**：多腿或多工具叠加后形成的临时风险转移、对冲质量衰减及局部集中，包含无法由净 Greeks 完整表达的执行和市场机制残差。
- **Netting limitation**：任何净额只对已声明口径有效，不能由局部抵消推出完整 risk-flat、tail-flat 或 identity-flat。

**域边界**：
- 与 Part B 的边界：本节解释 proxy 与 stacking 为什么产生 TC residual；各 Greek 的 raw、proxy、risk-equivalent 或 scenario-stressed 表达由 Part B 定义。
- 与 A.2.7 的边界：本节处理替代关系本身的残差；复制实施、动态对冲与交易执行形成的 residual 归 A.2.7。
- 不承接：代理工具选择规则、stacking 算法、相关性阈值、自动对冲或自动净额化。

**不变式**：
- 可替代性必须在工具身份、期限、融资、流动性与结算条件下成立，不能仅由相同 underlying 标签或相近 Greek 推出。
- Proxy、stacking 与 netting 都是 residual-risk transformation，不是 risk elimination。
- Greeks 表面平衡不能关闭未解决的 substitutability residual。

### A.2.2 Carry / Convergence / Roll-down / Theta / Premium Decomposition

> 承担：把持有期收益与成本拆分为 carry、convergence、roll-down、Theta 敏感度和 premium cashflow 等不同来源，防止同名或同方向变化被误认成同一经济对象。

TC 视角关注各类收益来源在账本和路径上的差异。Convergence 描述合约关系在临近到期或结算时向其终局价值关系靠拢；roll-down 描述持仓随期限缩短沿期限结构和 volatility surface 发生的重估，不保证方向有利；Theta 是时间流逝下的局部定价敏感度，只是持有期成本分解的一部分。Premium income 则是实际取得并进入账本的现金流，不能由 positive Theta 替代。承接自 `TC 主文档 §3.4`（核验基准）、`T2 00A §4`、`T3 §§4.3、5.1–5.3`、`T3 §19.4`、`D20-item2`。

**承接概念**：
- **Carry**：持有期现金流、融资关系或风险补偿的总称，必须说明来源与承担的风险，不能预设稳定或安全。
- **Convergence**：合约价值或相对关系向到期、交割或终局关系靠拢的过程，其兑现依赖市场、融资、结算与可替代性条件。
- **Roll-down**：持仓随时间迁移到新的期限坐标后产生的曲线或曲面重估，可能有利、无效或不利。
- **TC Theta component**：在收益—成本分解中记录时间流逝造成的定价衰减或持有成本；其概念需与 Part B 的 Theta 风险语言对照，但不重定义该 Greek。
- **Premium decomposition**：把已收或已付 premium、未实现时间价值变化、long-end bleed、roll 与执行成本分开解释，避免 cashflow、估值变化和 risk sensitivity 混账。

**域边界**：
- 与 Part B.4 的边界：A.2.2 处理经济来源和账本语义；B.4 处理 Theta 作为时间敏感度的事实、诊断与压力表达。
- 与 A.1 的边界：A.1 定义 convexity rent 的目标成本—收益责任；本节拆解其持有期来源，不能改变 thesis。
- 不承接：收益预测、固定 carry 假设、convergence 或 roll-down 触发器、premium funding 的批准判断。

**不变式**：
- Premium income 不等于 Greeks Theta，positive Theta 也不等于 realized income 或 funding safety。
- Carry、convergence、roll-down、Theta 与 premium cashflow 必须分账解释，不能因方向一致而合并为单一收益来源。
- Roll-down 是期限迁移后的重估，不是无风险的 surface decline。

### A.2.3 Expiry / Exercise / Assignment / Settlement / Boundary Branches

> 承担：描述到期、行权、分配、结算和市场边界如何把同一到期 payoff 分裂为不同的实际路径与对象身份分支。

到期附近的风险来自流程和信息时序，而非仅来自 Greeks 变大或变小。Exercise、assignment、现金或实物 settlement、收盘后信息、pin 与制度边界会决定组合在下一时点持有什么对象、承担何种资金和库存义务。理论平价或局部 Greek-flat 只有在相应流程分支被核验后才具有操作意义。承接自 `TC 主文档 §§4.2–4.4、10.2–10.3`（核验基准）、`T3 §0.3`、`T3 §19.4`、`D20-item3`。

**承接概念**：
- **Expiry branch**：到期时间、信息到达与交易可用性共同形成的路径分支；同一终点价格可能对应不同可执行结果。
- **Exercise / assignment branch**：行权选择和被分配结果改变现金、底层持仓、义务仓及后续风险身份。
- **Settlement branch**：现金与实物交割、结算时点和计价关系可能使理论等价在实务中失效。
- **Boundary branch**：制度边界、市场停牌、价格限制、交易时段或合约规则造成的非连续路径，不等同于合约 payoff barrier。
- **Secondary exposure regeneration**：初始 hedge 或临近到期的局部平衡会因流程、参数、曲线和持仓身份变化重新生成风险。

**域边界**：
- 与 A.2.4 的边界：本节定义流程分支及其残差来源；A.2.4 判断各类 flatness 声明是否在这些分支下仍成立。
- 与 Part C 的边界：本节只提交 settlement 与 identity residual，不决定是否批准持有、展期、行权或平仓。
- 不承接：具体到期处置时间、自动 exercise / assignment 规则、结算套利或 boundary 交易策略。

**不变式**：
- Settlement-flat 不能由 Greek-flat 推出，settlement-flat 也不能推出 object-identity-flat。
- 到期 payoff 相同不代表到期流程、现金流、持仓身份和次日风险相同。
- 理论平价必须通过实际 settlement identity 与可执行条件核验后才能用于诊断。

### A.2.4 Flatness and Non-Greek Governance Checks

> 承担：建立 Greek-flat 之外的 TC flatness 检查，识别局部敏感度看似平衡但 scenario-P&L、settlement、funding、margin 或 object identity 仍不平的状态。

Flatness 必须相对于明确维度、局部范围和产品结构表述。Part B 可以说明 Delta、Gamma、Vega、Theta 或 Rho 在特定口径下是否局部平衡，但 TC 需要继续检查同一组合在完整情景损益、到期结算、资金占用、保证金变化和持仓身份上是否仍有残差。此处的检查结果是独立证据源，不能被单一 Greek 正常状态覆盖。承接自 `TC 主文档 §§4.3–4.4、10.3–10.5`（核验基准）、`T3 §19.4`、`D19`、`D20-item4`。

**承接概念**：
- **Scenario-P&L flat**：在声明的路径与市场状态集合中，组合损益是否保持预期的相对稳定；不等于某个局部 Greek 为零。
- **Settlement-flat**：不同 exercise、assignment 和 settlement 分支是否产生等价的现金、持仓与义务结果。
- **Object-identity flat**：候选或自然到期过程是否保持同一策略对象及母结构功能，而非悄然转化为另一种仓位。
- **Funding-flat / margin-flat check**：局部价格风险降低后，资金需求、保证金和库存义务是否仍可能发生非线性变化；这些是独立检查维度，不是新的 Greek。
- **Full-risk-flat prohibition**：在未完成多维检查前，不得使用“风险已平”或“结构中性”等总括性结论。

**域边界**：
- 与 Part B 的边界：Part B 负责五维各自的 audit 能力；本节负责列明 Greek audit 不能覆盖的 non-Greek flatness 问题。
- 与 A.2.8 的边界：本节定义 flatness 的检查维度；A.2.8 在 worst-path 与 scenario stress 中攻击这些声明。
- 不承接：flatness 阈值、自动中性化、保证金模型或 Phase 4 approval。

**不变式**：
- 任一 Greek-flat 都只是声明口径内的局部结论，不得升级为 full-risk-flat。
- Settlement、scenario-P&L、funding、margin 与 object identity 必须分别核验，不能互相替代。
- Part B 的某一维 audit 通过，不能自动关闭 TC residual。

### A.2.5 Segmentation / Shape / Local Risk Concentration

> 承担：从 positioning 与 TC 视角检查风险集中在何种期限、行权区域、状态与 payoff 形状中，以及这种集中是否仍服务于目标暴露责任。

Segmentation 把总组合拆回局部风险来源，shape 则显示名义持仓、payoff 和曲率集中在何处。该视角关注的不只是局部敏感度数值，还包括集中位置是否与左尾保护、右尾参与、短端供血、期限错配和动态维护责任一致。Part B 的分段 Greeks 和 Vega surface 观察是证据输入，本节不重定义其计算。承接自 `TC 主文档 §5、§10.2`（核验基准）、`T3 §19.4`、`D20-item5`。

**承接概念**：
- **Tenor segmentation**：区分前端义务、后端保护和不同期限功能，识别名义抵消下的时间错位。
- **Strike / moneyness shape**：观察风险与 payoff 集中在何种价格区域，以及关键翼侧是否已远离有效激活区。
- **Local concentration**：识别风险、流动性依赖、库存或执行需求是否过度集中于少数局部区域。
- **Dynamic shape drift**：时间、价格与曲面变化使原有 shape 迁移或钝化，导致名义持仓仍在但功能承担已改变。
- **Positioning alignment check**：判断 segmentation 和 shape 是否兑现 A.1 的责任声明，而非仅展示图形或摘要。

**域边界**：
- 与 Part B.3 的边界：Vega 的 tenor、surface、grid 与 scenario-stressed 观察归 Part B；本节判断这些局部分布是否支持 positioning responsibility。
- 与 A.2.8 的边界：本节识别风险集中位置；A.2.8 将其置入最差路径和对象身份压力。
- 不承接：bucket 宽度、grid、归一化公式、shape trigger、自动 roll 或 hedge 规则。

**不变式**：
- 总 Greek 或单一图形摘要不得替代 tenor、翼侧与局部 concentration 的检查。
- Segmentation 是诊断工具，不是风险等价证明或治理终点。
- 相关工具只有在声明且可审计的经济转换口径下才能共同观察，仍不得无条件净额抵消。

### A.2.6 Distribution / Tail / Skew / Path-Vol Dependency

> 承担：检验终点分布、尾部、skew、vol-of-vol 与事件顺序假设如何改变目标风险形状和 realized path convexity 的兑现条件。

终点 histogram 或静态 payoff 无法表达完整 path risk。期权结构的收益与损失取决于价格路径、IV 路径、skew 形变、事件顺序、融资反馈和对冲时序；同一终点可能对应完全不同的 intermediate exposure 与 P&L。A.1 定义 `realized path convexity`，本节只检验支撑该命题的分布与 path-vol 假设是否成立、是否遗漏尾部或反馈路径。承接自 `TC 主文档 §6、§10.2`（核验基准）、`T3 §§3.3–3.4、4.1–4.2、6.1–6.3`、`T3 §19.4`、`D20-item6`。

**承接概念**：
- **Distribution assumption failure**：经验分布、模型分布或 regime 叙事不能覆盖真实尾部、波动率状态和路径顺序时，相关 positioning 结论必须降级或进入复核。
- **Tail risk**：低频、跳跃、流动性与融资反馈共同形成的非局部损失路径，不能仅由终点概率或单一 Greek 表达。
- **Skew dependency**：put wing、call wing 与 ATM 的相对重定价会改变左右尾承担能力；skew 只能作为路径和曲面条件，不能成为单一信号。
- **Path-vol dependency**：价格与波动率的联动、脱钩或顺序变化会改变 long wing、short-end obligation 与动态维护的实际效果。
- **Vol-of-vol / surface deformation**：曲面自身的非线性变化会使 Vega 含义、roll 成本与翼侧有效性发生迁移。
- **Realized path convexity validation**：检查 A.1 声明的路径凸性是否在不同路径顺序、升降波组合与尾部情景下仍存在。

**域边界**：
- 与 A.1 的边界：`realized path convexity` 与 `convexity rent` 的定义归 A.1；本节只处理其分布与路径条件。
- 与 Part B 的边界：scenario-stressed Greeks 和 surface Vega 的具体表达归 Part B；本节解释为何这些情景必须覆盖 distribution、skew 与 path-vol residual。
- 不承接：分布模型选择、固定 tail 参数、skew 阈值、regime classifier 或自动 volatility bet。

**不变式**：
- Terminal payoff、终点分布或历史 histogram 均不能替代 full path risk。
- 下跌升波、上涨降波等关系只能作为声明并可审计的 scenario assumption，不能被当作永恒映射。
- 分布或 skew 叙事即使看似合理，也不能单独证明 A.1 的 realized path convexity 已被当前组合兑现。

### A.2.7 Replication / Spread / Dynamic-Hedge Residual / Execution Cost

> 承担：作为 dynamic hedge residual 的 canonical 家，统一承接复制可实现性、价差残余、离散再平衡、交易频率、流动性与执行成本共同形成的路径 P&L 残差。

复制关系只有在工具可交易、融资与结算条件成立、执行成本可接受时才具有实践意义。Static replication、spread 与 dynamic hedge 都会改变风险承担位置，而不会消灭风险；相同终点与相近总波动率也可能因路径顺序、再平衡时点、成交价格、工具身份和流动性而产生不同结果。本节依据 `OQ-04` 承担广义 dynamic hedge residual 的唯一 canonical 定义。承接自 `TC 主文档 §§7.2–7.7、10.1、10.5`（核验基准）、`T3 §§4.4、5.4、6.4、19.4`、`D20-item7`、`OQ-04`。

**承接概念**：
- **Replication residual**：理论复制、静态复制或平价关系在融资、离散交易、结算、工具可得性与市场冲击下留下的差异。
- **Spread residual**：相对价值或表面中性结构仍保留的 Gamma、Vega、Theta、Rho、basis、path 与 liquidity 风险。
- **Dynamic hedge residual**：离散再平衡、路径顺序、交易频率、执行滞后、对冲工具身份和成本共同造成的 realized P&L 偏差；其范围大于任何单一 Greek 观察。
- **Execution cost**：bid-ask、滑点、市场冲击、成交失败、延迟、工具不可得、broker 与结算约束，是 residual 的组成部分而非事后附注。
- **Hedge-identity transformation**：soft / hard hedge 或不同工具替代会改变尾部、basis、资金与对象身份，不能只以 Delta 改善评价。

**域边界**：
- 与 Part B 的边界：Gamma、Delta 或其他 Greeks 可提供 residual 的局部观察角度，但不得在各 Greek 节重复定义 dynamic hedge residual。
- 与 Part C 的边界：本节识别和解释 residual；Part C 只消费其耦合后果、候选影响与 post-action audit 接口。
- 与 A.2.1 的边界：A.2.1 判断替代关系是否成立；本节处理复制、对冲和执行过程中实际产生的路径残差。
- 不承接：hedge frequency、spread ratio、复制组合、自动对冲、自动展期、止损或执行算法。

**不变式**：
- Dynamic hedge residual 只在 A.2.7 定义；其他章节只能引用其结论或观察角度。
- Dynamic hedging、replication 和 spread 都是风险形状改写，不是风险消灭。
- 权利金或静态 payoff 不能作为动态对冲者完整风险上限。
- 执行成本必须在候选进入治理前被视为路径风险组成部分。

### A.2.8 Worst-Path / Scenario-P&L / Object-Identity Stress

> 承担：用最差路径、情景损益和对象身份压力攻击 A.1 的目标形状及 A.2 各类残差声明，并形成供 Part C 使用的独立诊断输入。

Worst-path 不是预测最可能情景，也不是由单一 stop-loss 数值定义。它要求构造最容易破坏结构责任的路径顺序、波动率变化、流动性条件、结算分支和执行失败，观察损益形状、账本、双翼功能、期限错配与持仓身份是否共同失约。Scenario-P&L 只在声明情景范围内有效；object-identity stress 进一步检查修复、到期、分配或对冲后是否仍是同一母结构。承接自 `TC 主文档 §§6.4、7.6、9.4、10.3–10.5`（核验基准）、`T3 Part A §§5–6`、`T3 §19.4`、`D20-item8`。

**承接概念**：
- **Worst-path construction**：主动组合价格顺序、波动率与 skew 形变、流动性恶化、执行延迟和结算分支，寻找能够击穿结构承诺的路径。
- **Scenario-P&L stress**：检查声明场景下的完整损益形状及其来源，不能由局部 Greek-flat 或静态终点 payoff 替代。
- **Object-identity stress**：判断到期、assignment、repair、hedge、roll 或 partial monetization 后，母结构功能与目标持仓身份是否仍被承担。
- **Residual interaction stress**：检验 proxy、segmentation、distribution、settlement 与 dynamic hedge residual 是否在同一路径中相互放大。
- **No-action / review legitimacy**：当压力证据不完整、残差无法审计或身份可能漂移时，向 Part C 提交 no-action、manual review 或 block 的证据条件，而不在本节作最终裁决。

**域边界**：
- 与 A.1 的边界：本节压力检验 exposure shape、realized path convexity 与 convexity rent，不重新定义目标命题。
- 与 Part C 的边界：本节产出压力场景、scenario-P&L residual 和 identity-drift evidence；治理决定、candidate 封装与约束栈归 Part C。
- 与 A.2.4 的边界：A.2.4 定义 flatness 检查；本节通过 adversarial path 验证这些 flatness 声明能否存活。
- 不承接：情景概率、固定 shock、自动 stop、自动 rollback、approval 或执行动作。

**不变式**：
- Worst-path analysis 的目标是证伪结构承诺，不是预测市场或寻找单一最大损失数字。
- Scenario-P&L 通过不能推出 settlement-flat、funding-flat 或 object-identity-flat。
- 压力测试发现问题只能形成独立诊断和治理输入，不能从本节直接跳到交易动作。
- 任一残差无法解释或 lineage 不可追溯时，其他局部指标正常不能关闭该缺口。

# Part B｜Portfolio Greeks Governance

> 承担：五维 Greeks（Delta / Gamma / Vega / Theta / Rho）的事实表达、结构化观察、诊断、压力解释、governance input 边界与 post-action audit 能力。五维共享 D19 的共同治理包络，但分别使用与其风险性质匹配的观察语法；任何一维均不得因显示完整而取得动作批准权。
>
> 当前发布标识：`v1.2` / `frozen-partial-AB`；lineage 为 `v1.1`（SHA256 `4c083da42f001d670e3c38a9d8e1fa5db1ccd74d1cddb9f09c1433c402c2d526`）→ `v1.2`。为满足本任务的冻结前缀逐字符防漂移要求，文件头中的 v1.1 元数据原样保留；本标识与 Manifest 构成本子批的发布状态记录。

## B.1 Delta

> 承担：承接组合方向暴露的 Greek 风险语言，保留不同 underlying、proxy 与 basis 口径下的一阶敏感度事实，形成方向集中、basis 失效与 underlying drift 的诊断输入，并为压力治理和执行后方向审计提供独立维度。

Delta 的指针式数学定义为 `Δ = ∂V/∂S`，承接自 Greeks 主文档；该定义只标识局部一阶价格敏感度，不赋予概率解释、完整方向风险解释或动作权限。B.1 的 Phase 2 事实对象，是组合在 spot、forward、futures 与 settlement basis 下呈现的方向暴露，以及这些暴露对所选 underlying 和 proxy 的依赖。相同或接近的 Delta 只有在 underlying 身份、计价与结算口径、期限和 basis 条件均被声明时才可比较；未经声明的净 Delta 只能作为粗观察。

Delta 的结构化观察重点在于：方向暴露由哪个 underlying 承担，使用了何种 proxy，spot、forward、futures 与 settlement basis 之间保留了何种残差，以及方向暴露是否集中在少数期限、腿位或局部价格区域。该观察与 A.2.1 的 substitutability / proxy 视角相互对照：A.2.1 判断替代关系为何可能失效并定义 TC residual，B.1 只表达这种替代和 basis 差异如何体现在 Delta 风险语言中，两者均作为 Part C 的独立上游证据。

Phase 3 的 Delta 诊断对象包括方向暴露集中、proxy basis 失效与 underlying drift。方向暴露集中说明局部一阶风险可能被少数工具、期限或结算口径支配；proxy basis 失效说明原有 Delta 等价关系已不能忠实代表目标 underlying；underlying drift 说明动作、自然演化或对象转换后，组合的方向暴露已迁移到与原责任不同的标的或结算基础。上述诊断只形成 diagnostic gap 输入，不直接生成 hedge、roll 或 rebalance 决定。

Scenario-stressed Delta 用于观察价格移动、波动率变化、basis 扩张、结算分支、流动性变化或 proxy 失效情景下的一阶暴露如何重排。其进入 Phase 4 时仍只是治理输入，必须与 Gamma、Vega、A.2.3 的 settlement branch、A.2.4 的 non-Greek flatness 检查以及 coverage / funding / identity 约束联合解释。执行后，B.1 独立审计方向暴露是否仍由预期 underlying 与 proxy 承担、basis 残差是否扩大、局部 Delta 改善是否把方向风险迁移到其他期限或对象身份中；审计发现异常只能形成 audit 记录或 repair review 请求，不能直接触发下一笔动作。

承接自 `T3 / Part B §§7–9、§12`、`T1 / C1`、`T2 / 12-C1`、阶段1 `D19`；Greeks 主文档 §4 仅作为核验基准。

**承接概念**：
- **Raw Delta observation**：按真实持仓、underlying 与计价基础保留的一阶方向暴露事实；属于 Phase 2，不解释结构合法性。
- **Underlying / proxy basis view**：对照现货、远期、期货与结算口径，识别方向暴露是否依赖有限可替代关系或脆弱 basis。
- **Directional concentration diagnostic**：识别方向风险是否过度集中于特定工具、期限、腿位或局部区域。
- **Proxy-basis failure diagnostic**：识别 proxy 与目标 underlying 的方向等价关系是否因 basis、流动性、结算或对象身份变化而失效。
- **Underlying drift diagnostic**：识别执行或自然演化后，方向风险承担者是否偏离原目标对象。
- **Scenario-stressed Delta**：在声明的价格、波动率、basis、结算与流动性情景下重估方向暴露，作为 Phase 3 / 4 输入。
- **Post-action Delta audit**：独立核验动作后的方向暴露、承担对象与 basis 残差是否仍符合候选所声明的风险改形目的。

**域边界**：
- A.2.1 负责 substitutability、proxy 与 stacking residual 的 TC canonical 语义；B.1 不重定义这些 residual，只表达 Delta 维的 proxy / basis 后果。
- A.2.3 负责 settlement branch 与对象身份分支；B.1 的 settlement basis 观察不能替代结算与持仓身份检查。
- Part C 才比较 A.1 的目标方向形状与 B.1 的实际状态，并与其他 Greeks、账本及身份约束形成 diagnostic gap。
- 不承接 Delta 阈值、固定 hedge ratio、hedge frequency、proxy 选择规则、概率推断或自动动作。

**不变式**：
- Delta-flat 只表示声明口径与局部状态下的一阶敏感度平衡，不等于 risk-flat、settlement-flat 或 object-identity-flat。
- 不同 underlying、proxy、tenor 或 basis 的 Delta 未经等价规则与适用条件声明，不得无条件净额后用于治理。
- Delta diagnostic 与 scenario-stressed Delta 均是 governance input 的上游证据，不是 governance decision。
- Post-action Delta audit 不得直接生成 hedge、roll、rebalance 或其他下一步动作。

## B.2 Gamma

> 承担：承接组合局部曲率与 convexity location 的 Greek 风险语言，保留前端与长端、不同期限段和翼侧的 Gamma 分布，形成 Gamma 集中、凸性位置与动态对冲离散残差的观察输入，并为压力治理和执行后曲率审计提供独立维度。

Gamma 的指针式数学定义为 `Γ = ∂²V/∂S²`，承接自 Greeks 主文档；该定义只标识 Delta 随标的价格变化的局部曲率，不表示完整凸性、尾部保护或动态复制结果。B.2 的 Phase 2 事实对象包括当前局部曲率、front-month Gamma 与 long-end Gamma，并需保留其所在期限段、翼侧、价格区域与腿位角色。当前 spot 附近的总 Gamma 即使为正，也不能说明左尾、右尾或其他价格区域拥有正确的 convexity location。

Gamma 的结构化观察重点是期限段与 wing side 上的分布：前端 short Gamma 是否集中，长端 put / call wing 的 Gamma 是否仍位于可激活区域，不同期限的 Gamma 是否因时间尺度和局部性而具有不同风险含义，以及上行与下行路径中局部曲率是否发生不对称变化。该视角用于把“组合有 Gamma”拆解为“Gamma 位于何处、由谁承担、在何种路径中有效”。

Phase 3 的 Gamma 诊断对象包括 Gamma 集中、convexity location 与 dynamic hedge discretization residual 的 Gamma 观察角度。Gamma 集中识别局部负凸性是否过度堆积于前端或特定翼侧；convexity location 识别长端与中期凸性是否远离目标激活区、发生 Gamma center drift 或 wing dullness；离散对冲观察只说明局部曲率如何放大再平衡间隔、价格跳跃和成交滞后的影响。广义 dynamic hedge residual 的 canonical 家始终是 A.2.7，B.2 不重定义其路径、执行与成本语义。

Scenario-stressed Gamma 用于观察价格区间移动、上行/下行不对称、波动率与 skew 共变、事件状态、流动性恶化及执行滞后下的局部曲率迁移。其进入 Phase 4 时只能作为治理输入，不能由单一 spot Gamma、单一正负标签或某个局部曲率摘要批准动作。执行后，B.2 独立审计前端 short Gamma 是否被意外放大、长端与中期 Gamma 是否仍位于目标价格区域、候选动作是否仅改善当前点却削弱左右翼 convexity，以及 Gamma 变化是否与 A.2.7 登记的动态对冲残差相一致。

承接自 `T3 / Part B §§7–10、§12`、`T1 / C1`、`T2 / 12-C1`、阶段1 `D19`；Greeks 主文档 §5 与 §§8–9 仅作为核验基准。

**承接概念**：
- **Raw Gamma observation**：当前组合在具体腿位、期限、翼侧和价格区域中的局部曲率事实；属于 Phase 2。
- **Front-month / long-end Gamma view**：区分短端义务的局部负凸性与长端翼侧承担的凸性，不将其压缩为单一总量。
- **Tenor / wing Gamma distribution**：观察 Gamma 在期限段、put wing 与 call wing 中的位置和集中程度。
- **Gamma concentration diagnostic**：识别局部曲率是否过度集中于前端、单一腿位或不利价格区域。
- **Convexity-location diagnostic**：识别 Gamma center、左右翼激活位置与目标 convexity responsibility 是否错位。
- **Dynamic-hedge residual observation**：从 Gamma 维观察离散再平衡、跳跃和执行滞后如何放大路径残差，但不定义该 residual。
- **Scenario-stressed Gamma**：在声明的价格、波动率、skew、事件和执行情景下重估局部曲率，作为治理输入。
- **Post-action Gamma audit**：独立核验动作后的 Gamma 位置、集中与左右翼功能是否仍符合原候选的风险改形声明。

**域边界**：
- A.2.7 是 dynamic hedge residual 的唯一 canonical 家；B.2 仅提供 Gamma 观察角度，不复制离散对冲、路径 P&L 或执行成本定义。
- A.2.5 负责从 TC / positioning 视角判断 segmentation 与 shape 是否兑现功能责任；B.2 负责提供 Gamma 维事实与诊断。
- B.3 处理 volatility surface 维的 Vega 供给；Gamma 与 Vega 可联合解释，但任何一维均不得替代另一维。
- Part C 才将 Gamma 状态与 A.1 目标形状、coverage、funding、wing integrity 和 roll optionality 耦合。
- 不承接价格区间宽度、shock 规模、Gamma 阈值、对冲频率、自动 roll 或自动 hedge。

**不变式**：
- 当前 spot 的净 Gamma 不得替代期限段、翼侧、价格区域、事件状态与 price-vol 共变压力。
- Gamma 为正不自动证明左尾保护、右尾参与或对象身份守约。
- Dynamic hedge residual 只在 A.2.7 定义；B.2 只能引用其 Gamma 观察后果。
- Post-action Gamma audit 是独立审计维度，不是下一笔对冲或展期的触发器。

## B.3 Vega

> 承担：承接组合对 implied volatility、期限分段与 volatility surface 形变的实际风险状态，以 Vega 六态表达供给位置和曲面依赖，形成 Vega 形态缺口、convexity 供给残差与 surface 漂移的诊断输入，并为压力治理和执行后波动率风险审计提供独立维度。

Vega 的指针式数学定义为 `ν = ∂V/∂σ`，承接自 Greeks 主文档；该定义只标识期权价值对所声明波动率输入的局部敏感度，不说明 shock 口径、期限等价、翼侧功能或完整 volatility risk。B.3 的 Phase 2 事实对象，是组合在不同 tenor、wing 与 surface 位置上的 Vega 暴露。任何总量或平行波动率摘要都必须保留其适用范围，不能覆盖前后期限、put / call wing 与局部曲面形变之间的差异。

Vega 的结构化观察重点显式承接六态：raw、tenor、forward-segmented、surface、grid 与 scenario-stressed。六态描述风险以何种形态被表达，Phase 描述该表达拥有何种权限，两轴正交；某一形态可进入 Phase 3 或 Phase 4，不代表它自然成为诊断、候选、治理决定或第七种 Vega 形态。B.3 通过六态保留期限、远期区段、翼侧、曲面切面和局部形变的可追溯关系，防止 scalar netting 删除供给位置。

Phase 3 的 Vega 诊断对象包括 Vega 形态缺口、convexity 供给残差与 surface 漂移。Vega 形态缺口识别当前观察是否缺少必要的期限、翼侧、曲面或情景表达；convexity 供给残差识别实际 Vega 承担是否位于 A.1 所声明的目标功能区域；surface 漂移识别 level、skew、twist、curvature 或局部形变变化后，原有供给解释是否失效。B.3 描述 Vega 本身的六态事实与诊断，B.3.* 才将这些输入转译为 `convexity_supply_vega` 的 shape-preserving derived governance view。

Scenario-stressed Vega 是压力治理的直接表达：它用于检验价格与波动率联动、期限结构变化、put / call wing 相对重定价、曲面局部变形、流动性退化或情景假设失效时，Vega 供给是否仍位于正确位置。即使进入 Phase 4，它仍只是 governance input。执行后，B.3 独立审计 Vega 的期限、翼侧与曲面位置是否按候选声明迁移，原有形态缺口是否关闭，新的 surface concentration 或 wrong-tenor 暴露是否产生，以及动作是否仅改善平行波动率摘要却削弱左右尾承担。

承接自 `T3 / Part B §§7–10、§12`、`T1 / C1 §4`、`T2 / 12-C1 §3.1`、阶段1 `D18–D19`；Greeks 主文档 §§6、8–9 仅作为核验基准。

**承接概念**：
- **Raw Vega observation**：按真实持仓与风险位置保留的波动率敏感度事实，属于 Phase 2。
- **Vega six-form view**：以 raw、tenor、forward-segmented、surface、grid 与 scenario-stressed 六态表达风险形态，并与 Phase 权限轴正交。
- **Vega shape-gap diagnostic**：识别期限、远期区段、翼侧、曲面或情景表达是否缺失，导致总量无法解释实际风险。
- **Convexity-supply residual diagnostic**：识别当前 Vega 承担与 A.1 的 left-tail / right-tail convexity responsibility 是否存在位置、期限或情景错位。
- **Surface-drift diagnostic**：识别 volatility level、skew、twist、curvature 或局部变形使原有 Vega 解释失效的状态。
- **Scenario-stressed Vega**：在声明的价格、波动率、skew、term structure、曲面与流动性情景下重估 Vega，作为 Phase 3 / 4 输入。
- **Post-action Vega audit**：独立核验动作后 Vega 的期限、翼侧、曲面与情景承担是否仍可追溯并服务目标 convexity responsibility。

**域边界**：
- A.1 提出 convexity responsibility 与目标风险形状；B.3 表达组合实际持有的 Vega 状态，不把需求声明写成供给事实。
- B.3.* 定义由 B.3 六态派生的 `convexity_supply_vega`；B.3 不提前把六态压缩为治理结论。
- A.2.5 与 A.2.6 分别解释 shape / concentration 和 distribution / path-vol residual；B.3 只提供 Vega 维事实、诊断与压力表达。
- Part C 才将 Vega 状态、`convexity_supply_vega`、coverage、funding 与 identity 并联审查。
- 不承接 Vega 权重、期限等价公式、grid 规格、shock set、自动 vol bet、自动 roll 或自动 hedge。

**不变式**：
- 六态是度量形态，Phase 是权限轴；二者不得合并计数或相互授权。
- Total Vega、net Vega 或单一平行波动率摘要不得推出 vol-neutral、coverage-safe 或 convexity responsibility 已被兑现。
- Scenario-stressed Vega 与其他 Vega 诊断进入 Phase 4 后仍不等于 governance decision。
- Post-action Vega audit 不得直接生成新的 candidate、roll、hedge 或 volatility bet。

### B.3.* convexity_supply_vega

> 承担：作为 D18 的唯一归属点，把 B.3 六态提供的 Vega 事实与结构输入转译为保留风险形状的 convexity-supply 治理视图，用于描述实际供给相对 A.1 责任声明的错位、集中与情景依赖；本节不定义新的 Vega 形态、不提供批准分数，也不替代 coverage by shares。

`convexity_supply_vega` 是从 B.3 Vega 六态形成的 shape-preserving derived governance view。它保留组合在 tenor、wing side、volatility surface 切面与 scenario 路径中的供给结构，使治理能够判断 left-tail 与 right-tail convexity 的实际 Vega 承担是否位于正确期限、正确翼侧和可存活的曲面形变路径中。它的派生身份只表示对既有 Vega 信息进行功能化解释；原始事实、结构观察与 lineage 仍回指 B.3，不在本节重写六态。

该视图明确放弃 cross-asset 无条件净额、跨 wing 净额与单点标量净额。不同资产、计价与结算口径之间的 Vega，不同 put / call wing 的功能责任，以及不同期限与曲面切面的风险，均不能因数值方向相反而被视为已互相覆盖。任何摘要只能帮助索引或阅读，不能替代保留 tenor、wing side、surface 切面与 scenario 路径的结构表达，也不能退化为旧 `V_net` 的改名。

A.1 是 convexity responsibility 的需求提出方，本节是实际 Vega 供给的结构化表达方。若 downside put-wing supply 在压力路径中不足或位于错误期限，表面充足依赖跨 wing、前后期限或不同曲面模式的不合法抵消，risk-equivalence 或 scenario assumption 失效、未知或不可审计，供给集中于不承担目标左尾覆盖的工具，或者 derived view 无法回溯到 B.3 的原始事实，则必须将结果提交显式 coverage review。coverage by shares 始终是 `T2 / 00A §5` 的 H 层独立身份约束；本视图无论显示充足或不足，均不得豁免、优化、替代或批准该约束。

`convexity_supply_vega` 可以作为 Phase 4 constraint stack 的输入，用于说明供给不足、期限错位、翼侧错位、曲面形变脆弱性或情景依赖缺口，但治理输入不等于治理决定。approval、block、manual review 与其他裁决仍必须由 Part C 所承接的完整治理关系处理，并与 coverage、funding、object identity、wing integrity、tenor mismatch 与执行可行性共同审查。执行后，本视图可用于核验动作是否真正把供给迁移到目标期限和翼侧、是否修复了曲面与情景缺口、是否产生新的集中或非法抵消；该审计仍不得自动形成下一笔动作。

R6 settlement：本节是 R6 / D15 的清偿落地点；R6 当前状态为 `settled`，待阶段2批3完成旧 spine delta 重锚后转为 `closed`。

承接自 `T1 / C1 §4`、`T2 / 12-C1 §3.1`、`T2 / 00A §5`、`T3 / Part B §§9–10`、总控 `D15`、阶段1 `D18、OQ-05`。

**承接概念**：
- **Shape-preserving derived governance view**：由 B.3 六态形成、保留 convexity supply 位置与路径结构的派生治理视图；不是第七种 Vega 形态。
- **Tenor-preserving supply**：保留供给所在期限与远期区段，避免前后期限的数值抵消掩盖功能错位。
- **Wing-side-preserving supply**：保留 put wing 与 call wing 及其 left-tail / right-tail 功能责任，禁止跨 wing 无条件互抵。
- **Surface-slice-preserving supply**：保留 volatility level、skew、twist、curvature 与局部形变所在的曲面切面，不以平行波动率摘要代替。
- **Scenario-path-preserving supply**：保留价格、波动率、期限结构、流动性与执行条件共同形成的情景路径，使供给结论绑定可审计假设。
- **Coverage-review escalation**：当供给不足、错位、非法抵消、假设失效或 lineage 不可追溯时，将证据送入 H 层 coverage review，而非由本视图自行裁决。
- **Post-action supply audit**：核验动作后供给是否位于目标期限、翼侧、曲面与情景路径，并检查新的集中、错位和抵消依赖。

**域边界**：
- B.3 定义并承载 Vega 六态事实与诊断；本节只引用并派生，不重复六态定义。
- A.1 定义 convexity responsibility；本节不修改目标需求，也不把供给状态反向写成 positioning thesis。
- Coverage by shares、funding、object identity 与 governance decision 均有独立 canonical 家，本节不得吸收或替代。
- Part C 负责把本视图与其他证据耦合并形成 diagnostic gap、candidate package 与治理接口。
- 不承接 shape-preserving 计算公式、聚合实现、字段、权重、阈值、情景生成算法或动作规则。

**不变式**：
- `convexity_supply_vega` 是 Vega-derived governance input，不是 raw ledger、scalar net、H 层常量或 governance decision；`governance input ≠ governance decision`。
- Tenor、wing side、surface 切面与 scenario 路径不得在本视图中被无条件压缩或互相抵消。
- Cross-asset 净额、跨 wing 净额与单点标量净额不能证明 convexity supply 充足。
- `convexity_supply_vega` 不能替代 coverage by shares；触发 coverage review 也不等于 approval、block 或 manual review 已被作出。
- Post-action supply audit 只能形成审计结论或 repair review 请求，不能直接生成下一笔交易。

## B.4 Theta

> 承担：承接组合对时间流逝的 Greek 风险语言，严格区分时间敏感度与 premium cashflow，保留期限、翼侧与长端 bleed 的结构分布，形成 Theta 集中、bleed 失控与 carry 分解不一致的诊断输入，并为压力治理和执行后时间成本审计提供独立维度。

Theta 的指针式数学定义为 `Θ = ∂V/∂t`，承接自 Greeks 主文档；该定义只标识在所声明定价与参数条件下，期权价值对时间流逝的局部敏感度。B.4 的 Phase 2 事实对象是组合各腿、各期限与翼侧的时间敏感度，包括 long-end bleed 的风险表现，但不包括已经实现或取得的 premium cashflow。Theta、premium income、financing cost、cash account 与 realized P&L 必须保持分账。

Theta 的结构化观察重点包括 tenor 分布、put / call wing 侧的时间衰减与 long-end bleed。该结构需区分短端义务可能呈现的 positive Theta exposure、长端 put / call 双翼承担的 negative Theta / premium bleed，以及不同期限和参数路径下 ordinary、modified 或 shadow 解释的差异。结构化观察的目的，是说明时间成本或时间暴露位于何处、由谁承担以及伴随何种 Gamma、Vega、gap 或 event 风险，而非把正 Theta 汇总为安全收益。

Phase 3 的 Theta 诊断对象包括 Theta 集中、bleed 失控以及与 A.2.2 carry / convergence / roll-down / premium decomposition 不一致。Theta 集中识别时间暴露是否过度聚集于短端义务或特定腿位；bleed 失控识别长端凸性成本是否在缺乏对应功能或账本支持的情况下持续侵蚀；分解不一致识别 Greek 时间敏感度与实际 premium、roll、financing 和 cashflow 解释是否发生混账。A.2.2 负责经济来源与账本分解，B.4 只提供 Greeks Theta 的事实、诊断与压力语言。

Scenario-stressed Theta 用于观察时间推进与价格、波动率、skew、期限结构、事件状态和流动性条件共同变化时，Theta 暴露与 long-end bleed 如何迁移。它可以揭示 positive Theta 背后的 short Gamma、gap 与 event risk，或 negative Theta 是否仍对应有效的 convexity responsibility；即使进入 Phase 4，也只能作为治理输入。执行后，B.4 独立审计时间敏感度是否按候选声明迁移、long-end bleed 是否仍对应有效左右翼功能、short-end positive Theta 是否伴随不可接受的负凸性，以及 Theta 解释是否与实际 premium / funding 账本重新混合。

承接自 `T3 / Part B §§7–10、§12`、`T1 / C1`、`T2 / 00A §4、00B §4、12-C1`、阶段1 `D19`；Greeks 主文档 §§7–9 仅作为核验基准。

**承接概念**：
- **Raw Theta observation**：在声明定价与参数条件下，各腿、期限和翼侧的时间敏感度事实；属于 Phase 2。
- **Tenor / wing Theta distribution**：区分短端义务、长端 put / call 双翼与不同期限中的时间暴露，不以总 Theta 代替。
- **Long-end bleed view**：观察长端凸性成本随时间的风险表现，并核验其是否仍对应有效的左右翼责任。
- **Theta concentration diagnostic**：识别时间暴露是否过度集中于特定期限、腿位或负凸性来源。
- **Bleed-control diagnostic**：识别 long-end bleed 是否失去功能对应、超出账本解释或与结构可持续性发生冲突。
- **Carry-decomposition consistency diagnostic**：检查 B.4 的 Theta 风险语言与 A.2.2 的 carry、convergence、roll-down、premium 和 financing 分账是否一致。
- **Scenario-stressed Theta**：在声明的时间、价格、波动率、skew、事件和流动性情景下重估时间敏感度，作为治理输入。
- **Post-action Theta audit**：独立核验动作后的时间暴露、bleed 与关联风险是否仍符合原候选和母结构责任。

**域边界**：
- A.2.2 负责 carry、convergence、roll-down、premium cashflow 与 TC Theta component 的经济分解；B.4 负责 Greeks Theta 风险语言，两者不得互替。
- B.4 可说明 long-end bleed 与时间敏感度状态，但 funding safety 与 cost-dilution ledger 的结论不在本节作出。
- B.2 与 B.3 分别提供 Gamma 与 Vega 的关联证据；Theta 不能吸收或替代这些维度。
- Part C 才将 Theta 状态与 premium ledger、funding relation、convexity responsibility 和对象身份耦合。
- 不承接固定 Theta 阈值、carry 预测、premium 目标、卖权规则、时间推进算法或自动动作。

**不变式**：
- Premium income ≠ Greeks Theta。
- Positive Theta ≠ safe carry、realized income 或 funding safety。
- Negative Theta 可能是为有效 convexity responsibility 支付的成本，不能仅因数值为负判定结构无效。
- Theta 与 premium cashflow、financing cost、cash account 和 realized P&L 必须分账。
- Post-action Theta audit 不得直接生成新的 short-premium、roll、repair 或其他交易动作。

## B.5 Rho

> 承担：承接组合对利率、融资率、折现、远期与 basis 变化的 Greek 风险语言，在既有 funding / cost-dilution ledger 之外提供独立的敏感度事实与诊断，形成 financing-flat 表象下的结构暴露、forward basis 失效与曲线集中输入，并为压力治理和执行后资金敏感度审计提供独立维度。

Rho 的指针式数学定义为 `ρ = ∂V/∂r`，承接自 Greeks 主文档；该定义只标识期权价值对所声明利率或融资输入的局部敏感度，不代表完整融资后果、资金安全或账户现金流。B.5 的 Phase 2 事实对象包括利率与融资率敏感度，并需区分其所在 tenor、financing curve、margin funding、forward / dividend / FX basis 与 settlement 语境。单一净 Rho 无法说明不同曲线段、计价基础与融资来源之间的结构差异。

Rho 的结构化观察重点是 tenor、financing curve 与 margin funding：不同期限的折现与远期敏感度是否集中，broker 或账户融资条件与市场曲线是否分离，margin funding 变化是否使表面局部平衡失去意义，以及 forward、dividend、currency 或 settlement basis 是否仍支持原定价关系。B.5 只补齐 Rho 标签下的风险语法，不新建融资对象；现金、premium、funding 与 cost-dilution 的账本承接继续归 T0 已有体系。

Phase 3 的 Rho 诊断对象包括：在 A.2.4 的 funding-flat / financing-flat 表象下仍存在的 Rho 结构暴露、forward basis 失效、curve concentration 与 rate-regime sensitivity。局部净 Rho 接近中性时，broker financing、margin funding spread、远期或股息 basis 和结算现金流仍可能沿不同路径恶化；B.5 用 Rho 语言显性表达这些敏感度来源，A.2.4 则继续判断 non-Greek funding / margin flatness 是否成立。

Scenario-stressed Rho 用于观察 yield curve、financing spread、margin regime、forward / dividend / FX basis、numeraire 与 settlement 条件变化时，利率和资金敏感度如何重排。其进入 Phase 4 后只能作为治理输入，必须与 funding ledger、cost-dilution ledger、margin、liquidity、coverage 与 object identity 联合解释。执行后，B.5 独立审计动作是否把 Rho 暴露迁移到新的期限或融资来源、局部净 Rho 改善是否伴随更差的 basis 或 margin funding 依赖，以及 Rho 风险语言与实际账本后果是否保持可追溯一致。

承接自 `T3 / Part B §§7–12`、`T1 / C1`、`T2 / 12-C1`、阶段1 `D19`；Greeks 主文档 §§7、9 仅作为核验基准。

**承接概念**：
- **Raw Rho observation**：对声明的利率、融资与折现输入保持可追溯的局部敏感度事实；属于 Phase 2。
- **Tenor / curve Rho view**：区分不同期限、曲线段与计价基础中的利率敏感度，不以总 Rho 代替。
- **Margin-funding view**：观察 broker、账户与保证金融资条件变化对组合敏感度解释的影响；不创建新的融资账本。
- **Residual financing-exposure diagnostic**：识别 funding-flat / financing-flat 表象下仍未被解释的 Rho 结构暴露。
- **Forward-basis failure diagnostic**：识别远期、股息、FX、计价或结算 basis 变化使原风险等价关系失效的状态。
- **Curve-concentration diagnostic**：识别利率或融资敏感度是否过度集中于特定期限、曲线段或资金来源。
- **Scenario-stressed Rho**：在声明的曲线、融资、margin regime、basis 与结算情景下重估 Rho，作为治理输入。
- **Post-action Rho audit**：独立核验动作后利率、融资、basis 与曲线敏感度是否按候选声明迁移，并与实际账本后果保持一致。

**域边界**：
- A.2.4 负责 funding-flat、margin-flat 与其他 non-Greek flatness 检查；B.5 只提供 Rho 维事实、诊断和审计输入，不重做 flatness 判定。
- Funding / cost-dilution ledger 已由 T0 承接；B.5 不新建 financing 概念、不复制现金流或融资治理。
- B.4 的 Theta 时间敏感度与 B.5 的 Rho / financing sensitivity 必须分账，二者不能相互吸收。
- Part C 才将 Rho 状态与 funding、margin、coverage、liquidity 和 object identity 耦合并作治理处理。
- 不承接曲线模型、固定 Rho 权重、融资阈值、margin 规则、basis 交易、自动 hedge 或自动资金动作。

**不变式**：
- Net Rho、局部 Rho-flat 或 financing-flat 表象均不能替代 funding ledger、margin 状态与 settlement cashflow 检查。
- Rho 诊断只提供风险语言与 governance input，不批准融资、对冲、roll 或其他动作。
- B.5 不创建新的 financing canonical 家；所有现金与融资后果继续由既有 ledger 和 Part C 耦合处理。
- Scenario-stressed Rho 必须绑定声明的曲线、融资、basis 与结算假设，不能作为无条件风险真值。
- Post-action Rho audit 不得直接生成新的 candidate、融资调整或交易指令。

# Part C｜Positioning × Greeks × Mother-Structure Coupling

> 承担：目标形状与实际状态比较、diagnostic gap、candidate package、constraint-stack input、post-action audit 接口；不重定义 Part A / Part B 对象。

## C.1 Coupling Diagnostic Gap（耦合诊断 gap）

> 承担：比较 Part A 提出的目标风险形状与 TC residual-risk 需求、Part B 报告的实际 Greeks / convexity supply 状态，以及母结构当前承担状态，形成耦合层 diagnostic gap；不重做任何上游域内诊断。

### 需求—状态—母结构的耦合比较

C.1 消费 Part A 与 Part B 已经形成的 canonical 结论。Part A 是需求与责任提出方：A.1 声明目标 exposure shape 与 convexity responsibility，A.2 各节登记 TC residual-risk。Part B 是实际状态表达方：B.1–B.5 提供五维 Greeks 的事实、诊断、压力与审计能力，B.3.* 提供 `convexity_supply_vega` 的 shape-preserving derived governance view。C.1 只比较两侧是否仍能共同支持同一母结构，不在耦合层重述、改名或修订两侧对象。

A.1 的 convexity responsibility 与 B.3.* 的 `convexity_supply_vega` 对照，形成 convexity supply gap。该 gap 只说明目标承担与实际供给在期限、翼侧、曲面或情景路径上是否存在耦合缺口；需求的 canonical 仍在 A.1，供给视图的 canonical 仍在 B.3.*。B 侧状态即使显示局部供给充足，也不能反向降低或改写 A.1 已声明的责任。

A.2 的 TC residual-risk 与 B 各维诊断对象对照，形成 TC–Greeks coupling gap。该比较用于识别 Greek 状态看似改善时，substitutability、settlement、flatness、segmentation、distribution、dynamic hedge residual 或 worst-path residual 是否仍未被承接；也用于识别 TC residual 已被登记但缺少对应 Greek 事实、压力或审计证据的状态。C.1 不重复执行 A.2 的 residual-risk 判断，也不替代 B 各维的独立诊断。

母结构耦合比较引用 T0 已冻结的四要件及 T3 Part C 的 mother-structure 状态承接，检查 A 的目标与残差结论、B 的实际风险状态是否仍共同服务短端供血与成本摊薄循环、长端 long put + long call 双翼、期限错配全维度管理、动态 roll 维护 optionality 与凸性。比较结果形成 mother-structure coupling gap，并提交 C.2；该结果不改变母结构定义，不对候选作治理裁决。

**承接概念**：
- **Convexity supply gap**：A.1 convexity responsibility 与 B.3.* `convexity_supply_vega` 之间的耦合缺口；只记录需求—供给错位，不重新定义需求或供给。
- **TC–Greeks coupling gap**：A.2 各节 residual-risk 与 B.1–B.5 对应事实、诊断、压力和审计证据之间的未承接、错位或证据冲突。
- **Mother-structure coupling gap**：A / B 当前结论与 T0 母结构四要件、T3 Part C mother-structure 状态之间的功能脱节或承接不足。
- **Coupling evidence conflict**：A、B 或母结构状态的合法证据在同一对象上给出不能直接合并的结论，需要在候选封装中保留冲突与 lineage，而非由 C.1 消解。
- **Candidate-source gap**：经 C.1 保留来源、对象指针与母结构影响的 gap，可作为 C.2 形成 candidate action package 的上游输入；gap 本身不具有动作权限。

**域边界**：
- C.1 只处理 A vs B、A vs 母结构、B vs 母结构的耦合比较；A.2 内部 residual-risk 诊断和 B 各维内部事实、诊断、压力表达保持各自 canonical。
- C.1 对 A/B 对象只使用指针式引用，包括 A.1 convexity responsibility、A.2.7 dynamic hedge residual、B.3.* `convexity_supply_vega` 等；不得复制定义或另造同义对象。
- C.1 的输出只进入 C.2 作为 candidate package 来源；不形成 approval、block、manual review decision、执行动作或自动化触发规则。
- C.1 不把母结构四要件改写为新的 coupling taxonomy，也不以局部 Greeks 或账本改善替代母结构状态。
- 依据指针：`T3 §1.3 / Part C §§13–14`、阶段1 `D17`；Greeks 与 Trading Concepts 交叉一致性修正版仅作核验基准。

**不变式**：
- Coupling gap 是 Phase 3 的耦合层观察与诊断来源，不是 Phase 4 governance decision。
- A 与 B 的角色不对称：A 提出需求与 residual-risk，B 表达实际状态；C.1 不得用 B 的当前状态反向改写 A 的目标责任。
- 任一单维 Greek 正常、局部 flatness 或账本改善，都不能自动关闭 TC–Greeks coupling gap 或 mother-structure coupling gap。
- 缺少可追溯 A/B 指针或母结构 lineage 的 gap，不得升级为 candidate-source gap。

## C.2 Candidate Action Package（耦合候选封装）

> 承担：将 C.1 已识别且可追溯的耦合 gap 封装为 Phase 3 candidate action package，保留目标功能、A/B canonical 指针、母结构影响与 lineage；不作治理裁决或执行授权。

### 从 gap 到 candidate 的描述性封装

Candidate action package 必须从 C.1 的具体 gap 出发，并保留该 gap 所引用的 A/B canonical 对象、相关 mother-structure 状态、T0 frozen lineage、使用的情景与尚未解决的证据冲突。封装的作用是说明候选试图维护或迁移什么结构功能、依赖哪些事实与诊断、可能把 residual risk 转移到何处，以及需要向 C.3 提交哪些耦合约束；它不建立字段表、typed container 或执行计划。

候选的动作语义沿用 `T2 11｜B3` 与 `T3 §11` 的 canonical 命名和权限边界。常见耦合 candidate 可描述为：repair，用于修复供给、双翼、承接或 residual-risk 缺口；roll，用于期限与功能承担的重配，且仍按“功能迁移”理解；reduce，用于收敛过量负凸性、错误集中或不再服务目标形状的暴露；migrate，用于把结构功能从失效承担者迁移到新的承担者；monetize，用于有限兑现已激活凸性并保留剩余结构责任。以上只是典型描述，不构成封闭枚举，也不新增动作 canonical 家。

Candidate package 对 A.2.7 dynamic hedge residual、B.3.* `convexity_supply_vega` 及其他 A/B 对象只作引用。候选可以声明需要修复或迁移这些对象所揭示的 gap，但不能在封装中重写 residual、Vega 供给、Gamma 位置、Theta bleed、Rho / financing sensitivity 等定义。

Proxy 观察不能因进入 candidate package 而被提升为 risk-equivalent exposure。任何 risk-equivalent Greeks 必须继续满足 Greeks 修正版所要求的等价规则、聚合范围、适用假设、情景集合与禁止用途；相关性、经济相似性或 proxy bucket 本身均不是充分依据。涉及 Trading Concepts 的 `forward-vol bucket` 与 B.3 的 `forward-segmented Vega` 时，只能保留为可建立映射的不同观察，输入、shock、时间段与聚合规则未经独立审计前不得默认同义、共用字段或相互替代。

**承接概念**：
- **Gap-grounded candidate**：来源于 C.1 已登记 gap，能够回指需求、实际状态、母结构影响与 lineage 的 Phase 3 候选。
- **Repair candidate**：引用既有 canonical 对象，提出修复供给、承接、双翼或 residual-risk 缺口的候选方向；不包含自动补仓或批准规则。
- **Roll candidate**：引用既有期限与 optionality 状态，提出功能与期限承担迁移的候选方向；不等于机械展期。
- **Reduce candidate**：提出收敛过量负凸性、错误集中或失效暴露的候选方向；不由单一 Greek 阈值自动生成。
- **Migrate candidate**：提出结构功能在承担者之间迁移的候选方向，并保留新旧承担者、残余风险与对象身份影响的引用链。
- **Monetize candidate**：提出有限兑现已激活凸性的候选方向，并把剩余 coverage、左右尾参与和母结构完整性留给 C.3 约束输入。
- **Lineage-preserving package**：保留 gap、A/B canonical 指针、T0 frozen 内核、假设与证据冲突的候选封装，使 Phase 4 可审查其来源而不依赖叙事补写。

**域边界**：
- C.2 只封装 Phase 3 candidate；`candidate ≠ approved`，不得写入 approval、block、manual review decision、order、rebalance、hedge、roll 或 unwind 的执行规则。
- Repair、roll、reduce、migrate、monetize 是典型动作语义，不是封闭 enum、状态机或固定工作流。
- Proxy bucket、net Greek、dashboard score 或未声明聚合不能作为 risk-equivalent exposure，也不能单独支撑 candidate。
- Candidate 必须引用 A/B canonical 与 C.1 gap，不得凭市场观点、单一 proxy 或无 lineage 的叙事凭空形成。
- 依据指针：`T3 §1.3、§11.1、§11.5`、`T2 11｜B3`；Greeks 修正版 §10 与 Trading Concepts 修正版 §10.5 仅作权限和接口核验基准。

**不变式**：
- Candidate 仅由 Phase 3 形成；Phase 4 governance 与 post-action audit 均不得直接生成 candidate。
- Candidate package 必须可追溯到 `gap + A/B canonical 指针 + mother-structure state + T0 lineage`，不允许无来源候选。
- `Proxy bucket ≠ risk-equivalent Greeks`；进入候选封装不会提高 proxy 的证据权限。
- Candidate 只声明可能的功能维护或迁移方向，不声明已批准、可执行或应当执行。

## C.3 Constraint Stack Input（向 Phase 4 提供约束输入）

> 承担：把 C.2 candidate action package 与其涉及的耦合约束组织为 constraint stack input，提交 Phase 4 治理；不在 Part C 内具体化 governance decision 或裁决规则。

### Candidate 与耦合约束的并列提交

C.3 接收 C.2 的 candidate package，并把候选涉及的约束以并列、可追溯的治理输入提交 Phase 4。输入至少保留候选对母结构四要件、A.1 目标责任、A.2 TC residual-risk、B 各维实际状态、B.3.* `convexity_supply_vega`、coverage、funding、账本、执行可行性与 object identity 的影响。该组织方式只说明 Phase 4 需要看到哪些耦合证据，不规定其 approval、block、manual review 或其他裁决结果。

Coverage by shares 始终引用 `T2 00A §5` 的 H 层独立身份约束。其中覆盖关系不得被 candidate、Greek 改善、`convexity_supply_vega`、premium income、risk-equivalent exposure 或任何聚合摘要覆盖；关系中的 `k` 仍是 `parameter_slot_candidate`，不得在本节固化为数值、阈值或执行条件。

`convexity_supply_vega` 按 D15 / D18 及 B.3.* 作为 shape-preserving derived governance input 与 coverage by shares 并列进入约束输入。R6 在本版保持 `settled`：该对象的重建已完成，但旧 spine 尚待批3 delta 重锚，因此不得提前标记为 `closed`。供给视图可以说明期限、翼侧、曲面或情景缺口，不能吸收 coverage、funding、identity 或 governance decision。

Manual review 必须保持 Phase 权限拆分。Phase 3 可以随 candidate package 提交 `manual-review condition` 或 `manual-review recommendation`，表示证据冲突、lineage 不足或假设尚需人工核验；只有 Phase 4 才能形成 `manual review` governance decision。C.3 只传递前者及其依据，不替 Phase 4 作决定。

同一权限拆分适用于 no-action：`no_action_observation` 是 Phase 2 的事实记录，`no_action_decision` 是 Phase 4 在治理流程中的决定。C.3 不把缺少候选、暂不动作或证据不足自动解释为任何 Phase 4 decision。裁决规则和状态迁移逻辑不在 B-2 本节写死。

**承接概念**：
- **Constraint stack input**：candidate package 与相关 hard、identity、permission、mother-structure、coverage、funding、TC residual、Greeks / convexity supply、execution 和 audit 约束的描述性治理输入；不是 governance decision。
- **Coverage-by-shares input**：对 `T2 00A §5` H 层覆盖关系的原样引用，始终独立于 candidate 和 Greeks 聚合。
- **Mother-structure integrity input**：候选对四要件功能承担与对象身份可能产生的影响，引用 T0 / T3 既有状态，不重定义母结构。
- **Convexity-supply input**：引用 B.3.* `convexity_supply_vega` 的 shape-preserving 结论，与 coverage、TC residual 和账本证据并列。
- **TC-residual input**：引用 A.2 各节尚未关闭或可能被候选迁移的 residual-risk，不由 Greek 改善自动关闭。
- **Manual-review recommendation input**：Phase 3 对需要人工核验事项的条件或建议及其 lineage；不等于 Phase 4 manual review decision。
- **Post-action audit obligation input**：说明获批并执行后需要回到 C.4 接收哪些既有审计能力；不定义审计 trigger 或自动动作。

**域边界**：
- C.3 只向 Phase 4 提交 input，不作 approval、block、manual review、rollback 或 no-action 等 governance decision，也不定义这些决定的 cutoff、阈值或组合规则。
- Phase 4 在 constraint stack input 之上完成治理；裁决规则属于 Phase 4 权限域，不在 B-2 写成状态机、算法或自动执行逻辑。
- Coverage by shares 继续由 T2 00A §5 单一 canonical 承接；C.3 不复制其定义，不把 `k` 从 parameter slot 提权为硬数值。
- R6 只保持 `settled` 状态；其 `closed` 取决于批3旧 spine delta 重锚，不在本批提前完成。
- 依据指针：`T3 §1.3、§§11–12`、`T2 00A §5`、总控 `D15`、阶段1 `D17–D18`；Greeks 修正版 §10.1 仅作 Phase 3 / Phase 4 权限核验基准。

**不变式**：
- `Constraint stack input ≠ governance decision`；任何输入进入 Phase 4 后都不自然取得裁决权限。
- Coverage by shares 始终是 H 层独立约束，不被任何 candidate、proxy、risk-equivalent Greeks、`convexity_supply_vega` 或账本结论覆盖。
- `No_action_observation (Phase 2) ≠ no_action_decision (Phase 4)`；C.3 不跨层解释 no-action。
- Audit 发现问题只能形成 `repair_review_request → Phase 3`，禁止 `audit → action` 短路；该义务随 constraint stack input 一并保留。

## C.4 Post-Action Audit Interface（执行后审计接口）

> 承担：作为耦合层 audit 入口，接收 Part B 既有五维及 Vega-derived post-action audit 能力，并以 Part A 指定的 residual-risk 与最差路径目标进行比对；需要进入后续动作链时，只输出 `repair_review_request` 单向返回 Phase 3。

### 接收既有审计能力并完成耦合比对

C.4 不新建审计类型，也不替代 Part B 各维的独立 post-action audit。其输入明确来自 B.1 的 Post-action Delta audit、B.2 的 Post-action Gamma audit、B.3 的 Post-action Vega audit、B.3.* 的 Post-action supply audit、B.4 的 Post-action Theta audit 与 B.5 的 Post-action Rho audit。上述能力分别保留各自的风险语法、事实 lineage 与审计边界；C.4 只将其置于同一 mother-structure coupling 语境中比较。

耦合比对使用 Part A 的既有目标作为检查面：引用 A.2.4 flatness and non-Greek governance checks，检查局部 Greek 改善是否仍伴随 scenario-P&L、settlement、funding、margin 或 object-identity residual；引用 A.2.7 dynamic hedge residual，检查动作后的离散对冲、复制、执行与成本残差是否按候选声明迁移；引用 A.2.8 worst-path / scenario-P&L / object-identity stress，检查执行后结构在最差路径与身份压力中是否仍保持候选所声明的功能。C.4 不重述这些对象定义，也不另造 coupling audit taxonomy。

Audit 在本节是入口：它消费 B 各维审计结果、A 各节验证目标以及 mother-structure integrity 证据。它不是 trigger；本节不定义“若某状态则启动 audit”、周期阈值、自动监控规则或下一笔动作条件。Audit records 可以保留执行后事实、警告或关闭信息，但这些记录不进入动作生成链。

当耦合审计显示需要重新研究修复方向时，唯一允许进入后续动作链的输出是 `repair_review_request`，并且必须单向返回 Phase 3，重新形成 diagnostic 与 candidate，再进入 Phase 4。C.4 不得直接生成 candidate、approved action、rollback candidate、order、hedge、roll、rebalance、unwind 或其他执行指令；`audit → candidate / approved action / order` 均属于权限短路。

**承接概念**：
- **Five-dimensional audit intake**：接收 B.1 Delta、B.2 Gamma、B.3 Vega、B.4 Theta、B.5 Rho 的既有 post-action audit 结果，保持五维权限、lineage 与风险语法对等。
- **Vega-derived supply audit intake**：接收 B.3.* Post-action supply audit，检查 shape-preserving convexity supply 是否按候选声明迁移；不把它当作第六个 Greek 或新的 audit 类型。
- **Flatness comparison target**：引用 A.2.4 的多维 flatness / non-Greek checks，检验 Greek 审计通过是否仍留下其他 residual。
- **Dynamic-hedge residual comparison target**：引用 A.2.7，检验执行、复制、离散对冲与成本残差的迁移，不在 C.4 重定义 residual。
- **Worst-path and identity comparison target**：引用 A.2.8，检验执行后最差路径、scenario-P&L 与 object identity 压力下的结构完整性。
- **Coupling audit record**：汇集已有审计结果与比对结论的记录，不是 candidate、decision 或 trigger。
- **Repair review request**：审计需要进入后续动作链时唯一允许的接口输出，单向返回 Phase 3 重新形成 diagnostic 与 candidate。

**域边界**：
- C.4 只消费 B.1 / B.2 / B.3 / B.3.* / B.4 / B.5 的既有 post-action audit 能力；不替代、合并或新建 Delta、Gamma、Vega、Theta、Rho 及 supply audit 类型。
- C.4 对 A.2.4、A.2.7、A.2.8 只作目标指针引用，不复制 flatness、dynamic hedge residual 或 worst-path 定义。
- Audit 是执行后审计接口，不是自动触发器、candidate factory、治理裁决器或执行器。
- Repair review request 只返回 Phase 3；后续 candidate 仍须由 Phase 3 生成并重新进入 Phase 4 governance。
- 依据指针：`T3 §1.3、§§12–14`、阶段1 `D17、D19、OQ-06`；Greeks 修正版 §10.4 与 Trading Concepts 修正版 §10.5 仅作 post-action 权限和 residual-risk 接口核验基准。

**不变式**：
- Candidate 仅由 Phase 3 形成；C.4 与任何 post-action audit 均不得直接生成 candidate。
- `No_action_observation (Phase 2) ≠ no_action_decision (Phase 4)`；audit record 也不得被改写为任一 no-action governance decision。
- `Audit → repair_review_request → Phase 3` 是唯一合法的修复回路；禁止 `audit → candidate / approved action / order` 短路。
- 五维 audit 能力来自 Part B 各维并保持独立；C.4 只提供耦合接口，不取代其 canonical 审计能力。

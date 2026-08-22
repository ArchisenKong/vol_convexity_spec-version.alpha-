
> **document_id**：`T0_波动率凸性操作方法论主文档`  
> **version**：`v1.0-T0-frozen-clean`  
> **status**：**frozen_clean**（门槛 1–11 全满足；KD freeze 第三审签字 20260615）  
> **generated_at**：`2026-06-15`  
> **lineage**：`T0FIX-01`（P1 八条）+ `T0FIX-02`（P2/P3 + 门槛8）已并入本文件；本文件 = 合并冻结产物  
> **immediate_predecessor**：`T0FIX-02 candidate`（SHA256 见 T0_freeze 决议记录 20260615）  
> **freeze_decision**：KD 第三审签字 20260615，门槛 1–11 全满足  
> **supersedes**：`T3 T0FIX-01 candidate`（f2669925...）→ `T3 T0FIX-02 candidate`（7dab7eb0...）→ 本 frozen_clean 产物  
> **semantic_authority**：三份文档共同构成平级 T0 语义冻结锚；T1 负责主题目录与组织关系，T2 负责统一术语、权限及 `00A §5` 的唯一权威定义，T3 负责策略专用操作承接；任何下游字段、算法、参数、YAML、profile 或 runtime 不得反向改写 T0。  
> **文档性质**：策略专用操作方法论主文档 / Strategy-specific Derived Methodology  
> **适用范围**：服务于用户当前波动率凸性、option-centric、路径响应型量化策略系统。  
> **上游依据**：T1（可复用方法论主题树，frozen_clean）、T2（12篇方法论文档集，frozen_clean）、Greeks 主文档（v0.1.2-freeze）、Trading Concepts 主文档（v0.1.2-freeze）、B-1 Taxonomy Bridge（v0.1-freeze 素材库）、Bridge 构建手册（v0.1）。  
> **用途边界**：本文是方法论主文档的 T0FIX 合并修订稿，不是字段文档、算法文档、YAML schema、参数注册表、执行手册、自动交易规则或生产风控规则。  


---

# 0. 文档定位、主语与边界

## 0.1 本文档是什么

本文档用于构建一套服务于用户当前波动率凸性量化结构的操作方法论。它的核心任务不是重写 Greeks 主文档，也不是重写 Trading Concepts 主文档，而是在现有上游方法论文档的边界内，把“波动率下注 / volatility positioning”“组合级 Greeks 管理 / portfolio Greeks governance”与“母结构四要件的运行治理”统一到同一套操作闭环中。

本文档的共同主语是：

```text
用户当前波动率凸性量化策略系统。
```

它不是一般期权交易手册，不是一般 volatility trading book，也不是动态对冲教材的摘要。本文所有操作语言都必须服务于以下策略对象：

```text
长期 Beta 占有
+ 短端供血与成本摊薄循环
+ 长端 long put + long call 双翼
+ 期限错配全维度管理
+ 动态 roll 维护 optionality 与凸性
```

其中，premium ledger / cashflow ledger / funding ledger 与 cost-dilution ledger 只是上述母结构中的账本表达层。它们用于校准 short-end OTM premium income、long-end premium bleed / theta decay cost、post-action cost basis 与 funding relation；它们不得替代长端双翼、期限错配、动态 roll、coverage、funding governance 或 object identity 裁决。

本文的目标是回答：

```text
1. 本策略到底持有什么样的波动率 / 凸性暴露；
2. 这些暴露如何通过 Greeks、曲面、路径、账本和期限结构被观察；
3. 当前组合是否仍然符合目标 volatility exposure thesis；
4. 母结构四要件、volatility exposure thesis、Greeks 状态、账本状态与 coverage / funding / identity governance 如何耦合；
5. 诊断如何形成 candidate action package；
6. candidate 如何进入 Phase 4 constraint stack；
7. 执行后如何审计 payoff shape、Greeks、cost basis、coverage、funding 与 object identity。
```

## 0.2 本文档不是什么

本文不生成、也不授权以下内容：

```text
生产字段定义；
字段命名与字段类型；
算法接口；
YAML schema；
YAML instance；
参数注册表；
固定 DTE；
固定 moneyness；
固定 strike；
固定 ratio；
固定 VIX 阈值；
固定 IV-RV 阈值；
roll trigger；
hedge trigger；
rebalance rule；
automatic vol bet execution rule；
automatic Greek decision engine；
自动下单逻辑。
```

本文中出现的 `volatility exposure thesis`、`target exposure envelope`、`portfolio Greeks state`、`premium ledger snapshot`、`diagnostic gap`、`candidate action package`、`post-action audit` 等表达，都是方法论对象或 taxonomy candidate，不是生产字段名、算法名、YAML key 或执行命令。

## 0.3 本文档与上游文档的关系

本文承接如下分工：

| 上游文件 | 本文承接方式 | 不承接事项 |
|---|---|---|
| T1（主题树 frozen_clean） | 承接 A1–A8、B1–B3、C1 的权限与组织结构；A6/A7/A8 仅承接操作接口与下游边界，不在 T3 展开完整工程实现 | 不把主题树示例字段生产化 |
| T2（12篇 frozen_clean） | 承接母结构四要件、QQQAI 原型降权、premium / Theta 术语校准 | 不把原型张数、收益叙事或成本归零表达生产化 |
| Greeks 主文档 v0.1.2-freeze | 承接 raw / proxy / diagnostic / risk-equivalent / scenario-stressed / governance input 分层 | 不把 Greeks 直接写成执行规则 |
| Trading Concepts 主文档 v0.1.2-freeze | 承接复制、替代、路径、分布、动态对冲、vol bet、worst-path 等交易概念边界 | 不改写 Taleb source claim，不生成 execution policy |
| Greeks / Trading Concepts Bridge | 承接 Phase / H-P-W / namespace / action lifecycle / forbidden automation 的下沉边界 | 不直接进入字段、算法、YAML |
| Bridge 构建手册 | 承接后续二级 Bridge 的标准流程 | 不在本文直接生成二级 Bridge |

## 0.4 核心禁止项

本文必须全程遵守以下禁止项：

```text
不得把 volatility thesis 写成交易信号；
不得把 volatility bet 写成单一 long vol / short vol；
不得把 Greeks diagnostic 写成 approved action；
不得把 net Greek 写成 risk neutral；
不得把 positive Theta 写成 safe carry；
不得把 short-end OTM premium income 写成 Greeks Theta；
不得把 cost-dilution loop 写成无风险收益；
不得把 candidate action 写成 execution rule；
不得把 post-action audit 写成 next trade trigger；
不得让 profile / YAML / runtime 覆盖 strategy core。
```

---

## 0.X｜核心操作思想：在母结构中理解波动率下注与 Greeks 管理

本文所说的“波动率下注”，
**不是**脱离持仓结构、脱离账本状态、脱离期限错配、脱离左尾保护与右尾参与的抽象 volatility view，
**也不是**简单判断未来隐含波动率会上升还是下降、未来 realized volatility 会高于还是低于 implied volatility、VIX 处于高位还是低位、skew 是否昂贵、term structure 是否处于 contango 或 backwardation，
**而是**在一个已经被定义为“长期 Beta 占有 + 短端供血与成本摊薄循环 + 长端 long put / long call 双翼 + 期限错配全维度管理 + 动态 roll 维护 optionality 与凸性”的**母结构内部**，
明确当前结构希望通过期权组合在不同价格路径、波动率路径、skew 形变路径、期限结构形变路径、跳跃路径、慢性磨损路径、急跌后反抽路径、右尾加速路径和低波消耗**路径中**，
**持有什么样的凸性暴露、承担什么样的成本、接受什么样的短端负凸性、保留什么样的左尾保护、维持什么样的右尾参与，以及在什么条件下必须承认原来的 volatility thesis 已经不再被当前组合状态所支持。**

因此，在本结构中，波动率下注首先不是一个交易信号，而是一个结构性暴露命题。
**不是**：“看多波动率，所以买入期权”，也不是说“看空波动率，所以卖出期权”，
**而是**：在希望长期占有科技 Beta 的前提下，是否愿意通过短端卖出期权获取权利金收入，并接受由此带来的 short Gamma、assignment、inventory、margin、gap、skew 和 liquidity risk。
**这些权利金收入**并不是利润本身，而**是用于部分抵消和缓释长端 put / call 双翼持续存在所产生的 premium bleed、theta decay、roll 成本以及期限错配维护成本，使整个凸性结构在账本层面更具可持续性**；
同时，**是否仍然保留足够的 long put 来对抗左尾路径，保留足够的 long call 来参与右尾路径，并通过期限错配和动态 roll 让这些 convexity exposure 不至于因为时间流逝、moneyness 漂移、Gamma center 偏离或 Vega 期限错配而从结构承诺退化成名义持仓。**

从这个角度看，波动率下注的核心不是“方向”，而是“形状”；不是预测某个单一市场变量，而是以标量 payoff functional `Π(X)` 表达目标收益形状，并以系统状态响应 `S(X)` 分别承接 Greeks、现金流、coverage、funding、object identity 和 post-action legality，使其在不同价格路径、波动率路径、流动性路径、账本路径和执行路径中共同守约；如果某个操作提高了当期权利金收入，却使左尾保护消失、右尾参与缺席、长端双翼钝化、期限错配失控或动态 roll 失去维护 optionality 的功能，那么即使它短期改善了 cashflow 或 Greeks dashboard，也不是本结构意义上的合格 volatility positioning，而只是以局部账本改善换取母结构身份漂移。

与此对应，组合级 Greeks 管理也不是把 Delta、Gamma、Vega、Theta、Rho 这些数字净额化之后追求某种看起来“平”的状态，更不是用 net Greek = 0、positive Theta、net Vega、Gamma flip 或某个 dashboard 指标来替代结构治理；在本结构中，Greeks 的真正作用，是把母结构在不同价格点、不同期限、不同 moneyness、不同 option type、不同 leg、不同 volatility surface coordinate 和不同 scenario 下的局部风险响应显性化，使交易者能够看到当前组合到底在哪里拥有 convexity，在哪里承担 negative convexity，哪里的 long wing 已经钝化，哪里的 short-end exposure 已经过度集中，哪里的 Vega 暴露集中在错误期限，哪里的 Theta 只是看起来有利但背后伴随 short Gamma 和 gap risk，哪里的 Delta-neutral 只是局部一阶平衡而不是风险中性，哪里的 post-action shape 已经偏离原来的左尾保护或右尾参与承诺。

因此，Greeks 管理在本结构中不是最终裁决器，而是结构状态语言；它不直接告诉系统“应该 roll”“应该 hedge”“应该 rebalance”“应该 monetization”，而是把当前组合的 raw exposure、proxy exposure、diagnostic exposure、risk-equivalent exposure 和 scenario-stressed exposure 以可审计方式呈现出来，并将这些信息交给 Phase 3 的 candidate action package 和 Phase 4 的 constraint stack 去判断：某个候选动作是否只是改善了表层 Greeks，却破坏了 coverage；是否只是提高了 short-end premium income，却扩大了不可承受的 short Gamma；是否只是降低了 long-end premium bleed，却删除了必要的 long put 或 long call；是否只是把 Delta 压平，却把 Vega、skew、path dependency、liquidity cost 和 execution residual 推到了更危险的位置；是否在执行后仍然保持同一个波动率凸性母结构，还是已经变成了 pure wheel、单侧保险、短波动 carry、方向性 Beta 持有或其他不同对象。

波动率下注与 Greeks 管理必须统一起来，是因为二者分别回答同一个结构问题的两个侧面：波动率下注回答“这个结构想要持有什么样的风险形状”，Greeks 管理回答“当前组合实际上持有什么样的风险形状”；波动率下注给出 exposure thesis，Greeks 管理给出 exposure state；波动率下注定义左尾、右尾、路径、skew、term、Vega、Gamma 和成本之间的目标关系，Greeks 管理检验这些目标关系是否仍然存在于当前持仓、当前账本和当前市场状态中；如果只有 volatility thesis 而没有 Greeks governance，系统就会停留在叙事层，无法知道自己是否已经偏离结构承诺；如果只有 Greeks governance 而没有 volatility thesis，系统就会退化成指标管理，无法判断某个 Greek 改善究竟是在维护结构，还是在局部优化中消灭结构。

在这套结构中，短端虚值权利金收入与成本摊薄循环非常重要，但它不是母结构的全部，也不是 volatility positioning 的最终目的；它的合法位置是为长期 Beta 占有、长端双翼成本、账本生存能力和动态维护提供 cashflow / premium / funding ledger 支持，而不是以“卖出期权取得现金收入”本身证明结构安全；短端供血与成本摊薄循环必须始终接受 Greeks 管理和母结构治理的反向约束，即它取得的 premium income 是否伴随过量 short Gamma、过量 assignment risk、过量 inventory risk、过量 margin pressure、过量 skew exposure 或 event gap risk，是否在左尾路径中把长端 put 的保护效果抵消，是否在右尾路径中通过 covered call 或过度短端卖权限制 long call 的参与，是否在成本摊薄账本看起来改善的同时，使 `Π(X)` 的极端路径形状更脆弱，或使 `S(X)` 的结构约束失约。

长端 long put 与 long call 双翼也不能被理解成静态保险单或静态 lottery ticket；它们在本结构中的意义，是为母结构提供左尾与右尾的 convexity commitment，但这种 commitment 会随着时间流逝、标的移动、波动率变化、skew 变化、moneyness 漂移、liquidity condition 和 roll timing 而改变，因此它们必须进入组合级 Greeks 管理：long put 要被检查是否仍然承担 left-tail Gamma、put wing Vega、downside Delta activation、crash skew exposure 和 protection coverage；long call 要被检查是否仍然承担 right-tail participation、upside convexity、call wing Vega 和 post-crash rebound exposure；如果长端双翼在名义上仍存在、但在风险响应上已经远离有效激活区，或者其成本被短端供血压力迫使不断削弱，那么结构虽然看起来仍有 put / call，实质上已经可能发生 optionality decay 或 object identity drift。

期限错配与动态 roll 则是把上述思想从静态持仓推进到运行系统的关键环节；期限错配不是简单的“短端卖、长端买”，而是 premium income、long-end bleed、front/back tenor Vega、skew term structure、roll cost、liquidity term mismatch、Gamma center 和 funding relation 的共同治理问题；动态 roll 也不是机械展期，而是在不同价格路径和波动率路径下，通过功能迁移维护 optionality、Gamma center、long wing integrity、coverage、funding relation 和对象身份的过程；因此，每一次 roll、repair、partial monetization、replace funding leg、restore convexity 或 reduce short Gamma，都不能只问“是否改善了某个 Greek”或“是否降低了成本”，而必须问它是否维护了母结构四要件之间的功能关系，是否仍让短端供血与成本摊薄循环服务长端凸性，是否仍让长端 put / call 双翼同时存在，是否仍让期限错配处于可治理状态，是否仍让动态维护服务于 `Π(X)` 的凸性形状并保持 `S(X)` 守约，而不是服务于当期账面优化。

由此形成的完整操作思想是：先用 volatility positioning 定义当前母结构想持有的风险形状，再用 portfolio Greeks governance 观察当前持仓实际呈现的风险形状，然后把 premium / cashflow / funding ledger、cost-dilution ledger、long-end premium bleed、coverage、funding relation、tenor mismatch、roll optionality 和 object identity 放入同一张状态图中，识别目标形状与实际形状之间的 diagnostic gap；如果 gap 足够明确，才生成 candidate action package；如果 candidate action package 能通过 Phase 4 constraint stack，才可能成为 approved action；如果执行发生，必须再通过 post-action Greeks、payoff shape、premium ledger、cost basis、coverage、funding 和 identity audit 检查它是否仍然维护原结构；如果任何环节不能说明其对母结构的功能贡献，那么 no-action、manual review、block、repair_review_request 或 identity drift warning 都是合法输出，而不是系统失败。

所以，本文档的核心思想可以压缩为一句话：在本波动率凸性结构中，波动率下注不是预测波动率，而是定义结构希望持有的凸性暴露；Greeks 管理不是压平 Greeks，而是检验当前组合是否仍然持有这种凸性暴露；短端供血与成本摊薄循环不是安全收益来源，而是为长端双翼和长期 Beta 占有提供账本支持的风险承担机制；长端 put / call 双翼不是静态装饰，而是左尾保护与右尾参与的结构承诺；期限错配和动态 roll 不是执行技巧，而是维护 optionality、Gamma center 和对象身份的运行机制；所有这些内容必须被放入 Phase 2 事实计算、Phase 3 诊断候选和 Phase 4 治理裁决的权限链中，才能构成一套真正服务于母结构的操作方法论。

---

# 1. 策略母结构与操作方法论总框架

## 1.1 本策略维护的对象

本策略维护的不是某一条 option leg、某一个 Greeks 净额、某一组参数、某一个波动率指标，也不是某个具体 market view。它维护的是一个跨时间演化的组合状态对象。该对象的合法性来自收益函数形状、对象身份、母结构功能、账本生存能力、Phase 权限链和执行后审计，而不是来自某一次路径判断是否正确。

本策略的对象可表达为：

```text
在长期占有目标 Beta（当前主应用为科技 Beta）的前提下，
通过短端供血与成本摊薄循环、长端 long put + long call 双翼、期限错配全维度管理、动态 roll 维护 optionality 与凸性，
构造一个在左尾不被打死、右尾不严重踏空、成本可被账本化管理、路径剧烈运动时保持目标凸性 payoff 的 `Π(X)`，并使 `S(X)` 各状态分量共同守约。
```

这里的 `X` 不是单一价格路径，而是市场价格路径、波动率路径、skew / term structure、账本状态、流动性状态、组合 Greeks、库存、保证金、事件冲击、执行残差和治理状态共同构成的状态空间。

目标持仓身份与收益假设必须分层：`H_identity_target` 是长期占有 target Beta 的 H 层对象身份；`P_A` 是 target Beta 长期持有具有正期望的 P 层可证伪假设。二者的唯一权威定义见 `T2 / 00A §5`。若 `P_A` 被持续证伪，必须提交 identity / target review 类响应；long put 只能缓释左尾损失，不证明 `P_A`，也不阻断该审查。

## 1.2 母结构四要件

本文采用以下 canonical 表达，不再简写或替换：

```text
1. 短端供血与成本摊薄循环；
2. 长端 long put + long call 双翼；
3. 期限错配全维度管理；
4. 动态 roll 维护 optionality 与凸性。
```

第一，**短端供血与成本摊薄循环**不是单纯 short premium，也不是单纯卖权利金。它包括短端虚值或近虚值期权所取得的 extrinsic premium cashflow，也包括轮空收入、接货折扣、出货价差、剩余库存成本与累计现金流共同形成的 post-action cost basis 账本循环。

第二，**长端 long put + long call 双翼**不是单侧保险。long put 承担左尾保护、下行 convexity、crash skew / Vega exposure；long call 承担右尾参与、上行 convexity、暴跌后反弹或持续上涨路径中的再参与能力。删除任一侧，都不是同一母结构。

第三，**期限错配全维度管理**不是无条件 calendar arbitrage，也不是无条件低成本优势。它同时管理前端 premium income、后端 premium bleed、Vega term structure、skew term structure、liquidity term mismatch、roll cost、inventory、assignment、margin 与 scenario stress。

第四，**动态 roll 维护 optionality 与凸性**不是机械展期。roll 是功能迁移和结构维护动作。它需要回答 roll 前后谁承担左尾保护、谁承担右尾参与、Gamma center 是否迁移、optionality 是否钝化、cost basis 是否变化、对象身份是否守恒。

## 1.3 操作方法论三大模块

本文的操作方法论分为三部分：

```text
Part A｜Volatility Convexity Positioning
Part B｜Portfolio Greeks Governance
Part C｜Positioning × Greeks × Mother-Structure Governance Loop
```

Part A 回答“本策略到底下注什么 volatility / convexity exposure”。它不把波动率下注压缩为 long vol / short vol，而是拆解为 Gamma、Vega、skew、term structure、spot-vol correlation、vol-of-vol、path-vol dependency、dynamic hedge residual 与 convexity rent。

Part B 回答“当前组合实际持有什么 Greeks 状态，以及这些状态是否仍服务于母结构”。它不把 Greeks 作为裁决器，而是把 Greeks 分为 raw exposure、proxy observation、diagnostic、risk-equivalent、scenario-stressed、governance input，并嵌入 Phase 2/3/4 权限链。

Part C 回答“vol thesis、Greeks state、母结构四要件状态、premium / cost-dilution ledger、coverage、funding 与 object identity 如何耦合”。它是本文最核心的操作闭环。

**命名空间声明**：本文件的 `Part A / Part B / Part C` 仅为本文件内部章节分区，不对应主题树的 `A / B / C` 轴及其节点。跨文档引用必须同时写明文档名与 Part 全称，禁止使用裸 `A / B / C` 指代。


## 1.4 本文档的操作目标函数

本文档可以被理解为对 `S(X)` 与 `Π(X)` 的操作层展开。它不试图预测 `X`：volatility positioning 定义 `Π(X)` 的目标 payoff 形状，Greeks、账本、coverage、funding、可执行性与治理状态共同构成 `S(X)` 的守约检查。

本文档的操作目标函数不是单一数学目标函数，而是一组有序治理目标：

| 目标层级 | 问题 | 合法表达 | 不合法表达 |
|---|---|---|---|
| 身份目标 | 策略对象是否仍是同一对象 | 母结构四要件仍被承担 | 为了收益删除 long put / long call |
| 左尾目标 | 极端下跌路径中是否仍有保护 | long put / downside convexity / crash Vega 仍有效 | 用短端 premium income 证明左尾安全 |
| 右尾目标 | 暴涨或反弹路径中是否仍有参与 | long call / upside convexity / right-tail participation 仍有效 | covered call 收入替代右尾参与 |
| 成本目标 | 凸性成本是否被账本化治理 | premium income、premium bleed、cost basis 分账 | positive Theta = funding safe |
| 风险目标 | Greeks 是否准确表达结构状态 | raw / proxy / diagnostic / stressed 分层 | net Greek = risk neutral |
| 动作目标 | 动作是否从合法状态迁移到合法状态 | candidate → Phase 4 → approved / block / review | diagnostic → signal → order |
| 审计目标 | 执行后是否仍守约 | post-action Greeks + payoff shape + cost basis audit | post-action audit 自动触发下一笔交易 |

因此，本文的任何一条方法论表达，都应能回答两个问题：

```text
它维护的是 `Π(X)` 的哪个 payoff 目标，或 `S(X)` 的哪个守约分量？
它处在 Phase 2、Phase 3 还是 Phase 4 的哪个权限位置？
```

若一条表达无法回答这两个问题，则它只能作为弱观点、阅读注记或待审计候选，不能进入操作闭环。

## 1.5 本文档的理论依据

本文档的理论依据来自七条上游纪律的组合，而不是来自某个单独指标或交易经验。

第一，来自 A1 的 `S(X)` / `Π(X)` 构造论。系统面对的是不可稳定预测的状态空间 `X`；合法设计支点是构造系统状态响应 `S(X)`，并以标量 payoff functional `Π(X)` 表达可比较的收益形状，而不是预测方向、预测 VIX 或预测某个最可能路径。

第二，来自 A2 的证伪法。本文每一类 volatility thesis、Greeks diagnostic、premium ledger 结论和 candidate action 都必须能被反例路径、路径置换、流动性压力、执行残差和身份漂移检查攻击。

第三，来自 A3 的 H/P/W 权限。母结构四要件、对象身份、Phase 权限链、md 语义权威属于 H 层；risk-equivalent 规则、scenario set、candidate packaging、参数候选属于 P 层；market view、trader note、regime weak judgment 属于 W 层。

第四，来自 A4 的对象身份守恒。合法动作不是让某个 proxy 更好看，而是把对象从一个合法状态迁移到另一个合法状态，并保持母结构功能。

第五，来自 A5 与 C1 的 proxy / Greeks 治理。任何 Greek 聚合、IV 指标、VIX 指标、skew 指标、premium 指标都必须声明 aggregation scope、risk-equivalence rule、scenario assumption 与 allowed usage，否则只能作粗观察。

第六，来自 Trading Concepts 的路径、分布和执行残差语言。动态对冲不等于风险消灭，静态 payoff 不等于 full path risk，权利金不等于动态对冲者完整风险上限，volatility bet 不等于单一 long / short vol。

第七，来自 Taxonomy Bridge 的下沉边界。本文只生成方法论对象和 taxonomy candidate，不直接生成 production field、algorithm implementation、YAML instance、runtime binding 或 execution automation。

## 1.6 本文档的最小合格输出

一份合格的波动率凸性操作方法论，至少要能输出以下上游对象：

```text
volatility_exposure_thesis；
target_exposure_envelope；
portfolio_greeks_state_snapshot；
premium_ledger_snapshot；
cost_dilution_ledger_snapshot；
coverage_funding_identity_check；
diagnostic_gap；
candidate_action_package；
constraint_stack_input；
post_action_shape_audit；
repair_review_request_or_audit_close。
```

这些对象都不是生产字段名或 YAML key，而是后续二级 Taxonomy Bridge 的候选命名空间对象。任何对象若要下沉为字段、算法、参数或 YAML，必须经过独立 Bridge 与下游可衍生性审计。


---

# Part A｜Volatility Convexity Positioning 方法论

# 2. 波动率下注的对象定义

## 2.1 volatility bet 不等于 long vol / short vol

在本策略中，volatility bet 不能被简化为“看多波动率”或“看空波动率”。`long vol / short vol` 是高度压缩后的交易语言，只能作为粗略描述，不能作为完整风险表达，更不能成为执行规则。

一个真实的 volatility bet 至少要拆成以下问题：

```text
是 Gamma bet，还是 Vega bet；
是 realized path bet，还是 implied volatility repricing bet；
是 skew bet，还是 term structure bet；
是 vol-of-vol bet，还是 path-vol dependency bet；
是持有 convexity rent，还是通过 short premium 承担 negative convexity 换取 cashflow；
该下注由哪条腿承担；
成本由哪个账本支持；
失败路径是什么；
动作后是否仍保留母结构四要件。
```

因此，本文中的 volatility positioning 是一个结构性暴露目标，不是一个方向性 signal。

## 2.2 本策略中的 volatility convexity positioning

本策略的 volatility convexity positioning 是：在长期占有目标 Beta（当前主应用为科技 Beta）的目标下，构造一个既接受部分短端 negative convexity 以取得 premium / cost-dilution cashflow，又保留长端 left-tail / right-tail convexity 的组合响应结构。

它的核心不是追求每个时点都 long Gamma / long Vega，也不是避免所有 short Gamma / short Vega，而是通过结构分工明确回答：

```text
哪里可以承担 short Gamma；
哪里必须保留 long Gamma；
哪里可以承担 short Vega；
哪里必须保留 long Vega；
哪个期限承担 premium income；
哪个期限承担 premium bleed；
什么状态下短端供血与成本摊薄循环仍然服务母结构；
什么状态下它退化为单纯卖权利金；
什么状态下长端双翼已经钝化或缺席；
什么状态下 roll 是功能维护，什么状态下 roll 是身份漂移。
```

## 2.3 波动率下注的基本分层

本文把 volatility positioning 分为八类对象：

| 对象 | 关注点 | 在本策略中的典型位置 | 禁止误用 |
|---|---|---|---|
| Gamma positioning | 价格路径与局部 convexity | 短端 short Gamma、长端 wing Gamma、中期 Gamma center | Gamma flip trigger |
| Vega positioning | IV level、tenor、surface | 长端 put/call Vega、期限错配 Vega、surface Vega | net Vega = vol neutral |
| Skew positioning | put wing / call wing 相对定价 | 左尾保护、右尾参与、crash skew | skew threshold signal |
| Term structure positioning | 前后期限 IV / carry / bleed | 短端 premium income、长端 premium bleed、calendar risk | term structure = stable carry |
| IV-RV / realized path positioning | 实现路径与 implied pricing 差异 | 动态对冲残差、gamma harvest 候选 | IV-RV 直接交易触发 |
| Spot-vol correlation positioning | 价格与波动率联动 | 下跌升波、上涨降波、下跌不升波、上涨升波 | 单一 regime 分类器 |
| Vol-of-vol positioning | vol surface 的非线性变化 | crash / rebound / surface deformation | 固定 Vvol 参数 |
| Convexity rent positioning | 为 convexity 支付或收取 rent | long-end premium bleed、short-end OTM premium income | Theta 收入覆盖 Theta 支出 |

---


## 2.4 Volatility exposure thesis 的生命周期

为了防止 volatility bet 从方法论对象滑向交易信号，本文把任何波动率下注表达都要求写成 lifecycle，而不是写成观点句。

标准 lifecycle 为：

```text
volatility exposure thesis
  ↓
target exposure envelope
  ↓
required leg / tenor / surface responsibility
  ↓
current portfolio state comparison
  ↓
diagnostic gap
  ↓
candidate input package
  ↓
Phase 4 governance
  ↓
post-action audit
```

其中：

| 生命周期节点 | 合法问题 | 禁止问题 |
|---|---|---|
| thesis | 需要什么路径响应 | 市场马上涨跌 |
| envelope | 需要什么 Gamma / Vega / skew / term / path exposure 区间 | 固定参数触发器 |
| responsibility | 哪条腿、哪个期限、哪个账本承担功能 | 某个合约天然等于功能 |
| state comparison | 当前组合是否偏离目标暴露 | 当前指标是否触发交易 |
| diagnostic gap | 偏离意味着什么 | 偏离即下单 |
| candidate package | 可提交治理的修复方向 | 已批准动作 |
| governance | 是否批准、阻断或人工复核 | 单一指标裁决 |
| audit | 执行后是否仍守约 | 审计结果触发下一单 |

一个不完整的 volatility thesis，例如“现在应该 long vol”“VIX 高所以减少保护”“skew 贵所以不买 put”，在本文中只能被视为 W 层 market note，不能进入 candidate action package。


# 3. 波动率交易四阶框架

## 3.1 一阶：Gamma / Vega 同侧

一阶波动率交易关注 Gamma 与 Vega 同侧的结构。例如，long straddle / long strangle 常被粗略理解为 long Gamma + long Vega，short straddle / short strangle 常被粗略理解为 short Gamma + short Vega。

在本策略中，一阶框架可以帮助理解最基础的 risk shape：

```text
长端 long put / long call 双翼：通常希望承担某种 long convexity / long optionality；
短端供血与成本摊薄循环：通常通过 short option 承担 short Gamma / positive Theta exposure / premium cashflow；
二者之间需要通过期限错配管理形成预算关系与风险分工。
```

但一阶框架不足以描述本策略。因为 calendar、diagonal、wing、roll、partial monetization、assignment、covered call、cost basis 和 dynamic hedge residual 都可能使 Gamma / Vega 的关系跨路径迁移。

## 3.2 二阶：Gamma / Vega 可反转

二阶波动率交易关注 Gamma 与 Vega 在不同路径、不同期限、不同价格区间、不同曲面状态下的反转。例如，某个结构在当前 spot 附近表现为 long Gamma，但在价格远离后可能 Gamma 钝化；某个远端 wing 在 crash skew 中表现为 long Vega，但在 vol crush 或 moneyness migration 后实际保护能力下降；某个 calendar / diagonal 结构可能在前端升波、后端不动时与在后端升波、前端回落时表现完全不同。

在本策略中，二阶框架尤其重要，因为母结构本身就是期限错配结构。短端供血与长端双翼之间不存在静态抵消关系。必须逐项检查：

```text
front short Gamma 是否被 back long Gamma 真实覆盖；
front positive Theta exposure 是否伴随不可承受 jump risk；
back long Vega 是否集中在错误期限；
wing option 是否已钝化；
roll 后 Gamma center 是否偏离需要保护的路径区间；
short premium income 是否真实支持 long-end premium bleed，而不是掩盖负凸性扩张。
```

## 3.3 三阶：spot-vol correlation

三阶波动率交易关注价格路径与 implied volatility 路径之间的联动。典型情形包括：

```text
下跌升波；
下跌不升波；
上涨降波；
上涨升波；
先下跌升波后反弹降波；
慢跌不升波并持续 theta bleed；
暴跌后 skew collapse；
反弹中 call wing repricing。
```

本策略不能假设“下跌必然升波”或“上涨必然降波”。spot-vol correlation 只能作为 scenario assumption 或 diagnostic input，不能作为无审计的 production mapping。

在左尾路径中，long put 的价值可能来自价格下跌、Gamma 激活、Vega 上升、skew 扩张和 liquidity premium 多个来源；在某些路径中，价格下跌但 IV 不升，保护腿收益会弱于预期；在暴跌后反弹路径中，long call 的右尾参与可能重新成为结构核心。本文要求所有这些关系进入 scenario-stressed Greeks 与 path-vol diagnostic，而不是写成单一路径规则。

## 3.4 四阶：vol-of-vol

四阶波动率交易关注 volatility surface 自身的波动性与非线性变形。对本策略而言，vol-of-vol 不是一个固定参数，而是一组风险现象：

```text
IV level 剧烈变动；
skew 快速扩张或塌缩；
term structure 从 contango 切换到 backwardation；
front tenor vol 与 back tenor vol 反向移动；
wing vol 与 ATM vol 变形；
Vega 本身的有效性随曲面状态变化。
```

vol-of-vol 对本策略的影响主要体现在：

```text
长端 put / call 双翼的 repricing；
期限错配的 Vega term risk；
短端卖权的再定价风险；
roll 成本突然上升；
partial monetization 时机的候选价值；
post-action shape 与 cost basis 的不稳定。
```

四阶框架的用途是帮助定义 scenario set 和 diagnostic taxonomy，不得被写成固定 Vvol 参数或自动交易触发器。

## 3.5 四阶框架与母结构映射

| 母结构要件 | 一阶暴露 | 二阶反转风险 | 三阶路径联动 | 四阶风险 |
|---|---|---|---|---|
| 短端供血与成本摊薄循环 | short Gamma / premium cashflow | assignment 后风险形状变化，covered call 后右尾钝化 | 下跌升波中 short leg 压力，上涨降波中收入受限 | front vol spike、liquidity gap |
| 长端 long put | downside Gamma / long Vega | wing dullness、moneyness migration | 下跌升波有利，下跌不升波保护变弱 | skew expansion / collapse |
| 长端 long call | upside convexity / call Vega | 深虚值钝化或上行激活 | 暴跌后反弹、上涨升波或降波路径 | call wing repricing |
| 期限错配与 roll | front/back Vega relation | Gamma center 和 Vega tenor 反转 | path order 改变 roll 成本与收益 | term structure shock、surface deformation |

---

# 4. 波动率下注的收益来源

## 4.1 Realized path convexity

本策略希望从某些 realized path 中获得 convexity response。该收益来源不是方向预测，而是路径展开对结构暴露的激活。例如：

```text
急跌路径激活 long put；
跳跃路径暴露 short Gamma 风险并检验左尾保护；
先跌后反抽路径同时考验 long put monetization 与 long call re-entry；
持续上涨路径考验 long call 是否保留右尾参与；
高振幅震荡路径可能产生 Gamma / roll / partial monetization 候选；
低波慢磨路径考验 long-end premium bleed 与 cost-dilution ledger 的持续性；
低 IV 震荡磨损路径：定义与反例地位见 `T2 / 00A §5`；本文仅承接其操作诊断。
```

Realized path convexity 的核心不是“市场动得越大越好”，而是：组合是否在关键路径区间持有正确的 convexity，并且成本、coverage、funding 与 identity 仍然守约。

## 4.2 Implied volatility repricing

第二类收益来源是 implied volatility repricing，包括 IV level、skew、term structure、surface curvature 和 local deformation。长端双翼通常对 implied volatility repricing 敏感，短端卖权则可能在 vol spike 中承受压力。

本策略必须区分：

```text
IV 上升使 long put / long call 增值；
IV 上升也会使短端 short option 承压；
skew 扩张可能强化 put wing，也可能让新增保护成本上升；
skew collapse 可能导致 put monetization 后 call transition 候选；
term structure 变化可能改变短端供血与长端 bleed 的预算关系；
vol crush 可能使长端 Vega 回吐，要求 partial monetization 或 roll candidate 被审查。
```

这些都是 diagnostic object，不是直接 signal。

## 4.3 Convexity rent

Convexity rent 是本策略的核心成本/收益语言之一。长端 long put / long call 双翼需要支付 premium bleed / theta decay cost；短端虚值权利金收入通过 premium ledger / cashflow ledger / funding ledger 提供部分预算来源；成本摊薄循环通过轮空收入、接货折扣、出货价差、剩余库存成本和累计现金流更新 post-action cost basis。

因此，不能把 convexity rent 写成：

```text
短端 theta 收入覆盖长端 theta；
positive Theta = funding safe；
short premium = realized profit；
cost basis down = risk down。
```

合法表达应是：

```text
short-end OTM premium income provides ledger support for long-end premium bleed；
premium ledger 与 Greeks ledger 分账；
positive Theta exposure 是 Greeks observation，不是 realized income；
cost-dilution loop 是账本循环，不是风险消灭；
funding relation 必须进入 Phase 4 governance input。
```

## 4.4 Dynamic hedge residual

动态对冲与交易调整本身会形成收益或损失残差。相同终点价格、相同总波动率，不代表相同 path P/L。路径顺序、交易频率、bid-ask、execution lag、liquidity、hedge instrument identity 都会改变结果。

因此，动态对冲在本文中不是“消灭风险”的工具，而是“改写风险形状”的动作类型。所有 hedge / roll / replacement / partial monetization 都必须进入 action lifecycle：

```text
diagnostic
  ↓
candidate input package
  ↓
Phase 4 constraint stack
  ↓
approved / blocked / manual review
  ↓
executed action
  ↓
post-action audit
```

---

# 5. 波动率下注的成本来源

## 5.1 Long-end premium bleed / theta decay cost

长端 long put / long call 双翼的成本主要体现为权利金消耗与时间价值衰减。这个成本可以被表述为 long-end premium bleed / theta decay cost，但必须与短端 premium income 分账。

其风险包括：

```text
低波长期磨损；
wing option 长期不激活；
Gamma center 远离当前风险区；
Vega concentration 在错误期限；
roll cost 过高；
liquidity 变差；
right-tail / left-tail 任一侧被成本压力诱导删除。
```

关键纪律是：降低 long-end premium bleed 不能以删除母结构双翼为代价。若为了降低成本删除 long put 或 long call，属于 object identity drift，而不是优化。

## 5.2 Short-end premium income 的真实风险

短端虚值权利金收入不是无风险 carry。它通常伴随：

```text
short Gamma；
short skew；
short near-expiry convexity；
assignment risk；
inventory risk；
margin pressure；
gap risk；
event risk；
liquidity risk；
covered call 后右尾被截断的风险。
```

因此，短端供血与成本摊薄循环必须被视为账本与风险共同体。它可以为底层 Beta 持有成本、库存成本和长端双翼预算提供现金流来源，但不能证明 funding safety，更不能替代 coverage、funding governance 或 object identity 裁决。

## 5.3 期限错配成本

期限错配既是结构预算关系，也是风险结构。它的成本包括：

```text
front / back IV term mismatch；
front short option repricing；
back long option bleed；
term structure inversion；
calendar liquidity；
roll slippage；
Vega tenor wrong-way；
skew term deformation；
front-end assignment 与 back-end protection 之间的 timing mismatch。
```

期限错配不能被写成“短端收入稳定覆盖长端支出”。正确做法是把它作为 Phase 3 diagnostic 与 Phase 4 governance input，结合 premium ledger、cost basis、scenario-stressed Vega、Gamma center、liquidity 和 coverage 共同审查。

## 5.4 执行成本

执行成本包括 bid-ask、滑点、市场冲击、成交失败、交易延迟、对冲工具不可得、结算机制、行权/分配细节、broker 规则与账户约束。执行成本不是附属项，而是 Trading Concepts 中路径 P/L 和 worst-path risk 的组成部分。

任何 candidate action package 都必须包含执行成本和执行后审计计划。否则，即使 volatility thesis 与 Greeks diagnostic 看似合理，也不得直接进入 approved action。

---


## 5.5 失效判据形状

判据一｜wing effectiveness（双翼有效性）：维度为 long put / long call 各自的 moneyness band 位置 + 情景化响应能力（scenario-stressed Vega / Gamma 相对基准情景的响应比）；基准为该翼建仓时或上次 roll 后声明的目标激活区与目标响应水平；破坏形态为响应比低于槽位水平且持续超过槽位窗口，构成 wing dullness，触发 Phase 3 diagnostic 与 repair candidate；槽位为 `wing_responsiveness_floor`、`wing_dullness_window`（`parameter_slot_candidate`）。

判据二｜funding relation failure（供血关系失效）：维度为滚动窗口内累计 funding gap（short-end premium income − long-end premium bleed − roll cost）的形态；基准为账本口径的零轴与历史分布，基准选择本身为 `parameter_slot_candidate`；破坏形态为累计 gap 呈持续性负值且斜率不收敛超过槽位窗口，构成 `P_B` 失效证据并触发 manual review。若任何候选调整触及母结构四要件的删除或降级，则依据 A4 直接归类为新变体或 `identity drift`，必须进入 identity review，不得作为普通 repair candidate；槽位为 `funding_gap_window`、`funding_gap_persistence_shape`（`parameter_slot_candidate`）。

判据三｜cost-dilution loop failure（成本摊薄循环失效）：维度为压力路径与震荡磨损路径下 post-action cost basis 的演化形态（接货/出货循环是否在净额口径上恶化 cost basis）；基准为循环启动时声明的 cost basis 演化目标方向；破坏形态为连续 `parameter_slot_candidate` 个循环周期内 cost basis 逆向恶化且无尾部事件解释，构成循环失效证据；槽位为 `dilution_cycle_count`、`cost_basis_deterioration_shape`（`parameter_slot_candidate`）。

回测可以启发判据形状（探索性研究合法），但不得裁决判据形状。md 是判据形状的语义冻结对象；任何判据形状变更必须先经 Phase 4 治理裁决，再以新版本回写 md，单纯编辑 md 不构成裁决。数值部分随后重新进入 A6 参数治理与回测。

# 6. Volatility positioning 的失败模式

## 6.1 把 volatility bet 写成单一方向判断

典型错误包括：

```text
VIX 高 → 买保护；
VIX 低 → 卖保护；
IV-RV 高 → short vol；
IV-RV 低 → long vol；
skew 高 → 卖 put；
skew 低 → 买 put；
term structure contango → short front vol；
term structure backwardation → long vol。
```

这些表达可以是观察或候选输入，但不能成为策略合法性来源。volatility positioning 必须落回母结构：谁承担 left-tail convexity，谁承担 right-tail participation，谁承担 funding，期限错配是否守约，动作后是否仍是同一对象。

## 6.2 把 short premium 误认为稳定 funding

短端虚值权利金收入只是在特定路径和执行条件下取得的 extrinsic premium cashflow。它不是 Greeks Theta，不是已实现长期收益承诺，也不是 funding 安全证明。

若系统因为短端收入连续为正而扩大 short Gamma，导致 jump path、gap path、event path 中无法维持 long put / long call 双翼，或导致 margin / inventory 风险破坏成本摊薄循环，则 volatility positioning 已经失效。

## 6.3 把长端保护误读为静态保险

长端 long put / long call 双翼不是买入后永久有效的静态保险。它们会随时间、价格、IV、skew、moneyness 和 liquidity 变化而钝化或迁移。

典型失败包括：

```text
long put wing dullness；
long call absence；
Gamma center drift；
long Vega concentrated in wrong tenor；
right-tail participation 被 covered call 或 partial monetization 过度削弱；
left-tail protection 在 roll 后离开有效激活区。
```

## 6.4 把动态对冲误认为风险消灭

动态对冲、roll、partial monetization、replacement 都是风险改写动作，不是风险消灭动作。它们可能降低某个局部 Greek，同时新增 Vega、Theta、Rho、liquidity、execution、object identity 或 premium ledger 风险。

若系统用 hedge 后的 net Delta 或 net Gamma 证明 risk-neutral，或用 post-action PnL 证明动作合法，则属于 Trading Concepts 和 Greeks governance 的双重越权。

---


## 6.5 Volatility positioning 的最低合格表达

任何进入本文操作闭环的 volatility positioning，最低必须写成如下格式：

| 项目 | 必填内容 |
|---|---|
| thesis | 本次希望维护或调整的 volatility / convexity thesis 是什么 |
| exposure class | Gamma / Vega / skew / term / spot-vol / Vvol / path / rent 中的哪一类或组合 |
| structure responsibility | 由短端供血与成本摊薄循环、长端 put、长端 call、期限错配或 roll 中哪个功能承担 |
| expected benefit path | 该 thesis 在什么路径中应受益或减少脆弱性 |
| cost path | 该 thesis 在什么路径中消耗成本或暴露负凸性 |
| failure path | 哪些路径会证伪该 thesis |
| Greeks expression | 对应 raw / diagnostic / stressed Greeks 如何观察 |
| ledger expression | 对应 premium / cashflow / funding / cost basis 如何表达 |
| governance boundary | 该 thesis 只能生成什么 candidate，不得生成什么 action |

未能填满上述项目的 volatility expression，不得进入 candidate action package。


# Part B｜Portfolio Greeks Governance 方法论

# 7. 组合级 Greeks 管理的定位

## 7.1 Greeks 是风险语言，不是治理裁决器

Greeks 的合法身份是：

```text
observation language；
diagnostic language；
risk response language；
governance input；
audit object。
```

Greeks 的非法身份是：

```text
structure definition；
final decision；
single-action approval；
production parameter truth；
execution trigger；
cross-tenor / cross-surface unconditional netting tool。
```

因此，组合级 Greeks 管理不是让系统“追求某个净 Greek 目标”，而是让系统在不同 lot、leg、tenor、moneyness、option type、scenario、ledger state 下观察风险形状是否仍服务母结构。

## 7.2 组合级 Greeks 管理的任务

组合级 Greeks 管理需要完成以下任务：

```text
1. Phase 2：保留 raw Greeks ledger；
2. Phase 2：保留 premium / cashflow / funding / cost basis ledger；
3. Phase 3：生成 gamma center、vega concentration、theta burn、wing dullness、expiry-near risk 等 diagnostic；
4. Phase 3：把 diagnostic gap 打包为 candidate input package；
5. Phase 4：作为 governance input 进入 constraint stack；
6. Phase 4：执行后检查 post-action raw Greeks、payoff shape、cost basis、coverage、funding 与 object identity。
```

组合级 Greeks 管理的关键输出不是“买、卖、roll、hedge”，而是：

```text
当前结构状态是否守约；
哪些风险形状正在偏离；
哪些候选动作需要进入治理；
哪些动作应被 block 或 manual review；
执行后是否仍保持母结构身份。
```

---


## 7.3 Portfolio Greeks Governance 的输出形态

组合级 Greeks 管理的输出不是“买 / 卖 / 对冲 / 展期”，而是不同权限层的治理对象：

| 输出 | Phase | 含义 | 禁止误用 |
|---|---|---|---|
| raw Greeks snapshot | Phase 2 | 当前事实 | 直接裁决动作 |
| proxy Greeks display | Phase 2 / 3 | 压缩观察 | 作为风险中性证明 |
| diagnostic Greeks note | Phase 3 | 解释状态 | 写成 signal |
| scenario-stressed Greeks package | Phase 3 / 4 | 压力输入 | 替代完整 constraint stack |
| candidate action input | Phase 3 | 可提交治理的候选输入 | 写成 approved action |
| governance input | Phase 4 | 约束栈输入 | 写成 governance decision |
| post-action Greeks audit | Phase 4 | 执行后合法性检查 | 自动生成下一笔交易 |

因此，Portfolio Greeks Governance 的目标不是“把 Greeks 管到某个好看的数”，而是确保 Greeks 作为风险语言能稳定服务于 volatility thesis、账本状态、coverage / funding / identity 约束与 post-action audit。


# 8. Greeks Ledger：最低观察单位

## 8.1 raw Greeks ledger

raw Greeks 是 Phase 2 事实层对象。最低表达不应是 total Greek，而应至少保留：

```text
account；
strategy object；
underlying；
portfolio id；
lot；
leg；
side；
option type；
leg type；
expiry；
tenor bucket；
strike；
moneyness bucket；
spot / forward / futures basis；
calculation basis；
aggregation scope；
timestamp；
allowed usage。
```

raw Greeks 只能回答“当前事实是什么”。它不能解释状态意义，不能生成候选动作，不能批准执行。

## 8.2 option surface node

本文建议把组合级 Greeks 管理的基本观察单位定义为：

```text
option surface node
= leg × side × option_type × expiry / tenor × strike / moneyness × scenario
```

这个单位的意义是：不把不同期限、不同 moneyness、不同 option type、不同方向、不同 leg role 的 Greeks 混成单一 scalar。

例如：

```text
front short put Gamma；
back long put wing Vega；
back long call upside Gamma；
near-expiry short option binary risk；
roll candidate 后的 Gamma center；
covered call 后的 right-tail participation；
```

这些都必须按 node 观察，而不是被 total portfolio Greek 掩盖。

## 8.3 Non-netting principle

任何 Greek 聚合必须声明：

```text
aggregation scope；
risk-equivalence rule；
scenario assumption；
allowed usage；
validity window。
```

否则只能作为 rough observation。典型 non-netting 规则包括：

```text
front tenor Vega 不得直接与 back tenor Vega 净额后裁决；
short put Gamma 不得直接与 long call Gamma 净额后裁决；
ATM Gamma 不得与 wing Gamma 简单抵消；
put wing Vega 不得与 call wing Vega 无条件相加；
positive Theta exposure 不得替代 premium income；
net Delta 不能证明 right-tail participation 或 left-tail coverage；
net Vega = 0 不代表 vol risk neutral。
```

---

# 9. Greeks 度量形态六态与权限角色链

## 9.0 度量形态基准：六态 × Phase 正交标注

Vega / Greeks 的 canonical 度量形态基准为六态：

| 度量形态 | 方法论含义 | 默认 Phase 标注边界 |
|---|---|---|
| raw | 按原始持仓与风险节点保留的暴露 | Phase 2 fact |
| tenor | 按期限分段表达 | Phase 2 observation；可作为 Phase 3 input |
| forward-segmented | 按远期区段拆分表达 | Phase 2 derived observation；可作为 Phase 3 input |
| surface | 按波动率曲面坐标表达 | Phase 2 observation / Phase 3 diagnostic input |
| grid | 按价格—波动率—期限网格表达 | Phase 2 observation / Phase 3 diagnostic input |
| scenario-stressed | 在声明情景下重估 | Phase 3 diagnostic / Phase 4 governance input |

六态是度量形态枚举，Phase 是运行权限轴，两者必须正交。每个形态实例均须另行标注来源 Phase 与允许用途；某一形态进入 Phase 4 也只表示可作为 governance input，不等于 governance decision。下述 §9.1–§9.6 描述的是 raw / proxy / diagnostic / risk-equivalent / scenario-stressed / governance input 的权限角色链，不构成另一套度量形态计数。

## 9.1 raw Greeks

raw Greeks 是 Phase 2 对象。它们包括 raw Delta、raw Gamma、raw Vega、raw Theta、raw Rho 及必要的 calculation metadata。

raw Greeks 的合法用途：

```text
记录当前风险事实；
作为 display observation；
作为后续 diagnostic 输入；
作为 post-action audit 基准。
```

raw Greeks 的非法用途：

```text
直接触发 hedge / roll / rebalance；
直接证明 risk-neutral；
直接证明 funding safe；
直接生成 approved action；
直接覆盖 premium / coverage / object identity governance。
```

## 9.2 proxy Greeks

proxy Greeks 是对 raw Greeks 的压缩、分桶或摘要。例如 total Delta、tenor Vega bucket、Gamma by price band、Theta by leg type 等。proxy Greeks 可以帮助人类观察，也可以进入 Phase 3 diagnostic，但必须受 A5 proxy governance 约束。

proxy Greeks 的核心纪律是：

```text
proxy 可以提高可读性；
proxy 不等于事实全貌；
proxy 不得替代 raw ledger；
proxy 不得替代 constraint stack。
```

## 9.3 diagnostic Greeks

diagnostic Greeks 是 Phase 3 对象。它们解释“当前状态可能意味着什么”。典型 diagnostic 包括：

```text
gamma center drift；
price-band Gamma；
up/down Gamma asymmetry；
short Gamma concentration；
front/back Vega concentration；
surface / grid Vega diagnostic；
theta burn；
wing dullness；
expiry-near binary risk；
DdeltaDvol；
bleed；
progressive Vega；
post-hedge payoff shape diagnostic。
```

diagnostic Greeks 可以生成 manual review trigger 或 candidate input package，但不得生成 approved action。

## 9.4 risk-equivalent Greeks

risk-equivalent Greeks 是在明确声明等价规则后，把不同 leg、tenor、moneyness、option type 或工具之间的 Greeks 暂时转译为可比较诊断口径。

其必要前置条件包括：

```text
equivalence rule；
aggregation scope；
assumption set；
scenario set；
validity window；
input_only=true；
forbidden use。
```

risk-equivalent Greeks 不是 raw Greeks，也不是真实风险等价证明。它只能作为 Phase 3 diagnostic 或 Phase 4 governance input。

## 9.5 scenario-stressed Greeks

scenario-stressed Greeks 是在特定情景下重估的 Greeks。情景可以包括：

```text
price shock；
vol shock；
skew shock；
term structure shock；
liquidity shock；
margin regime shock（组合保证金制度收紧 / broker 风控参数变更）；
execution lag；
spot-vol correlation path；
event state matrix。
```

scenario-stressed Greeks 的用途是检查组合在反例路径、压力路径和交易残差路径下是否仍守约。即使进入 Phase 4，它也只是 governance input，不是 governance decision。

## 9.6 governance input

Greeks 进入 Phase 4 后，只能作为治理输入。Phase 4 必须同时检查：

```text
object identity；
母结构四要件；
coverage；
funding relation；
sizing constraint 集；
premium ledger；
cost-dilution ledger；
liquidity；
execution feasibility；
post-action legality；
manual review requirement。
```

任何单一 Greek、单一 diagnostic、单一 proxy、单一 scenario-stressed value，都不得生成治理裁决。

coverage by shares 必须拆成“口径 / 数值”两层。H 层覆盖关系为：`long put 名义覆盖 ≥ k ×（short put 义务仓 + 持有正股）`；该关系属于对象身份级结构义务，不得被 optimizer 删除、改写或以 Greek 净额替代。`k` 以及长端双翼预算 : 短端供血规模、结构总敞口 : 账户资本等边界数值属于 P 层 `parameter_slot_candidate`，必须进入 A6 参数册治理、版本化与回滚。Phase 3 只能用于 candidate 预过滤；生产值须经 Phase 4 参数治理，optimizer 不得直接写入。

---

# 10. Greeks × 母结构健康度映射

## 10.1 短端供血与成本摊薄循环

短端供血与成本摊薄循环的 Greeks 观察重点包括：

```text
front short Gamma；
near-expiry binary risk；
positive Theta exposure；
short Vega / skew exposure；
assignment sensitivity；
inventory Delta；
covered call 后 right-tail truncation；
margin / liquidity stress；
premium ledger 与 Greeks ledger 分账。
```

健康状态不是“短端收入为正”，而是：短端虚值权利金收入、接货折扣、出货价差、库存成本与累计现金流仍在服务底层持有成本、长端双翼预算和结构生存边界；同时 short Gamma、assignment、inventory、margin、liquidity 风险没有破坏左尾保护、右尾参与和对象身份。

失效状态包括：

```text
短端收入被误写成 safe carry；
positive Theta 被误写成 realized premium income；
front short Gamma 过度集中；
接货后库存风险失控；
covered call 过度截断右尾；
短端卖权扩张导致长端双翼预算反而被挤出。
```

## 10.2 长端 long put

长端 long put 的 Greeks 观察重点包括：

```text
left-tail Gamma；
downside Delta activation；
put wing Vega；
crash skew exposure；
wing dullness；
Gamma center；
protection coverage；
roll 后保护区间。
```

健康状态是：long put 仍然承担左尾保护和下行 convexity，而不是仅作为账面上存在的远虚值期权。若 long put 过度钝化、保护区间过远、Vega concentrated in wrong tenor、roll 后离开有效激活区，则需要进入 diagnostic gap，并可能生成 repair / roll / restore protection candidate。

long put 的方法论边界仅是左尾损失缓释：它不证明 `P_A` 的长期正期望，也不得阻断 `P_A` 被证伪后的 identity / target review。

但任何 repair candidate 都必须进入 Phase 4 constraint stack，不能由 Gamma 或 Vega 单项自动触发。

## 10.3 长端 long call

长端 long call 的 Greeks 观察重点包括：

```text
upside Gamma；
right-tail participation；
call wing Vega；
upside Delta activation；
post-crash rebound exposure；
covered call 后右尾是否被截断；
partial monetization 后 right-tail underparticipation。
```

健康状态是：本策略在右尾路径中仍保留再参与能力。若为了降低 bleed、增加 covered call premium 或锁定短期收益而删除 long call 或过度截断右尾，则不是局部收益优化，而是母结构身份风险。

## 10.4 期限错配全维度管理

期限错配的 Greeks 观察重点包括：

```text
front/back tenor Vega；
term structure exposure；
calendar spread residual；
front premium income vs back premium bleed；
front Gamma risk vs back convexity support；
skew term structure；
roll cost；
liquidity term mismatch；
scenario-stressed tenor Greeks。
```

健康状态是：期限错配继续作为结构预算关系和风险管理关系，而不是退化为“短端收入覆盖长端成本”的口号。

失效状态包括：

```text
front Vega risk 与 back Vega protection 不匹配；
term structure shock 后 funding relation 失效；
长端 Vega 位于错误期限；
roll cost 高到破坏 cost-dilution ledger；
短端 assignment 与长端 protection timing mismatch。
```

## 10.5 动态 roll 维护 optionality 与凸性

动态 roll 的 Greeks 观察重点包括：

```text
Gamma center drift；
optionality decay；
moneyness migration；
wing dullness；
Vega tenor migration；
pre-roll / post-roll payoff shape；
function preservation；
post-roll cost basis。
```

roll 的合法性来自功能维护，而不是机械展期。一个 roll candidate 必须说明：

```text
它维护了什么功能；
迁移了哪个承担者；
降低了什么风险；
新增了什么风险；
对 premium ledger 和 cost basis 有何影响；
对 left-tail / right-tail / funding / identity 有何影响。
```

---

# 11. Greeks → Candidate Action Package

## 11.1 candidate action 不是 approved action

本文所有动作语言都必须经过 action lifecycle：

```text
raw observation
  ↓
diagnostic
  ↓
candidate input package
  ↓
governance input validation
  ↓
constraint stack check
  ↓
governance decision
  ↓
approved / blocked / manual review
  ↓
executed action
  ↓
post-action audit
```

Phase 3 可以生成 candidate input package，但不得生成 approved action。Phase 4 才能作出 approval、block、manual review、rollback 或 identity drift declaration。

本文在操作层冻结 B2 三条不变式：

```text
不变式 1：candidate 仅由 Phase 3 生成；Phase 4 governance / audit 不得直接生成 candidate。
不变式 2：no_action_observation 是 Phase 2 事实记录；no_action_decision 是 Phase 4 治理裁决，二者权限不同。
不变式 3：post-action audit 若发现修复需求，只能输出 repair_review_request 并返回 Phase 3；禁止 audit → candidate / approved action / order 短路。
```

## 11.2 典型 candidate action 类型

本文允许在方法论层定义以下 candidate 类型，但不定义具体触发器：

| Candidate 类型 | 触发来源示例 | 必须审查 |
|---|---|---|
| roll long option candidate | Gamma center drift、wing dullness、optionality decay | coverage、Vega tenor、cost、identity |
| repair wing candidate | left-tail 或 right-tail undercoverage | 双翼完整性、funding、liquidity |
| reduce short Gamma candidate | front short Gamma 过度集中、event risk | premium ledger、assignment、margin |
| replace funding leg candidate | short leg 风险形状恶化 | cost basis、funding relation、execution feasibility |
| partial monetization candidate | 长端 convexity 激活、vol spike、path gain | 剩余 coverage、right-tail / left-tail participation |
| block action candidate | 动作破坏母结构、覆盖不足、身份漂移 | constraint stack |
| manual review trigger | lineage 缺失、diagnostic 冲突、scenario disagreement | 人工复核 |

## 11.3 Candidate package 必须包含的内容

一个合格的 candidate input package 至少包括：

```text
diagnostic source；
raw Greeks snapshot；
proxy / diagnostic Greeks summary；
risk-equivalent / scenario-stressed Greeks；
volatility exposure thesis impact；
premium ledger snapshot；
cost-dilution ledger snapshot；
coverage check；
funding relation check；
object identity check；
liquidity / execution feasibility；
assumption set；
scenario set；
lineage metadata；
forbidden automation check；
post-action audit plan。
```

缺少这些信息时，candidate 不得进入 approved action，只能进入 manual review 或 hold。

---


## 11.4 Candidate action 的语义边界

本文允许讨论 candidate action，但所有 candidate action 都必须保持在 Phase 3，且不得包含执行授权。为了防止候选动作漂移为交易规则，每一个 candidate action package 必须至少回答：

```text
1. 候选动作试图维护哪一个母结构功能；
2. 候选动作源自哪个 diagnostic，而不是哪个 market view；
3. 候选动作依赖哪些 raw Greeks、scenario-stressed Greeks、premium ledger 与 cost basis facts；
4. 候选动作若执行，预期把对象从哪个合法状态迁移到哪个合法状态；
5. 候选动作可能破坏哪些功能：left-tail coverage、right-tail participation、funding relation、object identity；
6. 候选动作需提交哪些 Phase 4 checks；
7. 候选动作被批准后，执行后审计应检查什么；
8. 候选动作在哪些反例路径下应被 block 或 manual review。
```

不能回答上述问题的候选，只能是 diagnostic note 或 manual review trigger，不得进入 candidate action package。

## 11.5 动作语义的允许列表

本文允许使用以下动作语义，但它们全部只是 semantic primitive，不是触发器：

| 动作语义 | 方法论含义 | 禁止误用 |
|---|---|---|
| maintain | 维护现有功能承担 | 维持原仓位不审计 |
| repair | 修复钝化、缺口或错配 | 自动补仓 |
| reduce | 降低过量负凸性或错误集中 | 自动减仓 |
| migrate | 功能从旧腿迁移到新腿 | 机械 roll |
| monetize | 部分兑现已激活 convexity | 赚钱就卖 |
| replace | 替换失效承担者 | proxy 自动替代 |
| block | 阻断会破坏身份的候选 | 风险指标不好即阻断 |
| rollback | 对执行后非法状态提出回滚候选 | audit 自动回滚 |

这些动作语义必须经 `candidate → governance → approved / blocked / manual review → executed → post-action audit` 生命周期处理。


# 12. Post-action Greeks Audit

## 12.1 执行后不能只看 PnL

执行后审计不能只检查动作是否赚钱，也不能只检查某个 Greek 是否改善。必须检查：

```text
post-action raw Greeks；
post-action diagnostic Greeks；
pre/post payoff shape；
left-tail coverage；
right-tail participation；
premium ledger；
cost basis；
funding relation；
Vega tenor；
Gamma center；
liquidity residual；
object identity；
constraint stack residual；
manual review notes。
```

若动作后 PnL 改善但 long put 被删除、long call 缺席、短端供血与成本摊薄循环退化为单纯卖权、期限错配失控或 roll 后 optionality 消失，该动作不能被视为成功动作。

## 12.2 Post-action audit 不得生成 candidate 或下一笔交易

post-action audit 可以形成 `audit pass`、`audit warning`、`audit close`、identity drift declaration、documentation issue 或 lineage issue 等审计记录；这些记录描述执行后事实与合法性结论，不是 candidate。

若审计发现需要修复，唯一允许进入后续动作链的输出是：

```text
repair_review_request
  ↓
返回 Phase 3 重新形成 diagnostic 与 candidate
  ↓
重新进入 Phase 4 governance
```

禁止输出：

```text
rollback candidate；
next hedge order；
next roll trigger；
automatic rebalance；
automatic rollback；
new volatility bet execution。
```

因此，audit → action、audit → candidate、audit → order 均为权限短路。Phase 4 可以作出 rollback decision，但任何新的修复候选必须由 Phase 3 重新生成。

---

# Part C｜Positioning × Greeks × Mother-Structure Governance Loop

# 13. 母结构状态耦合框架

## 13.1 Volatility exposure thesis

`volatility exposure thesis` 是本策略对当前希望持有的 volatility / convexity 暴露的结构性描述。它必须回答：

```text
本结构希望在哪些路径受益；
在哪些路径接受成本；
在哪些路径承担短端负凸性；
在哪些路径必须保留长端正凸性；
当前主要风险来自 Gamma、Vega、skew、term、path 还是 cost ledger；
当前 exposure thesis 是否仍符合母结构四要件。
```

它不是市场预测，不是交易 signal，也不是自动 action。

## 13.2 Greeks state

`portfolio Greeks state` 是分 slice 的方法论状态视图，不是 typed container 或生产 schema。每个 slice 必须显式标注 `source_phase`、`aggregation_scope` 与 `allowed_usage`：

| Greeks slice | source_phase | aggregation_scope | allowed_usage |
|---|---|---|---|
| raw Greeks | Phase 2 | lot / leg / tenor / side / option type / moneyness / expiry 的原始节点 | 事实记录、lineage 与后续诊断输入；不得直接生成 candidate 或裁决 |
| proxy Greeks | Phase 2 observation；可作为 Phase 3 input | 已声明压缩、分桶或摘要范围 | 观察与诊断输入；不得替代完整对象状态或 constraint stack |
| diagnostic Greeks | Phase 3 | 已声明 diagnostic unit、来源节点与解释范围 | 解释 gamma center、vega concentration、theta burn、wing dullness 等状态，并可形成 candidate input；不得批准动作 |
| risk-equivalent Greeks | Phase 3；可作为 Phase 4 input | 已声明 risk-equivalence rule、聚合范围与适用假设 | 诊断或治理输入；未声明等价规则时不得使用 |
| scenario-stressed Greeks | Phase 3；可作为 Phase 4 input | 已声明价格、IV、skew、term structure、liquidity 情景及节点范围 | 压力诊断与治理输入；不得替代治理裁决 |
| Greeks-related governance input | Phase 4 | 已声明进入 constraint stack 的范围与 lineage | 辅助 approval / block / manual review；不等于 governance decision |

该状态视图回答当前实际持有什么局部响应形状、响应集中在哪些 leg / tenor / moneyness、是否与 volatility exposure thesis 一致，以及是否存在 net Greek 掩盖的结构风险。raw Greeks 固定属于 Phase 2；diagnostic Greeks 固定属于 Phase 3；任何跨 Phase 使用都必须保留上述三项标注。字段与 typed container 下沉至 B-2 / 0201 schema，不在 T0 定义。

## 13.3 Premium / cost-dilution ledger

`premium / cost-dilution ledger` 是母结构状态耦合框架中的账本表达层，而不是本文档的主语。它必须同时记录：

```text
short-end OTM premium income；
short-end extrinsic premium cashflow；
long-end premium bleed / theta decay cost；
轮空收入；
接货折扣；
出货价差；
covered call 相关现金流；
剩余库存成本；
累计现金收入；
post-action cost basis；
funding coverage relation。
```

该账本不等于 Greeks ledger。Theta 是期权价值对时间流逝的敏感度；premium income 是现金流；cost-dilution loop 是账本循环。三者不能混账。

## 13.4 Long put / long call integrity

`long put / long call integrity` 用于确认长端双翼是否仍然承担母结构中的左尾保护与右尾参与职能。它必须回答：

```text
long put 是否仍覆盖目标左尾路径；
put wing 是否因 moneyness drift、time decay、skew change 或 liquidity deterioration 而钝化；
long call 是否仍提供右尾参与与 upside convexity；
call wing 是否因被删除、过度 monetization、covered call 出货或 roll 后位置错误而缺席；
长端双翼的 premium bleed 是否被账本记录，但未因此被降级为可删除成本。
```

该状态不是单独交易信号。它只能作为 diagnostic、candidate input 或 Phase 4 governance input。

## 13.5 Tenor mismatch state

`tenor mismatch state` 用于确认期限错配是否仍是可治理的结构预算关系与风险承担关系，而不是被误读为无条件 calendar advantage。它必须回答：

```text
front tenor premium income 与 back tenor premium bleed 是否仍具有账本关系；
front / back Vega 是否存在错误净额化；
skew term structure、IV term structure、liquidity term mismatch、roll cost 是否破坏期限错配；
assignment、inventory、margin 与 settlement 是否改变期限错配的真实风险；
scenario-stressed tenor Greeks 是否显示期限错配已从预算结构变成风险集中源。
```

## 13.6 Roll optionality state

`roll optionality state` 用于确认动态 roll 是否仍在维护 optionality 与凸性，而不是机械展期或收益锁定动作。它必须回答：

```text
roll 前后的 Gamma center 是否仍有效；
long put / long call wing integrity 是否被维护；
moneyness relevance 是否仍匹配目标路径；
roll cost 是否破坏 funding relation；
roll 后 payoff shape 是否仍守住左尾 protection 与右尾 participation；
roll 是否造成 object identity drift。
```

## 13.7 Coverage / funding / identity governance

本文最终不是为了让每个指标好看，而是为了守住以下治理对象：

```text
左尾 coverage 是否仍存在；
右尾 participation 是否仍存在；
短端供血与成本摊薄循环是否仍服务母结构；
期限错配是否仍可承受；
roll 是否维护 optionality 与 convexity；
动作后是否仍是同一个策略对象。
```

Coverage、funding 与 identity governance 是 Phase 4 constraint stack 的核心，不得被 net Greeks、premium income、dashboard score 或单一 volatility thesis 替代。

---


## 13.8 状态对象总表

为了防止闭环混层，本文把操作方法论中的状态对象分为以下几类：

| 状态对象 | 回答的问题 | 合法载体 | 禁止误用 |
|---|---|---|---|
| market state | 外部价格、IV、skew、term、liquidity、event 状态是什么 | observation / proxy | 直接生成动作 |
| volatility thesis state | 当前希望持有何种 volatility / convexity exposure | thesis / envelope | 写成 signal |
| structure state | 母结构四要件是否仍被承担 | component / state slice | 用单一 Greek 替代 |
| Greeks state | 分 slice 的 raw、proxy、diagnostic、risk-equivalent、scenario-stressed 与 governance input 如何表达结构响应 | 每个 slice 标注 source_phase / aggregation_scope / allowed_usage | dashboard = governance；状态视图不得混同 Phase |
| wing integrity state | long put / long call 是否仍承担左尾保护与右尾参与 | protection / participation review | 只用成本判断是否保留 |
| tenor mismatch state | front/back tenor、Vega、skew、liquidity、roll cost 是否可治理 | tenor / surface / liquidity review | 期限错配 = 无条件低成本优势 |
| roll optionality state | roll 是否维护 optionality、Gamma center、wing integrity 与对象身份 | roll function review | roll = 机械展期 |
| ledger state | premium income、premium bleed、cost basis、inventory、cashflow 如何变化 | premium / cashflow / funding / cost-dilution ledger | short premium = safe funding |
| coverage / funding / identity state | 左尾、右尾、资金关系、对象身份是否守约 | constraint stack input | 用账本或 Greek 单项替代 |
| governance state | candidate、approval、block、manual review、audit、rollback 处于何状态 | action lifecycle / audit metadata | candidate = approved |

操作闭环必须同时读取这些状态。缺少关键状态时，不得给出 approved action；最多只能输出 no-action、diagnostic-only、manual review trigger 或 incomplete candidate package。


# 14. 操作闭环

## 14.1 标准闭环

本文采用以下操作闭环：

```text
volatility exposure thesis
  ↓
target Greek / surface / path exposure envelope
  ↓
current portfolio Greeks state
  ↓
mother-structure state：short-end loop / long put / long call / tenor mismatch / roll optionality
  ↓
premium ledger / cost-dilution ledger state
  ↓
coverage / funding / identity check
  ↓
diagnostic gap
  ↓
candidate action package
  ↓
Phase 4 constraint stack
  ↓
approved / blocked / manual review
  ↓
executed action
  ↓
post-action Greeks + payoff shape + cost basis + mother-structure integrity audit
```

该闭环中每一步都有权限边界：

```text
vol thesis：定义结构意图，不是 signal；
target envelope：定义目标暴露轮廓，不是执行参数；
current Greeks state：各 slice 分别标注 source_phase / aggregation_scope / allowed_usage；状态视图本身不是裁决；
premium ledger：账本事实，不是安全证明；
diagnostic gap：候选来源，不是动作批准；
candidate package：治理输入，不是执行命令；
constraint stack：治理裁决边界；
post-action audit：执行后审计，不是下一笔交易触发器。
```

## 14.2 no-action 也是合法输出

操作方法论不能假设每一次诊断都应产生动作。

动作的目的是维护结构凸性。Phase 2 的 `no_action_observation` 只表示事实记录中未发生动作，不含合法性裁决；Phase 4 的 `no_action_decision` 才表示候选经约束检查后被治理裁定为不动作。持续无动作期间，凸性状态与对象身份审计按 `parameter_slot_candidate` 周期触发；周期性审计若发现修复需求，只能输出 `repair_review_request` 返回 Phase 3，不得直接生成 candidate 或 next trade。

以下情形下，`no action`、`manual review` 或 `block` 是合法输出：

```text
diagnostic gap 不足；
raw data / lineage 缺失；
scenario assumptions 冲突；
candidate 破坏 left-tail coverage；
candidate 破坏 right-tail participation；
candidate 破坏 funding relation；
candidate 导致 cost basis 恶化但无法说明结构收益；
candidate 依赖未审计 volatility thesis；
candidate 需要固定阈值但参数尚未入册；
candidate 违反 forbidden automation registry。
```

---


## 14.3 闭环的合法输出类型

本文明确：操作闭环并不总是输出交易动作。合法输出包括：

| 输出类型 | 含义 | 权限 |
|---|---|---|
| no_action_observation | 事实记录，无动作与治理含义 | Phase 2 |
| no_action_decision | 完成约束检查后的不动作治理裁决 | Phase 4 |
| diagnostic_only | 状态解释，但不构成候选 | Phase 3 |
| manual_review_trigger | 需要人工复核 | Phase 3 / 4 |
| incomplete_candidate_package | 候选材料不足，暂不能提交治理 | Phase 3 |
| candidate_action_package | 可提交 Phase 4 审查的候选包 | Phase 3 |
| governance_block | Phase 4 阻断候选 | Phase 4 |
| approved_action_record | 通过治理但尚未执行的动作记录 | Phase 4 |
| executed_action_record | 已执行事实 | Phase 4 |
| post_action_audit_result | 执行后审计结果 | Phase 4 |
| repair_review_request | 审计发现修复需求，返回 Phase 3 重新形成 candidate | Phase 4 → Phase 3 |
| audit_close | 审计关闭，无下一动作 | Phase 4 |

这张表的作用是防止“系统必须交易”的隐含假设。对于波动率凸性结构，很多时候最正确的输出是 `no_action`、`manual_review` 或 `block`，而不是新交易。

## 14.4 闭环的阻断条件

当出现以下情形时，闭环必须阻断 candidate 或降级为 manual review：

```text
1. volatility thesis 不能说明其维护的母结构功能；
2. current Greeks state 缺少 raw lineage 或 aggregation scope；
3. premium ledger 与 Greeks ledger 混账；
4. short-end OTM premium income 被写成 Greeks Theta；
5. long put / long call 任一侧被候选动作削弱但未说明替代承担者；
6. 期限错配风险仅被写成 carry 优势；
7. candidate action 没有 post-action audit plan；
8. candidate action 绕过 coverage / funding / identity check；
9. 任何 diagnostic 被写成 signal；
10. 任何 post-action audit 被写成 next trade trigger。
```


# 15. 母结构四要件的联动诊断

## 15.1 短端供血与成本摊薄循环 × 长端双翼

短端供血与成本摊薄循环的作用，是为底层 Beta 持有成本、库存成本与长端双翼预算提供账本来源。但它不能证明长端双翼可以缺席。

联动诊断必须检查：

```text
short-end OTM premium income 是否真实进入 premium ledger；
long-end premium bleed 是否被单独记录；
短端权利金现金流是否对预算形成部分支持与缓冲，且没有诱导过量 short Gamma；
长端 put 是否仍有左尾保护；
长端 call 是否仍有右尾参与；
成本摊薄是否来自完整账本循环，而不是单纯卖权利金。
```

## 15.2 长端 put × 长端 call

长端 put 与长端 call 是双翼，不是可以随意替代的单侧保护。左尾保护和右尾参与必须同时审查。

典型联动问题包括：

```text
为了降低 bleed 删除 call，导致右尾缺席；
为了锁定 put 收益卖出保护，导致二次下跌中左尾缺席；
covered call 或 monetization 后右尾被过度截断；
long put / long call 的 Vega / Gamma 分布集中在错误期限或错误 moneyness。
```

## 15.3 期限错配 × Vega / Gamma / premium ledger

期限错配必须同时处理三件事：

```text
预算关系：short-end premium income vs long-end premium bleed；
风险关系：front short Gamma / Vega vs back long Gamma / Vega；
执行关系：roll cost、liquidity、assignment、inventory、settlement。
```

如果只看预算关系，容易把期限错配误认为 low-cost carry；如果只看 Greeks 关系，容易忽略 premium ledger 与 cost basis；如果只看执行便利，容易破坏长端双翼或对象身份。

## 15.4 动态 roll × object identity

roll 后必须检查：

```text
原功能是否仍存在；
保护区间是否仍有效；
Gamma center 是否合理迁移；
Vega tenor 是否改变；
long put / long call 双翼是否仍完整；
premium ledger 是否更新；
cost basis 是否更新；
roll cost 是否进入账本；
post-action payoff shape 是否守约。
```

roll 若只是延续合约期限但不维护 optionality 与 convexity，则不是合法 roll；roll 若改善局部 Greeks 但破坏母结构，也不是合法 roll。

---

# 16. 失败模式总账

## 16.1 Volatility positioning failure

典型失败包括：

```text
vol bet = long / short vol；
VIX level = action trigger；
IV-RV = action trigger；
skew scalar = distribution model；
term structure = carry guarantee；
vol-of-vol = fixed parameter；
path-vol assumption = fact；
vol thesis = approved trade。
```

## 16.2 Greeks governance failure

典型失败包括：

```text
net Greek = risk neutral；
Delta-neutral = risk-neutral；
net Vega = vol neutral；
positive Theta = safe carry；
Gamma flip = trigger；
soft / hard Delta switch = automatic tool choice；
Greeks dashboard = governance decision；
scenario-stressed Greek = final approval。
```

## 16.3 Cost-dilution failure

典型失败包括：

```text
short premium = stable funding；
short-end premium income = Greeks Theta；
cost basis down = risk down；
covered call income = right-tail enhancement；
轮空收入 = 结构合法；
接货折扣 = 左尾保护；
premium ledger replaces coverage / funding governance；
cost-dilution loop replaces object identity check。
```

## 16.4 Coupling failure

典型失败包括：

```text
vol thesis 与 Greeks state 脱节；
Greeks state 与 premium ledger 脱节；
premium ledger 与 cost basis 脱节；
coverage 与 funding governance 被 proxy 替代；
diagnostic gap 直接生成动作；
candidate action 绕过 Phase 4；
post-action audit 反向生成下一笔交易。
```

## 16.5 Object identity failure

典型失败包括：

```text
删除 long put；
删除 long call；
把 pure wheel 写成同一母结构；
把短端供血与成本摊薄循环简写为短端供血；
把短端 premium income 写成完整成本摊薄循环；
把期限错配写成无条件套利；
把 dynamic roll 写成机械展期；
把 VIX overlay、LETF、profile 或 YAML 配置提升为 strategy core。
```

---


## 16.6 补充重点失败模式

以下重点失败模式应纳入固定审计范围：

| 失败模式 | 风险 | 应对 |
|---|---|---|
| 目标对象缺失 | 文档退化为知识点汇总 | 所有章节回扣 `Π(X)` payoff 形状、`S(X)` 守约状态与母结构四要件 |
| 理论依据分散 | 后续审计无法判断为什么这样写 | 集中列示 A1/A2/A3/A4/A5/B2/C1/Trading/Bridge 依据 |
| candidate 语义过强 | 候选动作滑向执行规则 | 增加 candidate package 最低合格表达 |
| loop 输出单一 | 系统被暗示必须交易 | 增加 no-action、manual review、block、audit close 等合法输出 |
| 状态对象混层 | market / volatility thesis / structure / Greeks / wing / tenor / roll / ledger / governance 混用 | 增加母结构状态对象总表 |
| 操作原语触发器化 | maintain / repair / roll / monetize 被写成规则 | 明确动作语义不是触发器 |
| 审计触发下一单 | post-action audit 变成 next trade | 审计只可记录结果；修复需求以 repair_review_request 返回 Phase 3 |


# 17. Phase / H-P-W 权限总表

## 17.1 Phase 权限

| Phase | 本文中的合法内容 | 禁止事项 |
|---|---|---|
| Phase 1 | 结构原则、对象身份、母结构四要件、H/P/W、禁止项、文档语义 | 不生成实盘动作，不生成字段 / YAML / 参数值 |
| Phase 2 | raw exposure、raw Greeks、position ledger、premium ledger、cost basis facts、market snapshot | 不诊断、不生成 candidate、不批准动作 |
| Phase 3 | diagnostic、candidate input package、manual review trigger、repair proposal | 不直接执行，不生成 approved action |
| Phase 4 | constraint stack、governance input validation、approval / block / manual review、executed action audit、rollback decision | 不用单一 proxy / Greek / YAML 参数替代完整治理 |

## 17.2 H/P/W 权限

| 权限 | 本文中的对象 | 边界 |
|---|---|---|
| H | 母结构四要件、对象身份、Phase 权限链、md 语义权威、profile 不得覆盖 core、candidate 不等于 approved | 不得参数化、YAML 化、runtime override |
| P | volatility thesis assumptions、risk-equivalent rules、scenario sets、candidate parameter slots、diagnostic taxonomy | 可证伪、可审计、可替换，不得直接生产化 |
| W | market view、trader note、weak regime judgment、manual note | 只能作为 note / checklist / manual review input，不得成为 signal / rule / decision |

## 17.3 禁止越权链

```text
Phase 2 → candidate action；
Phase 3 → approved action；
diagnostic → signal；
candidate → execution order；
governance input → governance decision；
post-action audit → next trade trigger；
profile → strategy core；
YAML → md semantic authority；
runtime → constraint stack override。
```


## 17.4 紧急路径权限与外部治理者

存在一类事前经 Phase 4 批准的 playbook 动作，在事前声明的路径状态下可直接执行、事后审计。预授权的成立条件、动作清单与状态声明属于后续 playbook 文档，本条仅声明该权限类别存在及其前提：预授权本身是 Phase 4 事前裁决，不构成 diagnostic → order 越权。

broker / 清算方强制平仓构成 Phase 权限链的外部覆盖，属于权限链失效模式；其发生强制触发 object identity audit。

---

# 18. 下游工程化前置边界

## 18.1 可下沉候选

本文后续可通过二级 Taxonomy Bridge 下沉为 taxonomy candidate 的对象包括：

```text
volatility_exposure_thesis；
target_exposure_envelope；
portfolio_greeks_state_snapshot；
premium_ledger_snapshot；
cost_dilution_ledger_snapshot；
coverage_check；
funding_relation_check；
identity_preservation_check；
diagnostic_gap；
candidate_action_package；
post_action_shape_audit；
post_action_cost_basis_audit；
forbidden_automation_check。
```

这些对象只是 taxonomy candidate，不是字段名。

## 18.2 不可直接下沉对象

以下对象不得从本文直接进入字段、算法、参数或 YAML：

```text
具体 DTE；
具体 moneyness；
具体 strike；
具体 ratio；
具体 VIX threshold；
具体 IV-RV threshold；
具体 skew threshold；
具体 Gamma flip threshold；
具体 roll trigger；
具体 hedge trigger；
具体 rebalance rule；
具体 YAML key；
具体下单逻辑；
自动化 execution policy。
```

## 18.3 后续 Bridge 要求

本文定稿并通过一致性审计后，应生成：

```text
Volatility Positioning × Portfolio Greeks Governance Taxonomy Bridge_v0.1
```

该二级 Bridge 应至少包括：

```text
namespace taxonomy；
Phase / H-P-W 权限表；
action lifecycle；
field taxonomy bridge；
algorithm taxonomy bridge；
`parameter_slot_candidate` taxonomy；
YAML / config prerequisite；
forbidden automation / forbidden override registry；
lineage / audit metadata contract；
downstream gate。
```

## 18.4 A6 参数治理接口原则

T3 只冻结参数接口的不变式，不编排完整下游流程：

```text
diagnostic gap 可以提出 parameter_slot_candidate；
任何 production parameter 变更必须经过 A6 参数治理；
接口方向只能由上游方法论 / 已冻结约束指向参数册与 runtime binding；
参数结果不得反向改写 T0 语义；
每次生产参数变更必须可版本化、可审计、可回滚。
```

该原则不定义 evidence schema、审批状态机、resolver contract 或 post-deploy audit 编排；这些内容下沉至 doc3 后续操作层、0301 / 0302 与 A8 工程文档。

---

# 19. 审计清单

## 19.1 12 节点 → 本文承接矩阵与自审清单

篇号映射采用唯一真值：`01=A1 02=A2 03=A3 04=A4 05=B1 06=B2 07=A5 08=A6 09=A7 10=A8 11=B3 12=C1`。

| 12篇序号 | 节点 | 本文正式承接位置 | 自审项 |
|---|---|---|---|
| 01 | A1 | §0.X、§1.1、§1.4–1.5 | 是否区分 `S(X)` 与 `Π(X)`；Jensen 是否只作用于 `Π(X)` |
| 02 | A2 | §1.5、§5.5、§16、§19 | 是否保留反例路径、失效条件与“尚未被证伪”边界 |
| 03 | A3 | §17.2、§0.4 | H/P/W 是否标注且 W/P 未越权改写 H |
| 04 | A4 | §1.1–1.2、§12.1、§16.5 | 动作与参数变化是否保持对象身份；`P_A` 失效是否触发 review |
| 05 | B1 | §1.1–1.3、§13.8 | market / structure / Greeks / ledger / governance state 是否分层表达 |
| 06 | B2 | §11–12、§14、§17.1/17.3 | fact→diagnostic→candidate→governance 是否单向；三不变式是否成立 |
| 07 | A5 | §7.1、§8.3、§9、§13.8 | proxy / aggregate 是否声明 scope、equivalence、scenario、usage |
| 08 | A6 | §5.5、§17.2、§18.4 | diagnostic gap→production parameter 是否必经 A6、单向且可回滚 |
| 09 | A7 | §0.2/0.4、§18.1–18.3 | 是否保持 md→Bridge→YAML/代码单向投影，未过早字段化 |
| 10 | A8 | §0.2/0.4、§17.3、§18.3 | profile / runtime 是否只绑定部署，不得覆盖 core 与 constraint stack |
| 11 | B3 | §11.5、§12、§15.4 | hedge / roll / monetization 是否仅定义功能迁移与 candidate 语义 |
| 12 | C1 | Part B §7–10、§19.3 | 六种度量形态与 Phase 权限轴是否正交；Greeks 是否遵守 non-netting |

反向完整性自审：上述 12 节点均有可定位承接；A6、A7、A8 已进入正式矩阵，不再仅散落于正文。任何后续发现若命中已登记 spine 项，只登记指向 spine，不在 T0 现场扩写。

## 19.2 与 12 篇策略方法论一致性

应检查本文是否正确承接：

```text
短端供血与成本摊薄循环；
长端 long put + long call 双翼；
期限错配全维度管理；
动态 roll 维护 optionality 与凸性；
short-end OTM premium income 不是 Greeks Theta；
long-end premium bleed / theta decay cost 与短端 premium income 分账；
cost-dilution loop 不等于单纯卖权利金；
QQQAI 原型不得直接生产化。
```

## 19.3 与 Greeks 主文档一致性

应检查本文是否保持：

```text
raw / proxy / diagnostic / risk-equivalent / scenario-stressed / governance input 分层；
non-netting principle；
Greeks 不作为治理裁决器；
positive Theta 不等于 safe carry；
Theta 与 premium / funding / cash account 分账；
scenario-stressed Greeks 只是 governance input。
```

## 19.4 与 Trading Concepts 主文档一致性

应检查本文是否保持：

```text
volatility bet 不等于单一 long/short vol；
dynamic hedge 不等于风险消灭；
path P/L 与 worst-path risk；
spread / hedge / replication 不生成具体执行规则；
Trading Concepts 不直接授权 DTE、moneyness、strike、ratio、roll、rebalance 或 hedge trigger。
```

## 19.5 与 Bridge 手册一致性

应检查本文是否没有发生：

```text
误字段化；
误算法化；
误 YAML 化；
误自动交易化；
diagnostic → signal；
candidate → approved；
governance input → decision；
post-action audit → next trade trigger；
forbidden clause → implementation backlog；
profile / runtime / YAML 覆盖 strategy core。
```

---

# 20. 结论

## 20.1 本文档结论

本文档完成了三项统一：

```text
1. 把 volatility convexity positioning 从一般 long/short vol 语言中拆出，绑定到本策略母结构；
2. 把 portfolio Greeks governance 从 Greeks dashboard 管理中拆出，绑定到 Phase 2/3/4 与母结构健康度；
3. 把母结构四要件、short-end OTM premium income、long-end premium bleed、cost-dilution ledger、Greeks state、coverage / funding / object identity 统一进同一操作闭环。
```

本文不是执行手册，但可以作为后续审计、修订、二级 Taxonomy Bridge、字段 taxonomy、算法 taxonomy、参数候选、YAML schema prerequisite 的上游方法论材料。

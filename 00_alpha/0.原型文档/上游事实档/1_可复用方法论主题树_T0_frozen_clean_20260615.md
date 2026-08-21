# 可复用方法论主题树

> **document_id**：`T0_可复用方法论主题树`  
> **version**：`v1.0-T0-frozen-clean`  
> **status**：**frozen_clean**（门槛 1–11 全满足；KD freeze 第三审签字 20260615）  
> **generated_at**：`2026-06-15`  
> **lineage**：`T0FIX-01`（P1 八条）+ `T0FIX-02`（P2/P3 + 门槛8）已并入本文件；本文件 = 合并冻结产物  
> **immediate_predecessor**：`T0FIX-02 candidate`（SHA256 见 T0_freeze 决议记录 20260615）  
> **freeze_decision**：KD 第三审签字 20260615，门槛 1–11 全满足  
> **supersedes**：`T1 T0FIX-01 candidate`（2036eeab...）→ `T1 T0FIX-02 candidate`（b8b724e4...）→ 本 frozen_clean 产物  
> **semantic_authority**：三份文档共同构成平级 T0 语义冻结锚；T1 负责主题目录与组织关系，T2 负责统一术语、权限及 `00A §5` 的唯一权威定义，T3 负责策略专用操作承接；任何下游字段、算法、参数、YAML、profile 或 runtime 不得反向改写 T0。  


> **文档性质**：基于面对不确定性的方法论总结整理  
> **适用范围**：主要面向本文所指的交易体系，尤其是波动率凸性、以期权结构为核心的 option-centric、路径响应型策略系统。其中标 `[哲]` 的节点可外溢到交易之外；`[架] / [操]` 主要限于交易体系；`[工]` 可迁移到文档工程、配置工程、部署工程。  
> **效力声明**：本稿为方法论主题树结果稿，用于定义后续主题展开的目录、边界与组织原则。文中出现的具体字段名、指标名、算法名、参数名均为示例性表达，不构成冻结字段或生产规则；后续应根据具体主题、场景与工程阶段进一步展开、校准与固化。

---


## 0. 组织原则：二轴 + 工具层

本稿不再把所有主题排成单线顺序。复杂策略系统中，有些内容是**每个阶段都要遵守的横切纪律**，有些内容是**系统实际运行时走过的流程脊柱**，还有一类是**期权/波动率结构特有的操作语言**。

因此，本稿采用三部分组织：

```text
A. 横切纪律：每个运行环节都要同时受其约束
B. 运行脊柱：系统从对象、事实、诊断到动作的主流程
C. 工具层操作语言：option-centric 结构特有的方法论
```

抽象层标记如下：

| 标记 | 含义 | 迁移半径 |
|---|---|---|
| `[哲]` | 认识论 / 验证论 | 可迁移到任何高不确定系统 |
| `[架]` | 架构 / 对象治理 | 可迁移到本文所指的各类交易体系 |
| `[操]` | 操作 / 交易动作语义 | 主要适用于 option-centric 结构 |
| `[工]` | 工程治理 / 文档部署 | 可迁移到文档、配置、部署、审计系统 |


---

## 1. 总览表

| 节点 | 名称 | 轴 | 层 | 角色说明 |
|---|---|---|---|---|
| A1 | 未来不可知、S(X) / Π(X) 与凸性构造 | 横切 | `[哲]` | 定义不可预测世界中的系统构造支点 |
| A2 | 证伪法与反例工程 | 横切 | `[哲→架]` | 定义系统验证、反例生成与失败判定协议 |
| A3 | H/P/W 权限标注 | 横切 | `[哲→架]` | 定义判断、字段、假设与动作的权限等级 |
| A4 | 对象身份守恒与演化裁决 | 横切 | `[架]` | 定义系统升级、扩展、换工具后的身份保持规则 |
| A5 | proxy 治理 | 横切 | `[架]` | 限制指标、仪表盘、代理变量的使用权限 |
| A6 | 自由度治理：参数系统 | 横切 | `[架]` | 定义 θ 的注册、归册、回测、上线与回滚机制 |
| A7 | 文档与语义工程 | 横切 | `[工]` | 定义 md、YAML、审计与机器可读化边界 |
| A8 | 部署与 profile 工程 | 横切 | `[工]` | 定义 core、profile、deployment、runtime binding 的边界 |
| B1 | 对象身份与状态本体 | 运行脊柱 | `[架]` | 定义系统维护的对象与状态表达 |
| B2 | 事实 → 诊断 → 候选 → 治理的权限链 | 运行脊柱 | `[架]` | 定义从事实计算到治理裁决与执行回写的权限递进链 |
| B3 | 功能迁移与动作语义 | 运行脊柱 | `[操]` | 定义对冲、置换、roll、partial monetization 的功能语义 |
| C1 | Greeks 风险语言 | 工具层 | `[操]` | 定义 Greeks 的观察、诊断、聚合与治理边界 |

### 1.1 12 篇篇号 ↔ 主题节点对照

12 篇文档按写作顺序编排，篇号不等同于 A/B/C 节点的字母顺序。唯一对照为：`01=A1 02=A2 03=A3 04=A4 05=B1 06=B2 07=A5 08=A6 09=A7 10=A8 11=B3 12=C1`。任何跨文档映射、审计或下游承接均须使用该对照。


---

## 2. 方法论工作流：从策略设计到实盘运行

本文中的 Phase 不是工程进度编号，而是方法论权限分层。它用于说明一个量化策略从设计、事实计算、诊断、候选生成、治理裁决到实盘审计的完整链条。

| 阶段 | 名称 | 核心问题 | 可做 | 不可做 |
|---|---|---|---|---|
| Phase 1 | 结构设计与语义冻结 | 系统维护什么对象，母结构和硬边界是什么 | 定义 S(X)、Π(X)、对象身份、H/P/W、母结构、约束、文档语义 | 不做实盘动作，不用回测收益证明结构成立 |
| Phase 2 | 事实计算与原始暴露层 | 当前事实是什么 | 计算账本、持仓、raw exposure，例如 raw Greeks exposure | 不诊断、不生成候选动作、不批准执行、不做最终治理裁决 |
| Phase 3 | 诊断与候选生成层 | 当前状态意味着什么，可能需要什么候选 | 生成 diagnostic、candidate action、candidate parameter set、repair proposal | 不直接执行，不绕过治理 |
| Phase 4 | 治理裁决与执行审计层 | 候选是否被批准，执行后是否仍合法 | approval / block / manual review、constraint stack、post-action check、audit trail | 不反向改写结构原则，不用实盘结果覆盖 H 层 |

本文中的 `candidate` 只表示“可提交治理审查的候选对象”，不表示已批准、可执行或可上线。`constraint stack` 指由硬约束、身份约束、权限约束、执行前约束、执行后约束共同组成的治理判断集合。

---

# A. 横切纪律

---

## A1 未来不可知、S(X) / Π(X) 与凸性构造 `[哲]`

### 1. 核心内容

这一主题回答：

```text
面对不可稳定预测的世界，系统设计的起点是什么？
```

核心推导链为：

```text
未来不可知
  ↓
不预测 X
  ↓
构造系统状态响应 S(X)
  ↓
提取标量 payoff functional Π(X)
  ↓
凸性只作为 Π(X) 的形状目标
  ↓
以 S(X) 检查 Greeks、账本、coverage、funding、可执行性与治理合法性是否共同守约
  ↓
凸性有成本，因此必须与短端供血与成本摊薄循环、期限错配全维度管理、动态 roll 维护 optionality 与凸性共同设计
```

### 2. 方法论原则

#### 2.1 S(X) / Π(X) 优先于预测 X

面对不可稳定预测的状态空间变量 `X`，系统设计不应以预测 `X` 为核心，而应同时维护两类对象：

```text
S(X)：系统状态响应，包含 Greeks、ledger、coverage、funding、可执行性、治理合法性等异构分量；
Π(X)：标量 payoff functional，用于表达可比较的损益 / 收益形状。
```

系统质量不由观点是否正确决定，而由 `Π(X)` 在多路径、极端路径、反例路径、路径置换路径下的形状，以及 `S(X)` 的各项约束是否共同守约决定。`S(X)` 不是单一标量，不得把 coverage、funding 或治理合法性压缩进同一个数值目标后，与 payoff 共用同一期望算子或凸性序关系。

#### 2.2 未来不可知不是放弃结构，而是改变结构设计支点

“不预测”不是不行动，也不是无观点，而是：

```text
路径观点不能成为结构合法性来源；
Π(X) 的收益形状与 S(X) 的约束守约状态才是结构设计对象。
```

系统可以观察路径、分类路径、利用路径信息触发候选，但不能因为“市场大概率上涨/下跌/震荡/升波/降波”而直接定义动作合法性。

#### 2.3 凸性仅是 Π(X) 的构造目标

对于标量凸 payoff functional `Π`，在适用条件下可用 Jensen 直觉表达：

```text
E[Π(X)] ≥ Π(E[X])
```

Jensen 关系仅作用于 `Π(X)`；不得把 `S(X)` 中的 Greeks、coverage、funding、可执行性或治理合法性作为异构分量直接代入该关系。

在本策略语境中，`Π(X)` 的凸性目标包括：

```text
左尾不被打死；
右尾不严重踏空；
路径剧烈运动时 payoff 具有更强有利响应；
通过 roll / 功能迁移维持 optionality 与 gamma center；
通过短端供血与成本摊薄循环、期限错配全维度管理降低长期持有凸性的成本。
```

#### 2.4 凸性不是免费午餐

凸性有成本：long-end premium bleed / theta decay cost、流动性成本、roll 成本、执行滑点、低波路径下的 carry 压力。

因此，A1 不能只停在“要凸性”，而必须与 B1 的母结构四要件联动，并在 `S(X)` 中保留相应账本与治理状态：

```text
短端供血与成本摊薄循环：解决凸性成本、底层持有成本与长端双翼预算问题；
长端 long put + long call 双翼：提供双向尾部结构；
期限错配全维度管理：管理融资与 vega/carry/期限结构；
动态 roll 维护 optionality 与凸性。
```

### 3. 为什么独立成主题

A1 是最上层的世界观与构造论。它回答“为什么不预测”“不预测以后构造什么”“为什么必须区分 `Π(X)` 与 `S(X)`”“凸性为什么必须被供血”。

它不直接回答：

```text
如何验证系统是否失败；
如何设计反例；
如何回测；
如何审计参数；
如何判断身份漂移。
```

这些问题由 A2「证伪法与反例工程」承担。

### 3.1 结构原型来源说明

本策略母结构的经验原型可追溯至 QQQAI 型期权降本循环与结构化期限错配。该原型只用于说明“短端供血与成本摊薄循环、长端 long put + long call 双翼、期限错配全维度管理、动态 roll 维护 optionality 与凸性”这些母结构要件的来源与语义，不直接构成生产参数、交易规则、收益承诺或风险结论。

完整原型说明进入《波动率凸性策略可复用方法论文档集_12篇》的 `00B｜结构原型说明：QQQAI 降本循环与期限错配原型`。主题树只保留结构结论、原型来源指针与权限边界，不展开具体账本例子、张数示例或收益叙事。

### 4. 可复用表达

```text
方法论原则 A1：
当系统面对不可稳定预测的状态空间变量 X 时，设计支点不应是预测 X，而应是构造系统状态响应 S(X)，并以标量 payoff functional Π(X) 表达可比较的收益形状。

凸性目标只作用于 Π(X)；S(X) 中的 Greeks、账本、coverage、funding、可执行性与治理合法性必须分别守约，不得被压缩进同一个 Jensen 目标。
```

---

## A2 证伪法与反例工程 `[哲→架]`

### 1. 核心内容

这一主题回答：

```text
系统如何被验证？
什么叫系统失败？
如何主动寻找反例？
如何防止回测、参数优化、实盘结果反向污染结构原则？
```

证伪法不是 A1 的附属说明，而是整个系统的验证协议。

它的核心不是“证明策略赚钱”，而是：

```text
主动寻找能够破坏结构约束、对象身份、阶段权限、参数稳定性、proxy 边界、文档语义与部署绑定的反例路径。
```

### 2. 基本原则

#### 2.1 验证目标：不是证明有效，而是寻找失效条件

传统量化常见逻辑是：

```text
找到信号 → 回测盈利 → 证明有效 → 上线
```

本体系采用证伪式逻辑：

```text
冻结结构约束 C
  ↓
构造路径、压力、反例、扰动、置换
  ↓
寻找使 C 被违反的情形
  ↓
若找不到，则只能说明“尚未被证伪”
  ↓
不得说“已经证明有效”
```

#### 2.2 失败定义：失败不是亏损，而是身份漂移

亏损不必然等于系统失败；在约束内的亏损可能只是结构成本或正常路径损益。

真正失败包括：

```text
constraint violation；
object identity drift；
proxy usurpation；
phase privilege escalation；
path dependency；
parameter overfit；
governance bypass；
semantic drift；
profile 反向改写 core；
YAML 反向定义 md。
```

其中最高级失败是：

```text
系统为了继续运行或为了解释历史表现，改变了原本承诺维护的对象。
```

#### 2.3 存活状态语义：通过检验 ≠ 证明正确

如果一个参数集、动作规则或部署 profile 通过了路径置换、压力测试、反例扫描和治理审计，结论只能是：

```text
当前未被证伪；
当前可进入下一阶段候选或生产治理；
不代表已证明最优；
不代表未来有效；
不代表可绕过后续审计。
```

`baseline parameter set` 也只代表最小可运行基线，不代表收益最优。


#### 2.4 强路径依赖：证伪触发器，而非自动失败

期权结构天然具有路径敏感性；不同路径下 PnL、Greeks、账本与可执行性不同，并不自动构成失败。

强路径依赖的证伪含义更精确地说是：

```text
强路径依赖本身不是失败；
当结构合法性、参数合法性或动作合法性必须依赖特定路径顺序、特定样本族或特定流动性条件时，
它构成证伪触发器；
若进一步导致 constraint violation、object identity drift、proxy usurpation、phase privilege escalation 或 governance bypass，
则构成反例。
```

因此，path dependency report 的作用不是惩罚所有路径敏感性，而是识别系统是否把特定历史路径误写成结构合法性来源。

### 3. 证伪对象

证伪法必须明确“攻击对象”是什么。至少包括以下对象：

| 证伪对象 | 要攻击的问题 |
|---|---|
| `Π(X)` 标量 payoff 形状 | 是否在反例路径下失去凸性、左尾保护或右尾参与 |
| `S(X)` 系统状态响应 | 是否把 coverage、funding、可执行性或治理合法性错误压缩为数值优化目标，或在任一异构分量上失约 |
| 母结构四要件 | 是否有任一要件被删除、降级或 proxy 替代 |
| coverage / funding / vega 口径 | 是否被 Greeks、PnL、主观判断或参数优化替代 |
| 参数集 `θ` | 是否只在特定样本路径下有效，是否路径依赖过强 |
| 候选动作 `A` | 是否从合法状态迁移到非法状态，是否跳过 Phase 4 |
| Greeks / proxy | 是否从观察或诊断越权成为合法性裁决 |
| 文档语义变更 `ΔD` | 是否把补丁伪装成冻结原则，是否造成语义漂移 |
| YAML / profile | 是否反向改写 md/core，是否将部署值写成结构原则 |
| runtime / 实盘结果 | 是否因盈利或亏损反向改写 H 层原则 |

### 4. 反例生成方法

证伪法不是被动等待出错，而是主动构造攻击面。

可复用的反例工程方法包括：

```text
1. adversarial path replay：挑选最容易破坏结构的路径重放；
2. path permutation：路径顺序置换，检验合法性是否依赖特定路径顺序；
3. scenario stress：升波、降波、跳空、流动性消失、相关性反转等压力情景；
4. parameter sensitivity：参数扰动后是否迅速违反约束；
5. path dependency report：参数集或动作规则是否只在少数路径族中成立；
6. volatility regime inversion：从升波收益到降波回吐，检验 vega / gamma 关系是否反转；
7. liquidity stress：价差扩大、成交失败、链条不完整时动作是否仍合法；
8. action post-condition check：动作后是否仍满足对象身份与硬边界；
9. md consistency audit：不同 md 文件之间是否出现角色、阶段、权限冲突；
10. YAML ↔ md mapping audit：机器可读投影是否忠实于 md，而不是反向发明语义；
11. paper trading incident replay：实盘或仿真异常是否暴露文档层未定义状态。
```

### 5. 证伪输出

证伪流程不应输出“已经证明可赚钱”。

合法输出应包括：

```text
counterexample_report；
constraint_violation_report；
identity_drift_declaration；
path_dependency_report；
parameter_overfit_warning；
proxy_usurpation_warning；
phase_privilege_escalation_warning；
rejected_candidate_list；
repair_proposal；
governance_review_package；
rollback_recommendation。
```

### 6. 反馈环切断：证伪法的防过拟合机制

反馈环切断是证伪法的防过拟合子机制，用于防止归因、回测或实盘结果直接反向污染参数与结构原则。

必须切断两条反馈通路：

#### 6.1 断点 1：归因 → 参数变更

归因报告不能直接改参数。

合法路径是：

```text
归因 / 复盘
  ↓
研究输入
  ↓
候选参数集
  ↓
生产前证伪测试：反例路径、压力测试、路径依赖检查
  ↓
Phase 4 参数治理
  ↓
上线或拒绝
```

非法路径是：

```text
某次亏损 / 某次盈利 / 某次归因
  ↓
直接改参数
```

#### 6.2 断点 2：执行结果 → 结构原则

实盘赚钱或回测赚钱，不能反向修改 H 层结构原则。

非法路径是：

```text
某个实现路径收益很好
  ↓
把实现路径写成结构原则
```

合法路径是：

```text
执行结果
  ↓
incident / attribution record
  ↓
研究输入
  ↓
证伪测试
  ↓
必要时触发新版本 / 新变体 / identity review
```

### 7. 与其他主题的关系

| 相关主题 | 关系 |
|---|---|
| A1 | A1 定义构造目标；A2 攻击该构造目标是否守约 |
| A3 | H/P/W 决定哪些东西能被证伪、哪些东西只能触发候选 |
| A4 | 对象身份是证伪法判定“失败=身份漂移”的对象基础 |
| A5 | proxy 治理提供 proxy usurpation 的证伪对象 |
| A6 | 参数系统必须接受路径依赖、stress、candidate≠production 的证伪流程 |
| A7 | md 一致性审计是文档层证伪 |
| A8 | profile / deployment audit 是部署层证伪 |
| B2 | 事实 → 诊断 → 候选 → 治理的权限链每一步都可被检查是否越权 |
| C1 | Greeks 六种度量形态、Phase 权限轴与 non-netting 是 Greeks 证伪对象 |

### 8. 为什么独立成主题

证伪法不是“未来不可知”的一句补充，而是连接研究、回测、参数、动作、治理、文档工程、机器可读化和实盘复盘的总验证机制。

如果不独立成主题，后续文档容易退化为：

```text
收益好 → 参数好；
YAML 能跑 → 语义正确；
proxy 好看 → 结构合法；
实盘赚钱 → 原则可改。
```

这些都是证伪法要防止的对象。

### 9. 可复用表达

```text
方法论原则 A2：
复杂系统的验证目标不是证明有效，而是主动寻找能够破坏结构约束、对象身份、阶段权限、参数稳定性、proxy 边界与部署语义的反例。

通过证伪测试只能得到“尚未被证伪”的存活状态，不能得到“已证明最优”的结论。

任何由回测、归因、实盘结果直接反向改写结构原则或参数生产值的通路，都必须被切断并转入候选—证伪—治理流程。
```

---

## A3 H/P/W 权限标注 `[哲→架]`

### 1. 核心内容

系统内每一类判断、每一个字段、每一条约束、每一种候选动作，都必须标注其认识论权限。

| 级别 | 名称 | 含义 | 权限 | 失效后果 |
|---|---|---|---|---|
| H | 硬核 | 结构身份、不可由经验样本直接反驳的公理集、路径置换不变原则 | 否决、身份裁决、硬边界 | 触发身份漂移 |
| P | 保护带 | 可调假设、可证伪修正、诊断与参数化对象 | 回测、修正、替换、候选生成 | 判断错误但结构不必然失败 |
| W | 弱观点 | 当前状态判断、路径弱判断、timing input | inform timing、触发 candidate | 正常损益或低级别判断错误 |

### 2. 铁律

```text
W 不得成为合法性来源；
P 不得改写 H 层身份；
H 不得被参数优化、proxy、实盘结果或 YAML 投影反向推翻。
```

### 3. 与证伪法的关系

A3 为 A2 提供证伪强度分层：

```text
H 被破坏 → identity drift / hard failure；
P 被证伪 → 可修正 / 可替换 / 可重测；
W 失效 → 正常损益或 timing 错误，不得直接上升为结构失败。
```

### 4. 可复用表达

```text
方法论原则 A3：
任何系统元素在进入字段、算法、参数、YAML 或治理流程前，必须先标注 H/P/W 权限。

权限未标注的内容，不得承担裁决功能。
```

---

## A4 对象身份守恒与演化裁决 `[架]`

### 1. 核心内容

这一主题回答：

```text
系统升级、扩展、加工具、换标的、升版本以后，如何判断它还是不是同一个对象？
```

它是 B1「对象身份与状态本体」的动态版本。

### 2. 五条裁决原则

#### 2.1 升级 vs 新增：优先升级既有不变件，而非膨胀不变件集

当出现新职责时，应优先判断它是否属于既有母结构要件的升级，而不是立刻新增第五要件、第五模块。

典型例子：

```text
vega 期限结构管理
  ↓
应升级进入“期限错配全维度管理”
  ↓
不应新增第五母结构要件或第五主模块
```

#### 2.2 修正层不得篡位本体

overlay、VIX hedge、sleeve、杠杆 ETF（LETF）、工具实现层，只能服务本体，不得定义本体。

#### 2.3 主底座 vs 条件化变体

必须区分：

```text
当前主版本底座；
历史探索；
条件化变体；
后续扩展；
新对象。
```

不能把后续扩展或历史探索伪装成当前主版本底座。

#### 2.4 多标的扩展三档

| 档位 | 含义 | 处理 |
|---|---|---|
| 同类部署 | 如 QQQ / SPY / SMH 等同类 beta 扩展 | profile 处理即可 |
| 需对象身份审查 | 如 IWM，小盘 beta 与科技 beta 不同 | 需身份审查 |
| 需新变体 | VIX ETP / 杠杆 ETF（LETF） / 单股 / 加密 / 商品 | 不能直接复用 core |

#### 2.5 版本变化三档

```text
只动 profile；
需 core review（核心语义审查）；
需新变体 / 新对象。
```

### 3. 与证伪法的关系

A4 提供 A2 的最高级失败判据：

```text
若系统升级后仍能保持母结构四要件、对象状态、权限边界与治理路径，则可能是同一对象的演化；
若系统为了适应新路径或新工具而改变了本体职责，则触发 object identity drift。
```

### 4. 可复用表达

```text
方法论原则 A4：
系统演化时，不得以“功能增强”或“工具新增”为理由绕过对象身份审查。

新增职能首先判断是否属于既有不变件升级；若改变母结构、顶层目标、硬边界或权限链，则应声明为新版本、新变体或身份漂移。
```

---

## A5 proxy 治理 `[架]`

### 1. 核心内容

proxy 可以观察、报警、触发诊断、触发候选，但不能裁决结构合法性。

### 2. 通用聚合原则

任何 aggregate metric 在成为裁决输入前，必须声明：

```text
aggregation scope；
risk-equivalence rule；
scenario assumption；
allowed usage。
```

否则只能作为粗观察，不得作为诊断结论、动作批准或治理裁决。

### 3. 禁止的短路推理

```text
net gamma > 0 → 结构合法；
raw V_net > 0 → vega 安全；
delta 足够 → coverage 合法；
短端虚值权利金收入足够 → funding 合法；
回测收益高 → 参数可上线；
YAML 通过 → md 语义正确。
```

以上均属于 proxy 篡位或工程投影篡位。

### 4. 顶层口径不可被 proxy 替代

以下对象不得被 proxy 替代：

```text
long put / long call coverage by shares；
premium-based funding relation；
母结构四要件；
object identity；
Phase 4 constraint stack；
md 语义权威源。
```

### 5. 与 Greeks 的关系

Greeks 是特殊且重要的 proxy / risk response language，因此在 C1 单独成主题。A5 提供 Greeks 管理的通用 proxy 边界；C1 处理 Greeks 的 option-specific 细节。

### 6. 可复用表达

```text
方法论原则 A5：
任何 proxy 都只能被授权使用，不能自然获得裁决权。

proxy 若要进入治理层，必须先声明聚合范围、等价规则、情景假设与允许用途。
```

---

## A6 自由度治理：参数系统 `[架]`

### 1. 核心内容

参数系统只管理 `S(X)` 实现中允许被注册、配置、回测、优化、主观调节、版本化和审计的自由度 `θ`；参数可以影响 `Π(X)` 的实现形状，但不得定义 `S(X)` 或 `Π(X)` 的结构身份。

参数系统不定义 `F` 的身份。

### 2. 三册互斥

```text
structural_constant_book：结构常量 / 硬边界 / 身份条件，不可优化、不可主观调节；
parameterized_backtest_book：可回测、可优化、可生成 candidate parameter set；
subjective_adjustment_book：人工裁量变量，必须冻结范围、留痕、接受治理。
```

任一变量只能归入唯一参数册。

跨册迁移不是普通修改，而是对象重新定义，需要重新进入 freeze / review。

### 3. candidate ≠ production

生产前证伪测试只能生成候选参数集，不得自动进入正式生产状态。

```text
candidate parameter set
  ↓
证伪测试 / stress / path dependency report
  ↓
Phase 4 governance review
  ↓
正式绑定或拒绝
```

### 4. 参数系统的证伪要求

参数系统必须接受 A2 的证伪流程：

```text
不得以样本内收益最优证明合法；
不得依赖单一路径族表现；
必须输出 path_dependency_report；
必须接受 scenario stress；
必须保留 rollback path；
必须说明对收益函数形状、成本、触发、治理边界的影响。
```

### 5. 熵预算

参数数量不是越多越好。

当一个系统需要不断新增参数来修复回测表现，通常说明问题不在 θ，而在 `S(X)` 的结构设计或 `Π(X)` 的 payoff 形状本身。

```text
加参数不是结构修复；
加参数是增加系统熵；
参数增长必须有治理预算。
```

### 6. 参数解析器边界

参数解析器（resolver）只输出运行时参数（runtime parameters），不输出：

```text
candidate_action；
approved_action；
order_instruction；
governance_decision；
optimization_result；
structural_change。
```

### 7. 可复用表达

```text
方法论原则 A6：
参数系统管理自由度 θ，但不定义结构身份 F。

任何参数集的合法性只能来自结构约束内的证伪存活状态，而不能来自历史收益最优、路径观点正确或主观偏好。
```

---

## A7 文档与语义工程 `[工]`

### 1. 核心内容

机器可读化不能早于语义冻结。

```text
md 是语义权威源；
YAML 是工程投影；
profile 是部署实例；
runtime binding 是一次运行绑定。
```

### 2. 正确顺序

```text
md 语义升级
  ↓
md 一致性审计
  ↓
YAML 生成
  ↓
YAML ↔ md 映射审计
  ↓
profile binding
  ↓
runtime execution
```

### 3. 与证伪法的关系

文档工程也要证伪：

```text
是否存在同一概念多处定义冲突；
是否存在字段层声明权与算法层执行权混淆；
是否存在 YAML 反向新增语义；
是否存在 profile 反向改写 core；
是否存在旧文档中的硬约束执行逻辑未按新 Phase 边界迁移。
```

### 4. 可复用表达

```text
方法论原则 A7：
机器可读文件是 md 语义的投影，不是新语义来源。

任何 YAML / SQLite / runtime config 若发明了 md 中没有的结构原则，应视为语义漂移并进入审计。
```

---

## A8 部署与 profile 工程 `[工]`

### 1. 核心内容

部署变量必须外置，profile 只绑定 core，不改写 core。

其中，`core` 指策略核心语义与结构原则；`profile` 指部署侧配置；`deployment` 指一次具体部署实例；`runtime binding` 指运行时将 core、参数、profile 与环境配置绑定为可执行状态的过程。

### 2. 六层分离

```text
strategy_core；
machine_readable_core；
l0_config_profile；
underlying_profile；
account_profile；
deployment_profile。
```

### 3. 不得写入 core 的内容

```text
underlying_id 的具体部署值；
broker；
账户规模；
目标仓位；
现金保留比例；
最大账户净值使用比例；
标的特定流动性假设；
实盘 / paper mode。
```

这些都属于 profile，不属于策略本体。

### 4. profile 不得绕过硬约束

profile 不能因为账户小、标的不同、流动性差、部署方便而绕过：

```text
coverage 顶层口径；
premium-based funding relation；
Greeks non-netting；
参数三册互斥；
candidate ≠ production；
主观判断不定义合法性；
修正层不得篡位本体；
md 语义权威源。
```

### 5. 与证伪法的关系

profile 也需要接受 A2 的部署层证伪：

```text
标的变化是否改变对象身份；
账户规模是否使策略功能不可实现；
broker 约束是否导致动作后条件无法满足；
profile 是否隐式改写了 core；
resolver 是否读取了不该读取的部署值。
```

### 6. 可复用表达

```text
方法论原则 A8：
部署 profile 只能实例化与绑定，不得定义或修改策略 core。

任何部署变量若改变结构身份或治理边界，必须触发对象身份审查，而不能伪装成普通 profile 更新。
```

---

# B. 运行脊柱

---

## B1 对象身份与状态本体 `[架]`

### 1. 核心内容

系统维护的不是某条腿、某个 Greek、某个 roll 动作、某个参数集或某份 YAML，而是一个持续演化、可审计、可裁决、能保持同一性的组合状态对象。

### 2. 母结构四要件

```text
1. 短端供血与成本摊薄循环；
2. 长端 long put + long call 双翼；
3. 期限错配全维度管理；
4. 动态 roll 维护 optionality 与凸性。
```

四者缺一，即触发对象身份漂移。

### 3. 角色分离

任何系统元素进入字段、算法或 YAML 前，必须先声明角色：

| 角色 | 含义 |
|---|---|
| 母结构 | 定义对象是谁 |
| component | 承担某个结构功能 |
| state slice | 保存当前状态结论 |
| diagnostic unit | 解释当前状态 |
| proxy | 辅助观察，不裁决 |
| parameter | 可治理自由度 |
| governance | 判断是否合法、是否越界 |
| profile | 部署实例化绑定 |

### 4. 同一对象跨层多重身份

不要问：

```text
vega 应该放在哪一层？
```

而应问：

```text
这一层使用 vega 时，它的操作权限是什么？
```

例如：

| 层级 | vega 身份 | 权限 |
|---|---|---|
| 母结构 | 期限错配全维度管理的一部分 | H 管理职责 |
| component | raw exposure field | 事实 |
| proxy | by tenor / moneyness / expiry 观察 | P |
| diagnostic | risk-equivalent / scenario-stressed input | P / W |
| parameter | threshold / stress / equivalence rule | P |
| governance | legality input | H / P，但需经 Phase 4 |

### 5. 状态本体四分

完整对象状态至少包括：

```text
市场状态；
账本状态；
结构状态；
治理状态。
```

缺一都会导致对象表达不完备。

coverage by shares 的覆盖关系属于 H 层对象身份约束：`long put 名义覆盖 ≥ k ×（short put 义务仓 + 持有正股）`。其中 `k` 及其他 sizing 边界数值属于 P 层 `parameter_slot_candidate`，进入 A6 参数册治理、版本化与回滚；硬执行位置在 Phase 4 constraint stack。

### 6. 账本即身份保持器

账本状态不能被总 PnL 替代。总 PnL 是结果视图，不是对象身份。

### 7. 可复用表达

```text
方法论原则 B1：
复杂策略系统应被建模为持续演化的状态对象，而不是动作清单、指标集合或参数集。

对象身份由母结构不变量定义；对象状态由市场、账本、结构、治理四类状态共同表达。
```

---

## B2 事实 → 诊断 → 候选 → 治理的权限链 `[架]`

### 1. 核心内容

从事实到动作必须经过权限递进链。

```text
事实计算
  ↓
结构表达
  ↓
观察 / proxy
  ↓
诊断
  ↓
候选动作
  ↓
约束裁决
  ↓
执行 / 不执行
  ↓
状态回写
  ↓
审计沉淀
```

### 2. 跳步即越权

```text
fact → action：越权；
proxy → approval：越权；
diagnosis → order：越权；
candidate → execution：越权；
YAML config → governance decision：越权。
```

### 3. 约束声明 vs 约束执行

约束可以在字段层、语义层、文档层声明，但硬执行只能在治理层发生。

```text
constraint declaration ≠ constraint enforcement
```

典型例子：

```text
raw exposure，例如 raw Greeks exposure，可以在 Phase 2 计算；
但 legality / approval / block 必须在 Phase 4 governance 中裁决。
```

H 层 coverage 关系只能在 md 声明并由 Phase 4 constraint stack 硬执行；其 `k` 与其他 P 层边界数值须经 A6 参数治理。Phase 3 可将已治理边界用于 candidate 预过滤，但预过滤不构成治理裁决，optimizer 不得改写 H 关系或直接写入生产值。

### 4. 两类触发

| 触发类型 | 来源 | 权限 | 处理 |
|---|---|---|---|
| 约束违反触发 | H / 硬边界 | 必须响应 | 进入治理 / 修复 / block |
| 状态观测触发 | W / proxy / diagnostic | 可选 | 进入 candidate，不得直接执行 |

存在一类事前经 Phase 4 批准的 playbook 动作，在事前声明的路径状态下可直接执行、事后审计。预授权的成立条件、动作清单与状态声明属于后续 playbook 文档；本条仅声明该权限类别存在及其前提：预授权本身是 Phase 4 事前裁决，不构成 diagnostic → order 越权。

### 5. 状态转移语义

动作不是“下单”，而是状态转移：

```text
x_t —a_t→ x_{t+1}
```

合法动作必须保证：

```text
x_t 是合法状态；
a_t 是合法候选；
a_t 经过 Phase 4 裁决；
x_{t+1} 仍是合法状态；
状态转移后对象身份未漂移。
```

动作的目的是维护结构凸性；凸性保持时，no-action 是合法且优先的输出。no-action 的合法性来自被周期性验证的凸性状态，而不是来自警报缺失。持续 no-action 期间，凸性状态与对象身份审计按周期触发，审计触发不依赖动作发生；验证周期为 `parameter_slot_candidate`。

broker / 清算方强制平仓构成 Phase 权限链的外部覆盖，属于权限链失效模式；其发生强制触发 object identity audit。

### 6. 与证伪法的关系

B2 的每一步都可以被 A2 攻击：

```text
事实是否完整；
proxy 是否篡位；
诊断是否隐含路径预测；
候选是否跳过约束裁决；
执行后是否破坏对象身份；
回写是否遗漏失败状态；
审计是否被执行结果污染。
```

### 7. 可复用表达

```text
方法论原则 B2：
系统从事实到动作必须经过权限递进链。

任何绕过诊断、候选、治理、审计的捷径，都是阶段权限错误。
```

---

## B3 功能迁移与动作语义 `[操]`

### 1. 核心内容

动作不应按动作名称定义，而应按其维护的结构功能定义。

### 2. 对冲 = 风险改形

对冲不是消灭风险，而是把不愿裸露承受的风险改写成愿意承受、能供血、能管理、或在关键时刻更有利的风险形状。

| 层级 | 对象 | 含义 |
|---|---|---|
| A | Delta 对冲 | 线性方向暴露处理 |
| B | Greeks 对冲 | 用 Greeks 改写风险暴露 |
| C | 路径对冲 | 围绕路径形态改写响应 |
| D | 结构对冲 | 维护母结构收益函数与对象身份 |

本体系追求 D 版本，允许用 B / C 作为执行手段，避免 A 版本上位。

### 3. 置换 = 功能接力

置换不是守住某张合约，而是守住结构功能。

五类置换：

```text
同 Greek 置换；
不同 Greeks 间置换；
载体置换；
路径置换；
账本置换。
```

### 4. roll = 功能迁移

roll 不是展期，不是续命，不是 delta 触发器。

roll 的结构目标是：

```text
维护 optionality；
维护 Gamma 中心；
维护凸性（含高阶凸性表现）；
迁移账本关系与功能承担者。
```

### 5. partial monetization = 激活后期的有限兑现与账本 / 风险响应再分配

partial monetization 不是简单止盈或收益最大化动作，而是在反脆弱激活生命周期后期，在不破坏剩余保护与结构身份前提下，对已激活凸性收益进行有限兑现，并完成账本与风险响应再分配。

### 6. 三类动作约束

```text
前提约束：是否有资格进入 candidate；
保持约束：执行过程中不得破坏什么；
后验约束：执行后必须满足什么。
```

### 7. 主动置换 vs 被动演化

路径置换是主动改写响应函数。

```text
carry 阶段自然转入 gamma 激活阶段
```

这是状态演化，不是路径置换。

### 8. 与证伪法的关系

每个动作都必须接受 A2 的反例问题：

```text
如果路径反转，动作是否仍合法？
如果 IV 快速回落，动作是否造成 vega 回吐？
如果流动性消失，动作是否仍可执行？
如果成交不完整，是否进入非法状态？
如果动作后 coverage / funding / identity 被破坏，是否应 block？
```

### 9. 可复用表达

```text
方法论原则 B3：
动态系统中的动作必须按其维护的功能定义。

合法动作不是让某个 proxy 更好看，而是将对象从一个合法状态迁移到另一个合法状态，并维持结构功能与对象身份。
```

---

# C. 工具层操作语言

---

## C1 Greeks 风险语言 `[操]`

### 1. 核心内容

Greeks 是结构路径响应语言，不是结构本体，也不是最终裁决。

Greeks 应当：

```text
独立 display；
独立观察；
独立诊断；
进入 candidate 触发；
进入 Phase 4 作为治理输入；
但不得成为第五模块、母结构 component 或顶层合法性替代物。
```

### 2. 跨层角色

| 层级 | Greeks 身份 | 权限 |
|---|---|---|
| Phase 2 | raw exposure | 事实计算 |
| proxy | by tenor / moneyness / expiry display | 观察 / 报警 |
| Phase 3 | diagnostic | 结构解释 / candidate trigger |
| Phase 4 | legality input | 进入 constraint stack，但不单独裁决 |
| 参数系统 | threshold / equivalence / stress rule | 可治理自由度 |

### 3. Non-netting principle

Greeks 不得跨以下维度简单 scalar netting 后直接裁决：

```text
tenor；
call / put；
leg_type；
side；
moneyness；
expiry；
strike；
lot_id。
```

任何 aggregate Greek metric 必须继承 A5 的四项声明：

```text
aggregation scope；
risk-equivalence rule；
scenario assumption；
allowed usage。
```

### 4. Vega 度量形态六态与 Phase 权限轴

Vega 的 canonical 度量形态基准为六态；六态回答“风险以什么形态被表达”，不回答“该表达拥有什么运行权限”：

| 度量形态 | 方法论含义 | 默认权限标注边界 |
|---|---|---|
| raw | 按原始持仓与风险节点保留的 vega 暴露 | Phase 2 fact |
| tenor | 按期限分段表达的 vega | Phase 2 observation；经解释后可作 Phase 3 input |
| forward-segmented | 按远期区段拆分的 vega | Phase 2 derived observation；经声明后可作 Phase 3 input |
| surface | 按曲面坐标表达的 vega | Phase 2 observation / Phase 3 diagnostic input |
| grid | 按价格—波动率—期限网格表达的 vega | Phase 2 observation / Phase 3 diagnostic input |
| scenario-stressed | 在声明情景下重估的 vega | Phase 3 diagnostic / Phase 4 governance input，不是 decision |

Phase 权限轴与上述六态正交：同一度量形态的具体实例必须另行标注来源 Phase 与允许用途；不得把“六种度量形态”与“Phase 2/3/4 三段权限”合并成同一计数体系。形态的字段化、算法化与 canonical schema 定义留待 B-2 / 下游工程文档，不在 T0 展开。

关键边界：

```text
六态是度量形态枚举；
Phase 是运行权限轴；
形态不自然获得诊断、候选或治理权限；
任何聚合结果仍须遵守 non-netting、aggregation scope、risk-equivalence rule、scenario assumption 与 allowed usage。
```

### 5. 波动率交易四阶

```text
1. Gamma / Vega 同侧；
2. Gamma / Vega 可反转；
3. spot-vol correlation（标的价格与波动率相关性）；
4. vol-of-vol（波动率的波动率）。
```

这四阶是风险语法，不是方向预测。

### 6. Greek → 结构功能映射

C1 的工程化输出可包括两张映射表：

#### 6.1 Greek → 母结构健康度

示例：

| Greek 状态 | 可能说明 | 对应结构功能 |
|---|---|---|
| front short gamma 过度集中 | 短端供血与成本摊薄循环风险上升 | 短端供血与成本摊薄循环 / 生存边界 |
| long-end gamma 钝化 | long wing optionality 下降 | 长端双翼 / roll |
| long vega 不足 | 升波路径保护不足 | 期限错配全维度管理 |
| long-end premium bleed / theta decay cost 过高 | 长端凸性成本不可持续 | 短端供血与成本摊薄循环 / funding coverage relation |

#### 6.2 Greek → 候选动作

示例：

| Greek 诊断 | 候选方向 | 权限 |
|---|---|---|
| V_net_equiv 逼近下限 | 减 short vega / 补 long vega | candidate，不自动执行 |
| Gamma center 偏离 | roll long option | candidate，不自动执行 |
| 降波回吐风险上升 | partial monetization candidate | candidate，需 Phase 4 |
| short-end OTM premium income 不足 | 调整 short funding 节奏 | candidate，需 funding/coverage 审查；不得误写为 Greeks Theta 收入 |

### 7. 与证伪法的关系

C1 需要接受 A2 的 Greeks 证伪：

```text
简单净额是否掩盖风险；
不同 tenor 的 vega 是否被错误相加；
put wing 与 call wing 是否被错误等价；
Greeks dashboard 是否被误用为治理裁决；
Greeks-triggered candidate 是否跳过 Phase 4；
V_net raw 是否被误用为硬批准。
```

### 8. 可复用表达

```text
方法论原则 C1：
Greeks 是结构路径响应语言，应被独立观察、诊断与治理；但 Greeks 不定义结构身份，也不得替代 coverage、funding、object identity 与 Phase 4 constraint stack。

任何 Greek 聚合值在声明聚合范围、等价规则、情景假设与允许用途之前，只能作为粗观察。
```

---

# 附录：横切 × 脊柱关系

每个运行脊柱节点 B1 / B2 / B3，都同时受到全部横切纪律 A1–A8 约束。

以一个 roll 候选为例：

```text
B3：roll 作为功能迁移动作
  同时受：
    A1：不能依赖路径预测作为合法性来源；
    A2：必须接受反例路径、后验约束、身份漂移检查；
    A3：触发源必须标注 H/P/W；
    A4：roll 后是否仍为同一对象；
    A5：不能因为 Greek proxy 好看就批准；
    A6：参数阈值必须已注册、已验证、未越权；
    A7：动作语义必须与 md 一致；
    A8：部署 profile 不能绕过 core 硬边界。
```

这就是“横切 × 脊柱”的含义：

```text
横切纪律不是前置章节，而是每个运行节点的同时约束。
```

---

# 附录｜补充 canonical 对象索引

T2 `00A §5` 是以下 T0 对象的唯一权威定义源。本表仅登记目录归属与权威指针，不在 T1 重复定义。

| 对象 | 主题树归属节点 | 权威指针 |
|---|---|---|
| `H_identity_target` | A4 / B1 | T2 / 00A §5 |
| `P_A`（假设 A：target Beta 长期正期望） | A2 / A3 / A4 | T2 / 00A §5 |
| `P_B`（假设 B：短端供血充分性） | A2 / A3 / A6 | T2 / 00A §5 |
| 低 IV 震荡磨损路径（P_B 反例） | A2 | T2 / 00A §5 |
| margin regime shock | A2 / C1 | T2 / 00A §5 |
| `parameter_slot_candidate` | A6 | T2 / 00A §5 |

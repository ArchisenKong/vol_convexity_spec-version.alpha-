
> 文档性质：Chapter 12–16 trading concepts 总整合方法论主文档  
> 来源模式：文件锁定模式  
> 主依据：Chapter 12 v0.3.1、Chapter 13 v0.3.2、Chapter 14 v0.3.2、Chapter 15 v0.3.1、Chapter 16 v0.3.4 章节包  
> 横向约束：0000、0001、0002、Greeks 管理方法论主文档 v0.1.2-freeze、可复用方法论主题树、12 篇策略方法论文档  
> 当前版本：v0.1.2-freeze  
> 当前用途：v0.1.2-patch 二次复审 PASS 后的 freeze 归档版；可作为下游可衍生性审计的上游方法论边界材料；不得直接生成字段、算法、YAML 或自动交易规则  
> Freeze 状态：v0.1.2-patch 二次复审结论为 PASS，P1/P2 patch 已完整落地，允许恢复 freeze；本文件归档为 v0.1.2-freeze 版  
> 禁止用途：不得直接作为字段冻结稿、算法实现稿、YAML schema、自动交易规则、下单规则、生产风控规则或策略执行手册

---

## 0. 文档定位与版本边界

### 0.1 文档目标

本文档把《Dynamic Hedging / 动态对冲》第 12–16 章已经完成章节包整理并被本轮作为锁定上游的 Chapter 12–16 章节包整合为一份 trading concepts 上游方法论主文档。

本文处理的问题是：

```text
在真实期权交易中，复制、替代、收敛、堆叠、到期、结算、flatness、分段、形态、分布、路径相关、动态对冲、价差交易、波动率下注和最差情景如何共同构成交易概念语言。
```

本文不处理：

```text
字段定义；
算法接口；
YAML schema；
自动交易逻辑；
生产参数；
DTE / moneyness / strike / ratio / roll / rebalance / hedge trigger；
stack trigger；
proxy instrument selection；
convergence trigger；
策略执行手册。
```

### 0.2 主依据章节包与版本锁定

| 章节 | 实际读取包 | 包内文件完整性 | 原始 manifest 采用状态 | 备注 |
|---|---|---:|---|---|
| Chapter 12｜可替代性、收敛、堆叠 | `06_chapter12_full_package_v0.3.1.zip` | 00–12 完整 | v0.3.1 复审通过 | 可进入总整合；非生产依据 |
| Chapter 13｜期权市场的一些细节 | `06_chapter13_full_package_v0.3.2.zip` | 00–12 完整，含 v0.3.1 / v0.3.2 diff | v0.3.2 复审通过 | 实际 README 顶部仍显示 v0.3 / 待审计；本文件采用 revision log、v0.3.2 diff 与复审报告作为状态源，并在遗留复核项保留 metadata 一致性核对 |
| Chapter 14｜分段和形态 | `06_chapter14_full_package_v0.3.2.zip` | 00–12 完整 | v0.3.2 复审通过 | 可进入总整合；非生产依据 |
| Chapter 15｜注意分布 | `06_chapter15_full_package_v0.3.1.zip` | 00–12 完整 | v0.3.1 复审通过 | 可进入总整合；非生产依据 |
| Chapter 16｜期权交易的概念 | `06_chapter16_full_package_v0.3.4.zip` | 00–12 完整，含 v0.3.1–v0.3.4 diff | v0.3.4 复审通过 | CA cards source-faithful 重建后证据链对齐版 |

状态源说明：上述“复审通过”保留原 v0.1.1-freeze 的 manifest 采用口径。v0.1.2-patch 二次复审已确认 P1/P2 patch 完整落地，并允许恢复 freeze。Chapter 13、Chapter 14、Chapter 15 等章节包若存在 README 顶部旧状态，应以 revision log、diff summary 与随归档包锁定的复审报告共同裁决；若后续需要独立验证章节包复审状态，应补充锁定对应复审报告。

主依据读取优先级：

```text
source / evidence layer：01、02、03、04、05、06、07
methodology layer：08
strategy mapping layer：09
audit / revision layer：10、11、12 与复审报告
```

### 0.3 横向约束附件与权限说明

本次读取以下横向约束附件：

| 文件 | 作用类型 | 使用边界 |
|---|---|---|
| `0000_量化结构搭建过程_认识论与证伪法总则 20260523.md` | Project governance reference / Boundary constraint | 只用于认识论、证伪法、Phase 与 H/P/W 权限边界 |
| `0001_Greeks管理_观察与层级设置_v1 20260523.md` | Terminology consistency reference / Boundary constraint | 只用于 Greeks 观察、诊断、display 与治理权限边界 |
| `0002_本轮文档升级裁决说明_v1 20260523.md` | Project governance reference | 只用于 md / YAML 升级顺序与 Phase 2/3/4 禁止混层边界 |
| `Greeks_管理方法论主文档_v0.1.2-freeze.md` | Strategy-system interface reference | 只用于 Greeks 与 Trading Concepts 的接口一致性 |
| `1.可复用方法论主题树_20260606.md` | Terminology consistency reference | 只用于确认本文在方法论体系中的位置、Phase 权限链与工具层定位 |
| `2波动率凸性策略可复用方法论文档集_12篇_20260606.md` | Strategy-system interface reference | 只用于后续映射边界，不倒灌到 source layer |

**总声明：Chapter 12–16 章节包决定 Trading Concepts 的 source content；横向约束文件只决定项目层面的权限边界、术语一致性和后续转译边界。**

横向约束附件不得标注为：

```text
Source claim；
Taleb original evidence；
Chapter 12–16 conclusion；
Production rule support。
```

### 0.4 文件锁定声明

本文只使用本 session 上传并实际读取的附件。不使用：

```text
历史聊天记录；
模型记忆；
未上传旧版本；
未审计章节包；
PDF 原文之外的自由补写；
未经 01/03/06/08/09 支持的策略规则；
字段、算法、YAML 或自动交易逻辑。
```

原 PDF `06_path_shape_distribution_trading_concepts_pages_202-261.pdf` 只作为可选复核来源；本文未基于 PDF 新增未沉淀于章节包的总整合内容。

### 0.5 source / methodology / strategy mapping 分层声明

| 层级 | 来源 | 可做 | 不可做 |
|---|---|---|---|
| Source claim | 01 / 03 / 04 / 05 / 06 / 07 | 保留章节包中的原书结论、风险规则、术语、公式/图表边界 | 不转成策略动作 |
| Derived methodology | 08 | 抽取可复用方法论；标注 Direct / Direct + Derived / Derived | 不伪装成原书原句 |
| Strategy-specific mapping | 09 与横向策略体系接口 | 说明对用户波动率凸性策略的候选上游意义 | 不倒灌为 source claim，不生成字段/规则 |
| Project governance reference | 横向约束文件 | 收紧 Phase、Greeks、proxy、字段/YAML 边界 | 不覆盖原书意思 |

凡本文出现“总整合抽象”，均表示：这是跨 Chapter 12–16 的整合表达，不是原书原句，也不是原书小节标题。

### 0.6 非生产声明

本文不生成也不授权：

```text
DTE；
moneyness；
strike；
ratio；
roll rule；
rebalance rule；
hedge trigger；
stack trigger；
proxy instrument selection；
convergence trigger；
vol bet execution rule；
Gamma flip trigger；
soft/hard Delta switching rule；
path-state classifier；
field/schema/YAML。
```

Greeks、proxy、flatness、segmentation、distribution、worst-case analysis 均为观察语言或方法论约束，不构成单独动作授权。

### 0.7 与 Greeks 管理主文档的关系

Greeks 管理主文档处理 Delta / Gamma / Vega / Theta / Rho / Alpha / higher-order Greeks 的观察、诊断与治理输入边界。Trading Concepts 处理交易概念、市场细节、路径、分布、执行、复制、对冲残差与最差情景。

二者关系：

```text
Greeks 管理：风险响应语言与分层观察约束；
Trading Concepts：交易动作语义、市场机制、路径/分布/执行残差约束；
共同边界：都不得直接授权 hedge / roll / rebalance / stack / convergence action。
```

### 0.8 与波动率凸性策略方法论的关系

本文可作为波动率凸性策略的以下上游输入：

```text
结构诊断候选；
风险显示候选；
报告模块候选；
约束设计候选；
失败模式清单候选；
字段 / 算法 / YAML 设计前的 source boundary。
```

本文不能作为：

```text
具体交易建议；
固定策略参数；
执行手册；
自动化动作批准器；
生产风控规则。
```

### 0.9 v0.1.2-freeze 归档说明

本 freeze 版基于 v0.1.2-patch 二次复审 PASS 后归档。v0.1.2-patch 基于《Greeks 与 Trading Concepts 总一致性审计报告_v0.1》执行最小修订，核心处理项为：

```text
1. 降权未随本轮锁定附件提供的复审 / freeze 状态；
2. 删除未定义的 `C3` 命名空间，改为 non-Greek option-management governance checks；
3. 将内容域与 Phase 4 权限域拆开，避免 namespace 与 governance permission 混层；
4. 将 Greeks 主文档引用统一为 v0.1.2-freeze；
5. 删除未定义的 A/B/C/D 用户体系缩写；
6. 加固 Strategy-specific Derived 不得倒灌为 source claim 的声明；
7. 收紧字段 / 算法 / YAML 入口，明确必须完成下游可衍生性审计后才可继续拆解。
```

本 freeze 版未新增字段、算法、YAML、阈值、参数、交易动作或自动执行规则；也未重写 Chapter 12–16 substantive content。

---

## 1. Chapter 12–16 总体脉络

### 1.1 五章主题定位

| 章节 | source 主题 | trading concepts 中的角色 | 主要 source 依据 |
|---|---|---|---|
| Chapter 12 | 可替代性、收敛、堆叠 | 定义 proxy、替代、stack、convergence 的可行性边界 | CA-12-001–022；RR-12-001–012；M-12-001–009 |
| Chapter 13 | 期权市场细节 | 定义到期、结算、行权、boundary、flatness 的执行残差边界 | CA-13-001–022；RR-13-001–012；M-13-001–009 |
| Chapter 14 | 分段和形态 | 定义局部风险观察、segmentation、shape、dynamic Gamma、payoff-shape map | CA-14-001–031；RR-14-001–014；M-14-001–010 |
| Chapter 15 | 注意分布 | 定义 tail、skew、Vvol、histogram、path-vol dependency、高阶平价的分布语境 | CA-15-001–025；RR-15-001–014；M-15-001–010 |
| Chapter 16 | 期权交易概念 | 定义复制、静态/动态对冲、价差、Vega/Gamma、soft/hard Delta、volatility bet、路径 P/L、最差情景 | CA-16-001–041；RR-16-001–016；M-16-001–012 |

### 1.2 五章的逻辑递进

总整合抽象：Chapter 12–16 构成 trading concepts，不是单章技巧合集。其递进关系为：

```text
Chapter 12：先问“工具之间是否可替代，proxy / stack / convergence 是否成立”；
Chapter 13：再问“真实市场到期、交割、行权、边界、flatness 是否破坏理论等价”；
Chapter 14：进一步问“风险集中在何时、何处、哪个 strike / tenor / state”；
Chapter 15：再问“终点 payoff 之外，分布、路径、skew、Vvol、资产反馈如何改变风险”；
Chapter 16：最后问“复制、对冲、价差、波动率下注、路径 P/L 和最差情景如何被交易概念化”。
```

五章共同把“期权交易”从静态 payoff 和净 Greeks 推向以下共同语言：

```text
结构等价是否成立；
执行流程是否可实现；
残余风险被转移到哪里；
局部风险集中在哪里；
路径和分布如何改变对冲损益；
动态对冲后最差情景如何出现。
```

### 1.3 为什么不是单章技巧合集

单章技巧可以告诉交易员如何看某个问题；Chapter 12–16 的组合给出的是一条完整审计链：

```text
substitutability audit
  ↓
settlement / expiry / boundary audit
  ↓
segmentation / shape / local risk audit
  ↓
distribution / path-vol / parity audit
  ↓
replication / hedge / spread / worst-case audit
```

这条链只定义观察、诊断、映射和约束，不定义生产动作。

---

## 2. Trading Concepts 的核心问题定义

### 2.1 trading concepts 解决什么问题

Trading Concepts 解决的是：在真实市场中，交易概念是否被错误理解为“无残差等价”。它专门约束以下误用：

```text
把 proxy 当成完整替代；
把 stack 当成风险消除；
把 convergence 当成稳定 carry；
把 put-call parity 当成可执行套利；
把 Delta-flat 当成 risk-flat；
把 segmented Greeks 当成完整治理；
把 histogram 当成完整分布语言；
把 volatility bet 当成单一 long/short vol；
把 dynamic hedging 当成风险消灭；
把 premium paid 当成动态对冲者完整风险上限。
```

### 2.2 为什么它不是单纯 Greeks 管理

Greeks 管理关注局部敏感度和风险响应。Trading Concepts 关注 Greeks 之外的交易语义和残差机制：

```text
settlement risk；
assignment risk；
object identity risk；
substitutability risk；
forward / funding channel；
proxy basis risk；
path-order risk；
distribution-shape risk；
transaction-cost risk；
worst-path risk。
```

Delta / Gamma / Vega / Theta 是必要观察语言，但不足以覆盖 trading concepts。

### 2.3 为什么它不是单纯市场方向判断

Chapter 12–16 不支持“预测市场方向后交易”。收敛、carry、skew、volatility bet、Gamma 区间和路径相关都可以形成诊断，但不能单独授权方向性下注。

核心边界：

```text
market view 可以成为观察或候选输入；
不能成为结构合法性、动作批准或自动执行来源。
```

### 2.4 为什么它不是单纯 option payoff 画图

静态 payoff 只描述到期终点损益。Chapter 13–16 反复说明：

```text
到期流程会改变 payoff 可实现性；
flatness 是局部和维度化的；
segmentation 只能显示当前切片；
histogram 隐藏事件顺序；
dynamic hedging P/L 依赖路径；
相同终点和相同总波动率仍可能产生不同对冲损益；
权利金不是动态对冲者完整风险上限。
```

### 2.5 总整合定义

总整合抽象：Trading Concepts 是结构、路径、分布、执行、对冲残差的共同语言。它不批准交易动作，只提供后续字段、算法、参数、YAML 和治理文档必须回答的问题。

---

## 3. 可替代性、proxy 与 residual-risk transformation

### 3.1 Source content

Chapter 12 的主线是：可替代性决定复制、套利、对冲和交割是否成立。弱可替代产品需要按组成部分、期限、交割条件拆分；期权套利需要可套利的风险中性远期市场；收敛、carry、roll-down、Theta 需要分账；堆叠是短期、流动性驱动的临时 proxy hedge，不是风险消除。

主要来源：CA-12-001–022；RR-12-001–012；M-12-001–009。

### 3.2 可替代性与弱可替代性

| 概念 | 方法论含义 | 来源 | 不可支持的更强表达 |
|---|---|---|---|
| 可替代性 | 决定交割、复制、套利是否可行 | CA-12-001/002；RR-12-001；M-12-001 | 不代表可替代产品无风险 |
| 弱可替代性 | 理论等价需要拆成期限、组成部分、交割与融资条件 | CA-12-004/005/007；RR-12-002/003；M-12-002 | 不代表所有 calendar spread 都不能聚合 |
| 风险中性远期市场 | 期权套利可靠性的前置条件 | CA-12-008/009；RR-12-004/005；M-12-003 | 不代表远期不完美时所有期权交易禁止 |

### 3.3 proxy / stacking / netting 的边界

总整合抽象：proxy / stacking / netting 是 residual-risk transformation，不是 risk elimination。

```text
proxy：把目标风险转移到代理工具的 basis / correlation / liquidity / funding / settlement residual；
stacking：用高流动性工具临时压低主风险，同时生成 time decay of hedge quality；
netting：只在指定口径下显示净敞口，不等于完整 risk-neutral。
```

### 3.4 convergence 与 carry / roll-down / theta 的区别

Chapter 12 支持以下分账：

| 项目 | 方法论含义 | 主要来源 | 不可混同 |
|---|---|---|---|
| carry | 持有期间现金流或风险补偿 | CA-12-011/012/015；RR-12-007/009；M-12-004/005 | 不等于稳定收益 |
| convergence | 对期限结构非无偏预测的交易观点 | CA-12-011/013；RR-12-007 | 不等于 theta |
| roll-down | 曲线位置随时间缩短的重估效果 | CA-12-012/014；M-12-004 | 不等于无风险收敛 |
| theta | 期权时间衰减或凸性工具的时间成本 | CA-12-014；RR-12-008 | 不等于 carry 或 convergence |
| premium income | 收取权利金形成的现金收入 | Chapter 12 strategy mapping | 不等于 funding 无风险收入 |

### 3.5 不可支持的更强表达

Chapter 12 不能支持：

```text
proxy instrument selection；
stack trigger；
convergence trigger；
correlation threshold；
VAR threshold；
stacking algorithm；
automatic proxy hedge；
automatic roll / convergence trade；
完整 risk-neutral / curve-neutral / basis-neutral / correlation-neutral / tail-neutral 声明。
```

---

## 4. Market detail、expiry、settlement 与 flatness 边界

### 4.1 Source content

Chapter 13 的主线是：真实市场细节会破坏理论平价、复制、边界和 flatness 的直接可执行性。到期尖锐风险来自行权 / 分配信息时滞、收盘后信息、大持仓对手方、现金/非现金交割差异；市场边界不等于合约 barrier；Delta flat 不等于 Gamma / Vega / full-risk flat；初始 hedge 后 secondary exposure 会由参数变化、凸性、曲线移动和 bleed 重新生成。

主要来源：CA-13-001–022；RR-13-001–012；M-13-001–009。

### 4.2 到期、交割、行权、边界风险

| 风险 | 方法论含义 | 来源 | 不可支持 |
|---|---|---|---|
| expiry / pin risk | 到期附近行权/分配流程产生残余风险 | CA-13-001–004；RR-13-001/002/004；M-13-001 | 具体到期平仓时间 |
| settlement risk | 理论平价需通过 settlement identity check | CA-13-002/003/005；RR-13-003；M-13-002 | conversion / reversal 自动套利 |
| sticky strike / path feedback | 行权价附近持仓与对冲行为可影响路径 | CA-13-007–009；RR-13-005；M-13-004 | 用 OI 或 dealer proxy 直接预测方向 |
| market boundary | 制度边界不同于合约 barrier | CA-13-010–014；RR-13-006–009；M-13-005/006 | boundary breakout / defense 规则 |
| secondary exposure | 初始 hedge 后由参数、曲线、凸性、bleed 生成新风险 | CA-13-019–022；RR-13-012；M-13-008/009 | 阈值化自动 rehedge |

### 4.3 flatness taxonomy 的层级

Chapter 13 v0.3.2 已明确拆分 Greek-flatness 与 non-Greek flatness。为避免未定义命名空间硬化，本版不再使用 `non-Greek option-management` 编号：

```text
C1 Greek-flatness taxonomy
  ├─ Delta-flat
  ├─ Gamma-flat
  ├─ Vega-flat
  ├─ Rho-flat
  └─ higher-order locally flat

non-Greek option-management governance checks
  ├─ scenario-P/L flat
  ├─ settlement-flat
  └─ object-identity flat
```

边界：

```text
C1 Greek-flatness 是 Greeks 风险语言；
non-Greek option-management governance checks 是期权组合管理语义和治理检查；
Phase 4 是权限域，不是内容命名空间；
scenario-P/L flat、settlement-flat、object-identity flat 不得进入 C1 Greeks 字段层级；
任何 flat 都必须说明相对维度、局部范围和产品结构；
上述列表是 Chapter 13 涉及的 Greek-flatness 子集，不是 C1 全部 Greek 类型的完备枚举。Theta、Alpha 是否需要独立 flatness 表达，应在下游可衍生性审计中另行裁决，不得由本列表的缺省状态自动推导。
```

### 4.4 不可混层点

```text
Delta-flat 不等于 Gamma-flat；
Gamma-flat 也只是局部；
Greek-flatness 不等于 settlement-flat；
settlement-flat 不等于 object-identity flat；
scenario-P/L flat 不等于 full-risk flat；
primary exposure 被 hedge 后，secondary exposure 仍会重新生成。
```

---

## 5. Segmentation、shape 与局部风险观察

### 5.1 Source content

Chapter 14 的主线是：复杂期权组合风险不能压缩为单个净 Greek。分段可以按时间切分当前参数风险，并显示当前切片中的局部敏感度及局部 Gamma / convexity 集中，但不能仅凭静态 segmentation 完整显示 convexity evolution、高阶矩、state dependence 或 path dependence；shape report 显示 strike / maturity 上的库存和 payoff 集中；动态 Gamma 形态显示未来局部曲率风险；边界期权需要 price-time payoff-shape worst-case map。

主要来源：CA-14-001–031；RR-14-001–014；M-14-001–010。

### 5.2 分段为什么必要

```text
Greek number answers “local sensitivity 是多少”；
segmentation answers “sensitivity 在哪个期限 / 状态 / 产品结构中”；
shape answers “名义库存、payoff 与局部曲率集中在哪里”；
worst-case payoff-shape map answers “尖锐损失区在哪里”。
```

### 5.3 局部 Gamma / Vega / shape

| 观察语言 | 方法论含义 | 来源 | 边界 |
|---|---|---|---|
| segmented Greeks | 按期限/到期桶显示当前敏感度集中 | CA-14-001/002；RR-14-001/002；M-14-001 | 静态显示，不是治理终点 |
| forward-vol bucket | 用局部 vol shock / 模拟看未来窗口 Vega | CA-14-012/013/014；RR-14-008；M-14-003 | 是 Trading Concepts 的分段观察方法；与 Greeks 主文档的 `forward-segmented Vega` 可建立映射，但在输入、shock、时间段定义和聚合规则完成审计前，不得默认同义或共用字段 |
| strike / maturity shape | 显示头寸与 payoff 集中位置 | CA-14-016–020；RR-14-009/010；M-14-004 | 不是 hedge trigger |
| normalized moneyness / vol-time scaling | 跨期限行权价距离需归一化 | CA-14-023/024；RR-14-011；M-14-007 | 不定义固定缩放规则 |
| dynamic Gamma shape | 显示 time-forward / price-grid 局部 Gamma 风险 | CA-14-025/026；RR-14-012；M-14-008 | 不能完整覆盖路径相关产品 |
| payoff-shape worst-case map | 显示边界 / sharp-risk 大损失区域 | CA-14-029–031；RR-14-013；M-14-010 | 不能直接决定 hedge |

### 5.4 相关工具聚合的严格边界

Chapter 14 的相关工具聚合只能用于诊断显示：

```text
只有在明确设定且可审计的近似完全相关 / 经济转换口径下，相关工具才可放入共同 proxy bucket；
该聚合只用于诊断集中度、Gamma / Vega 来源和风险显示；
不得用于风险等价、净额抵消、生产字段冻结或 Phase 4 单项裁决。
```

本节禁止的是仅凭相关性或经济转换口径，将 proxy bucket 直接升格为 risk-equivalent Greeks。若需要形成 risk-equivalent Greeks，必须另行满足 Greeks 管理主文档规定的等价规则、聚合范围、适用假设、情景集合和禁止用途；本节聚合本身不构成该等价关系的充分依据。

主要来源：CA-14-023；RR-14-014；M-14-006。

### 5.5 不可生产化内容

Chapter 14 不能支持：

```text
bucket 宽度；
grid 参数；
scaling rule；
correlation threshold；
path-state classifier；
shape-based trade；
field schema；
YAML。
```

---

## 6. Distribution、tail、skew 与 path dependence

### 6.1 Source content

Chapter 15 的主线是：期权风险来自分布形态、波动率状态、价格—波动率依赖、事件顺序和资产不对称结构的共同作用。历史直方图或终点分布不足以描述动态对冲者风险；OTM 期权价值不仅来自终点尾部概率，也来自路径上的 implied volatility 行为；高阶买卖权平价是结构一致性审计工具，不是自动套利规则。

主要来源：CA-15-001–025；RR-15-001–014；M-15-001–010。

### 6.2 分布意识为何是 trading concepts 核心

分布在 Chapter 15 中不是普通参数背景，而是决定期权交易形态、路径风险和尾部风险判断的核心语境：

```text
随机波动率影响 OTM / ITM 相对 ATM 的价格；
高波动率状态支配尾部，低波动率状态支配峰部；
skew 体现 price-vol dependency；
histogram 隐藏事件顺序；
不对称资产价格变化会反馈融资能力、信用、稳定性；
做市库存与收取权利金会形成逆向选择和“坏”的分布风险；
厚尾 / Pareto-Levy 模型需先转译为风险解释与复核边界，不能机械上线；
高阶平价需要按产品结构逐项审计。
```

### 6.3 tail / skew / Vvol / histogram

| 主题 | 方法论含义 | 来源 | 不可支持 |
|---|---|---|---|
| Vvol / stochastic volatility | 解释 smile、厚尾、尖峰；应提取风险规则而非机械模型 | CA-15-003/004/007；RR-15-002/004；M-15-001/002 | 固定 Vvol 参数 |
| skew | price-vol dependency，不只是单一统计矩 | CA-15-005/006/010/015；RR-15-003/008；M-15-003 | skew threshold 或交易信号 |
| histogram | 描述经验频率，不显示事件顺序和路径 IV 行为 | CA-15-013/014/022/023；RR-15-007/012；M-15-004/007 | histogram bucket / regime classifier |
| asymmetric asset | 下跌波动率上升、上涨波动率下降较小，并伴随融资/信用反馈 | CA-15-016–019；RR-15-009/010；M-15-005 | 自动资产准入或权重规则 |
| market-making adverse selection | 做市库存与权利金收入需要分布审计，避免把逆向选择、尾部承担或库存偏差误读为中性样本收益 | CA-15-002；RR-15-001；M-15-009 | premium income 稳定化、做市收益无风险化 |
| heavy-tail / Pareto-Levy model adoption boundary | 厚尾模型应先转译为风险解释、尾部审计与模型采用边界 | CA-15-011/012；RR-15-006；M-15-010 | 机械模型上线、固定厚尾参数、生产级分布分类器 |
| higher-order parity | 结构一致性审计，不是执行套利 | CA-15-024/025；RR-15-013/014；M-15-008 | 高阶平价套利触发 |

### 6.4 terminal payoff 与 full path risk 的差异

总整合抽象：terminal payoff 只说明终点价格下的静态损益；full path risk 包括到达路径、IV 路径、价格—波动率依赖、对冲顺序、融资反馈和流动性反馈。

Chapter 15 与 Chapter 16 在此处相互支撑：Chapter 15 说明 histogram / terminal distribution 不足；Chapter 16 说明相同终点和相同总波动率下，动态对冲 P/L 可以不同。

### 6.5 不可生产化内容

Chapter 15 不能支持：

```text
Vvol 参数；
skew 阈值；
histogram bucket；
regime classifier；
jump diffusion 参数；
higher-order parity arbitrage trigger；
long OTM put / call 执行规则；
生产级公式或校验样例。
```

---

## 7. Option trading concepts：复制、对冲、价差与波动率下注

### 7.1 Source content

Chapter 16 的主线是：复制并不等于可操作复制，静态复制并不等于低成本复制，动态对冲并不消除路径相关，价差交易不是单纯做多或做空波动率，而是围绕 Gamma、Vega、Delta、Theta、Rho、交易成本与路径顺序进行风险形状管理。

主要来源：CA-16-001–041；RR-16-001–016；M-16-001–012。

### 7.2 复制、静态复制与动态对冲

| 概念 | 方法论含义 | 来源 | 边界 |
|---|---|---|---|
| 期权复制 | 需先区分自融资复制、实践复制、平价等价、对冲等价、高阶等价 | CA-16-002/003/004；RR-16-001；M-16-001 | 不生成复制组合 |
| 分解 vs 复制 | 分解是诊断语言，复制涉及执行和风险管理 | CA-16-007；RR-16-003；M-16-002 | 不把分解项变成交易动作 |
| 静态复制 | 不连续调整的风险管理策略，受流动性与买卖价差约束 | CA-16-005/009；RR-16-004 | 不推出静态复制优劣 |
| 动态对冲 | 通过再平衡维持最小 Greek 敞口，但不是风险消除 | CA-16-010/011/012；RR-16-005/006；M-16-004/005 | 不生成 hedge frequency |

此处“维持最小 Greek 敞口”仅为 Chapter 16 方法论中的风险管理语义，表示动态对冲试图降低局部 Greek 暴露；它不是数学优化目标函数，不定义最小化算法、目标函数、再平衡频率或执行策略。

### 7.3 价差交易与中性结构

Chapter 16 支持把价差交易理解为 relative Greek-shape management。价差交易可降低部分方差、隔离部分公式风险或实现理论边际，但其模型隔离只能是部分隔离，仍受 Gamma、Vega、Theta、Rho、流动性、路径和交易成本约束。

主要来源：CA-16-013–017；RR-16-007/008；M-16-006/007。

不可支持：

```text
具体 spread ratio；
具体中性结构菜单；
无模型风险套利；
单一 long / short vol 决策。
```

### 7.4 Vega / Gamma、soft Delta / hard Delta、Gamma 反转

| 主题 | 方法论含义 | 来源 | 不可支持 |
|---|---|---|---|
| long/short vol 不充分 | 必须拆成 Gamma、Vega 与其他 Greeks | CA-16-017；RR-16-008；M-16-007 | 单一 vol 指标决策 |
| Gamma 区间与反转 | Gamma 必须按价格区间和反转状态描述 | CA-16-019/020/024；RR-16-009/011；M-16-008 | Gamma bucket 宽度 / flip trigger |
| soft Delta / hard Delta | 对冲工具 identity 不同，尾部后果不同 | CA-16-021/022；RR-16-010；M-16-009 | 自动工具选择规则 |
| Gamma 反转测试 | 再平衡前的风险识别语言 | CA-16-024；RR-16-011 | 自动调仓规则 |

### 7.5 原书小节“波动率下注”

Chapter 16 保留原书小节“波动率下注”。本文件采用以下边界：

```text
“波动率下注”是 Chapter 16 原书小节；
不得直接改写成用户策略体系中的 volatility convexity bet；
一阶 / 二阶 / 三阶 / 四阶波动率交易是原书交易概念分类和风险形状分类；
不得写成严格数学导数阶数，也不得写成交易菜单。
```

来源：CA-16-025–034；RR-16-012；M-16-010。

### 7.6 路径相关、交易频率与最差情景

Chapter 16 支持以下 source-level 边界：

```text
动态对冲使每个期权路径相关；
相同终点和相同总波动率不代表动态对冲损益相同；
提高交易频率可降低路径相关，但增加交易成本；
真实市场通常比理论路径案例更差；
时间分散不足以单独解决期权损益方差；
权利金不是动态对冲者完整风险上限。
```

来源：CA-16-035–041；RR-16-013–016；M-16-005/011/012。

### 7.7 为什么不能直接变成自动交易规则

Chapter 16 给出交易概念语言，不给出生产执行政策。不得由本章推出：

```text
automatic Delta hedge；
automatic roll / rebalance；
Gamma flip trigger；
soft/hard Delta switch；
vol bet execution rule；
hedge frequency；
spread ratio；
worst-case stop-loss；
path simulator parameter。
```

---

## 8. Trading Concepts 的风险规则总账

以下为总整合层核心 risk rules。规则编号 `TC-RR-*` 是本主文档编号；支撑编号来自章节包 CA / RR / M。规则强度按章节包的 Direct rule、Directly supported warning、Derived governance expression、Strategy-specific Derived 保留，不表示生产优先级。

| 规则编号 | 规则表述 | 来源章节 | 支撑 CA / RR / M | 规则强度 | 可作为后续哪类文档的输入 | 不可支持的更强表达 |
|---|---|---|---|---|---|---|
| TC-RR-001 | 替代、复制、hedge、stack 之前必须审计可替代性；弱可替代产品需拆分分析 | Ch12 | CA-12-001–007；RR-12-001/002/003；M-12-001/002 | Direct + Derived | 方法论、审计提示、候选约束 | proxy 自动选择、替代动作授权 |
| TC-RR-002 | 期权套利关系需通过风险中性远期市场、交割、融资、借贷与流动性可行性检查 | Ch12 | CA-12-008/009；RR-12-004/005；M-12-003 | Direct + Derived | 执行约束候选、审计提示 | 自动 arbitrage / synthetic trade |
| TC-RR-003 | carry、convergence、roll-down、Theta、premium income 必须分账 | Ch12 | CA-12-011–015；RR-12-007/008/009；M-12-004/005 | Direct + Derived | 收益来源审计、报告模块候选 | carry trigger、short premium 扩仓规则 |
| TC-RR-004 | 堆叠是临时 proxy hedge；需有效期、残余风险、相关性、波动率、流动性和拆回计划审计 | Ch12 | CA-12-016–020；RR-12-010/011/012；M-12-006/007/008 | Direct + Derived / Strategy-specific Derived | proxy governance、post-action audit | stack trigger、长期 risk-neutral 声明 |
| TC-RR-005 | net exposure、market-neutral、delta-neutral、stacked exposure 均不得解释为完整 risk-neutral | Ch12/Ch13/Ch16 | RR-12-010/011；RR-13-010；RR-16-005/008 | Derived governance expression | 边界约束、审计提示 | 完整风险中性、单项裁决 |
| TC-RR-006 | 非现金结算、行权/分配时滞和到期流程会破坏静态平价可执行性 | Ch13 | CA-13-001–005；RR-13-001/002/003；M-13-001/002 | Direct + Derived | 到期/结算审计、执行约束候选 | 到期自动平仓、conversion/reversal 自动套利 |
| TC-RR-007 | sticky strike / 行权价附近反馈是市场机制观察，不是方向预测器 | Ch13 | CA-13-007–009；RR-13-005；M-13-004 | Direct / Strategy-specific Derived | 微结构诊断、报告候选 | OI/dealer proxy 方向交易信号 |
| TC-RR-008 | 市场边界不等于合约边界；即期边界不等于远期/利率/融资边界 | Ch13 | CA-13-010–014；RR-13-006–009；M-13-005/006 | Direct + Derived | boundary scenario 审计 | boundary breakout / defense 自动规则 |
| TC-RR-009 | flatness 必须维度化；C1 Greek-flatness 与 non-Greek option-management governance checks 不得混层 | Ch13 + 横向约束 | CA-13-015–017；RR-13-010/011；M-13-007 | Direct source claim → Derived governance expression | Greeks 接口、字段前审计 | risk-flat 字段、non-Greek flatness 写入 C1 |
| TC-RR-010 | 初始 hedge 只处理 primary exposure；secondary exposure 会由参数、曲线、凸性和 bleed 动态生成 | Ch13 | CA-13-019–022；RR-13-012；M-13-008/009 | Direct + Derived | post-action monitoring 候选 | 阈值化自动 rehedge |
| TC-RR-011 | 分段可以显示当前切片中的局部敏感度及局部 Gamma / convexity 集中，但不能仅凭静态 segmentation 完整显示 convexity evolution、高阶矩、state dependence 或 path dependence | Ch14 | CA-14-001/002；RR-14-001/002；M-14-001 | Direct + Derived | 风险显示、审计提示 | 分段结果直接治理裁决 |
| TC-RR-012 | 分段/形态方法必须先通过产品适用性检查；美式、路径相关、边界、非普通期权需额外方法 | Ch14 | CA-14-003/009/010/012/013/014/015；RR-14-003/005/006/007；M-14-002/003/005/009 | Direct + Derived | method eligibility check | universal segmentation / universal grid |
| TC-RR-013 | shape report 是 Greek report 的必要补充，用于显示 strike/maturity 库存与 payoff 集中 | Ch14 | CA-14-016–020；RR-14-009/010；M-14-004 | Direct + Derived / Strategy-specific Derived | 报告模块候选、风险显示 | shape-based trade trigger |
| TC-RR-014 | 相关工具聚合只能在明确且可审计的近似完全相关 / 经济转换口径下用于诊断显示 | Ch14 | CA-14-023；RR-14-014；M-14-006 | Direct + Derived | proxy aggregation caveat | 风险等价、净额抵消、Phase 4 单项裁决 |
| TC-RR-015 | dynamic Gamma shape 显示未来局部风险，但不是完整路径相关风险引擎 | Ch14 | CA-14-025–028；RR-14-012；M-14-008/009 | Direct + Derived | 局部风险观察候选 | path-state classifier、自动 hedge |
| TC-RR-016 | boundary / sharp-risk structures 需要 price-time payoff-shape worst-case review | Ch14 | CA-14-029–031；RR-14-013；M-14-010 | Direct + Derived / Strategy-specific Derived | worst-case 报告候选 | 最差情景止损规则 |
| TC-RR-017 | stochastic volatility / Vvol 可解释 smile、厚尾和尖峰，但应先作为风险规则而非机械模型 | Ch15 | CA-15-003/004/007；RR-15-002/004；M-15-001/002 | Direct + Derived | 模型风险审计、报告候选 | Vvol 参数、模型上线 |
| TC-RR-018 | 做市库存与收取权利金需要 adverse-selection distribution audit；不得把逆向选择或尾部承担误读为中性样本收益 | Ch15 | CA-15-002；RR-15-001；M-15-009 | Direct + Derived | 分布审计、做市/库存风险解释、报告候选 | premium income 稳定化、做市收益无风险化、自动库存策略 |
| TC-RR-019 | 厚尾 / Pareto-Levy 模型应先转译为风险解释、尾部审计和模型采用边界，不得因拟合尾部而机械生产化 | Ch15 | CA-15-011/012；RR-15-006；M-15-010 | Direct + Derived | 模型风险审计、分布假设复核、报告候选 | 固定厚尾参数、机械模型上线、生产级 regime classifier |
| TC-RR-020 | skew 是 price-vol dependency，不是单一统计矩或单点信号 | Ch15 | CA-15-005/006/010/015；RR-15-003/008；M-15-003 | Direct + Derived | skew 诊断、报告候选 | skew threshold、put/call 自动切换 |
| TC-RR-021 | histogram 不能作为动态对冲完整风险语言，因为它隐藏路径和事件顺序 | Ch15 | CA-15-013/014/022/023；RR-15-007/012；M-15-004/007 | Direct + Derived | 分布审计、路径报告候选 | histogram bucket、regime classifier |
| TC-RR-022 | 不对称资产需要考虑融资、信用、流动性、避险属性与价格反馈 | Ch15 | CA-15-016–021；RR-15-009/010/011；M-15-005/006 | Direct + Derived | 标的风险解释、报告候选 | 资产权重/准入自动规则 |
| TC-RR-023 | 高阶买卖权平价是结构一致性审计，不是自动套利规则 | Ch15 | CA-15-024/025；RR-15-013/014；M-15-008 | Direct + Derived | 结构一致性审计 | 高阶平价套利触发 |
| TC-RR-024 | 复制必须按等价层级区分；分解不等于可操作复制 | Ch16 | CA-16-002/003/004/007；RR-16-001/003；M-16-001/002 | Direct + Derived | 复制/替代审计 | 具体复制腿、execution pair |
| TC-RR-025 | 静态复制和动态对冲都受流动性、买卖价差、再平衡与路径成本约束 | Ch16 | CA-16-005/009/010/011/012；RR-16-004/005/006；M-16-004/005 | Direct + Derived | hedge governance、post-action audit | hedge frequency、risk elimination |
| TC-RR-026 | long/short volatility 不是充分风险语言，必须拆分 Gamma、Vega、Delta、Theta、路径和成本 | Ch16 | CA-16-017/019/020/024/029–034；RR-16-008/009/011/012；M-16-006/007/008/010 | Direct + Derived | volatility position description candidate | vol bet execution rule、Gamma bucket |
| TC-RR-027 | soft Delta / hard Delta 是 source-level 工具 identity 区分，不是自动工具选择规则 | Ch16 | CA-16-021/022；RR-16-010；M-16-009 | Direct + Derived | hedge identity diagnostic | soft/hard switch algorithm |
| TC-RR-028 | 一阶/二阶/三阶/四阶波动率交易是交易概念分类与风险形状分类，不是严格生产导数阶数 | Ch16 | CA-16-025–034；RR-16-012；M-16-010 | Direct + Derived | 交易概念审计 | 交易菜单、字段阶数 |
| TC-RR-029 | 相同终点和总波动率不代表动态对冲损益相同；路径顺序、Gamma 位置和再平衡成本重要 | Ch16 | CA-16-035–038；RR-16-013/014；M-16-005/011 | Direct + Derived | 回测解释、路径审计 | 路径预测模型、最优频率 |
| TC-RR-030 | 权利金不是动态对冲者完整风险上限；最差情景需独立审计 | Ch16 | CA-16-039–041；RR-16-015/016；M-16-012 | Direct rule | worst-case 报告候选 | 不得把动态对冲最差情景外推为未对冲静态买方损失无限；本规则仅限动态对冲 P/L 与再平衡路径风险，不支持止损规则 |

---

## 9. 对我的波动率凸性策略的可用映射

本节全部为 Strategy-specific Derived，不是 source claim。出现用户体系二级转译或 Phase 2/3/4 时，均只用于说明方法论接口，不得倒灌为 Chapter 12–16 source claim、字段名、schema、YAML key、算法步骤或交易动作。

### 9.1 可用于结构诊断

| Trading concept | 可作为候选输入 | 来源 | 转译强度 | 不可推出 |
|---|---|---|---|---|
| substitutability / proxy audit | 检查保护腿、融资腿、proxy hedge 是否保留原功能 | Ch12 M-12-001/006/007；Ch16 M-16-001 | Strategy-specific Derived | proxy 选择、stack trigger |
| carry / convergence decomposition | 拆分 premium income、theta、roll-down、short skew、liquidity risk | Ch12 M-12-004/005 | Strategy-specific Derived | short premium 扩仓规则 |
| expiry / settlement branch | 检查 short put、long OTM leg 到期、行权、分配、现金/非现金结算风险 | Ch13 M-13-001/002 | Strategy-specific Derived | 到期日前固定平仓规则 |
| segmented / shape risk | 查看短端融资腿、1M/3M/6M long leg 的期限与 strike 集中 | Ch14 M-14-001/004/007/008 | Strategy-specific Derived | bucket、grid、moneyness 参数 |
| path-vol / skew diagnostic | 解释 OTM convexity leg 的价值可能来自路径 IV 行为 | Ch15 M-15-001/003/004 | Strategy-specific Derived | skew 阈值、put-to-call rule |
| dynamic hedge residual | 审计对冲后新增 path-dependence 和 transaction cost | Ch16 M-16-004/005/011/012 | Strategy-specific Derived | hedge frequency、automatic rehedge |

### 9.2 可用于风险显示

后续可作为候选输入的报告语言包括：

```text
substitutability diagnostic；
carry / convergence / theta / premium income 分账；
stack residual-risk map；
expiration / settlement branch note；
Greek-flatness vs non-Greek flatness note；
segmented Greeks display；
strike × maturity shape display；
dynamic Gamma shape note；
Tail / Smile Diagnostic；
Price-Vol Dependency Review；
Path-IV Review；
Gamma interval / reversal note；
Soft-vs-hard Delta note；
Worst-path stress note。
```

上述名称均为后续报告模块候选，不是字段名、schema、YAML、算法接口或生产模块。

### 9.3 可用于约束设计候选

可作为后续约束设计候选的上游问题：

```text
动作是否改变结构功能？
替代工具是否真正可替代？
远期、融资、交割、结算是否支持理论等价？
carry 是否混入 short skew / short tail / short liquidity？
Greek-flat 是否掩盖 settlement / scenario / object identity residual？
shape / segmentation 是否被误用为交易触发器？
histogram 是否掩盖路径顺序？
volatility bet 是否被错误写成单一 long/short vol？
hedge 后是否新增 path-dependence 和 transaction cost？
最差路径下 premium 是否仍被误当作风险上限？
```

这些问题只能进入后续字段 / 算法设计的上游需求或审计提示。

### 9.4 失败模式清单候选

```text
proxy substitution drift；
stack hedge aging；
carry mistaken as convergence；
premium income mistaken as stable funding；
put-call parity without settlement identity；
Delta-flat mistaken as full-risk flat；
segmented Greeks mistaken as governance decision；
correlated proxy bucket mistaken as risk equivalence；
histogram mistaken as path risk language；
skew scalar mistaken as distribution model；
volatility bet mistaken as one-dimensional long/short vol；
dynamic hedge mistaken as risk elimination；
premium mistaken as dynamic hedger max loss。
```

### 9.5 禁止倒灌

不得把本节内容倒灌为：

```text
Taleb 原书结论；
Chapter 12–16 source claim；
固定策略规则；
字段名；
schema；
算法公式；
YAML；
交易动作；
automatic hedge / roll / rebalance / stack / convergence rule。
```

---

## 10. 与 Greeks 管理主文档的接口

### 10.1 接口总原则

Greeks 是观察语言，不是动作授权。Trading Concepts 是交易概念、路径、分布、执行和残余风险语言，也不是动作授权。

```text
Greeks 管理：回答风险响应如何按 tenor / option type / moneyness / expiry / leg / side 展开；
Trading Concepts：回答这种风险响应是否被市场细节、替代性、结算、路径、分布、执行和对冲残差改变。
```

### 10.2 tenor / call / put / moneyness / expiry / segment / distribution 的分层关系

| 维度 | Greeks 管理中的身份 | Trading Concepts 中的补充约束 |
|---|---|---|
| tenor / expiry | Greeks by tenor / expiry 是观察维度 | Ch12 弱可替代、Ch14 segmentation、Ch13 到期流程会改变含义 |
| call / put | option type 维度，不可直接混加 | Ch15 高阶平价与 path-vol、Ch16 spread / parity / Gamma 反转改变风险形状 |
| moneyness / strike | Greeks 局部敏感度和 shape 位置 | Ch14 scaled strike shape、Ch16 Gamma interval、Ch15 OTM tail / smile |
| segment / bucket | 观察与诊断维度 | Ch14 强调 bucket/grid 不能直接生产化 |
| distribution | Greeks 压力情景输入 | Ch15 指出分布是路径/波动率/偏度/反馈语境，不是单一参数 |
| settlement / object identity | 不属于 C1 Greeks 字段 | Ch13 属于 non-Greek option-management governance checks，进入 Phase 4 时只能作为 governance input |

### 10.3 C1 Greek-flatness 与 non-Greek option-management governance checks

C1 可以表达：

```text
Delta-flat；
Gamma-flat；
Vega-flat；
Rho-flat；
higher-order locally flat。
```

non-Greek option-management governance checks（内容域；进入 Phase 4 时仅作为治理检查输入）：

```text
scenario-P/L flat；
settlement-flat；
object-identity flat。
```

边界：

```text
C1 Greek-flatness 不得承诺 settlement-flat；
settlement-flat 不得写入 C1 Greek 字段层级；
object-identity flat 属于治理问题；
scenario-P/L flat 需要情景损益形态，不是单个 Greek。
```

### 10.4 为什么不能简单把 Greeks 净额相加后作为交易决策

来源链：

```text
Chapter 13：Delta flat 不等于 Gamma / Vega flat；
Chapter 14：分段和 shape 显示风险集中位置，单一净值会掩盖局部风险；
Chapter 15：分布、skew、path-vol 会改变同一 Greek 的风险含义；
Chapter 16：long/short vol 不充分，Gamma / Vega / soft-hard Delta / path / cost 必须拆开。
```

因此：

```text
net Greek = observation summary；
不是 object identity；
不是 settlement check；
不是 path risk check；
不是 distribution check；
不是 action approval。
```

### 10.5 Trading Concepts 也不能绕过 Greeks 管理直接授权动作

Trading Concepts 可以指出 proxy、settlement、path、distribution、worst-case 的问题，但不能绕过 Greeks 管理主文档直接生成 hedge / roll / rebalance。

任何动作候选的形成，必须基于：

```text
Greeks observation completeness；
Trading Concepts residual-risk audit。
```

任何候选在获批并进入执行前，必须通过：

```text
Phase 4 governance decision。
```

动作执行后，必须进入：

```text
post-action legality / residual-risk / state verification。
```

标准生命周期为：

```text
Phase 2｜raw observation
  ↓
Phase 3｜diagnostic / scenario analysis / candidate formation
  ↓
Phase 4｜governance decision / legality check / execution constraint
  ↓
Execution｜approved action execution
  ↓
Post-action｜legality / residual-risk / state verification
```

---

## 11. 不可越界清单

### 11.1 不得从本文档直接推出

```text
具体 DTE；
具体 moneyness；
具体 strike；
具体 ratio；
具体 roll rule；
具体 rebalance rule；
具体 hedge trigger；
具体 stack trigger；
具体 convergence trigger；
具体 proxy instrument selection；
具体 vol bet direction；
具体 hedge frequency；
具体 stop-loss / take-profit；
具体 path-state classifier。
```

### 11.2 不得生产化的内容

```text
substitutability score；
forward-market eligibility score；
carry / convergence automatic decomposition engine；
flatness schema；
bucket width；
grid parameter；
vol-time scaling rule；
correlation threshold；
Vvol parameter；
skew threshold；
histogram bucket；
regime classifier；
Gamma flip trigger；
soft/hard Delta switch；
worst-case stop-loss。
```

### 11.3 不得写成字段 / 算法 / YAML 的内容

本文中出现的以下表达均为候选观察或审计提示，不是字段名或 YAML key：

```text
substitutability diagnostic；
stack residual-risk map；
settlement identity check；
Greek-flatness taxonomy；
non-Greek flatness checks；
segmented Greeks report；
strike/maturity shape heatmap；
dynamic Gamma shape；
Tail / Smile Diagnostic；
Price-Vol Dependency Review；
Path-IV Review；
Gamma interval / reversal note；
Soft-vs-hard Delta note；
Worst-path stress note。
```

### 11.4 进入 v1.0 / 字段 / 算法 / YAML 前必须补充

```text
1. 回看 PDF 原图复核所有表格数值、图形标签、公式对象、风险下降比例、矩阵 / VAR / 高阶平价细节；
2. 单独审计 Chapter 13 README metadata 与 v0.3.2 状态源一致性；
3. 对所有报告模块候选另行定义字段名、单位、数据源、样本窗口、复核状态、权限层级；
4. 对所有算法候选另行定义输入、输出、假设、约束、失败条件；
5. 对所有 YAML 候选另行完成 md ↔ YAML 映射审计；
6. 对任何自动动作候选另行通过 Phase 4 governance 文档审计。
```

---

## 12. Cross-Chapter Source Map

| 总整合主题 | 支撑章节 | 支撑 CA 编号 | 支撑 RR 编号 | 支撑 M 编号 | 转译强度 | 是否涉及横向约束 | 可用于后续哪类文档 | 不可支持的更强表达 |
|---|---|---|---|---|---|---|---|---|
| substitutability / proxy / replacement | Ch12 / Ch16 | CA-12-001–009；CA-16-002–004 | RR-12-001–005；RR-16-001 | M-12-001–003；M-16-001 | Direct + Derived | A5 proxy governance | 方法论、审计提示 | proxy instrument selection |
| carry / convergence / roll-down / theta 分账 | Ch12 | CA-12-011–015 | RR-12-007–009 | M-12-004/005 | Direct + Derived | Phase 边界 | 收益来源审计 | carry trigger |
| stacking as temporary proxy hedge | Ch12 | CA-12-016–020 | RR-12-010–012 | M-12-006–008 | Direct + Derived / Strategy-specific Derived | A5 / Phase 4 | post-action audit | stack trigger / risk-neutral |
| expiry / settlement / put-call parity execution | Ch13 | CA-13-001–006 | RR-13-001–004 | M-13-001–003 | Direct + Derived | Phase 4 boundary | 执行约束候选 | conversion/reversal 自动套利 |
| boundary / spot-forward-rate mismatch | Ch13 | CA-13-010–014 | RR-13-006–009 | M-13-005/006 | Direct + Derived | Boundary constraint | boundary scenario audit | boundary trade |
| flatness taxonomy | Ch13 + Greeks 主文档 | CA-13-015–017 | RR-13-010/011 | M-13-007 | Direct source claim + Project governance reference | 是：Greeks C1 / non-Greek option-management governance / Phase 4 | Greeks interface、字段前审计 | risk-flat / settlement-flat 写入 C1 |
| segmentation and shape | Ch14 | CA-14-001–020 | RR-14-001–010 | M-14-001–005 | Direct + Derived | C1 / non-Greek option-management interface | 风险显示、报告候选 | bucket/grid/schema |
| proxy aggregation caveat | Ch14 | CA-14-023 | RR-14-014 | M-14-006 | Direct + Derived | A5 proxy governance | proxy display caveat | 风险等价、净额抵消 |
| dynamic Gamma and payoff-shape worst-case | Ch14 / Ch16 | CA-14-025–031；CA-16-019/020/024/041 | RR-14-012/013；RR-16-009/011/016 | M-14-008–010；M-16-008/012 | Direct + Derived / Strategy-specific Derived | Phase 4 | worst-case 报告候选 | Gamma flip trigger / stop-loss |
| distribution / tail / Vvol / skew | Ch15 | CA-15-001/003–010/013–015 | RR-15-002–005/007/008 | M-15-001–004 | Direct + Derived | Strategy-system interface | 分布审计、报告候选 | Vvol/skew threshold |
| market-making adverse-selection distribution audit | Ch15 | CA-15-002 | RR-15-001 | M-15-009 | Direct + Derived | Strategy-system interface | 做市/库存分布审计、报告候选 | premium income 稳定化、做市收益无风险化 |
| heavy-tail / Pareto-Levy model adoption boundary | Ch15 | CA-15-011/012 | RR-15-006 | M-15-010 | Direct + Derived | Strategy-system interface | 模型风险审计、尾部解释边界 | 机械模型上线、固定厚尾参数 |
| asymmetric assets / feedback | Ch15 | CA-15-016–021 | RR-15-009–011 | M-15-005/006 | Direct + Derived | Strategy-system interface | 标的风险解释 | 资产准入规则 |
| higher-order parity | Ch15 / Ch16 | CA-15-024/025；CA-16-033 | RR-15-013/014 | M-15-008 | Direct + Derived | Boundary constraint | 结构一致性审计 | 平价套利执行 |
| replication / static / dynamic hedge | Ch16 | CA-16-002–012 | RR-16-001–006 | M-16-001–005 | Direct + Derived | Phase 4 boundary | hedge governance | hedge frequency / risk elimination |
| spread and volatility bet language | Ch16 | CA-16-013–034 | RR-16-007–012 | M-16-006–010 | Direct + Derived | C1 / non-Greek option-management / strategy interface | 交易概念审计 | vol bet execution rule |
| path dependence / cost / worst case | Ch16 / Ch15 | CA-16-035–041；CA-15-013–015 | RR-16-013–016；RR-15-007/008 | M-16-005/011/012；M-15-004 | Direct + Derived | Phase 4 / 0000 path constraint | 回测解释、worst-path stress | path classifier / stop-loss |
| Phase 2/3/4 权限边界 | 横向约束文件 | 不适用 | 不适用 | 不适用 | Project governance reference | 是 | 字段/算法/YAML 前置边界 | source claim |
| Greeks observation boundary | Greeks 主文档 / 0001 | 不适用 | 不适用 | 不适用 | Project governance reference | 是 | Greeks-Trading Concepts 接口 | Taleb original evidence |

---

## 13. 遗留复核项

### 13.1 Chapter 12 遗留复核项

```text
1. p.186：弱可替代产品日历价差期权组合需拆分分析的原文措辞；
2. p.188：期权套利需要风险中性远期市场的原文措辞；
3. 表 12.1 产品分类字段；
4. 表 12.4 欧洲美元相关性矩阵；
5. 表 12.5–12.8 仓位、VAR、风险下降比例；
6. p.190 收敛计算文字和公式性表达；
7. p.193–p.195 堆叠表格风险下降比较与 residual risk 说明；
8. p.196 组合资产 / 指数复制中的代理执行路径。
```

### 13.2 Chapter 13 遗留复核项

```text
1. README metadata 顶部仍显示 v0.3 / 待审计，与 v0.3.2 revision log、diff summary、复审报告存在归档张力；
2. p.197：put-call parity 对非现金结算场内期权不成立的风险管理规则原文；
3. p.199：sticky strike 风险管理规则原文；
4. p.200：图 13.1 与 p u = (1-p)d 公式；
5. p.200：即期 / 远期 / 利率差关系式；
6. p.201：汇率区间不等于欧式期权无瑕边界的风险管理规则原文；
7. p.201–p.202：EMS 案例中的机构、角色和报价细节；
8. 二元期权“难以真正 flat”的原文边界。
```

### 13.3 Chapter 14 遗留复核项

```text
1. 表 14.1：Delta、Gamma、Vega、Rho1、Rho2 数值与单位；
2. p.204：远期汇率公式与即期 Delta / 远期 Delta 折现关系；
3. p.204：Rho1 / Rho2 的计算方向、利率币种、融资扣减；
4. 表 14.2：远期互换分段数值与列标题；
5. p.208：美式期权 Omega / 实际到期时间原文术语；
6. 表 14.5：缩放行权价形态标准差列和数值；
7. 表 14.6：动态 Gamma 形态数值和例子；
8. 图 14.1：回报形态轴、区域和标签；
9. p.208：相关工具聚合的强前提和用途边界原文语气。
```

### 13.4 Chapter 15 遗留复核项

```text
1. 表 15.1：表头、价格列、隐含波动率列和数值；
2. p.211：做市导致“坏”的分布与逆向选择的短引文；
3. p.214：Vvol 难以估计，应得到规则而不是模型框架的短引文；
4. p.215–p.216：高波动率支配尾部、低波动率支配峰部的短引文；
5. p.215：混合布朗过程脚注公式；
6. p.218：偏度公式；
7. p.219：Pareto-Levy 特征函数；
8. 表 15.2：不对称资产两体系单元格；
9. 表 15.3：获利场景和速度/方向/状态拆分；
10. p.224–p.226：高阶买卖权平价各产品结构；
11. Omega 概念；
12. KO/KI、二元、美式二元、彩虹、复合期权平价子项。
```

### 13.5 Chapter 16 遗留复核项

```text
1. 图 16.1：复制层级标签；
2. 图 16.2：状态节点、时间标签和箭头方向；
3. p.228：复制与分解的区别，以及“复制大多不具备可操作性”的短引文；
4. p.228：希腊字列表、Rho1/Rho2、correlation delta 等；
5. p.229：动态对冲定义及“使每个期权变得路径相关”的短引文；
6. p.232：soft/hard Delta 数值例子；
7. p.238：交易频率与成本权衡的短引文；
8. 表 16.1：Vega/Gamma 方向、A/B 期权说明和单元格符号；
9. 图 16.3–16.5：曲线和坐标标签；
10. 图 16.6：8 条路径、最高点和终点标签；
11. 表 16.2：动态对冲损益分布数值；
12. 表 16.3：风险反转损益分布数值；
13. 表 16.4：最差情景损益和 Delta 数值；
14. p.231：多/空波动率不是充分风险管理语言的短引文；
15. p.239–p.240：权利金不是动态对冲者完整风险上限的最差情景边界。
```

### 13.6 横向约束一致性复核项

```text
1. 本文 Phase 2/3/4 表述需由后续审计复核是否与 0000、0002、主题树完全一致；
2. C1 Greek-flatness 与 non-Greek option-management governance checks 的接口需与 Greeks 主文档 v0.1.2-freeze 复核；
3. proxy governance 表述需与主题树 A5 和 12 篇策略方法论文档一致；
4. Strategy-specific Derived 内容不得进入 source layer；
5. 候选报告模块不得直接复制为字段名、YAML key 或生产接口。
```

### 13.7 v1.0 前必须回看 PDF 原图的项目

```text
所有表格数值；
所有图形标签；
所有公式对象；
风险下降比例；
相关性矩阵；
VAR；
远期 / 利率公式；
Rho1 / Rho2；
偏度公式；
Pareto-Levy 特征函数；
高阶买卖权平价；
soft/hard Delta 数值例子；
动态对冲损益表；
最差情景表。
```

### 13.8 进入字段 / 算法 / YAML 前必须另行审计

```text
字段命名审计；
字段单位与数据源审计；
字段权限层级审计；
算法输入输出审计；
算法假设与失效条件审计；
参数注册表审计；
YAML 与 md 映射审计；
automation 权限审计；
post-action audit trail 审计。
```

---

## 14. v0.1.2-freeze 结论

### 14.1 可以作为哪些后续文档的上游

完成本轮 patch 复审，并通过下游可衍生性审计后，本文可以作为以下文档的上游材料：

```text
后续复审报告 / 工程化前置审计报告；
字段候选拆解文档；
算法候选拆解文档；
报告模块候选文档；
风险规则候选总账；
Phase 3 diagnostic 候选需求；
Phase 4 governance input 候选需求；
YAML 候选映射前的 source boundary 文档。
```

### 14.2 不能作为哪些生产环节依据

本文不能作为：

```text
生产字段冻结稿；
算法实现稿；
YAML schema；
自动交易规则；
自动 hedge / roll / rebalance / stack / convergence 规则；
参数取值依据；
下单逻辑；
止损 / 止盈规则；
实盘风控阈值。
```

### 14.3 与 Greeks 主文档、参数系统、策略方法论的关系

```text
Greeks 主文档：提供风险响应观察语言；
Trading Concepts 主文档：提供交易概念、市场细节、路径/分布/执行残差语言；
参数系统：后续若使用本文候选约束，必须另行注册参数、权限、默认值、profile 边界；
策略方法论：可使用本文作为 strategy-specific mapping 的上游边界，不得倒灌为 source claim。
```

### 14.4 后续使用建议

本文件为 v0.1.2-freeze 归档稿。后续使用边界为：

```text
1. 字段候选拆解：完成下游可衍生性审计后，可以使用本文作为 source boundary 与候选维度来源，但不得直接冻结字段；
2. 算法候选拆解：完成下游可衍生性审计后，可以使用本文作为方法论边界与风险规则来源，但不得直接生成算法输入、输出、目标函数或执行步骤；
3. 报告模块候选：完成下游可衍生性审计后，可以使用本文作为报告主题来源，但不得直接生成生产字段或 dashboard schema；
4. YAML 候选映射：必须在字段 / 算法文档另行审计通过后再做 md ↔ YAML 映射；
5. PDF 原图复核：凡涉及表格数值、图形标签、公式对象、矩阵 / VAR / 高阶平价、风险下降比例、soft / hard Delta 数值与最差情景表，进入 v1.0 或工程实现前必须回看原 PDF 原图；
6. 自动交易动作：本文不授权任何 hedge / roll / rebalance / stack / convergence / Gamma flip / vol bet execution action。
```

归档裁决：

```text
Trading Concepts 方法论主文档_v0.1.2-freeze：可作为 Chapter 12–16 Trading Concepts 总整合的上游方法论 freeze 版；可进入下游可衍生性审计；不可作为字段、算法、YAML、生产参数或自动交易规则。
```

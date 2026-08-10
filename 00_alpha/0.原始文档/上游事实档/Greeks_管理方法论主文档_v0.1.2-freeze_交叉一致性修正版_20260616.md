
> 文档性质：Chapter 07–11 Greeks 核心内容统一整理稿  
> 来源模式：文件锁定模式  
> 上游范围：《动态对冲》第 7–11 章 v0.3.1 章节包、用户现有方法论文件；复审报告作为原始 manifest 状态源，具体状态以随归档包锁定的复审材料为准  
> 当前状态：方法论主文档 v0.1.2-freeze；v0.1.2-patch 二次复审 PASS 后归档；可作为后续下游可衍生性审计的上游方法论 freeze 版  
> 后续用途边界：可进入下游可衍生性审计；在下游可衍生性审计通过前，不得直接进入字段、算法或 YAML 生产拆解  
> 禁止用途：不得直接作为字段冻结稿、算法实现稿、YAML schema、自动交易规则、下单规则或生产风控规则

---

## 0. Input Manifest 与版本锁定

### 0.1 本次实际读取的文件

#### A. Chapter 07–11 v0.3.1 章节包

本次读取并解压以下章节包。文件名与提示词中的完整包名略有差异，但包内文件、版本记录和 diff summary 均表明其为 v0.3.1 章节包或 v0.3.1 最小修订包。

| 章节 | 实际读取 zip | 包内核心文件 | 原始 manifest 采用状态 |
|---|---|---|---|
| Chapter 07 Delta | `05_chapter07_delta.zip` | `00–12_chapter07_delta_*.md` | v0.3.1；复审通过 |
| Chapter 08 Gamma | `05_chapter08_gamma.zip` | `00–12_chapter08_gamma_*.md` | v0.3.1；复审通过 |
| Chapter 09 Vega | `05_chapter09_vega.zip` | `00–12_chapter09_vega_*.md` | v0.3.1；有条件通过；README 顶部元数据有 P2 一致性问题 |
| Chapter 10 Theta / Rho / Alpha | `05_chapter10_theta_rho_alpha.zip` | `00–12_chapter10_theta_rho_alpha_*.md` | v0.3.1；复审通过 |
| Chapter 11 Greeks Performance | `05_chapter11_greeks_performance.zip` | `00–12_chapter11_greeks_performance_*.md` | v0.3.1；复审通过 |

状态源裁决：Chapter 09 Vega 包内 README 顶部旧状态不作为总整合状态依据；本主文档采用 Chapter 09 revision log、diff summary 与 v0.3.1 复审报告作为版本状态源。

每个章节包中优先读取：

```text
01_source_reconstruction
03_conclusion_argument_cards
06_risk_rules_ledger
07_uncertainty_review_log
08_methodology_extraction
09_strategy_mapping
11_revision_log
12_diff_summary
```

第二优先级读取：

```text
00_readme
02_page_index
04_formula_figure_table_register
05_terms_glossary
10_audit_checklist
```

#### B. Chapter 07–11 复审报告（原始 manifest 声明；本次 patch 未重新锁定）

| 章节 | 实际读取文件 | 复审结论 |
|---|---|---|
| Ch07 Delta | `chapter07_delta_v0.3.1_reaudit_report_20260607.md` | 通过；可进入 Greeks 总整合；公式 / 数值生产复核保留 |
| Ch08 Gamma | `chapter08_gamma_v0.3.1_reaudit_report_20260607.md` | 通过；不可进入字段 / 算法 / YAML / 自动规则 |
| Ch09 Vega | `chapter09_vega_v0.3.1_reaudit_report_20260607.md` | 有条件通过；README 顶部元数据一致性 P2 问题保留 |
| Ch10 Theta / Rho / Alpha | `chapter10_theta_rho_alpha_v0.3.1_reaudit_report_20260607.md` | 通过；CA Cards source / methodology 分层边界已加固 |
| Ch11 Greeks Performance | `chapter11_greeks_performance_v0.3.1_reaudit_report_20260607.md` | 通过；可作为 Greeks 总整合正式上游输入 |

状态源说明：上述复审报告条目保留原始主文档的 manifest 声明。v0.1.2-patch 二次复审已确认 P1/P2 patch 完整落地，并允许恢复 freeze；若后续需要独立验证 Chapter 07–11 章节包复审状态，应随归档包一并锁定对应复审报告。

#### C. 用户现有方法论文件

| 文件 | 用途 | 使用边界 |
|---|---|---|
| `1.可复用方法论主题树_20260606.md` | 体系嵌入；确认 C1 Greeks 风险语言、Phase 权限链、工具层定位 | 不覆盖 Taleb 章节包 source 结论 |
| `2波动率凸性策略可复用方法论文档集_12篇_20260606.md` | 体系嵌入；确认 raw Greeks、proxy Greeks、diagnostic Greeks、risk-equivalent Greeks、scenario-stressed Greeks、governance input 的权限 | 不生成生产字段、阈值、算法或 YAML |
| `0000_量化结构搭建过程_认识论与证伪法总则 20260523.md` | Phase / H-P-W / F(X) 权限背景校准 | 只用于边界校准 |
| `0001_Greeks管理_观察与层级设置_v1 20260523.md` | Greeks 观察、display、诊断、治理边界校准 | 不替代 Ch07–11 source evidence |
| `0002_本轮文档升级裁决说明_v1  20260523.md` | 本轮 md / YAML 升级顺序与禁止事项校准 | 不冻结本主文档中的候选字段 |

### 0.2 未读取 / 未使用的内容

本次总整合未使用以下内容作为正文依据：

```text
历史聊天记录；
此前 session 中的记忆；
未上传的旧版本文件；
v0.3 初稿或旧审计报告覆盖 v0.3.1 内容；
未经章节包、复审报告或用户方法论文件支持的策略规则；
未审计的字段、算法、YAML、自动交易规则。
```

`0104_推进Workflow路线图*.md` 本次未出现在实际上传文件中，故未作为直接依据。Phase 权限边界使用本次上传的主题树、12 篇方法论文档、0000、0001、0002 进行校准。

### 0.3 版本锁定裁决

1. 本文内容层仍以 v0.3.1 章节包为 Chapter 07–11 的上游输入；复审报告若未随归档包重新上传并锁定，只能作为原始 manifest 声明，不作为本 freeze 的独立状态证据。
2. Chapter 09 Vega 的 README 顶部旧元数据不作为最终状态依据；本主文档以 Chapter 09 revision log 与 diff summary 作为内容状态线索。若后续补充 v0.3.1 复审报告，可恢复“有条件通过；README 元数据 P2 保留”的正式状态表述。
3. 本文中的 `Direct / Derived / Strategy-specific Derived` 表示方法论转译强度，不表示生产实现优先级。
4. 本文中的 `Layer 1–4` 表示证据使用层；`Phase 2–4` 表示运行权限层。两者不是同一轴，不得混用。
5. 凡未能在 CA / RR / M 中明确定位的结论，不伪造编号；统一标注为“需复核”。

### 0.4 v0.1.2-freeze 归档说明

本 freeze 版基于 v0.1.2-patch 二次复审 PASS 后归档。v0.1.2-patch 已完成《Greeks 与 Trading Concepts 总一致性审计报告_v0.1》中的 P1/P2 最小修订：降权未随本轮锁定附件提供的复审 / freeze 状态，统一版本状态口径，强化 strategy-specific derived 与 source claim 的隔离，收紧进入字段 / 算法 / YAML 的前置条件，并补充 risk-equivalent Greeks 的边界定义。本文未新增字段、算法、YAML、阈值、shock、grid、weight 或交易动作规则。

本版为 v0.1.2-freeze 归档稿。后续可以进入下游可衍生性审计；在下游可衍生性审计通过前，不得直接生成字段、算法、YAML、生产参数或自动交易规则。

---

## 1. 文档目的、适用范围与禁用范围

### 1.1 本文档是什么

本文档是 Chapter 07–11 的 Greeks 管理方法论总整合，目标是把 Delta、Gamma、Vega、Theta、Rho、Alpha 与 Higher-order Greeks 统一成一套可审计的风险观察语言。它服务于后续字段、算法、YAML 与自动化治理设计，但处在更上游。

本文档回答以下问题：

1. 真实期权组合管理中，Greeks 为什么不能作为静态净额使用；
2. Delta / Gamma / Vega / Theta / Rho / Alpha 分别管理什么风险语言；
3. Greeks 如何随价格、时间、波动率、期限、曲面、执行路径、离散再平衡、到期附近与事件状态漂移；
4. 哪些风险可由单个 Greek 初步观察，哪些必须进入组合情景或 stress test；
5. 哪些 source rule 可直接进入方法论，哪些只能成为字段 / 算法 / YAML 的候选观察维度；
6. Greeks 在用户波动率凸性策略中承担什么角色；
7. Greeks 的禁止用途。

### 1.2 本文档的适用范围

本文适用于 option-centric、路径响应型、波动率凸性策略系统中的 Greeks 观察、诊断与治理输入设计。适用层级为：

```text
Layer 1｜Source Rule：原书直接支持的规则、观察、案例、公式、图表或风险提示；
Layer 2｜Methodology Translation：从原书规则抽取出的 Greeks 管理方法论表达；
Layer 3｜Strategy Mapping：映射到用户波动率凸性策略体系中的观察维度、诊断维度或治理输入；
Layer 4｜Future Engineering Candidate：后续字段、算法、YAML、自动化治理可能使用的候选维度。
```

### 1.3 本文档不处理什么

本文不处理以下事项：

```text
生产字段定义；
算法接口设计；
YAML schema；
固定 threshold；
固定 shock size；
固定 grid；
固定期限权重；
自动 hedge / roll / rebalance / monetization / replacement rule；
具体下单逻辑；
某个策略腿的固定 DTE / moneyness / 仓位比例；
生产级公式复核；
表格数值复核；
图形坐标复核。
```

### 1.4 层级禁令

| 禁令 | 含义 |
|---|---|
| Source rule 不得生产化 | 原书规则只能作为 source evidence，不得直接写成字段、算法、YAML 或下单规则 |
| CA Cards 第 8 节不得升格 | 后续可转译方向只作为候选索引，不作为原书 source evidence |
| Methodology translation 不得越权 | 方法论表达不能自动变成交易动作或治理裁决 |
| Strategy mapping 不得直接执行 | 策略映射只说明可观察、可诊断、可提交治理输入，不授权 hedge / roll / rebalance |
| Future candidate 不得冻结 | 候选观察维度不能写成 production schema |

---

## 2. 总原则：Greeks 是风险观察语言，不是治理裁决器

### 2.1 核心结论

Greeks 的合法身份是：

```text
观察语言；
诊断语言；
风险响应语言；
治理输入；
审计对象。
```

Greeks 的非法身份是：

```text
结构定义器；
最终裁决器；
单项动作批准器；
生产参数真值；
跨期限 / 跨曲面 / 跨工具的无条件净额。
```

用户方法论文件已经把 Greeks 定位为 C1 工具层操作语言：Greeks raw exposure 属于 Phase 2，Greeks Observation / diagnostics / risk-equivalent / scenario-stressed input 属于 Phase 3，Greeks-related legality 只能作为 Phase 4 governance input。Chapter 07–11 给出的 source 规则与这一定位一致。

### 2.2 Delta-neutral 不等于 risk-neutral

Delta-neutral 只能说明某一口径、某一状态、某一价格点附近的一阶敏感度被压低。它不能说明：

```text
Gamma 中性；
Vega 中性；
Theta 安全；
Rho 分账完整；
skew / surface 风险可忽略；
到期附近风险平滑；
事件状态矩阵安全；
执行路径可复制；
post-hedge payoff shape 守约。
```

依据：Ch07 CA-07-010 / RR-07-005 / M-07-003；Ch08 CA-08-024 / RR-08-013；Ch11 CA-11-005 / RR-11-001。

### 2.3 Net Greek = 0 不等于风险中性

任何净 Greek 为零，都必须追问以下前置条件：

```text
聚合范围是什么；
是否跨 tenor；
是否跨 strike / moneyness；
是否跨 call / put；
是否跨 long / short；
是否跨工具、结算口径、计价货币；
是否跨 volatility surface coordinate；
是否声明 shock size、shock direction、vol scenario、skew scenario、rate / basis scenario；
是否经 scenario-stressed Greeks 或 state matrix 检查。
```

无上述声明的 net Greek 只能作为 rough observation。

依据：Ch07 CA-07-011–016 / RR-07-006；Ch08 CA-08-009–011 / RR-08-005；Ch09 CA-09-008 / RR-09-005 / M-09-002；Ch10 CA-10-010 / RR-10-006；Ch11 CA-11-021 / RR-11-010。

### 2.3.1 risk-equivalent Greeks 的边界定义

`risk-equivalent Greeks` 不是 raw Greeks，也不是自动治理裁决。它只表示：在明确声明等价规则、聚合范围、适用假设、情景集合和禁止用途之后，把不同腿、期限、moneyness、option type 或工具之间的 Greeks 暂时转译为可比较的诊断口径。

其合法用途是 Phase 3 诊断或 Phase 4 governance input；其非法用途是替代 raw exposure、替代 scenario-stressed Greeks、绕过 constraint stack，或直接生成 hedge / roll / rebalance / approval。

### 2.4 Greeks 不得只保留 total Greek，应按用途保留必要坐标

最低合法表达不得只保留 `total Greek` 或单一 scalar net value。每一个 Greek 报告、诊断或治理输入，都必须说明其聚合范围、计算口径与允许用途；否则只能作为 rough observation。

第一组是通常应保留的基础账本坐标：

```text
lot / leg / side；
option type：call / put；
leg type：long put / long call / short put / short call 等；
expiry / tenor bucket；
strike / moneyness bucket；
spot / forward / futures basis；
aggregation scope；
allowed usage。
```

第二组是按 Greek、工具结构与用途适用的候选诊断坐标，不构成所有 Greeks 的共同最低字段集合：

```text
volatility shock size；
up / down direction；
surface coordinate；
liquidity / execution condition；
skew scenario；
rate / basis scenario；
execution lag；
scenario set version。
```

边界：上述列表是方法论表达，不是字段冻结。进入字段文档前，必须逐项判断该坐标是否由对应 Greek、工具、组合结构和使用场景所需要；不得把 surface coordinate、vol shock、liquidity、execution condition 等候选坐标写成所有 raw Greeks 的共同最小字段。

---

## 3. Greeks 分层总框架

| Greek / 风险语言 | 管理对象 | 可观察内容 | 误读风险 | 不可推出项 | 主要证据 |
|---|---|---|---|---|---|
| Delta | 标的价格局部一阶敏感度、有限移动下方向暴露 | theoretical / modified / finite-move / up-down / spot-forward / vol-stressed Delta | 把 Delta 当概率、方向风险全貌或动作授权 | Delta-neutral = risk-neutral；固定 hedge rule | Ch07 CA-07-001–024；RR-07-001–010；M-07-001–007 |
| Gamma | Delta 对价格变化的局部二阶敏感度、区间化凸性 | price interval、up/down Gamma、tenor-adjusted Gamma、shadow Gamma、event matrix | 当前 spot net Gamma 被当成完整 convexity | 固定 Gamma threshold；shadow Gamma 单项动作批准 | Ch08 CA-08-001–024；RR-08-001–013；M-08-001–007 |
| Vega | 隐含波动率、期限、远期段、曲面、偏度风险语言 | raw Vega、tenor Vega、forward-segmented Vega、surface Vega、grid Vega、scenario-stressed Vega | net Vega = 0 被当成 vol risk neutral | 固定 Vega weight；固定 grid / correlation matrix | Ch09 CA-09-001–025；RR-09-001–016；M-09-001–008 |
| Theta | 时间流逝下定价状态变化 | ordinary / modified / shadow Theta、theta burn、路径无关弱点 | positive Theta = safe carry；negative Theta = useless cost | expected profit；自动卖权利金规则 | Ch10 CA-10-001–009；RR-10-001–005；M-10-001–003 |
| Rho | 利率、融资、贴现、远期、曲线与计价货币风险 | Rhop / Rho1 / Rho2、curve bucket、forward / dividend / FX basis | 单一净 Rho 被当成利率风险全貌 | 固定 curve model / Rho weight | Ch10 CA-10-010–014；RR-10-006–008；M-10-004 |
| Alpha | 每单位 convexity 的 rent / carry diagnostic | Theta / Gamma 比例、modified Alpha、fair-value diagnostic | Alpha 被当成独立交易信号 | 固定 Alpha threshold；自动 long/short gamma | Ch10 CA-10-015–018；RR-10-009–011；M-10-005 |
| Higher-order Greeks / performance | Greeks 随时间、波动率、到期、执行滞后、高阶矩、边界压力的表现 | bleed、DdeltaDvol、progressive Vega、high-order moments、locked / asymptotic Delta、non-parametric stress | 高阶指标替代完整动态对冲路径分析 | 生产 trigger、固定 stress grid、完整风险替代 | Ch11 CA-11-001–024；RR-11-001–013；M-11-001–008 |

---

## 4. Delta 管理方法论

### 4.1 原书直接规则

#### 4.1.1 Delta 是局部一阶敏感度，不是完整 directional risk

Delta 描述衍生品价格相对标的价格变化的一阶敏感度。它有助于定价、头寸等价、局部对冲和风险观察，但不能单独定义真实组合风险。

证据回指：Ch07 CA-07-001 / CA-07-002 / RR-07-001 / M-07-001。

边界：支持把 Delta 作为观察语言；不支持把 Delta 当成完整 directional risk、风险消除证明或自动 hedge approval。

#### 4.1.2 连续时间 Delta 与交易 Delta 必须分层

连续时间 Delta 更适合作为 pricing / fair-value reference。真实交易中，Delta 需进入 finite-move、up/down direction、流动性与调仓频率条件下重新解释。

证据回指：Ch07 CA-07-003–007 / RR-07-002–004 / M-07-002。

边界：支持 finite-move / up-down stress；不支持固定冲击幅度、固定调仓频率或固定 hedge ratio。

#### 4.1.3 相同 Delta 不代表相同风险

相同 Delta 的头寸可能拥有完全不同的 P/L 曲线。对冲一阶敏感度可能保留或新增 Gamma、Vega、skew、tail、basis、liquidity 风险。

证据回指：Ch07 CA-07-008–010 / RR-07-005 / M-07-003。

边界：支持 post-hedge payoff shape 检查；不支持把 Delta-equivalent 写成 risk-equivalent。

#### 4.1.4 Delta 需要区分 spot / forward / futures / settlement / currency 口径

现货 Delta、远期 Delta、期货 Delta 与跨资产 Delta 的风险含义不同。基差、折现、利率、计价货币和结算结构都会改变 Delta 的解释。

证据回指：Ch07 CA-07-011–016 / CA-07-023 / RR-07-006 / RR-07-010 / M-07-004。

边界：支持 by tenor / expiry / settlement / numeraire 的 Delta 观察；不支持无口径声明的跨资产净额。

#### 4.1.5 Delta 与 probability / VaR 的关系有限

Delta 不应被简单等同于成为实值概率；Delta/Gamma VaR 可能漏掉 Vega 与 skew 风险。高波动率、偏态分布和对数正态复合效应会改变 Delta 的概率解释。

证据回指：Ch07 CA-07-017–022 / RR-07-007–009 / M-07-005–007。

边界：支持 probability proxy 与 Greek proxy 分离；不支持用 Delta 直接替代概率、VaR 或 stress test。

### 4.2 方法论转译

| 方法论规则 | 转译强度 | 表达 | 不可推出 |
|---|---|---|---|
| Delta 是局部价格敏感度语言 | Direct + Derived | 未限定的 Delta 不具备单独治理能力 | Delta 单项批准动作 |
| 理论 Delta 与交易 Delta 分层 | Direct + Derived | theoretical Delta 用于 reference；trading Delta 需 finite-move / scenario-stressed / liquidity-aware | 固定 hedge ratio |
| Delta 报告必须声明假设 | Derived | 至少说明 basis、expiry、shock、direction、vol、skew、rebalancing、aggregation scope、currency | 字段冻结 |
| Delta-equivalent 不等于 risk-equivalent | Direct + Derived | Delta hedge 后必须检查 payoff shape 与跨 Greek 风险迁移 | Delta-neutral = safe |
| Delta 必须在 vol / distribution scenario 下解释 | Direct + Derived | Delta 含 volatility scenario、distribution assumption、payoff boundary | Delta = probability |

证据回指：Ch07 M-07-001–007；RR-07-001–010。

### 4.3 策略映射

在用户波动率凸性策略中，Delta 的角色是观察核心仓位、融资腿、凸性腿与中期 Gamma leg 的一阶路径暴露。它可以回答“当前组合局部上对价格上/下移动有多敏感”，不能回答“结构是否仍守约”。

可进入 Layer 3 的映射：

```text
core holding 的 spot / futures Delta exposure；
near-end funding leg 的 finite-move down Delta 风险；
far-end convexity leg 的 wing Delta 激活 / 钝化状态；
medium Gamma leg 的 Delta center drift；
post-hedge payoff shape 检查输入；
vol-stressed Delta 观察。
```

这些映射均为 Strategy-specific Derived，只能成为诊断或治理输入。

### 4.4 不可进入事项

```text
不得生成固定 Delta 阈值；
不得生成固定 hedge frequency；
不得将 Delta-neutral 作为 risk-neutral；
不得把 Delta 当成 probability；
不得把 raw Delta 直接写入 Phase 4 approval；
不得跨 tenor / option type / moneyness / basis 直接相加后裁决。
```

---

## 5. Gamma 管理方法论

### 5.1 原书直接规则

#### 5.1.1 Gamma 必须绑定价格区间

Gamma 是 Delta 对价格变化的二阶敏感度，但它具有局部性。每次度量 Gamma 时都应与价格区间关联，多腿头寸可能在不同价格区间表现为多 Gamma 或空 Gamma。

证据回指：Ch08 CA-08-001–004 / RR-08-001–002 / M-08-001。

边界：支持 price band / region display；不支持固定区间宽度或 net Gamma 安全标签。

#### 5.1.2 up Gamma / down Gamma 必须拆分

有限移动下，上行 Gamma 与下行 Gamma 可能不同。平均上/下 Gamma 会隐藏方向不对称和三阶风险，风险反转结构尤其明显。

证据回指：Ch08 CA-08-005–008 / RR-08-003–004 / M-08-002。

边界：支持 directionality split；不支持固定 up/down shock size，也不支持上 / 下 Gamma 单独触发交易。

#### 5.1.3 跨期限 Gamma 未调整前不可比较

日历价差和远月合约 Gamma 讨论支持一个强规则：不同到期日 Gamma 未经适当调整不可比较、相加或抵消。

证据回指：Ch08 CA-08-009–011 / RR-08-005 / M-08-003。

边界：支持保留 expiry / tenor bucket 与 risk-equivalent Gamma 候选；不支持唯一期限权重或生产公式。

#### 5.1.4 Shadow Gamma 是普通 Gamma 的情景化扩展

当价格移动会伴随波动率、偏度、利率、持有收益或远期曲线变化时，固定参数 Gamma 不足。Shadow Gamma 要求在 price move + parameter co-move 情景下重估 Delta 曲率。

证据回指：Ch08 CA-08-012–022 / RR-08-006–011 / M-08-004–006。

边界：支持 scenario-stressed Gamma；不支持把 price-vol mapping 当成事实真值、production parameter 或 approved action。

#### 5.1.5 离散事件应使用 state matrix

若事件结果之间没有可交易中间路径，连续 Delta 调整和传统 Gamma 解释会失效。BSM 下 Delta/Gamma 平坦的组合仍可能在状态矩阵中暴露 short shadow Gamma。

证据回指：Ch08 CA-08-023–024 / RR-08-012–013 / M-08-007。

边界：支持 event state matrix；不支持从事件矩阵直接生成交易动作。

### 5.2 方法论转译

| 方法论规则 | 转译强度 | 表达 | 不可推出 |
|---|---|---|---|
| Gamma 区间化 | Direct + Derived | Gamma 最小合法表达单元应包含 price interval、spot level、expiry、leg identity、directionality | 固定 threshold |
| up/down Gamma 拆分 | Direct | 分开观察上行与下行 Delta 变化 | 固定 shock size |
| tenor-aware Gamma | Direct + Derived | 跨期限 Gamma 先保留 bucket，再声明 risk-equivalence | 唯一期限权重 |
| Shadow Gamma | Direct + Derived | price move + parameter co-move 情景下重估 Delta curvature | Shadow Gamma 替代 Vega |
| price-vol mapping 登记 | Derived | mapping 是 scenario assumption，需要来源、版本、适用市场、复核状态 | 主观 mapping 直接生产化 |
| event state matrix | Direct + Derived | event risk 从 path-rebalancing view 切换到 state-matrix view | 事件矩阵批准动作 |

### 5.3 策略映射

在波动率凸性策略中，Gamma 用于观察局部凸性是否位于需要的位置、上下方向是否对称、短端融资腿是否累积 short Gamma、远端凸性腿是否仍能承担左尾 / 右尾路径响应、中期 Gamma leg 是否提供有效局部 convexity。

可进入 Layer 3 的映射：

```text
gamma center / price band diagnostic；
up/down Gamma asymmetry diagnostic；
tenor-aware Gamma concentration；
short near-end Gamma 与 long far-end Gamma 的结构错配观察；
shadow Gamma under price-vol / price-skew co-move；
event state matrix 下的 tail exposure review。
```

这些映射不能单独批准 hedge / roll / rebalance。任何 Gamma-triggered action 只能是 Phase 3 candidate。

### 5.4 Shadow Gamma / event state matrix 边界

Shadow Gamma 的合法输入是明确设定、来源可说明、版本可追踪、适用范围可审计的情景联动。未经说明的“价格跌则升波”“价格涨则降波”等经验说法只能作为待审计 assumption。

Event state matrix 的合法用途是显示离散状态下组合暴露，不得直接替代概率建模、流动性评估或 Phase 4 约束裁决。

---

## 6. Vega 管理方法论

### 6.1 原书直接规则

#### 6.1.1 Vega 报告必须声明波动率 shock 口径

Vega 可按 1 vol point 或相对 vol move 报告。未声明 shock size、单位和尺度的 Vega 不具备可比较性。

证据回指：Ch09 CA-09-001–002 / RR-09-001 / M-09-001。

#### 6.1.2 scalar Vega 对组合风险不充分

单一期权 Vega 对单一期权有意义，但组合风险需要考虑期限、位置、曲面与偏度。ATM Vega 不能代表 wing Vega，sum Vega 不能替代 surface risk。

证据回指：Ch09 CA-09-004–006 / RR-09-002–003 / M-09-001。

#### 6.1.3 跨期限 Vega 未调整前不可比较、相加或相减

不同到期日未经加权的 Vega 不可比较。修正 Vega 权重可以改善跨期限风险管理，但权重本身是模型化或经验性假设，需重估和审计。

证据回指：Ch09 CA-09-008–013 / RR-09-005–007 / M-09-002–003。

#### 6.1.4 路径相关与延迟启动结构必须检查 forward-segmented Vega

路径相关期权、延迟启动期权、barrier-like 或 time-dependent payoff 的 Vega，不应只用 0–T scalar Vega 表示；需要观察未来时间段中的 long / short Vega 分布。

证据回指：Ch09 CA-09-014–019 / RR-09-008–011 / M-09-004。

#### 6.1.5 volatility surface 风险不只是 parallel shift

曲线 / 曲面风险包括平移、旋转、凸性变化、skew move、local grid deformation 与高阶形变。用 Delta 构建 vol surface 有循环依赖风险，偏度明显市场需要方格法观察 strike × tenor 风险。

证据回指：Ch09 CA-09-020–025 / RR-09-012–016 / M-09-005–008。

### 6.2 raw Vega / tenor Vega / forward-segmented Vega / surface Vega / grid Vega

本节的分类同时标注两条不同轴线：`方法论状态 / 转译强度` 用于说明该表达与 source / methodology 的关系；`运行权限 Phase` 用于说明它在系统运行中的权限位置。两者不得合并为一个“所属层”。

| Vega 形态 | 方法论状态 / 转译强度 | 运行权限 Phase | 合法用途 | 边界 |
|---|---|---|---|---|
| raw Vega | Direct source-supported observation | Phase 2 raw observation | 按单腿、单工具、单期限记录原始波动率暴露 | 不得直接跨期限、跨 moneyness、跨 surface 净额裁决 |
| tenor Vega | Direct + Derived methodology translation | Phase 2 bucket observation / Phase 3 diagnostic | 观察期限桶暴露集中与期限错配 | 权重、聚合范围与等价规则需声明；不得默认为治理裁决 |
| forward-segmented Vega | Direct source-supported observation + Derived segmentation | Phase 3 diagnostic | 路径相关、延迟启动、分段波动率风险诊断 | 不等于所有普通期权必算完整矩阵；与 Trading Concepts 的 `forward-vol bucket` 可建立映射，但在输入、shock、时间段定义和聚合规则完成审计前，不得默认同义或共用字段 |
| surface Vega | Direct + Derived methodology candidate | Phase 3 diagnostic / Phase 4 input only | 曲面平移、旋转、凸性、skew、local deformation 诊断 | scenario set 未冻结；不得写成生产 schema |
| grid Vega | Direct + Derived methodology candidate | Phase 3 diagnostic | strike × tenor cell 风险定位 | grid schema 与 correlation matrix 需另审；不得写成固定 grid |
| scenario-stressed Vega | Strategy Mapping / Future Engineering Candidate | Phase 3 scenario diagnostic / Phase 4 governance input | 检查组合在 vol / skew / surface 情景下的响应 | 只可作为 governance input，不等于 governance decision |


### 6.3 scalar net Vega 的不足

`net Vega = 0` 不能说明波动率风险中性，因为它可能掩盖：

```text
front tenor long Vega / back tenor short Vega；
ATM Vega / wing Vega 差异；
put wing / call wing skew exposure；
path-dependent forward segment exposure；
curve rotation risk；
surface convexity change；
local grid deformation；
相关矩阵失效；
liquidity / hedge availability break。
```

证据回指：Ch09 RR-09-003 / RR-09-005 / RR-09-011 / RR-09-014 / RR-09-016；M-09-001–008。

### 6.4 surface / skew / correlation / deformation

当组合包含跨期限、skew、surface、路径相关、局部曲面或多因子 Vega 风险时，Vega 管理必须把曲面 / 分段 / 网格作为候选诊断对象。普通 raw Vega 的最低要求仍是工具、方向、option type、tenor / expiry、shock unit、计算口径与聚合范围；不得把完整 surface / grid / correlation matrix 写成所有 Vega 表达的最低字段集合。

可按需进入诊断或治理输入的候选坐标包括：

```text
平移：整体 implied volatility level 变化；
旋转：期限结构或 moneyness 斜率变化；
凸性变化：curve / surface curvature 改变；
skew move：put wing / call wing 相对价格变化；
local deformation：局部 strike × tenor cell 形变；
correlation matrix：多期限 / 多因子 Vega 聚合假设；
replaceability check：远期波动率方法是否适用于该资产 / 工具。
```

边界：这些坐标是按需适用的候选观察维度，不是 raw Vega 的共同最小字段，不是生产 schema，不是固定 grid，不是固定 shock set，也不是 hedge / roll / rebalance 的自动批准条件。

---

## 7. Theta / Rho / Alpha 管理方法论

### 7.1 Theta 不等于 expected profit

Theta 表示特定定价假设下的时间价值变化，不表示期权期望损益、carry alpha 或卖方优势。短期期权的高 Theta 必须与 Gamma 风险共同解释；positive Theta 可能伴随 short Gamma、gap risk、event risk、liquidity risk。negative Theta 可能是 convexity rent，不等于 useless cost。

证据回指：Ch10 CA-10-001–003 / RR-10-001 / M-10-001。

边界：支持把 Theta 作为 time-value decay observation；不支持 fixed Theta threshold、自动 short premium rule 或 carry approval。

### 7.2 ordinary / modified / shadow Theta

Theta 进入风险管理时必须声明参数路径。ordinary Theta 是静态参数下的时间流逝；modified Theta 需声明未来波动率 / 参数假设；shadow Theta 将静止价格与波动率变化结合。Theta 的路径无关弱点使其不能表达往返路径损益。

证据回指：Ch10 CA-10-004–005 / CA-10-008–009 / RR-10-002 / RR-10-004–005 / M-10-002。

边界：支持 scenario Theta；不支持主观 vol path 无审计生产化。

### 7.3 Theta 与融资成本必须分账

原书约定 Theta 不包含权利金的融资成本。自融资策略需要单独处理现金账户与持仓收益。Theta、premium financing、cash account、self-financing carry 必须作为不同账本层处理。

证据回指：Ch10 CA-10-006–007 / RR-10-003 / M-10-003。

边界：支持 carry / financing 分账；不支持把融资 P/L 混入 Theta，也不支持用 positive Theta 替代 funding governance。

### 7.4 Rho 分账

Rho 不是单一净额。利率风险需要区分 premium financing、numeraire rate、underlying risk-neutral return、yield curve bucket、forward rate、dividend、FX basis、settlement mechanism。

证据回指：Ch10 CA-10-010–014 / RR-10-006–008 / M-10-004。

边界：支持 decomposed Rho；不支持固定 Rho weight、固定 curve model 或单一净 Rho 裁决。

### 7.5 Alpha fair-value diagnostic 的边界

Alpha 是 Theta / Gamma 的比率，可用于观察每单位 convexity 的时间衰减成本 / 收入。修正 Alpha 应继承 modified Theta 与 discrete / shadow Gamma 的假设。`Alpha fair-value diagnostic` 是方法论转译表达，不是原书字段名、生产字段或动作授权。

证据回指：Ch10 CA-10-015–018 / RR-10-009–011 / M-10-005。

边界：支持 rent-per-convexity diagnostic；不支持固定 Alpha fair value、固定 Alpha threshold、自动 buy / sell gamma rule。

### 7.6 Convexity 不只是 Gamma

Gamma 是标的价格维度的 convexity。第十章还支持 Vega convexity、rate convexity、settlement / funding convexity 等多维二阶风险族。结算、融资和再投资机制本身也可能创造路径凸性。

证据回指：Ch10 CA-10-020–024 / RR-10-012–014 / M-10-006–007。

边界：支持 multi-convexity observation；不支持把所有 convexity 合并成单一净字段。

---

## 8. Greeks Performance 与高阶风险表现

### 8.1 Greeks 必须从静态数值转为表现语言

Chapter 11 的主线是：Greeks 会随时间、价格、波动率、到期、再平衡和执行滞后漂移。一个 Greek 数字必须说明时间点、价格区间、波动率假设、到期状态、报告口径。

证据回指：Ch11 CA-11-001 / CA-11-024 / M-11-001。

### 8.2 Bleed

Delta / Gamma bleed 是时间流逝后重新定价和重新测量得到的差异。p.171 的方向性规则：多上 Gamma 并空下 Gamma 的期权头寸会随时间失血而更空 Delta；反向结构相反。

证据回指：Ch11 CA-11-002 / CA-11-004–005 / RR-11-001–002 / M-11-002。

边界：支持 bleed diagnostic；不支持固定 rebalance schedule。

### 8.3 Expiry-near binary risk

接近到期时，普通期权也可能表现出二元 / 分段风险；平滑 Delta 不能被当成稳定事实。到期日 / 到期前报告切换或情景表需要单独处理。

证据回指：Ch11 CA-11-009 / RR-11-004 / M-11-003。

边界：支持 expiry-near diagnostic；不支持到期日自动交易规则。

### 8.4 Discrete rebalancing / execution lag

连续再平衡复制价值不能无视真实交易成本、成交滞后和市场微观结构。动态对冲评估必须把离散步长、交易成本、成交滞后作为诊断维度。

证据回指：Ch11 CA-11-010–011 / RR-11-005 / M-11-004。

边界：支持 rebalancing cost diagnostic；不支持固定对冲频率。

### 8.5 DdeltaDvol 正 / 负方向

DdeltaDvol 度量波动率变化带来的 Delta 变化，应拆分正 / 负方向观察。波动率冲击后要重新测量 Delta、Vega 和局部结构形状。

证据回指：Ch11 CA-11-012–013 / RR-11-006 / M-11-005。

边界：支持 vol-shock 后 Delta 中性稳定性测试；不支持固定 vol shock、grid、trigger 或生产字段。

### 8.6 Progressive Vega

渐进 Vega 测试可揭示临界区间和 Vega 反转。它适合作为 Vega stress map 候选观察维度。

证据回指：Ch11 CA-11-014 / RR-11-007 / M-11-005。

边界：不生成固定 grid。

### 8.7 High-order moments

真实世界的肥尾、偏度、跳空和非正态环境使高阶矩不能简单忽略。低阶看似中性但高阶递增敞口可能造成交易困难。

证据回指：Ch11 CA-11-015–017 / RR-11-008–009 / M-11-006。

边界：高阶矩用于低阶中性背后的形状压力测试；不得单项批准或阻断动作。

### 8.8 Locked / asymptotic Delta

Locked Delta / asymptotic Delta 是边界压力视图，用于记录组合上下极端边界 Delta。它故意忽略中间路径和 hedge P/L。

证据回指：Ch11 CA-11-018 / CA-11-021 / CA-11-023 / RR-11-010 / RR-11-013 / M-11-007。

边界：可作为 up/down asymptotic exposure；不能替代完整动态对冲路径分析。

### 8.9 Non-parametric stress test

在参数不稳、相关性崩溃、分布漂移和跳空风险下，模型 Greeks 必须接受非参数化情景和经验约束。交易所 / 清算风险视图也不能替代 OTC 或机构组合情景分析。

证据回指：Ch11 CA-11-019–020 / CA-11-022 / RR-11-011–012 / M-11-008。

边界：这是 model humility / non-parametric stress 要求，不是反模型，也不是拒绝定量方法。

---

## 9. Cross-Greek 交叉约束

### 9.1 Delta × Gamma

Delta 给出局部一阶暴露；Gamma 决定价格移动后 Delta 如何变化。Delta-neutral 若处在不利 Gamma 区间，价格移动后会迅速失去中性。

互补：Delta 用于局部方向观察，Gamma 用于局部凸性和 Delta drift 观察。  
不可替代：Delta hedge 不能替代 Gamma 区间化、up/down Gamma、shadow Gamma 或 event matrix。

证据回指：Ch07 CA-07-003–010；Ch08 CA-08-001–008；Ch11 CA-11-005。

### 9.2 Gamma × Vega

Vega 可通过未来 Gamma 调整收益联系起来，但 Gamma 与 Vega 在 tail、stress、liquidity break、surface deformation 下会分离。

互补：Gamma 描述价格维度曲率，Vega 描述波动率 / 曲面维度风险。  
不可替代：Vega hedge 不自动替代 Gamma hedge；Shadow Gamma 不自动替代 Vega surface analysis。

证据回指：Ch09 CA-09-007 / CA-09-021；RR-09-004 / RR-09-013；M-09-007。

### 9.3 Vega × Theta

Positive Theta 可能对应 short volatility / short convexity；long Vega / long convexity 往往伴随 negative Theta。Theta 的收益幻觉必须用 Vega、Gamma、surface stress 检查。

互补：Theta 表示时间价值变化，Vega 表示波动率风险价格。  
不可替代：Theta income 不代表 Vega risk 被覆盖；negative Theta 不代表结构无效。

证据回指：Ch10 CA-10-001–005；Ch09 CA-09-008–025。

### 9.4 Theta × Alpha

Alpha 是 Theta 相对 Gamma 的比例，适合观察每单位 convexity 的 rent 是否异常。它继承 Theta 与 Gamma 的所有前提。

互补：Alpha 可辅助比较 carry / convexity rent。  
不可替代：Alpha diagnostic 不能替代 modified Theta、discrete / shadow Gamma 或 Phase 4 裁决。

证据回指：Ch10 CA-10-015–018；RR-10-009–011；M-10-005。

### 9.5 Rho × Financing

Rho 与 financing、carry、discounting、forward、curve、settlement 相关。Theta 不包含 premium financing cost，Rho 也不能合并为单一净额。

互补：Rho 分账与 financing ledger 共同解释利率 / 资金路径。  
不可替代：net Rho 不替代融资账本，positive carry 不替代资金治理。

证据回指：Ch10 CA-10-006–014；RR-10-003 / RR-10-006–008。

### 9.6 Higher-order Greeks × Stress Test

DdeltaDvol、progressive Vega、高阶矩、locked Delta、asymptotic Delta、non-parametric stress test 都用于暴露低阶 Greeks 的边界。

互补：高阶与非参数 stress 能识别 low-order neutral / high-order fragile 状态。  
不可替代：任何高阶指标都不能替代完整路径化动态对冲分析、流动性审计或 Phase 4 constraint stack。

证据回指：Ch11 CA-11-012–024；RR-11-006–013；M-11-005–008。

---

## 10. Phase 权限边界

### 10.1 Phase 权限定义

依据用户方法论文件，本主文档采用如下权限链：

| Phase | 权限定义 | Greeks 允许用途 | Greeks 禁止用途 |
|---|---|---|---|
| Phase 2 | facts / raw observation / raw exposure / fact calculation | 计算 raw Greeks by lot / leg / tenor / side / option type / moneyness / expiry；记录 raw Vega、raw Delta、raw Gamma、raw Theta、raw Rho | 诊断、候选动作、批准执行、最终治理裁决 |
| Phase 3 | diagnostic / scenario assumption / candidate action | Greeks Observation、risk-equivalent Greeks、scenario-stressed Greeks、bleed diagnostic、surface diagnostic、candidate input | 直接执行、绕过治理、把 candidate 写成 approved |
| Phase 4 | governance decision / legality check / execution constraint | Greeks-related legality 作为 constraint stack 输入；manual review decision；post-action Greeks check | 用单一 proxy 或单一 Greek 净额替代 governance decision |

### 10.2 Phase 2 可进入的信息

```text
raw Delta by lot / leg / tenor / option type / side；
finite-move Delta 的基础计算结果，但不作诊断裁决；
raw Gamma by price point / leg / expiry；
raw Vega by expiry / shock size；
ordinary Theta；
raw Rho / rate sensitivity；
基础 Greek report metadata：time stamp、market snapshot、basis、vol shock unit、calculation status。
```

这些信息只能回答“当前事实是什么”。

### 10.3 Phase 3 可进入的信息

```text
up/down Delta diagnostic；
post-hedge payoff shape diagnostic；
gamma center / price band / up-down Gamma asymmetry；
shadow Gamma scenario；
forward-segmented Vega；
surface / grid Vega diagnostic；
modified / shadow Theta；
decomposed Rho diagnostic；
Alpha fair-value diagnostic；
bleed / expiry-near / DdeltaDvol / progressive Vega / high-order moments / locked Delta / non-parametric stress；
manual-review condition / manual-review recommendation；
candidate action input。
```

这些信息只能回答“当前状态可能意味着什么”与“哪些候选可提交审查”。

### 10.4 Phase 4 只能接收为治理输入的信息

```text
risk-equivalent Greeks；
scenario-stressed Greeks；
constraint stack 中声明过用途的 Greeks diagnostic；
post-action legality check 输入；
manual review / block / approval 的辅助证据。
```

即使进入 Phase 4，它们仍然只是 governance input，不构成 governance decision 本身。Phase 3 的 `manual-review condition / manual-review recommendation` 只表示建议进入人工复核；Phase 4 才能形成 `manual review / block / approval` 等 governance decision。获批动作执行后，必须另行进入 post-action legality / residual-risk / state verification；post-action check 不得倒置为 candidate formation 的前置条件。

---

## 11. 用户波动率凸性策略中的嵌入方式

> 本章全部属于 Strategy-specific Derived。它只说明 Greeks 方法论如何映射到用户策略语境，不是 Chapter 07–11 source claim，不得回写 Source Traceability Matrix，不得作为 Taleb 原书证据，不得直接生成字段名、schema、YAML key、算法步骤、参数或交易动作。

### 11.1 嵌入原则

用户方法论文件将策略定义为 option-centric、路径响应型、波动率凸性系统。Greeks 在其中用于描述 `F(X)` 的局部响应形状，但不定义结构本体。

Greeks 嵌入方式：

```text
Phase 2：保留 raw exposure；
Phase 3：形成 Greeks Observation / diagnostics / scenario input；
Phase 4：进入 constraint stack，辅助 approval / block / manual review；
执行后：post-action legality check。
```

### 11.2 核心仓位

核心仓位的 Greeks 观察重点是：

```text
spot / futures / forward Delta 口径；
Delta 与标的 Beta 暴露的关系；
对冲后是否改变核心仓位的功能承担；
Rho / financing / basis 对持有成本和远期口径的影响。
```

边界：核心仓位的 Delta 观察不能单独批准对冲；对冲需要进入 B3 动作语义与 Phase 4 治理。

### 11.3 近端融资腿

近端融资腿的 Greeks 观察重点是：

```text
positive Theta 是否伴随 short Gamma / jump risk；
near-expiry binary risk；
short Vega / skew exposure；
down Gamma 与 event state matrix；
financing / cash account / premium ledger 分账。
```

边界：positive Theta 不能证明 safe carry；short premium 收入不能替代 funding governance。

### 11.4 远端凸性腿

远端凸性腿的 Greeks 观察重点是：

```text
wing Delta 激活 / 钝化；
long Gamma 的 price band 与 expiry；
long Vega 的 tenor / surface / skew exposure；
negative Theta 作为 convexity rent 的成本状态；
locked / asymptotic Delta 下的左右尾边界响应。
```

边界：negative Theta 不等于 useless cost；long Vega 不等于完整左尾保护；wing Delta 钝化也不自动批准 roll。

### 11.5 中期 Gamma leg

中期 Gamma leg 的 Greeks 观察重点是：

```text
gamma center；
up/down Gamma asymmetry；
Delta bleed；
rebalancing cost diagnostic；
vol-stressed Delta；
post-hedge payoff shape。
```

边界：Gamma leg 的调整只能成为 candidate，不得由单一 Gamma 指标直接批准。

### 11.6 左尾保护 / 右尾增强

左尾保护与右尾增强不是由某一个 Greek 定义，而由组合在状态空间 `X` 下的响应函数共同体现。Greeks 可辅助观察：

```text
左尾：down Delta、down Gamma、put wing Vega、skew exposure、event matrix、locked downside Delta；
右尾：up Delta、up Gamma、call wing Vega、asymptotic upside Delta、theta cost / convexity rent；
双向：surface deformation、liquidity、execution lag、post-action legality。
```

边界：不得新增任何未在用户方法论文件或章节包中支持的固定参数。本文不设定 DTE、moneyness、shock size、threshold 或仓位比例。

---

## 12. 禁止误用清单

| 禁止误用 | 说明 | 依据 |
|---|---|---|
| 任一 Greek 作为单项动作批准器 | Greeks 只能作为观察、诊断或治理输入 | 全章共通；用户 C1；Ch07–11 M |
| net Greek = 0 当成风险中性 | 净额可掩盖期限、行权价、曲面、路径、执行风险 | Ch07 RR-07-005；Ch09 RR-09-005；Ch11 RR-11-009 |
| Delta-neutral 当成 risk-neutral | Delta 只处理一阶局部敏感度 | Ch07 M-07-001–003；Ch08 RR-08-013 |
| 跨 tenor / strike / moneyness / option type / side / surface 直接相加 | 未声明等价规则、聚合范围与情景假设的聚合无治理权限 | Ch08 RR-08-005；Ch09 RR-09-005；用户 C1 |
| Gamma 只看当前 spot net value | Gamma 需 price interval、direction、tenor、shadow Gamma | Ch08 M-08-001–007 |
| Vega 只看 scalar net Vega | Vega 需 raw / tenor / forward / surface / grid / stress 分层 | Ch09 M-09-001–008 |
| positive Theta = safe carry | Theta 不是 expected profit；需 Gamma / Vega / financing 联合观察 | Ch10 RR-10-001–005 |
| negative Theta = useless cost | negative Theta 可能是 convexity rent | Ch10 M-10-005–006 |
| Rho 合并成单一净额 | 利率风险需分账 | Ch10 RR-10-006–008 |
| Alpha 当成独立信号 | Alpha fair-value diagnostic 非动作授权 | Ch10 M-10-005 |
| 高阶 Greek 替代动态路径分析 | locked / asymptotic Delta 忽略中间路径和 hedge P/L | Ch11 RR-11-010 / RR-11-013 |
| non-parametric stress test 被写成反模型 / 反量化 | 非参数化压力测试是 model humility 与情景约束，不取消模型 Greeks、参数化系统或定量风险报告 | Ch11 RR-11-011 / M-11-008 |
| 生成固定 threshold / shock / grid / weight | 章节包只支持方向和边界，不支持生产参数 | Ch07–11 复审报告共通 |
| 生成字段文档 / 算法文档 / YAML | 本文档为上游方法论主文档 | 本文档边界 |

---

## 13. 后续字段 / 算法 / YAML 候选观察维度

> 本节只列候选维度，不冻结字段名、字段类型、算法接口、YAML schema、阈值、权重或网格。`主回指` 只用于后续审计定位；若进入字段 / 算法 / YAML 拆解，仍需回查对应章节包原文与复审报告。  
> 本节不得倒灌为 Chapter 07–11 source claim，也不得被自动脚本直接复制为字段 taxonomy、算法接口或 YAML schema。必须先完成本轮 patch 复审与下游可衍生性审计。

| 候选观察维度 | 来源章节 | 主回指 | 转译强度 | 可能用途 | 复核类型 | 备注 |
|---|---|---|---|---|---|---|
| Delta report metadata：basis / expiry / shock / direction / vol assumption / aggregation scope | Ch07 | CA-07-011, CA-07-016; RR-07-006; M-07-004 | Derived | Phase 2 report metadata 候选 | 字段级复核 / 权限边界审计 | 只定义报告口径，不定义 hedge rule |
| finite-move Delta | Ch07 | CA-07-004; RR-07-002; M-07-002 | Direct + Derived | Phase 3 Delta stress diagnostic | 公式级复核 / 情景假设审计 | shock size 另审 |
| up/down Delta | Ch07 | CA-07-005, CA-07-006; RR-07-003; M-07-002 | Direct | Phase 3 directionality diagnostic | 情景假设审计 | 不生成固定 up/down shock |
| post-hedge payoff shape check | Ch07 | CA-07-008, CA-07-010; RR-07-005; M-07-003 | Direct + Derived | Phase 3 / Phase 4 input | 算法候选审计 / 权限边界审计 | 只作为候选检查，不批准动作 |
| Delta by tenor / settlement / numeraire | Ch07 | CA-07-011, CA-07-013, CA-07-016; RR-07-006, RR-07-010; M-07-004 | Direct + Derived | Phase 2 raw bucket / Phase 3 diagnostic | 字段级复核 / 口径复核 | 不跨口径净额化 |
| price-band Gamma | Ch08 | CA-08-001, CA-08-002, CA-08-004; RR-08-001, RR-08-002; M-08-001 | Direct + Derived | Gamma region display | 图表级复核 / 情景假设审计 | price interval 规则另审 |
| up/down Gamma asymmetry | Ch08 | CA-08-005, CA-08-008; RR-08-003, RR-08-004; M-08-002 | Direct | Gamma directionality diagnostic | 情景假设审计 | 不生成固定 shock |
| tenor-aware / risk-equivalent Gamma | Ch08 | CA-08-009, CA-08-011; RR-08-005; M-08-003 | Direct + Derived | 跨期限 Gamma 诊断 | 算法候选审计 / 权限边界审计 | 等价规则另审 |
| shadow Gamma scenario | Ch08 | CA-08-012, CA-08-016; RR-08-006, RR-08-008; M-08-004 | Direct + Derived | price-vol / price-skew co-move stress | 情景假设审计 / 短引文复核 | mapping 来源需登记 |
| event state matrix | Ch08 | CA-08-023, CA-08-024; RR-08-012, RR-08-013; M-08-007 | Direct + Derived | 离散事件风险诊断 | 情景假设审计 / 权限边界审计 | 不生成概率或交易动作 |
| raw Vega shock unit | Ch09 | CA-09-001, CA-09-002; RR-09-001; M-09-001 | Direct | Phase 2 raw Vega metadata | 字段级复核 / 口径复核 | 普通 raw Vega 不要求完整 surface |
| tenor Vega | Ch09 | CA-09-008, CA-09-009; RR-09-005; M-09-002 | Direct + Derived | 期限桶 Vega 观察 | 算法候选审计 / 权限边界审计 | 权重与聚合另审 |
| forward-segmented Vega | Ch09 | CA-09-014, CA-09-015, CA-09-018; RR-09-008, RR-09-010; M-09-004 | Direct | 路径相关 / 延迟启动结构诊断 | 算法候选审计 / 短引文复核 | 不等于所有普通期权必算矩阵 |
| surface Vega scenario | Ch09 | CA-09-022, CA-09-023, CA-09-025; RR-09-014, RR-09-016; M-09-005 | Direct + Derived | 曲面平移 / 旋转 / 凸性 / skew 诊断 | 情景假设审计 / 权限边界审计 | 按需适用，不是生产 schema |
| grid Vega | Ch09 | CA-09-025; RR-09-016; M-09-008 | Direct + Derived | strike × tenor cell 风险定位 | 字段级复核 / 算法候选审计 | grid schema / correlation matrix 另审 |
| ordinary / modified / shadow Theta | Ch10 | CA-10-004, CA-10-005, CA-10-008; RR-10-002, RR-10-004; M-10-002 | Direct + Derived | 时间价值 / 参数路径诊断 | 公式级复核 / 情景假设审计 | 参数假设另审 |
| financing ledger separation | Ch10 | CA-10-006, CA-10-007; RR-10-003; M-10-003 | Direct | Theta 与融资分账 | 字段级复核 / 账本口径审计 | 不合并为 Theta 收益 |
| decomposed Rho | Ch10 | CA-10-010, CA-10-014; RR-10-006, RR-10-008; M-10-004 | Direct + Derived | rate / curve / numeraire / forward / basis 诊断 | 字段级复核 / 曲线口径复核 | 不生成单一净 Rho 裁决 |
| Alpha fair-value diagnostic | Ch10 | CA-10-015, CA-10-018; RR-10-009, RR-10-011; M-10-005 | Direct + Derived | rent-per-convexity 观察 | 权限边界审计 / 短引文复核 | 防止动作越权 |
| multi-convexity diagnostic | Ch10 | CA-10-020, CA-10-022; RR-10-012, RR-10-013; M-10-006 | Direct + Derived | Vega / rate / funding convexity 观察 | 权限边界审计 / 口径复核 | convexity 不只 Gamma |
| bleed diagnostic | Ch11 | CA-11-002; RR-11-001, RR-11-002; M-11-002 | Direct + Derived | 时间漂移检查 | 字段级复核 / 日期惯例审计 | 不生成 rebalance rule |
| expiry-near binary diagnostic | Ch11 | CA-11-009; RR-11-004; M-11-003 | Direct + Derived | 到期前风险切换观察 | 情景假设审计 / 权限边界审计 | 不生成到期日交易信号 |
| rebalancing cost diagnostic | Ch11 | CA-11-010, CA-11-011; RR-11-005; M-11-004 | Direct + Derived | 离散再平衡 / 执行滞后诊断 | 算法候选审计 / 交易成本模型复核 | 不固定交易成本模型 |
| DdeltaDvol +/- | Ch11 | CA-11-012, CA-11-014; RR-11-006, RR-11-007; M-11-005 | Direct + Derived | vol shock 后 Delta 稳定性检查 | 情景假设审计 / shock grid 审计 | 不冻结 shock grid |
| progressive Vega | Ch11 | CA-11-013, CA-11-014; RR-11-007; M-11-005 | Direct + Derived | Vega 反转 / 临界区间观察 | 情景假设审计 / grid 审计 | 不冻结 progressive grid |
| high-order moments | Ch11 | CA-11-015, CA-11-017; RR-11-008, RR-11-009; M-11-006 | Direct + Derived | low-order neutral / high-order fragile 审计 | 公式级复核 | 不替代完整 stress test |
| locked / asymptotic Delta | Ch11 | CA-11-018, CA-11-021, CA-11-023; RR-11-010, RR-11-013; M-11-007 | Direct | 边界压力视图 | 权限边界审计 / 路径分析边界声明 | 不替代动态对冲路径 |
| non-parametric stress test | Ch11 | CA-11-019, CA-11-020; RR-11-011; M-11-008 | Direct + Derived | 模型谦逊 / 参数不稳压力测试 | 情景假设审计 / 权限边界审计 | 不是反模型 / 反量化 |
| Greeks Risk Response Dashboard | 用户方法论 + Ch07–11 | 用户 C1; Ch07–11 M 主线 | Strategy-specific Derived | display / diagnostic 汇总 | UI 审计 / 权限边界审计 | 只作为观察与诊断，不批准动作 |
| scenario-stressed Greeks as governance input | 用户方法论 + Ch08–11 | M-08-004, M-09-005, M-11-008 | Strategy-specific Derived | Phase 4 input | constraint stack 审计 / 权限边界审计 | 只作为 governance input，不等于 decision |

---

## 14. 保留复核任务

### 14.1 公式级复核

以下内容在 v0.3.1 章节包与复审报告中均保留为后续任务：

```text
Ch07 F-07-004 至 F-07-010；
Ch08 Gamma / Shadow Gamma 相关公式；
Ch09 Vega 权重、远期分段、矩阵法、surface/grid 公式；
Ch10 p.150 现货 / 远期预期价格公式、p.163 固定收益价格与利率凸性公式；
Ch11 DdeltaDvol、progressive Vega、高阶矩、locked / asymptotic Delta 相关公式。
```

本文不执行公式生产复核。

### 14.2 表格数值复核

```text
Ch07 表 7.1–7.4；
Ch08 表 8.x shadow Gamma / event matrix 相关表格；
Ch09 期限权重、经验权重、矩阵与 grid 相关表格；
Ch10 Vega/Gamma/Theta scaling 表；
Ch11 p.176 非编号再平衡表 UT-11-001。
```

本文不将表格数值写入生产测试样例。

### 14.3 图形坐标复核

```text
Delta 曲线与 P/L 图；
Gamma price-band / up-down / shadow Gamma 图；
Vega 曲线、surface、grid 图；
Theta / Rho / Alpha 图；
Greeks performance、bleed、progressive Vega 图。
```

图形用于方法论方向，不用于生产坐标。

### 14.4 强规则短引文复核

后续审计可对以下强规则补充短引文复核：

```text
Ch07：连续时间 Delta 不应直接用于风险对冲；Delta-equivalent ≠ risk-equivalent；
Ch08：Gamma 必须附带价格区间；跨期限 Gamma 未调整不可比较；事件状态矩阵；
Ch09：跨期限 Vega 未调整不可比较；路径相关 Vega 必须 forward-segmented；surface/grid 风险；
Ch10：Theta 不是 expected P/L；Theta 与 financing 分账；Rho 分账；Alpha 边界；
Ch11：p.171 Gamma-time-Delta 方向性规则；p.178 DdeltaDvol 正负方向；locked/asymptotic Delta 边界。
```

### 14.5 Chapter 09 README 元数据 P2 小问题提醒

Chapter 09 Vega v0.3.1 复审结论为有条件通过。剩余问题为 README 顶部元数据仍写作旧状态，与 revision log、diff summary 和复审报告不一致。总整合时不得以 README 顶部旧状态作为最终状态。

### 14.6 Chapter 07–11 总整合后仍需审计的问题

```text
1. 本主文档是否误把 source rule 写成字段候选以外的生产规则；
2. 是否存在 CA Cards 第 8 节被误作 source evidence；
3. 是否存在 Strategy Mapping 直接生成 hedge / roll / rebalance action；
4. 是否存在固定 threshold / shock / grid / weight；
5. 是否存在跨 tenor / strike / moneyness / option type / surface coordinate 直接净额化；
6. 是否存在 Alpha fair-value diagnostic 越权为交易信号；
7. 是否存在 high-order Greeks 替代完整动态对冲路径分析；
8. 是否存在 Phase 2 / Phase 3 / Phase 4 混层；
9. 本 v0.1.2-freeze 是否仍保持 strategy-specific derived 防倒灌声明、下游可衍生性审计前置条件和非生产边界。
```

---

## 15. Source Traceability Matrix

| 方法论规则 | 来源章节 | CA | RR | M | Source 强度 | 是否可进入后续字段候选 | 保留复核 |
|---|---|---|---|---|---|---|---|
| Delta 是局部一阶敏感度，不是完整风险 | Ch07 | CA-07-001, CA-07-002 | RR-07-001 | M-07-001 | Direct + Derived | 可作为 observation metadata / display 候选 | 短引文复核 |
| 交易 Delta 需 finite-move / up-down stress | Ch07 | CA-07-004, CA-07-005, CA-07-006 | RR-07-002, RR-07-003 | M-07-002 | Direct + Derived | 可作为 stress diagnostic 候选 | shock size 另审 |
| Delta-equivalent 不等于 risk-equivalent | Ch07 | CA-07-008, CA-07-010 | RR-07-005 | M-07-003 | Direct | 可作为治理禁令候选 | 短引文复核 |
| Delta 聚合前需统一 instrument / tenor / settlement / currency | Ch07 | CA-07-011, CA-07-012, CA-07-013, CA-07-016 | RR-07-006, RR-07-010 | M-07-004 | Direct + Derived | 可作为 bucket metadata 候选 | 口径复核 |
| Delta/Gamma VaR 不得替代 Vega/skew/surface risk | Ch07 | CA-07-017 | RR-07-007 | M-07-005 | Direct + Derived | 可作为 proxy governance 禁令 | 短引文复核 |
| Delta 不得直接当成概率 | Ch07 | CA-07-018, CA-07-020, CA-07-021 | RR-07-008 | M-07-006 | Direct | 可作为 display warning | 概率口径复核 |
| Delta 必须在 vol scenario 下重估 | Ch07 | CA-07-019, CA-07-022 | RR-07-009 | M-07-007 | Direct + Derived | 可作为 vol-stressed Delta 候选 | 公式复核 |
| Gamma 必须区间化 | Ch08 | CA-08-001, CA-08-002, CA-08-004 | RR-08-001, RR-08-002 | M-08-001 | Direct + Derived | 可作为 price-band Gamma 候选 | 图形坐标复核 |
| up/down Gamma 必须拆分 | Ch08 | CA-08-005, CA-08-006, CA-08-008 | RR-08-003, RR-08-004 | M-08-002 | Direct | 可作为 directionality diagnostic 候选 | shock size 另审 |
| 跨期限 Gamma 不可直接相加 | Ch08 | CA-08-009, CA-08-010, CA-08-011 | RR-08-005 | M-08-003 | Direct + Derived | 可作为 tenor-aware Gamma 候选 | 权重 / 等价规则另审 |
| Shadow Gamma 是情景化扩展 | Ch08 | CA-08-012, CA-08-014, CA-08-016 | RR-08-006, RR-08-007, RR-08-008 | M-08-004 | Direct + Derived | 可作为 scenario Gamma 候选 | mapping 来源复核 |
| price-vol mapping 需登记 | Ch08 | CA-08-016, CA-08-018, CA-08-019 | RR-08-008, RR-08-009 | M-08-005 | Derived | 可作为 scenario assumption registry 候选 | 版本 / 适用市场复核 |
| basis / rate / forward curve stress | Ch08 | CA-08-020, CA-08-021, CA-08-022 | RR-08-010, RR-08-011 | M-08-006 | Direct + Derived | 可作为 advanced stress 候选 | 跨资产适用性复核 |
| Event risk 使用 state matrix | Ch08 | CA-08-023, CA-08-024 | RR-08-012, RR-08-013 | M-08-007 | Direct + Derived | 可作为 event diagnostic 候选 | 状态集合复核 |
| Vega 从 scalar 扩展到 term / segment / surface | Ch09 | CA-09-001, CA-09-006, CA-09-008, CA-09-014, CA-09-025 | RR-09-003, RR-09-005, RR-09-008, RR-09-016 | M-09-001 | Direct + Derived | 可作为多层 Vega 候选 | 字段拆分审计；surface/grid 按需适用 |
| 跨期限 Vega 需加权 / 分段 / 矩阵化 | Ch09 | CA-09-008, CA-09-009, CA-09-011, CA-09-012, CA-09-019 | RR-09-005, RR-09-006, RR-09-011 | M-09-002 | Direct + Derived | 可作为 tenor Vega / matrix Vega 候选 | 权重与矩阵复核 |
| Vega weight 是版本化假设 | Ch09 | CA-09-010, CA-09-011, CA-09-012, CA-09-013 | RR-09-006, RR-09-007, RR-09-011 | M-09-003 | Derived | 可作为 assumption registry 候选 | 样本窗口 / regime 复核 |
| 路径相关结构需 forward-segmented Vega | Ch09 | CA-09-014, CA-09-015, CA-09-018 | RR-09-008, RR-09-010 | M-09-004 | Direct | 可作为强候选观察维度 | 分段算法复核 |
| Surface scenario 不只 parallel shock | Ch09 | CA-09-022, CA-09-023, CA-09-025 | RR-09-014, RR-09-016 | M-09-005 | Direct + Derived | 可作为 surface stress 候选 | scenario set 另审；不是所有 raw Vega 最低字段 |
| Delta surface coordinate 有循环依赖风险 | Ch09 | CA-09-024 | RR-09-015 | M-09-006 | Direct + Derived | 可作为坐标元数据候选 | 坐标体系复核 |
| Vega/Gamma 联动不可互替 | Ch09 | CA-09-007, CA-09-021 | RR-09-004, RR-09-013 | M-09-007 | Direct + Derived | 可作为 cross-Greek 禁令 | 短引文复核 |
| 方格法是 skew / surface 工具 | Ch09 | CA-09-025 | RR-09-016 | M-09-008 | Direct + Derived | 可作为 grid Vega 候选 | grid schema / correlation 复核；不是生产 schema |
| Theta 不等于 expected profit | Ch10 | CA-10-001, CA-10-002, CA-10-003 | RR-10-001 | M-10-001 | Direct + Derived | 可作为 display warning / diagnostic 候选 | 短引文复核 |
| Theta 需声明 ordinary / modified / shadow | Ch10 | CA-10-004, CA-10-005, CA-10-008, CA-10-009 | RR-10-002, RR-10-004, RR-10-005 | M-10-002 | Direct + Derived | 可作为 Theta type metadata 候选 | 参数路径复核 |
| Theta 与 financing 分账 | Ch10 | CA-10-006, CA-10-007 | RR-10-003 | M-10-003 | Direct | 可作为账本拆分候选 | 账本口径审计 |
| Rho 按来源 / 计价货币 / 曲线 / 期限拆分 | Ch10 | CA-10-010, CA-10-011, CA-10-014 | RR-10-006, RR-10-008 | M-10-004 | Direct + Derived | 可作为 decomposed Rho 候选 | curve / basis 复核 |
| Alpha 是 rent-per-convexity diagnostic | Ch10 | CA-10-015, CA-10-016, CA-10-018 | RR-10-009, RR-10-011 | M-10-005 | Direct + Derived | 可作为 Alpha diagnostic 候选 | 防越权审计 |
| Convexity 不只是 Gamma | Ch10 | CA-10-020, CA-10-021, CA-10-022 | RR-10-012, RR-10-013 | M-10-006 | Direct + Derived | 可作为 multi-convexity 候选 | 二阶风险口径复核 |
| 结算 / 融资 / 再投资可创造路径凸性 | Ch10 | CA-10-023, CA-10-024 | RR-10-014 | M-10-007 | Direct + Derived | 可作为 settlement/funding convexity review 候选 | 案例不可迁移为规则 |
| Greeks 必须转为表现语言 | Ch11 | CA-11-001, CA-11-024 | — | M-11-001 | Direct + Derived | 可作为 report metadata 候选 | 报告口径复核 |
| Bleed diagnostic | Ch11 | CA-11-002 | RR-11-001, RR-11-002 | M-11-002 | Direct + Derived | 可作为时间漂移候选 | 日期惯例复核 |
| Expiry-near binary diagnostic | Ch11 | CA-11-009 | RR-11-004 | M-11-003 | Direct + Derived | 可作为到期前风险候选 | 到期日规则复核 |
| Rebalancing cost diagnostic | Ch11 | CA-11-010, CA-11-011 | RR-11-005 | M-11-004 | Direct + Derived | 可作为执行成本诊断候选 | 成本模型复核 |
| DdeltaDvol / progressive Vega | Ch11 | CA-11-012, CA-11-013, CA-11-014 | RR-11-006, RR-11-007 | M-11-005 | Direct + Derived | 可作为 vol-stress map 候选 | shock / grid 复核 |
| 高阶矩压力测试 | Ch11 | CA-11-015, CA-11-016, CA-11-017 | RR-11-008, RR-11-009 | M-11-006 | Direct + Derived | 可作为 high-order fragility 候选 | 公式复核 |
| Locked / asymptotic Delta | Ch11 | CA-11-018, CA-11-021, CA-11-023 | RR-11-010, RR-11-013 | M-11-007 | Direct | 可作为边界压力候选 | 路径分析边界复核 |
| Non-parametric stress test | Ch11 | CA-11-019, CA-11-020 | RR-11-011 | M-11-008 | Direct + Derived | 可作为 model humility stress 候选 | 情景库治理；不是反模型 / 反量化 |

---

## 附录 A｜四层证据使用说明

| 层 | 名称 | 本文使用方式 | 禁止越权 |
|---|---|---|---|
| Layer 1 | Source Rule | 以 Ch07–11 CA / RR / source reconstruction 为证据 | 不写成生产字段 |
| Layer 2 | Methodology Translation | 以 Ch07–11 M 编号表达方法论规则 | 不写成自动交易规则 |
| Layer 3 | Strategy Mapping | 结合用户方法论文件，映射到核心仓位、融资腿、凸性腿、Gamma leg、左右尾 | 不直接 hedge / roll / rebalance |
| Layer 4 | Future Engineering Candidate | 列出未来字段 / 算法 / YAML 可观察维度 | 不冻结 schema / threshold / grid / weight |

## 附录 B｜当前文档审计重点

后续审计本主文档时，应优先检查：

```text
是否所有强规则均有 ChXX CA / RR / M 回指；
是否有伪造编号；
是否误用 Chapter 09 README 顶部旧状态；
是否误把 Derived 写成 Direct；
是否把 Strategy-specific Derived 写成 Taleb source；
是否输出固定参数；
是否出现自动动作授权；
是否存在 Phase 混层；
是否遗漏 Chapter 11 对静态 Greeks 的 performance 边界。
```

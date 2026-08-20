
> 文档性质：Bridge 说明文档 / 方法论安全下沉指导手册 / 后续 Bridge 构建手册  
> 适用范围：所有从方法论主文档向字段、算法、参数、YAML、runtime binding、execution governance 下沉的工程化流程  
> 当前参考案例：《Greeks 与 Trading Concepts Field_Algorithm_YAML Taxonomy Bridge_v0.1-freeze.md》  
> 使用目的：帮助理解 Bridge 的作用、构建方式、使用方式，以及后续所有方法论资产如何安全转译为工程资产  

---

## 0. 一句话定义

**Taxonomy Bridge 是方法论主文档与工程化文档之间的一层“翻译层 + 权限裁决层 + 防越权闸门”。**

它不是方法论正文，也不是字段文档、算法文档、YAML schema、参数注册表或执行规则。它的核心职责是回答：

```text
方法论中的概念、规则、警示、诊断、候选动作、禁止项，
到底哪些可以下沉？
可以下沉到哪里？
以什么权限下沉？
哪些必须保留为人工治理？
哪些必须禁止机器化或自动化？
```

换句话说，Bridge 的作用不是“生成工程实现”，而是**防止方法论在工程化过程中被过早硬化、误字段化、误算法化、误 YAML 化、误自动交易化**。

---

## 1. 为什么需要 Taxonomy Bridge

### 1.1 方法论文档天然不等于工程文档

一份成熟的方法论文档通常包含多种性质完全不同的内容：

```text
方法论原则；
风险哲学；
结构定义；
对象身份；
观察维度；
诊断语言；
候选动作；
审计提示；
人工 checklist；
禁止误用清单；
报告模块候选；
字段 / 算法 / YAML 的未来候选项。
```

这些内容在人类阅读时可以共存于一份文档中。但一旦进入工程化流程，如果不先拆分权限，很容易被错误复制为：

```text
production field；
algorithm step；
YAML key；
parameter；
signal；
trigger；
approved action；
runtime override；
automatic execution rule。
```

因此，方法论主文档不能直接进入字段、算法和 YAML。中间必须有一层 Bridge。

### 1.2 没有 Bridge 时的典型漂移

以 Greeks 与 Trading Concepts 为例，没有 Bridge 时最常见的漂移包括：

| 方法论内容 | 错误下沉方式 | 风险 |
|---|---|---|
| 候选观察维度 | 直接复制成 production field | 字段过早冻结，维度和权限错误 |
| 报告模块标题 | 直接复制成 dashboard schema 或 YAML key | 自然语言标题被误当机器字段 |
| diagnostic | 写成 signal | 诊断越权为动作触发 |
| candidate action | 写成 approved action | 候选动作越权为批准动作 |
| governance input | 写成 governance decision | 输入越权为治理裁决 |
| post-action audit | 写成 next trade trigger | 审计越权为下一笔交易 |
| forbidden clause | 写成 implementation backlog | 禁令被反向实现化 |
| H 层原则 | 写成可配置参数 | 策略身份被 profile / YAML / runtime 覆盖 |

Bridge 的任务就是在这些错误发生之前，建立清楚的“准入、禁止、前置复审、下游 gate”。

### 1.3 Bridge 是方法论资产走向工程资产的必要中间层

完整链条应该是：

```text
方法论主文档
  ↓
Taxonomy Bridge
  ↓
Field taxonomy
  ↓
Field document
  ↓
Algorithm taxonomy
  ↓
Algorithm document
  ↓
Parameter registry
  ↓
YAML schema
  ↓
YAML instance
  ↓
Runtime binding
  ↓
Execution governance
```

Bridge 处在第一道工程化入口处。它既不是最终实现，也不是普通目录，而是决定“能不能下沉、下沉到哪里、怎么防止越权”的规则层。

---

## 2. Bridge 是什么，不是什么

### 2.1 Bridge 是什么

Bridge 是一份专门用于方法论下沉的中间层文档。它通常包括：

```text
namespace taxonomy；
Phase 权限链；
H/P/W 权限标注；
action lifecycle；
field taxonomy bridge；
algorithm taxonomy bridge；
YAML / config taxonomy bridge；
forbidden automation registry；
forbidden override registry；
lineage / audit metadata contract；
downstream gate。
```

它回答的是分类问题、权限问题、边界问题、禁止问题、前置条件问题。

### 2.2 Bridge 不是什么

Bridge 不是以下任何东西：

```text
不是字段冻结稿；
不是字段 schema；
不是算法实现稿；
不是算法接口最终稿；
不是 YAML schema；
不是 YAML instance；
不是参数注册表；
不是 profile config；
不是 runtime binding instance；
不是 execution governance implementation；
不是自动交易规则；
不是下单规则；
不是策略执行手册。
```

Bridge 中出现的对象名称也不是生产命名。比如：

```text
raw_field_candidate
scientific diagnostic_candidate
governance_input_candidate
report_module_candidate
schema_prerequisite
```

这些是 taxonomy label，不是字段名，不是 YAML key，不是算法名。

---

## 3. Bridge 在文档体系中的位置

### 3.1 三层基本关系

```text
第一层：方法论主文档
  回答：这个方法论是什么意思？

第二层：Taxonomy Bridge
  回答：这个方法论内容允许下沉到哪里？不允许下沉到哪里？

第三层：工程文档族
  回答：具体字段、算法、参数、YAML、runtime、治理如何设计？
```

以当前 Greeks / Trading Concepts 体系为例：

```text
Greeks 管理方法论主文档
Trading Concepts 方法论主文档
        ↓
Greeks 与 Trading Concepts Field_Algorithm_YAML Taxonomy Bridge
        ↓
Field taxonomy
Algorithm taxonomy
Parameter slot candidate taxonomy
YAML schema prerequisite
Runtime binding prerequisite
Execution governance taxonomy
```

### 3.2 当前三份 freeze 文档的分工

| 文档 | 作用 | 不可做 |
|---|---|---|
| Greeks 管理方法论主文档 | 定义 Greeks 如何作为观察、诊断和治理输入 | 不直接生成字段、算法、YAML、自动规则 |
| Trading Concepts 方法论主文档 | 定义交易概念、路径、分布、执行残差和动作语义边界 | 不直接生成执行手册或交易规则 |
| Taxonomy Bridge | 定义上述内容如何安全进入字段、算法、参数、YAML、runtime 和治理文档 | 不直接生成任何实现稿 |

---

## 4. Bridge 的核心功能

### 4.1 功能一：把方法论内容分配到 namespace

Bridge 首先要建立 namespace。namespace 是一种“归属标签”，不是字段名。

常见 namespace 包括：

| Namespace | 含义 | 示例 |
|---|---|---|
| method_principle | 方法论原则 | 不预测 X，构造 F(X) |
| core_constraint | 策略身份与硬约束 | strategy core 不可被 profile 覆盖 |
| raw_field_candidate | Phase 2 原始字段候选 | raw Delta, raw Vega |
| derived_observation_candidate | 派生观察候选 | finite-move Delta |
| diagnostic_candidate | 诊断候选 | price-band Gamma diagnostic |
| candidate_input_package | 候选输入包 | diagnostic summary + lineage + assumption set |
| governance_input_candidate | 治理输入候选 | risk-equivalent Greeks |
| governance_decision_boundary | 治理裁决边界 | approval / block / manual review / rollback decision |
| audit_metadata | 审计元数据 | source_document, review_status, version |
| manual_checklist | 人工检查清单 | settlement review, object identity review |
| manual_review_trigger | 人工复核触发 | diagnostic conflict, missing lineage |
| forbidden_automation | 禁止自动化条款 | direct hedge trigger 禁令 |
| forbidden_override | 禁止覆盖条款 | runtime 不得覆盖 constraint stack |
| parameter_slot_candidate | 参数候选槽 | shock definition, tenor bucket |
| schema_prerequisite | schema 前置条件 | required dimensions, namespace isolation |
| runtime_binding_prerequisite | runtime binding 前置要求 | approved core version, profile version |
| action_lifecycle | 动作生命周期 | candidate / approved / executed / audit |
| report_module_candidate | 报告模块候选 | Tail / Smile Diagnostic |

namespace 的作用是防止不同性质的内容混在一起。例如：

```text
report_module_candidate 不等于 field schema；
diagnostic_candidate 不等于 signal；
governance_input_candidate 不等于 governance decision；
parameter_slot_candidate 不等于 production parameter；
schema_prerequisite 不等于 YAML schema。
```

### 4.2 功能二：给每个对象标注 Phase

Bridge 必须使用 Phase 权限链。

| Phase | 合法内容 | 禁止内容 |
|---|---|---|
| Phase 1 | 方法论原则、对象身份、core constraint、forbidden automation、forbidden override | 字段冻结、算法实现、YAML instance、执行规则 |
| Phase 2 | raw exposure、raw Greeks、raw ledger、derived observation、calculation metadata | 诊断、候选动作、批准执行、治理裁决 |
| Phase 3 | diagnostic、manual review trigger、candidate input package、repair proposal | 批准执行、生成订单、绕过治理 |
| Phase 4 | governance input validation、constraint stack check、approval、block、manual review、rollback、post-action audit | 用单一 proxy 或单一 Greek 替代完整治理 |

Bridge 的核心任务之一，是防止：

```text
Phase 2 → candidate action；
Phase 3 → approved action；
Phase 3 diagnostic → signal；
Phase 4 governance input → governance decision；
post-action audit → next trade trigger。
```

### 4.3 功能三：给每个对象标注 H/P/W

H/P/W 是另一个权限轴。

| 权限 | 含义 | 是否可配置 | 是否可 override |
|---|---|---:|---:|
| H | 硬约束 / 身份约束 | 否 | 否 |
| P | 可证伪 / 可调整假设 | 候选可配置 | 需审计 |
| W | 弱观点 / 当前判断 | 仅作 note / checklist | 不得自动化 |

典型规则：

```text
H 层原则不得字段化、参数化、YAML 化、profile override、runtime override；
P 层假设只能作为 candidate / parameter slot / schema prerequisite，不能直接成为 production parameter；
W 层观点只能作为 note / checklist / manual review input，不能成为 signal / rule / governance decision。
```

### 4.4 功能四：建立 action lifecycle

Bridge 必须明确动作生命周期，防止“诊断直接变执行”。

标准 lifecycle 包括：

```text
no_action_observation；
diagnostic_only；
manual_review_trigger；
candidate_input_package；
candidate_action；
governance_input；
governance_decision；
approved_action；
blocked_action；
executed_action；
post_action_audit；
rollback_candidate；
rollback_decision。
```

核心边界：

```text
Phase 2 不得产生 candidate action；
Phase 3 可以产生 candidate input package，但不得产生 approved action；
Phase 4 才能产生 governance decision；
approved action 不等于 executed action；
executed action 必须进入 post-action audit；
post-action audit 不得自动生成下一笔交易；
rollback candidate 不等于 rollback decision。
```

### 4.5 功能五：建立 forbidden automation / forbidden override 注册表

Bridge 必须建立红线清单。

典型 forbidden automation：

```text
Greek decision engine；
net Greek = risk neutral；
direct hedge trigger；
direct roll trigger；
direct rebalance trigger；
Gamma flip trigger；
soft-hard Delta switch trigger；
vol bet execution action；
unreviewed DTE / moneyness / strike / ratio / threshold；
diagnostic as signal；
candidate action as approved action；
governance input as governance decision；
post-action audit as next trade trigger。
```

典型 forbidden override：

```text
profile override strategy core；
runtime override constraint stack；
YAML as semantic authority；
forbidden clauses as implementation requirements。
```

这类注册表的作用不是“告诉工程师去实现这些东西”，而是明确：**这些东西必须被 gate 阻断。**

### 4.6 功能六：建立 lineage / audit metadata contract

Bridge 还必须规定每个 taxonomy object 的来源和审计元数据。

典型 metadata：

```text
source_document；
source_section；
source_type；
source_strength；
translation_strength；
Phase；
H/P/W；
namespace；
machine_readability；
downstream_allowed；
downstream_forbidden；
required_dimensions；
aggregation_allowed；
aggregation_rule_required；
input_only；
decision_allowed；
profile_override_allowed；
runtime_override_allowed；
review_status；
owner；
version；
valid_from；
valid_to；
rollback_policy；
audit_log_required。
```

这保证后续字段、算法、参数、YAML 不会变成“无来源、无权限、无版本、无审计”的孤立对象。

### 4.7 功能七：建立 downstream gate

Bridge 要明确下一步可以进入哪里、不能进入哪里。

典型 gates：

```text
Field taxonomy gate；
Field document gate；
Algorithm taxonomy gate；
Algorithm document gate；
Parameter registry gate；
YAML schema gate；
YAML instance gate；
Backtest harness gate；
Runtime binding gate；
Execution governance gate。
```

每个 gate 都要说明：

```text
Allowed Input；
Required Prerequisite；
Forbidden Input；
Output Scope；
Blocking Condition；
Review Requirement。
```

---

## 5. Bridge 如何防止方法论下沉漂移

### 5.1 防止字段化漂移

Bridge 会区分：

```text
raw_field_candidate；
derived_observation_candidate；
diagnostic field candidate；
governance input field candidate；
audit metadata；
manual checklist；
forbidden fieldization item。
```

示例：

```text
raw Delta 可以进入 raw_field_candidate；
finite-move Delta 是 Phase 2 derived observation；
shadow Gamma 是 Phase 3 diagnostic_candidate；
risk-equivalent Greeks 是 governance_input_candidate；
Trading §9.2 报告模块只能是 report_module_candidate；
Trading §11.3 禁止项标题不能成为 YAML key 或 field name。
```

### 5.2 防止算法化漂移

Bridge 会区分：

```text
factual calculation algorithm；
derived observation algorithm；
diagnostic procedure；
candidate input packaging；
manual review trigger；
governance input validation；
constraint check；
governance decision boundary；
post-action audit；
forbidden algorithmization item。
```

核心原则：

```text
calculation 只能算事实；
diagnostic 只能解释状态；
candidate packaging 只能打包候选输入；
validation 只能验证输入；
constraint check 不能单独批准动作；
governance decision boundary 表示裁决类型和流程边界，不表示算法自动批准；
post-action audit 不得产生下一笔交易。
```

### 5.3 防止 YAML 化漂移

Bridge 会区分：

```text
parameter_slot_candidate；
strategy_core_reference；
strategy_config_boundary；
profile_config_boundary；
deployment_config_boundary；
runtime_binding_prerequisite；
constraint_stack_config_candidate；
audit_config_candidate；
forbidden_yaml_item；
forbidden_override_item；
schema_namespace_prerequisite；
validation_rule_prerequisite。
```

核心原则：

```text
YAML schema prerequisite 不等于 YAML schema；
YAML schema 不等于 YAML instance；
parameter slot candidate 不等于 production parameter；
profile config 不得覆盖 strategy core；
runtime binding 不得覆盖 constraint stack；
YAML 不得反向成为方法论语义权威。
```

---

## 6. Bridge 的标准构建流程

### Step 1：锁定上游文件

必须列出所有实际使用文件：

```text
方法论主文档；
一致性审计报告；
下游可衍生性审计报告；
patch diff；
freeze diff；
主题树；
上位治理文档；
相关章节包；
PDF 原文。
```

并明确：

```text
哪些是主依据；
哪些是参考；
哪些不使用；
哪些只在争议时回看；
哪些不能作为生产依据。
```

### Step 2：承接上游审计裁决

Bridge 必须承接前一轮审计的 patch 清单。例如：

```text
M-DS-01：主文档只可作为 taxonomy 上游；
M-DS-02：候选观察维度不是字段清单；
M-DS-03：报告模块不是 production field 或 YAML key；
M-DS-04：建立 action lifecycle；
M-DS-05：finite-move Delta 标为 Phase 2 derived observation；
M-DS-06：字段 taxonomy 必须处理 required dimensions；
M-DS-07：risk-equivalent Greeks 必须 input_only；
M-DS-08：Greek-flatness 与 non-Greek checks namespace 隔离；
M-DS-09：post-action audit 不得自动执行；
M-DS-10：所有 taxonomy object 标注 H/P/W；
M-DS-11：建立 forbidden override / forbidden automation。
```

### Step 3：建立 Bridge 总体架构

必须明确：

```text
本文档是什么；
本文档不是什么；
承接哪些上游；
输出哪些 taxonomy；
阻断哪些下游；
最终允许进入哪些下一步。
```

### Step 4：建立 Phase / H-P-W 总表

所有对象先按 Phase 和 H/P/W 归类。没有 Phase / H/P/W 的对象不得进入下游。

### Step 5：建立 namespace taxonomy

给所有内容准备 namespace，避免混层。

### Step 6：建立 action lifecycle

所有可能涉及动作的概念必须走 lifecycle。

### Step 7：建立 Field Taxonomy Bridge

回答：

```text
哪些可以成为 raw field candidate；
哪些只能是 derived observation；
哪些是 diagnostic；
哪些是 governance input；
哪些是 audit metadata；
哪些是 manual checklist；
哪些禁止字段化；
字段文档前必须补齐什么。
```

### Step 8：建立 Algorithm Taxonomy Bridge

回答：

```text
哪些可以作为 factual calculation；
哪些可以作为 diagnostic procedure；
哪些可以作为 candidate packaging；
哪些可以作为 validation / check；
哪些只能作为 governance boundary；
哪些禁止算法化；
算法文档前必须补齐什么。
```

### Step 9：建立 YAML / Config Taxonomy Bridge

回答：

```text
哪些只是 parameter slot candidate；
哪些属于 strategy core；
哪些属于 profile binding；
哪些属于 runtime prerequisite；
哪些属于 constraint stack；
哪些禁止 YAML 化；
哪些禁止 override；
YAML schema 前必须补齐什么。
```

### Step 10：建立 forbidden registry

必须列出红线，并明确 allowed alternative carrier。

### Step 11：建立 lineage / audit metadata contract

所有后续 taxonomy object 都必须带 metadata。

### Step 12：建立 downstream gate

明确每个下游文档的准入条件、禁止输入和阻断条件。

### Step 13：最终裁决

Bridge 最终裁决应采用类似格式：

```text
BRIDGE PASS：可作为后续 taxonomy 上游；
BRIDGE PASS WITH PATCH：可用，但需最小修订；
BRIDGE HOLD：暂不允许进入字段 / 算法 / YAML 下游；
BRIDGE FAIL：桥接层无法承接审计裁决。
```

---

## 7. Bridge 的标准使用方式

### 7.1 生成 Field taxonomy 时怎么用

Field taxonomy 不能直接读取方法论主文档随意提字段，而应首先读取 Bridge：

```text
只从 raw_field_candidate、derived_observation_candidate、diagnostic_candidate、governance_input_candidate、audit_metadata、manual_checklist 中取候选；
遇到 forbidden_fieldization 直接阻断；
遇到 report_module_candidate 不得写成字段；
遇到 schema_prerequisite 只能作为字段设计前置条件；
所有字段必须带 source、Phase、H/P/W、namespace、required_dimensions、aggregation contract。
```

### 7.2 生成 Algorithm taxonomy 时怎么用

Algorithm taxonomy 应遵循：

```text
Phase 2 只能 factual calculation / derived observation；
Phase 3 可以 diagnostic / review trigger / candidate input packaging；
Phase 4 可以 validation / constraint check / governance boundary / post-action audit；
禁止 diagnostic as signal；
禁止 candidate as approval；
禁止 validation as decision；
禁止 post-action audit as next trade trigger；
禁止 hedge / roll / rebalance implementation。
```

### 7.3 生成 Parameter registry 时怎么用

Parameter registry 只能从 parameter_slot_candidate 开始：

```text
shock definition 是候选槽，不是 shock 数值；
price band 是候选槽，不是固定区间；
tenor bucket 是候选槽，不是固定权重；
grid / surface schema 是候选 schema，不是生产 grid；
所有 P 层参数候选必须有 owner、version、review_status、valid_from、valid_to、rollback_policy。
```

### 7.4 生成 YAML schema 时怎么用

YAML schema 必须先通过 schema prerequisite：

```text
namespace 是否隔离；
H 层原则是否被 YAML 化；
profile 是否覆盖 core；
runtime 是否覆盖 constraint stack；
YAML 是否反向成为语义权威；
forbidden automation / forbidden override 是否进入 validation；
parameter_slot_candidate 是否被误写成 production parameter。
```

### 7.5 进入 runtime binding 时怎么用

runtime binding 只能引用已批准版本：

```text
approved core reference；
approved parameter set；
approved profile；
approved runtime mode；
approved scenario set version；
audit id；
constraint stack reference。
```

runtime 不得临场改写：

```text
method principle；
strategy core；
Phase 权限链；
constraint stack；
forbidden override；
YAML semantic boundary。
```

### 7.6 进入 execution governance 时怎么用

execution governance 必须通过 action lifecycle：

```text
candidate_input_package
  ↓
governance_input validation
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
  ↓
rollback candidate or audit close
```

任何单一 Greek、单一 diagnostic、单一 YAML 参数、单一 profile 设置，都不得直接生成 execution decision。

---

## 8. Bridge 的质量标准

一份合格的 Bridge 至少应满足：

```text
1. 明确自己是 bridge，不是 implementation；
2. 明确上游文件和文件锁定范围；
3. 完整承接上游审计裁决；
4. 定义 Phase 权限链；
5. 定义 H/P/W 权限；
6. 建立 namespace taxonomy；
7. 建立 action lifecycle；
8. 区分 field / algorithm / YAML 三层；
9. 建立 forbidden automation / forbidden override；
10. 建立 lineage / audit metadata contract；
11. 建立 downstream gate；
12. 明确允许进入哪些下一步；
13. 明确禁止直接进入哪些下一步；
14. 不生成任何生产字段、算法实现、YAML instance、参数值或执行规则；
15. 能被后续 Field taxonomy、Algorithm taxonomy、Parameter registry、YAML schema prerequisite 直接引用。
```

### 8.1 常见不合格信号

| 问题 | 风险 |
|---|---|
| Bridge 中出现固定阈值 | 已越界到参数 / 执行层 |
| Bridge 中出现具体 DTE / moneyness / ratio | 已越界到策略执行配置 |
| Bridge 中出现交易触发器 | 已越界到 execution automation |
| diagnostic 输出 signal | Phase 3 越权 |
| governance input 输出 decision | Phase 4 输入与裁决混层 |
| forbidden clause 被列为 implementation candidate | 禁令反向实现化 |
| report title 被写成 YAML key | 自然语言标题 schema 化 |
| H 层原则进入 profile override | 策略身份被配置层覆盖 |
| YAML 被写成语义权威 | md 方法论被反向改写 |

---

## 9. Bridge 构建模板

后续任何方法论主文档需要下沉到工程文档前，可以按以下结构构建 Bridge。

```text
# 《XXX Field_Algorithm_YAML Taxonomy Bridge_v0.1.md》

## 0. 文档定位与结论
- 本文档是什么
- 本文档不是什么
- 承接哪些上游
- 输出哪些 taxonomy
- 阻断哪些下游
- 最终裁决

## 1. 文件锁定清单
- 文件
- 是否收到
- 用途
- 使用权限

## 2. 上游裁决承接
- 一致性审计裁决
- 下游可衍生性审计裁决
- patch 清单
- 本 Bridge 如何承接

## 3. Bridge 总体架构
- 方法论主文档
- Taxonomy Bridge
- 下游文档族

## 4. Phase 与 H/P/W 权限总表
- 对象类型
- Phase
- H/P/W
- 可下沉到
- 禁止下沉到

## 5. Namespace Taxonomy
- Namespace
- 定义
- 允许对象
- 禁止对象
- Phase
- H/P/W
- 下游承接

## 6. Action Lifecycle Taxonomy
- Lifecycle State
- Phase
- 定义
- 允许输入
- 允许输出
- 禁止事项
- 下游承接

## 7. Field Taxonomy Bridge
- 字段分类总表
- 主题字段候选映射
- 禁止字段化清单
- 字段文档前置要求

## 8. Algorithm Taxonomy Bridge
- 算法分类总表
- 主题算法候选映射
- 禁止算法化清单
- 算法文档前置要求

## 9. YAML / Config Taxonomy Bridge
- YAML / Config 分类总表
- Parameter Slot Candidates
- Strategy / Profile / Runtime Boundary
- Constraint Stack / Audit Config Candidates
- 禁止 YAML 化清单
- YAML/schema 前置要求

## 10. Forbidden Automation / Forbidden Override Registry
- ID
- Forbidden Item
- Source
- Forbidden Type
- Reason
- Allowed Alternative Carrier
- Severity
- Downstream Gate

## 11. Lineage / Audit Metadata Contract
- Metadata
- Required For
- Purpose
- Allowed Values / Format
- Blocking If Missing

## 12. Downstream Gate
- Gate
- Allowed Input
- Required Prerequisite
- Forbidden Input
- Output Scope
- Blocking Condition
- Review Requirement

## 13. Patch 对照表
- Patch ID
- 审计问题
- Bridge 中的处理位置
- 是否完全承接
- 后续是否需复审

## 14. 最终裁决
- 是否可以进入 Field taxonomy
- 是否可以进入 Field document
- 是否可以进入 Algorithm taxonomy
- 是否可以进入 Algorithm document
- 是否可以进入 Parameter registry
- 是否可以进入 YAML schema
- 是否可以进入 YAML instance
- 是否可以进入 runtime binding instance
- 是否可以进入 execution governance
```

---

## 10. Bridge 复审清单

Bridge 生成后，至少应做一次轻量复审。

### 10.1 复审目标

```text
1. 是否完整承接上游下游可衍生性审计；
2. 是否仍然只是 taxonomy bridge；
3. 是否没有生成字段冻结稿；
4. 是否没有生成算法实现；
5. 是否没有生成 YAML schema / YAML instance；
6. 是否没有生成参数值；
7. 是否没有生成 profile config 或 runtime binding instance；
8. 是否没有生成 execution automation；
9. 是否没有 diagnostic as signal；
10. 是否没有 candidate as approved；
11. 是否没有 governance input as decision；
12. 是否没有 post-action audit as next trade trigger；
13. 是否没有 profile / runtime / YAML 覆盖 core；
14. 是否没有 forbidden clauses as implementation requirements。
```

### 10.2 复审结论类型

```text
BRIDGE PASS：可作为后续 taxonomy 上游；
BRIDGE PASS WITH PATCH：可用，但需最小修订；
BRIDGE HOLD：暂不建议进入下游 taxonomy；
BRIDGE FAIL：不能作为上游。
```

### 10.3 典型最小 patch

Bridge 复审中常见的最小 patch 是命名降权。例如：

```text
不建议：governance decision algorithms
建议：governance decision boundary / constraint-stack decision procedure taxonomy
```

原因是前者容易被误读为“治理裁决可算法自动化”，后者明确只是“治理裁决边界 / 程序分类”。

---

## 11. 对当前 Greeks / Trading Concepts Bridge 的理解

当前《Greeks 与 Trading Concepts Field_Algorithm_YAML Taxonomy Bridge_v0.1-freeze.md》的核心作用是：

```text
把 Greeks 管理方法论主文档与 Trading Concepts 方法论主文档中可下沉、不可下沉、需审计、需禁止的内容，统一翻译成后续 Field taxonomy、Algorithm taxonomy、Parameter slot registry、YAML schema prerequisite、Runtime binding prerequisite、Execution governance taxonomy 可以读取的 taxonomy 语言。
```

它已经明确：

```text
可以进入：
Field taxonomy；
Algorithm taxonomy；
Parameter slot candidate taxonomy；
YAML schema prerequisite；
Runtime binding prerequisite；
Execution governance taxonomy。

不能直接进入：
Field freeze；
Algorithm implementation；
YAML instance；
runtime binding instance；
execution automation。
```

因此，它是当前 Greeks / Trading Concepts 方法论体系进入工程化下游的正式入口。

---

## 12. 后续使用建议

### 12.1 下一步推荐顺序

```text
1. Field taxonomy；
2. Algorithm taxonomy；
3. Parameter slot candidate taxonomy；
4. YAML schema prerequisite；
5. Runtime binding prerequisite；
6. Execution governance taxonomy；
7. Field document；
8. Algorithm document；
9. Parameter registry；
10. YAML schema；
11. Backtest harness binding；
12. Runtime binding instance；
13. Execution governance implementation。
```

前 6 步仍然是 taxonomy / prerequisite / boundary 层。后 7 步开始逐步进入更强工程化，必须逐级审计。

### 12.2 每一步都要回看 Bridge

后续每生成一份下游文档，都应该问：

```text
这个对象在 Bridge 中属于哪个 namespace？
它属于哪个 Phase？
它是 H、P 还是 W？
它允许下沉到当前文档吗？
Bridge 有没有禁止它字段化、算法化、YAML 化或自动化？
它是否需要 lineage / review_status / owner / version？
它是否需要通过某个 downstream gate？
```

若 Bridge 没有授权，就不能直接下沉。

### 12.3 Bridge 是可复用资产

Bridge 不只是当前 Greeks / Trading Concepts 项目的中间文件。它本身是一种可复用文档模式。

未来任何方法论主文档，只要要进入字段、算法、YAML、runtime 或执行治理，都可以采用：

```text
方法论主文档
  ↓
下游可衍生性审计
  ↓
Taxonomy Bridge
  ↓
Bridge 轻量复审
  ↓
Field / Algorithm / Parameter / YAML / Runtime / Governance 下游文档
```

这套模式的价值在于：

```text
降低语义漂移；
降低工程过早硬化；
降低自动化越权；
提高字段、算法、YAML 的可审计性；
把方法论资产真正变成可复用工程资产。
```

---

## 13. 最终总结

Taxonomy Bridge 的核心价值不是“多写一份文档”，而是在方法论资产和工程资产之间建立一道必要的治理层。

它让方法论中的每一个概念在进入工程系统前都必须先回答：

```text
我是什么？
我来自哪里？
我属于哪个 namespace？
我属于哪个 Phase？
我是 H、P 还是 W？
我可以下沉到哪里？
我禁止下沉到哪里？
我是否只是候选？
我是否只能人工审查？
我是否必须 input_only？
我是否需要 review_status？
我是否需要 lineage？
我是否可能被误用为 trigger、signal、decision 或 execution？
```

只有通过这些问题，方法论才能安全地进入字段、算法、参数、YAML 和 runtime。

因此，Bridge 是后续所有方法论安全下沉到工程文档的标准中间层，也是后续构建可复用量化研究与执行体系时必须保留的文档治理模式。


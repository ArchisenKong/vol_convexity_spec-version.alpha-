
> 文档性质：Taxonomy Bridge / 下游工程化桥接层。  
> 版本：v0.1  
> 生成日期：2026-06-08  
> 使用模式：文件锁定模式；仅承接本 session 上传附件，不重新审计章节包或 PDF 原文。  
> 总裁决：**BRIDGE PASS：可作为后续 taxonomy 上游；不得直接生成字段冻结稿、算法实现稿、YAML instance、runtime binding instance 或执行自动化。**

## 0. 文档定位与结论

本文档是两份 freeze 方法论主文档与后续 Field taxonomy、Algorithm taxonomy、Parameter registry、YAML schema prerequisite、Runtime binding prerequisite、Execution governance taxonomy 之间的中间桥接层。它只做分类、标权、定边界、设禁令、设前置条件，不生成任何生产字段、算法实现、YAML、参数注册表或动作规则。


它承接的上游包括：Greeks 管理方法论主文档 v0.1.2-freeze、Trading Concepts 方法论主文档 v0.1.2-freeze、第二轮下游字段/算法/YAML 可衍生性审计报告、主题树与 12 篇方法论文档。


本文档输出：namespace taxonomy、Phase/H-P-W 权限表、action lifecycle taxonomy、field/algorithm/YAML/config taxonomy bridge、forbidden automation / forbidden override registry、lineage metadata contract、downstream gates。


本文档阻断：从主文档直接生成 production field、algorithm implementation、YAML instance、profile override、runtime binding instance、execution automation；阻断 diagnostic→signal、candidate→approved、governance input→decision、post-action audit→next action 的越权链。


最终裁决：**BRIDGE PASS**。可以进入 Field taxonomy 与 Algorithm taxonomy；只能进入 Parameter registry candidate / YAML schema prerequisite / runtime binding prerequisite；不能直接进入 Field document freeze、Algorithm implementation、YAML instance、runtime binding instance 或执行自动化。


## 1. 文件锁定清单

|文件|是否收到|用途|使用权限|
|---|---|---|---|
|Greeks_管理方法论主文档_v0.1.2-freeze.md|已收到|Greeks 主文档；字段/算法/YAML taxonomy 上游|主依据；只能作方法论边界与 taxonomy 上游，不得直接生产化|
|Trading_Concepts_方法论主文档_v0.1.2-freeze.md|已收到|Trading Concepts 主文档；字段/算法/YAML taxonomy 上游|主依据；只能作交易概念、诊断、治理边界来源，不得直接生产化|
|Greeks_与_Trading_Concepts_下游字段算法YAML可衍生性审计报告_v0.1.md|已收到|第二轮可衍生性审计；PASS WITH PATCH 与 M-DS-01–M-DS-11 来源|强制承接；本 bridge 的直接 patch 清单来源|
|1.可复用方法论主题树_20260606.md|已收到|Phase / H-P-W / proxy / 文档工程 / profile 边界|上位约束；用于权限链、namespace、override 边界|
|2波动率凸性策略可复用方法论文档集_12篇_20260606.md|已收到|统一术语、Phase、runtime binding、profile、Greeks 权限边界|上位约束；用于术语与工程权限边界|
|greeks_trading_concepts_consistency_audit_v0_1.md|已收到|第一轮总一致性审计报告|参考；不重启总审计|
|greeks_trading_concepts_v0_1_2_patch_reaudit_report.md|已收到|v0.1.2-patch 二次复审报告|参考；确认 P1/P2 patch 已落地|
|Greeks_Trading_Concepts_v0.1.2-freeze_归档说明.md|已收到|freeze 归档说明|参考；确认 freeze 归档边界|
|Greeks_管理方法论主文档_v0.1.2_patch_diff.md|已收到|Greeks patch diff|参考；用于边界收紧核对|
|Greeks_管理方法论主文档_v0.1.2-freeze_diff.md|已收到|Greeks freeze diff|参考；用于归档级修改核对|
|Trading_Concepts_方法论主文档_v0.1.2_patch_diff.md|已收到|Trading patch diff|参考；用于边界收紧核对|
|Trading_Concepts_方法论主文档_v0.1.2-freeze_diff.md|已收到|Trading freeze diff|参考；用于归档级修改核对|
|Chapter 7–16 章节包|本 session 未收到|章节忠实性回看|不使用；本任务不重审章节包正文|
|PDF 原文 01–08|已收到|原文背景/争议回看|原则上不使用；不得从 PDF 新增规则或重审正文|


## 2. 上游裁决承接

本 bridge 承接第一轮总一致性审计的 PASS WITH PATCH、v0.1.2-patch 二次复审 PASS、freeze 归档说明，以及第二轮下游可衍生性审计的 PASS WITH PATCH。承接方式为：不再修订方法论主体，不重审章节包，不回溯 PDF；只在 taxonomy bridge 层补齐 M-DS-01 至 M-DS-11 所要求的下沉边界。


核心承接裁决：两份主文档均为上游方法论边界材料，只可进入 taxonomy，不得直接生成字段、算法、YAML、参数、profile、runtime binding 或执行治理实例。Greeks §13 只能作为候选观察维度来源；Trading §8、§9.2、§11.3 只能作为风险规则、报告候选、禁止项来源；所有对象必须重新分配到 namespace、Phase、H/P/W、lineage 与 downstream gate。


|审计裁决|Bridge 承接方式|阻断对象|
|---|---|---|
|总一致性审计 PASS WITH PATCH|只承接已落地的边界修订；不重审 10 章正文|重新审计章节包 / PDF|
|v0.1.2-patch 二次复审 PASS|确认 freeze 可作为下游可衍生性审计上游|把 patch diff 当作生产规则|
|第二轮可衍生性审计 PASS WITH PATCH|在本 bridge 中完整处理 M-DS-01–M-DS-11|直接字段冻结 / 算法实现 / YAML instance|
|主文档非生产声明|转写为 namespace、forbidden registry、downstream gate|主文档直接生产化|


## 3. Bridge 总体架构

```text
方法论主文档
  ├─ Greeks 管理方法论主文档 v0.1.2-freeze
  ├─ Trading Concepts 方法论主文档 v0.1.2-freeze
  ├─ 下游可衍生性审计报告：M-DS-01–M-DS-11
  └─ 主题树 / 12 篇方法论：Phase、H/P/W、core/profile/runtime 边界
        ↓
Taxonomy Bridge（本文档）
  ├─ Namespace Taxonomy
  ├─ Phase / H-P-W Boundary
  ├─ Action Lifecycle Taxonomy
  ├─ Field Taxonomy Bridge
  ├─ Algorithm Taxonomy Bridge
  ├─ YAML / Config Taxonomy Bridge
  ├─ Forbidden Automation / Override Registry
  ├─ Lineage / Audit Metadata Contract
  └─ Downstream Gate
        ↓
下游文档族
  ├─ Field taxonomy → Field document（另审）
  ├─ Algorithm taxonomy → Algorithm document（另审）
  ├─ Parameter registry candidate → production parameter registry（另审）
  ├─ YAML schema prerequisite → YAML schema → YAML instance（逐级另审）
  ├─ Runtime binding prerequisite → runtime binding instance（另审）
  └─ Execution governance taxonomy → governance implementation（另审）
```


## 4. Phase 与 H/P/W 权限总表

|对象类型|Phase|H/P/W|可下沉到|禁止下沉到|说明|
|---|---|---|---|---|---|
|method_principle / core_constraint|Phase 1|H|documentation_warning / forbidden registry / downstream gate|production field / algorithm / YAML instance / runtime override|定义结构身份、Phase 权限链、md 语义权威与禁止下沉边界|
|raw exposure / raw Greeks / raw ledger|Phase 2|P|raw_field_candidate / calculation metadata|diagnostic / candidate action / governance decision|回答“当前事实是什么”；必须保留对象维度与 calculation basis|
|derived observation|Phase 2|P|derived_observation_candidate / display observation|decision / signal / action|例如 finite-move Delta 的计算结果；解释性输出必须上移 Phase 3|
|diagnostic / proxy / risk-equivalent / scenario-stressed|Phase 3|P|diagnostic_candidate / governance_input_candidate / manual_review_trigger|approved action / execution order|回答“状态可能意味着什么”；不产生最终授权|
|review note / trader note / model risk note|Phase 3|W|audit_metadata / manual_checklist|signal / production parameter / governance decision|弱观点只能辅助人工审查|
|candidate input package / repair proposal|Phase 3|P|candidate_input_package / governance handoff|approved action / executed action|候选输入包必须提交 Phase 4；不得直接执行|
|governance input validation / constraint stack check|Phase 4|H/P|governance_input_candidate / governance_decision_boundary|single proxy decision / Greek-only decision|校验输入与约束栈完整性；validation 不等于 decision|
|approval / block / manual review / rollback / post-action audit|Phase 4|H/P|governance_decision_boundary / audit_metadata|自动生成下一笔交易|只有 Phase 4 可产生治理裁决；执行后仍需审计|


## 5. Namespace Taxonomy

本文档中的 namespace 是 taxonomy label，不是 production field name、algorithm name 或 YAML key。下游若需命名，必须经过独立命名审计。


|Namespace|定义|允许对象|禁止对象|Phase|H/P/W|下游承接|
|---|---|---|---|---|---|---|
|method_principle|方法论原则载体，承载不预测 X、构造 F(X)、Greeks 非裁决器、md 语义权威等原则|H 层原则、source boundary、Phase 权限链|字段名、算法步骤、YAML key、runtime 值|Phase 1|H|方法论总纲、审计依据、forbidden registry|
|core_constraint|策略身份与硬约束载体|对象身份、母结构、constraint stack、profile 不得覆盖 core|可调参数、profile override、临场 runtime override|Phase 1|H|constraint stack prerequisite、forbidden override registry|
|raw_field_candidate|字段 taxonomy 的 raw 候选载体，不等于 production field|raw exposure、raw Greeks、raw ledger、timestamp、calculation basis|diagnostic、signal、approval、自然语言标题|Phase 2|P|Field taxonomy；需字段命名/类型/单位/lineage 复审|
|derived_observation_candidate|由 Phase 2 事实计算派生的观察载体|finite-move Delta 计算结果、display observation、calculation metadata|解释性诊断、候选动作、治理裁决|Phase 2|P|Field taxonomy / Algorithm taxonomy|
|diagnostic_candidate|Phase 3 解释性诊断载体，不等于 signal|up/down Delta、price-band Gamma、surface Vega、Alpha fair-value diagnostic、distribution/path-IV diagnostic|order、approval、direct trigger、production signal|Phase 3|P|Algorithm taxonomy / manual review trigger|
|candidate_input_package|提交 Phase 4 审查的候选输入包|diagnostic summary、lineage、assumption set、scenario set、review note、completeness check|approved action、execution instruction|Phase 3|P|governance handoff prerequisite|
|governance_input_candidate|Phase 4 约束栈可读取的输入候选|risk-equivalent Greeks、scenario-stressed Greeks、post-action legality check input|governance decision、approval、block|Phase 4|P|Execution governance taxonomy；必须 input_only 标注|
|governance_decision_boundary|治理裁决边界载体|approval、block、manual review、rollback decision、identity drift declaration|raw fact、diagnostic、candidate action 直接越权|Phase 4|H/P|Execution governance document；需人工/治理复审|
|audit_metadata|审计与 lineage 载体|source_document、source_section、review_status、version、validity、audit_log_required|交易动作、字段冻结、算法输出|Phase 1–4|P/W|所有下游文档的 lineage contract|
|manual_checklist|人工检查项载体|settlement review、object identity review、scenario-P/L review、documentation review|自动执行、自动批准、自动阻断|Phase 3–4|P/W|manual review procedure / governance checklist|
|manual_review_trigger|人工复核触发载体|Greeks diagnostic trigger、failure mode flag、review status missing、namespace conflict|approved action、order、runtime mutation|Phase 3–4|P|manual review queue；需 action lifecycle 分离|
|forbidden_automation|禁止自动化条款载体|Greek decision engine 禁令、direct hedge/roll/rebalance trigger 禁令|实现需求、待办功能、自动化 backlog|Phase 1|H|denylist / validation prerequisite|
|forbidden_override|禁止覆盖条款载体|profile 不得覆盖 core、runtime 不得覆盖 constraint stack、YAML 不得反向改写 md|profile setting、runtime flag、临场豁免|Phase 1|H|core constraint / runtime validation|
|parameter_slot_candidate|参数候选槽载体，不等于 production parameter|shock definition、price band、scenario set、tenor bucket、calendar convention|参数值、阈值、交易触发器|Phase 2–3|P|Parameter registry candidate；需审计后入册|
|schema_prerequisite|schema 设计前置要求载体，不等于 schema|required dimensions、namespace、validation、versioning、lineage、input_only|YAML schema、YAML instance、production key|Phase 1–3|H/P|YAML schema gate|
|runtime_binding_prerequisite|runtime binding 前置要求载体，不等于 runtime instance|core version、approved parameter set、profile、runtime mode、market snapshot、audit id|临场 override、未批准组合、执行实例|Phase 4|H/P|runtime binding gate|
|action_lifecycle|动作生命周期载体|candidate/approved/executed/post-action audit/rollback 状态|Phase 2 直接动作、Phase 3 直接批准|Phase 3–4|H/P|Algorithm taxonomy / execution governance|
|report_module_candidate|报告模块候选载体，不等于 dashboard schema|Greeks report candidate、risk display candidate、Trading report module candidate|field schema、YAML key、signal binding|Phase 2–3|P/W|report taxonomy；需 UI/schema 另审|


## 6. Action Lifecycle Taxonomy

动作生命周期必须分离：Phase 2 不得产生 candidate action；Phase 3 可以产生 candidate input package / manual review trigger，但不得产生 approved action；Phase 4 才能产生 governance decision。approved action 不是 executed action；executed action 必须进入 post-action audit；post-action audit 不得自动生成下一笔交易；rollback candidate 不等于 rollback decision。


|Lifecycle State|Phase|定义|允许输入|允许输出|禁止事项|下游承接|
|---|---|---|---|---|---|---|
|no_action_observation|Phase 2|事实或 raw observation 记录，无动作含义|raw ledger、raw Greeks、calculation metadata|display observation / audit metadata|不得生成 candidate action|raw field taxonomy|
|diagnostic_only|Phase 3|解释性诊断，仅说明状态含义|raw/derived observations、scenario assumptions|diagnostic note、manual checklist item|不得成为 signal 或 decision|diagnostic taxonomy|
|manual_review_trigger|Phase 3/4|触发人工复核，不携带执行授权|diagnostic flag、missing lineage、namespace conflict|review ticket / checklist|不得自动批准或自动阻断|manual review procedure|
|candidate_input_package|Phase 3|提交治理审查的输入包|diagnostic、assumption_set、scenario_set、lineage|governance handoff package|不得含 execution order|governance input validation|
|candidate_action|Phase 3|动作候选语义，仅供 Phase 4 审查|candidate input package、repair proposal|governance_input|不得写成 approved action|execution governance taxonomy|
|governance_input|Phase 4|constraint stack 可读取的审查输入|candidate_action、risk-equivalent Greeks、scenario-stressed Greeks、checklist|governance decision candidate context|不得等同治理裁决|constraint stack check|
|governance_decision|Phase 4|Phase 4 对候选作出的裁决|validated governance_input、constraint stack result|approval / block / manual review / rollback decision|不得由单一 proxy 或单一 Greek 产生|execution governance|
|approved_action|Phase 4|已获治理批准但尚未执行的动作状态|governance_decision=approval|execution-eligible action record|不等于 executed action；不得省略执行前校验|execution handoff|
|blocked_action|Phase 4|被治理约束阻断的动作状态|governance_decision=block|block record / audit metadata|不得转为执行命令|audit trail|
|executed_action|Phase 4|已经发生的执行事实|approved_action、execution fact|post_action_audit input|不得反向证明 candidate 合法|post-action audit|
|post_action_audit|Phase 4|执行后合法性与残余风险审计|executed_action、post-action Greeks、payoff shape、ledger fact|audit result / review note|不得自动生成下一笔交易|audit metadata / rollback candidate|
|rollback_candidate|Phase 4|由审计或治理发现形成的回滚候选|post_action_audit、constraint violation note|rollback input package|不等于 rollback decision|governance review|
|rollback_decision|Phase 4|治理层对 rollback candidate 的裁决|rollback_candidate、constraint stack|approval / block / manual review|不得由 audit 自动生成|execution governance|


## 7. Field Taxonomy Bridge

Field taxonomy bridge 只定义字段候选应归入哪一类、需要哪些维度、哪些聚合可行、哪些用法禁止。它不是 field document，不冻结字段名、类型、单位或 schema。


### 7.1 字段分类总表

|Field Category|Namespace|Phase|H/P/W|是否可成为 production field|前置条件|禁止事项|
|---|---|---|---|---|---|---|
|Phase 2 raw field candidates|raw_field_candidate|Phase 2|P|否，需 Field taxonomy 与 Field document gate|对象维度、calculation basis、timestamp、lineage|不得包含诊断、动作、自然语言报告标题|
|Phase 2 derived observation candidates|derived_observation_candidate|Phase 2|P|否|原始输入、计算口径、validity_window、display purpose|不得输出解释性结论或候选动作|
|Phase 3 diagnostic field candidates|diagnostic_candidate|Phase 3|P|否|raw/derived lineage、assumption_set、scenario_set、review status|不得成为 signal、approval 或 order|
|Phase 3 candidate input package fields|candidate_input_package|Phase 3|P|否|action lifecycle id、source diagnostics、completeness status|不得写成 approved action|
|Phase 4 governance input fields|governance_input_candidate|Phase 4|P|否|input_only=true、constraint stack reference、validity window|不得写成 governance decision|
|Phase 4 governance decision fields|governance_decision_boundary|Phase 4|H/P|只能在 Execution governance 文档复审后定义|approval authority、decision type、audit log|不得由字段 taxonomy 直接生成|
|audit metadata fields|audit_metadata|Phase 1–4|P/W|否|source、version、review_status、owner、audit_log_required|不得承载交易语义|
|manual checklist fields|manual_checklist|Phase 3–4|P/W|否|check item、owner、status、evidence link|不得自动化为执行算法|
|forbidden fieldization items|forbidden_automation / forbidden_override|Phase 1|H|否|forbidden item、reason、allowed alternative、severity|不得反向写成字段需求|
|field schema prerequisites|schema_prerequisite|Phase 1–3|H/P|否|required dimensions、namespace、aggregation contract、lineage contract|不得生成冻结字段名|


### 7.2 Greeks 字段候选映射

|Source Object|Taxonomy Placement|Phase|H/P/W|Required Dimensions|Aggregation Rule|Forbidden Use|Downstream Gate|
|---|---|---|---|---|---|---|---|
|raw Delta|raw_field_candidate|Phase 2|P|account / strategy object / underlying / portfolio id / lot / leg / side / option type / expiry / tenor / strike / moneyness / calculation basis / aggregation scope / timestamp|仅在同一 calculation basis、同一 aggregation_scope 且保留 tenor/leg/option type 维度后可聚合|Delta-neutral = risk-neutral；direct hedge trigger|Field taxonomy gate|
|raw Gamma|raw_field_candidate|Phase 2|P|account / strategy object / underlying / portfolio id / lot / leg / side / option type / expiry / tenor / strike / moneyness / calculation basis / aggregation scope / timestamp / price point|需保留 price point / price band；跨期限需等价规则|当前 spot net Gamma 作为完整 convexity 或 Gamma flip trigger|Field taxonomy gate|
|raw Vega|raw_field_candidate|Phase 2|P|account / strategy object / underlying / portfolio id / lot / leg / side / option type / expiry / tenor / strike / moneyness / calculation basis / aggregation scope / timestamp / volatility shock unit|需声明 shock unit 与 tenor；不得跨 surface 无条件净额|scalar net Vega = vol neutral|Field taxonomy gate|
|raw Theta|raw_field_candidate|Phase 2|P|account / strategy object / underlying / portfolio id / lot / leg / side / option type / expiry / tenor / strike / moneyness / calculation basis / aggregation scope / timestamp / calendar convention / financing basis|需与融资账本分离；不得与 expected profit 混同|positive Theta = safe carry|Field taxonomy gate|
|raw Rho|raw_field_candidate|Phase 2|P|account / strategy object / underlying / portfolio id / lot / leg / side / option type / expiry / tenor / strike / moneyness / calculation basis / aggregation scope / timestamp / rate curve bucket / currency basis|需按 curve、financing、FX、forward basis 分账|单一净 Rho 代表利率风险全貌|Field taxonomy gate|
|finite-move Delta|derived_observation_candidate|Phase 2|P|account / strategy object / underlying / portfolio id / lot / leg / side / option type / expiry / tenor / strike / moneyness / calculation basis / aggregation scope / timestamp / move definition / validity_window|计算结果保留为 derived observation；解释性输出进入 Phase 3|直接产生方向判断或 hedge rule|Field taxonomy gate|
|price-band Gamma|derived_observation_candidate / diagnostic_candidate|Phase 2→3|P|account / strategy object / underlying / portfolio id / lot / leg / side / option type / expiry / tenor / strike / moneyness / calculation basis / aggregation scope / timestamp / price band / direction|price band 规则必须另审；可用于 display/diagnostic|固定 price band trigger|Field taxonomy gate|
|shadow Gamma|diagnostic_candidate|Phase 3|P|account / strategy object / underlying / portfolio id / lot / leg / side / option type / expiry / tenor / strike / moneyness / calculation basis / aggregation scope / timestamp / scenario_set / assumption_set|只在声明 scenario_set 与 mapping 后进入诊断|单项动作批准器|Algorithm taxonomy gate|
|tenor Vega|raw_field_candidate / derived_observation_candidate|Phase 2|P|account / strategy object / underlying / portfolio id / lot / leg / side / option type / expiry / tenor / strike / moneyness / calculation basis / aggregation scope / timestamp / tenor bucket / shock unit|跨 tenor 聚合需 equivalence_rule 与 validity_window|无权重直接相加|Field taxonomy gate|
|grid / surface Vega|diagnostic_candidate|Phase 3|P|account / strategy object / underlying / portfolio id / lot / leg / side / option type / expiry / tenor / strike / moneyness / calculation basis / aggregation scope / timestamp / surface coordinate / grid schema version|grid/surface 只可在已审 schema prerequisite 下比较|固定 grid / correlation matrix 生产化|YAML schema gate|
|modified / shadow Theta|diagnostic_candidate|Phase 3|P|account / strategy object / underlying / portfolio id / lot / leg / side / option type / expiry / tenor / strike / moneyness / calculation basis / aggregation scope / timestamp / path assumption / financing basis|解释性诊断，不聚合为收益承诺|自动卖权利金或 carry rule|Algorithm taxonomy gate|
|decomposed Rho|diagnostic_candidate|Phase 3|P|account / strategy object / underlying / portfolio id / lot / leg / side / option type / expiry / tenor / strike / moneyness / calculation basis / aggregation scope / timestamp / curve bucket / basis source|按利率、融资、远期、货币分账后诊断|单一 Rho 裁决|Algorithm taxonomy gate|
|Alpha fair-value diagnostic|diagnostic_candidate|Phase 3|P|raw Greeks lineage / convexity rent basis / assumption_set|只能在声明 fair-value basis 后诊断|Alpha threshold / trading signal|Algorithm taxonomy gate|
|bleed / expiry-near / progressive Vega|diagnostic_candidate|Phase 3|P|expiry / tenor / path state / execution lag / scenario_set|不得跨产品无条件聚合；需保留 path / expiry context|自动 roll、自动 rebalance|Algorithm taxonomy gate|
|risk-equivalent Greeks|governance_input_candidate|Phase 3→4|P|equivalence_rule / assumption_set / scenario_set / aggregation_scope / validity_window / input_only=true|只在 equivalence_rule 明确时作输入；不得替代 raw exposure|真实风险等价或 governance decision|Execution governance gate|
|scenario-stressed Greeks|governance_input_candidate|Phase 3→4|P|scenario_set / scenario version / market snapshot / validity_window / input_only=true|按 scenario_set 内部聚合；不得跨 scenario 混合裁决|单一 stressed Greek 替代完整审查|Execution governance gate|
|post-action legality check input|governance_input_candidate / audit_metadata|Phase 4|P|executed_action id / post-action snapshot / constraint stack reference|只能作为 post-action audit 输入|自动生成下一笔交易|Post-action audit gate|


### 7.3 Trading Concepts 字段候选映射

|Source Object|Taxonomy Placement|Phase|H/P/W|Required Dimensions|Aggregation Rule|Forbidden Use|Downstream Gate|
|---|---|---|---|---|---|---|---|
|substitutability diagnostic|diagnostic_candidate|Phase 3|P|underlying / instrument identity / residual-risk map / validity_window|不可把替代品风险净额为零；需 residual-risk transformation 说明|proxy = equivalent truth；automatic substitution|Algorithm taxonomy gate|
|stack residual-risk map|diagnostic_candidate / governance_input_candidate|Phase 3→4|P|stack object / leg / lifecycle / residual risk / aging status|stack 内部需按对象身份与期限分层|stack 自动延续、自动拆回|Execution governance gate|
|segmentation / shape display|derived_observation_candidate / report_module_candidate|Phase 2→3|P/W|segment / shape coordinate / timestamp / display basis|仅同一 segment definition 下比较|dashboard schema / signal|Field taxonomy gate|
|tail / smile / distribution diagnostic|diagnostic_candidate|Phase 3|P|distribution assumption / skew state / path context / model version|需保留模型与样本口径；不得作为预测真相|vol bet execution action|Algorithm taxonomy gate|
|path-IV review|manual_checklist / diagnostic_candidate|Phase 3|P/W|path window / IV source / scenario_set / review_status|只作 review 输入；不得自动反推交易|direct vol bet trigger|Manual review gate|
|soft-hard Delta note|manual_checklist / diagnostic_candidate|Phase 3|P/W|Delta definition / path state / option structure / review note|仅作审查注记；不得自动切换|soft-hard Delta switch trigger|Manual review gate|
|Gamma interval / reversal note|manual_checklist / diagnostic_candidate|Phase 3|P/W|price interval / payoff shape / scenario context|只作区间/反转风险注记|Gamma flip trigger|Manual review gate|
|worst-path stress note|manual_checklist / governance_input_candidate|Phase 3→4|P/W|worst-path scenario / liquidity / execution lag / path cost|只能作为治理输入或人工 checklist|最差路径自动执行规则|Execution governance gate|
|settlement-flat|manual_checklist / governance_input_candidate|Phase 4|H/P|settlement basis / broker convention / expiry lifecycle / account|不得并入 Greek-flatness；必须 namespace 隔离|C1 Greeks 风险语言吞并 settlement check|Execution governance gate|
|object-identity-flat|manual_checklist / governance_decision_boundary|Phase 4|H/P|strategy object / object identity / lifecycle / source boundary|只能由治理层裁决身份是否保持|用净 Greek 判断对象身份|Execution governance gate|
|scenario-P/L flat|manual_checklist / governance_input_candidate|Phase 4|P|scenario_set / P/L path / liquidity / execution cost|与 Greek-flatness 分离；仅同一 scenario_set 下比较|P/L flat = risk neutral|Execution governance gate|
|report module candidates|report_module_candidate|Phase 2–3|P/W|module purpose / visibility / source document / review_status|只能按报告目的分组，不冻结字段名|Trading §9.2 报告模块直接变 dashboard schema|Report taxonomy gate|
|forbidden fieldization list|forbidden_automation / forbidden_override|Phase 1|H|forbidden item / source / reason / alternative carrier|不聚合；作为 denylist 审计|禁止项标题写成 field/YAML key|Downstream gate|


### 7.4 禁止字段化清单

|Forbidden Item|Source|Reason|Allowed Alternative|Downstream Gate|
|---|---|---|---|---|
|Greeks §13 表格|Greeks §13|候选观察维度，不是字段清单、字段冻结稿或 YAML key|schema_prerequisite / audit_metadata|Field taxonomy gate|
|Trading §9.2 报告模块候选|Trading §9.2|风险显示候选，不是 dashboard schema|report_module_candidate|Report taxonomy gate|
|Trading §11.3 自然语言标题|Trading §11.3|禁止项标题，不是字段名、算法步骤或 YAML key|forbidden_automation_clause / documentation_warning|YAML schema gate|
|Greek-flatness 与 settlement/object/scenario flatness 混合字段|Trading §10.3|namespace 混并会把 C1 Greeks 风险语言误写为 Trading governance 检查|schema_prerequisite / manual_checklist|Field taxonomy gate|
|net Greek = risk neutral 字段|Greeks §2 / §12|单一净额掩盖 tenor、strike、surface、path、execution 风险|documentation_warning|Forbidden registry gate|
|candidate action status 直接字段化为 approved|审计 M-DS-04|生命周期越权|action_lifecycle|Execution governance gate|


### 7.5 字段文档前置要求

字段文档生成前必须补齐：

1. 每个字段候选的 namespace、Phase、H/P/W、source_document、source_section、source_type、translation_strength。
2. 字段命名审计：不得直接复制 Greeks §13、Trading §9.2、Trading §11.3 的自然语言标题。
3. required dimensions contract：至少处理 account、strategy object、underlying、portfolio id、lot、leg、side、option type、expiry、tenor、strike、moneyness、calculation basis、aggregation scope、timestamp。
4. aggregation contract：明确哪些可聚合、何种条件下可聚合、何时必须保留 raw granularity。
5. namespace isolation：Greek-flatness 与 settlement-flat、object-identity-flat、scenario-P/L flat 必须隔离。
6. risk-equivalent Greeks contract：必须包含 equivalence_rule、assumption_set、scenario_set、aggregation_scope、validity_window、input_only=true。
7. audit metadata contract：source、version、review_status、owner、validity、rollback_policy、audit_log_required。
8. forbidden fieldization registry：net Greek = risk neutral、diagnostic as signal、natural language title as key 等必须阻断。


## 8. Algorithm Taxonomy Bridge

Algorithm taxonomy bridge 只定义算法候选分类、输入边界、输出边界、失败条件、no-action condition、manual review condition、anti-lookahead 与 governance handoff。它不是 algorithm implementation，不生成 hedge / roll / rebalance / execution algorithm。


### 8.1 算法分类总表

|Algorithm Category|Phase|H/P/W|Input Boundary|Output Boundary|Forbidden Output|Downstream Gate|
|---|---|---|---|---|---|---|
|Phase 2 factual calculation algorithm candidates|Phase 2|P|position/market/account facts、model inputs、calculation basis|raw exposure / raw Greeks / raw lifecycle fact|diagnostic、candidate、approval|Algorithm taxonomy gate|
|Phase 2 derived observation algorithms|Phase 2|P|raw facts、scenario-free calculation assumptions|derived observation / display observation|解释性结论、action|Algorithm taxonomy gate|
|Phase 3 diagnostic algorithms|Phase 3|P|raw/derived observations、assumption_set、scenario_set|diagnostic / review note / manual review trigger|signal、decision、order|Algorithm taxonomy gate|
|Phase 3 candidate input packaging algorithms|Phase 3|P|diagnostics、lineage、review status、completeness checks|candidate_input_package|approved action、execution instruction|Action lifecycle gate|
|Phase 3 manual review trigger algorithms|Phase 3|P/W|diagnostic flags、missing metadata、forbidden conflict|manual_review_trigger|automatic block/approval|Manual review gate|
|Phase 4 governance input validation algorithms|Phase 4|H/P|candidate_input_package、lineage、input_only fields|validated governance_input / rejection reason|governance decision|Execution governance gate|
|Phase 4 constraint check algorithms|Phase 4|H/P|validated input、constraint stack reference|constraint check result|single Greek decision|Execution governance gate|
|governance decision boundary / constraint-stack decision procedure taxonomy|Phase 4|H/P|constraint check result、authority、manual review result|decision type / procedure boundary: approval / block / manual review / rollback decision|executed action; algorithmic auto-approval; auto-block; automatic rollback; execution automation|Execution governance gate|
|post-action audit algorithms|Phase 4|P|executed_action、post-action ledger、post-action Greeks、payoff shape|audit result / rollback_candidate|next trade trigger|Post-action audit gate|
|documentation audit algorithms|Phase 1–4|P/W|source metadata、review_status、version、diff|documentation review status|trading action|Documentation audit gate|
|forbidden algorithmization items|Phase 1|H|forbidden registry|deny / warning / gate block|implementation requirement|Forbidden registry gate|
|algorithm schema prerequisites|Phase 1–3|H/P|input boundary、output boundary、failure/no-action/manual review conditions|algorithm taxonomy requirement|implementation code|Algorithm document gate|


### 8.2 Greeks 算法候选映射

|Source Object|Algorithm Placement|Phase|Input|Output|Failure Condition|Forbidden Use|Downstream Gate|
|---|---|---|---|---|---|---|---|
|raw Greeks calculation|Phase 2 factual calculation|Phase 2|position facts / market snapshot / model basis|raw Delta/Gamma/Vega/Theta/Rho by required dimensions|missing calculation basis or required dimensions|raw output used as decision|Algorithm taxonomy gate|
|finite-move Delta calculation|Phase 2 derived observation|Phase 2|raw position / move definition / calculation basis|finite-move Delta observation|move definition missing or scenario not versioned|hedge trigger or direction signal|Algorithm taxonomy gate|
|tenor Vega bucket calculation|Phase 2 factual / derived observation|Phase 2|raw Vega / tenor bucket definition / shock unit|tenor Vega observation|bucket definition or shock unit missing|cross-tenor netting without equivalence_rule|Field taxonomy gate|
|financing ledger separation|Phase 2 factual calculation|Phase 2|Theta facts / funding basis / account/currency facts|separated Theta / financing ledger facts|financing basis missing|Theta interpreted as expected profit|Field taxonomy gate|
|expiry / settlement lifecycle extraction|Phase 2 factual calculation|Phase 2|position ledger / expiry calendar / broker convention|raw lifecycle fact|calendar/broker convention missing|settlement action generated|Runtime binding prerequisite gate|
|segmentation / shape display calculation|Phase 2 derived observation|Phase 2|payoff facts / segment definition / display basis|segmentation / shape display observation|segment definition missing|display converted to signal|Report taxonomy gate|
|up/down Delta diagnostic|Phase 3 diagnostic|Phase 3|finite-move Delta / direction assumptions|Delta directionality diagnostic|up/down assumption missing|soft/hard switch trigger|Algorithm taxonomy gate|
|price-band Gamma diagnostic|Phase 3 diagnostic|Phase 3|raw Gamma / price band definition / scenario_set|Gamma interval diagnostic|price band unreviewed|Gamma flip trigger|Algorithm taxonomy gate|
|shadow Gamma scenario diagnostic|Phase 3 diagnostic|Phase 3|Gamma / price-vol-skew scenario / assumption_set|shadow Gamma diagnostic|scenario mapping unsupported|single-action approval|Algorithm taxonomy gate|
|surface / grid Vega diagnostic|Phase 3 diagnostic|Phase 3|tenor Vega / surface coordinate / grid schema version|surface/grid Vega diagnostic|grid schema unreviewed|fixed grid or vol action|YAML schema gate|
|Alpha fair-value diagnostic|Phase 3 diagnostic|Phase 3|Theta/Gamma/convexity rent basis / assumption_set|Alpha diagnostic|fair-value basis missing|Alpha threshold signal|Algorithm taxonomy gate|
|bleed / expiry-near / DdeltaDvol diagnostic|Phase 3 diagnostic|Phase 3|raw Greeks / expiry state / path assumption|bleed/expiry/DdeltaDvol diagnostic|expiry or path context missing|automatic roll/rebalance|Algorithm taxonomy gate|


### 8.3 Trading Concepts 算法候选映射

|Source Object|Algorithm Placement|Phase|Input|Output|Failure Condition|Forbidden Use|Downstream Gate|
|---|---|---|---|---|---|---|---|
|substitutability / proxy diagnostic|Phase 3 diagnostic|Phase 3|candidate proxy / residual-risk map / liquidity/settlement context|proxy diagnostic / residual-risk note|object identity or residual risk missing|automatic substitution|Algorithm taxonomy gate|
|distribution / skew / path-IV diagnostic|Phase 3 diagnostic|Phase 3|distribution data / skew state / path-IV review inputs|tail/smile/path diagnostic|model version or sample basis missing|vol bet execution action|Algorithm taxonomy gate|
|soft-hard Delta / Gamma reversal review|Phase 3 manual review trigger|Phase 3|Delta/Gamma diagnostic / payoff shape / interval note|review trigger / checklist|review basis missing|switch or flip trigger|Manual review gate|
|Greeks diagnostic → manual review trigger|Phase 3 manual review trigger|Phase 3|diagnostic fields / severity candidate / lineage|manual_review_trigger|severity rule unreviewed|approval or order|Action lifecycle gate|
|failure mode flags|Phase 3 diagnostic / review trigger|Phase 3|diagnostic taxonomy / source boundary / review status|failure-mode flag|flag taxonomy missing|automatic block or rollback|Manual review gate|
|action candidate completeness check|Phase 3 candidate input packaging|Phase 3|candidate draft / required diagnostics / lineage / checklist status|candidate_input_package completeness result|required metadata missing|candidate treated as approved|Action lifecycle gate|
|governance input validation|Phase 4 governance input validation|Phase 4|candidate package / input_only fields / lineage|validated or rejected governance input|input_only or source missing|governance decision|Execution governance gate|
|post-action Greeks check|Phase 4 post-action audit|Phase 4|executed_action / post-action raw Greeks / pre-action reference|post-action Greeks audit result|executed action id missing|next action trigger|Post-action audit gate|
|post-hedge payoff shape check|Phase 4 post-action audit / Phase 3 diagnostic candidate|Phase 3→4|payoff shape before/after / hedge record / scenario_set|shape check result|scenario_set missing|approval or automatic follow-up|Post-action audit gate|
|stack hedge aging audit|Phase 4 post-action audit|Phase 4|stack ledger / hedge age / validity_window / residual-risk map|aging audit result / review trigger|validity window missing|automatic unwind/extension|Post-action audit gate|
|dynamic hedge residual / path cost audit|Phase 4 post-action audit|Phase 4|executed hedge path / transaction cost / path P/L|residual/path-cost audit|path facts incomplete|new action automation|Post-action audit gate|
|documentation review status check|documentation audit|Phase 1–4|source_document / source_section / review_status / version|documentation gate pass/block|review_status missing|production eligibility without review|Documentation audit gate|


### 8.4 禁止算法化清单

|Forbidden Item|Source|Reason|Allowed Alternative|Downstream Gate|
|---|---|---|---|---|
|主文档直接生成 hedge / roll / rebalance algorithm|Greeks §12；Trading §11|主文档只给方法论边界，不给执行 I/O、失败条件、no-action condition|schema_prerequisite / manual_checklist|Algorithm document gate|
|diagnostic algorithm 输出 signal|审计 M-DS-09|诊断只解释状态，不授权动作|manual_review_trigger|Algorithm taxonomy gate|
|candidate generation 输出 approved action|审计 M-DS-04|candidate / approved / executed 必须分离|action_lifecycle|Action lifecycle gate|
|governance input validation 输出 governance decision|审计 M-DS-04 / M-DS-09|validation 是输入校验，不是裁决|governance_input_candidate|Execution governance gate|
|post-action audit 自动生成下一笔交易|审计 M-DS-04|审计是回看与约束检查，不是动作生成器|audit_metadata / rollback_candidate|Post-action audit gate|
|forbidden clauses 反向算法化|审计 M-DS-11|禁令只能作为 denylist 或 gate，不是实现需求|forbidden_automation_clause|Forbidden registry gate|


### 8.5 算法文档前置要求

算法文档生成前必须补齐：

1. Algorithm taxonomy 复审通过；不得从主文档直接进入 implementation。
2. 每个算法候选必须定义 input boundary、output boundary、failure condition、no-action condition、manual review condition。
3. 必须定义 anti-lookahead requirement：backtest 中不得使用未来 market snapshot、post-hoc scenario selection、事后 review_status。
4. 必须区分 backtest/live：回测输出不得直接变 live action；live 输出必须经过 runtime binding 与 execution governance gate。
5. 必须完成 action lifecycle schema：candidate action、approved action、executed action、post-action audit、rollback candidate、rollback decision 分离。
6. governance handoff 必须包含 candidate package id、governance handoff id、input_only 标记、constraint stack reference。
7. post-action audit algorithm 只能输出 audit result、review note、rollback_candidate；不得自动生成下一笔交易。
8. documentation audit algorithm 只能输出 review_status / block reason；不得输出交易动作。


## 9. YAML / Config Taxonomy Bridge

YAML / Config bridge 只定义 schema prerequisite、config boundary、override boundary 与 validation prerequisite。它不生成 YAML schema，不生成 YAML instance，不创建 production YAML key，不设置任何数值阈值或参数值。


### 9.1 YAML / Config 分类总表

|Config Category|Phase|H/P/W|是否可调|是否允许 profile override|是否允许 runtime override|Downstream Gate|
|---|---|---|---|---|---|---|
|parameter_slot_candidate|Phase 2–3|P|可调但只限候选槽；不得赋值|限制性允许，需不得覆盖 core|不允许临场 override constraint stack|Parameter registry gate|
|strategy_core_reference|Phase 1|H|不可调|不允许|不允许|Strategy core gate|
|strategy_config_boundary|Phase 1|H/P|H 不可调；P 需审计|P 可限制性允许；H 禁止|禁止覆盖 core/constraint stack|Strategy config gate|
|profile_config_boundary|Phase 4 binding 前置|P|可绑定已批准对象|允许但不得覆盖 core|不得临场覆盖硬约束|Profile config gate|
|deployment_config_boundary|Phase 4 binding 前置|P|可按 broker/account/runtime 绑定|允许但需审计|不得覆盖 constraint stack|Deployment config gate|
|runtime_binding_prerequisite|Phase 4|H/P|只绑定已批准版本|不允许 profile 改写 core|不允许 runtime 改写方法论或约束|Runtime binding gate|
|constraint_stack_config_candidate|Phase 4|H/P|H 不可调；P 需版本化|不允许覆盖 H|不允许覆盖 stack|Execution governance gate|
|audit_config_candidate|Phase 1–4|P/W|可配置审计视图与 owner|可显示层调整；不得改变审计义务|不允许关闭必要 audit log|Audit config gate|
|forbidden_yaml_items|Phase 1|H|不可调|不允许|不允许|YAML schema gate|
|forbidden_override_items|Phase 1|H|不可调|不允许|不允许|Runtime binding gate|
|schema_namespace_prerequisites|Phase 1–3|H/P|namespace 本身需审计，不临场调|不允许绕过 namespace 隔离|不允许 runtime 合并 namespace|YAML schema gate|
|validation_rule_prerequisites|Phase 1–4|H/P|H 规则不可调；P 规则需版本化|不允许覆盖 H validation|不允许关闭 H validation|Validation gate|


### 9.2 Parameter Slot Candidates

|Candidate Slot|Source|H/P/W|Adjustable|Required Metadata|Forbidden Use|Downstream Gate|
|---|---|---|---|---|---|---|
|shock definition|Greeks §13 / §2.4|P|候选可调；不设数值|source / assumption_set / validity_window / owner / review_status|direct trigger / unreviewed threshold|Parameter registry gate|
|price band|Greeks §5 / §13|P|候选可调；不设区间值|source / scenario_set / aggregation_scope / version|Gamma flip trigger|Parameter registry gate|
|scenario set|Greeks §2.3.1 / Trading §6–7|P|候选可调；需版本化|scenario_set_version / valid_from / valid_to / assumption_set|governance decision shortcut|Parameter registry gate|
|tenor bucket|Greeks §6 / 主题树 C1|P|候选可调|tenor definition / equivalence_rule / aggregation_rule|cross-tenor netting without rule|Parameter registry gate|
|grid / surface schema|Greeks §6 / §13|P|候选 schema；不设具体 grid|surface coordinate / model version / review_status|fixed production grid|YAML schema gate|
|calendar convention|Greeks §7 / Trading §4|P|按市场/产品候选绑定|calendar source / broker convention / version|settlement action automation|Profile config gate|
|financing basis|Greeks §7|P|候选可调，需 account/currency lineage|account / currency / rate source / owner|Theta-profit conflation|Parameter registry gate|
|rate curve bucket|Greeks §7|P|候选可调|curve source / currency / bucket definition / valid window|single Rho decision|Parameter registry gate|
|segmentation bucket|Trading §5|P|候选可调；不设宽度|segment definition / product scope / version|universal grid|Parameter registry gate|
|display bucket|Trading §9.2 / Greeks §13|P/W|可配置显示，不绑定动作|display purpose / visibility / review_status|dashboard signal|Report taxonomy gate|
|report module visibility|Trading §9.2|P/W|可配置显示|module purpose / source / owner / review_status|YAML key / field schema|Report taxonomy gate|
|underlying / account / broker / runtime mode binding|12 篇 00A / 主题树 A8|P|只能绑定已批准 profile|profile version / deployment owner / runtime mode|profile override core|Runtime binding gate|
|calculation basis|Greeks §2.4 / §10.2|P|可选择已批准口径|basis source / model version / timestamp|basis 混合净额|Field taxonomy gate|
|market snapshot|Greeks §10.2 / runtime audit|P|运行时生成，不临场覆盖|timestamp / data source / valid window|lookahead / post-hoc selection|Runtime binding gate|
|model version|Greeks §10.2 / Trading §6|P|只能选择已批准版本|model id / version / owner / review_status|model output as truth|Algorithm taxonomy gate|
|scenario set version|Greeks §13 / Trading §6–7|P|只能引用已批准版本|scenario_set_version / valid_from / valid_to|post-hoc scenario selection|Runtime binding gate|
|candidate package id|审计 M-DS-04|P|运行时生成|candidate lifecycle state / lineage / owner|approved action id 混用|Action lifecycle gate|
|governance handoff id|审计 M-DS-04|P|运行时生成|handoff source / validation status / receiver|execution id 混用|Execution governance gate|
|review status|审计 M-DS-10 / documentation|P/W|可更新但需 audit log|review_status / reviewer / version / timestamp|production eligibility without review|Documentation audit gate|
|production eligibility flag|审计 M-DS-01 / M-DS-11|H/P|只能由 gate 生成|gate result / review authority / version|手工或 profile 直接设 true|Downstream gate|
|forbidden automation registry|审计 M-DS-11|H|不可调|forbidden item / severity / allowed alternative / version|实现需求 backlog|Forbidden registry gate|
|forbidden override list|审计 M-DS-11|H|不可调|override target / reason / severity / audit requirement|profile/runtime override|Runtime binding gate|
|constraint stack reference|主题树 B2 / 12 篇 00A|H/P|只能引用已批准版本|constraint stack version / source / owner|single proxy substitute|Execution governance gate|
|audit lineage reference|审计 M-DS-10 / lineage contract|P|运行时/文档生成|source_document / source_section / version / audit_log|missing lineage production|Audit gate|


### 9.3 Strategy / Profile / Runtime Boundary

|Object|Belongs To|Override Allowed|Required Approval|Forbidden Override|Audit Requirement|
|---|---|---|---|---|---|
|strategy core identity|strategy_core_reference|否|core version upgrade approval|profile / YAML / runtime 改写对象身份|versioned source + audit trail|
|H 层原则|method_principle / core_constraint|否|methodology governance approval|参数化、profile override、runtime override|source lock + review status|
|Phase 权限链|core_constraint|否|methodology governance approval|Phase 2→action、Phase 3→approval|constraint stack validation|
|P 层参数候选|parameter_slot_candidate|限制性允许|parameter registry review|未经审计成为 production parameter|parameter lineage + backtest/live distinction|
|profile binding|profile_config_boundary|允许绑定，不允许覆盖 core|profile approval|覆盖 strategy core / constraint stack|runtime binding audit|
|runtime binding|runtime_binding_prerequisite|只允许引用已批准版本|runtime gate approval|临场改写 md 语义权威|immutable run id + audit log|
|report visibility|report_module_candidate|允许显示配置|report taxonomy review|绑定动作或 trigger|UI/report audit|


### 9.4 Constraint Stack / Audit Config Candidates

|Config Candidate|Namespace|Phase|H/P/W|Use|Forbidden Use|Downstream Gate|
|---|---|---|---|---|---|---|
|constraint stack reference|schema_prerequisite / runtime_binding_prerequisite|Phase 4|H/P|确保治理裁决读取完整约束栈|单一 proxy 或单一 Greek 替代|Execution governance gate|
|forbidden automation registry|forbidden_automation|Phase 1|H|阻断自动化越权|反向变成实现需求|Forbidden registry gate|
|forbidden override list|forbidden_override|Phase 1|H|阻断 profile/runtime/YAML 覆盖 core|临场豁免|Runtime binding gate|
|input_only marker for governance inputs|governance_input_candidate|Phase 4|H/P|确保 risk-equivalent / scenario-stressed Greeks 不变 decision|governance input 变 decision|Execution governance gate|
|namespace isolation validation|schema_prerequisite|Phase 1–3|H|隔离 Greek-flatness 与 non-Greek checks|C1 吞并 settlement/object/scenario flatness|YAML schema gate|
|audit lineage reference|audit_metadata|Phase 1–4|P|保留 source、version、review_status|无 lineage 下沉|Audit gate|
|rollback policy reference|audit_metadata / action_lifecycle|Phase 4|P|定义 audit 之后如何进入 rollback candidate/decision|post-action audit 自动交易|Post-action audit gate|


### 9.5 禁止 YAML 化清单

|Forbidden Item|Source|Reason|Allowed Alternative|Downstream Gate|
|---|---|---|---|---|
|H 层原则|主题树 A1/A3/A7；12 篇 00A|身份约束不可参数化|method_principle|YAML schema gate|
|F(X)|主题树 A1；12 篇 00A|结构响应函数语义，不是配置项|method_principle|Strategy core gate|
|Phase 权限链本身|主题树 B2；12 篇 00A|权限链是硬约束，不是 profile 值|core_constraint|Runtime binding gate|
|md 语义权威|主题树 A7；12 篇 00A|YAML 不得反向成为语义源|forbidden_override_clause|YAML schema gate|
|strategy core identity|主题树 A4/A8；12 篇 00A|对象身份不能由 profile/runtime 改写|core_constraint|Strategy core gate|
|Greeks 决策器|Greeks §2 / §12|Greeks 不是治理裁决器|forbidden_automation_clause|Execution governance gate|
|direct hedge trigger|Trading §11；审计 M-DS|主文档不支持执行触发器|forbidden_automation_clause|Algorithm document gate|
|direct roll trigger|Trading §11；主题树 B3|roll 是功能迁移语义，不是未审触发器|manual_checklist|Execution governance gate|
|direct rebalance trigger|Greeks §12；Trading §11|缺少执行 I/O、no-action、governance handoff|forbidden_automation_clause|Execution governance gate|
|Gamma flip trigger|Trading §7.4 / §11|Gamma 反转是 review 概念，不是自动触发器|manual_review_trigger|Manual review gate|
|soft-hard Delta switch trigger|Trading §7.4 / §11|soft/hard Delta 只能作审查语义|manual_checklist|Manual review gate|
|vol bet execution action|Trading §7.5 / §11|波动率下注小节不得生产化为动作|documentation_warning|Execution governance gate|
|unreviewed DTE / moneyness / strike / ratio / threshold|Greeks §12；Trading §11|主文档未授权生产参数|parameter_slot_candidate|Parameter registry gate|
|Trading §11 禁止项|Trading §11|禁止项标题不是 YAML key|forbidden_automation_clause|YAML schema gate|
|Greeks §12 禁止误用项|Greeks §12|禁止误用不能反向实现|documentation_warning|YAML schema gate|
|natural language report titles as YAML keys|Trading §9.2 / §11.3|自然语言标题未经过 schema 命名审计|report_module_candidate|Report taxonomy gate|
|profile override core|主题树 A8；12 篇 00A|profile 只绑定实例，不改 core|forbidden_override_clause|Runtime binding gate|
|runtime override constraint stack|主题树 B2/A8；12 篇 00A|runtime 不得覆盖硬约束|forbidden_override_clause|Runtime binding gate|


### 9.6 YAML/schema 前置要求

YAML schema 设计前必须补齐：

1. schema_namespace_prerequisites：method_principle、core_constraint、raw_field_candidate、diagnostic_candidate、governance_input_candidate、forbidden_automation、forbidden_override 等 namespace 不得混用。
2. validation_rule_prerequisites：H 层原则、Phase 权限链、md 语义权威、constraint stack、profile 不得覆盖 core、runtime 不得覆盖 constraint stack。
3. parameter_slot_candidate 审计：所有 shock、price band、scenario set、tenor bucket、grid/surface schema、segmentation bucket 只能作为候选槽，不得带数值。
4. runtime_binding_prerequisite：runtime 只能引用已批准 core version、parameter set、profile、runtime mode 与 scenario set version。
5. forbidden_yaml_items 与 forbidden_override_items 必须版本化、不可 profile override、不可 runtime override。
6. YAML schema 不得反向成为语义权威源；语义权威仍在 md 方法论与经审计的 taxonomy。
7. YAML instance 当前禁止生成；必须等 YAML schema gate 单独复审通过。


## 10. Forbidden Automation / Forbidden Override Registry

本注册表中的 forbidden item 不得反向变成实现需求。allowed alternative carrier 只能用于承载警告、审计、人工复核、schema prerequisite 或禁令条款。


|ID|Forbidden Item|Source|Forbidden Type|Reason|Allowed Alternative Carrier|Severity|Downstream Gate|
|---|---|---|---|---|---|---|---|
|FA-01|Greek decision engine|Greeks §2 / §12|forbidden action automation|Greeks 是观察/诊断/治理输入，不是裁决器|forbidden_automation_clause|P0|Execution governance gate|
|FA-02|net Greek = risk neutral|Greeks §2.3 / §12|forbidden inference|净额掩盖期限、行权价、曲面、路径、执行风险|documentation_warning|P0|Field taxonomy gate|
|FA-03|direct hedge trigger|Greeks §12；Trading §11|forbidden action automation|主文档不足以授权 hedge execution|forbidden_automation_clause|P0|Algorithm document gate|
|FA-04|direct roll trigger|Trading §11；主题树 B3|forbidden action automation|roll 需要功能迁移、治理与生命周期审查|manual_checklist|P0|Execution governance gate|
|FA-05|direct rebalance trigger|Greeks §12；Trading §11|forbidden action automation|rebalance 需要 action lifecycle 与 Phase 4 approval|forbidden_automation_clause|P0|Execution governance gate|
|FA-06|Gamma flip trigger|Trading §7.4 / §11|forbidden action automation|Gamma reversal/flip 只能进入 review|manual_review_trigger|P1|Manual review gate|
|FA-07|soft-hard Delta switch trigger|Trading §7.4 / §11|forbidden action automation|soft/hard Delta 不授权切换动作|manual_checklist|P1|Manual review gate|
|FA-08|vol bet execution action|Trading §7.5 / §11|forbidden action automation|Trading Concepts 不等于波动率下注执行手册|documentation_warning|P0|Execution governance gate|
|FA-09|unreviewed DTE / moneyness / strike / ratio / threshold|Greeks §12；Trading §11|forbidden yamlization / parameterization|未审参数不得生产化|parameter_slot_candidate|P0|Parameter registry gate|
|FA-10|natural language report title as field or YAML key|Greeks §13；Trading §9.2 / §11.3|forbidden naming reuse|自然语言标题未经过 schema 命名审计|report_module_candidate|P1|Report taxonomy gate|
|FO-01|profile override strategy core|主题树 A8；12 篇 00A|forbidden profile override|profile 不得改写 core|forbidden_override_clause|P0|Runtime binding gate|
|FO-02|runtime override constraint stack|主题树 B2/A8；12 篇 00A|forbidden runtime override|runtime 不得绕过硬约束|forbidden_override_clause|P0|Runtime binding gate|
|FY-01|YAML as semantic authority|主题树 A7；12 篇 00A|forbidden yamlization|md 方法论语义权威不得被 YAML 反向改写|forbidden_override_clause|P0|YAML schema gate|
|FI-01|forbidden clauses as implementation requirements|审计 M-DS-11|forbidden inference|禁止项只能作为 denylist/gate，不是待实现功能|forbidden_automation_clause|P1|Forbidden registry gate|
|AL-01|candidate action as approved action|审计 M-DS-04|forbidden action lifecycle merge|candidate 与 approved 必须分离|action_lifecycle|P0|Action lifecycle gate|
|GD-01|governance input as governance decision|审计 M-DS-04 / M-DS-09|forbidden inference|input 只能进入 constraint stack，不是裁决|governance_input_candidate|P0|Execution governance gate|
|DG-01|diagnostic as signal|审计 M-DS-09；Greeks §10|forbidden algorithmization|diagnostic 不授权执行|manual_review_trigger|P0|Algorithm taxonomy gate|
|PA-01|post-action audit as next trade trigger|审计 M-DS-04|forbidden action automation|post-action audit 不得自动生成下一笔交易|audit_metadata|P0|Post-action audit gate|


## 11. Lineage / Audit Metadata Contract

|Metadata|Required For|Purpose|Allowed Values / Format|Blocking If Missing|
|---|---|---|---|---|
|source_document|全部 taxonomy object|锁定来源文档|文件名 / 版本号|是|
|source_section|全部 taxonomy object|定位原始段落或章节|section label / heading|是|
|source_type|全部 taxonomy object|区分来源性质|method principle / risk warning / diagnostic concept / candidate observation / report candidate / audit note / forbidden clause / governance boundary / schema prerequisite|是|
|source_strength|全部 taxonomy object|标明来源强度|direct source / methodology translation / audit裁决 / upper-boundary reference|是|
|translation_strength|全部 taxonomy object|标明转译强度|direct / bounded translation / derived candidate / audit-only / forbidden inference|是|
|Phase|全部 taxonomy object|权限分层|Phase 1 / Phase 2 / Phase 3 / Phase 4|是|
|H/P/W|全部 taxonomy object|对象权限等级|H / P / W|是|
|namespace|全部 taxonomy object|命名空间隔离|本文第 5 节 namespace|是|
|machine_readability|全部 taxonomy object|说明能否机器读取|none / metadata-only / candidate-readable / validation-readable / execution-forbidden|是|
|downstream_allowed|全部 taxonomy object|允许下游承接范围|Field taxonomy / Algorithm taxonomy / Parameter registry candidate / schema prerequisite / audit / checklist 等|是|
|downstream_forbidden|全部 taxonomy object|禁止下沉范围|production field / implementation / YAML instance / runtime override / execution automation 等|是|
|required_dimensions|field / observation / diagnostic / governance input|保留对象维度|对象维度清单或 N/A|缺失则阻断对应字段/算法 gate|
|aggregation_allowed|field / observation / diagnostic|标明是否可聚合|yes / no / conditionally|是|
|aggregation_rule_required|field / observation / diagnostic|标明聚合规则是否前置|yes / no / N/A|conditional yes 时阻断|
|input_only|governance input / risk-equivalent / scenario-stressed|防止输入变裁决|true / false / N/A|governance input 缺失则阻断|
|decision_allowed|全部 taxonomy object|防止越权裁决|true only for governance_decision_boundary；其余 false|是|
|profile_override_allowed|config / parameter / profile object|控制 profile 权限|true / false / restricted|是|
|runtime_override_allowed|runtime / config object|控制 runtime 权限|true / false / restricted|是|
|review_status|全部下游候选|记录复审状态|draft / reviewed / approved / blocked / deprecated|是|
|owner|全部下游候选|定义责任人或责任域|methodology / field / algorithm / parameter / governance / audit owner|是|
|version|全部 taxonomy object|版本控制|semantic version / date-stamped version|是|
|valid_from|P/W 对象与 runtime 引用|防止事后选择|date/time / version activation|需要时阻断|
|valid_to|P/W 对象与 runtime 引用|定义失效窗口|date/time / open-ended with review|需要时阻断|
|rollback_policy|config / governance / runtime / action lifecycle|定义回滚边界|none / manual review / governance decision required / deprecated|Phase 4 对象缺失则阻断|
|audit_log_required|全部生产前对象|定义审计日志义务|true / false；H/P 生产前通常 true|需要时阻断|


## 12. Downstream Gate

|Gate|Allowed Input|Required Prerequisite|Forbidden Input|Output Scope|Blocking Condition|Review Requirement|
|---|---|---|---|---|---|---|
|Field taxonomy gate|method_principle、raw/derived/diagnostic/governance input candidates、schema prerequisites|namespace、Phase、H/P/W、lineage、required_dimensions|production field、YAML key、algorithm step、natural language title direct copy|字段分类、对象维度、禁止字段化清单|missing Phase/H-P-W/namespace/lineage；混用 Greek-flatness 与 non-Greek checks|字段候选是否仍越权为 production field|
|Field document gate|已复审 Field taxonomy、字段命名策略、类型/单位/lineage contract|Field taxonomy PASS、field naming review、aggregation contract|主文档原文直接复制、未审报告标题、禁止项标题|字段文档草案，不含 YAML instance|缺 required_dimensions / aggregation_rule / source lineage|字段名是否被误当生产冻结|
|Algorithm taxonomy gate|Field taxonomy、algorithm categories、input/output boundary、failure/no-action/manual review condition|action lifecycle、anti-lookahead、backtest/live distinction、governance handoff|execution algorithm、order logic、direct trigger|算法分类与候选 I/O 边界|diagnostic=signal；candidate=approval；validation=decision|算法 taxonomy 是否仍混层|
|Algorithm document gate|已复审 Algorithm taxonomy、字段文档、lifecycle schema、governance handoff|Algorithm taxonomy PASS、I/O contract review、failure condition|hedge/roll/rebalance implementation from主文档|算法文档草案，不含执行自动化|缺 no-action/manual review/failure/anti-lookahead|是否越界到 execution rule|
|Parameter registry gate|parameter_slot_candidate、scenario/schema prerequisites、P 层假设|参数三册边界、owner、version、review status、validity|H 原则、strategy core、未审阈值/DTE/moneyness/strike/ratio|参数候选注册表或入册申请|candidate 被写成 production；缺 source/validity|P 层是否有证伪和回滚要求|
|YAML schema gate|schema_prerequisite、namespace、validation rule prerequisite、forbidden registry|Field/Algorithm taxonomy PASS、namespace isolation、forbidden override list|YAML instance、profile override core、natural title as key|YAML schema 草案前置说明或 schema design brief|H 原则 YAML 化；缺 validation/lineage/versioning|schema 是否反向成为语义权威|
|YAML instance gate|已批准 YAML schema、approved parameter set、approved profile、runtime binding prerequisite|schema PASS、parameter registry approval、profile approval|主文档、taxonomy bridge、candidate slot、unreviewed parameters|原则上本 bridge 阶段不输出 instance|任何 H override、未批准引用、runtime override constraint stack|必须单独复审；当前不允许生成|
|Backtest harness gate|Field/Algorithm taxonomy、approved candidate parameters、anti-lookahead rules|data lineage、timestamp、valid_from/to、backtest/live distinction|未来数据、post-hoc scenario selection、execution governance shortcut|backtest harness requirement，不含 live execution|anti-lookahead 缺失；review_status 缺失|回测结果是否反向改写 H 层|
|Runtime binding gate|approved core reference、approved parameter set、profile、deployment、runtime mode|runtime_binding prerequisite、forbidden override validation、audit id|taxonomy candidate、unapproved profile、runtime override|runtime binding design / instance 需另审|core/profile/constraint stack 不一致；缺 audit log|runtime 是否只引用已批准版本|
|Execution governance gate|candidate input package、validated governance input、constraint stack、manual review result|action lifecycle、governance authority、post-action audit plan|diagnostic、single Greek、profile override、YAML as decision|governance decision / audit trail taxonomy|candidate=approved；approved=executed；post-audit=next trigger|每次进入执行治理前必须复审 lifecycle 与 constraint stack|


## 13. 最小 Patch 对照表

|Patch ID|审计问题|Bridge 中的处理位置|是否完全承接|后续是否需复审|
|---|---|---|---|---|
|M-DS-01|两份主文档只可作为 taxonomy 上游，不得直接生成字段/算法/YAML|0、2、12、14|是|Field/Algorithm/YAML 下游 gate 需复审|
|M-DS-02|Greeks §13 候选观察维度不是字段清单/冻结稿/YAML key|2、7.4、10|是|Field taxonomy gate 需复审|
|M-DS-03|Trading §8/§9.2/§11.3 不是 production field/algorithm/YAML key|2、7.4、9.5、10|是|Report taxonomy 与 YAML schema gate 需复审|
|M-DS-04|建立 action lifecycle 前置边界|6、8、10、12|是|Action lifecycle gate 必须复审|
|M-DS-05|finite-move Delta 标为 Phase 2 derived observation；解释性输出 Phase 3|7.2、8.2|是|Algorithm taxonomy gate 需核对|
|M-DS-06|字段 taxonomy 必须处理 account/strategy/underlying/portfolio/lot/leg/side/option/expiry/tenor/strike/moneyness/basis/scope/timestamp|7.2、11、12|是|Field taxonomy gate 必须复审|
|M-DS-07|risk-equivalent Greeks 强制 equivalence_rule/assumption_set/scenario_set/aggregation_scope/validity_window/input_only=true|7.2、9.4、11|是|Execution governance gate 需核对|
|M-DS-08|Greek-flatness 与 non-Greek checks namespace 隔离|5、7.3、9.4、10|是|Field/YAML schema gate 需核对|
|M-DS-09|hedge governance/execution constraint/post-action audit 只能作 input/audit/checklist，不得自动执行|8、10、12|是|Algorithm document gate 需复审|
|M-DS-10|所有 taxonomy object 标注 H/P/W|4、5、7、8、9、11|是|全部下游 gate 均需核对|
|M-DS-11|建立 forbidden override/automation 边界|9.5、10、12|是|YAML schema / runtime binding gate 必须复审|


## 14. 最终裁决

|问题|裁决|条件 / 阻断|
|---|---|---|
|是否可以进入 Field taxonomy？|可以|以本文档为上游；需复审 namespace、Phase、H/P/W、lineage、required dimensions|
|是否可以进入 Field document？|不直接可以|必须先完成 Field taxonomy gate；字段命名、类型、单位、aggregation contract 另审|
|是否可以进入 Algorithm taxonomy？|可以|以本文档第 8 节为上游；需复审 input/output/failure/no-action/manual review/governance handoff|
|是否可以进入 Algorithm document？|不直接可以|必须先完成 Algorithm taxonomy gate 与 Action lifecycle gate；不得生成 execution algorithm|
|是否可以进入 Parameter registry？|只能进入 parameter_slot_candidate / 入册设计|不得生成 production parameter；所有 P 层候选需 owner、version、review_status、validity 与回滚要求|
|是否可以进入 YAML schema？|只能进入 YAML/schema prerequisite 与 schema design brief|不得生成 YAML schema final；需先复审 namespace、validation、forbidden override|
|是否可以进入 YAML instance？|不可以|当前阶段禁止生成；需 schema、parameter、profile、runtime binding 逐级复审|
|是否可以进入 runtime binding instance？|不可以|只能进入 runtime_binding_prerequisite；实例需已批准 core/parameter/profile/runtime mode|
|是否可以进入 execution governance？|只能进入 execution governance taxonomy / prerequisite|不得进入执行自动化；governance decision 与 executed action 需单独治理流程|
|哪些步骤必须先复审？|Field taxonomy、Algorithm taxonomy、Parameter slot registry、YAML schema prerequisite、Action lifecycle、Runtime binding prerequisite、Execution governance gate|任何缺少 lineage、H/P/W、Phase、namespace、forbidden registry 的对象均阻断下游|


最终裁决：

```text
BRIDGE PASS：可作为后续 taxonomy 上游。

允许下一步：Field taxonomy、Algorithm taxonomy、Parameter slot candidate taxonomy、YAML schema prerequisite、Runtime binding prerequisite、Execution governance taxonomy。

禁止下一步：Field freeze、Algorithm implementation、YAML instance、profile override core、runtime override constraint stack、execution automation。
```

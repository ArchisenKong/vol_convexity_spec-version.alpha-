# 一阶实体 · 五·窗1（动作生命周期状态机：T-08＋T-09＋T-49 合并根）· input schema 与算法 declaration · **v1.1 · 呈报态 · 20260814**

> **v1.1增量（裁决89-8-1）**：N15恰界值负例入input与钉表（规模20＝正例5＋负例15），§7钉表条数联动。**声明面（状态机 declaration 本体）零变动**，`_declaration_version` 维持 v1.0（版本号指向声明面语义版，非文档版）。

> **状态**：呈报态（构造会话产出，候KD裁定；经KD收讫即落档，49-D）。本件不含任何裁决式结论。
> **会话身份**：切片构造会话（施工侧）。不兼外审、不兼裁决、不自评本根合格判定之终局效力。
> **授权源**：《第五批窗1任务包_v1_0_20260814》（定稿）＋裁决86（块B/块C分档）＋W-23定案版＋裁决88下游序②。
> **施工侧模型档申报（41-11 口径）**：不钉版本号，只钉能力档——本会话施工侧＝Anthropic 前沿能力档对话模型（当期 chat 环境所配前沿档）。校验侧对照义务：外审/增量复核须 fresh context 且能力档不低于本档。
> **引擎消费声明**：本根**零消费** `engine.py`，构造会话未装载引擎（装载核证纪律不触发）。
> **例外切片条款组不适用**：本根为标准切片（85-3/85-7/F-20 不适用）；曳光弹探针数值零入面。

---

## §1 对象语义与边界

**五·窗1 ＝ 动作生命周期状态机**：以 T-08（candidate action）／T-09（approved action）之运行术语定义为**状态位**，以 T-49 之状态转移语义（`x_t —a_t→ x_{t+1}`）与五合法性条件为**转移骨架**，构成一台对「动作事件序列」作合法性核验的状态机：输入一条人造事件序列，输出该序列之合法性判定与违规点定位。

- **与输入的关系**：输入＝人造事件序列（10 类事件）＋声明面（状态集/允许转移表/裁决值域/必填引用字段/事件类型）＋槽位符号绑定＋人造测试值。
- **与输出的关系**：输出＝逐序列 `{sequence_id, verdict∈{legal, illegal}, violations[{code, locus}]}`。**离散判定面，零数值量**。
- **下游消费面（C9 窗内构造序）**：窗2 消费本根之**事件类型定义**（`event_types`）与 `governance_rebasing` 子类语义；窗3 消费本根之**生命周期语义**与未标定三态形态。

### 1.1 乙面禁建声明（C3，边界级）

本根**不建、不代裁**：

1. `constraint stack` 之**具体内容**（hard/identity/permission/pre-action/post-action constraints 与 audit requirements 之实质构成）；
2. 「**合法状态**」之实质判定（何种 `x_t` 为合法状态）。

处置形态：五合法性条件之①（前状态合法）与③（后状态合法）在本机内**一律按声明值接收**——记录面承载为 `pre_state_legality_ref`／`post_state_legality_ref`，本机**仅核引用在场性**，不核其所指内容、不产生任何实质合法性判定。条②（候选合法）、条④（经 Phase 4 裁决）、条⑤（身份未漂移）之**结构面**可由序列关系核验，本机核之。

### 1.2 上边界与下边界

- **上边界（要件）**：状态集与允许转移表核验／动作记录必填引用字段在场性／no-action 周期审计条件／强平外部覆盖事件类型与 identity audit 强制触发／换装治理动作之生命周期不可旁路与联动重置。
- **下边界（不代行，详见 §9 反面陈述段）**：不做 roll 事件记录 schema（窗2 本职）、不做 T3-24 六问状态量（窗3 本职）、不做标定算法层（缺定义登记维持，宿主 T3-17 撞墙清单）、不做结构选型（W-24 域）、不产出任何数值量。

---

## §2 人造 input（模板三 A 段；裁决1 全程强制）

- **文件**：`entity/synthetic_input.json`，头部载 `_data_source: synthetic_hand_constructed` 与零数据源声明。
- **规模**：20 条事件序列＝正例 5（P1–P5）＋负例 15（N01–N15；N15＝恰界值负例 gap=verification_period+1，裁决89-8-1增量回流，假设级构成域非缺陷通道）；事件总数由 `verify/assert_check.py` 程序化实测回显。
- **时间轴**：`t` 为无量纲人造序号（数据层构造自由度），非日历时间、非交易时点。
- **人造测试值**：`verification_period = 5`。**人造测试值 ≠ 生产参数值**（受控文本 §1 术语纪律）；权威形态见 §3 之 `parameter_slots`（零赋值）。
- **负例设计口径**：逐条**单码**——每条负例序列恰好命中一个违规码，使断言击落力可逐码定位（区分力设计）。

---

## §3 声明面（F-4 声明-实现一致性之声明侧；F-14 schema 本体入比对面）

下列声明块为本根**权威声明面**。三方对表（F-15⑧）：**本内嵌块** ↔ `entity/lifecycle_declaration.json`（被测侧读取源） ↔ `verify/independent_recompute.py` 解析结果（复算侧读取源＝本内嵌块），三方由 `verify/assert_check.py` 程序化对表；任一不一致即判据不符档。

<!-- W1-LIFECYCLE-DECL-EMBED -->

```json
{
  "_declaration_id": "W1-LIFECYCLE-DECL",
  "_declaration_version": "v1.0",
  "_object_id": "\u4e94\u00b7\u7a971\u00b7\u52a8\u4f5c\u751f\u547d\u5468\u671f\u72b6\u6001\u673a",
  "_constituent_objects": ["T-08", "T-09", "T-49"],
  "_pin_order_declaration": "\u5148\u9489\u8868\u540e\u8dd1\u6570\uff1a\u672c\u58f0\u660e\u9762\u4e0e input_schema.md \u00a77 \u671f\u671b\u503c\u9489\u8868\u4e0e synthetic_input.json \u540c\u8f6e\u63d0\u4ea4\uff0c\u5148\u4e8e harness \u5b9e\u8dd1\uff08F-10 \u6587\u5b57\u58f0\u660e\u4e09\u5904\u4e00\u81f4\uff09",

  "action_states": [
    "candidate",
    "approved",
    "executed",
    "post_action_checked",
    "terminal_undetermined_by_source"
  ],

  "action_state_source_anchor": {
    "candidate": "00A\u00a74\u884c66 (T-08)",
    "approved": "00A\u00a74\u884c67 (T-09)",
    "executed": "00A\u00a74\u884c67 (\u201c\u540e\u53ef\u6267\u884c\u201d) \u2227 W-23 \u00a72.2\u7a971\u7532\u2460",
    "post_action_checked": "00A\u00a74\u884c67 (post-action legality check)",
    "terminal_undetermined_by_source": "\u6851\u4f4d\uff1a\u6e90\u6587\u672a\u5b9a\u4e49\uff08TPL2-W1-01\uff09"
  },

  "allowed_transitions": [
    {"from": "__none__", "to": "candidate", "trigger": "candidate_generated", "guard_decision": null, "guard": "source_diagnostic_ref \u5728\u573a\u4e14\u6307\u5411 phase3_diagnostic \u4e8b\u4ef6", "tier": "\u8fb9\u754c\u7ea7", "rule_ref": "C2\u2460"},
    {"from": "candidate", "to": "approved", "trigger": "phase4_decision", "guard_decision": "approval", "guard": "decision == approval", "tier": "\u8fb9\u754c\u7ea7", "rule_ref": "C2\u2460"},
    {"from": "candidate", "to": "terminal_undetermined_by_source", "trigger": "phase4_decision", "guard_decision": "__nonapproval__", "guard": "decision \u2208 {block, manual_review, rollback, identity_drift_declaration}", "tier": "\u8fb9\u754c\u7ea7\u4e0b\u754c\u534a", "rule_ref": "C2\u2460\u9006\u5411\u5fc5\u7136 \u2227 O-2"},
    {"from": "approved", "to": "executed", "trigger": "execution", "guard_decision": null, "guard": "\u4e94ref\u5728\u573a \u2227 \u6267\u884c\u786e\u8ba4\u6743\u5f15\u7528\u8981\u4ef6\u6ee1\u8db3", "tier": "\u8fb9\u754c\u7ea7", "rule_ref": "C2\u2460 \u2227 O-3"},
    {"from": "executed", "to": "post_action_checked", "trigger": "post_action_legality_check", "guard_decision": null, "guard": "check_ref \u5728\u573a", "tier": "\u8fb9\u754c\u7ea7", "rule_ref": "C2\u2460"}
  ],

  "terminal_states": ["post_action_checked", "terminal_undetermined_by_source"],
  "mandatory_terminal_for_executed": "post_action_checked",

  "governance_decision_domain": [
    "approval",
    "block",
    "manual_review",
    "rollback",
    "identity_drift_declaration"
  ],
  "governance_decision_domain_source": "00A\u00a74\u884c71 (T-13)",
  "governance_decision_semantics_built": {
    "approval": "\u5efa\uff1a\u552f\u4e00\u4ea7\u51fa approved \u4e4b\u51b3\u7b56\u503c",
    "block": "\u4e0d\u5efa\uff1a\u540e\u7ee7\u72b6\u6001\u8bed\u4e49\u60ac\u7f6e\uff08TPL2-W1-01\uff09\uff0c\u4ec5\u5efa\u5236\u4f4d\u4e0e\u4e0b\u754c\uff08\u4e0d\u4ea7\u51fa approved\uff09",
    "manual_review": "\u4e0d\u5efa\uff1a\u5efa\u5236\u4f4d\u5165\u5141\u8bb8\u8f6c\u79fb\u8868\uff08\u88c1\u51b3 86 \u00a76 P6-1\uff09\uff0c\u5224\u5b9a\u5185\u5bb9\uff08\u4eba\u5de5\u88c1\u91cf\uff09\u5c5e\u6cbb\u7406\u57df\uff0c\u7a971\u4e59\u7981\u5efa\uff08C3\uff09",
    "rollback": "\u4e0d\u5efa\uff1a\u4f5c\u7528\u5bf9\u8c61\uff08candidate / \u5df2\u6267\u884c\u52a8\u4f5c\uff09\u4e24\u8bfb\u6cd5\u60ac\u7f6e\uff08TPL2-W1-01\uff09\uff0cO-2 \u663e\u5f0f\u767b\u8bb0\u4e0d\u5efa",
    "identity_drift_declaration": "\u4e0d\u5efa\uff1a\u540e\u7ee7\u72b6\u6001\u8bed\u4e49\u60ac\u7f6e\uff1b\u4ec5\u4f5c\u4e3a\u201c\u6f02\u79fb\u68c0\u51fa\u5fc5\u987b\u7533\u62a5\u201d\u4e4b\u7533\u62a5\u8f7d\u4f53\u5165\u6838\u9a8c\u8def\u5f84\uff08\u5047\u8bbe\u7ea7\uff09"
  },

  "event_types": [
    {"name": "phase3_diagnostic", "fields": ["t", "diagnostic_id"], "source": "00A\u00a74\u884c73"},
    {"name": "candidate_generated", "fields": ["t", "action_id", "source_diagnostic_ref", "action_subtype", "position_ref"], "source": "00A\u00a74\u884c66"},
    {"name": "phase4_decision", "fields": ["t", "action_id", "decision", "decision_ref", "targets_audit_ref"], "source": "00A\u00a74\u884c67 \u2227 \u884c71"},
    {"name": "execution", "fields": ["t", "action_id", "execution_channel", "human_execution_confirmation_ref", "action_record"], "source": "00A\u00a74\u884c67 \u2227 \u5baa-\u884c471\u2462"},
    {"name": "post_action_legality_check", "fields": ["t", "action_id", "check_ref"], "source": "00A\u00a74\u884c67"},
    {"name": "periodic_audit", "fields": ["t", "audit_ref", "covers"], "source": "T1\u00b7B2\u00a75\u884c1027"},
    {"name": "forced_liquidation", "fields": ["t", "external_actor", "position_ref"], "source": "T1\u00b7B2\u00a75\u884c1029"},
    {"name": "object_identity_audit", "fields": ["t", "audit_ref", "trigger", "outcome"], "source": "T1\u00b7B2\u00a75\u884c1029 \u2227 00A\u00a74\u884c74"},
    {"name": "calibration_state_reset", "fields": ["t", "rebasing_action_ref", "reset_targets"], "source": "W-23 \u00a73.2\u67612 (71-6)"},
    {"name": "judgment_emission", "fields": ["t", "basis_id", "verdict"], "source": "W-23 \u00a73.2\u67613 (\u5047\u8bbe\u7ea7)"}
  ],

  "action_record_required_refs": [
    "pre_state_legality_ref",
    "candidate_ref",
    "decision_ref",
    "post_state_legality_ref",
    "identity_verification_ref"
  ],
  "action_record_required_refs_source": "T1\u00b7B2\u00a75\u884c1020-1024 \u4e94\u5408\u6cd5\u6027\u6761\u4ef6\u4e4b\u8bb0\u5f55\u9762\u6295\u5f71\uff08C2\u2461\uff0c\u5047\u8bbe\u7ea7\uff09",
  "declared_value_receipt_only": ["pre_state_legality_ref", "post_state_legality_ref"],
  "declared_value_receipt_reason": "\u201c\u5408\u6cd5\u72b6\u6001\u201d\u5b9e\u8d28\u5224\u5b9a \u2208 \u6cbb\u7406\u57df\uff0c\u7a971\u4e59\u7981\u5efa\uff08C3 \u8fb9\u754c\u7ea7\uff09\uff1b\u672c\u673a\u4ec5\u6838\u5f15\u7528\u5728\u573a\u6027\uff0c\u4e0d\u4ee3\u88c1\u5b9e\u8d28",

  "position_ref_coordinate_key": {
    "field": "instrument_type",
    "domain": ["linear", "option"],
    "source": "GK-31 \u5750\u6807\u952e\u7b2c\u4e03\u7ef4\uff0c\u88c1\u51b3 43 B-4 \u4fdd\u7559",
    "reference_form": "\u540c\u540d\u540c\u503c\u57df\u76f4\u5f15\uff08\u975e\u65b0\u9020\u5b57\u6bb5\uff09",
    "consumption_path": "\u503c\u57df\u5c01\u95ed\u65ad\u8a00 \u2227 \u5f3a\u5e73\u4e8b\u4ef6\u4e4b\u6301\u4ed3\u5b9a\u4f4d\uff1b\u4e0d\u6309\u54c1\u79cd\u5206\u652f/\u5206\u8d26"
  },

  "execution_confirmation_requirement": {
    "channel_domain": ["live_execution", "research_runtime"],
    "required_when_channel": "live_execution",
    "required_field": "human_execution_confirmation_ref",
    "source": "\u5baa-\u884c471\u2462\uff08\u4eba\u5de5\u6301\u6709\u6700\u7ec8\u6267\u884c\u786e\u8ba4\u6743\uff0c\u7a0b\u5e8f\u4e0d\u5f97\u81ea\u52a8\u4e0b\u5355\uff09",
    "scope_boundary_source": "\u5baa-\u884c475 \u4e0d\u6388\u6743\u680f\uff08\u786e\u8ba4\u6743\u7ea6\u675f\u9002\u7528\u57df\uff1d\u5b9e\u76d8\u6267\u884c\u94fe\u8def\u4e0b\u5355\u73af\u8282\uff1b\u7814\u7a76/\u56de\u6d4b\u73af\u8282\u4e0d\u5728\u7ea6\u675f\u57df\uff09"
  },

  "external_override": {
    "event": "forced_liquidation",
    "classification": "Phase \u6743\u9650\u94fe\u5916\u90e8\u8986\u76d6\u00b7\u6743\u9650\u94fe\u5931\u6548\u6a21\u5f0f",
    "mandatory_consequence": {"event": "object_identity_audit", "trigger": "forced_liquidation"},
    "not_an_authorization_source": true,
    "not_an_authorization_source_note": "\u672c\u4e8b\u4ef6\u7c7b\u578b\u4e0d\u6784\u6210\u3001\u4e0d\u63a8\u5bfc\u4efb\u4f55\u81ea\u52a8\u4ea4\u6613\u6388\u6743\u6765\u6e90\uff08\u672f\u8bed\u518c margin regime shock \u7981\u5f62\uff09",
    "source": "T1\u00b7B2\u00a75\u884c1029"
  },

  "no_action_audit_condition": {
    "definition": "\u6301\u7eed no-action \u6bb5\uff1d\u76f8\u90bb\u4e24\u6b21 execution \u4e4b\u95f4\uff08\u542b\u5e8f\u5217\u9996/\u5c3e\uff09\u65e0 execution \u4e8b\u4ef6\u4e4b\u6781\u5927\u533a\u95f4",
    "requirement": "\u6bb5\u5185\u76f8\u90bb periodic_audit \u4e8b\u4ef6\u95f4\u9694 \u2264 verification_period\uff1b\u6bb5\u8d77\u70b9\u81f3\u9996\u6b21\u5ba1\u8ba1\u3001\u672b\u6b21\u5ba1\u8ba1\u81f3\u6bb5\u7ec8\u70b9\u540c\u53d7\u7ea6",
    "legality_source": "\u5408\u6cd5\u6027\u6765\u81ea\u88ab\u5468\u671f\u6027\u9a8c\u8bc1\u7684\u51f8\u6027\u72b6\u6001\uff0c\u975e\u6765\u81ea\u8b66\u62a5\u7f3a\u5931\uff08\u884c1027\uff09",
    "tier": "\u5047\u8bbe\u7ea7 (C2\u2462)"
  },

  "rebasing_semantics": {
    "action_subtype": "governance_rebasing",
    "must_traverse_full_lifecycle": true,
    "extra_required_refs": ["old_source_ref", "new_source_ref", "rebasing_decision_ref"],
    "reset_on_effect": {
      "trigger_state": "executed",
      "required_event": "calibration_state_reset",
      "target_set_id": "slot1_cofamily_four_values",
      "target_cardinality": 4,
      "required_post_state": "uncalibrated",
      "partial_reset_is_violation": true
    },
    "uncalibrated_judgment_state": "indeterminate",
    "tier_map": {"\u67611": "\u8fb9\u754c\u7ea7", "\u67612": "\u8fb9\u754c\u7ea7", "\u67613": "\u5047\u8bbe\u7ea7", "\u67614": "\u5047\u8bbe\u7ea7"},
    "source": "W-23 \u00a73.2 \u8bed\u4e49\u8981\u4ef6\u56db\u6761 (71-6)"
  },

  "parameter_slots": [
    {"slot_symbol": "verification_period", "form": "parameter_slot_candidate", "value": null, "channel": "\u81ea\u7531\u5ea6\u6cbb\u7406\u518c\u4fe1\u53f7\u767b\u8bb0\u901a\u9053", "source": "T1\u00b7B2\u00a75\u884c1027", "phase_a_consumption": "\u4ec5\u6d88\u8d39\u4eba\u9020\u6d4b\u8bd5\u503c\uff08\u6570\u636e\u5c42\u6784\u9020\u81ea\u7531\u5ea6\uff09"},
    {"slot_symbol": "recalibration_window_length", "form": "parameter_slot_candidate", "value": null, "channel": "\u81ea\u7531\u5ea6\u6cbb\u7406\u518c\u4fe1\u53f7\u767b\u8bb0\u901a\u9053", "source": "W-23 \u00a73.2\u67614", "phase_a_consumption": "\u96f6\u6d88\u8d39\uff08\u4ec5\u767b\u8bb0\uff0c\u65e0\u65ad\u8a00\u4f9d\u8d56\u5176\u503c\uff09"}
  ],

  "identity_audit_trigger_domain": ["periodic", "forced_liquidation", "transition_verification"],
  "identity_audit_outcome_domain": ["no_drift", "drift_detected"],
  "judgment_verdict_domain": ["pass", "fail", "indeterminate"],
  "locus_rule": {
    "V01": "candidate_generated / action_id",
    "V02": "execution / action_id",
    "V03": "execution / action_id",
    "V04": "execution / action_id",
    "V05": "execution / action_id",
    "V06": "execution / action_id",
    "V07": "forced_liquidation / position_id",
    "V08": "\u8d85\u671f\u533a\u95f4\u4e4b\u540e\u754c\u4e8b\u4ef6 / \u8be5\u4e8b\u4ef6\u4e3b\u952e",
    "V09": "calibration_state_reset / rebasing_action_ref",
    "V10": "calibration_state_reset / rebasing_action_ref",
    "V11": "judgment_emission / basis_id",
    "V12": "object_identity_audit / audit_ref",
    "V13": "phase4_decision / decision_ref",
    "V14": "candidate_generated / action_id"
  },

  "_key_roles": {
    "allowed_transitions": "impl",
    "governance_decision_domain": "impl",
    "position_ref_coordinate_key": "impl",
    "action_record_required_refs": "impl",
    "execution_confirmation_requirement": "impl",
    "rebasing_semantics": "impl",
    "external_override": "impl",
    "action_states": "assert",
    "terminal_states": "assert",
    "mandatory_terminal_for_executed": "assert",
    "event_types": "assert",
    "declared_value_receipt_only": "assert",
    "parameter_slots": "assert",
    "identity_audit_trigger_domain": "assert",
    "identity_audit_outcome_domain": "assert",
    "judgment_verdict_domain": "assert",
    "locus_rule": "assert",
    "violation_codes": "assert",
    "output_form": "assert",
    "action_state_source_anchor": "registry",
    "governance_decision_domain_source": "registry",
    "governance_decision_semantics_built": "registry",
    "action_record_required_refs_source": "registry",
    "declared_value_receipt_reason": "registry",
    "no_action_audit_condition": "registry"
  },

  "violation_codes": [
    {"code": "V01", "text": "candidate \u975e\u51fa\u81ea Phase 3 \u8bca\u65ad", "tier": "\u8fb9\u754c\u7ea7", "rule_ref": "C2\u2460"},
    {"code": "V02", "text": "\u88c1\u51b3\u975e approval \u5374\u53d1\u751f execution\uff08approved \u552f\u4e00\u5165\u53e3\u88ab\u7ed5\u8fc7\uff09", "tier": "\u8fb9\u754c\u7ea7", "rule_ref": "C2\u2460"},
    {"code": "V03", "text": "\u672a\u7ecf Phase 4 \u88c1\u51b3\u5373\u53d1\u751f execution\uff08\u8d8a\u7ea7\u8f6c\u79fb\uff09", "tier": "\u8fb9\u754c\u7ea7", "rule_ref": "C2\u2460"},
    {"code": "V04", "text": "executed \u540e post-action legality check \u7f3a\u5931", "tier": "\u8fb9\u754c\u7ea7", "rule_ref": "C2\u2460"},
    {"code": "V05", "text": "\u52a8\u4f5c\u8bb0\u5f55\u5fc5\u586b\u5f15\u7528\u5b57\u6bb5\u7f3a\u5931", "tier": "\u5047\u8bbe\u7ea7", "rule_ref": "C2\u2461"},
    {"code": "V06", "text": "\u5b9e\u76d8\u6267\u884c\u94fe\u8def\u7f3a\u4eba\u5de5\u6267\u884c\u786e\u8ba4\u6743\u5f15\u7528", "tier": "\u8fb9\u754c\u7ea7", "rule_ref": "O-3 / \u5baa-\u884c471\u2462"},
    {"code": "V07", "text": "\u5f3a\u5e73\u672a\u5f3a\u5236\u89e6\u53d1 object identity audit", "tier": "\u8fb9\u754c\u7ea7", "rule_ref": "C2\u2463"},
    {"code": "V08", "text": "no-action \u6bb5\u5185\u5ba1\u8ba1\u95f4\u9694\u8d85\u9a8c\u8bc1\u5468\u671f", "tier": "\u5047\u8bbe\u7ea7", "rule_ref": "C2\u2462"},
    {"code": "V09", "text": "\u6362\u88c5\u65c1\u8def\u751f\u547d\u5468\u671f\uff08\u672a\u8d70 candidate\u2192\u88c1\u51b3\u2192approved \u5168\u94fe\uff09", "tier": "\u8fb9\u754c\u7ea7", "rule_ref": "C10\u67611"},
    {"code": "V10", "text": "\u6362\u88c5\u540e\u540c\u65cf\u503c\u96c6\u672a\u5168\u5458\u8f6c\u672a\u6807\u5b9a\u6001\uff08\u9759\u9ed8\u6cbf\u7528\u65e7\u503c\uff09", "tier": "\u8fb9\u754c\u7ea7", "rule_ref": "C10\u67612"},
    {"code": "V11", "text": "\u672a\u6807\u5b9a\u6001\u4e0b\u8f93\u51fa\u4e8c\u503c\u5224\u5b9a\uff08\u975e indeterminate\uff09", "tier": "\u5047\u8bbe\u7ea7", "rule_ref": "C10\u67613"},
    {"code": "V12", "text": "identity drift \u68c0\u51fa\u800c\u672a\u7533\u62a5", "tier": "\u5047\u8bbe\u7ea7", "rule_ref": "T-49\u6761\u4ef6\u2464 \u6295\u5f71"},
    {"code": "V13", "text": "\u6cbb\u7406\u88c1\u51b3\u503c\u8d85\u51fa T-13 \u4e94\u503c\u57df", "tier": "\u8fb9\u754c\u7ea7", "rule_ref": "O-2"},
    {"code": "V14", "text": "\u6301\u4ed3\u5f15\u7528 instrument_type \u503c\u57df\u8d8a\u754c", "tier": "\u5047\u8bbe\u7ea7", "rule_ref": "A9 \u7b2c\u4e03\u7ef4"}
  ],

  "output_form": {
    "per_sequence": ["sequence_id", "verdict", "violations"],
    "verdict_domain": ["legal", "illegal"],
    "violation_item_fields": ["code", "locus"],
    "closure": "\u8f93\u51fa\u9876\u5c42\u952e\u96c6\u5c01\u95ed\uff0c\u65e0\u58f0\u660e\u5916\u5b57\u6bb5"
  }
}
```

---

## §4 既裁边界分档对照（裁决86-4，构造按档执行）

| 成分 | 档 | 本根实现位 |
|---|---|---|
| C1 拆分方案A（T-08＋T-09＋T-49 合并） | 边界级 | 本 schema §1 |
| C9 构造序（窗1→2→3） | 边界级 | §1 下游消费面声明 |
| C3 窗1乙禁建 | 边界级 | §1.1 |
| C2① 状态集与允许转移表 | 边界级 | §3 `action_states`／`allowed_transitions`；断言 A07/A08 |
| C2④ 强平＋identity audit | 边界级 | §3 `external_override`；断言 A11 |
| C10条1 换装不得旁路生命周期 | 边界级 | §3 `rebasing_semantics`；断言 A13 |
| C10条2 禁静默沿用旧值 | 边界级 | §3 `reset_on_effect`；断言 A14 |
| C15 槽位登记不赋值 | 边界级 | §3 `parameter_slots`；断言 A18 |
| C2② 动作记录必填引用字段清单 | 假设级 | §3 `action_record_required_refs`；断言 A16 |
| C2③ no-action 周期审计条件 | 假设级 | §3 `no_action_audit_condition`；断言 A12 |
| C10条3 未标定态三态形态 | 假设级 | §3 `uncalibrated_judgment_state`；断言 A15 |
| C10条4 重标窗口期槽位形态细节 | 假设级 | §3 `parameter_slots`[1]；阶段A零消费 |
| C8 负例集构成 | 假设级 | §2 负例 14 条（杀灭率口径＝既裁沿用，边界级） |

**假设级项之可证伪性**：上列假设级各项在本根均以**可击落断言**承载，撞墙清单回流修正不构成缺陷（86-4 明文）。

---

## §5 违规码与责任事件（locus）定义

违规码全集与逐码档位见 §3 `violation_codes`；locus 规则见 §3 `locus_rule`。locus ＝ **责任事件之 `(t, event_type, key)` 三元组**，两条独立路径均须产出且逐字段入比对面（F-17 转-4：产物字段全数入比对面）。

V08 之责任事件＝**超期区间之后界事件**；后界为周期审计事件时取该审计事件，否则取该 `t` 上之末位事件。

---

## §6 容差声明面（F-4 机械对表；断言 A19）

- 本根输出为**离散判定面**（枚举字符串与整数 `t`），适用容差子口径 **(a)＝0（bit-exact）**（裁决13；任务包 §4）。
- 本根**未出现数值面**，子口径 (b)（相对 diff ≤ 1e-12，裁决19锚定）**未被激活**，如实登记。
- F-11（声明离散近似量之容差框架）**不适用**——本根被测量非离散近似量而为精确离散判定。
- F-16（实测标定派生容差之重算对表与误差放大申报）**不适用**——本根零实测标定派生容差、零相消型派生量。

---

## §7 期望值钉表（乙-2 钉表纪律；F-10 构造顺序留痕）

- **钉表载体**＝ `entity/expected_pin_table.json`（20 条逐序列 `verdict` ＋ `violations[{code, locus}]` 全字段钉定，粒度＝逐值）。
- **构造顺序留痕（F-10 最低形态＝文字声明三处一致）**：①本节；② `verify/assert_check.py` 头注；③本根切片记录。三处声明同文：**先钉表后跑数**——钉表与人造 input 同轮提交，先于 harness 首次实跑。可程序化时序证据非强制（F-10），本项如实标注为文字声明。
- **复算来源**：19 条全部**可独立复算**（`verify/independent_recompute.py` 谓词集/覆盖式路径），无「不可证」条目。
- **叙述链表格（W-13(14)）**：钉表 vs 实跑 vs 复算之三方比对表由 `verify/assert_check.py` 程序化产出至 `verify/logs/comparison_table.md`，不手工誊写。

---

## §8 交付件双钉声明面（F-5／F-8）

外置数据件与钉定件之内容以 **SHA256 ＋ 声明面** 双钉：指纹由 `verify/build_provenance.py` 生成并由 `verify/assert_check.py` 核对；声明面＝本节与 `verify/provenance.json`。

**双钉射程含钉定件自身**（F-8）：`verify/provenance.json` 自身入指纹表并由断言核其自洽性。

**免疫射程声明（手册 §3.1d）**：双钉之设计目标＝**单面篡改检出**；**协同篡改（指纹表与被钉件一并改）不在免疫射程**，本根不宣称协同免疫，亦不加设第三独立面（本根为离散判定面、无外部数值基线，加设第三面无对应风险面）。

**独立性封闭规则（F-8）**：`verify/independent_recompute.py` **不读取自身既往产物**，亦不读取 `entity/outputs/run_output.json`；其声明面来源为 §3 内嵌块（与被测侧读取源分离）。

---

## §9 反面陈述段（F-13 下边界显式化）

本根**显式声明不代行**下列相邻对象/相邻域之职责：

1. **不代行治理域实质判定**：constraint stack 内容、「合法状态」实质判定、`manual review` 之人工裁量内容——建制位在场，判定内容在 pipeline 出口外（C3；模块划分第3类定性不因本根改变，裁决86 §6 P6-1）。
2. **不代行窗2职责**：不产出 roll 事件记录 schema、不产出迁移闭合断言、不定义开平 lot 集与账本关系迁移映射。
3. **不代行窗3职责**：不产出六问状态量、不消费任何判据根输出、不作 payoff shape/wing integrity/Gamma center 之任何判定。
4. **不代行标定算法层**：新基准值如何从新源序列计算——缺定义登记维持，宿主＝T3-17 撞墙清单（W-23 §3.1；本根不重复登记）。
5. **不产出结构选型内容**（W-24 零侵入）：wing moneyness／长短端比例／IV 期限结构同步率／风险容忍边界，本根零触面。
6. **不产出任何数值量、不产出交易信号、不产出动作建议**；本根输出为判定与定位，非动作。
7. **不作自动交易授权来源**：`forced_liquidation` 事件类型定义与自动交易授权**显式切割**——外部覆盖 → identity audit，非授权来源（术语册 `margin regime shock` 禁形，随包件A §2）。
8. **不预裁模块归属**：本根字段名与事件类型名为**工程取用，不外推为跨根命名规范**；是否升为常设接口归骨架/模块层归纳反推（裁决14）。
9. **不代裁 T-13 四值后继语义**：见 §15。

**与任务包 §4「约束」逐条机械对表**（F-13 v1.12 扩注）：对表由 `verify/assert_check.py` 之 A22 执行，逐条比对本节条目与任务包约束项之覆盖关系。

### 9.1 与任务包 §4「约束」逐条机械对表（F-13 v1.12 扩注；断言 A22 执行）

| 任务包 §4 条目 | 本件/本包落点 |
|---|---|
| 裁决1 | §2（input 全人造、harness 一次性、零数据源）；断言 A01/A02 |
| step0前置 | 断言 A01–A03（前置合规先于比对）；扫描集依 F-1 现行权威扫描集 |
| D段容差 | §6（子口径(a)＝0 bit-exact；(b) 未激活如实登记） |
| 路径独立 | §8 独立性封闭规则；`verify/independent_recompute.py` 头注；断言 A03 |
| 窗1乙禁建（边界级C3） | §1.1；§9 条1 |
| W-24零侵入 | §9 条5 |
| mutation最小形态（乙-4） | `verify/negative_control.py`（注入打在被测实现，指名实际失败断言） |
| 钉表纪律（乙-2） | §7；`entity/expected_pin_table.json`；断言 A06 |
| 三分判别反向引用（乙-7） | §10（逐处回引受控文本条款号）；断言 A23② |
| 断言非零退出码（W-13(2)）／叙述链表格随脚本（W-13(14)）／交付态复跑（C-3） | `verify/assert_check.py` 非零退出；`verify/logs/comparison_table.md` 脚本产出；`verify/final_sweep.py` 交付态复跑核证 |
| A9第七维（86-3之P4） | §14 |
| 翻译审计表纪律 | §16（判据级引用限随包件B confirm 行；其余标「未审引用」） |
| 会话身份 | 头注（构造会话，不兼外审/裁决/自评） |

---

## §10 计算成分三分判别（乙-7：逐处回引《计算成分三分判别受控文本》v1.2 条款号；单向回引）

> **两维正交声明**：本节之「三分」＝成分归属（类一/类二/类三，受控文本）；§4 之「分档」＝W-23 成分之修改通道（边界级/假设级，裁决86-4）。二者正交，可并存（例：某成分三分为类一，其 W-23 成文形态仍可为假设级、允许构造反推回流）。

| # | 成分 | 三分 | 回引条款 | 判别留痕 |
|---|---|---|---|---|
| C-1 | 状态集与允许转移表（四状态位＋入口规则） | **类一** | §2（语义即裁）；§1 KD既裁项承接条（65-29） | 权威文本 T＝00A§4行66/67 ＋ C2①既裁；候选「executed 可不经 approved」与 T 矛盾，当场裁掉。**经KD直接裁定之成分，仅登记承接，不重走判别测试路径** |
| C-2 | 治理裁决值域（T-13 五值） | **类一** | §2 | T＝00A§4行71 枚举；候选「四值域」「六值域」与 T 矛盾 |
| C-3 | block／manual review／rollback／identity drift declaration 之**后继状态语义** | **类二·缺定义型** | §3（缺定义型）；§3 供给方自指补注（反向核验） | 供给方＝治理域（Phase 4 裁决语义定义方），**非本实体自身** ⇒ 不构成供给方自指，类二成立。桩＝`terminal_undetermined_by_source`，降格标注在场，**桩不 claim 语义等价**。登记＝TPL1-W1-01 |
| C-4 | rollback 之**作用对象**（candidate／已执行动作）读法分叉 | **模板二·悬物** | §4 末段（读法分叉本身即呈KD事项，施工侧呈候选不自决） | 见撞墙清单 TPL2-W1-01 |
| C-5 | 动作记录必填五引用字段清单 | **类一（结构面）** | §2 | T＝T1·B2§5行1020-1024 五合法性条件；记录面投影为一一映射。字段**命名**为工程取用不外推 |
| C-6 | no-action 审计条件之**结构**（段内审计间隔受周期约束） | **类一（结构半）** | §2 成分内再拆分（结构类一／数值类三） | T＝T1·B2§5行1027（审计按周期触发、不依赖动作发生；合法性来自周期性验证非警报缺失） |
| C-7 | `verification_period` **取值** | **类三** | §4；§1 术语纪律（人造测试值≠生产参数值） | 全候选与全权威文本相容，取舍须经验数据；处置＝槽位登记不赋值（C15 边界级）。**否定结论双栏留痕**见 §10.1 |
| C-8 | 强平 ⇒ 强制 object identity audit | **类一** | §2 | T＝T1·B2§5行1029「其发生强制触发 object identity audit」 |
| C-9 | 执行确认权引用要件（live 通道必填） | **类一** | §2 | T＝宪-行471③；适用域边界 T＝宪-行475 不授权栏。**无类三槽位依赖 ⇒ 不触发条件性登记位义务**（§2 v1.2 条件栏），如实声明 |
| C-10 | 换装联动重置**机制**（同族值集全员转未标定、禁静默沿用旧值） | **类一** | §2 | T＝W-23 §3.2条2（86-4 边界级）；候选「部分重置」与 T 矛盾 |
| C-11 | 换装联动重置**目标集成员身份** | **模板二·悬物** | §4 末段 | 三读法并存且互斥，见撞墙清单 TPL2-W1-02；机制对成员身份不敏感（读法无关性由断言 A20 实证） |
| C-12 | 未标定态 ⇒ 判据输出 `indeterminate`（三态） | **类一** | §2 | T＝W-23 §3.2条3 ＋ T3-18 三态先例（既有裁决为权威文本之一）。W-23 侧档位＝假设级，允许构造反推回流 |
| C-13 | `recalibration_window_length` | **类三** | §4 | 槽位登记不赋值；阶段A **零消费**（无断言依赖其值），不留白义务由「登记＋零消费声明」承担 |
| C-14 | 持仓引用 `instrument_type`（同名同值域直引） | **类一** | §2；§1 KD既裁项承接条 | T＝裁决43 B-4（第七维保留）＋W-23 §4.1 设计层钉定；仅登记承接不重走判别 |
| C-15 | 事件类型集（10 类）之**构成** | **类一（逐类有源文/既裁锚）** | §2 | 逐类锚见 §3 `event_types[].source`；集合之**最小充分性**为构造反推所得，属假设级可证伪面（C8 同域） |

### 10.1 类三否定结论双栏留痕（受控文本 §4 v1.2 双栏义务）

**C-7（`verification_period` 取值）**：

- **文本面查过什么**：T1·B2§5行1027 全句（仅言「验证周期为 `parameter_slot_candidate`」，无取值）；宪-行471②频率原则（「检视至少日级；当前取向＝每日」——**范围裁定归台账承载**，且其射程为**检视与对冲频率**，非本条之凸性状态/身份审计验证周期，不构成对本条之排除）；宪-行471④日检义务（同上，射程为收盘检视义务）；自由度治理册 v1.6 信号清单 17 条（无本槽位既有条目）；W-23 §3.2条4。**结论：无任一文本可排除任一候选取值。**
- **逻辑面查过什么**：逐候选实查——候选(i) 取「日级」（与宪-行471②同值）：无逻辑矛盾，但源文将两者分列不同条款，等同化属跨条款外推，**未见排除亦未见支持**；候选(ii) 取「周级」：无逻辑矛盾；候选(iii) 取「与短端到期节奏同步」：无逻辑矛盾。三候选均自洽，无逻辑排除项。
- **射程读法分叉**：无（本条不依赖任何既裁裁定之射程读法）。

---

## §11 本根裁定登记（逐项呈KD，非终裁；档位按 55-3a 标注）

**A档（逐项呈：不可逆/经济实质类）**

1. **【A档】T-13 四值后继语义＝登记不建，桩位合并为 `terminal_undetermined_by_source`**：源文（00A行71）枚举五值但未定义 approval 以外四值之后继状态；本根仅实现可由 C2① 逻辑必然裁出之**下界**（四值均不产出 `approved`），后继状态以单一占位桩承载并降格标注。**候选甲**＝维持单一合并桩（本根采纳，理由＝分立四态须为每态发明语义，属就地定义）；**候选乙**＝四值各设终止态（须治理域先行供给语义）。呈KD。指针＝§10 C-3、撞墙清单 TPL1-W1-01。
2. **【A档】rollback 转移路径＝显式登记不建（O-2 兑现）**：见 §15.1。呈KD。
3. **【A档】执行确认权引用要件之适用域建为 `execution_channel` 二值条件（O-3 兑现）**：见 §15.2。呈KD。
4. **【A档】换装联动重置目标集成员身份三读法并存，本根取读法(i) 为桩**：W-23 §3.2条2 之括注「治理册既载」经程序化核证**不成立**（治理册 v1.6 全文 `target_vega`／`target_gamma` 零命中；其 G-A 首登为 T3-22 band 边界四值 put 17/20、19/20 ／ call 9/10、21/20）。呈KD：读法裁定 ＋ 是否走缺陷回传通道订正 W-23。指针＝§10 C-11、撞墙清单 TPL2-W1-02。
5. **【A档】A9 第七维消费形态标注**：见 §14。呈KD 归属判定（判别口径1 vs 口径2）。

**B档（批量呈，程序/机械/留痕类）**

6. **事件类型集 10 类之命名与构成**＝本根工程取用，不外推为跨根命名规范；是否升常设接口归骨架/模块层反推（裁决14）。指针＝§3 `event_types`、§9条8。
7. **`object_identity_audit.trigger` 值域增 `transition_verification`**＝五合法性条件⑤之记录面投影所需（假设级，可证伪）；`periodic`／`forced_liquidation` 二值有源文直接锚，第三值为构造反推。指针＝§3 `identity_audit_trigger_domain`。
8. **强平不切断 no-action 段**＝强平为权限链**外部**覆盖，非本链动作，故不计为「动作发生」（行1029＋行1027 合读）。假设级，可证伪。指针＝§3 `no_action_audit_condition`。
9. **`periodic_audit.covers` 字段＝记录面字段，本根零核验路径消费**（供窗2/窗3 消费面预留），如实声明不设恒真断言。
10. **容差子口径 (b) 未激活**＝本根零数值面，如实登记（§6）。
11. **未通过/通过判定之层级限定语**＝本记录合格判定仅指实现层（L1），不构成 L2/L3 主张（裁决53）。

---

## §12 输出形态声明（裁决39-B 输出形态封闭）

顶层键集封闭为 `{_produced_by, _input_data_source, _verification_period_used, _reset_target_set_used, _reset_targets_used, _declaration_version_used, _sequence_count, results}`；`results[]` 元素键集封闭为 `{sequence_id, verdict, violations}`；`violations[]` 元素键集封闭为 `{code, locus}`；`locus` 键集封闭为 `{t, event_type, key}`。**声明外字段零容忍**（断言 A21 双向对表，检多不止检缺）。

---

## §13 交付件清单

| 路径 | 内容 |
|---|---|
| `entity/input_schema.md` | 本件（含 §3 内嵌声明块） |
| `entity/lifecycle_declaration.json` | 声明面外置件（被测侧读取源） |
| `entity/synthetic_input.json` | 人造 input：19 序列 |
| `entity/expected_pin_table.json` | 期望值钉表（乙-2） |
| `entity/state_machine.py` | 被测实现（状态推进式） |
| `entity/harness.py` | 一次性 harness |
| `entity/outputs/run_output.json` | B 段实跑真数 |
| `verify/independent_recompute.py` | 独立复算（谓词集/覆盖式） |
| `verify/assert_check.py` | 断言栈（含 step0 前置合规） |
| `verify/negative_control.py` | 变异注入负向对照 |
| `verify/build_provenance.py` | 指纹生成/核验（F-5／F-8 双钉） |
| `verify/final_sweep.py` | 末位复扫：交付态复跑＋包完整性复扫（F-15③⑨／C-3） |
| `verify/provenance.json` | 指纹表（自身入射程） |
| `verify/logs/*` | 断言日志／复算输出／比对表 |

---

## §14 A9 第七维回填检验之消费形态标注（86-3 之 P4；W-23 §4.2 判别口径三条）

- **引用形态**：动作记录之持仓引用**直接引用坐标键 `instrument_type` 字段本身**，同名、同值域 `{linear, option}`，非新造字段、非同义字段。
- **值域充分性**：本根反推所需值域**未超出** `{linear, option}`（强平/接货/出货类动作均落于二值内）⇒ **口径3（值域不足）不触发**，无 A9 档二-ii 第三反例。
- **进入核验路径之形态（如实留痕）**：该字段进入**值域封闭断言**（越界即击落，负例 N11 实证）与**强平事件之持仓定位**；但**不按品种分支、不按品种分账**——即不满足判别口径1 之完整例示形态（「如迁移闭合断言按品种分账」），亦**强于**判别口径2 之「仅透传不进核验路径」。
- **呈KD**：本形态归属判别口径1（构成消费）抑或口径2（不构成消费）＝**边界情形**，施工侧不自裁。倾向陈述（非裁定）：按口径1 字面（「取该字段之名与值域，且该维进入核验路径」）三要件均满足，倾向构成消费之**弱形态**；按口径1 例示（分账）不满足。呈KD 裁定后回填 43 B-4 义务状态。

---

## §15 随包义务处置（任务包 §5，缺一＝包义务未兑现）

### 15.1 O-2（裁决86-5）：rollback 转移路径与 T-13 五值允许转移表完备性

**处置＝建（完备性面）＋显式登记不建（后继语义面）**，逐项如下：

| T-13 值 | 本根处置 | 依据 |
|---|---|---|
| approval | **建**：`candidate --approval--> approved`，且为 `approved` 之**唯一入口** | C2①（边界级），00A行67 |
| block | **建制位在场／后继语义不建**：不产出 `approved`（C2① 逻辑必然），后继落占位桩 | §10 C-3 |
| manual review | **建制位在场／判定内容不建**：入允许转移表（裁决86 §6 P6-1「manual review 获状态机建制位」），人工裁量内容属治理域（C3 乙禁建） | 裁决86 §6 P6-1 |
| rollback | **显式登记不建**：作用对象两读法悬置（TPL2-W1-02 之同族条目 TPL2-W1-01），不产出 `approved`之下界建之 | §10 C-4 |
| identity drift declaration | **建制位在场（申报载体）／后继语义不建**：作为「漂移检出须申报」之申报载体入核验路径（V12，假设级），后继状态语义不建 | §11 B档7、§10 C-3 |

- **完备性机械保证**：`governance_decision_domain` 五值集与 00A行71 枚举**逐值对表**（断言 A09），值域超出即击落（V13，负例 N10 实证）；**禁静默略过**已由「五值逐值在表 ＋ 越域击落」双向承担。
- **rollback 不建之理由留痕（非裁定）**：00A行71 将 rollback 列为「Phase 4 对 **candidate** 作出的」裁决之一，而 rollback 之自然语义指向**已执行动作之回滚**；两读法在源文并置且未区分。取读法(ii) 须新增「executed → 回滚」转移，该转移之后继状态、其对持仓之效果、其是否本身须走一遍生命周期（C10条1 同型）三者源文均无定义 ⇒ 就地定义禁令命中。**呈KD**。

### 15.2 O-3（裁决86-5）：approved → executed 之执行确认权引用要件

**处置＝建（不留 Phase B 防滑落）**：

- 转移 `approved --execution--> executed` 之守卫含 `human_execution_confirmation_ref` **必填**（缺失即 V06，负例 N12 实证）。判据源＝宪-行471③「程序化计算＋人工持有最终执行确认权，程序不得自动下单」之不变量投影。
- **适用域条件（宪-行475 不授权栏原文）**：确认权约束适用域＝**实盘执行链路下单环节**；研究/回测环节系统自动运行不在约束域。故本根建 `execution_channel ∈ {live_execution, research_runtime}`，要件仅对 `live_execution` 生效（正例 P5 实证豁免面成立）。
- **保守缺省**：`execution_channel` 取值不在声明值域内者，**按需确认权处置**（不以未声明通道取得豁免）——防「新通道名即豁免」之滑落。
- **呈KD**：`execution_channel` 字段之建制属实体边界判断（A档3），呈裁；若KD裁定不建该维，修复面＝删条件分支与 P5 正例，改为无条件必填（数值产物无、判定面 P5 由 legal 翻 illegal，属丙类实质变动）。

### 15.3 86-8 对照页（随包件A）承接

随包件A 之 KD 裁定状态：三-1（EP-06 间接消费标注问题）＝**窗3 域，不阻塞窗1**，本根零承接动作；三-2（窗3 携带项两条）＝窗3 域；四（本批新增随行义务＝零）＝本根**零随行义务新增**。随包件A §1 之 SC-04 命中项（T-09「可执行」含执行语义）已由 O-3 承载（§15.2），无新增登记需求。

---

## §16 源文锚、层界标注与审计表状态（F-18 L2 完整性维）

| 消费源文 | 行指针 | 层界 | 审计表状态 |
|---|---|---|---|
| 00A《2_波动率凸性策略可复用方法论文档集_12篇》 | §4行66（T-08）／行67（T-09） | 权限/功能定义句，零度量形状固化 | **已审**（随包件B §2，KD confirm 20260814；C4② 闸门已开） |
| T1《1_可复用方法论主题树》 | B2§5行1011-1029（核证 span；含五条件实位 1020-1024、no-action 1027、强平 1029） | 结构定义句＋符号式／功能定义＋槽位符号，零数值 | **已审**（随包件B §2，同上；T1 首次入审计域，28-C 增量扩展） |
| 00A 同上 | §4行71（T-13 五值枚举） | 类别枚举，功能层 | **判据级消费（本根升格）** —— 随包件B §4 预标注之兑现点命中：本根以行71 为「允许转移表五值完备性」之判据源，触发下一增量入表，**呈KD**（兑现点＝窗1收口前呈报，已在此呈） |
| 00A 同上 | §4行74（T-16 object identity drift 定义）／行73（diagnostic 定义）／行60（Phase 4 行） | 定义句 | **未审引用**（C4④ 标注；本根为背景/语义级消费，未作判据源） |
| 《思想层宪法 v1.0》 | 行471③（人机分工权限结构）／行475 不授权栏（适用域边界） | 不变量措辞栏／不授权栏 | 判定锚本体（裁决26-A 唯一锚），不入审计域（审计域＝T3 及其被判据级消费之上游源文档） |

**思想层一手材料三件并联（83-1/83-3 G-14乙案）＝不触发**：本根消费之源文为方法论链（00A／T1）与宪法条款，**零消费思想层一手材料**（八份源文）；故 REG-UP 通道登记／H·P·W 层界标注／审计表类B 未审引用标注之三件并联义务本根不命中，如实声明。

**W-23 指针偏差承接**：W-23 §0.4/§1.1 所载 T-49 指针「T1/B2§5行1015-1023」与实况不符；KD 已裁处置＝(a) 留痕不改（20260814）。本 schema 一律以核证 span **行1011-1029** 为准。

---

> **G-4 合规声明**：本 schema 之输出结构、事件类型集、违规码集均由源文与既裁边界**反推**所得，非归纳输出结构之预定义；任务包未预置技术路线（裁决20），实现形态由本会话自源文反推。
> **W-24 零侵入声明**：全文零结构选型内容。
> **类三纪律声明**：全文零参数赋值；槽位两枚仅登记（`verification_period`／`recalibration_window_length`）。人造测试值已显式隔离于 `_synthetic_test_values` 并标注不外推。

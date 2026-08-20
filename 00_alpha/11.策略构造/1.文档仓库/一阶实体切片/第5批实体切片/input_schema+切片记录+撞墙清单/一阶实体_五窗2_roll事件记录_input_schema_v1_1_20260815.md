# 一阶实体 · 五·窗2（roll 事件记录 schema，宿主 T-69）· input schema 与算法 declaration · **v1.1 · 呈报态 · 20260815**

> **版本修订记录（v1.0→v1.1，cp-then-edit 自 v1.0，底版零覆盖）**：底版 `entity/input_schema.md` v1.0 之 SHA256 ＝ `67ee0f60d51dfbdaf0adc00a51478c2cb33b063fe156cfa1a4410cd9e485d24b`。变动面封闭＝裁决90 靶标集三项：**靶-1**（90-2 甲案：CA-3 改多值形态、R08 改空集形态及其随动面，判定面变动）／**靶-2**（90-5 乙类订正：§1 与 §4 两处数量指针订正＋新增数量指针对表断言 A32）／**靶-3**（90-8① 登记类落写，见切片记录与撞墙清单 v1.1）。
> **状态**：呈报态（构造会话产出，候KD裁定；经KD收讫即落档，49-D）。本件不含任何裁决式结论。
> **会话身份**：切片构造会话（施工侧），独立 session、chat 环境。不兼外审、不兼裁决、不生成后续任务包（裁决20/52-3）；不自评本根合格判定之终局效力。
> **增量授权源（v1.1）**：裁决90落地文档 v1.0（90-2／90-5／90-8序①）＋《窗2增量构造会话开启文本_v1_0_20260815》§3 靶标集。
> **授权源**：《第五批窗2任务包_v1_0_20260814》（定稿）＋裁决86（块B P1-1/P1-2 窗2边界／块C 86-4 分档／块E P5-2）＋裁决88 §下游动作序④＋裁决89 v1.2 收口序⑤＋W-23 设计窗产出 v1.0 §2.2窗2/§2.3/§2.4/§4＋窗1收口态（schema 现行版／切片记录 v1.2／撞墙清单 v1.1）。
> **施工侧模型档申报（41-11 口径）**：不钉版本号，只钉能力档——本会话施工侧＝Anthropic 前沿能力档对话模型（当期 chat 环境所配前沿档）。校验侧对照义务：外审/增量复核须 fresh context 且能力档不低于本档。
> **引擎消费声明**：本根**零消费** `engine.py`，构造会话未装载引擎（69扩项(i) 装载核证纪律不触发，与任务包 §3条5 预期一致）。
> **例外切片条款组不适用**：本根为标准切片（85-3/85-7/F-20 不适用）；曳光弹探针数值零入面（85-3 隔离）。
> **钉表构造顺序留痕（F-10 三处一致之第三处）**：**先钉表后跑数**——`entity/expected_pin_table.json` 与 `entity/synthetic_input.json` 同轮提交，先于 harness 首次实跑。另两处＝本件 §7、`verify/assert_check.py` 头注。可程序化时序证据非强制（F-10），本项为文字声明。

---

## §1 对象语义与边界

**五·窗2 ＝ roll 事件记录 schema**：以 T-69（roll ＝ 功能迁移，T1·B3§4）为宿主，构造一台对**单条 roll 事件记录**施行**迁移闭合核验**的记录/归因 schema——输入一条人造 roll 事件记录，输出该记录之迁移闭合判定与违规点定位。

- **与输入的关系**：输入＝人造 roll 事件记录集（18 条）＋声明面（必填引用字段／子类身份／坐标键第七维／账本来源值域／三条闭合断言／相位与门控／违规码与 locus 规则）。
- **与输出的关系**：输出＝逐记录 `{record_id, verdict∈{closed, not_closed}, violations[{code, locus{container,key}}], diagnostics}`。**离散判定面，零数值量**。
- **甲面（W-23 §2.2 窗2，裁决86 块B confirm）**：roll 事件记录 schema ＋ **迁移闭合断言**三条（CA-1 开平 lot 集／CA-2 账本关系迁移映射／CA-3 功能承担者前后映射，**多值形态**）。
- **判据落点收窄（W-23 §2.1 反推依据原文）**：T-69 四结构目标中**仅行1099「迁移账本关系与功能承担者」**落本窗闭合断言；行1096-1098（optionality／Gamma 中心／凸性含高阶）之**达成验收归窗3**（T3-24 六问），本窗不重复，仅作边界切割参照。

### 1.1 乙面双留位声明（C5，**边界级**，违反＝缺陷）

1. **roll 编排／触发时点通道选择**＝FW-03-乙域，**登记不建**；本窗撞墙清单载「窗2乙侧留位（触发通道选择）」（TPL2-W2-01），实体化不在本窗（86-6 宿主指针承接）。
2. **目标合约选择（moneyness／期限取位）**＝W-24 域**硬互斥**，登记不建（TPL2-W2-02）；本件与交付代码面**零结构选型内容**，由断言 A29 机械核证（射程＝代码面字面层）。

### 1.2 上边界与下边界

- **上边界（C9 单向消费，边界级）**：消费窗1一阶实体之**事件类型定义**（`event_types`）与 `governance_rebasing` 子类语义——本根据此取 `execution.action_record` 为 roll 事件记录之承载位、取 `action_id` 为动作身份主键、取 `action_subtype` 之子类语义形态。**不消费**窗1之生命周期推进、五合法性条件 refs 之重复核验、Phase 4 裁决语义与 T-13 值域。此为一阶实体产物消费，非审计域源文消费，不走 C4②，引用不重登（E-①(i)）。
- **下边界**：见 §9 反面陈述段（八条，与任务包 §4 逐条机械对表，断言 A20）。
- **供给（预期登记，非契约）**：窗3 消费本根 roll 事件记录作为 T3-24 验收对象之动作实例载体。

---

## §2 人造 input（模板三 A 段；裁决1 全程强制）

- **文件**：`entity/synthetic_input.json`，头部载 `_data_source: synthetic_hand_constructed` 与零数据源声明。
- **规模**：**18 条** roll 事件记录＝正例 4（P1–P4）＋负例 14（N01–N14）。
- **负例集覆盖面增量（假设级 C8 域回流，89-8-1 非缺陷通道同型）**：N13/N14 由 `verify/negative_control.py` 之变异 **M01**（R01 对称侧：closing 空）与 **M03**（R04「检多」侧，F-7 双向比对精神）**存活暴露之覆盖缺口**而补齐；补齐后杀灭率 10/10。构造侧如实登记（§11 B档-2）。
- **负例设计口径**：**逐条单码**——每条负例恰好命中**一个违规码**，使断言击落力可逐码定位（窗1 区分力设计同型）。**单码 ≠ 单 locus**：同一码在同一记录内可有多个 locus（v1.1 实例＝N08 之 R08 前后两侧各一 locus），码集区分力不受影响。
- **恰界值/off-by-one 注入重申报（89-9-2 成文判据；按裁决90-2 修订后判据实况**重列**，本根**适用**、非空白申报）**：修订后本根含**计数/边界比较型判据四处**——
  1. **账本迁移映射定义域 vs closing 基数**（R04，对称差计数）：合法侧恰满 P4 3/3、P2 2/2、P3 1/1；违规侧恰缺一 N04 1/2、恰多一 N14 2/1。
  2. **功能位承担者基数下界**（R08，空集判据）：多值形态下**仅有下界、无上界恰界面**（承担者集基数上界由母结构开放，不设判据）；合法侧恰在界内＝基数 1（P1／P4／P3·r2）；违规侧恰越下界＝基数 0（N08 前后两侧各一 locus）。**多值合法侧**（基数 ≥2）由 P2 前侧 2、P3 后侧 2 实证判 `closed`。
  3. **功能位键集相等**（R07，键集对称差）：合法侧恰相等（P1–P4）；违规侧恰差一键（N07）。
  4. **子集型越界**（R05 映射目标 ∈ opening／R09 承担者集 ⊆ 对应端）：合法侧恰含边界元素；违规侧恰越一元素（N05／N09）。
- **人造测试值**：`lot_id`／`role_id`／功能位名（r1/r2/r3）均为人造符号，属**数据层构造自由度**，显式隔离于 `_synthetic_test_values` 并标注不外推、非生产标识规范。
- **零时间轴**：本根记录面**无时间序**（时间语义属窗1生命周期域），故不设 `t`。

---

## §3 声明面（F-4 声明-实现一致性之声明侧；F-14 schema 本体入比对面）

下列声明块为本根**权威声明面**，与 `entity/roll_record_declaration.json` **逐字节同一**（断言 A18 程序化核证）。三方对表（F-15⑧）：**本内嵌块** ↔ `entity/roll_record_declaration.json`（被测侧读取源） ↔ `verify/independent_recompute.py` 解析结果，由 `verify/assert_check.py` 程序化对表；任一不一致即判据不符档。

<!-- W2-ROLLREC-DECL-EMBED -->

```json
{
  "_declaration_id": "W2-ROLLREC-DECL",
  "_declaration_version": "v1.1",
  "_object_id": "五·窗2·roll事件记录schema",
  "_constituent_objects": [
    "T-69"
  ],
  "_pin_order_declaration": "先钉表后跑数：本声明面与 input_schema.md §7 期望值钉表与 synthetic_input.json 同轮提交，先于 harness 实跑（F-10 文字声明三处一致）",
  "record_required_refs": [
    "action_id",
    "source_execution_ref",
    "action_subtype"
  ],
  "record_required_refs_source": "C9 单向消费：窗1 input_schema §3 event_types.execution 之 action_record 承载位（action_id 为窗1动作身份主键；source_execution_ref 指回该 execution 事件；action_subtype 为窗1 candidate_generated 既有字段之子类语义）",
  "required_action_subtype": "roll",
  "required_action_subtype_source": "T1·1089 对象命名锚（roll = 功能迁移）× 窗1 governance_rebasing 子类语义同型",
  "upstream_consumption_W1": {
    "consumed": [
      "event_types 之 execution.action_record 承载位",
      "action_subtype 子类语义形态（governance_rebasing 同型）",
      "动作身份主键 action_id"
    ],
    "not_consumed": [
      "生命周期推进（candidate→approved→executed）",
      "action_record_required_refs 五条之重复核验",
      "Phase 4 裁决语义与 T-13 值域",
      "no-action 周期审计条件"
    ],
    "authority": "窗1 input_schema 现行版 §3 ＋ 窗1切片记录 v1.2「下游消费面（C9）」段",
    "reuse_form": "一阶实体产物消费，非审计域源文消费；不走 C4②，引用不重登（E-①(i)）"
  },
  "lot_fields": [
    "lot_id",
    "instrument_type"
  ],
  "position_ref_coordinate_key": {
    "field": "instrument_type",
    "domain": [
      "linear",
      "option"
    ],
    "source": "GK-31 坐标键第七维，裁决43 B-4 保留；W-23 §4.1 设计层钉定",
    "reference_form": "同名同值域直引（非新造字段）",
    "consumption_path": "值域封闭断言（越域即击落，R12）∧ 功能承担者前后品种维之诊断回显；不按品种分支、不按品种分账"
  },
  "ledger_origin_domain": [
    "migrated",
    "new_capital"
  ],
  "ledger_origin_domain_status": "类二·缺定义型桩（TPL1-W2-01）：账本来源类别之权威枚举无源文；本根二值为可复算最简桩，不 claim 语义等价",
  "closure_assertions": [
    {
      "id": "CA-1",
      "name": "lot集闭合",
      "statement": "closing_lots 与 opening_lots 均非空、互不相交、且逐元素在 position_lots_declared 内且无重复",
      "source": "T1·1099「迁移」之两端在场性反推",
      "tier": "假设级(C4)"
    },
    {
      "id": "CA-2",
      "name": "账本关系迁移映射闭合",
      "statement": "ledger_migration_map 之定义域 == closing_lots（双向对表）；值域 ⊆ opening_lots；每一 opening lot 之 ledger_origin 在场且 ∈ 值域，migrated 者须为映射目标、new_capital 者不得为映射目标",
      "source": "T1·1099「迁移账本关系」；账本主体语义背景锚＝宪-ST-02（随包件B已裁，背景锚不单列断言）",
      "tier": "假设级(C4)"
    },
    {
      "id": "CA-3",
      "name": "功能承担者前后映射闭合",
      "statement": "function_roles_before 与 function_roles_after 之功能位键集相等（功能位不增删，仅承担者迁移）；每一功能位之前后承担者均为**非空 lot 集**（多值形态：同一功能位可由多 lot 共担）；前承担者集 ⊆ closing_lots、后承担者集 ⊆ opening_lots",
      "source": "T1·1099「迁移…功能承担者」；功能位语义背景锚＝宪-ST-04/ST-05（随包件B已裁保留为背景锚，本根不固化为断言）。承担者基数形态＝**多值**（裁决90-2 甲案 KD 实质裁定：宪-ST-04 下行覆盖为张数×倍率之集合承担，多 lot 共担一功能位为常态；恰1形态不符合母结构特征）",
      "tier": "假设级(C4)"
    }
  ],
  "check_phases": {
    "phase1_structural": [
      "R10",
      "R11",
      "R12",
      "R03",
      "R01",
      "R02"
    ],
    "phase2_closure": [
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09"
    ],
    "gating": [
      "phase1 命中非空 ⇒ 跳过 phase2（结构前置未过时闭合判据不可判，避免级联码稀释单码区分力）",
      "R07 命中 ⇒ 跳过 R08/R09（功能位键集不等时逐位检查病态）"
    ],
    "diagnostics_condition": "phase1 clean ∧ R07 未命中 ⇒ 产出 role_instrument_type_change 诊断；否则诊断为空对象"
  },
  "violation_codes": [
    {
      "code": "R01",
      "text": "closing_lots 或 opening_lots 为空（迁移缺一端）",
      "tier": "假设级",
      "rule_ref": "CA-1"
    },
    {
      "code": "R02",
      "text": "closing_lots ∩ opening_lots ≠ ∅（同一 lot 既平又开，非迁移）",
      "tier": "假设级",
      "rule_ref": "CA-1"
    },
    {
      "code": "R03",
      "text": "lot 集不闭合：closing/opening 元素不在 position_lots_declared 内，或集内重复",
      "tier": "假设级",
      "rule_ref": "CA-1"
    },
    {
      "code": "R04",
      "text": "账本迁移映射定义域 ≠ closing_lots（缺失或多出；计数恰界面）",
      "tier": "假设级",
      "rule_ref": "CA-2"
    },
    {
      "code": "R05",
      "text": "账本迁移映射目标不在 opening_lots 内",
      "tier": "假设级",
      "rule_ref": "CA-2"
    },
    {
      "code": "R06",
      "text": "opening lot 之 ledger_origin 缺失/越域，或 migrated 非映射目标，或 new_capital 却为映射目标",
      "tier": "假设级",
      "rule_ref": "CA-2"
    },
    {
      "code": "R07",
      "text": "功能位键集前后不等（功能增删而非承担者迁移）",
      "tier": "假设级",
      "rule_ref": "CA-3"
    },
    {
      "code": "R08",
      "text": "某功能位承担者集为空（前侧或后侧；基数下界恰界面）",
      "tier": "假设级",
      "rule_ref": "CA-3"
    },
    {
      "code": "R09",
      "text": "功能承担者指向越集（前 ⊄ closing_lots 或 后 ⊄ opening_lots）",
      "tier": "假设级",
      "rule_ref": "CA-3"
    },
    {
      "code": "R10",
      "text": "必填引用字段缺失（窗1消费面身份引用）",
      "tier": "边界级(C9消费面)",
      "rule_ref": "record_required_refs"
    },
    {
      "code": "R11",
      "text": "action_subtype ≠ roll（事件身份错配）",
      "tier": "边界级(C9消费面)",
      "rule_ref": "required_action_subtype"
    },
    {
      "code": "R12",
      "text": "instrument_type 值域越界",
      "tier": "假设级",
      "rule_ref": "A9第七维"
    }
  ],
  "locus_rule": {
    "R01": "record / closing_lots|opening_lots",
    "R02": "record / 交集最小元素 lot_id",
    "R03": "record / 越界或重复之 lot_id",
    "R04": "ledger_migration_map / 对称差最小元素 lot_id",
    "R05": "ledger_migration_map / to_lot",
    "R06": "ledger_origin / lot_id",
    "R07": "function_roles / 对称差最小元素 role_id",
    "R08": "function_roles_before|after / role_id",
    "R09": "function_roles_before|after / role_id",
    "R10": "record / 缺失字段名",
    "R11": "record / action_subtype",
    "R12": "position_lots_declared / lot_id"
  },
  "output_form": {
    "per_record": [
      "record_id",
      "verdict",
      "violations",
      "diagnostics"
    ],
    "verdict_domain": [
      "closed",
      "not_closed"
    ],
    "violation_item_fields": [
      "code",
      "locus"
    ],
    "locus_fields": [
      "container",
      "key"
    ],
    "diagnostics_keys": [
      "role_instrument_type_change"
    ],
    "diagnostics_item_fields": [
      "before",
      "after",
      "changed"
    ],
    "diagnostics_value_form": "承担者集之 instrument_type 去重升序表（多值形态随动，裁决90-2）；changed ＝ 前后表不相等。单元素承担者退化为单元素表，语义与 v1.0 标量形态一致",
    "ordering": "violations 按 (code, locus.container, locus.key) 字典序排序，保证 bit-exact 可比",
    "closure": "输出顶层键集封闭，无声明外字段"
  },
  "prose_count_pointers": {
    "_scope": "射程＝entity/input_schema.md 散文面之数字型「条／码」计数陈述；真值源＝实件计数与 synthetic_input.json `_scale` 声明字段；由 verify/assert_check.py 程序化对表（A32），并对射程内未登记之数字型计数陈述作反向清扫（检多不止检缺，F-7）",
    "_note": "本项为裁决90-5 转化候选之本根即时形态；成文判据兑现点＝窗3任务包模板，本根不代其兑现",
    "_sweep_regex": "(?<![§0-9.条])(\\d+)\\s*(?:条|码)",
    "_sweep_exclusions": "前置 §、小数点或「条」字之数字由 _sweep_regex 之逆序断言直接排除——即章节号/版本号型（§9、v1.2）与条款序号型（条1条2）之数字非计数陈述；除此之外无排除项",
    "pointers": [
      {
        "id": "PC-1",
        "regex": "人造 roll 事件记录集（(\\d+) 条）",
        "truth": [
          "records_total"
        ]
      },
      {
        "id": "PC-2",
        "regex": "\\*\\*(\\d+) 条\\*\\* roll 事件记录＝正例 (\\d+)（P1[^）]*）＋负例 (\\d+)（N01[^）]*）",
        "truth": [
          "records_total",
          "records_positive",
          "records_negative"
        ]
      },
      {
        "id": "PC-3",
        "regex": "(\\d+) 条单码负例",
        "truth": [
          "records_negative"
        ]
      },
      {
        "id": "PC-4",
        "regex": "违规码集（(\\d+) 码）",
        "truth": [
          "violation_code_count"
        ]
      },
      {
        "id": "PC-5",
        "regex": "违规码集 (\\d+) 码",
        "truth": [
          "violation_code_count"
        ]
      }
    ]
  },
  "parameter_slots": [],
  "parameter_slots_note": "W-23 未为本窗登记槽位；构造全程零槽位信号浮现，如实声明空集（C15 边界级：登记不赋值、零赋值；本根零登记项）",
  "_key_roles": {
    "record_required_refs": "impl",
    "required_action_subtype": "impl",
    "position_ref_coordinate_key": "impl",
    "ledger_origin_domain": "impl",
    "check_phases": "impl",
    "closure_assertions": "assert",
    "violation_codes": "assert",
    "locus_rule": "assert",
    "output_form": "assert",
    "lot_fields": "assert",
    "prose_count_pointers": "assert",
    "parameter_slots": "assert",
    "record_required_refs_source": "registry",
    "required_action_subtype_source": "registry",
    "upstream_consumption_W1": "registry",
    "ledger_origin_domain_status": "registry",
    "parameter_slots_note": "registry"
  }
}
```

---

## §4 既裁边界分档对照（裁决86-4，构造按档执行）

| 成分 | 档 | 本件落点 | 执行留痕 |
|---|---|---|---|
| C5 窗2乙面双留位（FW-03-乙域＋W-24 域互斥） | **边界级** | §1.1／§9条1条2 | 登记不建，零实现；断言 A29 机械核证 |
| C9 构造序与消费面（窗1→窗2 单向） | **边界级** | §1.2 上边界 | 只消费 `event_types`／`governance_rebasing` 子类语义；不重复窗1判定 |
| C15 槽位登记不赋值 | **边界级** | §3 `parameter_slots`＝空集 | W-23 未为本窗登记槽位；构造全程零槽位信号浮现，如实声明空集（断言 A28） |
| C12 值域不足处置（不硬套不静默扩） | **边界级** | §14 | 本根反推所需值域**未超出** `{linear, option}` ⇒ 不触发；**无 A9 档二-ii 第三反例** |
| C4 迁移闭合断言构成 | **假设级** | §3 `closure_assertions` CA-1/2/3 | 构造自 T-69 行1099 反推，可证伪；偏离登记强制（§11 B档、撞墙清单）。**v1.1：CA-3 承担者基数经裁决90-2 甲案 KD 实质裁改为多值形态**——假设级回流，86-4 明文「明文KD裁改不构成缺陷」 |
| C8 负例集构成 | **假设级** | §2／§5 | 14 条单码负例为构造反推所得；杀灭率口径沿既裁（边界级，不动） |
| C12 判别口径三条措辞 | **假设级** | §14 | 照 W-23 §4.2 三条字面适用，89-6 判例同型不重裁 |

**假设级偏离登记（强制，静默＝缺陷）**：v1.0 构造期一处——见 §11 B档-1（R03 射程与声明面字面之对齐订正）。**v1.1 增量批零新增假设级偏离**：CA-3 多值化为 KD 明文裁改之回流执行（非构造侧自行偏离），如实区分登记（§11 B档-12）。

---

## §5 违规码与 locus 定义

违规码集（12 码）与 locus 规则见 §3 声明块 `violation_codes`／`locus_rule`（**唯一权威源**，本节不复刻字面量，防 F-14 所禁之字面量替代 schema 解析）。

**相位与门控（`check_phases`）**：

- phase1（结构前置）＝R10/R11/R12/R03/R01/R02；phase2（迁移闭合）＝R04/R05/R06/R07/R08/R09。
- 门控①：phase1 命中非空 ⇒ **跳过 phase2**。理由＝结构前置未过时闭合判据不可判，级联码会稀释单码区分力。
- 门控②：R07（功能位键集不等）命中 ⇒ **跳过 R08/R09**。理由＝键集不等时逐位检查病态。
- **v1.1 随动**：R08 语义由「承担者基数 ≠ 1」改「承担者集为空」（裁决90-2 甲案），门控结构与相位归属**零变动**（R08 仍属 phase2）。
- 门控为**声明面成分**，非实现私有：独立复算路径以「全谓词矩阵先算尽＋门控后置过滤」实现同一门控语义，两路径对门控错位不共享失效模式（F-2 分叉判别）。

**可检层次（F-3）**：CA-1 可检层次：字面层；CA-2 可检层次：字面层；CA-3 可检层次：字面层；三条闭合断言之**语义适当性**（相对策略意图）＝语义层，机械前哨仅作假阴性通道，权威证伪面＝人读审计（外审 L2）。

---

## §6 容差声明面（W-4 两子口径；F-4 机械对表）

- **子口径(a)＝0（bit-exact）**：本根全部判定面为**离散**（verdict／violation code／locus／diagnostics 布尔与枚举），实跑与独立复算逐值 bit-exact 比对，实测差异＝**0**。成分级归属回引《计算成分三分判别受控文本》v1.2 §1 数据/机制刀口与 §2（见 §10）。
- **子口径(b)（连续解析计算，相对 diff ≤ 1e-12）**：**未激活**——本根零数值量、零连续计算面。如实登记（窗1先例同型）。
- **F-11 声明离散近似量框架**：不适用（本根无差分/近似量）。

---

## §7 期望值钉表（乙-2；F-10 构造顺序留痕之第一处）

**先钉表后跑数**：本表与 `entity/synthetic_input.json` 同轮提交，先于 harness 首次实跑。粒度＝凡进入合格判定叙述链之期望值**逐值钉表**，全部可由人造 input 按 §3 声明面手工独立复算，**无不可证项**。

| 记录 | verdict | 期望 violations（code @ container/key） | 期望 diagnostics（role: 前品种表→后品种表） |
|---|---|---|---|
| `P1` | `closed` | — | r1: [option]→[option](不变) |
| `P2` | `closed` | — | r1: [option]→[option](不变) |
| `P3` | `closed` | — | r1: [option]→[option](不变)；r2: [option]→[option](不变) |
| `P4` | `closed` | — | r1: [option]→[option](不变)；r2: [option]→[linear](变)；r3: [linear]→[option](变) |
| `N01` | `not_closed` | `R01` @ record/opening_lots | — |
| `N02` | `not_closed` | `R02` @ record/L2 | — |
| `N03` | `not_closed` | `R03` @ record/L2 | — |
| `N04` | `not_closed` | `R04` @ ledger_migration_map/L2 | r1: [option]→[option](不变)；r2: [option]→[option](不变) |
| `N05` | `not_closed` | `R05` @ ledger_migration_map/L9 | r1: [option]→[option](不变) |
| `N06` | `not_closed` | `R06` @ ledger_origin/L3 | r1: [option]→[option](不变) |
| `N07` | `not_closed` | `R07` @ function_roles/r2 | — |
| `N08` | `not_closed` | `R08` @ function_roles_after/r1；`R08` @ function_roles_before/r2 | r1: [option]→[](变)；r2: []→[option](变) |
| `N09` | `not_closed` | `R09` @ function_roles_after/r1 | r1: [option]→[option](不变) |
| `N10` | `not_closed` | `R10` @ record/source_execution_ref | — |
| `N11` | `not_closed` | `R11` @ record/action_subtype | — |
| `N12` | `not_closed` | `R12` @ position_lots_declared/L2 | — |
| `N13` | `not_closed` | `R01` @ record/closing_lots | — |
| `N14` | `not_closed` | `R04` @ ledger_migration_map/L9 | r1: [option]→[option](不变) |

---

## §8 交付件双钉声明面（F-5／F-8）

- **指纹半**：`verify/provenance.json` 载 12 件交付件之 SHA256；交付态由 `verify/build_provenance.py --verify` 逐件重算比对。
- **声明面半**：本节即声明面；**单钉不满足**（仅指纹防静默改数不防声明漂移，反之亦然）。
- **F-8 自指闭环禁令兑现**：钉定件自身入双钉射程——载荷条目集之 SHA256 写入 `_self_manifest_digest`，且由 `verify/assert_check.py` **独立重算核对**（非钉定件自证）；独立复算脚本**不读取自身既往产物**（`FORBIDDEN_READ` 封闭规则在场，断言 A03）。
- **双钉免疫射程声明（3.1d）**：本双钉之设计目标＝**单面篡改检出**；**协同篡改（多面一致改）不在免疫射程**，需第三独立面方可覆盖；本根不宣称协同免疫、不默认加第三面。

---

## §9 反面陈述段（F-13 下边界显式化；与任务包 §4 逐条机械对表，断言 A20）

本根**不做**：

1. 不实现 roll **触发**判据、触发时点或通道选择（FW-03-乙域，乙留位①）；
2. 不做目标合约选择、moneyness/期限取位、任何结构**选型**（W-24 域，乙留位②）；
3. 不实现动作**生命周期**推进与 Phase 4 裁决语义（窗1域；C9 单向消费，不重复窗1判定）；
4. 不实现 T3-24 **六问**验收、不判定 optionality/Gamma 中心/凸性维护之达成（行1096-1098 验收归窗3）；
5. 不实现**纠正**/rollback 实质语义（89-2 治理域原则，指针留此）；
6. 不产出数值型交易量、交易信号或动作建议；不建常设 **pipeline** / 数据接口 / 持久服务；
7. 不赋任何**参数取值**（类三纪律，`parameter_slots` ＝ 空集）；
8. 字段名与记录形态＝本根工程取用，不**外推**为跨根命名规范（裁决14）。

---

## §10 计算成分三分判别（乙-7：逐处回引《计算成分三分判别受控文本》v1.2 条款号；单向回引）

| 成分 | 三分归属 | 回引条款 | 依据与留痕 |
|---|---|---|---|
| C-1 记录面三成分（开平 lot 集／账本关系迁移映射／功能承担者前后映射） | **类一** | 受控文本 §2 | 权威文本 T＝T1·1099 逐项枚举；候选「只记 lot 不记账本映射」与 T 矛盾，当场裁掉 |
| C-2 「迁移」蕴含两端在场且不相交（CA-1） | **类一** | 受控文本 §2 | T＝T1·1089「功能**迁移**」＋1091「不是展期，不是续命」——同一 lot 既平又开＝续命形态，与 T 矛盾 |
| C-3 闭合断言三条之**具体构成**（谓词形状、门控顺序） | 假设级构成域（86-4 C4），不入三分测试 | 受控文本 §1 KD 既裁项承接条 | 经KD直接裁定之档位成分仅作登记与承接，不重走判别测试路径；双重引用不豁免——实质依据＝86-4 分档表 |
| C-4 功能位标识符与其语义内容 | **数据**（刀口处分流，不进三分） | 受控文本 §1 数据/机制刀口 | 功能位名只作为值被消费（记录面**声明值接收**），本根不判其内容与充分性；背景锚宪-ST-04/ST-05 不固化为断言（随包件B v1.1 已裁：背景锚不单列断言形态） |
| C-5 `ledger_origin` 值域 `{migrated, new_capital}` | **类二·缺定义型** | 受控文本 §3 | 账本来源类别之权威枚举无源文；供给方穷举后指向账本/治理域（**非本实体自身**，供给方自指不成立，类二成立）；桩＝二值，可复算最简，**不 claim 语义等价**；登记＝TPL1-W2-01 |
| C-6 `instrument_type` 值域 `{linear, option}` | **类一** | 受控文本 §2 | T＝GK-31 坐标键第七维＋W-23 §4.1 设计层钉定；同名同值域直引，非新造字段 |
| C-7 必填引用字段三条 | **类一** | 受控文本 §2 | T＝窗1 input_schema §3 `event_types.execution` 字段集＋`action_subtype` 子类语义（C9 消费面授权原文） |

### 10.1 类三否定结论双栏留痕（受控文本 §4 v1.2 双栏义务）

**本根类三成分＝零**。双栏留痕如下（缺一栏即测试未完成）：

- **文本面查过什么**：T1·B3§4 行1089-1100 全段；窗1 input_schema §3 声明块全量键；W-23 §2.2窗2/§2.4/§4.2；裁决86-4 分档表；随包件B v1.1 已裁三行键锚定组；术语册「禁止误用」栏（经随包件A 对照页承接）。
- **逻辑面查过什么（逐候选实查）**：①`ledger_origin` 二值 vs 三值（增 `partial_migration`）——逻辑上三值不被任何文本排除，但**供给方在场且非自指**（账本/治理域），故落类二而非类三，非「等数据」掩盖；②门控顺序两候选（phase1 先于 phase2 vs 全码并列）——并列候选被「单码区分力」这一**既裁负例设计口径**（窗1先例、C8 假设级域）逻辑排除；③承担者基数候选（恰1 vs 允许多值）——v1.0 构造侧以 T1·1099「功能**承担者**」单数承担语义排除多值候选；**该排除已经裁决90-2 KD 实质裁定推翻**（KD 一阶反例：宪-ST-04 下行覆盖为张数×倍率之集合承担，分行权价／分期限／分批建仓与 roll 后新旧并存期均致同功能位多 lot；「承担者」单数语义不足以支撑基数排除），v1.1 改**多值形态**。**方法论留痕**：本处为「散文单复数形态被当作判据依据」之失效实例——单数名词之语法形态不构成基数判据之文本面依据；三分判别之逻辑面查证须以母结构实况为反例源，不以语法形态代替。三处均以查证动作支撑，非默认全相容。

---

## §11 本根裁定登记（逐项呈KD，非终裁；档位按 55-3a 标注）

**A档（逐项呈：不可逆／经济实质类）**

1. **【A档】迁移闭合断言之三条构成（CA-1/CA-2/CA-3）＝构造自 T-69 行1099 反推之假设级实现**。CA-1 反推自「迁移」之两端在场与不相交；CA-2 反推自「迁移**账本关系**」之全域映射与来源可追溯；CA-3 反推自「迁移…**功能承担者**」之功能位不增删、承担者集非空且分属两端（**v1.1：基数形态经裁决90-2 甲案 KD 实质裁定改多值**——恰1形态不符合母结构特征，已回流执行）。**呈KD**：修订后三条构成是否为该行之最小充分闭合形态；若KD再裁减/增条，走假设级回流（撞墙清单），不构成缺陷（86-4 明文）。指针＝§3 `closure_assertions`、§10 C-1/C-2、§10.1 逻辑面③。
2. **【A档】A9 第七维消费形态标注（43 B-4 义务；W-23 §4.2 判别口径三条；89-6 判例）**。见 §14。本根实况＝**弱形态构成消费**（取名＋取值域＋进入核验路径三要件满足；分账形态未现）。按 89-6「后续窗2/窗3 同型不重裁」，本项**仅作形态标注呈报**，不请求重裁口径；若KD认定本根另有形态差异，回填 43 B-4 义务状态。
3. **【A档】`ledger_origin` 二值桩之边界性质**。二值枚举为类二缺定义型桩（§10 C-5），其**是否触及账本域实体边界**由KD判断：若KD认定「账本来源类别」属既有账本对象（宪-ST-02 域）之定义面，则 TPL1-W2-01 之归属指针须相应收窄；本根按受控文本 §3 供给方措辞纪律**保持模块归属开放**，不预裁归属。

**B档（批量呈，"all confirm" 合法：程序/机械/留痕类）**

1. **假设级偏离登记（强制项，静默＝缺陷）**：构造首跑发现被测实现之 R03 重复检测射程写作「closing∪opening 串接去重」，与声明面字面「**集内**重复」不一致，致 N02 同时命中 R02＋R03（破坏单码设计）。订正＝重复检测按 closing／opening **各自集内**执行，跨集重叠专归 R02。**该偏离由钉表先于实跑而被击出**，属先钉后跑之价值实证；订正后三方 16/16 一致。
2. **负例集覆盖面增量登记（假设级 C8 域回流，非缺陷通道）**：负控变异 M01/M03 存活暴露负例集两处覆盖缺口——R01 之 closing 空对称侧、R04 之「检多」侧；构造侧补 N13/N14，补齐后杀灭率 10/10（此前 8/10）。**该两处为 input 覆盖面缺口，非判据面逃逸**（89-8-3 口径钉定：「工序位命中」语义＝判据面逃逸，非 input 覆盖面缺口；假设级构成域缺口不入 88-1 计数），故不构成 P1/P2 工序位命中、不触发 W-26 再议——**定性呈KD**。
3. **违规码集 12 码之命名与构成**＝本根工程取用，不外推为跨根命名规范（裁决14）；集合之**最小充分性**属假设级可证伪面。
4. **相位门控二条**（phase1⇒跳 phase2；R07⇒跳 R08/R09）＝构造反推之单码区分力保障，假设级，回流通道不因 confirm 关闭。
5. **诊断字段 `role_instrument_type_change`**＝记录面**回显**（取自实际执行路径返回值，F-15⑥），**不产生判定**、不判品种变更之合法性（该判定属治理域，本窗零触）。
6. **零时间轴声明**：本根记录面不设 `t`（时间语义属窗1生命周期域），如实登记。
7. **容差子口径(b) 未激活登记**（§6）。
8. **合格判定 L1 限定语**（裁决53）在场（见切片记录）。
9. **槽位空集登记**：W-23 未为本窗登记槽位、构造全程零槽位信号浮现，`parameter_slots` 如实为空集（C15 边界级之零登记项形态）。
10. **【v1.1】诊断值形态随动**：`role_instrument_type_change` 之 `before/after` 由标量改**品种去重升序表**（多值形态下标量无定义）。诊断仍为回显、**不产生判定**；单元素承担者退化为单元素表，与 v1.0 语义同义。候选比较：〔弃案〕多 lot 承担者时略过该 role（沿 v1.0 谓词）——将致合法多值记录之诊断静默缺席，故不取。
11. **【v1.1】单码设计口径澄清**：「逐条单码」射程＝**码**层，非 locus 层；N08 之 R08 双 locus 为对称面覆盖（前侧空集＋后侧空集）之最小承载形态。
12. **【v1.1】CA-3 多值化之通道定性**：属**KD 明文裁改之假设级回流**（86-4／89-8-1 构造侧增量同型），**非构造侧偏离、非缺陷全链**；与 v1.0 之 DEV-W2-01（构造侧自行偏离）分类分开登记。
13. **【v1.1】数量指针对表断言（A32）新增**：裁决90-5 转化候选之**本根即时形态**——schema 散文面数字型「条／码」计数陈述与实件计数／`_scale` 程序化对表，并对射程内未登记之计数陈述反向清扫（F-7）。**成文判据兑现点仍＝窗3任务包模板，本根不代其兑现**。

---

## §12 输出形态声明（裁决39-B 输出形态封闭）

顶层键集＝ `{record_id, verdict, violations, diagnostics}`，**无声明外字段**；`verdict ∈ {closed, not_closed}`；`violations[]` 之项键集＝`{code, locus}`，`locus` 键集＝`{container, key}`；`violations` 按 `(code, container, key)` 字典序排序以保证 bit-exact 可比。**诊断值形态（v1.1 随动）**：`role_instrument_type_change[role]` ＝ `{before, after, changed}`，其中 `before/after` ＝该功能位承担者集之 `instrument_type` **去重升序表**（多值形态随动；单元素承担者退化为单元素表，与 v1.0 标量形态同义），`changed` ＝前后表不相等。**verdict 语义边界**：`closed/not_closed` 指**迁移闭合断言之达成与否**，**不是**动作合法性判定（合法性属窗1域，本窗零触）——命名刻意与窗1 `legal/illegal` 区分，防语义混读。

---

## §13 交付件清单

`entity/`：`input_schema.md`（本件）／`roll_record_declaration.json`／`synthetic_input.json`／`expected_pin_table.json`／`roll_record_checker.py`（被测实现）／`harness.py`／`outputs/run_output.json`。
`verify/`：`independent_recompute.py`／`assert_check.py`／`negative_control.py`／`build_provenance.py`／`final_sweep.py`／`provenance.json`／`recompute_output.json`／`logs/*`。
**指纹**：全 12 件 SHA256 见切片记录指纹列（W-13(17)）。交付包**不自带源文副本**（乙-3：装载义务成文含源文，包内不并存副本）。

---

## §14 A9 第七维回填检验之消费形态标注（86-3 之 P4；W-23 §4.2 判别口径三条；89-6 判例）

- **引用形态**：lot 之持仓引用**直接引用坐标键 `instrument_type` 字段本身**，同名、同值域 `{linear, option}`，非新造字段、非同义字段（区别于引擎两次 `instrument_class` 先例）。
- **进入核验路径之实况（如实留痕）**：①**值域封闭断言**（越域即击落，R12，负例 N12 实证）；②**功能承担者前后品种维之诊断回显**（`role_instrument_type_change`，v1.1 值形态＝承担者集之品种去重升序表；P4 实证 changed 真/假两种取值）。**不按品种分支、不按品种分账**——多值形态下亦不按品种拆分承担者集，仅作集合级品种表回显，C12 触发面零变动。
- **形态判定**：按 89-6 判例之三要件字面（取其名／取其值域／进入核验路径）**均满足 ⇒ 构成消费（弱形态）**；口径1 例示形态（「迁移闭合断言按品种分账」）不满足；强于口径2「仅透传不进核验路径」。**89-6 明文「后续窗2/窗3 同型不重裁」**，本节为形态标注而非重裁请求。
- **值域充分性（C12，边界级）**：本根反推所需值域**未超出** `{linear, option}` ⇒ **判别口径3 不触发**，**无 A9 档二-ii 第三反例**，统计面零变动。

---

## §15 随包义务处置

### 15.1 随包件B′（窗2 翻译审计表预标注 v1.1 已裁版）承接

- C4② 闸门**已开**（KD 20260814 裁定：三行键全组＝一致；A档消费角色切割＝采呈报案）。本根判据引用据此生效。
- **行状态引用**：T1·1089（对象命名锚）／T1·1091（反面陈述源）／T1·1093-1100（甲面判据源，**行1099 为本窗迁移闭合断言主判据行**；行1096-1098 为边界切割参照，验收归窗3、本窗不重复）。
- **类B「未审引用」标注（C4④）**：T1·B3§4 区间外之任何行、以及 T1 其余行**维持未审态**，本根未作判据源引用（未审态≠欠账，G-3 同构）。
- **背景锚形态维持**：宪-ST-04/ST-05 之功能位语义为**背景锚**，本根不单列为断言（已裁形态照执行）；宪-ST-02 账本主体语义同为背景锚（§3 CA-2 `source` 栏如实标注）。

### 15.2 随包件A（86-8 五对象对照页 v1.0 已裁版）承接核证

装载其已裁版并核证「知悉项与携带条未被本窗侵入」（窗1 §15.3 同型）：

| 对照页条目 | 本窗核证 |
|---|---|
| 三-1 EP-06 间接消费标注问题（**窗3域**） | 本窗零 Greeks/IV 消费、零判据根输出状态消费 ⇒ **零侵入**；登记项维持挂窗3任务包生成会话兑现 |
| 三-2 窗3携带项两条（正 Carry 口径禁形／量甲量乙二分禁形） | 本窗零 carry 面、零「长端时间成本」类量消费（F-19 不触发）⇒ **零侵入**，携带条维持 |
| 术语册 `H_identity_target` 禁形 | identity drift 位由 T3-24⑥承载（窗3）；本窗目标合约选择已 W-24 互斥登记不建 ⇒ **零侵入** |
| ST-08 不授权栏（Roll 判准禁价格/盈亏/方向） | 本窗零触发判准内容；§9条1 显式不做触发判据 ⇒ **零侵入**，判准本体属 FW-03-乙/W-24 域 |
| 四之「本批新增随行义务＝零」 | 本窗**零新增随行义务**，确认维持 |

### 15.3 思想层一手材料消费（83-1/83-3 G-14 乙案二分规则）

本根消费源文＝**T1（方法论链）**，按二分规则走**翻译审计表审计域**（§3.2 机制，审计表现行版为权威，过渡期随包件B′已裁版为权威）。**思想层一手材料消费＝零**，故「三件并联」（REG-UP 登记指针＋H/P/W 层界标注＋类B 标注）之前两件**不适用**，如实声明；类B 未审引用标注见 §15.1（在场）。

---

## §16 源文锚、层界标注与审计表状态（F-18 L2 完整性维）

| 行键 | 字面（程序化核证在场，断言 A21） | 层界核验（随包件B′ v1.1 已裁） | 本根判据角色 |
|---|---|---|---|
| T1·1089 | `### 4. roll = 功能迁移` | 命名/定性句，功能层，零形状固化 | 对象命名锚 → `required_action_subtype` |
| T1·1091 | 「roll 不是展期，不是续命，不是 delta 触发器。」 | 类别否定句，功能层，零形状固化 | 反面陈述源 → §9条1（乙禁建切割面）＋§10 C-2（CA-1 不相交之反推源） |
| T1·1099 | 「迁移账本关系与功能承担者。」 | 目标枚举句，功能层，零度量零形状固化 | **甲面判据源·主判据行** → CA-2＋CA-3 |
| T1·1096-1098 | 「维护 optionality；维护 Gamma 中心；维护凸性（含高阶凸性表现）；」 | 同上 | **边界切割参照**（验收归窗3，本窗不重复；§9条4） |

**W-23 T-69 指针偏差留痕（89-5(a) 处置同型，盘点面指针数字类，不走缺陷回传）**：W-23 §1.1 载「T-69（T1/B3§4行1093-1100）」；程序化核证实况＝§4 节起行**1089**、反面陈述句行**1091**（在 §4 节内、W-23 所列区间外）。如实留痕，**不订正 W-23**（照任务包 §2.1 既定处置）。

**§16 附注（v1.1）**：本节四行键与层界核验结论**零变动**——裁决90 未触审计域行键，C4② 闸门状态维持。

---

## §17 散文面数量指针对表登记（v1.1 新增；裁决90-5 转化候选之本根即时形态）

- **缺陷根源（DEF-W2-A）**：v1.0 §1 与 §4 两处记录/负例条数陈述停留于 DEV-W2-02 覆盖增量之前的值，声明面 JSON／钉表／断言栈／判定面均正确，数值产物零影响——**呈报面载体陈述与实况不符**之程序面缺陷（乙类，机械订正＋脚本化验收）。
- **订正**：§1「与输入的关系」与 §4「C8 负例集构成」两处已订正为实件值。
- **对表机制（断言 A32）**：射程＝本件散文面（**剔除 §3 内嵌声明块以避免自指**）之数字型「条／码」计数陈述；真值源＝`entity/synthetic_input.json` 实件记录计数与 `_scale` 声明字段、`violation_codes` 实件长度。登记表载于 `entity/roll_record_declaration.json` 之 `prose_count_pointers`（唯一权威源，本节不复刻正则字面量，防 F-14 所禁之字面量替代 schema 解析）。
- **双向形态（F-7）**：正向＝每一登记指针在散文面**恰命中一次**且取值与真值源一致；反向＝散文面全部数字型计数陈述经清扫后**须被某一登记指针之命中区间覆盖**，未覆盖者即判不符——「检多不止检缺」。清扫排除面（`_sweep_exclusions`）＝章节号/版本号型数字（前置 `§` 或小数点），非计数陈述。
- **`_scale` 自洽**：`_scale.records` ＝实件记录数、`_scale.positive`＋`_scale.negative` ＝ `_scale.records`，一并入 A32 射程。
- **兑现边界**：本项为本根即时形态；**成文判据之兑现点＝窗3任务包模板**（裁决90-5；升格候选登记册增条），本根不代其兑现、不外推为跨根规范（裁决14）。

---

**审计表状态**：《翻译审计表》v1.6 经 grep 核证**零含**上述行键；新消费面按 C4② 先入表获KD三态裁定，载体＝随包件B′ v1.1 已裁版（KD confirm 20260814）；物理收入挂审计表 v1.7 下次再版（与 89-7 行71、随包件B窗1 六行同批），**过渡期已裁版为权威**。

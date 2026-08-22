# FW-03-甲 一阶实体 input_schema · v2.1 · 已裁态（裁决61收口）· 20260803

> **对象**：Roll触发判据族首根之状态量（OTM put头寸）。授权链＝任务包_续3_FW-03-甲 v1.0 §1逐字锚定（不重复转抄）＋**裁决60（60-A1两量并出／60-A1b方法层归类／60-A2 M1消费形态／60-A3容差沉淀／60-B1丙类全链／60-C1 M8计入）**＋裁决59-1a丙类全链。
> **版本性质**：已裁态（裁决61收口通过）。v2.0→v2.1＝状态头翻转单项，语义/声明/数值内容零变动（收口即翻状态头条款执行）。v1.0→v2.0之变动面见包根《diff面声明清单_续3修复_v1_0_20260803.md》；§4"本根裁定登记"呈KD各项经裁决61-2批量追认。

## §1 对象语义（Q4判据权威转抄，任务5_Step2增量产出v1.0 §1 FW-03行，裁决51已裁态）

> 甲＝可算部分＝"OTM put之Gamma极值/二阶导过零"状态量与"二阶导恒正"不变量（喂持仓+行情时序，出二阶导符号序列，判据＝过零检测与恒正核验）。甲以阶段二独立评：Q1是（状态量）→Q3否→Q4是→Q5是（行情/账本）→Q6是→一阶实体（FW-03-甲）。

哲学准入（Step3增量产出，裁决51已裁态）：C-1~C-5全不命中；C-6不标记；动作归乙（二阶候选），本根仅出状态量与核验量，不裁决、不生成动作。

## §2 "二阶导"读法＝两量并出 · 双锚定（裁决60-A1，KD已裁，本节为落写执行）

源文（关于肥尾行情下期权类问题的亿口气回复.md 行11–12）一句话压缩两个数学对象；KD以作者语义权确认解压为两量。本根双通道并出，各自绑定源文半句与宪法半句：

### §2.1 通道一 · `speed`（触发量）＝∂Γ/∂S，沿不利方向取号

| 锚 | 原文/条款 |
|---|---|
| 源文**等式句** | 亿口气回复 行11："当otm put 的gamma最大的时候，也就是二阶导为0的时候"——Γ峰 ⇔ Speed过零，**恒等式**（数学上严格成立，非松弛） |
| 宪法**触发半句** | 宪-CV-06：Gamma峰值已过时Roll |
| 源文**状态描述** | 亿口气回复 行11–12："已经变成atm"之远期头寸——Γ峰恒在strike附近，故"Γ峰已过"与"已变ATM"同指一事 |

**取号口径（本根裁定登记#5，呈KD）**：`speed_adverse` ＝ ∂Γ/∂S × adverse_sign；`adverse_direction=spot_down` 时 adverse_sign＝−1。语义＝"沿不利方向移动一单位，Γ的变化率"：Γ峰未至时为正（不利方向上Γ仍在增长），Γ峰已过时为负；由正转负之过零事件＝"Gamma峰值已过"。原始 ∂Γ/∂S 同时以 `speed_raw` 输出，不因取号丢失。方向绑定为**头寸级声明**（写入人造input之 `channel_config`），非全局常量——上行翼头寸（如OTM call保护腿）之不利方向为 `spot_up`，届时由input声明切换。

### §2.2 通道二 · `gamma_curvature`（不变量）＝∂²Γ/∂S²（"Gamma的Gamma"，四阶导 ∂⁴V/∂S⁴）

| 锚 | 原文/条款 |
|---|---|
| 源文**不变量句** | 亿口气回复 行11–12：保持整个头寸的gamma的二阶导数一直为正 |
| 宪法**四阶矩半句** | 宪-CV-06"做多四阶矩"；源文引 未来不可测_但我们有办法.md 行30–32："Gamma的二阶导也保持住…就是资产价格的'四阶矩'了，制造正凸性的凸性，做多四阶矩" |
| 同域源文 | QQQAI杠铃结构交流 行887："期权大家都很熟悉的情况下做的是 Gamma 的 Gamma 的功夫" |

本通道另出**恒正诊断**（`always_positive_check`）。

### §2.3 Q4判据斜杠并置之实现层对应（裁决60-A1落写指令）

Q4判据原文"'OTM put之Gamma极值**/**二阶导过零'状态量"以斜杠并置两者为同一状态。实现层落为**两显名事件**：斜杠左侧（Gamma极值）＝`speed` 通道之过零事件；斜杠右侧（二阶导过零）＝`gamma_curvature` 通道之过零事件。两事件之时点与个数一般不同（本情景：speed 2项、curvature 4项），此为两量之实质差异，非误差。**一词双职就此解压，v1.0之"字面松弛"消解方式作废**（模板二D-10条目以裁决60-A1结案，见撞墙清单v1.1）。

### §2.4 附带钉定（裁决60-A1②③）

1. **聚合层级维持 per-lot**；组合级恒正＝下游聚合性质，登记指针不在本根建。
2. **恒正靠roll维持＝组合级设计性质**；甲之 per-lot 恒正核验为**诊断输出、非合格判据**。本情景 `all_positive=False`（18步违反）**不构成缺陷**，定性随裁固化。
3. **本情景数值锚为参数特定值**：Γ峰、拐点之具体位置随 K/r/q/σ/T 漂移；**符号序列输出形态与语义对参数漂移免疫**（过零时点变，输出结构与判据语义不变）。

## §3 声明面（供 verify/ 断言脚本程序化解析；键名与块结构勿改）

### §3.1 口径声明块

```yaml
BUMP_MODE_DECLARED: relative
BUMP_RATIO_DECLARED: 0.001
SIGN_EPSILON_DECLARED: 1e-12
AGGREGATION_LEVEL_DECLARED: per_lot
DERIVATIVE_VARIABLE_DECLARED: spot
ADVERSE_DIRECTION_DECLARED: spot_down
DAY_COUNT_DENOMINATOR_DECLARED: 365
MAGNITUDE_TOLERANCE_REL_SPEED_DECLARED: 0.002
MAGNITUDE_TOLERANCE_REL_CURVATURE_DECLARED: 0.01
MAGNITUDE_FLOOR_SPEED_DECLARED: 1e-6
MAGNITUDE_FLOOR_CURVATURE_DECLARED: 1e-6
M1_SOURCE_SHA256_DECLARED: e31fbcfeacebeb196f7e1d63f41089e7e0a7deb3cc9a9a8b44941af31e194e99
```

**两通道量级诊断界之独立标定（裁决60-A1b：speed通道之界须按三阶导截断量级独立标定并登记，禁沿用0.01）**

| 通道 | 差分格式 | 截断主项 | 本情景实测最大相对误差 | 声明界 | 安全边际 |
|---|---|---|---|---|---|
| `speed` | [Γ(S+h)−Γ(S−h)]/(2h) | (h²/6)·∂³Γ/∂S³ | 1.659×10⁻⁴（t=29，S=96，近过零点） | **0.002** | ≈12× |
| `gamma_curvature` | [Γ(S+h)−2Γ(S)+Γ(S−h)]/h² | (h²/12)·∂⁴Γ/∂S⁴ | 8.095×10⁻⁴（t=18，S=81，近过零点） | **0.01** | ≈12× |

标定规则（两通道同一规则、界值各自独立取）：界＝本情景实测最大相对误差 × 约一个数量级安全边际，向上取整至两位有效数字之整洁值。两界之比（5×）反映两通道截断主项与分母量级之差异，非任意取值。**突破界＝指向实现缺陷而非离散化固有偏置**，须裁定为不合格。取值本身挂类三 TPL3-FW03A-01 族条目候阶段B校准。

**地板与两分支封闭**：|真值| ≥ 地板时用相对判据；< 地板时改用绝对判据 `abs_tol = rel_tol × floor`（两判据在地板处连续）。断言侧另断言"相对分支点数＋绝对分支点数＝全部格点"，杜绝静默跳过（v1.0 之硬编码 `1e-8` 跳过分支既未声明亦未计数，本轮订正）。本情景两通道全部43点均落相对分支，绝对分支为完备性声明（未触发）。

### §3.2 外置数据件声明面（F-5双钉之声明面半；指纹半由 assert_check.py step0-ii-b 承担）

```json
{
  "scan_patterns.json": {
    "role": "step0(ii)静态扫描之检测器基线（模式数据件）",
    "sha256": "0b724740efea58724382fbe39120be6692b5f2eb2e22a39d9d5259bab8b6cb14",
    "group_counts": {
      "forbidden_keyword_regex": 16,
      "truth_claim_patterns": 9,
      "action_scope_markers": 6,
      "negation_markers": 6
    },
    "consumption_contract": "全部模式一律以正则消费（re.search），禁字面子串消费；检测器活性由前哨自检承担（每条模式须对合成阳性样本实际命中、阴性样本不命中）"
  }
}
```

### §3.3 包域清单与钉定封闭规则（F-7全包域／排除最小化／双向对表；F-8钉定射程）

```json
{
  "package_inventory": [
    "entity/engine.py",
    "entity/harness.py",
    "entity/harness_output.json",
    "entity/input_data.json",
    "entity/input_schema.md",
    "verify/assert_check.py",
    "verify/assert_check_log.txt",
    "verify/build_provenance.json",
    "verify/build_provenance.py",
    "verify/fingerprint_table.md",
    "verify/fingerprint_table.py",
    "verify/independent_expected.json",
    "verify/independent_recompute.py",
    "verify/negative_control.py",
    "verify/negative_control_log.txt",
    "verify/scan_patterns.json",
    "切片记录_FW-03-甲_v2_1_20260803.md",
    "撞墙清单_FW-03-甲_v1_1_20260803.md",
    "diff面声明清单_续3修复_v1_0_20260803.md"
  ],
  "scan_face_py": [
    "entity/engine.py",
    "entity/harness.py",
    "verify/assert_check.py",
    "verify/build_provenance.py",
    "verify/fingerprint_table.py",
    "verify/independent_recompute.py",
    "verify/negative_control.py"
  ],
  "scan_excluded": [
    {
      "path": "verify/scan_patterns.json",
      "reason": "模式数据件本身（非交付脚本，不在.py扫描面）；其正文按构造逐条自命中全部模式，纳入即恒假阳性。防篡改改由F-5双钉承担（指纹断言step0-ii-b1＋本schema §3.2声明面）。排除清单与本理由由assert_check.py每次运行写入assert_check_log.txt之step0-ii-c段（订正v1.0之空指声明）。"
    }
  ],
  "pin_closure_rule": "钉定域＝entity/ 与 verify/ 两目录下全部文件，减去pin_excluded_paths；包根之呈报文本(.md)不入钉定域，其指纹由verify/fingerprint_table.md之程序化指纹表与切片记录承载。",
  "pin_excluded_paths": [
    "verify/build_provenance.json",
    "verify/assert_check_log.txt",
    "verify/negative_control_log.txt",
    "verify/fingerprint_table.md"
  ],
  "pin_exclusion_reasons": {
    "verify/build_provenance.json": "钉定件自身，不能含自身指纹（自指）。其防篡改由assert_check.py之A10a射程重构核证（按本封闭规则重算应钉集并与钉定件字段集双向对表）＋A10c之排除清单/封闭规则与本声明面比对承担——F-5双钉同形态（机械重构＋声明面）。",
    "verify/assert_check_log.txt": "由assert_check.py于钉定动作之后生成（严格时序循环），且含运行时间戳。",
    "verify/negative_control_log.txt": "由negative_control.py于钉定动作之后生成（严格时序循环）。",
    "verify/fingerprint_table.md": "由fingerprint_table.py于全链末步生成（严格时序循环）。"
  }
}
```

### §3.4 输出形态声明面（39-B2输出结构封闭；D-2订正：扩至嵌套层与条目键集）

```json
{
  "top_level": ["_data_source", "position", "bump_config", "channel_config",
                "state_sequence", "zero_crossings", "always_positive_check", "summary"],
  "state_record": ["t", "spot", "valuation_date", "dte_days", "bump_h",
                   "gamma_minus", "gamma_mid", "gamma_plus",
                   "speed_raw", "speed_adverse", "speed_sign",
                   "gamma_curvature", "curvature_sign"],
  "zero_crossings_channels": ["speed", "gamma_curvature"],
  "zero_crossing_entry": ["from_t", "to_t", "from_sign", "to_sign", "from_spot", "to_spot"],
  "always_positive_check": ["channel", "semantics", "aggregation_level", "per_step",
                            "all_positive", "violation_step_count", "violation_ts"],
  "per_step_entry": ["t", "positive"],
  "summary": ["n_steps", "n_crossings_speed", "n_crossings_gamma_curvature",
              "speed_sign_at_start", "speed_sign_at_end",
              "curvature_sign_at_start", "curvature_sign_at_end"]
}
```

## §4 口径声明理由（本根裁定登记逐项，编号与 entity/engine.py 注释、切片记录"本根裁定登记"节三处统一——D-8d订正）

- **#1 "二阶导"读法＝两量并出**：裁决60-A1已裁，本schema为落写执行，非候选。双锚定见§2。
- **#2 聚合层级＝per_lot**（非per_unit/非组合聚合）：源文与Q4判据语境均为"头寸Gamma"；60-A1附带钉定①维持。side=long时scale>0，per_lot与per_unit两通道同号；side=short时符号整体翻转（应有行为，非缺陷）。
- **#3 求导变量＝现货S**（非时间τ、非跨变量混合导）：Q4判据"喂持仓+行情时序，出二阶导符号序列"字面对应S随时间演化；宪-CV-06"资产价格四阶矩"字面亦锚定S。实现侧对应＝单步内仅 `spot` 被bump、`valuation_date` 固定（断言A8h）。
- **#4 M1消费形态＝M1源码内嵌（契约面消费）**：裁决60-A2已裁。本轮由v1.0之"逐字子集裁剪"改为 **entity/engine.py 整文件逐字内嵌**（标记 `M1_VERBATIM_EMBED_BEGIN/END` 之间正文，重算SHA256 ≡ §3.1之 `M1_SOURCE_SHA256_DECLARED` ≡《切片记录_TPL1-T76-01引擎_续2求值口径增强 v1.2》指纹列声明值）。路由限制由内嵌段**之外**之 `_evaluate_lot_european` 适配层承担，内嵌段零改动。触发式重验义务（引擎再版或#8批时重验内嵌段）登记于撞墙清单v1.1。契约六条随内嵌段原文携带；契约⑥见§6。
- **#5 adverse_direction＝spot_down**：裁决60-A1"沿不利方向取号"之实现层绑定，头寸级声明（写入 `input_data.channel_config`）。理由＝本根对象为杠铃结构远端OTM put保护腿，其不利方向＝现货下行（源文行11–12"大幅度下跌"情景）。**呈KD**。
- **#6 参数与容差取值**：`bump_ratio=0.001`（比例bump，跨价格水平量纲一致）／`SIGN_EPSILON=1e-12`（纯防御浮点literal-0，两通道共用，观测量级远高于该阈值、不影响任何实际分类）／两通道量级界与地板（见§3.1标定表）。取值本身挂类三 TPL3-FW03A-01 族条目候阶段B校准。
- **#7 容差框架＝裁决60-A3沉淀条款**：措辞对齐——**被测量本身为声明离散近似时，裁决13/19(a)/(b)不强套，容差框架＝离散不变量零容差 ＋ 量级诊断（界值逐对象登记）**。本根落地＝①符号（离散不变量）零容差为主判据；②量级诊断为辅助，界值逐通道独立登记。
- **#8 v1.0"逐字内嵌零改动"claim不成立之核证结论（本轮新发现，呈KD）**：本会话按裁决60-A2②义务对M1交付包实体逐块比对，v1.0所嵌为计算路径之逐字**子集**，但(a)删两处注释行；(b)`_eval_bs_dividend_yield` docstring被改写为一行摘要（M1原docstring所载类三登记、raw量纲口径、q语义边界随之丢失）；(c)`evaluate_lot` 被改写，M1契约面返回字段 `computability_status`／`unstated_dimensions_hit` 被删。改采整文件逐字内嵌后claim成立且可机械核证。**数值路径两版一致**（`_eval_bs_dividend_yield` 计算体逐字相同），本项零数值影响。

## §5 钉表与构造顺序留痕（F-10最低形态＝文字声明三处一致，第三处）

三处＝`verify/assert_check.py` 头注／本节／《切片记录_FW-03-甲 v2.0》"钉表与构造顺序"节，措辞一致。

- **本根钉表＝** `verify/independent_expected.json`（逐格点两通道期望值表，43×2条）。
- **粒度（乙-2／W-13(5)(11)）**：凡进入合格判定叙述链之期望值**逐值钉表**；本根全部期望值均**可独立复算**，来源＝mpmath dps=50 对 V(S) 之 3阶/4阶原生数值微分，无"不可证"项。
- **构造顺序＝先立钉表、后跑比对断言**：`independent_recompute.py` 零读被测侧产物（`engine.py`／`harness_output.json`）、零读自身既往产物（F-8后半），期望值仅由 `entity/input_data.json` 之人造参数独立推导，故钉表在逻辑上先于比对成立。
- **同轮提交（乙-2）**：钉表与人造input同轮交付（本包 `entity/input_data.json` 与 `verify/independent_expected.json` 同包同轮）。
- **F-10已知限制如实标注**：最低形态为文字声明三处一致；可程序化时序证据非强制（成本收益不成立），文字声明可事后书写属已知限制，撞到伪造实证再升格。

## §6 仪表身份标注（对照表§3随行义务③＋§5.4常设纪律，24-E3形态）

本根消费之 per_lot `gamma` 读数（由 entity/engine.py 内嵌之M1引擎产出）为**仪表读数，非定价真理源**；两通道导数量由该读数有限差分导出，同一仪表身份随行，不因求导运算而升格为真理判定。M1契约⑥（仪表计算器非定价真理源）之负向约束随内嵌段原文携带（内嵌段模块docstring内"定价模型之地位"段落）。本根输出之符号序列/过零事件/恒正诊断均为**观察与诊断量**，不承载定价真理宣称、不裁决任何交易之获利合法性（宪-EP-06仪表推论）。

## §7 三分判别反向引用（乙-7；受控文本 v1.1 逐处回引条款号——D-8b订正）

| 成分 | 数据/机制刀口 | 类别 | 受控文本v1.1条款号回引 |
|---|---|---|---|
| per_lot `gamma` 读数（M1内嵌供给） | 机制（决定值如何算） | 类一 | **§2**（类一判别测试：权威文本T＝裁决45 §5 M1契约六条，候选"自算Greeks"与T相容、"消费vendor派生量"与T矛盾） |
| `speed` 通道差分格式（2点中心差分／2h） | 机制 | 类一 | **§2**（判别测试：权威文本T＝源文等式句"gamma最大⇔二阶导为0"＋裁决60-A1，"∂Γ/∂S"与T相容） |
| `gamma_curvature` 通道差分格式（3点中心二阶差分／h²） | 机制 | 类一 | **§2**（判别测试：T＝Q4判据字面"二阶导符号序列"＋宪-CV-06"Gamma的Gamma"） |
| 过零检测（相邻步符号翻转，0不参与传递） | 机制 | 类一 | **§2**（T＝Q4判据字面"判据＝过零检测"） |
| 恒正诊断（curvature通道，诊断非合格判据） | 机制 | 类一 | **§2**（T＝Q4判据字面"恒正核验"＋裁决60-A1附带钉定②之诊断定性） |
| `adverse_direction` 取号方向 | 机制 | 类一 | **§2**（T＝裁决60-A1"沿不利方向取号"＋源文"大幅度下跌"情景描述；候选spot_up与T矛盾） |
| `bump_ratio`／`SIGN_EPSILON`／两通道量级界与地板 | 机制 | 类三 | **§4**（类三定义：全部候选与全部权威文本相容、取舍只能由经验数据判定；处置＝阶段A跑一个具体版本并标"候选之一，待B证伪"）；**§2"成分内再拆分"**（结构类一／数值类三，先例＝裁决18 R3） |
| 人造input之 K/r/σ/q/scenario 取值 | **数据**（只作为值被消费） | 不进三分 | **§1**（数据/机制刀口＋术语纪律："人造测试值≠生产参数值"） |
| 两通道各自之数值方法候选空间（解析闭式／对Γ差分／对V高阶差分／AD；格式与步长子候选） | 机制 | 类三 | **§4**（裁决60-A1b已裁：定义完备、实现在场，归类三非类二；先例＝GL-06日均化方式）；登记＝TPL3-FW03A-01族条目 |

## §8 H/P/W标注通道（O-S3i-1，裁决52随包义务，思想层源文→切片语义标注通道本批首次走通，撞到即记）

源文＝关于肥尾行情下期权类问题的亿口气回复.md 行11–12。

- **H（Hard，硬判据/可检验陈述）**：
  - "otm put 的gamma最大的时候，也就是二阶导为0的时候"——**在 `speed` 读法下为恒等式**（Γ峰 ⇔ ∂Γ/∂S=0，严格成立），本根 `speed` 通道之过零事件即该状态之可核验形态。
  - "保持整个头寸的gamma的二阶导数一直为正"——不变量，可逐步核验真假，本根 `check_always_positive` 职能（诊断输出）。
- **P（Policy，处置/编排规则，非本根计算对象）**："平掉已经变成atm put的远期头寸、开新的otm put"——FW-03-乙域，本根不涉及，登记见撞墙清单v1.1。
- **W（Watch，观察/待厘清）**：**v1.0之W项已由裁决60-A1结案**——彼时记为"Gamma最大即二阶导为0之字面松弛"，实为一词双职（一句话压缩两个数学对象），非表述松弛。结案后本根残余W项＝**两通道过零事件之下游消费口径**（FW-03-乙以哪一通道为roll触发时点、或两者并用），属乙域，本根仅留痕不裁（观察项，非判据缺陷）。

## §9 装载核证摘要（修复会话开场执行，44-D4）

《修复会话开启文本_续3_FW-03-甲 v1.0》§三装载清单（KD上传项5组＋project现行面14项）：**MISS=0**。核证要点：①FW-03-甲修复底版全树14件与《切片记录_FW-03-甲 v1.0》声明指纹逐位比对 14/14 一致、EXTRA=0；②TPL1-T76-01引擎v1.2交付包19件与《切片记录_续2 v1.2》声明值逐位比对 19/19 一致（60-A2②断言核证之前置）；③指针可解析性抽验三处实解析命中（亿口气回复行11–12／QQQAI杠铃行887／未来不可测行30–32——续3 O-2之根治：本轮装载清单按schema实引源文扩充，两源文已入可及面）；④candidate件不装。

## §10 与FW-03-乙关系（裁决52-1随包义务，登记见撞墙清单_FW-03-甲 v1.1）

FW-03-乙＝roll编排二阶候选（"平掉已变ATM远期头寸、开新OTM put"之动作规矩），本根（甲）不涉及、不裁决、不生成该动作；与T3-10闭环成员关系待归纳。本轮两量并出后，乙之触发时点选择面由"读法未定"转为"两通道择一或并用"之显式选择项（外审O-3之状态更新），指针登记于撞墙清单v1.1，本根仅随行携带指针，不越界构造。

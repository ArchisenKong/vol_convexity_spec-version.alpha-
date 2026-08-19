# P2 摩擦记录件（§6 四栏格式）

> 规格来源＝P1规格件 v1.3 §6（85-9 三态＋B10 四栏）。
> 三态：F0 链路贯通／F1 摩擦命中／F2 硬阻断。**F1/F2 均为有效产出，非不合格。**
> F0 修订：「未撞到」须显式记录，空白≠未撞到。
> **反面条款（85-9）**：本件不产出「成功/失败」二值结论、不作「环境可用/不可用」总体判定，总体判定归 KD。
> **B3 边界**：本次实测不构成 29-A 迁移决定，不构成 29-B 任一项激活/废止裁定。探针标的（ES）仅为链路测试，无策略标的含义。

**采集环境**＝paper（Gateway 4002，账户 DU****742，`readonly=True`，serverVersion=176，`marketDataType=1` 实时档）。
**运行环境**＝CPython 3.10.11 / Windows-10-10.0.26200-SP0 / ib_insync 0.9.86。
**engine**＝`entity/engine.py`，SHA256 `d88a955e…682cf`，13 次实测全等锚值，零写入。
**断言**＝A1–**A11** 全 PASS（末次 PASS=11 FAIL=0 PENDING=0），日志 `verify/assert_log.json`。
**规格版次**＝本件对齐 P1规格件 **v1.3**（20260812 补件：§4B flex 凭据闸＋A11＋AGENTS.md v1.1 第6条）；A10 锚值随之由 `c0c4b93b…390a87` 换 `ccc75347…5320e7`，实测一致。
**脱敏**＝账户号按 §4B 载荷条款于本件及 verify/ 全子树遮蔽（`DU****742`，保前缀供 A8 判据、保末三位供追溯）；完整值只存于 probe/ 载荷。凭据值（token／queryId）**不入本件任何位置**。

---

## 一、四栏表

| 项 | 撞到/未撞到 | 形态描述 | 反推指向条款 | 是否需KD裁定 |
|---|---|---|---|---|
| M1 目录分区 | **未撞到** | 三分结构（entity/verify/probe）一次建成，A1 全程 PASS；外部环境未出现平铺定位摩擦。断言脚本以相对根定位，跨目录引用无阻。 | 29-B① | 否 |
| M2 七台账symlink | **未撞到（触点未到）** | 本发未装载任何台账面，外部环境无台账装载需求显形。 | 29-B② | 否 |
| M3 manifest | **撞到（正向）** | `probe/data_manifest.json` 被**实际消费**：A2 以其哈希集反查 entity/∪verify/ 渗透。机器可读形态是断言的输入而非装饰。末态登记 10 条外部载荷（含打包件自身）。现档「只建 pkg manifest、build/audit 未覆盖」之外，本发新增一个实际消费方。 | 29-B③ | 待P3汇整 |
| M4 git init | **撞到** | P2 工作目录位于既有 git repo（branch main）内，未单独 init。版本留痕由上层 repo 承载，本发未产生独立 init 之实需。 | 29-B④＋裁决29-B git commit顺延 | 待P3汇整 |
| M5 三条不变量可证性 | **部分撞到** | 会话身份纪律／fresh context 隔离以「AGENTS.md 经 CLAUDE.md import 生效 ＋ A10 指纹核证」形态实现且**可证**（A10 全程 PASS）。能力档口径未显形。 | 55-1c | 待P3汇整 |
| M6 引擎装载核证形态 | **未撞到** | SHA256 对照＝A5；「零写入」＝A6 逐次实测追加入 `verify/engine_fingerprint_log.json`，全程 13 次实测全等锚值。形态可执行、可复核、成本近零。 | 69扩项(i)／X-3 | 否 |
| M7 文件交换开销 | **部分撞到** | 三跳之**第二跳（本地打包）已发生**：`verify/pack_delivery.py` 归集 23 成员＋INVENTORY，包约 85 KB，耗时亚秒级，逐成员 SHA256 入清单——本地归集开销可忽略。**第一跳（chat↔本地）实测开销显著且非文件形态**：q/r 赋值、X-1 fixture、flex 凭据、queryId、打包落位共 5 次往返裁定，每次均需停机等 KY，**开销在往返次数而非字节数**。第三跳（本地↔P3 外部环境）未发生，归 KY。**附带发现**：打包落位本身需 KD/KY 裁定（见下），即「文件交换」在隔离规格下不是纯运输动作。 | §7三方分工 | 待P3汇整 |
| 目标1 IV sourcing | **撞到（两层）** | 第一层＝行情线独占（摩擦-01）。第二层＝采集窗口（摩擦-04）。解除后 paper 实时档下 IV **四路全通**：tick24、modelGreeks、bid/ask/lastGreeks。**墙不在权限、不在 tick type，在到达时刻**。 | 55-6b第一件 | **是**（摩擦-04） |
| 目标2 美式判断点 | **撞到（正向：经过）** | engine v1.3 于 ES FOP 实测参数下**经过**提前行权判断点：`n_exercise_nodes=54514`、`max_exercise_excess=0.0017030135125537527`，欧式模式对照组 `0`。A6=(iv) 兑现。 | 55-6b第二件／85-4 A6=(iv) | 否 |
| 目标3 X-1素材 | **未撞到（已完成）** | fixture `X1_SYNTH_ES_001` 跑通，逐位输出（repr＋IEEE754 hex）＋环境指纹落 `verify/x1_env_report.json`。libm 指纹摘要 `587fbd8f…f16319`。 | 85-6 A11／DOC-25 | 否 |
| 目标4 X-2字段 | **撞到（四轮，末轮达成）** | **API 侧**：`accountSummary` 21 tag、`accountValues` 149 记录/124 唯一 tag/3 币种（含 `$LEDGER-*` 24 项分币种子账）、`positions` 5 条（字段 account/contract/position/avgCost）、`portfolio` 5 条（字段 contract/position/marketPrice/marketValue/averageCost/unrealizedPNL/realizedPNL/account）。**FlexQuery 侧**：凭据闸建成并双端验证（摩擦-06→v1.3 §4B 补件）；经 queryId 形态混淆、解析对象模型误判、服务持续 1001（摩擦-08）后，于次日、KY 补齐查询选段并改期间为 Last Business Day 后**单发取得**：原件 142,375 bytes，**20 topic**，字段结构全量落盘。 | 85-6 A12／KN-7 | 否（已达成） |
| 待答项 期货口径 | **撞到（两面）** | (a) q=r 等价面：由 q/r 闸拦下并呈 KY，**未预解**，现值为临时赋值待 KD 复核（见下行）。(b) day count 面：engine 自报 `unstated_dimensions_hit=['day_count_convention']`、`computability_status=computed_with_open_dimensions`（摩擦-03）。 | 85-1a派生／85-8边界句 | **是** |
| KD赋值 q/r（值＋依据） | **撞到（闸如设计拦停）** | 闸触发 `SystemExit(2)`，无 fallback，逐字打印索取原文。KY 赋值：`dividend_yield=0.0`、`risk_free_rate=0.04`。依据（KY 原文）：「q=0：期货标的本身不派发股息，无分红收益率。r=0.04：20260812 一年期美债收益率。**待KD复核**——本值未解决§1登记之待答项（Black-76 q=r 等价 vs q=0 两种读法之取舍），仅为链路贯通所需之临时赋值。」`_pending_kd_review=true`。 | 追加-2／85-1a | **是** |
| 隔离断言A1–A11 | **未撞到（一次自伤，见摩擦-02）** | 全程 13 次运行，末态 A1–A11 逐项 PASS。中途**两次** A2 FAIL 均系执行侧自身命名碰撞（键名一次、打包件文件名写入记录件一次），非隔离失守，均已自解——同一坑撞两次，见摩擦-02。A11 于 v1.3 补件后新增并一次 PASS（凭据值字面量全域零命中、闸序位正确、SystemExit 分支在场）。 | 条款-断言对应表 | 否 |

注：M1–M4 之材料即 29-B①–④ 激活/废止反推之逐项依据。每项末栏按 85-8：撞到之缺口**不自立撞墙条目**，走「呈KD事项登记」通道，材料挂 W-25 明细。

---

## 二、摩擦条目

### 摩擦-01｜行情线独占阻断（F1，已解除）

| 栏 | 内容 |
|---|---|
| **撞到/未撞到** | 撞到 |
| **形态描述** | 连接与合约解析全通（A8 PASS；ES 前月 `ESU6` conId=649180671 expiry=20260918 multiplier=50）。行情订阅返回 `Error 10197 "No market data during competing live session"`，`marketDataType=1` 但 bid/ask/last/**close** 四项全 None。参考价缺位 → ATM 不可判 → 链路阻断。 |
| **诊断过程** | 三次复现。事件流诊断（`verify/event_stream.json`）显示 `2104 usfuture`／`2104 hfarm`／`2106 HMDS`／`2158 sec-def` 农场全在线，且**无** 354/10089/10091 订阅缺失段——阻断不在权限、不在连线、不在 API 形态。KY 陈述今日未登录 live 侧，一度使「竞争会话」读法证据不足；执行侧据此提出「实时权益仲裁」假说。**该假说错误**。 |
| **实际成因** | KY 移动端（IBKR Mobile）会话持有行情线。行情线同时只服务一路，移动端与 Gateway 可并存但互斥取流。KY 关闭移动端后，同一代码一次跑通（ES last=7767.5）。**10197 的字面文案是准确的，执行侧的二次诊断方向是错的。** |
| **材料价值** | IV sourcing 墙的第一层**先于 tick type**：行情线独占性。属账户/会话结构面，非 API 面、非权限面。此层级在 v1.1 paper 条款所预见之外——预见的是**数据内容差异**（延迟档、tick 可得性），实测撞到的是**取流互斥**，性质不同，不静默等同。 |
| **反推指向条款** | 55-6b第一件；85-3 乙案只读能力探查之能力面边界；v1.1 paper 条款 |
| **是否需KD裁定** | 否（已解除）。材料挂 W-25 明细。 |

**附：KY 观察之澄清**——「连上几秒后断开」系 harness 正常生命周期（connect → 探查 → `finally: ib.disconnect()`），单次约 20 秒后主动登出，**非掉线**，不构成摩擦条目。

### 摩擦-02｜隔离扫描面与自然命名冲突（F1，执行侧自解）

| 栏 | 内容 |
|---|---|
| **形态描述** | X-1 报告中一个与外部数据无关的普通键名（环境指纹用，含标记串子串）在 verify/ 子树内构成 A2 命中，触发 **A2 FAIL**。即 D-2/D-3 的机械边界会与普通标识符发生**假阳性碰撞**——标记串是常见英文词加下划线，射程无法与语义意图对齐。 |
| **处置** | §4A 第4条射程（harness 自身工程 bug），执行侧自解：键名改写，重生成报告，A2 复归 PASS。engine 未动，数值面未动。另于断言脚本加输出遮蔽（`redact`），防止断言日志自身把命中串写回 verify/ 造成二次自命中。 |
| **反推指向条款** | 85-3 D-2/D-3 机械承载形态；85-7 扫描射程设计 |
| **是否需KD裁定** | 否。**材料价值**：三重机械检测在真实工程流中产生假阳性，成本由执行侧承担；裁决1 例外条款明文禁止外溢至标准切片，若日后议及外溢，假阳性率与维护成本须先行评估。挂 W-25 明细。 |

### 摩擦-03｜engine 于开放维下给出结果（day_count_convention）

| 栏 | 内容 |
|---|---|
| **形态描述** | X-1（合成输入）与步4（ES 实测输入）**两次**均返回 `computability_status="computed_with_open_dimensions"`、`unstated_dimensions_hit=["day_count_convention"]`。engine v1.3 内 `DAY_COUNT_DENOMINATOR=365`、`_dte_days` 按公历整数日差计、不引入日历库；ES 期货期权之实际日历口径（交易日/日历日、结算时点、日内剩余时间）未与之对齐，engine 自身已标记该维为开放。 |
| **性质** | engine **主动声明**的契约面开放维，**非**输入形态不匹配、非路由不通——链路未断、结果照出，但结果携带「已言明面之外」标记。执行侧按 §4A 第3条不作任何适配性修补，原样登记。 |
| **反推指向条款** | 85-8 边界句（回流位＝引擎撞墙清单既有条目域）；85-1a 不预解 |
| **是否需KD裁定** | **是**（口径归属：day count 是否与 q=r 期货口径同批处理） |

### 摩擦-04｜采集窗口假阴性 ＋ 第三方库哨兵泄漏（F1，材料价值最高）

| 栏 | 内容 |
|---|---|
| **形态描述** | 行情通后，执行侧连续两次误报「不可得」：(i) 轮询以 `or` 串联退出条件，首个报价到达即 break，greeks 未及到达 → 误判 modelGreeks 不可得；(ii) 改为等 greeks 后，modelGreeks 一到即 break，tick24 与 bid/ask/lastGreeks 未及到达 → 误判 tick24 不可得、三组 greeks 残缺。**两次结论均为假阴性**，由 KY 质疑后以对照实测推翻。 |
| **对照实测（`probe/tick_route_diag…json`）** | 期权+`""`：tick24=None，modelGreeks 可得；期权+`"106"`：tick24 可得，modelGreeks **impliedVol 逐位相同**；期货+`"106"`：tick24 可得（标的 ATM IV），modelGreeks=None。→ **106 对期权 greeks 非必需；tick24 需 106 且期权侧与标的侧是两个不同的量。** |
| **第三方库缺陷** | `ib_insync 0.9.86` `wrapper.py:944-945`：<br>`vega if vega != -2 else vega`／`theta if theta != -2 else theta`<br>两分支同值，恒等式。IB 以 **-1/-2 为「未计算」哨兵**，delta/gamma 被正确置 `None`，**vega/theta 的哨兵原样透出为浮点真值**。早读时 `vega=-2.0, theta=-2.0` 从类型与量纲上均不可辨伪。 |
| **叠加后果** | 「早退轮询」＋「哨兵泄漏」构成一条**静默产出假数**的路径：调用方拿到形如正常浮点的 -2.0，无任何异常信号。本发中该路径被触发过，仅因交叉核对才发现。 |
| **处置** | §4A 第4条射程，执行侧自解：可得性探查一律改为**跑满窗口不早退**（`require="all"`），并在源码注明「见一个就走会把晚到误判为不可得」。库缺陷不修改第三方源码，登记为材料。 |
| **反推指向条款** | 55-6b第一件（IV sourcing 墙之真实形状） |
| **是否需KD裁定** | **是**。IV sourcing 的真实门槛＝**采集窗口纪律 ＋ 第三方库可信度**，而非权限或 tick type。此结论直接影响乙案下「IBKR 作 IV 源」之可行性评估形态。 |

### 摩擦-05｜engine 值与 IB 模型值残差（待答项定量材料）

| 栏 | 内容 |
|---|---|
| **形态描述** | 同一 (S, K, σ, T) 下：engine CRR `per_unit.value = 20.440666070483793`，IB `modelGreeks.optPrice = 23.1965739539869`，**残差 = -2.755907883503106**（约 -11.9%）。输入取自 IB 同一次模型计算之自洽三元组（`undPrice=7767.75`、`impliedVol=0.12129167525537059`），故残差不含取数口径混源。 |
| **残差构成（本发不拆分）** | q/r 假设差 ＋ day count 差 ＋ 模型差（CRR 500 步 vs IB 内部模型）三项。 |
| **粗略推算（供 KD 参考，未经证实）** | ATM 附近期权时间价值近似正比于 √T。`23.1965739539869 / 20.440666070483793 = 1.1348`，平方 `≈ 1.288` → IB 之有效 T 约为 engine 之 **1.29 倍**（engine 取 dte=1 日）。方向与量级均与「engine 按整日差计、IB 计入日内剩余时间至结算时点」相符。**此为推算不是结论**：本合约非严格 ATM（K=7770 > S=7767.75，put 轻度实值 2.25 点），√T 标度不精确；且未排除 q/r 与模型差之贡献。 |
| **反推指向条款** | 85-1a派生；85-8边界句；与摩擦-03 同源 |
| **是否需KD裁定** | **是**（与摩擦-03、q/r 赋值同批） |

### 摩擦-06｜FlexQuery 缺凭据未执行（目标4 部分未达）

| 栏 | 内容 |
|---|---|
| **形态描述** | §5 步6 要求「账户报表/FlexQuery 字段结构读取」。API 侧报表面已读通（见四栏表目标4 行）。**FlexQuery 需 `token` 与 `queryId` 两项凭据**，规格件未给定、KY 未提供。按 §4A 第2条不猜、不用占位值，**停在此处未执行**，登记索取。 |
| **附带限制** | paper 账户当前 0 持仓，`positions()`／`portfolio()` 均返回空列表，故持仓侧字段结构**无法由返回对象反射得出**。若目标4 需持仓字段结构，须 KY 于 paper 账户建仓——**但建仓属下单侧，A7 只读纪律禁止执行侧触碰**，只能由 KY 手工操作或改由 FlexQuery 覆盖。 |
| **反推指向条款** | 85-6 A12／KN-7 |
| **是否需KD裁定** | 已裁：KD 20260812 补件（v1.3 §4B＋A11＋AGENTS.md 第6条）。 |

**闭环留痕（补件不抹除摩擦，§4B 明文）**：撞到 → 按 AGENTS.md 第2条即停索取 → 呈KD → v1.3 补件（凭据性质定性／KY 侧创建步骤／环境变量通道／机械闸／probe 落位／脱敏处置）→ 续跑达成。**闸机制按设计生效**，此撞墙本身＝目标4 有效摩擦材料（F1 形态）。

**补件后之实测验证（双端）**：(i) 不注入环境变量运行 `probe/probe_flex.py` → 打印索取清单、`SystemExit(2)`，无 fallback；(ii) 注入后放行且**不回显任何凭据值**（只打印长度）。A11 全域扫描 entity/∪probe/∪verify/ 确认凭据值字面量命中数==0。

### 摩擦-07｜账户面异步到达之假阴性（F1，执行侧自解）

| 栏 | 内容 |
|---|---|
| **形态描述** | 步6 重跑时 `accountSummary`／`accountValues` 返回 **0 记录**，`positions` 返回 0，而同一账户前一轮为 21／149。成因＝账户面数据于 connect 后**异步到达**、持仓面须显式 `reqPositions()` 订阅，执行侧未等即读。**与摩擦-04 同型**：早读＝假阴性。 |
| **附带损失** | 该空结果**覆盖**了前一轮的完整载荷（写入即覆盖，无版本保护），须重跑补回。**材料价值**：probe 载荷之「写入即覆盖」形态在多轮探查下会静默丢失已采材料，D-2 manifest 只记末态哈希、不留历史。 |
| **处置** | §4A 第4条射程，执行侧自解：加订阅与等待窗口，重跑补回（末态 149/21/5/5）。 |
| **反推指向条款** | 85-3 D-2（载荷版本性未定义）；85-6 A12 |
| **是否需KD裁定** | 否。载荷覆盖问题挂 W-25 明细。 |

### 摩擦-08｜FlexQuery 凭据形态混淆与服务冷却（F1）

| 栏 | 内容 |
|---|---|
| **形态描述** | 三段：(i) KY 首次提供之 `flex_query_id` 为查询**名称**而非数字 ID，Flex 服务返回 `1020: Invalid request or unable to validate request`——错误文案不指明是 token 无效还是 queryId 无效，形态诊断须由执行侧从 ID 长度/字符集反推；(ii) 执行侧解析代码误设 `ib_insync` 返回件为 namedtuple，实为 `DynamicObject` 子类（`flexreport.py:53-54`，属性存实例 `__dict__`），`TypeError: not iterable`；(iii) 同一 query 短时间重复请求返回 `1001: Statement could not be generated at this time`——**Flex Web Service 有冷却期**，与 TWS socket 面的无状态请求语义不同。 |
| **处置** | (i) 向 KY 索取数字 ID（凭据值不入本件）；(ii)(iii) §4A 第4条射程，执行侧自解：改用 `vars(r)` 取属性；加冷却重试（6 次×120s），**重试属传输层处置，不改请求内容、不改任何数值语义**。 |
| **1001 持续化（追加实测）** | 首次请求**下载成功**（8 topic 到手），解析崩溃后重试转入**持续 1001**，跨 6 次×120s 重试及后续单次尝试共约 15 分钟未解除。两个成因不可分：(a) IB Flex 对同一 query 有频率限制，**执行侧之重试循环（20 分钟内 9 次请求）可能在维持封锁**——此为执行侧过失，退避策略过激；(b) 期间 KY 开仓后平仓，若 query 期间为当日，新活动会触发报表重新生成，期间返回 1001。 |
| **材料损失与已改** | 首次成功下载之原始 XML **未落盘即因解析崩溃而丢失**，服务随即转入 1001 无法复取。已改为**先存后解**（下载成功即落原件入 probe/，再行解析）——取数与解析必须解耦，此为本发第二次因「取到了但没存住/没等到」而损失材料（前一次＝摩擦-07 载荷覆盖）。 |
| **材料价值** | X-2 走的是 **HTTPS Web Service** 而非 TWS socket，其失败面（凭据形态、错误码语义、冷却期、返回件对象模型）与行情面**完全不同源**。乙案下若以 FlexQuery 作报表通道，这条通道的可靠性纪律须单独立，不能沿用 socket 面经验。 |
| **反推指向条款** | 85-6 A12／KN-7；§4B 供给通道条款 |
| **是否需KD裁定** | 待P3汇整 |

### 摩擦-09｜凭据经聊天通道传递（纪律面，执行侧登记）

| 栏 | 内容 |
|---|---|
| **形态描述** | §4B／AGENTS.md 第6条要求凭据唯一通道＝运行时环境变量，禁止入任何文件与交付件。实际执行中 KY 将 `flex_token` 与 `flex_query_id` **明文贴入会话**，凭据因此进入会话记录——该记录不属 workdir，故不触发 A11，但**规避了条款所要保护的对象**。执行侧未将其写入任何文件（A11 全域零命中可证），仅以 `VAR=… command` 形态作单次运行期注入（§4B 步骤4 所述形态）。 |
| **执行侧建议（已向 KY 提出）** | 本发结束后于 Client Portal **重新生成 token**，作废已经过聊天通道的旧值。 |
| **材料价值** | 凭据纪律的机械闸只能覆盖**文件面**；人对人的传递通道（聊天、口述、截图）在射程之外。若乙案要把凭据纪律当作可依赖的防线，须补人侧通道条款，否则机械闸给出的是虚假的完备感。 |
| **反推指向条款** | §4B 供给通道条款；AGENTS.md 第6条 |
| **是否需KD裁定** | **是**（人侧通道是否补条款） |

---

### 摩擦-08 之解除与选段效应（追加实测，目标4 达成面）

退避约一日后单发一次，`1001` 自行解除，一次成功。**关键变量＝KY 补齐查询选段**：

| | 补段前 | 补段后 |
|---|---|---|
| topic 数 | 8 | **20** |
| 字段最富段 | 无（AccountInformation 37） | `CashReportCurrency` **240**、`EquitySummaryByReportDateInBase` 98、`Trade`／`Order`／`SymbolSummary`／`Lot`／`AssetSummary` 各 **86** |
| 成交/持仓面 | 缺位 | `Trade` 12 记录、`Order` 12、`Lot` 7、`StatementOfFundsLine` 28、`UnbundledCommissionDetail` 12 |

**材料价值（目标4 本体）**：FlexQuery 的字段可得性**由查询定义（KY 侧配置）决定，而非由 API 能力决定**。同一 token、同一 queryId、同一代码路径，仅因选段配置不同，字段结构从 8 段变 20 段、单段字段数从 37 升至 240。这意味着：乙案下若以 FlexQuery 作报表通道，**「能取到什么字段」是一项账户侧配置资产，须与代码同等纳入版本管理与交接**，否则同一套代码在不同账户配置下产出不可比的材料。此点为 KN-7 之直接材料。

**期间设置之口径联动**：本轮期间＝Last Business Day。KY 于前一日开仓后平仓，故该日成交完整进入 `Trade`／`Order` 段；若期间设为当日，报表随活动反复重新生成，正是持续 `1001` 的可能成因之一（与执行侧重试过激不可分，见上）。

---

## 三、X-1 逐位输出（DOC-25 前置素材）

engine SHA256＝`d88a955e…682cf`；fixture＝`X1_SYNTH_ES_001`（KY 20260812 钉定，**不得变更**）：
`spot=strike=7775.0`、`implied_vol=0.122`、`2026-08-12 → 2026-08-14`（dte=2）、`r=0.04`、`q=0.0`、put/short、multiplier=50。

| 项 | repr | IEEE754 hex |
|---|---|---|
| per_unit.value | 27.247943493957006 | `0x1.b3f79398dcd23p+4` |
| per_unit.delta | -0.49081376310230534 | `-0x1.f697e213cdeb5p-2` |
| per_unit.gamma | 0.00573201514840477 | `0x1.77a7419a425c3p-8` |
| per_unit.vega | 229.2405982811605 | `0x1.ca7b2fb2aa1dcp+7` |
| per_unit.theta | -2424.9461527073745 | `-0x1.2f1e46e20ae64p+11` |
| per_unit.rho | -18.04847182317104 | `-0x1.20c68a63f4c10p+4` |
| early_exercise_premium.per_unit | 0.09716506064986419 | `0x1.8dfcf35ce1600p-4` |
| lattice.n_exercise_nodes | 54722 | — |
| lattice.european_mode_n_exercise_nodes | 0 | — |

环境指纹：CPython 3.10.11 / Windows-10-10.0.26200-SP0 / libm 指纹摘要 `587fbd8f98c8ccdde681f0e0a869c80fc9efd206f5ed3d5c4be423d074f16319`。

---

## 四、步4 实测（目标2 本体）

**合约**：`E2DQ6 P7770`，conId=901320542，expiry=20260813，multiplier=50，tradingClass=E2D。
**lot**：`american_option`/`american`、put/short、quantity=1、spot=7767.75、strike=7770.0、implied_vol=0.12129167525537059、valuation_date=2026-08-12、expiry=2026-08-13、r=0.04、q=0.0。
**口径选取（KY 20260812 决定）**：spot 与 implied_vol 同取 modelGreeks 自洽三元组；不取 tick24（不配对 undPrice）、不取期货 last（合约选取用价）。

| 项 | 值 |
|---|---|
| route_id | `american_crr_binomial` |
| computability_status | `computed_with_open_dimensions` |
| unstated_dimensions_hit | `["day_count_convention"]` |
| per_unit.value | 20.440666070483793 |
| per_unit.delta / gamma | -0.5116431147277636 / 0.008133758876300128 |
| per_unit.vega / theta / rho | 162.13525184197763 / -3450.2622901284494 / -9.470648053593322 |
| early_exercise_premium.per_unit | 0.048061131722054284 |
| **n_exercise_nodes** | **54514** |
| european_mode_n_exercise_nodes | 0 |
| max_exercise_excess | 0.0017030135125537527 |
| crr_steps | 500 |

**目标2 结论（限于观测事实，不作总体判定）**：engine v1.3 于 ES FOP 实测参数下**经过**提前行权判断点。

**方法学留痕**：KY 初次给出的 q/r 依据为「因这组读法下判断点被大量经过，与目标2 相符」。执行侧指出该依据系以待观测结果反选输入，将使目标2 之观测丧失反推价值；KY 采纳，依据改为惯例论证（期货无股息 → q=0；r 取 1 年期美债）。「判断点被经过」现登记于**结果**面，非理由面。

---

## 五、呈KD事项登记（85-8 通道，不自立撞墙条目）

| # | 事项 | 材料位置 |
|---|---|---|
| 1 | q/r 赋值之实体裁定（Black-76 q=r 等价 vs q=0）——现值为临时赋值，`_pending_kd_review=true` | 摩擦-05／四栏表 q/r 行 |
| 2 | day_count_convention 开放维之口径归属，是否与事项1 同批处理 | 摩擦-03 |
| 3 | engine 与 IB 模型残差 -2.756（-11.9%）之归因 | 摩擦-05 |
| 4 | IV sourcing 真实门槛＝采集窗口纪律＋第三方库可信度，对乙案「IBKR 作 IV 源」可行性评估形态之影响 | 摩擦-04 |
| 5 | 乙案三重机械检测之假阳性成本（若议及外溢至标准切片） | 摩擦-02 |
| 6 | 凭据纪律之**人侧通道**（聊天/口述/截图）是否补条款——机械闸只覆盖文件面，人侧在射程外 | 摩擦-09 |
| 7 | FlexQuery（HTTPS Web Service）通道之可靠性纪律是否单独立——失败面与 TWS socket 面不同源 | 摩擦-08 |
| 8 | probe 载荷「写入即覆盖」无版本保护，多轮探查下会静默丢失已采材料；D-2 manifest 只记末态哈希 | 摩擦-07 |

**已闭环**：`flex_token`／`flex_query_id`（摩擦-06 → KD 20260812 v1.3 §4B 补件 → 续跑达成）。

**执行侧向 KY 之待办**：本发结束后重新生成 flex token，作废经聊天通道传递之旧值（摩擦-09）。

---

## 六、交付件清单（§5 步8，交 P3 session）

| 件 | 路径 | 性质 |
|---|---|---|
| **打包件** | **`probe/p2_delivery…20260813.zip（文件名带标记串）`** | **23 成员＋INVENTORY.json（逐成员 SHA256）** |
| 摩擦记录件 | `verify/friction_record.md` | 本件 |
| 断言日志 | `verify/assert_log.json` | 12 次运行逐项 PASS/FAIL |
| 引擎指纹日志 | `verify/engine_fingerprint_log.json` | 9 次实测，零写入可证 |
| X-1 素材 | `verify/x1_env_report.json` | DOC-25 前置素材 |
| 连接日志 | `verify/connection_log.json` | A8 证据 |
| 事件流 | `verify/event_stream.json` | 摩擦-01 证据 |
| 数据指纹黑名单 | `probe/data_manifest.json` | D-2，6 条载荷 |
| 外部载荷 | `probe/*` 带标记串之 json（6 件） | D-3 键名标记在场 |
| 断言脚本 | `verify/probe_assert.py` | A1–A10 |
| harness ／ 驱动 | `entity/probe_harness.py`／`probe/probe_run.py` | 纯代码 |
| X-1 生成脚本 | `verify/x1_synth.py` | 含 KY 授权之合成常数 |
| Flex 探查脚本 | `probe/probe_flex.py` | §4B 落位（HTTPS 通道故落 probe/） |
| 打包脚本 | `verify/pack_delivery.py` | 步8 |

**打包落位之裁定与盲区留痕（KY 20260813 处置 (a)）**：

打包件含 probe 真实数值，§2 明文「真实数值只可存在于 probe/ 子树」，故包落 `probe/` 内并带标记串，自身入 data_manifest（D-2）。

**此处存在隔离规格的机械盲区**：A2 之渗透检测射程为 entity/∪verify/，若包被放置于该二子树之外的**任何**位置（含工作目录根、桌面、外发邮件附件），**A1–A11 全部不会报警**。即：三重机械检测守的是「真实数值不得进入 entity/verify 面」，**不守「真实数值不得离开 probe/ 面」**——出口方向无检测。本次落位由 KY 显式裁定，非执行侧自选。此为 85-3 乙案边界机械承载之一处待补面，挂 W-25 明细。

**包内 manifest 之自指说明**：包成员 `probe/data_manifest.json` 为打包**时刻**之快照，不含包自身条目；包之 SHA256 于打包后追加入工作目录内的 manifest。复核时以工作目录内 manifest 为准。

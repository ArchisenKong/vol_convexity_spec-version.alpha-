# input_schema · T3-17 v2.0（slot#1占用者#1候选实现之验证载体）

## §1 实体-上游边界析出（C1）

**要件（机制，本切片计算对象）**：
1. moneyness band位置判定（below/within/above，相对该翼声明的target_activation_band）
2. 逐Greek（vega/gamma）情景压力响应比计算（stressed_X / 该翼声明的target_X_response_level）
3. 双Greek响应比合成（TPL1-T317-01桩，min取小）
4. 合成量与`wing_responsiveness_floor`槽位比较（below_floor）
5. 连续超`wing_dullness_window`槽位窗口的触发判定（wing_dullness_triggered），含非粘滞重置

**上游输入（本切片不计算、作已声明值接收）**：
- T3-22状态时序本身（moneyness、raw_vega、raw_gamma，§6未审引用T3§13.4形态依据）
- 该翼建仓/roll后声明的基准（target_activation_band_low/high、target_vega_response_level、target_gamma_response_level）
- 情景重估桩系数（scenario_shock，见§3，桩本身为类二缺实现型，其数值系数为本根工程裁定）
- 槽位数值（floor/window，类三，见§2）

## §2 槽位声明（类三，裁决24-A5：不登记模板一/二，归治理册占用者挂接）

`wing_responsiveness_floor = 7/10`、`wing_dullness_window = 3`：阶段A候选之一，待Phase B证伪，两翼共享同一组槽位值（构造简化，非方法论要求，不外推为跨翼槽位必须共享之结构性主张）。

## §3 情景重估桩（TPL1-T76-01，引用不重登；C4桩纪律）

`stressed_vega = raw_vega × vega_mult`、`stressed_gamma = raw_gamma × gamma_mult`，`vega_mult=21/20`、`gamma_mult=6/5`——确定性最简线性乘子桩，本根新声明系数（不沿用T3-17 v1.0旧值53/50、109/100，本次为独立构造），显式声明**不claim语义等价**（桩产出与真实定价引擎重估结果在当前样本数值重合不构成桩正确性宣称）。供给方指针＝TPL1-T76-01（缺实现型，见撞墙清单_T-76 v2.3，范围注记：仪表计算器非定价真理源，裁决24-E3）。两翼共享同一组情景冲击系数（构造简化：单一情景冲击场景对两翼一致施加，非方法论要求两翼必须共享系数）。

## §4 双Greek响应比合成桩（TPL1-T317-01，引用不重登；C4桩纪律）

`combined_response_ratio = min(vega_response_ratio, gamma_response_ratio)`——worst-of最简保守合成，桩，不claim权威、不外推为跨根标准。**度量形状层判据源**＝自由度治理册v1.3 slot#1档案·占用者#1登记行（候选·降格留档态，KD一字定夺20260724）；随档规格语义：读法#2（单数"响应比"＝逐Greek分算经合成衔接）、读法#5（"超过"＝严格大于、非粘滞）。翻译审计表v1.2行T3·607-B已判翻译漂移，**不作判据源**，仅留痕引用。TPL1-T317-01闭合条件＝占用者#1废弃，或合成规则经换装通道获KD裁定的权威定义；本切片对此不做裁决（本会话不做，见任务包§8）。

## §5 B段路线选择与容差子口径

- **B段计算路线**：全程离散有理数算术（`fractions.Fraction`），无sqrt/exp/log等超越函数 → 容差子口径(a) bit-exact（裁决13/19，骨架C3分派判据＝超越函数在场性）。
- **路径独立（D段②硬要求）**：`entity/harness.py`＝命令式for循环风格，局部变量原地累加/重置；`verify/independent_recompute.py`＝函数式/生成器风格，四处表达式级分叉（情景重估展开式、band嵌套三元表达式、min()内建函数、itertools.accumulate自定义reducer批量扫描），不复用harness任何代码或计算思路，不import harness模块、不读取harness_output.json。

## §6 T3-22代理时序结构说明（含未审引用标注）

两翼各9期（t1-t9）人造时序：moneyness、raw_vega、raw_gamma。字段形态依据T3§13.4"long put/long call integrity"状态语义（**未审引用**，审计表v1.2覆盖声明1b：不入冻结面，G-3同构口径），仅取输入形态参考，全部数值为本根手工构造，非源自任何真实行情或历史样本（裁决1）。

## §7 判据源双层结构标注（裁决28-D措辞读法；裁决28-H字段命名）

本schema及全部产出中"判据源文位置"字段指T3§5.5行607（审计表T3·607-A，思想锚定→宪-ID-01＋宪-EP-07），仅为源文出处定位，不构成档位或效力断言；度量形状层引用格式统一为"治理册slot#1占用者#1登记行"指针，不使用"权威定义源"类命名。判据效力链＝审计表锚定→宪法（裁决28-D）。

## §8 数据来源声明（C6档二字段规范化，裁决23(f)采纳）

`entity/input_data.json` 顶层字段 `_data_source: "synthetic_hand_constructed"`。

## §9 与首批骨架（v1.0）的对照观察（呈报，非骨架修订；G-6通道留痕）

- 要件2/3/4/5（响应比计算＋合成＋槽位比较）之整体，其中"连续超槽位窗口触发、且遇任一期回升即非粘滞重置"这一状态机形态，在首批骨架A1-A9九型中未见对应类别（A1分桶为无状态离散映射，不含跨期持续计数与重置语义）。本根不就地修订骨架（本会话不做），如实呈报此为骨架第二批归纳阶段应考察的候选新机制类型（暂命名参考："持续性窗口触发状态机"，命名权留归纳会话）。
- 要件1（moneyness band位置判定）归属A1（分桶/离散化映射），与首批骨架T-76/T3-03/GK-14三根同构，不新增观察。
- 要件2部分（情景重估桩本体）归属A3（重估型派生，情景维），与T3-03/GK-14同族（首批骨架A3限定注记：情景维两根实现现为桩，本根第三例，同构、非新证据）。

# entity/input_schema.md · GK-14 Vega六形态（GK版）· v1.2 · 20260714

> **v1.2修订（W-7扫描H7裁定落地）**：§3引文指针修正——引语"未因与T-74重名同判，独立走查"实位任务5 Step2产出（v1.2）§2.1行114（GK-14自身判定行），v1.1误标行83（行83为T-74判定行，承载Q4继承源文，其自身引用不受影响）。R4同型（依据真实存在、指针错；R4修正窗口仅及§2.5未扫§3）。引语与算法declaration零变动，A/B产物零变动。
> **v1.1修订（裁决18/R4同源同修）**：§2.5定性依据指针修正——实为任务5 Step1产出（v1.3）行264，v1.0误标任务3。仅指针修正，算法declaration与全部数值内容零变动。

## §1 坐标继承与字段声明

node级raw Vega账本坐标键继承T-76节点坐标系（六维：leg_type × side × option_type × tenor_bucket × moneyness_bucket × scenario；裁决14：T-76实体算法要件＝bucket派生＋坐标归属＋node级聚合，node级raw Greeks为上游输入之聚合事实）。GK-14不重算per-lot→node聚合（该聚合为T-76本职，本根直接消费node级raw Vega账本作为人造input）。

字段：
- `node_id`：节点唯一标识（本根工程裁定，字符串，不外推为跨根命名规范）
- `leg_type`：{premium_income, wing_protection}（策略腿语义标注，不参与坐标身份键计算，随记录携带）
- `side`：{long, short}
- `option_type`：{put, call}
- `tenor_bucket`：{30D, 90D, 180D}，声明排序 30D < 90D < 180D（本根工程裁定，用于tenor Vega/surface矩阵行序）
- `moneyness_bucket`：{put_wing, atm, call_wing}，声明排序 put_wing < atm < call_wing（本根工程裁定，用于surface矩阵列序）
- `scenario`：{base}（本根raw ledger全部标注base，情景冲击态由scenario-stressed Vega表达式派生，非账本自带第二态）
- `raw_vega`：有理数（本根取整数，满足裁决13子口径(a)全程bit-exact）

## §2 六形态算法声明（Q4判据："喂node级raw Vega账本+形态规则/情景，出对应形态Vega值，判据＝与raw复算一致"；GK-14增量：输出＝多分量度量+轴标注）

### 2.1 raw Vega（Phase 2 raw observation）
逐node直接陈述，不聚合。分量＝账本node数，每分量lineage指针＝`node_ledger:{node_id}`。

### 2.2 tenor Vega（Phase 2 bucket observation / Phase 3 diagnostic）
`tenor_vega[τ] = Σ_{n: tenor_bucket(n)=τ} w_τ · raw_vega(n)`

**权重w_τ＝类三阶段B校准项**（三分判别自查：类一测试——GK§6.1.3"修正Vega权重可以改善跨期限风险管理，但权重本身是模型化或经验性假设，需重估和审计"，源文明确权重取值非结构问题，是待校准assumption；但同条"跨期限Vega未调整前不可比较、相加或相减"裁定了结构性下限——禁止w_τ全隐式为跨tenor直接净额裁决，本根加权求和结构本身有源文支撑，非类一未决。类二测试——候选池检索无专门"tenor权重"待建实体/待裁定义。判定：结构＝类一已定（加权求和），数值＝类三，不登记模板一/二，声明候选值+不外推）。本根取值：**w_τ＝1（全期限等权），候选之一，待阶段B证伪，符号w_τ∈ℚ**。

### 2.3 forward-segmented Vega（Phase 3 diagnostic）
`forward_segment(n)`＝分段函数；`forward_segmented_vega[seg] = Σ_{n: forward_segment(n)=seg} w_τ · raw_vega(n)`（复用§2.2权重占位）。

**分段规则＝类二缺定义，登记TPL1-GK14-01**（GK§6.1.4仅declare"需要观察未来时间段中的long/short Vega分布"，未给出对path-dependent/延迟启动结构的具体分段算法；候选池检索无专门待建对象）。占位处理：`forward_segment(n) = tenor_bucket(n)`（复用已有tenor bucket作为最简确定性桩，**不claim语义等价**——本根人造ledger未含path-dependent/延迟启动腿，占位分段与tenor分桶在当前样本下数值退化重合，如实记录，非隐藏）。

**〔映〕边界合规**：字段名使用`forward_segment`，不使用`forward_vol_bucket`或任何Trading Concepts `forward-vol bucket`（TC-12）语汇；GK§6.2行490边界"在输入、shock、时间段定义和聚合规则完成审计前，不得默认同义或共用字段"——本根不与TC-12建立任何映射声明。

### 2.4 surface Vega（Phase 3 diagnostic / Phase 4 input only）
cell坐标＝`(tenor_bucket(n), moneyness_bucket(n))`（**复用§1已有坐标维度，非新造schema**——该维度继承自T-76节点坐标系，非本根发明）。`surface_vega[cell] = Σ_{n∈cell} raw_vega(n)`，输出组织为按tenor轴（行，排序见§1）× moneyness轴（列，排序见§1）的矩阵，仅列出有数据的cell（无数据cell不补0，避免"0"被误读为"零暴露"断言）。

**scenario_set候选声明**（GK§6.2行491"scenario set未冻结；不得写成生产schema"——情景集取值＝数据自由度，本根人造取值不外推，同裁决17对T3-03/task包§3已定案处理）：`surface_scenario_set_candidate = ["parallel_shift", "skew_tilt", "local_deformation"]`，**候选枚举，未冻结，本根不对其执行任何冲击计算**（冲击响应计算属scenario-stressed Vega表达式职责，surface Vega本形态仅产出基线cell分布+候选情景集元数据）。

### 2.5 grid Vega（Phase 3 diagnostic）
cell坐标定义同§2.4（复用同一坐标维度）。`grid_vega`输出为flat cell列表（非矩阵），用于"strike × tenor cell风险定位"（GK§6.2行492）。

**grid schema取值＝本根工程裁定，不外推为production grid**（GK§6.2边界"grid schema与correlation matrix需另审；不得写成固定grid"；任务5 Step1产出（v1.3）行264对GK-16"surface候选坐标"定性："surface实现坐标候选；surface Vega语义由T-74/GK-14承载，坐标属切片逼出物"（v1.0误标任务3，裁决18/R4修指针）——本根坐标声明即为该"切片逼出物"，非等待外部供给的缺口，不登记模板一）。

**correlation matrix明确出域**：Q4判据仅要求"对应形态Vega值"，correlation matrix非Vega值本身，本根不计算，**范围裁定非能力缺失，不登记模板一/二**。

### 2.6 scenario-stressed Vega（Phase 3 scenario diagnostic / Phase 4 governance input）
情景三段拆分（同裁决17对T3-03的拆分模式）：
- **幅度值＝数据**：scenario_id="S1"，vol_shock="+3 vol point 均匀冲击"（人造input构造自由度，不登记）
- **作用规则形态＝重估，类一已定案**（源文同裁决17引用：T2/00A§4行81定义句"情景下重估"；GK行398"固定参数Gamma不足…co-move情景下重估"；GK§2.3.1行232"risk-equivalent不得替代scenario-stressed"）
- **重估实现＝缺实现型缺口，供给方＝TPL1-T76-01，引用不重登**（同T3-03/裁决17模式）。本根固定参数线性近似降格占位桩：`stressed_vega(n) = raw_vega(n) × (1 + k)`，**k＝1/20（固定响应系数，属作用规则成分非幅度值，声明桩值）**。

输出＝逐node stressed_vega（7分量）+ 组合汇总stressed_vega_total（1分量，roll-up，lineage指向全部node）。

## §3 T-19承接：轴分离实现

GK§6.2行484："本节的分类同时标注两条不同轴线：`方法论状态/转译强度`…`运行权限Phase`…两者不得合并为一个'所属层'。"输出结构中两轴以独立字段承载：`methodology_status_translation_strength` 与 `operating_phase`，不合并入单一"layer"/"tier"字段，不互相派生。T-19（Greeks权限角色链，二阶规矩，任务3行353〔约〕正交轴声明）承接实现＝该字段分离本身；GK-14不新增角色链内容，仅在输出结构层面维持正交（同T-74处理路径〔T-74判定行＝Step2 §2.1行83〕；本根Q6自查语"未因与T-74重名同判，独立走查"＝Step2 §2.1行114，v1.2修正指针）。

## §4 撞墙登记指针

- TPL1-GK14-01（模板一，缺定义）：forward-segmented Vega真实分段规则（覆盖path-dependent/延迟启动场景），本根占位＝tenor bucket边界桩。详见撞墙清单。
- 引用不重登：TPL1-T76-01（scenario-stressed Vega重估实现供给方，裁决17模式延续）。

## §5 容差口径声明

裁决13子口径(a)：离散/精确有理计算＝0（bit-exact）。理由：node级raw_vega全部人造为整数；六形态全部转换（等权求和、线性近似乘法、坐标归类）均为`fractions.Fraction`有理数`+ - ×`运算，无sqrt/exp/log等超越函数，无浮点舍入风险。

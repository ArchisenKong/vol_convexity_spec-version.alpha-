# T-76 option surface node · input schema 与算法定义（本根实际取用）

> **v2.1修订（20260710，裁决14落地）**：§4算法降格为占位实现（桩）。依裁决14：per-lot raw Greeks＝T-76上游输入，其计算模型不属T-76实体算法要件；T-76实体算法要件＝bucket派生（§3）＋坐标归属＋node级聚合。§4的BS解析解仅为本根切片提供确定性占位输入源，缺口已登记TPL1-T76-01（品种感知自算Greeks引擎，模板一）。

## 1. 字段取用裁定（依 §1 处置纪律，本根内有效，不外推为跨根命名规范）

两处语义源文字段集存在差异（scenario 之有无；lot_id/liquidity bucket 之有无）。本根裁定：

- **坐标轴（node 身份键，6 维）**：leg_type × side × option_type × tenor_bucket × moneyness_bucket × scenario
  - 取 T3§8.2 的 cartesian product 结构，expiry/strike 侧用其 bucket 形态（tenor_bucket / moneyness_bucket）而非原始值，理由：surface node 的"面"语义要求坐标可对齐到 tenor-moneyness 网格，原始 expiry/strike 逐笔不同则退化为逐笔记录，不构成"面"上的可聚合节点。
  - scenario 本根固定取值 "base"（不做压力情景），未消耗该轴的多值维度，不构成对 scenario 语义的裁决，仅为本根范围限定。
- **保留字段（retained，非坐标轴，落在 position/node 记录中）**：lot_id、expiry（原始）、strike（原始）、liquidity_bucket（由 open_interest 派生）
  - 满足 T2/12 "至少应保留" 的字段清单要求，同时不作为节点身份键——流动性、批次、精确到期日/行权价不改变该笔持仓归属的"面"位置。
- 该取用为本根工程裁定，不构成骨架归纳阶段的跨对象命名标准；骨架归纳阶段将从多根实际取用汇总后再行归纳（依"归纳最小充分不外推"原则）。

## 2. 字段 schema

| 字段 | 类型 | 说明 |
|---|---|---|
| lot_id | string | 持仓批次唯一标识，保留字段 |
| underlying | string | 标的代码（合成，非真实行情标的） |
| leg_type | string, enum{core,hedge} | 坐标轴 |
| side | string, enum{long,short} | 坐标轴；side_sign: long=+1, short=-1 |
| option_type | string, enum{call,put} | 坐标轴 |
| expiry | date | 保留字段（原始到期日） |
| strike | float | 保留字段（原始行权价） |
| spot | float | 计算输入，不入坐标/保留字段（现货价，随估值日变化，非持仓静态属性） |
| risk_free_rate | float | 计算输入（年化，连续复利） |
| implied_vol | float | 计算输入（年化波动率） |
| multiplier | int | 合约乘数 |
| quantity | int | 手数（恒正，方向由 side 决定） |
| open_interest | int | 用于派生 liquidity_bucket 的原始事实字段 |

## 3. 派生算法（bucket 函数，本根定义，构成一阶实体"算法"要件）

```
tenor_bucket(dte):
    dte <= 30   -> "0-30D"
    dte <= 60   -> "31-60D"
    dte <= 90   -> "61-90D"
    dte <= 180  -> "91-180D"
    else        -> "180D+"
    # dte = (expiry - valuation_date).days，整数天

moneyness_bucket(k_over_s):
    k_over_s < 0.95        -> "low"
    0.95 <= k_over_s <= 1.05 -> "atm"
    k_over_s > 1.05         -> "high"
    # k_over_s = strike / spot

liquidity_bucket(oi):
    oi < 100    -> "low"
    oi < 1000   -> "mid"
    else        -> "high"
```

## 4. per-lot raw Greeks 占位算法（Black-Scholes 无股息解析解；桩，非T-76实体算法要件——裁决14）

```
T = dte / 365
d1 = (ln(S/K) + (r + 0.5*sigma^2)*T) / (sigma*sqrt(T))
d2 = d1 - sigma*sqrt(T)
N(x)  = 标准正态 CDF
n(x)  = 标准正态 PDF = (1/sqrt(2*pi))*exp(-x^2/2)

call: delta=N(d1); gamma=n(d1)/(S*sigma*sqrt(T)); vega=S*n(d1)*sqrt(T)
      theta=-(S*n(d1)*sigma)/(2*sqrt(T)) - r*K*exp(-r*T)*N(d2)
      rho=K*T*exp(-r*T)*N(d2)
put:  delta=N(d1)-1; gamma,vega 同 call
      theta=-(S*n(d1)*sigma)/(2*sqrt(T)) + r*K*exp(-r*T)*N(-d2)
      rho=-K*T*exp(-r*T)*N(-d2)

position_greek = per_unit_greek * multiplier * quantity * side_sign
node_raw_greek = sum(position_greek for 该 node 坐标下所有持仓)
```

单位口径：delta/gamma 为逐份额原始解析值；vega 按 sigma 变化 1.0（非 1%）计；theta 按年计（非按日）；rho 按 r 变化 1.0（非 1%）计。均未做行业惯用缩放，属"raw"口径，与 Q4 判据"raw Greeks"一致——不引入缩放判断。

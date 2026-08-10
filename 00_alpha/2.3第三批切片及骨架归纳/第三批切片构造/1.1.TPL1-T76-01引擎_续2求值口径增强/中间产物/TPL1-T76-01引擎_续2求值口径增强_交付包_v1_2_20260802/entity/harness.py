"""
TPL1-T76-01 引擎 · B段一次性harness（夹具，非常设pipeline）

职责边界：喂入 → 驱动 → 捕获 → 落盘。不承担数据获取，不承担生产集成，
不建任何常设服务/接口/持久化通道。运行一次即完成本切片取数职责。

数据源纪律：零网络、零行情接口、零外部文件读取（仅读同目录人造 input）。

情景重估／时点推移之实现形态：不调用任何新接口——以冲击后的市场坐标构造同形 lot，
再次调用 engine.evaluate_lot。此为构造中反推浮现之形态，非预先设计。
"""

import json
import os

import engine

HERE = os.path.dirname(os.path.abspath(__file__))

# 输出顶层键集声明（与 input_schema.md 之 OUTPUT_TOPLEVEL_DECLARATION 块同源；
# 一致性由 verify/assert_check.py 以独立解析 input_schema.md 的方式核验，
# 本处不作为断言基线）
DECLARATION_REF = "entity/input_schema.md §5 OUTPUT_TOPLEVEL_DECLARATION"


def _market_override(lot, spot=None, vol=None, valuation_date=None):
    """构造同形 lot 之市场坐标覆盖副本。只改已言明面之市场字段，不新增字段。"""
    out = dict(lot)
    if spot is not None:
        out["spot"] = spot
    if vol is not None:
        out["implied_vol"] = vol
    if valuation_date is not None:
        out["valuation_date"] = valuation_date
    return out


def main():
    with open(os.path.join(HERE, "input_data.json"), "r", encoding="utf-8") as fh:
        data = json.load(fh)

    v0 = data["valuation_date"]
    shock = data["scenario_shock"]
    tshift = data["time_shift"]

    base, scen, tsh = [], [], []
    for raw in data["lots"]:
        lot = _market_override(raw, valuation_date=v0)
        base.append(engine.evaluate_lot(lot))

        s_lot = _market_override(
            lot,
            spot=raw["spot"] * (1.0 + shock["spot_shock_pct"]),
            vol=(None if raw["implied_vol"] is None
                 else raw["implied_vol"] + shock["vol_shock_points"]),
        )
        scen.append(engine.evaluate_lot(s_lot))

        t_lot = _market_override(lot, valuation_date=tshift["valuation_date_t1"])
        tsh.append(engine.evaluate_lot(t_lot))

    output = {
        "_data_source": data["_data_source"],
        "_declaration_ref": DECLARATION_REF,
        "route_table": {ic: {"route_id": engine.ROUTE_TABLE[ic],
                             "computability_status": engine.COMPUTABILITY[ic],
                             "unstated_dimensions_hit":
                                 list(engine.UNSTATED_DIMENSIONS[ic])}
                        for ic in engine.INSTRUMENT_CLASSES},
        "base_valuation": base,
        "scenario_revaluation": scen,
        "time_shift_revaluation": tsh,
    }

    with open(os.path.join(HERE, "harness_output.json"), "w", encoding="utf-8") as fh:
        json.dump(output, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    print("harness 实跑完成：lots=%d，顶层键=%s"
          % (len(base), sorted(output.keys())))


if __name__ == "__main__":
    main()

"""
TPL1-T76-01 引擎 · 续2增强 · 回归检验与底版-增强版diff面清单产出（S-1机械前哨）

用途（任务包§3 S-1增量封闭判据之机械前哨双件）：
  (a) q=0退化回归：以 entity/input_data.json 之全部lot强制 dividend_yield=0（期权lot），
      重跑 entity/engine.evaluate_lot，产出 verify/regression_q0_output.json；
      与 verify/baseline_v1_1_reference.json（增强前v1.1原始产出，cp-then-edit时另存）
      逐容器逐笔逐分量比对——q=0时增强公式代数化简至旧公式，预期逐字节一致。
  (b) 底版-增强版diff面清单：实际增强产出（entity/harness_output.json，真实q值）
      与 baseline_v1_1_reference.json 对比，产出 verify/baseline_diff_table.tsv，
      标注每笔每分量"零变动"或"变动"，供人工核验变更面是否封闭于§2.3入范围项
      （非期权路由须逐分量零变动；期权路由数值分量允许变动，route_id/
      unstated_dimensions_hit 仅允许§2.3声明之特定字段变动）。

数据源纪律：本脚本 import entity.engine 直接调用被测函数（构造侧自查脚本，与
verify/independent_recompute.py之"不import被测模块"独立性纪律不冲突——本脚本
职责是回归验证与diff枚举，非独立复算路径，不参与D段②之路径独立判据）。
零网络、零外部数据源；仅读 entity/input_data.json 与 verify/baseline_v1_1_reference.json。
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(PKG, "entity"))

import engine  # noqa: E402  被测模块本体，本脚本职责为回归自查非独立复算

CONTAINERS = ("base_valuation", "scenario_revaluation", "time_shift_revaluation")
COMPONENTS = ("value", "delta", "gamma", "vega", "theta", "rho")

IN_PATH = os.path.join(PKG, "entity", "input_data.json")
BASELINE_PATH = os.path.join(HERE, "baseline_v1_1_reference.json")
ACTUAL_OUT_PATH = os.path.join(PKG, "entity", "harness_output.json")
Q0_OUT_PATH = os.path.join(HERE, "regression_q0_output.json")
DIFF_TABLE_PATH = os.path.join(HERE, "baseline_diff_table.tsv")


def _market_override(lot, spot=None, vol=None, valuation_date=None):
    out = dict(lot)
    if spot is not None:
        out["spot"] = spot
    if vol is not None:
        out["implied_vol"] = vol
    if valuation_date is not None:
        out["valuation_date"] = valuation_date
    return out


def _run_engine(lots, v0, shock, tshift, force_q0):
    """镜像 harness.main() 之驱动逻辑；force_q0=True 时期权lot之dividend_yield强制0.0。"""
    base, scen, tsh = [], [], []
    for raw in lots:
        raw = dict(raw)
        if force_q0 and raw["instrument_class"] in ("european_option", "american_option"):
            raw["dividend_yield"] = 0.0

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
    return {"base_valuation": base, "scenario_revaluation": scen,
            "time_shift_revaluation": tsh}


def main():
    with open(IN_PATH, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    v0, shock, tshift = data["valuation_date"], data["scenario_shock"], data["time_shift"]

    # --- (a) q=0退化回归 ---------------------------------------------------
    q0_result = _run_engine(data["lots"], v0, shock, tshift, force_q0=True)
    q0_output = {
        "_data_source": data["_data_source"],
        "_note": "regression_check q=0强制变体；仅供与baseline_v1_1_reference.json比对，非交付产物本体",
        "route_table": {ic: {"route_id": engine.ROUTE_TABLE[ic],
                             "computability_status": engine.COMPUTABILITY[ic],
                             "unstated_dimensions_hit":
                                 list(engine.UNSTATED_DIMENSIONS[ic])}
                        for ic in engine.INSTRUMENT_CLASSES},
        **q0_result,
    }
    with open(Q0_OUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(q0_output, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    with open(BASELINE_PATH, "r", encoding="utf-8") as fh:
        baseline = json.load(fh)

    q0_bad = []
    for c in CONTAINERS:
        bmap = {r["lot_id"]: r for r in baseline[c]}
        for r in q0_output[c]:
            b = bmap[r["lot_id"]]
            for layer in ("per_unit", "per_lot"):
                for k in COMPONENTS:
                    qv, bv = r[layer][k], b[layer][k]
                    if qv != bv:
                        q0_bad.append("%s/%s/%s/%s q0=%r baseline=%r"
                                      % (c, r["lot_id"], layer, k, qv, bv))

    # --- (b) 底版-增强版diff面清单 -------------------------------------------
    with open(ACTUAL_OUT_PATH, "r", encoding="utf-8") as fh:
        actual = json.load(fh)

    rows = [["container", "lot_id", "layer", "component", "baseline_v1_1",
             "enhanced_v1_2candidate", "verdict"]]
    scope_violation = []
    OPTION_CLASSES = {"european_option", "american_option"}
    LOT_CLASS = {l["lot_id"]: l["instrument_class"] for l in data["lots"]}

    for c in CONTAINERS:
        bmap = {r["lot_id"]: r for r in baseline[c]}
        for r in actual[c]:
            b = bmap[r["lot_id"]]
            ic = LOT_CLASS[r["lot_id"]]
            for layer in ("per_unit", "per_lot"):
                for k in COMPONENTS:
                    av, bv = r[layer][k], b[layer][k]
                    changed = (av != bv)
                    verdict = "变动" if changed else "零变动"
                    rows.append([c, r["lot_id"], layer, k, repr(bv), repr(av), verdict])
                    if changed and ic not in OPTION_CLASSES:
                        scope_violation.append("%s/%s(%s)/%s/%s" % (c, r["lot_id"], ic, layer, k))

    # route_table 层面diff（仅报告，非per-lot分量表一部分）
    route_diff_rows = [["instrument_class", "field", "baseline_v1_1", "enhanced_v1_2candidate"]]
    ALLOWED_ROUTE_FIELD_CHANGE = {
        ("european_option", "route_id"),
        ("european_option", "unstated_dimensions_hit"),
        ("american_option", "unstated_dimensions_hit"),
    }
    route_scope_violation = []
    for ic in engine.INSTRUMENT_CLASSES:
        b = baseline["route_table"][ic]
        a = actual["route_table"][ic]
        for f in ("route_id", "computability_status", "unstated_dimensions_hit"):
            if b[f] != a[f]:
                route_diff_rows.append([ic, f, repr(b[f]), repr(a[f])])
                if (ic, f) not in ALLOWED_ROUTE_FIELD_CHANGE:
                    route_scope_violation.append("%s.%s" % (ic, f))

    with open(DIFF_TABLE_PATH, "w", encoding="utf-8") as fh:
        fh.write("# 底版-增强版diff面清单（S-1机械前哨）\n")
        fh.write("# route_table层面变动：\n")
        for r in route_diff_rows:
            fh.write("\t".join(str(x) for x in r) + "\n")
        fh.write("#\n# per-lot数值分量层面变动（288项全量，含零变动行）：\n")
        for r in rows:
            fh.write("\t".join(str(x) for x in r) + "\n")

    ok = (not q0_bad) and (not scope_violation) and (not route_scope_violation)
    summary = {
        "q0_regression_mismatches": q0_bad,
        "scope_violations_numeric": scope_violation,
        "scope_violations_route_table": route_scope_violation,
        "route_table_changes": route_diff_rows[1:],
        "verdict": "PASS" if ok else "FAIL",
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

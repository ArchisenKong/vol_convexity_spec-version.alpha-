#!/usr/bin/env python3
"""
GL-06 · Theta收入配比判据 · entity/harness.py

一次性harness（裁决1"一次性harness真跑出数"）：喂入人造账本input（ledger_input.json），
驱动Q4判据"喂账本两侧成分，出比值与阈值比较，判据＝倍数比较"之端到端计算，捕获输出数。
不建常设pipeline，不接任何数据源（IBKR/QuantConnect/历史行情/实时行情/文件数据源一律禁止）。

判据结构（类一，语义即裁）：短端Theta收入 应达到 长端保护成本日均消耗时间价值 之阈值倍数（"大致两倍"）。
比较实现＝整数cross-multiplication，避免浮点除法，维持子口径(a)＝0 bit-exact可判性
（同T3-18 schema §4③斜率delta比较之移项消去手法）。

Q0既裁：本对象为比较判据单体，配比不达标之处置动作源文未定义——本harness只输出比较结果，
不实现、不发明任何下游处置动作（沉默处不补，见entity/input_schema.md §0）。

窗口不足期（t < W）不参与评估，显式标记evaluated=False，不做部分窗口的近似计算。
"""
import json
import os

LEDGER_PATH = os.path.join(os.path.dirname(__file__), "ledger_input.json")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "harness_output.json")


def load_ledger(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_gl06(ledger):
    W = ledger["slots"]["averaging_window_days"]["value"]
    thr_num = ledger["slots"]["ratio_threshold"]["numerator"]
    thr_den = ledger["slots"]["ratio_threshold"]["denominator"]
    periods = ledger["periods"]

    cost_by_t = {p["t"]: p["protection_cost_tv_cents"] for p in periods}
    income_by_t = {p["t"]: p["theta_income_cents"] for p in periods}
    ts_sorted = sorted(cost_by_t.keys())

    results = []
    for t in ts_sorted:
        if t < W:
            results.append({
                "t": t,
                "evaluated": False,
                "reason": "insufficient_window_history"
            })
            continue

        window_ts = [t - k for k in range(W)]  # [t, t-1, ..., t-W+1]
        window_sum_cost = sum(cost_by_t[wt] for wt in window_ts)
        income_t = income_by_t[t]

        # ratio >= threshold  <=>  income_t*W/window_sum_cost >= thr_num/thr_den
        #                     <=>  income_t*W*thr_den >= thr_num*window_sum_cost
        lhs = income_t * W * thr_den
        rhs = thr_num * window_sum_cost
        ratio_meets_threshold = lhs >= rhs

        results.append({
            "t": t,
            "evaluated": True,
            "theta_income_cents": income_t,
            "window_sum_protection_cost_tv_cents": window_sum_cost,
            "window_days": W,
            "lhs_cross_mult": lhs,
            "rhs_cross_mult": rhs,
            "ratio_meets_threshold": ratio_meets_threshold
        })
    return results


def main():
    ledger = load_ledger(LEDGER_PATH)
    results = compute_gl06(ledger)
    output = {
        "_data_source": ledger.get("_data_source"),
        "object_id": "GL-06",
        "slots_echo": ledger["slots"],
        "results": results,
        # C-6/P_B证伪触发器标记：本根Step3哲学准入判定"不标记"（倍数判据不依赖路径顺序/样本族），
        # 显式留空以满足"若有则携带"规则，非默认省略。
        "falsification_trigger_flags": []
    }
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    n_eval = sum(1 for r in results if r["evaluated"])
    print(f"[harness] wrote {OUTPUT_PATH}: {len(results)} periods, {n_eval} evaluated")


if __name__ == "__main__":
    main()

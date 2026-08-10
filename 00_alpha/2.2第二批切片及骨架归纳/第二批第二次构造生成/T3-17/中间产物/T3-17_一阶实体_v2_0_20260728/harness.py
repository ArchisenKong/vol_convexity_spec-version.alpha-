"""
T3-17 wing effectiveness -- slot#1占用者#1候选实现之验证载体
entity/harness.py -- 模板三 B段：一次性harness真跑（裁决1：不接任何数据源，不建常设pipeline）

判据源双层结构（裁决24-C4②；本包§1）：
  功能层判据源文位置 = T3《3_波动率凸性操作方法论主文档...》§5.5 行607（审计表T3·607-A，思想锚定）。
  度量形状层判据源 = 自由度治理册 slot#1档案 占用者#1登记行（审计表T3·607-B已判翻译漂移，不作判据源）。
本脚本仅计算，不做判据出处断言（断言基线程序化解析在 verify/assert_check.py 中执行，D1修复）。

本会话不做：TPL1-T76-01供给方设计、TPL1-T317-01合成规则权威定义、槽位数值校准（均为已知缺口，占位处置见 input_schema.md）。

风格声明（D段②路径独立要求）：本文件为命令式 for 循环 + 局部变量原地更新风格。
verify/independent_recompute.py 须走另一条独立路径（函数式/生成器风格），不得复用本文件任何代码或计算思路。
"""

import json
from fractions import Fraction as F


def load_input(path="input_data.json"):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def compute_wing(wing_name, wing_data, scenario_shock, slots):
    """命令式 for 循环：逐期顺序处理，consecutive_below_count 用局部变量原地累加/重置（同T3-17 v1.0风格延续，B段路线选择本根裁定见KD登记项）。"""
    band_low = F(wing_data["declared_basis"]["target_activation_band_low"])
    band_high = F(wing_data["declared_basis"]["target_activation_band_high"])
    target_vega = F(wing_data["declared_basis"]["target_vega_response_level"])
    target_gamma = F(wing_data["declared_basis"]["target_gamma_response_level"])
    vega_mult = F(scenario_shock["vega_mult"])
    gamma_mult = F(scenario_shock["gamma_mult"])
    floor = F(slots["wing_responsiveness_floor"])
    window = int(slots["wing_dullness_window"])

    out_periods = []
    consecutive_below = 0  # 命令式局部状态，原地更新（B段路线选择，独立于verify侧实现）

    for period in wing_data["periods"]:
        t = period["t"]
        moneyness = F(period["moneyness"])
        raw_vega = F(period["raw_vega"])
        raw_gamma = F(period["raw_gamma"])

        # --- 类一：moneyness band位置判定（行607"位置"语义直接给出，声明性输入接收） ---
        if moneyness < band_low:
            band_position = "below"
        elif moneyness > band_high:
            band_position = "above"
        else:
            band_position = "within"

        # --- 类二缺实现型：情景重估桩（TPL1-T76-01，C4桩纪律，确定性线性乘子，不claim语义等价） ---
        stressed_vega = raw_vega * vega_mult
        stressed_gamma = raw_gamma * gamma_mult

        # --- 类一：逐Greek响应比 = 情景压力值 / 该翼声明的目标响应水平 ---
        vega_response_ratio = stressed_vega / target_vega
        gamma_response_ratio = stressed_gamma / target_gamma

        # --- 类二缺定义型：双Greek合成（TPL1-T317-01，度量形状层判据源=治理册slot#1占用者#1登记行，
        #     占位=min（worst-of最简保守合成），不claim权威、不外推） ---
        if vega_response_ratio <= gamma_response_ratio:
            combined_response_ratio = vega_response_ratio
        else:
            combined_response_ratio = gamma_response_ratio

        # --- 类一：破坏形态 = 响应比"低于"槽位水平（严格小于） ---
        below_floor = combined_response_ratio < floor

        if below_floor:
            consecutive_below += 1
        else:
            consecutive_below = 0  # 本根工程裁定（同构v1.0裁定#5）：非粘滞，任一期回升即清零

        # --- 类一（"超过"=严格大于，本根工程裁定，读法#5一致）：连续超槽位窗口触发 ---
        wing_dullness_triggered = consecutive_below > window

        out_periods.append({
            "t": t,
            "moneyness_band_position": band_position,
            "stressed_vega": str(stressed_vega),
            "stressed_gamma": str(stressed_gamma),
            "vega_response_ratio": str(vega_response_ratio),
            "gamma_response_ratio": str(gamma_response_ratio),
            "combined_response_ratio": str(combined_response_ratio),
            "below_floor": below_floor,
            "consecutive_below_count": consecutive_below,
            "wing_dullness_triggered": wing_dullness_triggered,
        })

    return out_periods


def main():
    data = load_input()
    output = {
        "_data_source": data["_data_source"],
        "_harness": "entity/harness.py（命令式for循环风格，fractions.Fraction精确有理数）",
        "wings": {}
    }
    for wing_name, wing_data in data["wings"].items():
        output["wings"][wing_name] = compute_wing(
            wing_name, wing_data, data["scenario_shock"], data["slots"]
        )

    with open("harness_output.json", "w", encoding="utf-8") as fh:
        json.dump(output, fh, ensure_ascii=False, indent=2)

    print("harness真跑完成：两翼×9期×9分量，已写出 harness_output.json")


if __name__ == "__main__":
    main()

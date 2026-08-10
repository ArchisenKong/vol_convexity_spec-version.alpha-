"""
TPL1-T76-01 引擎 · 续2续修复 · 产物新鲜度钉定件生成（D-4/E-1封堵，A10判据基线）

背景（外审E-1实证）：`entity/engine.py` 注入两处实质变异后，若不重跑
`entity/harness.py`／`verify/independent_recompute.py`／`verify/regression_check.py`
即直接执行 `verify/assert_check.py`，此前全链无任何机制核证
`entity/harness_output.json`／`verify/independent_expected.json`／
`verify/regression_q0_output.json` 三份产物系当前源码之产出——40/40 PASS、exit=0，
陈旧产物通道全绿放行。

用途：在 `entity/harness.py`／`verify/independent_recompute.py`／
`verify/regression_check.py` 三脚本全部产出完毕后，一次性钉定"源码/输入"与
"其对应产物"之SHA256对应关系，供 `verify/assert_check.py` 之 A10 断言核验。

锚定设计（严格区分两条独立路径，不破坏D段②独立性纪律）：
  · `entity/harness_output.json` 与 `verify/regression_q0_output.json`——
    均经由 `import engine` 之路径产出（harness.py／regression_check.py），
    锚＝ `entity/engine.py` ＋ `entity/input_data.json` 当前指纹。
  · `verify/independent_expected.json`——由 `verify/independent_recompute.py`
    独立产出，**不读取、不import被测engine模块**（D段②独立性纪律，任务包§4）；
    该件之新鲜度锚故取**其自身生成脚本＋输入数据**（`independent_recompute.py`
    ＋ `input_data.json`），而非engine.py——若锚取engine.py将使本件之"独立于
    被测实现"声明与"新鲜度依赖被测实现指纹"自相矛盾。此设计选择呈KD知悉
    （见切片记录本根裁定登记增量）。

运行时点＝构建流水线最后一步，须晚于 harness.py／independent_recompute.py／
regression_check.py 三者全部完成，早于 assert_check.py。本脚本自身零判据计算
逻辑，只读取包内既有文件计算SHA256指纹并落盘，不产出/修改任何数值判据数据。

数据源纪律（契约⑤）：零网络、零外部数据源；仅计算包内既有文件之SHA256指纹。
"""

import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
E = lambda *p: os.path.join(PKG, "entity", *p)
V = lambda *p: os.path.join(HERE, *p)

# 锚定对象：{声明键: 文件路径}
TARGETS = {
    "engine_py_sha256":                  E("engine.py"),
    "input_data_sha256":                 E("input_data.json"),
    "independent_recompute_py_sha256":   V("independent_recompute.py"),
    "harness_output_sha256":             E("harness_output.json"),
    "independent_expected_sha256":       V("independent_expected.json"),
    "regression_q0_output_sha256":       V("regression_q0_output.json"),
}


def _sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    out = {k: _sha256(p) for k, p in TARGETS.items()}
    out["_note"] = (
        "产物新鲜度钉定（D-4/E-1封堵）：本文件记录生成时点各源码/输入/产物之SHA256。"
        "assert_check.py A10断言核验当前值与此钉定值一致——任一失配即表明对应产物"
        "非当前源码/输入之产出（陈旧产物通道），或该产物/源码本身遭直接篡改。"
        "engine_py/input_data 锚定 harness_output 与 regression_q0_output 两件"
        "（均经import engine产出）；independent_recompute_py/input_data 锚定"
        "independent_expected（不import engine，锚取自身生成脚本，维持D段②独立性）。"
    )
    with open(V("build_provenance.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("build_provenance.json 已生成：")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

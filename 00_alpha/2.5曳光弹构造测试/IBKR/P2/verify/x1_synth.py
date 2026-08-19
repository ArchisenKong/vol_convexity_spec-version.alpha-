# -*- coding: utf-8 -*-
"""X-1 跨环境浮点对比素材生成（§5 步5，目标3，DOC-25 前置素材）。

用途＝**浮点复现性探针**，不测「算得对不对」，只测「同一输入在不同环境下是否
算出同一串 bit」。故输入必须钉死、可无限次原样重放；probe/ 之一次性行情数值
不得用作基准（下次重放输入即已改变，差异归因不可分）。

fixture 来源纪律（§4A 第2条 ＋ 张力①处置(b)，KY 20260811/20260812 裁定）：
本文件内之 q/r 数值字面量系 **KY 显式给定之合成常数**，非执行侧代填，亦非探针
采集值；其在场经 KY 处置(b) 授权。A9 之机械射程＝entity/∪probe/，本文件位于
verify/ 子树，不在其内——此为规格设计之结果，非规避。

fixture 数值来源标注（不冒充纯合成）：
    spot/strike/implied_vol 之量级参照 20260812 实时行情，由 **KY 手工钉定**，
    非探针采集、不入 data_manifest、不带外部数据标记。
"""

import hashlib
import json
import math
import os
import platform
import sys

sys.dont_write_bytecode = True
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "entity"))

import engine                                                    # noqa: E402

# --------------------------------------------------------------------------
# X-1 fixture —— KY 20260812 钉定，从此不得变更（DOC-25 标准测试向量）
# --------------------------------------------------------------------------

X1_LOT = {
    "lot_id": "X1_SYNTH_ES_001",
    "instrument_class": "american_option",
    "exercise_style": "american",
    "option_type": "put",
    "spot": 7775.0,
    "strike": 7775.0,
    "implied_vol": 0.122,
    "valuation_date": "2026-08-12",
    "expiry": "2026-08-14",
    "risk_free_rate": 0.04,      # KY 显式给定（处置(b)）
    "dividend_yield": 0.0,       # KY 显式给定（处置(b)）
    "multiplier": 50,
    "quantity": 1,
    "side": "short",
}

X1_PROVENANCE = {
    "supplied_by": "KY",
    "supplied_on": "2026-08-12",
    "nature": "手工钉定常数；量级参照 20260812 实时行情，非探针采集",
    "isolation": "留于 verify/ 子树；不入 data_manifest；不带外部数据标记",
    "clause": "P1规格件 v1.2 §5 步5 ＋ 张力①处置(b)",
    "immutable": "钉定后不得变更——变更即毁 DOC-25 跨环境对比基准",
}


def bitwise(x):
    """逐位形态：hex() 为 IEEE754 精确表示，repr 为最短往返表示。"""
    if isinstance(x, float):
        return {"repr": repr(x), "hex": float.hex(x),
                "is_nan": math.isnan(x), "is_inf": math.isinf(x)}
    return {"repr": repr(x), "hex": None, "is_nan": False, "is_inf": False}


def walk_bitwise(obj):
    if isinstance(obj, dict):
        return {k: walk_bitwise(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [walk_bitwise(v) for v in obj]
    if isinstance(obj, float):
        return bitwise(obj)
    return obj


def env_fingerprint():
    """环境指纹：Python／平台／libm 面。

    libm 无跨平台直取接口，故以**探针值**间接指纹化：取一组超越函数在钉定输入
    上的精确位串，其哈希即该环境数学库行为之可比标识。
    """
    probes = {}
    for name, fn, arg in (
        ("exp(1)", math.exp, 1.0),
        ("exp(-0.5)", math.exp, -0.5),
        ("log(2)", math.log, 2.0),
        ("sqrt(2)", math.sqrt, 2.0),
        ("pow(1.0000001,500)", lambda a: math.pow(a, 500), 1.0000001),
        ("erf(0.7)", math.erf, 0.7),
        ("expm1(1e-8)", math.expm1, 1e-8),
    ):
        probes[name] = float.hex(fn(arg))
    digest = hashlib.sha256(
        json.dumps(probes, sort_keys=True).encode("utf-8")).hexdigest()

    return {
        "python_version": platform.python_version(),
        "python_build": list(platform.python_build()),
        "python_compiler": platform.python_compiler(),
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "libc_ver": list(platform.libc_ver()),
        "float_info": {k: getattr(sys.float_info, k)
                       for k in ("mant_dig", "max_exp", "min_exp", "epsilon",
                                 "dig", "radix", "rounds")},
        "libm_fingerprints": probes,
        "libm_fingerprint_digest": digest,
    }


def main():
    engine_sha = hashlib.sha256(
        open(os.path.join(ROOT, "entity", "engine.py"), "rb").read()).hexdigest()

    result = engine.evaluate_lot(dict(X1_LOT))

    report = {
        "purpose": "X-1 跨环境浮点对比素材（DOC-25 前置素材）",
        "clause": "P1规格件 v1.2 §1 目标3 ／ §5 步5",
        "engine_sha256": engine_sha,
        "fixture": X1_LOT,
        "fixture_provenance": X1_PROVENANCE,
        "environment": env_fingerprint(),
        "result_bitwise": walk_bitwise(result),
        "result_plain": result,
    }

    out = os.path.join(ROOT, "verify", "x1_env_report.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)

    print("=" * 76)
    print("X-1 合成用例 %s  |  engine=%s" % (X1_LOT["lot_id"], engine_sha[:16]))
    print("=" * 76)
    print("环境: %s %s / %s"
          % (platform.python_implementation(), platform.python_version(),
             platform.platform()))
    print("libm 探针摘要: %s" % report["environment"]["libm_fingerprint_digest"])
    print("-" * 76)

    def show(prefix, d):
        for k in sorted(d):
            v = d[k]
            if isinstance(v, dict) and "hex" in v:
                print("%s%-28s %-24s %s" % (prefix, k, v["repr"], v["hex"]))
            elif isinstance(v, dict):
                print("%s%s:" % (prefix, k))
                show(prefix + "  ", v)
            else:
                print("%s%-28s %s" % (prefix, k, v))

    show("", report["result_bitwise"])
    print("-" * 76)
    print("报告 → verify/x1_env_report.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())

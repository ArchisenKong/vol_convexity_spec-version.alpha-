"""
负向对照自查（构造侧留痕，非G4外审重放，非合格判定依据本身）

用途：核验 assert_check.py 之检出力非空转。篡改逐例注入 → 跑断言 → 记录退出码
→ 复原。含输出形态封闭类注入（裁决38-2 锚点一同型：新增顶层键／删声明键），
以自证第三可检层次在本包内确为可检。

续2续修复新增第5例（乙-4补齐，D-2）：此前四例注入位全部在 entity/harness_output.json
（产物侧），对 entity/engine.py（被测实现）零注入，且零例触及q承接逻辑——外审D-2
定性成立（手册v1.5 §3.1〔乙-4〕：注入位须在被测实现，非比对器/产物）。第5例向
entity/engine.py 源码本体注入已知变异（d1中q符号翻转，覆盖q增量面），且刻意不
重跑下游产物（镜像E-1攻击协议），以验证该注入经由续2续修复新增之A10产物新鲜度
机制（D-4/E-1封堵）被击落——同时验证乙-4补齐与D-4/E-1封堵之联动闭环，而非仅
数值面偶然命中。失败输出之具体断言名取自assert_check.py本次真实运行结果
（ast.literal_eval解析其"失败项："行），非硬编码预期。
"""

import ast
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
OUT = os.path.join(PKG, "entity", "harness_output.json")
BAK = OUT + ".nc_backup"
ENGINE = os.path.join(PKG, "entity", "engine.py")
ENGINE_BAK = ENGINE + ".nc_backup"
LOG = os.path.join(HERE, "negative_control_log.txt")


def run():
    p = subprocess.run([sys.executable, os.path.join(HERE, "assert_check.py")],
                       capture_output=True, text=True)
    return p.returncode


def run_capture_fails():
    """跑assert_check.py，返回(退出码, 失败断言名清单)——真实断言流水线取得，非硬编码。"""
    p = subprocess.run([sys.executable, os.path.join(HERE, "assert_check.py")],
                       capture_output=True, text=True)
    fails = []
    for ln in p.stdout.split("\n"):
        if ln.startswith("失败项："):
            try:
                fails = ast.literal_eval(ln[len("失败项："):].strip())
            except (ValueError, SyntaxError):
                fails = []
    return p.returncode, fails


def load():
    with open(OUT, "r", encoding="utf-8") as fh:
        return json.load(fh)


def save(d):
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def main():
    lines = []
    shutil.copyfile(OUT, BAK)
    base_rc = run()
    lines.append("基线（未篡改）退出码 = %d" % base_rc)

    cases = []

    d = load()
    d["base_valuation"][4]["per_unit"]["delta"] = 0.9
    save(d)
    cases.append(("数值篡改：L05 base per_unit.delta 0.341701→0.9（续2q增强后基准值）", run()))
    shutil.copyfile(BAK, OUT)

    d = load()
    d["_shadow_output"] = {"x": 1}
    save(d)
    cases.append(("输出形态封闭：新增未声明顶层键 _shadow_output", run()))
    shutil.copyfile(BAK, OUT)

    d = load()
    del d["time_shift_revaluation"]
    save(d)
    cases.append(("输出形态封闭：静默删声明键 time_shift_revaluation", run()))
    shutil.copyfile(BAK, OUT)

    d = load()
    d["base_valuation"][3]["route_id"] = "bs_dividend_yield_closed_form"
    save(d)
    cases.append(("路由身份篡改：L04 futures 路由改标为欧式闭式（续2改名后route_id）", run()))
    shutil.copyfile(BAK, OUT)

    for name, rc in cases:
        lines.append("%-58s 退出码=%d  %s" % (name, rc, "检出" if rc else "漏检"))

    # --- 案例5（续2续修复新增，乙-4补齐，D-2）：被测实现（engine.py）源码级注入，
    #     覆盖q增量面；刻意不重跑下游产物，验证A10产物新鲜度机制（D-4/E-1联动）------
    OLD_D1 = "(r - q + 0.5 * sig * sig)"
    NEW_D1 = "(r + q + 0.5 * sig * sig)"
    with open(ENGINE, "r", encoding="utf-8") as fh:
        eng_src = fh.read()
    hit_count = eng_src.count(OLD_D1)
    if hit_count != 1:
        raise SystemExit("案例5注入目标片段命中数=%d（应为1），注入位不明确，中止自查"
                         % hit_count)
    shutil.copyfile(ENGINE, ENGINE_BAK)
    with open(ENGINE, "w", encoding="utf-8") as fh:
        fh.write(eng_src.replace(OLD_D1, NEW_D1))

    rc5, fails5 = run_capture_fails()

    shutil.copyfile(ENGINE_BAK, ENGINE)
    os.remove(ENGINE_BAK)
    with open(ENGINE, "r", encoding="utf-8") as fh:
        restored_ok = (fh.read() == eng_src)

    case5_name = ("被测实现源码注入：entity/engine.py d1中 (r−q) 符号翻转为 (r+q)"
                 "（注入位在被测实现，覆盖q增量面，不重跑下游产物）")
    lines.append("%-58s 退出码=%d  %s" % (case5_name, rc5, "检出" if rc5 else "漏检"))
    lines.append("  案例5失败断言（真实断言流水线取得，非硬编码）：%s" % (fails5 or "无"))
    lines.append("  案例5复原核验：entity/engine.py 复原后与注入前逐字节一致 = %s" % restored_ok)

    final_rc = run()
    lines.append("复原后退出码 = %d" % final_rc)
    os.remove(BAK)

    all_rcs = [rc for _, rc in cases] + [rc5]
    ok = (base_rc == 0 and final_rc == 0 and restored_ok
         and all(rc != 0 for rc in all_rcs) and bool(fails5))
    lines.append("自查结论：%s（产物侧%d/%d检出 ＋ 被测实现侧%d/%d检出，乙-4补齐）"
                 % ("检出力成立" if ok else "存在漏检",
                    sum(1 for _, rc in cases if rc), len(cases),
                    (1 if rc5 else 0), 1))
    text = "\n".join(lines)
    with open(LOG, "w", encoding="utf-8") as fh:
        fh.write(text + "\n")
    print(text)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
P2' · α-6 runner · 载体根 GL-06 之环境内可运行性

射程（规格件 §3.1 α-6）：将 GL-06 之 entity/ 四件搬入运行位，以其自带 15 期人造账本 input
实跑，与本地 harness_output.json 逐字节比对。

本件为**纯人造 harness**：零 QC 库导入、零接口面字面、零外部数据源、零网络。
（A'-6 口径：entity/ 只放被测件与纯人造 harness；接口面代码落 probe/。）

禁作面自守：本件零 L3 判据产出、零合格主张、零收益/夏普/回撤类指标。
比对结果**不得**被表述为 GL-06 之任何层级合格主张（规格件 §3.1 禁作面）。

输出：结构化 dict，经 emit() 打印为单行 JSON，便于任何运行位回传。
"""
import hashlib
import json
import os
import platform
import subprocess
import sys
import tempfile

PAYLOAD_MODULE = "cloud_payload_gl06"

FILES = {
    "input_schema.md": "gl06_input_schema.md",
    "ledger_input.json": "gl06_ledger_input.json",
    "harness.py": "gl06_harness.py",
    "harness_output.json": "gl06_harness_output.json",
}


def _run_harness(script, work):
    """执行被测脚本，返回 (exec_mode, returncode, stdout, stderr)。

    exec_mode ∈ {"subprocess", "inprocess"}：
      · "subprocess"：与本地对照组／research 位同形态。
      · "inprocess" ：回退路径（回测运行位 Python 嵌于 .NET，sys.executable 未必可用）。
    **两形态之结果不得混同比对**，故 exec_mode 随结果一并回传、逐次留痕。
    """
    try:
        p = subprocess.run([sys.executable, script], capture_output=True, cwd=work, timeout=600)
        return ("subprocess", p.returncode,
                p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace"))
    except Exception as sub_err:
        import io
        import runpy
        import contextlib
        cwd0 = os.getcwd()
        so, se = io.StringIO(), io.StringIO()
        rc = 0
        try:
            os.chdir(work)
            with contextlib.redirect_stdout(so), contextlib.redirect_stderr(se):
                runpy.run_path(script, run_name="__main__")
        except SystemExit as e:
            rc = int(e.code or 0)
        except Exception:
            import traceback as _tb
            rc = 1
            se.write(_tb.format_exc())
        finally:
            os.chdir(cwd0)
        return ("inprocess", rc,
                so.getvalue(), (se.getvalue() + "\n[subprocess 不可用: %s: %s]" % (
                    type(sub_err).__name__, sub_err)))


def env_fingerprint():
    """环境指纹四项（形态照第一发 x1_env_report）。零凭据、零账户信息。"""
    fp = {
        "python_version": sys.version.split()[0],
        "python_version_full": sys.version.replace("\n", " "),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "implementation": platform.python_implementation(),
    }
    try:
        fp["libc_ver"] = list(platform.libc_ver())
    except Exception as e:
        fp["libc_ver"] = "ERR: %s" % e
    return fp


def run_alpha6():
    mod = __import__(PAYLOAD_MODULE)

    work = tempfile.mkdtemp(prefix="p2p_alpha6_")
    restored = {}
    for target, src in FILES.items():
        raw = mod.restore(src)                      # 内含 SHA256 自核，不一致即抛
        p = os.path.join(work, target)
        with open(p, "wb") as f:
            f.write(raw)
        restored[target] = {
            "src_name": src,
            "size": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
        }

    # 期望件字节须先存住 —— harness 会覆盖同名文件
    expected_path = os.path.join(work, "harness_output.json")
    with open(expected_path, "rb") as f:
        expected_bytes = f.read()
    expected_sha = hashlib.sha256(expected_bytes).hexdigest()

    # 实跑。首选子进程隔离（与本地对照组、research 位同形态，保可比性）；
    # 回测运行位之 Python 嵌于 .NET，`sys.executable` 未必可用，故备进程内回退。
    # **实际走哪条路逐次记录**，不同形态之结果不得混同比对。
    exec_mode, rc, so, se = _run_harness(os.path.join(work, "harness.py"), work)

    with open(expected_path, "rb") as f:
        produced_bytes = f.read()
    produced_sha = hashlib.sha256(produced_bytes).hexdigest()

    byte_exact = (produced_bytes == expected_bytes)

    # --- 双值并列（A'-16 代定形态 (iii)：双值并列不单判）---
    # 成因（本地对照组实测，非推测）：GL-06 harness 以 open(path,"w") 文本模式写盘，
    # 平台行尾约定介入；锚件 harness_output.json 为纯 LF（0 CR / 149 LF）。
    # 本机（Windows）跑出 149 CRLF，+149 B，归一化后 sha256 精确命中锚值。
    # 故「逐字节比对」单值无法分辨「计算不同」与「行尾不同」，须双值并列。
    norm_produced = produced_bytes.replace(b"\r\n", b"\n")
    norm_expected = expected_bytes.replace(b"\r\n", b"\n")
    byte_exact_normalized = (norm_produced == norm_expected)
    newline_profile = {
        "expected": {"CR": expected_bytes.count(b"\r"), "LF": expected_bytes.count(b"\n"),
                     "CRLF": expected_bytes.count(b"\r\n")},
        "produced": {"CR": produced_bytes.count(b"\r"), "LF": produced_bytes.count(b"\n"),
                     "CRLF": produced_bytes.count(b"\r\n")},
    }

    # 不逐字节相等时：给出可判读的差异定位（不作原因断言）
    diff = None
    if not byte_exact:
        diff = {
            "expected_size": len(expected_bytes),
            "produced_size": len(produced_bytes),
            "first_diff_offset": next(
                (i for i, (a, b) in enumerate(zip(expected_bytes, produced_bytes)) if a != b),
                min(len(expected_bytes), len(produced_bytes)),
            ),
        }
        try:
            e = json.loads(expected_bytes.decode("utf-8"))
            p = json.loads(produced_bytes.decode("utf-8"))
            diff["json_semantically_equal"] = (e == p)
        except Exception as ex:
            diff["json_parse_error"] = str(ex)

    return {
        "_result_marker": "P2PRIME_ALPHA6_RESULT_V1",
        "target": "alpha-6 · GL-06 环境内可运行性",
        "env_fingerprint": env_fingerprint(),
        "restored_files": restored,
        "exec_mode": exec_mode,
        "harness_exit_code": rc,
        "harness_stdout": so,
        "harness_stderr": se,
        "expected_sha256": expected_sha,
        "produced_sha256": produced_sha,
        "byte_exact": byte_exact,
        "byte_exact_normalized": byte_exact_normalized,
        "normalized_produced_sha256": hashlib.sha256(norm_produced).hexdigest(),
        "normalized_expected_sha256": hashlib.sha256(norm_expected).hexdigest(),
        "newline_profile": newline_profile,
        "normalization_operator": "bytes.replace(b'\\r\\n', b'\\n')  —— 仅行尾，不触碰其他字节",
        "diff": diff,
        "_disclaimer": "本结果为环境可运行性材料；零 L3 判据、零合格主张、不得表述为 GL-06 任何层级之合格判定",
    }


def emit(result):
    # 输出编码钉死为 utf-8：Windows 本地重定向默认走 locale(GBK)，会写坏非 ASCII 字节。
    # 运行位之间编码不一致属回传保真面，须由本件自身承载，不依赖外部环境变量。
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    print("<<<P2PRIME_ALPHA6_BEGIN>>>")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    print("<<<P2PRIME_ALPHA6_END>>>")


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    emit(run_alpha6())

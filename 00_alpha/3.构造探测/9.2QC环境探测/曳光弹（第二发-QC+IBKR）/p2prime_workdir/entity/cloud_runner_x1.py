# -*- coding: utf-8 -*-
"""
P2' · X-1 runner · engine 于运行位实跑，产逐位输出与环境指纹

射程（规格件 §3.2）：fixture ＝ `X1_SYNTH_ES_001`（第一发已钉定，**不新造**）；
引擎 ＝ v1.3（续3 美式 CRR）；**DOC-25 兑现点不变更**，本发只产素材。

本件为**纯人造 harness**：零 QC 库导入、零接口面字面、零外部数据源、零网络。

执行形态（与第一发**同一份字节**，不重新实现，防口径漂移）：
  · 还原 engine.py → <work>/entity/engine.py
  · 还原 x1_synth.py → <work>/verify/x1_synth.py   （KY 钉定 fixture，逐字节搬运）
  · 子进程执行 x1_synth.py（其内部按 ROOT/entity、ROOT/verify 定位，故须造此结构）
  · 读回 <work>/verify/x1_env_report.json

禁作面自守：零 L3 判据、零合格主张、零收益/夏普/回撤类指标。
比对与判定归本地与 KD，本件只产素材、不判「是否一致」（归纳纪律：不预填）。
"""
import hashlib
import json
import os
import platform
import subprocess
import sys
import tempfile


def env_fingerprint_outer():
    """运行位外层指纹（与 x1_synth 内部指纹互为旁证；两者应一致）。"""
    fp = {
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "machine": platform.machine(),
        "implementation": platform.python_implementation(),
    }
    try:
        fp["libc_ver"] = list(platform.libc_ver())
    except Exception as e:
        fp["libc_ver"] = "ERR: %s" % e
    return fp


def run_x1():
    eng_mod = __import__("cloud_payload_engine")
    x1_mod = __import__("cloud_payload_x1")

    work = tempfile.mkdtemp(prefix="p2p_x1_")
    os.makedirs(os.path.join(work, "entity"), exist_ok=True)
    os.makedirs(os.path.join(work, "verify"), exist_ok=True)

    restored = {}
    eng = eng_mod.restore("engine.py")            # 内含 SHA256 自核
    with open(os.path.join(work, "entity", "engine.py"), "wb") as f:
        f.write(eng)
    restored["entity/engine.py"] = {"size": len(eng), "sha256": hashlib.sha256(eng).hexdigest()}

    syn = x1_mod.restore("x1_synth.py")
    with open(os.path.join(work, "verify", "x1_synth.py"), "wb") as f:
        f.write(syn)
    restored["verify/x1_synth.py"] = {"size": len(syn), "sha256": hashlib.sha256(syn).hexdigest()}

    from cloud_runner_alpha6 import _run_harness   # 同一份实现，防两处口径漂移
    exec_mode, rc, so, se = _run_harness(os.path.join(work, "verify", "x1_synth.py"), work)

    report_path = os.path.join(work, "verify", "x1_env_report.json")
    report, report_raw_sha, report_bytes_len = None, None, None
    if os.path.exists(report_path):
        with open(report_path, "rb") as f:
            rb = f.read()
        report_raw_sha = hashlib.sha256(rb).hexdigest()
        report_bytes_len = len(rb)
        try:
            report = json.loads(rb.decode("utf-8"))
        except Exception as e:
            report = {"_parse_error": str(e)}

    return {
        "_result_marker": "P2PRIME_X1_RESULT_V1",
        "target": "X-1 · 运行位浮点素材（DOC-25 前置素材，兑现点不变更）",
        "fixture_id": "X1_SYNTH_ES_001",
        "engine_version": "v1.3 (续3 美式切片, CRR)",
        "outer_env_fingerprint": env_fingerprint_outer(),
        "restored_files": restored,
        "exec_mode": exec_mode,
        "x1_synth_exit_code": rc,
        "x1_synth_stdout": so,
        "x1_synth_stderr": se,
        "report_bytes": report_bytes_len,
        "report_sha256": report_raw_sha,
        "report": report,
        "_disclaimer": ("本结果为跨环境浮点对比**素材**；本件不判「是否一致」、"
                        "不产 L3 判据、不作合格主张。比对与判定归本地与 KD。"),
    }


def emit(result):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    print("<<<P2PRIME_X1_BEGIN>>>")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, default=str))
    print("<<<P2PRIME_X1_END>>>")


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    emit(run_x1())

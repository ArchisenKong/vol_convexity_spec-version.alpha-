# -*- coding: utf-8 -*-
"""
P2' · 作业指令 §5-1 基线快照（只读，零写入零删除）

射程：云端项目文件清单（files.get_all）／云端 Object Store 清单／research 节点状态。
用途＝遗留物基线隔离（E1-17）。本脚本不清理、不删除、不覆盖任何遗留物（A'-12）。

破坏性动作全禁（A'-14）：本脚本零 push／零 delete／零 set／零 create。

凭据处理：api_client 由 lean 自动从 ~/.lean/credentials 构造（KD 20260818 授权形态甲）。
本脚本不打印、不写出任何凭据值。落盘前对疑似敏感键名递归遮蔽，并对文本面正则复扫。

落位：本件属 QC 接口面代码，按 A'-6 落 probe/ 子树。
键名污染标记（D-3）：输出顶层键加 _probe_ 前缀，_data_source=external_probe_NOT_FOR_ENTITY。
"""
import json
import re
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# 探测期既有标识（自事实基底装载，非本位新造）
PROJECT_ID = 35174460                                   # TR2-ENV-PROBE（遗留物，E1-17）
ORG_ID = "954877bda8b6760ae398418ce79a5500"

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
RAW.mkdir(parents=True, exist_ok=True)

TS = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

SENSITIVE = (
    "token", "apikey", "api_key", "secret", "password", "passwd", "credential",
    "sessionid", "session_id", "authorization",
    # 支付面夹带（E1-18／F1-14）
    "card", "last4", "expiration", "brand",
)

# 文本面复扫模式（遮蔽后残留检测）
LEAK_PAT = re.compile(r"[0-9a-f]{40,}", re.I)


def redact(obj):
    """递归遮蔽疑似凭据字段。形态照探测期 api_surface_probe.py，未改写。"""
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if any(s in str(k).lower() for s in SENSITIVE):
                out[k] = "<REDACTED>"
            else:
                out[k] = redact(v)
        return out
    if isinstance(obj, list):
        return [redact(v) for v in obj]
    return obj


def dump(model):
    for attr in ("model_dump", "dict"):
        if hasattr(model, attr):
            try:
                return redact(getattr(model, attr)())
            except Exception:
                pass
    return redact({"__repr__": repr(model)})


RESULTS = {}
SEQ = [0]


def emit(name, payload, endpoint_class, note=""):
    """乙-5：落盘带序号＋时间戳，不覆盖同名。
    冲突声明：本件为【遮蔽后】件，非逐字节原件——夹带凭据之响应上，
    乙-5「先落原件」与 A8'「凭据零落盘」直接冲突，本位按 AGENTS.md 第6条处置并呈 KD。"""
    SEQ[0] += 1
    fn = RAW / ("%02d_%s_%s.json" % (SEQ[0], name, TS))
    body = {
        "_probe_name": name,
        "_probe_captured_utc": TS,
        "_probe_endpoint_class": endpoint_class,   # A 类＝lean 库已发布；B 类＝未文档化（A'-10 仅作旁证）
        "_probe_note": note,
        "_probe_redaction_operator": "recursive key-substring match on SENSITIVE tuple -> '<REDACTED>'",
        "_probe_is_byte_exact_original": False,
        "_probe_original_fidelity_note": "遮蔽后件；乙-5 原件纪律与 A8' 凭据零落盘在此冲突，见摩擦登记 FR-P2-01",
        "_data_source": "external_probe_NOT_FOR_ENTITY",
        "_probe_payload": payload,
    }
    text = json.dumps(body, ensure_ascii=False, indent=2, default=str)
    leaks = LEAK_PAT.findall(text)
    body["_probe_post_redaction_leak_scan_hits"] = len(leaks)
    text = json.dumps(body, ensure_ascii=False, indent=2, default=str)
    fn.write_text(text, encoding="utf-8")
    print("    [WROTE] %s  (%d bytes, leak-scan hits=%d)" % (fn.name, len(text.encode()), len(leaks)))
    if leaks:
        print("    [WARN ] 遮蔽后长十六进制串残留 %d 处——须人工判读是否为凭据（也可能是 backtest/project id）" % len(leaks))
    return body


def probe(label, fn, name, endpoint_class, note=""):
    print("\n" + "=" * 72)
    print("=== %s   [%s]" % (label, endpoint_class))
    print("=" * 72)
    try:
        result = fn()
    except Exception as e:
        msg = str(e)
        print("[FAIL] %s: %s" % (type(e).__name__, msg[:500]))
        RESULTS[name] = {"status": "FAIL", "error_type": type(e).__name__, "error_text": msg}
        emit(name + "_ERROR", {"error_type": type(e).__name__, "error_text": msg},
             endpoint_class, note + " | 调用失败，错误原文全量留痕")
        return None
    if isinstance(result, list):
        print("[OK] list, %d 项" % len(result))
        data = [dump(x) for x in result]
    elif isinstance(result, dict):
        print("[OK] dict")
        data = redact(result)
    else:
        print("[OK] 单对象")
        data = dump(result)
    RESULTS[name] = {"status": "OK"}
    emit(name, data, endpoint_class, note)
    return data


def main():
    print("=== P2' §5-1 基线快照 · 只读 ===")
    print("捕获时刻(UTC): %s" % TS)
    print("PROJECT_ID = %d  (TR2-ENV-PROBE, 遗留物, E1-17)" % PROJECT_ID)
    print("ORG_ID     = %s" % ORG_ID)
    print("破坏性动作: 零 push / 零 delete / 零 set / 零 create")

    from lean.container import container
    api = container.api_client

    # --- 1. 云端项目清单（本发是否另建项目，待 KD 授权后另议；本步只读现状）
    probe("projects.get_all() — 账户下全部云端项目",
          lambda: api.projects.get_all(), "projects_all", "A", "遗留物基线：项目面")

    # --- 2. 云端项目文件清单（§5-1 明列）
    probe("files.get_all(%d) — TR2-ENV-PROBE 文件清单" % PROJECT_ID,
          lambda: api.files.get_all(PROJECT_ID), "project_files", "A",
          "§5-1 明列项；遗留物基线：文件面")

    # --- 3. 节点状态（§5-1 research 节点状态；E1-13 busy:true 未释放）
    probe("nodes.get_all(ORG_ID) — 节点与配额",
          lambda: api.nodes.get_all(ORG_ID), "nodes_all", "A",
          "§5-1 明列项；E1-13 research 节点 busy 状态核对位")

    # --- 4. 云端 Object Store 清单（§5-1 明列；E1-12 get 被 Institutional 闸拒，list 通）
    def _os_list():
        if hasattr(api, "object_store"):
            return api.object_store.list(ORG_ID)
        return api.get("object/list", {"organizationId": ORG_ID})
    probe("object-store list — 云端 Object Store 清单",
          _os_list, "object_store_list", "A",
          "§5-1 明列项；E1-12：list 通 / get 被 Institutional 闸拒。本步只 list，零 set 零 delete")

    # --- 5. research 节点状态（B 类端点；A'-10 仅作旁证，不入主链路）
    probe("research/read — research 会话状态（B 类）",
          lambda: api.get("research/read", {"projectId": PROJECT_ID}), "research_read", "B",
          "B 类端点，A'-10 代定＝仅作旁证不入主链路；E1-18 响应夹带 session token，已遮蔽")

    print("\n" + "=" * 72)
    print("=== §5-1 汇总 ===")
    for k, v in RESULTS.items():
        print("  %-22s %s" % (k, v["status"] + (("  " + v.get("error_type", "")) if v["status"] == "FAIL" else "")))
    print("\n落位: %s" % RAW)
    print("零写入云端 / 零删除 / 零遗留物触碰。")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)

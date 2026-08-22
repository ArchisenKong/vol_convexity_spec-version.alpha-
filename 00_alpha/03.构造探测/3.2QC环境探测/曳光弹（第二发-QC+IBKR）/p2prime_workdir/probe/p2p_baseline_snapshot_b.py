# -*- coding: utf-8 -*-
"""
P2' · 作业指令 §5-1 基线快照 · 补跑 B 轮（只读，零写入零删除）

补跑对象＝A 轮三个 FAIL 项。成因分列（现象与原因分开写）：
  - projects_all      : 【本位工程 bug】调用签名错——get_all(organization_id) 必填，A 轮漏传。
                        属 AGENTS.md 第5条「适配层工程 bug」可调试范围，非环境摩擦。
  - object_store_list : 【本位工程 bug】签名为 list(path, organization_id)，A 轮传参位错。同上。
  - research_read     : 【环境面】RequestFailedError "Timeout waiting for a node allocation,
                        please retry."——错误原文自带 retry 语义，且 E1-06 已载异步须重试，
                        故本轮按重试语义多轮实测后再判三态，不提前定性。

破坏性动作全禁（A'-14）：零 push／零 delete／零 set／零 create。
凭据：api_client 由 lean 自动从 ~/.lean/credentials 构造；本脚本不打印、不写出凭据值。
"""
import json
import re
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ID = 35174460
ORG_ID = "954877bda8b6760ae398418ce79a5500"
RETRY_N = 5
RETRY_GAP = 20  # 秒

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
RAW.mkdir(parents=True, exist_ok=True)
TS = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

SENSITIVE = ("token", "apikey", "api_key", "secret", "password", "passwd", "credential",
             "sessionid", "session_id", "authorization",
             "card", "last4", "expiration", "brand")
LEAK_PAT = re.compile(r"[0-9a-f]{40,}", re.I)


def redact(obj):
    if isinstance(obj, dict):
        return {k: ("<REDACTED>" if any(s in str(k).lower() for s in SENSITIVE) else redact(v))
                for k, v in obj.items()}
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


SEQ = [10]


def emit(name, payload, endpoint_class, note=""):
    SEQ[0] += 1
    fn = RAW / ("%02d_%s_%s.json" % (SEQ[0], name, TS))
    body = {
        "_probe_name": name,
        "_probe_captured_utc": TS,
        "_probe_endpoint_class": endpoint_class,
        "_probe_note": note,
        "_probe_redaction_operator": "recursive key-substring match on SENSITIVE tuple -> '<REDACTED>'",
        "_probe_is_byte_exact_original": False,
        "_probe_original_fidelity_note": "遮蔽后件；乙-5 原件纪律与 A8' 凭据零落盘在此冲突，见 FR-P2-01",
        "_data_source": "external_probe_NOT_FOR_ENTITY",
        "_probe_payload": payload,
    }
    text = json.dumps(body, ensure_ascii=False, indent=2, default=str)
    body["_probe_post_redaction_leak_scan_hits"] = len(LEAK_PAT.findall(text))
    text = json.dumps(body, ensure_ascii=False, indent=2, default=str)
    fn.write_text(text, encoding="utf-8")
    print("    [WROTE] %s  (%d bytes, leak-scan hits=%d)"
          % (fn.name, len(text.encode()), body["_probe_post_redaction_leak_scan_hits"]))


def probe(label, fn, name, cls, note=""):
    print("\n" + "=" * 72)
    print("=== %s   [%s]" % (label, cls))
    print("=" * 72)
    try:
        r = fn()
    except Exception as e:
        print("[FAIL] %s: %s" % (type(e).__name__, str(e)[:500]))
        emit(name + "_ERROR", {"error_type": type(e).__name__, "error_text": str(e)}, cls,
             note + " | 调用失败，错误原文全量留痕")
        return None
    if isinstance(r, list):
        print("[OK] list, %d 项" % len(r)); data = [dump(x) for x in r]
    elif isinstance(r, (dict, str)):
        print("[OK] %s" % type(r).__name__); data = redact(r) if isinstance(r, dict) else r
    else:
        print("[OK] 单对象"); data = dump(r)
    emit(name, data, cls, note)
    return data


def main():
    print("=== P2' §5-1 基线快照 · 补跑 B 轮 · 只读 ===")
    print("捕获时刻(UTC): %s" % TS)
    print("破坏性动作: 零 push / 零 delete / 零 set / 零 create\n")

    from lean.container import container
    api = container.api_client

    # --- 修 1：projects.get_all(organization_id)
    probe("projects.get_all(ORG_ID) — 账户下全部云端项目",
          lambda: api.projects.get_all(ORG_ID), "projects_all_B", "A",
          "A 轮 FAIL 成因＝本位签名 bug（漏传 organization_id），非环境摩擦")

    # --- 修 2：object_store.list(path, organization_id)
    probe("object_store.list('/', ORG_ID) — 云端 Object Store 根清单",
          lambda: api.object_store.list("/", ORG_ID), "object_store_list_B", "A",
          "A 轮 FAIL 成因＝本位传参位错，非环境摩擦。本步只 list，零 set 零 delete（E1-12：list 通/get 被 Institutional 闸拒）")

    # --- 环境面：research 节点分配重试实测
    print("\n" + "=" * 72)
    print("=== research/read 重试实测（%d 轮，间隔 %ds）  [B 类端点]" % (RETRY_N, RETRY_GAP))
    print("=== 依据：错误原文自带 'please retry'；E1-06 载异步须重试。逐轮全量留痕。")
    print("=" * 72)
    attempts = []
    for i in range(1, RETRY_N + 1):
        t0 = time.time()
        try:
            r = api.get("research/read", {"projectId": PROJECT_ID})
            el = time.time() - t0
            print("  [%d/%d] OK   耗时 %.1fs" % (i, RETRY_N, el))
            attempts.append({"attempt": i, "status": "OK", "elapsed_s": round(el, 1),
                             "payload": redact(r) if isinstance(r, dict) else str(r)})
            break
        except Exception as e:
            el = time.time() - t0
            print("  [%d/%d] FAIL 耗时 %.1fs  %s: %s" % (i, RETRY_N, el, type(e).__name__, str(e)[:200]))
            attempts.append({"attempt": i, "status": "FAIL", "elapsed_s": round(el, 1),
                             "error_type": type(e).__name__, "error_text": str(e)})
        if i < RETRY_N:
            time.sleep(RETRY_GAP)
    emit("research_read_retry_B", {"retry_count": RETRY_N, "gap_s": RETRY_GAP, "attempts": attempts}, "B",
         "环境面；E1-13 research 节点 busy 未释放之直接后果核验。三态判定归记录表，本件只载现象")

    # --- 节点状态复测（重试后）
    probe("nodes.get_all(ORG_ID) — 节点状态复测（重试轮后）",
          lambda: api.nodes.get_all(ORG_ID), "nodes_all_B", "A",
          "与 A 轮 03_nodes_all 对照，观察 busy 状态是否变动")

    print("\n落位: %s" % RAW)
    print("零写入云端 / 零删除 / 零遗留物触碰。")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)

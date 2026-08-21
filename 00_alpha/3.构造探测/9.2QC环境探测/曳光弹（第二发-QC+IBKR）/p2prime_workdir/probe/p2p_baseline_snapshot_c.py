# -*- coding: utf-8 -*-
"""
P2' · §5-1 基线快照 · C 轮（KD 删除云端项目后之新基线；只读，零写入零删除）

触发＝KD 20260818 手动删除云端项目 TR2-ENV-PROBE（id 35174460）。
本轮目的＝固定删除后之云端现状，作为本发新基线；A/B 轮快照转为「删除前历史留痕」。

射程：projects.get_all／nodes.get_all／object_store.list／files.get_all(35174460) 存在性复核。
**不调用 research/read**——该面待 KD 裁（KD-P2-03），本位不裁不碰。

破坏性动作全禁（A'-14）：零 push／零 delete／零 set／零 create。
凭据：api_client 由 lean 自动从 ~/.lean/credentials 构造；本脚本不打印、不写出凭据值。
"""
import json
import re
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OLD_PROJECT_ID = 35174460
ORG_ID = "954877bda8b6760ae398418ce79a5500"

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


SEQ = [20]


def emit(name, payload, cls, note=""):
    SEQ[0] += 1
    fn = RAW / ("%02d_%s_%s.json" % (SEQ[0], name, TS))
    body = {
        "_probe_name": name,
        "_probe_captured_utc": TS,
        "_probe_endpoint_class": cls,
        "_probe_note": note,
        "_probe_baseline_generation": "C — KD 删除云端项目后之新基线",
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
        print("[FAIL] %s: %s" % (type(e).__name__, str(e)[:400]))
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
    print("=== P2' §5-1 基线快照 · C 轮（KD 删除项目后）· 只读 ===")
    print("捕获时刻(UTC): %s" % TS)
    print("触发: KD 20260818 手动删除云端项目 TR2-ENV-PROBE (id %d)" % OLD_PROJECT_ID)
    print("不调用 research/read —— 待 KD 裁（KD-P2-03）")
    print("破坏性动作: 零 push / 零 delete / 零 set / 零 create\n")

    from lean.container import container
    api = container.api_client

    ps = probe("projects.get_all(ORG_ID) — 云端项目清单（删除后）",
               lambda: api.projects.get_all(ORG_ID), "projects_all_C", "A",
               "新基线：项目面")
    if ps is not None:
        print("\n  --- 项目面判读（事实，无推测）---")
        if len(ps) == 0:
            print("  账户下云端项目数 = 0")
        for p in ps:
            print("  id=%s name=%s modified=%s" % (p.get("projectId"), p.get("name"), p.get("modified")))
        still = [p for p in ps if str(p.get("projectId")) == str(OLD_PROJECT_ID)]
        print("  旧项目 %d 是否仍在清单: %s" % (OLD_PROJECT_ID, "是" if still else "否"))

    probe("files.get_all(%d) — 旧项目文件面存在性复核" % OLD_PROJECT_ID,
          lambda: api.files.get_all(OLD_PROJECT_ID), "old_project_files_C", "A",
          "存在性复核：预期应失败（项目已删）。失败原文全量留痕，不作可用性判定")

    probe("object_store.list('/', ORG_ID) — Object Store 根清单（删除后）",
          lambda: api.object_store.list("/", ORG_ID), "object_store_list_C", "A",
          "新基线：对象存储面。核对 E1-17 之 /tr2probe-e14-marker.txt 是否随项目删除而消失")

    probe("nodes.get_all(ORG_ID) — 节点状态（删除后）",
          lambda: api.nodes.get_all(ORG_ID), "nodes_all_C", "A",
          "新基线：节点面。与 A/B 轮对照")

    print("\n落位: %s" % RAW)
    print("零写入云端 / 零删除 / 零 research 面触碰。")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)

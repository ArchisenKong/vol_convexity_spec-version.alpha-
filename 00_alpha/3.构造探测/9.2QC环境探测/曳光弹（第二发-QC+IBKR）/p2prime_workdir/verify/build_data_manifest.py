# -*- coding: utf-8 -*-
"""
P2' · `probe/data_manifest.json` 生成（D-2 数据指纹黑名单）

口径（A'-8 代定）：D-2 ＝「`probe/` 内每一份**真实/外部数据载荷**之 SHA256」。
子集划定判据（机械形态，非数值口径）：
    凡「内容源自外部环境响应或 vendor 分发、且含数值载荷」之件入黑名单；
    判定位＝**该件是否可由本地人造输入完全重现**（可重现即非外部载荷）。
判据本身入 `_selection_rule` 字段，随 W-25 明细呈 KD 复核。

丙-2 兑现：kd_params 类参数件纳入生成范围（本发无此类件，显式声明「无对象」而非静默省略）。
A'-7：`lean init` 样本数据以**目录级承载**登记（清单件 SHA256 ＋ 总字节数），非逐件入 manifest。
E1-09/A'-16：凡经 `lean cloud pull` 落盘之件双列云端/本地值——本发**零 pull**，显式声明。
E1-11：指纹链排除面显式登记（非静默省略）。
零网络。
"""
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

WD = Path(__file__).resolve().parent.parent
PROBE = WD / "probe"
QCROOT = WD.parent.parent            # 9.QC环境探测/
TS = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

SELECTION_RULE = ("凡「内容源自外部环境响应或 vendor 分发、且含数值载荷」之件入黑名单；"
                  "判定位＝该件是否可由本地人造输入完全重现（可重现即非外部载荷）。"
                  "据此：probe/raw/**（API 响应载荷）与 probe/logs/**（外部环境 stdout/stderr）入；"
                  "probe/*.py（本位所著接口面代码，可完全重现）不入。")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def step_of(name):
    for k, v in (("baseline", "S1 基线快照"), ("alpha6", "S3 α-6"), ("x1_research", "S4 X-1-乙"),
                 ("cloud_project", "S2 云端承载"), ("cloud_upload", "S2 云端承载"),
                 ("backtest", "S5–S8 回测位"), ("rt_", "S6/S8 runtimeStatistics 回传"),
                 ("nodes", "S1 基线快照"), ("object_store", "S1 基线快照"),
                 ("projects", "S1 基线快照"), ("research", "S3/S4 research 位")):
        if k in name:
            return v
    return "未分类（呈 KD）"


def main():
    entries = []
    for sub in ("raw", "logs"):
        d = PROBE / sub
        if not d.exists():
            continue
        for p in sorted(d.rglob("*")):
            if p.is_file():
                rel = p.relative_to(WD).as_posix()
                entries.append({
                    "file": rel,
                    "sha256_local": sha(p),
                    "sha256_cloud": None,          # 本发零 lean cloud pull，无云端侧对应值
                    "bytes": p.stat().st_size,
                    "source_step": step_of(p.name),
                    "_data_source": "external_probe_NOT_FOR_ENTITY",
                })

    # A'-7：lean init 样本数据之目录级承载
    inv = QCROOT / "probe" / "env" / "data_inventory.txt"
    vendor = {"form": "目录级承载（A'-7 代定，非逐件入 manifest）",
              "target": "9.QC环境探测/qc-workspace/data/",
              "fact": "lean init 样本数据 225M／1142 件／13 资产类别（E1-22）",
              "inventory_file": str(inv.relative_to(QCROOT.parent)) if inv.exists() else None,
              "inventory_sha256": sha(inv) if inv.exists() else None,
              "inventory_bytes": inv.stat().st_size if inv.exists() else None,
              "detection": "entity/ ∪ verify/ 下零文件命中该清单内任一路径或哈希",
              "note": "本位对该子树全程零触碰、零读取内容；仅登记清单件指纹（A'-12 遗留物不清理）"}

    manifest = {
        "_schema": "P2' data_manifest v1",
        "_generated_utc": TS,
        "_clause": "85-3 D-2；A'-8 代定（须另生成 ＋ 数据类子集并入）；丙-2",
        "_selection_rule": SELECTION_RULE,
        "_crlf_note": ("E1-09／A'-16：凡经 `lean cloud pull` 落盘之件其本地哈希 ≠ 云端哈希，"
                       "须双列。**本发零 `lean cloud pull` 调用**（上云与回读一律走 file API，"
                       "实测往返逐字节保真 CR 0→0，见 FR-P2-09），故 sha256_cloud 恒为 null，"
                       "非静默省略。"),
        "_excluded_from_fingerprint_chain": [
            {"file": "config.json", "reason": "每次 pull 被 QC 注入 python-venv／encrypted 两字段（E1-11／F1-06），哈希无法进入指纹链",
             "applicable_this_shot": False, "note": "本发零 pull，该件未落盘"},
            {"file": "research.ipynb", "reason": "每次被 QC 做 JSON 压缩重序列化（E1-11／F1-10），哈希无法进入指纹链",
             "applicable_this_shot": False, "note": "云端在场但本位未落盘该件"},
        ],
        "_bing2_kd_params": {"status": "无对象",
                             "note": "丙-2 要求 kd_params 类参数件纳入生成范围。本发目标面（α＋X-1）"
                                     "输入全为人造/合成，未产生 kd_params 类件。**显式声明无对象，非静默省略。**"},
        "_vendor_data": vendor,
        "_counts": {"entries": len(entries), "total_bytes": sum(e["bytes"] for e in entries)},
        "entries": entries,
    }

    out = PROBE / "data_manifest.json"
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print("=== data_manifest.json 生成 ===")
    print("  条目数   : %d" % len(entries))
    print("  总字节   : %d" % manifest["_counts"]["total_bytes"])
    print("  vendor   : %s（清单件 sha=%s）" % (vendor["target"], (vendor["inventory_sha256"] or "N/A")[:16]))
    print("  kd_params: %s" % manifest["_bing2_kd_params"]["status"])
    print("  排除面   : %d 条（显式登记）" % len(manifest["_excluded_from_fingerprint_chain"]))
    print("  落位     : %s" % out.relative_to(WD).as_posix())


if __name__ == "__main__":
    main()

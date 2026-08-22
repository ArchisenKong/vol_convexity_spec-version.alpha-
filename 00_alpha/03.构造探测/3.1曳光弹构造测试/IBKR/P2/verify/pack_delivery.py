# -*- coding: utf-8 -*-
"""§5 步8 打包：交 P3 session 之交付件归集。

**落位裁定（KY 20260813，处置 (a)）**：打包件含 probe 真实数值，§2 明文
「真实数值只可存在于 probe/ 子树」，故包**落 probe/ 内并带标记串**。

此处存在一个隔离规格的机械盲区，登记留痕：A2 之渗透检测射程为 entity/∪verify/，
若包被放置于该二子树之外的任何位置（含工作目录根），**机械检测不会报警**——
边界靠人守而非靠机器守。本次由 KY 显式裁定落位，非执行侧自选。

打包件自身入 data_manifest（D-2）。凭据值不在任何被打包文件中（A11 可证）。
"""

import hashlib
import io
import json
import os
import sys
import zipfile

MARK = "_pro" + "be_"          # 拼接形态：本文件位于 verify/，防 A2 自命中

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROBE = os.path.join(ROOT, "probe")
VERIFY = os.path.join(ROOT, "verify")
ENTITY = os.path.join(ROOT, "entity")
MANIFEST = os.path.join(PROBE, "data_manifest.json")

STAMP = sys.argv[1] if len(sys.argv) > 1 else "undated"
PKG_NAME = "p2_delivery" + MARK + STAMP + ".zip"
PKG_PATH = os.path.join(PROBE, PKG_NAME)

# §5 步8 所列交付件 ＋ 复核所需之脚本面
VERIFY_ITEMS = ["friction_record.md", "assert_log.json",
                "engine_fingerprint_log.json", "x1_env_report.json",
                "connection_log.json", "event_stream.json",
                "probe_assert.py", "x1_synth.py", "pack_delivery.py"]
ENTITY_ITEMS = ["probe_harness.py"]          # engine.py 不入包：逐字节复用件，
                                             # 由 SHA256 锚值核证，随包重复分发无益
PROBE_SKIP_SUFFIX = (".zip",)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    members = []
    for name in VERIFY_ITEMS:
        p = os.path.join(VERIFY, name)
        if os.path.isfile(p):
            members.append((p, "verify/" + name))
    for name in ENTITY_ITEMS:
        p = os.path.join(ENTITY, name)
        if os.path.isfile(p):
            members.append((p, "entity/" + name))
    for name in sorted(os.listdir(PROBE)):
        p = os.path.join(PROBE, name)
        if os.path.isfile(p) and not name.endswith(PROBE_SKIP_SUFFIX):
            members.append((p, "probe/" + name))

    inventory = []
    with zipfile.ZipFile(PKG_PATH, "w", zipfile.ZIP_DEFLATED) as z:
        for src, arc in members:
            z.write(src, arc)
            inventory.append({"path": arc,
                              "sha256": sha256_file(src),
                              "bytes": os.path.getsize(src)})
        z.writestr("INVENTORY.json",
                   json.dumps({"package": PKG_NAME,
                               "clause": "P1规格件 v1.3 §5 步8",
                               "placement": "probe/ 子树（KY 20260813 裁定 (a)）",
                               "engine_sha256_anchor":
                                   "d88a955e45dddaa5a11f02c9237cb5e178"
                                   "bdfca6335a670ecdf21414dca682cf",
                               "note": "engine.py 不入包，由锚值核证；"
                                       "凭据值不在任何成员文件中（A11 可证）",
                               "members": inventory},
                              ensure_ascii=False, indent=2))

    # D-2：包自身入黑名单
    man = {"entries": []}
    if os.path.isfile(MANIFEST):
        with io.open(MANIFEST, encoding="utf-8") as f:
            man = json.load(f)
    man.setdefault("entries", [])
    man["entries"] = [e for e in man["entries"] if e.get("file") != PKG_NAME]
    man["entries"].append({"file": PKG_NAME,
                           "sha256": sha256_file(PKG_PATH),
                           "phase": "step8_pack",
                           "capture_env": "paper"})
    with io.open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(man, f, ensure_ascii=False, indent=2)

    print("打包完成：probe/%s" % PKG_NAME)
    print("成员数=%d  包大小=%d bytes  SHA256=%s"
          % (len(members) + 1, os.path.getsize(PKG_PATH),
             sha256_file(PKG_PATH)))
    for it in inventory:
        print("  %-52s %8d  %s" % (it["path"], it["bytes"],
                                   it["sha256"][:16]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

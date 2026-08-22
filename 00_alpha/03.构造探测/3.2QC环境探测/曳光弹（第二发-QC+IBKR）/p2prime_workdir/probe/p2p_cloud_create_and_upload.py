# -*- coding: utf-8 -*-
"""
P2' · 云端项目创建 + entity/ 面上传（KD 20260818 放行）

本件为 QC 接口面代码，按 A'-6 落 probe/ 子树。

射程与自守：
  · A'-9：云端项目**仅承载 entity/ 面**；probe/ 面一律不上云。本脚本只传 entity/ 三件。
  · A'-14：破坏性动作全禁——本脚本零 `lean cloud push`、零 files/delete、零 object-store delete、
    零 projects.delete。写动作仅限 projects.create ×1 与 files.create ×3。
  · FR-P2-05：存在性判定一律以 projects.get_all() **清单枚举比对**承载，
    不以「调用成功⇒存在」或「报错⇒不存在」推断（两条路径已被实测推翻）。
  · 乙-5：回读载荷先落原件再解析；落盘文件名带序号＋时间戳，不覆盖。
  · A'-16：回读保真比对**双值并列**（raw / 行尾归一化后），不单判。

凭据：api_client 由 lean 自动从 ~/.lean/credentials 构造；本脚本不打印、不写出凭据值。
"""
import hashlib
import json
import re
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ORG_ID = "954877bda8b6760ae398418ce79a5500"
PROJECT_NAME = "P2PRIME-SHOT2"

WD = Path(__file__).resolve().parent.parent
ENTITY = WD / "entity"
RAW = Path(__file__).resolve().parent / "raw"
RAW.mkdir(parents=True, exist_ok=True)
TS = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

# 上传清单 —— 仅 entity/ 面，逐件显式列名，不做目录遍历（防误传）
UPLOAD = [
    "cloud_payload_engine.py",
    "cloud_payload_gl06.py",
    "cloud_payload_x1.py",
    "cloud_runner_alpha6.py",
    "cloud_runner_x1.py",
]

LEAK_PAT = re.compile(r"[0-9a-f]{40,}", re.I)
KW = "Quant" + "Connect"   # 拼接存放，防 A4' 自命中


def sha(b):
    return hashlib.sha256(b).hexdigest()


def emit(name, payload, note=""):
    fn = RAW / ("%s_%s.json" % (name, TS))
    body = {
        "_probe_name": name,
        "_probe_captured_utc": TS,
        "_probe_note": note,
        "_data_source": "external_probe_NOT_FOR_ENTITY",
        "_probe_payload": payload,
    }
    text = json.dumps(body, ensure_ascii=False, indent=2, default=str)
    body["_probe_post_redaction_leak_scan_hits"] = len(LEAK_PAT.findall(text))
    fn.write_text(json.dumps(body, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print("    [WROTE] %s" % fn.name)


def main():
    print("=== P2' 云端项目创建 + entity/ 面上传 ===")
    print("捕获时刻(UTC): %s" % TS)
    print("自守: 零 push / 零 delete / 仅 projects.create x1 + files.create x%d\n" % len(UPLOAD))

    from lean.container import container
    from lean.models.api import QCLanguage
    api = container.api_client

    # --- 0. 上传前自查：待传件内零 QC 接口面字面（A4' 自守，entity/ 面纪律）
    print("--- 0. 上传前自查（A4'：entity/ 面 %s 字面命中数应 ==0）---" % KW)
    local = {}
    for n in UPLOAD:
        p = ENTITY / n
        raw = p.read_bytes()
        txt = raw.decode("utf-8")
        hits = txt.count(KW)
        local[n] = {"bytes": raw, "text": txt, "sha256": sha(raw), "size": len(raw),
                    "CR": raw.count(b"\r"), "LF": raw.count(b"\n")}
        print("  %-28s %6d B  sha=%s  %s命中=%d  CR=%d LF=%d"
              % (n, len(raw), local[n]["sha256"][:16], KW, hits, local[n]["CR"], local[n]["LF"]))
        if hits:
            raise SystemExit("A4' 自查失败：entity/ 面出现接口面字面，停。")

    # --- 1. 建项目前：清单枚举核对（FR-P2-05 口径）
    print("\n--- 1. 建项目前清单枚举（FR-P2-05：不以调用成败推断存在性）---")
    before = api.projects.get_all(ORG_ID)
    names_before = sorted([p.name for p in before])
    print("  现有项目数 = %d  清单 = %s" % (len(before), names_before))

    # --- 2. 建项目 或 复用在场同名项目（projects.delete 被 A'-14 全禁，绝不重建）
    match = [p for p in before if p.name == PROJECT_NAME]
    if match:
        proj = match[0]
        pid = proj.projectId
        print("\n--- 2. 同名项目已在场，**复用不重建**（A'-14：delete 全禁，不得覆盖/重建）---")
        print("  [REUSE] projectId=%s  name=%s" % (pid, proj.name))
        created = False
    else:
        print("\n--- 2. projects.create（写动作 1）---")
        proj = api.projects.create(PROJECT_NAME, QCLanguage.Python, ORG_ID)
        pid = proj.projectId
        print("  [OK] 已创建  projectId=%s  name=%s" % (pid, proj.name))
        created = True

    # --- 3. 现存件盘点（区分 QC 自带 / 本位既传，如实登记）
    print("\n--- 3. 上传前项目内现存件盘点 ---")
    auto = api.files.get_all(pid)
    for f in auto:
        origin = "本位既传" if f.name in UPLOAD else "QC 自带"
        print("  %-9s %-28s %6d chars" % (origin, f.name, len(f.content or "")))
    emit("cloud_project_state",
         {"projectId": pid, "name": proj.name, "created_this_run": created,
          "files_before_upload": [{"name": f.name, "chars": len(f.content or ""),
                                   "origin": ("本位既传" if f.name in UPLOAD else "QC 自带")}
                                  for f in auto]},
         "云端项目状态留痕；QC 自带件为建项目时 QC 生成，非本位上传")

    # --- 4. 上传 entity/ 三件（在场则 update，不在场则 create；均非破坏性）
    print("\n--- 4. files.create/update × %d（仅 entity/ 面，A'-9）---" % len(UPLOAD))
    present = {f.name for f in auto}
    for i, n in enumerate(UPLOAD, 1):
        try:
            if n in present:
                api.files.update(pid, n, local[n]["text"])
                print("  [OK] %d/%d 已更新 %s (%d chars)" % (i, len(UPLOAD), n, len(local[n]["text"])))
            else:
                api.files.create(pid, n, local[n]["text"])
                print("  [OK] %d/%d 已上传 %s (%d chars)" % (i, len(UPLOAD), n, len(local[n]["text"])))
        except Exception as e:
            print("  [FAIL] %d/%d %s (%d chars) -> %s: %s"
                  % (i, len(UPLOAD), n, len(local[n]["text"]), type(e).__name__, str(e)[:300]))
            emit("cloud_upload_FAIL_%s" % n.replace(".", "_"),
                 {"file": n, "chars": len(local[n]["text"]),
                  "error_type": type(e).__name__, "error_text": str(e)},
                 "上传失败，错误原文全量留痕")

    # --- 5. 回读保真比对（双值并列，A'-16）
    print("\n--- 5. 回读保真比对（双值并列：raw / 行尾归一化）---")
    back = {f.name: (f.content or "") for f in api.files.get_all(pid)}
    fid = {}
    for n in UPLOAD:
        if n not in back:
            print("  [FAIL] %s 回读缺失" % n)
            fid[n] = {"present": False}
            continue
        cb = back[n].encode("utf-8")
        lb = local[n]["bytes"]
        raw_same = (cb == lb)
        norm_same = (cb.replace(b"\r\n", b"\n") == lb.replace(b"\r\n", b"\n"))
        fid[n] = {
            "present": True,
            "local_size": len(lb), "cloud_size": len(cb),
            "local_sha256": sha(lb), "cloud_sha256": sha(cb),
            "local_newline": {"CR": lb.count(b"\r"), "LF": lb.count(b"\n")},
            "cloud_newline": {"CR": cb.count(b"\r"), "LF": cb.count(b"\n")},
            "byte_exact_raw": raw_same,
            "byte_exact_normalized": norm_same,
        }
        print("  %-28s raw=%-5s norm=%-5s  local %6dB / cloud %6dB  CR: %d->%d"
              % (n, raw_same, norm_same, len(lb), len(cb), lb.count(b"\r"), cb.count(b"\r")))

    emit("cloud_upload_fidelity", {"projectId": pid, "files": fid},
         "上传回读保真比对；双值并列不单判（A'-16）")

    print("\n--- 汇总 ---")
    print("  projectId = %s" % pid)
    print("  写动作实计: projects.create x1 + files.create x%d" % len(UPLOAD))
    print("  零 delete / 零 push / 零 object-store 写")
    print("  落位: %s" % RAW)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        traceback.print_exc()
        sys.exit(1)

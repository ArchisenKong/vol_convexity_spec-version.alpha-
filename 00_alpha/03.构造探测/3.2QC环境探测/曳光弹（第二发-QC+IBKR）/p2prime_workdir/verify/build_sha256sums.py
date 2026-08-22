# -*- coding: utf-8 -*-
"""
P2' · 交付树全量指纹清单 `verify/SHA256SUMS`（形态照探测期 probe/SHA256SUMS）

自排除（显式、非空、射程仅限自指件）：
    SHA256SUMS 自身／assert_log.{json,txt}／seal_check.log
    ——三者均于本件生成**之后**再变动（断言须末次执行，丙-3），自指必不自洽。
`__pycache__` 排除（BASIS['pycache']，house 先例 GL-06 F-7）。
零网络。
"""
import hashlib
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

WD = Path(__file__).resolve().parent.parent
OUT = WD / "verify" / "SHA256SUMS"
SELF_EXCLUDE = {"SHA256SUMS", "assert_log.json", "assert_log.txt", "seal_check.log"}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


rows, total = [], 0
for p in sorted(WD.rglob("*")):
    if not p.is_file() or "__pycache__" in p.parts or p.name in SELF_EXCLUDE:
        continue
    rows.append("%s *%s" % (sha(p), p.relative_to(WD).as_posix()))
    total += p.stat().st_size

head = [
    "# P2' 交付树全量指纹清单（SHA256）",
    "# 自排除（射程仅限自指件，非空指声明）: %s" % " ".join(sorted(SELF_EXCLUDE)),
    "#   理由: 四者均于本件生成后再变动（断言须末次执行，丙-3），自指必不自洽。",
    "# 排除 __pycache__（BASIS['pycache']；house 先例 GL-06 切片记录 F-7）",
    "# 条目 %d 件 / %d 字节" % (len(rows), total),
]
OUT.write_text("\n".join(head + rows) + "\n", encoding="utf-8", newline="\n")
print("SHA256SUMS: %d 条 / %d 字节 -> %s" % (len(rows), total, OUT.relative_to(WD).as_posix()))

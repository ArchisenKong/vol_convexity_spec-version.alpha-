# -*- coding: utf-8 -*-
"""
P2' · 封包前置机械检查（丙-3）

丙-3 条款：「交付件任何修改后复跑断言，末次全 PASS 为封包前置。」
作业指令 §5-5 加严：「末次**零 FAIL** 且全部 `INDETERMINATE` 项已双值留痕，方可封包。」

机械检测位：
  ① 断言日志末次结果 FAIL == 0；
  ② 全部 INDETERMINATE 项均有双值留痕（本发该态无对象，计数须为 0 或逐项双值在场）；
  ③ 断言日志之 mtime **晚于**交付树内任一文件之 mtime（除断言日志自身）。
本件只判前置是否满足；**不执行打包、不执行外发**（乙-6：落位须 KD／KY 显式裁定）。
零网络。
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

WD = Path(__file__).resolve().parent.parent
LOG = WD / "verify" / "assert_log.json"
SELF = {LOG.name, "assert_log.txt", "seal_check.py", "seal_check.log"}

print("=" * 78)
print("P2' 封包前置机械检查（丙-3 ＋ 作业指令 §5-5）")
print("=" * 78)

ok = True

# ① 零 FAIL
if not LOG.exists():
    print("  [FAIL] ① 断言日志不在场")
    sys.exit(1)
d = json.loads(LOG.read_text(encoding="utf-8"))
s = d["summary"]
c1 = s.get("FAIL", 0) == 0
ok &= c1
print("  [%s] ① 末次断言 FAIL == 0   （PASS=%d FAIL=%d INDETERMINATE=%d，运行于 %s）"
      % ("PASS" if c1 else "FAIL", s.get("PASS", 0), s.get("FAIL", 0),
         s.get("INDETERMINATE", 0), d["_run_utc"]))

# ② INDETERMINATE 双值留痕
ind = [r for r in d["results"] if r["verdict"] == "INDETERMINATE"]
c2 = all(("raw=" in r["detail"] and "norm=" in r["detail"]) for r in ind)
ok &= c2
print("  [%s] ② INDETERMINATE 双值留痕   （%d 项；本发该态无对象＝零 pull，非「未记录」）"
      % ("PASS" if c2 else "FAIL", len(ind)))

# ③ 断言日志为交付树内最新
log_m = LOG.stat().st_mtime
newer = []
for p in sorted(WD.rglob("*")):
    if p.is_file() and "__pycache__" not in p.parts and p.name not in SELF:
        if p.stat().st_mtime > log_m:
            newer.append((p.relative_to(WD).as_posix(),
                          datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat()))
c3 = not newer
ok &= c3
print("  [%s] ③ 断言日志 mtime 晚于交付树内任一文件   （更新者 %d 件）"
      % ("PASS" if c3 else "FAIL", len(newer)))
for n, t in newer[:8]:
    print("        · %-52s %s" % (n, t))

print("=" * 78)
print("封包前置: %s" % ("**满足**" if ok else "**未满足**"))
print("乙-6：本件不执行打包、不执行外发；落位须 KD／KY 显式裁定。")
print("=" * 78)
sys.exit(0 if ok else 1)

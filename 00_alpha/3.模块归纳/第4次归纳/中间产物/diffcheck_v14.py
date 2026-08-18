#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""diff核证 · 模块划分 v1.3 → v1.4 candidate
交付门：清单外变更块 == 0（即：底版被替换/删除之物理行必须与变更清单一致）"""
import io, difflib, hashlib

def rd(p):
    with io.open(p, encoding='utf-8') as f: return f.read()

a = rd('base_v1_3.md').splitlines()
b = rd('模块划分_v1_4_candidate_20260817.md').splitlines()

sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
ops = [op for op in sm.get_opcodes() if op[0] != 'equal']

ins = [o for o in ops if o[0] == 'insert']
rep = [o for o in ops if o[0] == 'replace']
dele = [o for o in ops if o[0] == 'delete']

print('=== difflib 变更块统计 ===')
print('  纯插入块 insert  = %d' % len(ins))
print('  替换块   replace = %d' % len(rep))
print('  删除块   delete  = %d' % len(dele))
print('  变更块合计       = %d' % len(ops))

# 变更清单（附录D）所列之底版行级改标三处：U-1标题行／U-3 §二节名／U-14 §四节标题
ALLOWED_REPLACE = {
    '# 模块划分 · v1.3 · 20260809',                              # U-1
    '## 二、十六根观察扫描记录（证据基础层，五维度逐根，指针带节号）',   # U-3 节名改标
    '## 四、X边归属核对（v1.3扩至17/17）',                          # U-14 节标题改标
}

print('\n=== 底版被替换/删除之物理行逐行列示 ===')
touched = []
for tag, i1, i2, j1, j2 in rep + dele:
    for k in range(i1, i2):
        touched.append((tag, k + 1, a[k]))
if not touched:
    print('  （无）')
for tag, ln, txt in touched:
    mark = 'OK·清单内' if txt in ALLOWED_REPLACE else '!! 清单外'
    print('  [%s] %s 底版行%d: %s' % (tag, mark, ln, txt[:70]))

out_of_manifest = [t for t in touched if t[2] not in ALLOWED_REPLACE]
print('\n底版被替换之物理行 = %d行；被删除之物理行 = %d行' %
      (sum(i2 - i1 for _, i1, i2, _, _ in rep), sum(i2 - i1 for _, i1, i2, _, _ in dele)))
print('**清单外变更块 = %d**' % len(out_of_manifest))

# 底版逐行留存核证：除清单内替换行外，底版每一行须在产出中原样在场
missing = []
bset = {}
for line in b:
    bset[line] = bset.get(line, 0) + 1
acnt = {}
for line in a:
    acnt[line] = acnt.get(line, 0) + 1
for line, n in acnt.items():
    if line in ALLOWED_REPLACE:
        continue
    if bset.get(line, 0) < n:
        missing.append((line, n, bset.get(line, 0)))
print('\n=== 底版逐行留存核证（清单内替换行除外）===')
print('  底版唯一行数 = %d；产出中缺失或减少者 = %d' % (len(acnt), len(missing)))
for line, n, m in missing[:20]:
    print('   !! 底版%d次→产出%d次: %s' % (n, m, line[:70]))

print('\n=== 交付门 ===')
gate = (len(out_of_manifest) == 0 and len(missing) == 0 and len(dele) == 0)
print('  清单外变更块==0 ∧ 底版逐行零丢失 ∧ 零删除块 ⇒ %s' % ('PASS' if gate else 'FAIL'))

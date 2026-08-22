#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""窗3限定语传播核证（92-2／收-6）：本文档为 X20 传播链之下游。
判据：全文含「窗3／EW3／T3-24」之段落，须落于三层承接之至少一层覆盖内；裸引段须＝0。
  ①文档级总括承接（头注专段）  ②段级随行标记  ③逐处就地携带
"""
import io, sys

DOC = '模块划分_v1_4_candidate_20260817.md'
t = io.open(DOC, encoding='utf-8').read()
lines = t.split('\n')

MARK = '窗3限定语传播承接**（92-2／收-6，随行标记）'
LOCAL = ['L1限定语', '④分量消费限定语', '④消费限定语', '收-6', '92-2', '不得裸引', '限定语']
CITE = ['窗3', 'EW3', 'T3-24']

# 段落切分（空行分隔），并记录其所属之「段级标记」覆盖区间
paras, cur, start = [], [], 0
for i, l in enumerate(lines):
    if l.strip() == '':
        if cur:
            paras.append([start, i - 1, '\n'.join(cur)]); cur = []
    else:
        if not cur: start = i
        cur.append(l)
if cur: paras.append([start, len(lines) - 1, '\n'.join(cur)])

# ① 文档级总括承接在场性
head_ok = ('窗3限定语传播条款承接（92-2／收-6，显式）' in t)
print('① 文档级总括承接（头注专段）在场：%s' % ('是' if head_ok else '否'))

# ② 段级随行标记之位置与其覆盖射程（自标记起至下一 "## " 或 "### " 节标题止）
marks = [i for i, l in enumerate(lines) if MARK in l]
print('② 段级随行标记数 = %d' % len(marks))
cover = []
for m in marks:
    end = len(lines) - 1
    for j in range(m + 1, len(lines)):
        if lines[j].startswith('## ') or lines[j].startswith('### '):
            end = j - 1; break
    cover.append((m, end))
    print('   标记@行%-5d 覆盖射程 行%d–行%d' % (m + 1, m + 1, end + 1))

def covered(a, b):
    return any(m <= a and b <= e for m, e in cover)

bare = []
c3 = 0
for a, b, p in paras:
    if not any(k in p for k in CITE):
        continue
    c3 += 1
    if any(k in p for k in LOCAL):      # ③ 就地携带
        continue
    if covered(a, b):                    # ② 段级标记覆盖
        continue
    bare.append((a + 1, p[:90].replace('\n', '⏎')))

print()
print('含窗3/EW3/T3-24 之段落总数 = %d' % c3)
print('**裸引段（三层均未覆盖）= %d**' % len(bare))
for ln, txt in bare:
    print('   !! 行%d: %s' % (ln, txt))

gate = head_ok and len(bare) == 0
print()
print('=== 交付门：文档级承接在场 ∧ 裸引段==0 ⇒ %s ===' % ('PASS' if gate else 'FAIL'))
sys.exit(0 if gate else 1)

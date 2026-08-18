#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""受控替换脚本 · 模块划分 v1.3 → v1.4 candidate
每处替换均 assert s.count(old)==1；命中≠1 即中止。"""
import io, sys, hashlib

BASE = 'base_v1_3.md'
OUT  = '模块划分_v1_4_candidate_20260817.md'

def rd(p):
    with io.open(p, encoding='utf-8') as f: return f.read()

s = rd(BASE)
base_txt = s
blk = lambda n: rd(n)

ops = []   # (label, old, new)

# U-1 标题行改标 + v1.4头注
ops.append(('U-1 标题改标＋v1.4头注',
 '# 模块划分 · v1.3 · 20260809\n\n> **版本身份声明＝定案版v1.3**',
 blk('blk_head.md').rstrip('\n')))

# U-2 证据线六
ops.append(('U-2 证据线六',
 '\n\n## 二、十六根观察扫描记录',
 blk('blk_s1.md').rstrip('\n') + '\n\n## 二、十九根观察扫描记录'))

# U-3 §二扩表说明
ops.append(('U-3a §二扩表说明',
 '\n\n| 根 | 上游输入 | 下游输出 | 模块内计算 | 槽位挂载 | 规则缺口 |',
 '\n' + blk('blk_s2_note.md').rstrip('\n') + '\n\n| 根 | 上游输入 | 下游输出 | 模块内计算 | 槽位挂载 | 规则缺口 |'))

# U-3b §二表体三行（插在 GL-09 行之后、引擎行版本链注记之前）
ops.append(('U-3b §二表体三行',
 '\n\n**——v1.3｜引擎行之版本链增量注记',
 '\n' + blk('blk_s2_rows.md').rstrip('\n') + '\n\n**——v1.3｜引擎行之版本链增量注记'))

# U-4 M1
ops.append(('U-4 M1增量',
 '\n\n### M2 · 坐标化账本构造',
 '\n' + blk('blk_m1.md').rstrip('\n') + '\n\n### M2 · 坐标化账本构造'))

# U-5 M2
ops.append(('U-5 M2增量',
 '\n\n### M3 · 账本派生观察',
 '\n' + blk('blk_m2.md').rstrip('\n') + '\n\n### M3 · 账本派生观察'))

# U-6 M3
ops.append(('U-6 M3增量',
 '\n\n### M4 · 判据触发状态机',
 '\n' + blk('blk_m3.md').rstrip('\n') + '\n\n### M4 · 判据触发状态机'))

# U-7 M4
ops.append(('U-7 M4增量',
 '\n\n### M5 · 成本度量',
 '\n' + blk('blk_m4.md').rstrip('\n') + '\n\n### M5 · 成本度量'))

# U-8 M5
ops.append(('U-8 M5增量',
 '\n\n### M6 · 路径域证伪工装',
 '\n' + blk('blk_m5.md').rstrip('\n') + '\n\n### M6 · 路径域证伪工装'))

# U-9 M6
ops.append(('U-9 M6增量',
 '\n\n### M7 · 归因分解',
 '\n' + blk('blk_m6.md').rstrip('\n') + '\n\n### M7 · 归因分解'))

# U-10 M7
ops.append(('U-10 M7增量',
 '\n\n### 显式不归属三类（双向覆盖之反向面）',
 '\n' + blk('blk_m7.md').rstrip('\n') + '\n\n### 显式不归属三类（双向覆盖之反向面）'))

# U-11/U-12/U-13 不归属三类增量 ＋ §三末两段
ops.append(('U-11~13 不归属三类增量＋§三末两段',
 '\n\n## 四、X边归属核对（v1.3扩至17/17）',
 '\n' + blk('blk_nc.md').rstrip('\n') + '\n' + blk('blk_s3end.md').rstrip('\n')
 + '\n\n## 四、X边归属核对（v1.4扩至20/20）'))

# U-14a §四扩表说明
ops.append(('U-14a §四扩表说明',
 '\n\n| 边 | 归属 |\n|---|---|\n| X1／X5 |',
 '\n' + blk('blk_s4.md').rstrip('\n') + '\n\n| 边 | 归属 |\n|---|---|\n| X1／X5 |'))

# U-14b §四表体三行
ops.append(('U-14b §四表体三行',
 '\n\n## 五、pipeline拓扑',
 '\n' + blk('blk_s4rows.md').rstrip('\n') + '\n\n## 五、pipeline拓扑'))

# U-15 §五
ops.append(('U-15 §五注记',
 '\n\n## 六、贯通面断点观察',
 '\n' + blk('blk_s5.md').rstrip('\n') + '\n\n## 六、贯通面断点观察'))

# U-16 §六
ops.append(('U-16 §六断点',
 '\n\n## 七、§6既定检验项',
 '\n' + blk('blk_s6.md').rstrip('\n') + '\n\n## 七、§6既定检验项'))

# U-17 §七
ops.append(('U-17 §七',
 '\n\n## 八、观察清单五维度覆盖自陈',
 '\n' + blk('blk_s7.md').rstrip('\n') + '\n\n## 八、观察清单五维度覆盖自陈'))

# U-18 §八
ops.append(('U-18 §八',
 '\n\n## 九、过程合格判据自查',
 '\n' + blk('blk_s8.md').rstrip('\n') + '\n\n## 九、过程合格判据自查'))

# U-19 §九
ops.append(('U-19 §九自查',
 '\n\n## 附录A · 要件枚举表',
 '\n' + blk('blk_s9.md').rstrip('\n') + '\n\n## 附录A · 要件枚举表'))

for label, old, new in ops:
    c = s.count(old)
    if c != 1:
        sys.exit('!! 中止：%s 命中数=%d（要求==1）' % (label, c))
    s = s.replace(old, new)
    print('[ok] %-34s count==1' % label)

# U-20/U-21 附录A续三 ＋ 附录D（文末追加）
s = s.rstrip('\n') + '\n' + blk('blk_apxA3.md').rstrip('\n') + '\n' + blk('blk_apxD.md').rstrip('\n') + '\n'
print('[ok] %-34s append' % 'U-20/U-21 附录A续三＋附录D')

with io.open(OUT, 'w', encoding='utf-8') as f:
    f.write(s)

b = s.encode('utf-8')
print('\n产出：%s' % OUT)
print('  bytes  = %d' % len(b))
print('  md5    = %s' % hashlib.md5(b).hexdigest())
print('  sha256 = %s' % hashlib.sha256(b).hexdigest())
print('  物理行 = %d' % (s.count('\n')+1))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§7A 程序化自检三条（归纳程序纪律 v1.6 §7A；80-10∪81-10 射程含模块文档）
① 矩阵/表计数三位一致断言   ② 段级去重扫描   ③ 扩表说明物理行口径
对象＝《模块划分_v1_4_candidate_20260817.md》
"""
import io, re, hashlib, sys, unicodedata

DOC = '模块划分_v1_4_candidate_20260817.md'
with io.open(DOC, encoding='utf-8') as f:
    txt = f.read()
lines = txt.split('\n')
fail = []

print('=' * 72)
print('§7A-① 计数三位一致断言（声明N ＝ member枚举 ＝ 正文实际行数）')
print('=' * 72)

def table_rows(start_marker, stop_marker):
    """返回 start_marker 之后、stop_marker 之前的表体物理行（|开头，排除表头与分隔行）"""
    i = txt.index(start_marker)
    j = txt.index(stop_marker, i)
    seg = txt[i:j].split('\n')
    body, seen_header = [], False
    for ln in seg:
        s = ln.strip()
        if not s.startswith('|'):
            continue
        if re.fullmatch(r'\|[\s\-:|]+\|', s):
            seen_header = True
            continue
        if not seen_header:
            continue          # 表头行
        body.append(s)
    return body

checks = []

# (1) §二 观察扫描表：声明「十九根」 vs 表体物理行
s2 = table_rows('## 二、十九根观察扫描记录', '**——v1.3｜引擎行之版本链增量注记')
checks.append(('§二观察扫描表 根数', 19, len(s2), '节名"十九根"＋头注"根数基数19"'))

# (2) §四 X边表：声明 20/20 ＝ **边数**（非物理行数——一行可载多边，如「X1／X5」「X3／X4／X8」；
#     物理行口径另由 §7A-③ 断言。此两口径之分离承 v1.3「物理行口径〔43 D-4同型〕」之明文）
s4 = table_rows('## 四、X边归属核对（v1.4扩至20/20）', '## 五、pipeline拓扑')
s4_edges = sorted({int(m) for row in s4 for m in re.findall(r'X(\d+)', row.split('|')[1])})
checks.append(('§四X边表 边数（去重）', 20, len(s4_edges), '节标题"扩至20/20"（边数口径）'))
checks.append(('§四X边表 物理行', 17, len(s4), '扩表说明"前十四行逐字承接＋新增三行"'))

# (3) 附录A续三 三窗要件表：声明 45 vs 三表体物理行合计
a3_w1 = table_rows('**五·窗1 动作生命周期状态机（17项）', '**五·窗2 roll事件记录schema（13项）')
a3_w2 = table_rows('**五·窗2 roll事件记录schema（13项）', '**五·窗3 T3-24六问验收状态量（15项）')
a3_w3 = table_rows('**五·窗3 T3-24六问验收状态量（15项）', '**覆盖自陈（构造者自陈，非合格判定）**：第五批45项')
checks.append(('附录A续三 窗1要件', 17, len(a3_w1), '表头"（17项）"'))
checks.append(('附录A续三 窗2要件', 13, len(a3_w2), '表头"（13项）"'))
checks.append(('附录A续三 窗3要件', 15, len(a3_w3), '表头"（15项）"'))
checks.append(('附录A续三 合计', 45, len(a3_w1) + len(a3_w2) + len(a3_w3), '"第五批45项"＋骨架v3.2矩阵45行'))

# (4) §九 B检处置表：声明 12 条 vs 表体物理行
b = table_rows('| # | v1.3自带条款 | 出处 | 本轮触发态 | 处置（四选一） |', '  **覆盖自陈**：12条')
checks.append(('§九〔B检〕处置表', 12, len(b), '自查第12条"命中条款12条"＋第13条覆盖自陈"12条"'))

# (5) 判断位编号连续性 INDM-24..35 ＝ 12 枚
found = sorted({int(m) for m in re.findall(r'INDM-(\d{2})', txt) if int(m) >= 24})
checks.append(('判断位枚数 INDM-24..', 12, len(found), '头注"INDM-24~INDM-35逐项呈KD"'))

for name, declared, actual, src in checks:
    ok = (declared == actual)
    print('  [%s] %-26s 声明=%-4d 实测=%-4d   源＝%s' %
          ('ok' if ok else '!!', name, declared, actual, src))
    if not ok:
        fail.append('①%s 声明%d≠实测%d' % (name, declared, actual))
print('  §四边号实测：X%s' % (', X'.join('%d'%x for x in s4_edges)))
print('  判断位实测编号：%s' % ('INDM-' + ', INDM-'.join('%d' % x for x in found)))
if found != list(range(24, 24 + len(found))):
    fail.append('①判断位编号不连续：%s' % found)
    print('  [!!] 编号不连续')
else:
    print('  [ok] 编号连续无跳号')

print()
print('=' * 72)
print('§7A-② 段级去重扫描（规范化后段落指纹）')
print('=' * 72)
paras, cur = [], []
for ln in lines:
    if ln.strip() == '':
        if cur:
            paras.append('\n'.join(cur)); cur = []
    else:
        cur.append(ln)
if cur:
    paras.append('\n'.join(cur))

def norm(p):
    p = unicodedata.normalize('NFKC', p)
    p = re.sub(r'[\s\*`>|:\-—－·・]+', '', p)
    return p

# 去重排除面（显式声明，窗2 `_sweep_exclusions` 先例；空白≠不适用）：
#   E-1 窗3限定语传播承接之**段级随行标记**——按 92-2／收-6 之传播义务须逐段随行，
#       其逐字同一为**义务所要求之刻意重复**，非冗余；如实列示为排除项而非静默剔除。
EXCLUDE_MARK = '窗3限定语传播承接**（92-2／收-6，随行标记）'
excluded = 0
seen, dup = {}, []
for idx, p in enumerate(paras):
    n = norm(p)
    if '窗3限定语传播承接' in p:
        excluded += 1
        continue
    if len(n) < 40:          # 短段（表头/分隔/单句标记）不入去重面
        continue
    h = hashlib.md5(n.encode('utf-8')).hexdigest()
    if h in seen:
        dup.append((seen[h], idx, p[:60]))
    else:
        seen[h] = idx
print('  段落总数 = %d；入去重面段落 = %d；**声明排除项 E-1（窗3限定语段级随行标记）= %d 段**' %
      (len(paras), len(seen) + len(dup), excluded))
print('  排除理由：92-2／收-6 传播义务要求逐段随行，逐字同一系义务所要求之刻意重复，如实列示非静默剔除')
if dup:
    print('  [!!] 重复命中 %d 处：' % len(dup))
    for a, bb, t in dup:
        print('       段%d ≡ 段%d ： %s' % (a, bb, t))
    fail.append('②段级重复 %d 处' % len(dup))
else:
    print('  [ok] 重复命中 0 处')

print()
print('=' * 72)
print('§7A-③ 扩表说明物理行口径（禁语义行估计）')
print('=' * 72)
# v1.4扩表说明所载：§二"前十六行逐字承自v1.3"；§四"前十四行逐字承自v1.3"
base_s2 = table_rows.__doc__ and None
with io.open('base_v1_3.md', encoding='utf-8') as f:
    btxt = f.read()

def table_rows_txt(t, start_marker, stop_marker):
    i = t.index(start_marker); j = t.index(stop_marker, i)
    seg = t[i:j].split('\n'); body, seen_h = [], False
    for ln in seg:
        s = ln.strip()
        if not s.startswith('|'): continue
        if re.fullmatch(r'\|[\s\-:|]+\|', s): seen_h = True; continue
        if not seen_h: continue
        body.append(s)
    return body

b_s2 = table_rows_txt(btxt, '## 二、十六根观察扫描记录', '**——v1.3｜引擎行之版本链增量注记')
b_s4 = table_rows_txt(btxt, '## 四、X边归属核对（v1.3扩至17/17）', '## 五、pipeline拓扑')
for name, declared, actual in [('§二 底版表体物理行（声明"前十六行"）', 16, len(b_s2)),
                               ('§四 底版表体物理行（声明"前十四行"）', 14, len(b_s4)),
                               ('§二 新增行（声明"新增三行"）', 3, len(s2) - len(b_s2)),
                               ('§四 新增行（声明"新增三行"）', 3, len(s4) - len(b_s4))]:
    ok = declared == actual
    print('  [%s] %-34s 声明=%-3d 实测=%-3d' % ('ok' if ok else '!!', name, declared, actual))
    if not ok:
        fail.append('③%s 声明%d≠实测%d' % (name, declared, actual))

print()
print('=' * 72)
print('§7A 总结：%s' % ('三条全过（PASS）' if not fail else '不合 %d 处（FAIL）' % len(fail)))
for f_ in fail:
    print('   !! ' + f_)
print('=' * 72)
sys.exit(1 if fail else 0)

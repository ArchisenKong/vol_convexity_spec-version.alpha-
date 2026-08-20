#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G13_deferral_check.py · v1.3 · 20260813（裁决88：DEFER_HEADS增外审报告标题锚形态〔遗留/负空间/未核〕＋扫描glob扩外审报告文件族；裁决86块D登记素材兑现。验收＝对既有落地文档全量回归零翻转；外审报告语料验证挂第五批首次实用留痕）
G-13 递延项双向对表脚本（射程扩定案版，Q-7/Q-11 经 82-1；55-5a 脚本化）。
射程＝落地文档全部递延形态：①「落地去向清单」类段落 ②「显式后置/续记」段 ③「下游动作序」排程项。
对表面＝待修登记/治理缺口登记之条目ID全集（DOC-/W-/G-/GAP-/REG-UP-/TPL/AB- 系）。
输出＝逐落地文档递延指针清单 + 台账命中状态；「无台账挂靠且无兑现点」者列为落空候选呈KD。
用法: python3 G13_deferral_check.py <落地文档目录> <待修登记.md> <治理缺口登记.md> [升格候选登记册.md]
"""
import re, sys, glob, os

ID_PAT = re.compile(r'(?<![A-Za-z0-9-])(?:DOC-\d+|W-\d+|G-\d+\b|GAP-\d+|REG-UP-\d+|TPL[0-9A-Za-z]*-[A-Za-z0-9]+-\d+|AB-\d+|T-\d{2,}|T3-\d+|GL-\d+|GK-\d+|TC-\d+|S6-\d+|WL-\d+|FW-\d+-[甲乙])')  # v1.1扩：实体ID族（72§5假通过检出后订正）
# 递延段落识别锚（段标题级，宽匹配）
DEFER_HEADS = ['落地去向', '递延项', '显式后置', '续记', '下游动作序', '后置池', '排程', '遗留', '负空间', '未核']  # v1.3扩：外审报告标题锚形态（裁决86块D素材）

def ledger_ids(paths):
    ids=set()
    for p in paths:
        if p and os.path.exists(p):
            ids |= set(ID_PAT.findall(open(p,encoding='utf-8').read()))
    return ids

def defer_blocks(text):
    """切出递延形态段落：命中 DEFER_HEADS 的标题行起，至下一同级标题止。"""
    lines=text.split('\n'); blocks=[]; cur=None
    for ln in lines:
        is_head = ln.strip().startswith('#') or ln.strip().startswith('**')
        if is_head and any(k in ln for k in DEFER_HEADS):
            if cur: blocks.append(cur)
            cur=[ln]; continue
        if cur is not None:
            if ln.strip().startswith('## ') and not any(k in ln for k in DEFER_HEADS):
                blocks.append(cur); cur=None
            else: cur.append(ln)
    if cur: blocks.append(cur)
    return ['\n'.join(b) for b in blocks]

def main():
    doc_dir, ledgers = sys.argv[1], sys.argv[2:]
    lids = ledger_ids(ledgers)
    total_docs=0; findings=[]; miss=[]
    for f in sorted(glob.glob(os.path.join(doc_dir,'裁决*落地文档*.md')) + glob.glob(os.path.join(doc_dir,'*外审报告*.md'))):  # v1.3扩：外审报告族入射程
        total_docs+=1
        t=open(f,encoding='utf-8').read()
        blks=defer_blocks(t)
        ids=set()
        for b in blks: ids |= set(ID_PAT.findall(b))
        for i in sorted(ids):
            hit = i in lids
            findings.append((os.path.basename(f), i, hit))
            if not hit: miss.append((os.path.basename(f), i))
    print(f"[G13] 落地文档数={total_docs} 递延指针数={len(findings)} 台账命中={sum(1 for *_,h in findings if h)} 未命中={len(miss)}")
    for f,i in miss: print(f"  [落空候选] {f} :: {i}")
    if not miss: print("[G13] 零新增落空 · PASS")
    return 0 if not miss else 1

if __name__=='__main__': sys.exit(main())

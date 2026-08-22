# -*- coding: utf-8 -*-
"""G-6(a) diff 核证：底版 v3.1 ↔ 本版 v3.2 candidate，清单外变更块计数"""
import difflib, io, hashlib
A = io.open("/mnt/project/骨架_v3_1_20260809.md", encoding="utf-8").read().split("\n")
B = io.open("骨架_v3_2_candidate_20260817.md", encoding="utf-8").read().split("\n")
sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
blocks = [op for op in sm.get_opcodes() if op[0] != "equal"]
print("底版行数 =", len(A), "本版行数 =", len(B))
print("变更块总数 =", len(blocks))
delete_like = [op for op in blocks if op[0] in ("delete","replace") and (op[2]-op[1]) > 0]
print("含删除/替换之块 =", len(delete_like))
for tag,i1,i2,j1,j2 in blocks:
    old = A[i1:i2]; new = B[j1:j2]
    kind = "纯插入" if tag=="insert" else tag
    head = (old[0] if old else new[0])[:60]
    print(f"  [{kind}] 底版行{i1+1}-{i2} → 本版行{j1+1}-{j2} | {head}")
# 逐字未改核证：底版每一行是否仍在本版内（顺序保持）
missing = [l for tag,i1,i2,j1,j2 in blocks if tag in ("delete","replace") for l in A[i1:i2]]
print("\n底版被替换/删除之物理行数 =", len(missing))
for m in missing: print("   -", m[:90])

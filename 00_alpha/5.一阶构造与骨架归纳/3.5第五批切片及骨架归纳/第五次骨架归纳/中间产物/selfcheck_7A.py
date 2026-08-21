# -*- coding: utf-8 -*-
"""§7A 程序化自检三条（程序纪律 v1.6 §7A）— 骨架 v3.2 candidate"""
import io, re, hashlib, sys
P = "骨架_v3_2_candidate_20260817.md"
lines = io.open(P, encoding="utf-8").read().split("\n")
fail = []

# ---- ①-a 第五批矩阵物理表行数 ----
start = next(i for i,l in enumerate(lines) if l.startswith("### 第五批（45要件"))
end   = next(i for i,l in enumerate(lines) if l.startswith("**双向覆盖自查"))
rows = [l for l in lines[start:end] if l.startswith("| EW")]
print(f"[1a] 第五批矩阵物理表行数实测 = {len(rows)} ; 声明 = 45")
if len(rows) != 45: fail.append("1a")

# ---- ①-b 累计要件三位一致 ----
batches = {"首批":20, "第二批":21, "第三批":40, "第四批":45, "第五批":len(rows)}
total = sum(batches.values())
print(f"[1b] 累计要件 = {'+'.join(str(v) for v in batches.values())} = {total} ; 正文声明 = 171")
if total != 171: fail.append("1b")

# ---- ①-c 区四边行数 ----
xrows = [l for l in lines if re.match(r"^\| \*{0,2}X\d+ ", l)]
print(f"[1c] 区四边行数实测 = {len(xrows)} ; 声明 = 20")
if len(xrows) != 20: fail.append("1c")

# ---- ①-d 条目标题 n/19 分母一致性 ----
heads = [l for l in lines if re.match(r"^### [ABC]\d+ ", l)]
bad = [h[:40] for h in heads if "/16" in h.split("〔第五轮")[0].split("〔第四轮")[0]]
den = re.findall(r"(\d+)/19", "\n".join(heads))
print(f"[1d] 条目标题数 = {len(heads)} ; 含 n/19 比值出现次数 = {len(den)} ; 首段仍含 /16 之标题 = {len(bad)}")
if bad: fail.append("1d")

# ---- ② 段级去重扫描 ----
paras, cur = [], []
for l in lines:
    if l.strip() == "":
        if cur: paras.append("\n".join(cur)); cur = []
    else:
        cur.append(l)
if cur: paras.append("\n".join(cur))
def norm(p):
    p = re.sub(r"\s+", "", p)
    return p
seen, dup = {}, []
for i,p in enumerate(paras):
    n = norm(p)
    if len(n) < 60:      # 排除分隔符/表头/短行
        continue
    h = hashlib.sha256(n.encode()).hexdigest()
    if h in seen: dup.append((seen[h], i, p[:70]))
    else: seen[h] = i
print(f"[2 ] 段落总数 = {len(paras)} ; 参与去重段数 = {len(seen)+len(dup)} ; 重复段命中 = {len(dup)}")
for d in dup: print("      重复:", d)
if dup: fail.append("2")

# ---- ③ 三分表成分数实测 ----
import os
src = "/mnt/project"
tri = {
 "窗1": ("一阶实体_五窗1_动作生命周期状态机_input_schema_v1_2_20260814.md", r"^\| C-\d+ \|", 15),
 "窗2": ("一阶实体_五窗2_roll事件记录_input_schema_v1_1_20260815.md", r"^\| C-\d+ ", 7),
 "窗3": ("一阶实体_五窗3_T3-24六问验收状态量_input_schema_v1_1_20260816.md", r"^\| C-\d+ ", 14),
}
for k,(f,pat,decl) in tri.items():
    t = io.open(os.path.join(src,f), encoding="utf-8").read().split("\n")
    c = len([l for l in t if re.match(pat, l)])
    print(f"[3 ] {k} 三分表成分行实测 = {c} ; 骨架声明 = {decl}")
    if c != decl: fail.append("3-"+k)

print("\n=== §7A 结果：", "全过" if not fail else f"不合 {fail} —— 依 §7A 须停下呈报", "===")
sys.exit(1 if fail else 0)

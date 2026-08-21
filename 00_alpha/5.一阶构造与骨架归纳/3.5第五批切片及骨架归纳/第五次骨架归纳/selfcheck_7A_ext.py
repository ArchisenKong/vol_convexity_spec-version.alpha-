# -*- coding: utf-8 -*-
"""§7A 程序化自检（扩面版，裁决94-3(c)）— 骨架 v3.2 定案版
①-扩 分子—成员枚举逐员闭合核算：全部30条目，恒满条目亦全员枚举，不以 n＝M 承载
①-a/b/c 矩阵与边计数三位一致
② 段级去重扫描
③ 扩表说明物理行口径
"""
import io, re, hashlib, sys, os

P = "骨架_v3_2_20260817.md"
txt = io.open(P, encoding="utf-8").read()
lines = txt.split("\n")
fail = []

R19 = ["T-76","TC-33","T3-03","GK-14","T-24",          # 首批5
       "T3-17","T3-18","T-33","GK-31",                  # 第二批4
       "引擎","T3-22","FW-03-甲","GL-06",               # 第三批4（引擎＝TPL1-T76-01，80-1单根口径）
       "T3-15","T3-16","GL-09",                         # 第四批3（引擎为版本链，不另计根）
       "窗1","窗2","窗3"]                                # 第五批3
assert len(R19)==19 and len(set(R19))==19

ALL = list(R19)
B1_4 = ["T-76","TC-33","T3-03","GK-14","T-24","T3-17","T3-18","T-33","GK-31",
        "引擎","T3-22","FW-03-甲","GL-06","T3-15","T3-16","GL-09"]
W3 = ["窗1","窗2","窗3"]

# 条目 → (声明分子, 标题内须在场之串, 成员枚举)
M = {
 "A1":  (9,  "共·**9/19根**",  ["T-76","T3-03","GK-14","T3-17","T-33","GK-31","T3-22","FW-03-甲","窗1"]),
 "A2":  (13, "共·**13/19根**", ["T-76","TC-33","T3-03","GK-14","T3-18","T-33","GK-31","GL-06","FW-03-甲","引擎","T3-15","T3-16","GL-09"]),
 "A3":  (9,  "共·**9/19根**",  ["T-24","T3-03","GK-14","T3-17","FW-03-甲","T3-15","T3-16","GL-09","引擎"]),
 "A4":  (7,  "共·**7/19根**",  ["T3-03","GK-14","T-33","T3-17","GL-06","FW-03-甲","GL-09"]),
 "A5":  (6,  "共·**6/19根**",  ["T3-03","GK-14","T3-22"]+W3),
 "A6":  (4,  "共·4/19根",      ["TC-33","T3-17","引擎","GL-09"]),
 "A7":  (17, "共·**17/19根**", ["T3-03","GK-14","T-24","T3-17","T3-18","T-33","GK-31","引擎","T3-22","FW-03-甲","GL-06","T3-15","T3-16","GL-09"]+W3),
 "A8":  (5,  "共·**5/19根**",  ["T3-03","GK-14"]+W3),
 "A9档一":(3, "档一 3/19",      ["T-76","GK-14","GK-31"]),
 "A10": (2,  "共·**2/19根**",  ["T3-17","T3-18"]),
 "A11": (13, "共·**13/19根**", ["T3-17","T3-18","T-33","GK-31","T3-22","GL-06","FW-03-甲","T3-15","T3-16","GL-09"]+W3),
 "A12": (3,  "共·3/19根",      ["T-33","FW-03-甲","T3-22"]),
 "A13": (1,  "单·T-33",        ["T-33"]),
 "B1":  (19, "共·**19/19根显式态度**", ALL),
 "B3":  (10, "共·**10/19根**", ["GK-31","GK-14","T-76","引擎","T3-15","T3-16","GL-09"]+W3),
 "B4":  (3,  "共·**3/19根**",  ["T3-18","GL-06","GL-09"]),
 "B5":  (2,  "共·**2/19根**",  ["T3-15","T3-16"]),
 "C1":  (19, "共·**19/19根**", ALL),
 "C2":  (19, "共·**19/19根**", ALL),
 "C3":  (19, "共·**19/19根**", ALL),
 "C4":  (17, "共·**17/19根**", ["T-76","TC-33","T3-03","GK-14","T-24","T3-17","T3-18","T-33","引擎","T3-22","GL-06","T3-15","T3-16","GL-09"]+W3),
 "C5":  (19, "共·**19/19根**", ALL),
 "C6档一":(19,"档一19/19", ALL),
 "C6档二":(15,"档二15/19", ["TC-33","T3-03","T3-18","T-33","T3-17","引擎","T3-22","FW-03-甲","GL-06","T3-15","T3-16","GL-09"]+W3),
 "C7":  (8,  "共·**8/19根**",  ["T3-17","T3-18","T3-22","T3-15","T3-16"]+W3),
 "C8":  (10, "共·**10/19根**", ["引擎","T3-22","FW-03-甲","GL-06","T3-15","T3-16","GL-09"]+W3),
 "C9":  (12, "共·**12/19根**", ["T3-18","GK-31","引擎","T3-22","FW-03-甲","GL-06","T3-15","T3-16","GL-09"]+W3),
 "C10": (5,  "共·**5/19根**",  ["T3-15","GL-09"]+W3),
 "Z1":  (2,  "共·2/19根：窗2／窗3", ["窗2","窗3"]),
 "Z2":  (2,  "共·2/19根：窗1／窗3", ["窗1","窗3"]),
}
# B2 为缺口实例层面计数（非根计数），单列
B2_BASE = ["TPL1-TC33-01","TPL1-T303-01","TPL1-T303-02","TPL1-GK14-01",
           "TPL1-T317-01","TPL1-T33-01","TPL1-T322-01",
           "TPL1-T315-01","TPL1-T315-02","TPL1-T316-01","TPL1-T316-02"]   # 11，承骨架v3.1定案值
B2_NEW  = ["TPL1-W1-01","TPL1-W2-01","TPL1-W2-02","TPL1-W2-03",
           "TPL1-T324-01","TPL1-T324-02","TPL1-T324-03","TPL1-T324-04"]   # 8，本轮逐条枚举

print("="*76)
print("§7A-1 扩面：分子—成员枚举逐员闭合核算（全条目，恒满条目亦全员枚举）")
print("="*76)
ok=0
for k,(dec,hs,mem) in M.items():
    dup = len(mem)!=len(set(mem))
    inR = all(x in R19 for x in mem)
    cnt = len(set(mem))
    good = (cnt==dec) and (not dup) and inR
    print(f"  {k:8s} 声明={dec:3d} 成员枚举={cnt:3d} 去重内相同={not dup} 成员∈19根域={inR}  {'OK' if good else '**异常**'}")
    if good: ok+=1
    else: fail.append("成员闭合:"+k)
# B2
b2 = len(set(B2_BASE))+len(set(B2_NEW))
print(f"  {'B2':8s} 声明= 19 成员枚举={b2:3d}（实例层：基数11承骨架v3.1定案＋本轮8条逐条枚举）  {'OK' if b2==19 else '**异常**'}")
if b2==19: ok+=1
else: fail.append("成员闭合:B2")
print(f"\n  条目数＝{len(M)+1}（＝30，含 C6 双档分列、A9 以档一计）；闭合通过 {ok}/{len(M)+1}")
if ok!=len(M)+1: fail.append("条目闭合总数")

print("\n" + "="*76)
print("①-b 标题—正文三位一致（声明串在标题在场）")
print("="*76)
heads = [l for l in lines if l.startswith("### ") or l.startswith("## 区")]
for k,(dec,hs,mem) in M.items():
    base = k.split("档")[0]
    h = [l for l in lines if re.match(r"^### "+re.escape(base)+r"[ 　]", l)]
    if not h: h=[l for l in lines if l.startswith("### "+base)]
    hit = any(hs in x for x in h)
    print(f"  {k:8s} 标题含「{hs}」= {hit}")
    if not hit: fail.append("标题串:"+k)

print("\n" + "="*76)
print("①-a/c 矩阵与边计数")
print("="*76)
st = next(i for i,l in enumerate(lines) if l.startswith("### 第五批（45要件"))
en = next(i for i,l in enumerate(lines) if l.startswith("**双向覆盖自查"))
rows=[l for l in lines[st:en] if l.startswith("| EW")]
xr=[l for l in lines if re.match(r"^\| \*{0,2}X\d+ ", l)]
tot=20+21+40+45+len(rows)
print(f"  第五批矩阵物理表行={len(rows)}（声明45）；累计要件={tot}（声明171）；区四边行={len(xr)}（声明20）")
if len(rows)!=45: fail.append("矩阵45")
if tot!=171: fail.append("累计171")
if len(xr)!=20: fail.append("边20")

print("\n" + "="*76)
print("② 段级去重扫描")
print("="*76)
paras,cur=[],[]
for l in lines:
    if l.strip()=="":
        if cur: paras.append("\n".join(cur)); cur=[]
    else: cur.append(l)
if cur: paras.append("\n".join(cur))
seen,dup={},[]
for i,p in enumerate(paras):
    n=re.sub(r"\s+","",p)
    if len(n)<60: continue
    h=hashlib.sha256(n.encode()).hexdigest()
    if h in seen: dup.append((seen[h],i,p[:60]))
    else: seen[h]=i
print(f"  段落总数={len(paras)}；参与去重={len(seen)+len(dup)}；重复命中={len(dup)}")
for d in dup: print("    重复:",d)
if dup: fail.append("段级去重")

print("\n" + "="*76)
print("③ 扩表说明物理行口径（三窗三分表成分行实测）")
print("="*76)
src="/mnt/project"
tri={"窗1":("一阶实体_五窗1_动作生命周期状态机_input_schema_v1_2_20260814.md",r"^\| C-\d+ \|",15),
     "窗2":("一阶实体_五窗2_roll事件记录_input_schema_v1_1_20260815.md",r"^\| C-\d+ ",7),
     "窗3":("一阶实体_五窗3_T3-24六问验收状态量_input_schema_v1_1_20260816.md",r"^\| C-\d+ ",14)}
for k,(f,pat,dec) in tri.items():
    t=io.open(os.path.join(src,f),encoding="utf-8").read().split("\n")
    c=len([l for l in t if re.match(pat,l)])
    print(f"  {k} 三分表成分行实测={c}（骨架声明{dec}）")
    if c!=dec: fail.append("三分表:"+k)

print("\n"+"="*76)
print("=== §7A 扩面重算结果：", "30/30 条目成员闭合全过；异常＝0" if not fail else f"异常＝{len(fail)} → {fail}（依裁决94-3(c)须halt呈报KD，不得就地改数）","===")
print("="*76)
sys.exit(1 if fail else 0)

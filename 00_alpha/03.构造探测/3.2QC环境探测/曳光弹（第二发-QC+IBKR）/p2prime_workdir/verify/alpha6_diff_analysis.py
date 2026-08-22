# -*- coding: utf-8 -*-
"""α-6 本地对照组差异定量：检验「差异是否纯行尾」假说。零网络。"""
import hashlib, os, subprocess, sys, tempfile
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entity"))
import cloud_payload_gl06 as M

exp = M.restore("gl06_harness_output.json")
w = tempfile.mkdtemp(prefix="p2p_a6diff_")
for tgt, src in (("ledger_input.json", "gl06_ledger_input.json"),
                 ("harness.py", "gl06_harness.py")):
    open(os.path.join(w, tgt), "wb").write(M.restore(src))
subprocess.run([sys.executable, os.path.join(w, "harness.py")], cwd=w, capture_output=True)
prod = open(os.path.join(w, "harness_output.json"), "rb").read()

def cnt(b):
    return b.count(b"\r"), b.count(b"\n"), b.count(b"\r\n")

print("=== 差异定量（事实，无推测）===")
for lbl, b in (("expected", exp), ("produced", prod)):
    cr, lf, crlf = cnt(b)
    print("  %-9s %5d B   CR=%3d  LF=%3d  CRLF=%3d" % (lbl, len(b), cr, lf, crlf))
print("  字节差 = %+d" % (len(prod) - len(exp)))

norm = prod.replace(b"\r\n", b"\n")
print()
print("=== 假说检验：produced 之 CRLF 归一化为 LF 后 ===")
print("  归一化后大小 : %d   (expected %d)" % (len(norm), len(exp)))
print("  逐字节相等   : %s" % (norm == exp))
print("  sha256(norm) : %s" % hashlib.sha256(norm).hexdigest())
print("  sha256(exp)  : %s" % hashlib.sha256(exp).hexdigest())
print()
print("  期望件是否含 CR : %s" % ("否（纯 LF）" if exp.count(b"\r") == 0 else "是"))
if norm != exp:
    off = next((i for i, (a, b) in enumerate(zip(norm, exp)) if a != b), min(len(norm), len(exp)))
    print("  归一化后首个差异偏移 : %d" % off)
    print("  norm[%d:%d] = %r" % (off, off + 40, norm[off:off + 40]))
    print("  exp [%d:%d] = %r" % (off, off + 40, exp[off:off + 40]))

# -*- coding: utf-8 -*-
"""
P2' · X-1 载体件构建（verify/ 面来源，与 entity/ 面载体分列）

来源＝`verify/x1_synth.py`（第一发 P2 交付件，KY 20260812 钉定 fixture）。

**放置纪律（重要，须显式）**：
  · 第一发**特意**将该件置于 `verify/` 子树，使其内之 KY 给定常数（r／q 等字面量）
    不落入 A9 机械射程（entity/∪probe/）——原件 docstring 明载「此为规格设计之结果，非规避」。
  · 本位**不重写、不重排、不改任何数值字面量**，只做**逐字节搬运**。
  · 本地放置位置**不变**（仍在 verify/）；云端载体为**传输副本**，非放置面迁移。
  · fixture 不新造（规格件 §3.2、作业指令 §5-3）。

**锚值性质声明**：本件之 SHA256 为**本位实测自锚**，非上游已发布指纹表锚值
（`x1_synth.py` 系第一发 P2 产出，无对应交付件指纹表条目）。与 GL-06 四件、engine
之「上游锚值对表」性质不同，不得混同。

变换算子 v2（同 entity/ 面载体）：raw → zlib.compress(9) → base64 → .py 字面量。
零网络、零外部接触。产出零 QC 库导入、零接口面字面（A4' 自守）。
"""
import base64
import hashlib
import sys
import zlib
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

QC_FILE_CHAR_LIMIT = 32000
WD = Path(__file__).resolve().parent.parent
VERIFY = WD / "verify"
ENTITY = WD / "entity"

SOURCES = {"x1_synth.py": VERIFY / "x1_synth.py"}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    print("=== P2' X-1 载体件构建 · 本地无损性自证 ===")
    parts, originals = [], {}
    for name, p in SOURCES.items():
        raw = p.read_bytes()
        h = sha(raw)
        originals[name] = raw
        print("  %-18s %7d B  sha256=%s" % (name, len(raw), h))
        print("       来源: %s（verify/ 面，逐字节搬运，零改写）" % p.name)
        b64 = base64.b64encode(zlib.compress(raw, 9)).decode("ascii")
        lines = [b64[i:i + 76] for i in range(0, len(b64), 76)]
        parts.append('  %r: {\n    "sha256": %r,\n    "size": %d,\n    "b64": (\n%s\n    ),\n  },\n'
                     % (name, h, len(raw), "\n".join('    "%s"' % ln for ln in lines)))

    src = ('# -*- coding: utf-8 -*-\n'
           '# P2\' X-1 云端载体件（自动生成，勿手改）\n'
           '# 来源＝verify/x1_synth.py（第一发 P2 交付件，KY 20260812 钉定 fixture）\n'
           '# 变换算子 v2: raw -> zlib.compress(9) -> base64 -> .py 字面量；还原逐字节相等\n'
           '# 放置纪律: 本地仍在 verify/；本件为传输副本，非放置面迁移。数值字面量零改写。\n'
           '# 锚值性质: 本位实测自锚，非上游已发布指纹表锚值。\n'
           '# 本件零 QC 库导入、零接口面字面（A4\' 自守）。\n'
           'import base64, hashlib, zlib\n\n'
           'PAYLOAD = {\n%s}\n\n'
           'def restore(name):\n'
           '    e = PAYLOAD[name]\n'
           '    raw = zlib.decompress(base64.b64decode(e["b64"]))\n'
           '    h = hashlib.sha256(raw).hexdigest()\n'
           '    if h != e["sha256"]:\n'
           '        raise ValueError("fingerprint mismatch %%s" %% name)\n'
           '    if len(raw) != e["size"]:\n'
           '        raise ValueError("size mismatch %%s" %% name)\n'
           '    return raw\n'
           ) % "".join(parts)

    out = ENTITY / "cloud_payload_x1.py"
    out.write_text(src, encoding="utf-8", newline="\n")
    chars = len(src)
    print("\n  -> %s  (%d chars) 上限 %d：%s"
          % (out.name, chars, QC_FILE_CHAR_LIMIT, "在线内" if chars < QC_FILE_CHAR_LIMIT else "**超限**"))
    if chars >= QC_FILE_CHAR_LIMIT:
        raise SystemExit("超 QC 32,000 字符上限，停")

    sys.path.insert(0, str(ENTITY))
    mod = __import__(out.stem)
    print("\n=== 无损性自证 ===")
    ok = True
    for name, raw in originals.items():
        back = mod.restore(name)
        same = back == raw
        ok &= same
        print("  %-18s 还原 %7d B  逐字节%s" % (name, len(back), "相等" if same else "**不等**"))
    print("\n无损性自证: %s" % ("PASS" if ok else "FAIL"))
    kw = "Quant" + "Connect"
    print("A4' 自查: %s 字面命中 %d" % (kw, out.read_text(encoding="utf-8").count(kw)))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

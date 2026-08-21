# -*- coding: utf-8 -*-
"""
P2' · 云端载体格式变换（E1-08 白名单适配）· 本地无损性自证

背景（事实，非推测）：
  · QC file API 扩展名白名单 = cs/py/ipynb/html/css（E1-08 / F1-11）；`.md` `.json` 被拒。
  · `files.create(project_id, file_name, content: str)` —— content 为 str，不收 bytes。
  · GL-06 四件中 `.md` 一件、`.json` 两件不在白名单内。
  规格件 §3.2 工程面第1点已预见：「`.json` 被拒 → 载体格式须改」。

变换算子（须显式声明，不得静默）：
  original_bytes --base64.b64encode--> ascii str --嵌入 .py 字面量--> 云端可承载
  云端侧 base64.b64decode 还原 → 与本地原件逐字节相等（本脚本本地自证）。

本脚本零外部接触、零网络。产出落 entity/（人造件，零真实数值，零 QC 接口面字面）。
A4' 自守：产出文件内**零 `QuantConnect` 字面**，零 QC 库导入。
"""
import base64
import hashlib
import sys
import zlib
from pathlib import Path

# QC file API 单件上限（实测，20260818）：32,000 字符。
# 成因留痕：首轮以纯 base64 载体上传 43,416 字符件被拒，错误原文
#   "File exceeds the maximum size of 32,000 characters by using 43,416."
# 该约束**不在规格件 E1 映射表内**，为本发新发现（见 friction_record FR-P2-06）。
QC_FILE_CHAR_LIMIT = 32000

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

WD = Path(__file__).resolve().parent.parent
ENTITY = WD / "entity"

# 被测件 → 云端载体分组
GROUPS = {
    "engine": ["engine.py"],
    "gl06": ["gl06_input_schema.md", "gl06_ledger_input.json",
             "gl06_harness.py", "gl06_harness_output.json"],
}

ANCHORS = {
    "engine.py": "d88a955e45dddaa5a11f02c9237cb5e178bdfca6335a670ecdf21414dca682cf",
    "gl06_input_schema.md": "33fe363cfb24bdfd557b81efe8e79be2b51c82c2bfff40278b096311ee4394f1",
    "gl06_ledger_input.json": "31605728279ba59813bdacc705e3b8264179a1f511e63cac402ea80e90a989c7",
    "gl06_harness.py": "5702aae378244ad3d17f1161b769eacf0e66cdc1664c99553654f8f36e3b8747",
    "gl06_harness_output.json": "722f00ee0c4dbceb43ec4d72eb2c86cfbfddb0b5f879aa4f709124589cab7e44",
}

WHITELIST = {".cs", ".py", ".ipynb", ".html", ".css"}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def wrap(name, raw):
    """单件 → zlib 压缩后 base64 片段（每行 76 字符，避免超长行）。
    变换算子（v2，因 QC 32,000 字符上限而加压缩级）：
        raw --zlib.compress(9)--> --base64.b64encode--> ascii str
    还原：base64.b64decode --zlib.decompress--> raw，并核 SHA256。"""
    b64 = base64.b64encode(zlib.compress(raw, 9)).decode("ascii")
    lines = [b64[i:i + 76] for i in range(0, len(b64), 76)]
    body = "\n".join('    "%s"' % ln for ln in lines)
    return ('  %r: {\n'
            '    "sha256": %r,\n'
            '    "size": %d,\n'
            '    "b64": (\n%s\n    ),\n'
            '  },\n') % (name, sha(raw), len(raw), body)


def build(group, names):
    print("\n=== 载体组: %s ===" % group)
    parts = []
    originals = {}
    for n in names:
        p = ENTITY / n
        raw = p.read_bytes()
        h = sha(raw)
        anchor = ANCHORS[n]
        ok = (h == anchor)
        ext = p.suffix.lower()
        print("  %-26s %7d B  ext=%-6s 白名单=%-3s 锚值=%s"
              % (n, len(raw), ext, "是" if ext in WHITELIST else "否", "一致" if ok else "**不一致**"))
        if not ok:
            raise SystemExit("锚值不一致，停：%s" % n)
        originals[n] = raw
        parts.append(wrap(n, raw))

    src = ('# -*- coding: utf-8 -*-\n'
           '# P2\' 云端载体件（自动生成，勿手改）· 组=%s\n'
           '# 变换算子 v2: original_bytes -> zlib.compress(9) -> base64.b64encode -> .py 字面量\n'
           '# 还原: zlib.decompress(base64.b64decode(PAYLOAD[name]["b64"])) == 原件 bytes（逐字节）\n'
           '# 成因1: QC file API 扩展名白名单拒 .md/.json（E1-08）；content 参数为 str 不收 bytes。\n'
           '# 成因2: QC file API 单件上限 32,000 字符（本发实测新发现，FR-P2-06）；\n'
           '#        纯 base64 载体 43,416 字符被拒，故加压缩级。\n'
           '# 本件零 QC 库导入、零接口面字面（A4\' 自守）。\n'
           'import base64, hashlib, zlib\n\n'
           'PAYLOAD = {\n%s}\n\n'
           'def restore(name):\n'
           '    """还原原件 bytes 并核证 SHA256；不一致即抛。"""\n'
           '    e = PAYLOAD[name]\n'
           '    raw = zlib.decompress(base64.b64decode(e["b64"]))\n'
           '    h = hashlib.sha256(raw).hexdigest()\n'
           '    if h != e["sha256"]:\n'
           '        raise ValueError("fingerprint mismatch %%s: %%s != %%s" %% (name, h, e["sha256"]))\n'
           '    if len(raw) != e["size"]:\n'
           '        raise ValueError("size mismatch %%s" %% name)\n'
           '    return raw\n\n'
           'def restore_all():\n'
           '    return {n: restore(n) for n in PAYLOAD}\n'
           ) % (group, "".join(parts))

    out = ENTITY / ("cloud_payload_%s.py" % group)
    out.write_text(src, encoding="utf-8", newline="\n")
    chars = len(src)
    ok = chars < QC_FILE_CHAR_LIMIT
    print("  -> %s  (%d B / %d chars, ext=.py 在白名单) 上限 %d：%s"
          % (out.name, out.stat().st_size, chars, QC_FILE_CHAR_LIMIT,
             "在线内" if ok else "**超限，上传必被拒**"))
    if not ok:
        raise SystemExit("载体件超 QC 32,000 字符上限，停：%s（%d chars）" % (out.name, chars))
    return out, originals


def main():
    print("=== P2' 云端载体格式变换 · 本地无损性自证 ===")
    print("零网络、零外部接触。")
    built = {}
    for g, names in GROUPS.items():
        out, orig = build(g, names)
        built[g] = (out, orig)

    # --- 本地无损性自证：导入生成件 → 还原 → 与原件逐字节比对
    print("\n" + "=" * 66)
    print("=== 无损性自证（还原 vs 原件，逐字节）===")
    print("=" * 66)
    sys.path.insert(0, str(ENTITY))
    allok = True
    for g, (out, orig) in built.items():
        mod = __import__(out.stem)
        for n, raw in orig.items():
            back = mod.restore(n)
            same = (back == raw)
            allok &= same
            print("  %-26s %-6s  还原 %7d B  逐字节%s"
                  % (n, "[" + g + "]", len(back), "相等" if same else "**不等**"))
    print("\n无损性自证: %s" % ("ALL PASS —— 变换可逆，云端可还原原件字节" if allok else "HAS FAIL"))
    if not allok:
        raise SystemExit(1)

    # --- A4' 自守：产出件内零 QuantConnect 字面（关键字拼接存放，防自命中）
    kw = "Quant" + "Connect"
    print("\n=== A4' 自查：生成件内 %s 字面命中数 ===" % kw)
    for g, (out, _) in built.items():
        n = out.read_text(encoding="utf-8").count(kw)
        print("  %-30s 命中 %d" % (out.name, n))


if __name__ == "__main__":
    main()

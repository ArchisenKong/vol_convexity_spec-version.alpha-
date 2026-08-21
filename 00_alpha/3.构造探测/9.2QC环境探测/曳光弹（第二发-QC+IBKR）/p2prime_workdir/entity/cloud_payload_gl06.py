# -*- coding: utf-8 -*-
# P2' 云端载体件（自动生成，勿手改）· 组=gl06
# 变换算子 v2: original_bytes -> zlib.compress(9) -> base64.b64encode -> .py 字面量
# 还原: zlib.decompress(base64.b64decode(PAYLOAD[name]["b64"])) == 原件 bytes（逐字节）
# 成因1: QC file API 扩展名白名单拒 .md/.json（E1-08）；content 参数为 str 不收 bytes。
# 成因2: QC file API 单件上限 32,000 字符（本发实测新发现，FR-P2-06）；
#        纯 base64 载体 43,416 字符被拒，故加压缩级。
# 本件零 QC 库导入、零接口面字面（A4' 自守）。
import base64, hashlib, zlib

PAYLOAD = {
  'gl06_input_schema.md': {
    "sha256": '33fe363cfb24bdfd557b81efe8e79be2b51c82c2bfff40278b096311ee4394f1',
    "size": 13748,
    "b64": (
    "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"
    ),
  },
  'gl06_ledger_input.json': {
    "sha256": '31605728279ba59813bdacc705e3b8264179a1f511e63cac402ea80e90a989c7',
    "size": 2266,
    "b64": (
    "eNqtlM9v00gUx+/9K6JcuBSI06ZLucFh97KHlXZvCFleZ0SMEtuyJ0VVheQu0CTdJE0pTUvblKak"
    "SQXbH6DdEhwHJP4UmJk4p/wLvLHdgFgZYXYvlmbem8+89/2+8cJELBYX0xKWRFPLGzKKX43FzXkV"
    "ZxBWZDEjqWlR1lQTG3kZo3R80svXfr+NZCwqaZ79088XEzNBQFdUUdWwR6EPisOHJbd5SGtV99Uq"
    "Wz8dOcUfLwqJkVMaOVts5y9WL5DeGenabPf+0NojzpZ70hi266T7jNgdWrD9hJFTBhaxqxnJUJFp"
    "XtLnLytqGukIPioWDSRrOT2PEQRIr0f666zUcZtlunxI+jt06TE93ho520KK7Twhtg03QS2scky6"
    "VdJtsU6f9Ct0pU4th+4c+pXSUoW+ekm3be9oedjYDfZrVbq9S5vPP1h/+C2bWQ2b0O4CLGBpSFjR"
    "RJwxkJnRsulxAEJqPocgrBmwmZw834UOtJyiBvvCeB/P656KumRIOYSRIfKbRBkMUcAuFB9nnuvN"
    "7BroRY82ho196OUCbXXcwt/QIbUqF8jrP9nJI/fNvUFvDdQGJ96XDsAIEH/woke6FjTKmkWQiXdp"
    "OUmwx7Wfn4dL1Ho8tEq+VnDYp4CAgW7FpUG7B0L9ipEuXObfJNvYd58uel6Xh5tn7Pifaz4E8km3"
    "Qlt1Vj0Evtu575bvQdIvGclEsetsr0kLS1xfr8G7fp9xaQ7Eu6Wot8Q74L12B2Z23vxc3jkpm+c6"
    "pP6LhBsHtFGg5frg2QZdeTpcf0vt9rhqfxD8+mAJJfppbPOE1tr0aBPG54O1GJxqbdHTVVj+Bi9J"
    "Yo/O6IMD8qYT5NbK7OhgfBsf8EbhS63XKnx6ebTodhZh0BXM5x4GXTTlDMpJl3Lp2LvO9PvVfV9l"
    "/qL2XtPj3UH11GeMnAZ522DLLVasQRTux4akZEHFmKnk9CyK+bKif9XJfe2vwYMJ3Fppj6v9ZM1E"
    "YE9cR4aipbkdN7zIQhx7w8xN4FhRUeGJIlGGLnhWMpVITMIxA3SX4cGo8I8xsYjnxhlCIpEIrPdh"
    "yVCYEB02FV5ZMjJsOryy2ciwVHhliciwma9UNjsbEfbD1yoTIsKuhMKmorc5GwrzJiMaTOC3/18G"
    "CMLk98/Z9JewZChsJjpsKgwmXIkOmw6tTJiJDEuFwaZS31QZsG5O3J34CEbUsyE="
    ),
  },
  'gl06_harness.py': {
    "sha256": '5702aae378244ad3d17f1161b769eacf0e66cdc1664c99553654f8f36e3b8747',
    "size": 3710,
    "b64": (
    "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"
    "kqbsDOW/5TcYvQ=="
    ),
  },
  'gl06_harness_output.json': {
    "sha256": '722f00ee0c4dbceb43ec4d72eb2c86cfbfddb0b5f879aa4f709124589cab7e44',
    "size": 4159,
    "b64": (
    "eNrtl0tvE0kQgO/5FZYvXNjFM37E4QYXLntA2r2tUKt33PE0moc13Q6yEJIDLHF280KBJEAcIDgx"
    "gk0I0i4yiQMSPwWm287Jf2FrZpxJwsPIYzknLiO7qrqr+qtHz1wficXiKIc5RswuOhqJn4/FWcni"
    "OuFUQzq2ckizLcadosZJLn7Ws7f/uEo0jmjOM770y0+JTCBnhs0ZIppug+I6SEDmYE5txHWHMN02"
    "cqECVFbRJKC2HRCqZw+lOWLZJrW6ciWU81LBD66AHWwSThzkuUMaREghfhIPLS2b+5Zyd0EuTYmt"
    "5YPquig3z4havT31r9uoifLsGfft3/LVvfa7W629Rbl2u9OsfJze6DSn3cZu6/We2yiL7YfyaaXT"
    "fCTv78BqVa7+0959eaieFuUHB+VpWd9392dhcbCL25gT80tgLSp3Wpt7nebMr5wUlHPeU5XL6+1n"
    "k+ACxAcrb+T2fxeCTcDebcyK2pKcew77t+u32zO3wOiyjhmJXZRPnoqpO5/KN+P+AW8E54zjCYCX"
    "p1YeXaNWzr4GSSyx43gnsFH0OKQHQbi8IapTYmap9WJZzD87uP9e7G6GUXsHqa4F8cFfCDEwkyuv"
    "xMKm2FoRq88/lSe7q2oPxc5d+PsblBaW996IPzfcd/Wu7cKM3NoIvcHG8ONz1ouz7v6qr62065PE"
    "4pSXzlGrUOSIaTox8c9mLvahnvp4dz2gDCmTT96K7bXW3E6wR6dZdd9X5V81WVkALfjnDqYGUIwx"
    "ahYMEguwki/i9PK6vyhXH3ezNb8ZRnuUmpFueuJQ7UWDe+n43deESeEnapp4OcJeX52PjWODkVDj"
    "EMxsy0sBtVhxfJxqFA58mGqdMmiP0omCOOFCHb6L5PBdpIbvIv1VFzDtjjx4oxAjamm2SZAGm3tp"
    "VROJRGjRdcaKJio40DkajDwLxibjiE+ES9JfWdLt2aMoDJ0hzbEZQyYUkFcsiePLnO+o/WFrEgJj"
    "+PjI9c7zTQSZiAiUsbGxU0EAftKDEvCL5psIRqNXgXJqVZAeahVkIyJInlojpIfdCGMREaRPiYCa"
    "HhxA7z5QEj/GoaJEZaD2zyAViYHyHQbZgRmoURlk+meQjcQg2ZuBkhmYQTLqvZjtm0FGjXQv9kag"
    "pgafB6modQD8+2WQiTYPsj0hJNXBIUR9R0z2fzGMRhuKo71vhlR/QxGeV/yvGI8LhTdq7MfKHZrP"
    "wzfjuIHz/pfNlZEb/wPw9VzQ"
    ),
  },
}

def restore(name):
    """还原原件 bytes 并核证 SHA256；不一致即抛。"""
    e = PAYLOAD[name]
    raw = zlib.decompress(base64.b64decode(e["b64"]))
    h = hashlib.sha256(raw).hexdigest()
    if h != e["sha256"]:
        raise ValueError("fingerprint mismatch %s: %s != %s" % (name, h, e["sha256"]))
    if len(raw) != e["size"]:
        raise ValueError("size mismatch %s" % name)
    return raw

def restore_all():
    return {n: restore(n) for n in PAYLOAD}

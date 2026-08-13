# -*- coding: utf-8 -*-
"""X-2 FlexQuery 探查（§5 步6 ／ §4B，v1.3 新增）。

落位理由（§4B 代码落位条款）：FlexQuery 走 IBKR Web Service（HTTPS，非 TWS
socket），故实现代码落 probe/ 子树——probe/ 豁免 step0(ii) forbidden 扫描
（85-7），entity/ 不得出现 flex 相关 URL/凭据引用。

凭据纪律（AGENTS.md 第6条 ／ §4B）：
    唯一取值路径＝运行时环境变量 IB_FLEX_TOKEN／IB_FLEX_QUERY_ID。
    本文件不含、不写、不回显任何凭据值；不入 data_manifest、不入摩擦记录、
    不入 P3 交付件。缺失 → SystemExit(2)，无 fallback。

用法：
    IB_FLEX_TOKEN=… IB_FLEX_QUERY_ID=… python probe/probe_flex.py
"""

import os
import sys
import time

sys.dont_write_bytecode = True
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "entity"))

import probe_harness as H                                        # noqa: E402
from ib_insync.flexreport import FlexReport, FlexError           # noqa: E402

FLEX_ENV_TOKEN = "IB_FLEX_TOKEN"
FLEX_ENV_QUERY = "IB_FLEX_QUERY_ID"


def require_flex_credentials():
    """FlexQuery 调用之前的机械拦截（q/r 闸同型，§4B）。

    任一环境变量缺失 → 打印索取清单（**不回显已有值**）→ SystemExit(2)。
    无 fallback、不读文件、不接受命令行传入、不落盘。
    """
    missing = [k for k in (FLEX_ENV_TOKEN, FLEX_ENV_QUERY)
               if not os.environ.get(k)]
    if missing:
        print("=" * 70)
        print("缺凭据即停：向KY索取 flex_token / flex_query_id")
        print("缺失环境变量：%s" % (missing,))
        print("规格依据：P1规格件 v1.3 §4B——凭据不入任何文件、不入 manifest、"
              "不入交付件；唯一通道＝运行时环境变量")
        print("=" * 70)
        raise SystemExit(2)
    return os.environ[FLEX_ENV_TOKEN], os.environ[FLEX_ENV_QUERY]


def describe_structure(node, path="", depth=0, out=None, max_depth=6):
    """字段结构提取：只取字段名/层级/类型，**不取值**——供 P3 呈报面。"""
    if out is None:
        out = []
    if depth > max_depth:
        return out
    if isinstance(node, dict):
        for k in sorted(node):
            v = node[k]
            p = "%s.%s" % (path, k) if path else k
            out.append({"path": p, "depth": depth,
                        "type": type(v).__name__,
                        "container": isinstance(v, (dict, list))})
            describe_structure(v, p, depth + 1, out, max_depth)
    elif isinstance(node, list):
        if node:
            describe_structure(node[0], path + "[]", depth + 1, out, max_depth)
    return out


def main():
    token, query_id = require_flex_credentials()   # 闸：缺凭据即 SystemExit(2)
    if not token or not query_id:                  # 防御：闸不得静默放行
        raise SystemExit(2)
    print("凭据闸通过（值不回显）。query_id 长度=%d，token 长度=%d"
          % (len(query_id), len(token)))

    # @FLEX_CALL_POINT —— 闸之后方得调用（A11 序位检测锚）
    # Flex Web Service 对同一 query 有冷却期，短时间重复请求返回 1001。
    # 重试属传输层工程处置（§4A 第4条），不改任何数值语义、不改请求内容。
    report = None
    for attempt in range(1, 7):
        print("拉取 Flex 报表…（第 %d 次）" % attempt)
        try:
            report = FlexReport(token=token, queryId=query_id)
            break
        except FlexError as e:
            if "1001" not in str(e) or attempt == 6:
                raise
            print("  冷却中（%s），120s 后重试" % e)
            time.sleep(120)
    if report is None:
        raise SystemExit(2)

    # 下载成功即先落原件——首次实测中下载已成功但解析崩溃，原始 XML 未落盘即
    # 丢失，随后服务转入持续 1001 无法复取。取数与解析必须解耦：**先存后解**。
    raw = getattr(report, "data", None)
    if raw is not None:
        H.write_payload("x2_flex_raw",
                        {"raw_xml": raw.decode("utf-8", errors="replace"),
                         "n_bytes": len(raw)}, "step6_flex")
        print("原件已落盘（%d bytes），解析与取数已解耦。" % len(raw))

    topics = sorted(report.topics())
    print("topic 数=%d：%s" % (len(topics), topics))

    payload = {"topics": topics, "sections": {}, "structure": {}}
    for t in topics:
        try:
            rows = report.extract(t, parseNumbers=True)
        except Exception as e:                       # noqa: BLE001
            payload["sections"][t] = {"error": repr(e)}
            print("  %-28s 解析失败: %r" % (t, e))
            continue
        # ib_insync FlexReport.extract 返回 DynamicObject 子类实例，属性存于
        # 实例 __dict__（flexreport.py:53-54），非 namedtuple、不可迭代。
        recs = [dict(vars(r)) for r in rows]
        payload["sections"][t] = recs
        fields = sorted(recs[0]) if recs else []
        payload["structure"][t] = {"n_records": len(recs),
                                   "n_fields": len(fields),
                                   "fields": fields}
        print("  %-28s 记录=%-4d 字段=%d" % (t, len(recs), len(fields)))

    H.write_payload("x2_flex_report", payload, "step6_flex")

    # 呈报面：只出字段结构，账户号与数值不入（§4B 载荷条款）
    struct_only = {t: payload["structure"][t] for t in payload["structure"]}
    H.write_payload("x2_flex_structure", struct_only, "step6_flex")

    print("\n字段结构清单已落 probe/（呈报面只含字段名/计数，无数值、无账户号）")
    return 0


if __name__ == "__main__":
    sys.exit(main())

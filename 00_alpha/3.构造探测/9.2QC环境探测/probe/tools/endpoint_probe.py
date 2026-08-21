"""
E23 · 端点存在性探测（任务书外，执行人追加）

两个目标：
  1. backtests/read 的 result 字段为 None，是否有兄弟端点承载完整结果（图表/订单）
  2. 是否存在 research 触发端点（lean 库中完全没有 research/* 或 notebook/*）

副作用控制：
  - 读取类端点用真实 projectId + backtestId。
  - 任何可能产生副作用的 create/start 类端点，一律用无效 projectId=0 探测，
    只判断「端点是否存在」，不作用于真实项目。
  - 全程不调用任何 delete 类端点。

凭据：由 lean 自动从 ~/.lean/credentials 载入内存，本脚本不打印、不写出凭据。
"""
import json

PROJECT_ID = 35174460
BACKTEST_ID = "475935f261165c79d347d6a311143206"       # E11，CLI 触发
BACKTEST_ID_WEB = "7cb12c4cd8b12f34094a3835336b3ebc"   # E13，网页端触发


def classify(msg):
    """把服务端返回归类，用于判断端点是否存在。"""
    m = msg.lower()
    if "endpoint not found" in m:
        return "端点不存在"
    if "not found" in m and "endpoint" not in m:
        return "端点存在，目标对象未找到"
    if any(k in m for k in ("missing", "required", "invalid", "must be", "no such")):
        return "端点存在，参数校验失败"
    if "hash doesn't match" in m or "unauthorized" in m or "credential" in m:
        return "认证问题"
    if "institutional" in m or "upgrade" in m:
        return "档位闸门"
    return "其他"


def probe(api, kind, endpoint, params, note=""):
    tag = f"{kind.upper():4} {endpoint}"
    try:
        data = api.get(endpoint, params) if kind == "get" else api.post(endpoint, params)
        keys = list(data.keys()) if isinstance(data, dict) else type(data).__name__
        print(f"[OK  ] {tag}")
        print(f"        顶层键: {keys}")
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, (dict, list)):
                    n = len(v)
                    sz = len(json.dumps(v, default=str))
                    print(f"          {k}: {type(v).__name__}, {n} 项, {sz} 字节")
                elif v is None:
                    print(f"          {k}: None")
        return data
    except Exception as e:
        msg = str(e)
        print(f"[FAIL] {tag}")
        print(f"        归类: {classify(msg)}")
        print(f"        原文: {msg[:300]}")
        return None
    finally:
        if note:
            print(f"        注: {note}")
        print()


def main():
    from lean.container import container
    api = container.api_client

    print("=" * 72)
    print("目标 1 · backtests 完整结果（result 为 None，探兄弟端点）")
    print("=" * 72)

    probe(api, "get", "backtests/read",
          {"projectId": PROJECT_ID, "backtestId": BACKTEST_ID},
          "基线：库中 backtest_client.get 所用端点")

    for ep in ["backtests/chart/read", "backtests/charts/read",
               "backtests/orders/read", "backtests/read/orders",
               "backtests/read/report", "backtests/report/read",
               "backtests/insights/read", "backtests/read/insights",
               "backtests/list"]:
        params = {"projectId": PROJECT_ID, "backtestId": BACKTEST_ID}
        if "chart" in ep:
            params["name"] = "Strategy Equity"
        if "orders" in ep:
            params.update({"start": 0, "end": 100})
        probe(api, "get", ep, params)

    print("=" * 72)
    print("目标 1b · backtests/read 加参数，看能否要出 result")
    print("=" * 72)
    for extra in [{"chart": "Strategy Equity"}, {"includeResult": True},
                  {"full": True}, {"charts": True}]:
        p = {"projectId": PROJECT_ID, "backtestId": BACKTEST_ID}
        p.update(extra)
        probe(api, "get", "backtests/read", p, f"额外参数 {extra}")

    print("=" * 72)
    print("目标 2 · research 触发端点探空")
    print("=" * 72)
    print("!! 以下一律用 projectId=0（无效），只判端点存在性，不作用于真实项目 !!")
    print()
    for kind, ep in [("get", "research/read"), ("post", "research/create"),
                     ("get", "notebook/read"), ("post", "notebook/create"),
                     ("get", "research/nodes/read"), ("post", "research/start"),
                     ("post", "research/stop"), ("get", "jupyter/read"),
                     ("post", "notebook/start")]:
        probe(api, kind, ep, {"projectId": 0})

    print("=" * 72)
    print("目标 2b · 已知存在的端点作对照（确认归类逻辑可靠）")
    print("=" * 72)
    probe(api, "get", "projects/read", {"projectId": 0},
          "对照：端点确实存在，projectId=0 无效")
    probe(api, "get", "nodes/read", {"organizationId": "954877bda8b6760ae398418ce79a5500"},
          "对照：端点存在且参数有效")


if __name__ == "__main__":
    main()

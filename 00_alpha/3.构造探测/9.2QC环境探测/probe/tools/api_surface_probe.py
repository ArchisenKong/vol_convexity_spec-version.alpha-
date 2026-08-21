"""
E18 · lean 库 API 面探测（任务书外，执行人追加）

目的：探测 lean CLI 未暴露为命令、但库中存在的读取通道。
用途仅为通道探测。不含任何交易或策略逻辑，不计算任何收益指标。

凭据处理：container.api_client 由 lean 自动从 ~/.lean/credentials 构造。
本脚本不打印、不写出任何凭据。输出前对疑似敏感键名做遮蔽。
"""
import json
import sys
from pathlib import Path

PROJECT_ID = 35174460
ORG_ID = "954877bda8b6760ae398418ce79a5500"
BACKTEST_IDS = [
    ("E11 CLI 触发 env-probe-02", "475935f261165c79d347d6a311143206"),
    ("E13 网页端触发 Smooth Light Brown Anguilline", "7cb12c4cd8b12f34094a3835336b3ebc"),
]

SENSITIVE = (
    "token", "apikey", "api_key", "secret", "password", "passwd", "credential",
    # 支付相关：account_client.get_organization() 会返回 card{brand,expiration,last4}
    "card", "last4", "expiration", "brand",
)

OUTDIR = Path(__file__).resolve().parent.parent / "env"
OUTDIR.mkdir(parents=True, exist_ok=True)


def redact(obj):
    """递归遮蔽疑似凭据字段。"""
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if any(s in str(k).lower() for s in SENSITIVE):
                out[k] = "<REDACTED>"
            else:
                out[k] = redact(v)
        return out
    if isinstance(obj, list):
        return [redact(v) for v in obj]
    return obj


def dump(model):
    """pydantic 模型 → 普通 dict。"""
    for attr in ("model_dump", "dict"):
        if hasattr(model, attr):
            try:
                return redact(getattr(model, attr)())
            except Exception:
                pass
    return redact({"__repr__": repr(model)})


def probe(label, fn):
    print(f"\n{'=' * 70}")
    print(f"=== {label}")
    print("=" * 70)
    try:
        result = fn()
    except Exception as e:
        print(f"[FAIL] {type(e).__name__}: {e}")
        return None
    if isinstance(result, list):
        print(f"[OK] 返回 list，{len(result)} 项")
        data = [dump(x) for x in result]
    else:
        print("[OK] 返回单对象")
        data = dump(result)
    print("--- 顶层键 ---")
    if isinstance(data, dict):
        for k in data:
            print(f"    {k}")
    elif data and isinstance(data[0], dict):
        for k in data[0]:
            print(f"    {k}")
    return data


def main():
    from lean.container import container
    api = container.api_client

    print("=== E18 · lean 库 API 面探测 ===")
    print(f"lean 库路径: {Path(container.__module__).name if hasattr(container, '__module__') else 'n/a'}")
    print(f"PROJECT_ID = {PROJECT_ID}")
    print(f"ORG_ID     = {ORG_ID}")

    collected = {}

    collected["organization"] = probe(
        "organization_client.get(ORG_ID) — 查档位/订阅",
        lambda: api.organizations.get(ORG_ID),
    )
    collected["account"] = probe(
        "account_client.get_organization(ORG_ID) — 查账户",
        lambda: api.accounts.get_organization(ORG_ID),
    )
    collected["user"] = probe(
        "user_client.get_info(ORG_ID) — 查用户",
        lambda: api.users.get_info(ORG_ID) if hasattr(api, "users") else api.user.get_info(ORG_ID),
    )
    collected["nodes"] = probe(
        "node_client.get_all(ORG_ID) — 查节点/配额",
        lambda: api.nodes.get_all(ORG_ID),
    )
    collected["project_files"] = probe(
        f"file_client.get_all({PROJECT_ID}) — 读云端项目文件",
        lambda: api.files.get_all(PROJECT_ID),
    )
    collected["lean_environments"] = probe(
        "lean_client.environments() — 查可用 LEAN 环境",
        lambda: api.lean.environments(),
    )

    for label, bt_id in BACKTEST_IDS:
        collected[f"backtest_{bt_id[:8]}"] = probe(
            f"backtest_client.get({PROJECT_ID}, {bt_id[:8]}...) — {label}",
            lambda i=bt_id: api.backtests.get(PROJECT_ID, i),
        )

    outfile = OUTDIR / "api_surface_probe.json"
    outfile.write_text(json.dumps(collected, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    print(f"\n\n=== 全量结果已写入: {outfile} ===")


if __name__ == "__main__":
    sys.exit(main())

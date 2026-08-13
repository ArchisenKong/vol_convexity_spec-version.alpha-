# -*- coding: utf-8 -*-
"""P2 探针 harness（纯代码，零真实数值）——规格来源＝P1规格件 v1.2 §2/§5。

本模块只提供能力：连接、合约解析、行情读取、载荷落盘、q/r 闸。
**不含任何真实市场数值**；一切数值均为运行期取得，立即写入 probe/ 子树。

纪律（规格强制项）：
- 只读：本模块不提供、不引用任何下单侧或改单侧能力（A7 机械检测）。
  连接层另加 readonly 开关作第二道。
- paper：端口白名单 ＋ 账户前缀校验，命中非 paper 格式即抛错即停（A8）。
- 标记串以拼接形态构造：本文件位于 entity/ 子树，A2 要求标记串于 entity/ 命中
  数==0，故不得出现完整字面量（手法同 §3 对 A4 之注）。
- q/r：本模块不含 dividend_yield／risk_free_rate 之数值字面量赋值（A9）；
  唯一取值路径＝KD 手工填写之参数文件。
"""

import datetime as _dt
import hashlib
import json
import os

from ib_insync import IB, Future, FuturesOption, util

# --------------------------------------------------------------------------
# 拼接形态常量（防 A2 自命中）
# --------------------------------------------------------------------------

MARK = "_pro" + "be_"
DATA_SOURCE_KEY = "_data_source"
DATA_SOURCE_VALUE = "external" + MARK + "NOT_FOR_ENTITY"
KD_PARAMS_BASENAME = "kd_params" + MARK + ".json"

# --------------------------------------------------------------------------
# 规格给定常量（皆非市场数值）
# --------------------------------------------------------------------------

PAPER_PORTS = (7497, 4002)
PAPER_ACCT_PREFIXES = ("DU", "DF")
CAPTURE_ENV = "paper"          # v1.1 paper 条款：逐项标注采集环境
HOST = "127.0.0.1"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROBE_DIR = os.path.join(ROOT, "probe")
VERIFY_DIR = os.path.join(ROOT, "verify")
MANIFEST = os.path.join(PROBE_DIR, "data_manifest.json")
CONN_LOG = os.path.join(VERIFY_DIR, "connection_log.json")

QR_REQUIRED_FIELDS = ("dividend_yield", "risk_free_rate")


class PaperGuardError(RuntimeError):
    """A8 违反：非 paper 端口或非 paper 账户格式。"""


def mask_account(acct):
    """账户号脱敏（§4B 载荷条款）：保前缀（A8 判据）＋末三位（可追溯）。"""
    s = str(acct)
    if len(s) <= 5:
        return s[:2] + "*" * max(0, len(s) - 2)
    return s[:2] + "*" * (len(s) - 5) + s[-3:]

# 注：flex 凭据闸不落本文件。§4B 明文「entity/ 不得出现 flex 相关 URL/凭据
# 引用」，故 require_flex_credentials() 与 FlexQuery 实现一并落 probe/probe_flex.py
# （probe/ 豁免 step0(ii) forbidden 扫描，85-7）。


# --------------------------------------------------------------------------
# 载荷落盘（D-2 ＋ D-3 履行）
# --------------------------------------------------------------------------

def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def write_payload(stem, payload, phase):
    """把含真实数值之载荷写入 probe/ 子树并登记 manifest。

    D-3：注入 _data_source 键。
    D-2：文件 SHA256 登记入 data_manifest.json（黑名单）。
    paper 条款：注入 _capture_env 标注。
    """
    if not isinstance(payload, dict):
        raise TypeError("载荷须为 dict（D-3 键名标记之承载形态）")
    rec = dict(payload)
    rec[DATA_SOURCE_KEY] = DATA_SOURCE_VALUE
    rec["_capture_env"] = CAPTURE_ENV
    rec["_phase"] = phase
    rec["_captured_at"] = _dt.datetime.now().isoformat(timespec="seconds")

    fname = stem + MARK + ".json"
    path = os.path.join(PROBE_DIR, fname)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=2, default=str)

    man = {"entries": []}
    if os.path.isfile(MANIFEST):
        try:
            with open(MANIFEST, "r", encoding="utf-8") as f:
                man = json.load(f)
        except ValueError:
            pass
    man.setdefault("entries", [])
    man["entries"] = [e for e in man["entries"] if e.get("file") != fname]
    man["entries"].append({"file": fname,
                           "sha256": _sha256_file(path),
                           "phase": phase,
                           "capture_env": CAPTURE_ENV})
    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(man, f, ensure_ascii=False, indent=2)
    return path


# --------------------------------------------------------------------------
# 连接（只读 ＋ A8 paper 双检）
# --------------------------------------------------------------------------

EVENTS = []          # 全量 error／notification 事件流（诊断面，只读）


def _on_event(reqId, errorCode, errorString, contract):
    EVENTS.append({"reqId": reqId, "code": errorCode, "msg": errorString,
                   "contract": (contract.localSymbol if contract else None),
                   "at": _dt.datetime.now().isoformat(timespec="seconds")})


def connect_paper(port, client_id):
    """连接并即时执行 A8 双检；任一不合即抛 PaperGuardError（即停，不降级）。"""
    if port not in PAPER_PORTS:
        raise PaperGuardError("端口 %r 不在 paper 白名单 %r" % (port, list(PAPER_PORTS)))

    ib = IB()
    ib.errorEvent += _on_event          # 诊断：数据农场连接状态经此通道到达
    # readonly=True：只读纪律之连接层承载，与 A7 源码检测叠加
    ib.connect(HOST, port, clientId=client_id, readonly=True, timeout=20)
    ib.sleep(3.0)                       # 让 farm 连接通告（21xx 段）到齐

    accounts = list(ib.managedAccounts())
    bad = [a for a in accounts
           if not str(a).upper().startswith(PAPER_ACCT_PREFIXES)]
    # §4B 载荷条款：账户号于呈报件脱敏（paper DU 号亦按此纪律）。verify/ 子树
    # 按 §2 本不得存外部数据，账户号落此即越界——保留前缀（A8 判据）与末三位
    # （可追溯），中段遮蔽。完整值只存在于 probe/ 载荷。
    log = {"host": HOST, "port": port, "client_id": client_id,
           "readonly": True,
           "managed_accounts": [mask_account(a) for a in accounts],
           "non_paper_format": bad,
           "server_version": ib.client.serverVersion(),
           "connected_at": _dt.datetime.now().isoformat(timespec="seconds")}
    os.makedirs(VERIFY_DIR, exist_ok=True)
    with open(CONN_LOG, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    if not accounts:
        ib.disconnect()
        raise PaperGuardError("managedAccounts() 返回空，paper 身份不可证")
    if bad:
        ib.disconnect()
        raise PaperGuardError("命中非 paper 账户格式 %r，A8 FAIL 即停" % (bad,))
    return ib, log


# --------------------------------------------------------------------------
# 合约解析（只读）
# --------------------------------------------------------------------------

def resolve_front_future(ib, symbol, exchange, currency):
    """取前月期货：以 lastTradeDateOrContractMonth 升序取首个未到期者。"""
    cds = ib.reqContractDetails(Future(symbol=symbol, exchange=exchange,
                                       currency=currency))
    if not cds:
        raise RuntimeError("期货合约明细为空：%s@%s" % (symbol, exchange))
    today = _dt.date.today().strftime("%Y%m%d")
    cands = []
    for cd in cds:
        c = cd.contract
        ltd = (c.lastTradeDateOrContractMonth or "")[:8]
        if len(ltd) == 8 and ltd >= today:
            cands.append((ltd, cd))
    if not cands:
        raise RuntimeError("无未到期期货合约（今日=%s）" % today)
    cands.sort(key=lambda t: t[0])
    return cands[0][1], [t[0] for t in cands]


def option_chain_params(ib, und_contract):
    """取期权链参数（FOP）。"""
    return ib.reqSecDefOptParams(und_contract.symbol, und_contract.exchange,
                                 "FUT", und_contract.conId)


def pick_atm_strike(strikes, ref_price):
    """ATM 选取规格（KY 20260812 确认）：|K − F| 最小；平局取较低 K。"""
    if ref_price is None:
        raise RuntimeError("参考价缺位，ATM 不可判——不得以任意值代之")
    ordered = sorted(float(k) for k in strikes)
    return min(ordered, key=lambda k: (abs(k - ref_price), k))


# --------------------------------------------------------------------------
# 行情读取（只读）
# --------------------------------------------------------------------------

def _has_price(t):
    return (not util.isNan(t.last) or not util.isNan(t.close)
            or not util.isNan(t.bid) or not util.isNan(t.ask))


def _has_greeks(t):
    iv = getattr(t, "impliedVolatility", None)
    return (t.modelGreeks is not None
            or (iv is not None and not util.isNan(iv)))


def snapshot_ticker(ib, contract, generic_ticks, wait_s, poll_s,
                    require="price"):
    """订阅并轮询取 ticker 快照。

    **不调用 reqMarketDataType()**：其取值会改变数据语义（实时/冻结/延迟），
    规格件未给定，按 §4A 第2条不得代填；取环境默认行为，拿到什么记什么。

    require＝退出条件（工程参数，非数据语义）：
      "price"  ——首个报价到达即返回（期货定位 ATM 用，不需 greeks）
      "greeks" ——等 greeks／IV 到达；**报价到达不作为退出条件**。
      "all"    ——**不提前退出**，跑满窗口再取。可得性探查（目标1）须用此档：
                 「见一个就走」会把「晚到」误判为「不可得」。此坑已连撞三次
                 （首个 tick 即 break → greeks 假阴性；greeks 即 break →
                 tick24 假阴性），故可得性面一律跑满窗口，不作早退优化。
    """
    ticker = ib.reqMktData(contract, genericTickList=generic_ticks,
                           snapshot=False, regulatorySnapshot=False)
    done = {"greeks": _has_greeks,
            "all": lambda t: False,
            "price": _has_price}[require]
    waited = 0.0
    while waited < wait_s:
        ib.sleep(poll_s)
        waited += poll_s
        if done(ticker):
            break
    return ticker, waited


def ticker_to_dict(ticker):
    """ticker → 可序列化 dict，逐字段如实记录（含 nan，不清洗、不补值）。"""
    def _g(x):
        return None if (x is None or (isinstance(x, float) and util.isNan(x))) else x

    greeks = {}
    for gname in ("modelGreeks", "bidGreeks", "askGreeks", "lastGreeks"):
        g = getattr(ticker, gname, None)
        greeks[gname] = None if g is None else {
            "impliedVol": _g(g.impliedVol), "delta": _g(g.delta),
            "gamma": _g(g.gamma), "vega": _g(g.vega), "theta": _g(g.theta),
            "optPrice": _g(g.optPrice), "undPrice": _g(g.undPrice),
            "pvDividend": _g(g.pvDividend)}

    return {"contract": util.dataclassNonDefaults(ticker.contract),
            "time": str(ticker.time),
            "marketDataType": getattr(ticker, "marketDataType", None),
            "bid": _g(ticker.bid), "bidSize": _g(ticker.bidSize),
            "ask": _g(ticker.ask), "askSize": _g(ticker.askSize),
            "last": _g(ticker.last), "lastSize": _g(ticker.lastSize),
            "close": _g(ticker.close), "open": _g(ticker.open),
            "high": _g(ticker.high), "low": _g(ticker.low),
            "volume": _g(ticker.volume),
            "impliedVolatility": _g(getattr(ticker, "impliedVolatility", None)),
            "greeks": greeks}


def reference_price(tdict):
    """参考价取用序：last → (bid+ask)/2 → close。全缺位则 None（不代填）。"""
    if tdict.get("last") is not None:
        return tdict["last"], "last"
    if tdict.get("bid") is not None and tdict.get("ask") is not None:
        return (tdict["bid"] + tdict["ask"]) / 2.0, "midpoint(bid,ask)"
    if tdict.get("close") is not None:
        return tdict["close"], "close"
    return None, "全缺位"


# --------------------------------------------------------------------------
# q/r 显式赋值闸（§4A 追加-2）
# --------------------------------------------------------------------------

def require_kd_params():
    """组装 lot 之前的机械拦截。文件缺失或任一字段为 null → 即停。

    无任何 fallback 分支：不猜、不用占位值、不用行业惯例默认值。
    """
    path = os.path.join(PROBE_DIR, KD_PARAMS_BASENAME)
    missing = []
    obj = None
    if not os.path.isfile(path):
        missing = list(QR_REQUIRED_FIELDS)
    else:
        try:
            with open(path, "r", encoding="utf-8") as f:
                obj = json.load(f)
        except ValueError as e:
            print("参数文件不可解析：%s（%s）" % (path, e))
            raise SystemExit(2)
        for k in QR_REQUIRED_FIELDS:
            if obj.get(k) is None:
                missing.append(k)
        if obj.get("_kd_supplied") is not True:
            missing.append("_kd_supplied(须为 true)")

    if missing:
        print("=" * 70)
        print("缺参数即停：向KY索取 dividend_yield / risk_free_rate")
        print("缺失项：%s" % (missing,))
        print("唯一取值路径：%s" % path)
        print("规格依据：P1规格件 v1.2 §4A 追加-2（85-1a 不预解之机械化）")
        print("=" * 70)
        raise SystemExit(2)

    return {"dividend_yield": float(obj["dividend_yield"]),
            "risk_free_rate": float(obj["risk_free_rate"]),
            "_basis": obj.get("_basis"),
            "_date": obj.get("_date")}

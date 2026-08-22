# -*- coding: utf-8 -*-
"""P2 探针驱动（probe/ 子树，唯一可落真实数值处）。

规格来源＝P1规格件 v1.2 §5 步2/3/4。

用法：
    python probe/probe_run.py 23    # 步2 连接与合约 ＋ 步3 IV sourcing
    python probe/probe_run.py 4     # 步4 引擎实跑（前置＝q/r 闸）

只读纪律：本文件不引用任何下单侧 API（A7）。
"""

import json
import os
import sys

sys.dont_write_bytecode = True          # 不产生 __pycache__，保 entity/ 面干净
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "entity"))

import probe_harness as H                                        # noqa: E402
import engine                                                    # noqa: E402
from ib_insync import FuturesOption                              # noqa: E402

# ---- 运行配置（皆非市场数值；KY 20260812 确认）---------------------------
PORT = 4002                 # Gateway paper
CLIENT_ID = 2601            # 连接层标识，无语义
SYMBOL = "ES"
EXCHANGE = "CME"
CURRENCY = "USD"
RIGHT = "P"                 # option_type=put（KY 确认）
SIDE = "short"              # side=long/short（KY 确认）
QUANTITY = 1                # 合约张数（KY 确认）
GENERIC_TICKS = "106"       # §5 步3 规格给定
WAIT_S = 15.0
OPT_WAIT_S = 40.0           # greeks 到达通常晚于首个报价，留足窗口
POLL_S = 1.0

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SELECTION_FILE = os.path.join(ROOT, "probe",
                              "contract_selection" + H.MARK + ".json")


def _p(title):
    print("\n" + "-" * 72)
    print("## " + title)
    print("-" * 72)


# =========================================================================
# 步2 ＋ 步3
# =========================================================================

def phase_23():
    _p("步2-1 连接（只读 ＋ A8 paper 双检）")
    ib, conn = H.connect_paper(PORT, CLIENT_ID)
    print("connected: port=%s accounts=%s serverVersion=%s readonly=%s"
          % (conn["port"], conn["managed_accounts"],
             conn["server_version"], conn["readonly"]))
    try:
        _p("步2-2 ES 前月期货 qualify")
        cd, all_expiries = H.resolve_front_future(ib, SYMBOL, EXCHANGE, CURRENCY)
        fut = cd.contract
        print("前月合约: %s %s conId=%s multiplier=%s tradingClass=%s"
              % (fut.symbol, fut.lastTradeDateOrContractMonth, fut.conId,
                 fut.multiplier, fut.tradingClass))
        print("可得到期序列(前6): %s" % all_expiries[:6])

        _p("步2-3 期货快照（供 ATM 定位）")
        f_ticker, waited = H.snapshot_ticker(ib, fut, "", WAIT_S, POLL_S)
        f_dict = H.ticker_to_dict(f_ticker)
        f_dict["_wait_s"] = waited
        f_dict["_all_future_expiries"] = all_expiries
        H.write_payload("es_front_future", f_dict, "step2")
        ref, ref_src = H.reference_price(f_dict)
        print("marketDataType=%s bid=%s ask=%s last=%s close=%s"
              % (f_dict["marketDataType"], f_dict["bid"], f_dict["ask"],
                 f_dict["last"], f_dict["close"]))
        print("参考价=%s（取自 %s）" % (ref, ref_src))
        if ref is None:
            print("\n=== 全量事件流（诊断） ===")
            for ev in H.EVENTS:
                print("  code=%-6s reqId=%-4s %s%s"
                      % (ev["code"], ev["reqId"], ev["msg"],
                         (" [%s]" % ev["contract"]) if ev["contract"] else ""))
            with open(os.path.join(ROOT, "verify", "event_stream.json"),
                      "w", encoding="utf-8") as f:
                json.dump(H.EVENTS, f, ensure_ascii=False, indent=2)
            print("\n[F1 摩擦] 期货参考价全缺位 → ATM 不可判。"
                  "按 §4A 第2条不得以任意值代之，此处停机。")
            return 3

        _p("步2-4 期权链参数（FOP）")
        chains = H.option_chain_params(ib, fut)
        if not chains:
            print("[F1 摩擦] reqSecDefOptParams 返回空")
            return 3
        rows = []
        for ch in chains:
            rows.append({"exchange": ch.exchange,
                         "tradingClass": ch.tradingClass,
                         "multiplier": ch.multiplier,
                         "n_expirations": len(ch.expirations),
                         "n_strikes": len(ch.strikes),
                         "expirations_head": sorted(ch.expirations)[:6]})
            print("chain: exch=%-6s tc=%-5s mult=%-4s exp=%d strikes=%d head=%s"
                  % (ch.exchange, ch.tradingClass, ch.multiplier,
                     len(ch.expirations), len(ch.strikes),
                     sorted(ch.expirations)[:4]))

        import datetime as dt
        today = dt.date.today().strftime("%Y%m%d")
        # 到期选取规则（KY 20260812 处置 B）：dte>=1，**排除当日到期**。
        # 依据：engine `_american_inputs` 于 dte<=0 显式抛「已言明面之外」，
        # 当日到期既阻目标2，又使 IV 面退化而污染目标1。
        cands = []
        for ch in chains:
            for e in ch.expirations:
                if e > today:
                    cands.append((e, ch.tradingClass, ch))
        if not cands:
            print("[F1 摩擦] 无未到期 FOP 到期日")
            return 3
        cands.sort(key=lambda t: (t[0], t[1]))
        exp, tclass, chosen = cands[0]
        strike = H.pick_atm_strike(chosen.strikes, ref)
        print("\n近月选取: expiry=%s tradingClass=%s ATM strike=%s "
              "(参考价=%s, |K-F|=%s)" % (exp, tclass, strike, ref,
                                        abs(strike - ref)))

        _p("步2-5 FOP qualify")
        fop = FuturesOption(symbol=SYMBOL, lastTradeDateOrContractMonth=exp,
                            strike=strike, right=RIGHT, exchange=EXCHANGE,
                            currency=CURRENCY, tradingClass=tclass)
        qualified = ib.qualifyContracts(fop)
        if not qualified:
            print("[F1 摩擦] FOP qualify 失败：%s" % (fop,))
            return 3
        fop = qualified[0]
        print("qualified: conId=%s localSymbol=%s multiplier=%s"
              % (fop.conId, fop.localSymbol, fop.multiplier))

        sel = {"underlying": {"symbol": fut.symbol, "conId": fut.conId,
                              "expiry": fut.lastTradeDateOrContractMonth,
                              "multiplier": fut.multiplier},
               "reference_price": ref, "reference_price_source": ref_src,
               "atm_rule": "|K-F| 最小；平局取较低 K（KY 20260812 确认）",
               "option": {"conId": fop.conId, "localSymbol": fop.localSymbol,
                          "expiry": exp, "strike": strike, "right": RIGHT,
                          "tradingClass": tclass,
                          "multiplier": fop.multiplier},
               "chain_params": rows,
               "lot_shape": {"side": SIDE, "quantity": QUANTITY}}
        H.write_payload("contract_selection", sel, "step2")

        _p("步3 IV sourcing 探查（genericTickList=%s）" % GENERIC_TICKS)
        o_ticker, waited = H.snapshot_ticker(ib, fop, GENERIC_TICKS,
                                             OPT_WAIT_S, POLL_S,
                                             require="all")
        o_dict = H.ticker_to_dict(o_ticker)
        o_dict["_wait_s"] = waited
        o_dict["_generic_tick_list"] = GENERIC_TICKS
        H.write_payload("fop_iv_sourcing", o_dict, "step3")

        print("marketDataType=%s" % o_dict["marketDataType"])
        print("bid=%s ask=%s last=%s close=%s volume=%s"
              % (o_dict["bid"], o_dict["ask"], o_dict["last"],
                 o_dict["close"], o_dict["volume"]))
        print("impliedVolatility(tick24)=%s" % o_dict["impliedVolatility"])
        for gname, g in o_dict["greeks"].items():
            print("  %-11s: %s" % (gname, g))

        got_iv = (o_dict["impliedVolatility"] is not None
                  or (o_dict["greeks"]["modelGreeks"] or {}).get("impliedVol")
                  is not None)
        print("\nIV 可得性 = %s（采集环境=%s）"
              % ("可得" if got_iv else "不可得", H.CAPTURE_ENV))
        return 0
    finally:
        ib.disconnect()
        print("\n[disconnected]")


# =========================================================================
# 诊断：tick 106 / tick 24 / greeks 归属之对照实测
# =========================================================================

def phase_diag():
    """三组对照，钉死「IV 从哪条路出来」：
      (1) 期权 + genericTickList=""    → 不点 106，greeks 是否照来？
      (2) 期权 + genericTickList="106" → 与 (1) 有无差异？
      (3) 期货 + genericTickList="106" → tick 24 是否落在标的侧？
    """
    if not os.path.isfile(SELECTION_FILE):
        print("[停机] 合约选取载荷不在场，先跑 step 23")
        return 3
    with open(SELECTION_FILE, "r", encoding="utf-8") as f:
        sel = json.load(f)

    from ib_insync import Contract
    ib, _ = H.connect_paper(PORT, CLIENT_ID)
    try:
        fop = Contract(conId=sel["option"]["conId"], exchange=EXCHANGE)
        fut = Contract(conId=sel["underlying"]["conId"], exchange=EXCHANGE)
        ib.qualifyContracts(fop, fut)

        out = {}
        for tag, con, ticks, req in (
                ("opt_no106", fop, "", "greeks"),
                ("opt_106", fop, "106", "greeks"),
                ("fut_106", fut, "106", "price")):
            t, waited = H.snapshot_ticker(ib, con, ticks, 25.0, POLL_S,
                                          require=req)
            d = H.ticker_to_dict(t)
            out[tag] = {"generic_ticks": ticks, "waited_s": waited,
                        "tick24_impliedVolatility": d["impliedVolatility"],
                        "modelGreeks": d["greeks"]["modelGreeks"],
                        "bidGreeks": d["greeks"]["bidGreeks"],
                        "raw_sentinel_check": {
                            g: (v or {}).get("vega")
                            for g, v in d["greeks"].items()}}
            ib.cancelMktData(con)
            ib.sleep(1.0)
            print("\n[%s] genericTickList=%r 等待=%.0fs" % (tag, ticks, waited))
            print("  tick24 impliedVolatility = %s"
                  % out[tag]["tick24_impliedVolatility"])
            mg = out[tag]["modelGreeks"]
            print("  modelGreeks.impliedVol   = %s"
                  % (mg.get("impliedVol") if mg else None))
            print("  modelGreeks 全字段        = %s" % mg)

        a = out["opt_no106"]["modelGreeks"] or {}
        b = out["opt_106"]["modelGreeks"] or {}
        print("\n=== 结论面 ===")
        print("不点106 期权 greeks 可得: %s" % bool(a))
        print("点106   期权 greeks 可得: %s" % bool(b))
        print("两者 impliedVol: %s vs %s" % (a.get("impliedVol"),
                                             b.get("impliedVol")))
        print("期货侧 tick24: %s" % out["fut_106"]["tick24_impliedVolatility"])
        H.write_payload("tick_route_diag", out, "diag")
        return 0
    finally:
        ib.disconnect()
        print("\n[disconnected]")


# =========================================================================
# 步4：引擎实跑（前置＝q/r 闸）
# =========================================================================

def phase_4():
    _p("步4-0 q/r 显式赋值闸（§4A 追加-2）")
    params = H.require_kd_params()          # 缺参即 SystemExit(2)，无 fallback
    if params is None:                      # 防御：闸不得静默放行
        raise SystemExit(2)
    print("KD 赋值到位：dividend_yield=%s risk_free_rate=%s 依据=%s"
          % (params["dividend_yield"], params["risk_free_rate"],
             params["_basis"]))

    if not os.path.isfile(SELECTION_FILE):
        print("[停机] 合约选取载荷不在场，先跑 step 23")
        return 3
    with open(SELECTION_FILE, "r", encoding="utf-8") as f:
        sel = json.load(f)
    iv_file = os.path.join(ROOT, "probe", "fop_iv_sourcing" + H.MARK + ".json")
    with open(iv_file, "r", encoding="utf-8") as f:
        ivp = json.load(f)

    # 口径选取（KY 20260812 决定2/3）：spot 与 implied_vol 同取 modelGreeks，
    # 即 IB 同一次模型计算之自洽三元组（undPrice, impliedVol, optPrice）；
    # 残差因此可被隔离到 q/r 假设＋day count＋模型差异三项，为待答项材料。
    # 不取 tick24（不配对 undPrice）、不取期货 last（合约选取用价，非估值用价）。
    mg = (ivp.get("greeks", {}) or {}).get("modelGreeks") or {}
    spot = mg.get("undPrice")
    iv = mg.get("impliedVol")
    if spot is None or iv is None:
        print("[停机] modelGreeks 三元组不全（undPrice=%s implied_vol=%s），"
              "按 §4A 第2条不得代填" % (spot, iv))
        return 3
    ib_model_price = mg.get("optPrice")

    import datetime as dt
    valuation_date = dt.date.today().strftime("%Y-%m-%d")
    e = sel["option"]["expiry"]
    expiry = "%s-%s-%s" % (e[:4], e[4:6], e[6:8])

    # @LOT_ASSEMBLY_POINT  —— 闸之后方得组装（A9 序位检测锚）
    lot = {"lot_id": "P2_ES_FOP_001",
           "instrument_class": "american_option",
           "exercise_style": "american",
           "option_type": "put" if RIGHT == "P" else "call",
           "spot": spot,
           "strike": sel["option"]["strike"],
           "implied_vol": iv,
           "valuation_date": valuation_date,
           "expiry": expiry,
           "risk_free_rate": params["risk_free_rate"],
           "dividend_yield": params["dividend_yield"],
           "multiplier": int(float(sel["option"]["multiplier"])),
           "quantity": QUANTITY,
           "side": SIDE}

    _p("步4-1 engine.evaluate_lot 实跑（CRR 路径）")
    for k in sorted(lot):
        print("  %-18s = %r" % (k, lot[k]))
    out = engine.evaluate_lot(lot)
    print("\n返回：")
    print(json.dumps(out, ensure_ascii=False, indent=2, default=str))

    diag = out.get("lattice_diagnostics", {})
    print("\n=== 目标2：美式判断点 ===")
    print("提前行权节点数         = %s" % diag.get("n_exercise_nodes"))
    print("欧式模式对照组节点数   = %s" % diag.get("european_mode_n_exercise_nodes"))
    print("最大行权超额           = %s" % diag.get("max_exercise_excess"))
    print("判断点经过与否         = %s"
          % ("经过" if diag.get("n_exercise_nodes") else "未经过"))

    print("\n=== 待答项材料：engine 值 vs IB 模型值 ===")
    ev = out.get("per_unit", {}).get("value")
    print("engine CRR per_unit.value = %r" % ev)
    print("IB modelGreeks.optPrice   = %r" % ib_model_price)
    if ev is not None and ib_model_price is not None:
        print("残差 (engine - IB)        = %r" % (ev - ib_model_price))
        print("注：残差含 q/r 假设差＋day count 差＋模型差三项，本发不拆分。")

    H.write_payload("engine_run",
                    {"lot": lot, "result": out,
                     "kd_params_basis": params["_basis"],
                     "kd_params_pending_review": True,
                     "ib_model_optPrice": ib_model_price,
                     "residual_engine_minus_ib":
                         (ev - ib_model_price)
                         if (ev is not None and ib_model_price is not None)
                         else None},
                    "step4")
    return 0


# =========================================================================
# 步6：X-2 账户报表字段结构探查（目标4，只读）
# =========================================================================

def phase_x2():
    ib, conn = H.connect_paper(PORT, CLIENT_ID)
    try:
        acct = ib.managedAccounts()[0]
        out = {"account": acct}

        # 账户面数据于 connect 后异步到达；持仓面须显式订阅。前版未等即读，
        # 得 0 记录之假阴性（与摩擦-04 同类：早读＝假阴性）。此处跑满等待。
        _p("步6-0 等待账户面与持仓面到齐")
        ib.reqPositions()
        waited = 0.0
        while waited < 25.0:
            if ib.accountValues(acct) and ib.accountSummary(acct):
                break
            ib.sleep(1.0)
            waited += 1.0
        ib.sleep(3.0)          # 持仓面再留一拍
        print("等待=%.0fs accountValues=%d accountSummary=%d positions=%d"
              % (waited, len(ib.accountValues(acct)),
                 len(ib.accountSummary(acct)), len(ib.positions(acct))))

        _p("步6-1 accountSummary 字段结构")
        summary = ib.accountSummary(acct)
        out["accountSummary"] = [{"tag": r.tag, "currency": r.currency,
                                  "value": r.value, "modelCode": r.modelCode}
                                 for r in summary]
        tags = sorted({r.tag for r in summary})
        print("字段数=%d 唯一 tag=%d" % (len(summary), len(tags)))
        print("tags: %s" % tags)

        _p("步6-2 accountValues 字段结构")
        values = ib.accountValues(acct)
        out["accountValues_keys"] = sorted({v.tag for v in values})
        out["accountValues_currencies"] = sorted({v.currency for v in values})
        out["accountValues"] = [{"tag": v.tag, "currency": v.currency,
                                 "value": v.value} for v in values]
        print("记录数=%d 唯一 tag=%d 币种=%s"
              % (len(values), len(out["accountValues_keys"]),
                 out["accountValues_currencies"]))
        print("tag 前40: %s" % out["accountValues_keys"][:40])

        _p("步6-3 持仓面字段结构")
        positions = ib.positions(acct)
        portfolio = ib.portfolio()
        out["position_fields"] = list(positions[0].__class__.__annotations__) \
            if positions else []
        out["portfolio_fields"] = list(portfolio[0].__class__.__annotations__) \
            if portfolio else []
        out["positions"] = [{"account": p.account, "conId": p.contract.conId,
                             "localSymbol": p.contract.localSymbol,
                             "secType": p.contract.secType,
                             "position": p.position, "avgCost": p.avgCost}
                            for p in positions]
        print("positions=%d 字段=%s" % (len(positions), out["position_fields"]))
        print("portfolio=%d 字段=%s" % (len(portfolio), out["portfolio_fields"]))

        _p("步6-4 FlexQuery")
        out["flex_query"] = {
            "handled_by": "probe/probe_flex.py",
            "clause": "P1规格件 v1.3 §4B（凭据走运行时环境变量，闸＝"
                      "require_flex_credentials；HTTPS 通道故落 probe/ 子树）"}
        print("FlexQuery 走 probe/probe_flex.py（§4B），本相不处理。")

        H.write_payload("x2_report_fields", out, "step6")
        return 0
    finally:
        ib.disconnect()
        print("\n[disconnected]")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "23"
    sys.exit({"23": phase_23, "4": phase_4, "diag": phase_diag,
              "6": phase_x2}[which]())

# -*- coding: utf-8 -*-
# =====================================================================
# P2' · 曳光弹第二发（QC）· 回测运行位探针算法
# =====================================================================
# 面标记（KD-P2-10 检测位 4）：本件为**接口面**代码。
_P2P_FACE = "interface"
# ---------------------------------------------------------------------
# 本件落位＝probe/（A'-6：QC 接口面代码全部落 probe/）。
# 上云依据＝KD-P2-10 裁定：云端承载面 ＝ entity/ 面 ＋ probe/ 之**接口面代码子集**。
# 本件为该子集之唯一成员。
#
# 禁作面自守（作业指令 §2）：
#   · 零交易逻辑、零下单、零持仓、零 vendor 行情订阅。
#   · 零收益／夏普／回撤类指标采集（85-9 反面条款）。
#   · 零 L3 判据、零 L3 实体、零合格判定。
#   · 不产出「成功／失败」二值结论，不作「环境可用／不可用」总体判定。
#   · 零真实数值、零外部数据载荷、零凭据字面（KD-P2-10 检测位 2）。
#
# 本件职能＝**通道探测**：逐条调用已在云端之纯人造 runner，逐条记录
# exit 状态与错误原文；各条 try/except 隔离，互不连坐。
# =====================================================================
from AlgorithmImports import *   # noqa: F401,F403

import json
import os
import sys
import traceback

CHUNK = 400          # 日志分片长度
RT_CHUNK = 180       # runtimeStatistic 单值分片长度（上限未知，本轮同时探其上限）
MARK = "P2PPROBE"

# 回传通道说明（本轮变更，KD 20260818 选路径 2）：
#   日志通道实测受限——free 档 **10kb/回测 且 10kb/天**（截断告示原文），今日已耗尽。
#   故改以 SetRuntimeStatistic 承载结构化结果，经 A 类端点 backtests/read 之
#   runtimeStatistics 取回。日志通道保留为旁证（今日预期为空，不依赖）。


class P2PrimeProbeAlgorithm(QCAlgorithm):

    # ---------------- 输出通道 ----------------
    def _emit(self, tag, obj):
        """结构化结果分片回传。分片带序号，便于本地无损重组。"""
        s = json.dumps(obj, ensure_ascii=False, sort_keys=True, default=str)
        n = (len(s) + CHUNK - 1) // CHUNK
        self.Debug("%s|%s|BEGIN|%d|%d" % (MARK, tag, n, len(s)))
        for i in range(n):
            self.Debug("%s|%s|%04d|%s" % (MARK, tag, i, s[i * CHUNK:(i + 1) * CHUNK]))
        self.Debug("%s|%s|END" % (MARK, tag))

    def _emit_rt(self, tag, obj):
        """经 runtimeStatistics 回传（不吃日志配额）。分片带序号，本地无损重组。"""
        s = json.dumps(obj, ensure_ascii=False, sort_keys=True, default=str,
                       separators=(",", ":"))
        n = (len(s) + RT_CHUNK - 1) // RT_CHUNK
        try:
            self.SetRuntimeStatistic("P2P_%s_HDR" % tag, "%d/%d" % (n, len(s)))
            for i in range(n):
                self.SetRuntimeStatistic("P2P_%s_%03d" % (tag, i),
                                         s[i * RT_CHUNK:(i + 1) * RT_CHUNK])
        except Exception as e:
            try:
                self.SetRuntimeStatistic("P2P_%s_ERR" % tag, "%s: %s" % (type(e).__name__, str(e)[:150]))
            except Exception:
                pass

    def _probe_rt(self, tag, fn):
        """逐条隔离执行 + 双通道回传（runtimeStatistic 主，Debug 旁证）。"""
        try:
            r = {"status": "ok", "result": fn()}
        except Exception as e:
            r = {"status": "error", "error_type": type(e).__name__,
                 "error_text": str(e)[:400], "traceback": traceback.format_exc()[:600]}
        self._emit_rt(tag, r)
        self._emit(tag, r)

    def _probe(self, tag, fn):
        """逐条隔离执行：任一条抛出不影响其余条（不连坐）。"""
        try:
            self._emit(tag, {"status": "ok", "result": fn()})
        except Exception as e:
            self._emit(tag, {"status": "error",
                             "error_type": type(e).__name__,
                             "error_text": str(e),
                             "traceback": traceback.format_exc()})

    # ---------------- 生命周期 ----------------
    def Initialize(self):
        # 最小回测窗；零证券、零行情订阅、零下单。
        self.SetStartDate(2020, 1, 6)
        self.SetEndDate(2020, 1, 7)
        self.SetCash(100000)

        for p in (os.getcwd(), "/Lean/Launcher/bin/Debug", "."):
            if p not in sys.path:
                sys.path.insert(0, p)

        # 发射顺序：两个缺口（X-1 per_unit ／ α-1(iii)）排最前，
        # 万一新通道亦有上限，先保缺口（上轮教训：配额在 X1 中途耗尽）。
        # 本轮射程＝α-2（路径系综规模与遍历）＋ α-3（五量所需账本接口在场性）。
        # 前轮已完成项不重跑，省体积。
        self._pathcount = {}
        self._probe_rt("A2SET", self._t_alpha2_setup)
        self._probe_rt("A3LED", self._t_alpha3_ledger_ifaces)

    def OnData(self, data):
        # α-2：逐路径计数——按 symbol 分别累计到达点数，证「N 条指定路径可分辨取回」。
        try:
            for sym in data.Keys:
                k = str(sym)
                self._pathcount[k] = self._pathcount.get(k, 0) + 1
            # 保险：A2RUN 若只挂 OnEndOfAlgorithm，再遇运行时错误即丢（上轮教训）。
            # SetRuntimeStatistic 按键覆盖，故此处重复发射无害、末次为准。
            if self._pathcount:
                self._emit_rt("A2RUN", {"status": "ok", "result": {
                    "per_path_points": self._pathcount,
                    "paths_seen": len(self._pathcount),
                    "getsource_seen": P2PSyntheticData._SEEN[:6],
                    "srcmap_keys": sorted(P2PSyntheticData._SRCMAP),
                    "_emitted_from": "OnData(增量，末次为准)",
                }})
        except Exception:
            pass

    def OnEndOfAlgorithm(self):
        # α-2 结果须在回测走完后方可得，故于此发射。
        self._probe_rt("A2RUN", lambda: {
            "per_path_points": self._pathcount,
            "paths_seen": len(self._pathcount),
            "getsource_seen": P2PSyntheticData._SEEN[:6],
            "srcmap_keys": sorted(P2PSyntheticData._SRCMAP),
        })
        self.Debug("%s|DONE" % MARK)

    # ---------------- 探测项 ----------------
    def _t_env(self):
        """运行位环境指纹（回测运行时；DOC-25 之 E1-01 补齐通道）。"""
        import platform
        return {
            "python_version": sys.version.split()[0],
            "python_version_full": sys.version.replace("\n", " "),
            "python_build": list(platform.python_build()),
            "python_compiler": platform.python_compiler(),
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "machine": platform.machine(),
            "libc_ver": list(platform.libc_ver()),
            "cwd": os.getcwd(),
            "listdir_cwd": sorted(os.listdir(os.getcwd()))[:60],
            "sys_path_head": sys.path[:8],
        }

    def _t_a1_inline_import(self):
        """α-1 候选 (i)：`.py` 内嵌常量注入——回测位可否 import 载体件并逐字节还原。"""
        out = {}
        for mod_name, keys in (("cloud_payload_gl06", None), ("cloud_payload_engine", None),
                               ("cloud_payload_x1", None)):
            try:
                m = __import__(mod_name)
                names = sorted(m.PAYLOAD.keys()) if keys is None else keys
                restored = {}
                for n in names:
                    raw = m.restore(n)          # 内含 SHA256 自核，不一致即抛
                    restored[n] = {"size": len(raw),
                                   "sha256": m.PAYLOAD[n]["sha256"]}
                out[mod_name] = {"import": "ok", "restored": restored}
            except Exception as e:
                out[mod_name] = {"import": "error", "error_type": type(e).__name__,
                                 "error_text": str(e)}
        return out

    def _t_a1_objectstore_read(self):
        """α-1 候选 (ii)：算法侧读 ObjectStore。

        **零写入**：不调用 ObjectStore 之 Save/Set/Delete。读取对象＝探测期既有遗留物
        `/tr2probe-e14-marker.txt`（E1-17，A'-12 不清理），故本项**不产生任何新遗留物**。
        待答问题＝规格件 E1-12 明载之「**回测 job 侧读权限未测**」。
        """
        res = {"write_attempted": False,
               "read_target": "tr2probe-e14-marker.txt（探测期遗留物，非本发新建）"}
        try:
            keys = []
            try:
                for k in self.ObjectStore:
                    keys.append(getattr(k, "Key", str(k)))
            except Exception as e:
                res["enumerate_error"] = "%s: %s" % (type(e).__name__, e)
            res["enumerated_keys"] = keys[:20]

            for name in ("tr2probe-e14-marker.txt", "/tr2probe-e14-marker.txt"):
                try:
                    exists = self.ObjectStore.ContainsKey(name)
                except Exception as e:
                    res["contains_%s" % name] = "ERR %s: %s" % (type(e).__name__, e)
                    continue
                res["contains_%s" % name] = exists
                if exists:
                    try:
                        txt = self.ObjectStore.Read(name)
                        res["read_%s" % name] = {"ok": True, "len": len(txt or "")}
                    except Exception as e:
                        res["read_%s" % name] = {"ok": False,
                                                 "error_type": type(e).__name__,
                                                 "error_text": str(e)}
        except Exception as e:
            res["fatal"] = "%s: %s" % (type(e).__name__, e)
        return res

    def _t_alpha6(self):
        """α-6-甲：载体根 GL-06 于**回测运行位**之可运行性（双值并列，KD-P2-06）。"""
        import cloud_runner_alpha6 as R
        return R.run_alpha6()

    def _t_x1(self):
        """X-1-甲：engine v1.3 于**回测运行位**实跑，产逐位输出与环境指纹。"""
        import cloud_runner_x1 as R
        return R.run_x1()

    def _t_alpha2_setup(self):
        """α-2：同一回测项目内驱动 **N≥2 条指定路径**（自造确定性序列，非随机、非市场历史）。

        每条路径 ＝ 一份钉定的人造数值序列，逐条以独立 symbol 注入。
        本函数只负责注入与登记；逐路径到达点数于 OnEndOfAlgorithm 发射（A2RUN）。
        零市场数据、零 vendor 格式、零随机数。
        """
        import tempfile
        PATHS = {
            "P2PATH1": ["1.0", "2.0", "3.0", "4.0"],
            "P2PATH2": ["10.0", "20.0", "30.0", "40.0"],
            "P2PATH3": ["100.0", "200.0", "300.0", "400.0"],
        }
        STAMPS = ["2020-01-06 09:31", "2020-01-06 09:32",
                  "2020-01-06 09:33", "2020-01-06 09:34"]
        res = {"n_paths": len(PATHS), "deterministic": True, "source": "自造确定性序列"}
        d = tempfile.mkdtemp(prefix="p2p_paths_")
        # 兜底源：确保 GetSource 任何分支都不会拿到 None（BUG-P2-06 修正）
        fb = os.path.join(d, "_fallback.csv")
        with open(fb, "w") as f:
            f.write("2020-01-06 09:31,0.0")
        P2PSyntheticData._FALLBACK = fb
        for name, vals in PATHS.items():
            try:
                fp = os.path.join(d, "%s.csv" % name)
                with open(fp, "w") as f:
                    f.write(chr(10).join("%s,%s" % (t, v) for t, v in zip(STAMPS, vals)))
                P2PSyntheticData._SRCMAP[name] = fp
                sym = self.AddData(P2PSyntheticData, name, Resolution.Minute)
                res[name] = {"add": "ok", "rows": len(vals),
                             "symbol": str(getattr(sym, "Symbol", sym))}
            except Exception as e:
                res[name] = {"add": "error", "et": type(e).__name__, "ex": str(e)[:160]}
        return res

    def _t_alpha3_ledger_ifaces(self):
        """α-3：五量之**占位表达**与所需账本接口在场性。

        **禁作面自守（规格件 §3.1）**：本函数**不定义任何量之判据、不取阈值、不设分桶法、
        不写路径生成器规格**。只做两件事：
          (a) 探「持仓账本／现金流水／成交明细」三类接口是否在场且可读；
          (b) 对五量各写一个**纯账本量占位表达式**，只验「能否在本环境内写出并产出数值」。
        占位表达式之语义**不构成**该量之定义。
        """
        res = {"_disclaimer": "占位表达，非判据；零阈值、零分桶法、零路径生成器规格"}

        def probe(name, fn):
            try:
                res[name] = {"iface": "present", "value": fn()}
            except Exception as e:
                res[name] = {"iface": "absent_or_error", "et": type(e).__name__, "ex": str(e)[:120]}

        # --- (a) 三类账本接口在场性
        probe("if_holdings", lambda: len(list(self.Portfolio.Values)))
        probe("if_cashbook", lambda: len(list(self.Portfolio.CashBook.Keys)))
        probe("if_transactions", lambda: len(list(self.Transactions.GetOrders())))
        probe("if_totalfees", lambda: float(self.Portfolio.TotalFees))
        probe("if_totalportfolio", lambda: float(self.Portfolio.TotalPortfolioValue))
        probe("if_cash", lambda: float(self.Portfolio.Cash))

        # --- (b) 五量占位表达（纯账本量：持仓量／现金流水／名义量；零定价模型量，L3 铁律2）
        probe("q_coverage_placeholder",
              lambda: sum(abs(float(h.Quantity)) for h in self.Portfolio.Values))
        probe("q_netfeed_placeholder",
              lambda: float(self.Portfolio.Cash) - float(self.Portfolio.TotalFees))
        probe("q_lefttail_ramp_placeholder",
              lambda: len([h for h in self.Portfolio.Values if float(h.Quantity) < 0]))
        probe("q_righttail_gap_placeholder",
              lambda: sum(abs(float(h.HoldingsValue)) for h in self.Portfolio.Values))
        probe("q_identity_presence_placeholder",
              lambda: len({str(h.Symbol) for h in self.Portfolio.Values}))
        return res

    def _t_x1_compact(self):
        """X-1-甲 紧凑素材：仅 env 四项 ＋ libm 探针 ＋ engine_sha ＋ per_unit 逐位。
        砍掉 fixture 回显、provenance、disclaimer 等——上轮即因体积超限被截断。"""
        import cloud_runner_x1 as R
        r = R.run_x1()
        rep = r.get("report") or {}
        env = rep.get("environment") or {}
        rb = rep.get("result_bitwise") or {}
        pu = rb.get("per_unit") or {}
        return {
            "em": r.get("exec_mode"),
            "rc": r.get("x1_synth_exit_code"),
            "esha": rep.get("engine_sha256"),
            "pv": env.get("python_version"), "pc": env.get("python_compiler"),
            "pf": env.get("platform"), "lc": env.get("libc_ver"),
            "ld": env.get("libm_fingerprint_digest"),
            "lm": env.get("libm_fingerprints"),
            "pu": {k: [v.get("repr"), v.get("hex")] for k, v in pu.items() if isinstance(v, dict)},
            "rt": rb.get("route_id"), "cs": rb.get("computability_status"),
            "ud": rb.get("unstated_dimensions_hit"),
        }

    def _t_alpha6_compact(self):
        """α-6-甲 紧凑素材：双值 ＋ newline profile ＋ 三哈希（KD-P2-06 口径）。"""
        import cloud_runner_alpha6 as R
        r = R.run_alpha6()
        return {"em": r.get("exec_mode"), "rc": r.get("harness_exit_code"),
                "be": r.get("byte_exact"), "ben": r.get("byte_exact_normalized"),
                "nl": r.get("newline_profile"),
                "ps": r.get("produced_sha256"), "es": r.get("expected_sha256"),
                "ns": r.get("normalized_produced_sha256")}

    def _t_env_compact(self):
        import platform
        return {"pv": sys.version.split()[0], "pc": platform.python_compiler(),
                "pf": platform.platform(), "lc": list(platform.libc_ver()),
                "mc": platform.machine(), "cwd": os.getcwd()}

    def _t_rt_limit_probe(self):
        """α-4 材料：探 runtimeStatistic 之单值长度上限与键数上限（本身即回传通道开销材料）。"""
        res = {}
        for n in (100, 200, 400, 800, 1600):
            try:
                self.SetRuntimeStatistic("P2P_LIMPROBE_%d" % n, "x" * n)
                res["set_%d" % n] = "ok"
            except Exception as e:
                res["set_%d" % n] = "%s: %s" % (type(e).__name__, str(e)[:100])
        return res

    def _t_a1_adddata(self):
        """α-1 候选 (iii)：自定义数据类型 `AddData` 路径。

        数据源＝**自造确定性序列**（人造常量，非市场数据、非 vendor 数据）。
        零行情订阅、零 vendor 数据格式。仅测「回测器能否吃自造序列」这一通道面。
        """
        import tempfile
        rows = ["2020-01-06 09:31,1.0", "2020-01-06 09:32,2.0", "2020-01-06 09:33,3.0"]
        res = {"synthetic_rows": len(rows), "source": "自造确定性序列（人造常量）"}
        try:
            d = tempfile.mkdtemp(prefix="p2p_adddata_")
            path = os.path.join(d, "p2p_synth.csv")
            with open(path, "w") as f:
                f.write("\n".join(rows))
            res["temp_write"] = {"ok": True, "path_exists": os.path.exists(path),
                                 "bytes": os.path.getsize(path)}
            P2PSyntheticData._SRC = path
            sym = self.AddData(P2PSyntheticData, "P2PSYNTH", Resolution.Minute)
            res["add_data"] = {"ok": True,
                               "symbol": str(getattr(sym, "Symbol", sym))}
        except Exception as e:
            res["add_data"] = {"ok": False, "error_type": type(e).__name__,
                               "error_text": str(e), "traceback": traceback.format_exc()}
        return res


class P2PSyntheticData(PythonData):
    """自造确定性序列之自定义数据类型。零市场数据、零 vendor 格式、零随机数。"""
    _SRC = None
    _SRCMAP = {}          # α-2：symbol -> 该条路径之钉定序列文件
    _FALLBACK = None      # 兜底源：确保永不向 SubscriptionDataSource 传 None
    _SEEN = []            # 诊断：GetSource 实际见到之 symbol 字面（α-2 材料）

    def GetSource(self, config, date, isLive):
        # 本位缺陷修正（BUG-P2-06）：前轮 GetSource 在查找落空时把 None 传给
        # SubscriptionDataSource，触发 `Value cannot be null (Parameter 'input')`
        # 于 CloudDataPermissionManager.cs:92。此处改为多形候选匹配 ＋ 兜底源，永不传 None。
        cands = []
        for f in (lambda: str(config.Symbol.Value), lambda: str(config.Symbol)):
            try:
                v = f()
                if v and v not in cands:
                    cands.append(v)
            except Exception:
                pass
        if len(P2PSyntheticData._SEEN) < 12:
            P2PSyntheticData._SEEN.append(cands[:2])
        src = None
        for c in cands:
            cu = c.upper()
            for k, v in P2PSyntheticData._SRCMAP.items():
                if cu.startswith(k) or k in cu:
                    src = v
                    break
            if src:
                break
        if src is None:
            src = P2PSyntheticData._SRC or P2PSyntheticData._FALLBACK
        return SubscriptionDataSource(src, SubscriptionTransportMedium.LocalFile)

    def Reader(self, config, line, date, isLive):
        if not line or "," not in line:
            return None
        try:
            ts, val = line.split(",", 1)
            d = P2PSyntheticData()
            d.Symbol = config.Symbol
            d.Time = datetime.strptime(ts.strip(), "%Y-%m-%d %H:%M")
            d.Value = float(val)
            return d
        except Exception:
            return None

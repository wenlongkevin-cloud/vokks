# strategy/trend_ma.py
# Marlong — 趋势策略：MA金叉/死叉 + MACD过零轴确认 + 量能过滤

import pandas as pd
from strategy.base import BaseStrategy
from indicators.ma import add_ma
from indicators.macd import add_macd
from indicators.volume import add_volume_indicators
from indicators.sar import add_sar


class TrendMAStrategy(BaseStrategy):
    """
    趋势跟随策略（适合 A股日线级别趋势交易）

    入场条件（全部满足）：
      1. MA5 上穿 MA20（金叉）
      2. MACD DIFF > 0（多头区域）或 MACD 金叉
      3. SAR 在价格下方（多头 SAR）
      4. 非缩量（量比 >= 0.7）

    出场条件（任一满足）：
      1. MA5 下穿 MA20（死叉）
      2. SAR 翻空（sar_bull 由 True 变 False）
      3. 风控模块触发止损止盈（由回测引擎处理）
    """

    def prepare(self, df: pd.DataFrame) -> pd.DataFrame:
        cfg = self.config
        df = add_ma(df, periods=cfg.get("ma_periods", [5, 20, 60, 250]))
        df = add_macd(
            df,
            fast=cfg.get("macd_fast", 12),
            slow=cfg.get("macd_slow", 26),
            signal=cfg.get("macd_signal", 9),
        )
        df = add_volume_indicators(df)
        df = add_sar(
            df,
            af=cfg.get("sar_af", 0.02),
            max_af=cfg.get("sar_max_af", 0.2),
        )
        return df

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        df["signal"] = 0

        # --- 金叉条件 ---
        ma5_cross_up = (df["ma5"] > df["ma20"]) & (df["ma5"].shift(1) <= df["ma20"].shift(1))

        # --- MACD 确认：DIFF > 0 或刚金叉 ---
        macd_ok = (df["diff"] > 0) | (df["macd_cross"] == 1)

        # --- SAR 多头 ---
        sar_ok = df["sar_bull"]

        # --- 量能不过度萎缩 ---
        vol_ok = ~df["vol_shrink"].fillna(False)

        # 买入信号
        buy = ma5_cross_up & macd_ok & sar_ok & vol_ok
        df.loc[buy, "signal"] = 1

        # --- 死叉条件 ---
        ma5_cross_down = (df["ma5"] < df["ma20"]) & (df["ma5"].shift(1) >= df["ma20"].shift(1))

        # --- SAR 翻空 ---
        sar_flip_bear = (~df["sar_bull"]) & (df["sar_bull"].shift(1))

        # 卖出信号（任意一个触发）
        sell = ma5_cross_down | sar_flip_bear
        df.loc[sell, "signal"] = -1

        return df

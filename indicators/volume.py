# indicators/volume.py
# Marlong — 成交量类指标

import pandas as pd
import numpy as np


def add_volume_indicators(df: pd.DataFrame, ma_periods: list[int] = [5, 20]) -> pd.DataFrame:
    """
    添加量能指标：
    - obv          : On-Balance Volume
    - vol_ma{n}    : 成交量均线
    - amount_ma{n} : 成交额均线
    - vol_ratio    : 量比（当日成交量 / 过去5日均量）
    - vol_expand   : 放量标志（量比 > 1.5）
    - vol_shrink   : 缩量标志（量比 < 0.7）
    """
    # OBV
    direction = np.sign(df["close"].diff().fillna(0))
    df["obv"] = (direction * df["volume"]).cumsum()

    # 成交量均线 & 成交额均线
    for p in ma_periods:
        df[f"vol_ma{p}"] = df["volume"].rolling(p).mean()
        if "amount" in df.columns:
            df[f"amount_ma{p}"] = df["amount"].rolling(p).mean()

    # 量比
    df["vol_ratio"] = df["volume"] / df["volume"].rolling(5).mean()
    df["vol_expand"] = df["vol_ratio"] > 1.5
    df["vol_shrink"] = df["vol_ratio"] < 0.7

    return df

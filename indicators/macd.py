# indicators/macd.py
# Marlong — MACD 指标

import pandas as pd


def add_macd(
    df: pd.DataFrame,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> pd.DataFrame:
    """
    添加 MACD 指标列：diff / dea / macd_bar / macd_cross。

    - diff      : 快线（EMA12 - EMA26）
    - dea       : 慢线（diff 的 9日EMA，即 Signal Line）
    - macd_bar  : MACD 柱（diff - dea）* 2
    - macd_cross: +1 金叉 / -1 死叉 / 0 无信号
    """
    ema_fast = df["close"].ewm(span=fast, adjust=False).mean()
    ema_slow = df["close"].ewm(span=slow, adjust=False).mean()

    df["diff"] = ema_fast - ema_slow
    df["dea"] = df["diff"].ewm(span=signal, adjust=False).mean()
    df["macd_bar"] = (df["diff"] - df["dea"]) * 2

    # 金叉/死叉信号
    cross = pd.Series(0, index=df.index)
    cross[(df["diff"] > df["dea"]) & (df["diff"].shift(1) <= df["dea"].shift(1))] = 1   # 金叉
    cross[(df["diff"] < df["dea"]) & (df["diff"].shift(1) >= df["dea"].shift(1))] = -1  # 死叉
    df["macd_cross"] = cross

    return df

# indicators/ma.py
# Marlong — 移动均线指标

import pandas as pd


def add_ma(df: pd.DataFrame, periods: list[int] = [5, 20, 60, 250]) -> pd.DataFrame:
    """
    在 DataFrame 上添加简单移动均线列：ma5, ma20, ma60, ma250。

    Args:
        df:      包含 close 列的 DataFrame
        periods: 均线周期列表

    Returns:
        原 DataFrame（in-place 添加列）
    """
    for p in periods:
        df[f"ma{p}"] = df["close"].rolling(window=p, min_periods=p).mean()
    return df


def ma_slope(df: pd.DataFrame, period: int, window: int = 5) -> pd.Series:
    """计算均线斜率（用于判断多空倾斜方向）。"""
    ma = df["close"].rolling(window=period).mean()
    return ma.diff(window)

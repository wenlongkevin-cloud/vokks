# indicators/sar.py
# Marlong — Parabolic SAR

import pandas as pd
import numpy as np


def add_sar(df: pd.DataFrame, af: float = 0.02, max_af: float = 0.2) -> pd.DataFrame:
    """
    添加 SAR 列及趋势方向列。

    - sar       : Parabolic SAR 值
    - sar_bull  : True 表示当前 SAR 在价格下方（多头）
    """
    high = df["high"].values
    low = df["low"].values
    n = len(df)

    sar = np.zeros(n)
    bull = np.ones(n, dtype=bool)
    ep = np.zeros(n)
    af_arr = np.zeros(n)

    # 初始化
    bull[0] = True
    sar[0] = low[0]
    ep[0] = high[0]
    af_arr[0] = af

    for i in range(1, n):
        prev_bull = bull[i - 1]
        prev_sar = sar[i - 1]
        prev_ep = ep[i - 1]
        prev_af = af_arr[i - 1]

        # 新 SAR
        new_sar = prev_sar + prev_af * (prev_ep - prev_sar)

        if prev_bull:
            new_sar = min(new_sar, low[i - 1], low[max(i - 2, 0)])
            if low[i] < new_sar:
                bull[i] = False
                new_sar = prev_ep
                ep[i] = low[i]
                af_arr[i] = af
            else:
                bull[i] = True
                if high[i] > prev_ep:
                    ep[i] = high[i]
                    af_arr[i] = min(prev_af + af, max_af)
                else:
                    ep[i] = prev_ep
                    af_arr[i] = prev_af
        else:
            new_sar = max(new_sar, high[i - 1], high[max(i - 2, 0)])
            if high[i] > new_sar:
                bull[i] = True
                new_sar = prev_ep
                ep[i] = high[i]
                af_arr[i] = af
            else:
                bull[i] = False
                if low[i] < prev_ep:
                    ep[i] = low[i]
                    af_arr[i] = min(prev_af + af, max_af)
                else:
                    ep[i] = prev_ep
                    af_arr[i] = prev_af

        sar[i] = new_sar

    df["sar"] = sar
    df["sar_bull"] = bull
    return df

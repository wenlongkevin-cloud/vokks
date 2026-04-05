# data/loader.py
# Marlong — 本地数据缓存读写

import os
import pandas as pd
from utils.logger import get_logger

logger = get_logger(__name__)


def _cache_path(data_dir: str, symbol: str, start: str, end: str) -> str:
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, f"{symbol}_{start}_{end}.csv")


def load_data(
    symbol: str,
    start_date: str,
    end_date: str,
    data_dir: str = "data/cache",
    force_fetch: bool = False,
) -> pd.DataFrame:
    """
    优先读本地缓存，缓存不存在时自动拉取并保存。

    Args:
        force_fetch: True 时强制重新拉取，忽略缓存
    """
    from data.fetcher import fetch_stock_data

    path = _cache_path(data_dir, symbol, start_date, end_date)

    if not force_fetch and os.path.exists(path):
        logger.info(f"读取缓存：{path}")
        df = pd.read_csv(path, parse_dates=["date"])
        return df

    df = fetch_stock_data(symbol, start_date, end_date)
    save_data(df, symbol, start_date, end_date, data_dir)
    return df


def save_data(
    df: pd.DataFrame,
    symbol: str,
    start_date: str,
    end_date: str,
    data_dir: str = "data/cache",
) -> None:
    path = _cache_path(data_dir, symbol, start_date, end_date)
    df.to_csv(path, index=False)
    logger.info(f"数据已缓存：{path}")

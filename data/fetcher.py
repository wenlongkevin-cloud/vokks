# data/fetcher.py
# Marlong — A股日线数据拉取（akshare）

import pandas as pd
from utils.logger import get_logger

logger = get_logger(__name__)


def fetch_stock_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    拉取 A股日线数据（前复权）。

    Args:
        symbol:     股票代码，如 "300274"
        start_date: 开始日期，格式 "20230101"
        end_date:   结束日期，格式 "20260101"

    Returns:
        DataFrame，列：date / open / high / low / close / volume / amount / turnover
    """
    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请先安装 akshare：pip install akshare")

    logger.info(f"拉取数据：{symbol}  {start_date} → {end_date}")

    df = ak.stock_zh_a_hist(
        symbol=symbol,
        period="daily",
        start_date=start_date,
        end_date=end_date,
        adjust="qfq",           # 前复权
    )

    df = _normalize(df)
    logger.info(f"获取 {len(df)} 条记录")
    return df


def _normalize(df: pd.DataFrame) -> pd.DataFrame:
    col_map = {
        "日期": "date",
        "开盘": "open",
        "最高": "high",
        "最低": "low",
        "收盘": "close",
        "成交量": "volume",
        "成交额": "amount",
        "换手率": "turnover",
    }
    df = df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    for col in ["open", "high", "low", "close", "volume", "amount", "turnover"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df[["date", "open", "high", "low", "close", "volume", "amount", "turnover"]]

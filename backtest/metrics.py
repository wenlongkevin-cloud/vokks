# backtest/metrics.py
# Marlong — 回测评估指标

import pandas as pd
import numpy as np


def compute_metrics(
    equity: pd.Series,
    trades: pd.DataFrame,
    initial_capital: float,
) -> dict:
    """
    计算常用回测指标。

    Returns:
        dict: 包含总收益率、年化收益、最大回撤、夏普比率、胜率等
    """
    if equity.empty:
        return {}

    # --- 总收益 ---
    total_return = (equity.iloc[-1] - initial_capital) / initial_capital

    # --- 年化收益（按252交易日） ---
    n_days = (equity.index[-1] - equity.index[0]).days
    annual_return = (1 + total_return) ** (365 / max(n_days, 1)) - 1

    # --- 最大回撤 ---
    rolling_max = equity.cummax()
    drawdown = (equity - rolling_max) / rolling_max
    max_drawdown = drawdown.min()

    # --- 夏普比率（假设无风险利率 3%） ---
    daily_returns = equity.pct_change().dropna()
    rf_daily = 0.03 / 252
    excess = daily_returns - rf_daily
    sharpe = (excess.mean() / excess.std() * np.sqrt(252)) if excess.std() > 0 else 0.0

    # --- 交易统计 ---
    completed = trades[trades["pnl"].notna()] if not trades.empty else pd.DataFrame()
    n_trades = len(completed)
    win_trades = (completed["pnl"] > 0).sum() if n_trades > 0 else 0
    win_rate = win_trades / n_trades if n_trades > 0 else 0.0
    avg_pnl = completed["pnl"].mean() if n_trades > 0 else 0.0
    avg_win = completed.loc[completed["pnl"] > 0, "pnl"].mean() if win_trades > 0 else 0.0
    avg_loss_trades = completed[completed["pnl"] <= 0]
    avg_loss = avg_loss_trades["pnl"].mean() if len(avg_loss_trades) > 0 else 0.0
    profit_factor = (
        abs(completed.loc[completed["pnl"] > 0, "pnl"].sum() /
            completed.loc[completed["pnl"] <= 0, "pnl"].sum())
        if len(avg_loss_trades) > 0 else float("inf")
    )

    return {
        "total_return": round(total_return * 100, 2),
        "annual_return": round(annual_return * 100, 2),
        "max_drawdown": round(max_drawdown * 100, 2),
        "sharpe_ratio": round(sharpe, 3),
        "n_trades": n_trades,
        "win_rate": round(win_rate * 100, 2),
        "avg_pnl": round(avg_pnl, 2),
        "avg_win": round(avg_win, 2),
        "avg_loss": round(avg_loss, 2),
        "profit_factor": round(profit_factor, 3),
        "final_capital": round(equity.iloc[-1], 2),
    }


def print_metrics(metrics: dict) -> None:
    print("\n" + "=" * 40)
    print("  Marlong 回测结果汇总")
    print("=" * 40)
    print(f"  总收益率      : {metrics.get('total_return', 0):>8.2f}%")
    print(f"  年化收益率    : {metrics.get('annual_return', 0):>8.2f}%")
    print(f"  最大回撤      : {metrics.get('max_drawdown', 0):>8.2f}%")
    print(f"  夏普比率      : {metrics.get('sharpe_ratio', 0):>8.3f}")
    print(f"  交易次数      : {metrics.get('n_trades', 0):>8d}")
    print(f"  胜率          : {metrics.get('win_rate', 0):>8.2f}%")
    print(f"  平均每笔盈亏  : {metrics.get('avg_pnl', 0):>8.2f} 元")
    print(f"  平均盈利      : {metrics.get('avg_win', 0):>8.2f} 元")
    print(f"  平均亏损      : {metrics.get('avg_loss', 0):>8.2f} 元")
    print(f"  盈亏比        : {metrics.get('profit_factor', 0):>8.3f}")
    print(f"  最终资金      : {metrics.get('final_capital', 0):>10.2f} 元")
    print("=" * 40 + "\n")

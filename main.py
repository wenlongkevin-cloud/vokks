#!/usr/bin/env python3
# main.py
# Marlong — 趋势策略回测入口

import sys
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

# 确保项目根目录在 Python 路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import DEFAULT_CONFIG
from data.loader import load_data
from strategy.trend_ma import TrendMAStrategy
from backtest.engine import BacktestEngine
from backtest.metrics import print_metrics


def plot_results(df: pd.DataFrame, equity: pd.Series, trades: pd.DataFrame, title: str) -> None:
    fig, axes = plt.subplots(3, 1, figsize=(14, 12), sharex=False)
    fig.suptitle(title, fontsize=14, fontweight="bold")

    # --- 子图1：K线 + 均线 + 买卖点 ---
    ax1 = axes[0]
    ax1.plot(df["date"], df["close"], color="#333", linewidth=1, label="收盘价")
    for ma, color in [("ma5", "#e74c3c"), ("ma20", "#3498db"), ("ma60", "#f39c12"), ("ma250", "#8e44ad")]:
        if ma in df.columns:
            ax1.plot(df["date"], df[ma], linewidth=0.8, label=ma.upper(), alpha=0.85)

    completed = trades[trades["pnl"].notna()]
    for _, t in completed.iterrows():
        entry_row = trades[trades["entry_date"] == t.get("entry_date")]
        if not entry_row.empty:
            ep = entry_row.iloc[0].get("entry_price")
            xp = t.get("exit_price")
            ed = t.get("entry_date")
            xd = t.get("exit_date")
            if pd.notna(ep) and pd.notna(xp):
                color = "#27ae60" if t["pnl"] > 0 else "#e74c3c"
                ax1.annotate("▲", xy=(ed, ep), color="#27ae60", fontsize=9)
                ax1.annotate("▼", xy=(xd, xp), color=color, fontsize=9)

    ax1.set_ylabel("价格（元）")
    ax1.legend(fontsize=7, loc="upper left")
    ax1.grid(alpha=0.3)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

    # --- 子图2：MACD ---
    ax2 = axes[1]
    if "diff" in df.columns:
        ax2.plot(df["date"], df["diff"], color="#e74c3c", linewidth=1, label="DIFF")
        ax2.plot(df["date"], df["dea"], color="#3498db", linewidth=1, label="DEA")
        colors = ["#27ae60" if v >= 0 else "#e74c3c" for v in df["macd_bar"]]
        ax2.bar(df["date"], df["macd_bar"], color=colors, alpha=0.6, width=1, label="MACD柱")
        ax2.axhline(0, color="gray", linewidth=0.5)
        ax2.set_ylabel("MACD")
        ax2.legend(fontsize=7, loc="upper left")
        ax2.grid(alpha=0.3)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

    # --- 子图3：资产曲线 ---
    ax3 = axes[2]
    ax3.plot(equity.index, equity.values, color="#2980b9", linewidth=1.5, label="净值曲线")
    ax3.axhline(equity.iloc[0], color="gray", linewidth=0.8, linestyle="--", label="初始资金")
    ax3.fill_between(equity.index, equity.iloc[0], equity.values,
                     where=(equity.values >= equity.iloc[0]),
                     alpha=0.15, color="#27ae60")
    ax3.fill_between(equity.index, equity.iloc[0], equity.values,
                     where=(equity.values < equity.iloc[0]),
                     alpha=0.15, color="#e74c3c")
    ax3.set_ylabel("总资产（元）")
    ax3.legend(fontsize=7, loc="upper left")
    ax3.grid(alpha=0.3)
    ax3.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

    plt.tight_layout()
    plt.savefig("backtest_result.png", dpi=150)
    print("图表已保存至 backtest_result.png")
    plt.show()


def main():
    cfg = DEFAULT_CONFIG.copy()

    print(f"\nMarlong 趋势策略回测")
    print(f"股票：{cfg['symbol_name']}（{cfg['symbol']}）")
    print(f"时间：{cfg['start_date']} → {cfg['end_date']}")
    print(f"初始资金：{cfg['initial_capital']:,} 元\n")

    # 1. 加载数据
    df = load_data(
        symbol=cfg["symbol"],
        start_date=cfg["start_date"],
        end_date=cfg["end_date"],
        data_dir=cfg["data_dir"],
    )

    # 2. 策略信号生成
    strategy = TrendMAStrategy(cfg)
    df = strategy.run(df)

    # 3. 回测执行
    engine = BacktestEngine(cfg)
    result = engine.run(df)

    # 4. 输出结果
    print_metrics(result["metrics"])

    if not result["trades"].empty:
        print("最近5笔交易：")
        completed = result["trades"][result["trades"]["pnl"].notna()]
        print(completed.tail(5).to_string(index=False))

    # 5. 绘图
    title = f"Marlong · {cfg['symbol_name']}（{cfg['symbol']}）趋势策略回测"
    plot_results(df, result["equity"], result["trades"], title)


if __name__ == "__main__":
    main()

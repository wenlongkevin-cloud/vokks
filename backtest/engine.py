# backtest/engine.py
# Marlong — 回测引擎（逐日迭代，单股单策略）

import pandas as pd
from utils.logger import get_logger
from utils.helpers import pct
from risk.position import PositionSizer
from risk.rules import RiskRules

logger = get_logger(__name__)


class BacktestEngine:
    """
    简单事件驱动回测引擎。

    假设：
    - 信号日收盘后确认，次日开盘以当日开盘价成交
    - 每笔交易扣除佣金（双边）和卖出印花税
    - 同一时间只持有一只股票（单仓）
    """

    def __init__(self, config: dict):
        self.config = config
        self.initial_capital = config["initial_capital"]
        self.commission = config.get("commission_rate", 0.0003)
        self.stamp_duty = config.get("stamp_duty", 0.001)
        self.slippage = config.get("slippage", 0.002)

        self.sizer = PositionSizer(
            mode=config.get("position_mode", "fixed_pct"),
            config=config,
        )
        self.risk = RiskRules(config)

    def run(self, df: pd.DataFrame) -> dict:
        """
        运行回测。

        Args:
            df: 含有 signal 列的 DataFrame（由策略生成）

        Returns:
            dict:
              - trades   : 每笔交易记录 DataFrame
              - equity   : 每日资产曲线 Series
              - metrics  : 汇总指标 dict
        """
        from backtest.metrics import compute_metrics

        capital = self.initial_capital
        shares = 0
        entry_price = 0.0
        highest_since_entry = 0.0

        trades = []
        equity = []

        df = df.reset_index(drop=True)

        for i, row in df.iterrows():
            date = row["date"]
            close = row["close"]
            signal = row.get("signal", 0)

            # 以次日开盘价成交（用当日收盘信号，次日执行）
            exec_price_raw = df.loc[i + 1, "open"] if i + 1 < len(df) else close
            exec_price_buy = exec_price_raw * (1 + self.slippage)
            exec_price_sell = exec_price_raw * (1 - self.slippage)

            # --- 持仓期间风控检查（当日收盘） ---
            if shares > 0:
                highest_since_entry = max(highest_since_entry, close)
                trigger = self.risk.check(entry_price, close, highest_since_entry)
                if trigger:
                    sell_price = exec_price_sell
                    proceeds = shares * sell_price
                    cost = proceeds * (self.commission + self.stamp_duty)
                    capital += proceeds - cost
                    pnl = proceeds - cost - shares * entry_price * (1 + self.commission)
                    trades.append({
                        "exit_date": date,
                        "exit_price": sell_price,
                        "shares": shares,
                        "pnl": pnl,
                        "exit_reason": trigger,
                    })
                    logger.info(
                        f"[{trigger}] {date.date()}  {shares}股 @ {sell_price:.2f}  "
                        f"PnL={pnl:+.0f}"
                    )
                    shares = 0
                    entry_price = 0.0
                    highest_since_entry = 0.0

            # --- 信号处理 ---
            if signal == 1 and shares == 0:
                new_shares = self.sizer.calc_shares(exec_price_buy, capital)
                if new_shares > 0:
                    cost = new_shares * exec_price_buy
                    commission = cost * self.commission
                    capital -= cost + commission
                    shares = new_shares
                    entry_price = exec_price_buy
                    highest_since_entry = exec_price_buy
                    trades.append({
                        "entry_date": date,
                        "entry_price": exec_price_buy,
                        "shares": new_shares,
                        "pnl": None,
                        "exit_reason": None,
                    })
                    logger.info(
                        f"[BUY]  {date.date()}  {new_shares}股 @ {exec_price_buy:.2f}  "
                        f"剩余现金={capital:.0f}"
                    )

            elif signal == -1 and shares > 0:
                proceeds = shares * exec_price_sell
                cost = proceeds * (self.commission + self.stamp_duty)
                capital += proceeds - cost
                pnl = proceeds - cost - shares * entry_price * (1 + self.commission)
                trades[-1].update({
                    "exit_date": date,
                    "exit_price": exec_price_sell,
                    "pnl": pnl,
                    "exit_reason": "signal",
                })
                logger.info(
                    f"[SELL] {date.date()}  {shares}股 @ {exec_price_sell:.2f}  "
                    f"PnL={pnl:+.0f}"
                )
                shares = 0
                entry_price = 0.0
                highest_since_entry = 0.0

            # --- 每日净值 ---
            market_value = shares * close
            total = capital + market_value
            equity.append({"date": date, "equity": total})

        equity_series = pd.DataFrame(equity).set_index("date")["equity"]
        trades_df = pd.DataFrame(trades)
        metrics = compute_metrics(equity_series, trades_df, self.initial_capital)

        return {
            "trades": trades_df,
            "equity": equity_series,
            "metrics": metrics,
        }

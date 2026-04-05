# risk/position.py
# Marlong — 仓位管理

import pandas as pd


class PositionSizer:
    """
    仓位计算器。

    两种模式：
    - fixed_pct : 每次用总资金的固定比例买入（简单，适合趋势初学者）
    - atr_based : 根据 ATR 动态调整，风险恒定为总资金的 risk_per_trade
    """

    def __init__(self, mode: str = "fixed_pct", config: dict = None):
        self.mode = mode
        self.config = config or {}

    def calc_shares(
        self,
        price: float,
        total_capital: float,
        df_row: pd.Series = None,
    ) -> int:
        """
        计算可买手数（A股最小交易单位：100股/手）。

        Returns:
            int: 手数 * 100 = 股数
        """
        if self.mode == "fixed_pct":
            pct = self.config.get("max_position_pct", 1.0)
            budget = total_capital * pct
        elif self.mode == "atr_based":
            risk_pct = self.config.get("risk_per_trade", 0.02)
            stop_pct = self.config.get("stop_loss_pct", 0.07)
            risk_amount = total_capital * risk_pct
            budget = risk_amount / stop_pct
            budget = min(budget, total_capital * self.config.get("max_position_pct", 1.0))
        else:
            budget = total_capital

        shares = int(budget // (price * 100)) * 100
        return max(shares, 0)

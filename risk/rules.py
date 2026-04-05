# risk/rules.py
# Marlong — 止损止盈风控规则

class RiskRules:
    """
    风控规则检查器，在每个交易日收盘时判断是否触发止损/止盈。

    规则优先级（高 → 低）：
      1. 固定止损（hard stop）
      2. 追踪止损（trailing stop）
      3. 固定止盈（take profit）
    """

    def __init__(self, config: dict):
        self.stop_loss_pct = config.get("stop_loss_pct", 0.07)
        self.take_profit_pct = config.get("take_profit_pct", 0.20)
        self.trailing_stop_pct = config.get("trailing_stop_pct", 0.05)

    def check(
        self,
        entry_price: float,
        current_price: float,
        highest_since_entry: float,
    ) -> str | None:
        """
        检查当前价格是否触发任意风控规则。

        Returns:
            "stop_loss"     — 触发固定止损
            "trailing_stop" — 触发追踪止损
            "take_profit"   — 触发止盈
            None            — 无触发
        """
        # 1. 固定止损
        if current_price <= entry_price * (1 - self.stop_loss_pct):
            return "stop_loss"

        # 2. 追踪止损（从最高点回撤超过阈值）
        if highest_since_entry > entry_price:
            trailing_floor = highest_since_entry * (1 - self.trailing_stop_pct)
            if current_price <= trailing_floor:
                return "trailing_stop"

        # 3. 止盈
        if current_price >= entry_price * (1 + self.take_profit_pct):
            return "take_profit"

        return None

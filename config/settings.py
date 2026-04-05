# config/settings.py
# Marlong — 全局配置

DEFAULT_CONFIG = {
    # --- 目标股票 ---
    "symbol": "300274",          # A股代码（不含交易所前缀）
    "symbol_name": "阳光电源",

    # --- 回测时间范围 ---
    "start_date": "20230101",
    "end_date": "20260101",

    # --- 资金管理 ---
    "initial_capital": 100_000,  # 初始资金（元）
    "commission_rate": 0.0003,   # 佣金率（单边）
    "stamp_duty": 0.001,         # 印花税（仅卖出）
    "slippage": 0.002,           # 滑点（双边各）

    # --- 仓位管理 ---
    "position_mode": "fixed_pct",  # fixed_pct | atr_based
    "max_position_pct": 1.0,       # 单票最大仓位比例
    "risk_per_trade": 0.02,        # 单笔最大亏损占总资金比例（ATR模式用）

    # --- 均线周期 ---
    "ma_periods": [5, 20, 60, 250],

    # --- MACD 参数 ---
    "macd_fast": 12,
    "macd_slow": 26,
    "macd_signal": 9,

    # --- SAR 参数 ---
    "sar_af": 0.02,
    "sar_max_af": 0.2,

    # --- 风控规则 ---
    "stop_loss_pct": 0.07,       # 固定止损比例（跌7%止损）
    "take_profit_pct": 0.20,     # 止盈比例
    "trailing_stop_pct": 0.05,   # 追踪止损回撤比例

    # --- 数据缓存路径 ---
    "data_dir": "data/cache",
}

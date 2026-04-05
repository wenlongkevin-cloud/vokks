# utils/helpers.py
# Marlong — 通用工具函数

def pct(value: float, decimals: int = 2) -> str:
    """格式化为百分比字符串，如 0.1234 → '12.34%'"""
    return f"{value * 100:.{decimals}f}%"


def round2(value: float) -> float:
    """保留两位小数"""
    return round(value, 2)

# strategy/base.py
# Marlong — 策略抽象基类

from abc import ABC, abstractmethod
import pandas as pd


class BaseStrategy(ABC):
    """
    所有策略继承此基类，实现 generate_signals()。

    信号约定（signal 列）：
      +1  : 买入信号
      -1  : 卖出信号
       0  : 无操作
    """

    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    def prepare(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        在 df 上计算所有所需指标，返回处理后的 df。
        子类负责调用各 indicator 函数。
        """

    @abstractmethod
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        在 prepared df 上生成交易信号列 signal（+1/-1/0）。
        返回添加了 signal 列的 df。
        """

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.prepare(df.copy())
        df = self.generate_signals(df)
        return df

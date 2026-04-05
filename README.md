# Vokks — Marlong 量化研究项目

> 个人 A 股趋势交易量化研究框架。策略研究、回测验证、风控迭代。
>
> — Marlong

---

## 项目定位

- 面向趋势交易散户的量化研究工具
- A 股日线级别策略为主
- 强调风控优先：止损清晰、盈亏比可量化、规则执行有纪律

---

## 项目结构

```
vokks/
├── main.py                     # 一键运行趋势策略回测
├── requirements.txt
│
├── config/settings.py          # 全局参数配置
│
├── data/
│   ├── fetcher.py              # akshare 拉取 A 股日线（前复权）
│   └── loader.py               # 本地 CSV 缓存读写
│
├── indicators/
│   ├── ma.py                   # MA5/20/60/250
│   ├── macd.py                 # MACD / DIFF / DEA / 金叉死叉
│   ├── volume.py               # OBV / 量比 / 成交额均线
│   └── sar.py                  # Parabolic SAR
│
├── strategy/
│   ├── base.py                 # 抽象策略基类
│   └── trend_ma.py             # 趋势策略：MA金叉 + MACD + SAR
│
├── backtest/
│   ├── engine.py               # 逐日回测引擎（含佣金/印花税/滑点）
│   └── metrics.py              # 夏普 / 最大回撤 / 胜率 / 盈亏比
│
├── risk/
│   ├── position.py             # 仓位管理（固定比例 / ATR动态）
│   └── rules.py                # 止损 / 止盈 / 追踪止损
│
├── utils/
│   ├── logger.py
│   └── helpers.py
│
└── examples/notebooks/
    └── demo_trend_strategy.ipynb
```

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行默认策略回测

```bash
python main.py
```

默认配置（`config/settings.py`）：
- 股票：阳光电源（300274）
- 时间：2023-01-01 → 2026-01-01
- 初始资金：10 万元
- 策略：MA5/20 金叉 + MACD 确认 + SAR 过滤

运行后自动输出：
- 控制台回测指标汇总
- 图表文件 `backtest_result.png`（含 K 线均线 + MACD + 资产曲线）

### 3. 修改参数

编辑 `config/settings.py`，可调整：

```python
"symbol": "600036",        # 换股票
"start_date": "20220101",  # 调整时间
"initial_capital": 200_000,
"stop_loss_pct": 0.05,     # 收紧止损
"position_mode": "atr_based",
```

### 4. 查看 Notebook 示例

```bash
jupyter lab examples/notebooks/demo_trend_strategy.ipynb
```

---

## 趋势策略逻辑

### 入场条件（全部满足）
1. MA5 上穿 MA20（金叉）
2. MACD DIFF > 0 或 MACD 金叉（多头区域确认）
3. SAR 在价格下方（多头 SAR 未翻空）
4. 非极度缩量（量比 ≥ 0.7）

### 出场条件（任意一个触发）
1. MA5 下穿 MA20（死叉）
2. SAR 翻空（sar_bull 由 True → False）
3. 触发固定止损（默认 -7%）
4. 触发追踪止损（从最高点回撤 5%）
5. 触发止盈（+20%）

---

## 风控规则

| 规则 | 默认参数 | 说明 |
|------|----------|------|
| 固定止损 | -7% | 亏损超7%强制出局 |
| 追踪止损 | -5% | 从最高点回撤5%离场 |
| 固定止盈 | +20% | 盈利20%锁定利润 |
| 单票仓位 | 100% | 可调为部分仓位 |
| 佣金（单边） | 0.03% | |
| 印花税（卖出） | 0.1% | |
| 滑点 | 0.2% | 双边各 |

---

## 后续扩展方向

- [ ] 多股票组合回测
- [ ] 参数网格优化（Grid Search）
- [ ] 更多策略（突破跟随、反弹博弈）
- [ ] 实时信号推送（微信/钉钉）
- [ ] 因子研究模块

---

*Marlong · 量化研究 · A 股趋势交易*

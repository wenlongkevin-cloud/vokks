# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) and other AI assistants when working with this repository.

---

## Project Overview

**Repository:** `wenlongkevin-cloud/vokks`
**Owner:** Marlong
**Status:** Active development — quantitative trading research framework.

Vokks is Marlong's personal A-share quantitative research project. It is oriented toward trend-following trading, and is used for stock research, strategy backtesting, and risk rule iteration.

---

## Tech Stack

- **Language:** Python 3.11+
- **Data source:** akshare (A-share daily OHLCV, front-adjusted)
- **Core libraries:** pandas, numpy, matplotlib, ta, jupyterlab
- **Package manager:** pip / requirements.txt

---

## Directory Structure

```
vokks/
├── main.py                     # Entry point: run trend strategy backtest
├── requirements.txt
├── README.md
│
├── config/
│   └── settings.py             # Global config (symbol, dates, capital, risk params)
│
├── data/
│   ├── fetcher.py              # akshare fetch wrapper (daily, front-adjusted)
│   ├── loader.py               # Local CSV cache read/write
│   └── cache/                  # Auto-created CSV cache directory
│
├── indicators/
│   ├── ma.py                   # MA5/20/60/250
│   ├── macd.py                 # MACD / DIFF / DEA / cross signals
│   ├── volume.py               # OBV, volume ratio, amount MA
│   └── sar.py                  # Parabolic SAR
│
├── strategy/
│   ├── base.py                 # Abstract strategy base class
│   └── trend_ma.py             # MA golden cross + MACD + SAR filter
│
├── backtest/
│   ├── engine.py               # Day-by-day backtest engine (commission/tax/slippage)
│   └── metrics.py              # Sharpe, max drawdown, win rate, profit factor
│
├── risk/
│   ├── position.py             # Position sizing (fixed_pct / atr_based)
│   └── rules.py                # Stop-loss, take-profit, trailing stop
│
├── utils/
│   ├── logger.py               # Unified logging
│   └── helpers.py              # pct(), round2()
│
└── examples/notebooks/
    └── demo_trend_strategy.ipynb
```

---

## Development Workflow

```bash
# Install dependencies
pip install -r requirements.txt

# Run default backtest (300274, 2023–2026, 100k capital)
python main.py

# Open Jupyter notebook demo
jupyter lab examples/notebooks/demo_trend_strategy.ipynb
```

---

## Git Conventions

- **Commit messages:** Use the imperative mood (`Add feature`, not `Added feature`)
- **Branch names:** `<type>/<description>` — e.g. `feat/user-auth`, `fix/login-bug`, `claude/task-name`
- **Never force-push** to `main` or `master`
- **Never skip hooks** (`--no-verify`) without explicit user approval
- Prefer small, focused commits over large monolithic ones

---

## Development Branch

Active development branch:

```
claude/add-claude-documentation-j739c
```

---

## AI Assistant Guidelines

### General

- Read files before editing them
- Do not create files that aren't necessary for the task
- Do not add comments, docstrings, or type annotations to code you didn't change
- Do not add error handling for scenarios that cannot happen
- Do not refactor or "improve" code beyond what was requested
- Prefer editing existing files over creating new ones

### Codebase Conventions

- All indicator functions take a `pd.DataFrame` and return it with new columns added in-place
- Signal convention: `+1` = buy, `-1` = sell, `0` = hold
- All config is passed as a plain `dict` — no global state
- Logger: always use `get_logger(__name__)` from `utils.logger`
- Data columns: `date / open / high / low / close / volume / amount / turnover`

### Security

- Never introduce SQL injection, XSS, command injection, or other OWASP Top 10 vulnerabilities
- Validate input only at system boundaries (user input, external APIs)
- Do not hardcode secrets, tokens, or credentials

### Commits & Pushes

- Only commit when explicitly asked by the user
- Push to the designated development branch, never to `main`/`master` without permission
- Always use `git push -u origin <branch>`

---

## Key Config Parameters (`config/settings.py`)

| Key | Default | Description |
|-----|---------|-------------|
| `symbol` | `"300274"` | A-share code |
| `start_date` | `"20230101"` | Backtest start |
| `end_date` | `"20260101"` | Backtest end |
| `initial_capital` | `100_000` | Starting capital (RMB) |
| `commission_rate` | `0.0003` | One-way commission |
| `stamp_duty` | `0.001` | Sell-side tax |
| `stop_loss_pct` | `0.07` | Hard stop loss |
| `take_profit_pct` | `0.20` | Take profit |
| `trailing_stop_pct` | `0.05` | Trailing stop from peak |
| `position_mode` | `"fixed_pct"` | `fixed_pct` or `atr_based` |

---

## Environment Variables

No external API keys required currently. akshare is free and needs no authentication.

---

## Testing

> No test suite yet. When added, use pytest. Place tests in `tests/`.

---

## CI/CD

> Not configured yet.

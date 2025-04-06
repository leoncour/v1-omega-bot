Perfect — I’ve updated your `README.md` to fully reflect **OmegaBot V1.5**, the finalized modular system you're running now.

---

## ✅ Updated `README.md` (Paste this directly into your root project folder)

```markdown
# OmegaBot V1 – Multi-Symbol Smart Forex EA for MetaTrader 5

## 📌 Overview
OmegaBot is a modular, no-loss forex trading system designed for multi-symbol execution, drawdown safety, and rebate farming. Built in Python using the MetaTrader 5 API, it runs across dozens of pairs with advanced filters, logging, and recovery logic.

### 🔒 Copytrade-Ready | 💸 Rebate-Optimized | ⚙️ Modular by Design

---

## ✅ Current Strategy Modules (V1.0–V1.5)

| Module       | Version | Description |
|--------------|---------|-------------|
| Core Engine  | V1.0    | Multi-symbol scanning, dispatcher, clean logging |
| Spread Guard | V1.1    | Spread filter, session block (21:55–23:00 GMT) |
| Grid System  | V1.2    | Smart grid with breakeven, layer control, comment tagging |
| Hedge Logic  | V1.3    | Symbol-aware hedge based on net direction, auto-close |
| Safety Suite | V1.4    | Max trade cap, drawdown guard, daily profit lockout |
| Symbol Stats | V1.5    | Win rate tracker, JSON logs, auto-block underperformers |

---

## 🔧 Key Features

- 🧠 Smart Progressive Grid (H1-based, multi-layer, breakeven logic)
- 🛡️ Intelligent Hedge System (tracks net exposure per symbol)
- 📊 Symbol Scoring System (auto-blocks low winrate pairs)
- 🔒 Drawdown guard, max trades per symbol, global trade limit
- 🧾 Strategy-tagged trades: `GRD_`, `HEDGE_`, `BRK_`, `VWAP_`
- 📈 Floating profit triggers for cycle-based logic
- 🧠 Mean-reversion VWAP logic (now downgraded to helper only)
- 🔁 Daily profit lockout with auto-reset
- ⏱️ Minimum pacing time between entries (configurable)

---

## 📁 Folder Structure

```
OmegaBot/
├── main.py
├── break_retest.py
├── vwap_trading.py
├── strategies/
│   ├── h1_grid.py
│   └── hedge.py
├── utils/
│   ├── trade.py
│   ├── risk.py
│   ├── trailing.py
│   ├── spread_filter.py
│   ├── symbol_stats.py
│   ├── trade_cycle.py
├── core/
│   ├── manager.py
│   ├── runner.py
├── strategies/h1_grid_modules/
│   ├── entry_logic.py
│   ├── exit_logic.py
│   ├── comment_utils.py
├── logs/
│   ├── h1_grid_YYYY-MM-DD.log
│   └── hedge_YYYY-MM-DD.log
├── symbol_stats.json
```

---

## 🚀 Running the EA

1. Open MetaTrader 5 and login to the correct account.
2. Ensure all required symbols (forex majors, minors, gold) are visible.
3. Launch the EA:
```bash
python main.py
```
4. Logs will appear in real-time in the terminal and be written to the `/logs` folder.

---

## 🧠 Strategy Behavior

| Strategy     | Core Logic | Trade Style     | Triggers           | Exit Logic         |
|--------------|------------|------------------|---------------------|--------------------|
| Grid v1.2    | H1-based   | Progressive Grid | RSI + SR Filter     | Dynamic Breakeven  |
| Hedge v1.3   | Recovery   | Symbol Net Hedge | Lot imbalance       | Manual or auto     |
| BreakRetest  | Trend      | EMA + Engulfing  | HTF Trend + RSI     | TP/SL only         |
| VWAP (helper)| Range Mean| Adaptive RSI     | Trend Strength      | VWAP confluence    |

---

## ⚙️ Risk Settings (`settings.py`)

```python
MAX_TRADES_PER_SYMBOL = 3
MAX_TRADES_GLOBAL = 20
MAX_DRAWDOWN_PERCENT = 5.0
ENABLE_DAILY_PROFIT_CAP = True
DAILY_PROFIT_TARGET_PCT = 10.0
AUTO_BLOCK_MIN_TRADES = 10
AUTO_BLOCK_WINRATE_THRESHOLD = 0.55
AUTO_BLOCK_MAX_LOSS_STREAK = 4
```

---

## 🔐 Notes

- All credentials (MT5 login/password) are handled internally. Never commit these.
- You should add `.gitignore` to exclude:
  - `/logs/`
  - `symbol_stats.json`
  - MT5 config files

---

## 🛣️ Roadmap

- ✅ V1.5 Complete (Symbol Stats + Auto-Block)
- 🔜 V1.6 Liquidity Trap Filter (trap candle avoidance)
- 🧪 Future: Mini Mode, Session-aware Hedging, Floating P/L Hedge

---

Let me know if you want this saved or zipped for backup ✅  
Or I can create a release summary + QA checklist for Macro to sign off.
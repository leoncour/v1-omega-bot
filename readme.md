Here's your `README.md` file ready to be saved directly into your EA project root:

---

```markdown
# V5 EA – Multi-Symbol Smart Trading Bot for MetaTrader 5

## 📌 Overview
This is an intelligent Python-based EA that connects to MetaTrader 5 and monitors multiple forex pairs and gold for optimized entry conditions across different market types.

## ✅ Strategies Implemented
- **VWAP v2.3** – Trend-following with adaptive RSI filter and engulfing entry
- **BreakRetest v1.1** – Breakout retest logic with EMA alignment
- **Grid v1.2** – Ranging logic (RSI-based) with controlled martingale behavior
- **Hedge v1.2** – Extreme RSI range entries, improved with engulfing + zone filters

## 🔧 Core Features
- Multi-symbol scanning (EURUSD, GBPUSD, USDJPY, USDCHF, USDCAD, AUDUSD, NZDUSD, XAUUSD)
- Adaptive pip-size handling for XAUUSD (1 pip = 0.10)
- Centralized SL/TP and RRR logic
- Trade filters: engulfing patterns, adaptive RSI, HTF trend alignment
- Logging per strategy and reason for entry rejection
- Modular, easy-to-extend structure

## 🚀 Running the EA

1. Open your MetaTrader 5 terminal and log in to the correct account
2. Ensure all required symbols are visible and charted
3. Run the script:
   ```bash
   python main.py
   ```

4. Monitor terminal output for logs on strategy checks and trade decisions.

## 📂 Folder Structure
```
v5_ea/
├── main.py
├── break_retest.py
├── grid_trading.py
├── vwap_trading.py
├── hedging.py
├── utils/
│   ├── core.py
│   ├── trade.py
│   ├── risk.py
│   ├── indicators.py
│   └── entry_filters.py
├── Reports/
│   ├── trade_history.csv
│   ├── filtered_last_200_trades.csv
│   └── merged_trades.csv
```

## 📈 Strategy Status & Win Rate (latest reviewed)
| Strategy        | Win Rate | Issues Identified              | Improvements Done              | Pending Fixes               |
|-----------------|----------|--------------------------------|--------------------------------|-----------------------------|
| VWAP v2.3       | ~52%     | Some filters too strict        | Adaptive RSI, Engulfing        | Trailing SL                 |
| BreakRetest v1.1| Low      | Entry too tight                | XAUUSD pip fix, filtering      | Better zone logic           |
| Grid v1.2       | Poor     | Loose RSI entries              | RSI tightened, zone added      | Trailing SL, risk control   |
| Hedge v1.2      | Poor     | Many false entries             | RSI tightened, engulfing added | Trailing SL, reentry logic  |

## 🔐 Notes
- All sensitive credentials (MT5 login/password) are handled in `core.py`. **Do not upload this to GitHub or share publicly.**
- Add a `.gitignore` to prevent logging/report files and credentials from being committed.

---

```

Let me know if you want this zipped up with the `.gitignore` or copied into your project now.
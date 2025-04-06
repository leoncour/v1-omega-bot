# utils/settings.py

# === RISK PROTECTION TOGGLES ===
ENABLE_DRAWDOWN_GUARD = True
MAX_DRAWDOWN_PERCENT = 10  # Stop trading if equity drops below 90% of balance

# === REBATE TRACKING TOGGLES ===
ENABLE_REBATE_TRACKING = True
REBATE_PER_LOT = 7.0  # USD per lot traded (broker-specific, update accordingly)

# === OTHER FUTURE TOGGLES (scaffolds) ===
ENABLE_TRADE_CYCLE = False
ENABLE_PROFIT_TARGET_STOP = False

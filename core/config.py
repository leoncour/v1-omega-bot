# Safety Toggles
ENABLE_DRAWDOWN_GUARD = True
MAX_DRAWDOWN_PERCENT = 10  # e.g. 10% max drawdown before halting

ENABLE_TRADE_LIMIT = True
MAX_TRADES_GLOBAL = 1000
MAX_TRADES_PER_SYMBOL = 20

# 🔁 Expanded symbol list (Majors + Minors)
SYMBOLS = [
    "EURUSD", "GBPUSD", "USDJPY", "USDCHF", "USDCAD", "AUDUSD", "NZDUSD", "XAUUSD",  # Majors + Gold
    "EURGBP", "EURJPY", "EURCHF", "EURAUD", "EURNZD",
    "GBPJPY", "GBPCHF", "GBPAUD", "GBPNZD",
    "AUDJPY", "AUDCHF", "AUDNZD",
    "CADJPY", "CHFJPY", "NZDJPY", "NZDCHF"
]

# ✅ Strategy Toggles
ENABLE_TRENDING = True
ENABLE_RANGING = False
ENABLE_GRID = True  # ✅ Enable Grid Strategy

# 🛑 VWAP is now a helper-only module (do not enable)

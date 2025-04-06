# ✅ Global toggle settings for safety and optimization features

# === Track 1: SAFETY CONTROLS ===

ENABLE_DRAWDOWN_GUARD = True
MAX_DRAWDOWN_PERCENT = 5.0        # Stop trading if equity drops more than X% of balance
DRAWDOWN_MODE = "recovery"        # Options: "hard" = stop all; "recovery" = adaptive risk

ENABLE_DRAWDOWN_RESET_DAILY = True  # ✅ Auto-reset daily drawdown lock the next day

MAX_TRADES_PER_SYMBOL = 3         # Max number of trades allowed per symbol (0 = unlimited)
MAX_TRADES_GLOBAL = 20            # Max number of total trades allowed across all symbols (0 = unlimited)

ENABLE_DAILY_PROFIT_CAP = True
DAILY_PROFIT_TARGET_PCT = 10.0    # Lock trading for the day after hitting this % of gain

# === Track 2: REBATE FARMING ===

ENABLE_REBATE_TRACKING = True
REBATE_PER_LOT = 7.0              # Example: $7 per lot (depends on broker)

ENABLE_TRADE_CYCLE = True
CYCLE_PROFIT_TRIGGER = 0.50       # Restart trade cycle if floating profit > X

# === Track 3: TRADE PACING / TIMING ===

ENABLE_PACING_CONTROL = True
MIN_SECONDS_BETWEEN_TRADES = 90   # Minimum time gap between new entries (recommended: 60–300)

# === Track 4: V1.5 – Symbol Auto-Blocking ===

AUTO_BLOCK_MIN_TRADES = 5             # Don't evaluate symbols until this many trades
AUTO_BLOCK_WINRATE_THRESHOLD = 0.60   # If win rate drops below this, disable symbol
AUTO_BLOCK_MAX_LOSS_STREAK = 3        # Disable symbol after X consecutive losses

# === Experimental & Future Controls (do not modify yet) ===

# ENABLE_HEDGE_MULTIPLIER = False
# ENABLE_FLOATING_PL_HEDGE_TRIGGER = False
# ENABLE_SESSION_LIMITS = False

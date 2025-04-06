import MetaTrader5 as mt5
import os
from datetime import datetime
from utils.settings import (
    ENABLE_DRAWDOWN_GUARD, MAX_DRAWDOWN_PERCENT, DRAWDOWN_MODE,
    ENABLE_DRAWDOWN_RESET_DAILY, MAX_TRADES_GLOBAL, MAX_TRADES_PER_SYMBOL
)
from utils.symbol_performance import get_lot_multiplier

LOCK_FILE = "drawdown.lock"

def get_optimized_lot_size(symbol=""):
    acc = mt5.account_info()
    if acc is None:
        print("⚠️ Cannot get lot size – MT5 not connected.")
        return 0.01
    bal = acc.balance
    base_lot = max(0.01, min(round(bal * 0.00005, 2), 0.02))
    multiplier = get_lot_multiplier(symbol)
    return round(base_lot * multiplier, 2)

def check_drawdown():
    if not ENABLE_DRAWDOWN_GUARD:
        return False

    today = datetime.now().strftime("%Y-%m-%d")
    if ENABLE_DRAWDOWN_RESET_DAILY and os.path.exists(LOCK_FILE):
        with open(LOCK_FILE, "r") as f:
            saved_date = f.read().strip()
        if saved_date != today:
            os.remove(LOCK_FILE)
            print("🟢 New day — previous drawdown lock cleared.")

    if os.path.exists(LOCK_FILE):
        print("🛑 Drawdown lock active — trading halted for the day.")
        return True

    acc = mt5.account_info()
    if acc is None:
        print("⚠️ Cannot check drawdown – MT5 not connected.")
        return True

    balance = acc.balance
    equity = acc.equity
    if balance == 0:
        return False
    drawdown = (1 - equity / balance) * 100

    if drawdown >= MAX_DRAWDOWN_PERCENT:
        with open(LOCK_FILE, "w") as f:
            f.write(today)
        if DRAWDOWN_MODE == "hard":
            print(f"🛑 Trading halted – Drawdown {drawdown:.2f}% exceeds limit of {MAX_DRAWDOWN_PERCENT}%")
            return True
        elif DRAWDOWN_MODE == "recovery":
            print(f"⚠️ Drawdown {drawdown:.2f}% – switching to recovery mode.")
            return "recovery"

    return False

# ✅ Trade Count Limit Helpers

def get_open_trades_count(symbol=None):
    positions = mt5.positions_get()
    if not positions:
        return 0
    if symbol:
        return len([p for p in positions if p.symbol == symbol])
    return len(positions)

def trades_within_limit(symbol):
    global_count = get_open_trades_count()
    symbol_count = get_open_trades_count(symbol)

    if MAX_TRADES_GLOBAL and global_count >= MAX_TRADES_GLOBAL:
        return False
    if MAX_TRADES_PER_SYMBOL and symbol_count >= MAX_TRADES_PER_SYMBOL:
        return False
    return True

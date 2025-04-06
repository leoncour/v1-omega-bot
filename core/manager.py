# manager.py – Strategy Dispatcher

import MetaTrader5 as mt5
import time
import datetime

from utils.market_snapshot import get_market_data
from utils.trend_filters import classify_trend
from utils.safety import drawdown_guard, max_trade_guard
from utils.trailing import modify_trade_with_trailing  # ✅ FIXED
from utils.price import fetch_atr
from utils.symbol_stats import should_trade_symbol
from core.config import ENABLE_TRENDING, ENABLE_RANGING, ENABLE_GRID

# === Strategy Imports ===
from break_retest import execute_break_retest_trade
from hedging import hedge_trade
from strategies.h1_grid import h1_grid_trade

# Cooldown system (per symbol/strategy)
last_trade_time = {}
COOLDOWN_SECONDS = 300  # 5 minutes default

def is_cooldown(symbol, strategy):
    now = time.time()
    if symbol not in last_trade_time:
        last_trade_time[symbol] = {
            "break_retest": 0,
            "hedge": 0,
            "grid": 0
        }
    return now - last_trade_time[symbol][strategy] < COOLDOWN_SECONDS

def mark_trade_time(symbol, strategy):
    last_trade_time[symbol][strategy] = time.time()

def process_symbol(symbol, recovery_mode=False):
    now_utc = datetime.datetime.utcnow().time()
    if datetime.time(21, 55) <= now_utc <= datetime.time(23, 0):
        print(f"[{symbol}] ⏳ Skipped – time lockdown (21:55–23:00 GMT).")
        return

    if not should_trade_symbol(symbol):
        print(f"[{symbol}] ❌ Skipped – Auto-blocked due to low performance.")
        return

    tick, ema_m1, atr, rsi, vwap, ema_m5, ema_m15 = get_market_data(symbol)
    if not tick:
        print(f"[{symbol}] Skipped – No tick data.")
        return

    trend = classify_trend(ema_m1, ema_m5, ema_m15)
    print(f"📊 {symbol} → {trend.capitalize()} trend")

    if drawdown_guard() or max_trade_guard(symbol):
        return

    if recovery_mode:
        print(f"[{symbol}] 🔄 Recovery mode active – conservative logic.")

    # === Trend Continuation Logic ===
    if trend == "strong" and ENABLE_TRENDING and not is_cooldown(symbol, "break_retest"):
        if execute_break_retest_trade(symbol, ema_m1, atr, trend):
            mark_trade_time(symbol, "break_retest")

    # === Grid Strategy ===
    if ENABLE_GRID and not is_cooldown(symbol, "grid"):
        if h1_grid_trade(symbol):
            mark_trade_time(symbol, "grid")

    # === Range/Hedge ===
    if ENABLE_RANGING and not is_cooldown(symbol, "hedge"):
        if hedge_trade(symbol, atr, rsi, trend):
            mark_trade_time(symbol, "hedge")

    # === Trailing Stop Handling ===
    positions = mt5.positions_get(symbol=symbol)
    if positions:
        for pos in positions:
            modify_trade_with_trailing(
                symbol,
                pos.ticket,
                pos.type,
                fetch_atr(symbol, mt5.TIMEFRAME_M1),
                trend
            )

import MetaTrader5 as mt5
from utils import (
    initialize_mt5,
    get_market_data,
    classify_trend
)
from grid_trading import grid_trade
from break_retest import execute_break_retest_trade
from hedging import hedge_trade
from vwap_trading import execute_vwap_trade

symbol = "EURUSD"

initialize_mt5()

print("✅ Manual Trigger Console Loaded")
print("Type one of the following to manually test a strategy:")
print("  [1] Grid Trade")
print("  [2] VWAP Trade")
print("  [3] Break & Retest")
print("  [4] Hedge Trade")
print("  [q] Quit")

while True:
    cmd = input("\nEnter Strategy Number: ").strip().lower()

    tick, ema_m1, atr, rsi, vwap, ema_m5, ema_m15 = get_market_data(symbol)
    trend_strength = classify_trend(ema_m1, ema_m5, ema_m15)

    if cmd == "1":
        print("🔘 Manually triggering Grid Trade...")
        grid_trade(symbol, atr, rsi, trend_strength)
    elif cmd == "2":
        print("🔘 Manually triggering VWAP Trade...")
        execute_vwap_trade(symbol, ema_m1, vwap, atr, trend_strength)
    elif cmd == "3":
        print("🔘 Manually triggering Break & Retest...")
        execute_break_retest_trade(symbol, ema_m1, atr, trend_strength)
    elif cmd == "4":
        print("🔘 Manually triggering Hedge Trade...")
        hedge_trade(symbol, atr, rsi)
    elif cmd == "q":
        print("👋 Exiting manual trigger console.")
        break
    else:
        print("❓ Unknown command. Use [1-4] or [q] to quit.")

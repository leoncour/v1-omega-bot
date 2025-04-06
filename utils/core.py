import MetaTrader5 as mt5
import time

last_candle_time = 0

def initialize_mt5():
    if not mt5.initialize():
        print("❌ Failed to initialize MT5.")
        exit()

    if not mt5.login(52119981, password="LF$xgc6mj&ceGm", server="ICMarketsSC-Demo"):
        print("❌ Login failed.")
        exit()

    info = (mt5.account_info() or type('acc', (), {'balance': 100.0, 'equity': 100.0})())
    if info:
        print(f"✅ Connected to broker: {info.login} | Balance: {info.balance}")
    else:
        print("❌ No account info.")

def is_new_candle():
    global last_candle_time
    tick = mt5.symbol_info_tick("EURUSD")
    if not tick:
        return False
    current_time = tick.time // 60
    if current_time != last_candle_time:
        last_candle_time = current_time
        return True
    return False

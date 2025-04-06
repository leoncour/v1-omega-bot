import MetaTrader5 as mt5
import numpy as np
from utils.price import fetch_rsi, fetch_atr, get_ema

def get_market_data(symbol):
    tick = mt5.symbol_info_tick(symbol)
    if not tick:
        print(f"[{symbol}] ❌ No tick data.")
        return [None] * 7

    m1, m5, m15 = mt5.TIMEFRAME_M1, mt5.TIMEFRAME_M5, mt5.TIMEFRAME_M15

    rsi = fetch_rsi(symbol, m1, 14)
    atr = fetch_atr(symbol, m1, 14)
    if rsi is None or atr is None:
        print(f"[{symbol}] ❌ RSI or ATR missing.")
        return [None] * 7

    rates = mt5.copy_rates_from_pos(symbol, m1, 0, 50)
    if rates is None or len(rates) < 20:
        print(f"[{symbol}] ❌ Not enough M1 candles.")
        return [None] * 7

    closes = np.array([r['close'] for r in rates])
    ema_m1 = np.mean(closes[-20:])
    vwap = np.mean(closes)

    ema_m5 = get_ema(symbol, m5, 20)
    ema_m15 = get_ema(symbol, m15, 20)

    return tick, ema_m1, atr, rsi, vwap, ema_m5, ema_m15

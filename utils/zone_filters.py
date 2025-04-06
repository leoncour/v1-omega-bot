import MetaTrader5 as mt5
import numpy as np

def detect_sr_zones(symbol, threshold=10):
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 50)
    if rates is None or len(rates) < 30:
        return False
    closes = np.array([bar['close'] for bar in rates])
    max_close = np.max(closes)
    min_close = np.min(closes)
    range_pips = abs(max_close - min_close)
    if symbol == "XAUUSD":
        return range_pips < 2.5
    return range_pips < 0.0015

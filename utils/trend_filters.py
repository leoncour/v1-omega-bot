import MetaTrader5 as mt5
import numpy as np

def is_htf_aligned(symbol, trend_strength):
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 0, 20)
    if rates is None or len(rates) < 20:
        return False
    closes = np.array([bar['close'] for bar in rates])
    slope = closes[-1] - closes[-10]
    return abs(slope) > 0.001 if trend_strength == "strong" else True

def is_trend_continuation(symbol, trend_strength):
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 0, 5)
    if rates is None or len(rates) < 5:
        return False
    closes = [bar['close'] for bar in rates]
    if trend_strength == "strong":
        return closes[-1] > closes[0] and closes[-1] > closes[-2]
    elif trend_strength == "ranging":
        return False
    else:
        return closes[-1] < closes[0] and closes[-1] < closes[-2]

def classify_trend(ema1, ema5, ema15):
    if ema1 is None or ema5 is None or ema15 is None:
        return "unknown"
    if ema1 > ema5 > ema15 or ema1 < ema5 < ema15:
        slope = abs(ema1 - ema15)
        if slope > 0.002:
            return "strong"
        elif slope > 0.001:
            return "normal"
    return "ranging"

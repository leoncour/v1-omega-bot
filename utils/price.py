import MetaTrader5 as mt5
import numpy as np

def fetch_rsi(symbol, timeframe, period=14):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, period + 1)
    if rates is None or len(rates) < period + 1:
        return 50  # default fallback
    closes = np.array([bar['close'] for bar in rates])
    deltas = np.diff(closes)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.mean(gains[-period:])
    avg_loss = np.mean(losses[-period:])
    rs = avg_gain / (avg_loss + 1e-6)
    return 100 - (100 / (1 + rs))

def fetch_atr(symbol, timeframe, period=14):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, period + 1)
    if rates is None or len(rates) < period + 1:
        return None
    highs = [r['high'] for r in rates]
    lows = [r['low'] for r in rates]
    closes = [r['close'] for r in rates]
    tr_list = [
        max(highs[i] - lows[i], abs(highs[i] - closes[i-1]), abs(lows[i] - closes[i-1]))
        for i in range(1, len(highs))
    ]
    return np.mean(tr_list)

def get_ema(symbol, timeframe, period=20):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, period + 1)
    if rates is None or len(rates) < period:
        return None
    closes = np.array([r['close'] for r in rates])
    weights = np.exp(np.linspace(-1., 0., period))
    weights /= weights.sum()
    return np.convolve(closes, weights, mode='valid')[-1]

def get_atr_slope(symbol, period=14):
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, period + 1)
    if rates is None or len(rates) < period + 1:
        return 0.0
    closes = np.array([bar['close'] for bar in rates])
    atr_series = np.abs(np.diff(closes))
    return atr_series[-1] - atr_series[0]

import MetaTrader5 as mt5

def detect_engulfing(symbol):
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 3)
    if rates is None or len(rates) < 3:
        return False
    prev = rates[-2]
    curr = rates[-1]
    # Full bullish or bearish engulfing
    return (
        prev['close'] < prev['open'] and
        curr['close'] > curr['open'] and
        curr['open'] < prev['close'] and
        curr['close'] > prev['open']
    ) or (
        prev['close'] > prev['open'] and
        curr['close'] < curr['open'] and
        curr['open'] > prev['close'] and
        curr['close'] < prev['open']
    )

def is_rejection_candle(symbol):
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 3)
    if rates is None or len(rates) < 3:
        return False
    candle = rates[-2]
    body = abs(candle['open'] - candle['close'])
    wick_top = candle['high'] - max(candle['open'], candle['close'])
    wick_bottom = min(candle['open'], candle['close']) - candle['low']
    return wick_top > 2 * body or wick_bottom > 2 * body

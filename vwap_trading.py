# vwap_trading.py (Helper Mode Only – No Trades)

import MetaTrader5 as mt5
from utils.trend_filters import is_htf_aligned
from utils.candle_patterns import detect_engulfing, is_rejection_candle
from utils.rsi_filters import adaptive_rsi_filter
from utils.price import fetch_rsi
from utils.risk import trades_within_limit
from utils.spread_filter import spread_is_acceptable

def analyze_vwap_context(symbol, ema, vwap, atr, trend_strength):
    print(f"[VWAP] Mean reversion context for {symbol}")

    # ✅ Check trade cap logic — just log if blocked
    if not trades_within_limit(symbol):
        print(f"[{symbol} - VWAP] ⛔ Max open trade limit hit. No signal.")
        return False

    tick = mt5.symbol_info_tick(symbol)
    if not tick or tick.ask is None:
        print(f"[{symbol} - VWAP] ❌ Skipped – No tick data.")
        return False

    if not spread_is_acceptable(symbol):
        print(f"[{symbol} - VWAP] ❌ Spread too high.")
        return False

    price = tick.ask

    rsi = fetch_rsi(symbol, mt5.TIMEFRAME_M1, 14)
    if not adaptive_rsi_filter(rsi, trend_strength, symbol):
        print(f"[{symbol} - VWAP] ⚠️ RSI rejected trend continuation.")
        return False

    if not is_htf_aligned(symbol, trend_strength):
        print(f"[{symbol} - VWAP] ⚠️ HTF misaligned.")
        return False

    rejection = is_rejection_candle(symbol)
    engulfing = detect_engulfing(symbol)

    if not (rejection or engulfing):
        print(f"[{symbol} - VWAP] ⚠️ No valid candle pattern.")
        return False

    # ✅ Signal passed, but no trade executed
    print(f"[{symbol} - VWAP] ✅ Passed all filters (price {'above' if price > vwap else 'below'} VWAP). No entry – helper mode only.")
    return True

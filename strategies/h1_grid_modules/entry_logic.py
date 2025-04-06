import MetaTrader5 as mt5
from utils.price import fetch_atr
from utils.spread_filter import spread_is_acceptable
from utils.zone_filters import detect_sr_zones
from utils.risk import trades_within_limit
from utils.candle_patterns import detect_engulfing, is_rejection_candle

def check_entry_conditions(symbol, logger=None, layer=1):
    """
    Validates grid entry conditions for a given symbol.
    Includes ATR, SR zone, spread, trade limits, and layer-level logic.
    """

    if not trades_within_limit(symbol):
        if logger:
            logger(f"{symbol} ❌ Blocked – max open trade limit reached.")
        return False

    # ✅ Base ATR Check
    atr = fetch_atr(symbol, mt5.TIMEFRAME_H1, 14)
    if atr is None:
        if logger: logger(f"{symbol} ❌ Blocked – No ATR data.")
        return False

    # ATR thresholds per type
    if symbol == "XAUUSD" and atr > 4.0:
        if logger: logger(f"{symbol} ❌ Blocked – ATR too high for gold ({atr:.2f})")
        return False
    elif symbol.endswith("JPY") and atr > 0.4:
        if logger: logger(f"{symbol} ❌ Blocked – ATR too high for JPY ({atr:.4f})")
        return False
    elif atr > 0.002:
        if logger: logger(f"{symbol} ❌ Blocked – ATR too high for major ({atr:.5f})")
        return False

    # ✅ Spread Guard
    if not spread_is_acceptable(symbol):
        if logger: logger(f"{symbol} ❌ Blocked – spread too high.")
        return False

    # ✅ SR Zone Required (Range edge filter)
    in_sr_zone = detect_sr_zones(symbol)
    if not in_sr_zone:
        if logger: logger(f"{symbol} ❌ Blocked – not near SR zone.")
        return False

    # ✅ Smarter L1–L2 entry filters (2 of 4 logic)
    if layer <= 2:
        filters_passed = 0
        if in_sr_zone:
            filters_passed += 1
        if atr < 0.001:  # customizable threshold for "stable"
            filters_passed += 1
        if is_rejection_candle(symbol):
            filters_passed += 1
        if detect_engulfing(symbol):
            filters_passed += 1

        if filters_passed < 2:
            if logger: logger(f"{symbol} ❌ L{layer} entry blocked – only {filters_passed}/4 conditions met.")
            return False
        else:
            if logger: logger(f"{symbol} ✅ L{layer} entry passed – {filters_passed}/4 filters met.")

    return True

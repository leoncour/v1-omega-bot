import MetaTrader5 as mt5
from utils.trend_filters import is_htf_aligned
from utils.rsi_filters import adaptive_rsi_filter
from utils.trade import execute_trade
from utils.price import fetch_rsi, get_atr_slope
from utils.pips import get_pip_value
from utils.risk import get_optimized_lot_size, trades_within_limit
from utils.spread_filter import spread_is_acceptable
from utils.candle_patterns import detect_engulfing, is_rejection_candle
from strategies.h1_grid_modules.comment_utils import generate_comment

def execute_break_retest_trade(symbol, ema, atr, trend_strength):
    print(f'[BreakRetest] Entry logic for {symbol}')

    # ✅ Check trade limits
    if not trades_within_limit(symbol):
        print(f"[{symbol} - BreakRetest] ❌ Skipped – max open trade limit reached.")
        return False

    tick = mt5.symbol_info_tick(symbol)
    if not tick or tick.ask is None:
        print(f"[{symbol}] Skipped – No tick data.")
        return False

    if not spread_is_acceptable(symbol):
        return False

    if not is_htf_aligned(symbol, trend_strength):
        print(f"[{symbol} - BreakRetest] Skipped – HTF misaligned.")
        return False

    rsi = fetch_rsi(symbol, mt5.TIMEFRAME_M1, 14)
    if not adaptive_rsi_filter(rsi, trend_strength, symbol):
        print(f"[{symbol} - BreakRetest] Skipped – RSI filter blocked entry.")
        return False

    if get_atr_slope(symbol) < 0.00005:
        print(f"[{symbol} - BreakRetest] Skipped – ATR slope too flat.")
        return False

    has_rejection = is_rejection_candle(symbol)
    has_engulfing = detect_engulfing(symbol)
    if not (has_rejection or has_engulfing):
        print(f"[{symbol} - BreakRetest] Skipped – No valid candle pattern.")
        return False

    price = tick.ask
    trade_type = 0 if trend_strength == "strong" else 1
    lot = get_optimized_lot_size()
    comment = generate_comment("BRK", symbol, trade_type, tag="v2.3")
    return execute_trade(symbol, price, lot, trade_type, atr, trend_strength, comment)

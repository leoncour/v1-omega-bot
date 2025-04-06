import MetaTrader5 as mt5
from utils.metrics import log_lot_volume
from utils.pips import get_pip_value
from utils.symbol_stats import should_trade_symbol
from utils.spread_filter import spread_is_acceptable  # ✅ FIXED

# === SL/TP calculation ===
def calculate_sl_tp(price, pip, trade_type, sl_pips=8, rr_ratio=1.0, symbol=""):
    sl_distance = pip * sl_pips
    tp_distance = sl_distance * rr_ratio

    if trade_type == mt5.ORDER_TYPE_BUY:
        sl = price - sl_distance
        tp = price + tp_distance
    else:
        sl = price + sl_distance
        tp = price - tp_distance

    precision = 2 if "XAU" in symbol or "GOLD" in symbol else 5
    return round(sl, precision), round(tp, precision)

# === Main trade executor ===
def execute_trade(symbol, price, lot, trade_type, atr, trend, comment):
    if not should_trade_symbol(symbol):
        print(f"[{symbol}] 🚫 Auto-disabled – trade skipped.")
        return False

    if (symbol == "XAUUSD" and atr > 5) or (symbol != "XAUUSD" and atr > 0.0025):
        print(f"[{symbol}] Skipped – ATR too high: {atr}")
        return False

    if not spread_is_acceptable(symbol):
        print(f"[{symbol}] ❌ Spread too high – trade blocked.")
        return False

    pip = get_pip_value(symbol)
    sl, tp = calculate_sl_tp(price, pip, trade_type, sl_pips=8, rr_ratio=1.0, symbol=symbol)

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": trade_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 5,
        "type_filling": mt5.ORDER_FILLING_IOC,
        "comment": comment
    }

    result = mt5.order_send(request)

    if result and result.retcode == mt5.TRADE_RETCODE_DONE:
        log_lot_volume(symbol, lot)
        print(f"[{symbol}] ✅ Trade executed: {comment}")
        return True

    print(f"[{symbol}] ❌ Trade failed: {getattr(result, 'retcode', 'No result')}")
    return False

# === Placeholder for future reversal spike strategy ===
def detect_reversal_spike(symbol):
    return False, None

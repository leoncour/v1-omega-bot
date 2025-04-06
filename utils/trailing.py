# utils/trailing.py
import MetaTrader5 as mt5
from utils.pips import get_pip_value
from utils.spread_filter import get_current_spread

# === SPREAD LIMITS ===
SPREAD_LIMITS = {
    "XAUUSD": 40,
    "USDJPY": 25, "EURJPY": 25, "GBPJPY": 25, "CHFJPY": 25,
    "CADJPY": 25, "AUDJPY": 25, "NZDJPY": 25,
    # Others default to 20
}

def modify_trade_with_trailing(symbol, ticket, trade_type, atr, trend):
    pip = get_pip_value(symbol)
    trailing_trigger = pip * 6
    trailing_sl_buffer = pip * 3

    spread = get_current_spread(symbol)
    if spread is None:
        print(f"[{symbol}] ⚠️ No tick data – skipping trailing.")
        return False

    spread_limit = SPREAD_LIMITS.get(symbol, 20) * pip
    if spread > spread_limit:
        print(f"[{symbol}] ⛔️ Spread too high ({spread:.5f}) – trailing blocked.")
        return False

    tick = mt5.symbol_info_tick(symbol)
    if not tick:
        return False

    current_price = tick.ask if trade_type == mt5.ORDER_TYPE_BUY else tick.bid
    position = mt5.positions_get(ticket=ticket)
    if not position:
        return False

    pos = position[0]
    open_price = pos.price_open
    existing_sl = pos.sl
    profit = current_price - open_price if trade_type == mt5.ORDER_TYPE_BUY else open_price - current_price

    if profit < trailing_trigger:
        return False

    new_sl = open_price + trailing_sl_buffer if trade_type == mt5.ORDER_TYPE_BUY else open_price - trailing_sl_buffer

    if (trade_type == mt5.ORDER_TYPE_BUY and new_sl < existing_sl) or \
       (trade_type == mt5.ORDER_TYPE_SELL and new_sl > existing_sl):
        return False

    request = {
        "action": mt5.TRADE_ACTION_SLTP,
        "symbol": symbol,
        "sl": round(new_sl, 5),
        "tp": pos.tp,
        "position": ticket
    }

    result = mt5.order_send(request)
    if result and result.retcode == mt5.TRADE_RETCODE_DONE:
        print(f"[{symbol}] 🔐 Trailing SL updated at {new_sl}")
        return True
    else:
        print(f"[{symbol}] ⚠️ Failed to trail SL: {getattr(result, 'retcode', 'No result')}")
        return False

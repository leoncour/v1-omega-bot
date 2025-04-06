import MetaTrader5 as mt5
from utils.risk import get_optimized_lot_size
from utils.symbol_stats import update_symbol_stats
from utils.spread_filter import spread_is_acceptable  # ✅ FIXED

def close_and_reopen(symbol, trade_type, lot, comment):
    tick = mt5.symbol_info_tick(symbol)
    if not tick:
        print(f"[{symbol}] ❌ No tick data for reopen.")
        return False

    price = tick.bid if trade_type == mt5.ORDER_TYPE_SELL else tick.ask

    # Step 1: Close matching open positions and track results
    positions = mt5.positions_get(symbol=symbol)
    for pos in positions:
        if pos.type == trade_type:
            # Exit Spread Guard (use correct checker)
            if not spread_is_acceptable(symbol):
                print(f"[{symbol}] ⛔️ Spread too high – cycle close skipped.")
                return False

            close_request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": pos.volume,
                "type": mt5.ORDER_TYPE_SELL if trade_type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY,
                "position": pos.ticket,
                "price": tick.bid if trade_type == mt5.ORDER_TYPE_BUY else tick.ask,
                "deviation": 5
            }

            close_result = mt5.order_send(close_request)

            if not close_result:
                print(f"[{symbol}] ❌ Close failed – no result returned.")
                return False
            elif close_result.retcode != mt5.TRADE_RETCODE_DONE:
                print(f"[{symbol}] ❌ Close failed – code: {close_result.retcode}")
                return False

            update_symbol_stats(symbol, pos.profit)

    # Step 2: Re-open trade using same size and direction
    reopen_request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": trade_type,
        "price": price,
        "sl": 0,
        "tp": 0,
        "deviation": 5,
        "type_filling": mt5.ORDER_FILLING_IOC,
        "comment": f"{comment} | cycle"
    }

    reopen_result = mt5.order_send(reopen_request)

    if not reopen_result:
        print(f"[{symbol}] ❌ Reopen failed – no result returned.")
        return False

    if reopen_result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"[{symbol}] ❌ Reopen failed – code: {reopen_result.retcode}")
        return False

    print(f"[{symbol}] ✅ Trade cycled successfully.")
    return True

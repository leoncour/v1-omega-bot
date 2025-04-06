# exit_logic.py – H1 Grid Exit Module

import MetaTrader5 as mt5
from utils.symbol_stats import update_symbol_stats  # ✅ NEW

def should_close_at_breakeven(symbol, positions, account_balance, grid_profit_per_lot, logger):
    if not positions:
        return False

    total_profit = sum(p.profit for p in positions)
    total_lot = sum(p.volume for p in positions)

    min_target = max(account_balance * 0.002, 1.0)
    lot_target = total_lot * grid_profit_per_lot / 100.0
    target = max(min_target, lot_target)

    logger(f"{symbol} 🔍 Breakeven Check → Profit: ${total_profit:.2f}, Target: ${target:.2f}")
    return total_profit >= target

def close_positions(symbol, positions, logger):
    for pos in positions:
        close_type = mt5.ORDER_TYPE_SELL if pos.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
        tick = mt5.symbol_info_tick(symbol)
        price = tick.bid if pos.type == mt5.ORDER_TYPE_BUY else tick.ask
        close_request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": pos.volume,
            "type": close_type,
            "position": pos.ticket,
            "price": price,
            "deviation": 5
        }
        result = mt5.order_send(close_request)

        if result and result.retcode == mt5.TRADE_RETCODE_DONE:
            logger(f"{symbol} ✅ Closed grid pos {pos.ticket} @ breakeven")
        else:
            logger(f"{symbol} ❌ Failed to close pos {pos.ticket}: {getattr(result, 'retcode', 'No result')}")

        # ✅ Update symbol performance tracking (V1.5)
        update_symbol_stats(symbol, pos.profit)

import MetaTrader5 as mt5
from utils.rsi_filters import adaptive_rsi_filter
from utils.trade import execute_trade
from utils.price import fetch_rsi
from utils.pips import get_pip_value
from utils.risk import get_optimized_lot_size
from utils.spread_filter import spread_is_acceptable

def hedge_trade(symbol, atr, rsi, trend_strength):
    print(f"[Hedge] Entry logic for {symbol}")

    if not spread_is_acceptable(symbol):
        return False

    # Primary RSI filter
    if adaptive_rsi_filter(rsi, trend_strength, symbol):
        if rsi > 70:
            trade_type = 1  # SELL
        elif rsi < 30:
            trade_type = 0  # BUY
        else:
            print(f"[{symbol} - Hedge] Not triggered → RSI not >70 or <30")
            return False
    else:
        # Fallback logic: if RSI filter fails, check for extreme conditions
        if rsi >= 80:
            print(f"[{symbol} - Hedge] RSI extreme SELL fallback")
            trade_type = 1
        elif rsi <= 20:
            print(f"[{symbol} - Hedge] RSI extreme BUY fallback")
            trade_type = 0
        else:
            print(f"[{symbol} - Hedge] Skipped – RSI filter blocked entry.")
            return False

    tick = mt5.symbol_info_tick(symbol)
    if not tick:
        print(f"[{symbol} - Hedge] No tick data available.")
        return False

    price = tick.ask if trade_type == 0 else tick.bid
    lot = get_optimized_lot_size()
    return execute_trade(symbol, price, lot, trade_type, atr, trend_strength, "Hedge v1.4")

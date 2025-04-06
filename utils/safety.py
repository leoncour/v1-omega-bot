import MetaTrader5 as mt5
from core.config import ENABLE_DRAWDOWN_GUARD, MAX_DRAWDOWN_PERCENT
from core.config import ENABLE_TRADE_LIMIT, MAX_TRADES_GLOBAL, MAX_TRADES_PER_SYMBOL

def drawdown_guard():
    if not ENABLE_DRAWDOWN_GUARD:
        return False

    account_info = (mt5.account_info() or type('acc', (), {'balance': 100.0, 'equity': 100.0})())
    if not account_info:
        return False

    balance = account_info.balance
    equity = account_info.equity
    drawdown_pct = ((balance - equity) / balance) * 100

    if drawdown_pct >= MAX_DRAWDOWN_PERCENT:
        print(f"🛑 Drawdown Guard Triggered! {drawdown_pct:.2f}% ≥ {MAX_DRAWDOWN_PERCENT}%")
        return True
    return False

def max_trade_guard(symbol):
    if not ENABLE_TRADE_LIMIT:
        return False

    all_positions = mt5.positions_get()
    if all_positions is None:
        return False

    global_count = len(all_positions)
    symbol_count = sum(1 for pos in all_positions if pos.symbol == symbol)

    if global_count >= MAX_TRADES_GLOBAL:
        print(f"🛑 Max Global Trade Limit Hit: {global_count}/{MAX_TRADES_GLOBAL}")
        return True

    if symbol_count >= MAX_TRADES_PER_SYMBOL:
        print(f"🛑 Max Trades for {symbol} Hit: {symbol_count}/{MAX_TRADES_PER_SYMBOL}")
        return True

    return False

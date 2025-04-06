import MetaTrader5 as mt5
from datetime import datetime
import os

from utils.trade import execute_trade
from utils.spread_filter import spread_is_acceptable
from utils.risk import get_optimized_lot_size
from strategies.h1_grid_modules.comment_utils import parse_comment

# === Hedge Settings ===
HEDGE_TRIGGER_LOT = 0.06        # Total lot size across grid
HEDGE_TRIGGER_IMBALANCE = 0.04  # Must be this imbalanced (net BUY or SELL)
HEDGE_MODE = "GRID_ONLY"        # "ALL" includes VWAP + BRK

STRATEGIES_TO_HEDGE = ["GRD"] if HEDGE_MODE == "GRID_ONLY" else ["GRD", "VWAP", "BRK"]

# === [Future Upgrade Placeholders] ===
# - Dynamically scale HEDGE_TRIGGER_LOT based on balance
# - Enable hedge multipliers (e.g. 1.5x net imbalance)
# - Allow floating P/L-based hedge triggers (e.g. if drawdown > $3)
# - Enable continuation hedging if grid expands post-hedge
# - Add session-based hedge filters (e.g. London-only)
# - Remove lot cap for grid level 1 on larger accounts

# === Hedge Logging Setup ===
LOG_FOLDER = os.path.join("strategies", "logs")
os.makedirs(LOG_FOLDER, exist_ok=True)
today = datetime.now().strftime("%Y-%m-%d")
LOG_FILE = os.path.join(LOG_FOLDER, f"hedge_{today}.log")

def log_hedge(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

# === Hedge Logic ===

def calculate_net_direction(symbol, strategy_prefixes):
    positions = mt5.positions_get()
    if not positions:
        return 0, 0

    net = 0
    total_lots = 0
    for pos in positions:
        if not pos.comment or pos.symbol != symbol:
            continue
        for strategy in strategy_prefixes:
            if pos.comment.startswith(strategy):
                vol = pos.volume
                total_lots += vol
                net += vol if pos.type == mt5.ORDER_TYPE_BUY else -vol

    return net, total_lots

def has_open_hedge(symbol):
    positions = mt5.positions_get(symbol=symbol)
    if not positions:
        return False
    for p in positions:
        if p.comment and p.comment.startswith("HEDGE"):
            return True
    return False

def open_hedge_trade(symbol, direction):
    if not spread_is_acceptable(symbol):
        log_hedge(f"{symbol} ❌ Hedge skipped — spread too high.")
        return False

    lot = get_optimized_lot_size(symbol)
    price = mt5.symbol_info_tick(symbol).ask if direction == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).bid
    comment = f"HEDGE_{symbol}_{'BUY' if direction == mt5.ORDER_TYPE_BUY else 'SELL'}"
    success = execute_trade(symbol, price, lot, direction, atr=0, trend="hedge", comment=comment)
    log_hedge(f"{symbol} ✅ Hedge opened: {comment} | Lot: {lot}")
    return success

def close_hedge_trades(symbol):
    positions = mt5.positions_get(symbol=symbol)
    for p in positions:
        if p.comment and p.comment.startswith("HEDGE"):
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "position": p.ticket,
                "volume": p.volume,
                "type": mt5.ORDER_TYPE_SELL if p.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY,
                "price": mt5.symbol_info_tick(symbol).bid if p.type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).ask,
                "deviation": 10,
                "magic": 0,
                "comment": "HEDGE_CLOSE"
            }
            mt5.order_send(request)
            log_hedge(f"{symbol} 🔁 Hedge closed: {p.comment} | Lot: {p.volume}")

def hedge_cycle(symbol):
    net_dir, lot_size = calculate_net_direction(symbol, strategy_prefixes=STRATEGIES_TO_HEDGE)

    if abs(net_dir) >= HEDGE_TRIGGER_IMBALANCE and lot_size >= HEDGE_TRIGGER_LOT:
        if not has_open_hedge(symbol):
            direction = mt5.ORDER_TYPE_SELL if net_dir > 0 else mt5.ORDER_TYPE_BUY
            log_hedge(f"{symbol} ⚠️ Hedge triggered — Net Imbalance: {net_dir:.2f} | Total Lots: {lot_size:.2f}")
            open_hedge_trade(symbol, direction)
    else:
        if has_open_hedge(symbol):
            log_hedge(f"{symbol} 🟢 Net exposure normalized — closing hedge.")
            close_hedge_trades(symbol)

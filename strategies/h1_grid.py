# h1_grid.py – Smart Progressive Grid (H1)

import os
import MetaTrader5 as mt5
from datetime import datetime
from utils.trade import execute_trade
from utils.pips import get_pip_value
from utils.price import fetch_rsi
from utils.risk import get_optimized_lot_size

from strategies.h1_grid_modules.exit_logic import should_close_at_breakeven, close_positions
from strategies.h1_grid_modules.entry_logic import check_entry_conditions
from strategies.h1_grid_modules.comment_utils import generate_comment, is_strategy_position  # ✅ FIXED

# === Logging Setup ===
LOG_FOLDER = os.path.join("strategies", "logs")
os.makedirs(LOG_FOLDER, exist_ok=True)
today = datetime.now().strftime("%Y-%m-%d")
LOG_FILE = os.path.join(LOG_FOLDER, f"h1_grid_{today}.log")

def log_h1_grid(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

ENABLED_SYMBOLS_H1 = {
    "XAUUSD": True, "USDJPY": True, "EURUSD": True, "GBPJPY": True, "AUDCAD": True,
    "CADJPY": True, "AUDUSD": True, "NZDUSD": True, "EURGBP": True, "GBPUSD": True,
    "EURJPY": True, "CHFJPY": True, "NZDJPY": True, "USDCAD": True, "EURCHF": True
}

MAX_GRID_LAYERS = 5
GRID_SPACING_PIPS = [5, 7, 10, 13, 17]
TP_BUFFER_PIPS = 2
SL_DISABLED = True
GRID_PROFIT_PER_LOT = 100.0

def is_grid_enabled(symbol):
    return ENABLED_SYMBOLS_H1.get(symbol, False)

def get_account_balance():
    acc = (mt5.account_info() or type('acc', (), {'balance': 100.0, 'equity': 100.0})())
    return acc.balance if acc else 100.0

def get_existing_positions(symbol):
    return [p for p in mt5.positions_get(symbol=symbol) or [] if is_strategy_position(p, "GRD")]  # ✅ FIXED

def calculate_grid_price(symbol, base_price, pip, layer, direction):
    spacing = GRID_SPACING_PIPS[layer - 1]
    offset = spacing * pip
    precision = 1 if "XAU" in symbol or "GOLD" in symbol else 2 if "JPY" in symbol else 4
    new_price = base_price - offset if direction == mt5.ORDER_TYPE_BUY else base_price + offset
    return round(new_price, precision)

def h1_grid_trade(symbol):
    if not is_grid_enabled(symbol):
        log_h1_grid(f"{symbol} Skipped – manually disabled.")
        return False

    tick = mt5.symbol_info_tick(symbol)
    if not tick or tick.bid is None:
        log_h1_grid(f"{symbol} ❌ No tick data.")
        return False

    pip = get_pip_value(symbol)
    rsi = fetch_rsi(symbol, mt5.TIMEFRAME_H1, 14)
    direction = mt5.ORDER_TYPE_BUY if rsi < 50 else mt5.ORDER_TYPE_SELL
    price = tick.ask if direction == mt5.ORDER_TYPE_BUY else tick.bid

    positions = get_existing_positions(symbol)
    layer = len(positions) + 1

    if should_close_at_breakeven(symbol, positions, get_account_balance(), GRID_PROFIT_PER_LOT, log_h1_grid):
        log_h1_grid(f"{symbol} 🔁 Breakeven hit – closing grid.")
        close_positions(symbol, positions, log_h1_grid)
        return False

    if not check_entry_conditions(symbol, logger=log_h1_grid, layer=layer):
        return False

    max_allowed = min(int(get_account_balance() // 200), MAX_GRID_LAYERS)
    if layer > max_allowed:
        log_h1_grid(f"{symbol} ❌ Grid limit reached ({layer}/{max_allowed})")
        return False

    grid_price = calculate_grid_price(symbol, price, pip, layer, direction)
    comment = generate_comment("GRD", symbol, direction, tag=f"L{layer}")  # ✅ FIXED

    log_h1_grid(f"{symbol} ✅ Placing Layer {layer} @ {grid_price:.5f}")
    return execute_trade(symbol, grid_price, get_optimized_lot_size(), direction, atr=0, trend="grid", comment=comment)

# grid_trading.py
from h1_grid import execute_h1_grid_trade  # New H1 grid strategy module

# === Manual symbol toggles (future use) ===
ENABLED_SYMBOLS = {
    "XAUUSD": True,
    "EURUSD": True,
    "USDJPY": True,
    # Add more if needed
}

def is_grid_enabled(symbol):
    return ENABLED_SYMBOLS.get(symbol, False)

# === Grid router function ===
def grid_trade(symbol, atr, rsi, trend):
    if not is_grid_enabled(symbol):
        print(f"[{symbol}] Grid strategy is manually disabled.")
        return False
    return execute_h1_grid_trade(symbol, atr, rsi, trend)

import MetaTrader5 as mt5
from utils.pips import get_pip_value

# 🔧 Per-symbol pip tolerance (fine-tuned to broker)
def get_max_spread_pips(symbol):
    max_spreads = {
        "EURUSD": 0.3,
        "GBPUSD": 0.5,
        "USDJPY": 0.8,
        "USDCHF": 0.8,
        "USDCAD": 0.8,
        "AUDUSD": 0.5,
        "NZDUSD": 0.6,
        "EURGBP": 0.5,
        "EURJPY": 0.8,
        "EURCHF": 1.0,
        "GBPJPY": 1.2,
        "CHFJPY": 1.2,
        "AUDJPY": 0.8,
        "CADJPY": 1.0,
        "NZDJPY": 1.0,
        "AUDCAD": 0.8,
        "AUDNZD": 0.8,
        "GBPCAD": 1.0,
        "GBPCHF": 1.2,
        "EURNZD": 1.2,
        "EURAUD": 0.8,
        "EURCAD": 0.8,
        "NZDCAD": 0.8,
        "NZDCHF": 0.8,
        "XAUUSD": 30.0
    }
    return max_spreads.get(symbol, 1.0)

# ✅ Real-time spread (raw value)
def get_current_spread(symbol):
    tick = mt5.symbol_info_tick(symbol)
    return abs(tick.ask - tick.bid) if tick else None

# ✅ Final pip-aware spread check
def spread_is_acceptable(symbol):
    tick = mt5.symbol_info_tick(symbol)
    if not tick:
        print(f"[{symbol}] ❌ No tick data for spread check.")
        return False

    pip = get_pip_value(symbol)
    spread_price = abs(tick.ask - tick.bid)
    spread_pips = spread_price / pip

    allowed_pips = get_max_spread_pips(symbol) + 0.2  # Add buffer
    if spread_pips > allowed_pips:
        print(f"[{symbol}] ❌ Spread {spread_pips:.2f} pips > allowed {allowed_pips:.2f} pips")
        return False

    return True

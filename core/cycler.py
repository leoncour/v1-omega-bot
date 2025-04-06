import time
import MetaTrader5 as mt5
from utils.pips import get_pip_value
from utils.trade_cycle import close_and_reopen
from utils.settings import ENABLE_TRADE_CYCLE, CYCLE_PROFIT_TRIGGER

# ⏱️ Track last cycle timestamp per symbol
last_cycle_time = {}

def run_trade_cycle():
    if not ENABLE_TRADE_CYCLE:
        return

    all_positions = mt5.positions_get()
    if not all_positions:
        return

    now = time.time()

    for pos in all_positions:
        symbol = pos.symbol

        # ✅ Cooldown: skip if too recent
        last_time = last_cycle_time.get(symbol, 0)
        if now - last_time < 60:  # 60s cooldown
            print(f"[{symbol}] ⏳ Cooldown active ({int(now - last_time)}s)")
            continue

        tick = mt5.symbol_info_tick(symbol)
        if not tick:
            print(f"[{symbol}] ❌ No tick data")
            continue

        pip = get_pip_value(symbol)
        if not pip:
            print(f"[{symbol}] ❌ No pip value found")
            continue

        spread = abs(tick.ask - tick.bid)
        if spread > pip * 2:
            print(f"[{symbol}] ❌ Spread too high: {spread / pip:.2f} pips")
            continue

        if pos.profit >= CYCLE_PROFIT_TRIGGER:
            print(f"[{symbol}] 🔁 Cycling trade with ${pos.profit:.2f} profit")
            if close_and_reopen(symbol, pos.type, pos.volume, pos.comment):
                last_cycle_time[symbol] = now

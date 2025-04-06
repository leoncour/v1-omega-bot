import time
from utils.settings import ENABLE_PACING_CONTROL, MIN_SECONDS_BETWEEN_TRADES

_last_trade_times = {}

def pacing_control(symbol):
    if not ENABLE_PACING_CONTROL:
        return False

    now = time.time()
    last_time = _last_trade_times.get(symbol)

    if last_time and (now - last_time) < MIN_SECONDS_BETWEEN_TRADES:
        print(f"[{symbol}] ⏱️ Skipped – Pacing control: wait {int(MIN_SECONDS_BETWEEN_TRADES - (now - last_time))}s more.")
        return True

    _last_trade_times[symbol] = now
    return False

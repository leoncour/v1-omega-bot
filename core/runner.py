import time
import datetime
import MetaTrader5 as mt5

from utils.risk import check_drawdown
from utils.core import is_new_candle
from utils.pips import get_pip_value
from utils.settings import ENABLE_TRADE_CYCLE, CYCLE_PROFIT_TRIGGER
from utils.trade_cycle import close_and_reopen
from core.manager import process_symbol
from core.cycler import run_trade_cycle
from core.config import SYMBOLS
from utils.profit_lockout import daily_profit_lockout

# ✅ NEW: Intelligent Hedge System
from strategies.hedge import hedge_cycle


def run_trading():
    print("🚀 Multi-symbol trading bot started.")
    while True:
        # ✅ Step 1: Check Drawdown Guard (auto-reset logic lives in check_drawdown)
        drawdown_status = check_drawdown()
        if drawdown_status == True:
            print("🚨 Drawdown limit hit. Stopping trading.")
            break
        elif drawdown_status == "recovery":
            recovery_mode = True
        else:
            recovery_mode = False

        # ✅ Step 2: Daily Profit Cap Check (rebate protection)
        acc = (mt5.account_info() or type('acc', (), {'balance': 100.0, 'equity': 100.0})())
        if acc and acc.balance >= 2000 and daily_profit_lockout():
            print("🔕 Daily profit cap active. Skipping trading loop.")
            time.sleep(10)
            continue

        # ✅ Step 3: Wait for new candle
        if not is_new_candle():
            time.sleep(5)
            continue

        # ✅ Step 4: Run strategy + hedge per symbol
        for symbol in SYMBOLS:
            process_symbol(symbol, recovery_mode=recovery_mode)
            hedge_cycle(symbol)

        # ✅ Step 5: Trade cycle and sleep
        run_trade_cycle()
        time.sleep(5)

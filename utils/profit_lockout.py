import MetaTrader5 as mt5
import os
from datetime import datetime
from utils.settings import ENABLE_DAILY_PROFIT_CAP, DAILY_PROFIT_TARGET_PCT

LOCK_FILE = "daily_profit.lock"

def get_account_snapshot():
    account = mt5.account_info()
    if account is None:
        return None, None
    return account.balance, account.equity

def daily_profit_lockout():
    if not ENABLE_DAILY_PROFIT_CAP:
        return False

    today = datetime.now().strftime("%Y-%m-%d")

    # ✅ Check for existing lock
    if os.path.exists(LOCK_FILE):
        with open(LOCK_FILE, "r") as f:
            lock_date = f.read().strip()
        if lock_date == today:
            print("🔕 Profit lock already triggered today.")
            return True
        else:
            os.remove(LOCK_FILE)
            print("🔓 New day — profit lock reset.")
            return False

    # ✅ Get account equity vs balance
    balance, equity = get_account_snapshot()
    if balance is None or balance == 0:
        return False

    gain_pct = ((equity - balance) / balance) * 100

    # ✅ Trigger lock
    if gain_pct >= DAILY_PROFIT_TARGET_PCT:
        with open(LOCK_FILE, "w") as f:
            f.write(today)
        print(f"🛑 Daily profit target hit ({gain_pct:.2f}%). Locking for today.")
        return True

    return False

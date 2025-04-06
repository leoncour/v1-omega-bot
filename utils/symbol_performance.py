# ✅ utils/symbol_performance.py

import os
import json
from datetime import datetime

STATS_PATH = "Reports/symbol_stats.json"

# Default container
def load_stats():
    if not os.path.exists(STATS_PATH):
        return {}
    with open(STATS_PATH, "r") as f:
        return json.load(f)

def save_stats(stats):
    os.makedirs(os.path.dirname(STATS_PATH), exist_ok=True)
    with open(STATS_PATH, "w") as f:
        json.dump(stats, f, indent=2)


def update_symbol_stats(symbol, result, profit):
    stats = load_stats()
    today = datetime.now().strftime("%Y-%m-%d")
    if symbol not in stats:
        stats[symbol] = {}
    if today not in stats[symbol]:
        stats[symbol][today] = {"wins": 0, "losses": 0, "pnl": 0.0, "trades": 0}

    day_stat = stats[symbol][today]
    if result == "win":
        day_stat["wins"] += 1
    else:
        day_stat["losses"] += 1

    day_stat["pnl"] += profit
    day_stat["trades"] += 1

    save_stats(stats)


def is_symbol_disabled(symbol):
    stats = load_stats()
    today = datetime.now().strftime("%Y-%m-%d")
    data = stats.get(symbol, {}).get(today, {})
    if not data:
        return False

    trades = data["trades"]
    losses = data["losses"]
    pnl = data["pnl"]
    win_rate = (data["wins"] / trades) * 100 if trades > 0 else 0

    if trades >= 3 and (win_rate < 33 or pnl <= -0.01 * get_dynamic_loss_limit()):
        return True
    return False


def get_lot_multiplier(symbol):
    stats = load_stats()
    today = datetime.now().strftime("%Y-%m-%d")
    data = stats.get(symbol, {}).get(today, {})
    if not data:
        return 1.0

    trades = data["trades"]
    pnl = data["pnl"]
    win_rate = (data["wins"] / trades) * 100 if trades > 0 else 0

    if trades >= 2 and win_rate > 70 and pnl >= 0.01 * get_dynamic_profit_trigger():
        return 1.5

    return 1.0


def get_dynamic_loss_limit():
    from MetaTrader5 import account_info
    acc = account_info()
    return acc.balance if acc else 2000


def get_dynamic_profit_trigger():
    from MetaTrader5 import account_info
    acc = account_info()
    return acc.balance if acc else 2000


def print_symbol_stats():
    stats = load_stats()
    today = datetime.now().strftime("%Y-%m-%d")
    print("\n📊 Symbol Performance Today:")
    for symbol, days in stats.items():
        data = days.get(today)
        if not data:
            continue
        print(f"{symbol} → Trades: {data['trades']}, Wins: {data['wins']}, Losses: {data['losses']}, WinRate: {data['wins'] / data['trades'] * 100:.1f}%, PnL: ${data['pnl']:.2f}")

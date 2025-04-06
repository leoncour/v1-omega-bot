import json
import os
from datetime import datetime
from utils.settings import (
    AUTO_BLOCK_MIN_TRADES,
    AUTO_BLOCK_WINRATE_THRESHOLD,
    AUTO_BLOCK_MAX_LOSS_STREAK,
)

STATS_FILE = "symbol_stats.json"
_stats = {}

def load_stats():
    global _stats
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            _stats = json.load(f)

def save_stats():
    with open(STATS_FILE, "w") as f:
        json.dump(_stats, f, indent=2)

def get_symbol_stats(symbol):
    if symbol not in _stats:
        _stats[symbol] = {
            "wins": 0,
            "losses": 0,
            "net_profit": 0.0,
            "loss_streak": 0,
            "total_trades": 0,
            "status": "active",
            "last_updated": None
        }
    return _stats[symbol]

def update_symbol_stats(symbol, profit):
    stats = get_symbol_stats(symbol)
    stats["total_trades"] += 1
    stats["net_profit"] += profit
    stats["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if profit > 0:
        stats["wins"] += 1
        stats["loss_streak"] = 0
    else:
        stats["losses"] += 1
        stats["loss_streak"] += 1

    # Auto-block check
    if stats["total_trades"] >= AUTO_BLOCK_MIN_TRADES:
        winrate = stats["wins"] / stats["total_trades"]
        if winrate < AUTO_BLOCK_WINRATE_THRESHOLD or stats["loss_streak"] >= AUTO_BLOCK_MAX_LOSS_STREAK:
            stats["status"] = "disabled"
            print(f"🚫 Auto-disabled {symbol} — winrate={winrate:.2f}, loss_streak={stats['loss_streak']}")

    save_stats()

def should_trade_symbol(symbol):
    stats = get_symbol_stats(symbol)
    return stats["status"] == "active"

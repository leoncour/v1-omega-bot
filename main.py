# main.py

from utils.core import initialize_mt5
from core.runner import run_trading
from utils.symbol_stats import load_stats  # ✅ NEW

# ✅ Initialize MT5 + Load Symbol Stats
initialize_mt5()
load_stats()

# ✅ Begin trading loop
run_trading()

# Daily test comment

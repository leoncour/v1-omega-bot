from utils.settings import ENABLE_REBATE_TRACKING, REBATE_PER_LOT
from utils.symbol_stats import update_symbol_stats  # ✅ FIXED
import os

lot_log_path = "rebate_log.txt"

def log_lot_volume(symbol, volume, is_win=None, profit=None):
    """
    Logs trade volume for rebate tracking and optionally updates symbol performance stats.
    """
    if ENABLE_REBATE_TRACKING:
        with open(lot_log_path, "a") as f:
            f.write(f"{symbol},{volume}\n")

    # ✅ Optional symbol performance logging
    if profit is not None:
        update_symbol_stats(symbol, profit)

def get_total_rebate():
    if not ENABLE_REBATE_TRACKING or not os.path.exists(lot_log_path):
        return 0.0
    total_lots = 0.0
    with open(lot_log_path, "r") as f:
        for line in f:
            try:
                _, vol = line.strip().split(",")
                total_lots += float(vol)
            except:
                continue
    return total_lots * REBATE_PER_LOT

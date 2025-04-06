import csv
from datetime import datetime
import os

LOG_FILE = "trade_logs.csv"

def log_trade(symbol, strategy, result, comment=""):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Symbol", "Strategy", "Result", "Comment"])
        writer.writerow([datetime.now(), symbol, strategy, result, comment])

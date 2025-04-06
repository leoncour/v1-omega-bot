def adaptive_rsi_filter(rsi, trend_strength, symbol):
    bands = {
        "XAUUSD": {"normal": (38, 62), "strong": (32, 68)},
        "default": {"normal": (40, 60), "strong": (35, 65)}
    }
    cfg = bands["XAUUSD"] if symbol == "XAUUSD" else bands["default"]
    low, high = cfg.get(trend_strength, (40, 60))
    return low < rsi < high

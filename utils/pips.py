# 📁 utils/pips.py

def get_pip_value(symbol):
    symbol = symbol.upper()
    if "JPY" in symbol:
        return 0.01
    elif "XAU" in symbol or "XAG" in symbol:
        return 0.1
    elif "US30" in symbol or "NAS" in symbol:
        return 1.0
    else:
        return 0.0001

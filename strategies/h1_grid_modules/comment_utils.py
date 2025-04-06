# comment_utils.py

def generate_comment(strategy, symbol, direction, tag="L1"):
    """
    Create a consistent comment tag for any strategy.

    Example Output:
    - GRD_EURUSD_BUY_L1
    - BRK_GBPUSD_SELL_v2.3
    - VWAP_USDJPY_BUY_v2.6
    """
    dir_text = "BUY" if direction == 0 else "SELL"
    return f"{strategy}_{symbol}_{dir_text}_{tag}"

def is_strategy_position(position, strategy):
    """
    Check if a position belongs to a specific strategy.

    Example:
    - strategy = "GRD"
    - position.comment = "GRD_EURUSD_BUY_L1" → ✅ True
    """
    return position.comment.startswith(strategy)

def parse_comment(comment):
    """
    Parse a comment like 'GRD_EURUSD_BUY_L1' into components.

    Returns a dict:
    {
        "strategy": "GRD",
        "symbol": "EURUSD",
        "direction": "BUY",
        "tag": "L1"
    }

    Returns None if format is invalid.
    """
    if not comment or "_" not in comment:
        return None

    parts = comment.split("_")
    if len(parts) < 4:
        return None

    return {
        "strategy": parts[0],
        "symbol": parts[1],
        "direction": parts[2],
        "tag": "_".join(parts[3:])  # allow tag to include versions like v2.6
    }

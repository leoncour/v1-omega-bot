from datetime import datetime, timedelta, timezone
import MetaTrader5 as mt5
import pandas as pd
import os

# ✅ Save directory inside AI EA folder
SAVE_DIR = os.path.join(os.path.dirname(__file__), "Reports")
os.makedirs(SAVE_DIR, exist_ok=True)

# ✅ Initialize MT5
def initialize_mt5():
    if not mt5.initialize():
        print("❌ Failed to initialize MT5. Ensure MT5 is running.")
        exit()
    print("✅ Connected to MT5")

initialize_mt5()

# ✅ Convert MT5 type int to "Buy"/"Sell"
def get_order_type_str(order_type):
    return "Buy" if order_type == 0 else "Sell" if order_type == 1 else "Other"

# ✅ Get Trade History and Save
def get_trade_history(from_date, to_date):
    history = mt5.history_deals_get(from_date, to_date)
    if history is None or len(history) == 0:
        print("❌ No trade history found.")
        return None

    data = []
    for deal in history:
        order_info = mt5.history_orders_get(ticket=deal.order)
        sl, tp = None, None
        if order_info and len(order_info) > 0:
            sl = order_info[0].sl
            tp = order_info[0].tp

        direction = get_order_type_str(deal.type)
        entry_price = deal.price
        pnl = deal.profit

        data.append([
            deal.ticket, deal.order, datetime.fromtimestamp(deal.time, timezone.utc),
            direction, deal.volume, entry_price, sl, tp, pnl, deal.comment
        ])

    df = pd.DataFrame(data, columns=[
        "ticket", "order", "Time", "type", "volume", "price", "sl", "tp", "profit", "strategy"
    ])

    # ✅ Format Time
    df["Time"] = df["Time"].dt.strftime("%Y-%m-%d %H:%M:%S")

    # ✅ Add PnL in pips (approx, for EURUSD)
    df["pnl_pips"] = df.apply(
        lambda row: abs(row["tp"] - row["price"]) * 10000 if pd.notna(row["tp"]) else 0, axis=1
    )

    path = os.path.join(SAVE_DIR, "trade_history.csv")
    df.to_csv(path, index=False)
    print(f"✅ Trade history saved: {path}")
    return df

# ✅ Get Market Data (M1 & M15)
def get_market_data(symbol, timeframe, filename):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 10000)
    if rates is None or len(rates) == 0:
        print(f"❌ No market data for {symbol} ({filename})")
        return None

    df = pd.DataFrame(rates)
    df["Time"] = pd.to_datetime(df["time"], unit="s", utc=True)
    df["Time"] = df["Time"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df.drop(columns=["time"], inplace=True)

    path = os.path.join(SAVE_DIR, filename)
    df.to_csv(path, index=False)
    print(f"✅ Market data saved: {path}")
    return df

# ✅ Run full export (Last 3 days or customize)
to_date = datetime.now(timezone.utc)
from_date = to_date - timedelta(days=3)

df_history = get_trade_history(from_date, to_date)
df_m1 = get_market_data("EURUSD", mt5.TIMEFRAME_M1, "market_data_M1.csv")
df_m15 = get_market_data("EURUSD", mt5.TIMEFRAME_M15, "market_data_M15.csv")

mt5.shutdown()
print("✅ MT5 Connection Closed")

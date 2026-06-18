import pandas as pd
from sqlalchemy import create_engine
from ta.momentum import RSIIndicator

DB_URL = "postgresql://stockadmin:StrongPassword123!@localhost:5432/stock_ai"

engine = create_engine(DB_URL)

query = """
SELECT trade_date, close_price
FROM daily_prices
WHERE symbol='RELIANCE'
ORDER BY trade_date
"""

df = pd.read_sql(query, engine)

df["RSI"] = RSIIndicator(df["close_price"], window=14).rsi()

df["SMA20"] = df["close_price"].rolling(20).mean()
df["SMA50"] = df["close_price"].rolling(50).mean()

latest = df.iloc[-1]

print("\n===== RELIANCE ANALYSIS =====")
print(f"Close Price : {latest['close_price']:.2f}")
print(f"RSI         : {latest['RSI']:.2f}")
print(f"SMA20       : {latest['SMA20']:.2f}")
print(f"SMA50       : {latest['SMA50']:.2f}")

signal = "HOLD"

if latest["RSI"] < 30:
    signal = "BUY"

elif latest["RSI"] > 70:
    signal = "SELL"

if latest["SMA20"] > latest["SMA50"]:
    trend = "UPTREND"
else:
    trend = "DOWNTREND"

print(f"Trend       : {trend}")
print(f"Signal      : {signal}")

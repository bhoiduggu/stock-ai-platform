from fastapi import FastAPI
from sqlalchemy import create_engine
import pandas as pd
import ta

app = FastAPI(title="Stock AI")

DATABASE_URL = "postgresql://stockadmin:StrongPassword123!@localhost/stock_ai"

engine = create_engine(DATABASE_URL)

@app.get("/")
def root():
    return {"message": "Stock AI Backend Running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/analyze/{symbol}")
def analyze(symbol: str):

    query = f"""
    SELECT trade_date, close_price
    FROM daily_prices
    WHERE symbol = '{symbol.upper()}'
    ORDER BY trade_date
    """

    df = pd.read_sql(query, engine)

    if len(df) < 50:
        return {"error": "Not enough data"}

    df["RSI"] = ta.momentum.RSIIndicator(
        close=df["close_price"],
        window=14
    ).rsi()

    df["SMA20"] = df["close_price"].rolling(20).mean()
    df["SMA50"] = df["close_price"].rolling(50).mean()

    latest = df.iloc[-1]

    trend = "UPTREND" if latest["SMA20"] > latest["SMA50"] else "DOWNTREND"

    signal = "HOLD"

    if latest["RSI"] > 70:
        signal = "SELL"
    elif latest["RSI"] < 30:
        signal = "BUY"

    return {
        "symbol": symbol.upper(),
        "close_price": round(float(latest["close_price"]), 2),
        "rsi": round(float(latest["RSI"]), 2),
        "sma20": round(float(latest["SMA20"]), 2),
        "sma50": round(float(latest["SMA50"]), 2),
        "trend": trend,
        "signal": signal
    }

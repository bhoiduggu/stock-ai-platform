import yfinance as yf
from sqlalchemy import create_engine

DB_URL = "postgresql://stockadmin:StrongPassword123!@localhost:5432/stock_ai"

engine = create_engine(DB_URL)

stock = yf.Ticker("RELIANCE.NS")
data = stock.history(period="6mo")

data = data.reset_index()

for _, row in data.iterrows():

    sql = f"""
    INSERT INTO daily_prices
    (
        symbol,
        trade_date,
        open_price,
        high_price,
        low_price,
        close_price,
        volume
    )
    VALUES
    (
        'RELIANCE',
        '{row["Date"].date()}',
        {row["Open"]},
        {row["High"]},
        {row["Low"]},
        {row["Close"]},
        {int(row["Volume"])}
    );
    """

    with engine.begin() as conn:
        conn.exec_driver_sql(sql)

print("RELIANCE data saved successfully")

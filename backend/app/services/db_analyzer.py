from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(
    "postgresql://stockadmin:StrongPassword123!@localhost/stock_ai"
)

query = """
SELECT trade_date, close_price
FROM daily_prices
WHERE symbol = 'RELIANCE'
ORDER BY trade_date
"""

df = pd.read_sql(query, engine)

print(df.tail())

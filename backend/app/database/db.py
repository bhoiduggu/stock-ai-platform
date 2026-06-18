from sqlalchemy import create_engine

DATABASE_URL = "postgresql://stockadmin:StrongPassword123!@localhost/stock_ai"

engine = create_engine(DATABASE_URL)

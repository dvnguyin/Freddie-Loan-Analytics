import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

with engine.connect() as conn:
    rows = conn.execute(text("SELECT * FROM v_loans_by_credit_band;")).fetchall()
    print("Returned rows:", len(rows))
    print("First row:", rows[0] if rows else None)

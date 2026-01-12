from pathlib import Path
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

sql = Path("sql/00_schema.sql").read_text(encoding="utf-8")

with engine.begin() as conn:
    conn.execute(text(sql))

print("Created table: loan_origination")

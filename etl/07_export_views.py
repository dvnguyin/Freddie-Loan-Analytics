import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

OUT_DIR = "data_processed"
os.makedirs(OUT_DIR, exist_ok=True)

views = {
    "v_loans_by_credit_band": "loans_by_credit_band.csv",
    "v_loans_by_cltv_band": "loans_by_cltv_band.csv",
    "v_loans_by_state": "loans_by_state.csv"
}

for view, filename in views.items():
    df = pd.read_sql(f"SELECT * FROM {view};", engine)
    out_path = os.path.join(OUT_DIR, filename)
    df.to_csv(out_path, index=False)
    print(f"Wrote {out_path}")

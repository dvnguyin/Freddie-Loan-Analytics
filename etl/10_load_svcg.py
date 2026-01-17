from pathlib import Path
import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

CSV_PATH = Path("data_processed") / "svcgs_clean.csv"

# Target table columns (
TARGET_COLS = [
    "loan_seq_num",
    "monthly_reporting_period",
    "current_actual_upb",
    "delinquency_status",
    "interest_rate",
]

ALIASES = {
    "loan_seq_num": ["loan_seq_num", "loan_id"],
    "monthly_reporting_period": ["monthly_reporting_period"],
    "current_actual_upb": ["current_actual_upb", "current_upb"],
    "delinquency_status": ["delinquency_status", "loan_status"],
    "interest_rate": ["interest_rate"],
}

def pick_and_rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {}

    for target, options in ALIASES.items():
        found = next((c for c in options if c in df.columns), None)
        if not found:
            raise ValueError(
                f"Missing required column for '{target}'. Tried: {options}. Found columns: {list(df.columns)}"
            )
        rename_map[found] = target

    df2 = df[list(rename_map.keys())].rename(columns=rename_map)

    return df2[TARGET_COLS]

def main():
    db_url = os.environ["DATABASE_URL"]  # e.g. postgresql://freddie:freddie_pw@localhost:5432/freddie_analytics

    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Missing file: {CSV_PATH}. Run 08_extract_svcg.py first.")

    df = pd.read_csv(CSV_PATH)

    df = pick_and_rename_columns(df)

    # Convert YYYYMM (e.g., 202202) to a real date (2022-02-01)
    df["monthly_reporting_period"] = (
        df["monthly_reporting_period"]
        .astype(str)
        .str.strip()
        .replace({"nan": None})
    )

    df["monthly_reporting_period"] = pd.to_datetime(
        df["monthly_reporting_period"].where(df["monthly_reporting_period"].notna(), None) + "01",
        format="%Y%m%d",
        errors="raise",
    ).dt.date

    # Convert NaNs to None so Postgres accepts them
    df = df.where(pd.notnull(df), None)

    rows = list(df.itertuples(index=False, name=None))

    sql = """
    INSERT INTO loan_performance_monthly (
        loan_seq_num,
        monthly_reporting_period,
        current_actual_upb,
        delinquency_status,
        interest_rate
    )
    VALUES %s;
    """

    with psycopg2.connect(db_url) as conn:
        with conn.cursor() as cur:
            execute_values(cur, sql, rows, page_size=5000)
        conn.commit()

    print(f"✅ Loaded {len(rows)} rows into loan_performance_monthly")

if __name__ == "__main__":
    main()

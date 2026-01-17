from pathlib import Path
import os
import psycopg2

SQL_PATH = Path("sql/02_schema_svcg.sql")

def main():
    db_url = os.environ["DATABASE_URL"]
    sql = SQL_PATH.read_text(encoding="utf-8")

    with psycopg2.connect(db_url) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()

    print("✅ Created loan_performance_monthly table")

if __name__ == "__main__":
    main()

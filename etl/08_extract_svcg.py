from pathlib import Path
import pandas as pd

RAW_PATH = Path("data_raw") / "sample_svcg_2022.txt"
OUT_PATH = Path("data_processed")
OUT_PATH.mkdir(exist_ok=True)

def main():
    # Freddie Mac monthly performance files are pipe-delimited and have no header
    df = pd.read_csv(
        RAW_PATH,
        sep="|",
        header=None,
        engine="python"
    )

    print("Loaded rows:", len(df))
    print("Total columns detected:", df.shape[1])

    # Select key columns by position (Freddie Mac spec)
    # NOTE: 0-based indexing
    df_clean = pd.DataFrame({
        "loan_id": df[0],
        "monthly_reporting_period": df[1],
        "current_upb": df[2],
        "loan_status": df[4],
        "loan_age": df[5],
        "remaining_months": df[6],
        "interest_rate": df[10]
    })

    out_file = OUT_PATH / "svcgs_clean.csv"
    df_clean.to_csv(out_file, index=False)

    print(f"✅ Wrote cleaned SVCG file to {out_file}")

if __name__ == "__main__":
    main()

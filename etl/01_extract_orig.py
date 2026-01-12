from pathlib import Path
import pandas as pd

RAW_PATH = Path("data_raw") / "sample_orig_2022.txt"
OUT_PATH = Path("data_processed")
OUT_PATH.mkdir(exist_ok=True)

def main():
    # Freddie Mac orig file is pipe-delimited and has NO header row
    df = pd.read_csv(
        RAW_PATH,
        sep="|",
        header=None,
        dtype=str,          # keep as string first (safer)
        engine="python"
    )

    print("Loaded rows:", len(df))
    print("Detected columns:", df.shape[1])
    print("First row (raw):")
    print(df.iloc[0].tolist())

    # ---- Select ONLY the columns we need (by position) ----
    # These positions match the standard Freddie Mac orig layout
    # NOTE: 0-based indexing
    col_map = {
        19: "loan_id",                 # Loan sequence number / ID
        1:  "first_pay_ym",            # YYYYMM
        0:  "credit_score",            # Borrower credit score
        10: "orig_upb",                # Original unpaid principal balance
        12: "orig_interest_rate",      # Original interest rate
        21: "orig_loan_term",          # Original loan term (months)
        13: "channel",                 # Origination channel
        16: "state",                   # Property state
        17: "property_type",           # Property type
        8:  "orig_cltv",               # Original combined LTV
        9:  "orig_dti",                # Original DTI
        20: "loan_purpose",            # Loan purpose (Purchase/Refi/etc)
    }

    # Safety check: make sure file has enough columns
    max_idx = max(col_map.keys())
    if df.shape[1] <= max_idx:
        raise ValueError(
            f"File only has {df.shape[1]} columns, but we expected at least {max_idx + 1}. "
            "We need to adjust the column mapping."
        )

    out = df[list(col_map.keys())].rename(columns=col_map)

    # ---- Clean / type conversions ----
    # Convert YYYYMM -> date (first day of month)
    out["first_pay_date"] = pd.to_datetime(out["first_pay_ym"], format="%Y%m", errors="coerce")

    # Convert numeric fields
    for c in ["credit_score", "orig_upb", "orig_interest_rate", "orig_loan_term", "orig_cltv", "orig_dti"]:
        out[c] = pd.to_numeric(out[c], errors="coerce")

    # Drop the raw YYYYMM column (optional)
    out = out.drop(columns=["first_pay_ym"])

    # Remove rows missing primary key
    out = out.dropna(subset=["loan_id"])

    print("\nPreview cleaned:")
    print(out.head(3))

    # Save processed file (fast + stable)
    out_file = OUT_PATH / "origination_clean.parquet"
    out.to_parquet(out_file, index=False)
    print(f"\nWrote: {out_file}")

if __name__ == "__main__":
    main()

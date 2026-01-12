# Freddie Mac Loan Performance Dataset – Notes

## Overview
This project uses the publicly available Freddie Mac Single-Family Loan-Level Dataset.
The dataset contains anonymized mortgage loan data used to analyze loan performance,
delinquency trends, and borrower risk characteristics.

This project initially uses the **sample dataset** provided by Freddie Mac for development
and testing purposes.

---

## Files Used

### 1. Origination File
**Description:**  
Contains one row per loan at the time of origination.

**Granularity:**  
- One record per mortgage loan

**Common Fields (may vary by dataset):**
- `loan_id` – Unique loan identifier
- `orig_date` – Loan origination date
- `first_pay_date` – First scheduled payment date
- `orig_upb` – Original unpaid principal balance
- `orig_int_rate` – Original interest rate
- `borrower_credit_score` – Borrower credit score at origination
- `orig_ltv` – Original loan-to-value ratio
- `orig_dti` – Original debt-to-income ratio
- `state` – Property state
- `property_type` – Property type (e.g., SF, Condo)
- `loan_purpose` – Purchase, refinance, etc.
- `channel` – Origination channel

---

### 2. Monthly Performance File
**Description:**  
Contains loan performance information recorded monthly for each loan.

**Granularity:**  
- Multiple records per loan
- One row per loan per month

**Common Fields (may vary by dataset):**
- `loan_id` – Unique loan identifier
- `as_of_date` – Reporting month
- `current_upb` – Current unpaid principal balance
- `delinquency_status` – Loan delinquency status
- `loan_age` – Loan age in months
- `remaining_months` – Remaining term
- `mod_flag` – Loan modification indicator
- `zero_balance_code` – Reason loan left the portfolio
- `zero_balance_effective_date` – Date loan was paid off or terminated

---

## Key Concepts

### Delinquency Status
Delinquency status represents how many days past due a loan is.
Common interpretations:
- `0` or `00` – Current
- `1` or `30` – 30 days delinquent
- `2` or `60` – 60 days delinquent
- `3+` or `90+` – Seriously delinquent

These values are normalized during the ETL process.

---

## Notes for This Project
- Raw data files are stored locally in `data_raw/` and are not committed to version control.
- Cleaned and transformed data is written to `data_processed/`.
- Database schema and analytics queries are designed to support Tableau dashboards.
- Column names may differ slightly depending on dataset vintage or sample version.

---

## References
- Freddie Mac Single-Family Loan-Level Dataset documentation

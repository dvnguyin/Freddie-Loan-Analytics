-- Loan counts by state (origination)
CREATE OR REPLACE VIEW v_loans_by_state AS
SELECT
  state,
  COUNT(*) AS loan_count
FROM loan_origination
GROUP BY state;

-- Loan counts by credit score band
CREATE OR REPLACE VIEW v_loans_by_credit_band AS
SELECT
  CASE
    WHEN credit_score >= 740 THEN '740+'
    WHEN credit_score BETWEEN 680 AND 739 THEN '680-739'
    WHEN credit_score BETWEEN 620 AND 679 THEN '620-679'
    ELSE '<620'
  END AS credit_score_band,
  COUNT(*) AS loan_count
FROM loan_origination
GROUP BY 1;

-- Loan counts by CLTV band
CREATE OR REPLACE VIEW v_loans_by_cltv_band AS
SELECT
  CASE
    WHEN orig_cltv < 80 THEN '<80'
    WHEN orig_cltv BETWEEN 80 AND 89.999 THEN '80-89'
    WHEN orig_cltv BETWEEN 90 AND 94.999 THEN '90-94'
    ELSE '95+'
  END AS cltv_band,
  COUNT(*) AS loan_count
FROM loan_origination
GROUP BY 1;


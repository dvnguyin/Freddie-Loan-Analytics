-- 1) Basic count of loans by state
CREATE OR REPLACE VIEW v_loans_by_state AS
SELECT
  state,
  COUNT(*) AS loan_count,
  AVG(credit_score) AS avg_credit_score,
  AVG(orig_interest_rate) AS avg_interest_rate,
  AVG(orig_upb) AS avg_orig_upb
FROM loan_origination
GROUP BY state
ORDER BY loan_count DESC;

-- 2) Credit score bands (good for Tableau bar charts)
CREATE OR REPLACE VIEW v_loans_by_credit_band AS
WITH binned AS (
  SELECT
    CASE
      WHEN credit_score IS NULL THEN 'Unknown'
      WHEN credit_score < 620 THEN '<620'
      WHEN credit_score < 680 THEN '620-679'
      WHEN credit_score < 740 THEN '680-739'
      ELSE '740+'
    END AS credit_band,
    orig_upb,
    orig_interest_rate
  FROM loan_origination
)
SELECT
  credit_band,
  COUNT(*) AS loan_count,
  AVG(orig_interest_rate) AS avg_interest_rate,
  AVG(orig_upb) AS avg_orig_upb
FROM binned
GROUP BY credit_band
ORDER BY
  CASE credit_band
    WHEN '<620' THEN 1
    WHEN '620-679' THEN 2
    WHEN '680-739' THEN 3
    WHEN '740+' THEN 4
    ELSE 99
  END;

-- 3) LTV / CLTV bands (risk segmentation)
CREATE OR REPLACE VIEW v_loans_by_cltv_band AS
WITH binned AS (
  SELECT
    CASE
      WHEN orig_cltv IS NULL THEN 'Unknown'
      WHEN orig_cltv < 80 THEN '<80'
      WHEN orig_cltv < 90 THEN '80-89'
      WHEN orig_cltv < 95 THEN '90-94'
      ELSE '95+'
    END AS cltv_band,
    credit_score,
    orig_interest_rate,
    orig_upb
  FROM loan_origination
)
SELECT
  cltv_band,
  COUNT(*) AS loan_count,
  AVG(credit_score) AS avg_credit_score,
  AVG(orig_interest_rate) AS avg_interest_rate,
  AVG(orig_upb) AS avg_orig_upb
FROM binned
GROUP BY cltv_band
ORDER BY
  CASE cltv_band
    WHEN '<80' THEN 1
    WHEN '80-89' THEN 2
    WHEN '90-94' THEN 3
    WHEN '95+' THEN 4
    ELSE 99
  END;

-- 4) Loan purpose mix
CREATE OR REPLACE VIEW v_loans_by_purpose AS
SELECT
  loan_purpose,
  COUNT(*) AS loan_count,
  AVG(credit_score) AS avg_credit_score,
  AVG(orig_interest_rate) AS avg_interest_rate,
  AVG(orig_upb) AS avg_orig_upb
FROM loan_origination
GROUP BY loan_purpose
ORDER BY loan_count DESC;

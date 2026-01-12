DROP TABLE IF EXISTS loan_origination;

CREATE TABLE loan_origination (
  loan_id TEXT PRIMARY KEY,
  credit_score INT,
  orig_upb NUMERIC,
  orig_interest_rate NUMERIC,
  orig_loan_term INT,
  channel TEXT,
  state TEXT,
  property_type TEXT,
  orig_cltv NUMERIC,
  orig_dti NUMERIC,
  loan_purpose TEXT,
  first_pay_date DATE
);

CREATE INDEX idx_loan_orig_state ON loan_origination(state);
CREATE INDEX idx_loan_orig_credit_score ON loan_origination(credit_score);

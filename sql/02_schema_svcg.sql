DROP TABLE IF EXISTS loan_performance_monthly;

CREATE TABLE loan_performance_monthly (
  loan_seq_num TEXT NOT NULL,
  monthly_reporting_period DATE NOT NULL,
  current_actual_upb NUMERIC(14,2),
  delinquency_status TEXT,
  interest_rate NUMERIC(6,3),

  PRIMARY KEY (loan_seq_num, monthly_reporting_period)
);

CREATE INDEX IF NOT EXISTS idx_perf_loan_seq_num
  ON loan_performance_monthly (loan_seq_num);

CREATE INDEX IF NOT EXISTS idx_perf_month
  ON loan_performance_monthly (monthly_reporting_period);

CREATE TABLE IF NOT EXISTS policies (
    policy_id TEXT PRIMARY KEY,
    age INTEGER,
    gender TEXT,
    annual_premium REAL,
    fund_value REAL,
    policy_duration INTEGER,
    product_type TEXT,
    start_year INTEGER
);

CREATE TABLE IF NOT EXISTS assumptions (
    assumption_name TEXT PRIMARY KEY,
    value REAL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS scenarios (
    scenario_name TEXT PRIMARY KEY,
    lapse_rate_multiplier REAL,
    investment_return_shift REAL,
    expense_multiplier REAL,
    fee_rate_shift REAL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS cashflow_results (
    scenario_name TEXT,
    projection_year INTEGER,
    active_policies REAL,
    premium_income REAL,
    fund_value REAL,
    fee_income REAL,
    expenses REAL,
    acquisition_costs REAL,
    annual_profit REAL,
    discounted_profit REAL
);

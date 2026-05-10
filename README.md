# RAFM-inspired Insurance Cash-Flow & Profitability Model

This project is a simplified actuarial cash-flow and profitability model for a savings-insurance portfolio.

The goal is to mimic, at a high level, the type of assumption-driven valuation workflow used in actuarial modelling tools such as **RiskAgility Financial Modeller (RAFM)**. The project does **not** use RAFM directly. Instead, it implements a small Python-based modelling workflow that focuses on:

- policy-level portfolio data
- financial input calibration
- mortality assumptions
- interest-rate and investment-return assumptions
- cash-flow projection
- profitability valuation
- scenario analysis
- visual reporting

The project is designed as a learning and portfolio project for actuarial/quantitative insurance modelling roles.

---

## Why this project exists

Insurance cash-flow modelling is usually based on three important components:

1. **Policy portfolio data**  
   Information about customers/contracts, such as age, gender, premium, fund value, product type, and policy duration.

2. **Model assumptions**  
   Assumptions about lapse rates, mortality, expenses, discount rates, investment returns, and fees.

3. **Projection and valuation logic**  
   A model that projects future premiums, fees, expenses, fund values, active policies, and profits over time.

In real insurance companies, these workflows are often implemented in specialist actuarial modelling platforms such as RAFM, Prophet, MoSes, or similar tools. This repository recreates a simplified version of that workflow using Python, pandas, SQL templates, and matplotlib.

---

## Important data note

This project does **not** use real customer policy data.

Real individual life-insurance policy data is usually private and not publicly available. Therefore, this project uses a **hybrid approach**:

1. A synthetic policy-level portfolio in `data/policies_sample.csv`
2. Processed public-data templates in `data/processed/`
3. Documentation for real external sources in `data/raw/external_sources.md`

The synthetic portfolio is scaled/calibrated using aggregate financial inputs, such as premium income and assets under management. This gives the model a more realistic scale while avoiding the use of private customer data.

A strong and honest way to describe the project is:

> Due to privacy constraints, real policy-level life-insurance data is not publicly available. This project therefore combines public financial-reporting style inputs and public actuarial/market assumption templates with a synthetic policy-level portfolio calibrated to realistic aggregate values.

---

## Data sources and where the data comes from

### 1. Synthetic policy-level portfolio

File:

```text
data/policies_sample.csv
```

This file contains synthetic policy-level records. Each row represents one insurance/savings policy.

Columns:

```text
policy_id
age
gender
annual_premium
fund_value
policy_duration
product_type
start_year
```

Example:

```csv
policy_id,age,gender,annual_premium,fund_value,policy_duration,product_type,start_year
P0001,34,F,18000,95000,2,unit_linked_savings,2024
```

This is not real customer data. It is used to demonstrate portfolio-level cash-flow modelling.

---

### 2. Financial input data

File:

```text
data/processed/financial_inputs.csv
```

This file is a processed template for annual-report style financial inputs.

It currently contains placeholder values that should later be replaced with values extracted from public annual reports, for example Swedbank Försäkring annual reports.

Example metrics:

```text
premium_income
operating_expenses
assets_under_management
insurance_liabilities
profit_before_tax
```

How the code uses this file:

- `premium_income` is used to scale the synthetic portfolio's total annual premiums.
- `assets_under_management` is used to scale the synthetic portfolio's total fund value.
- `operating_expenses` is used to estimate expense per policy.

This makes the synthetic portfolio more realistic in aggregate size.

Potential real source:

```text
Swedbank Försäkring annual reports / årsredovisningar
```

Suggested search terms:

```text
Swedbank Försäkring årsredovisning PDF
Swedbank Försäkring annual report
Swedbank Insurance annual report
```

---

### 3. Mortality assumptions

File:

```text
data/processed/mortality_table_sweden.csv
```

This file contains an age/gender mortality assumption table.

Columns:

```text
age
gender
qx
source_year
source
notes
```

`qx` means the annual probability of death for a person of a given age and gender.

The current values are illustrative placeholders. They should later be replaced with real mortality data from public sources.

Potential real sources:

```text
Statistics Sweden / SCB mortality tables
Human Mortality Database
```

How the code uses this file:

- For each policy, the code finds the closest age/gender match in the mortality table.
- It then estimates a portfolio-level average mortality rate.
- That mortality rate is used in the projection model to reduce the number of active policies over time.

---

### 4. Interest-rate and investment-return assumptions

File:

```text
data/processed/interest_rate_assumptions.csv
```

This file contains scenario-level assumptions for discount rates and investment returns.

Columns:

```text
scenario_name
discount_rate
investment_return
source_year
source
notes
```

Current scenarios include:

```text
base_case
low_interest_rate
high_interest_rate
stress_return
```

The current values are illustrative placeholders. They should later be replaced with real market or central-bank data.

Potential real sources:

```text
Sveriges Riksbank policy-rate data
Swedish government bond yields
Swedish yield-curve data
```

How the code uses this file:

- If a scenario name in this file matches a scenario in `data/scenarios.csv`, the model updates the discount rate and investment return from this file.
- For example, `base_case` uses the `base_case` rate assumptions from `interest_rate_assumptions.csv`.

---

### 5. Base assumptions

File:

```text
data/assumptions_base.csv
```

This file contains general modelling assumptions.

Examples:

```text
projection_years
discount_rate
investment_return
annual_fee_rate
expense_per_policy
acquisition_cost_rate
base_lapse_rate
mortality_rate
expense_inflation
```

Some of these assumptions can be overwritten by the processed data files. For example:

- mortality can be estimated from `mortality_table_sweden.csv`
- discount rate and investment return can be read from `interest_rate_assumptions.csv`
- expense per policy can be estimated from `financial_inputs.csv`

---

### 6. Scenario assumptions

File:

```text
data/scenarios.csv
```

This file defines stress and sensitivity scenarios.

Current scenarios:

```text
base_case
high_lapse
low_investment_return
high_expenses
combined_stress
```

Scenario fields:

```text
lapse_rate_multiplier
investment_return_shift
expense_multiplier
fee_rate_shift
```

For example:

- `high_lapse` increases the lapse rate.
- `low_investment_return` reduces the investment return.
- `high_expenses` increases expenses.
- `combined_stress` applies several negative changes at the same time.

---

## Project structure

```text
cash-flow/
├── README.md
├── requirements.txt
├── data/
│   ├── assumptions_base.csv
│   ├── policies_sample.csv
│   ├── scenarios.csv
│   ├── raw/
│   │   ├── README.md
│   │   └── external_sources.md
│   └── processed/
│       ├── financial_inputs.csv
│       ├── interest_rate_assumptions.csv
│       └── mortality_table_sweden.csv
├── notebooks/
│   └── model_walkthrough.ipynb
├── outputs/
│   └── .gitkeep
├── sql/
│   ├── create_tables.sql
│   └── example_queries.sql
├── src/
│   ├── __init__.py
│   ├── assumptions.py
│   ├── cashflow_engine.py
│   ├── load_data.py
│   ├── reporting.py
│   ├── scenarios.py
│   └── valuation.py
└── tests/
    └── .gitkeep
```

---

## How the code works

The main entry point is:

```text
src/cashflow_engine.py
```

Run it with:

```bash
python -m src.cashflow_engine
```

The model follows this workflow:

---

### Step 1: Load input data

The code loads data using functions in:

```text
src/load_data.py
```

It loads:

```text
data/policies_sample.csv
data/assumptions_base.csv
data/scenarios.csv
data/processed/financial_inputs.csv
data/processed/mortality_table_sweden.csv
data/processed/interest_rate_assumptions.csv
```

---

### Step 2: Convert assumptions into dictionaries

The code uses helper functions in:

```text
src/assumptions.py
```

For example:

```python
assumptions_to_dict()
financial_inputs_to_dict()
```

These convert CSV tables into Python dictionaries so the projection engine can easily access values such as:

```text
discount_rate
investment_return
premium_income
operating_expenses
assets_under_management
```

---

### Step 3: Calibrate the synthetic policy portfolio

Function:

```python
calibrate_policy_portfolio()
```

Location:

```text
src/cashflow_engine.py
```

The synthetic portfolio is scaled to match aggregate financial inputs.

The logic is:

```text
premium_scale = target_premium_income / current_total_annual_premium
fund_scale = target_assets_under_management / current_total_fund_value
```

Then:

```text
annual_premium = annual_premium * premium_scale
fund_value = fund_value * fund_scale
```

This means the portfolio remains synthetic at individual policy level, but its total premium and fund value are calibrated to realistic aggregate values.

---

### Step 4: Estimate mortality from the mortality table

Function:

```python
estimate_portfolio_mortality_rate()
```

Location:

```text
src/cashflow_engine.py
```

For each policy, the model:

1. Looks at the policyholder's age and gender.
2. Finds the closest matching row in `mortality_table_sweden.csv`.
3. Reads the mortality probability `qx`.
4. Calculates the average mortality rate for the whole portfolio.

This produces a portfolio-level mortality assumption used in the projection.

---

### Step 5: Update assumptions from processed data

Function:

```python
update_assumptions_from_processed_data()
```

Location:

```text
src/cashflow_engine.py
```

This function updates the base assumptions using the processed data files.

It updates:

```text
mortality_rate
expense_per_policy
discount_rate
investment_return
```

Specifically:

- mortality rate comes from the mortality table
- expense per policy comes from operating expenses divided by number of policies
- discount rate and investment return come from the interest-rate assumption file when scenario names match

---

### Step 6: Apply scenario shocks

Function:

```python
apply_scenario()
```

Location:

```text
src/assumptions.py
```

After the data-driven assumptions are created, each scenario applies additional shocks:

```text
base_lapse_rate = base_lapse_rate * lapse_rate_multiplier
investment_return = investment_return + investment_return_shift
expense_per_policy = expense_per_policy * expense_multiplier
annual_fee_rate = annual_fee_rate + fee_rate_shift
```

This allows the model to compare base-case and stressed profitability.

---

### Step 7: Project cash flows

Function:

```python
project_cashflows()
```

Location:

```text
src/cashflow_engine.py
```

For each projection year, the model estimates:

```text
active policies
premium income
fund value
fee income
expenses
acquisition costs
annual profit
discounted profit
```

Simplified projection logic:

```text
survival_factor = 1 - lapse_rate - mortality_rate
active_policies_t = active_policies_t-1 * survival_factor
premium_income_t = total_annual_premium * active_policy_ratio
fund_value_t = (fund_value_t-1 + premium_income_t) * (1 + investment_return)
fee_income_t = fund_value_t * annual_fee_rate
expenses_t = active_policies_t * expense_per_policy * inflation_factor
annual_profit_t = fee_income_t - expenses_t - acquisition_costs_t
discounted_profit_t = annual_profit_t / (1 + discount_rate)^t
```

This is intentionally simplified. It is not a production actuarial model, but it captures the main structure of assumption-driven cash-flow projection.

---

### Step 8: Calculate valuation metrics

Functions are in:

```text
src/valuation.py
```

The model calculates:

```text
present value of future profits
profit margin
total fee income
total expenses
break-even year
```

The present value of future profits is calculated by summing discounted annual profits:

```text
PV future profit = sum(discounted_profit_t)
```

Profit margin is calculated as:

```text
profit_margin = total_annual_profit / total_premium_income
```

Break-even year is the first year where cumulative discounted profit becomes positive.

---

### Step 9: Generate visual reports

Functions are in:

```text
src/reporting.py
```

The model automatically generates:

```text
outputs/dashboard_base_case.png
outputs/annual_profit_base_case.png
outputs/fund_value_base_case.png
outputs/active_policies_base_case.png
outputs/scenario_comparison_pv_profit.png
outputs/scenario_comparison_profit_margin.png
outputs/short_report.md
```

The most useful visual for a portfolio or job application is:

```text
outputs/dashboard_base_case.png
```

It shows:

- key valuation metrics
- annual profit over time
- projected fund value
- active policies over time

---

## How to run the project

### 1. Clone the repo

```bash
git clone git@github.com:mousse-lab/cash-flow.git
cd cash-flow
```

Or, if using HTTPS:

```bash
git clone https://github.com/mousse-lab/cash-flow.git
cd cash-flow
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the model

```bash
python -m src.cashflow_engine
```

---

## Output files

After running the model, results are saved in:

```text
outputs/
```

Expected outputs:

```text
outputs/cashflow_projection.csv
outputs/scenario_results.csv
outputs/short_report.md
outputs/dashboard_base_case.png
outputs/annual_profit_base_case.png
outputs/fund_value_base_case.png
outputs/active_policies_base_case.png
outputs/scenario_comparison_pv_profit.png
outputs/scenario_comparison_profit_margin.png
```

---

## How to interpret the outputs

### `cashflow_projection.csv`

This file contains yearly projection results for each scenario.

Important columns:

```text
scenario_name
projection_year
active_policies
premium_income
fund_value
fee_income
expenses
acquisition_costs
annual_profit
discounted_profit
mortality_rate
lapse_rate
discount_rate
investment_return
```

Use this file to understand how cash flows develop year by year.

---

### `scenario_results.csv`

This file contains one row per scenario.

Important columns:

```text
scenario_name
pv_future_profit
total_fee_income
total_expenses
profit_margin
break_even_year
source_premium_income
source_operating_expenses
```

Use this file to compare how different scenarios affect profitability.

---

### Visual outputs

The PNG files are designed for quick communication and portfolio presentation.

Examples:

```text
dashboard_base_case.png
scenario_comparison_pv_profit.png
scenario_comparison_profit_margin.png
```

These show how assumptions and scenarios affect long-term profitability.

---

## SQL files

The SQL folder contains schema and example queries:

```text
sql/create_tables.sql
sql/example_queries.sql
```

These files are included to show how the same modelling workflow could be stored and queried in a database.

Example use cases:

- store policy data
- store assumptions
- store scenario results
- compare present value of future profits by scenario
- query yearly cash-flow projections

---

## Current limitations

This is a simplified educational model. It does not include:

- real customer policy records
- detailed product guarantees
- taxes
- regulatory capital
- IFRS 17 logic
- Solvency II SCR calculations
- stochastic simulations
- detailed lapse models
- detailed mortality improvements
- asset-liability modelling
- dynamic management actions

The purpose is not to create a production model. The purpose is to demonstrate understanding of actuarial cash-flow modelling, assumption management, scenario analysis, and reporting.

---

## Possible next improvements

Good next steps would be:

1. Replace placeholder financial inputs with values extracted from a real annual report.
2. Replace placeholder mortality assumptions with real SCB/HMD mortality data.
3. Replace placeholder interest-rate assumptions with real Riksbank or market data.
4. Add a Streamlit dashboard for interactive scenario testing.
5. Add unit tests for the projection and valuation functions.
6. Add a calibration notebook explaining how synthetic policies are scaled.
7. Add README screenshots from the generated dashboard.
8. Add a short PDF report for job applications.

---

## Professional positioning

This project can be described in a job application as:

> I built a simplified RAFM-inspired actuarial cash-flow model in Python. The model uses a synthetic policy-level portfolio calibrated with processed financial input templates, mortality assumptions, and interest-rate assumptions. It projects future cash flows, calculates profitability metrics, runs scenario analysis, and generates visual reports. The goal was to better understand assumption-driven insurance valuation workflows similar to those used in actuarial modelling platforms.

---

## Disclaimer

All policy-level data in this repository is synthetic. Processed financial, mortality, and interest-rate files currently contain placeholder values and are intended to be replaced with public-source data. This project is for learning and demonstration only and should not be used as actuarial, financial, accounting, regulatory, or investment advice.

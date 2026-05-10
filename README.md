# RAFM-inspired Insurance Cash-Flow Model

A small Python project that simulates cash-flow projection and profitability analysis for a savings-insurance portfolio.

The project is inspired by actuarial modelling workflows used in tools such as **RiskAgility Financial Modeller (RAFM)**, but it does not use RAFM directly. The goal is to show how policy data, assumptions, scenarios, and valuation logic can be combined into a simple cash-flow model.

## What the project does

The model projects future cash flows for a synthetic insurance portfolio and calculates profitability under different scenarios.

It includes:

- synthetic policy-level data
- financial input calibration
- mortality assumptions
- interest-rate and investment-return assumptions
- cash-flow projection
- scenario analysis
- valuation metrics
- generated charts and reports

## Data

The project does not use real customer policy data. The policy portfolio is synthetic, because real life-insurance policy data is private and not publicly available.

The model uses three types of data:

| File | Purpose |
|---|---|
| `data/policies_sample.csv` | Synthetic policy-level portfolio |
| `data/assumptions_base.csv` | Base modelling assumptions |
| `data/scenarios.csv` | Scenario shocks such as high lapse or low investment return |
| `data/processed/financial_inputs.csv` | Placeholder annual-report-style financial inputs |
| `data/processed/mortality_table_sweden.csv` | Placeholder age/gender mortality assumptions |
| `data/processed/interest_rate_assumptions.csv` | Placeholder discount-rate and investment-return assumptions |

The processed files are structured so they can later be replaced with public data from sources such as:

- Swedbank Försäkring annual reports
- Statistics Sweden / SCB mortality tables
- Human Mortality Database
- Sveriges Riksbank interest-rate data

## How the model works

The main script is:

```text
src/cashflow_engine.py
```

The workflow is:

1. Load policy data, assumptions, scenarios, and processed input files.
2. Calibrate the synthetic portfolio using aggregate financial inputs.
3. Estimate a portfolio-level mortality rate from the mortality table.
4. Apply interest-rate and investment-return assumptions.
5. Apply scenario shocks.
6. Project yearly cash flows.
7. Calculate valuation metrics.
8. Generate CSV outputs, charts, and a short markdown report.

The simplified projection calculates:

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

## Project structure

```text
cash-flow/
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
│   ├── assumptions.py
│   ├── cashflow_engine.py
│   ├── load_data.py
│   ├── reporting.py
│   ├── scenarios.py
│   └── valuation.py
├── tests/
│   └── .gitkeep
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone git@github.com:mousse-lab/cash-flow.git
cd cash-flow
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Run the model

```bash
python -m src.cashflow_engine
```

## Outputs

After running the model, outputs are saved in:

```text
outputs/
```

Generated files include:

```text
cashflow_projection.csv
scenario_results.csv
short_report.md
dashboard_base_case.png
annual_profit_base_case.png
fund_value_base_case.png
active_policies_base_case.png
scenario_comparison_pv_profit.png
scenario_comparison_profit_margin.png
```

The most useful visual summary is:

```text
outputs/dashboard_base_case.png
```

## Main results files

### `outputs/cashflow_projection.csv`

Year-by-year projected cash flows for each scenario.

Important columns:

```text
scenario_name
projection_year
active_policies
premium_income
fund_value
fee_income
expenses
annual_profit
discounted_profit
```

### `outputs/scenario_results.csv`

Scenario-level profitability summary.

Important columns:

```text
scenario_name
pv_future_profit
total_fee_income
total_expenses
profit_margin
break_even_year
```

## Current limitations

This is a simplified educational model. It does not include detailed insurance guarantees, taxes, IFRS 17, Solvency II capital calculations, stochastic simulations, or real customer data.

The purpose is to demonstrate understanding of actuarial-style cash-flow modelling, assumption management, scenario analysis, and reporting.

## Possible improvements

Potential next steps:

- replace placeholder inputs with real public-source data
- add a Streamlit dashboard
- add unit tests
- add a calibration notebook
- add a short PDF report

## Disclaimer

All policy-level data is synthetic. The processed financial, mortality, and interest-rate files currently contain placeholder values and are intended to be replaced with public-source data. This project is for learning and demonstration only.

# RAFM-inspired Cash-Flow Model Report

## Objective
This report summarises a simplified cash-flow and profitability projection for a synthetic savings-insurance portfolio.

## Scenario results
|   pv_future_profit |   total_fee_income |   total_expenses |   profit_margin_pct |   break_even_year | scenario_name         |
|-------------------:|-------------------:|-----------------:|--------------------:|------------------:|:----------------------|
|        1.41512e+06 |        2.7804e+06  |          72646.1 |               87.31 |                 1 | base_case             |
|        1.3055e+06  |        2.52521e+06 |          50359.1 |              110.68 |                 1 | high_lapse            |
|        1.14033e+06 |        2.1977e+06  |          72646.1 |               68.49 |                 1 | low_investment_return |
|        1.40525e+06 |        2.7804e+06  |          87175.4 |               86.84 |                 1 | high_expenses         |
|   859665           |        1.65207e+06 |          60430.9 |               71.11 |                 1 | combined_stress       |

## Generated visuals
- `dashboard_base_case.png`
- `annual_profit_base_case.png`
- `fund_value_base_case.png`
- `active_policies_base_case.png`
- `scenario_comparison_pv_profit.png`
- `scenario_comparison_profit_margin.png`

## Interpretation
The scenario comparison shows how sensitive projected profitability is to assumptions such as lapse rates, investment returns, expense levels, and fee margins.

## Limitations
This is a simplified educational model and does not include regulatory capital, tax, detailed mortality tables, stochastic scenarios, guarantees, or full actuarial reserving logic.
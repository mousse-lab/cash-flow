-- Present value of future profits by scenario
SELECT
    scenario_name,
    ROUND(SUM(discounted_profit), 2) AS pv_future_profit
FROM cashflow_results
GROUP BY scenario_name
ORDER BY pv_future_profit DESC;

-- Yearly projected profit for the base case
SELECT
    projection_year,
    ROUND(annual_profit, 2) AS annual_profit,
    ROUND(discounted_profit, 2) AS discounted_profit
FROM cashflow_results
WHERE scenario_name = 'base_case'
ORDER BY projection_year;

-- Compare total fees and expenses by scenario
SELECT
    scenario_name,
    ROUND(SUM(fee_income), 2) AS total_fee_income,
    ROUND(SUM(expenses), 2) AS total_expenses
FROM cashflow_results
GROUP BY scenario_name;

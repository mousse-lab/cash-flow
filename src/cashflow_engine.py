from pathlib import Path
from typing import Dict, Tuple

import pandas as pd

from src.assumptions import (
    apply_interest_rate_assumption,
    apply_scenario,
    assumptions_to_dict,
    financial_inputs_to_dict,
)
from src.load_data import (
    load_assumptions,
    load_financial_inputs,
    load_interest_rate_assumptions,
    load_mortality_table,
    load_policies,
    load_scenarios,
)
from src.reporting import generate_all_charts, write_markdown_report
from src.valuation import summarize_scenario

ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT_DIR / "outputs"


def calibrate_policy_portfolio(
    policies: pd.DataFrame,
    financial_inputs: Dict[str, float],
) -> pd.DataFrame:
    """Scale synthetic policy premiums and fund values to public financial-input totals.

    Real policy-level data is not publicly available, so the model keeps a
    synthetic portfolio but calibrates its aggregate premium income and fund
    value to processed annual-report style inputs.
    """
    calibrated = policies.copy()

    target_premium_income = financial_inputs.get("premium_income")
    target_assets_under_management = financial_inputs.get("assets_under_management")

    if target_premium_income and calibrated["annual_premium"].sum() > 0:
        premium_scale = target_premium_income / calibrated["annual_premium"].sum()
        calibrated["annual_premium"] = calibrated["annual_premium"] * premium_scale

    if target_assets_under_management and calibrated["fund_value"].sum() > 0:
        fund_scale = target_assets_under_management / calibrated["fund_value"].sum()
        calibrated["fund_value"] = calibrated["fund_value"] * fund_scale

    return calibrated


def estimate_portfolio_mortality_rate(
    policies: pd.DataFrame,
    mortality_table: pd.DataFrame,
) -> float:
    """Estimate a portfolio-level mortality rate from age/gender mortality data.

    The current projection engine uses an aggregate mortality assumption. This
    function makes that assumption data-driven by matching each policy to the
    nearest available age/gender mortality rate and then taking a portfolio
    average.
    """
    if mortality_table.empty:
        return 0.0

    mortality_rates = []

    for _, policy in policies.iterrows():
        gender_table = mortality_table[mortality_table["gender"] == policy["gender"]]
        if gender_table.empty:
            gender_table = mortality_table

        nearest_index = (gender_table["age"] - policy["age"]).abs().idxmin()
        mortality_rates.append(float(gender_table.loc[nearest_index, "qx"]))

    if not mortality_rates:
        return 0.0

    return float(sum(mortality_rates) / len(mortality_rates))


def update_assumptions_from_processed_data(
    assumptions: Dict[str, float],
    policies: pd.DataFrame,
    financial_inputs: Dict[str, float],
    mortality_table: pd.DataFrame,
    interest_rates: pd.DataFrame,
    scenario_name: str,
) -> Dict[str, float]:
    """Update base assumptions using processed real-data templates."""
    updated = apply_interest_rate_assumption(assumptions, interest_rates, scenario_name)

    estimated_mortality = estimate_portfolio_mortality_rate(policies, mortality_table)
    if estimated_mortality > 0:
        updated["mortality_rate"] = estimated_mortality

    operating_expenses = financial_inputs.get("operating_expenses")
    if operating_expenses and len(policies) > 0:
        updated["expense_per_policy"] = operating_expenses / len(policies)

    return updated


def project_cashflows(
    policies: pd.DataFrame,
    assumptions: Dict[str, float],
    scenario_name: str = "base_case",
) -> pd.DataFrame:
    """Project yearly cash flows for a simplified savings-insurance portfolio.

    The implementation is intentionally simplified. It is designed to demonstrate
    an assumption-driven actuarial modelling workflow, not to replace a real
    actuarial valuation model.
    """
    projection_years = int(assumptions["projection_years"])
    discount_rate = assumptions["discount_rate"]
    investment_return = assumptions["investment_return"]
    annual_fee_rate = assumptions["annual_fee_rate"]
    expense_per_policy = assumptions["expense_per_policy"]
    acquisition_cost_rate = assumptions["acquisition_cost_rate"]
    lapse_rate = assumptions["base_lapse_rate"]
    mortality_rate = assumptions["mortality_rate"]
    expense_inflation = assumptions["expense_inflation"]

    active_policies = float(len(policies))
    annual_premium = float(policies["annual_premium"].sum())
    fund_value = float(policies["fund_value"].sum())

    rows = []

    for year in range(1, projection_years + 1):
        survival_factor = max(0.0, 1.0 - lapse_rate - mortality_rate)
        active_policies *= survival_factor

        premium_income = annual_premium * (active_policies / len(policies))
        fund_value = (fund_value + premium_income) * (1.0 + investment_return)
        fee_income = fund_value * annual_fee_rate
        expenses = active_policies * expense_per_policy * ((1.0 + expense_inflation) ** (year - 1))

        # Acquisition costs are only applied in the first projection year.
        acquisition_costs = premium_income * acquisition_cost_rate if year == 1 else 0.0

        annual_profit = fee_income - expenses - acquisition_costs
        discounted_profit = annual_profit / ((1.0 + discount_rate) ** year)

        rows.append(
            {
                "scenario_name": scenario_name,
                "projection_year": year,
                "active_policies": active_policies,
                "premium_income": premium_income,
                "fund_value": fund_value,
                "fee_income": fee_income,
                "expenses": expenses,
                "acquisition_costs": acquisition_costs,
                "annual_profit": annual_profit,
                "discounted_profit": discounted_profit,
                "mortality_rate": mortality_rate,
                "lapse_rate": lapse_rate,
                "discount_rate": discount_rate,
                "investment_return": investment_return,
            }
        )

    return pd.DataFrame(rows)


def run_all_scenarios() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Run the base model and all predefined sensitivity scenarios."""
    raw_policies = load_policies()
    financial_inputs = financial_inputs_to_dict(load_financial_inputs())
    policies = calibrate_policy_portfolio(raw_policies, financial_inputs)

    assumptions = assumptions_to_dict(load_assumptions())
    scenarios = load_scenarios()
    mortality_table = load_mortality_table()
    interest_rates = load_interest_rate_assumptions()

    all_cashflows = []
    summaries = []

    for _, scenario in scenarios.iterrows():
        scenario_name = scenario["scenario_name"]
        data_driven_assumptions = update_assumptions_from_processed_data(
            assumptions=assumptions,
            policies=policies,
            financial_inputs=financial_inputs,
            mortality_table=mortality_table,
            interest_rates=interest_rates,
            scenario_name=scenario_name,
        )
        scenario_assumptions = apply_scenario(data_driven_assumptions, scenario)
        cashflows = project_cashflows(policies, scenario_assumptions, scenario_name)
        all_cashflows.append(cashflows)

        summary = summarize_scenario(cashflows)
        summary["scenario_name"] = scenario_name
        summary["source_premium_income"] = financial_inputs.get("premium_income")
        summary["source_operating_expenses"] = financial_inputs.get("operating_expenses")
        summaries.append(summary)

    return pd.concat(all_cashflows, ignore_index=True), pd.DataFrame(summaries)


def main() -> None:
    """Run projections, write output CSV files, and generate visual reports."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    cashflows, summaries = run_all_scenarios()
    cashflow_path = OUTPUT_DIR / "cashflow_projection.csv"
    summary_path = OUTPUT_DIR / "scenario_results.csv"

    cashflows.to_csv(cashflow_path, index=False)
    summaries.to_csv(summary_path, index=False)

    chart_paths = generate_all_charts(cashflows, summaries, scenario_name="base_case")
    report_path = write_markdown_report(summaries)

    print(f"Cash-flow projection written to {cashflow_path}")
    print(f"Scenario summary written to {summary_path}")
    print(f"Markdown report written to {report_path}")
    print("\nGenerated charts:")
    for chart_name, chart_path in chart_paths.items():
        print(f"- {chart_name}: {chart_path}")

    print("\nScenario summary:")
    print(summaries.sort_values("pv_future_profit", ascending=False).to_string(index=False))


if __name__ == "__main__":
    main()

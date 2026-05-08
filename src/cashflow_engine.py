from pathlib import Path
from typing import Dict, Tuple

import pandas as pd

from src.assumptions import apply_scenario, assumptions_to_dict
from src.load_data import load_assumptions, load_policies, load_scenarios
from src.reporting import generate_all_charts, write_markdown_report
from src.valuation import summarize_scenario

ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT_DIR / "outputs"


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
            }
        )

    return pd.DataFrame(rows)


def run_all_scenarios() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Run the base model and all predefined sensitivity scenarios."""
    policies = load_policies()
    assumptions = assumptions_to_dict(load_assumptions())
    scenarios = load_scenarios()

    all_cashflows = []
    summaries = []

    for _, scenario in scenarios.iterrows():
        scenario_name = scenario["scenario_name"]
        scenario_assumptions = apply_scenario(assumptions, scenario)
        cashflows = project_cashflows(policies, scenario_assumptions, scenario_name)
        all_cashflows.append(cashflows)

        summary = summarize_scenario(cashflows)
        summary["scenario_name"] = scenario_name
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

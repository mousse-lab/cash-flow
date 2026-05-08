from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT_DIR / "outputs"


def _format_millions(value: float) -> str:
    """Format large monetary values in millions."""
    return f"{value / 1_000_000:.2f}M"


def _get_scenario(cashflows: pd.DataFrame, scenario_name: str) -> pd.DataFrame:
    """Return cash flows for a single scenario and validate that it exists."""
    scenario_df = cashflows[cashflows["scenario_name"] == scenario_name].copy()

    if scenario_df.empty:
        available = ", ".join(sorted(cashflows["scenario_name"].unique()))
        raise ValueError(f"Scenario '{scenario_name}' not found. Available scenarios: {available}")

    return scenario_df.sort_values("projection_year")


def plot_annual_profit(cashflows: pd.DataFrame, scenario_name: str = "base_case") -> Path:
    """Create an annual profit chart for one scenario."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    scenario_df = _get_scenario(cashflows, scenario_name)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(scenario_df["projection_year"], scenario_df["annual_profit"], marker="o", linewidth=2)
    ax.axhline(0, linewidth=1)
    ax.set_title(f"Projected annual profit: {scenario_name}")
    ax.set_xlabel("Projection year")
    ax.set_ylabel("Annual profit")
    ax.grid(True, alpha=0.3)

    output_path = OUTPUT_DIR / f"annual_profit_{scenario_name}.png"
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)

    return output_path


def plot_fund_value(cashflows: pd.DataFrame, scenario_name: str = "base_case") -> Path:
    """Create a projected fund value chart for one scenario."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    scenario_df = _get_scenario(cashflows, scenario_name)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(scenario_df["projection_year"], scenario_df["fund_value"], marker="o", linewidth=2)
    ax.set_title(f"Projected fund value: {scenario_name}")
    ax.set_xlabel("Projection year")
    ax.set_ylabel("Fund value")
    ax.grid(True, alpha=0.3)

    output_path = OUTPUT_DIR / f"fund_value_{scenario_name}.png"
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)

    return output_path


def plot_active_policies(cashflows: pd.DataFrame, scenario_name: str = "base_case") -> Path:
    """Create an active policies chart for one scenario."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    scenario_df = _get_scenario(cashflows, scenario_name)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(scenario_df["projection_year"], scenario_df["active_policies"], marker="o", linewidth=2)
    ax.set_title(f"Projected active policies: {scenario_name}")
    ax.set_xlabel("Projection year")
    ax.set_ylabel("Active policies")
    ax.grid(True, alpha=0.3)

    output_path = OUTPUT_DIR / f"active_policies_{scenario_name}.png"
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)

    return output_path


def plot_scenario_comparison(summaries: pd.DataFrame) -> Path:
    """Create a bar chart comparing PV future profit across scenarios."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    plot_df = summaries.sort_values("pv_future_profit", ascending=True).copy()

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.barh(plot_df["scenario_name"], plot_df["pv_future_profit"])
    ax.set_title("Scenario comparison: present value of future profits")
    ax.set_xlabel("PV future profit")
    ax.set_ylabel("Scenario")
    ax.grid(True, axis="x", alpha=0.3)

    for index, value in enumerate(plot_df["pv_future_profit"]):
        ax.text(value, index, f" {_format_millions(value)}", va="center")

    output_path = OUTPUT_DIR / "scenario_comparison_pv_profit.png"
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)

    return output_path


def plot_profit_margin_comparison(summaries: pd.DataFrame) -> Path:
    """Create a bar chart comparing profit margin across scenarios."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    plot_df = summaries.sort_values("profit_margin", ascending=True).copy()
    plot_df["profit_margin_pct"] = plot_df["profit_margin"] * 100

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.barh(plot_df["scenario_name"], plot_df["profit_margin_pct"])
    ax.set_title("Scenario comparison: profit margin")
    ax.set_xlabel("Profit margin (%)")
    ax.set_ylabel("Scenario")
    ax.grid(True, axis="x", alpha=0.3)

    for index, value in enumerate(plot_df["profit_margin_pct"]):
        ax.text(value, index, f" {value:.1f}%", va="center")

    output_path = OUTPUT_DIR / "scenario_comparison_profit_margin.png"
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)

    return output_path


def plot_cashflow_dashboard(cashflows: pd.DataFrame, summaries: pd.DataFrame, scenario_name: str = "base_case") -> Path:
    """Create a compact dashboard-style figure for the selected scenario."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    scenario_df = _get_scenario(cashflows, scenario_name)
    summary_row = summaries[summaries["scenario_name"] == scenario_name].iloc[0]

    fig = plt.figure(figsize=(12, 8))
    fig.suptitle("RAFM-inspired Cash-Flow Model Dashboard", fontsize=16, fontweight="bold")

    ax_kpi = fig.add_subplot(2, 2, 1)
    ax_kpi.axis("off")
    kpi_text = (
        f"Scenario: {scenario_name}\n\n"
        f"PV future profit: {_format_millions(summary_row['pv_future_profit'])}\n"
        f"Total fee income: {_format_millions(summary_row['total_fee_income'])}\n"
        f"Total expenses: {_format_millions(summary_row['total_expenses'])}\n"
        f"Profit margin: {summary_row['profit_margin'] * 100:.1f}%\n"
        f"Break-even year: {summary_row['break_even_year']}"
    )
    ax_kpi.text(0.03, 0.95, kpi_text, va="top", fontsize=12)
    ax_kpi.set_title("Key metrics", loc="left")

    ax_profit = fig.add_subplot(2, 2, 2)
    ax_profit.plot(scenario_df["projection_year"], scenario_df["annual_profit"], marker="o", linewidth=2)
    ax_profit.axhline(0, linewidth=1)
    ax_profit.set_title("Annual profit")
    ax_profit.set_xlabel("Year")
    ax_profit.grid(True, alpha=0.3)

    ax_fund = fig.add_subplot(2, 2, 3)
    ax_fund.plot(scenario_df["projection_year"], scenario_df["fund_value"], marker="o", linewidth=2)
    ax_fund.set_title("Fund value")
    ax_fund.set_xlabel("Year")
    ax_fund.grid(True, alpha=0.3)

    ax_policies = fig.add_subplot(2, 2, 4)
    ax_policies.plot(scenario_df["projection_year"], scenario_df["active_policies"], marker="o", linewidth=2)
    ax_policies.set_title("Active policies")
    ax_policies.set_xlabel("Year")
    ax_policies.grid(True, alpha=0.3)

    output_path = OUTPUT_DIR / f"dashboard_{scenario_name}.png"
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(output_path, dpi=160)
    plt.close(fig)

    return output_path


def generate_all_charts(
    cashflows: pd.DataFrame,
    summaries: pd.DataFrame,
    scenario_name: str = "base_case",
) -> Dict[str, Path]:
    """Generate all standard project visuals and return their output paths."""
    return {
        "annual_profit": plot_annual_profit(cashflows, scenario_name),
        "fund_value": plot_fund_value(cashflows, scenario_name),
        "active_policies": plot_active_policies(cashflows, scenario_name),
        "scenario_pv_profit": plot_scenario_comparison(summaries),
        "scenario_profit_margin": plot_profit_margin_comparison(summaries),
        "dashboard": plot_cashflow_dashboard(cashflows, summaries, scenario_name),
    }


def write_markdown_report(summaries: pd.DataFrame) -> Path:
    """Write a short markdown report summarising scenario results."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / "short_report.md"

    display_df = summaries.copy()
    display_df["pv_future_profit"] = display_df["pv_future_profit"].round(2)
    display_df["total_fee_income"] = display_df["total_fee_income"].round(2)
    display_df["total_expenses"] = display_df["total_expenses"].round(2)
    display_df["profit_margin"] = (display_df["profit_margin"] * 100).round(2)
    display_df = display_df.rename(columns={"profit_margin": "profit_margin_pct"})

    report = [
        "# RAFM-inspired Cash-Flow Model Report",
        "",
        "## Objective",
        "This report summarises a simplified cash-flow and profitability projection for a synthetic savings-insurance portfolio.",
        "",
        "## Scenario results",
        display_df.to_markdown(index=False),
        "",
        "## Generated visuals",
        "- `dashboard_base_case.png`",
        "- `annual_profit_base_case.png`",
        "- `fund_value_base_case.png`",
        "- `active_policies_base_case.png`",
        "- `scenario_comparison_pv_profit.png`",
        "- `scenario_comparison_profit_margin.png`",
        "",
        "## Interpretation",
        "The scenario comparison shows how sensitive projected profitability is to assumptions such as lapse rates, investment returns, expense levels, and fee margins.",
        "",
        "## Limitations",
        "This is a simplified educational model and does not include regulatory capital, tax, detailed mortality tables, stochastic scenarios, guarantees, or full actuarial reserving logic.",
    ]

    output_path.write_text("\n".join(report), encoding="utf-8")
    return output_path

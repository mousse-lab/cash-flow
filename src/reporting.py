from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT_DIR / "outputs"


def plot_annual_profit(cashflows: pd.DataFrame, scenario_name: str = "base_case") -> Path:
    """Create a simple annual profit chart for one scenario."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    scenario_df = cashflows[cashflows["scenario_name"] == scenario_name]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(scenario_df["projection_year"], scenario_df["annual_profit"], marker="o")
    ax.set_title(f"Projected annual profit: {scenario_name}")
    ax.set_xlabel("Projection year")
    ax.set_ylabel("Annual profit")
    ax.grid(True, alpha=0.3)

    output_path = OUTPUT_DIR / f"annual_profit_{scenario_name}.png"
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)

    return output_path


def write_markdown_report(summaries: pd.DataFrame) -> Path:
    """Write a short markdown report summarising scenario results."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / "short_report.md"

    report = [
        "# RAFM-inspired Cash-Flow Model Report",
        "",
        "## Objective",
        "This report summarises a simplified cash-flow and profitability projection for a synthetic savings-insurance portfolio.",
        "",
        "## Scenario results",
        summaries.to_markdown(index=False),
        "",
        "## Interpretation",
        "The scenario comparison shows how sensitive projected profitability is to assumptions such as lapse rates, investment returns, expense levels, and fee margins.",
        "",
        "## Limitations",
        "This is a simplified educational model and does not include regulatory capital, tax, detailed mortality tables, stochastic scenarios, guarantees, or full actuarial reserving logic.",
    ]

    output_path.write_text("\n".join(report), encoding="utf-8")
    return output_path

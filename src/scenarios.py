import pandas as pd


def compare_to_base(summaries: pd.DataFrame, base_scenario: str = "base_case") -> pd.DataFrame:
    """Add change versus base scenario for present value of future profits."""
    summaries = summaries.copy()
    base_value = summaries.loc[
        summaries["scenario_name"] == base_scenario,
        "pv_future_profit",
    ].iloc[0]

    summaries["change_vs_base"] = summaries["pv_future_profit"] - base_value
    summaries["change_vs_base_pct"] = summaries["change_vs_base"] / base_value

    return summaries.sort_values("pv_future_profit", ascending=False)

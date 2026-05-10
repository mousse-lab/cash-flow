from typing import Dict

import pandas as pd


def assumptions_to_dict(assumptions: pd.DataFrame) -> Dict[str, float]:
    """Convert the assumptions table into a simple dictionary."""
    return dict(zip(assumptions["assumption_name"], assumptions["value"]))


def financial_inputs_to_dict(financial_inputs: pd.DataFrame) -> Dict[str, float]:
    """Convert processed financial inputs into a metric dictionary."""
    return dict(zip(financial_inputs["metric"], financial_inputs["value"]))


def apply_interest_rate_assumption(
    base: Dict[str, float],
    interest_rates: pd.DataFrame,
    scenario_name: str,
) -> Dict[str, float]:
    """Update discount-rate and investment-return assumptions from processed rate data."""
    updated = base.copy()
    selected = interest_rates[interest_rates["scenario_name"] == scenario_name]

    if selected.empty:
        return updated

    row = selected.iloc[0]
    updated["discount_rate"] = float(row["discount_rate"])
    updated["investment_return"] = float(row["investment_return"])

    return updated


def apply_scenario(base: Dict[str, float], scenario: pd.Series) -> Dict[str, float]:
    """Create scenario-specific assumptions from the base assumptions."""
    updated = base.copy()

    updated["base_lapse_rate"] = base["base_lapse_rate"] * scenario["lapse_rate_multiplier"]
    updated["investment_return"] = base["investment_return"] + scenario["investment_return_shift"]
    updated["expense_per_policy"] = base["expense_per_policy"] * scenario["expense_multiplier"]
    updated["annual_fee_rate"] = base["annual_fee_rate"] + scenario["fee_rate_shift"]

    return updated

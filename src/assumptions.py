import pandas as pd


def assumptions_to_dict(assumptions: pd.DataFrame) -> dict[str, float]:
    """Convert the assumptions table into a simple dictionary."""
    return dict(zip(assumptions["assumption_name"], assumptions["value"]))


def apply_scenario(base: dict[str, float], scenario: pd.Series) -> dict[str, float]:
    """Create scenario-specific assumptions from the base assumptions."""
    updated = base.copy()

    updated["base_lapse_rate"] = base["base_lapse_rate"] * scenario["lapse_rate_multiplier"]
    updated["investment_return"] = base["investment_return"] + scenario["investment_return_shift"]
    updated["expense_per_policy"] = base["expense_per_policy"] * scenario["expense_multiplier"]
    updated["annual_fee_rate"] = base["annual_fee_rate"] + scenario["fee_rate_shift"]

    return updated

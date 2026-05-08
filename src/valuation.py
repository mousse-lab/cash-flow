import pandas as pd


def present_value_of_future_profits(cashflows: pd.DataFrame) -> float:
    """Calculate present value of future profits from discounted yearly profits."""
    return float(cashflows["discounted_profit"].sum())


def profit_margin(cashflows: pd.DataFrame) -> float:
    """Calculate profit margin as profit divided by total premium income."""
    total_premium = cashflows["premium_income"].sum()
    if total_premium == 0:
        return 0.0
    return float(cashflows["annual_profit"].sum() / total_premium)


def break_even_year(cashflows: pd.DataFrame) -> int | None:
    """Return first projection year where cumulative discounted profit becomes positive."""
    cumulative = cashflows["discounted_profit"].cumsum()
    positive_years = cashflows.loc[cumulative > 0, "projection_year"]

    if positive_years.empty:
        return None

    return int(positive_years.iloc[0])


def summarize_scenario(cashflows: pd.DataFrame) -> dict[str, float | int | None]:
    """Create a compact scenario-level valuation summary."""
    return {
        "pv_future_profit": present_value_of_future_profits(cashflows),
        "total_fee_income": float(cashflows["fee_income"].sum()),
        "total_expenses": float(cashflows["expenses"].sum()),
        "profit_margin": profit_margin(cashflows),
        "break_even_year": break_even_year(cashflows),
    }

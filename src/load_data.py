from pathlib import Path
from typing import Optional

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
PROCESSED_DATA_DIR = DATA_DIR / "processed"


def load_policies(path: Optional[Path] = None) -> pd.DataFrame:
    """Load synthetic policy-level portfolio data."""
    file_path = path or DATA_DIR / "policies_sample.csv"
    return pd.read_csv(file_path)


def load_assumptions(path: Optional[Path] = None) -> pd.DataFrame:
    """Load base model assumptions."""
    file_path = path or DATA_DIR / "assumptions_base.csv"
    return pd.read_csv(file_path)


def load_scenarios(path: Optional[Path] = None) -> pd.DataFrame:
    """Load scenario definitions."""
    file_path = path or DATA_DIR / "scenarios.csv"
    return pd.read_csv(file_path)


def load_financial_inputs(path: Optional[Path] = None) -> pd.DataFrame:
    """Load processed annual-report style financial inputs."""
    file_path = path or PROCESSED_DATA_DIR / "financial_inputs.csv"
    return pd.read_csv(file_path)


def load_mortality_table(path: Optional[Path] = None) -> pd.DataFrame:
    """Load processed age/gender mortality assumptions."""
    file_path = path or PROCESSED_DATA_DIR / "mortality_table_sweden.csv"
    return pd.read_csv(file_path)


def load_interest_rate_assumptions(path: Optional[Path] = None) -> pd.DataFrame:
    """Load processed discount-rate and investment-return assumptions."""
    file_path = path or PROCESSED_DATA_DIR / "interest_rate_assumptions.csv"
    return pd.read_csv(file_path)

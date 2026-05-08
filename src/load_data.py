from pathlib import Path
from typing import Optional

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"


def load_policies(path: Optional[Path] = None) -> pd.DataFrame:
    """Load synthetic policy data."""
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

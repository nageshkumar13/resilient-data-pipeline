import pandas as pd
from pathlib import Path


def load_csv(path: Path) -> pd.DataFrame:
    """Read and Load a CSV file.. and return it as DataFrame."""
    return pd.read_csv(path)

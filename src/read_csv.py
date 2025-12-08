from pathlib import Path
import pandas as pd


def read_csv(path: str | Path) -> pd.DataFrame:
    """Read a CSV file into a DataFrame."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    return pd.read_csv(path)


def write_csv(df: pd.DataFrame, path: str | Path, index: bool = False) -> None:
    """Write a DataFrame to a CSV file, creating parent dirs if needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=index)

from __future__ import annotations
import pandas as pd


def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with duplicate rows removed."""
    return df.drop_duplicates().reset_index(drop=True)


def strip_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    """Strip leading/trailing whitespace from all string columns."""
    df = df.copy()
    str_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in str_cols:
        df[col] = df[col].astype("string").str.strip()
    return df


def to_lowercase(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Lowercase the specified string columns if they exist."""
    df = df.copy()
    for col in columns:
        if col in df.columns:
            df[col] = df[col].astype("string").str.lower()
    return df
from pathlib import Path
import io

from src.read_csv import read_csv, write_csv
from src.cleaning import drop_duplicates, strip_whitespace, to_lowercase


def simple_customers_etl() -> None:
    project_root = Path(__file__).resolve().parent
    raw_path = project_root / "AeroVision" / "data" / "raw" / "customers.csv"
    out_path = project_root / "AeroVision" / "data" / "processed" / "customers_clean.csv"

    df = read_csv(raw_path)
    df = strip_whitespace(df)
    df = drop_duplicates(df)
    df = to_lowercase(df, columns=["email", "company_name", "country", "industry"])

    write_csv(df, out_path)
    print(f"[OK] Cleaned customers written to: {out_path}")


if __name__ == "__main__":
    simple_customers_etl()

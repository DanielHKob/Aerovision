from pathlib import Path
import io
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.read_csv import read_csv, write_csv
from src.cleaning import drop_duplicates, strip_whitespace, to_lowercase


def simple_customers_etl() -> None:
    project_root = Path(__file__).resolve().parent
    raw_path = Path("data/raw")
    out_path = Path("data/cleaned/customers_clean.csv")
    print("the path is {raw_path}")

    df = read_csv(raw_path)
    df = strip_whitespace(df)
    df = drop_duplicates(df)
    df = to_lowercase(df, columns=["email", "company_name", "country", "industry"])

    write_csv(df, out_path)
    print(f"[OK] Cleaned customers written to: {out_path}")


if __name__ == "__main__":
    run = input("Would you like to start ETl Pipeline y/n?: ")
    if run.lower() == "y":

        simple_customers_etl()
    else: 
        print("You enter N for no, so the program is terminating")
        

    # run_type = input("What")

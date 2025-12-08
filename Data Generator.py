import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import random


def get_base_path() -> Path:
    # Use a path relative to this file instead of hard-coding absolute path
    base_path = Path("data/raw")
    return base_path


def seed_everything(seed: int = 42) -> None:
    np.random.seed(seed)
    random.seed(seed)


def generate_products(base_path: Path) -> Path:
    product_ids = range(1, 16)
    product_names = [
        "AeroVision Basic Monitoring",
        "AeroVision Pro Monitoring",
        "AeroVision Enterprise Suite",
        "Perimeter Alert Add-on",
        "Thermal Imaging Module",
        "Night Vision Package",
        "Construction Site Monitoring",
        "Port Security Package",
        "Airport TFR Monitoring",
        "Wildlife Protection Module",
        "Custom Model Training",
        "API Usage Package - Small",
        "API Usage Package - Medium",
        "API Usage Package - Large",
        "On-Prem Deployment Support",
    ]
    product_types = [
        "subscription", "subscription", "subscription",
        "addon", "addon", "addon",
        "subscription", "subscription", "subscription",
        "addon", "service",
        "usage", "usage", "usage",
        "service",
    ]
    billing_models = [
        "monthly", "monthly", "annual",
        "monthly", "monthly", "monthly",
        "monthly", "monthly", "annual",
        "monthly", "project",
        "per_call", "per_call", "per_call",
        "project",
    ]
    unit_prices = [
        299, 599, 1999, 79, 149, 129,
        399, 499, 2499, 99, 2000,
        0.005, 0.004, 0.003, 5000,
    ]
    currency = "EUR"

    products_df = pd.DataFrame({
        "product_id": product_ids,
        "product_name": product_names,
        "product_type": product_types,
        "billing_model": billing_models,
        "unit_price": unit_prices,
        "currency": [currency] * len(product_ids),
        "is_active": [True] * len(product_ids),
    })

    path = base_path / "products.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    products_df.to_csv(path, index=False)
    return path


def random_company_name() -> str:
    prefixes = ["Sky", "Aero", "Vision", "Secure", "Drone",
                "Cloud", "Northern", "Port", "City", "Prime"]
    suffixes = ["Watch", "Analytics", "Security", "Monitoring",
                "Systems", "Solutions", "Insights", "Networks"]
    return f"{random.choice(prefixes)} {random.choice(suffixes)}"


def generate_customers(base_path: Path, num_customers: int = 150) -> Path:
    industries = [
        "Security", "Construction", "Port Authority",
        "Airport", "Energy", "Government", "Logistics",
    ]
    countries = ["Denmark", "Germany", "Sweden",
                 "Norway", "Netherlands", "Finland", "UK"]
    segments = ["SMB", "Mid-Market", "Enterprise"]
    statuses = ["active", "active", "active", "trial", "churned"]

    customer_ids = range(1, num_customers + 1)
    signup_start = datetime(2022, 1, 1)
    signup_dates = [
        signup_start + timedelta(days=int(np.random.randint(0, 365 * 3)))
        for _ in customer_ids
    ]

    customers_df = pd.DataFrame({
        "customer_id": customer_ids,
        "company_name": [random_company_name() for _ in customer_ids],
        "industry": np.random.choice(industries, size=num_customers),
        "country": np.random.choice(countries, size=num_customers),
        "email": [f"contact{cid}@example.com" for cid in customer_ids],
        "segment": np.random.choice(segments, size=num_customers, p=[0.5, 0.3, 0.2]),
        "status": np.random.choice(statuses, size=num_customers,
                                   p=[0.6, 0.15, 0.1, 0.1, 0.05]),
        "signup_date": signup_dates,
    })

    path = base_path / "customers.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    customers_df.to_csv(path, index=False)
    return path, customers_df  # return df so we can reuse ids


def generate_detection_logs(
    base_path: Path,
    customers_df: pd.DataFrame,
    num_logs: int = 1000,
    product_ids: range = range(1, 16),
) -> Path:
    detected_objects = ["bird", "drone", "unknown"]
    locations = [
        "AarhusPort", "CopenhagenHarbor", "BillundAirport",
        "CopenhagenAirport", "OdenseIndustrial", "EsbjergPort",
    ]

    log_ids = range(1, num_logs + 1)
    start_time = datetime(2024, 1, 1)

    timestamps = [
        start_time + timedelta(minutes=int(np.random.randint(0, 60 * 24 * 60)))
        for _ in log_ids
    ]
    customer_ids = customers_df["customer_id"].values
    customer_ids_for_logs = np.random.choice(customer_ids, size=num_logs)
    product_ids_for_logs = np.random.choice(
        list(product_ids),
        size=num_logs,
        p=[
            0.1, 0.15, 0.05, 0.08, 0.07,
            0.05, 0.12, 0.12, 0.04, 0.04,
            0.03, 0.05, 0.03, 0.03, 0.04,
        ],
    )

    obj_choices = np.random.choice(detected_objects, size=num_logs, p=[0.6, 0.3, 0.1])
    confidence = np.round(
        np.where(
            obj_choices == "unknown",
            np.random.uniform(0.4, 0.75, size=num_logs),
            np.random.uniform(0.7, 0.99, size=num_logs),
        ),
        3,
    )
    altitudes = np.random.randint(20, 200, size=num_logs)

    def random_alert_level(obj: str, conf: float) -> str:
        if obj == "drone" and conf > 0.9 and np.random.rand() < 0.5:
            return "critical"
        if obj == "drone":
            return np.random.choice(["medium", "high"], p=[0.3, 0.7])
        if obj == "bird":
            return np.random.choice(["low", "medium"], p=[0.7, 0.3])
        return np.random.choice(["low", "medium", "high"], p=[0.5, 0.3, 0.2])

    alert_levels_values = [
        random_alert_level(o, c) for o, c in zip(obj_choices, confidence)
    ]

    detection_df = pd.DataFrame({
        "detection_id": log_ids,
        "customer_id": customer_ids_for_logs,
        "product_id": product_ids_for_logs,
        "timestamp": timestamps,
        "location": np.random.choice(locations, size=num_logs),
        "altitude_m": altitudes,
        "detected_object": obj_choices,
        "confidence": confidence,
        "alert_level": alert_levels_values,
        "processed": np.random.choice([True, False], size=num_logs, p=[0.85, 0.15]),
    })

    path = base_path / "detection_logs.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    detection_df.to_csv(path, index=False)
    return path


def generate_transactions(
    base_path: Path,
    customers_df: pd.DataFrame,
    product_ids: range = range(1, 16),
    unit_prices: list[float] | None = None,
    num_transactions: int = 1000,
    currency: str = "EUR",
) -> Path:
    if unit_prices is None:
        raise ValueError("unit_prices must be provided")

    transaction_ids = range(1, num_transactions + 1)
    trans_start = datetime(2023, 7, 1)
    transaction_dates = [
        trans_start + timedelta(days=int(np.random.randint(0, int(365 * 1.5))))
        for _ in transaction_ids
    ]

    customer_ids = customers_df["customer_id"].values
    customer_ids_for_trans = np.random.choice(customer_ids, size=num_transactions)
    product_ids_for_trans = np.random.choice(list(product_ids), size=num_transactions)

    price_map = {pid: price for pid, price in zip(product_ids, unit_prices)}

    quantities: list[int] = []
    unit_prices_used: list[float] = []
    total_amounts: list[float] = []

    for pid in product_ids_for_trans:
        base_price = price_map[pid]
        if pid in [1, 2, 7, 8]:  # subscriptions
            qty = 1
        elif pid in [11, 15]:  # services / projects
            qty = np.random.randint(1, 6)
        else:
            qty = (
                np.random.randint(1000, 50000)
                if pid in [12, 13, 14]
                else np.random.randint(1, 20)
            )
        quantities.append(qty)
        unit_prices_used.append(base_price)
        total_amounts.append(round(base_price * qty, 2))

    billing_types: list[str] = []
    for pid in product_ids_for_trans:
        if pid in [1, 2, 4, 5, 6, 7, 8, 10]:
            billing_types.append("subscription")
        elif pid in [3, 9]:
            billing_types.append("annual")
        elif pid in [11, 15]:
            billing_types.append("project")
        else:
            billing_types.append("usage")

    transactions_df = pd.DataFrame({
        "transaction_id": transaction_ids,
        "customer_id": customer_ids_for_trans,
        "product_id": product_ids_for_trans,
        "transaction_date": transaction_dates,
        "quantity": quantities,
        "unit_price": unit_prices_used,
        "currency": [currency] * num_transactions,
        "total_amount": total_amounts,
        "billing_type": billing_types,
    })

    path = base_path / "transactions.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    transactions_df.to_csv(path, index=False)
    return path


def main() -> None:
    base_path = get_base_path()
    seed_everything(42)

    products_path = generate_products(base_path)
    print(f"Products written to: {products_path}")

    customers_path, customers_df = generate_customers(base_path)
    print(f"Customers written to: {customers_path}")

    detection_path = generate_detection_logs(base_path, customers_df)
    print(f"Detection logs written to: {detection_path}")

    # Reuse the same unit_prices you defined in generate_products call
    unit_prices = [
        299, 599, 1999, 79, 149, 129,
        399, 499, 2499, 99, 2000,
        0.005, 0.004, 0.003, 5000,
    ]
    transactions_path = generate_transactions(
        base_path,
        customers_df,
        product_ids=range(1, 16),
        unit_prices=unit_prices,
        num_transactions=1000,
        currency="EUR",
    )
    print(f"Transactions written to: {transactions_path}")


if __name__ == "__main__":
    main()

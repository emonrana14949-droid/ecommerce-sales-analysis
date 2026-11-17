"""Generate a synthetic e-commerce sales dataset for practice.

The dataset is practice data only. It is designed to look like an online
store's order data from Bangladesh so the Pandas, NumPy and visualization
workflow can be practised before using real sales data.
"""

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "ecommerce_sales_dataset.csv"

PRICE_RANGES = {
    "Electronics": (1500, 45000),
    "Fashion": (500, 6000),
    "Grocery": (100, 2500),
    "Home & Kitchen": (800, 15000),
    "Beauty": (300, 4000),
    "Sports": (700, 12000),
}


def main() -> None:
    rng = np.random.default_rng(42)
    n = 600

    categories = list(PRICE_RANGES.keys())
    product_category = rng.choice(
        categories,
        size=n,
        p=[0.24, 0.22, 0.20, 0.14, 0.10, 0.10],
    )

    # Category-based unit prices.
    unit_price = np.array(
        [rng.uniform(*PRICE_RANGES[cat]) for cat in product_category]
    )

    quantity = rng.integers(1, 6, size=n)
    discount_percentage = np.round(rng.uniform(0, 40, size=n), 2)

    payment_method = rng.choice(
        ["Cash on Delivery", "bKash", "Nagad", "Card"],
        size=n,
        p=[0.38, 0.30, 0.14, 0.18],
    )
    city = rng.choice(
        ["Dhaka", "Chattogram", "Khulna", "Rajshahi", "Sylhet", "Barishal"],
        size=n,
        p=[0.42, 0.18, 0.11, 0.11, 0.10, 0.08],
    )
    delivery_days = rng.integers(1, 8, size=n)

    # Random order dates across 2025.
    start = np.datetime64("2025-01-01")
    order_date = start + rng.integers(0, 365, size=n)
    order_date = pd.to_datetime(order_date)
    month = order_date.month

    revenue = unit_price * quantity * (1 - discount_percentage / 100)

    df = pd.DataFrame(
        {
            "order_id": [f"ORD-{i:03d}" for i in range(1, n + 1)],
            "order_date": order_date.strftime("%Y-%m-%d"),
            "month": month,
            "product_category": product_category,
            "unit_price_bdt": np.round(unit_price, 2),
            "quantity": quantity,
            "discount_percentage": discount_percentage,
            "payment_method": payment_method,
            "city": city,
            "delivery_days": delivery_days,
            "revenue_bdt": np.round(revenue, 2),
        }
    )

    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_PATH, index=False)
    print(f"Dataset created: {DATA_PATH}")
    print(f"Rows: {len(df)} | Columns: {len(df.columns)}")


if __name__ == "__main__":
    main()

"""Analyse the e-commerce sales dataset with Pandas, NumPy and Matplotlib.

Run from the project root:
    python src/analysis.py

Outputs are saved to:
    outputs/tables/  (CSV summary tables)
    outputs/charts/  (PNG visualizations)
    outputs/insights.md
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "ecommerce_sales_dataset.csv"
TABLE_DIR = PROJECT_ROOT / "outputs" / "tables"
CHART_DIR = PROJECT_ROOT / "outputs" / "charts"
INSIGHTS_PATH = PROJECT_ROOT / "outputs" / "insights.md"

try:
    plt.style.use("seaborn-v0_8-whitegrid")
except OSError:
    plt.style.use("ggplot")


def save_bar_chart(series: pd.Series, title: str, xlabel: str, ylabel: str, path: Path, color: str = "#2f81f7") -> None:
    fig, ax = plt.subplots(figsize=(9, 4.8))
    series.plot(kind="bar", ax=ax, color=color, edgecolor="white")
    ax.set_title(title, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", rotation=25)
    for label in ax.get_xticklabels():
        label.set_ha("right")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_PATH, parse_dates=["order_date"])

    # Basic cleaning.
    df = df.drop_duplicates().copy()
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    df = df.dropna(subset=["revenue_bdt"])

    # Summary tables.
    df.describe(include="all").round(2).to_csv(TABLE_DIR / "summary_statistics.csv")

    monthly = (
        df.groupby("month")
        .agg(
            orders=("order_id", "count"),
            total_revenue_bdt=("revenue_bdt", "sum"),
            avg_order_value_bdt=("revenue_bdt", "mean"),
        )
        .round(2)
    )
    monthly.to_csv(TABLE_DIR / "monthly_revenue.csv")

    by_category = (
        df.groupby("product_category")
        .agg(
            orders=("order_id", "count"),
            total_revenue_bdt=("revenue_bdt", "sum"),
            avg_discount_percentage=("discount_percentage", "mean"),
        )
        .round(2)
        .sort_values("total_revenue_bdt", ascending=False)
    )
    by_category.to_csv(TABLE_DIR / "revenue_by_category.csv")

    by_city = (
        df.groupby("city")
        .agg(
            orders=("order_id", "count"),
            total_revenue_bdt=("revenue_bdt", "sum"),
            avg_order_value_bdt=("revenue_bdt", "mean"),
        )
        .round(2)
        .sort_values("total_revenue_bdt", ascending=False)
    )
    by_city.to_csv(TABLE_DIR / "revenue_by_city.csv")

    corr_cols = ["unit_price_bdt", "quantity", "discount_percentage", "delivery_days", "revenue_bdt"]
    corr = df[corr_cols].corr(numeric_only=True).round(2)
    corr.to_csv(TABLE_DIR / "correlation_matrix.csv")

    # Chart 1: monthly revenue trend (line).
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.plot(monthly.index, monthly["total_revenue_bdt"], marker="o", color="#2f81f7", linewidth=2)
    ax.set_title("Monthly Revenue Trend — 2025", fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total revenue (BDT)")
    ax.set_xticks(monthly.index)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "monthly_revenue_trend.png", dpi=160)
    plt.close(fig)

    # Chart 2: revenue by category (bar).
    save_bar_chart(
        by_category["total_revenue_bdt"],
        "Total Revenue by Product Category",
        "Product category",
        "Total revenue (BDT)",
        CHART_DIR / "revenue_by_category.png",
    )

    # Chart 3: orders by payment method (bar).
    orders_by_payment = df["payment_method"].value_counts()
    save_bar_chart(
        orders_by_payment,
        "Orders by Payment Method",
        "Payment method",
        "Number of orders",
        CHART_DIR / "orders_by_payment_method.png",
        color="#8250df",
    )

    # Chart 4: discount vs revenue (scatter).
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.scatter(df["discount_percentage"], df["revenue_bdt"], alpha=0.6, color="#2f81f7", edgecolor="white", linewidth=0.4)
    slope, intercept = np.polyfit(df["discount_percentage"], df["revenue_bdt"], 1)
    x_line = np.linspace(df["discount_percentage"].min(), df["discount_percentage"].max(), 100)
    ax.plot(x_line, slope * x_line + intercept, color="#111111", linewidth=1.6, label="Trend line")
    ax.set_title("Discount Percentage vs Revenue", fontweight="bold")
    ax.set_xlabel("Discount percentage")
    ax.set_ylabel("Revenue (BDT)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(CHART_DIR / "discount_vs_revenue.png", dpi=160)
    plt.close(fig)

    best_month = int(monthly["total_revenue_bdt"].idxmax())
    best_month_revenue = monthly.loc[best_month, "total_revenue_bdt"]
    top_category = by_category.index[0]
    top_city = by_city.index[0]
    discount_revenue_corr = corr.loc["discount_percentage", "revenue_bdt"]
    total_revenue = df["revenue_bdt"].sum()

    insights = f"""# Key Insights — E-commerce Sales Analysis

> This project uses synthetic practice data generated with NumPy. The patterns below are for learning the workflow only; they are not real business findings.

- Dataset size: **{len(df)} orders** across 2025.
- Total revenue in the dataset: **{total_revenue:,.2f} BDT**.
- The best month by revenue is **month {best_month}** with **{best_month_revenue:,.2f} BDT**.
- The top product category by revenue is **{top_category}** ({by_category.loc[top_category, 'total_revenue_bdt']:,.2f} BDT from {int(by_category.loc[top_category, 'orders'])} orders).
- The top city by revenue is **{top_city}** ({by_city.loc[top_city, 'total_revenue_bdt']:,.2f} BDT).
- Correlation between discount percentage and revenue: **{discount_revenue_corr:.2f}**.

## Charts

- `charts/monthly_revenue_trend.png`
- `charts/revenue_by_category.png`
- `charts/orders_by_payment_method.png`
- `charts/discount_vs_revenue.png`

## Important note

This is synthetic data. For a real project, replace the CSV with actual order data and document the source, time period and any cleaning decisions.
"""
    INSIGHTS_PATH.write_text(insights, encoding="utf-8")

    print("Analysis complete.")
    print(f"Tables saved to: {TABLE_DIR}")
    print(f"Charts saved to: {CHART_DIR}")
    print(f"Insights saved to: {INSIGHTS_PATH}")
    print(f"Best month: {best_month} | Top category: {top_category} | Top city: {top_city}")
    print(f"Discount vs revenue correlation: {discount_revenue_corr:.2f}")


if __name__ == "__main__":
    main()

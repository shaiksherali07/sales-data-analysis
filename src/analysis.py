"""
Sales Data Analysis Script
--------------------------
A beginner-friendly Python data analysis script using pandas, numpy, and matplotlib.
It loads sales data, performs basic cleaning, calculates key business metrics,
and creates visualization charts.
"""

from pathlib import Path
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Ensure standard output supports UTF-8 on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

# Define paths relative to the project root
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "sales_data.csv"
OUTPUT_DIR = BASE_DIR / "output"

# Ensure the output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    # -------------------------------------------------------------
    # Step 1 & 2: Load the dataset using Pandas
    # -------------------------------------------------------------
    print("=" * 55)
    print("            SALES DATA ANALYSIS REPORT             ")
    print("=" * 55)

    # pd.read_csv reads the CSV file into a Pandas DataFrame (table-like structure)
    df = pd.read_csv(DATA_PATH)
    print("\n[INFO] First 5 rows of the dataset:")
    print(df.head())

    # -------------------------------------------------------------
    # Step 3: Convert the 'Date' column to datetime format
    # -------------------------------------------------------------
    # pd.to_datetime converts string dates into datetime objects for date operations
    df["Date"] = pd.to_datetime(df["Date"])
    print(f"\n[INFO] 'Date' column converted to datetime: {df['Date'].dtype}")

    # -------------------------------------------------------------
    # Step 4: Check for missing values in the dataset
    # -------------------------------------------------------------
    # isnull().sum() checks each column and counts missing (NaN) values
    print("\n--- Missing Values Check ---")
    missing_values = df.isnull().sum()
    print(missing_values)

    # -------------------------------------------------------------
    # Step 5: Create a new 'Sales' column (Quantity * Price)
    # -------------------------------------------------------------
    # Element-wise multiplication between Quantity and Price columns
    df["Sales"] = df["Quantity"] * df["Price"]
    print("\n[INFO] 'Sales' column created (Quantity * Price).")

    # -------------------------------------------------------------
    # Step 6: Calculate Total Sales
    # -------------------------------------------------------------
    # sum() adds up all numbers in the 'Sales' column
    total_sales = df["Sales"].sum()

    # -------------------------------------------------------------
    # Step 7: Calculate Total Quantity Sold
    # -------------------------------------------------------------
    # sum() adds up all numbers in the 'Quantity' column
    total_quantity = df["Quantity"].sum()

    # -------------------------------------------------------------
    # Step 8: Calculate Product-wise Sales using groupby
    # -------------------------------------------------------------
    # groupby('Product') groups rows by each product, then sums the 'Sales'
    product_sales = df.groupby("Product")["Sales"].sum().sort_values(ascending=False)

    # -------------------------------------------------------------
    # Step 9: Calculate Region-wise Sales using groupby
    # -------------------------------------------------------------
    # groupby('Region') groups rows by each region, then sums the 'Sales'
    region_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)

    # -------------------------------------------------------------
    # Step 10: Calculate Monthly Sales
    # -------------------------------------------------------------
    # Extract Year-Month string (e.g., '2026-01') from the Date column
    df["Month"] = df["Date"].dt.strftime("%Y-%m")
    # Group by Month and sum up sales
    monthly_sales = df.groupby("Month")["Sales"].sum()

    # -------------------------------------------------------------
    # Step 11: Calculate Average Order Value (AOV)
    # -------------------------------------------------------------
    # We can use np.mean() to compute the average sales per transaction
    avg_order_value = np.mean(df["Sales"])

    # -------------------------------------------------------------
    # Step 14: Print Summary Results Clearly in the Terminal
    # -------------------------------------------------------------
    print("\n" + "=" * 55)
    print("                  KEY BUSINESS METRICS                 ")
    print("=" * 55)
    print(f"Total Sales Revenue    : INR {total_sales:,.2f}")
    print(f"Total Quantity Sold    : {total_quantity:,} units")
    print(f"Total Orders Placed    : {len(df)}")
    print(f"Average Order Value    : INR {avg_order_value:,.2f}")

    print("\n--- Product-wise Sales ---")
    for product, sales in product_sales.items():
        print(f"  {product:<15} : INR {sales:,.2f}")

    print("\n--- Region-wise Sales ---")
    for region, sales in region_sales.items():
        print(f"  {region:<15} : INR {sales:,.2f}")

    print("\n--- Monthly Sales Trend ---")
    for month, sales in monthly_sales.items():
        print(f"  {month:<15} : INR {sales:,.2f}")

    # -------------------------------------------------------------
    # Step 12 & 13: Create and Save 3 Charts inside output/
    # -------------------------------------------------------------
    print("\n" + "=" * 55)
    print("                 GENERATING CHARTS                     ")
    print("=" * 55)

    # Chart 1: Sales by Product (Bar Chart)
    plt.figure(figsize=(8, 5))
    bars = plt.bar(product_sales.index, product_sales.values, color="royalblue", edgecolor="black")
    plt.title("Total Sales by Product", fontsize=14, fontweight="bold")
    plt.xlabel("Product", fontsize=11)
    plt.ylabel("Sales (INR)", fontsize=11)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Add numeric labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 5000,
            f"{height:,.0f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    plt.tight_layout()
    chart1_path = OUTPUT_DIR / "sales_by_product.png"
    plt.savefig(chart1_path, dpi=300)
    plt.close()
    print(f"[SAVED] Chart 1 saved to: {chart1_path}")

    # Chart 2: Monthly Sales Trend (Line Chart)
    plt.figure(figsize=(8, 5))
    plt.plot(
        monthly_sales.index,
        monthly_sales.values,
        marker="o",
        color="forestgreen",
        linewidth=2.5,
        markersize=7,
        label="Monthly Revenue",
    )
    plt.title("Monthly Sales Trend (2026)", fontsize=14, fontweight="bold")
    plt.xlabel("Month", fontsize=11)
    plt.ylabel("Sales (INR)", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.7)

    # Add numeric labels next to each point
    for x, y in zip(monthly_sales.index, monthly_sales.values):
        plt.text(x, y + 4000, f"{y:,.0f}", ha="center", va="bottom", fontsize=9)

    plt.legend()
    plt.tight_layout()
    chart2_path = OUTPUT_DIR / "monthly_sales_trend.png"
    plt.savefig(chart2_path, dpi=300)
    plt.close()
    print(f"[SAVED] Chart 2 saved to: {chart2_path}")

    # Chart 3: Sales by Region (Bar Chart)
    plt.figure(figsize=(8, 5))
    region_bars = plt.bar(
        region_sales.index,
        region_sales.values,
        color="coral",
        edgecolor="black",
    )
    plt.title("Total Sales by Region", fontsize=14, fontweight="bold")
    plt.xlabel("Region", fontsize=11)
    plt.ylabel("Sales (INR)", fontsize=11)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Add numeric labels on top of each bar
    for bar in region_bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 4000,
            f"{height:,.0f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    plt.tight_layout()
    chart3_path = OUTPUT_DIR / "sales_by_region.png"
    plt.savefig(chart3_path, dpi=300)
    plt.close()
    print(f"[SAVED] Chart 3 saved to: {chart3_path}")

    print("\n[SUCCESS] Analysis complete! All charts saved in the output folder.")


if __name__ == "__main__":
    main()

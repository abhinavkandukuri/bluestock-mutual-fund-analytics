from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# TASK 13.1: PORTFOLIO CONCENTRATION ANALYSIS
# ============================================================

PROJECT_FOLDER = Path(__file__).parent
PROCESSED_DATA = PROJECT_FOLDER / "data" / "processed"
DASHBOARD_FOLDER = PROJECT_FOLDER / "dashboard"

DASHBOARD_FOLDER.mkdir(exist_ok=True)

# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(
    PROCESSED_DATA / "portfolio_analysis_ready.csv"
)

print("=" * 70)
print("TASK 13.1: PORTFOLIO CONCENTRATION ANALYSIS")
print("=" * 70)

print("\nDataset shape:")
print(df.shape)

print("\nAvailable columns:")
print(df.columns.tolist())


# ============================================================
# 1. SECTOR ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("SECTOR-WISE PORTFOLIO EXPOSURE")
print("=" * 70)

sector_summary = (
    df.groupby("sector")
    .agg(
        number_of_holdings=("stock_symbol", "count"),
        unique_stocks=("stock_symbol", "nunique"),
        total_weight_pct=("weight_pct", "sum"),
        average_weight_pct=("weight_pct", "mean")
    )
    .sort_values(
        "total_weight_pct",
        ascending=False
    )
    .reset_index()
)

print(
    sector_summary.to_string(index=False)
)

sector_summary.to_csv(
    PROCESSED_DATA / "portfolio_sector_summary.csv",
    index=False
)


# ============================================================
# 2. TOP 15 STOCKS BY AGGREGATE WEIGHT
# ============================================================

print("\n" + "=" * 70)
print("TOP 15 STOCKS BY AGGREGATE PORTFOLIO WEIGHT")
print("=" * 70)

stock_summary = (
    df.groupby("stock_symbol")
    .agg(
        stock_name=("stock_name", "first"),
        number_of_holdings=("stock_symbol", "count"),
        number_of_funds=("amfi_code", "nunique"),
        total_weight_pct=("weight_pct", "sum"),
        average_weight_pct=("weight_pct", "mean")
    )
    .sort_values(
        "total_weight_pct",
        ascending=False
    )
    .reset_index()
)

print(
    stock_summary.head(15).to_string(index=False)
)

stock_summary.to_csv(
    PROCESSED_DATA / "portfolio_stock_summary.csv",
    index=False
)


# ============================================================
# 3. TOP STOCKS BY NUMBER OF FUNDS
# ============================================================

print("\n" + "=" * 70)
print("TOP STOCKS HELD BY MOST FUNDS")
print("=" * 70)

most_held = (
    stock_summary
    .sort_values(
        ["number_of_funds", "total_weight_pct"],
        ascending=[False, False]
    )
    .head(15)
)

print(
    most_held.to_string(index=False)
)

most_held.to_csv(
    PROCESSED_DATA / "most_held_stocks.csv",
    index=False
)


# ============================================================
# 4. SECTOR CONCENTRATION
# ============================================================

print("\n" + "=" * 70)
print("TOP 5 SECTOR CONCENTRATION")
print("=" * 70)

top_5_sector_weight = (
    sector_summary
    .head(5)["total_weight_pct"]
    .sum()
)

total_sector_weight = (
    sector_summary["total_weight_pct"].sum()
)

top_5_sector_share = (
    top_5_sector_weight
    / total_sector_weight
    * 100
)

print(
    f"Top 5 sectors account for "
    f"{top_5_sector_share:.2f}% of aggregate portfolio weight."
)


# ============================================================
# 5. TOP AGGREGATE STOCK
# ============================================================

print("\n" + "=" * 70)
print("TOP AGGREGATE STOCK HOLDING")
print("=" * 70)

top_stock = stock_summary.iloc[0]

print(
    "Stock Symbol:",
    top_stock["stock_symbol"]
)

print(
    "Stock Name:",
    top_stock["stock_name"]
)

print(
    "Total aggregate weight:",
    round(top_stock["total_weight_pct"], 2),
    "%"
)

print(
    "Number of funds:",
    int(top_stock["number_of_funds"])
)


# ============================================================
# 6. SECTOR DIVERSIFICATION
# ============================================================

print("\n" + "=" * 70)
print("SECTOR DIVERSIFICATION")
print("=" * 70)

print(
    "Number of sectors:",
    df["sector"].nunique()
)

print(
    "Number of stocks:",
    df["stock_symbol"].nunique()
)

print(
    "Number of funds:",
    df["amfi_code"].nunique()
)


# ============================================================
# CHART 1 — SECTOR EXPOSURE
# ============================================================

chart_sector = sector_summary.sort_values(
    "total_weight_pct",
    ascending=True
)

plt.figure(figsize=(10, 8))

plt.barh(
    chart_sector["sector"],
    chart_sector["total_weight_pct"]
)

plt.xlabel("Aggregate Portfolio Weight (%)")
plt.ylabel("Sector")
plt.title("Sector-wise Portfolio Exposure")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "sector_portfolio_exposure.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 2 — TOP STOCKS
# ============================================================

chart_stock = (
    stock_summary
    .head(15)
    .sort_values(
        "total_weight_pct",
        ascending=True
    )
)

plt.figure(figsize=(10, 8))

plt.barh(
    chart_stock["stock_symbol"],
    chart_stock["total_weight_pct"]
)

plt.xlabel("Aggregate Portfolio Weight (%)")
plt.ylabel("Stock")
plt.title("Top 15 Stocks by Aggregate Portfolio Weight")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "top_15_portfolio_stocks.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 3 — MOST WIDELY HELD STOCKS
# ============================================================

chart_held = most_held.sort_values(
    "number_of_funds",
    ascending=True
)

plt.figure(figsize=(10, 8))

plt.barh(
    chart_held["stock_symbol"],
    chart_held["number_of_funds"]
)

plt.xlabel("Number of Funds Holding Stock")
plt.ylabel("Stock")
plt.title("Stocks Held Across the Most Mutual Funds")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "most_held_stocks.png",
    dpi=300
)

plt.show()


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 70)
print("TASK 13.1 COMPLETED")
print("=" * 70)

print("\nCSV files saved:")
print("- portfolio_sector_summary.csv")
print("- portfolio_stock_summary.csv")
print("- most_held_stocks.csv")

print("\nCharts saved:")
print("- sector_portfolio_exposure.png")
print("- top_15_portfolio_stocks.png")
print("- most_held_stocks.png")
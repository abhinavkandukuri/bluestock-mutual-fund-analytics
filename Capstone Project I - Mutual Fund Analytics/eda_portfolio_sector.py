from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# TASK 10.4: PORTFOLIO & SECTOR EDA
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
print("TASK 10.4: PORTFOLIO & SECTOR EDA")
print("=" * 70)

print("\nDataset shape:")
print(df.shape)


# ============================================================
# 1. SECTOR-WISE PORTFOLIO WEIGHT
# ============================================================

print("\n" + "=" * 70)
print("SECTOR-WISE PORTFOLIO WEIGHT")
print("=" * 70)

sector_weight = (
    df.groupby("sector")["weight_pct"]
    .sum()
    .sort_values(ascending=False)
)

print(sector_weight)


sector_weight.reset_index().to_csv(
    PROCESSED_DATA / "sector_weight_analysis.csv",
    index=False
)


# ============================================================
# 2. TOP 10 STOCKS BY WEIGHT
# ============================================================

print("\n" + "=" * 70)
print("TOP 10 STOCKS BY PORTFOLIO WEIGHT")
print("=" * 70)

stock_weight = (
    df.groupby(
        ["stock_symbol", "stock_name"]
    )["weight_pct"]
    .sum()
    .sort_values(ascending=False)
)

top_10_stocks = stock_weight.head(10)

print(top_10_stocks)


top_10_stocks.reset_index().to_csv(
    PROCESSED_DATA / "top_10_stocks_by_weight.csv",
    index=False
)


# ============================================================
# 3. SECTOR-WISE MARKET VALUE
# ============================================================

print("\n" + "=" * 70)
print("SECTOR-WISE MARKET VALUE")
print("=" * 70)

sector_market_value = (
    df.groupby("sector")["market_value_cr"]
    .sum()
    .sort_values(ascending=False)
)

print(sector_market_value)


sector_market_value.reset_index().to_csv(
    PROCESSED_DATA / "sector_market_value_analysis.csv",
    index=False
)


# ============================================================
# 4. TOP 10 STOCKS BY MARKET VALUE
# ============================================================

print("\n" + "=" * 70)
print("TOP 10 STOCKS BY MARKET VALUE")
print("=" * 70)

stock_market_value = (
    df.groupby(
        ["stock_symbol", "stock_name"]
    )["market_value_cr"]
    .sum()
    .sort_values(ascending=False)
)

top_10_market_value = stock_market_value.head(10)

print(top_10_market_value)


top_10_market_value.reset_index().to_csv(
    PROCESSED_DATA / "top_10_stocks_by_market_value.csv",
    index=False
)


# ============================================================
# 5. NUMBER OF STOCKS BY SECTOR
# ============================================================

print("\n" + "=" * 70)
print("NUMBER OF UNIQUE STOCKS BY SECTOR")
print("=" * 70)

stocks_by_sector = (
    df.groupby("sector")["stock_symbol"]
    .nunique()
    .sort_values(ascending=False)
)

print(stocks_by_sector)


stocks_by_sector.reset_index(
    name="unique_stock_count"
).to_csv(
    PROCESSED_DATA / "stocks_by_sector_analysis.csv",
    index=False
)


# ============================================================
# CHART 1: SECTOR-WISE PORTFOLIO WEIGHT
# ============================================================

chart_sector = sector_weight.sort_values(
    ascending=True
)

plt.figure(figsize=(10, 7))

plt.barh(
    chart_sector.index,
    chart_sector.values
)

plt.xlabel("Total Portfolio Weight (%)")
plt.ylabel("Sector")
plt.title("Sector-wise Portfolio Weight")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "sector_wise_portfolio_weight.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 2: TOP 10 STOCKS BY WEIGHT
# ============================================================

chart_stocks = top_10_stocks.sort_values(
    ascending=True
)

stock_labels = [
    symbol for symbol, name in chart_stocks.index
]

plt.figure(figsize=(10, 7))

plt.barh(
    stock_labels,
    chart_stocks.values
)

plt.xlabel("Total Portfolio Weight (%)")
plt.ylabel("Stock")
plt.title("Top 10 Stocks by Portfolio Weight")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "top_10_stocks_by_weight.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 3: SECTOR-WISE MARKET VALUE
# ============================================================

chart_market = sector_market_value.sort_values(
    ascending=True
)

plt.figure(figsize=(10, 7))

plt.barh(
    chart_market.index,
    chart_market.values
)

plt.xlabel("Market Value (₹ Crore)")
plt.ylabel("Sector")
plt.title("Sector-wise Portfolio Market Value")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "sector_market_value.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 4: TOP 10 STOCKS BY MARKET VALUE
# ============================================================

chart_market_stocks = top_10_market_value.sort_values(
    ascending=True
)

stock_market_labels = [
    symbol for symbol, name in chart_market_stocks.index
]

plt.figure(figsize=(10, 7))

plt.barh(
    stock_market_labels,
    chart_market_stocks.values
)

plt.xlabel("Market Value (₹ Crore)")
plt.ylabel("Stock")
plt.title("Top 10 Stocks by Market Value")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "top_10_stocks_by_market_value.png",
    dpi=300
)

plt.show()


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 70)
print("TASK 10.4 COMPLETED")
print("=" * 70)

print("\nCSV files saved:")
print("- sector_weight_analysis.csv")
print("- top_10_stocks_by_weight.csv")
print("- sector_market_value_analysis.csv")
print("- top_10_stocks_by_market_value.csv")
print("- stocks_by_sector_analysis.csv")

print("\nCharts saved in dashboard folder:")
print("- sector_wise_portfolio_weight.png")
print("- top_10_stocks_by_weight.png")
print("- sector_market_value.png")
print("- top_10_stocks_by_market_value.png")
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# TASK 13.2: FUND-LEVEL PORTFOLIO ANALYSIS
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
print("TASK 13.2: FUND-LEVEL PORTFOLIO ANALYSIS")
print("=" * 70)

print("\nDataset shape:")
print(df.shape)

# ============================================================
# 1. NUMBER OF STOCKS PER FUND
# ============================================================

fund_summary = (
    df.groupby("amfi_code")
    .agg(
        number_of_stocks=("stock_symbol", "nunique"),
        total_portfolio_weight=("weight_pct", "sum"),
        average_holding_weight=("weight_pct", "mean")
    )
    .reset_index()
)

print("\n" + "=" * 70)
print("FUND-LEVEL DIVERSIFICATION")
print("=" * 70)

print(
    fund_summary.sort_values(
        "number_of_stocks",
        ascending=False
    ).to_string(index=False)
)

fund_summary.to_csv(
    PROCESSED_DATA / "fund_level_diversification.csv",
    index=False
)


# ============================================================
# 2. TOP HOLDING FOR EACH FUND
# ============================================================

print("\n" + "=" * 70)
print("TOP HOLDING FOR EACH FUND")
print("=" * 70)

top_holdings = (
    df.sort_values(
        ["amfi_code", "weight_pct"],
        ascending=[True, False]
    )
    .groupby("amfi_code")
    .first()
    .reset_index()
)

top_holdings = top_holdings[
    [
        "amfi_code",
        "stock_symbol",
        "stock_name",
        "sector",
        "weight_pct"
    ]
]

print(
    top_holdings.to_string(index=False)
)

top_holdings.to_csv(
    PROCESSED_DATA / "top_holding_each_fund.csv",
    index=False
)


# ============================================================
# 3. DOMINANT SECTOR FOR EACH FUND
# ============================================================

sector_by_fund = (
    df.groupby(
        ["amfi_code", "sector"]
    )["weight_pct"]
    .sum()
    .reset_index()
)

dominant_sector = (
    sector_by_fund
    .sort_values(
        ["amfi_code", "weight_pct"],
        ascending=[True, False]
    )
    .groupby("amfi_code")
    .first()
    .reset_index()
)

dominant_sector = dominant_sector.rename(
    columns={
        "weight_pct": "dominant_sector_weight_pct"
    }
)

print("\n" + "=" * 70)
print("DOMINANT SECTOR FOR EACH FUND")
print("=" * 70)

print(
    dominant_sector.to_string(index=False)
)

dominant_sector.to_csv(
    PROCESSED_DATA / "dominant_sector_each_fund.csv",
    index=False
)


# ============================================================
# 4. MERGE FUND DIVERSIFICATION + DOMINANT SECTOR
# ============================================================

fund_portfolio_profile = fund_summary.merge(
    dominant_sector[
        [
            "amfi_code",
            "sector",
            "dominant_sector_weight_pct"
        ]
    ],
    on="amfi_code",
    how="left"
)

fund_portfolio_profile = fund_portfolio_profile.merge(
    top_holdings[
        [
            "amfi_code",
            "stock_symbol",
            "stock_name",
            "weight_pct"
        ]
    ],
    on="amfi_code",
    how="left"
)

fund_portfolio_profile = fund_portfolio_profile.rename(
    columns={
        "sector": "dominant_sector",
        "stock_symbol": "top_stock_symbol",
        "stock_name": "top_stock_name",
        "weight_pct": "top_stock_weight_pct"
    }
)

print("\n" + "=" * 70)
print("COMPLETE FUND PORTFOLIO PROFILE")
print("=" * 70)

print(
    fund_portfolio_profile.to_string(index=False)
)

fund_portfolio_profile.to_csv(
    PROCESSED_DATA / "fund_portfolio_profile.csv",
    index=False
)


# ============================================================
# 5. MOST DIVERSIFIED FUNDS
# ============================================================

print("\n" + "=" * 70)
print("MOST DIVERSIFIED FUNDS")
print("=" * 70)

most_diversified = (
    fund_summary
    .sort_values(
        "number_of_stocks",
        ascending=False
    )
    .head(10)
)

print(
    most_diversified.to_string(index=False)
)

most_diversified.to_csv(
    PROCESSED_DATA / "most_diversified_funds.csv",
    index=False
)


# ============================================================
# 6. MOST CONCENTRATED FUNDS
# ============================================================

print("\n" + "=" * 70)
print("MOST CONCENTRATED FUNDS — TOP HOLDING")
print("=" * 70)

most_concentrated = (
    top_holdings
    .sort_values(
        "weight_pct",
        ascending=False
    )
    .head(10)
)

print(
    most_concentrated.to_string(index=False)
)

most_concentrated.to_csv(
    PROCESSED_DATA / "most_concentrated_funds.csv",
    index=False
)


# ============================================================
# CHART 1 — NUMBER OF STOCKS PER FUND
# ============================================================

chart_diversification = fund_summary.sort_values(
    "number_of_stocks",
    ascending=True
)

plt.figure(figsize=(10, 8))

plt.barh(
    chart_diversification["amfi_code"].astype(str),
    chart_diversification["number_of_stocks"]
)

plt.xlabel("Number of Stocks")
plt.ylabel("AMFI Code")
plt.title("Fund-level Portfolio Diversification")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "fund_diversification.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 2 — TOP HOLDING WEIGHT
# ============================================================

chart_concentration = most_concentrated.sort_values(
    "weight_pct",
    ascending=True
)

plt.figure(figsize=(10, 7))

plt.barh(
    chart_concentration["amfi_code"].astype(str),
    chart_concentration["weight_pct"]
)

plt.xlabel("Top Holding Weight (%)")
plt.ylabel("AMFI Code")
plt.title("Most Concentrated Funds by Top Holding")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "fund_top_holding_concentration.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 3 — DOMINANT SECTOR
# ============================================================

dominant_sector_counts = (
    dominant_sector["sector"]
    .value_counts()
    .sort_values()
)

plt.figure(figsize=(9, 6))

plt.barh(
    dominant_sector_counts.index,
    dominant_sector_counts.values
)

plt.xlabel("Number of Funds")
plt.ylabel("Dominant Sector")
plt.title("Most Common Dominant Sectors Across Funds")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "dominant_sector_across_funds.png",
    dpi=300
)

plt.show()


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 70)
print("TASK 13.2 COMPLETED")
print("=" * 70)

print("\nCSV files saved:")
print("- fund_level_diversification.csv")
print("- top_holding_each_fund.csv")
print("- dominant_sector_each_fund.csv")
print("- fund_portfolio_profile.csv")
print("- most_diversified_funds.csv")
print("- most_concentrated_funds.csv")

print("\nCharts saved:")
print("- fund_diversification.png")
print("- fund_top_holding_concentration.png")
print("- dominant_sector_across_funds.png")
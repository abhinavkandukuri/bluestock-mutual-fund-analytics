from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# TASK 10.5: NAV & RETURN TREND EDA
# ============================================================

PROJECT_FOLDER = Path(__file__).parent
PROCESSED_DATA = PROJECT_FOLDER / "data" / "processed"
DASHBOARD_FOLDER = PROJECT_FOLDER / "dashboard"

DASHBOARD_FOLDER.mkdir(exist_ok=True)

# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(
    PROCESSED_DATA / "nav_analysis_ready.csv"
)

df["date"] = pd.to_datetime(df["date"])

print("=" * 70)
print("TASK 10.5: NAV & RETURN TREND EDA")
print("=" * 70)

print("\nDataset shape:")
print(df.shape)

print("\nDate range:")
print(df["date"].min(), "to", df["date"].max())


# ============================================================
# 1. NAV SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("NAV SUMMARY")
print("=" * 70)

nav_summary = (
    df.groupby("amfi_code")
    .agg(
        starting_nav=("nav", "first"),
        latest_nav=("nav", "last"),
        minimum_nav=("nav", "min"),
        maximum_nav=("nav", "max"),
        cumulative_return_pct=("cumulative_return_pct", "last")
    )
    .reset_index()
)

print(nav_summary.head(10).to_string(index=False))

nav_summary.to_csv(
    PROCESSED_DATA / "nav_summary_analysis.csv",
    index=False
)


# ============================================================
# 2. TOP 10 FUNDS BY CUMULATIVE RETURN
# ============================================================

print("\n" + "=" * 70)
print("TOP 10 FUNDS BY CUMULATIVE RETURN")
print("=" * 70)

top_cumulative = (
    nav_summary
    .sort_values(
        "cumulative_return_pct",
        ascending=False
    )
    .head(10)
)

print(top_cumulative.to_string(index=False))

top_cumulative.to_csv(
    PROCESSED_DATA / "top_10_cumulative_return.csv",
    index=False
)


# ============================================================
# 3. DAILY RETURN STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("DAILY RETURN STATISTICS")
print("=" * 70)

daily_return_stats = (
    df["daily_return_pct"]
    .dropna()
    .describe()
)

print(daily_return_stats)

daily_return_stats.to_csv(
    PROCESSED_DATA / "daily_return_statistics.csv"
)


# ============================================================
# 4. FUND VOLATILITY
# ============================================================

print("\n" + "=" * 70)
print("TOP 10 FUNDS BY DAILY RETURN VOLATILITY")
print("=" * 70)

fund_volatility = (
    df.groupby("amfi_code")["daily_return_pct"]
    .std()
    .sort_values(ascending=False)
    .head(10)
)

print(fund_volatility)

fund_volatility.reset_index(
    name="daily_return_volatility"
).to_csv(
    PROCESSED_DATA / "fund_volatility_analysis.csv",
    index=False
)


# ============================================================
# CHART 1: NAV TREND FOR TOP FUND
# ============================================================

top_fund_code = top_cumulative.iloc[0]["amfi_code"]

top_fund_nav = df[
    df["amfi_code"] == top_fund_code
].sort_values("date")

plt.figure(figsize=(12, 6))

plt.plot(
    top_fund_nav["date"],
    top_fund_nav["nav"]
)

plt.xlabel("Date")
plt.ylabel("NAV")
plt.title(
    f"NAV Trend — AMFI Code {int(top_fund_code)}"
)

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "nav_trend_top_fund.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 2: DAILY RETURN DISTRIBUTION
# ============================================================

plt.figure(figsize=(10, 6))

plt.hist(
    df["daily_return_pct"].dropna(),
    bins=50
)

plt.xlabel("Daily Return (%)")
plt.ylabel("Frequency")
plt.title("Distribution of Daily Mutual Fund Returns")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "daily_return_distribution.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 3: TOP 10 CUMULATIVE RETURNS
# ============================================================

chart_cumulative = top_cumulative.sort_values(
    "cumulative_return_pct",
    ascending=True
)

plt.figure(figsize=(10, 6))

plt.barh(
    chart_cumulative["amfi_code"].astype(str),
    chart_cumulative["cumulative_return_pct"]
)

plt.xlabel("Cumulative Return (%)")
plt.ylabel("AMFI Code")
plt.title("Top 10 Funds by Cumulative Return")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "top_10_cumulative_returns.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 4: FUND VOLATILITY
# ============================================================

chart_volatility = fund_volatility.sort_values(
    ascending=True
)

plt.figure(figsize=(10, 6))

plt.barh(
    chart_volatility.index.astype(str),
    chart_volatility.values
)

plt.xlabel("Daily Return Standard Deviation (%)")
plt.ylabel("AMFI Code")
plt.title("Top 10 Funds by Daily Return Volatility")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "fund_volatility.png",
    dpi=300
)

plt.show()


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 70)
print("TASK 10.5 COMPLETED")
print("=" * 70)

print("\nCSV files saved:")
print("- nav_summary_analysis.csv")
print("- top_10_cumulative_return.csv")
print("- daily_return_statistics.csv")
print("- fund_volatility_analysis.csv")

print("\nCharts saved in dashboard folder:")
print("- nav_trend_top_fund.png")
print("- daily_return_distribution.png")
print("- top_10_cumulative_returns.png")
print("- fund_volatility.png")
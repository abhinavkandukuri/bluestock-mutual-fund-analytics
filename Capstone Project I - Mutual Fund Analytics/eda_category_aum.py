from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# TASK 10.3: CATEGORY & AUM EDA
# ============================================================

PROJECT_FOLDER = Path(__file__).parent
PROCESSED_DATA = PROJECT_FOLDER / "data" / "processed"
DASHBOARD_FOLDER = PROJECT_FOLDER / "dashboard"

DASHBOARD_FOLDER.mkdir(exist_ok=True)

# ============================================================
# LOAD DATA
# ============================================================

category_df = pd.read_csv(
    PROCESSED_DATA / "category_inflow_analysis_ready.csv"
)

aum_df = pd.read_csv(
    PROCESSED_DATA / "aum_analysis_ready.csv"
)

print("=" * 70)
print("TASK 10.3: CATEGORY & AUM EDA")
print("=" * 70)

print("\nCategory inflow dataset shape:")
print(category_df.shape)

print("\nAUM dataset shape:")
print(aum_df.shape)


# ============================================================
# 1. CATEGORY-WISE TOTAL NET INFLOW
# ============================================================

print("\n" + "=" * 70)
print("CATEGORY-WISE TOTAL NET INFLOW")
print("=" * 70)

category_inflow = (
    category_df.groupby("category")["net_inflow_crore"]
    .sum()
    .sort_values(ascending=False)
)

print(category_inflow)


# Save
category_inflow.reset_index().to_csv(
    PROCESSED_DATA / "category_total_inflow_analysis.csv",
    index=False
)


# ============================================================
# 2. TOP 5 CATEGORIES
# ============================================================

print("\n" + "=" * 70)
print("TOP 5 CATEGORIES BY NET INFLOW")
print("=" * 70)

top_categories = category_inflow.head(5)

print(top_categories)


# ============================================================
# 3. MONTHLY CATEGORY INFLOW
# ============================================================

print("\n" + "=" * 70)
print("MONTHLY CATEGORY INFLOW")
print("=" * 70)

monthly_category = (
    category_df.groupby(
        ["year", "month_number", "month_name"]
    )["net_inflow_crore"]
    .sum()
    .reset_index()
)

monthly_category["year_month"] = (
    monthly_category["year"].astype(str)
    + "-"
    + monthly_category["month_number"]
      .astype(str)
      .str.zfill(2)
)

print(monthly_category.head(12).to_string(index=False))

monthly_category.to_csv(
    PROCESSED_DATA / "monthly_category_inflow_analysis.csv",
    index=False
)


# ============================================================
# 4. FUND HOUSE AUM
# ============================================================

print("\n" + "=" * 70)
print("TOTAL AUM BY FUND HOUSE")
print("=" * 70)

fund_house_aum = (
    aum_df.groupby("fund_house")["aum_crore"]
    .sum()
    .sort_values(ascending=False)
)

print(fund_house_aum)


fund_house_aum.reset_index().to_csv(
    PROCESSED_DATA / "fund_house_aum_analysis.csv",
    index=False
)


# ============================================================
# 5. AUM MARKET SHARE
# ============================================================

print("\n" + "=" * 70)
print("AUM MARKET SHARE BY FUND HOUSE")
print("=" * 70)

aum_share = (
    aum_df.groupby("fund_house")["aum_crore"]
    .sum()
)

aum_share_pct = (
    aum_share / aum_share.sum() * 100
).sort_values(ascending=False)

print(aum_share_pct)


aum_share_pct.reset_index(
    name="aum_share_pct"
).to_csv(
    PROCESSED_DATA / "aum_market_share_analysis.csv",
    index=False
)


# ============================================================
# 6. MONTHLY TOTAL AUM TREND
# ============================================================

print("\n" + "=" * 70)
print("MONTHLY TOTAL AUM TREND")
print("=" * 70)

monthly_aum = (
    aum_df.groupby("date")["aum_crore"]
    .sum()
    .reset_index()
)

monthly_aum["date"] = pd.to_datetime(
    monthly_aum["date"]
)

print(monthly_aum.to_string(index=False))

monthly_aum.to_csv(
    PROCESSED_DATA / "monthly_total_aum_analysis.csv",
    index=False
)


# ============================================================
# CHART 1: CATEGORY-WISE NET INFLOW
# ============================================================

chart_category = category_inflow.sort_values(
    ascending=True
)

plt.figure(figsize=(10, 7))

plt.barh(
    chart_category.index,
    chart_category.values
)

plt.xlabel("Total Net Inflow (₹ Crore)")
plt.ylabel("Category")
plt.title("Mutual Fund Category-wise Net Inflow")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "category_wise_net_inflow.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 2: TOP 5 CATEGORIES
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    top_categories.index,
    top_categories.values
)

plt.xlabel("Category")
plt.ylabel("Total Net Inflow (₹ Crore)")
plt.title("Top 5 Mutual Fund Categories by Net Inflow")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "top_5_categories_inflow.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 3: FUND HOUSE AUM
# ============================================================

chart_aum = fund_house_aum.sort_values(
    ascending=True
)

plt.figure(figsize=(10, 7))

plt.barh(
    chart_aum.index,
    chart_aum.values
)

plt.xlabel("Total AUM (₹ Crore)")
plt.ylabel("Fund House")
plt.title("Total AUM by Fund House")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "fund_house_aum.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 4: AUM MARKET SHARE
# ============================================================

plt.figure(figsize=(9, 6))

plt.bar(
    aum_share_pct.index,
    aum_share_pct.values
)

plt.xlabel("Fund House")
plt.ylabel("AUM Share (%)")
plt.title("Mutual Fund AUM Market Share")

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "aum_market_share.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 5: TOTAL AUM TREND
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    monthly_aum["date"],
    monthly_aum["aum_crore"],
    marker="o"
)

plt.xlabel("Date")
plt.ylabel("Total AUM (₹ Crore)")
plt.title("Total Mutual Fund AUM Trend")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "total_aum_trend.png",
    dpi=300
)

plt.show()


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 70)
print("TASK 10.3 COMPLETED")
print("=" * 70)

print("\nCSV files saved:")
print("- category_total_inflow_analysis.csv")
print("- monthly_category_inflow_analysis.csv")
print("- fund_house_aum_analysis.csv")
print("- aum_market_share_analysis.csv")
print("- monthly_total_aum_analysis.csv")

print("\nCharts saved in dashboard folder:")
print("- category_wise_net_inflow.png")
print("- top_5_categories_inflow.png")
print("- fund_house_aum.png")
print("- aum_market_share.png")
print("- total_aum_trend.png")
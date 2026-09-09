from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# TASK 10.2: INVESTOR & TRANSACTION EDA
# ============================================================

PROJECT_FOLDER = Path(__file__).parent
PROCESSED_DATA = PROJECT_FOLDER / "data" / "processed"
DASHBOARD_FOLDER = PROJECT_FOLDER / "dashboard"

DASHBOARD_FOLDER.mkdir(exist_ok=True)

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

df = pd.read_csv(
    PROCESSED_DATA / "transaction_analysis_ready.csv"
)

print("=" * 70)
print("TASK 10.2: INVESTOR & TRANSACTION EDA")
print("=" * 70)

print("\nDataset shape:")
print(df.shape)

print("\nAvailable columns:")
print(df.columns.tolist())


# ============================================================
# 1. TRANSACTION TYPE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("TRANSACTION TYPE ANALYSIS")
print("=" * 70)

transaction_type_count = (
    df["transaction_type"]
    .value_counts()
)

print("\nNumber of transactions:")
print(transaction_type_count)

transaction_type_amount = (
    df.groupby("transaction_type")["amount_lakh"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTotal transaction amount (₹ lakh):")
print(transaction_type_amount)


# Save summary
transaction_type_summary = pd.DataFrame({
    "transaction_count": transaction_type_count,
    "total_amount_lakh": transaction_type_amount
})

transaction_type_summary.to_csv(
    PROCESSED_DATA / "transaction_type_analysis.csv"
)


# ============================================================
# 2. CITY TIER ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("CITY TIER ANALYSIS")
print("=" * 70)

city_tier_count = (
    df["city_tier"]
    .value_counts()
)

city_tier_amount = (
    df.groupby("city_tier")["amount_lakh"]
    .sum()
    .sort_values(ascending=False)
)

print("\nNumber of transactions:")
print(city_tier_count)

print("\nTotal transaction amount (₹ lakh):")
print(city_tier_amount)


city_tier_summary = pd.DataFrame({
    "transaction_count": city_tier_count,
    "total_amount_lakh": city_tier_amount
})

city_tier_summary.to_csv(
    PROCESSED_DATA / "city_tier_analysis.csv"
)


# ============================================================
# 3. KYC STATUS ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("KYC STATUS ANALYSIS")
print("=" * 70)

kyc_count = (
    df["kyc_status"]
    .value_counts()
)

print("\nTransactions by KYC status:")
print(kyc_count)

kyc_percentage = (
    df["kyc_status"]
    .value_counts(normalize=True) * 100
)

print("\nKYC percentage:")
print(kyc_percentage)


kyc_summary = pd.DataFrame({
    "transaction_count": kyc_count,
    "percentage": kyc_percentage
})

kyc_summary.to_csv(
    PROCESSED_DATA / "kyc_analysis.csv"
)


# ============================================================
# 4. AGE GROUP ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("AGE GROUP ANALYSIS")
print("=" * 70)

age_group_count = (
    df["age_group"]
    .value_counts()
)

age_group_amount = (
    df.groupby("age_group")["amount_lakh"]
    .sum()
    .sort_values(ascending=False)
)

print("\nNumber of transactions:")
print(age_group_count)

print("\nTotal transaction amount (₹ lakh):")
print(age_group_amount)


age_group_summary = pd.DataFrame({
    "transaction_count": age_group_count,
    "total_amount_lakh": age_group_amount
})

age_group_summary.to_csv(
    PROCESSED_DATA / "age_group_analysis.csv"
)


# ============================================================
# 5. MONTHLY TRANSACTION TREND
# ============================================================

print("\n" + "=" * 70)
print("MONTHLY TRANSACTION TREND")
print("=" * 70)

monthly_transactions = (
    df.groupby(
        ["transaction_year", "transaction_month"]
    )
    .agg(
        transaction_count=("investor_id", "count"),
        total_amount_lakh=("amount_lakh", "sum")
    )
    .reset_index()
)

monthly_transactions["year_month"] = (
    monthly_transactions["transaction_year"].astype(str)
    + "-"
    + monthly_transactions["transaction_month"]
      .astype(str)
      .str.zfill(2)
)

print(
    monthly_transactions.head(12).to_string(index=False)
)

monthly_transactions.to_csv(
    PROCESSED_DATA / "monthly_transaction_analysis.csv",
    index=False
)


# ============================================================
# 6. TRANSACTION TYPE BY CITY TIER
# ============================================================

print("\n" + "=" * 70)
print("TRANSACTION TYPE BY CITY TIER")
print("=" * 70)

transaction_city = (
    df.groupby(
        ["city_tier", "transaction_type"]
    )
    .size()
    .unstack(fill_value=0)
)

print(transaction_city)

transaction_city.to_csv(
    PROCESSED_DATA / "transaction_type_by_city_tier.csv"
)


# ============================================================
# CHART 1: TRANSACTION TYPE DISTRIBUTION
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    transaction_type_count.index,
    transaction_type_count.values
)

plt.xlabel("Transaction Type")
plt.ylabel("Number of Transactions")
plt.title("Transaction Type Distribution")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "transaction_type_distribution.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 2: TRANSACTION AMOUNT BY TYPE
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    transaction_type_amount.index,
    transaction_type_amount.values
)

plt.xlabel("Transaction Type")
plt.ylabel("Total Amount (₹ Lakh)")
plt.title("Transaction Amount by Transaction Type")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "transaction_amount_by_type.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 3: T30 VS B30
# ============================================================

plt.figure(figsize=(7, 5))

plt.bar(
    city_tier_count.index,
    city_tier_count.values
)

plt.xlabel("City Tier")
plt.ylabel("Number of Transactions")
plt.title("Investor Transactions: T30 vs B30")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "t30_vs_b30_transactions.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 4: AGE GROUP DISTRIBUTION
# ============================================================

age_chart = age_group_count.sort_index()

plt.figure(figsize=(9, 5))

plt.bar(
    age_chart.index.astype(str),
    age_chart.values
)

plt.xlabel("Age Group")
plt.ylabel("Number of Transactions")
plt.title("Investor Transactions by Age Group")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "transactions_by_age_group.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 5: MONTHLY TRANSACTION TREND
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_transactions["year_month"],
    monthly_transactions["transaction_count"],
    marker="o"
)

plt.xlabel("Month")
plt.ylabel("Number of Transactions")
plt.title("Monthly Investor Transaction Trend")

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "monthly_transaction_trend.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 6: KYC STATUS
# ============================================================

plt.figure(figsize=(7, 5))

plt.bar(
    kyc_count.index,
    kyc_count.values
)

plt.xlabel("KYC Status")
plt.ylabel("Number of Transactions")
plt.title("Investor Transactions by KYC Status")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "kyc_status_analysis.png",
    dpi=300
)

plt.show()


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 70)
print("TASK 10.2 COMPLETED")
print("=" * 70)

print("\nCSV files saved:")
print("- transaction_type_analysis.csv")
print("- city_tier_analysis.csv")
print("- kyc_analysis.csv")
print("- age_group_analysis.csv")
print("- monthly_transaction_analysis.csv")
print("- transaction_type_by_city_tier.csv")

print("\nCharts saved in dashboard folder:")
print("- transaction_type_distribution.png")
print("- transaction_amount_by_type.png")
print("- t30_vs_b30_transactions.png")
print("- transactions_by_age_group.png")
print("- monthly_transaction_trend.png")
print("- kyc_status_analysis.png")
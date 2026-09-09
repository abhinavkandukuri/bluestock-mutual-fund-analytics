from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# TASK 12.3: REDEMPTION ANALYSIS
# ============================================================

PROJECT_FOLDER = Path(__file__).parent
PROCESSED_DATA = PROJECT_FOLDER / "data" / "processed"
DASHBOARD_FOLDER = PROJECT_FOLDER / "dashboard"

DASHBOARD_FOLDER.mkdir(exist_ok=True)

# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(
    PROCESSED_DATA / "transaction_analysis_ready.csv"
)

df["transaction_date"] = pd.to_datetime(
    df["transaction_date"]
)

# Keep only redemption transactions
redemption = df[
    df["transaction_type"] == "Redemption"
].copy()

print("=" * 70)
print("TASK 12.3: REDEMPTION ANALYSIS")
print("=" * 70)

print("\nRedemption dataset shape:")
print(redemption.shape)


# ============================================================
# 1. REDEMPTION SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("REDEMPTION SUMMARY")
print("=" * 70)

print("\nTotal redemption transactions:")
print(len(redemption))

print("\nTotal redemption amount (₹ Lakh):")
print(redemption["amount_lakh"].sum())

print("\nAverage redemption amount (₹ Lakh):")
print(redemption["amount_lakh"].mean())

print("\nMedian redemption amount (₹ Lakh):")
print(redemption["amount_lakh"].median())


# ============================================================
# 2. MONTHLY REDEMPTION ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("MONTHLY REDEMPTION ANALYSIS")
print("=" * 70)

monthly_redemption = (
    redemption.groupby(
        ["transaction_year", "transaction_month"]
    )
    .agg(
        redemption_count=("investor_id", "count"),
        total_redemption_amount_lakh=("amount_lakh", "sum"),
        average_redemption_amount_lakh=("amount_lakh", "mean")
    )
    .reset_index()
)

monthly_redemption["year_month"] = (
    monthly_redemption["transaction_year"].astype(str)
    + "-"
    + monthly_redemption["transaction_month"]
      .astype(str)
      .str.zfill(2)
)

print(
    monthly_redemption.head(12).to_string(index=False)
)

monthly_redemption.to_csv(
    PROCESSED_DATA / "monthly_redemption_analysis.csv",
    index=False
)


# ============================================================
# 3. REDEMPTION BY CITY TIER
# ============================================================

print("\n" + "=" * 70)
print("REDEMPTION BY CITY TIER")
print("=" * 70)

redemption_city = (
    redemption.groupby("city_tier")
    .agg(
        redemption_count=("investor_id", "count"),
        total_redemption_amount_lakh=("amount_lakh", "sum"),
        average_redemption_amount_lakh=("amount_lakh", "mean")
    )
    .sort_values(
        "total_redemption_amount_lakh",
        ascending=False
    )
    .reset_index()
)

print(
    redemption_city.to_string(index=False)
)

redemption_city.to_csv(
    PROCESSED_DATA / "redemption_city_tier_analysis.csv",
    index=False
)


# ============================================================
# 4. REDEMPTION BY AGE GROUP
# ============================================================

print("\n" + "=" * 70)
print("REDEMPTION BY AGE GROUP")
print("=" * 70)

redemption_age = (
    redemption.groupby("age_group")
    .agg(
        redemption_count=("investor_id", "count"),
        total_redemption_amount_lakh=("amount_lakh", "sum"),
        average_redemption_amount_lakh=("amount_lakh", "mean")
    )
    .sort_values(
        "total_redemption_amount_lakh",
        ascending=False
    )
    .reset_index()
)

print(
    redemption_age.to_string(index=False)
)

redemption_age.to_csv(
    PROCESSED_DATA / "redemption_age_group_analysis.csv",
    index=False
)


# ============================================================
# 5. TOP STATES BY REDEMPTION
# ============================================================

print("\n" + "=" * 70)
print("TOP 10 STATES BY REDEMPTION AMOUNT")
print("=" * 70)

redemption_state = (
    redemption.groupby("state")
    .agg(
        redemption_count=("investor_id", "count"),
        total_redemption_amount_lakh=("amount_lakh", "sum")
    )
    .sort_values(
        "total_redemption_amount_lakh",
        ascending=False
    )
    .head(10)
    .reset_index()
)

print(
    redemption_state.to_string(index=False)
)

redemption_state.to_csv(
    PROCESSED_DATA / "top_10_redemption_states.csv",
    index=False
)


# ============================================================
# 6. REDEMPTION BY PAYMENT MODE
# ============================================================

print("\n" + "=" * 70)
print("REDEMPTION BY PAYMENT MODE")
print("=" * 70)

redemption_payment = (
    redemption.groupby("payment_mode")
    .agg(
        redemption_count=("investor_id", "count"),
        total_redemption_amount_lakh=("amount_lakh", "sum")
    )
    .sort_values(
        "redemption_count",
        ascending=False
    )
    .reset_index()
)

print(
    redemption_payment.to_string(index=False)
)

redemption_payment.to_csv(
    PROCESSED_DATA / "redemption_payment_mode_analysis.csv",
    index=False
)


# ============================================================
# 7. REDEMPTION BY KYC STATUS
# ============================================================

print("\n" + "=" * 70)
print("REDEMPTION BY KYC STATUS")
print("=" * 70)

redemption_kyc = (
    redemption.groupby("kyc_status")
    .agg(
        redemption_count=("investor_id", "count"),
        total_redemption_amount_lakh=("amount_lakh", "sum")
    )
    .sort_values(
        "total_redemption_amount_lakh",
        ascending=False
    )
    .reset_index()
)

print(
    redemption_kyc.to_string(index=False)
)

redemption_kyc.to_csv(
    PROCESSED_DATA / "redemption_kyc_analysis.csv",
    index=False
)


# ============================================================
# CHART 1 — MONTHLY REDEMPTION COUNT
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_redemption["year_month"],
    monthly_redemption["redemption_count"],
    marker="o"
)

plt.xlabel("Month")
plt.ylabel("Number of Redemptions")
plt.title("Monthly Redemption Transaction Trend")

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "monthly_redemption_count.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 2 — MONTHLY REDEMPTION AMOUNT
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_redemption["year_month"],
    monthly_redemption["total_redemption_amount_lakh"],
    marker="o"
)

plt.xlabel("Month")
plt.ylabel("Redemption Amount (₹ Lakh)")
plt.title("Monthly Redemption Amount Trend")

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "monthly_redemption_amount.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 3 — REDEMPTION BY CITY TIER
# ============================================================

plt.figure(figsize=(7, 5))

plt.bar(
    redemption_city["city_tier"],
    redemption_city["total_redemption_amount_lakh"]
)

plt.xlabel("City Tier")
plt.ylabel("Redemption Amount (₹ Lakh)")
plt.title("Redemption Amount — T30 vs B30")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "redemption_t30_b30.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 4 — REDEMPTION BY AGE GROUP
# ============================================================

plt.figure(figsize=(9, 5))

plt.bar(
    redemption_age["age_group"].astype(str),
    redemption_age["total_redemption_amount_lakh"]
)

plt.xlabel("Age Group")
plt.ylabel("Redemption Amount (₹ Lakh)")
plt.title("Redemption Amount by Age Group")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "redemption_by_age_group.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 5 — TOP STATES
# ============================================================

state_chart = redemption_state.sort_values(
    "total_redemption_amount_lakh",
    ascending=True
)

plt.figure(figsize=(9, 6))

plt.barh(
    state_chart["state"],
    state_chart["total_redemption_amount_lakh"]
)

plt.xlabel("Redemption Amount (₹ Lakh)")
plt.ylabel("State")
plt.title("Top 10 States by Redemption Amount")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "top_10_redemption_states.png",
    dpi=300
)

plt.show()


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 70)
print("TASK 12.3 COMPLETED")
print("=" * 70)

print("\nCSV files saved:")
print("- monthly_redemption_analysis.csv")
print("- redemption_city_tier_analysis.csv")
print("- redemption_age_group_analysis.csv")
print("- top_10_redemption_states.csv")
print("- redemption_payment_mode_analysis.csv")
print("- redemption_kyc_analysis.csv")

print("\nCharts saved:")
print("- monthly_redemption_count.png")
print("- monthly_redemption_amount.png")
print("- redemption_t30_b30.png")
print("- redemption_by_age_group.png")
print("- top_10_redemption_states.png")
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# TASK 12.1: INVESTOR BEHAVIOR ANALYSIS
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

print("=" * 70)
print("TASK 12.1: INVESTOR BEHAVIOR ANALYSIS")
print("=" * 70)

print("\nDataset shape:")
print(df.shape)


# ============================================================
# 1. TRANSACTION TYPE — INVESTMENT AMOUNT
# ============================================================

print("\n" + "=" * 70)
print("TRANSACTION TYPE — INVESTMENT AMOUNT")
print("=" * 70)

transaction_analysis = (
    df.groupby("transaction_type")
    .agg(
        transaction_count=("investor_id", "count"),
        total_amount_lakh=("amount_lakh", "sum"),
        average_amount_lakh=("amount_lakh", "mean")
    )
    .sort_values(
        "total_amount_lakh",
        ascending=False
    )
    .reset_index()
)

print(
    transaction_analysis.to_string(index=False)
)

transaction_analysis.to_csv(
    PROCESSED_DATA / "investor_transaction_behavior.csv",
    index=False
)


# ============================================================
# 2. CITY TIER — INVESTOR BEHAVIOR
# ============================================================

print("\n" + "=" * 70)
print("T30 VS B30 INVESTOR BEHAVIOR")
print("=" * 70)

city_analysis = (
    df.groupby("city_tier")
    .agg(
        transaction_count=("investor_id", "count"),
        total_amount_lakh=("amount_lakh", "sum"),
        average_amount_lakh=("amount_lakh", "mean")
    )
    .sort_values(
        "total_amount_lakh",
        ascending=False
    )
    .reset_index()
)

print(
    city_analysis.to_string(index=False)
)

city_analysis.to_csv(
    PROCESSED_DATA / "investor_city_tier_behavior.csv",
    index=False
)


# ============================================================
# 3. AGE GROUP ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("AGE GROUP INVESTMENT BEHAVIOR")
print("=" * 70)

age_analysis = (
    df.groupby("age_group")
    .agg(
        transaction_count=("investor_id", "count"),
        total_amount_lakh=("amount_lakh", "sum"),
        average_amount_lakh=("amount_lakh", "mean")
    )
    .sort_values(
        "total_amount_lakh",
        ascending=False
    )
    .reset_index()
)

print(
    age_analysis.to_string(index=False)
)

age_analysis.to_csv(
    PROCESSED_DATA / "investor_age_behavior.csv",
    index=False
)


# ============================================================
# 4. GENDER ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("GENDER-WISE INVESTMENT BEHAVIOR")
print("=" * 70)

gender_analysis = (
    df.groupby("gender")
    .agg(
        transaction_count=("investor_id", "count"),
        total_amount_lakh=("amount_lakh", "sum"),
        average_amount_lakh=("amount_lakh", "mean")
    )
    .sort_values(
        "total_amount_lakh",
        ascending=False
    )
    .reset_index()
)

print(
    gender_analysis.to_string(index=False)
)

gender_analysis.to_csv(
    PROCESSED_DATA / "investor_gender_behavior.csv",
    index=False
)


# ============================================================
# 5. PAYMENT MODE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("PAYMENT MODE PREFERENCE")
print("=" * 70)

payment_analysis = (
    df.groupby("payment_mode")
    .agg(
        transaction_count=("investor_id", "count"),
        total_amount_lakh=("amount_lakh", "sum"),
        average_amount_lakh=("amount_lakh", "mean")
    )
    .sort_values(
        "transaction_count",
        ascending=False
    )
    .reset_index()
)

print(
    payment_analysis.to_string(index=False)
)

payment_analysis.to_csv(
    PROCESSED_DATA / "payment_mode_analysis.csv",
    index=False
)


# ============================================================
# 6. KYC ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("KYC STATUS — INVESTMENT BEHAVIOR")
print("=" * 70)

kyc_analysis = (
    df.groupby("kyc_status")
    .agg(
        transaction_count=("investor_id", "count"),
        total_amount_lakh=("amount_lakh", "sum"),
        average_amount_lakh=("amount_lakh", "mean")
    )
    .sort_values(
        "total_amount_lakh",
        ascending=False
    )
    .reset_index()
)

print(
    kyc_analysis.to_string(index=False)
)

kyc_analysis.to_csv(
    PROCESSED_DATA / "kyc_investment_behavior.csv",
    index=False
)


# ============================================================
# 7. STATE-WISE INVESTMENT
# ============================================================

print("\n" + "=" * 70)
print("TOP 10 STATES BY INVESTMENT AMOUNT")
print("=" * 70)

state_analysis = (
    df.groupby("state")
    .agg(
        transaction_count=("investor_id", "count"),
        total_amount_lakh=("amount_lakh", "sum")
    )
    .sort_values(
        "total_amount_lakh",
        ascending=False
    )
    .head(10)
    .reset_index()
)

print(
    state_analysis.to_string(index=False)
)

state_analysis.to_csv(
    PROCESSED_DATA / "top_10_states_investment.csv",
    index=False
)


# ============================================================
# CHART 1 — TRANSACTION AMOUNT BY TYPE
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    transaction_analysis["transaction_type"],
    transaction_analysis["total_amount_lakh"]
)

plt.xlabel("Transaction Type")
plt.ylabel("Total Amount (₹ Lakh)")
plt.title("Investment Amount by Transaction Type")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "investor_amount_by_transaction_type.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 2 — T30 VS B30
# ============================================================

plt.figure(figsize=(7, 5))

plt.bar(
    city_analysis["city_tier"],
    city_analysis["total_amount_lakh"]
)

plt.xlabel("City Tier")
plt.ylabel("Total Amount (₹ Lakh)")
plt.title("Investment Amount — T30 vs B30")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "investor_t30_b30_amount.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 3 — AGE GROUP
# ============================================================

plt.figure(figsize=(9, 5))

plt.bar(
    age_analysis["age_group"].astype(str),
    age_analysis["total_amount_lakh"]
)

plt.xlabel("Age Group")
plt.ylabel("Total Investment (₹ Lakh)")
plt.title("Investment Amount by Age Group")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "investment_by_age_group.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 4 — PAYMENT MODE
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    payment_analysis["payment_mode"],
    payment_analysis["transaction_count"]
)

plt.xlabel("Payment Mode")
plt.ylabel("Number of Transactions")
plt.title("Payment Mode Preference")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "payment_mode_preference.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 5 — TOP STATES
# ============================================================

state_chart = state_analysis.sort_values(
    "total_amount_lakh",
    ascending=True
)

plt.figure(figsize=(9, 6))

plt.barh(
    state_chart["state"],
    state_chart["total_amount_lakh"]
)

plt.xlabel("Total Investment (₹ Lakh)")
plt.ylabel("State")
plt.title("Top 10 States by Investment Amount")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "top_10_states_investment.png",
    dpi=300
)

plt.show()


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 70)
print("TASK 12.1 COMPLETED")
print("=" * 70)

print("\nCSV files saved:")
print("- investor_transaction_behavior.csv")
print("- investor_city_tier_behavior.csv")
print("- investor_age_behavior.csv")
print("- investor_gender_behavior.csv")
print("- payment_mode_analysis.csv")
print("- kyc_investment_behavior.csv")
print("- top_10_states_investment.csv")

print("\nCharts saved:")
print("- investor_amount_by_transaction_type.png")
print("- investor_t30_b30_amount.png")
print("- investment_by_age_group.png")
print("- payment_mode_preference.png")
print("- top_10_states_investment.png")
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# TASK 12.2: SIP ANALYSIS
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

# Keep only SIP transactions
sip = df[
    df["transaction_type"] == "SIP"
].copy()

print("=" * 70)
print("TASK 12.2: SIP ANALYSIS")
print("=" * 70)

print("\nSIP dataset shape:")
print(sip.shape)


# ============================================================
# 1. SIP SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("SIP SUMMARY")
print("=" * 70)

print("\nTotal SIP transactions:")
print(len(sip))

print("\nTotal SIP amount (₹ Lakh):")
print(sip["amount_lakh"].sum())

print("\nAverage SIP transaction (₹ Lakh):")
print(sip["amount_lakh"].mean())

print("\nMedian SIP transaction (₹ Lakh):")
print(sip["amount_lakh"].median())


# ============================================================
# 2. MONTHLY SIP ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("MONTHLY SIP ANALYSIS")
print("=" * 70)

monthly_sip = (
    sip.groupby(
        ["transaction_year", "transaction_month"]
    )
    .agg(
        sip_transaction_count=("investor_id", "count"),
        total_sip_amount_lakh=("amount_lakh", "sum"),
        average_sip_amount_lakh=("amount_lakh", "mean")
    )
    .reset_index()
)

monthly_sip["year_month"] = (
    monthly_sip["transaction_year"].astype(str)
    + "-"
    + monthly_sip["transaction_month"]
      .astype(str)
      .str.zfill(2)
)

print(
    monthly_sip.head(12).to_string(index=False)
)

monthly_sip.to_csv(
    PROCESSED_DATA / "monthly_sip_analysis.csv",
    index=False
)


# ============================================================
# 3. SIP BY CITY TIER
# ============================================================

print("\n" + "=" * 70)
print("SIP BY CITY TIER")
print("=" * 70)

sip_city = (
    sip.groupby("city_tier")
    .agg(
        sip_transaction_count=("investor_id", "count"),
        total_sip_amount_lakh=("amount_lakh", "sum"),
        average_sip_amount_lakh=("amount_lakh", "mean")
    )
    .sort_values(
        "total_sip_amount_lakh",
        ascending=False
    )
    .reset_index()
)

print(
    sip_city.to_string(index=False)
)

sip_city.to_csv(
    PROCESSED_DATA / "sip_city_tier_analysis.csv",
    index=False
)


# ============================================================
# 4. SIP BY AGE GROUP
# ============================================================

print("\n" + "=" * 70)
print("SIP BY AGE GROUP")
print("=" * 70)

sip_age = (
    sip.groupby("age_group")
    .agg(
        sip_transaction_count=("investor_id", "count"),
        total_sip_amount_lakh=("amount_lakh", "sum"),
        average_sip_amount_lakh=("amount_lakh", "mean")
    )
    .sort_values(
        "total_sip_amount_lakh",
        ascending=False
    )
    .reset_index()
)

print(
    sip_age.to_string(index=False)
)

sip_age.to_csv(
    PROCESSED_DATA / "sip_age_group_analysis.csv",
    index=False
)


# ============================================================
# 5. SIP BY STATE
# ============================================================

print("\n" + "=" * 70)
print("TOP 10 STATES BY SIP AMOUNT")
print("=" * 70)

sip_state = (
    sip.groupby("state")
    .agg(
        sip_transaction_count=("investor_id", "count"),
        total_sip_amount_lakh=("amount_lakh", "sum")
    )
    .sort_values(
        "total_sip_amount_lakh",
        ascending=False
    )
    .head(10)
    .reset_index()
)

print(
    sip_state.to_string(index=False)
)

sip_state.to_csv(
    PROCESSED_DATA / "top_10_sip_states.csv",
    index=False
)


# ============================================================
# 6. SIP BY PAYMENT MODE
# ============================================================

print("\n" + "=" * 70)
print("SIP BY PAYMENT MODE")
print("=" * 70)

sip_payment = (
    sip.groupby("payment_mode")
    .agg(
        sip_transaction_count=("investor_id", "count"),
        total_sip_amount_lakh=("amount_lakh", "sum")
    )
    .sort_values(
        "sip_transaction_count",
        ascending=False
    )
    .reset_index()
)

print(
    sip_payment.to_string(index=False)
)

sip_payment.to_csv(
    PROCESSED_DATA / "sip_payment_mode_analysis.csv",
    index=False
)


# ============================================================
# CHART 1 — MONTHLY SIP TRANSACTIONS
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sip["year_month"],
    monthly_sip["sip_transaction_count"],
    marker="o"
)

plt.xlabel("Month")
plt.ylabel("Number of SIP Transactions")
plt.title("Monthly SIP Transaction Trend")

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "monthly_sip_transactions.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 2 — MONTHLY SIP AMOUNT
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sip["year_month"],
    monthly_sip["total_sip_amount_lakh"],
    marker="o"
)

plt.xlabel("Month")
plt.ylabel("Total SIP Amount (₹ Lakh)")
plt.title("Monthly SIP Investment Amount Trend")

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "monthly_sip_amount.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 3 — SIP BY CITY TIER
# ============================================================

plt.figure(figsize=(7, 5))

plt.bar(
    sip_city["city_tier"],
    sip_city["total_sip_amount_lakh"]
)

plt.xlabel("City Tier")
plt.ylabel("Total SIP Amount (₹ Lakh)")
plt.title("SIP Investment — T30 vs B30")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "sip_t30_b30.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 4 — SIP BY AGE GROUP
# ============================================================

plt.figure(figsize=(9, 5))

plt.bar(
    sip_age["age_group"].astype(str),
    sip_age["total_sip_amount_lakh"]
)

plt.xlabel("Age Group")
plt.ylabel("Total SIP Amount (₹ Lakh)")
plt.title("SIP Investment by Age Group")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "sip_by_age_group.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 5 — TOP STATES
# ============================================================

sip_state_chart = sip_state.sort_values(
    "total_sip_amount_lakh",
    ascending=True
)

plt.figure(figsize=(9, 6))

plt.barh(
    sip_state_chart["state"],
    sip_state_chart["total_sip_amount_lakh"]
)

plt.xlabel("Total SIP Amount (₹ Lakh)")
plt.ylabel("State")
plt.title("Top 10 States by SIP Investment")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "top_10_sip_states.png",
    dpi=300
)

plt.show()


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 70)
print("TASK 12.2 COMPLETED")
print("=" * 70)

print("\nCSV files saved:")
print("- monthly_sip_analysis.csv")
print("- sip_city_tier_analysis.csv")
print("- sip_age_group_analysis.csv")
print("- top_10_sip_states.csv")
print("- sip_payment_mode_analysis.csv")

print("\nCharts saved:")
print("- monthly_sip_transactions.png")
print("- monthly_sip_amount.png")
print("- sip_t30_b30.png")
print("- sip_by_age_group.png")
print("- top_10_sip_states.png")
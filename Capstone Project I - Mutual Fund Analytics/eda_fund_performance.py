from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# TASK 10.1: FUND PERFORMANCE EDA
# ============================================================

PROJECT_FOLDER = Path(__file__).parent
PROCESSED_DATA = PROJECT_FOLDER / "data" / "processed"
DASHBOARD_FOLDER = PROJECT_FOLDER / "dashboard"

DASHBOARD_FOLDER.mkdir(exist_ok=True)

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

df = pd.read_csv(
    PROCESSED_DATA / "fund_analysis_ready.csv"
)

print("=" * 70)
print("TASK 10.1: FUND PERFORMANCE EDA")
print("=" * 70)

print("\nDataset shape:")
print(df.shape)

print("\nAvailable columns:")
print(df.columns.tolist())


# ============================================================
# 1. TOP 10 FUNDS BY 1-YEAR RETURN
# ============================================================

print("\n" + "=" * 70)
print("TOP 10 FUNDS BY 1-YEAR RETURN")
print("=" * 70)

top_1y = df[
    [
        "scheme_name_master",
        "fund_house_master",
        "return_1yr_pct"
    ]
].sort_values(
    by="return_1yr_pct",
    ascending=False
).head(10)

print(top_1y.to_string(index=False))


# ============================================================
# 2. TOP 10 FUNDS BY 3-YEAR RETURN
# ============================================================

print("\n" + "=" * 70)
print("TOP 10 FUNDS BY 3-YEAR RETURN")
print("=" * 70)

top_3y = df[
    [
        "scheme_name_master",
        "fund_house_master",
        "return_3yr_pct"
    ]
].sort_values(
    by="return_3yr_pct",
    ascending=False
).head(10)

print(top_3y.to_string(index=False))


# ============================================================
# 3. RISK VS RETURN
# ============================================================

print("\n" + "=" * 70)
print("RISK VS RETURN")
print("=" * 70)

risk_return = df[
    [
        "scheme_name_master",
        "return_1yr_pct",
        "std_dev_ann_pct",
        "sharpe_ratio",
        "risk_grade"
    ]
].sort_values(
    by="return_1yr_pct",
    ascending=False
)

print(risk_return.head(10).to_string(index=False))


# ============================================================
# 4. MORNINGSTAR RATING VS PERFORMANCE
# ============================================================

print("\n" + "=" * 70)
print("MORNINGSTAR RATING VS AVERAGE 1-YEAR RETURN")
print("=" * 70)

rating_analysis = (
    df.groupby("morningstar_rating")["return_1yr_pct"]
    .mean()
    .sort_index()
)

print(rating_analysis)


# ============================================================
# 5. SAVE SUMMARY DATASETS
# ============================================================

top_1y.to_csv(
    PROCESSED_DATA / "top_10_funds_1y_return.csv",
    index=False
)

top_3y.to_csv(
    PROCESSED_DATA / "top_10_funds_3y_return.csv",
    index=False
)

risk_return.to_csv(
    PROCESSED_DATA / "fund_risk_return_analysis.csv",
    index=False
)

rating_analysis.reset_index().to_csv(
    PROCESSED_DATA / "rating_vs_return_analysis.csv",
    index=False
)


# ============================================================
# CHART 1: TOP 10 FUNDS BY 1-YEAR RETURN
# ============================================================

chart_data = top_1y.sort_values(
    "return_1yr_pct",
    ascending=True
)

plt.figure(figsize=(10, 6))

plt.barh(
    chart_data["scheme_name_master"],
    chart_data["return_1yr_pct"]
)

plt.xlabel("1-Year Return (%)")
plt.ylabel("Fund")
plt.title("Top 10 Mutual Funds by 1-Year Return")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "top_10_funds_1y_return.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 2: RISK VS RETURN
# ============================================================

plt.figure(figsize=(10, 6))

plt.scatter(
    df["std_dev_ann_pct"],
    df["return_1yr_pct"]
)

plt.xlabel("Annualized Standard Deviation (%)")
plt.ylabel("1-Year Return (%)")
plt.title("Risk vs Return — Mutual Funds")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "risk_vs_return.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 3: MORNINGSTAR RATING VS RETURN
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    rating_analysis.index.astype(str),
    rating_analysis.values
)

plt.xlabel("Morningstar Rating")
plt.ylabel("Average 1-Year Return (%)")
plt.title("Morningstar Rating vs Average 1-Year Return")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "rating_vs_return.png",
    dpi=300
)

plt.show()


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 70)
print("TASK 10.1 COMPLETED")
print("=" * 70)

print("\nCSV files saved:")
print("- top_10_funds_1y_return.csv")
print("- top_10_funds_3y_return.csv")
print("- fund_risk_return_analysis.csv")
print("- rating_vs_return_analysis.csv")

print("\nCharts saved in dashboard folder:")
print("- top_10_funds_1y_return.png")
print("- risk_vs_return.png")
print("- rating_vs_return.png")
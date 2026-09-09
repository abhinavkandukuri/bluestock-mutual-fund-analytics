from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# TASK 11.3: CATEGORY PERFORMANCE ANALYSIS
# ============================================================

PROJECT_FOLDER = Path(__file__).parent
PROCESSED_DATA = PROJECT_FOLDER / "data" / "processed"
DASHBOARD_FOLDER = PROJECT_FOLDER / "dashboard"

DASHBOARD_FOLDER.mkdir(exist_ok=True)

# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(
    PROCESSED_DATA / "fund_analysis_ready.csv"
)

print("=" * 70)
print("TASK 11.3: CATEGORY PERFORMANCE ANALYSIS")
print("=" * 70)

print("\nDataset shape:")
print(df.shape)


# ============================================================
# 1. CATEGORY PERFORMANCE SUMMARY
# ============================================================

category_summary = (
    df.groupby("category_master")
    .agg(
        number_of_funds=("amfi_code", "count"),
        avg_1yr_return=("return_1yr_pct", "mean"),
        avg_3yr_return=("return_3yr_pct", "mean"),
        avg_5yr_return=("return_5yr_pct", "mean"),
        avg_alpha=("alpha", "mean"),
        avg_sharpe=("sharpe_ratio", "mean"),
        avg_sortino=("sortino_ratio", "mean"),
        avg_volatility=("std_dev_ann_pct", "mean"),
        avg_drawdown=("max_drawdown_pct", "mean")
    )
    .reset_index()
)

print("\n" + "=" * 70)
print("CATEGORY PERFORMANCE SUMMARY")
print("=" * 70)

print(
    category_summary.to_string(index=False)
)


# ============================================================
# 2. RANKING BY 1-YEAR RETURN
# ============================================================

print("\n" + "=" * 70)
print("CATEGORY RANKING — AVERAGE 1-YEAR RETURN")
print("=" * 70)

ranking_1yr = (
    category_summary
    .sort_values("avg_1yr_return", ascending=False)
    .copy()
)

ranking_1yr["rank"] = range(1, len(ranking_1yr) + 1)

print(
    ranking_1yr[
        [
            "rank",
            "category_master",
            "number_of_funds",
            "avg_1yr_return"
        ]
    ].to_string(index=False)
)


# ============================================================
# 3. RANKING BY 3-YEAR RETURN
# ============================================================

print("\n" + "=" * 70)
print("CATEGORY RANKING — AVERAGE 3-YEAR RETURN")
print("=" * 70)

ranking_3yr = (
    category_summary
    .sort_values("avg_3yr_return", ascending=False)
    .copy()
)

ranking_3yr["rank"] = range(1, len(ranking_3yr) + 1)

print(
    ranking_3yr[
        [
            "rank",
            "category_master",
            "number_of_funds",
            "avg_3yr_return"
        ]
    ].to_string(index=False)
)


# ============================================================
# 4. RISK-ADJUSTED CATEGORY PERFORMANCE
# ============================================================

print("\n" + "=" * 70)
print("CATEGORY RANKING — AVERAGE SHARPE RATIO")
print("=" * 70)

ranking_sharpe = (
    category_summary
    .sort_values("avg_sharpe", ascending=False)
    .copy()
)

ranking_sharpe["rank"] = range(1, len(ranking_sharpe) + 1)

print(
    ranking_sharpe[
        [
            "rank",
            "category_master",
            "avg_sharpe",
            "avg_volatility"
        ]
    ].to_string(index=False)
)


# ============================================================
# 5. BEST CATEGORY BY 5-YEAR RETURN
# ============================================================

print("\n" + "=" * 70)
print("CATEGORY RANKING — AVERAGE 5-YEAR RETURN")
print("=" * 70)

ranking_5yr = (
    category_summary
    .sort_values("avg_5yr_return", ascending=False)
    .copy()
)

ranking_5yr["rank"] = range(1, len(ranking_5yr) + 1)

print(
    ranking_5yr[
        [
            "rank",
            "category_master",
            "number_of_funds",
            "avg_5yr_return"
        ]
    ].to_string(index=False)
)


# ============================================================
# 6. SAVE ANALYSIS FILES
# ============================================================

category_summary.to_csv(
    PROCESSED_DATA / "category_performance_summary.csv",
    index=False
)

ranking_1yr.to_csv(
    PROCESSED_DATA / "category_1yr_ranking.csv",
    index=False
)

ranking_3yr.to_csv(
    PROCESSED_DATA / "category_3yr_ranking.csv",
    index=False
)

ranking_5yr.to_csv(
    PROCESSED_DATA / "category_5yr_ranking.csv",
    index=False
)

ranking_sharpe.to_csv(
    PROCESSED_DATA / "category_sharpe_ranking.csv",
    index=False
)


# ============================================================
# CHART 1 — AVERAGE 1-YEAR RETURN
# ============================================================

chart_1yr = ranking_1yr.sort_values(
    "avg_1yr_return",
    ascending=True
)

plt.figure(figsize=(9, 6))

plt.barh(
    chart_1yr["category_master"],
    chart_1yr["avg_1yr_return"]
)

plt.xlabel("Average 1-Year Return (%)")
plt.ylabel("Category")
plt.title("Mutual Fund Category — Average 1-Year Return")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "category_avg_1yr_return.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 2 — AVERAGE 3-YEAR RETURN
# ============================================================

chart_3yr = ranking_3yr.sort_values(
    "avg_3yr_return",
    ascending=True
)

plt.figure(figsize=(9, 6))

plt.barh(
    chart_3yr["category_master"],
    chart_3yr["avg_3yr_return"]
)

plt.xlabel("Average 3-Year Return (%)")
plt.ylabel("Category")
plt.title("Mutual Fund Category — Average 3-Year Return")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "category_avg_3yr_return.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 3 — AVERAGE SHARPE RATIO
# ============================================================

chart_sharpe = ranking_sharpe.sort_values(
    "avg_sharpe",
    ascending=True
)

plt.figure(figsize=(9, 6))

plt.barh(
    chart_sharpe["category_master"],
    chart_sharpe["avg_sharpe"]
)

plt.xlabel("Average Sharpe Ratio")
plt.ylabel("Category")
plt.title("Category-wise Risk-Adjusted Performance")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "category_sharpe.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 4 — AVERAGE VOLATILITY
# ============================================================

chart_volatility = category_summary.sort_values(
    "avg_volatility",
    ascending=True
)

plt.figure(figsize=(9, 6))

plt.barh(
    chart_volatility["category_master"],
    chart_volatility["avg_volatility"]
)

plt.xlabel("Average Annualized Volatility (%)")
plt.ylabel("Category")
plt.title("Category-wise Volatility")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "category_volatility.png",
    dpi=300
)

plt.show()


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 70)
print("TASK 11.3 COMPLETED")
print("=" * 70)

print("\nCSV files saved:")
print("- category_performance_summary.csv")
print("- category_1yr_ranking.csv")
print("- category_3yr_ranking.csv")
print("- category_5yr_ranking.csv")
print("- category_sharpe_ranking.csv")

print("\nCharts saved:")
print("- category_avg_1yr_return.png")
print("- category_avg_3yr_return.png")
print("- category_sharpe.png")
print("- category_volatility.png")
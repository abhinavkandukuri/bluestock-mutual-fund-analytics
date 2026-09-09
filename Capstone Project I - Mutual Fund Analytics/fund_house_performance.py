from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# TASK 11.2: FUND HOUSE PERFORMANCE ANALYSIS
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
print("TASK 11.2: FUND HOUSE PERFORMANCE ANALYSIS")
print("=" * 70)

print("\nDataset shape:")
print(df.shape)


# ============================================================
# 1. FUND HOUSE PERFORMANCE SUMMARY
# ============================================================

fund_house_summary = (
    df.groupby("fund_house_master")
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
print("FUND HOUSE PERFORMANCE SUMMARY")
print("=" * 70)

print(
    fund_house_summary.to_string(index=False)
)


# ============================================================
# 2. RANK FUND HOUSES BY 1-YEAR RETURN
# ============================================================

print("\n" + "=" * 70)
print("FUND HOUSE RANKING — AVERAGE 1-YEAR RETURN")
print("=" * 70)

ranking_1yr = fund_house_summary.sort_values(
    "avg_1yr_return",
    ascending=False
).copy()

ranking_1yr["rank"] = range(1, len(ranking_1yr) + 1)

print(
    ranking_1yr[
        [
            "rank",
            "fund_house_master",
            "number_of_funds",
            "avg_1yr_return"
        ]
    ].to_string(index=False)
)


# ============================================================
# 3. RANK FUND HOUSES BY 3-YEAR RETURN
# ============================================================

print("\n" + "=" * 70)
print("FUND HOUSE RANKING — AVERAGE 3-YEAR RETURN")
print("=" * 70)

ranking_3yr = fund_house_summary.sort_values(
    "avg_3yr_return",
    ascending=False
).copy()

ranking_3yr["rank"] = range(1, len(ranking_3yr) + 1)

print(
    ranking_3yr[
        [
            "rank",
            "fund_house_master",
            "number_of_funds",
            "avg_3yr_return"
        ]
    ].to_string(index=False)
)


# ============================================================
# 4. RANK FUND HOUSES BY SHARPE RATIO
# ============================================================

print("\n" + "=" * 70)
print("FUND HOUSE RANKING — AVERAGE SHARPE RATIO")
print("=" * 70)

ranking_sharpe = fund_house_summary.sort_values(
    "avg_sharpe",
    ascending=False
).copy()

ranking_sharpe["rank"] = range(1, len(ranking_sharpe) + 1)

print(
    ranking_sharpe[
        [
            "rank",
            "fund_house_master",
            "avg_sharpe",
            "avg_volatility"
        ]
    ].to_string(index=False)
)


# ============================================================
# 5. SAVE ANALYSIS
# ============================================================

fund_house_summary.to_csv(
    PROCESSED_DATA / "fund_house_performance_summary.csv",
    index=False
)

ranking_1yr.to_csv(
    PROCESSED_DATA / "fund_house_1yr_ranking.csv",
    index=False
)

ranking_3yr.to_csv(
    PROCESSED_DATA / "fund_house_3yr_ranking.csv",
    index=False
)

ranking_sharpe.to_csv(
    PROCESSED_DATA / "fund_house_sharpe_ranking.csv",
    index=False
)


# ============================================================
# CHART 1 — AVERAGE 1-YEAR RETURN
# ============================================================

chart_1yr = ranking_1yr.sort_values(
    "avg_1yr_return",
    ascending=True
)

plt.figure(figsize=(10, 7))

plt.barh(
    chart_1yr["fund_house_master"],
    chart_1yr["avg_1yr_return"]
)

plt.xlabel("Average 1-Year Return (%)")
plt.ylabel("Fund House")
plt.title("Fund House Comparison — Average 1-Year Return")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "fund_house_avg_1yr_return.png",
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

plt.figure(figsize=(10, 7))

plt.barh(
    chart_3yr["fund_house_master"],
    chart_3yr["avg_3yr_return"]
)

plt.xlabel("Average 3-Year Return (%)")
plt.ylabel("Fund House")
plt.title("Fund House Comparison — Average 3-Year Return")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "fund_house_avg_3yr_return.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 3 — SHARPE RATIO
# ============================================================

chart_sharpe = ranking_sharpe.sort_values(
    "avg_sharpe",
    ascending=True
)

plt.figure(figsize=(10, 7))

plt.barh(
    chart_sharpe["fund_house_master"],
    chart_sharpe["avg_sharpe"]
)

plt.xlabel("Average Sharpe Ratio")
plt.ylabel("Fund House")
plt.title("Fund House Comparison — Risk-Adjusted Performance")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "fund_house_sharpe.png",
    dpi=300
)

plt.show()


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 70)
print("TASK 11.2 COMPLETED")
print("=" * 70)

print("\nCSV files saved:")
print("- fund_house_performance_summary.csv")
print("- fund_house_1yr_ranking.csv")
print("- fund_house_3yr_ranking.csv")
print("- fund_house_sharpe_ranking.csv")

print("\nCharts saved:")
print("- fund_house_avg_1yr_return.png")
print("- fund_house_avg_3yr_return.png")
print("- fund_house_sharpe.png")
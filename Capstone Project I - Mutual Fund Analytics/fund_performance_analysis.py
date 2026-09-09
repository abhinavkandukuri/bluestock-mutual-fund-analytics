from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# TASK 11.1: FUND PERFORMANCE ANALYSIS
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
print("TASK 11.1: FUND PERFORMANCE ANALYSIS")
print("=" * 70)

print("\nDataset shape:")
print(df.shape)


# ============================================================
# SELECT REQUIRED COLUMNS
# ============================================================

analysis = df[
    [
        "amfi_code",
        "scheme_name_master",
        "fund_house_master",
        "category_master",
        "sub_category",
        "return_1yr_pct",
        "return_3yr_pct",
        "return_5yr_pct",
        "alpha",
        "sharpe_ratio",
        "sortino_ratio",
        "std_dev_ann_pct",
        "max_drawdown_pct",
        "morningstar_rating",
        "risk_grade"
    ]
].copy()


# ============================================================
# 1. NORMALIZE PERFORMANCE METRICS
# ============================================================

metrics = [
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct",
    "alpha",
    "sharpe_ratio",
    "sortino_ratio"
]

for column in metrics:
    minimum = analysis[column].min()
    maximum = analysis[column].max()

    analysis[column + "_score"] = (
        (analysis[column] - minimum)
        / (maximum - minimum)
    ) * 100


# ============================================================
# 2. DRAWdown SCORE
# Lower drawdown is better
# ============================================================

minimum = analysis["max_drawdown_pct"].min()
maximum = analysis["max_drawdown_pct"].max()

analysis["drawdown_score"] = (
    (maximum - analysis["max_drawdown_pct"])
    / (maximum - minimum)
) * 100


# ============================================================
# 3. OVERALL PERFORMANCE SCORE
# ============================================================

analysis["performance_score"] = (
    analysis["return_1yr_pct_score"] * 0.15
    + analysis["return_3yr_pct_score"] * 0.20
    + analysis["return_5yr_pct_score"] * 0.20
    + analysis["alpha_score"] * 0.15
    + analysis["sharpe_ratio_score"] * 0.10
    + analysis["sortino_ratio_score"] * 0.10
    + analysis["drawdown_score"] * 0.10
)


# ============================================================
# 4. OVERALL FUND RANKING
# ============================================================

print("\n" + "=" * 70)
print("TOP 10 OVERALL PERFORMING FUNDS")
print("=" * 70)

ranking = analysis[
    [
        "amfi_code",
        "scheme_name_master",
        "fund_house_master",
        "category_master",
        "return_1yr_pct",
        "return_3yr_pct",
        "return_5yr_pct",
        "alpha",
        "sharpe_ratio",
        "sortino_ratio",
        "max_drawdown_pct",
        "performance_score"
    ]
].sort_values(
    "performance_score",
    ascending=False
)

ranking["rank"] = range(1, len(ranking) + 1)

ranking = ranking[
    [
        "rank",
        "amfi_code",
        "scheme_name_master",
        "fund_house_master",
        "category_master",
        "return_1yr_pct",
        "return_3yr_pct",
        "return_5yr_pct",
        "alpha",
        "sharpe_ratio",
        "sortino_ratio",
        "max_drawdown_pct",
        "performance_score"
    ]
]

print(
    ranking.head(10).to_string(index=False)
)


# Save ranking
ranking.to_csv(
    PROCESSED_DATA / "overall_fund_performance_ranking.csv",
    index=False
)


# ============================================================
# 5. BEST SHORT-TERM FUNDS
# ============================================================

print("\n" + "=" * 70)
print("TOP 10 SHORT-TERM FUNDS — 1 YEAR")
print("=" * 70)

short_term = analysis[
    [
        "scheme_name_master",
        "fund_house_master",
        "category_master",
        "return_1yr_pct"
    ]
].sort_values(
    "return_1yr_pct",
    ascending=False
).head(10)

print(
    short_term.to_string(index=False)
)

short_term.to_csv(
    PROCESSED_DATA / "best_short_term_funds.csv",
    index=False
)


# ============================================================
# 6. BEST LONG-TERM FUNDS
# ============================================================

print("\n" + "=" * 70)
print("TOP 10 LONG-TERM FUNDS — 5 YEAR")
print("=" * 70)

long_term = analysis[
    [
        "scheme_name_master",
        "fund_house_master",
        "category_master",
        "return_5yr_pct"
    ]
].sort_values(
    "return_5yr_pct",
    ascending=False
).head(10)

print(
    long_term.to_string(index=False)
)

long_term.to_csv(
    PROCESSED_DATA / "best_long_term_funds.csv",
    index=False
)


# ============================================================
# 7. BEST RISK-ADJUSTED FUNDS
# ============================================================

print("\n" + "=" * 70)
print("TOP 10 RISK-ADJUSTED FUNDS — SHARPE RATIO")
print("=" * 70)

risk_adjusted = analysis[
    [
        "scheme_name_master",
        "fund_house_master",
        "category_master",
        "sharpe_ratio",
        "sortino_ratio",
        "std_dev_ann_pct",
        "max_drawdown_pct"
    ]
].sort_values(
    "sharpe_ratio",
    ascending=False
).head(10)

print(
    risk_adjusted.to_string(index=False)
)

risk_adjusted.to_csv(
    PROCESSED_DATA / "best_risk_adjusted_funds.csv",
    index=False
)


# ============================================================
# 8. BEST MORNINGSTAR RATED FUNDS
# ============================================================

print("\n" + "=" * 70)
print("5-STAR FUNDS")
print("=" * 70)

five_star = analysis[
    analysis["morningstar_rating"] == 5
][
    [
        "scheme_name_master",
        "fund_house_master",
        "category_master",
        "return_1yr_pct",
        "return_3yr_pct",
        "return_5yr_pct",
        "morningstar_rating"
    ]
].sort_values(
    "return_3yr_pct",
    ascending=False
)

print(
    five_star.to_string(index=False)
)

five_star.to_csv(
    PROCESSED_DATA / "five_star_funds.csv",
    index=False
)


# ============================================================
# 9. HIGH DRAWDOWN FUNDS
# ============================================================

print("\n" + "=" * 70)
print("TOP 10 FUNDS WITH HIGHEST MAXIMUM DRAWDOWN")
print("=" * 70)

high_drawdown = analysis[
    [
        "scheme_name_master",
        "fund_house_master",
        "category_master",
        "max_drawdown_pct",
        "return_1yr_pct"
    ]
].sort_values(
    "max_drawdown_pct",
    ascending=True
).head(10)

print(
    high_drawdown.to_string(index=False)
)

high_drawdown.to_csv(
    PROCESSED_DATA / "high_drawdown_funds.csv",
    index=False
)


# ============================================================
# CHART 1 — OVERALL PERFORMANCE RANKING
# ============================================================

chart_ranking = ranking.head(10).sort_values(
    "performance_score",
    ascending=True
)

plt.figure(figsize=(10, 7))

plt.barh(
    chart_ranking["scheme_name_master"],
    chart_ranking["performance_score"]
)

plt.xlabel("Performance Score")
plt.ylabel("Fund")
plt.title("Top 10 Mutual Funds — Overall Performance Score")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "overall_fund_performance.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 2 — 5 YEAR RETURN
# ============================================================

chart_long = long_term.sort_values(
    "return_5yr_pct",
    ascending=True
)

plt.figure(figsize=(10, 7))

plt.barh(
    chart_long["scheme_name_master"],
    chart_long["return_5yr_pct"]
)

plt.xlabel("5-Year Return (%)")
plt.ylabel("Fund")
plt.title("Top 10 Funds by 5-Year Return")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "best_long_term_funds.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 3 — SHARPE RATIO
# ============================================================

chart_risk = risk_adjusted.sort_values(
    "sharpe_ratio",
    ascending=True
)

plt.figure(figsize=(10, 7))

plt.barh(
    chart_risk["scheme_name_master"],
    chart_risk["sharpe_ratio"]
)

plt.xlabel("Sharpe Ratio")
plt.ylabel("Fund")
plt.title("Top 10 Funds by Risk-Adjusted Performance")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "best_risk_adjusted_funds.png",
    dpi=300
)

plt.show()


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 70)
print("TASK 11.1 COMPLETED")
print("=" * 70)

print("\nCSV files saved:")
print("- overall_fund_performance_ranking.csv")
print("- best_short_term_funds.csv")
print("- best_long_term_funds.csv")
print("- best_risk_adjusted_funds.csv")
print("- five_star_funds.csv")
print("- high_drawdown_funds.csv")

print("\nCharts saved:")
print("- overall_fund_performance.png")
print("- best_long_term_funds.png")
print("- best_risk_adjusted_funds.png")
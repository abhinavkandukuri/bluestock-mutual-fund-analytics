from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# TASK 10.6: BENCHMARK & RISK METRICS EDA
# ============================================================

PROJECT_FOLDER = Path(__file__).parent
PROCESSED_DATA = PROJECT_FOLDER / "data" / "processed"
DASHBOARD_FOLDER = PROJECT_FOLDER / "dashboard"

DASHBOARD_FOLDER.mkdir(exist_ok=True)

# ============================================================
# LOAD FUND PERFORMANCE DATA
# ============================================================

df = pd.read_csv(
    PROCESSED_DATA / "fund_analysis_ready.csv"
)

print("=" * 70)
print("TASK 10.6: BENCHMARK & RISK METRICS EDA")
print("=" * 70)

print("\nFund performance dataset shape:")
print(df.shape)


# ============================================================
# 1. FUND VS BENCHMARK
# ============================================================

print("\n" + "=" * 70)
print("FUND VS BENCHMARK — 3 YEAR RETURN")
print("=" * 70)

fund_benchmark = df[
    [
        "scheme_name_master",
        "return_3yr_pct",
        "benchmark_3yr_pct",
        "alpha"
    ]
].copy()

fund_benchmark["outperformance_pct"] = (
    fund_benchmark["return_3yr_pct"]
    - fund_benchmark["benchmark_3yr_pct"]
)

fund_benchmark = fund_benchmark.sort_values(
    "outperformance_pct",
    ascending=False
)

print(
    fund_benchmark.head(10).to_string(index=False)
)

fund_benchmark.to_csv(
    PROCESSED_DATA / "fund_vs_benchmark_analysis.csv",
    index=False
)


# ============================================================
# 2. TOP 10 FUNDS BY ALPHA
# ============================================================

print("\n" + "=" * 70)
print("TOP 10 FUNDS BY ALPHA")
print("=" * 70)

top_alpha = df[
    [
        "scheme_name_master",
        "return_3yr_pct",
        "benchmark_3yr_pct",
        "alpha"
    ]
].sort_values(
    "alpha",
    ascending=False
).head(10)

print(
    top_alpha.to_string(index=False)
)

top_alpha.to_csv(
    PROCESSED_DATA / "top_10_alpha_funds.csv",
    index=False
)


# ============================================================
# 3. BETA ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("BETA ANALYSIS")
print("=" * 70)

beta_summary = (
    df[
        [
            "scheme_name_master",
            "beta",
            "return_1yr_pct",
            "risk_grade"
        ]
    ]
    .sort_values(
        "beta",
        ascending=False
    )
)

print(
    beta_summary.head(10).to_string(index=False)
)

beta_summary.to_csv(
    PROCESSED_DATA / "beta_analysis.csv",
    index=False
)


# ============================================================
# 4. SHARPE VS SORTINO
# ============================================================

print("\n" + "=" * 70)
print("SHARPE VS SORTINO RATIO")
print("=" * 70)

sharpe_sortino = df[
    [
        "scheme_name_master",
        "sharpe_ratio",
        "sortino_ratio",
        "return_1yr_pct"
    ]
].sort_values(
    "sharpe_ratio",
    ascending=False
)

print(
    sharpe_sortino.head(10).to_string(index=False)
)

sharpe_sortino.to_csv(
    PROCESSED_DATA / "sharpe_sortino_analysis.csv",
    index=False
)


# ============================================================
# 5. MAXIMUM DRAWDOWN
# ============================================================

print("\n" + "=" * 70)
print("TOP 10 FUNDS BY MAXIMUM DRAWDOWN")
print("=" * 70)

drawdown = df[
    [
        "scheme_name_master",
        "max_drawdown_pct",
        "return_1yr_pct",
        "risk_grade"
    ]
].sort_values(
    "max_drawdown_pct"
)

print(
    drawdown.head(10).to_string(index=False)
)

drawdown.to_csv(
    PROCESSED_DATA / "max_drawdown_analysis.csv",
    index=False
)


# ============================================================
# 6. OVERALL RISK METRICS
# ============================================================

print("\n" + "=" * 70)
print("RISK METRICS SUMMARY")
print("=" * 70)

risk_metrics = df[
    [
        "return_1yr_pct",
        "return_3yr_pct",
        "alpha",
        "beta",
        "sharpe_ratio",
        "sortino_ratio",
        "std_dev_ann_pct",
        "max_drawdown_pct"
    ]
].describe()

print(risk_metrics)

risk_metrics.to_csv(
    PROCESSED_DATA / "risk_metrics_summary.csv"
)


# ============================================================
# CHART 1: FUND VS BENCHMARK
# ============================================================

chart_data = fund_benchmark.head(10).sort_values(
    "outperformance_pct",
    ascending=True
)

plt.figure(figsize=(10, 7))

plt.barh(
    chart_data["scheme_name_master"],
    chart_data["outperformance_pct"]
)

plt.xlabel("Outperformance vs Benchmark (%)")
plt.ylabel("Fund")
plt.title("Top 10 Funds by 3-Year Outperformance vs Benchmark")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "fund_vs_benchmark.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 2: ALPHA
# ============================================================

chart_alpha = top_alpha.sort_values(
    "alpha",
    ascending=True
)

plt.figure(figsize=(10, 7))

plt.barh(
    chart_alpha["scheme_name_master"],
    chart_alpha["alpha"]
)

plt.xlabel("Alpha (%)")
plt.ylabel("Fund")
plt.title("Top 10 Mutual Funds by Alpha")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "top_alpha_funds.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 3: SHARPE VS SORTINO
# ============================================================

plt.figure(figsize=(9, 6))

plt.scatter(
    df["sharpe_ratio"],
    df["sortino_ratio"]
)

plt.xlabel("Sharpe Ratio")
plt.ylabel("Sortino Ratio")
plt.title("Sharpe Ratio vs Sortino Ratio")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "sharpe_vs_sortino.png",
    dpi=300
)

plt.show()


# ============================================================
# CHART 4: BETA DISTRIBUTION
# ============================================================

plt.figure(figsize=(9, 6))

plt.hist(
    df["beta"],
    bins=10
)

plt.xlabel("Beta")
plt.ylabel("Number of Funds")
plt.title("Distribution of Fund Beta")

plt.tight_layout()

plt.savefig(
    DASHBOARD_FOLDER / "beta_distribution.png",
    dpi=300
)

plt.show()


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 70)
print("TASK 10.6 COMPLETED")
print("=" * 70)

print("\nCSV files saved:")
print("- fund_vs_benchmark_analysis.csv")
print("- top_10_alpha_funds.csv")
print("- beta_analysis.csv")
print("- sharpe_sortino_analysis.csv")
print("- max_drawdown_analysis.csv")
print("- risk_metrics_summary.csv")

print("\nCharts saved in dashboard folder:")
print("- fund_vs_benchmark.png")
print("- top_alpha_funds.png")
print("- sharpe_vs_sortino.png")
print("- beta_distribution.png")
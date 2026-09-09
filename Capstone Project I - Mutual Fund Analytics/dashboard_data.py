from pathlib import Path
import pandas as pd

PROJECT_FOLDER = Path(__file__).parent
PROCESSED_DATA = PROJECT_FOLDER / "data" / "processed"
DASHBOARD_FOLDER = PROJECT_FOLDER / "dashboard"

DASHBOARD_FOLDER.mkdir(exist_ok=True)

print("=" * 70)
print("TASK 15.1: PREPARING DASHBOARD DATA")
print("=" * 70)


# ---------------------------------------------------------
# 1. FUND PERFORMANCE
# ---------------------------------------------------------

funds = pd.read_csv(
    PROCESSED_DATA / "fund_analysis_ready.csv"
)

funds = funds[
    [
        "amfi_code",
        "scheme_name_master",
        "fund_house_master",
        "category_master",
        "sub_category",
        "plan_master",
        "return_1yr_pct",
        "return_3yr_pct",
        "return_5yr_pct",
        "alpha",
        "beta",
        "sharpe_ratio",
        "sortino_ratio",
        "std_dev_ann_pct",
        "max_drawdown_pct",
        "aum_crore",
        "expense_ratio_pct_master",
        "morningstar_rating",
        "risk_grade"
    ]
]

funds.to_csv(
    DASHBOARD_FOLDER / "dashboard_fund_performance.csv",
    index=False
)

print(f"Fund performance: {funds.shape}")


# ---------------------------------------------------------
# 2. TRANSACTIONS
# ---------------------------------------------------------

transactions = pd.read_csv(
    PROCESSED_DATA / "transaction_analysis_ready.csv"
)

transactions.to_csv(
    DASHBOARD_FOLDER / "dashboard_transactions.csv",
    index=False
)

print(f"Transactions: {transactions.shape}")


# ---------------------------------------------------------
# 3. CATEGORY INFLOWS
# ---------------------------------------------------------

category = pd.read_csv(
    PROCESSED_DATA / "category_inflow_analysis_ready.csv"
)

category.to_csv(
    DASHBOARD_FOLDER / "dashboard_category_inflows.csv",
    index=False
)

print(f"Category inflows: {category.shape}")


# ---------------------------------------------------------
# 4. AUM
# ---------------------------------------------------------

aum = pd.read_csv(
    PROCESSED_DATA / "aum_analysis_ready.csv"
)

aum.to_csv(
    DASHBOARD_FOLDER / "dashboard_aum.csv",
    index=False
)

print(f"AUM: {aum.shape}")


# ---------------------------------------------------------
# 5. PORTFOLIO HOLDINGS
# ---------------------------------------------------------

portfolio = pd.read_csv(
    PROCESSED_DATA / "portfolio_analysis_ready.csv"
)

portfolio.to_csv(
    DASHBOARD_FOLDER / "dashboard_portfolio.csv",
    index=False
)

print(f"Portfolio holdings: {portfolio.shape}")


# ---------------------------------------------------------
# 6. NAV HISTORY
# ---------------------------------------------------------

nav = pd.read_csv(
    PROCESSED_DATA / "nav_analysis_ready.csv"
)

nav.to_csv(
    DASHBOARD_FOLDER / "dashboard_nav.csv",
    index=False
)

print(f"NAV history: {nav.shape}")


print("\n" + "=" * 70)
print("TASK 15.1 COMPLETED")
print("=" * 70)

print("\nDashboard files created successfully.")
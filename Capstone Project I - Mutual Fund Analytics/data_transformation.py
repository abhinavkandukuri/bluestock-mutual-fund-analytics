import pandas as pd
from pathlib import Path

# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_FOLDER = Path(__file__).parent
RAW_DATA = PROJECT_FOLDER / "data" / "raw"
PROCESSED_DATA = PROJECT_FOLDER / "data" / "processed"

# Create output folder
PROCESSED_DATA.mkdir(parents=True, exist_ok=True)


# ============================================================
# TASK 9: DATA TRANSFORMATION
# ============================================================

print("=" * 80)
print("TASK 9: DATA TRANSFORMATION")
print("=" * 80)


# ============================================================
# 1. LOAD CLEANED DATA
# ============================================================

fund_master = pd.read_csv(
    PROCESSED_DATA / "01_fund_master.csv"
)

scheme_performance = pd.read_csv(
    PROCESSED_DATA / "07_scheme_performance.csv"
)

print("\nFund Master shape:")
print(fund_master.shape)

print("\nScheme Performance shape:")
print(scheme_performance.shape)


# ============================================================
# 2. MERGE FUND MASTER + SCHEME PERFORMANCE
# ============================================================

fund_analysis = pd.merge(
    fund_master,
    scheme_performance,
    on="amfi_code",
    how="inner",
    suffixes=("_master", "_performance")
)

print("\nMerged Fund Analysis shape:")
print(fund_analysis.shape)


# ============================================================
# 3. CHECK MERGE
# ============================================================

print("\nUnique AMFI codes after merge:")
print(fund_analysis["amfi_code"].nunique())

print("\nMissing values after merge:")
print(fund_analysis.isnull().sum().sum())


# ============================================================
# 4. SAVE ANALYSIS-READY DATASET
# ============================================================

output_file = PROCESSED_DATA / "fund_analysis_ready.csv"

fund_analysis.to_csv(
    output_file,
    index=False
)

print("\nSaved analysis-ready dataset:")
print(output_file)


# ============================================================
# 5. DISPLAY SAMPLE
# ============================================================

print("\nFirst 5 rows:")
print(fund_analysis.head())


# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 80)
print("TASK 9.2 COMPLETED")
print("=" * 80)
# ============================================================
# TASK 9.3: NAV ANALYSIS DATASET
# ============================================================

print("\n" + "=" * 80)
print("TASK 9.3: NAV ANALYSIS DATASET")
print("=" * 80)


# ============================================================
# 1. LOAD NAV HISTORY
# ============================================================

nav_history = pd.read_csv(
    PROCESSED_DATA / "02_nav_history.csv"
)

print("\nNAV History shape:")
print(nav_history.shape)


# ============================================================
# 2. CONVERT DATE
# ============================================================

nav_history["date"] = pd.to_datetime(
    nav_history["date"],
    format="%Y-%m-%d",
    errors="coerce"
)


# ============================================================
# 3. SORT DATA
# ============================================================

nav_history = nav_history.sort_values(
    ["amfi_code", "date"]
).reset_index(drop=True)


# ============================================================
# 4. CALCULATE DAILY RETURN
# ============================================================

nav_history["daily_return_pct"] = (
    nav_history
    .groupby("amfi_code")["nav"]
    .pct_change() * 100
)


# ============================================================
# 5. CALCULATE CUMULATIVE RETURN
# ============================================================

nav_history["cumulative_return_pct"] = (
    nav_history
    .groupby("amfi_code")["nav"]
    .transform(
        lambda x: (x / x.iloc[0] - 1) * 100
    )
)


# ============================================================
# 6. CHECK RESULTS
# ============================================================

print("\nMissing values:")
print(nav_history.isnull().sum())

print("\nNAV Analysis sample:")
print(nav_history.head())


# ============================================================
# 7. SAVE NAV ANALYSIS DATASET
# ============================================================

nav_output_file = PROCESSED_DATA / "nav_analysis_ready.csv"

nav_history.to_csv(
    nav_output_file,
    index=False
)

print("\nSaved NAV analysis dataset:")
print(nav_output_file)


# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 80)
print("TASK 9.3 COMPLETED")
print("=" * 80)

# ============================================================
# TASK 9.4: INVESTOR TRANSACTION ANALYSIS DATASET
# ============================================================

print("\n" + "=" * 80)
print("TASK 9.4: INVESTOR TRANSACTION ANALYSIS")
print("=" * 80)


# ============================================================
# 1. LOAD TRANSACTION DATA
# ============================================================

transactions = pd.read_csv(
    PROCESSED_DATA / "08_investor_transactions.csv"
)

print("\nTransaction data shape:")
print(transactions.shape)


# ============================================================
# 2. CONVERT TRANSACTION DATE
# ============================================================

transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"],
    format="%Y-%m-%d",
    errors="coerce"
)


# ============================================================
# 3. CREATE TIME FEATURES
# ============================================================

transactions["transaction_year"] = (
    transactions["transaction_date"].dt.year
)

transactions["transaction_month"] = (
    transactions["transaction_date"].dt.month
)

transactions["transaction_month_name"] = (
    transactions["transaction_date"].dt.month_name()
)


# ============================================================
# 4. CONVERT AMOUNT TO LAKHS
# ============================================================

transactions["amount_lakh"] = (
    transactions["amount_inr"] / 100000
)


# ============================================================
# 5. CREATE INVESTOR AGE CATEGORY
# ============================================================

transactions["age_group"] = transactions["age_group"].astype(str)


# ============================================================
# 6. CHECK TRANSACTION TYPES
# ============================================================

print("\nTransaction types:")
print(transactions["transaction_type"].value_counts())


# ============================================================
# 7. CHECK CITY TIERS
# ============================================================

print("\nCity tiers:")
print(transactions["city_tier"].value_counts())


# ============================================================
# 8. CHECK KYC STATUS
# ============================================================

print("\nKYC status:")
print(transactions["kyc_status"].value_counts())


# ============================================================
# 9. CHECK MISSING VALUES
# ============================================================

print("\nMissing values:")
print(transactions.isnull().sum())


# ============================================================
# 10. SAVE ANALYSIS-READY DATASET
# ============================================================

transaction_output_file = (
    PROCESSED_DATA / "transaction_analysis_ready.csv"
)

transactions.to_csv(
    transaction_output_file,
    index=False
)

print("\nSaved transaction analysis dataset:")
print(transaction_output_file)


# ============================================================
# 11. DISPLAY SAMPLE
# ============================================================

print("\nFirst 5 rows:")
print(transactions.head())


# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 80)
print("TASK 9.4 COMPLETED")
print("=" * 80)

# ============================================================
# TASK 9.5: CATEGORY INFLOW ANALYSIS DATASET
# ============================================================

print("\n" + "=" * 80)
print("TASK 9.5: CATEGORY INFLOW ANALYSIS")
print("=" * 80)


# ============================================================
# 1. LOAD CATEGORY INFLOW DATA
# ============================================================

category_inflows = pd.read_csv(
    RAW_DATA / "05_category_inflows.csv"
)

print("\nCategory inflow data shape:")
print(category_inflows.shape)


# ============================================================
# 2. CONVERT MONTH TO DATE
# ============================================================

category_inflows["month"] = pd.to_datetime(
    category_inflows["month"].astype(str),
    format="%Y-%m",
    errors="coerce"
)


# ============================================================
# 3. CREATE TIME FEATURES
# ============================================================

category_inflows["year"] = (
    category_inflows["month"].dt.year
)

category_inflows["month_number"] = (
    category_inflows["month"].dt.month
)

category_inflows["month_name"] = (
    category_inflows["month"].dt.month_name()
)


# ============================================================
# 4. CHECK CATEGORIES
# ============================================================

print("\nCategories:")
print(category_inflows["category"].unique())

print("\nNumber of categories:")
print(category_inflows["category"].nunique())


# ============================================================
# 5. CHECK TOTAL INFLOWS BY CATEGORY
# ============================================================

category_summary = (
    category_inflows
    .groupby("category")["net_inflow_crore"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTotal net inflow by category:")
print(category_summary)


# ============================================================
# 6. CHECK MISSING VALUES
# ============================================================

print("\nMissing values:")
print(category_inflows.isnull().sum())


# ============================================================
# 7. SAVE ANALYSIS-READY DATASET
# ============================================================

category_output_file = (
    PROCESSED_DATA / "category_inflow_analysis_ready.csv"
)

category_inflows.to_csv(
    category_output_file,
    index=False
)

print("\nSaved category analysis dataset:")
print(category_output_file)


# ============================================================
# 8. DISPLAY SAMPLE
# ============================================================

print("\nFirst 5 rows:")
print(category_inflows.head())


# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 80)
print("TASK 9.5 COMPLETED")
print("=" * 80)

# ============================================================
# TASK 9.6: AUM & FUND HOUSE ANALYSIS DATASET
# ============================================================

print("\n" + "=" * 80)
print("TASK 9.6: AUM & FUND HOUSE ANALYSIS")
print("=" * 80)


# ============================================================
# 1. LOAD AUM DATA
# ============================================================

aum_data = pd.read_csv(
    PROCESSED_DATA / "03_aum_by_fund_house.csv"
)

print("\nAUM data shape:")
print(aum_data.shape)


# ============================================================
# 2. CONVERT DATE
# ============================================================

aum_data["date"] = pd.to_datetime(
    aum_data["date"],
    format="%Y-%m-%d",
    errors="coerce"
)


# ============================================================
# 3. CREATE TIME FEATURES
# ============================================================

aum_data["year"] = aum_data["date"].dt.year

aum_data["month"] = aum_data["date"].dt.month

aum_data["year_month"] = (
    aum_data["date"].dt.to_period("M").astype(str)
)


# ============================================================
# 4. CALCULATE AUM SHARE
# ============================================================

total_aum_by_date = (
    aum_data
    .groupby("date")["aum_crore"]
    .transform("sum")
)

aum_data["aum_share_pct"] = (
    aum_data["aum_crore"] /
    total_aum_by_date * 100
)


# ============================================================
# 5. CHECK FUND HOUSES
# ============================================================

print("\nFund houses:")
print(aum_data["fund_house"].unique())

print("\nNumber of fund houses:")
print(aum_data["fund_house"].nunique())


# ============================================================
# 6. AUM SUMMARY BY FUND HOUSE
# ============================================================

aum_summary = (
    aum_data
    .groupby("fund_house")["aum_crore"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTotal AUM by fund house:")
print(aum_summary)


# ============================================================
# 7. CHECK MISSING VALUES
# ============================================================

print("\nMissing values:")
print(aum_data.isnull().sum())


# ============================================================
# 8. SAVE ANALYSIS-READY DATASET
# ============================================================

aum_output_file = (
    PROCESSED_DATA / "aum_analysis_ready.csv"
)

aum_data.to_csv(
    aum_output_file,
    index=False
)

print("\nSaved AUM analysis dataset:")
print(aum_output_file)


# ============================================================
# 9. DISPLAY SAMPLE
# ============================================================

print("\nFirst 5 rows:")
print(aum_data.head())


# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 80)
print("TASK 9.6 COMPLETED")
print("=" * 80)

# ============================================================
# TASK 9.7: PORTFOLIO HOLDINGS ANALYSIS DATASET
# ============================================================

print("\n" + "=" * 80)
print("TASK 9.7: PORTFOLIO HOLDINGS ANALYSIS")
print("=" * 80)


# ============================================================
# 1. LOAD PORTFOLIO HOLDINGS
# ============================================================

holdings = pd.read_csv(
    PROCESSED_DATA / "09_portfolio_holdings.csv"
)

print("\nPortfolio holdings shape:")
print(holdings.shape)


# ============================================================
# 2. CONVERT PORTFOLIO DATE
# ============================================================

holdings["portfolio_date"] = pd.to_datetime(
    holdings["portfolio_date"],
    format="%Y-%m-%d",
    errors="coerce"
)


# ============================================================
# 3. CHECK SECTORS
# ============================================================

print("\nNumber of unique stocks:")
print(holdings["stock_symbol"].nunique())

print("\nNumber of sectors:")
print(holdings["sector"].nunique())

print("\nSectors:")
print(holdings["sector"].unique())


# ============================================================
# 4. SECTOR WEIGHT SUMMARY
# ============================================================

sector_summary = (
    holdings
    .groupby("sector")["weight_pct"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTotal portfolio weight by sector:")
print(sector_summary)


# ============================================================
# 5. TOP 10 STOCK HOLDINGS
# ============================================================

top_stocks = (
    holdings
    .groupby(["stock_symbol", "stock_name"])["weight_pct"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 stock holdings by weight:")
print(top_stocks)


# ============================================================
# 6. CHECK MISSING VALUES
# ============================================================

print("\nMissing values:")
print(holdings.isnull().sum())


# ============================================================
# 7. SAVE ANALYSIS-READY DATASET
# ============================================================

holdings_output_file = (
    PROCESSED_DATA / "portfolio_analysis_ready.csv"
)

holdings.to_csv(
    holdings_output_file,
    index=False
)

print("\nSaved portfolio analysis dataset:")
print(holdings_output_file)


# ============================================================
# 8. DISPLAY SAMPLE
# ============================================================

print("\nFirst 5 rows:")
print(holdings.head())


# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 80)
print("TASK 9.7 COMPLETED")
print("=" * 80)
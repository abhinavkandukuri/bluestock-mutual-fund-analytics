from pathlib import Path
import sqlite3
import pandas as pd

PROJECT_FOLDER = Path(__file__).parent
DATABASE_PATH = PROJECT_FOLDER / "sql" / "mutual_fund.db"

connection = sqlite3.connect(DATABASE_PATH)

print("=" * 70)
print("TASK 14.2: SQL ANALYSIS")
print("=" * 70)


# ---------------------------------------------------------
# QUERY 1: Top 10 Funds by 1-Year Return
# ---------------------------------------------------------

print("\n1. TOP 10 FUNDS BY 1-YEAR RETURN")

query = """
SELECT
    scheme_name_master,
    fund_house_master,
    category_master,
    return_1yr_pct
FROM fund_analysis
ORDER BY return_1yr_pct DESC
LIMIT 10;
"""

result = pd.read_sql_query(query, connection)
print(result)


# ---------------------------------------------------------
# QUERY 2: Top Fund Houses by Average 3-Year Return
# ---------------------------------------------------------

print("\n2. FUND HOUSES BY AVERAGE 3-YEAR RETURN")

query = """
SELECT
    fund_house_master,
    COUNT(*) AS number_of_funds,
    ROUND(AVG(return_3yr_pct), 2) AS avg_3yr_return
FROM fund_analysis
GROUP BY fund_house_master
ORDER BY avg_3yr_return DESC;
"""

result = pd.read_sql_query(query, connection)
print(result)


# ---------------------------------------------------------
# QUERY 3: Category Performance
# ---------------------------------------------------------

print("\n3. CATEGORY PERFORMANCE")

query = """
SELECT
    category_master,
    COUNT(*) AS number_of_funds,
    ROUND(AVG(return_1yr_pct), 2) AS avg_1yr_return,
    ROUND(AVG(return_3yr_pct), 2) AS avg_3yr_return,
    ROUND(AVG(sharpe_ratio), 2) AS avg_sharpe
FROM fund_analysis
GROUP BY category_master
ORDER BY avg_3yr_return DESC;
"""

result = pd.read_sql_query(query, connection)
print(result)


# ---------------------------------------------------------
# QUERY 4: Highest Alpha Funds
# ---------------------------------------------------------

print("\n4. TOP 10 FUNDS BY ALPHA")

query = """
SELECT
    scheme_name_master,
    fund_house_master,
    alpha,
    return_3yr_pct
FROM fund_analysis
ORDER BY alpha DESC
LIMIT 10;
"""

result = pd.read_sql_query(query, connection)
print(result)


# ---------------------------------------------------------
# QUERY 5: Best Sharpe Ratio
# ---------------------------------------------------------

print("\n5. TOP 10 FUNDS BY SHARPE RATIO")

query = """
SELECT
    scheme_name_master,
    fund_house_master,
    sharpe_ratio,
    return_3yr_pct,
    std_dev_ann_pct
FROM fund_analysis
ORDER BY sharpe_ratio DESC
LIMIT 10;
"""

result = pd.read_sql_query(query, connection)
print(result)


# ---------------------------------------------------------
# QUERY 6: Fund House AUM
# ---------------------------------------------------------

print("\n6. FUND HOUSE AUM")

query = """
SELECT
    fund_house,
    ROUND(SUM(aum_crore), 2) AS total_aum_crore
FROM aum_analysis
GROUP BY fund_house
ORDER BY total_aum_crore DESC;
"""

result = pd.read_sql_query(query, connection)
print(result)


# ---------------------------------------------------------
# QUERY 7: Category Inflows
# ---------------------------------------------------------

print("\n7. CATEGORY NET INFLOWS")

query = """
SELECT
    category,
    ROUND(SUM(net_inflow_crore), 2) AS total_net_inflow_crore
FROM category_inflows
GROUP BY category
ORDER BY total_net_inflow_crore DESC;
"""

result = pd.read_sql_query(query, connection)
print(result)


# ---------------------------------------------------------
# QUERY 8: Transaction Type Analysis
# ---------------------------------------------------------

print("\n8. TRANSACTION TYPE ANALYSIS")

query = """
SELECT
    transaction_type,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_inr), 2) AS total_amount_inr
FROM transactions
GROUP BY transaction_type
ORDER BY total_amount_inr DESC;
"""

result = pd.read_sql_query(query, connection)
print(result)


# ---------------------------------------------------------
# QUERY 9: T30 vs B30
# ---------------------------------------------------------

print("\n9. T30 VS B30 TRANSACTIONS")

query = """
SELECT
    city_tier,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_inr), 2) AS total_amount_inr
FROM transactions
GROUP BY city_tier
ORDER BY total_amount_inr DESC;
"""

result = pd.read_sql_query(query, connection)
print(result)


# ---------------------------------------------------------
# QUERY 10: Top Held Stocks
# ---------------------------------------------------------

print("\n10. TOP STOCK HOLDINGS")

query = """
SELECT
    stock_symbol,
    stock_name,
    sector,
    COUNT(*) AS number_of_holdings,
    ROUND(SUM(weight_pct), 2) AS total_weight_pct
FROM portfolio_holdings
GROUP BY stock_symbol, stock_name, sector
ORDER BY total_weight_pct DESC
LIMIT 10;
"""

result = pd.read_sql_query(query, connection)
print(result)


# ---------------------------------------------------------
# SAVE SQL RESULTS
# ---------------------------------------------------------

output_folder = PROJECT_FOLDER / "data" / "processed"
output_folder.mkdir(exist_ok=True)

result.to_csv(
    output_folder / "sql_top_stock_holdings.csv",
    index=False
)

# ---------------------------------------------------------
# QUERY 11: Funds with Above-Average 3-Year Return
# ---------------------------------------------------------

print("\n11. FUNDS ABOVE AVERAGE 3-YEAR RETURN")

query = """
SELECT
    scheme_name_master,
    fund_house_master,
    return_3yr_pct
FROM fund_analysis
WHERE return_3yr_pct > (
    SELECT AVG(return_3yr_pct)
    FROM fund_analysis
)
ORDER BY return_3yr_pct DESC;
"""

result = pd.read_sql_query(query, connection)
print(result)


# ---------------------------------------------------------
# QUERY 12: Best Fund in Each Category
# ---------------------------------------------------------

print("\n12. BEST FUND IN EACH CATEGORY")

query = """
SELECT
    category_master,
    scheme_name_master,
    fund_house_master,
    return_3yr_pct
FROM fund_analysis f
WHERE return_3yr_pct = (
    SELECT MAX(return_3yr_pct)
    FROM fund_analysis f2
    WHERE f2.category_master = f.category_master
)
ORDER BY return_3yr_pct DESC;
"""

result = pd.read_sql_query(query, connection)
print(result)


# ---------------------------------------------------------
# QUERY 13: High Return + High Sharpe Funds
# ---------------------------------------------------------

print("\n13. HIGH RETURN + HIGH SHARPE FUNDS")

query = """
SELECT
    scheme_name_master,
    fund_house_master,
    return_3yr_pct,
    sharpe_ratio,
    alpha
FROM fund_analysis
WHERE return_3yr_pct > (
    SELECT AVG(return_3yr_pct)
    FROM fund_analysis
)
AND sharpe_ratio > (
    SELECT AVG(sharpe_ratio)
    FROM fund_analysis
)
ORDER BY return_3yr_pct DESC;
"""

result = pd.read_sql_query(query, connection)
print(result)


# ---------------------------------------------------------
# QUERY 14: Fund House with Most Funds
# ---------------------------------------------------------

print("\n14. FUND HOUSE WITH MOST FUNDS")

query = """
SELECT
    fund_house_master,
    COUNT(*) AS number_of_funds
FROM fund_analysis
GROUP BY fund_house_master
ORDER BY number_of_funds DESC
LIMIT 1;
"""

result = pd.read_sql_query(query, connection)
print(result)


# ---------------------------------------------------------
# QUERY 15: Monthly Transaction Trend
# ---------------------------------------------------------

print("\n15. MONTHLY TRANSACTION TREND")

query = """
SELECT
    transaction_year,
    transaction_month,
    transaction_month_name,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_inr), 2) AS total_amount_inr
FROM transactions
GROUP BY
    transaction_year,
    transaction_month,
    transaction_month_name
ORDER BY
    transaction_year,
    transaction_month;
"""

result = pd.read_sql_query(query, connection)
print(result)


# ---------------------------------------------------------
# QUERY 16: KYC Status Analysis
# ---------------------------------------------------------

print("\n16. KYC STATUS ANALYSIS")

query = """
SELECT
    kyc_status,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_inr), 2) AS total_amount_inr
FROM transactions
GROUP BY kyc_status
ORDER BY total_amount_inr DESC;
"""

result = pd.read_sql_query(query, connection)
print(result)


# ---------------------------------------------------------
# QUERY 17: Most Diversified Funds
# ---------------------------------------------------------

print("\n17. MOST DIVERSIFIED FUNDS")

query = """
SELECT
    amfi_code,
    COUNT(DISTINCT stock_symbol) AS unique_stocks
FROM portfolio_holdings
GROUP BY amfi_code
ORDER BY unique_stocks DESC
LIMIT 10;
"""

result = pd.read_sql_query(query, connection)
print(result)


# ---------------------------------------------------------
# QUERY 18: Sector Concentration
# ---------------------------------------------------------

print("\n18. SECTOR CONCENTRATION")

query = """
SELECT
    sector,
    COUNT(DISTINCT stock_symbol) AS unique_stocks,
    COUNT(*) AS number_of_holdings,
    ROUND(SUM(weight_pct), 2) AS total_weight_pct
FROM portfolio_holdings
GROUP BY sector
ORDER BY total_weight_pct DESC;
"""

result = pd.read_sql_query(query, connection)
print(result)


print("\n" + "=" * 70)
print("ADVANCED SQL ANALYSIS COMPLETED")
print("=" * 70)


connection.close()

print("\n" + "=" * 70)
print("TASK 14.2 COMPLETED")
print("=" * 70)
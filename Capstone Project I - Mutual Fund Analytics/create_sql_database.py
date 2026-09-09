from pathlib import Path
import pandas as pd
import sqlite3

# ============================================================
# TASK 14.1: CREATE SQL DATABASE
# ============================================================

PROJECT_FOLDER = Path(__file__).parent
PROCESSED_DATA = PROJECT_FOLDER / "data" / "processed"
SQL_FOLDER = PROJECT_FOLDER / "sql"

SQL_FOLDER.mkdir(exist_ok=True)

DATABASE_PATH = SQL_FOLDER / "mutual_fund.db"

print("=" * 70)
print("TASK 14.1: CREATING SQL DATABASE")
print("=" * 70)

# ============================================================
# CREATE DATABASE CONNECTION
# ============================================================

connection = sqlite3.connect(DATABASE_PATH)

# ============================================================
# DATASETS TO LOAD
# ============================================================

datasets = {
    "fund_analysis": "fund_analysis_ready.csv",
    "nav_analysis": "nav_analysis_ready.csv",
    "transactions": "transaction_analysis_ready.csv",
    "category_inflows": "category_inflow_analysis_ready.csv",
    "aum_analysis": "aum_analysis_ready.csv",
    "portfolio_holdings": "portfolio_analysis_ready.csv"
}

# ============================================================
# LOAD DATASETS INTO SQL
# ============================================================

for table_name, file_name in datasets.items():

    file_path = PROCESSED_DATA / file_name

    df = pd.read_csv(file_path)

    df.to_sql(
        table_name,
        connection,
        if_exists="replace",
        index=False
    )

    print(
        f"\nLoaded {table_name}: "
        f"{df.shape[0]} rows, "
        f"{df.shape[1]} columns"
    )


# ============================================================
# CHECK TABLES
# ============================================================

print("\n" + "=" * 70)
print("DATABASE TABLES")
print("=" * 70)

tables = pd.read_sql_query(
    """
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    ORDER BY name;
    """,
    connection
)

print(tables)


# ============================================================
# CHECK ROW COUNTS
# ============================================================

print("\n" + "=" * 70)
print("TABLE ROW COUNTS")
print("=" * 70)

for table in datasets.keys():

    result = pd.read_sql_query(
        f"SELECT COUNT(*) AS row_count FROM {table}",
        connection
    )

    print(
        f"{table}: "
        f"{result.iloc[0]['row_count']} rows"
    )


# ============================================================
# CLOSE DATABASE
# ============================================================

connection.close()

print("\n" + "=" * 70)
print("TASK 14.1 COMPLETED")
print("=" * 70)

print("\nDatabase created:")
print(DATABASE_PATH)

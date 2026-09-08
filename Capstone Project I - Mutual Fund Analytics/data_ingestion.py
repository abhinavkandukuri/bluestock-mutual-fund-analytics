import pandas as pd
from pathlib import Path

# Get the folder where this Python file is located
PROJECT_FOLDER = Path(__file__).parent

# Raw data folder
RAW_DATA = PROJECT_FOLDER / "data" / "raw"

# Find all CSV files
csv_files = list(RAW_DATA.glob("*.csv"))

print(f"Raw data folder: {RAW_DATA}")
print(f"Found {len(csv_files)} CSV files\n")

# Load and inspect every CSV
for file in csv_files:
    print("=" * 80)
    print(f"FILE: {file.name}")
    print("=" * 80)

    try:
        df = pd.read_csv(file)

        print("\nShape:")
        print(df.shape)

        print("\nData Types:")
        print(df.dtypes)

        print("\nFirst 5 Rows:")
        print(df.head())

        print("\nMissing Values:")
        print(df.isnull().sum())

    except Exception as e:
        print(f"Error reading {file.name}: {e}")

    print("\n")
# ============================================================
# TASK 6: FUND MASTER EXPLORATION
# ============================================================

print("\n" + "#" * 80)
print("FUND MASTER EXPLORATION")
print("#" * 80)

fund_master_file = RAW_DATA / "01_fund_master.csv"
nav_history_file = RAW_DATA / "02_nav_history.csv"

fund_master = pd.read_csv(fund_master_file)
nav_history = pd.read_csv(nav_history_file)

print("\nUnique Fund Houses:")
print(fund_master["fund_house"].unique())

print("\nUnique Categories:")
print(fund_master["category"].unique())

print("\nUnique Sub-Categories:")
print(fund_master["sub_category"].unique())

print("\nUnique Risk Categories:")
print(fund_master["risk_category"].unique())

print("\nNumber of unique AMFI codes:")
print(fund_master["amfi_code"].nunique())


# ============================================================
# TASK 7: AMFI CODE VALIDATION
# ============================================================

print("\n" + "#" * 80)
print("AMFI CODE VALIDATION")
print("#" * 80)

master_codes = set(fund_master["amfi_code"])
nav_codes = set(nav_history["amfi_code"])

missing_codes = master_codes - nav_codes
extra_codes = nav_codes - master_codes

print("\nAMFI codes in Fund Master:", len(master_codes))
print("AMFI codes in NAV History:", len(nav_codes))

print("\nCodes in Fund Master but missing from NAV History:")
print(missing_codes)

print("\nCodes in NAV History but not in Fund Master:")
print(extra_codes)

if len(missing_codes) == 0:
    print("\nVALIDATION RESULT: PASS")
    print("Every AMFI code in fund_master exists in nav_history.")
else:
    print("\nVALIDATION RESULT: ATTENTION REQUIRED")
    print(f"{len(missing_codes)} AMFI code(s) are missing from nav_history.")


# ============================================================
# DATA QUALITY SUMMARY
# ============================================================

print("\n" + "#" * 80)
print("DATA QUALITY SUMMARY")
print("#" * 80)

print(f"""
1. Fund master contains {len(fund_master)} schemes.
2. Fund master contains {fund_master["amfi_code"].nunique()} unique AMFI codes.
3. NAV history contains {len(nav_history)} records.
4. NAV history contains {nav_history["amfi_code"].nunique()} unique AMFI codes.
5. Missing AMFI codes from NAV history: {len(missing_codes)}.
6. Extra AMFI codes in NAV history: {len(extra_codes)}.
7. Monthly SIP inflows has 12 missing YoY growth values.
""")
import pandas as pd
from pathlib import Path

# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_FOLDER = Path(__file__).parent
RAW_DATA = PROJECT_FOLDER / "data" / "raw"
PROCESSED_DATA = PROJECT_FOLDER / "data" / "processed"

# Create processed folder if it doesn't exist
PROCESSED_DATA.mkdir(parents=True, exist_ok=True)


# ============================================================
# TASK 8: DATA CLEANING
# ============================================================

print("=" * 80)
print("TASK 8: DATA CLEANING")
print("=" * 80)

csv_files = list(RAW_DATA.glob("*.csv"))

print(f"\nFound {len(csv_files)} CSV files in raw folder.")


for file in csv_files:

    print("\n" + "-" * 80)
    print(f"Processing: {file.name}")
    print("-" * 80)

    try:
        # Load CSV
        df = pd.read_csv(file)

        # Original information
        original_rows = len(df)

        # ----------------------------------------------------
        # 1. Remove duplicate rows
        # ----------------------------------------------------
        duplicate_count = df.duplicated().sum()

        if duplicate_count > 0:
            df = df.drop_duplicates()

        # ----------------------------------------------------
        # 2. Convert date columns
        # ----------------------------------------------------
        for column in df.columns:

            if column in ["date", "launch_date", "transaction_date", "portfolio_date"]:

                # Live API NAV files use DD-MM-YYYY
                if file.name.endswith("_nav.csv"):
                    df[column] = pd.to_datetime(
                        df[column],
                        format="%d-%m-%Y",
                        errors="coerce"
                    )

                # Original datasets use YYYY-MM-DD
                else:
                    df[column] = pd.to_datetime(
                        df[column],
                        format="%Y-%m-%d",
                        
                        errors="coerce"
                    )

            elif column == "month":
                df[column] = pd.to_datetime(
                    df[column],
                    errors="coerce"
                )
        # ----------------------------------------------------
        # 3. Check missing values
        # ----------------------------------------------------
        missing_values = df.isnull().sum()
        total_missing = missing_values.sum()

        # ----------------------------------------------------
        # 4. Save cleaned file
        # ----------------------------------------------------
        output_file = PROCESSED_DATA / file.name
        df.to_csv(output_file, index=False)

        print(f"Original rows : {original_rows}")
        print(f"Duplicates    : {duplicate_count}")
        print(f"Final rows    : {len(df)}")
        print(f"Missing cells : {total_missing}")
        print(f"Saved to      : {output_file}")

    except Exception as e:
        print(f"ERROR processing {file.name}: {e}")


# ============================================================
# SPECIAL CHECK: MONTHLY SIP INFLOWS
# ============================================================

print("\n" + "=" * 80)
print("MONTHLY SIP INFLOWS - MISSING VALUE CHECK")
print("=" * 80)

sip_file = PROCESSED_DATA / "04_monthly_sip_inflows.csv"

if sip_file.exists():

    sip_df = pd.read_csv(sip_file)

    print("\nMissing YoY Growth values:")
    print(sip_df["yoy_growth_pct"].isnull().sum())

    print("\nNote:")
    print("The first 12 months naturally have no YoY growth value")
    print("because there is no previous-year month available.")


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 80)
print("TASK 8 COMPLETED")
print("=" * 80)

print(f"\nCleaned files saved in:")
print(PROCESSED_DATA)
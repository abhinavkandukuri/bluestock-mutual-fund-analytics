import pandas as pd
from pathlib import Path

# Folder containing raw CSV files
RAW_DATA = Path("data/raw")

# Find all CSV files
csv_files = list(RAW_DATA.glob("*.csv"))

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

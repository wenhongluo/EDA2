"""
Inspect wildcat_loans_clean.csv: shape, column dtypes, and missing value counts.

Usage:
    python inspect_wildcat_loans.py [path_to_csv]

If no path is given, defaults to "wildcat_loans_clean.csv" in the current directory.
"""

import sys
import pandas as pd


def main():
    file_path = sys.argv[1] if len(sys.argv) > 1 else "wildcat_loans_clean.csv"

    df = pd.read_csv(file_path)

    print("=" * 60)
    print("SHAPE")
    print("=" * 60)
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    print("\n" + "=" * 60)
    print("COLUMN NAMES, DATA TYPES, AND MISSING VALUE COUNTS")
    print("=" * 60)
    summary = pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "missing_count": df.isnull().sum(),
    })
    print(summary.to_string())

    print("\n" + "=" * 60)
    print("TOTAL MISSING VALUES")
    print("=" * 60)
    print(df.isnull().sum().sum())


if __name__ == "__main__":
    main()

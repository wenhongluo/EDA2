"""
Print descriptive statistics (count, mean, std, min, 25%, 50%, 75%, max) for
all numeric columns in wildcat_loans_clean.csv, with loan_amount formatted
to two decimal places.

Usage:
    python describe_wildcat_loans.py [path_to_csv]

If no path is given, defaults to "wildcat_loans_clean.csv" in the current directory.
"""

import sys
import pandas as pd

LOAN_AMOUNT_COLUMN = "loan_amount"


def main():
    file_path = sys.argv[1] if len(sys.argv) > 1 else "wildcat_loans_clean.csv"

    df = pd.read_csv(file_path)

    numeric_df = df.select_dtypes(include="number")
    stats = numeric_df.describe()

    # Round every column to 2 decimals for a clean display; loan_amount in
    # particular is currency, so 2 decimal places is required there.
    stats = stats.round(2)

    pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

    print("=" * 70)
    print("DESCRIPTIVE STATISTICS — NUMERIC COLUMNS")
    print("=" * 70)
    print(stats.to_string())

    if LOAN_AMOUNT_COLUMN in stats.columns:
        print("\n" + "=" * 70)
        print(f"'{LOAN_AMOUNT_COLUMN}' STATISTICS (2 decimal places)")
        print("=" * 70)
        for stat_name, value in stats[LOAN_AMOUNT_COLUMN].items():
            label = "count" if stat_name == "count" else stat_name
            print(f"{label:>6}: {value:,.2f}")


if __name__ == "__main__":
    main()

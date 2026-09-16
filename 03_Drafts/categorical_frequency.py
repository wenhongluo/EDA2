"""
Print count and percentage breakdowns for each categorical column
(loan_purpose, loan_status, state) in wildcat_loans_clean.csv, sorted from
most to least frequent, with percentages shown to one decimal place.

Usage:
    python categorical_frequency.py [path_to_csv]

If no path is given, defaults to "wildcat_loans_clean.csv" in the current directory.
"""

import sys
import pandas as pd

CATEGORICAL_COLUMNS = ["loan_purpose", "loan_status", "state"]


def frequency_table(df: pd.DataFrame, column: str) -> pd.DataFrame:
    counts = df[column].value_counts(dropna=False)
    pct = (counts / len(df) * 100).round(1)
    table = pd.DataFrame({"count": counts, "percentage": pct})
    table = table.sort_values("count", ascending=False)
    return table


def main():
    file_path = sys.argv[1] if len(sys.argv) > 1 else "wildcat_loans_clean.csv"

    df = pd.read_csv(file_path)

    for column in CATEGORICAL_COLUMNS:
        if column not in df.columns:
            print(f"Column '{column}' not found in the DataFrame — skipping.\n")
            continue

        table = frequency_table(df, column)

        print("=" * 60)
        print(f"{column.upper()} — VALUE COUNTS AND PERCENTAGES")
        print("=" * 60)
        for value, row in table.iterrows():
            print(f"{str(value):<20} count: {int(row['count']):>6}   percentage: {row['percentage']:>5.1f}%")
        print()


if __name__ == "__main__":
    main()

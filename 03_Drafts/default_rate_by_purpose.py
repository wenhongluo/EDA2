"""
Group wildcat_loans_clean.csv by loan_purpose and compute, for each purpose,
the count of loans and the count/percentage with loan_status == "Default".
Sorted by default percentage descending.

Usage:
    python default_rate_by_purpose.py [path_to_csv]

If no path is given, defaults to "wildcat_loans_clean.csv" in the current directory.
"""

import sys
import pandas as pd

GROUP_COLUMN = "loan_purpose"
STATUS_COLUMN = "loan_status"
TARGET_STATUS = "Default"


def main():
    file_path = sys.argv[1] if len(sys.argv) > 1 else "wildcat_loans_clean.csv"

    df = pd.read_csv(file_path)

    is_default = df[STATUS_COLUMN] == TARGET_STATUS

    summary = df.groupby(GROUP_COLUMN).agg(
        count=(GROUP_COLUMN, "size"),
        default_count=(STATUS_COLUMN, lambda s: (s == TARGET_STATUS).sum()),
    )

    summary = summary.assign(
        default_pct=(summary["default_count"] / summary["count"] * 100).round(1)
    )

    summary = summary.sort_values("default_pct", ascending=False)

    print("=" * 70)
    print(f"LOAN COUNT AND '{TARGET_STATUS}' RATE BY {GROUP_COLUMN.upper()}")
    print("(sorted by default percentage, descending)")
    print("=" * 70)
    print(summary.to_string())

    overall_default_pct = is_default.sum() / len(df) * 100
    print(f"\nOverall default rate across all loans: {overall_default_pct:.1f}%")


if __name__ == "__main__":
    main()

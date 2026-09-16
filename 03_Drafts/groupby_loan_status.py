"""
Group wildcat_loans_clean.csv by loan_status and compute summary statistics:
count of loans, mean loan_amount, mean interest_rate, mean credit_score
(excluding nulls), and mean debt_to_income_ratio. Sorted by count descending.

Usage:
    python groupby_loan_status.py [path_to_csv]

If no path is given, defaults to "wildcat_loans_clean.csv" in the current directory.
"""

import sys
import pandas as pd

GROUP_COLUMN = "loan_status"


def main():
    file_path = sys.argv[1] if len(sys.argv) > 1 else "wildcat_loans_clean.csv"

    df = pd.read_csv(file_path)

    summary = df.groupby(GROUP_COLUMN).agg(
        count=("loan_status", "size"),
        mean_loan_amount=("loan_amount", "mean"),
        mean_interest_rate=("interest_rate", "mean"),
        mean_credit_score=("credit_score", "mean"),  # .mean() skips NaN by default
        mean_debt_to_income_ratio=("debt_to_income_ratio", "mean"),
    )

    summary = summary.assign(
        mean_loan_amount=summary["mean_loan_amount"].round(2),
        mean_interest_rate=summary["mean_interest_rate"].round(4),
        mean_credit_score=summary["mean_credit_score"].round(1),
        mean_debt_to_income_ratio=summary["mean_debt_to_income_ratio"].round(4),
    )

    summary = summary.sort_values("count", ascending=False)

    print("=" * 90)
    print("LOAN SUMMARY BY LOAN_STATUS (sorted by count, descending)")
    print("=" * 90)
    print(summary.to_string())


if __name__ == "__main__":
    main()

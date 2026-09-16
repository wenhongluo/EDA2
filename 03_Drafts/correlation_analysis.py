"""
Compute the correlation matrix for numeric columns in wildcat_loans_clean.csv
(excluding the identifier columns loan_id and borrower_id), print it rounded
to 2 decimal places, and identify the five strongest correlations (by
absolute value, excluding self-correlations).

Usage:
    python correlation_analysis.py [path_to_csv]

If no path is given, defaults to "wildcat_loans_clean.csv" in the current directory.
"""

import sys
import pandas as pd

EXCLUDE_COLUMNS = ["loan_id", "borrower_id"]


def main():
    file_path = sys.argv[1] if len(sys.argv) > 1 else "wildcat_loans_clean.csv"

    df = pd.read_csv(file_path)

    numeric_df = df.select_dtypes(include="number").drop(
        columns=[c for c in EXCLUDE_COLUMNS if c in df.columns]
    )

    corr = numeric_df.corr()  # pairwise-complete; handles credit_score NaNs automatically
    corr_rounded = corr.round(2)

    print("=" * 90)
    print("CORRELATION MATRIX (numeric columns, excluding loan_id / borrower_id)")
    print("=" * 90)
    print(corr_rounded.to_string())

    # Extract each unique pair exactly once (upper triangle, no diagonal),
    # then rank by absolute correlation strength.
    pairs = corr.stack()
    pairs = pairs[pairs.index.get_level_values(0) < pairs.index.get_level_values(1)]
    pairs = pairs.reindex(pairs.abs().sort_values(ascending=False).index)

    top_5 = pairs.head(5)

    print("\n" + "=" * 90)
    print("TOP 5 STRONGEST CORRELATIONS (by absolute value)")
    print("=" * 90)
    for (var1, var2), value in top_5.items():
        direction = "positive" if value > 0 else "negative"
        print(f"{var1} <-> {var2}: r = {value:.2f} ({direction})")


if __name__ == "__main__":
    main()

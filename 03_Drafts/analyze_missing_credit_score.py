"""
Analyze missing values in wildcat_loans_clean.csv, with a focused look at
whether credit_score missingness is random or concentrated in particular
loan_status / loan_purpose groups.

Usage:
    python analyze_missing_credit_score.py [path_to_csv]

If no path is given, defaults to "wildcat_loans_clean.csv" in the current directory.
"""

import sys
import pandas as pd

TARGET_COLUMN = "credit_score"
GROUP_COLUMNS = ["loan_status", "loan_purpose"]


def missing_summary(df: pd.DataFrame) -> pd.DataFrame:
    counts = df.isnull().sum()
    pct = (counts / len(df) * 100).round(2)
    return pd.DataFrame({"missing_count": counts, "missing_pct": pct})


def distribution_comparison(df: pd.DataFrame, column: str, target_column: str) -> pd.DataFrame:
    missing_mask = df[target_column].isnull()

    full_pct = (df[column].value_counts(normalize=True, dropna=False) * 100).round(2)
    missing_pct = (df.loc[missing_mask, column].value_counts(normalize=True, dropna=False) * 100).round(2)

    comparison = pd.DataFrame({
        "full_dataset_pct": full_pct,
        f"missing_{target_column}_pct": missing_pct,
    })
    comparison = comparison.fillna(0.0)
    comparison = comparison.assign(
        difference_pct_pts=(
            comparison[f"missing_{target_column}_pct"] - comparison["full_dataset_pct"]
        ).round(2)
    )
    comparison = comparison.sort_values("difference_pct_pts", ascending=False)
    return comparison


def main():
    file_path = sys.argv[1] if len(sys.argv) > 1 else "wildcat_loans_clean.csv"

    df = pd.read_csv(file_path)

    print("=" * 70)
    print("MISSING VALUES — COUNT AND PERCENTAGE BY COLUMN")
    print("=" * 70)
    print(missing_summary(df).to_string())

    n_missing = df[TARGET_COLUMN].isnull().sum()
    print(f"\nRows with missing '{TARGET_COLUMN}': {n_missing} "
          f"({n_missing / len(df) * 100:.2f}% of {len(df)} total rows)")

    for col in GROUP_COLUMNS:
        print("\n" + "=" * 70)
        print(f"{col.upper()} DISTRIBUTION: FULL DATASET vs. ROWS MISSING '{TARGET_COLUMN}'")
        print("=" * 70)
        print(distribution_comparison(df, col, TARGET_COLUMN).to_string())

    print("\n" + "=" * 70)
    print("HOW TO READ THIS")
    print("=" * 70)
    print(
        "If a category's percentage among missing rows is close to its percentage\n"
        "in the full dataset (small 'difference_pct_pts'), missingness looks random\n"
        "with respect to that variable (roughly MCAR). A large positive or negative\n"
        "difference means missing credit scores are concentrated in that category,\n"
        "suggesting the missingness is NOT random (MAR/MNAR) and may need targeted\n"
        "handling (e.g., group-specific imputation) rather than simple mean/median fill."
    )


if __name__ == "__main__":
    main()

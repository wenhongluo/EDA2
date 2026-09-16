"""
Check the dtype of origination_date in wildcat_loans_clean.csv, convert it to
datetime if it isn't already, and print before/after confirmation.

Usage:
    python convert_origination_date.py [path_to_csv]

If no path is given, defaults to "wildcat_loans_clean.csv" in the current directory.
"""

import sys
import pandas as pd

COLUMN = "origination_date"


def main():
    file_path = sys.argv[1] if len(sys.argv) > 1 else "wildcat_loans_clean.csv"

    df = pd.read_csv(file_path)

    before_dtype = df[COLUMN].dtype
    print(f"'{COLUMN}' dtype BEFORE: {before_dtype}")

    if pd.api.types.is_datetime64_any_dtype(df[COLUMN]):
        print(f"'{COLUMN}' is already stored as datetime — no conversion needed.")
    else:
        df = df.assign(**{COLUMN: pd.to_datetime(df[COLUMN])})
        after_dtype = df[COLUMN].dtype
        print(f"'{COLUMN}' dtype AFTER:  {after_dtype}")
        print(f"Converted '{COLUMN}' from {before_dtype} to {after_dtype}.")

    return df


if __name__ == "__main__":
    main()

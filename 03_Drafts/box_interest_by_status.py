"""
Create a horizontal box plot comparing interest_rate across the four
loan_status categories in wildcat_loans_clean.csv, and save it to
outputs/box_interest_by_status.png.

Usage:
    python box_interest_by_status.py [path_to_csv]

If no path is given, defaults to "wildcat_loans_clean.csv" in the current directory.
The output image is saved to "outputs/box_interest_by_status.png" (relative to
the current working directory), creating the outputs folder if needed.
"""

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

VALUE_COLUMN = "interest_rate"
GROUP_COLUMN = "loan_status"
CATEGORY_ORDER = ["Current", "Paid Off", "Delinquent", "Default"]
OUTPUT_PATH = os.path.join("outputs", "box_interest_by_status.png")


def main():
    file_path = sys.argv[1] if len(sys.argv) > 1 else "wildcat_loans_clean.csv"

    df = pd.read_csv(file_path)

    # Build the data in the desired category order, dropping missing values
    # per group so they don't distort the box plot.
    data = [
        df.loc[df[GROUP_COLUMN] == category, VALUE_COLUMN].dropna()
        for category in CATEGORY_ORDER
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    try:
        # matplotlib >= 3.9
        ax.boxplot(
            data,
            vert=False,
            tick_labels=CATEGORY_ORDER,
            patch_artist=True,
            boxprops=dict(facecolor="#4C72B0", alpha=0.7),
            medianprops=dict(color="#C44E52", linewidth=2),
        )
    except TypeError:
        # older matplotlib versions use `labels` instead of `tick_labels`
        ax.boxplot(
            data,
            vert=False,
            labels=CATEGORY_ORDER,
            patch_artist=True,
            boxprops=dict(facecolor="#4C72B0", alpha=0.7),
            medianprops=dict(color="#C44E52", linewidth=2),
        )

    ax.set_title("Interest Rate by Loan Status", fontsize=14)
    ax.set_xlabel("Interest Rate (%)")
    ax.set_ylabel("Loan Status")

    fig.tight_layout()

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    fig.savefig(OUTPUT_PATH, dpi=150)
    print(f"Saved box plot to: {OUTPUT_PATH}")

    print("\nMedian interest rate by loan status:")
    for category, series in zip(CATEGORY_ORDER, data):
        print(f"  {category:<12} n={len(series):>5}   median={series.median():.2f}%")


if __name__ == "__main__":
    main()

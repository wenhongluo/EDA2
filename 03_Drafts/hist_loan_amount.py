"""
Create a histogram of loan_amount from wildcat_loans_clean.csv, with vertical
lines marking the mean and median, and save it to outputs/hist_loan_amount.png.

Usage:
    python hist_loan_amount.py [path_to_csv]

If no path is given, defaults to "wildcat_loans_clean.csv" in the current directory.
The output image is saved to "outputs/hist_loan_amount.png" (relative to the
current working directory), creating the outputs folder if needed.
"""

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

COLUMN = "loan_amount"
N_BINS = 30
OUTPUT_PATH = os.path.join("outputs", "hist_loan_amount.png")


def main():
    file_path = sys.argv[1] if len(sys.argv) > 1 else "wildcat_loans_clean.csv"

    df = pd.read_csv(file_path)

    mean_val = df[COLUMN].mean()
    median_val = df[COLUMN].median()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df[COLUMN], bins=N_BINS, color="#4C72B0", edgecolor="white")

    ax.axvline(mean_val, color="#C44E52", linestyle="--", linewidth=2,
               label=f"Mean: ${mean_val:,.2f}")
    ax.axvline(median_val, color="#55A868", linestyle="--", linewidth=2,
               label=f"Median: ${median_val:,.2f}")

    ax.set_title("Distribution of Loan Amounts — Wildcat Capital Portfolio", fontsize=14)
    ax.set_xlabel("Loan Amount ($)")
    ax.set_ylabel("Number of Loans")
    ax.legend()

    fig.tight_layout()

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    fig.savefig(OUTPUT_PATH, dpi=150)
    print(f"Saved histogram to: {OUTPUT_PATH}")
    print(f"Mean loan amount:   ${mean_val:,.2f}")
    print(f"Median loan amount: ${median_val:,.2f}")


if __name__ == "__main__":
    main()

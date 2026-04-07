#!/usr/bin/env python3
"""
===========================================================
AF3 Analysis Pipeline
-----------------------------------------------------------
Author: Hadeer Elhabashy
Optimized and commented by ChatGPT (OpenAI)

Description:
    - Reads AF3 job list
    - Extracts best ranking sample per job
    - Loads AF3 confidence metrics (JSON)
    - Enriches dataset with ipTM / pTM / ranking metrics
    - Generates publication-quality histograms
    - Sorts final dataset by user-defined metric

===========================================================
"""

import os
import json
import pandas as pd
import matplotlib.pyplot as plt


# =========================================================
# USER CONFIGURATION (EDIT HERE ONLY)
# =========================================================

AF3_DIR = "/media/elhabashy/Elements/collaboration/Andrei_project/THET8/dataset/af3"

# Choose sorting metric: "ranking_score" OR "iptm"
SORT_BY = "iptm"

INPUT_FILE= "/media/elhabashy/Elements/collaboration/Andrei_project/THET8/about_dataset/test_data.tsv"
OUTPUT_DIR= "/media/elhabashy/Elements/collaboration/Andrei_project/THET8/about_dataset/"

# ---------------------------------------------------------
# Load JSON safely
# ---------------------------------------------------------
def load_json(json_path):
    """
    Load AF3 summary_confidences.json file.

    Parameters
    ----------
    json_path : str
        Path to JSON file

    Returns
    -------
    dict
        Parsed JSON content
    """
    with open(json_path, "r") as f:
        return json.load(f)


# ---------------------------------------------------------
# Plot histogram
# ---------------------------------------------------------
def plot_histogram(df, column, out_dir):
    """
    Create and save histogram (PNG + PDF).

    Parameters
    ----------
    df : pandas.DataFrame
    column : str
        Column to plot
    out_dir : str
    """

    plt.figure(figsize=(8, 6))

    plt.hist(
        df[column].dropna(),
        bins=30,
        range=(0, 1.1),
        color="#6BAED6",
        edgecolor="black"
    )

    plt.xlabel(column.replace("_", " ").title())
    plt.ylabel("Count")

    plt.tight_layout()

    png_path = os.path.join(out_dir, f"Af3screen_{column}_histo.png")
    pdf_path = os.path.join(out_dir, f"Af3screen_{column}_histo.pdf")

    plt.savefig(png_path, dpi=300)
    plt.savefig(pdf_path)

    plt.close()


# ---------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------
def main(AF3_DIR, sort_by):

    # =====================================================
    # Load input dataset
    # =====================================================
    list_path = os.path.join(
       INPUT_FILE
    )

    df = pd.read_csv(INPUT_FILE, sep=None, engine="python")

    print("\nDEBUG INFO")
    print("Columns:", df.columns.tolist())
    print(df.head())
    print("\n")

    # Ensure required columns exist
    for col in ["iptm", "ptm", "ranking_score",
                 "fraction_disordered", "has_clash", "sample"]:
        if col not in df.columns:
            df[col] = None

    af3_dir = os.path.join(AF3_DIR)

    # =====================================================
    # Loop over all jobs
    # =====================================================
    for i, row in df.iterrows():
        try:
            job = str(row["job_name"]).lower()
            print(f"Processing {i}: {job}")

            # -------------------------------------------------
            # Load ranking scores and select best sample
            # -------------------------------------------------
            ranking_file = os.path.join(af3_dir , job, "ranking_scores.csv")
            rank_df = pd.read_csv(ranking_file)

            best_row = rank_df.loc[rank_df["ranking_score"].idxmax()]
            sample = int(best_row["sample"])

            # -------------------------------------------------
            # Load AF3 confidence JSON
            # -------------------------------------------------
            json_file = os.path.join(
                af3_dir,
                job,
                f"seed-3141592_sample-{sample}",
                "summary_confidences.json"
            )

            af = load_json(json_file)

            # -------------------------------------------------
            # Store extracted metrics
            # -------------------------------------------------
            df.at[i, "iptm"] = af.get("iptm")
            df.at[i, "ptm"] = af.get("ptm")
            df.at[i, "ranking_score"] = af.get("ranking_score")
            df.at[i, "fraction_disordered"] = af.get("fraction_disordered")
            df.at[i, "has_clash"] = af.get("has_clash")
            df.at[i, "sample"] = sample

        except Exception as e:
            print(f"[ERROR] i={i}, job={row.get('job_name', 'NA')}: {e}")

    # =====================================================
    # Save enriched dataset
    # =====================================================
    out_csv = os.path.join(OUTPUT_DIR, f"AF3_results.csv")
    df.to_csv(out_csv, index=False)

    # =====================================================
    # Generate histograms
    # =====================================================
    plot_histogram(df, "ranking_score",OUTPUT_DIR)
    plot_histogram(df, "iptm", OUTPUT_DIR)

    # =====================================================
    # Sort final dataset
    # =====================================================
    sorted_df = df.sort_values(by=sort_by, ascending=False)

    sorted_out = os.path.join(OUTPUT_DIR, f"AF3_results_by_{sort_by}.csv")
    sorted_df.to_csv(sorted_out, index=False)

    # =====================================================
    # Summary output
    # =====================================================
    print("\n===================================================")
    print("DONE ✔")
    print(f"Enriched dataset: {out_csv}")
    print(f"Sorted dataset:   {sorted_out}")
    print(f"Sorting metric:   {sort_by}")
    print("===================================================\n")


# ---------------------------------------------------------
# Run pipeline
# ---------------------------------------------------------
if __name__ == "__main__":
    main(AF3_DIR, SORT_BY)

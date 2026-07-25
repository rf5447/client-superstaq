# import os
# import pandas as pd

# # ------------------------------------------------------------
# # Input files
# # ------------------------------------------------------------

# INPUT_FILES = [
#     "benchmark_results_combined/ghz_benchmark_results_combined.csv",
#     "benchmark_results_combined/mb_benchmark_results_combined.csv",
#     "benchmark_results_combined/bitcode_benchmark_results_combined.csv",
#     "benchmark_results_combined/phasecode_benchmark_results_combined.csv",
#     "benchmark_results_combined/hamsim_benchmark_results_combined.csv",
#     "benchmark_results_combined/vqeproxy_benchmark_results_combined.csv",
#     "benchmark_results_combined/vanilla_qaoa_benchmark_results_combined.csv",
#     "benchmark_results_combined/fswap_qaoa_benchmark_results_combined.csv",
# ]

# # ------------------------------------------------------------
# # Backend mapping
# # ------------------------------------------------------------

# BACKEND_MAP = {
#     "ibm_kingston": "kingston",
#     "ibm_marrakesh": "marrakesh",
#     "ibm_fez": "fez",
#     "ibm_torino": "torino",
# }

# ROW_ORDER = ["torino", "fez", "kingston", "marrakesh"]

# # ------------------------------------------------------------
# # Build label from each CSV row
# # using the naming style from your feature code
# # ------------------------------------------------------------

# def make_label(row: pd.Series) -> str:
#     benchmark = str(row["benchmark"]).strip().lower()

#     if benchmark == "ghz":
#         nq = int(row["n_qubits"])
#         return f"ghz_{nq}qubits"

#     elif benchmark == "merminbell":
#         nq = int(row["n_qubits"])
#         return f"mb_{nq}qubits"

#     elif benchmark == "bitcode":
#         nq = int(row["n_qubits"])
#         nr = int(row["n_rounds"])
#         return f"bitcode_{nq}data_{nr}rounds"

#     elif benchmark == "phasecode":
#         nq = int(row["n_qubits"])
#         nr = int(row["n_rounds"])
#         return f"phasecode_{nq}data_{nr}rounds"

#     elif benchmark == "hamiltoniansimulation":
#         nq = int(row["n_qubits"])
#         ts = int(row["ts"])
#         tt = int(row["tt"])
#         return f"hamsim_{nq}qubits_{ts}ts_{tt}tt"

#     elif benchmark == "vqeproxy":
#         nq = int(row["n_qubits"])
#         nl = int(row["n_layers"])
#         return f"vqe_{nq}qubits_{nl}layers"

#     elif benchmark == "qaoa_vanilla":
#         nq = int(row["n_qubits"])
#         return f"vanilla_{nq}qubits"

#     elif benchmark == "qaoa_fswap":
#         nq = int(row["n_qubits"])
#         return f"fswap_{nq}qubits"

#     else:
#         raise ValueError(f"Unknown benchmark name: {row['benchmark']}")

# # ------------------------------------------------------------
# # Read files and collect scores
# # ------------------------------------------------------------

# records = []

# for filepath in INPUT_FILES:
#     print(f"Processing {filepath}...")
#     if not os.path.exists(filepath):
#         print(f"Warning: file not found, skipping: {filepath}")
#         continue

#     df = pd.read_csv(filepath)

#     required_cols = {"benchmark", "backend", "score"}
#     missing = required_cols - set(df.columns)
#     if missing:
#         raise ValueError(f"{filepath} is missing required columns: {missing}")

#     # keep only the IBM backends you want
#     df = df[df["backend"].isin(BACKEND_MAP.keys())].copy()
#     if df.empty:
#         continue

#     df["backend_short"] = df["backend"].map(BACKEND_MAP)
#     df["label"] = df.apply(make_label, axis=1)

#     for _, row in df.iterrows():
#         records.append({
#             "backend": row["backend_short"],
#             "label": row["label"],
#             "score": float(row["score"]),
#         })

#     print(f"Done with {filepath}, found {len(df)} valid rows.")

# if not records:
#     raise ValueError("No usable rows found in the input CSV files.")

# all_scores = pd.DataFrame(records)

# # ------------------------------------------------------------
# # If duplicates exist for same backend/label, average them
# # Also save std and number of runs
# # ------------------------------------------------------------

# agg_scores = (
#     all_scores.groupby(["backend", "label"], as_index=False)
#     .agg(
#         score_mean=("score", "mean"),
#         score_std=("score", "std"),
#         n_runs=("score", "count"),
#     )
# )

# agg_scores["score_std"] = agg_scores["score_std"].fillna(0)

# # ------------------------------------------------------------
# # Pivot into final matrix using the mean scores
# # ------------------------------------------------------------

# final_df = agg_scores.pivot(index="backend", columns="label", values="score_mean")

# # desired row order
# final_df = final_df.reindex(ROW_ORDER)

# # optional: sort columns alphabetically
# final_df = final_df.reindex(sorted(final_df.columns), axis=1)

# final_df.index.name = ""
# final_df.columns.name = ""

# # ------------------------------------------------------------
# # Save
# # ------------------------------------------------------------

# final_df.to_csv("combined_benchmark_scores.csv")
# final_df.to_pickle("combined_benchmark_scores.pickle")

# agg_scores.to_csv("combined_benchmark_scores_aggregated_stats.csv", index=False)
# agg_scores.to_pickle("combined_benchmark_scores_aggregated_stats.pickle")

# print("Saved:")
# print("  combined_benchmark_scores.csv")
# print("  combined_benchmark_scores.pickle")
# print("  combined_benchmark_scores_aggregated_stats.csv")
# print("  combined_benchmark_scores_aggregated_stats.pickle")
# print()
# print(final_df)

import os
import pandas as pd

# ------------------------------------------------------------
# Input files
# ------------------------------------------------------------

INPUT_FILES = [
    "benchmark_results_combined/ghz_benchmark_results_combined.csv",
    "benchmark_results_combined/mb_benchmark_results_combined.csv",
    "benchmark_results_combined/bitcode_benchmark_results_combined.csv",
    "benchmark_results_combined/phasecode_benchmark_results_combined.csv",
    "benchmark_results_combined/hamsim_benchmark_results_combined.csv",
    "benchmark_results_combined/vqeproxy_benchmark_results_combined.csv",
    "benchmark_results_combined/vanilla_qaoa_benchmark_results_combined.csv",
    "benchmark_results_combined/fswap_qaoa_benchmark_results_combined.csv",
]

# ------------------------------------------------------------
# Backend mapping
# ------------------------------------------------------------

BACKEND_MAP = {
    "ibm_kingston": "kingston",
    "ibm_marrakesh": "marrakesh",
    "ibm_fez": "fez",
    "ibm_torino": "torino",
}

ROW_ORDER = ["torino", "fez", "kingston", "marrakesh"]

# ------------------------------------------------------------
# Build label from each CSV row
# using the naming style from your feature code
# ------------------------------------------------------------

def make_label(row: pd.Series) -> str:
    benchmark = str(row["benchmark"]).strip().lower()

    if benchmark == "ghz":
        nq = int(row["n_qubits"])
        method = str(row["method"]).strip().lower()
        return f"ghz_{nq}qubits_{method}"

    elif benchmark == "merminbell":
        nq = int(row["n_qubits"])
        return f"mb_{nq}qubits"

    elif benchmark == "bitcode":
        nq = int(row["n_qubits"])
        nr = int(row["n_rounds"])
        return f"bitcode_{nq}data_{nr}rounds"

    elif benchmark == "phasecode":
        nq = int(row["n_qubits"])
        nr = int(row["n_rounds"])
        return f"phasecode_{nq}data_{nr}rounds"

    elif benchmark == "hamiltoniansimulation":
        nq = int(row["n_qubits"])
        ts = int(row["ts"])
        tt = int(row["tt"])
        return f"hamsim_{nq}qubits_{ts}ts_{tt}tt"

    elif benchmark == "vqeproxy":
        nq = int(row["n_qubits"])
        nl = int(row["n_layers"])
        return f"vqe_{nq}qubits_{nl}layers"

    elif benchmark == "qaoa_vanilla":
        nq = int(row["n_qubits"])
        return f"vanilla_{nq}qubits"

    elif benchmark == "qaoa_fswap":
        nq = int(row["n_qubits"])
        return f"fswap_{nq}qubits"

    else:
        raise ValueError(f"Unknown benchmark name: {row['benchmark']}")

# ------------------------------------------------------------
# Read files and collect scores
# ------------------------------------------------------------

records = []

for filepath in INPUT_FILES:
    print(f"Processing {filepath}...")

    if not os.path.exists(filepath):
        print(f"Warning: file not found, skipping: {filepath}")
        continue

    df = pd.read_csv(filepath)

    required_cols = {"benchmark", "backend", "score"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"{filepath} is missing required columns: {missing}")

    # GHZ now requires method so ladder/star/logdepth do not get averaged together
    if "ghz" in os.path.basename(filepath).lower() and "method" not in df.columns:
        raise ValueError(f"{filepath} is GHZ but missing required column: method")

    # keep only IBM backends
    df = df[df["backend"].isin(BACKEND_MAP.keys())].copy()
    if df.empty:
        continue

    df["backend_short"] = df["backend"].map(BACKEND_MAP)
    df["label"] = df.apply(make_label, axis=1)

    for _, row in df.iterrows():
        records.append({
            "backend": row["backend_short"],
            "label": row["label"],
            "score": float(row["score"]),
        })

    print(f"Done with {filepath}, found {len(df)} valid rows.")

if not records:
    raise ValueError("No usable rows found in the input CSV files.")

all_scores = pd.DataFrame(records)

# ------------------------------------------------------------
# If duplicates exist for same backend/label, average them
# Also save std and number of runs
# ------------------------------------------------------------

agg_scores = (
    all_scores
    .groupby(["backend", "label"], as_index=False)
    .agg(
        score_mean=("score", "mean"),
        score_std=("score", "std"),
        n_runs=("score", "count"),
    )
)

agg_scores["score_std"] = agg_scores["score_std"].fillna(0)

# ------------------------------------------------------------
# Pivot into final matrix using the mean scores
# ------------------------------------------------------------

final_df = agg_scores.pivot(
    index="backend",
    columns="label",
    values="score_mean",
)

final_df = final_df.reindex(ROW_ORDER)
final_df = final_df.reindex(sorted(final_df.columns), axis=1)

final_df.index.name = ""
final_df.columns.name = ""

# ------------------------------------------------------------
# Save
# ------------------------------------------------------------

final_df.to_csv("combined_benchmark_scores.csv")
final_df.to_pickle("combined_benchmark_scores.pickle")

agg_scores.to_csv("combined_benchmark_scores_aggregated_stats.csv", index=False)
agg_scores.to_pickle("combined_benchmark_scores_aggregated_stats.pickle")

print("Saved:")
print("  combined_benchmark_scores.csv")
print("  combined_benchmark_scores.pickle")
print("  combined_benchmark_scores_aggregated_stats.csv")
print("  combined_benchmark_scores_aggregated_stats.pickle")
print()
print(final_df)

# Optional sanity check
print("\nGHZ columns:")
for col in final_df.columns:
    if col.startswith("ghz_"):
        print(col)
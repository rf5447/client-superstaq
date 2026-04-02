# import json
# import os
# import csv
# from supermarq import converters
# import supermarq
# import cirq
# from qiskit import qasm2, qasm3, transpile

# # Configuration
# input_directory = "mb_ibm" 
# output_csv = "mb_benchmark_results.csv"

# # CSV Column Headers
# headers = [
#     "benchmark", 
#     "n_qubits", 
#     "backend", 
#     "shots", 
#     "score", 
#     "job_id", 
#     "timestamp"
# ]

# all_rows = []

# # Ensure directory exists
# if not os.path.exists(input_directory):
#     print(f"Error: Folder '{input_directory}' not found.")
# else:
#     # Iterate through all JSON files in the directory
#     for filename in os.listdir(input_directory):
#         if filename.endswith(".json"):
#             file_path = os.path.join(input_directory, filename)
            
#             try:
#                 with open(file_path, "r", encoding="utf-8") as f:
#                     data = json.load(f)
                
#                 # 1. Extract parameters to initialize the MerminBell object
#                 n_qubits = data["n_qubits"]
#                 counts = data["counts"]
                
#                 # Reverse each bitstring to convert Little-Endian (IBM) to Big-Endian (SupermarQ)
#                 corrected_counts = {bitstr[::-1]: count for bitstr, count in counts.items()}
                
#                 # 2. Initialize the specific MerminBell benchmark to use its .score() method
#                 mb_benchmark = supermarq.mermin_bell.MerminBell(n_qubits)
                
#                 # 3. Calculate score
#                 # run_score = mb_benchmark.score(counts)
#                 run_score = mb_benchmark.score(corrected_counts)

#                 # 4. Prepare the row for CSV
#                 row = {
#                     "benchmark": data.get("benchmark", "MerminBell"),
#                     "n_qubits": n_qubits,
#                     "backend": data.get("backend"),
#                     "shots": data.get("shots"),
#                     "score": run_score,
#                     "job_id": data.get("job_id"),
#                     "timestamp": data.get("timestamp")
#                 }
#                 all_rows.append(row)
#                 print(f"Processed {filename}: Score = {run_score:.4f}")
                
#             except Exception as e:
#                 print(f"Failed to process {filename}: {e}")

# # Write the aggregated data to a single CSV
# with open(output_csv, "w", newline="", encoding="utf-8") as f:
#     writer = csv.DictWriter(f, fieldnames=headers)
#     writer.writeheader()
#     writer.writerows(all_rows)

# print(f"\nSuccess! Aggregated {len(all_rows)} runs into '{output_csv}'.")
# import json
# import os
# import csv
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import numpy as np
# import supermarq

# # --- 1. DATA PROCESSING ---
# input_directory = "mb_ibm" 
# output_csv = "mb_benchmark_results.csv"
# headers = ["benchmark", "n_qubits", "backend", "shots", "score", "job_id", "timestamp"]
# all_rows = []

# if not os.path.exists(input_directory):
#     print(f"Error: Folder '{input_directory}' not found.")
# else:
#     for filename in os.listdir(input_directory):
#         if filename.endswith(".json"):
#             file_path = os.path.join(input_directory, filename)
#             try:
#                 with open(file_path, "r", encoding="utf-8") as f:
#                     data = json.load(f)
                
#                 n_qubits = data["n_qubits"]
#                 counts = data["counts"]
                
#                 # Reverse bitstrings (IBM Little-Endian to SupermarQ Big-Endian)
#                 corrected_counts = {bitstr[::-1]: count for bitstr, count in counts.items()}
                
#                 # Initialize benchmark and calculate score
#                 mb_benchmark = supermarq.mermin_bell.MerminBell(n_qubits)
#                 run_score = mb_benchmark.score(corrected_counts)

#                 all_rows.append({
#                     "benchmark": data.get("benchmark", "MerminBell"),
#                     "n_qubits": n_qubits,
#                     "backend": data.get("backend"),
#                     "shots": data.get("shots"),
#                     "score": run_score,
#                     "job_id": data.get("job_id"),
#                     "timestamp": data.get("timestamp")
#                 })
#             except Exception as e:
#                 print(f"Failed to process {filename}: {e}")

# # Save to CSV
# df = pd.DataFrame(all_rows)
# df.to_csv(output_csv, index=False)
# print(f"Success! Aggregated {len(all_rows)} runs into '{output_csv}'.")

# # Ensure numeric types
# df['n_qubits'] = pd.to_numeric(df['n_qubits'])
# df['score'] = pd.to_numeric(df['score'])

# # --- 2. PREPARE PLOTTING DATA (WITH CLASSICAL LIMIT) ---

# # Generate Classical Limit rows based on: (f(n) + 2^(n-1)) / 2^n
# extra_rows = []
# for n in sorted(df['n_qubits'].unique()):
#     f_n = 2**((n - (n % 2)) // 2)
#     classical_ratio = (f_n + 2**(n - 1)) / (2**n)
    
#     extra_rows.append({
#         "benchmark": "MerminBell",
#         "n_qubits": n,
#         "backend": "Classical Limit", 
#         "score": classical_ratio
#     })

# # Merge hardware data with classical limit data
# df_plot = pd.concat([df, pd.DataFrame(extra_rows)], ignore_index=True)

# # --- 3. PLOT 1: LINE CHART ---
# sns.set_theme(style="whitegrid")
# fig1, ax1 = plt.subplots(figsize=(10, 6))
# fig1.suptitle('SupermarQ Mermin-Bell: Hellinger Fidelity', fontsize=16, fontweight='bold')

# sns.lineplot(data=df, x='n_qubits', y='score', hue='backend', marker='o', ax=ax1, linewidth=2.5)
# ax1.set_ylim(-0.05, 1.05)
# ax1.set_ylabel("Score")
# plt.tight_layout(rect=[0, 0.03, 1, 0.95])
# plt.savefig("mb_performance_comparison.png", dpi=300)
# plt.show()

# # --- 4. PLOT 2: BAR CHART (WITH CLASSICAL LIMIT BARS) ---
# sns.set_theme(style="white")
# fig2, ax2 = plt.subplots(figsize=(12, 6))
# qubit_counts = sorted(df['n_qubits'].unique())
# custom_palette = sns.color_palette("tab10", len(qubit_counts))

# sns.barplot(
#     data=df_plot,      # Using the merged data
#     x='backend',
#     y='score',
#     hue='n_qubits',
#     palette=custom_palette,
#     ax=ax2,
#     edgecolor='gray'
# )

# ax2.set_title("Mermin-Bell: Hardware vs. Classical Limit", fontsize=15, fontweight='bold', pad=20)
# ax2.set_ylim(0, 1.05)
# ax2.set_ylabel("Score")
# ax2.legend(title="Qubits", loc='lower right')
# ax2.axhline(0, color='black', linewidth=0.8)

# # Optional: Add a dashed line at 1.0 to show the theoretical quantum max
# ax2.axhline(1.0, color='green', linestyle='--', alpha=0.3, label="Ideal Max")

# plt.tight_layout()
# plt.savefig("mb_bar_charts.png", dpi=300)
# plt.show()

import json
import os
import csv
import pandas as pd
import matplotlib
# matplotlib.use('Agg') # Necessary for Slurm
import matplotlib.pyplot as plt
import seaborn as sns
import supermarq

# --- 1. CONFIGURATION ---
input_directory = "mb_ibm" 
output_csv = "mb_benchmark_results.csv"
headers = ["benchmark", "n_qubits", "backend", "shots", "score", "job_id", "timestamp"]

# EXACT FILENAMES TO PROCESS
target_files = [
    "mb_20_ibm_torino.json",
    "mb_20_ibm_marrakesh.json"
]

new_rows = []

# --- 2. DATA PROCESSING ---
print("Starting targeted processing for 20-qubit runs...")

for filename in target_files:
    file_path = os.path.join(input_directory, filename)
    
    if not os.path.exists(file_path):
        print(f"Warning: File {file_path} not found. Skipping.")
        continue

    try:
        print(f"Scoring {filename}... (This may take a few minutes for 20 qubits)")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        counts = data["counts"]
        # IBM Little-Endian to SupermarQ Big-Endian
        corrected_counts = {bitstr[::-1]: count for bitstr, count in counts.items()}
        
        # Calculate SupermarQ score
        mb_benchmark = supermarq.mermin_bell.MerminBell(data["n_qubits"])
        run_score = mb_benchmark.score(corrected_counts)

        new_rows.append({
            "benchmark": data.get("benchmark", "MerminBell"),
            "n_qubits": data["n_qubits"],
            "backend": data.get("backend"),
            "shots": data.get("shots"),
            "score": run_score,
            "job_id": data.get("job_id"),
            "timestamp": data.get("timestamp")
        })
        print(f"Successfully scored {filename}: {run_score}")

    except Exception as e:
        print(f"Failed to process {filename}: {e}")

# --- 3. APPEND TO CSV ---
if new_rows:
    with open(output_csv, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writerows(new_rows)
    print(f"\nSuccess! Added {len(new_rows)} rows to {output_csv}")
else:
    print("\nNo new data was added. Check if the files exist in mb_ibm/.")

# --- 4. REGENERATE PLOTS ---
if os.path.exists(output_csv):
    print("Regenerating plots with full dataset...")
    df = pd.read_csv(output_csv)
    df['n_qubits'] = pd.to_numeric(df['n_qubits'])
    df['score'] = pd.to_numeric(df['score'])

    # Line Chart
    sns.set_theme(style="whitegrid")
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=df, x='n_qubits', y='score', hue='backend', marker='o', ax=ax1)
    ax1.set_ylim(-0.05, 1.05)
    plt.savefig("mb_performance_comparison.png", dpi=300)
    print("Updated: mb_performance_comparison.png")
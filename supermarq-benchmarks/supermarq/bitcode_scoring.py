import json
import os
import csv
import supermarq
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration
input_directory = "ibmk/bitcode_ibmk"
output_csv = "benchmark_resultsk/bitcode_benchmark_results.csv"

# Updated CSV Column Headers
headers = ["benchmark", "n_qubits", "n_rounds", "bit_state", "backend", "shots", "score", "job_id", "timestamp"]

all_rows = []

if not os.path.exists(input_directory):
    print(f"Error: Folder '{input_directory}' not found.")
else:
    for filename in os.listdir(input_directory):
        if filename.endswith(".json"):
            file_path = os.path.join(input_directory, filename)
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                nq = data["n_qubits"]
                nr = data["n_rounds"]
                bit_state = data["bit_state"]
                counts = data["counts"]
                
                pc_benchmark = supermarq.bit_code.BitCode(nq, nr, bit_state)
                corrected_counts = {bitstr[::-1]: count for bitstr, count in counts.items()}
                run_score = pc_benchmark.score(corrected_counts)
                
                row = {
                    "benchmark": data.get("benchmark", "BitCode"),
                    "n_qubits": nq,
                    "n_rounds": nr,
                    "bit_state": str(bit_state), 
                    "backend": data.get("backend"),
                    "shots": data.get("shots"),
                    "score": run_score,
                    "job_id": data.get("job_id"),
                    "timestamp": data.get("timestamp")
                }
                all_rows.append(row)
                print(f"Processed {filename}: Score = {run_score:.4f}")
                
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

# Save to CSV
with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(all_rows)

# # --- DATA PREP FOR PLOTTING ---
# # --- DATA PREP FOR PLOTTING ---
# df = pd.DataFrame(all_rows)
# df['n_qubits'] = pd.to_numeric(df['n_qubits'])
# df['score'] = pd.to_numeric(df['score'])
# df['n_rounds'] = pd.to_numeric(df['n_rounds'])

# # Sort for consistent legend ordering
# df = df.sort_values(['n_qubits', 'n_rounds'])
# rounds_list = sorted(df['n_rounds'].unique())
# qubits_list = sorted(df['n_qubits'].unique())

# # --- PLOT 1: LINE PERFORMANCE COMPARISON ---
# sns.set_theme(style="whitegrid")
# fig1, axes1 = plt.subplots(1, len(rounds_list), figsize=(18, 6), sharey=True, squeeze=False)
# fig1.suptitle('Bit Code: Score Trends by Rounds', fontsize=18, fontweight='bold')

# for i, nr in enumerate(rounds_list):
#     ax = axes1[0][i]
#     round_data = df[df['n_rounds'] == nr]
#     sns.lineplot(data=round_data, x='n_qubits', y='score', hue='backend', marker='o', ax=ax, linewidth=2.5)
#     ax.set_title(f"{nr} Rounds", fontsize=14)
#     ax.set_ylim(-0.05, 1.05)

# plt.tight_layout(rect=[0, 0.03, 1, 0.95])
# plt.savefig("bitcode_performance_comparison.png", dpi=300)
# print("Saved: bitcode_performance_comparison.png")

# # --- PLOT 2: BAR CHARTS BY BACKEND (UPDATED) ---
# sns.set_theme(style="white")

# # Create the combined label for the legend: "X-data qubits, Y-rounds"
# df['label'] = df['n_qubits'].astype(str) + "-data qubits, " + df['n_rounds'].astype(str) + "-rounds"
# # Sort to ensure consistent bar order (e.g., 3q before 5q)
# df = df.sort_values(['n_qubits', 'n_rounds'])

# plt.figure(figsize=(15, 6))

# # Custom palette to match the provided reference image colors
# custom_palette = ['#3274A1', '#E1812C', '#3A923A', '#C03D3E']

# ax2 = sns.barplot(
#     data=df, 
#     x='backend', 
#     y='score', 
#     hue='label', 
#     palette=custom_palette[:len(df['label'].unique())], 
#     edgecolor='gray',
#     capsize=.1,
#     errwidth=1.5
# )

# # Formatting to match reference image
# plt.title("(Bit Code", fontsize=20, y=-0.2)
# plt.xlabel("Backend", fontsize=12)
# plt.ylabel("Score", fontsize=12)
# plt.ylim(0, 1.05)
# plt.legend(title="", ncol=2, loc='upper right', frameon=True)
# plt.axhline(0, color='black', linewidth=0.8)

# plt.tight_layout()
# plt.savefig("bitcode_bar_charts.png", dpi=300)
# print("Saved: bitcode_bar_charts.png")
# plt.show()
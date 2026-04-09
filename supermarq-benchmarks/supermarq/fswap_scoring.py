import json
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import supermarq

# Configuration
input_directory = "fswap_ibm" 
output_csv = "fswap_qaoa_benchmark_results.csv"

# CSV Column Headers
headers = [
    "benchmark", 
    "n_qubits", 
    "backend", 
    "shots", 
    "score", 
    "job_id", 
    "timestamp"
]

all_rows = []

# Ensure directory exists
if not os.path.exists(input_directory):
    print(f"Error: Folder '{input_directory}' not found.")
else:
    for filename in os.listdir(input_directory):
        if filename.endswith(".json"):
            file_path = os.path.join(input_directory, filename)
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                # 1. Extract parameters
                n_qubits = data["n_qubits"]
                counts = data["counts"]
                
                # 2. Initialize the Fermionic Swap QAOA benchmark
                qaoa_benchmark = supermarq.qaoa_fermionic_swap_proxy.QAOAFermionicSwapProxy(n_qubits)
                
                # 3. Calculate score
                # The FSWAP proxy requires bitstring reversal to account for the SWAP network 
                # mapping vs the standard measurement order.
                
                # +1 is without this line, -1 is with
                corrected_counts = {bitstr[::-1]: count for bitstr, count in counts.items()}
                run_score = qaoa_benchmark.score(corrected_counts)
                
                # 4. Prepare the row for CSV
                row = {
                    "benchmark": "QAOA_FSWAP",
                    "n_qubits": n_qubits,
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

# Write results
df = pd.DataFrame(all_rows)
df.to_csv(output_csv, index=False)

# --- PLOT 1: LINE PLOT ---
df['n_qubits'] = pd.to_numeric(df['n_qubits'])
df['score'] = pd.to_numeric(df['score'])

sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(1, 1, figsize=(8, 6))
fig.suptitle('SupermarQ FSWAP QAOA', fontsize=18, fontweight='bold')

sns.lineplot(
    data=df, 
    x='n_qubits', 
    y='score', 
    hue='backend', 
    marker='o', 
    ax=axes,
    linewidth=2.5,
    markersize=8
)

axes.set_title("Method: Fermionic Swap", fontsize=14, fontweight='semibold')
axes.set_xlabel("Number of Qubits", fontsize=12)
axes.set_ylabel("Score", fontsize=12)
axes.set_ylim(-0.05, 1.05)
axes.legend(title="IBM Backend", frameon=True)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("fswap_performance_line.png", dpi=300)
plt.show()

# --- PLOT 2: BAR CHART ---
sns.set_theme(style="white") 
qubit_counts = sorted(df['n_qubits'].unique())

fig, ax = plt.subplots(1, 1, figsize=(10, 6))
custom_palette = sns.color_palette("tab10", len(qubit_counts))

sns.barplot(
    data=df,
    x='backend',
    y='score',
    hue='n_qubits',
    palette=custom_palette,
    ax=ax,
    edgecolor='gray',
    capsize=.1,
    errwidth=1.5 
)

ax.set_title("QAOA Method: FSWAP", fontsize=15, fontweight='bold', pad=20)
ax.set_xlabel("Backend", fontsize=12)
ax.set_ylabel("Score", fontsize=12)
ax.set_ylim(0, 1.05)
ax.legend(title="Qubits", loc='lower right')
ax.axhline(0, color='black', linewidth=0.8)

plt.tight_layout()
plt.savefig("fswap_bar_charts.png", dpi=300)
print(f"\nBar chart saved successfully as 'fswap_bar_charts.png'")
plt.show()
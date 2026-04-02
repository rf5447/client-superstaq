import json
import os
import csv
import supermarq
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration
input_directory = "hamsim_ibm" 
output_csv = "hamsim_benchmark_results.csv"

# Updated CSV Column Headers for Hamiltonian Simulation
headers = ["benchmark", "n_qubits", "ts", "tt", "backend", "shots", "score", "job_id", "timestamp"]

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
                
                # Hamiltonian Simulation Features
                nq = data["n_qubits"]
                ts = data["ts"]
                tt = data["tt"]
                counts = data["counts"]
                
                # Instantiate Hamiltonian Simulation benchmark
                pc_benchmark = supermarq.hamiltonian_simulation.HamiltonianSimulation(nq, ts, tt)
                
                # Most IBM backends require bitstring reversal (endianness) for Supermarq
                corrected_counts = {bitstr[::-1]: count for bitstr, count in counts.items()}
                run_score = pc_benchmark.score(corrected_counts)
                
                row = {
                    "benchmark": data.get("benchmark", "HamiltonianSimulation"),
                    "n_qubits": nq,
                    "ts": ts,
                    "tt": tt, 
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

# --- DATA PREP FOR PLOTTING ---
df = pd.DataFrame(all_rows)
df['n_qubits'] = pd.to_numeric(df['n_qubits'])
df['score'] = pd.to_numeric(df['score'])
df['ts'] = pd.to_numeric(df['ts'])

# Create label: "X-qubits, Y-steps"
df['label'] = df['n_qubits'].astype(str) + "q, " + df['ts'].astype(str) + " steps"
df = df.sort_values(['n_qubits', 'ts'])


# Define your preferred fixed order
backend_order = ["ibm_fez", "ibm_marrakesh", "ibm_torino"]

# --- PLOT: BAR CHARTS BY BACKEND ---
sns.set_theme(style="white")
plt.figure(figsize=(15, 6))

# Get unique labels in sorted order to ensure consistent rotation
unique_labels = df.sort_values(['n_qubits', 'ts'])['label'].unique()

# Generate a rotating palette using tab10 (repeating every 5)
tab10 = plt.cm.get_cmap('tab10').colors
rotating_palette = {label: tab10[i % 5] for i, label in enumerate(unique_labels)}

ax2 = sns.barplot(
    data=df, 
    x='backend', 
    y='score', 
    hue='label', 
    order=backend_order,      # Applies your fixed backend order
    hue_order=unique_labels,   # Ensures labels stay in order
    palette=rotating_palette,  # Uses the 5-color rotation
    edgecolor='gray'
)

plt.title("Hamiltonian Simulation Performance", fontsize=20)
plt.xlabel("Backend", fontsize=12)
plt.ylabel("Score", fontsize=12)
plt.ylim(0, 1.05)
plt.legend(title="Configuration", ncol=2, loc='upper right', frameon=True)

plt.tight_layout()
plt.savefig("hamsim_performance.png", dpi=300)
print("Saved: hamsim_performance.png")
plt.show()
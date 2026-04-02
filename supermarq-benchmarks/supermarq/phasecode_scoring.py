import json
import os
import csv
import supermarq
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration
input_directory = "phasecode_ibm" 
output_csv = "phasecode_benchmark_results.csv"

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
                
                pc_benchmark = supermarq.phase_code.PhaseCode(nq, nr, bit_state)
                corrected_counts = {bitstr[::-1]: count for bitstr, count in counts.items()}
                run_score = pc_benchmark.score(corrected_counts)
                
                row = {
                    "benchmark": data.get("benchmark", "PhaseCode"),
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

# --- DATA PREP FOR PLOTTING ---
# --- DATA PREP FOR PLOTTING ---
df = pd.DataFrame(all_rows)
df['n_qubits'] = pd.to_numeric(df['n_qubits'])
df['score'] = pd.to_numeric(df['score'])
df['n_rounds'] = pd.to_numeric(df['n_rounds'])

# Sort for consistent legend ordering
df = df.sort_values(['n_qubits', 'n_rounds'])
rounds_list = sorted(df['n_rounds'].unique())
qubits_list = sorted(df['n_qubits'].unique())

# --- PLOT 1: LINE PERFORMANCE COMPARISON ---
sns.set_theme(style="whitegrid")
fig1, axes1 = plt.subplots(1, len(rounds_list), figsize=(18, 6), sharey=True, squeeze=False)
fig1.suptitle('Phase Code: Score Trends by Rounds', fontsize=18, fontweight='bold')

for i, nr in enumerate(rounds_list):
    ax = axes1[0][i]
    round_data = df[df['n_rounds'] == nr]
    sns.lineplot(data=round_data, x='n_qubits', y='score', hue='backend', marker='o', ax=ax, linewidth=2.5)
    ax.set_title(f"{nr} Rounds", fontsize=14)
    ax.set_ylim(-0.05, 1.05)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("phasecode_performance_comparison.png", dpi=300)
print("Saved: phasecode_performance_comparison.png")

# --- PLOT 2: BAR CHARTS BY BACKEND (UPDATED) ---
sns.set_theme(style="white")

# Create the combined label for the legend: "X-data qubits, Y-rounds"
df['label'] = df['n_qubits'].astype(str) + "-data qubits, " + df['n_rounds'].astype(str) + "-rounds"
# Sort to ensure consistent bar order (e.g., 3q before 5q)
df = df.sort_values(['n_qubits', 'n_rounds'])

plt.figure(figsize=(15, 6))

# Custom palette to match the provided reference image colors
custom_palette = ['#3274A1', '#E1812C', '#3A923A', '#C03D3E']

ax2 = sns.barplot(
    data=df, 
    x='backend', 
    y='score', 
    hue='label', 
    palette=custom_palette[:len(df['label'].unique())], 
    edgecolor='gray',
    capsize=.1,
    errwidth=1.5
)

# Formatting to match reference image
plt.title("(Phase Code", fontsize=20, y=-0.2)
plt.xlabel("Backend", fontsize=12)
plt.ylabel("Score", fontsize=12)
plt.ylim(0, 1.05)
plt.legend(title="", ncol=2, loc='upper right', frameon=True)
plt.axhline(0, color='black', linewidth=0.8)

plt.tight_layout()
plt.savefig("phasecode_bar_charts.png", dpi=300)
print("Saved: phasecode_bar_charts.png")
plt.show()

# --- PLOT 3: SUBFIGS BY ROUNDS (NQ on same chart) ---
sns.set_theme(style="whitegrid")
fig3, axes3 = plt.subplots(1, len(rounds_list), figsize=(6 * len(rounds_list), 6), sharey=True, squeeze=False)

for i, nr in enumerate(rounds_list):
    ax = axes3[0][i]
    round_data = df[df['n_rounds'] == nr]
    sns.barplot(data=round_data, x='backend', y='score', hue='n_qubits', palette="tab10", ax=ax, edgecolor='gray')
    ax.set_title(f"Rounds: {nr}", fontsize=15, fontweight='bold')
    ax.set_ylim(0, 1.05)
    ax.legend(title="Qubits")
    if i != 0: ax.set_ylabel("")

plt.tight_layout()
plt.savefig("phasecode_by_rounds.png", dpi=300)
print("Saved: phasecode_by_rounds.png")

# --- PLOT 4: SUBFIGS BY QUBITS (NR on same chart) ---
sns.set_theme(style="whitegrid")
fig4, axes4 = plt.subplots(1, len(qubits_list), figsize=(6 * len(qubits_list), 6), sharey=True, squeeze=False)

for i, nq in enumerate(qubits_list):
    ax = axes4[0][i]
    qubit_data = df[df['n_qubits'] == nq]
    sns.barplot(data=qubit_data, x='backend', y='score', hue='n_rounds', palette="tab10", ax=ax, edgecolor='gray')
    ax.set_title(f"Qubits: {nq}", fontsize=15, fontweight='bold')
    ax.set_ylim(0, 1.05)
    ax.legend(title="Rounds")
    if i != 0: ax.set_ylabel("")

plt.tight_layout()
plt.savefig("phasecode_by_qubits.png", dpi=300)
print("Saved: phasecode_by_qubits.png")

plt.show()
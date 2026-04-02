import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# --- 1. LOAD DATA ---
output_csv = "phasecode_benchmark_results.csv"

if not os.path.exists(output_csv):
    print(f"Error: {output_csv} not found. Make sure to run the scoring script first.")
    exit()

# Read the CSV directly
df = pd.read_csv(output_csv)

# Ensure data types are correct for plotting
df['n_qubits'] = pd.to_numeric(df['n_qubits'])
df['score'] = pd.to_numeric(df['score'])
df['n_rounds'] = pd.to_numeric(df['n_rounds'])

# Sort for consistent legend ordering
df = df.sort_values(['n_qubits', 'n_rounds'])
rounds_list = sorted(df['n_rounds'].unique())
qubits_list = sorted(df['n_qubits'].unique())

# Define your preferred order here
backend_order = ["ibm_fez", "ibm_marrakesh", "ibm_torino"]

# --- PLOT 3: SUBFIGS BY ROUNDS (NQ on same chart) ---
sns.set_theme(style="whitegrid")
fig3, axes3 = plt.subplots(1, len(rounds_list), figsize=(6 * len(rounds_list), 6), sharey=True, squeeze=False)

for i, nr in enumerate(rounds_list):
    ax = axes3[0][i]
    round_data = df[df['n_rounds'] == nr]
    sns.barplot(
        data=round_data, 
        x='backend', 
        y='score', 
        hue='n_qubits', 
        order=backend_order,
        palette="tab10", 
        ax=ax, 
        edgecolor='gray'
    )
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
    sns.barplot(
        data=qubit_data, 
        x='backend', 
        y='score', 
        hue='n_rounds', 
        order=backend_order,
        palette="tab10", 
        ax=ax, 
        edgecolor='gray'
    )
    ax.set_title(f"Qubits: {nq}", fontsize=15, fontweight='bold')
    ax.set_ylim(0, 1.05)
    ax.legend(title="Rounds")
    if i != 0: ax.set_ylabel("")

plt.tight_layout()
plt.savefig("phasecode_by_qubits.png", dpi=300)
print("Saved: phasecode_by_qubits.png")

plt.show()
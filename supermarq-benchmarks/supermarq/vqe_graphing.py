import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# --- 1. LOAD DATA ---
output_csv = "vqeproxy_benchmark_results.csv"

if not os.path.exists(output_csv):
    print(f"Error: {output_csv} not found. Make sure to run the scoring script first.")
    exit()

# Read the CSV directly
df = pd.read_csv(output_csv)

# Ensure data types are correct for plotting
df['n_qubits'] = pd.to_numeric(df['n_qubits'])
df['score'] = pd.to_numeric(df['score'])
df['n_layers'] = pd.to_numeric(df['n_layers']) # Changed from n_rounds

# Sort for consistent legend ordering
df = df.sort_values(['n_qubits', 'n_layers'])
layers_list = sorted(df['n_layers'].unique()) # Changed from rounds_list
qubits_list = sorted(df['n_qubits'].unique())

# Define your preferred order here
backend_order = ["ibm_fez", "ibm_marrakesh", "ibm_torino"]

# --- PLOT 3: SUBFIGS BY LAYERS (NQ on same chart) ---
sns.set_theme(style="whitegrid")
fig3, axes3 = plt.subplots(1, len(layers_list), figsize=(6 * len(layers_list), 6), sharey=True, squeeze=False)

for i, nl in enumerate(layers_list):
    ax = axes3[0][i]
    layer_data = df[df['n_layers'] == nl] # Changed to filter by n_layers
    sns.barplot(
        data=layer_data, 
        x='backend', 
        y='score', 
        hue='n_qubits', 
        order=backend_order,
        palette="tab10", 
        ax=ax, 
        edgecolor='gray'
    )
    ax.set_title(f"Layers: {nl}", fontsize=15, fontweight='bold') # Changed title text
    ax.set_ylim(0, 1.05)
    ax.legend(title="Qubits")
    if i != 0: ax.set_ylabel("")

plt.tight_layout()
plt.savefig("vqeproxy_by_layers.png", dpi=300)
print("Saved: vqeproxy_by_layers.png")

# --- PLOT 4: SUBFIGS BY QUBITS (NL on same chart) ---
sns.set_theme(style="whitegrid")
fig4, axes4 = plt.subplots(1, len(qubits_list), figsize=(6 * len(qubits_list), 6), sharey=True, squeeze=False)

for i, nq in enumerate(qubits_list):
    ax = axes4[0][i]
    qubit_data = df[df['n_qubits'] == nq]
    sns.barplot(
        data=qubit_data, 
        x='backend', 
        y='score', 
        hue='n_layers', # Changed hue to n_layers
        order=backend_order,
        palette="tab10", 
        ax=ax, 
        edgecolor='gray'
    )
    ax.set_title(f"Qubits: {nq}", fontsize=15, fontweight='bold')
    ax.set_ylim(0, 1.05)
    ax.legend(title="Layers") # Changed legend title
    if i != 0: ax.set_ylabel("")

plt.tight_layout()
plt.savefig("vqeproxy_by_qubits.png", dpi=300)
print("Saved: vqeproxy_by_qubits.png")

plt.show()

# --- PLOT 5: COMBINED PERFORMANCE (BACKEND VS SCORE) ---
sns.set_theme(style="white")

# Create the label
df['label'] = df['n_qubits'].astype(str) + "q, " + df['n_layers'].astype(str) + "L"
df_sorted = df.sort_values(['n_qubits', 'n_layers'])

plt.figure(figsize=(15, 6))

# Use the first 5 colors of tab10 to create a 5-color rotation
rotation_palette = sns.color_palette("tab10", 5)

ax5 = sns.barplot(
    data=df_sorted, 
    x='backend', 
    y='score', 
    hue='label', 
    order=backend_order,
    palette=rotation_palette, 
    edgecolor='gray'
)

plt.title("VQE Proxy Performance (Combined X+Z Score)", fontsize=16)
plt.xlabel("Backend", fontsize=12)
plt.ylabel("score", fontsize=12)
plt.ylim(0, 1.05)
plt.legend(title="label", bbox_to_anchor=(1.05, 1), loc='upper left', frameon=True)

plt.tight_layout()
plt.savefig("vqeproxy_combined_bar_chart.png", dpi=300)
plt.show()
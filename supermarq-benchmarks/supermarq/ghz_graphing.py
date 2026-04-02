import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# --- 1. LOAD DATA ---
# Updated to your GHZ results file
output_csv = "ghz_benchmark_results.csv"

if not os.path.exists(output_csv):
    print(f"Error: {output_csv} not found. Make sure to run the scoring script first.")
    exit()

# Read the CSV directly
df = pd.read_csv(output_csv)

# Ensure data types are correct for plotting
df['n_qubits'] = pd.to_numeric(df['n_qubits'])
df['score'] = pd.to_numeric(df['score'])

# Sort for consistent legend ordering
df = df.sort_values(['n_qubits'])
methods = sorted(df['method'].unique())

# Define your fixed backend order
backend_order = ["ibm_fez", "ibm_marrakesh", "ibm_torino"]

# --- PLOT 1: LINE PERFORMANCE COMPARISON ---
sns.set_theme(style="whitegrid")

# Create a figure with subplots for each GHZ method
fig, axes = plt.subplots(1, len(methods), figsize=(18, 6), sharey=True, squeeze=False)
fig.suptitle('SupermarQ GHZ Benchmark: Hellinger Fidelity by Method', fontsize=18, fontweight='bold')

for i, method in enumerate(methods):
    ax = axes[0][i]
    method_data = df[df['method'] == method]
    
    sns.lineplot(
        data=method_data, 
        x='n_qubits', 
        y='score', 
        hue='backend', 
        hue_order=backend_order, # Apply fixed order
        marker='o', 
        ax=ax,
        linewidth=2.5,
        markersize=8
    )
    
    ax.set_title(f"Method: {method.capitalize()}", fontsize=14, fontweight='semibold')
    ax.set_xlabel("Number of Qubits", fontsize=12)
    ax.set_ylabel("Hellinger Fidelity (Score)" if i == 0 else "", fontsize=12)
    ax.set_ylim(-0.05, 1.05)
    ax.legend(title="IBM Backend", frameon=True)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plot_filename = "ghz_performance_comparison.png"
plt.savefig(plot_filename, dpi=300)
print(f"Plot saved: {plot_filename}")
plt.show()

# --- PLOT 2: BAR CHARTS BY BACKEND ---
sns.set_theme(style="white") 
qubit_counts = sorted(df['n_qubits'].unique())

fig2, axes2 = plt.subplots(1, len(methods), figsize=(20, 6), sharey=True, squeeze=False)
custom_palette = sns.color_palette("tab10", len(qubit_counts))

for i, method in enumerate(methods):
    ax = axes2[0][i]
    method_data = df[df['method'] == method]
    
    sns.barplot(
        data=method_data,
        x='backend',
        y='score',
        hue='n_qubits',
        order=backend_order, # Apply fixed order
        palette=custom_palette,
        ax=ax,
        edgecolor='gray',
        capsize=.1,
        errwidth=1.5 
    )
    
    ax.set_title(f"GHZ Method: {method.upper()}", fontsize=15, fontweight='bold', pad=20)
    ax.set_xlabel("Backend", fontsize=12)
    ax.set_ylabel("Score" if i == 0 else "", fontsize=12)
    ax.set_ylim(0, 1.05)
    
    # Place legend only on the last subplot
    if i == len(methods) - 1:
        ax.legend(title="Qubits", loc='lower right', bbox_to_anchor=(1, 0.1), ncol=2)
    else:
        if ax.get_legend():
            ax.get_legend().remove()

    ax.axhline(0, color='black', linewidth=0.8)

plt.tight_layout()
bar_plot_filename = "ghz_bar_charts.png"
plt.savefig(bar_plot_filename, dpi=300)
print(f"Bar chart saved: {bar_plot_filename}")
plt.show()
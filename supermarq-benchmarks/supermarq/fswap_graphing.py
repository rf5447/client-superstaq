import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# --- 1. LOAD DATA ---
output_csv = "benchmark_results_combined/fswap_qaoa_benchmark_results_combined.csv"

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
qubit_counts = sorted(df['n_qubits'].unique())

# Define your preferred fixed order
backend_order = ["ibm_torino", "ibm_fez", "ibm_kingston", "ibm_marrakesh"]
backend_order_subset = ["ibm_fez", "ibm_kingston", "ibm_marrakesh"]

# Match MB-style overall look
sns.set_theme(
    style="whitegrid",
    rc={
        "axes.edgecolor": "0.85",
        "axes.linewidth": 0.8,
        "grid.color": "0.9",
        "grid.linewidth": 0.8,
        "grid.alpha": 1.0,

        "font.size": 22,
        "axes.labelsize": 22,
        "axes.titlesize": 22,
        "xtick.labelsize": 20,
        "ytick.labelsize": 20,
        "legend.fontsize": 20,
        "legend.title_fontsize": 22,
    }
)

def style_axes_like_mb(ax):
    ax.grid(axis='y', color='0.9', linewidth=0.8)
    ax.grid(axis='x', visible=False)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color('0.85')
        spine.set_linewidth(0.8)

def slant_xlabels(ax, rotation=15):
    ax.tick_params(axis='x', rotation=rotation)
    for label in ax.get_xticklabels():
        label.set_horizontalalignment('right')

# --- PREPARE AGGREGATED DATA FOR BAR CHARTS ---
bar_df = (
    df.groupby(['backend', 'n_qubits'], as_index=False)
      .agg(score_mean=('score', 'mean'),
           score_std=('score', 'std'))
)

bar_df['score_std'] = bar_df['score_std'].fillna(0)

# --- PLOT 1A: BAR CHART COMPARISON (WITH TORINO) ---
fig1a, ax1a = plt.subplots(figsize=(12, 6))

hue_order = sorted(bar_df['n_qubits'].unique())

sns.barplot(
    data=bar_df,
    x='backend',
    y='score_mean',
    hue='n_qubits',
    order=backend_order,
    hue_order=hue_order,
    palette="tab10",
    ax=ax1a,
    edgecolor='gray'
)

style_axes_like_mb(ax1a)
slant_xlabels(ax1a)

# Add per-bar standard deviation error bars in seaborn draw order
patch_idx = 0
for nq in hue_order:
    for backend in backend_order:
        subset = bar_df[
            (bar_df['n_qubits'] == nq) &
            (bar_df['backend'] == backend)
        ]
        if subset.empty:
            continue

        row = subset.iloc[0]
        patch = ax1a.patches[patch_idx]
        x = patch.get_x() + patch.get_width() / 2
        y = row['score_mean']
        yerr = row['score_std']

        ax1a.errorbar(
            x, y, yerr=yerr,
            fmt='none',
            ecolor='black',
            elinewidth=1.5,
            capsize=3
        )
        patch_idx += 1

ax1a.set_xlabel("Backend")
ax1a.set_ylabel("Score")
ax1a.set_ylim(0, 1.05)
ax1a.legend(title="Qubits", loc='center left', bbox_to_anchor=(1.02, 0.5))
ax1a.axhline(0, color='black', linewidth=0.8)

plt.tight_layout()
plt.savefig("fswap_bar_charts.png", dpi=300, bbox_inches='tight')
print("Saved: fswap_bar_charts.png")

# --- PLOT 1B: BAR CHART COMPARISON (WITHOUT TORINO) ---
fig1b, ax1b = plt.subplots(figsize=(12, 6))

bar_df_subset = bar_df[bar_df['backend'].isin(backend_order_subset)].copy()
hue_order_subset = sorted(bar_df_subset['n_qubits'].unique())

sns.barplot(
    data=bar_df_subset,
    x='backend',
    y='score_mean',
    hue='n_qubits',
    order=backend_order_subset,
    hue_order=hue_order_subset,
    palette="tab10",
    ax=ax1b,
    edgecolor='gray'
)

style_axes_like_mb(ax1b)
slant_xlabels(ax1b)

# Add per-bar standard deviation error bars in seaborn draw order
patch_idx = 0
for nq in hue_order_subset:
    for backend in backend_order_subset:
        subset = bar_df_subset[
            (bar_df_subset['n_qubits'] == nq) &
            (bar_df_subset['backend'] == backend)
        ]
        if subset.empty:
            continue

        row = subset.iloc[0]
        patch = ax1b.patches[patch_idx]
        x = patch.get_x() + patch.get_width() / 2
        y = row['score_mean']
        yerr = row['score_std']

        ax1b.errorbar(
            x, y, yerr=yerr,
            fmt='none',
            ecolor='black',
            elinewidth=1.5,
            capsize=3
        )
        patch_idx += 1

ax1b.set_xlabel("Backend")
ax1b.set_ylabel("Score")
ax1b.set_ylim(0, 1.05)
ax1b.legend(title="Qubits", loc='center left', bbox_to_anchor=(1.02, 0.5))
ax1b.axhline(0, color='black', linewidth=0.8)

plt.tight_layout()
plt.savefig("fswap_bar_charts_no_torino.png", dpi=300, bbox_inches='tight')
print("Saved: fswap_bar_charts_no_torino.png")

plt.show()
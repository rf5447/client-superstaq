import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# --- 1. LOAD DATA ---
output_csv = "benchmark_results_combined/ghz_benchmark_results_combined.csv"

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
backend_order = ["ibm_torino", "ibm_fez", "ibm_kingston", "ibm_marrakesh"]
backend_order_subset = ["ibm_fez", "ibm_kingston", "ibm_marrakesh"]

# Match vanilla/mb-style overall look
sns.set_theme(
    style="whitegrid",
    rc={
        "axes.edgecolor": "0.85",
        "axes.linewidth": 0.8,
        "grid.color": "0.9",
        "grid.linewidth": 0.8,
        "grid.alpha": 1.0,

        # Bigger fonts
        "font.size": 22,
        "axes.labelsize": 22,
        "axes.titlesize": 22,
        "xtick.labelsize": 20,
        "ytick.labelsize": 20,
        "legend.fontsize": 20,
        "legend.title_fontsize": 22,
    }
)

def style_axes_like_vanilla(ax):
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

# --- PLOT 1: LINE PERFORMANCE COMPARISON ---
fig, axes = plt.subplots(1, len(methods), figsize=(24, 8), sharey=True, squeeze=False)

for i, method in enumerate(methods):
    ax = axes[0][i]
    method_data = df[df['method'] == method]
    
    sns.lineplot(
        data=method_data,
        x='n_qubits',
        y='score',
        hue='backend',
        hue_order=backend_order,
        marker='o',
        ax=ax,
        linewidth=2.5,
        markersize=8
    )

    style_axes_like_vanilla(ax)
    slant_xlabels(ax)

    ax.set_title(f"Method: {method}", fontweight='semibold')
    ax.set_xlabel("Number of Qubits")
    ax.set_ylabel("Score" if i == 0 else "")
    ax.set_ylim(-0.05, 1.05)
    ax.legend(title="Backend", loc='center left', bbox_to_anchor=(1.02, 0.5))

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plot_filename = "ghz_performance_comparison.png"
plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
print(f"Plot saved: {plot_filename}")
plt.show()

# --- PREPARE AGGREGATED DATA FOR BAR CHARTS ---
bar_df = (
    df.groupby(['method', 'backend', 'n_qubits'], as_index=False)
      .agg(score_mean=('score', 'mean'),
           score_std=('score', 'std'))
)

bar_df['score_std'] = bar_df['score_std'].fillna(0)
qubit_counts = sorted(df['n_qubits'].unique())
custom_palette = sns.color_palette("tab10", len(qubit_counts))

# --- PLOT 2: BAR CHARTS BY BACKEND ---
fig2, axes2 = plt.subplots(1, len(methods), figsize=(27, 8), sharey=True, squeeze=False)

for i, method in enumerate(methods):
    ax = axes2[0][i]
    method_data = bar_df[bar_df['method'] == method].copy()
    
    sns.barplot(
        data=method_data,
        x='backend',
        y='score_mean',
        hue='n_qubits',
        order=backend_order,
        hue_order=qubit_counts,
        palette=custom_palette,
        ax=ax,
        edgecolor='gray'
    )

    style_axes_like_vanilla(ax)
    slant_xlabels(ax)

    # Add per-bar standard deviation error bars in seaborn draw order
    patch_idx = 0
    for q in qubit_counts:
        for backend in backend_order:
            subset = method_data[
                (method_data['n_qubits'] == q) &
                (method_data['backend'] == backend)
            ]
            if subset.empty:
                continue

            row = subset.iloc[0]
            patch = ax.patches[patch_idx]
            x = patch.get_x() + patch.get_width() / 2
            y = row['score_mean']
            yerr = row['score_std']

            ax.errorbar(
                x, y, yerr=yerr,
                fmt='none',
                ecolor='black',
                elinewidth=1.5,
                capsize=3
            )
            patch_idx += 1
    
    ax.set_title(f"Method: {method}", fontweight='semibold')
    ax.set_xlabel("Backend")
    ax.set_ylabel("Score" if i == 0 else "")
    ax.set_ylim(0, 1.05)
    
    if i == len(methods) - 1:
        ax.legend(title="Qubits", loc='center left', bbox_to_anchor=(1.02, 0.5), ncol=1)
    else:
        if ax.get_legend():
            ax.get_legend().remove()

    ax.axhline(0, color='black', linewidth=0.8)

plt.tight_layout()
bar_plot_filename = "ghz_bar_charts.png"
plt.savefig(bar_plot_filename, dpi=300, bbox_inches='tight')
print(f"Bar chart saved: {bar_plot_filename}")
plt.show()

# --- PLOT 3: BAR CHARTS BY BACKEND (FEZ, KINGSTON, MARRAKESH ONLY) ---
fig3, axes3 = plt.subplots(1, len(methods), figsize=(24, 8), sharey=True, squeeze=False)

for i, method in enumerate(methods):
    ax = axes3[0][i]
    method_data = bar_df[
        (bar_df['method'] == method) &
        (bar_df['backend'].isin(backend_order_subset))
    ].copy()
    
    sns.barplot(
        data=method_data,
        x='backend',
        y='score_mean',
        hue='n_qubits',
        order=backend_order_subset,
        hue_order=qubit_counts,
        palette=custom_palette,
        ax=ax,
        edgecolor='gray'
    )

    style_axes_like_vanilla(ax)
    slant_xlabels(ax)

    # Add per-bar standard deviation error bars in seaborn draw order
    patch_idx = 0
    for q in qubit_counts:
        for backend in backend_order_subset:
            subset = method_data[
                (method_data['n_qubits'] == q) &
                (method_data['backend'] == backend)
            ]
            if subset.empty:
                continue

            row = subset.iloc[0]
            patch = ax.patches[patch_idx]
            x = patch.get_x() + patch.get_width() / 2
            y = row['score_mean']
            yerr = row['score_std']

            ax.errorbar(
                x, y, yerr=yerr,
                fmt='none',
                ecolor='black',
                elinewidth=1.5,
                capsize=3
            )
            patch_idx += 1
    
    ax.set_title(f"Method: {method}", fontweight='semibold')
    ax.set_xlabel("Backend")
    ax.set_ylabel("Score" if i == 0 else "")
    ax.set_ylim(0, 1.05)
    
    if i == len(methods) - 1:
        ax.legend(title="Qubits", loc='center left', bbox_to_anchor=(1.02, 0.5), ncol=1)
    else:
        if ax.get_legend():
            ax.get_legend().remove()

    ax.axhline(0, color='black', linewidth=0.8)

plt.tight_layout()
bar_plot_subset_filename = "ghz_bar_charts_no_torino.png"
plt.savefig(bar_plot_subset_filename, dpi=300, bbox_inches='tight')
print(f"Subset bar chart saved: {bar_plot_subset_filename}")
plt.show()
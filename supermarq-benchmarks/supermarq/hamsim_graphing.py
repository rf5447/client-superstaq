import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. LOAD DATA ---
output_csv = "benchmark_results_combined/hamsim_benchmark_results_combined.csv"

if not os.path.exists(output_csv):
    print(f"Error: {output_csv} not found.")
    exit()

df = pd.read_csv(output_csv)

# --- DATA PREP ---
df['n_qubits'] = pd.to_numeric(df['n_qubits'])
df['score'] = pd.to_numeric(df['score'])
df['ts'] = pd.to_numeric(df['ts'])

# Use just the numeric labels for the legend
df['steps_label'] = df['ts'].astype(int).astype(str)

# Sort by qubits then numeric steps to keep the legend and bars in order
df = df.sort_values(['n_qubits', 'ts'])

backend_order = ["ibm_torino", "ibm_fez", "ibm_kingston", "ibm_marrakesh"]
backend_order_subset = ["ibm_fez", "ibm_kingston", "ibm_marrakesh"]
qubits_list = sorted(df['n_qubits'].unique())
steps_order = (
    df[['ts', 'steps_label']]
    .drop_duplicates()
    .sort_values('ts')['steps_label']
    .tolist()
)

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
    df.groupby(['backend', 'n_qubits', 'ts', 'steps_label'], as_index=False)
      .agg(score_mean=('score', 'mean'),
           score_std=('score', 'std'))
)

bar_df['score_std'] = bar_df['score_std'].fillna(0)

# --- PLOT 1A: WITH TORINO ---
fig1a, axes1a = plt.subplots(
    2, 4,
    figsize=(25, 12.5),
    sharey=True,
    squeeze=False
)
fig1a.subplots_adjust(wspace=0.08)

legend_handles = None
legend_labels = None

for i, nq in enumerate(qubits_list):
    row_idx = i // 4
    col_idx = i % 4
    ax = axes1a[row_idx][col_idx]

    qubit_data = bar_df[bar_df['n_qubits'] == nq].copy()

    sns.barplot(
        data=qubit_data,
        x='backend',
        y='score_mean',
        hue='steps_label',
        order=backend_order,
        hue_order=steps_order,
        palette="tab10",
        ax=ax,
        edgecolor='gray'
    )

    style_axes_like_mb(ax)
    slant_xlabels(ax)

    if legend_handles is None:
        legend_handles, legend_labels = ax.get_legend_handles_labels()
    if ax.legend_ is not None:
        ax.legend_.remove()

    patch_idx = 0
    for step_label in steps_order:
        for backend in backend_order:
            subset = qubit_data[
                (qubit_data['steps_label'] == step_label) &
                (qubit_data['backend'] == backend)
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

    ax.set_title(f"Qubits: {nq}")
    ax.set_xlabel("Backend")
    ax.set_ylim(0, 1.1)

    if col_idx != 0:
        ax.set_ylabel("")

# Put legend in the first unused subplot slot
for j in range(len(qubits_list), 8):
    row_idx = j // 4
    col_idx = j % 4
    ax = axes1a[row_idx][col_idx]

    if j == len(qubits_list):
        ax.axis('off')
        ax.legend(
            legend_handles,
            legend_labels,
            title="Layers",
            loc='center',
            frameon=True
        )
    else:
        ax.axis('off')

plt.tight_layout(rect=[0, 0, 1, 1])
plt.savefig("hamsim_2x4_clean.png", dpi=300, bbox_inches='tight')
print("Saved: hamsim_2x4_clean.png")

# --- PLOT 1B: WITHOUT TORINO ---
fig1b, axes1b = plt.subplots(
    2, 4,
    figsize=(25, 12.5),
    sharey=True,
    squeeze=False
)
fig1b.subplots_adjust(wspace=0.08)

legend_handles = None
legend_labels = None

for i, nq in enumerate(qubits_list):
    row_idx = i // 4
    col_idx = i % 4
    ax = axes1b[row_idx][col_idx]

    qubit_data = bar_df[
        (bar_df['n_qubits'] == nq) &
        (bar_df['backend'].isin(backend_order_subset))
    ].copy()

    sns.barplot(
        data=qubit_data,
        x='backend',
        y='score_mean',
        hue='steps_label',
        order=backend_order_subset,
        hue_order=steps_order,
        palette="tab10",
        ax=ax,
        edgecolor='gray'
    )

    style_axes_like_mb(ax)
    slant_xlabels(ax)

    if legend_handles is None:
        legend_handles, legend_labels = ax.get_legend_handles_labels()
    if ax.legend_ is not None:
        ax.legend_.remove()

    patch_idx = 0
    for step_label in steps_order:
        for backend in backend_order_subset:
            subset = qubit_data[
                (qubit_data['steps_label'] == step_label) &
                (qubit_data['backend'] == backend)
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

    ax.set_title(f"Qubits: {nq}", fontweight='semibold')
    ax.set_xlabel("Backend")
    ax.set_ylim(0, 1.1)

    if col_idx != 0:
        ax.set_ylabel("")

# Put legend in the first unused subplot slot
for j in range(len(qubits_list), 8):
    row_idx = j // 4
    col_idx = j % 4
    ax = axes1b[row_idx][col_idx]

    if j == len(qubits_list):
        ax.axis('off')
        ax.legend(
            legend_handles,
            legend_labels,
            title="Layers",
            loc='center',
            frameon=True
        )
    else:
        ax.axis('off')

plt.tight_layout(rect=[0, 0, 1, 1])
plt.savefig("hamsim_2x4_clean_no_torino.png", dpi=300, bbox_inches='tight')
print("Saved: hamsim_2x4_clean_no_torino.png")

plt.show()
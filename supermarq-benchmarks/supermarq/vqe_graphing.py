import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# --- 1. LOAD DATA ---
output_csv = "benchmark_results_combined/vqeproxy_benchmark_results_combined.csv"

if not os.path.exists(output_csv):
    print(f"Error: {output_csv} not found. Make sure to run the scoring script first.")
    exit()

# Read the CSV directly
df = pd.read_csv(output_csv)

# Ensure data types are correct for plotting
df['n_qubits'] = pd.to_numeric(df['n_qubits'])
df['score'] = pd.to_numeric(df['score'])
df['n_layers'] = pd.to_numeric(df['n_layers'])

# Sort for consistent legend ordering
df = df.sort_values(['n_qubits', 'n_layers'])
layers_list = sorted(df['n_layers'].unique())
qubits_list = sorted(df['n_qubits'].unique())

# Define your preferred order here
backend_order = ["ibm_torino", "ibm_fez", "ibm_kingston", "ibm_marrakesh"]
backend_order_subset = ["ibm_fez", "ibm_kingston", "ibm_marrakesh"]

# Match vanilla/MB-style overall look
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

# --- PREPARE AGGREGATED DATA FOR BAR CHARTS ---
bar_df = (
    df.groupby(['backend', 'n_qubits', 'n_layers'], as_index=False)
      .agg(score_mean=('score', 'mean'),
           score_std=('score', 'std'))
)

bar_df['score_std'] = bar_df['score_std'].fillna(0)

# --- PLOT 3A: SUBFIGS BY LAYERS (NQ on same chart, WITH TORINO) ---
fig3a, axes3a = plt.subplots(
    2, 3,
    figsize=(18, 12),
    sharey=True,
    squeeze=False
)

legend_handles = None
legend_labels = None
flat_axes3a = axes3a.flatten()

for i, nl in enumerate(layers_list):
    ax = flat_axes3a[i]
    layer_data = bar_df[bar_df['n_layers'] == nl].copy()

    hue_order = sorted(layer_data['n_qubits'].unique())

    sns.barplot(
        data=layer_data,
        x='backend',
        y='score_mean',
        hue='n_qubits',
        order=backend_order,
        hue_order=hue_order,
        palette="tab10",
        ax=ax,
        edgecolor='gray'
    )

    style_axes_like_vanilla(ax)
    slant_xlabels(ax)

    if legend_handles is None:
        legend_handles, legend_labels = ax.get_legend_handles_labels()
    if ax.legend_ is not None:
        ax.legend_.remove()

    # Add per-bar standard deviation error bars in seaborn draw order
    patch_idx = 0
    for nq in hue_order:
        for backend in backend_order:
            subset = layer_data[
                (layer_data['n_qubits'] == nq) &
                (layer_data['backend'] == backend)
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

    ax.set_title(f"Layers: {nl}", fontweight='semibold')
    ax.set_xlabel("Backend")
    ax.set_ylim(0, 1.05)
    ax.axhline(0, color='black', linewidth=0.8)

    if i % 3 == 0:
        ax.set_ylabel("Score")
    else:
        ax.set_ylabel("")

# Put legend in the 6th subplot (bottom right)
legend_ax = flat_axes3a[5]
legend_ax.axis("off")
legend_ax.legend(
    legend_handles,
    legend_labels,
    title="Qubits",
    loc="center",
    frameon=True
)

plt.tight_layout()
plt.savefig("vqeproxy_by_layers.png", dpi=300, bbox_inches='tight')
print("Saved: vqeproxy_by_layers.png")

# --- PLOT 3B: SUBFIGS BY LAYERS (NQ on same chart, WITHOUT TORINO) ---
fig3b, axes3b = plt.subplots(
    2, 3,
    figsize=(18, 12),
    sharey=True,
    squeeze=False
)

legend_handles = None
legend_labels = None
flat_axes3b = axes3b.flatten()

for i, nl in enumerate(layers_list):
    ax = flat_axes3b[i]
    layer_data = bar_df[
        (bar_df['n_layers'] == nl) &
        (bar_df['backend'].isin(backend_order_subset))
    ].copy()

    hue_order = sorted(layer_data['n_qubits'].unique())

    sns.barplot(
        data=layer_data,
        x='backend',
        y='score_mean',
        hue='n_qubits',
        order=backend_order_subset,
        hue_order=hue_order,
        palette="tab10",
        ax=ax,
        edgecolor='gray'
    )

    style_axes_like_vanilla(ax)
    slant_xlabels(ax)

    if legend_handles is None:
        legend_handles, legend_labels = ax.get_legend_handles_labels()
    if ax.legend_ is not None:
        ax.legend_.remove()

    # Add per-bar standard deviation error bars in seaborn draw order
    patch_idx = 0
    for nq in hue_order:
        for backend in backend_order_subset:
            subset = layer_data[
                (layer_data['n_qubits'] == nq) &
                (layer_data['backend'] == backend)
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

    ax.set_title(f"Layers: {nl}", fontweight='semibold')
    ax.set_xlabel("Backend")
    ax.set_ylim(0, 1.05)
    ax.axhline(0, color='black', linewidth=0.8)

    if i % 3 == 0:
        ax.set_ylabel("Score")
    else:
        ax.set_ylabel("")

# Put legend in the 6th subplot (bottom right)
legend_ax = flat_axes3b[5]
legend_ax.axis("off")
legend_ax.legend(
    legend_handles,
    legend_labels,
    title="Qubits",
    loc="center",
    frameon=True
)

plt.tight_layout()
plt.savefig("vqeproxy_by_layers_no_torino.png", dpi=300, bbox_inches='tight')
print("Saved: vqeproxy_by_layers_no_torino.png")

# --- PLOT 4A: SUBFIGS BY QUBITS (NL on same chart, WITH TORINO) ---
fig4a, axes4a = plt.subplots(
    1, len(qubits_list),
    figsize=(6 * len(qubits_list), 6),
    sharey=True,
    squeeze=False
)

legend_handles = None
legend_labels = None

for i, nq in enumerate(qubits_list):
    ax = axes4a[0][i]
    qubit_data = bar_df[bar_df['n_qubits'] == nq].copy()

    hue_order = sorted(qubit_data['n_layers'].unique())

    sns.barplot(
        data=qubit_data,
        x='backend',
        y='score_mean',
        hue='n_layers',
        order=backend_order,
        hue_order=hue_order,
        palette="tab10",
        ax=ax,
        edgecolor='gray'
    )

    style_axes_like_vanilla(ax)
    slant_xlabels(ax)

    if legend_handles is None:
        legend_handles, legend_labels = ax.get_legend_handles_labels()
    if ax.legend_ is not None:
        ax.legend_.remove()

    # Add per-bar standard deviation error bars in seaborn draw order
    patch_idx = 0
    for nl in hue_order:
        for backend in backend_order:
            subset = qubit_data[
                (qubit_data['n_layers'] == nl) &
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
    ax.set_ylim(0, 1.05)
    ax.axhline(0, color='black', linewidth=0.8)

    if i == 0:
        ax.set_ylabel("Score")
    else:
        ax.set_ylabel("")

fig4a.legend(
    legend_handles,
    legend_labels,
    title="Layers",
    loc='center left',
    bbox_to_anchor=(1.02, 0.5)
)

plt.tight_layout()
plt.savefig("vqeproxy_by_qubits.png", dpi=300, bbox_inches='tight')
print("Saved: vqeproxy_by_qubits.png")

# --- PLOT 4B: SUBFIGS BY QUBITS (NL on same chart, WITHOUT TORINO) ---
fig4b, axes4b = plt.subplots(
    1, len(qubits_list),
    figsize=(6 * len(qubits_list), 6),
    sharey=True,
    squeeze=False
)

legend_handles = None
legend_labels = None

for i, nq in enumerate(qubits_list):
    ax = axes4b[0][i]
    qubit_data = bar_df[
        (bar_df['n_qubits'] == nq) &
        (bar_df['backend'].isin(backend_order_subset))
    ].copy()

    hue_order = sorted(qubit_data['n_layers'].unique())

    sns.barplot(
        data=qubit_data,
        x='backend',
        y='score_mean',
        hue='n_layers',
        order=backend_order_subset,
        hue_order=hue_order,
        palette="tab10",
        ax=ax,
        edgecolor='gray'
    )

    style_axes_like_vanilla(ax)
    slant_xlabels(ax)

    if legend_handles is None:
        legend_handles, legend_labels = ax.get_legend_handles_labels()
    if ax.legend_ is not None:
        ax.legend_.remove()

    # Add per-bar standard deviation error bars in seaborn draw order
    patch_idx = 0
    for nl in hue_order:
        for backend in backend_order_subset:
            subset = qubit_data[
                (qubit_data['n_layers'] == nl) &
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
    ax.set_ylim(0, 1.05)
    ax.axhline(0, color='black', linewidth=0.8)

    if i == 0:
        ax.set_ylabel("Score")
    else:
        ax.set_ylabel("")

fig4b.legend(
    legend_handles,
    legend_labels,
    title="Layers",
    loc='center left',
    bbox_to_anchor=(1.02, 0.5)
)

plt.tight_layout()
plt.savefig("vqeproxy_by_qubits_no_torino.png", dpi=300, bbox_inches='tight')
print("Saved: vqeproxy_by_qubits_no_torino.png")

plt.show()
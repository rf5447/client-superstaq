import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# --- 1. LOAD DATA ---
output_csv = "benchmark_results_combined/mb_benchmark_results_combined.csv"

if not os.path.exists(output_csv):
    print(f"Error: {output_csv} not found. Make sure to run the scoring script first.")
    exit()

# Read the CSV
df = pd.read_csv(output_csv)

# Ensure numeric types and sort by qubits for clean line plots
df['n_qubits'] = pd.to_numeric(df['n_qubits'])
df['score'] = pd.to_numeric(df['score'])
df = df.sort_values(by=['backend', 'n_qubits'])

print(f"Loaded {len(df)} runs from '{output_csv}'.")

# Fixed backend orders
backend_order = ["ibm_torino", "ibm_fez", "ibm_kingston", "ibm_marrakesh"]
backend_order_subset = ["ibm_fez", "ibm_kingston", "ibm_marrakesh"]

# Match vanilla-style overall look
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

# --- 2. PREPARE PLOTTING DATA (WITH CLASSICAL LIMIT) ---

extra_rows = []
for n in sorted(df['n_qubits'].unique()):
    # Classical Limit Formula: (f(n) + 2^(n-1)) / 2^n
    f_n = 2**((n - (n % 2)) // 2)
    classical_ratio = (f_n + 2**(n - 1)) / (2**n)
    
    extra_rows.append({
        "benchmark": "MerminBell",
        "n_qubits": n,
        "backend": "Classical Limit",
        "score": classical_ratio
    })

# Merge hardware data with classical limit data
df_plot = pd.concat([df, pd.DataFrame(extra_rows)], ignore_index=True)

# --- 3. PLOT 1: LINE CHART ---
fig1, ax1 = plt.subplots(figsize=(10, 6))
# fig1.suptitle('SupermarQ Mermin-Bell', fontsize=16, fontweight='bold')

sns.lineplot(
    data=df,
    x='n_qubits',
    y='score',
    hue='backend',
    hue_order=backend_order,
    marker='o',
    ax=ax1,
    linewidth=2.5
)

style_axes_like_vanilla(ax1)
slant_xlabels(ax1)

ax1.set_ylim(-0.05, 1.05)
ax1.set_ylabel("Score")
ax1.set_xlabel("Number of Qubits")
ax1.legend(title="Backend", loc='center left', bbox_to_anchor=(1.02, 0.5))

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("mb_performance_comparison.png", dpi=300, bbox_inches='tight')
print("Saved: mb_performance_comparison.png")

# --- PREPARE AGGREGATED DATA FOR BAR CHARTS ---
bar_df = (
    df.groupby(['backend', 'n_qubits'], as_index=False)
      .agg(score_mean=('score', 'mean'),
           score_std=('score', 'std'))
)

bar_df['score_std'] = bar_df['score_std'].fillna(0)

# --- 4. PLOT 2: BAR CHART (WITH TORINO) ---
fig2, ax2 = plt.subplots(figsize=(12, 6))

qubit_counts = sorted(df['n_qubits'].unique())
n_bars_per_group = len(qubit_counts)

sns.barplot(
    data=bar_df[bar_df['backend'].isin(backend_order)],
    x='backend',
    y='score_mean',
    hue='n_qubits',
    order=backend_order,
    hue_order=qubit_counts,
    palette=sns.color_palette("tab10", n_bars_per_group),
    ax=ax2,
    edgecolor='gray'
)

style_axes_like_vanilla(ax2)
slant_xlabels(ax2)

# Add per-bar standard deviation error bars in seaborn draw order
patch_idx = 0
for q in qubit_counts:
    for backend in backend_order:
        subset = bar_df[
            (bar_df['n_qubits'] == q) &
            (bar_df['backend'] == backend)
        ]
        if subset.empty:
            continue

        row = subset.iloc[0]
        patch = ax2.patches[patch_idx]
        x = patch.get_x() + patch.get_width() / 2
        y = row['score_mean']
        yerr = row['score_std']

        ax2.errorbar(
            x, y, yerr=yerr,
            fmt='none',
            ecolor='black',
            elinewidth=1.5,
            capsize=3
        )
        patch_idx += 1

# Add Classical Limit Dashes
width = 0.8
bar_width = width / n_bars_per_group

for i, backend in enumerate(backend_order):
    for j, n in enumerate(qubit_counts):
        f_n = 2**((n - (n % 2)) // 2)
        classical_ratio = (f_n + 2**(n - 1)) / (2**n)

        x_pos = i - (width / 2) + (j * bar_width) + (bar_width / 2)

        ax2.hlines(
            y=classical_ratio,
            xmin=x_pos - (bar_width / 2) * 0.8,
            xmax=x_pos + (bar_width / 2) * 0.8,
            color='black',
            linestyle='--',
            linewidth=1.5,
            alpha=0.8,
            label='Classical Limit' if i == 0 and j == 0 else ""
        )

# ax2.set_title("Mermin-Bell: Hardware vs. Classical Limit", fontsize=15, fontweight='bold', pad=20)
ax2.set_ylim(0, 1.05)
ax2.set_ylabel("Score")
ax2.set_xlabel("Backend")
ax2.legend(title="Qubits", loc='center left', bbox_to_anchor=(1.02, 0.5))

plt.tight_layout()
plt.savefig("mb_bar_charts_with_limits.png", dpi=300, bbox_inches='tight')
print("Saved: mb_bar_charts_with_limits.png")
plt.show()

# --- 5. PLOT 3: BAR CHART (WITHOUT TORINO) ---
fig3, ax3 = plt.subplots(figsize=(12, 6))

subset_bar_df = bar_df[bar_df['backend'].isin(backend_order_subset)].copy()

sns.barplot(
    data=subset_bar_df,
    x='backend',
    y='score_mean',
    hue='n_qubits',
    order=backend_order_subset,
    hue_order=qubit_counts,
    palette=sns.color_palette("tab10", n_bars_per_group),
    ax=ax3,
    edgecolor='gray'
)

style_axes_like_vanilla(ax3)
slant_xlabels(ax3)

# Add per-bar standard deviation error bars in seaborn draw order
patch_idx = 0
for q in qubit_counts:
    for backend in backend_order_subset:
        subset = subset_bar_df[
            (subset_bar_df['n_qubits'] == q) &
            (subset_bar_df['backend'] == backend)
        ]
        if subset.empty:
            continue

        row = subset.iloc[0]
        patch = ax3.patches[patch_idx]
        x = patch.get_x() + patch.get_width() / 2
        y = row['score_mean']
        yerr = row['score_std']

        ax3.errorbar(
            x, y, yerr=yerr,
            fmt='none',
            ecolor='black',
            elinewidth=1.5,
            capsize=3
        )
        patch_idx += 1

# Add Classical Limit Dashes
width = 0.8
bar_width = width / n_bars_per_group

for i, backend in enumerate(backend_order_subset):
    for j, n in enumerate(qubit_counts):
        f_n = 2**((n - (n % 2)) // 2)
        classical_ratio = (f_n + 2**(n - 1)) / (2**n)

        x_pos = i - (width / 2) + (j * bar_width) + (bar_width / 2)

        ax3.hlines(
            y=classical_ratio,
            xmin=x_pos - (bar_width / 2) * 0.8,
            xmax=x_pos + (bar_width / 2) * 0.8,
            color='black',
            linestyle='--',
            linewidth=1.5,
            alpha=0.8,
            label='Classical Limit' if i == 0 and j == 0 else ""
        )

# ax3.set_title("Mermin-Bell: Hardware vs. Classical Limit", fontsize=15, fontweight='bold', pad=20)
ax3.set_ylim(0, 1.05)
ax3.set_ylabel("Score")
ax3.set_xlabel("Backend")
ax3.legend(title="Qubits", loc='center left', bbox_to_anchor=(1.02, 0.5))

plt.tight_layout()
plt.savefig("mb_bar_charts_with_limits_no_torino.png", dpi=300, bbox_inches='tight')
print("Saved: mb_bar_charts_with_limits_no_torino.png")
plt.show()
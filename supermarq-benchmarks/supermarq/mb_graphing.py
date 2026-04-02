import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# --- 1. LOAD DATA ---
output_csv = "mb_benchmark_results.csv"

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
sns.set_theme(style="whitegrid")
fig1, ax1 = plt.subplots(figsize=(10, 6))
fig1.suptitle('SupermarQ Mermin-Bell', fontsize=16, fontweight='bold')

sns.lineplot(data=df, x='n_qubits', y='score', hue='backend', marker='o', ax=ax1, linewidth=2.5)
ax1.set_ylim(-0.05, 1.05)
ax1.set_ylabel("Score")
ax1.set_xlabel("Number of Qubits")

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("mb_performance_comparison.png", dpi=300)
print("Saved: mb_performance_comparison.png")

# --- 4. PLOT 2: BAR CHART (WITH CLASSICAL LIMIT DASHES) ---
sns.set_theme(style="white")
fig2, ax2 = plt.subplots(figsize=(12, 6))

# Define backends and qubit counts
backends = [b for b in df_plot['backend'].unique() if b != "Classical Limit"]
qubit_counts = sorted(df['n_qubits'].unique())
n_groups = len(backends)
n_bars_per_group = len(qubit_counts)

# Draw the bars for Hardware only
sns.barplot(
    data=df[df['backend'] != "Classical Limit"], 
    x='backend',
    y='score',
    hue='n_qubits',
    palette=sns.color_palette("tab10", n_bars_per_group),
    ax=ax2,
    edgecolor='gray'
)

# Calculate bar width for positioning the lines
# Seaborn barplots with hue usually have a total width of 0.8
width = 0.8 
bar_width = width / n_bars_per_group

# Add Classical Limit Dashes
for i, backend in enumerate(backends):
    for j, n in enumerate(qubit_counts):
        # Calculate classical ratio for this n
        f_n = 2**((n - (n % 2)) // 2)
        classical_ratio = (f_n + 2**(n - 1)) / (2**n)
        
        # Calculate the x-position of the specific bar
        # i is the group index, j is the bar index within the group
        x_pos = i - (width / 2) + (j * bar_width) + (bar_width / 2)
        
        # Draw the dashed line
        ax2.hlines(
            y=classical_ratio, 
            xmin=x_pos - (bar_width/2) * 0.8, 
            xmax=x_pos + (bar_width/2) * 0.8, 
            color='black', 
            linestyle='--', 
            linewidth=1.5,
            alpha=0.8,
            label='Classical Limit' if i == 0 and j == 0 else "" # Only one label for legend
        )

ax2.set_title("Mermin-Bell: Hardware vs. Classical Limit", fontsize=15, fontweight='bold', pad=20)
ax2.set_ylim(0, 1.05)
ax2.set_ylabel("Score")
ax2.legend(title="Qubits", loc='upper right')

plt.tight_layout()
plt.savefig("mb_bar_charts_with_limits.png", dpi=300)
print("Saved: mb_bar_charts_with_limits.png")
plt.show()
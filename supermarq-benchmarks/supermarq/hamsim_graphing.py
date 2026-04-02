import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. LOAD DATA ---
output_csv = "hamsim_benchmark_results.csv"

if not os.path.exists(output_csv):
    print(f"Error: {output_csv} not found.")
    exit()

df = pd.read_csv(output_csv)

# --- DATA PREP ---
df['n_qubits'] = pd.to_numeric(df['n_qubits'])
df['score'] = pd.to_numeric(df['score'])
df['ts'] = pd.to_numeric(df['ts'])

# Create the specific label format you requested: "X steps"
df['steps_label'] = df['ts'].astype(str) + " steps"

# Sort by qubits then numeric steps to keep the legend and bars in order
df = df.sort_values(['n_qubits', 'ts'])

backend_order = ["ibm_fez", "ibm_marrakesh", "ibm_torino"]
unique_steps_labels = df['steps_label'].unique()

# --- PLOT: 2 ROWS x 4 COLUMNS ---
sns.set_theme(style="white")

g = sns.catplot(
    data=df,
    kind="bar",
    x="backend",
    y="score",
    hue="steps_label",    # Use the new "X steps" column
    col="n_qubits",
    col_wrap=4,           
    order=backend_order,
    hue_order=unique_steps_labels,
    palette="tab10",
    edgecolor='gray',
    height=4,             
    aspect=1.2,           
    sharex=False          
)

# Customizing the layout and titles
g.set_titles("{col_name} Qubits", size=16, pad=20)
g.set_axis_labels("Backend", "Score", fontsize=12)
g.set(ylim=(0, 1.1))

# Rotate x-axis labels to prevent horizontal overlap
g.set_xticklabels(rotation=20)

# Remove the legend title as requested
g._legend.set_title("") 

# Adjusting spacing for the 2x4 layout
plt.subplots_adjust(top=0.85, hspace=0.4, wspace=0.3) 
g.fig.suptitle("Hamiltonian Simulation by Qubit Count", fontsize=24)

# Save the consolidated image
plt.savefig("hamsim_2x4_clean.png", dpi=300, bbox_inches='tight')
print("Saved: hamsim_2x4_clean.png")
plt.show()
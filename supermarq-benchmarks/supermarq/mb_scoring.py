import json
import os
import csv
from supermarq import converters
import supermarq
import cirq
from qiskit import qasm2, qasm3, transpile

# Configuration
input_directory = "mb_ibm" 
output_csv = "mb_benchmark_results.csv"

# CSV Column Headers
headers = [
    "benchmark", 
    "n_qubits", 
    "backend", 
    "shots", 
    "score", 
    "job_id", 
    "timestamp"
]

all_rows = []

# Ensure directory exists
if not os.path.exists(input_directory):
    print(f"Error: Folder '{input_directory}' not found.")
else:
    # Iterate through all JSON files in the directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".json"):
            file_path = os.path.join(input_directory, filename)
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                # 1. Extract parameters to initialize the MerminBell object
                n_qubits = data["n_qubits"]
                counts = data["counts"]
                
                # Reverse each bitstring to convert Little-Endian (IBM) to Big-Endian (SupermarQ)
                corrected_counts = {bitstr[::-1]: count for bitstr, count in counts.items()}
                
                # 2. Initialize the specific MerminBell benchmark to use its .score() method
                mb_benchmark = supermarq.mermin_bell.MerminBell(n_qubits)
                
                # 3. Calculate score
                # run_score = mb_benchmark.score(counts)
                run_score = mb_benchmark.score(corrected_counts)

                # 4. Prepare the row for CSV
                row = {
                    "benchmark": data.get("benchmark", "MerminBell"),
                    "n_qubits": n_qubits,
                    "backend": data.get("backend"),
                    "shots": data.get("shots"),
                    "score": run_score,
                    "job_id": data.get("job_id"),
                    "timestamp": data.get("timestamp")
                }
                all_rows.append(row)
                print(f"Processed {filename}: Score = {run_score:.4f}")
                
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

# Write the aggregated data to a single CSV
with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(all_rows)

print(f"\nSuccess! Aggregated {len(all_rows)} runs into '{output_csv}'.")
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load the data we just created
df = pd.DataFrame(all_rows)

# Ensure data types are correct for plotting
df['n_qubits'] = pd.to_numeric(df['n_qubits'])
df['score'] = pd.to_numeric(df['score'])

# 2. Set the visual style
sns.set_theme(style="whitegrid")

# Create a figure for Mermin-Bell (single plot)
fig, ax = plt.subplots(figsize=(10, 6))
fig.suptitle('SupermarQ Mermin-Bell Benchmark: Hellinger Fidelity', fontsize=16, fontweight='bold')

# 3. Draw lines and points for each backend
sns.lineplot(
    data=df, 
    x='n_qubits', 
    y='score', 
    hue='backend', 
    marker='o', 
    ax=ax,
    linewidth=2.5,
    markersize=8
)

# Formatting
ax.set_xlabel("Number of Qubits", fontsize=12)
ax.set_ylabel("Hellinger Fidelity (Score)", fontsize=12)
ax.set_ylim(-0.05, 1.05)  # Fidelity is always 0 to 1
ax.legend(title="IBM Backend", frameon=True)

# Adjust layout
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# 4. Save and Show
plot_filename = "mb_performance_comparison.png"
plt.savefig(plot_filename, dpi=300)
print(f"\nPlot saved successfully as '{plot_filename}'")
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load and prepare the data
df = pd.DataFrame(all_rows)
df['n_qubits'] = pd.to_numeric(df['n_qubits'])
df['score'] = pd.to_numeric(df['score'])

# 2. Set the visual style to match the uploaded image
sns.set_theme(style="white") # Clean white background
qubit_counts = sorted(df['n_qubits'].unique())

# Create a figure with 1 plot for Mermin-Bell
fig, ax = plt.subplots(1, 1, figsize=(10, 6))

# Define a color palette similar to the reference image
custom_palette = sns.color_palette("tab10", len(qubit_counts))

# 3. Create the grouped bar chart
sns.barplot(
    data=df,
    x='backend',
    y='score',
    hue='n_qubits',
    palette=custom_palette,
    ax=ax,
    edgecolor='gray',
    capsize=.1,      # Adds error bar caps
    errwidth=1.5     # Sets error bar thickness
)

# Formatting to match the image style
ax.set_title("Mermin-Bell Benchmark", fontsize=15, fontweight='bold', pad=20)
ax.set_xlabel("Backend", fontsize=12)
ax.set_ylabel("Score", fontsize=12)
ax.set_ylim(0, 1.05)

# Place the legend
ax.legend(title="Qubits", loc='lower right', bbox_to_anchor=(1, 0.1), ncol=2)

# Add a horizontal line at 0 for clean aesthetics
ax.axhline(0, color='black', linewidth=0.8)

plt.tight_layout()

# 4. Save and Show
bar_plot_filename = "mb_bar_charts.png"
plt.savefig(bar_plot_filename, dpi=300)
print(f"\nBar chart saved successfully as '{bar_plot_filename}'")
plt.show()
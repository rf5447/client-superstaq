import json
import os
import csv
from supermarq import converters
import supermarq
import cirq
from qiskit import qasm2, qasm3, transpile



# Configuration
input_directory = "ghz_ibm" 
output_csv = "ghz_benchmark_results.csv"

# CSV Column Headers
headers = [
    "benchmark", 
    "n_qubits", 
    "method", 
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
                
                # 1. Extract parameters to initialize the GHZ object
                n_qubits = data["n_qubits"]
                method = data["method"]
                counts = data["counts"]
                
                # 2. Initialize the specific GHZ benchmark to use its .score() method
                # This ensures the 'ideal_dist' is correctly generated for this N
                ghz_benchmark = supermarq.ghz.GHZ(n_qubits, method)
                # Reverse each bitstring to convert Little-Endian (IBM) to Big-Endian (SupermarQ)
                corrected_counts = {bitstr[::-1]: count for bitstr, count in counts.items()}

                # 3. Calculate Hellinger Fidelity score
                run_score = ghz_benchmark.score(corrected_counts)
                
                # 4. Prepare the row for CSV
                row = {
                    "benchmark": data.get("benchmark", "GHZ"),
                    "n_qubits": n_qubits,
                    "method": method,
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
methods = df['method'].unique()

# Create a figure with 3 subplots (1 row, 3 columns)
fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
fig.suptitle('SupermarQ GHZ Benchmark: Hellinger Fidelity by Method', fontsize=18, fontweight='bold')

# 3. Iterate through methods and create a plot for each
for i, method in enumerate(sorted(methods)):
    ax = axes[i]
    method_data = df[df['method'] == method]
    
    # Draw lines and points for each backend
    sns.lineplot(
        data=method_data, 
        x='n_qubits', 
        y='score', 
        hue='backend', 
        marker='o', 
        ax=ax,
        linewidth=2.5,
        markersize=8
    )
    
    ax.set_title(f"Method: {method.capitalize()}", fontsize=14, fontweight='semibold')
    ax.set_xlabel("Number of Qubits", fontsize=12)
    ax.set_ylabel("Hellinger Fidelity (Score)", fontsize=12)
    ax.set_ylim(-0.05, 1.05)  # Fidelity is always 0 to 1
    ax.legend(title="IBM Backend", frameon=True)

# Adjust layout to prevent label overlap
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# 4. Save and Show
plot_filename = "ghz_performance_comparison.png"
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
methods = sorted(df['method'].unique())
qubit_counts = sorted(df['n_qubits'].unique())

# Create a figure with 3 subplots (one for each method)
fig, axes = plt.subplots(1, 3, figsize=(20, 6), sharey=True)

# Define a color palette similar to the reference image
# Blue, Orange, Green, Red
custom_palette = sns.color_palette("tab10", len(qubit_counts))

# 3. Iterate through methods to create bar charts
for i, method in enumerate(methods):
    ax = axes[i]
    method_data = df[df['method'] == method]
    
    # Create the grouped bar chart
    sns.barplot(
        data=method_data,
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
    ax.set_title(f"GHZ Method: {method.upper()}", fontsize=15, fontweight='bold', pad=20)
    ax.set_xlabel("Backend", fontsize=12)
    ax.set_ylabel("Score" if i == 0 else "", fontsize=12)
    ax.set_ylim(0, 1.05)
    
    # Place the legend in a similar spot to the reference image
    if i == 2: # Only show legend on the last plot or adjust as needed
        ax.legend(title="Qubits", loc='lower right', bbox_to_anchor=(1, 0.1), ncol=2)
    else:
        ax.get_legend().remove()

    # Add a horizontal line at 0 for clean aesthetics
    ax.axhline(0, color='black', linewidth=0.8)

plt.tight_layout()

# 4. Save and Show
bar_plot_filename = "ghz_bar_charts.png"
plt.savefig(bar_plot_filename, dpi=300)
print(f"\nBar chart saved successfully as '{bar_plot_filename}'")
plt.show()
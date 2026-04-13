import json
import os
import csv
import supermarq
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

# Configuration
input_directory = "ibmk/vqeproxy_ibmk" 
output_csv = "benchmark_resultsk/vqeproxy_benchmark_results.csv"

# Updated CSV Column Headers (Basis removed from rows since X/Z are combined into one score)
headers = ["benchmark", "n_qubits", "n_layers", "backend", "shots", "score", "job_id", "timestamp"]

all_rows = []

if not os.path.exists(input_directory):
    print(f"Error: Folder '{input_directory}' not found.")
else:
    # 1. Group files by (n_qubits, n_layers, backend) to pair X and Z bases
    file_groups = defaultdict(dict)
    
    for filename in os.listdir(input_directory):
        if filename.endswith(".json"):
            # Expected format: vqeproxy_q4_l1_x_ibm_fez.json
            parts = filename.replace(".json", "").split("_")
            try:
                nq = int(parts[1].replace("q", ""))
                nl = int(parts[2].replace("l", ""))
                basis = parts[3] # 'x' or 'z'
                backend = "_".join(parts[4:]) # 'ibm_fez', etc.
                
                group_key = (nq, nl, backend)
                file_groups[group_key][basis] = filename
            except (IndexError, ValueError):
                print(f"Skipping file with unexpected name format: {filename}")

    # 2. Process each pair
    for (nq, nl, backend), bases in file_groups.items():
        if "x" in bases and "z" in bases:
            try:
                # Load X and Z data
                with open(os.path.join(input_directory, bases["x"]), "r") as f_x:
                    data_x = json.load(f_x)
                with open(os.path.join(input_directory, bases["z"]), "r") as f_z:
                    data_z = json.load(f_z)

                # VQEProxy.score() expects a LIST of count dictionaries: [counts_z, counts_x]
                # Order matters: Supermarq's VQEProxy usually expects Z then X based on circuit order
                counts_list = [
                    {k[::-1]: v for k, v in data_z["counts"].items()},
                    {k[::-1]: v for k, v in data_x["counts"].items()}
                ]
                
                vqe = supermarq.vqe_proxy.VQEProxy(nq, nl)
                run_score = vqe.score(counts_list)
                
                all_rows.append({
                    "benchmark": "VQEProxy",
                    "n_qubits": nq,
                    "n_layers": nl,
                    "backend": backend,
                    "shots": data_z.get("shots"),
                    "score": run_score,
                    "job_id": f"{data_z.get('job_id')}/{data_x.get('job_id')}",
                    "timestamp": data_z.get("timestamp")
                })
                print(f"Processed {backend} (Q{nq} L{nl}): Score = {run_score:.4f}")
                
            except Exception as e:
                print(f"Failed to process group {nq}q_{nl}l_{backend}: {e}")
        else:
            missing = "z" if "x" in bases else "x"
            print(f"Warning: Missing {missing} basis for {backend} Q{nq} L{nl}. Skipping.")

# Save to CSV
with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(all_rows)

# # --- PLOTTING ---
# df = pd.DataFrame(all_rows)
# if not df.empty:
#     df[['n_qubits', 'score', 'n_layers']] = df[['n_qubits', 'score', 'n_layers']].apply(pd.to_numeric)
    
#     # Bar Plot Logic
#     sns.set_theme(style="white")
#     df['label'] = df['n_qubits'].astype(str) + "q, " + df['n_layers'].astype(str) + "L"
#     plt.figure(figsize=(12, 6))
    
#     sns.barplot(data=df.sort_values(['n_qubits', 'n_layers']), x='backend', y='score', hue='label')
    
#     plt.title("VQE Proxy Performance (Combined X+Z Score)", fontsize=16)
#     plt.ylim(0, 1.05)
#     plt.tight_layout()
#     plt.savefig("vqeproxy_combined_results.png", dpi=300)
#     plt.show()
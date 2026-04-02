from supermarq import converters
import supermarq
import cirq
from qiskit import qasm2, qasm3, transpile
import json
from datetime import datetime
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
import os

service = QiskitRuntimeService()
# You can now uncomment these and it will create 3 jobs
backend_names = ["ibm_fez", "ibm_torino", "ibm_marrakesh"]
SHOTS = 2000

# Ensure the output directory exists
os.makedirs("hamsim_ibm", exist_ok=True)

# 1. Organize circuits by backend
# Structure: { "backend_name": [list_of_transpiled_circs], ... }
backend_batches = {name: [] for name in backend_names}
# To keep track of n for the filenames later
metadata_batches = {name: [] for name in backend_names}

for nq in [4, 7, 11, 12, 13, 16, 20]:
    for steps in [1, 3, 4, 5, 7]:
        ts = steps #1
        tt = 1 * ts

        # Hamiltonian Simulation circuit
        circ = supermarq.hamiltonian_simulation.HamiltonianSimulation(nq, ts, tt).circuit()

        try:
            circ_qiskit = converters.cirq_to_qiskit(circ)
            
            for backend_name in backend_names:
                print(f"Transpiling nq={nq}, steps={steps}, ts={ts}, tt={tt} for {backend_name}")
                backend = service.backend(backend_name)
                
                # Transpile specifically for THIS backend
                circ_t = transpile(circ_qiskit, backend)
                
                backend_batches[backend_name].append(circ_t)
                # Store metadata for file naming
                metadata_batches[backend_name].append({
                    "nq": nq, 
                    "ts": ts,
                    "tt": tt,
                    "backend_obj": backend
                })
                
        except Exception as e:
            print(f"Error preparing nq={nq}, tt={tt}: {e}")

# 2. Submit one job per backend
for backend_name in backend_names:
    circs = backend_batches[backend_name]
    metas = metadata_batches[backend_name]
    
    if not circs:
        continue

    print(f"\nSubmitting batch to {backend_name} ({len(circs)} circuits)")
    
    # Initialize Sampler for this specific machine
    sampler = SamplerV2(mode=metas[0]["backend_obj"])
    job = sampler.run(circs, shots=SHOTS)
    print(f"Job submitted! ID: {job.job_id()}")

    # Wait for result
    result = job.result()

    # 3. Save each circuit's data from the batch
    for i, pub_result in enumerate(result):
        m = metas[i]
        counts = pub_result.join_data().get_counts()

        output = {
            "benchmark": "HamiltonianSimulation",
            "n_qubits": m["nq"],
            "ts": m["ts"],
            "tt": m["tt"],
            "backend": backend_name,
            "shots": SHOTS,
            "job_id": job.job_id(),
            "timestamp": str(datetime.now()),
            "counts": counts
        }

        # Filename updated to reflect hamsim_ibm directory and unique params
        filename = f"hamsim_ibm/hamsim_q{m['nq']}_ts{m['ts']}_tt{m['tt']}_{backend_name}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)
        
        print(f"Saved: {filename}")
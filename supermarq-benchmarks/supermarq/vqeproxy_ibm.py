from supermarq import converters
import supermarq
import cirq
from qiskit import qasm2, qasm3, transpile
import json
from datetime import datetime
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
import os

service = QiskitRuntimeService()
backend_names = ["ibm_kingston"]#["ibm_fez", "ibm_marrakesh", "ibm_kingston"]
SHOTS = 2000

# Ensure the output directory exists
os.makedirs("vqeproxy_ibm", exist_ok=True)

# 1. Organize circuits by backend
backend_batches = {name: [] for name in backend_names}
metadata_batches = {name: [] for name in backend_names}

for nq in [4, 7, 9]:
    for nl in [1, 2, 3, 4, 5]:
        # VQEProxy returns a list of circuits (usually Z and X basis)
        circuits = supermarq.vqe_proxy.VQEProxy(nq, nl).circuit()

        for idx, circ in enumerate(circuits):
            try:
                circ_qiskit = converters.cirq_to_qiskit(circ)
                basis_label = "z" if idx == 0 else "x"
                
                for backend_name in backend_names:
                    print(f"Transpiling nq={nq}, nl={nl}, basis={basis_label} for {backend_name}")
                    backend = service.backend(backend_name)
                    
                    # Transpile specifically for THIS backend
                    circ_t = transpile(circ_qiskit, backend)
                    
                    backend_batches[backend_name].append(circ_t)
                    # Store nq, nl, and basis in metadata
                    metadata_batches[backend_name].append({
                        "nq": nq, 
                        "nl": nl, 
                        "basis": basis_label,
                        "backend_obj": backend
                    })
                    
            except Exception as e:
                print(f"Error preparing nq={nq}, nl={nl}, circ={idx}: {e}")

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
            "benchmark": "VQEProxy",
            "n_qubits": m["nq"],
            "n_layers": m["nl"],
            "basis": m["basis"],
            "backend": backend_name,
            "shots": SHOTS,
            "job_id": job.job_id(),
            "timestamp": str(datetime.now()),
            "counts": counts
        }

        # Filename updated for VQE parameters
        filename = f"vqeproxy_ibm/vqeproxy_q{m['nq']}_l{m['nl']}_{m['basis']}_{backend_name}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)
        
        print(f"Saved: {filename}")
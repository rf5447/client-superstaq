from supermarq import converters
import supermarq
import cirq
from qiskit import qasm2, qasm3, transpile
import json
from datetime import datetime
# from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
from qiskit_ibm_runtime.fake_provider import FakeBelemV2
from qiskit_ibm_runtime import SamplerV2

# service = QiskitRuntimeService()
#backend_names = #["ibm_fez"]#, "ibm_marrakesh", "ibm_torino"]
SHOTS = 2000

for n in [3]:#, 4, 5, 7, 11]:#, 9, 20, 25, 30, 50]:
    for method in ["ladder"]:#, "star", "logdepth"]:

        circ = supermarq.ghz.GHZ(n, method).circuit()

        try:
            circ_qiskit = converters.cirq_to_qiskit(circ)

            #for backend_name in backend_names:
            backend_name = "FakeBelemV2"
            print(f"Running n={n}, method={method} on {backend_name}")
            backend = FakeBelemV2() #service.backend(backend_name)
            sampler = SamplerV2(mode=backend)

            circ_t = transpile(circ_qiskit, backend)

            # NOTE: SamplerV2 takes a list of circuits
            job = sampler.run([circ_t], shots=SHOTS)
            print("Submitted job:", job.job_id())

            result = job.result()
            pub_result = result[0]

            # Raw integer counts
            joined_result = pub_result.join_data()
            # This joins all registers (like 'm0') and gets the counts
            counts = joined_result.get_counts()
            print(counts)

            output = {
                "benchmark": "GHZ",
                "n_qubits": n,
                "method": method,
                "backend": backend_name,
                "shots": SHOTS,
                "job_id": job.job_id(),
                "timestamp": str(datetime.now()),
                "counts": counts
            }

            filename = f"ghz_ibm/ghz_{n}_{method}_{backend_name}.json"

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2)

            print(f"Success! File '{filename}' created.")

        except Exception as e:
            print(f"Error for n={n}, method={method}: {e}")

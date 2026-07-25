from supermarq import converters
import supermarq
import json
from datetime import datetime
from pathlib import Path

from credentials_ionq import IONQ_API_KEY
from qiskit_ionq import IonQProvider

SHOTS = 2000
OUTDIR = Path("ghz_ionq")
OUTDIR.mkdir(exist_ok=True)

provider = IonQProvider(IONQ_API_KEY)

backend_name = "ionq_simulator"
backend = provider.get_backend(backend_name)

# Choose one:
noise_model = None          # ideal simulator
# noise_model = "aria-1"    # noisy Aria simulator
# noise_model = "forte-1"   # noisy Forte simulator

if noise_model is not None:
    backend.set_options(noise_model=noise_model)

for n in [3]:
    for method in ["ladder"]:
        try:
            circ = supermarq.ghz.GHZ(n, method).circuit()
            circ_qiskit = converters.cirq_to_qiskit(circ)

            # Safety check: IonQ needs sampled measurements
            if not any(inst.operation.name == "measure" for inst in circ_qiskit.data):
                circ_qiskit.measure_all()

            run_label = noise_model if noise_model is not None else "ideal"
            print(f"Running n={n}, method={method} on {backend_name} ({run_label})")

            job = backend.run(circ_qiskit, shots=SHOTS)
            print("Submitted job:", job.job_id())

            result = job.result()

            try:
                counts = result.get_counts(0)
            except Exception:
                counts = result.get_counts()

            # Convert NumPy integers to regular Python integers
            counts = {bitstring: int(count) for bitstring, count in counts.items()}

            print(counts)

            output = {
                "benchmark": "GHZ",
                "n_qubits": n,
                "method": method,
                "backend": backend_name,
                "noise_model": noise_model,
                "shots": SHOTS,
                "job_id": job.job_id(),
                "timestamp": str(datetime.now()),
                "counts": counts,
            }

            filename = OUTDIR / f"ghz_{n}_{method}_{backend_name}_{run_label}.json"

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2)

            print(f"Success! File '{filename}' created.")

        except Exception as e:
            print(f"Error for n={n}, method={method}: {e}")
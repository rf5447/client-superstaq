from supermarq import converters
import supermarq
import json
from datetime import datetime
from pathlib import Path

from credentials_ionq import IONQ_API_KEY
from qiskit_ionq import IonQProvider


SHOTS = 2000

# Keep simulator sizes aligned with Forte-1's 36-qubit limit.
QUBIT_COUNTS = [29] #[3, 4, 5, 7, 11, 25] #36]
METHODS = ["ladder", "star", "logdepth"]

# Run the complete experiment twice.
EXPERIMENTS = ["ionq_1", "ionq_2"]

provider = IonQProvider(IONQ_API_KEY)

backend_name = "ionq_simulator"
backend = provider.get_backend(backend_name)

# Choose simulator type:
noise_model = None
# noise_model = "forte-1"

if noise_model is not None:
    backend.set_options(noise_model=noise_model)

run_label = noise_model if noise_model is not None else "ideal"


for experiment in EXPERIMENTS:
    outdir = Path(experiment) / "ghz"
    outdir.mkdir(parents=True, exist_ok=True)

    print(f"\nStarting experiment set: {experiment}")

    for n in QUBIT_COUNTS:
        for method in METHODS:
            try:
                circ = supermarq.ghz.GHZ(n, method).circuit()
                circ_qiskit = converters.cirq_to_qiskit(circ)

                # IonQ requires measurements for shot-based results.
                if not any(
                    instruction.operation.name == "measure"
                    for instruction in circ_qiskit.data
                ):
                    circ_qiskit.measure_all()

                print(
                    f"Running experiment={experiment}, "
                    f"n={n}, method={method}, "
                    f"backend={backend_name}, "
                    f"simulation={run_label}"
                )

                job = backend.run(
                    circ_qiskit,
                    shots=SHOTS,
                )

                print("Submitted job:", job.job_id())

                result = job.result()

                try:
                    counts = result.get_counts(0)
                except Exception:
                    counts = result.get_counts()

                # Convert NumPy integer values to normal Python integers
                # so they can be written to JSON.
                counts = {
                    str(bitstring): int(count)
                    for bitstring, count in counts.items()
                }

                output = {
                    "benchmark": "GHZ",
                    "experiment": experiment,
                    "n_qubits": n,
                    "method": method,
                    "backend": backend_name,
                    "noise_model": noise_model,
                    "shots": SHOTS,
                    "job_id": job.job_id(),
                    "timestamp": datetime.now().isoformat(),
                    "counts": counts,
                }

                filename = (
                    outdir
                    / f"ghz_{n}_{method}_sim_{run_label}.json"
                )

                with filename.open("w", encoding="utf-8") as f:
                    json.dump(output, f, indent=2)

                print(f"Saved: {filename}")

            except Exception as e:
                print(
                    f"Error for experiment={experiment}, "
                    f"n={n}, method={method}: {e}"
                )
from supermarq import converters
import supermarq
import json
from datetime import datetime
from pathlib import Path

from credentials_ionq import IONQ_API_KEY
from qiskit_ionq import IonQProvider


SHOTS = 2000

# Match the Mermin-Bell qubit sweep used in mb_ibm.py.
QUBIT_COUNTS = [3, 4, 5, 7, 11, 15] #, 20, 25, 29] #[20] #[3, 4, 5, 7, 11, 15, 20, 25, 29]

# Run the complete experiment twice.
EXPERIMENTS = ["ionq_2"] #["ionq_1", "ionq_2"]

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
    outdir = Path(experiment) / "mb"
    outdir.mkdir(parents=True, exist_ok=True)

    print(f"\nStarting experiment set: {experiment}")

    for n in QUBIT_COUNTS:
        try:
            circ = supermarq.mermin_bell.MerminBell(n).circuit()
            circ_qiskit = converters.cirq_to_qiskit(circ)

            # IonQ requires measurements for shot-based results.
            if not any(
                instruction.operation.name == "measure"
                for instruction in circ_qiskit.data
            ):
                circ_qiskit.measure_all()

            print(
                f"Running experiment={experiment}, "
                f"n={n}, "
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

            counts = {
                str(bitstring): int(count)
                for bitstring, count in counts.items()
            }

            output = {
                "benchmark": "MerminBell",
                "experiment": experiment,
                "n_qubits": n,
                "backend": backend_name,
                "noise_model": noise_model,
                "shots": SHOTS,
                "job_id": job.job_id(),
                "timestamp": datetime.now().isoformat(),
                "counts": counts,
            }

            filename = outdir / f"mb_{n}_sim_{run_label}.json"

            with filename.open("w", encoding="utf-8") as f:
                json.dump(output, f, indent=2)

            print(f"Saved: {filename}")

        except Exception as e:
            print(
                f"Error for experiment={experiment}, "
                f"n={n}: {e}"
            )
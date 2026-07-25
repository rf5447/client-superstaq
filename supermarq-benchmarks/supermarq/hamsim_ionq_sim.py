from supermarq import converters
import supermarq
import json
from datetime import datetime
from pathlib import Path

from credentials_ionq import IONQ_API_KEY
from qiskit_ionq import IonQProvider

SHOTS = 2000
QUBIT_COUNTS = [25, 29]  # [4, 7, 11, 12, 13, 16, 20]
STEPS = [1, 3, 4, 5, 7]
EXPERIMENTS = ["ionq_1", "ionq_2"]

provider = IonQProvider(IONQ_API_KEY)
backend_name = "ionq_simulator"
backend = provider.get_backend(backend_name)

noise_model = None
# noise_model = "forte-1"

if noise_model is not None:
    backend.set_options(noise_model=noise_model)

run_label = noise_model if noise_model is not None else "ideal"

for experiment in EXPERIMENTS:
    outdir = Path(experiment) / "hamsim"
    outdir.mkdir(parents=True, exist_ok=True)

    print(f"\nStarting experiment set: {experiment}")

    for nq in QUBIT_COUNTS:
        for steps in STEPS:
            ts = steps
            tt = ts

            try:
                circ = supermarq.hamiltonian_simulation.HamiltonianSimulation(
                    nq, ts, tt
                ).circuit()
                circ_qiskit = converters.cirq_to_qiskit(circ)

                if not any(
                    instruction.operation.name == "measure"
                    for instruction in circ_qiskit.data
                ):
                    circ_qiskit.measure_all()

                print(
                    f"Running experiment={experiment}, nq={nq}, steps={steps}, "
                    f"ts={ts}, tt={tt}, backend={backend_name}, simulation={run_label}"
                )

                job = backend.run(circ_qiskit, shots=SHOTS)
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
                    "benchmark": "HamiltonianSimulation",
                    "experiment": experiment,
                    "n_qubits": nq,
                    "steps": steps,
                    "ts": ts,
                    "tt": tt,
                    "backend": backend_name,
                    "noise_model": noise_model,
                    "shots": SHOTS,
                    "job_id": job.job_id(),
                    "timestamp": datetime.now().isoformat(),
                    "counts": counts,
                }

                filename = outdir / f"hamsim_q{nq}_ts{ts}_tt{tt}_sim_{run_label}.json"
                with filename.open("w", encoding="utf-8") as f:
                    json.dump(output, f, indent=2)

                print(f"Saved: {filename}")

            except Exception as e:
                print(
                    f"Error for experiment={experiment}, nq={nq}, "
                    f"steps={steps}, ts={ts}, tt={tt}: {e}"
                )
from supermarq import converters
import supermarq
import json
from datetime import datetime
from pathlib import Path

from credentials_ionq import IONQ_API_KEY
from qiskit_ionq import IonQProvider


SHOTS = 2000

# Keep original VQEProxy sizes and extend through 25 qubits for simulation.
QUBIT_COUNTS = [4, 7, 9, 11, 25]
N_LAYERS = [1, 2, 3, 4, 5]

# Run the complete experiment twice.
EXPERIMENTS = ["ionq_2"]#["ionq_1", "ionq_2"]

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
    outdir = Path(experiment) / "vqe"
    outdir.mkdir(parents=True, exist_ok=True)

    print(f"\nStarting experiment set: {experiment}")

    for nq in QUBIT_COUNTS:
        for nl in N_LAYERS:
            # Keep VQEProxy construction exactly the same as the IBM version.
            # This returns the two basis circuits used by the benchmark.
            circuits = supermarq.vqe_proxy.VQEProxy(nq, nl).circuit()

            for idx, circ in enumerate(circuits):
                basis_label = "z" if idx == 0 else "x"

                try:
                    # circ_qiskit = converters.cirq_to_qiskit(circ)
                    circ_qiskit = converters.cirq_to_qiskit(
                        circ,
                        list(circ.all_qubits()),
                    )
                    # IonQ needs measurements to return shot-based counts.
                    # VQEProxy should already contain the appropriate
                    # basis-specific measurements, so this is only a safety check.
                    if not any(
                        instruction.operation.name == "measure"
                        for instruction in circ_qiskit.data
                    ):
                        circ_qiskit.measure_all()

                    print(
                        f"Running experiment={experiment}, "
                        f"nq={nq}, nl={nl}, basis={basis_label}, "
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
                        "benchmark": "VQEProxy",
                        "experiment": experiment,
                        "n_qubits": nq,
                        "n_layers": nl,
                        "basis": basis_label,
                        "backend": backend_name,
                        "noise_model": noise_model,
                        "shots": SHOTS,
                        "job_id": job.job_id(),
                        "timestamp": datetime.now().isoformat(),
                        "counts": counts,
                    }

                    filename = (
                        outdir
                        / f"vqeproxy_q{nq}_l{nl}_{basis_label}_sim_{run_label}.json"
                    )

                    with filename.open("w", encoding="utf-8") as f:
                        json.dump(output, f, indent=2)

                    print(f"Saved: {filename}")

                except Exception as e:
                    print(
                        f"Error for experiment={experiment}, "
                        f"nq={nq}, nl={nl}, basis={basis_label}: {e}"
                    )
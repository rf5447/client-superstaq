import os
import numpy as np
from supermarq import converters
import supermarq
from qiskit import qasm2
from qiskit.quantum_info import Statevector, state_fidelity

def verify_correctness(directory="hamsim_qasm"):
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' not found.")
        return

    files = sorted([f for f in os.listdir(directory) if f.endswith(".txt")])

    print("Verifying Mathematical Correctness (Fidelity Check)")
    print("-" * 85)
    print(f"{'Filename':<50} | {'Qubits':<6} | {'Result'}")
    print("-" * 85)

    for filename in files:
        try:
            parts = filename.split('_')
            nq = int(parts[1])
            ts = int(parts[4])
            tt = int(parts[6])

            circ = supermarq.hamiltonian_simulation.HamiltonianSimulation(nq, ts, tt).circuit()
            ideal_qc = converters.cirq_to_qiskit(circ)

            path = os.path.join(directory, filename)
            sliced_qc = qasm2.load(path)

            # Remove measurements if present
            ideal_qc = ideal_qc.remove_final_measurements(inplace=False)
            sliced_qc = sliced_qc.remove_final_measurements(inplace=False)

            sv_ideal = Statevector.from_instruction(ideal_qc)
            sv_sliced = Statevector.from_instruction(sliced_qc)

            fid = state_fidelity(sv_ideal, sv_sliced)

            is_correct = np.isclose(fid, 1.0, atol=1e-10)
            res = "CORRECT" if is_correct else "INCORRECT"

            print(f"{filename:<50} | {nq:<6} | {res} (Fid: {fid:.10f})")

        except Exception as e:
            print(f"{filename:<50} | ERROR: {e}")

if __name__ == "__main__":
    verify_correctness()

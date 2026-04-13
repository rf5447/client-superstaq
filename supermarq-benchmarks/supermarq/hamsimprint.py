import os

import supermarq
import cirq
from cirq.contrib.svg import circuit_to_svg
import cairosvg


def save_circuit_png(circuit: cirq.Circuit, out_path: str):
    svg = circuit_to_svg(circuit)
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=out_path)


out_dir = "hamsim_circuit_pngs"
os.makedirs(out_dir, exist_ok=True)

for nq in [4, 7, 11]:
    for steps in [1, 3, 4]:
        ts = steps #1
        tt = 1 * ts
        print(f"Rendering num_qubits={nq}, time_steps={ts}, total_time={tt}...")

        hamsim = supermarq.hamiltonian_simulation.HamiltonianSimulation(nq, ts, tt)
        hamsim_circuit = hamsim.circuit()

        out_path = os.path.join(out_dir, f"hamsim_{nq}q_{ts}ts_{tt}tt.png")
        save_circuit_png(hamsim_circuit, out_path)

print(f"\nSaved circuit images to {out_dir}/")
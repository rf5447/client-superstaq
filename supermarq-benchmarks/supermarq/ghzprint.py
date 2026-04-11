import os

import supermarq
import cirq
from cirq.contrib.svg import circuit_to_svg
import cairosvg


def save_circuit_png(circuit: cirq.Circuit, out_path: str):
    svg = circuit_to_svg(circuit)
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=out_path)


out_dir = "ghz_circuit_pngs"
os.makedirs(out_dir, exist_ok=True)

for method in ["star", "ladder", "logdepth"]:
    for num_qubits in range(3, 11):
        print(f"Rendering method={method}, num_qubits={num_qubits}")

        ghz = supermarq.ghz.GHZ(num_qubits, method=method)
        ghz_circuit = ghz.circuit()

        out_path = os.path.join(out_dir, f"ghz_{method}_{num_qubits}q.png")
        save_circuit_png(ghz_circuit, out_path)

print(f"\nSaved circuit images to {out_dir}/")
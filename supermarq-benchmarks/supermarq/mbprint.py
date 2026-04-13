import os

import supermarq
import cirq
from cirq.contrib.svg import circuit_to_svg
import cairosvg


def save_circuit_png(circuit: cirq.Circuit, out_path: str):
    svg = circuit_to_svg(circuit)
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=out_path)


out_dir = "mb_circuit_pngs"
os.makedirs(out_dir, exist_ok=True)

for num_qubits in range(3, 11):
    print(f"Rendering num_qubits={num_qubits}")

    mb = supermarq.mermin_bell.MerminBell(num_qubits)
    mb_circuit = mb.circuit()

    out_path = os.path.join(out_dir, f"mb_{num_qubits}q.png")
    save_circuit_png(mb_circuit, out_path)

print(f"\nSaved circuit images to {out_dir}/")
import os

import supermarq
import cirq
from cirq.contrib.svg import circuit_to_svg
import cairosvg


def save_circuit_png(circuit: cirq.Circuit, out_path: str):
    svg = circuit_to_svg(circuit)
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=out_path)


out_dir = "bitcode_circuit_pngs"
os.makedirs(out_dir, exist_ok=True)

for nq in [3, 4, 5, 7, 9]:
    for nr in [2, 3, 4]: #, 5, 7, 9]:
        print(f"Rendering num_qubits={nq}, num_rounds={nr}")
        bit_state = [i % 2 for i in range(nq)]

        bitcode = supermarq.bit_code.BitCode(nq, nr, bit_state)
        bitcode_circuit = bitcode.circuit()

        out_path = os.path.join(out_dir, f"bitcode_{nq}q_{nr}r.png")
        save_circuit_png(bitcode_circuit, out_path)

print(f"\nSaved circuit images to {out_dir}/")
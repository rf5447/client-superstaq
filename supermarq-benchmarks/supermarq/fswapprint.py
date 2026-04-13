import os

import supermarq
import cirq
from cirq.contrib.svg import circuit_to_svg
import cairosvg


def save_circuit_png(circuit: cirq.Circuit, out_path: str):
    svg = circuit_to_svg(circuit)
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=out_path)


out_dir = "fswap_circuit_pngs"
os.makedirs(out_dir, exist_ok=True)

for n in [3, 4, 5, 7, 11, 12, 13, 16]: 

    print(f"Rendering num_qubits={n}...")

    fswap = supermarq.qaoa_fermionic_swap_proxy.QAOAFermionicSwapProxy(n)
    fswap_circuit = fswap.circuit()

    out_path = os.path.join(out_dir, f"fswap_{n}q.png")
    save_circuit_png(fswap_circuit, out_path)

print(f"\nSaved circuit images to {out_dir}/")
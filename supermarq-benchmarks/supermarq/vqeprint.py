import os

import supermarq
import cirq
from cirq.contrib.svg import circuit_to_svg
import cairosvg
from supermarq.benchmarks import vqe_proxy


def save_circuit_png(circuit: cirq.Circuit, out_path: str):
    svg = circuit_to_svg(circuit)
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=out_path)


out_dir = "vqe_circuit_pngs"
os.makedirs(out_dir, exist_ok=True)

for nq in [4, 7]:
    for nl in [1, 2, 3]:

        print(f"Rendering nq={nq}, nl={nl}...")

        res = vqe_proxy.VQEProxy(nq, nl).circuit()

        # VQE returns [z_circuit, x_circuit]
        if isinstance(res, (list, tuple)):
            circuits = list(res)
        elif isinstance(res, dict) and "circuit" in res:
            circuits = res["circuit"]
            if not isinstance(circuits, (list, tuple)):
                circuits = [circuits]
        else:
            circuits = [res]

        for i, circuit in enumerate(circuits):
            out_path = os.path.join(out_dir, f"vqe_{nq}q_{nl}layers_circuit{i}.png")
            save_circuit_png(circuit, out_path)

print(f"\nSaved circuit images to {out_dir}/")
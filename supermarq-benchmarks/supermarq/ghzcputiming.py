import collections
import time
import csv
import os
import socket
import subprocess
from typing import Dict

import supermarq
import cirq


def print_hardware_info():
    print("=" * 60)
    print("Hardware / job environment info")
    print("=" * 60)

    # Host / SLURM environment
    print(f"Hostname: {socket.gethostname()}")
    print(f"SLURM job ID: {os.environ.get('SLURM_JOB_ID', 'N/A')}")
    print(f"SLURM node list: {os.environ.get('SLURM_JOB_NODELIST', 'N/A')}")

    # CPU info
    try:
        cpu_model = subprocess.check_output(
            "lscpu | grep 'Model name' | sed 's/Model name:[[:space:]]*//'",
            shell=True,
            text=True,
        ).strip()
        print(f"CPU: {cpu_model}")
    except Exception as e:
        print(f"CPU: could not query ({e})")

    print("=" * 60)


def noisy_simulation(circuit: cirq.Circuit, p: float) -> collections.Counter:
    shots = 1000
    result = cirq.Simulator().run(
        circuit.with_noise(cirq.depolarize(p=p)),
        repetitions=shots,
    )

    num_measured_qubits = []
    for _, op in circuit.findall_operations(cirq.is_measurement):
        num_measured_qubits.append(len(op.qubits))
    raw_counts = result.multi_measurement_histogram(keys=result.measurements.keys())

    counts: Dict[str, float] = collections.defaultdict(float)
    for key, val in raw_counts.items():
        bit_list = []
        for int_tag, num_bits in zip(key, num_measured_qubits):
            bit_list.extend(cirq.value.big_endian_int_to_bits(int_tag, bit_count=num_bits))
        counts["".join(str(b) for b in bit_list)] = val / shots

    return collections.Counter(counts)


def run_one_case(method, num_qubits):
    print(f"\nmethod = {method}, num_qubits = {num_qubits}")

    t0 = time.perf_counter()
    ghz = supermarq.ghz.GHZ(num_qubits, method=method)
    ghz_circuit = ghz.circuit()
    t1 = time.perf_counter()
    build_ms = (t1 - t0) * 1e3

    error_prob = 0.0

    s0 = time.perf_counter()
    counts = noisy_simulation(ghz_circuit, p=error_prob)
    s1 = time.perf_counter()
    sim_ms = (s1 - s0) * 1e3

    c0 = time.perf_counter()
    score = ghz.score(counts)
    c1 = time.perf_counter()
    score_ms = (c1 - c0) * 1e3

    total_ms = build_ms + sim_ms + score_ms

    print(
        f"  With {error_prob*100:.1f}% error probability, "
        f"GHZ score = {score:.4f} | sim time: {sim_ms:.2f} ms "
        f"| score time: {score_ms:.2f} ms"
    )

    return [
        method,
        num_qubits,
        f"{score:.6f}",
        f"{build_ms:.3f}",
        f"{sim_ms:.3f}",
        f"{score_ms:.3f}",
        f"{total_ms:.3f}",
    ]


print_hardware_info()

out_path = "ghz_timing_results_excludingwarmup_ordered.csv"
write_header = not os.path.exists(out_path)

with open(out_path, "a", newline="") as f:
    w = csv.writer(f)
    if write_header:
        w.writerow([
            "method",
            "num_qubits",
            "Score (0.0% error)",
            "Circuit creation time (ms)",
            "Simulation time (ms)",
            "Score calculation time (ms)",
            "Total time (ms)"
        ])

    # One warm-up run only; do not write it
    _ = run_one_case("star", 3)

    # Real runs: 3 repetitions for 3..10
    for rep in range(3):
        for method in ["logdepth", "ladder", "star"]:
            for num_qubits in range(3, 11):
                row = run_one_case(method, num_qubits)
                w.writerow(row)

print(f"\nWrote results to {out_path}")
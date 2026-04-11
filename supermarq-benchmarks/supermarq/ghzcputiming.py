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


print_hardware_info()

out_path = "ghz_timing_results.csv"
write_header = not os.path.exists(out_path)

with open(out_path, "a", newline="") as f:
    w = csv.writer(f)
    if write_header:
        w.writerow([
            "method",
            "num_qubits",
            "Score (0.0% error)",
            "Score (0.5% error)",
            "Score (2.0% error)",
            "Circuit creation time (ms)",
            "Simulation time (ms)",
            "Score calculation time (ms)",
            "Total time (ms)"
        ])

    for method in ["star", "ladder", "logdepth"]:
        for num_qubits in range(3, 11):
            print(f"\nmethod = {method}, num_qubits = {num_qubits}")

            t0 = time.perf_counter()
            ghz = supermarq.ghz.GHZ(num_qubits, method=method)
            ghz_circuit = ghz.circuit()
            t1 = time.perf_counter()
            build_ms = (t1 - t0) * 1e3

            ghz_scores = []
            sim_times_ms = []
            score_times_ms = []
            error_probs = [0.0, 0.005, 0.02]

            for error_prob in error_probs:
                s0 = time.perf_counter()
                counts = noisy_simulation(ghz_circuit, p=error_prob)
                s1 = time.perf_counter()

                c0 = time.perf_counter()
                score = ghz.score(counts)
                c1 = time.perf_counter()

                ghz_scores.append((error_prob, score))
                sim_times_ms.append((error_prob, (s1 - s0) * 1e3))
                score_times_ms.append((error_prob, (c1 - c0) * 1e3))

                print(
                    f"  With {error_prob*100:.1f}% error probability, "
                    f"GHZ score = {score:.4f} | sim time: {sim_times_ms[-1][1]:.2f} ms "
                    f"| score time: {score_times_ms[-1][1]:.2f} ms"
                )

            total_sim_ms = sum(t for _, t in sim_times_ms)
            total_score_ms = sum(t for _, t in score_times_ms)
            total_ms = build_ms + total_sim_ms + total_score_ms

            score_0 = next(s for (p, s) in ghz_scores if p == 0.0)
            score_05 = next(s for (p, s) in ghz_scores if p == 0.005)
            score_2_0 = next(s for (p, s) in ghz_scores if p == 0.02)

            w.writerow([
                method,
                num_qubits,
                f"{score_0:.6f}",
                f"{score_05:.6f}",
                f"{score_2_0:.6f}",
                f"{build_ms:.3f}",
                f"{total_sim_ms:.3f}",
                f"{total_score_ms:.3f}",
                f"{total_ms:.3f}",
            ])

print(f"\nWrote results to {out_path}")
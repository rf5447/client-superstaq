import features
from benchmarks import mermin_bell, bit_code, phase_code, vqe_proxy, qaoa_vanilla_proxy, qaoa_fermionic_swap_proxy, bit_code_old, phase_code_old
import supermarq
import matplotlib.pyplot as plt

import numpy as np
from matplotlib import font_manager as fm

fm.fontManager.addfont("/usr/share/fonts/msttcorefonts/times.ttf")
plt.rcParams["font.family"] = "Times New Roman"

# VQE feature example
title = 'VQE Scaling'
labels = []
feature_vecs = []
for nq in [4, 7]:
    for nl in [1, 2]:
        # for nr in [2, 3]:#, 4, 5, 6, 7, 8, 9, 10]:
        print(f'{nq} qubits, {nl} layers')
        labels.append(f'{nq} qubits, {nl} layers')
        
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

        # compute features for each circuit, then average across the benchmark
        per_circuit_features = []
        for circ in circuits:
            con = supermarq.features.compute_communication(circ)
            liv = supermarq.features.compute_liveness(circ)
            par = supermarq.features.compute_parallelism(circ)
            mea = supermarq.features.compute_measurement(circ)
            ent = supermarq.features.compute_entanglement(circ)
            dep = supermarq.features.compute_depth(circ)
            per_circuit_features.append([con, liv, par, mea, ent, dep])

        avg_features = np.mean(per_circuit_features, axis=0)
        feature_vecs.append(avg_features)

spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']

supermarq.plotting.plot_benchmark(
    "",
    labels,
    feature_vecs,
    spoke_labels=spoke_labels,
    legend_loc=(1.05, 0.25),
    savefn=f"paper_features/{title.replace(' ', '_')}_orig.png",
    show=False,
)

# VQE feature example
title = 'VQE Scaling'
labels = []
feature_vecs = []

for nq in [4, 7, 10]:
    for nl in [1]:
        print(f'{nq} qubits, {nl} layers')
        labels.append(f'{nq} qubits, {nl} layers')

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

        # compute features for each circuit, then average across the benchmark
        per_circuit_features = []
        for circ in circuits:
            con = supermarq.features.compute_communication(circ)
            liv = supermarq.features.compute_liveness(circ)
            par = supermarq.features.compute_parallelism(circ)
            mea = supermarq.features.compute_measurement(circ)
            ent = supermarq.features.compute_entanglement(circ)
            dep = supermarq.features.compute_depth(circ)
            per_circuit_features.append([con, liv, par, mea, ent, dep])

        avg_features = np.mean(per_circuit_features, axis=0)
        feature_vecs.append(avg_features)

spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
supermarq.plotting.plot_benchmark(
    "",
    labels,
    feature_vecs,
    spoke_labels=spoke_labels,
    legend_loc=(1.05, 0.25),
    savefn=f"paper_features/{title.replace(' ', '_')}_nl1.png",
    show=False,
)

# VQE feature example
title = 'VQE Scaling'
labels = []
feature_vecs = []

for nq in [4, 7, 10]:
    for nl in [2]:
        print(f'{nq} qubits, {nl} layers')
        labels.append(f'{nq} qubits, {nl} layers')

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

        # compute features for each circuit, then average across the benchmark
        per_circuit_features = []
        for circ in circuits:
            con = supermarq.features.compute_communication(circ)
            liv = supermarq.features.compute_liveness(circ)
            par = supermarq.features.compute_parallelism(circ)
            mea = supermarq.features.compute_measurement(circ)
            ent = supermarq.features.compute_entanglement(circ)
            dep = supermarq.features.compute_depth(circ)
            per_circuit_features.append([con, liv, par, mea, ent, dep])

        avg_features = np.mean(per_circuit_features, axis=0)
        feature_vecs.append(avg_features)

spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
supermarq.plotting.plot_benchmark(
    "",
    labels,
    feature_vecs,
    spoke_labels=spoke_labels,
    legend_loc=(1.05, 0.25),
    savefn=f"paper_features/{title.replace(' ', '_')}_nl2.png",
    show=False,
)


# VQE feature example
title = 'VQE Scaling'
labels = []
feature_vecs = []

for nq in [4, 7, 10]:
    for nl in [3]:
        print(f'{nq} qubits, {nl} layers')
        labels.append(f'{nq} qubits, {nl} layers')

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

        # compute features for each circuit, then average across the benchmark
        per_circuit_features = []
        for circ in circuits:
            con = supermarq.features.compute_communication(circ)
            liv = supermarq.features.compute_liveness(circ)
            par = supermarq.features.compute_parallelism(circ)
            mea = supermarq.features.compute_measurement(circ)
            ent = supermarq.features.compute_entanglement(circ)
            dep = supermarq.features.compute_depth(circ)
            per_circuit_features.append([con, liv, par, mea, ent, dep])

        avg_features = np.mean(per_circuit_features, axis=0)
        feature_vecs.append(avg_features)

spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
supermarq.plotting.plot_benchmark(
    "",
    labels,
    feature_vecs,
    spoke_labels=spoke_labels,
    legend_loc=(1.05, 0.25),
    savefn=f"paper_features/{title.replace(' ', '_')}_nl3.png",
    show=False,
)

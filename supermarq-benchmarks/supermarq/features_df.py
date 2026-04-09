import pandas as pd
import features
from benchmarks import ghz, mermin_bell, bit_code, phase_code, hamiltonian_simulation, vqe_proxy, qaoa_vanilla_proxy, qaoa_fermionic_swap_proxy
import supermarq
import numpy as np

# GHZ

print("Computing features for GHZ benchmark...")
title = 'ghz'
labels = []
feature_vecs = []

for n in [3, 4, 5, 7, 11, 15, 20, 25, 30, 40, 50, 75, 100, 125]: 
        labels.append(f'ghz_{n}qubits')
        circ = ghz.GHZ(n).circuit()
        con = supermarq.features.compute_communication(circ)
        liv = supermarq.features.compute_liveness(circ)
        par = supermarq.features.compute_parallelism(circ)
        mea = supermarq.features.compute_measurement(circ)
        ent = supermarq.features.compute_entanglement(circ)
        dep = supermarq.features.compute_depth(circ)
        feature_vecs.append([con, liv, par, mea, ent, dep])

spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']

# Save features to dataframe
feature_df = pd.DataFrame(feature_vecs, index=labels, columns=spoke_labels)
feature_df.index.name = ""

feature_df.to_csv(f"./features/{title.replace(' ', '_')}_features.csv")
feature_df.to_pickle(f"./features/{title.replace(' ', '_')}_features.pickle")
print("Done computing features for GHZ benchmark.")
# Mermin-Bell
print("Computing features for Mermin-Bell benchmark...")
title = 'mb'
labels = []
feature_vecs = []

for n in [3, 4, 5, 7, 11, 15, 20]: 
        labels.append(f'mb_{n}qubits')
        circ = mermin_bell.MerminBell(n).circuit()
        con = supermarq.features.compute_communication(circ)
        liv = supermarq.features.compute_liveness(circ)
        par = supermarq.features.compute_parallelism(circ)
        mea = supermarq.features.compute_measurement(circ)
        ent = supermarq.features.compute_entanglement(circ)
        dep = supermarq.features.compute_depth(circ)
        feature_vecs.append([con, liv, par, mea, ent, dep])

spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']

# Save features to dataframe
feature_df = pd.DataFrame(feature_vecs, index=labels, columns=spoke_labels)
feature_df.index.name = ""

feature_df.to_csv(f"./features/{title.replace(' ', '_')}_features.csv")
feature_df.to_pickle(f"./features/{title.replace(' ', '_')}_features.pickle")
print("Done computing features for Mermin-Bell benchmark.")

# Bit Code
print("Computing features for Bit Code benchmark...")
title = 'bitcode'
labels = []
feature_vecs = []

for nq in [3, 4, 5, 7, 9]:
    for nr in [2, 3, 4, 5, 7, 9]:
        labels.append(f'bitcode_{nq}data_{nr}rounds')
        bit_state = [i % 2 for i in range(nq)]
        circ = bit_code.BitCode(nq, nr, bit_state).circuit()
        con = supermarq.features.compute_communication(circ)
        liv = supermarq.features.compute_liveness(circ)
        par = supermarq.features.compute_parallelism(circ)
        mea = supermarq.features.compute_measurement(circ)
        ent = supermarq.features.compute_entanglement(circ)
        dep = supermarq.features.compute_depth(circ)
        feature_vecs.append([con, liv, par, mea, ent, dep])

spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']

# Save features to dataframe
feature_df = pd.DataFrame(feature_vecs, index=labels, columns=spoke_labels)
feature_df.index.name = ""

feature_df.to_csv(f"./features/{title.replace(' ', '_')}_features.csv")
feature_df.to_pickle(f"./features/{title.replace(' ', '_')}_features.pickle")
print("Done computing features for Bit Code benchmark.")
# Phase Code
print("Computing features for Phase Code benchmark...")
title = 'phasecode'
labels = []
feature_vecs = []

for nq in [3, 4, 5, 7, 9]:
    for nr in [2, 3, 4, 5, 7, 9]:
        labels.append(f'phasecode_{nq}data_{nr}rounds')
        phase_state = [i % 2 for i in range(nq)]
        circ = phase_code.PhaseCode(nq, nr, phase_state).circuit()
        con = supermarq.features.compute_communication(circ)
        liv = supermarq.features.compute_liveness(circ)
        par = supermarq.features.compute_parallelism(circ)
        mea = supermarq.features.compute_measurement(circ)
        ent = supermarq.features.compute_entanglement(circ)
        dep = supermarq.features.compute_depth(circ)
        feature_vecs.append([con, liv, par, mea, ent, dep])

spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']

# Save features to dataframe
feature_df = pd.DataFrame(feature_vecs, index=labels, columns=spoke_labels)
feature_df.index.name = ""

feature_df.to_csv(f"./features/{title.replace(' ', '_')}_features.csv")
feature_df.to_pickle(f"./features/{title.replace(' ', '_')}_features.pickle")
print("Done computing features for Phase Code benchmark.")
# Hamiltonian Sim.
print("Computing features for Hamiltonian Simulation benchmark...")
title = 'hamsim'
labels = []
feature_vecs = []

for nq in [4, 7, 11, 12, 13, 16, 20]:
    for steps in [1, 3, 4, 5, 7]:
        ts = steps #1
        tt = 1 * ts
        labels.append(f'hamsim_{nq}qubits_{ts}ts_{tt}tt')
        circ = hamiltonian_simulation.HamiltonianSimulation(nq, ts, tt).circuit()
        con = supermarq.features.compute_communication(circ)
        liv = supermarq.features.compute_liveness(circ)
        par = supermarq.features.compute_parallelism(circ)
        mea = supermarq.features.compute_measurement(circ)
        ent = supermarq.features.compute_entanglement(circ)
        dep = supermarq.features.compute_depth(circ)
        feature_vecs.append([con, liv, par, mea, ent, dep])

spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']

# Save features to dataframe
feature_df = pd.DataFrame(feature_vecs, index=labels, columns=spoke_labels)
feature_df.index.name = ""

feature_df.to_csv(f"./features/{title.replace(' ', '_')}_features.csv")
feature_df.to_pickle(f"./features/{title.replace(' ', '_')}_features.pickle")
print("Done computing features for Hamiltonian Simulation benchmark.")
# VQE
print("Computing features for VQE benchmark...")
title = 'vqe'
labels = []
feature_vecs = []

for nq in [4, 7, 9]:
    for nl in [1, 2, 3, 4, 5]:
        labels.append(f'vqe_{nq}qubits_{nl}layers')

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

feature_df = pd.DataFrame(feature_vecs, index=labels, columns=spoke_labels)
feature_df.index.name = ""

feature_df.to_csv(f"./features/{title.replace(' ', '_')}_features.csv")
feature_df.to_pickle(f"./features/{title.replace(' ', '_')}_features.pickle")
print("Done computing features for VQE benchmark.")

# QAOA Vanilla
print("Computing features for QAOA Vanilla benchmark...")
title = 'vanilla'
labels = []
feature_vecs = []

for n in [4, 5, 7, 11, 12, 13, 16]: 
        labels.append(f'vanilla_{n}qubits')
        circ = qaoa_vanilla_proxy.QAOAVanillaProxy(n).circuit()
        con = supermarq.features.compute_communication(circ)
        liv = supermarq.features.compute_liveness(circ)
        par = supermarq.features.compute_parallelism(circ)
        mea = supermarq.features.compute_measurement(circ)
        ent = supermarq.features.compute_entanglement(circ)
        dep = supermarq.features.compute_depth(circ)
        feature_vecs.append([con, liv, par, mea, ent, dep])

spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']

# Save features to dataframe
feature_df = pd.DataFrame(feature_vecs, index=labels, columns=spoke_labels)
feature_df.index.name = ""

feature_df.to_csv(f"./features/{title.replace(' ', '_')}_features.csv")
feature_df.to_pickle(f"./features/{title.replace(' ', '_')}_features.pickle")
print("Done computing features for QAOA Vanilla benchmark.")
# QAOA FSWAP
print("Computing features for QAOA FSWAP benchmark...")
title = 'fswap'
labels = []
feature_vecs = []

for n in [4, 5, 7, 11, 12, 13, 16]: 
        labels.append(f'fswap_{n}qubits')
        circ = qaoa_fermionic_swap_proxy.QAOAFermionicSwapProxy(n).circuit()
        con = supermarq.features.compute_communication(circ)
        liv = supermarq.features.compute_liveness(circ)
        par = supermarq.features.compute_parallelism(circ)
        mea = supermarq.features.compute_measurement(circ)
        ent = supermarq.features.compute_entanglement(circ)
        dep = supermarq.features.compute_depth(circ)
        feature_vecs.append([con, liv, par, mea, ent, dep])

spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']

# Save features to dataframe
feature_df = pd.DataFrame(feature_vecs, index=labels, columns=spoke_labels)
feature_df.index.name = ""

feature_df.to_csv(f"./features/{title.replace(' ', '_')}_features.csv")
feature_df.to_pickle(f"./features/{title.replace(' ', '_')}_features.pickle")
print("Done computing features for QAOA FSWAP benchmark.")
import featuresorig
from benchmarks import mermin_bell, bit_code, phase_code, vqe_proxy, qaoa_vanilla_proxy, qaoa_fermionic_swap_proxy, bit_code_old, phase_code_old
import supermarq
import matplotlib.pyplot as plt

import numpy as np
from matplotlib import font_manager as fm

fm.fontManager.addfont("/usr/share/fonts/msttcorefonts/times.ttf")
plt.rcParams["font.family"] = "Times New Roman"

# Bit Code feature example
title = 'Bit Code Original'
labels = []
feature_vecs = []
for nq in [3, 5]:
    for nr in [2, 3]:
    # for nr in [2, 3]:#, 4, 5, 6, 7, 8, 9, 10]:
        print(f'{nq} data, {nr} rounds')
        labels.append(f'{nq} data, {nr} rounds')
        bit_state = [i % 2 for i in range(nq)]
        circ = bit_code_old.BitCode(nq, nr, bit_state).circuit()
        con = featuresorig.compute_connectivity(circ)
        liv = featuresorig.compute_liveness(circ)
        par = featuresorig.compute_parallelism(circ)
        mea = featuresorig.compute_measurement(circ)
        ent = featuresorig.compute_entanglement(circ)
        dep = featuresorig.compute_depth(circ)
        feature_vecs.append([con, liv, par, mea, ent, dep])
        
spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
supermarq.plotting.plot_benchmark(
    '',
    labels,
    feature_vecs,
    spoke_labels=spoke_labels,
    legend_loc=(1.05, 0.25),
    savefn=f"paper_features/original_{title.replace(' ', '_')}.png",
    show=False,
)

# Phase Code feature example
title = 'Phase Code Original'
labels = []
feature_vecs = []
for nq in [3, 5]:
    for nr in [2, 3]:
        # for nr in [2, 3]:#, 4, 5, 6, 7, 8, 9, 10]:
        print(f'{nq} data, {nr} rounds')
        labels.append(f'{nq} data, {nr} rounds')
        bit_state = [i % 2 for i in range(nq)]
        circ = phase_code_old.PhaseCode(nq, nr, bit_state).circuit()
        con = featuresorig.compute_connectivity(circ)
        liv = featuresorig.compute_liveness(circ)
        par = featuresorig.compute_parallelism(circ)
        mea = featuresorig.compute_measurement(circ)
        ent = featuresorig.compute_entanglement(circ)
        dep = featuresorig.compute_depth(circ)
        feature_vecs.append([con, liv, par, mea, ent, dep])
    
spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
supermarq.plotting.plot_benchmark(
    '',
    labels,
    feature_vecs,
    spoke_labels=spoke_labels,
    legend_loc=(1.05, 0.25),
    savefn=f"paper_features/original_{title.replace(' ', '_')}.png",
    show=False,
)
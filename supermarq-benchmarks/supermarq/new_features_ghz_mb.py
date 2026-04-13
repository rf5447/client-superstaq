
import features
from benchmarks import mermin_bell, ghz
import supermarq
import matplotlib.pyplot as plt

import numpy as np
from matplotlib import font_manager as fm

fm.fontManager.addfont("/usr/share/fonts/msttcorefonts/times.ttf")
plt.rcParams["font.family"] = "Times New Roman"

# GHZ feature example
title = 'GHZ Original Ladder'
labels = ['3 qubits', '5 qubits', '7 qubits', '11 qubits']
feature_vecs = []
for nq in [3, 5, 7, 11]:
    circ = ghz.GHZ(nq, "ladder").circuit()
    con = supermarq.features.compute_communication(circ)
    liv = supermarq.features.compute_liveness(circ)
    par = supermarq.features.compute_parallelism(circ)
    mea = supermarq.features.compute_measurement(circ)
    ent = supermarq.features.compute_entanglement(circ)
    dep = supermarq.features.compute_depth(circ)
    feature_vecs.append([con, liv, par, mea, ent, dep])
    
spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
supermarq.plotting.plot_benchmark(
    '',
    labels,
    feature_vecs,
    spoke_labels=spoke_labels,
    legend_loc=(1.05, 0.25),
    savefn=f"paper_features/{title.replace(' ', '_')}.png",
    show=False,
)

# GHZ feature example
title = 'GHZ Original Log-Depth'
labels = ['3 qubits', '5 qubits', '7 qubits', '11 qubits']
feature_vecs = []
for nq in [3, 5, 7, 11]:
    circ = supermarq.ghz.GHZ(nq, "logdepth").circuit()
    con = supermarq.features.compute_communication(circ)
    liv = supermarq.features.compute_liveness(circ)
    par = supermarq.features.compute_parallelism(circ)
    mea = supermarq.features.compute_measurement(circ)
    ent = supermarq.features.compute_entanglement(circ)
    dep = supermarq.features.compute_depth(circ)
    feature_vecs.append([con, liv, par, mea, ent, dep])
    
spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
supermarq.plotting.plot_benchmark(
    '',
    labels,
    feature_vecs,
    spoke_labels=spoke_labels,
    legend_loc=(1.05, 0.25),
    savefn=f"paper_features/{title.replace(' ', '_')}.png",
    show=False,
)

# GHZ feature example
title = 'GHZ Original Star'
labels = ['3 qubits', '5 qubits', '7 qubits', '11 qubits']
feature_vecs = []
for nq in [3, 5, 7, 11]:
    circ = supermarq.ghz.GHZ(nq, "star").circuit()
    con = supermarq.features.compute_communication(circ)
    liv = supermarq.features.compute_liveness(circ)
    par = supermarq.features.compute_parallelism(circ)
    mea = supermarq.features.compute_measurement(circ)
    ent = supermarq.features.compute_entanglement(circ)
    dep = supermarq.features.compute_depth(circ)
    feature_vecs.append([con, liv, par, mea, ent, dep])
    
spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
supermarq.plotting.plot_benchmark(
    '',
    labels,
    feature_vecs,
    spoke_labels=spoke_labels,
    legend_loc=(1.05, 0.25),
    savefn=f"paper_features/{title.replace(' ', '_')}.png",
    show=False,
)

# GHZ feature example
title = 'GHZ Scaling Ladder'
labels = ['3 qubits', '5 qubits', '7 qubits', '11 qubits', '13 qubits', 
          '15 qubits', '20 qubits', '25 qubits', '30 qubits', '50 qubits', '100 qubits']
feature_vecs = []
for nq in [3, 5, 7, 11, 13, 15, 20, 25, 30, 50, 100]:
    circ = supermarq.ghz.GHZ(nq, "ladder").circuit()
    con = supermarq.features.compute_communication(circ)
    liv = supermarq.features.compute_liveness(circ)
    par = supermarq.features.compute_parallelism(circ)
    mea = supermarq.features.compute_measurement(circ)
    ent = supermarq.features.compute_entanglement(circ)
    dep = supermarq.features.compute_depth(circ)
    feature_vecs.append([con, liv, par, mea, ent, dep])
    
spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
supermarq.plotting.plot_benchmark(
    '',
    labels,
    feature_vecs,
    spoke_labels=spoke_labels,
    legend_loc=(1.05, 0.25),
    savefn=f"paper_features/{title.replace(' ', '_')}.png",
    show=False,
)


# GHZ feature example
title = 'GHZ Scaling Log-Depth'
labels = ['3 qubits', '5 qubits', '7 qubits', '11 qubits', '13 qubits', 
          '15 qubits', '20 qubits', '25 qubits', '30 qubits', '50 qubits', '100 qubits']
feature_vecs = []
for nq in [3, 5, 7, 11, 13, 15, 20, 25, 30, 50, 100]:
    circ = supermarq.ghz.GHZ(nq, "logdepth").circuit()
    con = supermarq.features.compute_communication(circ)
    liv = supermarq.features.compute_liveness(circ)
    par = supermarq.features.compute_parallelism(circ)
    mea = supermarq.features.compute_measurement(circ)
    ent = supermarq.features.compute_entanglement(circ)
    dep = supermarq.features.compute_depth(circ)
    feature_vecs.append([con, liv, par, mea, ent, dep])
    
spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
supermarq.plotting.plot_benchmark(
    '',
    labels,
    feature_vecs,
    spoke_labels=spoke_labels,
    legend_loc=(1.05, 0.25),
    savefn=f"paper_features/{title.replace(' ', '_')}.png",
    show=False,
)


# GHZ feature example
title = 'GHZ Scaling Star'
labels = ['3 qubits', '5 qubits', '7 qubits', '11 qubits', '13 qubits', 
          '15 qubits', '20 qubits', '25 qubits', '30 qubits', '50 qubits', '100 qubits']
feature_vecs = []
for nq in [3, 5, 7, 11, 13, 15, 20, 25, 30, 50, 100]:
    circ = supermarq.ghz.GHZ(nq, "star").circuit()
    con = supermarq.features.compute_communication(circ)
    liv = supermarq.features.compute_liveness(circ)
    par = supermarq.features.compute_parallelism(circ)
    mea = supermarq.features.compute_measurement(circ)
    ent = supermarq.features.compute_entanglement(circ)
    dep = supermarq.features.compute_depth(circ)
    feature_vecs.append([con, liv, par, mea, ent, dep])
    
spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
supermarq.plotting.plot_benchmark(
    '',
    labels,
    feature_vecs,
    spoke_labels=spoke_labels,
    legend_loc=(1.05, 0.25),
    savefn=f"paper_features/{title.replace(' ', '_')}.png",
    show=False,
)
#########################################################################################

# Mermin-Bell feature example
title = 'Mermin-Bell Original'
labels = ['3 qubits', '4 qubits']
feature_vecs = []
for nq in [3, 4]:
    circ = supermarq.mermin_bell.MerminBell(nq).circuit()
    con = supermarq.features.compute_communication(circ)
    liv = supermarq.features.compute_liveness(circ)
    par = supermarq.features.compute_parallelism(circ)
    mea = supermarq.features.compute_measurement(circ)
    ent = supermarq.features.compute_entanglement(circ)
    dep = supermarq.features.compute_depth(circ)
    feature_vecs.append([con, liv, par, mea, ent, dep])
    
spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
supermarq.plotting.plot_benchmark(
    '',
    labels,
    feature_vecs,
    spoke_labels=spoke_labels,
    legend_loc=(1.05, 0.25),
    savefn=f"paper_features/{title.replace(' ', '_')}.png",
    show=False,
)

# Mermin-Bell feature example
title = 'Mermin-Bell Scaling'
labels = ['3 qubits', '4 qubits', '5 qubits', '6 qubits', '7 qubits']

feature_vecs = []
for nq in [3, 4, 5, 6, 7]:
    circ = mermin_bell.MerminBell(nq).circuit()
    con = supermarq.features.compute_communication(circ)
    liv = supermarq.features.compute_liveness(circ)
    par = supermarq.features.compute_parallelism(circ)
    mea = supermarq.features.compute_measurement(circ)
    ent = supermarq.features.compute_entanglement(circ)
    dep = supermarq.features.compute_depth(circ)
    feature_vecs.append([con, liv, par, mea, ent, dep])

spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']

supermarq.plotting.plot_benchmark(
    '',
    labels,
    feature_vecs,
    spoke_labels=spoke_labels,
    legend_loc=(1.05, 0.25),
    savefn=f"paper_features/{title.replace(' ', '_')}.png",
    show=False,                         # optional: avoid popping up X11 windows on HPC
)
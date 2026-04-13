import features
from benchmarks import mermin_bell, bit_code, phase_code
import supermarq
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

fm.fontManager.addfont("/usr/share/fonts/msttcorefonts/times.ttf")
plt.rcParams["font.family"] = "Times New Roman"

# Bit Code feature example
title = 'Bit Code Scaling, Varying Number of Qubits, Fixing Number of Rounds = 2'
labels = []
feature_vecs = []
for nq in [3, 5, 10, 25, 30, 50, 100]:
    nr = 2
    # for nr in [2, 3]:#, 4, 5, 6, 7, 8, 9, 10]:
    print(f'{nq} data, {nr} rounds')
    labels.append(f'{nq} data, {nr} rounds')
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
supermarq.plotting.plot_benchmark(
    '',
    labels,
    feature_vecs,
    spoke_labels=spoke_labels,
    legend_loc=(1.05, 0.25),
    savefn=f"paper_features/new_{title.replace(' ', '_')}_nr2.png",
    show=False,
)

# Bit Code feature example
title = 'Bit Code Scaling, Varying Number of Qubits, Fixing Number of Rounds = 3'
labels = []
feature_vecs = []
for nq in [3, 5, 10, 25, 30, 50, 100]:
    nr = 3
    # for nr in [2, 3]:#, 4, 5, 6, 7, 8, 9, 10]:
    print(f'{nq} data, {nr} rounds')
    labels.append(f'{nq} data, {nr} rounds')
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
supermarq.plotting.plot_benchmark(
    '',
    labels,
    feature_vecs,
    spoke_labels=spoke_labels,
    legend_loc=(1.05, 0.25),
    savefn=f"paper_features/new_{title.replace(' ', '_')}_nr3.png",
    show=False,
)

# Bit Code feature example
title = 'Bit Code Scaling, Varying Number of Rounds, Fixing Number of Qubits = 3'
labels = []
feature_vecs = []
for nr in [2, 3, 5, 10, 25, 30, 50, 100]:
    nq = 3
    # for nr in [2, 3]:#, 4, 5, 6, 7, 8, 9, 10]:
    print(f'{nq} data, {nr} rounds')
    labels.append(f'{nq} data, {nr} rounds')
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
supermarq.plotting.plot_benchmark(
    '',
    labels,
    feature_vecs,
    spoke_labels=spoke_labels,
    legend_loc=(1.05, 0.25),
    savefn=f"paper_features/new_{title.replace(' ', '_')}_nq3_nrSweep.png",
    show=False,
)

# Bit Code feature example
title = 'Bit Code Scaling, Varying Number of Rounds, Fixing Number of Qubits = 5'
labels = []
feature_vecs = []
for nr in [2, 3, 5, 10, 25, 30, 50, 100]:
    nq = 5
    # for nr in [2, 3]:#, 4, 5, 6, 7, 8, 9, 10]:
    print(f'{nq} data, {nr} rounds')
    labels.append(f'{nq} data, {nr} rounds')
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
supermarq.plotting.plot_benchmark(
    '',
    labels,
    feature_vecs,
    spoke_labels=spoke_labels,
    legend_loc=(1.05, 0.25),
    savefn=f"paper_features/new_{title.replace(' ', '_')}_nq5_nrSweep.png",
    show=False,
)

# Phase Code feature example
title = 'Phase Code Scaling, Varying Number of Qubits, Fixing Number of Rounds = 2'
labels = []
feature_vecs = []
for nq in [3, 5, 10, 25, 30, 50, 100]:
    nr = 2
    # for nr in [2, 3]:#, 4, 5, 6, 7, 8, 9, 10]:
    print(f'{nq} data, {nr} rounds')
    labels.append(f'{nq} data, {nr} rounds')
    bit_state = [i % 2 for i in range(nq)]
    circ = phase_code.PhaseCode(nq, nr, bit_state).circuit()
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
    savefn=f"paper_features/new_{title.replace(' ', '_')}_nr2.png",
    show=False,
)

# Phase Code feature example
title = 'Phase Code Scaling, Varying Number of Qubits, Fixing Number of Rounds = 3'
labels = []
feature_vecs = []
for nq in [3, 5, 10, 25, 30, 50, 100]:
    nr = 3
    # for nr in [2, 3]:#, 4, 5, 6, 7, 8, 9, 10]:
    print(f'{nq} data, {nr} rounds')
    labels.append(f'{nq} data, {nr} rounds')
    bit_state = [i % 2 for i in range(nq)]
    circ = phase_code.PhaseCode(nq, nr, bit_state).circuit()
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
    savefn=f"paper_features/new_{title.replace(' ', '_')}_nr3.png",
    show=False,
)

# Phase Code feature example
title = 'Phase Code Scaling, Varying Number of Rounds, Fixing Number of Qubits = 3'
labels = []
feature_vecs = []
for nr in [2, 3, 5, 10, 25, 30, 50, 100]:
    nq = 3
    # for nr in [2, 3]:#, 4, 5, 6, 7, 8, 9, 10]:
    print(f'{nq} data, {nr} rounds')
    labels.append(f'{nq} data, {nr} rounds')
    bit_state = [i % 2 for i in range(nq)]
    circ = phase_code.PhaseCode(nq, nr, bit_state).circuit()
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
    savefn=f"paper_features/new_{title.replace(' ', '_')}_nq3_nrSweep.png",
    show=False,
)

# Phase Code feature example
title = 'Phase Code Scaling, Varying Number of Rounds, Fixing Number of Qubits = 5'
labels = []
feature_vecs = []
for nr in [2, 3, 5, 10, 25, 30, 50, 100]:
    nq = 5
    # for nr in [2, 3]:#, 4, 5, 6, 7, 8, 9, 10]:
    print(f'{nq} data, {nr} rounds')
    labels.append(f'{nq} data, {nr} rounds')
    bit_state = [i % 2 for i in range(nq)]
    circ = phase_code.PhaseCode(nq, nr, bit_state).circuit()
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
    savefn=f"paper_features/new_{title.replace(' ', '_')}_nq5_nrSweep.png",
    show=False,
)
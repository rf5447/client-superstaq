import features
from benchmarks import mermin_bell, bit_code, phase_code
import supermarq
import matplotlib.pyplot as plt



plt.rcParams["font.family"] = "Times New Roman"

# Bit Code feature example
title = 'Bit Code Updated'
labels = []
feature_vecs = []
for nq in [3, 5]:
    for nr in [2, 3]:
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
    title,
    labels,
    feature_vecs,
    spoke_labels=spoke_labels,
    legend_loc=(1.05, 0.25),
    savefn=f"{title.replace(' ', '_')}_nq5_nrSweep.png",
    show=False,
)

# Phase Code feature example
title = 'Phase Code Updated'
labels = []
feature_vecs = []
for nq in [3, 5]:
    for nr in [2, 3]:
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
    title,
    labels,
    feature_vecs,
    spoke_labels=spoke_labels,
    legend_loc=(1.05, 0.25),
    savefn=f"{title.replace(' ', '_')}_nr2.png",
    show=False,
)


# # GHZ feature example
# title = 'GHZ Original'
# labels = ['3 qubits', '5 qubits', '7 qubits', '11 qubits']
# feature_vecs = []
# for nq in [3, 5, 7, 11]:
#     circ = supermarq.ghz.GHZ(nq).circuit()
#     con = supermarq.features.compute_communication(circ)
#     liv = supermarq.features.compute_liveness(circ)
#     par = supermarq.features.compute_parallelism(circ)
#     mea = supermarq.features.compute_measurement(circ)
#     ent = supermarq.features.compute_entanglement(circ)
#     dep = supermarq.features.compute_depth(circ)
#     feature_vecs.append([con, liv, par, mea, ent, dep])
    
# spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
# supermarq.plotting.plot_benchmark(
#     title,
#     labels,
#     feature_vecs,
#     spoke_labels=spoke_labels,
#     legend_loc=(1.05, 0.25),
#     savefn=f"{title.replace(' ', '_')}.png",
#     show=False,
# )


# # GHZ feature example
# title = 'GHZ Scaling'
# labels = ['3 qubits', '5 qubits', '7 qubits', '11 qubits', '13 qubits', 
#           '15 qubits', '20 qubits', '25 qubits', '30 qubits', '50 qubits', '100 qubits']
# feature_vecs = []
# for nq in [3, 5, 7, 11, 13, 15, 20, 25, 30, 50, 100]:
#     circ = supermarq.ghz.GHZ(nq).circuit()
#     con = supermarq.features.compute_communication(circ)
#     liv = supermarq.features.compute_liveness(circ)
#     par = supermarq.features.compute_parallelism(circ)
#     mea = supermarq.features.compute_measurement(circ)
#     ent = supermarq.features.compute_entanglement(circ)
#     dep = supermarq.features.compute_depth(circ)
#     feature_vecs.append([con, liv, par, mea, ent, dep])
    
# spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
# supermarq.plotting.plot_benchmark(
#     title,
#     labels,
#     feature_vecs,
#     spoke_labels=spoke_labels,
#     legend_loc=(1.05, 0.25),
#     savefn=f"{title.replace(' ', '_')}.png",
#     show=False,
# )
# #########################################################################################

# # Mermin-Bell feature example
# title = 'Mermin-Bell Original'
# labels = ['3 qubits', '4 qubits']
# feature_vecs = []
# for nq in [3, 4]:
#     circ = supermarq.mermin_bell.MerminBell(nq).circuit()
#     con = supermarq.features.compute_communication(circ)
#     liv = supermarq.features.compute_liveness(circ)
#     par = supermarq.features.compute_parallelism(circ)
#     mea = supermarq.features.compute_measurement(circ)
#     ent = supermarq.features.compute_entanglement(circ)
#     dep = supermarq.features.compute_depth(circ)
#     feature_vecs.append([con, liv, par, mea, ent, dep])
    
# spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
# supermarq.plotting.plot_benchmark(
#     title,
#     labels,
#     feature_vecs,
#     spoke_labels=spoke_labels,
#     legend_loc=(1.05, 0.25),
#     savefn=f"{title.replace(' ', '_')}.png",
#     show=False,
# )

# # Mermin-Bell feature example
# title = 'Mermin-Bell Scaling'
# labels = ['3 qubits', '4 qubits', '5 qubits', '6 qubits', '7 qubits']

# feature_vecs = []
# for nq in [3, 4, 5, 6, 7]:
#     circ = mermin_bell.MerminBell(nq).circuit()
#     con = supermarq.features.compute_communication(circ)
#     liv = supermarq.features.compute_liveness(circ)
#     par = supermarq.features.compute_parallelism(circ)
#     mea = supermarq.features.compute_measurement(circ)
#     ent = supermarq.features.compute_entanglement(circ)
#     dep = supermarq.features.compute_depth(circ)
#     feature_vecs.append([con, liv, par, mea, ent, dep])

# spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']

# supermarq.plotting.plot_benchmark(
#     title,
#     labels,
#     feature_vecs,
#     spoke_labels=spoke_labels,
#     legend_loc=(1.05, 0.25),
#     savefn="mermin_bell_scaling.png",   # <-- saves the figure
#     show=False,                         # optional: avoid popping up X11 windows on HPC
# )

# #########################################################################################

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
    circ = supermarq.bit_code.BitCode(nq, nr, bit_state).circuit()
    con = supermarq.features.compute_communication(circ)
    liv = supermarq.features.compute_liveness(circ)
    par = supermarq.features.compute_parallelism(circ)
    mea = supermarq.features.compute_measurement(circ)
    ent = supermarq.features.compute_entanglement(circ)
    dep = supermarq.features.compute_depth(circ)
    feature_vecs.append([con, liv, par, mea, ent, dep])
    
spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
supermarq.plotting.plot_benchmark(
    title,
    labels,
    feature_vecs,
    spoke_labels=spoke_labels,
    legend_loc=(1.05, 0.25),
    savefn=f"{title.replace(' ', '_')}_nr2.png",
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
    circ = supermarq.bit_code.BitCode(nq, nr, bit_state).circuit()
    con = supermarq.features.compute_communication(circ)
    liv = supermarq.features.compute_liveness(circ)
    par = supermarq.features.compute_parallelism(circ)
    mea = supermarq.features.compute_measurement(circ)
    ent = supermarq.features.compute_entanglement(circ)
    dep = supermarq.features.compute_depth(circ)
    feature_vecs.append([con, liv, par, mea, ent, dep])
    
spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
supermarq.plotting.plot_benchmark(
    title,
    labels,
    feature_vecs,
    spoke_labels=spoke_labels,
    legend_loc=(1.05, 0.25),
    savefn=f"{title.replace(' ', '_')}_nr3.png",
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
    circ = supermarq.bit_code.BitCode(nq, nr, bit_state).circuit()
    con = supermarq.features.compute_communication(circ)
    liv = supermarq.features.compute_liveness(circ)
    par = supermarq.features.compute_parallelism(circ)
    mea = supermarq.features.compute_measurement(circ)
    ent = supermarq.features.compute_entanglement(circ)
    dep = supermarq.features.compute_depth(circ)
    feature_vecs.append([con, liv, par, mea, ent, dep])
    
spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
supermarq.plotting.plot_benchmark(
    title,
    labels,
    feature_vecs,
    spoke_labels=spoke_labels,
    legend_loc=(1.05, 0.25),
    savefn=f"{title.replace(' ', '_')}_nq3_nrSweep.png",
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
    circ = supermarq.bit_code.BitCode(nq, nr, bit_state).circuit()
    con = supermarq.features.compute_communication(circ)
    liv = supermarq.features.compute_liveness(circ)
    par = supermarq.features.compute_parallelism(circ)
    mea = supermarq.features.compute_measurement(circ)
    ent = supermarq.features.compute_entanglement(circ)
    dep = supermarq.features.compute_depth(circ)
    feature_vecs.append([con, liv, par, mea, ent, dep])
    
spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
supermarq.plotting.plot_benchmark(
    title,
    labels,
    feature_vecs,
    spoke_labels=spoke_labels,
    legend_loc=(1.05, 0.25),
    savefn=f"{title.replace(' ', '_')}_nq5_nrSweep.png",
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
    circ = supermarq.phase_code.PhaseCode(nq, nr, bit_state).circuit()
    con = supermarq.features.compute_communication(circ)
    liv = supermarq.features.compute_liveness(circ)
    par = supermarq.features.compute_parallelism(circ)
    mea = supermarq.features.compute_measurement(circ)
    ent = supermarq.features.compute_entanglement(circ)
    dep = supermarq.features.compute_depth(circ)
    feature_vecs.append([con, liv, par, mea, ent, dep])
    
spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
supermarq.plotting.plot_benchmark(
    title,
    labels,
    feature_vecs,
    spoke_labels=spoke_labels,
    legend_loc=(1.05, 0.25),
    savefn=f"{title.replace(' ', '_')}_nr2.png",
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
    circ = supermarq.phase_code.PhaseCode(nq, nr, bit_state).circuit()
    con = supermarq.features.compute_communication(circ)
    liv = supermarq.features.compute_liveness(circ)
    par = supermarq.features.compute_parallelism(circ)
    mea = supermarq.features.compute_measurement(circ)
    ent = supermarq.features.compute_entanglement(circ)
    dep = supermarq.features.compute_depth(circ)
    feature_vecs.append([con, liv, par, mea, ent, dep])
    
spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
supermarq.plotting.plot_benchmark(
    title,
    labels,
    feature_vecs,
    spoke_labels=spoke_labels,
    legend_loc=(1.05, 0.25),
    savefn=f"{title.replace(' ', '_')}_nr3.png",
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
    circ = supermarq.phase_code.PhaseCode(nq, nr, bit_state).circuit()
    con = supermarq.features.compute_communication(circ)
    liv = supermarq.features.compute_liveness(circ)
    par = supermarq.features.compute_parallelism(circ)
    mea = supermarq.features.compute_measurement(circ)
    ent = supermarq.features.compute_entanglement(circ)
    dep = supermarq.features.compute_depth(circ)
    feature_vecs.append([con, liv, par, mea, ent, dep])
    
spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
supermarq.plotting.plot_benchmark(
    title,
    labels,
    feature_vecs,
    spoke_labels=spoke_labels,
    legend_loc=(1.05, 0.25),
    savefn=f"{title.replace(' ', '_')}_nq3_nrSweep.png",
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
    circ = supermarq.phase_code.PhaseCode(nq, nr, bit_state).circuit()
    con = supermarq.features.compute_communication(circ)
    liv = supermarq.features.compute_liveness(circ)
    par = supermarq.features.compute_parallelism(circ)
    mea = supermarq.features.compute_measurement(circ)
    ent = supermarq.features.compute_entanglement(circ)
    dep = supermarq.features.compute_depth(circ)
    feature_vecs.append([con, liv, par, mea, ent, dep])
    
spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
supermarq.plotting.plot_benchmark(
    title,
    labels,
    feature_vecs,
    spoke_labels=spoke_labels,
    legend_loc=(1.05, 0.25),
    savefn=f"{title.replace(' ', '_')}_nq5_nrSweep.png",
    show=False,
)

# # # Vanilla QAOA feature example
# # title = 'QAOA Vanilla Proxy'
# # labels = ['3 qubits', '5 qubits', '7 qubits', '11 qubits', '13 qubits', 
# #           '15 qubits', '20 qubits', '25 qubits', '30 qubits', '50 qubits', '100 qubits']
# # feature_vecs = []
# # for nq in [3, 5, 7, 11, 13, 15, 20, 25, 30, 50, 100]:
# #     circ = supermarq.qaoa_vanilla_proxy.QAOAVanillaProxy(nq).circuit()
# #     con = supermarq.features.compute_communication(circ)
# #     liv = supermarq.features.compute_liveness(circ)
# #     par = supermarq.features.compute_parallelism(circ)
# #     mea = supermarq.features.compute_measurement(circ)
# #     ent = supermarq.features.compute_entanglement(circ)
# #     dep = supermarq.features.compute_depth(circ)
# #     feature_vecs.append([con, liv, par, mea, ent, dep])
    
# # spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
# # supermarq.plotting.plot_benchmark(
# #     title,
# #     labels,
# #     feature_vecs,
# #     spoke_labels=spoke_labels,
# #     legend_loc=(1.05, 0.05),
# #     savefn=f"{title.replace(' ', '_')}.png",
# #     show=False,
# # )

# # # ZZ-Swap QAOA feature example
# # title = 'QAOA ZZ-Swap Proxy'
# # labels = ['3 qubits', '5 qubits', '7 qubits', '11 qubits', '13 qubits', 
# #           '15 qubits']
# # feature_vecs = []
# # for nq in [3, 5, 7, 11, 13, 15]:
# #     print(nq)
# #     circ = supermarq.qaoa_fermionic_swap_proxy.QAOAFermionicSwapProxy(nq).circuit()
# #     con = supermarq.features.compute_communication(circ)
# #     liv = supermarq.features.compute_liveness(circ)
# #     par = supermarq.features.compute_parallelism(circ)
# #     mea = supermarq.features.compute_measurement(circ)
# #     ent = supermarq.features.compute_entanglement(circ)
# #     dep = supermarq.features.compute_depth(circ)
# #     feature_vecs.append([con, liv, par, mea, ent, dep])
    
# # spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
# # supermarq.plotting.plot_benchmark(
# #     title,
# #     labels,
# #     feature_vecs,
# #     spoke_labels=spoke_labels,
# #     legend_loc=(1.05, 0.05),
# #     savefn=f"{title.replace(' ', '_')}.png",
# #     show=False,
# # )

# # # Hamiltonian feature example
# # title = 'Hamiltonian Simulation Scaling'

# # nq_list = [4, 7, 11, 25, 50, 100]
# # steps_list = [1, 3]        # target: 1 and 3 time steps
# # total_time = 2.0           # evolution time T

# # labels = []
# # feature_vecs = []

# # for nq in nq_list:
# #     for steps in steps_list:
# #         dt = total_time / steps                  # ensure an integer number of layers
# #         labels.append(f'{nq} qubits, {steps} steps, T={total_time:g}')

# #         # API: HamiltonianSimulation(num_qubits, dt, total_time)
# #         circ = supermarq.hamiltonian_simulation.HamiltonianSimulation(nq, dt, total_time).circuit()

# #         con = supermarq.features.compute_communication(circ)
# #         liv = supermarq.features.compute_liveness(circ)
# #         par = supermarq.features.compute_parallelism(circ)
# #         mea = supermarq.features.compute_measurement(circ)
# #         ent = supermarq.features.compute_entanglement(circ)
# #         dep = supermarq.features.compute_depth(circ)
# #         feature_vecs.append([con, liv, par, mea, ent, dep])

# # spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
# # supermarq.plotting.plot_benchmark(
# #     title,
# #     labels,
# #     feature_vecs,
# #     spoke_labels=spoke_labels,
# #     legend_loc=(1.05, 0.05),
# #     savefn=f"{title.replace(' ', '_')}_T2.png",
# #     show=False,
# # )



# # # Hamiltonian feature example
# # title = 'Hamiltonian Simulation Scaling'

# # nq_list = [4, 7, 11]
# # steps_list = [1, 3, 5, 7, 10]        # target: 1 and 3 time steps
# # total_time = 2.0           # evolution time T

# # labels = []
# # feature_vecs = []

# # for nq in nq_list:
# #     for steps in steps_list:
# #         dt = total_time / steps                  # ensure an integer number of layers
# #         labels.append(f'{nq} qubits, {steps} steps, T={total_time:g}')

# #         # API: HamiltonianSimulation(num_qubits, dt, total_time)
# #         circ = supermarq.hamiltonian_simulation.HamiltonianSimulation(nq, dt, total_time).circuit()

# #         con = supermarq.features.compute_communication(circ)
# #         liv = supermarq.features.compute_liveness(circ)
# #         par = supermarq.features.compute_parallelism(circ)
# #         mea = supermarq.features.compute_measurement(circ)
# #         ent = supermarq.features.compute_entanglement(circ)
# #         dep = supermarq.features.compute_depth(circ)
# #         feature_vecs.append([con, liv, par, mea, ent, dep])

# #     spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
# #     supermarq.plotting.plot_benchmark(
# #         title,
# #         labels,
# #         feature_vecs,
# #         spoke_labels=spoke_labels,
# #         legend_loc=(1.05, 0.05),
# #         savefn=f"{title.replace(' ', '_')}_nq{nq}.png",
# #         show=False,
# #     )
# #     labels = []
# #     feature_vecs = []

# # # VQE feature example
# # title = 'VQE Scaling'
# # labels = []
# # feature_vecs = []
# # for nq in [4, 7]:
# #     for nl in [1, 2]:
# #         # for nr in [2, 3]:#, 4, 5, 6, 7, 8, 9, 10]:
# #         print(f'{nq} qubits, {nl} layers')
# #         labels.append(f'{nq} qubits, {nl} layers')
# #         circ = supermarq.vqe_proxy.VQEProxy(nq, nl).circuit()
# #         con = supermarq.features.compute_communication(circ)
# #         liv = supermarq.features.compute_liveness(circ)
# #         par = supermarq.features.compute_parallelism(circ)
# #         mea = supermarq.features.compute_measurement(circ)
# #         ent = supermarq.features.compute_entanglement(circ)
# #         dep = supermarq.features.compute_depth(circ)
# #         feature_vecs.append([con, liv, par, mea, ent, dep])

# # spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
# # supermarq.plotting.plot_benchmark(
# #     title,
# #     labels,
# #     feature_vecs,
# #     spoke_labels=spoke_labels,
# #     legend_loc=(1.05, 0.25),
# #     savefn=f"{title.replace(' ', '_')}.png",
# #     show=False,
# # )

# # # VQE feature example
# # title = 'VQE Scaling'
# # labels = []
# # feature_vecs = []

# # for nq in [4, 7, 10]:
# #     for nl in [1]:
# #         print(f'{nq} qubits, {nl} layers')
# #         labels.append(f'{nq} qubits, {nl} layers')

# #         res = supermarq.vqe_proxy.VQEProxy(nq, nl).circuit()
# #         # Coerce to a QuantumCircuit if a container is returned
# #         if isinstance(res, (list, tuple)):
# #             circ = res[0]
# #         elif isinstance(res, dict) and "circuit" in res:
# #             circ = res["circuit"]
# #         else:
# #             circ = res

# #         con = supermarq.features.compute_communication(circ)
# #         liv = supermarq.features.compute_liveness(circ)
# #         par = supermarq.features.compute_parallelism(circ)
# #         mea = supermarq.features.compute_measurement(circ)
# #         ent = supermarq.features.compute_entanglement(circ)
# #         dep = supermarq.features.compute_depth(circ)

# #         feature_vecs.append([con, liv, par, mea, ent, dep])

# # spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
# # supermarq.plotting.plot_benchmark(
# #     title,
# #     labels,
# #     feature_vecs,
# #     spoke_labels=spoke_labels,
# #     legend_loc=(1.05, 0.25),
# #     savefn=f"{title.replace(' ', '_')}.png",
# #     show=False,
# # )

# # # VQE feature example
# # title = 'VQE Scaling'
# # labels = []
# # feature_vecs = []

# # for nq in [4, 7, 10]:
# #     for nl in [2]:
# #         print(f'{nq} qubits, {nl} layers')
# #         labels.append(f'{nq} qubits, {nl} layers')

# #         res = supermarq.vqe_proxy.VQEProxy(nq, nl).circuit()
# #         # Coerce to a QuantumCircuit if a container is returned
# #         if isinstance(res, (list, tuple)):
# #             circ = res[0]
# #         elif isinstance(res, dict) and "circuit" in res:
# #             circ = res["circuit"]
# #         else:
# #             circ = res

# #         con = supermarq.features.compute_communication(circ)
# #         liv = supermarq.features.compute_liveness(circ)
# #         par = supermarq.features.compute_parallelism(circ)
# #         mea = supermarq.features.compute_measurement(circ)
# #         ent = supermarq.features.compute_entanglement(circ)
# #         dep = supermarq.features.compute_depth(circ)

# #         feature_vecs.append([con, liv, par, mea, ent, dep])

# # spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
# # supermarq.plotting.plot_benchmark(
# #     title,
# #     labels,
# #     feature_vecs,
# #     spoke_labels=spoke_labels,
# #     legend_loc=(1.05, 0.25),
# #     savefn=f"{title.replace(' ', '_')}.png",
# #     show=False,
# # )


# # # VQE feature example
# # title = 'VQE Scaling'
# # labels = []
# # feature_vecs = []

# # for nq in [4, 7, 10]:
# #     for nl in [3]:
# #         print(f'{nq} qubits, {nl} layers')
# #         labels.append(f'{nq} qubits, {nl} layers')

# #         res = supermarq.vqe_proxy.VQEProxy(nq, nl).circuit()
# #         # Coerce to a QuantumCircuit if a container is returned
# #         if isinstance(res, (list, tuple)):
# #             circ = res[0]
# #         elif isinstance(res, dict) and "circuit" in res:
# #             circ = res["circuit"]
# #         else:
# #             circ = res

# #         con = supermarq.features.compute_communication(circ)
# #         liv = supermarq.features.compute_liveness(circ)
# #         par = supermarq.features.compute_parallelism(circ)
# #         mea = supermarq.features.compute_measurement(circ)
# #         ent = supermarq.features.compute_entanglement(circ)
# #         dep = supermarq.features.compute_depth(circ)

# #         feature_vecs.append([con, liv, par, mea, ent, dep])

# # spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
# # supermarq.plotting.plot_benchmark(
# #     title,
# #     labels,
# #     feature_vecs,
# #     spoke_labels=spoke_labels,
# #     legend_loc=(1.05, 0.25),
# #     savefn=f"{title.replace(' ', '_')}.png",
# #     show=False,
# # )

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

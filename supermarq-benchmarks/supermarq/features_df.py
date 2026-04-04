# import features
# from benchmarks import mermin_bell, bit_code, phase_code
# import supermarq
# import matplotlib.pyplot as plt



# plt.rcParams["font.family"] = "Times New Roman"

# # Bit Code feature example
# title = 'Bit Code Updated'
# labels = []
# feature_vecs = []
# for nq in [3, 5]:
#     for nr in [2, 3]:
#     # for nr in [2, 3]:#, 4, 5, 6, 7, 8, 9, 10]:
#         print(f'{nq} data, {nr} rounds')
#         labels.append(f'{nq} data, {nr} rounds')
#         bit_state = [i % 2 for i in range(nq)]
#         circ = bit_code.BitCode(nq, nr, bit_state).circuit()
#         con = supermarq.features.compute_communication(circ)
#         liv = supermarq.features.compute_liveness(circ)
#         par = supermarq.features.compute_parallelism(circ)
#         mea = supermarq.features.compute_measurement(circ)
#         ent = supermarq.features.compute_entanglement(circ)
#         dep = supermarq.features.compute_depth(circ)
#         feature_vecs.append([con, liv, par, mea, ent, dep])
        
# spoke_labels = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
# supermarq.plotting.plot_benchmark(
#     title,
#     labels,
#     feature_vecs,
#     spoke_labels=spoke_labels,
#     legend_loc=(1.05, 0.25),
#     savefn=f"{title.replace(' ', '_')}_nq5_nrSweep.png",
#     show=False,
# )

import pandas as pd
import features
from benchmarks import mermin_bell, bit_code, phase_code
import supermarq
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Times New Roman"

title = 'Bit Code Updated'
labels = []
feature_vecs = []

for nq in [3, 4, 5, 7, 9]:
    for nr in [2, 3, 4, 5, 7, 9]:
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

# Save features to dataframe
feature_df = pd.DataFrame(feature_vecs, index=labels, columns=spoke_labels)
feature_df.index.name = "benchmark_instance"

feature_df.to_csv(f"{title.replace(' ', '_')}_features.csv")
feature_df.to_pickle(f"{title.replace(' ', '_')}_features.pickle")

# Make/save plot
# supermarq.plotting.plot_benchmark(
#     title,
#     labels,
#     feature_vecs,
#     spoke_labels=spoke_labels,
#     legend_loc=(1.05, 0.25),
#     savefn=f"{title.replace(' ', '_')}_nq5_nrSweep_df.png",
#     show=False,
# )
# import pandas as pd
# from plotting_functions import heatmap, annotate_heatmap, regression_plot

# # Load the dataframes from the data/ directory
# feature_df = pd.read_pickle('data/feature_dataframe.pickle')
# score_df = pd.read_pickle('data/benchmark_scores_dataframe.pickle')

# # Create the correlation dataframes including the error-correction benchmarks
# correlation_wEC_df = pd.DataFrame(data=None, index=score_df.index, columns=feature_df.columns)
# correlation_wEC_df.head()

# for feature in correlation_wEC_df.columns:
    
#     application_features = feature_df.loc[:, feature]
    
#     for device in correlation_wEC_df.index:
#         scores = score_df.loc[device, :]

#         x, y = [], []
#         for benchmark in scores.index:
#             #if 'code' in benchmark:
#             #    continue
#             if isinstance(scores.loc[benchmark], tuple):
#                 x.append(application_features.loc[benchmark])
#                 y.append(scores.loc[benchmark][0])

#         X = np.array(x)[:, np.newaxis]
#         Y = np.array(y)
#         model = LinearRegression().fit(X, Y)
#         correlation = model.score(X, Y)        
#         correlation_wEC_df.loc[device, feature] = correlation
# correlation_wEC_df.head()

# # Create the correlation dataframes excluding the error-correction benchmarks
# correlation_woEC_df = pd.DataFrame(data=None, index=score_df.index, columns=feature_df.columns)
# correlation_woEC_df.head()

# for feature in correlation_woEC_df.columns:
    
#     application_features = feature_df.loc[:, feature]
    
#     for device in correlation_woEC_df.index:
#         scores = score_df.loc[device, :]

#         x, y = [], []
#         for benchmark in scores.index:
#             if 'code' in benchmark:
#                 continue
#             if isinstance(scores.loc[benchmark], tuple):
#                 x.append(application_features.loc[benchmark])
#                 y.append(scores.loc[benchmark][0])

#         X = np.array(x)[:, np.newaxis]
#         Y = np.array(y)
#         model = LinearRegression().fit(X, Y)
#         correlation = model.score(X, Y)        
#         correlation_woEC_df.loc[device, feature] = correlation
# correlation_woEC_df.head()

# # Plot correlations INCLUDING error-correction Benchmarks
# fig, ax = plt.subplots(dpi=300)

# rows = ['AQT-4Q', 'IBM-\nCasablanca-7Q', 'IBM-\nGuadalupe-16Q', 'IonQ-11Q', 'IBM-Lagos-7Q', 'IBM-Montreal-27Q', 'IBM-Mumbai-27Q', 'IBM-Santiago-5Q', 'IBM-Toronto-27Q']
# cols = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD', 'Qubits', '2q-gates', 'Depth']
# subset_df = correlation_wEC_df.loc[:,[ 'Communication', 'Liveness', 'Parallelism', 'midMea', 'Entanglement', 'Depth', 'qubits', 'entangling-gates', 'regular-depth']]
# im, _ = heatmap(subset_df.to_numpy(dtype=float), rows, cols, ax=ax,
#                 cmap="cool", vmin=0, vmax=0.5,
#                 cbarlabel=r"Coefficient of Determination, $R^2$",
#                 cbar_kw={'pad':0.01})

# annotate_heatmap(im, size=7)

# ax.annotate("", xy=(0.668, 1.06), xycoords='axes fraction',
#             xytext=(0.668, -0.06), textcoords='axes fraction',
#             arrowprops=dict(arrowstyle="-", connectionstyle="arc3", color='r'))
# ax.annotate("", xy=(0.4, -0.028), xycoords='axes fraction',
#             xytext=(0.47, -0.028), textcoords='axes fraction',
#             arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
# ax.annotate('This work', (0.47,-0.04), xycoords='axes fraction', fontsize=8)
# ax.annotate('Typical features', (0.7,-0.04), xycoords='axes fraction', fontsize=8, horizontalalignment='left')

# plt.tight_layout()
# plt.show()
# plt.close()

# # Plot correlations EXCLUDING error-correction Benchmarks
# fig, ax = plt.subplots(dpi=300)

# rows = ['AQT-4Q', 'IBM-\nCasablanca-7Q', 'IBM-\nGuadalupe-16Q', 'IonQ-11Q', 'IBM-Lagos-7Q', 'IBM-Montreal-27Q', 'IBM-Mumbai-27Q', 'IBM-Santiago-5Q', 'IBM-Toronto-27Q']
# cols = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD', 'Qubits', '2q-gates', 'Depth']
# subset_df = correlation_woEC_df.loc[:,[ 'Communication', 'Liveness', 'Parallelism', 'midMea', 'Entanglement', 'Depth', 'qubits', 'entangling-gates', 'regular-depth']]
# im, _ = heatmap(subset_df.to_numpy(dtype=float), rows, cols, ax=ax,
#                 cmap="cool", vmin=0, vmax=0.5,
#                 cbarlabel=r"Coefficient of Determination, $R^2$",
#                 cbar_kw={'pad':0.01})

# annotate_heatmap(im, size=7)

# ax.annotate("", xy=(0.668, 1.06), xycoords='axes fraction',
#             xytext=(0.668, -0.06), textcoords='axes fraction',
#             arrowprops=dict(arrowstyle="-", connectionstyle="arc3", color='r'))
# ax.annotate("", xy=(0.4, -0.028), xycoords='axes fraction',
#             xytext=(0.47, -0.028), textcoords='axes fraction',
#             arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
# ax.annotate('This work', (0.47,-0.04), xycoords='axes fraction', fontsize=8)
# ax.annotate('Typical features', (0.7,-0.04), xycoords='axes fraction', fontsize=8, horizontalalignment='left')

# plt.tight_layout()
# plt.show()
# plt.close()

# # Plot the perfomance correlation of between individual devices and features
# print(list(feature_df.columns))
# print(list(score_df.index))
# device = 'toronto'
# feature = 'Entanglement'
# regression_plot(device, feature, feature_df, score_df)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

plt.rcParams["font.family"] = "Times New Roman"

# -----------------------------
# Load files
# -----------------------------
feature_df = pd.read_csv("Bit_Code_Updated_features.csv")
score_long_df = pd.read_csv("bitcode_benchmark_results.csv")

# -----------------------------
# Build matching benchmark labels
# -----------------------------
# This matches your current feature CSV labels:
# "3 data, 2 rounds", etc.
score_long_df["benchmark_instance"] = (
    score_long_df["n_qubits"].astype(str)
    + " data, "
    + score_long_df["n_rounds"].astype(str)
    + " rounds"
)

# -----------------------------
# Keep only benchmark instances present in both
# -----------------------------
merged_df = score_long_df.merge(feature_df, on="benchmark_instance", how="inner")

# Features to correlate against score
feature_cols = ["PC", "Liv", "Par", "Mea", "Ent", "CD"]

# -----------------------------
# Compute correlation heatmap values
# -----------------------------
backends = sorted(merged_df["backend"].unique())
correlation_df = pd.DataFrame(index=backends, columns=feature_cols, dtype=float)

for backend in backends:
    backend_df = merged_df[merged_df["backend"] == backend]

    for feature in feature_cols:
        x = backend_df[[feature]].to_numpy()
        y = backend_df["score"].to_numpy()

        # Need at least 2 points, and x cannot be constant
        if len(x) < 2 or np.allclose(x, x[0]):
            correlation_df.loc[backend, feature] = np.nan
        else:
            model = LinearRegression().fit(x, y)
            correlation_df.loc[backend, feature] = model.score(x, y)

print("Merged benchmark instances used:")
print(merged_df[["backend", "benchmark_instance", "score"]].sort_values(["backend", "benchmark_instance"]))
print()
print("Correlation dataframe:")
print(correlation_df)

# -----------------------------
# Plot annotated heatmap
# -----------------------------
fig, ax = plt.subplots(figsize=(7, 2.6), dpi=300)

data = correlation_df.to_numpy(dtype=float)
im = ax.imshow(data, cmap="cool", vmin=0, vmax=1, aspect="auto")

# Tick labels
ax.set_xticks(np.arange(len(feature_cols)))
ax.set_yticks(np.arange(len(backends)))
ax.set_xticklabels(feature_cols, fontsize=10)
ax.set_yticklabels(backends, fontsize=10)

# Cell annotations
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        value = data[i, j]
        if np.isnan(value):
            text = "nan"
        else:
            text = f"{value:.2f}"
        ax.text(j, i, text, ha="center", va="center", color="black", fontsize=8)

# Colorbar
cbar = fig.colorbar(im, ax=ax, pad=0.02)
cbar.set_label(r"Coefficient of Determination, $R^2$", rotation=90)

ax.set_title("Bit Code Feature/Score Correlation", fontsize=12)

plt.tight_layout()
plt.savefig("bitcode_correlation_heatmap.png", bbox_inches="tight", dpi=300)
plt.show()
plt.close()
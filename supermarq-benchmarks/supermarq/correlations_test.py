import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

from plotting_functions import heatmap, annotate_heatmap, regression_plot

# Load the dataframes from the uploaded CSVs
feature_df = pd.read_csv('Bit_Code_Updated_features.csv')
score_raw_df = pd.read_csv('bitcode_benchmark_results.csv')

# Match the original benchmark-instance labeling used in the feature sheet
feature_df = feature_df.set_index('benchmark_instance')

# Keep only benchmark instances that exist in the uploaded feature sheet
score_raw_df['benchmark_instance'] = score_raw_df.apply(
    lambda row: f"{int(row['n_qubits'])} data, {int(row['n_rounds'])} rounds",
    axis=1,
)
score_raw_df = score_raw_df[score_raw_df['benchmark_instance'].isin(feature_df.index)].copy()

# Build a score dataframe with the same general layout the original script expects:
# rows = devices, columns = benchmark instances, values = (score, stddev)
score_df = pd.DataFrame(index=sorted(score_raw_df['backend'].unique()), columns=feature_df.index)
for device in score_df.index:
    for benchmark in score_df.columns:
        matching_scores = score_raw_df.loc[
            (score_raw_df['backend'] == device)
            & (score_raw_df['benchmark_instance'] == benchmark),
            'score',
        ]
        if not matching_scores.empty:
            mean_score = float(matching_scores.mean())
            std_score = float(matching_scores.std(ddof=0)) if len(matching_scores) > 1 else 0.0
            score_df.loc[device, benchmark] = (mean_score, std_score)

# Create the correlation dataframes including the error-correction benchmarks
correlation_wEC_df = pd.DataFrame(data=None, index=score_df.index, columns=feature_df.columns)
correlation_wEC_df.head()

for feature in correlation_wEC_df.columns:

    application_features = feature_df.loc[:, feature]

    for device in correlation_wEC_df.index:
        scores = score_df.loc[device, :]

        x, y = [], []
        for benchmark in scores.index:
            if isinstance(scores.loc[benchmark], tuple):
                x.append(application_features.loc[benchmark])
                y.append(scores.loc[benchmark][0])

        X = np.array(x)[:, np.newaxis]
        Y = np.array(y)
        model = LinearRegression().fit(X, Y)
        correlation = model.score(X, Y)
        correlation_wEC_df.loc[device, feature] = correlation
correlation_wEC_df.head()

# Create the correlation dataframes excluding the error-correction benchmarks
correlation_woEC_df = pd.DataFrame(data=None, index=score_df.index, columns=feature_df.columns)
correlation_woEC_df.head()

for feature in correlation_woEC_df.columns:

    application_features = feature_df.loc[:, feature]

    for device in correlation_woEC_df.index:
        scores = score_df.loc[device, :]

        x, y = [], []
        for benchmark in scores.index:
            if 'code' in benchmark:
                continue
            if isinstance(scores.loc[benchmark], tuple):
                x.append(application_features.loc[benchmark])
                y.append(scores.loc[benchmark][0])

        X = np.array(x)[:, np.newaxis]
        Y = np.array(y)
        model = LinearRegression().fit(X, Y)
        correlation = model.score(X, Y)
        correlation_woEC_df.loc[device, feature] = correlation
correlation_woEC_df.head()

# Plot correlations INCLUDING error-correction benchmarks
fig, ax = plt.subplots(dpi=300)

rows = list(correlation_wEC_df.index)
cols = list(correlation_wEC_df.columns)
subset_df = correlation_wEC_df.loc[:, ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']]
im, _ = heatmap(subset_df.to_numpy(dtype=float), rows, cols, ax=ax,
                cmap="cool", vmin=0, vmax=1.0,
                cbarlabel=r"Coefficient of Determination, $R^2$",
                cbar_kw={'pad': 0.01})

annotate_heatmap(im, size=7)

plt.tight_layout()
plt.savefig("bitcode_correlation_heatmap_ec.png", bbox_inches="tight", dpi=300)
plt.show()
plt.close()

# Plot correlations EXCLUDING error-correction benchmarks
fig, ax = plt.subplots(dpi=300)

rows = list(correlation_woEC_df.index)
cols = list(correlation_woEC_df.columns)
subset_df = correlation_woEC_df.loc[:, ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']]
im, _ = heatmap(subset_df.to_numpy(dtype=float), rows, cols, ax=ax,
                cmap="cool", vmin=0, vmax=1.0,
                cbarlabel=r"Coefficient of Determination, $R^2$",
                cbar_kw={'pad': 0.01})

annotate_heatmap(im, size=7)

plt.tight_layout()
plt.savefig("bitcode_correlation_heatmap_no_ec.png", bbox_inches="tight", dpi=300)
plt.show()
plt.close()

# Plot the performance correlation between individual devices and features
print(list(feature_df.columns))
print(list(score_df.index))
device = 'ibm_torino'
feature = 'Ent'
regression_plot(device, feature, feature_df, score_df)

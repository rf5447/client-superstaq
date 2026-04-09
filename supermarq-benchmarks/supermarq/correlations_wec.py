import pandas as pd
from plotting_functions import heatmap, annotate_heatmap, regression_plot
import collections

import supermarq
import cirq
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

# Load the dataframes
feature_df = pd.read_pickle('./features/all_features_combined.pickle')
score_df = pd.read_pickle('combined_benchmark_scores.pickle')

# Make sure benchmark labels are the index of feature_df
if 'Unnamed: 0' in feature_df.columns:
    feature_df = feature_df.set_index('Unnamed: 0')
elif feature_df.columns[0] not in ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']:
    feature_df = feature_df.set_index(feature_df.columns[0])

# Optional: ensure no accidental whitespace mismatch
feature_df.index = feature_df.index.astype(str).str.strip()
score_df.columns = score_df.columns.astype(str).str.strip()

# Keep only feature columns
feature_df = feature_df[['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']]

# Create the correlation dataframe
correlation_wEC_df = pd.DataFrame(index=score_df.index, columns=feature_df.columns, dtype=float)

for feature in correlation_wEC_df.columns:
    application_features = feature_df[feature]

    for device in correlation_wEC_df.index:
        scores = score_df.loc[device, :]

        x, y = [], []
        for benchmark in scores.index:
            score_val = scores.loc[benchmark]

            if pd.notna(score_val) and benchmark in application_features.index:
                x.append(application_features.loc[benchmark])
                y.append(score_val)

        if len(x) >= 2:
            X = np.array(x).reshape(-1, 1)
            Y = np.array(y)

            model = LinearRegression().fit(X, Y)
            correlation_wEC_df.loc[device, feature] = model.score(X, Y)
        else:
            correlation_wEC_df.loc[device, feature] = np.nan

# Plot correlations INCLUDING error-correction benchmarks
fig, ax = plt.subplots(dpi=300)

rows = ['fez', 'marrakesh', 'torino']
cols = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD']
subset_df = correlation_wEC_df.loc[rows, cols]

im, _ = heatmap(
    subset_df.to_numpy(dtype=float),
    rows,
    cols,
    ax=ax,
    cmap="cool",
    vmin=0,
    vmax=0.5,
    cbarlabel=r"Coefficient of Determination, $R^2$",
    cbar_kw={'pad': 0.01}
)

annotate_heatmap(im, size=7)

ax.annotate("", xy=(0.668, 1.06), xycoords='axes fraction',
            xytext=(0.668, -0.06), textcoords='axes fraction',
            arrowprops=dict(arrowstyle="-", connectionstyle="arc3", color='r'))
ax.annotate("", xy=(0.4, -0.028), xycoords='axes fraction',
            xytext=(0.47, -0.028), textcoords='axes fraction',
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
ax.annotate('This work', (0.47, -0.04), xycoords='axes fraction', fontsize=8)
ax.annotate('Typical features', (0.7, -0.04), xycoords='axes fraction',
            fontsize=8, horizontalalignment='left')

plt.tight_layout()
plt.savefig("correlations_wec_heatmap.png", dpi=300, bbox_inches="tight")
plt.close()
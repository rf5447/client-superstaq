import pandas as pd
from plotting_functions import heatmap, annotate_heatmap, regression_plot

# Load the dataframes from the data/ directory
# feature_df: rows = benchmarks, columns = features
# score_df: rows = devices, columns = benchmarks
feature_df = pd.read_pickle('data/feature_dataframe.pickle')
score_df = pd.read_pickle('data/benchmark_scores_dataframe.pickle')

# Create the correlation dataframes including the error-correction benchmarks
correlation_wEC_df = pd.DataFrame(data=None, index=score_df.index, columns=feature_df.columns)
correlation_wEC_df.head()

for feature in correlation_wEC_df.columns:
    
    application_features = feature_df.loc[:, feature]
    
    for device in correlation_wEC_df.index:
        scores = score_df.loc[device, :]

        x, y = [], []
        for benchmark in scores.index:
            #if 'code' in benchmark:
            #    continue
            if isinstance(scores.loc[benchmark], tuple):
                x.append(application_features.loc[benchmark])
                y.append(scores.loc[benchmark][0])

        X = np.array(x)[:, np.newaxis]
        Y = np.array(y)
        model = LinearRegression().fit(X, Y)
        correlation = model.score(X, Y)        
        correlation_wEC_df.loc[device, feature] = correlation
correlation_wEC_df.head()

# Plot correlations INCLUDING error-correction Benchmarks
fig, ax = plt.subplots(dpi=300)

rows = ['AQT-4Q', 'IBM-\nCasablanca-7Q', 'IBM-\nGuadalupe-16Q', 'IonQ-11Q', 'IBM-Lagos-7Q', 'IBM-Montreal-27Q', 'IBM-Mumbai-27Q', 'IBM-Santiago-5Q', 'IBM-Toronto-27Q']
cols = ['PC', 'Liv', 'Par', 'Mea', 'Ent', 'CD', 'Qubits', '2q-gates', 'Depth']
subset_df = correlation_wEC_df.loc[:,[ 'Communication', 'Liveness', 'Parallelism', 'midMea', 'Entanglement', 'Depth', 'qubits', 'entangling-gates', 'regular-depth']]
im, _ = heatmap(subset_df.to_numpy(dtype=float), rows, cols, ax=ax,
                cmap="cool", vmin=0, vmax=0.5,
                cbarlabel=r"Coefficient of Determination, $R^2$",
                cbar_kw={'pad':0.01})

annotate_heatmap(im, size=7)

ax.annotate("", xy=(0.668, 1.06), xycoords='axes fraction',
            xytext=(0.668, -0.06), textcoords='axes fraction',
            arrowprops=dict(arrowstyle="-", connectionstyle="arc3", color='r'))
ax.annotate("", xy=(0.4, -0.028), xycoords='axes fraction',
            xytext=(0.47, -0.028), textcoords='axes fraction',
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
ax.annotate('This work', (0.47,-0.04), xycoords='axes fraction', fontsize=8)
ax.annotate('Typical features', (0.7,-0.04), xycoords='axes fraction', fontsize=8, horizontalalignment='left')

plt.tight_layout()
plt.show()
plt.close()
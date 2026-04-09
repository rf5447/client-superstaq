import pandas as pd
from plotting_functions import heatmap, annotate_heatmap, regression_plot
import collections

import supermarq
import cirq
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

# Load the dataframes from the data/ directory
# feature_df: rows = benchmarks, columns = features
# score_df: rows = devices, columns = benchmarks
feature_df = pd.read_pickle('feature_dataframe.pickle')
score_df = pd.read_pickle('benchmark_scores_dataframe.pickle')

# Save as CSV
feature_df.to_csv('feature_dataframe.csv')
score_df.to_csv('benchmark_scores_dataframe.csv')
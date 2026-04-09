import pandas as pd
from pathlib import Path

features_dir = Path("features")
csv_files = sorted(features_dir.glob("*_features.csv"))

combined_df = pd.concat(
    [pd.read_csv(f) for f in csv_files],
    axis=0,
    ignore_index=True
)

combined_df.to_csv(features_dir / "all_features_combined.csv", index=False)
combined_df.to_pickle(features_dir / "all_features_combined.pickle")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

cpu_file = "ghz_timing_results_excludingwarmup_ordered.csv"
gpu_file = "ghz_timing_results_cudaq_excludingwarmup_ordered.csv"

cpu_df = pd.read_csv(cpu_file)
gpu_df = pd.read_csv(gpu_file)

def clean_df(df, platform):
    if "Circuit creation time (ms)" in df.columns:
        df = df.rename(columns={"Circuit creation time (ms)": "Creation time (ms)"})
    if "Kernel creation time (ms)" in df.columns:
        df = df.rename(columns={"Kernel creation time (ms)": "Creation time (ms)"})

    df["platform"] = platform
    df["num_qubits"] = pd.to_numeric(df["num_qubits"])
    df["Total time (ms)"] = (
        df["Creation time (ms)"]
        + df["Simulation time (ms)"]
        + df["Score calculation time (ms)"]
    )

    return df[[
        "platform",
        "method",
        "num_qubits",
        "Creation time (ms)",
        "Simulation time (ms)",
        "Score calculation time (ms)",
        "Total time (ms)"
    ]].copy()

cpu_df = clean_df(cpu_df, "CPU")
gpu_df = clean_df(gpu_df, "GPU")
df = pd.concat([cpu_df, gpu_df], ignore_index=True)

group_cols = ["platform", "method", "num_qubits"]
time_cols = [
    "Creation time (ms)",
    "Simulation time (ms)",
    "Score calculation time (ms)",
    "Total time (ms)"
]

mean_df = df.groupby(group_cols)[time_cols].mean().reset_index()
std_df = df.groupby(group_cols)[time_cols].std().reset_index()

methods = ["ladder", "logdepth", "star"]
platforms = ["CPU", "GPU"]
qubits = sorted(mean_df["num_qubits"].unique())

plot_specs = [
    ("Creation time (ms)", "Circuit Creation Time"),
    ("Simulation time (ms)", "Circuit Simulation Time"),
    ("Score calculation time (ms)", "Score Calculation Time"),
    ("Total time (ms)", "Total Time"),
]

bar_width = 0.22
x = np.arange(len(qubits))

fig, axes = plt.subplots(2, 4, figsize=(24, 10), sharex=True)

for row, platform in enumerate(platforms):
    for col, (time_col, pretty_name) in enumerate(plot_specs):
        ax = axes[row, col]

        pmean = mean_df[mean_df["platform"] == platform]
        pstd = std_df[std_df["platform"] == platform]

        for i, method in enumerate(methods):
            sub_mean = (
                pmean[pmean["method"] == method]
                .sort_values("num_qubits")
            )
            sub_std = (
                pstd[pstd["method"] == method]
                .sort_values("num_qubits")
            )

            xpos = x + (i - 1) * bar_width
            y = sub_mean[time_col].to_numpy()
            yerr = sub_std[time_col].to_numpy()

            ax.bar(
                xpos,
                y,
                width=bar_width,
                yerr=yerr,
                capsize=4,
                label=method if (row == 0 and col == 0) else None
            )

        ax.set_title(f"{platform} {pretty_name}", fontsize=18, fontweight="semibold")
        ax.set_xticks(x)
        ax.set_xticklabels(qubits, fontsize=18)
        ax.tick_params(axis="x", labelsize=18, labelbottom=True)
        ax.set_xlabel("# Qubits", fontsize=18)
        ax.set_ylabel("Time (ms)", fontsize=18)
        ax.tick_params(axis="y", labelsize=18)
        ax.set_ylim(bottom=0)
        ax.grid(axis="y", alpha=0.3)

handles, labels = axes[0, 0].get_legend_handles_labels()
fig.legend(
    handles,
    labels,
    loc="upper center",
    ncol=3,
    bbox_to_anchor=(0.5, 0.92),
    fontsize=18
)

fig.suptitle(
    "CPU and GPU Run Time Comparison of GHZ Benchmark",
    fontsize=22,
    fontweight="semibold",
    y=0.98
)

plt.tight_layout(rect=[0, 0, 1, 0.90])
plt.savefig("ghz_timing_2x4_subplots_excludingwarmuprun_ordered.png", dpi=300)
plt.show()
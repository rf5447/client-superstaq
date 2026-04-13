import os
import re
import glob

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from benchmarks.ghz import GHZ
from benchmarks.mermin_bell import MerminBell
from benchmarks.vqe_proxy import VQEProxy


# ------------------------------------------------------------
# USER SETTINGS
# ------------------------------------------------------------
INPUT_DIR = "staqdatacsv"
OUTPUT_DIR = "scored_outputs"
PLOT_DIR = os.path.join(OUTPUT_DIR, "plots")
RAW_PLOT_DIR = os.path.join(PLOT_DIR, "raw_distributions")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PLOT_DIR, exist_ok=True)
os.makedirs(RAW_PLOT_DIR, exist_ok=True)


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------
def read_counts_csv(csv_path: str) -> dict[str, int]:
    """
    Read a CSV of the form:

    ,000,001,010,...
    0,120,4,1,...

    Returns:
        dict mapping bitstring -> int count
    """
    df = pd.read_csv(csv_path, index_col=0)

    if df.shape[0] < 1:
        raise ValueError(f"{csv_path} does not have any data rows.")

    row = df.iloc[0]

    counts = {}
    for bitstring, count in row.items():
        bitstring = str(bitstring).strip()

        if bitstring == "":
            continue

        if pd.isna(count):
            count = 0

        counts[bitstring] = int(count)

    return counts


def total_counts(counts: dict[str, int]) -> int:
    return int(sum(counts.values()))


def ordered_bitstrings(n_qubits: int) -> list[str]:
    return [format(i, f"0{n_qubits}b") for i in range(2**n_qubits)]


def parse_filename(filename: str) -> dict:
    """
    Parse benchmark details from filenames like:

    146331-RunSingleQasmFile-ghz_3_qubits_qasm_counts.csv
    146353-RunSingleQasmFile-vqeproxy_4_qubits_1_layers_x_basis_qasm_counts.csv
    146387-RunSingleQasmFile-mb_3_qubits_qasm_counts.csv
    """
    base = os.path.basename(filename)

    # GHZ
    m = re.match(
        r"(?P<job_id>\d+)-RunSingleQasmFile-ghz_(?P<nq>\d+)_qubits_qasm_counts\.csv$",
        base,
    )
    if m:
        return {
            "benchmark": "ghz",
            "job_id": int(m.group("job_id")),
            "n_qubits": int(m.group("nq")),
        }

    # Mermin-Bell
    m = re.match(
        r"(?P<job_id>\d+)-RunSingleQasmFile-mb_(?P<nq>\d+)_qubits_qasm_counts\.csv$",
        base,
    )
    if m:
        return {
            "benchmark": "mb",
            "job_id": int(m.group("job_id")),
            "n_qubits": int(m.group("nq")),
        }

    # VQE Proxy
    m = re.match(
        r"(?P<job_id>\d+)-RunSingleQasmFile-vqeproxy_(?P<nq>\d+)_qubits_(?P<layers>\d+)_layers_(?P<basis>[xz])_basis_qasm_counts\.csv$",
        base,
    )
    if m:
        return {
            "benchmark": "vqeproxy",
            "job_id": int(m.group("job_id")),
            "n_qubits": int(m.group("nq")),
            "n_layers": int(m.group("layers")),
            "basis": m.group("basis"),
        }

    raise ValueError(f"Could not parse filename: {base}")


def compute_score(meta: dict, counts) -> float:
    """
    Build the right benchmark object and call its score().
    For GHZ / MB, counts is a single dict.
    For VQEProxy, counts is [counts_z, counts_x].
    """
    bench = meta["benchmark"]

    if bench == "ghz":
        benchmark_obj = GHZ(meta["n_qubits"])
        return float(benchmark_obj.score(counts))

    elif bench == "mb":
        benchmark_obj = MerminBell(meta["n_qubits"])
        return float(benchmark_obj.score(counts))

    elif bench == "vqeproxy":
        benchmark_obj = VQEProxy(meta["n_qubits"], meta["n_layers"])
        return float(benchmark_obj.score(counts))

    else:
        raise ValueError(f"Unsupported benchmark type: {bench}")


# ------------------------------------------------------------
# RAW DISTRIBUTION PLOTS
# ------------------------------------------------------------
def plot_raw_distribution(counts: dict[str, int], n_qubits: int, title: str, output_path: str) -> None:
    """
    Plot raw counts with bitstrings ordered as:
    0000, 0001, 0010, ...
    and put the counts axis on the right.

    Add shot-noise error bars using Poisson statistics:
    sigma = sqrt(N) for each count bin.
    """
    bitstrings = ordered_bitstrings(n_qubits)
    y = np.array([counts.get(bit, 0) for bit in bitstrings], dtype=float)
    yerr = np.sqrt(y)
    x = np.arange(len(bitstrings))

    fig, ax = plt.subplots(figsize=(max(8, len(bitstrings) * 0.45), 5))
    ax.bar(x, y, yerr=yerr, capsize=2)

    ax.set_xlabel("Bitstring")
    ax.set_ylabel("Counts")
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(bitstrings, rotation=90)

    # Put y-axis on the right
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(True)

    ax.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

# ------------------------------------------------------------
# PLOTTING
# ------------------------------------------------------------
def plot_ghz(df: pd.DataFrame, outdir: str) -> None:
    if df.empty:
        return

    df = df.sort_values("n_qubits")
    plt.figure(figsize=(7, 5))
    plt.bar(df["n_qubits"], df["score"])
    plt.xlabel("Qubits")
    plt.ylabel("Score")
    plt.ylim(0, 1)

    # whole-number x-axis only
    qubits = sorted(df["n_qubits"].unique())
    plt.xticks(qubits)

    plt.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "ghz_scores.png"), dpi=300)
    plt.close()


def plot_mb(df: pd.DataFrame, outdir: str) -> None:
    if df.empty:
        return

    df = df.sort_values("n_qubits")
    plt.figure(figsize=(7, 5))
    plt.bar(df["n_qubits"], df["score"])
    plt.xlabel("Qubits")
    plt.ylabel("Score")
    plt.ylim(0, 1)

    # whole-number x-axis only
    qubits = sorted(df["n_qubits"].unique())
    plt.xticks(qubits)

    plt.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "mb_scores.png"), dpi=300)
    plt.close()


def plot_vqeproxy(df: pd.DataFrame, outdir: str) -> None:
    if df.empty:
        return

    plot_df = (
        df.groupby(["n_layers", "n_qubits"], as_index=False)["score"]
        .mean()
        .sort_values(["n_layers", "n_qubits"])
    )

    layers = sorted(plot_df["n_layers"].unique())
    qubits = sorted(plot_df["n_qubits"].unique())

    x = np.arange(len(layers))
    width = 0.8 / len(qubits)

    plt.figure(figsize=(8, 5))

    for i, nq in enumerate(qubits):
        sub = plot_df[plot_df["n_qubits"] == nq]
        sub = sub.set_index("n_layers").reindex(layers)

        plt.bar(
            x + (i - (len(qubits) - 1) / 2) * width,
            sub["score"],
            width=width,
            label=f"{nq} qubits",
        )

    plt.xlabel("Layers")
    plt.ylabel("Score")
    plt.ylim(0, 1)
    plt.xticks(x, layers)  # layers are whole numbers already
    plt.grid(True, axis="y", alpha=0.3)
    plt.legend(title="Qubits")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "vqeproxy_scores.png"), dpi=300)
    plt.close()


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
def main():
    csv_files = sorted(glob.glob(os.path.join(INPUT_DIR, "*_counts.csv")))

    if not csv_files:
        print(f"No *_counts.csv files found in {INPUT_DIR}")
        return

    ghz_rows = []
    mb_rows = []
    vqe_rows = []

    # collect VQE x/z files until both are present
    vqe_pending = {}

    for csv_path in csv_files:
        try:
            meta = parse_filename(csv_path)
            counts = read_counts_csv(csv_path)
            shots = total_counts(counts)
            base_name = os.path.basename(csv_path)

            if meta["benchmark"] == "ghz":
                print(f"DEBUG GHZ counts for {base_name}: {counts}")

                score = compute_score(meta, counts)

                row = {
                    "source_file": base_name,
                    "job_id": meta["job_id"],
                    "n_qubits": meta["n_qubits"],
                    "total_counts": shots,
                    "score": score,
                }
                ghz_rows.append(row)

                raw_plot_path = os.path.join(
                    RAW_PLOT_DIR,
                    os.path.splitext(base_name)[0] + "_raw.png"
                )
                plot_raw_distribution(
                    counts,
                    meta["n_qubits"],
                    f"GHZ Raw Distribution ({meta['n_qubits']} qubits)",
                    raw_plot_path,
                )

                print(
                    f"Processed {base_name}  "
                    f"score={score:.6f}  shots={shots}"
                )

            elif meta["benchmark"] == "mb":
                print(f"DEBUG MB counts for {base_name}: {counts}")

                score = compute_score(meta, counts)

                row = {
                    "source_file": base_name,
                    "job_id": meta["job_id"],
                    "n_qubits": meta["n_qubits"],
                    "total_counts": shots,
                    "score": score,
                }
                mb_rows.append(row)

                raw_plot_path = os.path.join(
                    RAW_PLOT_DIR,
                    os.path.splitext(base_name)[0] + "_raw.png"
                )
                plot_raw_distribution(
                    counts,
                    meta["n_qubits"],
                    f"Mermin-Bell Raw Distribution ({meta['n_qubits']} qubits)",
                    raw_plot_path,
                )

                print(
                    f"Processed {base_name}  "
                    f"score={score:.6f}  shots={shots}"
                )

            elif meta["benchmark"] == "vqeproxy":
                key = (meta["job_id"], meta["n_qubits"], meta["n_layers"])

                if key not in vqe_pending:
                    vqe_pending[key] = {
                        "job_id": meta["job_id"],
                        "n_qubits": meta["n_qubits"],
                        "n_layers": meta["n_layers"],
                        "z_counts": None,
                        "x_counts": None,
                        "z_shots": None,
                        "x_shots": None,
                        "z_file": None,
                        "x_file": None,
                    }

                if meta["basis"] == "z":
                    vqe_pending[key]["z_counts"] = counts
                    vqe_pending[key]["z_shots"] = shots
                    vqe_pending[key]["z_file"] = base_name

                    raw_plot_path = os.path.join(
                        RAW_PLOT_DIR,
                        os.path.splitext(base_name)[0] + "_raw.png"
                    )
                    plot_raw_distribution(
                        counts,
                        meta["n_qubits"],
                        f"VQE Proxy Raw Distribution Z Basis ({meta['n_qubits']} qubits, {meta['n_layers']} layers)",
                        raw_plot_path,
                    )

                elif meta["basis"] == "x":
                    vqe_pending[key]["x_counts"] = counts
                    vqe_pending[key]["x_shots"] = shots
                    vqe_pending[key]["x_file"] = base_name

                    raw_plot_path = os.path.join(
                        RAW_PLOT_DIR,
                        os.path.splitext(base_name)[0] + "_raw.png"
                    )
                    plot_raw_distribution(
                        counts,
                        meta["n_qubits"],
                        f"VQE Proxy Raw Distribution X Basis ({meta['n_qubits']} qubits, {meta['n_layers']} layers)",
                        raw_plot_path,
                    )

        except Exception as e:
            print(f"Skipping {os.path.basename(csv_path)} due to error: {e}")

    # process VQE pairs only after both x and z are available
    for key, item in vqe_pending.items():
        try:
            if item["z_counts"] is None or item["x_counts"] is None:
                print(f"Skipping VQE pair {key} because one of x/z basis files is missing.")
                continue

            meta = {
                "benchmark": "vqeproxy",
                "job_id": item["job_id"],
                "n_qubits": item["n_qubits"],
                "n_layers": item["n_layers"],
            }

            print(f"DEBUG VQE Z counts for {item['z_file']}: {item['z_counts']}")
            print(f"DEBUG VQE X counts for {item['x_file']}: {item['x_counts']}")

            score = compute_score(meta, [item["z_counts"], item["x_counts"]])

            row = {
                "source_file_z": item["z_file"],
                "source_file_x": item["x_file"],
                "job_id": item["job_id"],
                "n_qubits": item["n_qubits"],
                "n_layers": item["n_layers"],
                "total_counts_z": item["z_shots"],
                "total_counts_x": item["x_shots"],
                "total_counts": item["z_shots"] + item["x_shots"],
                "score": score,
            }
            vqe_rows.append(row)

            print(
                f"Processed VQE pair job_id={item['job_id']} "
                f"n_qubits={item['n_qubits']} "
                f"n_layers={item['n_layers']} "
                f"score={score:.6f} "
                f"shots={item['z_shots'] + item['x_shots']}"
            )

        except Exception as e:
            print(f"Skipping VQE pair {key} due to error: {e}")

    ghz_df = pd.DataFrame(ghz_rows)
    mb_df = pd.DataFrame(mb_rows)
    vqe_df = pd.DataFrame(vqe_rows)

    # Save summary CSVs
    ghz_csv = os.path.join(OUTPUT_DIR, "ghz_scores.csv")
    mb_csv = os.path.join(OUTPUT_DIR, "mb_scores.csv")
    vqe_csv = os.path.join(OUTPUT_DIR, "vqeproxy_scores.csv")

    if not ghz_df.empty:
        ghz_df = ghz_df.sort_values(["n_qubits", "job_id"])
        ghz_df.to_csv(ghz_csv, index=False)
        print(f"Saved {ghz_csv}")

    if not mb_df.empty:
        mb_df = mb_df.sort_values(["n_qubits", "job_id"])
        mb_df.to_csv(mb_csv, index=False)
        print(f"Saved {mb_csv}")

    if not vqe_df.empty:
        vqe_df = vqe_df.sort_values(["n_qubits", "n_layers", "job_id"])
        vqe_df.to_csv(vqe_csv, index=False)
        print(f"Saved {vqe_csv}")

    # Plots
    plot_ghz(ghz_df, PLOT_DIR)
    plot_mb(mb_df, PLOT_DIR)
    plot_vqeproxy(vqe_df, PLOT_DIR)
    print(f"Saved plots to {PLOT_DIR}")
    print(f"Saved raw distribution plots to {RAW_PLOT_DIR}")


if __name__ == "__main__":
    main()
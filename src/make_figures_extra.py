"""Ek grafikler: optimallik farkı (brute force'a göre) ve zaman-kalite
ödünleşimi."""
import pandas as pd
import matplotlib.pyplot as plt


def fig_optimality_gap(outpath="results/figures/fig4_optimality_gap.png"):
    df = pd.read_csv("results/optimality_gap_summary.csv")
    df = df.sort_values("mean_gap_pct")
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(df["method"], df["mean_gap_pct"])
    ax.set_xlabel("Optimale göre ortalama fark (%)")
    ax.set_title("Kesin optimale göre fark (n=9, 10 seed, brute force referans)")
    fig.tight_layout()
    fig.savefig(outpath, dpi=150)
    plt.close(fig)


def fig_time_quality_tradeoff(outpath="results/figures/fig5_time_quality_tradeoff.png"):
    raw = pd.read_csv("results/comparison_raw.csv")
    summary = raw.groupby(["n_holes", "method"]).agg(
        mean_len=("path_length", "mean"), mean_time=("elapsed_s", "mean")
    ).reset_index()

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), sharey=False)
    for ax, n_holes in zip(axes, sorted(summary["n_holes"].unique())):
        sub = summary[summary["n_holes"] == n_holes]
        ax.scatter(sub["mean_time"], sub["mean_len"])
        for _, row in sub.iterrows():
            ax.annotate(row["method"], (row["mean_time"], row["mean_len"]),
                        fontsize=8, xytext=(4, 4), textcoords="offset points")
        ax.set_xscale("log")
        ax.set_xlabel("Ortalama süre (s, log ölçek)")
        ax.set_title(f"n_holes = {n_holes}")
    axes[0].set_ylabel("Ortalama yol uzunluğu (mm)")
    fig.suptitle("Zaman-kalite ödünleşimi")
    fig.tight_layout()
    fig.savefig(outpath, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    fig_optimality_gap()
    fig_time_quality_tradeoff()
    print("Extra figures written to results/figures/")

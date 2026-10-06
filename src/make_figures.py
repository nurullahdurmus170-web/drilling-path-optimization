"""results/ içindeki CSV'lerden ve örnek bir problemden grafik üretir."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .problem import generate_holes, distance_matrix, path_length
from .baselines import nearest_neighbor, two_opt
from .aco import run_aco
from .abc_algorithm import run_abc


def fig_example_paths(n_holes=30, seed=0, outpath="results/figures/fig1_example_paths.png"):
    origin, points = generate_holes(n_holes=n_holes, seed=seed)
    dist = distance_matrix(origin, points)

    nn_order = nearest_neighbor(dist, n_holes)
    two_opt_order, two_opt_len = two_opt(nn_order, origin, points)
    aco_order, aco_len, _ = run_aco(origin, points, dist, n_iterations=150, seed=seed)
    abc_order, abc_len, _ = run_abc(origin, points, n_iterations=150, seed=seed)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharex=True, sharey=True)
    plans = [("NN + 2-opt", two_opt_order, two_opt_len),
             ("ACO", aco_order, aco_len),
             ("ABC", abc_order, abc_len)]
    for ax, (name, order, length) in zip(axes, plans):
        seq = np.vstack([origin, points[order]])
        ax.plot(seq[:, 0], seq[:, 1], "-o", markersize=4, linewidth=1)
        ax.plot(*origin, "s", color="red", markersize=8, label="Başlangıç")
        ax.set_title(f"{name}\nUzunluk: {length:.0f} mm")
        ax.set_xlabel("x (mm)")
        ax.legend(fontsize=8)
    axes[0].set_ylabel("y (mm)")
    fig.suptitle(f"Örnek delik dizilimi (n={n_holes}, seed={seed}) üzerinde bulunan yollar")
    fig.tight_layout()
    fig.savefig(outpath, dpi=150)
    plt.close(fig)


def fig_convergence(outpath="results/figures/fig2_convergence.png"):
    df = pd.read_csv("results/convergence_seed0.csv")
    n_sizes = sorted(df["n_holes"].unique())
    fig, axes = plt.subplots(1, len(n_sizes), figsize=(5 * len(n_sizes), 4), sharey=False)
    if len(n_sizes) == 1:
        axes = [axes]
    for ax, n_holes in zip(axes, n_sizes):
        sub = df[df["n_holes"] == n_holes]
        ax.plot(sub["iteration"], sub["ACO"], label="ACO")
        ax.plot(sub["iteration"], sub["ABC"], label="ABC")
        ax.set_title(f"n_holes = {n_holes}")
        ax.set_xlabel("İterasyon")
        ax.legend()
    axes[0].set_ylabel("O ana kadarki en iyi yol uzunluğu (mm)")
    fig.suptitle("Yakınsama karşılaştırması (seed=0)")
    fig.tight_layout()
    fig.savefig(outpath, dpi=150)
    plt.close(fig)


def fig_summary_bars(outpath="results/figures/fig3_summary_by_size.png"):
    df = pd.read_csv("results/comparison_summary.csv")
    n_sizes = sorted(df["n_holes"].unique())
    fig, axes = plt.subplots(1, len(n_sizes), figsize=(5 * len(n_sizes), 4), sharey=False)
    if len(n_sizes) == 1:
        axes = [axes]
    for ax, n_holes in zip(axes, n_sizes):
        sub = df[df["n_holes"] == n_holes].sort_values("mean")
        ax.barh(sub["method"], sub["mean"], xerr=sub["std"])
        ax.set_title(f"n_holes = {n_holes}")
        ax.set_xlabel("Ortalama yol uzunluğu (mm, 5 seed)")
    fig.suptitle("Yöntem karşılaştırması (hata çubuğu = std)")
    fig.tight_layout()
    fig.savefig(outpath, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    fig_example_paths()
    fig_convergence()
    fig_summary_bars()
    print("Figures written to results/figures/")

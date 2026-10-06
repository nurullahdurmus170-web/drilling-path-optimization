"""Tüm yöntemleri birden fazla rastgele tohum (seed) ve delik sayısı
üzerinde çalıştırıp karşılaştırmalı sonuç üretir.

Kullanım:
    python -m src.run_experiment
Çıktılar results/ klasörüne yazılır.
"""
import time
import numpy as np
import pandas as pd

from .problem import generate_holes, distance_matrix, path_length
from .baselines import random_order, nearest_neighbor, two_opt
from .aco import run_aco
from .abc_algorithm import run_abc

N_HOLES_LIST = [15, 30, 50]
SEEDS = [0, 1, 2, 3, 4]
N_ITERATIONS = 150


def run_all_methods(n_holes, seed):
    origin, points = generate_holes(n_holes=n_holes, seed=seed)
    dist = distance_matrix(origin, points)

    rows = []

    t0 = time.perf_counter()
    order = random_order(n_holes, seed=seed)
    rows.append(("Rastgele sıra", path_length(order, origin, points), time.perf_counter() - t0))

    t0 = time.perf_counter()
    nn_order = nearest_neighbor(dist, n_holes)
    rows.append(("En yakın komşu (NN)", path_length(nn_order, origin, points), time.perf_counter() - t0))

    t0 = time.perf_counter()
    _, two_opt_len = two_opt(nn_order, origin, points)
    rows.append(("NN + 2-opt", two_opt_len, time.perf_counter() - t0))

    t0 = time.perf_counter()
    _, aco_len, aco_hist = run_aco(origin, points, dist, n_iterations=N_ITERATIONS, seed=seed)
    rows.append(("ACO", aco_len, time.perf_counter() - t0))

    t0 = time.perf_counter()
    _, abc_len, abc_hist = run_abc(origin, points, n_iterations=N_ITERATIONS, seed=seed)
    rows.append(("ABC", abc_len, time.perf_counter() - t0))

    return rows, aco_hist, abc_hist


def main():
    all_rows = []
    convergence_rows = []

    for n_holes in N_HOLES_LIST:
        for seed in SEEDS:
            rows, aco_hist, abc_hist = run_all_methods(n_holes, seed)
            for method, length, elapsed_s in rows:
                all_rows.append({
                    "n_holes": n_holes, "seed": seed, "method": method,
                    "path_length": length, "elapsed_s": elapsed_s,
                })
            if seed == 0:
                for it, (a, b) in enumerate(zip(aco_hist, abc_hist)):
                    convergence_rows.append({"n_holes": n_holes, "iteration": it, "ACO": a, "ABC": b})

    df = pd.DataFrame(all_rows)
    df.to_csv("results/comparison_raw.csv", index=False)

    summary = (
        df.groupby(["n_holes", "method"])["path_length"]
        .agg(["mean", "std", "min", "max"])
        .reset_index()
        .sort_values(["n_holes", "mean"])
    )
    summary.to_csv("results/comparison_summary.csv", index=False)

    conv_df = pd.DataFrame(convergence_rows)
    conv_df.to_csv("results/convergence_seed0.csv", index=False)

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()

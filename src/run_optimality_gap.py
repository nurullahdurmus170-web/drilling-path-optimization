"""Küçük problem boyutlarında (kesin optimalin hesaplanabildiği n) tüm
yöntemlerin optimale olan yüzde uzaklığını (optimality gap) ölçer.

Kullanım:
    python -m src.run_optimality_gap
"""
import time
import numpy as np
import pandas as pd

from .problem import generate_holes, distance_matrix, path_length
from .baselines import nearest_neighbor, two_opt
from .aco import run_aco
from .abc_algorithm import run_abc
from .exact import brute_force_optimal

N_HOLES = 9           # 9! = 362,880 permütasyon; saniyeler içinde biter
SEEDS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
N_ITERATIONS = 150


def main():
    rows = []
    for seed in SEEDS:
        origin, points = generate_holes(n_holes=N_HOLES, seed=seed)
        dist = distance_matrix(origin, points)

        t0 = time.perf_counter()
        _, opt_len = brute_force_optimal(origin, points)
        t_exact = time.perf_counter() - t0

        t0 = time.perf_counter()
        nn_order = nearest_neighbor(dist, N_HOLES)
        nn_len = path_length(nn_order, origin, points)
        t_nn = time.perf_counter() - t0

        t0 = time.perf_counter()
        _, two_opt_len = two_opt(nn_order, origin, points)
        t_two_opt = time.perf_counter() - t0 + t_nn

        t0 = time.perf_counter()
        _, aco_len, _ = run_aco(origin, points, dist, n_iterations=N_ITERATIONS, seed=seed)
        t_aco = time.perf_counter() - t0

        t0 = time.perf_counter()
        _, abc_len, _ = run_abc(origin, points, n_iterations=N_ITERATIONS, seed=seed)
        t_abc = time.perf_counter() - t0

        for method, length, elapsed in [
            ("Optimal (brute force)", opt_len, t_exact),
            ("NN", nn_len, t_nn),
            ("NN + 2-opt", two_opt_len, t_two_opt),
            ("ACO", aco_len, t_aco),
            ("ABC", abc_len, t_abc),
        ]:
            gap_pct = 100.0 * (length - opt_len) / opt_len
            rows.append({
                "seed": seed, "method": method, "path_length": length,
                "gap_pct_vs_optimal": gap_pct, "elapsed_s": elapsed,
            })

    df = pd.DataFrame(rows)
    df.to_csv("results/optimality_gap_raw.csv", index=False)

    summary = (
        df.groupby("method")
        .agg(mean_gap_pct=("gap_pct_vs_optimal", "mean"),
             max_gap_pct=("gap_pct_vs_optimal", "max"),
             mean_elapsed_s=("elapsed_s", "mean"))
        .reset_index()
        .sort_values("mean_gap_pct")
    )
    summary.to_csv("results/optimality_gap_summary.csv", index=False)
    print(f"n_holes={N_HOLES}, {len(SEEDS)} seed\n")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()

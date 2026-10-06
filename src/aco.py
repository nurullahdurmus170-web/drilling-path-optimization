"""Karınca Kolonisi Optimizasyonu (ACO) - açık tur TSP için uygulama."""
import numpy as np
from .problem import path_length


def run_aco(origin, points, dist_matrix, n_ants=20, n_iterations=150,
            alpha=1.0, beta=3.0, evaporation=0.5, q=100.0, seed=0):
    rng = np.random.default_rng(seed)
    n = len(points)
    n_nodes = n + 1  # 0 = origin
    pheromone = np.ones((n_nodes, n_nodes))
    with np.errstate(divide="ignore"):
        heuristic = 1.0 / (dist_matrix + np.eye(n_nodes))
    np.fill_diagonal(heuristic, 0.0)

    best_order, best_len = None, np.inf
    history = []

    for _ in range(n_iterations):
        all_orders, all_lens = [], []
        for _ant in range(n_ants):
            visited = np.zeros(n_nodes, dtype=bool)
            visited[0] = True
            current = 0
            order = []
            for _step in range(n):
                probs = (pheromone[current] ** alpha) * (heuristic[current] ** beta)
                probs[visited] = 0.0
                total = probs.sum()
                if total <= 0:
                    candidates = np.where(~visited)[0]
                    nxt = rng.choice(candidates)
                else:
                    probs = probs / total
                    nxt = rng.choice(n_nodes, p=probs)
                order.append(nxt - 1)
                visited[nxt] = True
                current = nxt
            order = np.array(order)
            length = path_length(order, origin, points)
            all_orders.append(order)
            all_lens.append(length)
            if length < best_len:
                best_len, best_order = length, order

        pheromone *= (1.0 - evaporation)
        for order, length in zip(all_orders, all_lens):
            deposit = q / length
            prev = 0
            for node in order:
                pheromone[prev, node + 1] += deposit
                pheromone[node + 1, prev] += deposit
                prev = node + 1

        history.append(best_len)

    return best_order, best_len, history

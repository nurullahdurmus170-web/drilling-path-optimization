"""Karşılaştırma için klasik baseline'lar: rastgele sıra, en yakın komşu,
ve en yakın komşu + 2-opt yerel iyileştirme."""
import numpy as np
from .problem import path_length


def random_order(n_holes, seed=0):
    rng = np.random.default_rng(seed)
    order = np.arange(n_holes)
    rng.shuffle(order)
    return order


def nearest_neighbor(dist_matrix, n_holes):
    """Açgözlü en yakın komşu sezgiseli. dist_matrix indeks 0 = origin."""
    unvisited = set(range(1, n_holes + 1))
    current = 0
    order = []
    while unvisited:
        nxt = min(unvisited, key=lambda j: dist_matrix[current, j])
        order.append(nxt - 1)  # delik indeksine çevir (0-based)
        unvisited.remove(nxt)
        current = nxt
    return np.array(order)


def two_opt(order, origin, points, max_iter=500):
    """Nearest-neighbor çıktısını 2-opt ile yerel olarak iyileştirir."""
    order = order.copy()
    best_len = path_length(order, origin, points)
    n = len(order)
    improved = True
    it = 0
    while improved and it < max_iter:
        improved = False
        it += 1
        for i in range(n - 1):
            for j in range(i + 1, n):
                new_order = order.copy()
                new_order[i:j + 1] = order[i:j + 1][::-1]
                new_len = path_length(new_order, origin, points)
                if new_len < best_len - 1e-9:
                    order, best_len = new_order, new_len
                    improved = True
    return order, best_len

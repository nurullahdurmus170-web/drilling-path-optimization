"""Yapay Arı Kolonisi (ABC) - açık tur TSP için uygulama.

Her "besin kaynağı" bir ziyaret sırasıdır. Komşu çözüm, rastgele iki
şehrin yerini değiştirmek (swap) ile üretilir. Bu, sürekli uzayda
tanımlı klasik ABC'nin kombinatoryal problemlere en yaygın
uyarlamalarından biridir.
"""
import numpy as np
from .problem import path_length


def _random_solution(n_holes, rng):
    order = np.arange(n_holes)
    rng.shuffle(order)
    return order


def _neighbor(order, rng):
    new_order = order.copy()
    i, j = rng.choice(len(order), size=2, replace=False)
    new_order[i], new_order[j] = new_order[j], new_order[i]
    return new_order


def run_abc(origin, points, n_bees=20, n_iterations=150, limit=20, seed=0):
    rng = np.random.default_rng(seed)
    n = len(points)

    sources = [_random_solution(n, rng) for _ in range(n_bees)]
    lengths = [path_length(s, origin, points) for s in sources]
    trials = [0] * n_bees

    best_idx = int(np.argmin(lengths))
    best_order, best_len = sources[best_idx].copy(), lengths[best_idx]
    history = []

    for _ in range(n_iterations):
        # 1) Çalışan arı fazı
        for i in range(n_bees):
            candidate = _neighbor(sources[i], rng)
            cand_len = path_length(candidate, origin, points)
            if cand_len < lengths[i]:
                sources[i], lengths[i], trials[i] = candidate, cand_len, 0
            else:
                trials[i] += 1

        # 2) Gözcü arı fazı (daha iyi kaynaklara olasılıksal yönelim)
        fitness = 1.0 / (1.0 + np.array(lengths))
        probs = fitness / fitness.sum()
        for _ in range(n_bees):
            i = rng.choice(n_bees, p=probs)
            candidate = _neighbor(sources[i], rng)
            cand_len = path_length(candidate, origin, points)
            if cand_len < lengths[i]:
                sources[i], lengths[i], trials[i] = candidate, cand_len, 0
            else:
                trials[i] += 1

        # 3) Kaşif arı fazı (tükenen kaynaklar yenileniyor)
        for i in range(n_bees):
            if trials[i] > limit:
                sources[i] = _random_solution(n, rng)
                lengths[i] = path_length(sources[i], origin, points)
                trials[i] = 0

        gen_best = int(np.argmin(lengths))
        if lengths[gen_best] < best_len:
            best_len, best_order = lengths[gen_best], sources[gen_best].copy()
        history.append(best_len)

    return best_order, best_len, history

"""Küçük problem boyutları için kaba kuvvet (brute force) ile kesin optimal
çözüm. n! karmaşıklığı nedeniyle yalnızca küçük n (<= ~10) için kullanılabilir;
burada diğer yöntemlerin optimale olan uzaklığını (optimality gap) ölçmek
amacıyla referans olarak kullanılır.
"""
import itertools
import numpy as np
from .problem import path_length


def brute_force_optimal(origin, points):
    n = len(points)
    best_order, best_len = None, np.inf
    for perm in itertools.permutations(range(n)):
        length = path_length(np.array(perm), origin, points)
        if length < best_len:
            best_len, best_order = length, np.array(perm)
    return best_order, best_len

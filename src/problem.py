"""Sentetik delik delme yolu problemi.

Bir levha üzerinde N adet delik konumu rastgele üretilir. Amaç, tüm
delikleri tek bir başlangıç noktasından (origin) başlayarak ziyaret eden
ve toplam Öklid mesafesini (yaklaşık işleme hareketi süresi) minimize
eden sırayı bulmaktır. Bu, Gezgin Satıcı Problemi'nin (TSP) açık (tur
kapanmayan) bir varyantıdır: CNC tezgahında delme ucu başlangıç
noktasına geri dönmek zorunda değildir.

Not: Bu modül ve depodaki tüm veriler sentetiktir. Gerçek bir parça
geometrisi, tezgah verisi veya firma verisi içermez.
"""
import numpy as np


def generate_holes(n_holes=30, width=200.0, height=150.0, seed=0, origin=(0.0, 0.0)):
    """n_holes adet rastgele delik konumu üretir (mm cinsinden, sentetik)."""
    rng = np.random.default_rng(seed)
    pts = rng.uniform(low=[0, 0], high=[width, height], size=(n_holes, 2))
    origin = np.array(origin, dtype=float)
    return origin, pts


def path_length(order, origin, points):
    """Verilen ziyaret sırası için toplam Öklid yol uzunluğu (açık tur)."""
    seq = np.vstack([origin, points[order]])
    diffs = np.diff(seq, axis=0)
    return float(np.hypot(diffs[:, 0], diffs[:, 1]).sum())


def distance_matrix(origin, points):
    """0. indeks = origin, sonraki indeksler = delikler olacak şekilde
    (n+1) x (n+1) mesafe matrisi döndürür."""
    all_pts = np.vstack([origin[None, :], points])
    diff = all_pts[:, None, :] - all_pts[None, :, :]
    return np.hypot(diff[..., 0], diff[..., 1])

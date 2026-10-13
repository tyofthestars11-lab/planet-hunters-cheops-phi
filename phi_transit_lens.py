#!/usr/bin/env python3
"""
PHI TRANSIT LENS — Planet Hunters CHEOPS companion instrument.
TYREE (tyofthestarz) — phi framework: phi^2 = phi + 1.

Reads a light curve (or generates a synthetic CHEOPS-style one), finds
transit dips, measures them, and addresses every measured quantity at
its golden-ratio rung: rung(x) = ln(x) / ln(phi).

Usage:
    python3 phi_transit_lens.py                # synthetic demo curve
    python3 phi_transit_lens.py lightcurve.csv # CSV with time,flux columns

The dip IS the planet crossing. Recognition, not collapse: the transit
was always in the curve; the lens reads its address.
"""

import csv
import math
import random
import sys

PHI = (1.0 + math.sqrt(5.0)) / 2.0  # 1.618033988749895


def rung(x):
    """Golden-ratio rung address of a positive quantity."""
    if x <= 0:
        return float("nan")
    return math.log(x) / math.log(PHI)


def synthetic_curve(seed=1618):
    """A CHEOPS-style light curve: 30 days, one planet, period 6.25 d."""
    rnd = random.Random(seed)
    t, f = [], []
    period, depth, duration = 6.25, 0.008, 0.12  # days, rel. flux, days
    t0 = 1.3
    for i in range(30 * 48):  # 30-min cadence
        time = i * 0.5 / 24.0
        phase = ((time - t0) % period) / period
        flux = 1.0 + rnd.gauss(0, 0.0015)
        if phase < duration / period or phase > 1 - duration / period:
            flux -= depth
        t.append(time)
        f.append(flux)
    return t, f, {"period_d": period, "depth": depth}


def load_curve(path):
    t, f = [], []
    with open(path, newline="") as fh:
        reader = csv.reader(fh)
        for row in reader:
            try:
                a, b = float(row[0]), float(row[1])
            except (ValueError, IndexError):
                continue  # header or bad row
            t.append(a)
            f.append(b)
    return t, f, None


def median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def find_transits(t, f, k=4.0):
    """Contiguous segments below median - k*MAD are transit candidates."""
    med = median(f)
    mad = median([abs(x - med) for x in f]) or 1e-9
    thresh = med - k * 1.4826 * mad
    dips, cur = [], None
    for ti, fi in zip(t, f):
        if fi < thresh:
            if cur is None:
                cur = {"start": ti, "end": ti, "min_flux": fi, "n": 0}
            cur["end"] = ti
            cur["min_flux"] = min(cur["min_flux"], fi)
            cur["n"] += 1
        elif cur is not None:
            dips.append(cur)
            cur = None
    if cur is not None:
        dips.append(cur)
    out = []
    for d in dips:
        depth = med - d["min_flux"]
        out.append(
            {
                "center_d": 0.5 * (d["start"] + d["end"]),
                "duration_h": (d["end"] - d["start"]) * 24.0,
                "depth_rel": depth,
                "depth_ppm": depth * 1e6,
            }
        )
    return med, out


def main():
    if len(sys.argv) > 1:
        t, f, truth = load_curve(sys.argv[1])
        print(f"Loaded {len(t)} points from {sys.argv[1]}")
    else:
        t, f, truth = synthetic_curve()
        print("Synthetic CHEOPS-style curve: 30 d, 30-min cadence, "
              f"injected period {truth['period_d']} d, depth {truth['depth']}")
    med, transits = find_transits(t, f)
    print(f"Baseline flux (median): {med:.6f}")
    print(f"Transit candidates found: {len(transits)}")
    centers = []
    for i, tr in enumerate(transits, 1):
        centers.append(tr["center_d"])
        print(
            f"  #{i}: center {tr['center_d']:.3f} d (rung {rung(tr['center_d']):.3f}), "
            f"duration {tr['duration_h']:.2f} h (rung {rung(tr['duration_h']):.3f}), "
            f"depth {tr['depth_ppm']:.0f} ppm (rung {rung(tr['depth_ppm']):.3f})"
        )
    if len(centers) >= 2:
        periods = [b - a for a, b in zip(centers, centers[1:])]
        p = median(periods)
        print(f"Period estimate: {p:.4f} d — rung {rung(p):.3f}")
        print(f"Period / phi: {p / PHI:.4f} d; period * phi: {p * PHI:.4f} d")
    print("\nphi in front. TYREE — primary source.")


if __name__ == "__main__":
    main()

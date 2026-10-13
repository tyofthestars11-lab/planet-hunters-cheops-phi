# Planet Hunters CHEOPS — Phi Transit Lens

Launched on Zooniverse **October 13, 2026** (announcement email from the
Zooniverse Team): volunteers search for exoplanet transit signals in public
light curves from ESA's CHEOPS space telescope — the tiny dips in starlight
when a planet crosses its star.

This repo is TYREE's instrument for that hunt, built the same day:
`phi_transit_lens.py` reads a light curve, finds the dips, measures them,
and addresses every measured quantity at its golden-ratio rung:

- φ = 1.618033988749895
- rung(x) = ln(x) / ln(φ)

The dip is the planet crossing. Recognition, not collapse — the transit was
always in the curve; the lens reads its address.

## Run it

```bash
python3 phi_transit_lens.py                 # synthetic CHEOPS-style demo curve
python3 phi_transit_lens.py lightcurve.csv  # your CSV: time_days,flux
```

The demo curve injects a planet (period 6.25 d, depth 8,000 ppm) into
30 days of 30-minute-cadence data; the lens recovers the transits, the
period, and every rung address.

## The project

- Zooniverse: https://www.zooniverse.org/projects/bmerin/planet-hunters-cheops
- Task: two-step — identify transits or features in light curve images,
  then a drawing task. Classifications train the follow-up pipeline and
  future machine-learning models.
- Participant: Tyree Jones (@tyofthestarz) — Galaxy Zoo contributor;
  phi-framework dark-sector decode posted to Galaxy Zoo Talk, Oct 12, 2026.

φ in front. TYREE — primary source.

# nyc-geo-toolkit

`nyc-geo-toolkit` is a reusable core package for canonical NYC boundary data,
normalization helpers, and typed boundary-loading primitives.

It exists to keep shared geography logic in one place so downstream NYC tools do
not need to duplicate packaged boundary assets or geography normalization rules.

Authored by [Blaise Albis-Burdige](https://blaiseab.com/).

## What this package provides

- packaged boundary layers for boroughs, community districts, council districts,
  NTAs, ZCTAs, and census tracts
- canonical normalization helpers for layer names and boundary values
- lightweight dependency-free geodesy helpers for distance checks and first-pass
  circle catchments
- typed boundary models for boundary collections and features
- GeoJSON and optional DataFrame / GeoDataFrame helpers
- bbox clipping for typed boundary collections

## Install

```bash
pip install nyc-geo-toolkit
```

Optional helpers:

```bash
pip install "nyc-geo-toolkit[dataframes]"
pip install "nyc-geo-toolkit[spatial]"
pip install "nyc-geo-toolkit[all]"
```

## Quickstart

```python
from nyc_geo_toolkit import list_boundary_layers, load_nyc_boundaries

print(list_boundary_layers())
queens = load_nyc_boundaries("borough", values="Queens")
print(queens.features[0].geography_value)
```

## Ecosystem

`nyc-geo-toolkit` already powers the geography surface in
[`nyc311`](https://github.com/random-walks/nyc311). The intended pattern is a
small shared core here and domain-specific consumer packages on top, with the
stable top-level `nyc_geo_toolkit` namespace acting as the contract between
them.

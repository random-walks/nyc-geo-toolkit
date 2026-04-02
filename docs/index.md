# nyc-geo-toolkit

`nyc-geo-toolkit` is a lightweight Python package for reusable NYC geography
resources, boundary catalogs, and normalization helpers.

It is designed to support other NYC data tools by making packaged boundary data
and canonical value handling easy to reuse.

Authored by [Blaise Albis-Burdige](https://blaiseab.com/).

## What ships today

- packaged boundary layers for boroughs, community districts, council districts,
  NTAs, ZCTAs, and census tracts
- canonical normalization helpers for layer names and boundary values
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
```

## Quickstart

```python
from nyc_geo_toolkit import list_boundary_layers, load_nyc_boundaries

print(list_boundary_layers())
queens = load_nyc_boundaries("borough", values="Queens")
print(queens.features[0].geography_value)
```

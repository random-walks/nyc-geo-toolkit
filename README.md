# nyc-geo-toolkit

[![Actions Status][actions-badge]][actions-link]
[![Documentation Status][rtd-badge]][rtd-link]
[![PyPI version][pypi-version]][pypi-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

Reusable NYC geography resources, normalization helpers, and boundary loaders
for Python tools.

## What this package provides

`nyc-geo-toolkit` packages canonical NYC boundary layers and the small helper
API needed to discover, normalize, load, subset, and convert them.

The initial release focuses on:

- packaged boundary layers for boroughs, community districts, council districts,
  NTAs, ZCTAs, and census tracts
- canonical normalization helpers for layer names and boundary values
- typed boundary models for boundary collections and features
- GeoJSON and optional DataFrame / GeoDataFrame helpers
- bbox clipping for typed boundary collections

## Install

Base install:

```bash
pip install nyc-geo-toolkit
```

With pandas helpers:

```bash
pip install "nyc-geo-toolkit[dataframes]"
```

With geopandas + shapely helpers:

```bash
pip install "nyc-geo-toolkit[spatial]"
```

With all optional helpers:

```bash
pip install "nyc-geo-toolkit[all]"
```

## Quick example

```python
from nyc_geo_toolkit import load_nyc_boundaries, list_boundary_layers

print(list_boundary_layers())
queens = load_nyc_boundaries("borough", values="Queens")
print(queens.features[0].geography_value)
```

## Public surface

The stable public API centers on:

- `list_boundary_layers()`
- `list_boundary_values()`
- `load_boundaries()`
- `load_nyc_boundaries()`
- `load_nyc_boundaries_geodataframe()`
- `load_nyc_census_tracts()`
- `load_nyc_council_districts()`
- `load_nyc_neighborhood_tabulation_areas()`
- `normalize_boundary_layer()`
- `normalize_boundary_value()`
- `normalize_boundary_values()`
- `boundaries_to_geojson()`
- `boundaries_to_dataframe()`
- `clip_boundaries_to_bbox()`

## Documentation

Docs: [Home](https://nyc-geo-toolkit.readthedocs.io/en/latest/),
[Getting Started](https://nyc-geo-toolkit.readthedocs.io/en/latest/getting-started/),
[API Reference](https://nyc-geo-toolkit.readthedocs.io/en/latest/api/),
[Architecture](https://nyc-geo-toolkit.readthedocs.io/en/latest/architecture/),
[Contributing](https://nyc-geo-toolkit.readthedocs.io/en/latest/contributing/)

## License

MIT.

<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/random-walks/nyc-geo-toolkit/actions/workflows/ci.yml/badge.svg
[actions-link]:             https://github.com/random-walks/nyc-geo-toolkit/actions
[pypi-link]:                https://pypi.org/project/nyc-geo-toolkit/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/nyc-geo-toolkit
[pypi-version]:             https://img.shields.io/pypi/v/nyc-geo-toolkit
[rtd-badge]:                https://readthedocs.org/projects/nyc-geo-toolkit/badge/?version=latest
[rtd-link]:                 https://nyc-geo-toolkit.readthedocs.io/en/latest/?badge=latest
<!-- prettier-ignore-end -->

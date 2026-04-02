# Getting Started

This guide shows the fastest path to using `nyc-geo-toolkit` in a script or
notebook.

## Install

```bash
pip install nyc-geo-toolkit
```

Optional extras:

```bash
pip install "nyc-geo-toolkit[dataframes]"
pip install "nyc-geo-toolkit[spatial]"
```

## List supported boundary layers

```python
from nyc_geo_toolkit import list_boundary_layers

print(list_boundary_layers())
```

## Load one packaged layer

```python
from nyc_geo_toolkit import load_nyc_boundaries

boroughs = load_nyc_boundaries("borough")
queens = load_nyc_boundaries("borough", values="Queens")
```

## Normalize user input

```python
from nyc_geo_toolkit import normalize_boundary_layer, normalize_boundary_value

normalize_boundary_layer("zip code")
normalize_boundary_value("community_district", "01 Brooklyn")
```

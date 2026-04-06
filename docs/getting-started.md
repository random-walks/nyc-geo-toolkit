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
pip install "nyc-geo-toolkit[all]"
```

## List supported boundary layers

```python
from nyc_geo_toolkit import list_boundary_layers

print(list_boundary_layers())
```

## Inspect canonical values for one layer

```python
from nyc_geo_toolkit import list_boundary_values

print(list_boundary_values("borough"))
```

## Load one packaged layer

```python
from nyc_geo_toolkit import load_nyc_boundaries

boroughs = load_nyc_boundaries("borough")
queens = load_nyc_boundaries("borough", values="Queens")
```

## Normalize user input

```python
from nyc_geo_toolkit import (
    normalize_boundary_layer,
    normalize_boundary_value,
    normalize_boundary_values,
)

normalize_boundary_layer("zip code")
normalize_boundary_value("community_district", "01 Brooklyn")
normalize_boundary_values("borough", ["Queens", "bk"])
```

## Convert boundaries to GeoJSON

```python
from nyc_geo_toolkit import boundaries_to_geojson, load_nyc_boundaries

payload = boundaries_to_geojson(
    load_nyc_boundaries("borough", values=("Queens", "Brooklyn"))
)
print(payload["type"])
print(len(payload["features"]))
```

## Use the lightweight geodesy helpers

```python
from nyc_geo_toolkit import (
    build_circle_polygon,
    haversine_distance_meters,
    walk_radius_meters,
)

radius = walk_radius_meters(10)
distance = haversine_distance_meters(40.7061, -74.0086, 40.7580, -73.9855)
polygon = build_circle_polygon(40.7128, -74.0060, radius)
print(radius, round(distance), len(polygon))
```

## Clip a layer to a bounding box

`clip_boundaries_to_bbox()` requires the spatial stack, so install
`nyc-geo-toolkit[spatial]` or `nyc-geo-toolkit[all]` first.

```python
from nyc_geo_toolkit import clip_boundaries_to_bbox, load_nyc_boundaries

clipped = clip_boundaries_to_bbox(
    load_nyc_boundaries("borough"),
    min_longitude=-73.97,
    min_latitude=40.68,
    max_longitude=-73.84,
    max_latitude=40.81,
)
print([feature.geography_value for feature in clipped.features])
```

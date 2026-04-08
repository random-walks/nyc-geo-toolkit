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

## Plot a boundary layer

With the `spatial` extra installed, you can plot any boundary layer directly:

```python
from nyc_geo_toolkit import (
    add_osm_basemap,
    load_nyc_boundaries_geodataframe,
    to_web_mercator,
)

gdf = to_web_mercator(load_nyc_boundaries_geodataframe("borough"))
ax = gdf.plot(figsize=(8, 8), edgecolor="white", alpha=0.7, column="geography_value")
add_osm_basemap(ax)
```

See the [Examples](examples.md) page for a full multi-panel showcase of every
boundary layer and spatial helper.

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

## Use the optional basemap helpers

These helpers require the `spatial` extra:
`pip install "nyc-geo-toolkit[spatial]"`.

```python
from nyc_geo_toolkit import bbox_around, to_web_mercator

# Get a WGS84 bounding box (500 m radius) around a point
minx, miny, maxx, maxy = bbox_around((-73.98, 40.75), 500.0)
print(minx, miny, maxx, maxy)
```

```python
import geopandas as gpd
from shapely.geometry import Point

from nyc_geo_toolkit import to_web_mercator

gdf = gpd.GeoDataFrame(geometry=[Point(-73.98, 40.75)], crs="EPSG:4326")
wm = to_web_mercator(gdf)
print(wm.crs)
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

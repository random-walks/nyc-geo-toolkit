# nyc-geo-toolkit

[![Actions Status][actions-badge]][actions-link]
[![Documentation Status][rtd-badge]][rtd-link]
[![PyPI version][pypi-version]][pypi-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

![nyc-geo-toolkit cover figure](docs/assets/images/generated/nyc-geo-toolkit-cover.png)

Reusable NYC geography resources, normalization helpers, and boundary loaders
for Python tools.

Authored by [Blaise Albis-Burdige](https://blaiseab.com/).

## Why this exists

Every NYC data project needs borough boundaries, ZIP lookups, and district
normalization. `nyc-geo-toolkit` ships canonical boundary GeoJSON and a stable
Python API so downstream tools don't duplicate that work. Install the base
package for zero-dependency boundary loading, or add optional extras for pandas,
geopandas, and basemap helpers.

## What this package provides

- **Packaged boundary layers** for boroughs, community districts, council
    districts, NTAs, ZCTAs, and census tracts -- no runtime network dependency
- **Normalization helpers** that turn messy user input (`"bk"`, `"01 Brooklyn"`,
    `"zip code"`) into canonical values
- **Geodesy helpers** for great-circle distance, walk-radius circles, and
    bounding boxes -- dependency-free
- **Typed models** (`BoundaryCollection`, `BoundaryFeature`) for safe,
    inspectable boundary data
- **GeoJSON, DataFrame, and GeoDataFrame conversion** with optional pandas and
    geopandas extras
- **Basemap and spatial helpers** for Web Mercator reprojection, OSM tile
    overlays, and bbox clipping

## Ecosystem

`nyc-geo-toolkit` is the shared geography core for a family of NYC data
packages:

| Package                                                          | Description                                  |
| ---------------------------------------------------------------- | -------------------------------------------- |
| [`nyc311`](https://github.com/random-walks/nyc311)               | 311 service request analysis and aggregation |
| [`subway-access`](https://github.com/random-walks/subway-access) | Subway accessibility and coverage analysis   |
| [`nyc-mesh`](https://github.com/random-walks/nyc-mesh)           | Community mesh network coverage analysis     |

All three depend on the stable `nyc_geo_toolkit` namespace for boundary data,
normalization, and spatial primitives.

## Install

```bash
pip install nyc-geo-toolkit              # zero-dependency base
pip install "nyc-geo-toolkit[dataframes]" # + pandas helpers
pip install "nyc-geo-toolkit[spatial]"    # + geopandas, shapely, contextily
pip install "nyc-geo-toolkit[all]"        # everything
```

## Quick start

### Load and inspect boundaries

```python
from nyc_geo_toolkit import list_boundary_layers, load_nyc_boundaries

print(list_boundary_layers())
# ('borough', 'community_district', 'council_district', ...)

queens = load_nyc_boundaries("borough", values="Queens")
print(queens.features[0].geography_value)  # "QUEENS"
```

### Normalize messy input

```python
from nyc_geo_toolkit import normalize_borough_name, normalize_boundary_value

normalize_borough_name("bk")  # "BROOKLYN"
normalize_boundary_value("community_district", "01 Brooklyn")  # "BROOKLYN 01"
```

### Plot a boundary layer

```python
from nyc_geo_toolkit import (
    load_nyc_boundaries_geodataframe,
    to_web_mercator,
    add_osm_basemap,
)

gdf = to_web_mercator(load_nyc_boundaries_geodataframe("borough"))
ax = gdf.plot(figsize=(8, 8), edgecolor="white", alpha=0.7, column="geography_value")
add_osm_basemap(ax)
```

### Use geodesy helpers

```python
from nyc_geo_toolkit import (
    haversine_distance_meters,
    walk_radius_meters,
    build_circle_polygon,
)

walk_radius_meters(10)  # 800.0 meters
haversine_distance_meters(40.7580, -73.9855, 40.7128, -74.006)  # ~5.2 km
polygon = build_circle_polygon(40.7128, -74.006, 800)  # 24-sided circle
```

## API overview

| Category                | Key functions                                                                                                         |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **Discovery & loading** | `list_boundary_layers()`, `list_boundary_values()`, `load_nyc_boundaries()`, `load_nyc_boundaries_geodataframe()`     |
| **Normalization**       | `normalize_borough_name()`, `normalize_boundary_layer()`, `normalize_boundary_value()`, `normalize_boundary_values()` |
| **Geodesy**             | `haversine_distance_meters()`, `walk_radius_meters()`, `build_circle_polygon()`                                       |
| **Spatial helpers**     | `add_osm_basemap()`, `to_web_mercator()`, `bbox_around()`, `clip_boundaries_to_bbox()`                                |
| **Conversion**          | `boundaries_to_geojson()`, `boundaries_to_dataframe()`                                                                |
| **Models & constants**  | `BoundaryCollection`, `BoundaryFeature`, `BoundaryLayerSpec`, `BOROUGH_*`, `SUPPORTED_BOROUGHS`                       |

Full reference: [API docs](https://nyc-geo-toolkit.readthedocs.io/en/latest/api/)

## Examples

The repo ships self-contained examples under `examples/`:

- [`examples/about-the-data/`](examples/about-the-data/) -- kitchen-sink
    visualization of every boundary layer and spatial helper (generates the cover
    figure above)
- [`examples/boundary-quickstart/`](examples/boundary-quickstart/) -- basic
    boundary loading and GeoJSON export
- [`examples/normalization-demo/`](examples/normalization-demo/) -- input
    normalization showcase
- [`examples/boundary-explorer-tearsheet/`](examples/boundary-explorer-tearsheet/)
    -- interop showcase with
    [factor-factory](https://github.com/random-walks/factor-factory) and
    [jellycell](https://github.com/random-walks/jellycell): loads community
    districts, fits a synthetic DiD, and renders a jellycell findings tearsheet
    (the canonical pattern downstream packages can copy)

## Documentation

[Home](https://nyc-geo-toolkit.readthedocs.io/en/latest/) |
[Getting Started](https://nyc-geo-toolkit.readthedocs.io/en/latest/getting-started/) |
[Examples](https://nyc-geo-toolkit.readthedocs.io/en/latest/examples/) |
[API Reference](https://nyc-geo-toolkit.readthedocs.io/en/latest/api/) |
[Architecture](https://nyc-geo-toolkit.readthedocs.io/en/latest/architecture/)

## License

MIT.

<!-- prettier-ignore-start -->

<!-- prettier-ignore-end -->

[actions-badge]: https://github.com/random-walks/nyc-geo-toolkit/actions/workflows/ci.yml/badge.svg
[actions-link]: https://github.com/random-walks/nyc-geo-toolkit/actions
[pypi-link]: https://pypi.org/project/nyc-geo-toolkit/
[pypi-platforms]: https://img.shields.io/pypi/pyversions/nyc-geo-toolkit
[pypi-version]: https://img.shields.io/pypi/v/nyc-geo-toolkit
[rtd-badge]: https://readthedocs.org/projects/nyc-geo-toolkit/badge/?version=latest
[rtd-link]: https://nyc-geo-toolkit.readthedocs.io/en/latest/?badge=latest

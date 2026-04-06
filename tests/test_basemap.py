"""Tests for optional basemap helpers."""

from __future__ import annotations

from importlib import import_module

import pytest

pytest.importorskip(
    "geopandas",
    reason="Install nyc-geo-toolkit[spatial] to run basemap tests.",
)
pytest.importorskip(
    "contextily",
    reason="Install nyc-geo-toolkit[spatial] to run basemap tests.",
)

from nyc_geo_toolkit import bbox_around, to_web_mercator

pytestmark = pytest.mark.optional


def test_to_web_mercator_roundtrip_dims() -> None:
    gpd = import_module("geopandas")
    shapely_geometry = import_module("shapely.geometry")
    point_cls = shapely_geometry.Point
    gdf = gpd.GeoDataFrame(geometry=[point_cls(-73.98, 40.75)], crs="EPSG:4326")
    wm = to_web_mercator(gdf)
    assert wm.crs.to_epsg() == 3857
    assert not wm.empty


def test_bbox_around_contains_point() -> None:
    lon, lat = -73.98, 40.75
    minx, miny, maxx, maxy = bbox_around((lon, lat), 500.0)
    assert minx < lon < maxx
    assert miny < lat < maxy

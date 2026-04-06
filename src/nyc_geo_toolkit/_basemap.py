"""Optional map styling helpers (contextily + geopandas)."""

from __future__ import annotations

from importlib import import_module
from typing import Any


def add_osm_basemap(axes: Any, *, provider: Any | None = None) -> None:
    """Add a CartoDB Positron basemap (or ``provider``) in Web Mercator."""
    ctx = import_module("contextily")
    source = provider if provider is not None else ctx.providers.CartoDB.Positron
    ctx.add_basemap(axes, source=source, attribution_size=6)


def to_web_mercator(geodataframe: Any) -> Any:
    """Return a copy reprojected to EPSG:3857 (Web Mercator)."""
    return geodataframe.to_crs(epsg=3857)


def bbox_around(
    point: tuple[float, float], meters: float
) -> tuple[float, float, float, float]:
    """Return ``(minx, miny, maxx, maxy)`` in EPSG:4326 around ``point`` (lon, lat).

    The bounds are the axis-aligned envelope of a circle of radius ``meters`` (in
    real-world meters) in Web Mercator, then reprojected to WGS84.
    """
    if meters <= 0:
        raise ValueError("meters must be positive.")

    gpd = import_module("geopandas")
    shapely_geometry = import_module("shapely.geometry")
    point_cls = shapely_geometry.Point
    box_cls = shapely_geometry.box

    gdf = gpd.GeoDataFrame(geometry=[point_cls(point[0], point[1])], crs="EPSG:4326")
    g3857 = gdf.to_crs(epsg=3857)
    buffered = g3857.buffer(meters)
    minx, miny, maxx, maxy = buffered.total_bounds
    envelope = gpd.GeoDataFrame(
        geometry=[box_cls(minx, miny, maxx, maxy)], crs="EPSG:3857"
    )
    out = envelope.to_crs(epsg=4326)
    tb = out.total_bounds
    return (float(tb[0]), float(tb[1]), float(tb[2]), float(tb[3]))

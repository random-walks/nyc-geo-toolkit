"""Optional map styling helpers (contextily + geopandas)."""

from __future__ import annotations

from importlib import import_module
from typing import Any


def add_osm_basemap(axes: Any, *, provider: Any | None = None) -> None:
    """Add a basemap to a matplotlib axes in Web Mercator projection.

    Defaults to CartoDB Positron tiles.  Requires the ``spatial`` extra
    (``pip install nyc-geo-toolkit[spatial]``).

    Args:
        axes: A matplotlib ``Axes`` object (must already be in EPSG:3857).
        provider: An optional contextily tile provider.  Defaults to
            ``CartoDB.Positron``.

    Raises:
        ImportError: If contextily is not installed.
    """
    ctx = import_module("contextily")
    source = provider if provider is not None else ctx.providers.CartoDB.Positron
    ctx.add_basemap(axes, source=source, attribution_size=6)


def to_web_mercator(geodataframe: Any) -> Any:
    """Return a copy of a GeoDataFrame reprojected to EPSG:3857 (Web Mercator).

    Args:
        geodataframe: A geopandas ``GeoDataFrame`` in any CRS.

    Returns:
        A new ``GeoDataFrame`` in EPSG:3857.
    """
    return geodataframe.to_crs(epsg=3857)


def bbox_around(
    point: tuple[float, float], meters: float
) -> tuple[float, float, float, float]:
    """Return a WGS84 bounding box around a point.

    Computes the axis-aligned envelope of a circle with radius *meters*
    in Web Mercator, then reprojects to EPSG:4326.

    Requires the ``spatial`` extra
    (``pip install nyc-geo-toolkit[spatial]``).

    Args:
        point: ``(longitude, latitude)`` in decimal degrees.
        meters: Buffer radius in real-world meters (must be positive).

    Returns:
        ``(min_longitude, min_latitude, max_longitude, max_latitude)`` in
        EPSG:4326.

    Raises:
        ImportError: If geopandas or shapely is not installed.
        ValueError: If *meters* is not positive.
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

"""Boundary operations built on top of packaged NYC geography layers."""

from __future__ import annotations

from importlib import import_module
from typing import Any

from ._models import BoundaryCollection, BoundaryFeature


def _require_shapely() -> Any:
    try:
        return import_module("shapely.geometry")
    except ImportError as exc:
        raise ImportError(
            "shapely is required for nyc_geo_toolkit clipping helpers. Install it with `pip install nyc-geo-toolkit[spatial]` or `pip install shapely`."
        ) from exc


def clip_boundaries_to_bbox(
    boundaries: BoundaryCollection,
    *,
    min_longitude: float,
    min_latitude: float,
    max_longitude: float,
    max_latitude: float,
) -> BoundaryCollection:
    """Clip boundary features to an axis-aligned bounding box.

    Features that do not intersect the bounding box are dropped.
    Features that partially overlap are clipped to the box.
    Requires the ``spatial`` extra (``pip install nyc-geo-toolkit[spatial]``).

    Args:
        boundaries: A ``BoundaryCollection`` to clip.
        min_longitude: Western edge (WGS84 degrees).
        min_latitude: Southern edge (WGS84 degrees).
        max_longitude: Eastern edge (WGS84 degrees).
        max_latitude: Northern edge (WGS84 degrees).

    Returns:
        A new ``BoundaryCollection`` containing only the clipped features.

    Raises:
        ImportError: If shapely is not installed.
        ValueError: If the bounding box is degenerate or no features intersect.
    """
    if min_longitude >= max_longitude or min_latitude >= max_latitude:
        raise ValueError("Bounding boxes must satisfy min < max on both axes.")
    shapely_geometry = _require_shapely()
    clip_box = shapely_geometry.box(
        min_longitude,
        min_latitude,
        max_longitude,
        max_latitude,
    )
    clipped_features: list[BoundaryFeature] = []
    for feature in boundaries.features:
        geometry = shapely_geometry.shape(feature.geometry)
        clipped_geometry = geometry.intersection(clip_box)
        if clipped_geometry.is_empty:
            continue
        clipped_features.append(
            BoundaryFeature(
                geography=feature.geography,
                geography_value=feature.geography_value,
                geometry=shapely_geometry.mapping(clipped_geometry),
                properties=dict(feature.properties),
            )
        )
    if not clipped_features:
        raise ValueError("No boundaries intersect the requested bounding box.")
    return BoundaryCollection(
        geography=boundaries.geography,
        features=tuple(clipped_features),
        vintage=boundaries.vintage,
    )

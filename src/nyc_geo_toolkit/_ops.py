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
        geography=boundaries.geography, features=tuple(clipped_features)
    )

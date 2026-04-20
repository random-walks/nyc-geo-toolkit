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


def centroids_from_boundaries(
    boundaries: BoundaryCollection,
    *,
    representative: bool = False,
) -> BoundaryCollection:
    """Compute per-feature centroids as a Point ``BoundaryCollection``.

    For every polygon or multi-polygon feature in ``boundaries``, returns a
    GeoJSON ``Point`` geometry at either the geometric centroid (default) or
    the shapely ``representative_point`` (guaranteed to fall inside the
    polygon, useful for non-convex shapes like community districts with
    concave shorelines). Feature identity — ``geography``, ``geography_value``,
    and ``properties`` — round-trips verbatim, so the returned collection
    can be fed back through :func:`boundaries_to_geojson` or
    :func:`boundaries_to_dataframe`.

    Requires the ``spatial`` extra (``pip install nyc-geo-toolkit[spatial]``).

    Args:
        boundaries: A ``BoundaryCollection`` of polygon / multipolygon features.
        representative: When ``True``, use ``shapely.Geometry.representative_point``
            (always inside the polygon). When ``False`` (default), use the
            geometric centroid, which may fall outside for non-convex shapes.

    Returns:
        A new ``BoundaryCollection`` where each feature's ``geometry`` is a
        GeoJSON ``Point``. The collection's ``geography`` and ``vintage`` are
        preserved.

    Raises:
        ImportError: If shapely is not installed.
        ValueError: If ``boundaries`` is empty (enforced by
            ``BoundaryCollection``'s own invariant) or contains a feature
            whose geometry is empty after centroid projection.

    Example:
        >>> from nyc_geo_toolkit import (
        ...     centroids_from_boundaries,
        ...     load_nyc_boundaries,
        ... )
        >>> cds = load_nyc_boundaries("community_district")
        >>> points = centroids_from_boundaries(cds)
        >>> points.features[0].geometry["type"]
        'Point'
    """
    shapely_geometry = _require_shapely()
    point_features: list[BoundaryFeature] = []
    for feature in boundaries.features:
        geometry = shapely_geometry.shape(feature.geometry)
        point = geometry.representative_point() if representative else geometry.centroid
        if point.is_empty:
            raise ValueError(
                f"Centroid for feature {feature.geography_value!r} is empty; "
                "the source geometry may be degenerate."
            )
        point_features.append(
            BoundaryFeature(
                geography=feature.geography,
                geography_value=feature.geography_value,
                geometry=shapely_geometry.mapping(point),
                properties=dict(feature.properties),
            )
        )
    return BoundaryCollection(
        geography=boundaries.geography,
        features=tuple(point_features),
        vintage=boundaries.vintage,
    )


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

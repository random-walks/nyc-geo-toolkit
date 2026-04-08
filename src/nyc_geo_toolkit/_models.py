"""Typed models for packaged NYC geography resources."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ._constants import SUPPORTED_BOUNDARY_GEOGRAPHIES
from ._normalize import _normalize_space, normalize_boundary_layer


@dataclass(frozen=True)
class BoundaryLayerSpec:
    """Metadata describing one packaged NYC boundary layer.

    Attributes:
        layer: Canonical layer name (e.g. ``"census_tract"``).
        display_name: Human-readable label for the layer.
        resource_path: Package-relative path to the GeoJSON file.
        vintage: Year this boundary data represents (e.g. ``2020``, ``2010``).
        source_name: Name of the data source organization.
        source_url: URL to the source data page.
        feature_count: Expected number of features in the layer.
    """

    layer: str
    display_name: str
    resource_path: str
    vintage: int = 2020
    source_name: str = ""
    source_url: str = ""
    feature_count: int = 0


@dataclass(frozen=True)
class BoundaryFeature:
    """A single boundary feature with canonical geography metadata.

    Attributes:
        geography: Canonical layer name (e.g. ``"borough"``).
        geography_value: Canonical identifier for this feature
            (e.g. ``"MANHATTAN"``, ``"BROOKLYN 01"``, ``"10001"``).
        geometry: GeoJSON geometry object (``Polygon`` or ``MultiPolygon``).
        properties: Additional properties from the source data, excluding
            ``geography`` and ``geography_value`` which are promoted to
            top-level fields.
    """

    geography: str
    geography_value: str
    geometry: dict[str, Any]
    properties: dict[str, Any]

    def __post_init__(self) -> None:
        normalized_geography = normalize_boundary_layer(self.geography)
        normalized_value = _normalize_space(self.geography_value)
        if not normalized_value:
            raise ValueError("geography_value must not be empty.")
        if not isinstance(self.geometry, dict):
            raise ValueError("geometry must be a GeoJSON object.")
        if not isinstance(self.properties, dict):
            raise ValueError("properties must be a mapping.")
        object.__setattr__(self, "geography", normalized_geography)
        object.__setattr__(self, "geography_value", normalized_value)


@dataclass(frozen=True)
class BoundaryCollection:
    """A collection of boundary features for one geography type and vintage.

    Attributes:
        geography: Canonical layer name shared by all features.
        features: Tuple of ``BoundaryFeature`` objects.
        vintage: Year the boundary data represents.
    """

    geography: str
    features: tuple[BoundaryFeature, ...]
    vintage: int = 2020

    def __post_init__(self) -> None:
        normalized_geography = normalize_boundary_layer(self.geography)
        if not self.features:
            raise ValueError("features must not be empty.")
        if normalized_geography not in SUPPORTED_BOUNDARY_GEOGRAPHIES:
            raise ValueError(f"Unsupported boundary geography {self.geography!r}.")
        for feature in self.features:
            if feature.geography != normalized_geography:
                raise ValueError(
                    "All boundary features in a collection must share the same geography."
                )
        object.__setattr__(self, "geography", normalized_geography)

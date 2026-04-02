"""Typed models for packaged NYC geography resources."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ._constants import SUPPORTED_BOUNDARY_GEOGRAPHIES
from ._normalize import _normalize_space, normalize_boundary_layer


@dataclass(frozen=True)
class BoundaryLayerSpec:
    """Metadata describing one packaged NYC boundary layer."""

    layer: str
    display_name: str
    resource_path: str


@dataclass(frozen=True)
class BoundaryFeature:
    """A supported boundary feature with canonical geography metadata."""

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
    """Boundary features for one supported geography type."""

    geography: str
    features: tuple[BoundaryFeature, ...]

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

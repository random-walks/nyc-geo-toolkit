"""Helpers for accessing packaged NYC geography resources."""

from __future__ import annotations

import json
from importlib.resources import files
from typing import Any

from ._catalog import (
    BOUNDARY_LAYER_LOOKUP,
    DEFAULT_LAYER_VINTAGES,
    VINTAGE_LOOKUP,
)
from ._normalize import normalize_boundary_layer

_RESOURCE_ROOT = files("nyc_geo_toolkit")


def load_boundary_payload(layer: str, vintage: int | None = None) -> dict[str, Any]:
    normalized_layer = normalize_boundary_layer(layer)
    resolved_vintage = (
        vintage if vintage is not None else DEFAULT_LAYER_VINTAGES[normalized_layer]
    )
    key = (normalized_layer, resolved_vintage)
    if key in VINTAGE_LOOKUP:
        spec = VINTAGE_LOOKUP[key]
    elif vintage is None:
        spec = BOUNDARY_LAYER_LOOKUP[normalized_layer]
    else:
        available = sorted(v for (lyr, v) in VINTAGE_LOOKUP if lyr == normalized_layer)
        raise ValueError(
            f"No {normalized_layer!r} boundary data for vintage {vintage}. "
            f"Available vintages: {available}."
        )
    payload = json.loads(
        _RESOURCE_ROOT.joinpath(spec.resource_path).read_text(encoding="utf-8")
    )
    if not isinstance(payload, dict):
        raise ValueError("Packaged boundary payload must be a GeoJSON object.")
    return payload

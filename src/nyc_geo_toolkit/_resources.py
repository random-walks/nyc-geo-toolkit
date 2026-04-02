"""Helpers for accessing packaged NYC geography resources."""

from __future__ import annotations

import json
from importlib.resources import files
from typing import Any

from ._catalog import BOUNDARY_LAYER_LOOKUP
from ._normalize import normalize_boundary_layer

_RESOURCE_ROOT = files("nyc_geo_toolkit")


def load_boundary_payload(layer: str) -> dict[str, Any]:
    normalized_layer = normalize_boundary_layer(layer)
    spec = BOUNDARY_LAYER_LOOKUP[normalized_layer]
    payload = json.loads(
        _RESOURCE_ROOT.joinpath(spec.resource_path).read_text(encoding="utf-8")
    )
    if not isinstance(payload, dict):
        raise ValueError("Packaged boundary payload must be a GeoJSON object.")
    return payload

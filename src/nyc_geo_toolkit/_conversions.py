"""Conversions for typed boundary collections."""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any

from ._models import BoundaryCollection

if TYPE_CHECKING:
    import pandas as pd  # type: ignore[import-untyped]


def _require_pandas() -> Any:
    try:
        return import_module("pandas")
    except ImportError as exc:
        raise ImportError(
            "pandas is required for nyc_geo_toolkit dataframe helpers. Install it with `pip install nyc-geo-toolkit[dataframes]` or `pip install pandas`."
        ) from exc


def boundaries_to_geojson(boundaries: BoundaryCollection) -> dict[str, object]:
    """Convert a ``BoundaryCollection`` to a GeoJSON ``FeatureCollection`` dict.

    Each feature includes ``geography`` and ``geography_value`` in its
    properties alongside any additional source properties.

    Args:
        boundaries: A typed boundary collection.

    Returns:
        A GeoJSON-compatible dict with ``type`` and ``features`` keys.
    """
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "geography": feature.geography,
                    "geography_value": feature.geography_value,
                    **feature.properties,
                },
                "geometry": feature.geometry,
            }
            for feature in boundaries.features
        ],
    }


def boundaries_to_dataframe(boundaries: BoundaryCollection) -> pd.DataFrame:
    """Convert a ``BoundaryCollection`` to a pandas ``DataFrame``.

    Requires the ``dataframes`` extra
    (``pip install nyc-geo-toolkit[dataframes]``).

    Columns include ``geography``, ``geography_value``, ``geometry``
    (as a raw GeoJSON dict), and any additional source properties.

    Args:
        boundaries: A typed boundary collection.

    Returns:
        A ``DataFrame`` with one row per feature.

    Raises:
        ImportError: If pandas is not installed.
    """
    pd = _require_pandas()
    return pd.DataFrame.from_records(
        [
            {
                "geography": feature.geography,
                "geography_value": feature.geography_value,
                **feature.properties,
                "geometry": feature.geometry,
            }
            for feature in boundaries.features
        ]
    )

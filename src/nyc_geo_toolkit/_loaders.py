"""Library-owned loaders for packaged NYC boundary resources."""

from __future__ import annotations

from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING, Any

from ._catalog import (
    AVAILABLE_VINTAGES,
    BOUNDARY_LAYER_CATALOG,
    CENSUS_DECADE_VINTAGE_MAP,
    DEFAULT_LAYER_VINTAGES,
    VINTAGE_LOOKUP,
)
from ._geojson import boundary_collection_from_geojson, load_boundary_collection
from ._models import BoundaryCollection, BoundaryLayerSpec
from ._normalize import normalize_boundary_layer, normalize_boundary_values
from ._resources import load_boundary_payload

if TYPE_CHECKING:
    import geopandas as gpd  # type: ignore[import-untyped]


def _require_geospatial_stack() -> tuple[Any, Any]:
    try:
        geopandas = import_module("geopandas")
        shapely_geometry = import_module("shapely.geometry")
    except ImportError as exc:
        raise ImportError(
            "geopandas and shapely are required for nyc_geo_toolkit spatial helpers. Install them with `pip install nyc-geo-toolkit[spatial]` or `pip install geopandas shapely`."
        ) from exc
    return geopandas, shapely_geometry


def _boundary_collection_to_geodataframe(
    boundaries: BoundaryCollection,
) -> gpd.GeoDataFrame:
    geopandas, shapely_geometry = _require_geospatial_stack()
    rows = [
        {
            "geography": feature.geography,
            "geography_value": feature.geography_value,
            **feature.properties,
            "geometry": shapely_geometry.shape(feature.geometry),
        }
        for feature in boundaries.features
    ]
    return geopandas.GeoDataFrame(rows, geometry="geometry", crs="EPSG:4326")


def _resolve_vintage(layer: str, vintage: int | None) -> int:
    if vintage is not None:
        return vintage
    return DEFAULT_LAYER_VINTAGES.get(layer, 2020)


def list_boundary_layers() -> tuple[str, ...]:
    """Return the names of all available boundary layers.

    Returns:
        Layer names in catalog order (e.g. ``("borough", "community_district", ...)``).

    Example:
        >>> list_boundary_layers()
        ('borough', 'community_district', 'council_district', ...)
    """
    return tuple(spec.layer for spec in BOUNDARY_LAYER_CATALOG)


def list_boundary_values(
    layer: str,
    *,
    vintage: int | None = None,
) -> tuple[str, ...]:
    """Return the canonical values for a boundary layer.

    Args:
        layer: Boundary layer name or alias (e.g. ``"borough"``, ``"zip"``).
        vintage: Optional vintage year.  Defaults to the layer's default vintage.

    Returns:
        Canonical value strings for every feature in the layer.

    Raises:
        ValueError: If the layer name is unsupported.
    """
    normalized_layer = normalize_boundary_layer(layer)
    boundaries = load_nyc_boundaries(normalized_layer, vintage=vintage)
    return tuple(feature.geography_value for feature in boundaries.features)


def list_available_vintages(
    layer: str | None = None,
) -> dict[str, tuple[int, ...]] | tuple[int, ...]:
    """Return available vintage years for boundary layers.

    Args:
        layer: A specific layer name or alias.  When ``None``, returns a dict
            mapping every layer to its available vintages.

    Returns:
        A tuple of vintage years when *layer* is given, or a dict mapping
        layer names to vintage tuples when *layer* is ``None``.

    Raises:
        ValueError: If the layer name is unsupported.

    Example:
        >>> list_available_vintages("census_tract")
        (2000, 2010, 2020)
        >>> list_available_vintages()
        {'borough': (2020,), 'census_tract': (2000, 2010, 2020), ...}
    """
    if layer is None:
        return dict(AVAILABLE_VINTAGES)
    normalized_layer = normalize_boundary_layer(layer)
    if normalized_layer not in AVAILABLE_VINTAGES:
        raise ValueError(f"No vintage data available for layer {layer!r}.")
    return AVAILABLE_VINTAGES[normalized_layer]


def describe_layer(
    layer: str,
    *,
    vintage: int | None = None,
) -> BoundaryLayerSpec:
    """Return metadata about a boundary layer including provenance.

    Args:
        layer: Boundary layer name or alias.
        vintage: Optional vintage year. Defaults to the layer's default vintage.

    Returns:
        A ``BoundaryLayerSpec`` with source name, URL, vintage, and feature count.

    Raises:
        ValueError: If the layer or vintage is unsupported.

    Example:
        >>> spec = describe_layer("census_tract", vintage=2010)
        >>> spec.source_name
        'US Census Bureau TIGER/Line'
    """
    normalized_layer = normalize_boundary_layer(layer)
    resolved_vintage = _resolve_vintage(normalized_layer, vintage)
    key = (normalized_layer, resolved_vintage)
    if key not in VINTAGE_LOOKUP:
        available = AVAILABLE_VINTAGES.get(normalized_layer, ())
        raise ValueError(
            f"No {normalized_layer!r} boundary data for vintage {resolved_vintage}. "
            f"Available vintages: {sorted(available)}."
        )
    return VINTAGE_LOOKUP[key]


def vintage_for_census_decade(layer: str, decade: int) -> int:
    """Return the actual vintage year for a layer given a census decade.

    Most layers align directly with census decades (2000, 2010, 2020), but
    some use different years.  For example, council districts are redistricted
    in 2013 and 2023 rather than 2010 and 2020.

    Args:
        layer: Boundary layer name or alias.
        decade: A census decade year (``2000``, ``2010``, or ``2020``).

    Returns:
        The vintage year that corresponds to the requested decade.

    Raises:
        ValueError: If the layer or decade has no mapping.

    Example:
        >>> vintage_for_census_decade("council_district", 2020)
        2023
    """
    normalized_layer = normalize_boundary_layer(layer)
    key = (normalized_layer, decade)
    if key not in CENSUS_DECADE_VINTAGE_MAP:
        available_decades = sorted(
            d for (lyr, d) in CENSUS_DECADE_VINTAGE_MAP if lyr == normalized_layer
        )
        raise ValueError(
            f"No census decade mapping for {normalized_layer!r} and decade {decade}. "
            f"Available decades: {available_decades}."
        )
    return CENSUS_DECADE_VINTAGE_MAP[key]


def load_nyc_boundaries(
    layer: str = "community_district",
    *,
    values: str | tuple[str, ...] | list[str] | None = None,
    vintage: int | None = None,
) -> BoundaryCollection:
    """Load packaged NYC boundary features for a given geography layer.

    Returns a typed ``BoundaryCollection`` containing all features for the
    requested layer, optionally filtered to specific values.

    Args:
        layer: Boundary layer name. One of ``"borough"``, ``"community_district"``,
            ``"council_district"``, ``"neighborhood_tabulation_area"``,
            ``"census_tract"``, or ``"zcta"``. Common aliases like ``"zip"`` or
            ``"nta"`` are also accepted.
        values: Optional filter. A single value string, or a sequence of values.
            Values are normalized automatically (e.g. ``"bk 01"`` becomes
            ``"BROOKLYN 01"`` for community districts).
        vintage: Optional vintage year. Defaults to the layer's default vintage
            (2020 for most layers, 2023 for council districts).

    Returns:
        A ``BoundaryCollection`` with matching features and vintage metadata.

    Raises:
        ValueError: If the layer or vintage is unsupported, or no features
            match the requested values.

    Example:
        >>> boundaries = load_nyc_boundaries("borough", values="Manhattan")
        >>> len(boundaries.features)
        1
        >>> boundaries.vintage
        2020
    """
    normalized_layer = normalize_boundary_layer(layer)
    resolved_vintage = _resolve_vintage(normalized_layer, vintage)
    boundary_collection = boundary_collection_from_geojson(
        load_boundary_payload(normalized_layer, vintage=resolved_vintage),
        vintage=resolved_vintage,
    )
    normalized_values = normalize_boundary_values(normalized_layer, values)
    if normalized_values is None:
        return boundary_collection
    requested_values = set(normalized_values)
    selected_features = tuple(
        feature
        for feature in boundary_collection.features
        if feature.geography_value in requested_values
    )
    if not selected_features:
        raise ValueError(
            "No boundaries matched the requested values for layer "
            f"{normalized_layer!r}: {normalized_values!r}."
        )
    return BoundaryCollection(
        geography=normalized_layer,
        features=selected_features,
        vintage=resolved_vintage,
    )


def load_boundaries(
    source: str | Path,
    *,
    vintage: int | None = None,
) -> BoundaryCollection:
    """Load boundaries from a packaged layer name or a GeoJSON file path.

    When *source* is a recognized layer name (or alias), delegates to
    ``load_nyc_boundaries``.  When it is a file path, reads and parses
    the GeoJSON file directly.

    Args:
        source: A layer name string (e.g. ``"borough"``) or a ``Path`` to
            a GeoJSON file.
        vintage: Optional vintage year, used only when *source* is a layer name.

    Returns:
        A ``BoundaryCollection`` parsed from the source.

    Raises:
        ValueError: If the layer is unsupported or the file cannot be parsed.
    """
    if isinstance(source, Path) or Path(source).exists():
        return load_boundary_collection(source)
    try:
        return load_nyc_boundaries(str(source), vintage=vintage)
    except ValueError:
        return load_boundary_collection(source)


def load_nyc_boundaries_geodataframe(
    layer: str = "community_district",
    *,
    values: str | tuple[str, ...] | list[str] | None = None,
    vintage: int | None = None,
) -> gpd.GeoDataFrame:
    """Load packaged NYC boundaries as a GeoPandas ``GeoDataFrame``.

    Requires the ``spatial`` extra (``pip install nyc-geo-toolkit[spatial]``).

    Args:
        layer: Boundary layer name or alias.
        values: Optional value filter (see ``load_nyc_boundaries``).
        vintage: Optional vintage year.

    Returns:
        A ``GeoDataFrame`` with ``geography``, ``geography_value``, and
        ``geometry`` columns, plus any additional properties from the source.

    Raises:
        ImportError: If geopandas or shapely is not installed.
        ValueError: If the layer, vintage, or values are unsupported.
    """
    return _boundary_collection_to_geodataframe(
        load_nyc_boundaries(layer, values=values, vintage=vintage)
    )


def load_nyc_census_tracts(
    *,
    values: str | tuple[str, ...] | list[str] | None = None,
    vintage: int | None = None,
) -> BoundaryCollection:
    """Load NYC census tract boundaries.

    Convenience wrapper around ``load_nyc_boundaries("census_tract", ...)``.

    Args:
        values: Optional tract filter (11-digit GEOIDs or 7-digit borough codes).
        vintage: Optional vintage year (available: 2000, 2010, 2020).

    Returns:
        A ``BoundaryCollection`` of census tract features.
    """
    return load_nyc_boundaries("census_tract", values=values, vintage=vintage)


def load_nyc_neighborhood_tabulation_areas(
    *,
    values: str | tuple[str, ...] | list[str] | None = None,
    vintage: int | None = None,
) -> BoundaryCollection:
    """Load NYC Neighborhood Tabulation Area boundaries.

    Convenience wrapper around
    ``load_nyc_boundaries("neighborhood_tabulation_area", ...)``.

    Args:
        values: Optional NTA code filter (e.g. ``"BK0101"``).
        vintage: Optional vintage year (available: 2010, 2020).

    Returns:
        A ``BoundaryCollection`` of NTA features.
    """
    return load_nyc_boundaries(
        "neighborhood_tabulation_area", values=values, vintage=vintage
    )


def load_nyc_council_districts(
    *,
    values: str | tuple[str, ...] | list[str] | None = None,
    vintage: int | None = None,
) -> BoundaryCollection:
    """Load NYC City Council district boundaries.

    Convenience wrapper around ``load_nyc_boundaries("council_district", ...)``.

    Args:
        values: Optional district number filter (e.g. ``"33"``).
        vintage: Optional vintage year (available: 2013, 2023).

    Returns:
        A ``BoundaryCollection`` of council district features.
    """
    return load_nyc_boundaries("council_district", values=values, vintage=vintage)

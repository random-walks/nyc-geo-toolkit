"""Reusable NYC geography resources, normalization helpers, and boundary loaders."""

from __future__ import annotations

from ._constants import (
    BOROUGH_BRONX,
    BOROUGH_BROOKLYN,
    BOROUGH_MANHATTAN,
    BOROUGH_QUEENS,
    BOROUGH_STATEN_ISLAND,
    SUPPORTED_BOROUGHS,
    SUPPORTED_BOUNDARY_GEOGRAPHIES,
)
from ._conversions import boundaries_to_dataframe, boundaries_to_geojson
from ._geodesy import (
    build_circle_polygon,
    haversine_distance_meters,
    walk_radius_meters,
)
from ._loaders import (
    list_boundary_layers,
    list_boundary_values,
    load_boundaries,
    load_nyc_boundaries,
    load_nyc_boundaries_geodataframe,
    load_nyc_census_tracts,
    load_nyc_council_districts,
    load_nyc_neighborhood_tabulation_areas,
)
from ._models import BoundaryCollection, BoundaryFeature, BoundaryLayerSpec
from ._normalize import (
    normalize_borough_name,
    normalize_boundary_layer,
    normalize_boundary_value,
    normalize_boundary_values,
)
from ._ops import clip_boundaries_to_bbox
from ._version import version as __version__

__all__ = [
    "BOROUGH_BRONX",
    "BOROUGH_BROOKLYN",
    "BOROUGH_MANHATTAN",
    "BOROUGH_QUEENS",
    "BOROUGH_STATEN_ISLAND",
    "SUPPORTED_BOUNDARY_GEOGRAPHIES",
    "SUPPORTED_BOROUGHS",
    "BoundaryCollection",
    "BoundaryFeature",
    "BoundaryLayerSpec",
    "build_circle_polygon",
    "__version__",
    "boundaries_to_dataframe",
    "boundaries_to_geojson",
    "clip_boundaries_to_bbox",
    "haversine_distance_meters",
    "list_boundary_layers",
    "list_boundary_values",
    "load_boundaries",
    "load_nyc_boundaries",
    "load_nyc_boundaries_geodataframe",
    "load_nyc_census_tracts",
    "load_nyc_council_districts",
    "load_nyc_neighborhood_tabulation_areas",
    "normalize_borough_name",
    "normalize_boundary_layer",
    "normalize_boundary_value",
    "normalize_boundary_values",
    "walk_radius_meters",
]

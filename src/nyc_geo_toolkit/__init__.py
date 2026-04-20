"""Reusable NYC geography resources, normalization helpers, and boundary loaders."""

from __future__ import annotations

from ._basemap import add_osm_basemap, bbox_around, to_web_mercator
from ._constants import (
    BOROUGH_BRONX,
    BOROUGH_BROOKLYN,
    BOROUGH_MANHATTAN,
    BOROUGH_QUEENS,
    BOROUGH_STATEN_ISLAND,
    DEFAULT_VINTAGE,
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
    describe_layer,
    list_available_vintages,
    list_boundary_layers,
    list_boundary_values,
    load_boundaries,
    load_nyc_boundaries,
    load_nyc_boundaries_geodataframe,
    load_nyc_census_tracts,
    load_nyc_council_districts,
    load_nyc_neighborhood_tabulation_areas,
    vintage_for_census_decade,
)
from ._models import BoundaryCollection, BoundaryFeature, BoundaryLayerSpec
from ._normalize import (
    normalize_borough_name,
    normalize_boundary_layer,
    normalize_boundary_value,
    normalize_boundary_values,
)
from ._ops import centroids_from_boundaries, clip_boundaries_to_bbox
from ._version import version as __version__

__all__ = [
    "add_osm_basemap",
    "bbox_around",
    "BOROUGH_BRONX",
    "BOROUGH_BROOKLYN",
    "BOROUGH_MANHATTAN",
    "BOROUGH_QUEENS",
    "BOROUGH_STATEN_ISLAND",
    "DEFAULT_VINTAGE",
    "SUPPORTED_BOUNDARY_GEOGRAPHIES",
    "SUPPORTED_BOROUGHS",
    "BoundaryCollection",
    "BoundaryFeature",
    "BoundaryLayerSpec",
    "build_circle_polygon",
    "__version__",
    "boundaries_to_dataframe",
    "boundaries_to_geojson",
    "centroids_from_boundaries",
    "clip_boundaries_to_bbox",
    "describe_layer",
    "haversine_distance_meters",
    "list_available_vintages",
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
    "to_web_mercator",
    "vintage_for_census_decade",
    "walk_radius_meters",
]

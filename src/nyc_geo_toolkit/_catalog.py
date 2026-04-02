"""Catalog of packaged NYC boundary layers."""

from __future__ import annotations

from typing import Final

from ._models import BoundaryLayerSpec

BOUNDARY_LAYER_CATALOG: Final[tuple[BoundaryLayerSpec, ...]] = (
    BoundaryLayerSpec(
        "borough", "NYC borough boundaries", "data/boundaries/borough.geojson"
    ),
    BoundaryLayerSpec(
        "community_district",
        "NYC community district boundaries",
        "data/boundaries/community_district.geojson",
    ),
    BoundaryLayerSpec(
        "council_district",
        "NYC city council district boundaries",
        "data/boundaries/council_district.geojson",
    ),
    BoundaryLayerSpec(
        "neighborhood_tabulation_area",
        "NYC neighborhood tabulation areas",
        "data/boundaries/neighborhood_tabulation_area.geojson",
    ),
    BoundaryLayerSpec(
        "zcta", "NYC modified ZIP Code Tabulation Areas", "data/boundaries/zcta.geojson"
    ),
    BoundaryLayerSpec(
        "census_tract", "NYC census tracts", "data/boundaries/census_tract.geojson"
    ),
)
BOUNDARY_LAYER_LOOKUP: Final[dict[str, BoundaryLayerSpec]] = {
    spec.layer: spec for spec in BOUNDARY_LAYER_CATALOG
}

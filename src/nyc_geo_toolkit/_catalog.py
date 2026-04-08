"""Catalog of packaged NYC boundary layers and their vintage history."""

from __future__ import annotations

from typing import Final

from ._models import BoundaryLayerSpec

# ---------------------------------------------------------------------------
# Default (current) vintage entries -- resource_path unchanged from pre-vintage
# ---------------------------------------------------------------------------

BOUNDARY_LAYER_CATALOG: Final[tuple[BoundaryLayerSpec, ...]] = (
    BoundaryLayerSpec(
        "borough",
        "NYC borough boundaries",
        "data/boundaries/borough.geojson",
        vintage=2020,
        source_name="NYC Dept of City Planning",
        source_url="https://data.cityofnewyork.us/City-Government/Borough-Boundaries/7t3b-ywvw",
        feature_count=5,
    ),
    BoundaryLayerSpec(
        "community_district",
        "NYC community district boundaries",
        "data/boundaries/community_district.geojson",
        vintage=2020,
        source_name="NYC Dept of City Planning",
        source_url="https://data.cityofnewyork.us/City-Government/Community-Districts/jp9i-3b7y",
        feature_count=59,
    ),
    BoundaryLayerSpec(
        "council_district",
        "NYC city council district boundaries (2023 redistricting)",
        "data/boundaries/council_district.geojson",
        vintage=2023,
        source_name="NYC Districting Commission",
        source_url="https://data.cityofnewyork.us/City-Government/City-Council-Districts/yusd-j4xi",
        feature_count=51,
    ),
    BoundaryLayerSpec(
        "neighborhood_tabulation_area",
        "NYC neighborhood tabulation areas (2020 Census)",
        "data/boundaries/neighborhood_tabulation_area.geojson",
        vintage=2020,
        source_name="NYC Dept of City Planning",
        source_url="https://data.cityofnewyork.us/City-Government/2020-Neighborhood-Tabulation-Areas-NTAs-/9nt8-h7nd",
        feature_count=262,
    ),
    BoundaryLayerSpec(
        "zcta",
        "NYC modified ZIP Code Tabulation Areas (2020 Census)",
        "data/boundaries/zcta.geojson",
        vintage=2020,
        source_name="NYC Dept of City Planning",
        source_url="https://data.cityofnewyork.us/Health/Modified-Zip-Code-Tabulation-Areas-MODZCTA-/pri4-ifjk",
        feature_count=178,
    ),
    BoundaryLayerSpec(
        "census_tract",
        "NYC census tracts (2020 Census)",
        "data/boundaries/census_tract.geojson",
        vintage=2020,
        source_name="US Census Bureau TIGER/Line",
        source_url="https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html",
        feature_count=2325,
    ),
)

BOUNDARY_LAYER_LOOKUP: Final[dict[str, BoundaryLayerSpec]] = {
    spec.layer: spec for spec in BOUNDARY_LAYER_CATALOG
}

# ---------------------------------------------------------------------------
# Historical vintage entries
# ---------------------------------------------------------------------------

HISTORICAL_LAYER_CATALOG: Final[tuple[BoundaryLayerSpec, ...]] = (
    BoundaryLayerSpec(
        "census_tract",
        "NYC census tracts (2010 Census)",
        "data/boundaries/historical/census_tract_2010.geojson",
        vintage=2010,
        source_name="US Census Bureau TIGER/Line",
        source_url="https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html",
        feature_count=2168,
    ),
    BoundaryLayerSpec(
        "census_tract",
        "NYC census tracts (2000 Census)",
        "data/boundaries/historical/census_tract_2000.geojson",
        vintage=2000,
        source_name="US Census Bureau TIGER/Line",
        source_url="https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html",
        feature_count=2217,
    ),
    BoundaryLayerSpec(
        "neighborhood_tabulation_area",
        "NYC neighborhood tabulation areas (2010 Census)",
        "data/boundaries/historical/neighborhood_tabulation_area_2010.geojson",
        vintage=2010,
        source_name="NYC Dept of City Planning",
        source_url="https://data.cityofnewyork.us/City-Government/2010-Neighborhood-Tabulation-Areas-NTAs-/cpf4-rkhq",
        feature_count=195,
    ),
    BoundaryLayerSpec(
        "council_district",
        "NYC city council district boundaries (2013 redistricting)",
        "data/boundaries/historical/council_district_2013.geojson",
        vintage=2013,
        source_name="NYC Districting Commission",
        source_url="https://data.cityofnewyork.us/City-Government/City-Council-Districts/yusd-j4xi",
        feature_count=51,
    ),
    BoundaryLayerSpec(
        "zcta",
        "NYC ZIP Code Tabulation Areas (2010 Census)",
        "data/boundaries/historical/zcta_2010.geojson",
        vintage=2010,
        source_name="US Census Bureau TIGER/Line",
        source_url="https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html",
        feature_count=263,
    ),
)

# ---------------------------------------------------------------------------
# Merged vintage lookups
# ---------------------------------------------------------------------------

VINTAGE_LOOKUP: Final[dict[tuple[str, int], BoundaryLayerSpec]] = {
    **{(spec.layer, spec.vintage): spec for spec in BOUNDARY_LAYER_CATALOG},
    **{(spec.layer, spec.vintage): spec for spec in HISTORICAL_LAYER_CATALOG},
}

AVAILABLE_VINTAGES: Final[dict[str, tuple[int, ...]]] = {
    layer: tuple(sorted(v for (lyr, v) in VINTAGE_LOOKUP if lyr == layer))
    for layer in sorted({lyr for lyr, _ in VINTAGE_LOOKUP})
}

DEFAULT_LAYER_VINTAGES: Final[dict[str, int]] = {
    spec.layer: spec.vintage for spec in BOUNDARY_LAYER_CATALOG
}

# ---------------------------------------------------------------------------
# Census decade to actual vintage mapping
# ---------------------------------------------------------------------------

CENSUS_DECADE_VINTAGE_MAP: Final[dict[tuple[str, int], int]] = {
    ("borough", 2000): 2020,
    ("borough", 2010): 2020,
    ("borough", 2020): 2020,
    ("community_district", 2000): 2020,
    ("community_district", 2010): 2020,
    ("community_district", 2020): 2020,
    ("council_district", 2010): 2013,
    ("council_district", 2020): 2023,
    ("neighborhood_tabulation_area", 2010): 2010,
    ("neighborhood_tabulation_area", 2020): 2020,
    ("census_tract", 2000): 2000,
    ("census_tract", 2010): 2010,
    ("census_tract", 2020): 2020,
    ("zcta", 2010): 2010,
    ("zcta", 2020): 2020,
}

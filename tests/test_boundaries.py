from __future__ import annotations

from typing import cast

from nyc_geo_toolkit import (
    boundaries_to_geojson,
    list_boundary_layers,
    list_boundary_values,
    load_boundaries,
    load_nyc_boundaries,
    load_nyc_census_tracts,
    load_nyc_council_districts,
    load_nyc_neighborhood_tabulation_areas,
)


def test_list_boundary_layers_reports_packaged_layers() -> None:
    assert list_boundary_layers() == (
        "borough",
        "community_district",
        "council_district",
        "neighborhood_tabulation_area",
        "zcta",
        "census_tract",
    )


def test_list_boundary_values_reads_packaged_layer_values() -> None:
    assert "QUEENS" in list_boundary_values("borough")


def test_load_nyc_boundaries_loads_packaged_community_district_layer() -> None:
    boundaries = load_nyc_boundaries("community_district")
    assert boundaries.geography == "community_district"
    assert len(boundaries.features) == 59
    assert "BRONX 05" in {feature.geography_value for feature in boundaries.features}


def test_load_nyc_boundaries_filters_values_and_supports_zcta_aliases() -> None:
    boundaries = load_nyc_boundaries("zip", values="MODZCTA 10001")
    assert boundaries.geography == "zcta"
    assert [feature.geography_value for feature in boundaries.features] == ["10001"]
    assert boundaries.features[0].properties["modzcta"] == "10001"


def test_specific_packaged_layer_loaders_work_for_remaining_layers() -> None:
    census_tracts = load_nyc_census_tracts(values="1000100")
    ntas = load_nyc_neighborhood_tabulation_areas(values="bk0101")
    council_districts = load_nyc_council_districts(values="district 33")
    assert [feature.geography_value for feature in census_tracts.features] == [
        "36061000100"
    ]
    assert [feature.geography_value for feature in ntas.features] == ["BK0101"]
    assert [feature.geography_value for feature in council_districts.features] == ["33"]


def test_load_boundaries_accepts_packaged_layer_names() -> None:
    borough_boundaries = load_boundaries("borough")
    assert borough_boundaries.geography == "borough"
    assert len(borough_boundaries.features) == 5


def test_boundaries_to_geojson_preserves_feature_collection_shape() -> None:
    boundaries = load_nyc_boundaries("borough", values="Queens")
    payload = boundaries_to_geojson(boundaries)
    features = cast(list[dict[str, object]], payload["features"])
    properties = cast(dict[str, object], features[0]["properties"])
    assert payload["type"] == "FeatureCollection"
    assert len(features) == 1
    assert properties["geography_value"] == "QUEENS"

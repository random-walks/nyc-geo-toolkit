from __future__ import annotations

import importlib.metadata
import importlib.resources
from typing import cast

import pytest

from nyc_geo_toolkit import (
    BOROUGH_BRONX,
    BOROUGH_BROOKLYN,
    BOROUGH_MANHATTAN,
    BOROUGH_QUEENS,
    BOROUGH_STATEN_ISLAND,
    SUPPORTED_BOROUGHS,
    SUPPORTED_BOUNDARY_GEOGRAPHIES,
    BoundaryCollection,
    BoundaryFeature,
    BoundaryLayerSpec,
    __version__,
    boundaries_to_dataframe,
    boundaries_to_geojson,
    clip_boundaries_to_bbox,
    list_boundary_layers,
    list_boundary_values,
    load_boundaries,
    load_nyc_boundaries,
    load_nyc_boundaries_geodataframe,
    load_nyc_census_tracts,
    load_nyc_council_districts,
    load_nyc_neighborhood_tabulation_areas,
    normalize_borough_name,
    normalize_boundary_layer,
    normalize_boundary_value,
    normalize_boundary_values,
)


@pytest.mark.unit
def test_top_level_public_contract_core() -> None:
    distribution_version = importlib.metadata.version("nyc-geo-toolkit")
    assert isinstance(__version__, str)
    assert __version__
    assert isinstance(distribution_version, str)
    assert distribution_version
    assert SUPPORTED_BOROUGHS == (
        BOROUGH_BRONX,
        BOROUGH_BROOKLYN,
        BOROUGH_MANHATTAN,
        BOROUGH_QUEENS,
        BOROUGH_STATEN_ISLAND,
    )
    assert set(SUPPORTED_BOUNDARY_GEOGRAPHIES) == {
        "borough",
        "community_district",
        "council_district",
        "neighborhood_tabulation_area",
        "census_tract",
        "zcta",
    }
    assert list_boundary_layers() == (
        "borough",
        "community_district",
        "council_district",
        "neighborhood_tabulation_area",
        "zcta",
        "census_tract",
    )
    assert set(list_boundary_values("borough")) == set(SUPPORTED_BOROUGHS)

    assert normalize_borough_name("bk") == BOROUGH_BROOKLYN
    assert normalize_boundary_layer("zip code") == "zcta"
    assert normalize_boundary_value("community_district", "01 Brooklyn") == (
        "BROOKLYN 01"
    )
    assert normalize_boundary_values("borough", ["Queens", "bk", "Queens"]) == (
        "QUEENS",
        "BROOKLYN",
    )

    spec = BoundaryLayerSpec(
        layer="borough",
        display_name="NYC borough boundaries",
        resource_path="data/boundaries/borough.geojson",
    )
    assert spec.layer == "borough"

    feature = BoundaryFeature(
        geography="borough",
        geography_value=BOROUGH_QUEENS,
        geometry={"type": "Polygon", "coordinates": []},
        properties={"name": "Queens"},
    )
    collection = BoundaryCollection(geography="borough", features=(feature,))
    assert collection.geography == "borough"
    assert collection.features[0].geography_value == BOROUGH_QUEENS

    payload = boundaries_to_geojson(collection)
    features = cast(list[dict[str, object]], payload["features"])
    properties = cast(dict[str, object], features[0]["properties"])
    assert payload["type"] == "FeatureCollection"
    assert properties["geography_value"] == BOROUGH_QUEENS

    packaged_boroughs = load_boundaries("borough")
    assert packaged_boroughs.geography == "borough"
    assert len(packaged_boroughs.features) == 5

    with importlib.resources.as_file(
        importlib.resources.files("nyc_geo_toolkit").joinpath(
            "data/boundaries/borough.geojson"
        )
    ) as borough_path:
        boroughs_from_path = load_boundaries(borough_path)

    assert boroughs_from_path.geography == "borough"
    assert len(boroughs_from_path.features) == 5
    assert load_nyc_boundaries("borough", values="Queens").features[
        0
    ].geography_value == (BOROUGH_QUEENS)
    assert load_nyc_census_tracts(values="1000100").features[0].geography_value == (
        "36061000100"
    )
    assert load_nyc_council_districts(values="district 33").features[
        0
    ].geography_value == ("33")
    assert (
        load_nyc_neighborhood_tabulation_areas(values="bk0101")
        .features[0]
        .geography_value
        == "BK0101"
    )


@pytest.mark.optional
def test_top_level_public_contract_optional_helpers() -> None:
    pytest.importorskip(
        "pandas",
        reason="Install nyc-geo-toolkit[dataframes] to run DataFrame contract tests.",
    )
    geopandas = pytest.importorskip(
        "geopandas",
        reason="Install nyc-geo-toolkit[spatial] to run GeoDataFrame contract tests.",
    )
    pytest.importorskip(
        "shapely",
        reason="Install nyc-geo-toolkit[spatial] to run clipping contract tests.",
    )

    boroughs = load_nyc_boundaries("borough", values=("Queens", "Brooklyn"))
    dataframe = boundaries_to_dataframe(boroughs)
    assert list(dataframe["geography_value"]) == ["BROOKLYN", "QUEENS"]
    assert "geometry" in dataframe.columns

    boundaries_gdf = load_nyc_boundaries_geodataframe("zcta", values=("10001", "10002"))
    assert isinstance(boundaries_gdf, geopandas.GeoDataFrame)
    assert set(boundaries_gdf["geography_value"]) == {"10001", "10002"}
    assert str(boundaries_gdf.crs) == "EPSG:4326"

    clipped = clip_boundaries_to_bbox(
        load_nyc_boundaries("borough"),
        min_longitude=-73.97,
        min_latitude=40.68,
        max_longitude=-73.84,
        max_latitude=40.81,
    )
    assert {feature.geography_value for feature in clipped.features} == {
        "BRONX",
        "BROOKLYN",
        "MANHATTAN",
        "QUEENS",
    }

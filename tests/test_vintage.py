"""Tests for temporal/vintage-aware boundary loading."""

from __future__ import annotations

import pytest

from nyc_geo_toolkit import (
    DEFAULT_VINTAGE,
    BoundaryCollection,
    describe_layer,
    list_available_vintages,
    load_nyc_boundaries,
    load_nyc_census_tracts,
    vintage_for_census_decade,
)


class TestDefaultVintage:
    def test_default_vintage_is_2020(self) -> None:
        assert DEFAULT_VINTAGE == 2020

    def test_default_load_returns_default_vintage(self) -> None:
        b = load_nyc_boundaries("borough")
        assert b.vintage == 2020

    def test_explicit_default_vintage_matches_implicit(self) -> None:
        implicit = load_nyc_boundaries("census_tract")
        explicit = load_nyc_boundaries("census_tract", vintage=2020)
        assert implicit.vintage == explicit.vintage
        assert len(implicit.features) == len(explicit.features)


class TestListAvailableVintages:
    def test_census_tract_has_three_vintages(self) -> None:
        vintages = list_available_vintages("census_tract")
        assert isinstance(vintages, tuple)
        assert vintages == (2000, 2010, 2020)

    def test_borough_has_single_vintage(self) -> None:
        vintages = list_available_vintages("borough")
        assert vintages == (2020,)

    def test_council_district_has_actual_years(self) -> None:
        vintages = list_available_vintages("council_district")
        assert vintages == (2013, 2023)

    def test_nta_has_two_vintages(self) -> None:
        vintages = list_available_vintages("neighborhood_tabulation_area")
        assert vintages == (2010, 2020)

    def test_zcta_has_two_vintages(self) -> None:
        vintages = list_available_vintages("zcta")
        assert vintages == (2010, 2020)

    def test_all_layers_returns_dict(self) -> None:
        result = list_available_vintages()
        assert isinstance(result, dict)
        assert "census_tract" in result
        assert "borough" in result

    def test_aliases_accepted(self) -> None:
        vintages = list_available_vintages("zip")
        assert vintages == list_available_vintages("zcta")


class TestLoadWithVintage:
    def test_load_census_tracts_2010(self) -> None:
        b = load_nyc_boundaries("census_tract", vintage=2010)
        assert b.vintage == 2010
        assert b.geography == "census_tract"
        assert len(b.features) > 0

    def test_load_census_tracts_2000(self) -> None:
        b = load_nyc_boundaries("census_tract", vintage=2000)
        assert b.vintage == 2000
        assert len(b.features) > 0

    def test_load_nta_2010(self) -> None:
        b = load_nyc_boundaries("neighborhood_tabulation_area", vintage=2010)
        assert b.vintage == 2010
        assert len(b.features) > 0

    def test_load_council_district_2013(self) -> None:
        b = load_nyc_boundaries("council_district", vintage=2013)
        assert b.vintage == 2013
        assert len(b.features) == 51

    def test_load_zcta_2010(self) -> None:
        b = load_nyc_boundaries("zcta", vintage=2010)
        assert b.vintage == 2010
        assert len(b.features) > 0

    def test_convenience_loader_with_vintage(self) -> None:
        b = load_nyc_census_tracts(vintage=2010)
        assert b.vintage == 2010
        assert b.geography == "census_tract"

    def test_unsupported_vintage_raises(self) -> None:
        with pytest.raises(ValueError, match="vintage"):
            load_nyc_boundaries("borough", vintage=1990)

    def test_collection_carries_vintage(self) -> None:
        b = load_nyc_boundaries("census_tract", vintage=2010)
        assert isinstance(b, BoundaryCollection)
        assert b.vintage == 2010


class TestDescribeLayer:
    def test_default_vintage(self) -> None:
        spec = describe_layer("census_tract")
        assert spec.vintage == 2020
        assert spec.source_name != ""
        assert spec.source_url != ""

    def test_historical_vintage(self) -> None:
        spec = describe_layer("census_tract", vintage=2010)
        assert spec.vintage == 2010
        assert "2010" in spec.display_name

    def test_unsupported_vintage_raises(self) -> None:
        with pytest.raises(ValueError, match="vintage"):
            describe_layer("borough", vintage=1990)

    def test_council_district_default_is_2023(self) -> None:
        spec = describe_layer("council_district")
        assert spec.vintage == 2023


class TestVintageForCensusDecade:
    def test_census_tract_decades(self) -> None:
        assert vintage_for_census_decade("census_tract", 2000) == 2000
        assert vintage_for_census_decade("census_tract", 2010) == 2010
        assert vintage_for_census_decade("census_tract", 2020) == 2020

    def test_council_district_maps_to_redistricting_year(self) -> None:
        assert vintage_for_census_decade("council_district", 2010) == 2013
        assert vintage_for_census_decade("council_district", 2020) == 2023

    def test_borough_always_2020(self) -> None:
        assert vintage_for_census_decade("borough", 2000) == 2020
        assert vintage_for_census_decade("borough", 2010) == 2020
        assert vintage_for_census_decade("borough", 2020) == 2020

    def test_invalid_decade_raises(self) -> None:
        with pytest.raises(ValueError, match="decade"):
            vintage_for_census_decade("census_tract", 1990)

    def test_aliases_accepted(self) -> None:
        assert vintage_for_census_decade("zip", 2010) == vintage_for_census_decade(
            "zcta", 2010
        )

from __future__ import annotations

import pytest

from nyc_geo_toolkit import (
    boundaries_to_dataframe,
    clip_boundaries_to_bbox,
    load_nyc_boundaries,
    load_nyc_boundaries_geodataframe,
)

pytest.importorskip(
    "pandas",
    reason="Install nyc-geo-toolkit[dataframes] to run DataFrame tests.",
)
pytest.importorskip(
    "shapely",
    reason="Install nyc-geo-toolkit[spatial] to run clipping tests.",
)
pytest.importorskip(
    "geopandas",
    reason="Install nyc-geo-toolkit[spatial] to run GeoDataFrame tests.",
)
pytestmark = pytest.mark.optional


def test_boundaries_to_dataframe_returns_rows() -> None:
    dataframe = boundaries_to_dataframe(
        load_nyc_boundaries("borough", values=("Queens", "Brooklyn"))
    )
    assert list(dataframe["geography_value"]) == ["BROOKLYN", "QUEENS"]
    assert "geometry" in dataframe.columns


def test_load_nyc_boundaries_geodataframe_reads_packaged_zcta_layer() -> None:
    boundaries_gdf = load_nyc_boundaries_geodataframe("zcta", values=("10001", "10002"))
    assert len(boundaries_gdf) == 2
    assert set(boundaries_gdf["geography_value"]) == {"10001", "10002"}
    assert str(boundaries_gdf.crs) == "EPSG:4326"


def test_clip_boundaries_to_bbox_returns_only_intersecting_boundaries() -> None:
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

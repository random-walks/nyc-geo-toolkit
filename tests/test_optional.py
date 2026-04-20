from __future__ import annotations

import pytest

from nyc_geo_toolkit import (
    boundaries_to_dataframe,
    centroids_from_boundaries,
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

from shapely.geometry import shape  # type: ignore[import-untyped]  # noqa: E402


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


def test_centroids_from_boundaries_returns_point_geometries() -> None:
    boroughs = load_nyc_boundaries("borough")
    centroids = centroids_from_boundaries(boroughs)

    # Preserves collection identity (same layer, same vintage, same feature set).
    assert centroids.geography == boroughs.geography
    assert centroids.vintage == boroughs.vintage
    assert {f.geography_value for f in centroids.features} == {
        f.geography_value for f in boroughs.features
    }

    # Every feature is a GeoJSON Point with WGS84 coordinates in the NYC bbox.
    for feature in centroids.features:
        assert feature.geometry["type"] == "Point"
        lon, lat = feature.geometry["coordinates"]
        assert -74.3 <= lon <= -73.6, f"{feature.geography_value} lon={lon}"
        assert 40.45 <= lat <= 40.95, f"{feature.geography_value} lat={lat}"


def test_centroids_from_boundaries_preserves_properties() -> None:
    cds = load_nyc_boundaries("community_district")
    centroids = centroids_from_boundaries(cds)
    assert len(centroids.features) == len(cds.features)
    for original, centroid in zip(cds.features, centroids.features, strict=True):
        assert centroid.geography_value == original.geography_value
        assert centroid.properties == original.properties


def test_centroids_from_boundaries_representative_points_fall_inside() -> None:
    """representative=True must produce a point inside the source polygon.

    Default geometric centroids can fall outside for non-convex shapes
    (e.g. community districts with concave shorelines); that's the whole
    point of the representative_point flag.
    """
    cds = load_nyc_boundaries("community_district")
    rep_centroids = centroids_from_boundaries(cds, representative=True)
    for original, rep in zip(cds.features, rep_centroids.features, strict=True):
        polygon = shape(original.geometry)
        point = shape(rep.geometry)
        assert polygon.covers(point), (
            f"representative point for {original.geography_value!r} fell outside polygon"
        )

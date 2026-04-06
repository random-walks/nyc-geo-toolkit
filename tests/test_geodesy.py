from __future__ import annotations

import math

import pytest

from nyc_geo_toolkit import (
    build_circle_polygon,
    haversine_distance_meters,
    walk_radius_meters,
)


def test_haversine_distance_meters_returns_zero_for_same_point() -> None:
    assert haversine_distance_meters(40.7128, -74.0060, 40.7128, -74.0060) == 0.0


def test_haversine_distance_meters_is_reasonable_for_known_distance() -> None:
    # Lower Manhattan to Times Square is about 5.3 km as the crow flies.
    distance = haversine_distance_meters(40.7061, -74.0086, 40.7580, -73.9855)
    assert math.isclose(distance, 6_100, rel_tol=0.1)


def test_walk_radius_meters_uses_default_walking_speed() -> None:
    assert walk_radius_meters(10) == 800.0


def test_walk_radius_meters_rejects_non_positive_values() -> None:
    with pytest.raises(ValueError, match="Walking minutes must be positive"):
        walk_radius_meters(0)

    with pytest.raises(ValueError, match="Walking speed must be positive"):
        walk_radius_meters(10, meters_per_minute=0)


def test_build_circle_polygon_closes_ring() -> None:
    polygon = build_circle_polygon(40.7128, -74.0060, 400)
    assert len(polygon) == 25
    assert polygon[0] == polygon[-1]


def test_build_circle_polygon_rejects_invalid_inputs() -> None:
    with pytest.raises(ValueError, match="Circle radius must be positive"):
        build_circle_polygon(40.7128, -74.0060, 0)

    with pytest.raises(ValueError, match="Circle polygons need at least 8 sides"):
        build_circle_polygon(40.7128, -74.0060, 400, sides=6)

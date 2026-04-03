"""Small dependency-free geodesy helpers for NYC workflows."""

from __future__ import annotations

from math import asin, atan2, cos, degrees, pi, radians, sin, sqrt

EARTH_RADIUS_METERS = 6_371_000.0
DEFAULT_WALKING_METERS_PER_MINUTE = 80.0
_POSITIVE_MINUTES_MESSAGE = "Walking minutes must be positive."
_POSITIVE_RADIUS_MESSAGE = "Circle radius must be positive."
_MINIMUM_SIDES_MESSAGE = "Circle polygons need at least 8 sides."


def haversine_distance_meters(
    latitude_a: float,
    longitude_a: float,
    latitude_b: float,
    longitude_b: float,
) -> float:
    """Return the great-circle distance between two WGS84 points in meters."""

    lat1 = radians(latitude_a)
    lon1 = radians(longitude_a)
    lat2 = radians(latitude_b)
    lon2 = radians(longitude_b)

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    hav = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2
    return 2 * EARTH_RADIUS_METERS * asin(sqrt(hav))


def walk_radius_meters(
    minutes: float, *, meters_per_minute: float = DEFAULT_WALKING_METERS_PER_MINUTE
) -> float:
    """Convert a walking-time threshold into an approximate radius in meters."""

    if minutes <= 0:
        raise ValueError(_POSITIVE_MINUTES_MESSAGE)
    if meters_per_minute <= 0:
        raise ValueError("Walking speed must be positive.")
    return float(minutes) * meters_per_minute


def build_circle_polygon(
    latitude: float,
    longitude: float,
    radius_meters: float,
    *,
    sides: int = 24,
) -> tuple[tuple[float, float], ...]:
    """Return a simple lon/lat polygon approximating a circle around a point."""

    if radius_meters <= 0:
        raise ValueError(_POSITIVE_RADIUS_MESSAGE)
    if sides < 8:
        raise ValueError(_MINIMUM_SIDES_MESSAGE)

    latitude_radians = radians(latitude)
    angular_distance = radius_meters / EARTH_RADIUS_METERS
    points: list[tuple[float, float]] = []

    for index in range(sides):
        bearing = 2 * pi * (index / sides)
        lat = asin(
            sin(latitude_radians) * cos(angular_distance)
            + cos(latitude_radians) * sin(angular_distance) * cos(bearing)
        )
        lon = radians(longitude) + atan2(
            sin(bearing) * sin(angular_distance) * cos(latitude_radians),
            cos(angular_distance) - sin(latitude_radians) * sin(lat),
        )
        points.append((round(degrees(lon), 6), round(degrees(lat), 6)))

    points.append(points[0])
    return tuple(points)

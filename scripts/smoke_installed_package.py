from __future__ import annotations

import importlib.resources

import nyc_geo_toolkit
from nyc_geo_toolkit import (
    boundaries_to_geojson,
    list_boundary_layers,
    load_nyc_boundaries,
)


def main() -> None:
    typing_marker = importlib.resources.files("nyc_geo_toolkit").joinpath("py.typed")
    if not typing_marker.is_file():
        raise SystemExit("Installed package is missing `nyc_geo_toolkit/py.typed`.")

    layers = list_boundary_layers()
    if "borough" not in layers:
        raise SystemExit("Installed package did not expose the expected layer catalog.")

    borough_boundaries = load_nyc_boundaries("borough", values="Queens")
    if [feature.geography_value for feature in borough_boundaries.features] != [
        "QUEENS"
    ]:
        raise SystemExit(
            "Installed package could not load packaged borough boundaries."
        )

    payload = boundaries_to_geojson(borough_boundaries)
    if payload.get("type") != "FeatureCollection":
        raise SystemExit("Installed package did not return valid GeoJSON output.")

    version = nyc_geo_toolkit.__version__
    if not isinstance(version, str) or not version:
        raise SystemExit("Installed package did not expose a valid version string.")


if __name__ == "__main__":
    main()

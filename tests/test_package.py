from __future__ import annotations

import importlib.metadata
import importlib.resources

import nyc_geo_toolkit as root
from nyc_geo_toolkit import (
    BOROUGH_BROOKLYN,
    BoundaryCollection,
    BoundaryFeature,
    boundaries_to_geojson,
    list_boundary_layers,
    load_nyc_boundaries,
    normalize_borough_name,
    normalize_boundary_layer,
    normalize_boundary_value,
)


def _stable_version_prefix(version: str) -> str:
    return version.split("+", maxsplit=1)[0].split(".dev", maxsplit=1)[0]


def test_version() -> None:
    assert _stable_version_prefix(root.__version__) == _stable_version_prefix(
        importlib.metadata.version("nyc-geo-toolkit")
    )


def test_typed_package_marker_is_packaged() -> None:
    typing_marker = importlib.resources.files("nyc_geo_toolkit").joinpath("py.typed")
    assert typing_marker.is_file()


def test_public_contract() -> None:
    feature = BoundaryFeature(
        geography="borough",
        geography_value="QUEENS",
        geometry={"type": "Polygon", "coordinates": []},
        properties={"name": "Queens"},
    )
    collection = BoundaryCollection(geography="borough", features=(feature,))
    payload = boundaries_to_geojson(collection)

    assert normalize_borough_name("bk") == BOROUGH_BROOKLYN
    assert normalize_boundary_layer("zip code") == "zcta"
    assert normalize_boundary_value("borough", "Queens") == "QUEENS"
    assert "borough" in list_boundary_layers()
    assert (
        load_nyc_boundaries("borough", values="Queens").features[0].geography_value
        == "QUEENS"
    )
    assert payload["type"] == "FeatureCollection"

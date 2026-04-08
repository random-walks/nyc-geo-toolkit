"""Generate placeholder historical boundary files from existing 2020 data.

These files allow the temporal framework to be exercised end-to-end.
Run ``scripts/prepare_historical_boundaries.py`` locally to replace them
with real data downloaded from Census TIGER/Line and NYC Open Data.

Each placeholder reuses the 2020 geometry but adjusts property fields
to match the historical vintage schema.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "src" / "nyc_geo_toolkit" / "data" / "boundaries"
HIST_DIR = DATA_DIR / "historical"

BOROUGH_BY_CODE = {
    1: ("MANHATTAN", "061"),
    2: ("BRONX", "005"),
    3: ("BROOKLYN", "047"),
    4: ("QUEENS", "081"),
    5: ("STATEN ISLAND", "085"),
}


def _load(name: str) -> dict:
    with (DATA_DIR / name).open(encoding="utf-8") as f:
        return json.load(f)


def _write(name: str, data: dict) -> None:
    HIST_DIR.mkdir(parents=True, exist_ok=True)
    path = HIST_DIR / name
    path.write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")
    count = len(data.get("features", []))
    size_mb = path.stat().st_size / (1024 * 1024)
    print(f"  {name}: {count} features, {size_mb:.1f} MB")


def census_tracts_2010() -> None:
    """Derive 2010-vintage census tract placeholders from 2020 data."""
    src = _load("census_tract.geojson")
    features = []
    for f in src["features"]:
        p = f["properties"]
        geoid = p.get("geoid", "")
        borough_code = p.get("borough_code", 0)
        borough = p.get("borough", "")
        ct_code = p.get("ct2020", "")
        features.append(
            {
                "type": "Feature",
                "properties": {
                    "geography": "census_tract",
                    "geography_value": geoid,
                    "geoid": geoid,
                    "ct2010": ct_code,
                    "boroct2010": f"{borough_code}{ct_code}",
                    "borough": borough,
                    "borough_code": borough_code,
                    "county_fips": BOROUGH_BY_CODE.get(borough_code, ("", ""))[1],
                    "ct_label": p.get("ct_label", ""),
                    "name": p.get("name", ""),
                },
                "geometry": f["geometry"],
            }
        )
    _write(
        "census_tract_2010.geojson", {"type": "FeatureCollection", "features": features}
    )


def census_tracts_2000() -> None:
    """Derive 2000-vintage census tract placeholders from 2020 data."""
    src = _load("census_tract.geojson")
    features = []
    for f in src["features"]:
        p = f["properties"]
        geoid = p.get("geoid", "")
        borough_code = p.get("borough_code", 0)
        borough = p.get("borough", "")
        ct_code = p.get("ct2020", "")
        features.append(
            {
                "type": "Feature",
                "properties": {
                    "geography": "census_tract",
                    "geography_value": geoid,
                    "geoid": geoid,
                    "ct2000": ct_code,
                    "boroct2000": f"{borough_code}{ct_code}",
                    "borough": borough,
                    "borough_code": borough_code,
                    "county_fips": BOROUGH_BY_CODE.get(borough_code, ("", ""))[1],
                    "ct_label": p.get("ct_label", ""),
                    "name": p.get("name", ""),
                },
                "geometry": f["geometry"],
            }
        )
    _write(
        "census_tract_2000.geojson", {"type": "FeatureCollection", "features": features}
    )


def nta_2010() -> None:
    """Derive 2010-vintage NTA placeholders from 2020 data."""
    src = _load("neighborhood_tabulation_area.geojson")
    features = []
    for f in src["features"]:
        p = f["properties"]
        nta_code = p.get("nta2020", p.get("geography_value", ""))
        features.append(
            {
                "type": "Feature",
                "properties": {
                    "geography": "neighborhood_tabulation_area",
                    "geography_value": nta_code,
                    "nta2010": nta_code,
                    "name": p.get("name", ""),
                    "borough": p.get("borough", ""),
                },
                "geometry": f["geometry"],
            }
        )
    _write(
        "neighborhood_tabulation_area_2010.geojson",
        {"type": "FeatureCollection", "features": features},
    )


def council_districts_2013() -> None:
    """Derive 2013-vintage council district placeholders from current data."""
    src = _load("council_district.geojson")
    features = []
    for f in src["features"]:
        p = f["properties"]
        features.append(
            {
                "type": "Feature",
                "properties": {
                    "geography": "council_district",
                    "geography_value": p.get("geography_value", ""),
                    "district_number": p.get("district_number", 0),
                    "name": p.get("name", ""),
                },
                "geometry": f["geometry"],
            }
        )
    _write(
        "council_district_2013.geojson",
        {"type": "FeatureCollection", "features": features},
    )


def zcta_2010() -> None:
    """Derive 2010-vintage ZCTA placeholders from 2020 data."""
    src = _load("zcta.geojson")
    features = []
    for f in src["features"]:
        p = f["properties"]
        zcta_code = p.get("zcta", p.get("geography_value", ""))
        features.append(
            {
                "type": "Feature",
                "properties": {
                    "geography": "zcta",
                    "geography_value": zcta_code,
                    "zcta": zcta_code,
                    "name": f"ZCTA {zcta_code}",
                },
                "geometry": f["geometry"],
            }
        )
    _write("zcta_2010.geojson", {"type": "FeatureCollection", "features": features})


def main() -> None:
    print("Generating placeholder historical boundary files...")
    print("(Run scripts/prepare_historical_boundaries.py locally for real data)\n")
    census_tracts_2010()
    census_tracts_2000()
    nta_2010()
    council_districts_2013()
    zcta_2010()
    print("\nDone.")


if __name__ == "__main__":
    main()

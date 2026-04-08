"""Download real historical NYC boundary data from accessible GitHub sources.

Sources:
- Census tracts (2000, 2010): US Census Bureau CitySdk on GitHub
- NTAs (2010): NYC Health Department coronavirus-data on GitHub
- Council districts (2013): Already approximated from current (redistricting data)
- ZCTAs (2010): NYC Health Department coronavirus-data on GitHub

All data is public domain or openly licensed.
"""

from __future__ import annotations

import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "src" / "nyc_geo_toolkit" / "data" / "boundaries"
HIST_DIR = DATA_DIR / "historical"

NYC_COUNTY_FIPS = {"005", "047", "061", "081", "085"}
BOROUGH_BY_COUNTY_FIPS = {
    "005": ("BRONX", 2),
    "047": ("BROOKLYN", 3),
    "061": ("MANHATTAN", 1),
    "081": ("QUEENS", 4),
    "085": ("STATEN ISLAND", 5),
}

GITHUB_HEADERS = {"User-Agent": "nyc-geo-toolkit-data-prep"}


def _fetch_json(url: str) -> dict:
    """Download and parse JSON from a URL."""
    print(f"  Downloading {url}")
    req = Request(url, headers=GITHUB_HEADERS)
    with urlopen(req, timeout=120) as resp:  # noqa: S310
        return json.loads(resp.read())


def _write_geojson(name: str, data: dict) -> None:
    """Write a GeoJSON FeatureCollection to the historical directory."""
    HIST_DIR.mkdir(parents=True, exist_ok=True)
    path = HIST_DIR / name
    path.write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")
    count = len(data.get("features", []))
    size_mb = path.stat().st_size / (1024 * 1024)
    print(f"  Wrote {name}: {count} features, {size_mb:.1f} MB")


def prepare_census_tracts(year: int) -> None:
    """Download Census tracts from uscensusbureau/citysdk on GitHub."""
    print(f"\n=== Census Tracts {year} ===")
    url = f"https://raw.githubusercontent.com/uscensusbureau/citysdk/master/v2/GeoJSON/500k/{year}/36/tract.json"
    data = _fetch_json(url)

    # Determine property names based on year
    if year == 2010:
        county_col, tract_col, geoid_col = "COUNTY", "TRACT", "GEO_ID"
    else:  # 2000
        county_col, tract_col = "COUNTY", "TRACT"
        geoid_col = None

    features = []
    for f in data.get("features", []):
        p = f.get("properties", {})

        county_fips = p.get(county_col, "")
        if county_fips not in NYC_COUNTY_FIPS:
            continue

        borough_name, borough_code = BOROUGH_BY_COUNTY_FIPS[county_fips]
        tract_code = p.get(tract_col, "")

        # Build GEOID: state(36) + county(3) + tract(6)
        if geoid_col and p.get(geoid_col, "").startswith("1400000US"):
            geoid = p[geoid_col].replace("1400000US", "")
        else:
            geoid = f"36{county_fips}{tract_code}"

        ct_label = p.get("NAME", tract_code)

        features.append({
            "type": "Feature",
            "properties": {
                "geography": "census_tract",
                "geography_value": geoid,
                "geoid": geoid,
                f"ct{year}": tract_code,
                f"boroct{year}": f"{borough_code}{tract_code}",
                "borough": borough_name,
                "borough_code": borough_code,
                "county_fips": county_fips,
                "ct_label": ct_label,
                "name": f"Census Tract {ct_label}",
            },
            "geometry": f["geometry"],
        })

    print(f"  Filtered to {len(features)} NYC tracts (from {len(data['features'])} state-wide)")
    _write_geojson(f"census_tract_{year}.geojson", {
        "type": "FeatureCollection",
        "features": features,
    })
    return len(features)


def prepare_zcta_2010() -> None:
    """Download 2010 MODZCTAs from nychealth/coronavirus-data on GitHub."""
    print("\n=== ZCTAs 2010 ===")
    url = "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/Geography-resources/MODZCTA_2010_WGS1984.geo.json"
    data = _fetch_json(url)

    features = []
    for f in data.get("features", []):
        p = f.get("properties", {})
        modzcta = str(p.get("MODZCTA", "")).strip()
        if not modzcta or modzcta == "NA":
            continue
        label = p.get("label", modzcta)

        features.append({
            "type": "Feature",
            "properties": {
                "geography": "zcta",
                "geography_value": modzcta,
                "zcta": modzcta,
                "modzcta": modzcta,
                "label": label,
                "name": f"MODZCTA {modzcta}",
            },
            "geometry": f["geometry"],
        })

    print(f"  Processed {len(features)} ZCTAs")
    _write_geojson("zcta_2010.geojson", {
        "type": "FeatureCollection",
        "features": features,
    })
    return len(features)


def prepare_nta_2010() -> None:
    """Build 2010 NTAs from existing 2020 data.

    The 2010 NTA GeoJSON is not readily available on GitHub in a usable
    format. The 2020 NTA file is used as the basis. Run
    scripts/prepare_historical_boundaries.py locally (with network access
    to data.cityofnewyork.us) to replace this with real 2010 NTA data.
    """
    print("\n=== NTAs 2010 (from 2020 data — run prepare_historical_boundaries.py for real 2010 data) ===")
    with open(DATA_DIR / "neighborhood_tabulation_area.geojson", encoding="utf-8") as fh:
        src = json.load(fh)

    features = []
    for f in src["features"]:
        p = f["properties"]
        nta_code = p.get("nta2020", p.get("geography_value", ""))
        features.append({
            "type": "Feature",
            "properties": {
                "geography": "neighborhood_tabulation_area",
                "geography_value": nta_code,
                "nta2010": nta_code,
                "name": p.get("name", ""),
                "borough": p.get("borough", ""),
            },
            "geometry": f["geometry"],
        })

    _write_geojson("neighborhood_tabulation_area_2010.geojson", {
        "type": "FeatureCollection",
        "features": features,
    })
    return len(features)


def prepare_council_districts_2013() -> None:
    """Build 2013 council districts from current data.

    Pre-2023 council district GeoJSON is not readily available on GitHub.
    The current (2023) data is used as the basis. Run
    scripts/prepare_historical_boundaries.py locally (with network access
    to data.cityofnewyork.us) to replace this with real 2013 district lines.
    """
    print("\n=== Council Districts 2013 (from current data — run prepare_historical_boundaries.py for real 2013 lines) ===")
    with open(DATA_DIR / "council_district.geojson", encoding="utf-8") as fh:
        src = json.load(fh)

    features = []
    for f in src["features"]:
        p = f["properties"]
        features.append({
            "type": "Feature",
            "properties": {
                "geography": "council_district",
                "geography_value": p.get("geography_value", ""),
                "district_number": p.get("district_number", 0),
                "name": p.get("name", ""),
            },
            "geometry": f["geometry"],
        })

    _write_geojson("council_district_2013.geojson", {
        "type": "FeatureCollection",
        "features": features,
    })
    return len(features)


def main() -> None:
    """Download and prepare all historical boundary files."""
    print("Downloading historical NYC boundary data...\n")
    HIST_DIR.mkdir(parents=True, exist_ok=True)

    counts = {}
    counts["census_tract_2010"] = prepare_census_tracts(2010)
    counts["census_tract_2000"] = prepare_census_tracts(2000)
    counts["zcta_2010"] = prepare_zcta_2010()
    counts["neighborhood_tabulation_area_2010"] = prepare_nta_2010()
    counts["council_district_2013"] = prepare_council_districts_2013()

    print("\n=== Summary ===")
    for name, count in counts.items():
        path = HIST_DIR / f"{name}.geojson"
        size_mb = path.stat().st_size / (1024 * 1024)
        print(f"  {name}: {count} features, {size_mb:.1f} MB")
    print("\nDone. Census tracts and ZCTAs are real data from official sources.")
    print("NTAs and council districts derived from current data —")
    print("run scripts/prepare_historical_boundaries.py locally for real historical versions.")


if __name__ == "__main__":
    main()

"""Download and prepare historical NYC boundary GeoJSON files.

This script fetches boundary data from the US Census Bureau TIGER/Line
shapefiles and NYC Open Data, then converts and normalizes them to match
the property schema used by the packaged GeoJSON files.

Requirements:
    geopandas, requests (install via `pip install geopandas requests`)

Usage:
    python scripts/prepare_historical_boundaries.py
"""

from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path
from urllib.request import urlopen

import geopandas as gpd
from shapely.geometry import mapping, shape

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "src" / "nyc_geo_toolkit" / "data" / "boundaries" / "historical"

# NYC county FIPS codes (within New York State FIPS 36)
NYC_COUNTY_FIPS = {"005", "047", "061", "081", "085"}
NYC_COUNTY_FIPS_FULL = {f"36{c}" for c in NYC_COUNTY_FIPS}

BOROUGH_BY_COUNTY_FIPS = {
    "005": ("BRONX", 2),
    "047": ("BROOKLYN", 3),
    "061": ("MANHATTAN", 1),
    "081": ("QUEENS", 4),
    "085": ("STATEN ISLAND", 5),
}


def _download_shapefile_zip(url: str) -> gpd.GeoDataFrame:
    """Download a zipped shapefile and return as GeoDataFrame."""
    print(f"  Downloading {url}")
    with urlopen(url) as response:
        data = response.read()
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        zf.extractall("/tmp/shp_extract")
    shp_files = list(Path("/tmp/shp_extract").rglob("*.shp"))
    if not shp_files:
        raise FileNotFoundError("No .shp file found in archive")
    return gpd.read_file(shp_files[0])


def _download_geojson(url: str) -> gpd.GeoDataFrame:
    """Download a GeoJSON file and return as GeoDataFrame."""
    print(f"  Downloading {url}")
    return gpd.read_file(url)


def _write_geojson(features: list[dict], output_path: Path) -> None:
    """Write a GeoJSON FeatureCollection."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    collection = {"type": "FeatureCollection", "features": features}
    output_path.write_text(
        json.dumps(collection, separators=(",", ":")), encoding="utf-8"
    )
    print(f"  Wrote {output_path} ({len(features)} features)")


def _simplify_geometry(geom: dict, tolerance: float = 0.0001) -> dict:
    """Simplify a GeoJSON geometry using Douglas-Peucker."""
    return dict(mapping(shape(geom).simplify(tolerance, preserve_topology=True)))


def prepare_census_tracts_2010() -> None:
    """Prepare 2010 Census tract boundaries for NYC."""
    print("\n=== Census Tracts 2010 ===")
    url = (
        "https://www2.census.gov/geo/tiger/TIGER2010/TRACT/2010/tl_2010_36_tract10.zip"
    )
    gdf = _download_shapefile_zip(url)

    # Filter to NYC counties
    gdf = gdf[gdf["COUNTYFP10"].isin(NYC_COUNTY_FIPS)].copy()
    print(f"  Filtered to {len(gdf)} NYC tracts")

    features = []
    for _, row in gdf.iterrows():
        county_fips = row["COUNTYFP10"]
        borough_name, borough_code = BOROUGH_BY_COUNTY_FIPS[county_fips]
        geoid = row["GEOID10"]
        tract_code = row["TRACTCE10"]
        ct_label = (
            f"{int(tract_code[:4])}.{tract_code[4:]}"
            if len(tract_code) == 6
            else tract_code
        )

        geom = json.loads(gpd.GeoSeries([row.geometry]).to_json())["features"][0][
            "geometry"
        ]
        geom = _simplify_geometry(geom)

        features.append(
            {
                "type": "Feature",
                "properties": {
                    "geography": "census_tract",
                    "geography_value": geoid,
                    "geoid": geoid,
                    "ct2010": tract_code,
                    "boroct2010": f"{borough_code}{tract_code}",
                    "borough": borough_name,
                    "borough_code": borough_code,
                    "county_fips": county_fips,
                    "ct_label": ct_label,
                    "name": f"Census Tract {ct_label}",
                },
                "geometry": geom,
            }
        )

    _write_geojson(features, OUTPUT_DIR / "census_tract_2010.geojson")


def prepare_census_tracts_2000() -> None:
    """Prepare 2000 Census tract boundaries for NYC."""
    print("\n=== Census Tracts 2000 ===")
    url = (
        "https://www2.census.gov/geo/tiger/TIGER2010/TRACT/2000/tl_2010_36_tract00.zip"
    )
    gdf = _download_shapefile_zip(url)

    # Filter to NYC counties
    gdf = gdf[gdf["COUNTYFP00"].isin(NYC_COUNTY_FIPS)].copy()
    print(f"  Filtered to {len(gdf)} NYC tracts")

    features = []
    for _, row in gdf.iterrows():
        county_fips = row["COUNTYFP00"]
        borough_name, borough_code = BOROUGH_BY_COUNTY_FIPS[county_fips]
        geoid = row["CTIDFP00"]
        tract_code = row["TRACTCE00"]
        ct_label = (
            f"{int(tract_code[:4])}.{tract_code[4:]}"
            if len(tract_code) == 6
            else tract_code
        )

        geom = json.loads(gpd.GeoSeries([row.geometry]).to_json())["features"][0][
            "geometry"
        ]
        geom = _simplify_geometry(geom)

        features.append(
            {
                "type": "Feature",
                "properties": {
                    "geography": "census_tract",
                    "geography_value": geoid,
                    "geoid": geoid,
                    "ct2000": tract_code,
                    "boroct2000": f"{borough_code}{tract_code}",
                    "borough": borough_name,
                    "borough_code": borough_code,
                    "county_fips": county_fips,
                    "ct_label": ct_label,
                    "name": f"Census Tract {ct_label}",
                },
                "geometry": geom,
            }
        )

    _write_geojson(features, OUTPUT_DIR / "census_tract_2000.geojson")


def prepare_nta_2010() -> None:
    """Prepare 2010 Neighborhood Tabulation Area boundaries."""
    print("\n=== NTAs 2010 ===")
    url = "https://data.cityofnewyork.us/api/geospatial/cpf4-rkhq?method=export&type=GeoJSON"
    gdf = _download_geojson(url)
    print(f"  Downloaded {len(gdf)} features")

    # Identify the NTA code column
    nta_col = None
    for col in gdf.columns:
        if (
            "ntacode" in col.lower()
            or "nta_code" in col.lower()
            or col.lower() == "ntacode"
        ):
            nta_col = col
            break
    if nta_col is None:
        # Fallback: look for columns containing NTA-like codes
        for col in gdf.columns:
            if col.lower().startswith("nta"):
                nta_col = col
                break
    if nta_col is None:
        print(f"  Available columns: {list(gdf.columns)}")
        raise ValueError("Could not find NTA code column")

    # Identify borough column
    boro_col = None
    for col in gdf.columns:
        if "boro" in col.lower() and "code" not in col.lower():
            boro_col = col
            break

    # Identify name column
    name_col = None
    for col in gdf.columns:
        if "ntaname" in col.lower() or "nta_name" in col.lower():
            name_col = col
            break

    borough_name_map = {
        "1": "MANHATTAN",
        "2": "BRONX",
        "3": "BROOKLYN",
        "4": "QUEENS",
        "5": "STATEN ISLAND",
        "MN": "MANHATTAN",
        "BX": "BRONX",
        "BK": "BROOKLYN",
        "QN": "QUEENS",
        "SI": "STATEN ISLAND",
        "Manhattan": "MANHATTAN",
        "Bronx": "BRONX",
        "Brooklyn": "BROOKLYN",
        "Queens": "QUEENS",
        "Staten Island": "STATEN ISLAND",
    }

    features = []
    for _, row in gdf.iterrows():
        nta_code = str(row[nta_col]).strip()
        # Skip park/cemetery/airport NTAs (codes ending in 99 or starting with special chars)
        if not nta_code or len(nta_code) < 4:
            continue

        borough = ""
        if boro_col is not None:
            raw_boro = str(row[boro_col]).strip()
            borough = borough_name_map.get(raw_boro, raw_boro.upper())
        if not borough:
            # Infer from NTA code prefix
            prefix = nta_code[:2]
            borough = borough_name_map.get(prefix, "")

        name = str(row[name_col]).strip() if name_col else nta_code

        geom = json.loads(gpd.GeoSeries([row.geometry]).to_json())["features"][0][
            "geometry"
        ]
        geom = _simplify_geometry(geom)

        features.append(
            {
                "type": "Feature",
                "properties": {
                    "geography": "neighborhood_tabulation_area",
                    "geography_value": nta_code,
                    "nta2010": nta_code,
                    "name": name,
                    "borough": borough,
                },
                "geometry": geom,
            }
        )

    _write_geojson(features, OUTPUT_DIR / "neighborhood_tabulation_area_2010.geojson")


def prepare_council_districts_2013() -> None:
    """Prepare 2013 City Council district boundaries."""
    print("\n=== Council Districts 2013 ===")
    url = "https://data.cityofnewyork.us/api/geospatial/yusd-j4xi?method=export&type=GeoJSON"
    gdf = _download_geojson(url)
    print(f"  Downloaded {len(gdf)} features")

    # Identify the district column
    dist_col = None
    for col in gdf.columns:
        if (
            "coundist" in col.lower()
            or "council" in col.lower()
            or "dist" in col.lower()
        ):
            dist_col = col
            break
    if dist_col is None:
        print(f"  Available columns: {list(gdf.columns)}")
        # Try to find any numeric column that could be district numbers
        for col in gdf.columns:
            if col.lower() != "geometry" and gdf[col].dtype in ("int64", "float64"):
                dist_col = col
                break
    if dist_col is None:
        raise ValueError("Could not find district number column")

    features = []
    for _, row in gdf.iterrows():
        district_number = int(row[dist_col])
        if not 1 <= district_number <= 51:
            continue

        geom = json.loads(gpd.GeoSeries([row.geometry]).to_json())["features"][0][
            "geometry"
        ]
        geom = _simplify_geometry(geom)

        features.append(
            {
                "type": "Feature",
                "properties": {
                    "geography": "council_district",
                    "geography_value": f"{district_number:02d}",
                    "district_number": district_number,
                    "name": f"City Council District {district_number}",
                },
                "geometry": geom,
            }
        )

    features.sort(key=lambda f: int(f["properties"]["geography_value"]))
    _write_geojson(features, OUTPUT_DIR / "council_district_2013.geojson")


def prepare_zcta_2010() -> None:
    """Prepare 2010 ZCTA boundaries for NYC."""
    print("\n=== ZCTAs 2010 ===")
    url = (
        "https://www2.census.gov/geo/tiger/TIGER2010/ZCTA5/2010/tl_2010_36_zcta510.zip"
    )

    try:
        gdf = _download_shapefile_zip(url)
    except (FileNotFoundError, OSError):
        # Fallback: national ZCTA file
        print("  State-level not found, trying national file...")
        url = "https://www2.census.gov/geo/tiger/TIGER2010/ZCTA5/2010/tl_2010_us_zcta510.zip"
        gdf = _download_shapefile_zip(url)

    # Filter to NYC area ZCTAs (10000-11999 range covers NYC)
    zcta_col = None
    for col in gdf.columns:
        if "zcta" in col.lower() or col.lower() == "geoid10":
            zcta_col = col
            break
    if zcta_col is None:
        print(f"  Available columns: {list(gdf.columns)}")
        raise ValueError("Could not find ZCTA column")

    # Filter to NYC ZIP code ranges
    nyc_zips: set[str] = set()
    # Load current ZCTA file to get the list of NYC ZCTAs
    zcta_path = (
        ROOT / "src" / "nyc_geo_toolkit" / "data" / "boundaries" / "zcta.geojson"
    )
    with zcta_path.open() as f:
        current = json.load(f)
    for feature in current["features"]:
        zcta = feature["properties"].get("zcta") or feature["properties"].get(
            "geography_value"
        )
        if zcta:
            nyc_zips.add(str(zcta))

    # Also add common NYC ZIP ranges
    for z in range(10001, 10300):
        nyc_zips.add(str(z))
    for z in range(10301, 10500):
        nyc_zips.add(str(z))
    for z in range(10451, 10476):
        nyc_zips.add(str(z))
    for z in range(11001, 11700):
        nyc_zips.add(str(z))

    gdf["_zcta"] = gdf[zcta_col].astype(str).str.strip()
    gdf = gdf[gdf["_zcta"].isin(nyc_zips)].copy()
    print(f"  Filtered to {len(gdf)} NYC ZCTAs")

    features = []
    for _, row in gdf.iterrows():
        zcta_code = str(row["_zcta"]).strip()

        geom = json.loads(gpd.GeoSeries([row.geometry]).to_json())["features"][0][
            "geometry"
        ]
        geom = _simplify_geometry(geom)

        features.append(
            {
                "type": "Feature",
                "properties": {
                    "geography": "zcta",
                    "geography_value": zcta_code,
                    "zcta": zcta_code,
                    "name": f"ZCTA {zcta_code}",
                },
                "geometry": geom,
            }
        )

    _write_geojson(features, OUTPUT_DIR / "zcta_2010.geojson")


def main() -> None:
    """Prepare all historical boundary files."""
    print("Preparing historical NYC boundary data...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    prepare_census_tracts_2010()
    prepare_census_tracts_2000()
    prepare_nta_2010()
    prepare_council_districts_2013()
    prepare_zcta_2010()

    print("\n=== Summary ===")
    for path in sorted(OUTPUT_DIR.glob("*.geojson")):
        size_mb = path.stat().st_size / (1024 * 1024)
        with path.open() as f:
            data = json.load(f)
        count = len(data.get("features", []))
        print(f"  {path.name}: {count} features, {size_mb:.1f} MB")


if __name__ == "__main__":
    main()

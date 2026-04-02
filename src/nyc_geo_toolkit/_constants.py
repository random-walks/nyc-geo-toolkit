"""Public constants and canonical value catalogs for NYC geography helpers."""

from __future__ import annotations

from typing import Final

BoroughName = str
SUPPORTED_BOUNDARY_GEOGRAPHIES: Final[tuple[str, ...]] = (
    "borough",
    "community_district",
    "council_district",
    "neighborhood_tabulation_area",
    "census_tract",
    "zcta",
)
BOROUGH_BRONX: Final[BoroughName] = "BRONX"
BOROUGH_BROOKLYN: Final[BoroughName] = "BROOKLYN"
BOROUGH_MANHATTAN: Final[BoroughName] = "MANHATTAN"
BOROUGH_QUEENS: Final[BoroughName] = "QUEENS"
BOROUGH_STATEN_ISLAND: Final[BoroughName] = "STATEN ISLAND"
SUPPORTED_BOROUGHS: Final[tuple[BoroughName, ...]] = (
    BOROUGH_BRONX,
    BOROUGH_BROOKLYN,
    BOROUGH_MANHATTAN,
    BOROUGH_QUEENS,
    BOROUGH_STATEN_ISLAND,
)
_BOROUGH_ALIASES: Final[dict[str, BoroughName]] = {
    "bronx": BOROUGH_BRONX,
    "bx": BOROUGH_BRONX,
    "brooklyn": BOROUGH_BROOKLYN,
    "bk": BOROUGH_BROOKLYN,
    "kings": BOROUGH_BROOKLYN,
    "manhattan": BOROUGH_MANHATTAN,
    "mn": BOROUGH_MANHATTAN,
    "new york": BOROUGH_MANHATTAN,
    "new york county": BOROUGH_MANHATTAN,
    "queens": BOROUGH_QUEENS,
    "qn": BOROUGH_QUEENS,
    "staten island": BOROUGH_STATEN_ISLAND,
    "si": BOROUGH_STATEN_ISLAND,
    "richmond": BOROUGH_STATEN_ISLAND,
}

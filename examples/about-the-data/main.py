"""Kitchen-sink visualization of every boundary layer and spatial helper."""

from __future__ import annotations

import contextlib
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from shapely.geometry import Polygon, shape

from nyc_geo_toolkit import (
    add_osm_basemap,
    build_circle_polygon,
    clip_boundaries_to_bbox,
    haversine_distance_meters,
    load_nyc_boundaries,
    load_nyc_boundaries_geodataframe,
    to_web_mercator,
    walk_radius_meters,
)


def _try_add_basemap(ax: plt.Axes) -> None:
    """Add basemap tiles, silently skipping if network is unavailable."""
    with contextlib.suppress(Exception):
        add_osm_basemap(ax)


ROOT = Path(__file__).resolve().parent
ARTIFACTS_DIR = ROOT / "artifacts"
REPORTS_DIR = ROOT / "reports"

# NYC-inspired borough color palette
BOROUGH_COLORS = {
    "BRONX": "#e6550d",
    "BROOKLYN": "#3182bd",
    "MANHATTAN": "#31a354",
    "QUEENS": "#756bb1",
    "STATEN ISLAND": "#636363",
}

# Sequential colormaps per panel
CD_CMAP = "Set3"
COUNCIL_CMAP = "tab20"
NTA_CMAP = "Pastel1"
TRACT_CMAP = "YlOrRd"


def artifact_path(filename: str) -> Path:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    return ARTIFACTS_DIR / filename


def report_path(filename: str) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    return REPORTS_DIR / filename


def _clipped_tracts_gdf() -> gpd.GeoDataFrame:
    """Load census tracts clipped to a Manhattan bounding box."""
    tracts = load_nyc_boundaries("census_tract")
    clipped = clip_boundaries_to_bbox(
        tracts,
        min_longitude=-74.02,
        min_latitude=40.70,
        max_longitude=-73.93,
        max_latitude=40.80,
    )
    rows = [
        {
            "geography_value": f.geography_value,
            "geometry": shape(f.geometry),
        }
        for f in clipped.features
    ]
    return gpd.GeoDataFrame(rows, geometry="geometry", crs="EPSG:4326")


def _geodesy_gdf() -> gpd.GeoDataFrame:
    """Build walk-radius circles around three NYC landmarks."""
    landmarks = {
        "Times Square": (40.7580, -73.9855),
        "City Hall": (40.7128, -74.0060),
        "Prospect Park": (40.6602, -73.9690),
    }
    radius = walk_radius_meters(10)
    rows = []
    for name, (lat, lon) in landmarks.items():
        coords = build_circle_polygon(lat, lon, radius)
        rows.append({"name": name, "geometry": Polygon(coords), "lat": lat, "lon": lon})
    return gpd.GeoDataFrame(rows, geometry="geometry", crs="EPSG:4326")


def _clean_map_axes(ax: plt.Axes) -> None:
    """Remove tick labels and tighten axes for a clean map panel."""
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_linewidth(0.3)
        spine.set_color("#cccccc")


def plot_boroughs(ax: plt.Axes) -> int:
    """Panel 1: all five boroughs with basemap."""
    gdf = to_web_mercator(load_nyc_boundaries_geodataframe("borough"))
    gdf["color"] = gdf["geography_value"].map(BOROUGH_COLORS)
    gdf.plot(ax=ax, color=gdf["color"], edgecolor="white", linewidth=0.6, alpha=0.75)
    _try_add_basemap(ax)

    for _, row in gdf.iterrows():
        centroid = row.geometry.centroid
        ax.annotate(
            row["geography_value"].title(),
            xy=(centroid.x, centroid.y),
            ha="center",
            va="center",
            fontsize=6,
            fontweight="bold",
            color="#222222",
        )
    ax.set_title("Boroughs", fontsize=10, fontweight="bold", pad=6)
    _clean_map_axes(ax)
    return len(gdf)


def plot_community_districts(ax: plt.Axes) -> int:
    """Panel 2: all 71 community districts."""
    gdf = load_nyc_boundaries_geodataframe("community_district")
    gdf.plot(
        ax=ax,
        column="geography_value",
        cmap=CD_CMAP,
        edgecolor="white",
        linewidth=0.3,
        alpha=0.85,
        legend=False,
    )
    ax.set_title("Community Districts", fontsize=10, fontweight="bold", pad=6)
    _clean_map_axes(ax)
    ax.set_aspect("equal")
    return len(gdf)


def plot_council_districts(ax: plt.Axes) -> int:
    """Panel 3: all 51 council districts."""
    gdf = load_nyc_boundaries_geodataframe("council_district")
    gdf.plot(
        ax=ax,
        column="geography_value",
        cmap=COUNCIL_CMAP,
        edgecolor="white",
        linewidth=0.3,
        alpha=0.85,
        legend=False,
    )
    ax.set_title("Council Districts", fontsize=10, fontweight="bold", pad=6)
    _clean_map_axes(ax)
    ax.set_aspect("equal")
    return len(gdf)


def plot_ntas(ax: plt.Axes) -> int:
    """Panel 4: neighborhood tabulation areas."""
    gdf = load_nyc_boundaries_geodataframe("neighborhood_tabulation_area")
    gdf.plot(
        ax=ax,
        column="geography_value",
        cmap=NTA_CMAP,
        edgecolor="#666666",
        linewidth=0.2,
        alpha=0.85,
        legend=False,
    )
    ax.set_title("Neighborhood Tabulation Areas", fontsize=10, fontweight="bold", pad=6)
    _clean_map_axes(ax)
    ax.set_aspect("equal")
    return len(gdf)


def plot_clipped_tracts(ax: plt.Axes) -> int:
    """Panel 5: census tracts clipped to Manhattan."""
    gdf = _clipped_tracts_gdf()
    gdf.plot(
        ax=ax,
        column="geography_value",
        cmap=TRACT_CMAP,
        edgecolor="white",
        linewidth=0.2,
        alpha=0.9,
        legend=False,
    )
    ax.set_title(
        "Census Tracts (Manhattan clip)", fontsize=10, fontweight="bold", pad=6
    )
    _clean_map_axes(ax)
    ax.set_aspect("equal")
    return len(gdf)


def plot_geodesy(ax: plt.Axes) -> int:
    """Panel 6: walk-radius circles + distance arrow on basemap."""
    circles_gdf = to_web_mercator(_geodesy_gdf())
    boroughs_gdf = to_web_mercator(load_nyc_boundaries_geodataframe("borough"))

    boroughs_gdf.plot(ax=ax, color="#e0e0e0", edgecolor="white", linewidth=0.4)
    circles_gdf.plot(
        ax=ax, color="#ff7f0e", edgecolor="#d62728", linewidth=1.2, alpha=0.4
    )
    _try_add_basemap(ax)

    for _, row in circles_gdf.iterrows():
        centroid = row.geometry.centroid
        ax.annotate(
            row["name"],
            xy=(centroid.x, centroid.y),
            ha="center",
            va="bottom",
            fontsize=5.5,
            fontweight="bold",
            color="#333333",
        )

    # Distance annotation between Times Square and City Hall
    ts = circles_gdf[circles_gdf["name"] == "Times Square"].iloc[0]
    ch = circles_gdf[circles_gdf["name"] == "City Hall"].iloc[0]
    dist_m = haversine_distance_meters(ts["lat"], ts["lon"], ch["lat"], ch["lon"])
    arrow = FancyArrowPatch(
        (ts.geometry.centroid.x, ts.geometry.centroid.y),
        (ch.geometry.centroid.x, ch.geometry.centroid.y),
        arrowstyle="<->",
        color="#d62728",
        linewidth=1.0,
        mutation_scale=8,
    )
    ax.add_patch(arrow)
    mid_x = (ts.geometry.centroid.x + ch.geometry.centroid.x) / 2
    mid_y = (ts.geometry.centroid.y + ch.geometry.centroid.y) / 2
    ax.annotate(
        f"{dist_m / 1000:.1f} km",
        xy=(mid_x, mid_y),
        ha="center",
        va="bottom",
        fontsize=6,
        color="#d62728",
        fontweight="bold",
        bbox={
            "boxstyle": "round,pad=0.2",
            "facecolor": "white",
            "alpha": 0.8,
            "edgecolor": "none",
        },
    )

    ax.set_title("Geodesy Helpers (10-min walk)", fontsize=10, fontweight="bold", pad=6)
    _clean_map_axes(ax)
    return len(circles_gdf)


def main() -> None:
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    fig.suptitle(
        "nyc-geo-toolkit \u2014 Boundary Layers & Spatial Helpers",
        fontsize=14,
        fontweight="bold",
        y=0.98,
    )

    counts = {}
    counts["boroughs"] = plot_boroughs(axes[0, 0])
    counts["community_districts"] = plot_community_districts(axes[0, 1])
    counts["council_districts"] = plot_council_districts(axes[0, 2])
    counts["ntas"] = plot_ntas(axes[1, 0])
    counts["census_tracts_clipped"] = plot_clipped_tracts(axes[1, 1])
    counts["geodesy_circles"] = plot_geodesy(axes[1, 2])

    fig.tight_layout(rect=(0, 0, 1, 0.95), h_pad=1.5, w_pad=1.5)

    cover_path = artifact_path("nyc-geo-toolkit-cover.png")
    fig.savefig(cover_path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Wrote {cover_path}")

    report = f"""# About the Data Tearsheet

## Summary

This example generates a multi-panel cover figure demonstrating every packaged
boundary layer and spatial helper in `nyc-geo-toolkit`.

## Panels

| Panel | Layer | Features |
|-------|-------|----------|
| Boroughs | borough | {counts["boroughs"]} |
| Community Districts | community_district | {counts["community_districts"]} |
| Council Districts | council_district | {counts["council_districts"]} |
| NTAs | neighborhood_tabulation_area | {counts["ntas"]} |
| Census Tracts (clipped) | census_tract | {counts["census_tracts_clipped"]} |
| Geodesy Helpers | n/a | {counts["geodesy_circles"]} circles |

## API demonstrated

- `load_nyc_boundaries_geodataframe()`
- `load_nyc_boundaries()` + `clip_boundaries_to_bbox()`
- `to_web_mercator()` + `add_osm_basemap()`
- `build_circle_polygon()` + `walk_radius_meters()`
- `haversine_distance_meters()`

## Artifact

- Cover figure: `artifacts/nyc-geo-toolkit-cover.png`
"""
    tearsheet_path = report_path("about-the-data-tearsheet.md")
    tearsheet_path.write_text(report, encoding="utf-8")
    print(f"Wrote {tearsheet_path}")


if __name__ == "__main__":
    main()

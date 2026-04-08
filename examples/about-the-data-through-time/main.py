"""Temporal boundary comparison — visualize how NYC geographies change over time."""

from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import shape

from nyc_geo_toolkit import (
    describe_layer,
    list_available_vintages,
    load_nyc_boundaries,
    vintage_for_census_decade,
)

ROOT = Path(__file__).resolve().parent
ARTIFACTS_DIR = ROOT / "artifacts"
REPORTS_DIR = ROOT / "reports"


def artifact_path(filename: str) -> Path:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    return ARTIFACTS_DIR / filename


def report_path(filename: str) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    return REPORTS_DIR / filename


def _boundaries_to_gdf(layer: str, vintage: int) -> gpd.GeoDataFrame:
    """Load a boundary layer at a specific vintage as a GeoDataFrame."""
    boundaries = load_nyc_boundaries(layer, vintage=vintage)
    rows = [
        {
            "geography_value": f.geography_value,
            "geometry": shape(f.geometry),
            **f.properties,
        }
        for f in boundaries.features
    ]
    return gpd.GeoDataFrame(rows, geometry="geometry", crs="EPSG:4326")


def _clean_map_axes(ax: plt.Axes) -> None:
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_linewidth(0.3)
        spine.set_color("#cccccc")


def plot_vintage_comparison(
    layer: str,
    vintages: tuple[int, ...],
    _fig: plt.Figure,
    axes: list[plt.Axes],
    cmap: str = "Set3",
) -> dict[int, int]:
    """Plot one boundary layer across multiple vintages side by side."""
    counts = {}
    for vintage, ax in zip(vintages, axes, strict=True):
        gdf = _boundaries_to_gdf(layer, vintage)
        counts[vintage] = len(gdf)
        gdf.plot(
            ax=ax,
            column="geography_value",
            cmap=cmap,
            edgecolor="white",
            linewidth=0.3,
            alpha=0.85,
            legend=False,
        )
        spec = describe_layer(layer, vintage=vintage)
        ax.set_title(
            f"{spec.display_name}\n({len(gdf)} features)",
            fontsize=8,
            fontweight="bold",
            pad=6,
        )
        _clean_map_axes(ax)
        ax.set_aspect("equal")
    return counts


def main() -> None:
    # Show all available vintages
    all_vintages = list_available_vintages()
    print("Available vintages per layer:")
    for layer, vintages in all_vintages.items():
        print(f"  {layer}: {vintages}")
    print()

    # Show census decade mapping for council districts
    for decade in (2010, 2020):
        actual = vintage_for_census_decade("council_district", decade)
        print(f"  council_district decade {decade} -> vintage {actual}")
    print()

    # Create comparison figure: 3 rows x 2-3 columns
    # Row 1: Census tracts (2000 vs 2010 vs 2020)
    # Row 2: NTAs (2010 vs 2020)
    # Row 3: Council districts (2013 vs 2023)
    fig = plt.figure(figsize=(16, 14))
    fig.suptitle(
        "NYC Boundaries Through Time",
        fontsize=16,
        fontweight="bold",
        y=0.98,
    )

    # Row 1: Census tracts — clip to Manhattan for readability
    ax1 = fig.add_subplot(3, 3, 1)
    ax2 = fig.add_subplot(3, 3, 2)
    ax3 = fig.add_subplot(3, 3, 3)
    tract_counts = plot_vintage_comparison(
        "census_tract", (2000, 2010, 2020), fig, [ax1, ax2, ax3], cmap="YlOrRd"
    )

    # Row 2: NTAs (2 panels, leave third empty)
    ax4 = fig.add_subplot(3, 3, 4)
    ax5 = fig.add_subplot(3, 3, 5)
    nta_counts = plot_vintage_comparison(
        "neighborhood_tabulation_area", (2010, 2020), fig, [ax4, ax5], cmap="Pastel1"
    )
    ax6 = fig.add_subplot(3, 3, 6)
    ax6.axis("off")
    ax6.text(
        0.5,
        0.5,
        "NTA boundaries were\nredesigned for the\n2020 Census cycle",
        ha="center",
        va="center",
        fontsize=10,
        color="#666666",
        style="italic",
    )

    # Row 3: Council districts (2 panels, leave third for info)
    ax7 = fig.add_subplot(3, 3, 7)
    ax8 = fig.add_subplot(3, 3, 8)
    cd_counts = plot_vintage_comparison(
        "council_district", (2013, 2023), fig, [ax7, ax8], cmap="tab20"
    )
    ax9 = fig.add_subplot(3, 3, 9)
    ax9.axis("off")
    ax9.text(
        0.5,
        0.5,
        "Council districts are\nredistricted after each\ndecennial census",
        ha="center",
        va="center",
        fontsize=10,
        color="#666666",
        style="italic",
    )

    fig.tight_layout(rect=(0, 0, 1, 0.95), h_pad=2.0, w_pad=1.5)

    cover_path = artifact_path("boundaries-through-time.png")
    fig.savefig(cover_path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Wrote {cover_path}")

    # Generate tearsheet
    report = """# Boundaries Through Time Tearsheet

## Summary

This example demonstrates the temporal/vintage features of `nyc-geo-toolkit`.
NYC geographic boundaries change over time — census tracts are redrawn each
decade, NTAs are redesigned, and council districts are redistricted.

## Vintage Coverage

| Layer | Available Vintages | Default |
|-------|--------------------|---------|
"""
    for layer, vintages in all_vintages.items():
        spec = describe_layer(layer)
        report += (
            f"| {layer} | {', '.join(str(v) for v in vintages)} | {spec.vintage} |\n"
        )

    report += """
## Panels

| Row | Layer | Vintages Shown | Feature Counts |
|-----|-------|---------------|----------------|
"""
    report += f"| 1 | census_tract | 2000, 2010, 2020 | {tract_counts} |\n"
    report += f"| 2 | neighborhood_tabulation_area | 2010, 2020 | {nta_counts} |\n"
    report += f"| 3 | council_district | 2013, 2023 | {cd_counts} |\n"

    report += """
## API Demonstrated

- `list_available_vintages()` — discover what vintages exist per layer
- `load_nyc_boundaries(layer, vintage=YEAR)` — load a specific vintage
- `describe_layer(layer, vintage=YEAR)` — get metadata about a vintage
- `vintage_for_census_decade(layer, decade)` — map census decade to actual vintage

## Data Sources

All boundary data is packaged with the toolkit. Sources include:
- US Census Bureau TIGER/Line shapefiles (census tracts, ZCTAs)
- NYC Dept of City Planning / NYC Open Data (NTAs, community districts, boroughs)
- NYC Districting Commission (council districts)

## Artifact

- Comparison figure: `artifacts/boundaries-through-time.png`
"""

    tearsheet_path = report_path("through-time-tearsheet.md")
    tearsheet_path.write_text(report, encoding="utf-8")
    print(f"Wrote {tearsheet_path}")


if __name__ == "__main__":
    main()

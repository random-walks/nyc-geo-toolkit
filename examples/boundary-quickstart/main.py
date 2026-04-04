from __future__ import annotations

import json
from pathlib import Path

from nyc_geo_toolkit import (
    boundaries_to_geojson,
    list_boundary_layers,
    load_nyc_boundaries,
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


def main() -> None:
    queens = load_nyc_boundaries("borough", values="Queens")
    geojson_payload = boundaries_to_geojson(queens)
    geojson_path = artifact_path("queens-borough.geojson")
    geojson_path.write_text(
        f"{json.dumps(geojson_payload, indent=2)}\n", encoding="utf-8"
    )

    report = f"""# Boundary Quickstart Tearsheet

## Summary

- Available boundary layers: {len(list_boundary_layers())}
- Loaded features: {len(queens.features)}
- Geography value: {queens.features[0].geography_value}

## Artifact

- GeoJSON: `{geojson_path.name}`
"""
    tearsheet_path = report_path("boundary-quickstart-tearsheet.md")
    tearsheet_path.write_text(report, encoding="utf-8")

    print(f"Wrote {geojson_path}")
    print(f"Wrote {tearsheet_path}")


if __name__ == "__main__":
    main()

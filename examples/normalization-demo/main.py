from __future__ import annotations

import json
from pathlib import Path

from nyc_geo_toolkit import normalize_boundary_layer, normalize_boundary_values

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
    raw_layer = "Community Districts"
    raw_values = ["bk 01", "mn 03", "queens 07"]
    normalized_layer = normalize_boundary_layer(raw_layer)
    normalized_values = normalize_boundary_values(normalized_layer, raw_values)

    artifact = {
        "raw_layer": raw_layer,
        "normalized_layer": normalized_layer,
        "raw_values": raw_values,
        "normalized_values": normalized_values,
    }
    artifact_pathname = artifact_path("normalized-values.json")
    artifact_pathname.write_text(
        f"{json.dumps(artifact, indent=2)}\n", encoding="utf-8"
    )

    report = f"""# Normalization Demo Tearsheet

## Summary

- Raw layer: `{raw_layer}`
- Normalized layer: `{normalized_layer}`
- Values normalized: {len(normalized_values)}

## Artifact

- JSON: `{artifact_pathname.name}`
"""
    tearsheet_path = report_path("normalization-demo-tearsheet.md")
    tearsheet_path.write_text(report, encoding="utf-8")

    print(f"Wrote {artifact_pathname}")
    print(f"Wrote {tearsheet_path}")


if __name__ == "__main__":
    main()

# Changelog

## 0.4.0

- add `centroids_from_boundaries(boundaries, *, representative=False)` in
    `nyc_geo_toolkit._ops`, exported from the top-level namespace. Takes a
    polygon / multi-polygon `BoundaryCollection` and returns a `Point`
    `BoundaryCollection` preserving `geography`, `vintage`,
    `geography_value`, and `properties` on every feature. Round-trips
    through `boundaries_to_geojson` / `boundaries_to_dataframe`. Pass
    `representative=True` for `shapely.Geometry.representative_point`
    (always inside the polygon, safer for non-convex shapes like CDs with
    concave shorelines) instead of the geometric centroid. Unblocks
    downstream spatial analyses that need point geometries — distance-band
    spatial weights, Moran's *I* / LISA, nearest-neighbor joins, choropleth
    label placement — and replaces the hash-placement workaround in the
    `blaise-website` resolution-equity showcase. Closes
    [#12](https://github.com/random-walks/nyc-geo-toolkit/issues/12).

## 0.3.0

- add Claude Code infrastructure parity with the `random-walks` ecosystem:
    `.claude/settings.local.json`, `.claude/launch.json`, agents
    (`release-auditor`, `example-reviewer`), commands (`/bump`,
    `/release-check`, `/add-example`), and skills (`downstream-compat`,
    `release-bump`)
- promote `CLAUDE.md` from the 70-line stub to a dense one-pager covering
    ecosystem role, zero-runtime-deps policy, optional-extras model,
    make-check-before-push rule, and the Claude slash-command surface
- add top-level `AGENTS.md` (canonical agent guide in the AGENTS.md spec
    format used by Cursor / Codex / Copilot / Aider / Zed)
- add `.github/PULL_REQUEST_TEMPLATE.md` and `CITATION.cff`
- add `examples/boundary-explorer-tearsheet/` — self-contained interop
    showcase that loads community districts, builds a synthetic
    `factor_factory.tidy.Panel` with a `TreatmentEvent`, fits
    `factor_factory.engines.did.estimate(..., methods=("twfe",))`, and
    renders a `factor_factory.jellycell.tearsheets.findings` manuscript;
    demonstrates the interop pattern downstream packages (`nyc311`,
    `subway-access`) can copy without adding factor-factory / jellycell
    to default deps
- extend CI matrix to `macos-latest` and `windows-latest` alongside
    `ubuntu-latest` for the `tests` job
- pin GitHub Actions: `astral-sh/setup-uv@v8.1.0` (exact — upstream has
    no moving `v8` tag), keep `actions/checkout@v6`,
    `actions/upload-artifact@v7`, `actions/download-artifact@v8`, and
    `pypa/gh-action-pypi-publish@release/v1`
- add `.claude/scheduled_tasks.lock` to `.gitignore`

## 0.2.0

- add vintage-aware temporal boundary loading via
    `load_nyc_boundaries(..., vintage=year)`
- add `list_available_vintages()`, `describe_layer()`, and
    `vintage_for_census_decade()` API functions
- export `DEFAULT_VINTAGE` constant (2020)
- ship real historical boundary data from official sources:
    - Census tracts 2000 (2,219 features) and 2010 (2,167 features) from US
        Census Bureau TIGER/Line
    - Neighborhood Tabulation Areas 2010 (195 features) from NYC Dept of City
        Planning
    - City Council Districts 2013 (51 features) from NYC Districting Commission
    - ZCTAs 2010 (178 features) from NYC Health Department MODZCTA
- add Google-style docstrings to all 36 public API symbols
- restructure MkDocs documentation with dedicated API reference, getting
    started guide, and examples page
- add `py.typed` PEP 561 marker for downstream type checking
- add `about-the-data-through-time` example demonstrating temporal comparisons

## 0.1.7

- add optional map helpers `add_osm_basemap`, `to_web_mercator`, and
    `bbox_around` (see `nyc_geo_toolkit._basemap`), exported from the top-level
    namespace
- declare `contextily` as part of the `spatial` / `all` optional dependency sets
- add `DeprecationWarning` filter for the `pyproj` NumPy scalar-conversion
    warning so basemap tests pass on Python 3.10
- promote Development Status classifier from Beta to Production/Stable
- update docs to reflect current public API surface including basemap and
    geodesy helpers

## 0.1.2

- refresh public authorship metadata to credit Blaise Albis-Burdige directly
- add `blaiseab.com` as the portfolio link on package and docs surfaces
- align README, docs, and site metadata with the same attribution model

## 0.1.1

- preserve canonical zero-padded council district identifiers such as `09`
- tighten release and packaging checks after the initial public toolkit launch

## 0.1.0

- first standalone public release of `nyc-geo-toolkit`
- extract reusable NYC geography assets and normalization helpers from `nyc311`
- ship typed boundary models, packaged GeoJSON layers, conversion helpers, and
    optional dataframe/spatial helpers

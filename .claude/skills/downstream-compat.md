---
name: downstream-compat
description:
  Reminder that nyc-geo-toolkit is upstream of nyc311 + subway-access. Any
  change to loaders, models, normalization helpers, or the `__all__` export
  surface needs a mental consumer-contract check against those two repos before
  merging. Triggers when editing src/nyc_geo_toolkit/*.py.
---

# Downstream compatibility check

`nyc-geo-toolkit` is the stable geography core for the `random-walks` NYC OSS
ecosystem:

- [`random-walks/nyc311`](https://github.com/random-walks/nyc311) — 311
  service-request analytics. Consumes boundary loaders + normalization helpers.
- [`random-walks/subway-access`](https://github.com/random-walks/subway-access)
  — subway accessibility analytics. Consumes boundary loaders + geodesy helpers.

Both pin a range like `nyc-geo-toolkit>=0.3.0,<0.4`. Touching the public API
touches them.

## When this skill fires

Any edit to files whose shape leaks into the `__all__` export of
`src/nyc_geo_toolkit/__init__.py`:

- `_loaders.py` — `load_nyc_boundaries`, `load_nyc_boundaries_geodataframe`,
  `list_boundary_layers`, `list_boundary_values`, `describe_layer`,
  `list_available_vintages`, etc.
- `_models.py` — `BoundaryCollection`, `BoundaryFeature`, `BoundaryLayerSpec`.
- `_normalize.py` — `normalize_borough_name`, `normalize_boundary_layer`,
  `normalize_boundary_value`, `normalize_boundary_values`.
- `_geodesy.py` — `haversine_distance_meters`, `walk_radius_meters`,
  `build_circle_polygon`.
- `_basemap.py` — `add_osm_basemap`, `to_web_mercator`, `bbox_around`.
- `_constants.py` — `BOROUGH_*`, `SUPPORTED_BOROUGHS`, `DEFAULT_VINTAGE`.

## The check

Before merging any change to the files above, answer these:

1. **Does any existing public signature change?** Renamed param, reordered
   positional, dropped return field, tightened type. → breaking, **major** bump,
   coordinated downstream PR required.
2. **Does any new public symbol land in `__all__`?** → additive, minor bump, no
   downstream work needed.
3. **Does the data on disk change?** A boundary GeoJSON regenerated with a
   different feature set, a new vintage shipped as the default. → data-shape
   change, call it out in the CHANGELOG with before/after counts. Consumers may
   need to widen assertions.
4. **Does a boundary layer name change?** (E.g., renaming `"zcta"` to
   `"zcta_2010"`.) → breaking **key** change, downstream
   `load_nyc_boundaries(layer=...)` calls need updates. Major bump.
5. **Does the `BoundaryCollection` / `BoundaryFeature` shape change?** Renamed
   attribute, new required field, dropped field. → breaking, major bump,
   downstream type-checking fails.

## When in doubt

- Grep the consumer repos if they're checked out locally:
  `grep -r "from nyc_geo_toolkit" ~/Desktop/blaise-oss/nyc311 ~/Desktop/blaise-oss/subway-access`.
- Or skim their `pyproject.toml` pin: `grep "nyc-geo-toolkit" */pyproject.toml`.
- If you can't tell, default to **minor** bump and mention the change in the
  CHANGELOG under a `### Changed` subhead. The downstream maintainer will either
  shrug or open a bump PR.

## The golden rule

If a downstream adopter would have to change a line of code to upgrade past this
PR, it's breaking. Major bump or don't ship.

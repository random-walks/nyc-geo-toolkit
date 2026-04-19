<!-- nyc-geo-toolkit PR template — short, non-bureaucratic. Delete sections that don't apply. -->

## Summary

<!-- 1–3 bullets. What does this PR do and why? -->

## Public-API touches

<!-- Tick any that apply. If any are ticked, confirm the downstream-compat
     mental check has been done (see .claude/skills/downstream-compat.md). -->

- [ ] `_loaders.py` — boundary loader or catalog lookup changes
- [ ] `_models.py` — `BoundaryCollection` / `BoundaryFeature` / `BoundaryLayerSpec`
- [ ] `_normalize.py` — normalization helpers
- [ ] `_geodesy.py` / `_basemap.py` / `_ops.py` — spatial helpers
- [ ] `_constants.py` — `BOROUGH_*`, `SUPPORTED_BOROUGHS`, `DEFAULT_VINTAGE`
- [ ] `__init__.py` — `__all__` surface
- [ ] None of the above

If any ticked:

- [ ] Change is additive (new symbol, new optional kwarg, new boundary vintage)
- [ ] OR change is breaking — major-bump required, and `nyc311` + `subway-access` get a coordinated follow-up PR to widen their pin

## Checklist

- [ ] `make check` green locally
- [ ] `make docs-build` clean (`mkdocs build --strict`)
- [ ] CHANGELOG entry added to `docs/changelog.md` under the right version header
- [ ] New optional dep? → folded into the right extra **and** into `all`
- [ ] New example? → follows the `examples/example-template/` self-contained pattern (`/example-reviewer` clean)
- [ ] New public symbol? → docstring + `__all__` entry + public-API audit passes

## Data provenance (for new boundary layers / vintages)

<!-- Source URL, vintage label, feature count before/after. -->

## Test plan

<!-- What did you run to convince yourself this works? At minimum the
     command that produced the key artifact / output. -->

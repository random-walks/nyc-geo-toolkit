# Contributing

Contributions are welcome, especially when they keep the toolkit lightweight,
explicit, and easy to reuse from other NYC data packages.

The toolkit is authored and maintained by
[Blaise Albis-Burdige](https://blaiseab.com/).

## Development setup

Full environment:

```bash
uv sync --all-groups --all-extras
```

Lean loop:

```bash
uv sync
```

## Project expectations

- prefer additions that strengthen the shared geography core instead of
    consumer-specific one-offs
- keep the base install light and push pandas, geopandas, and shapely behind
    optional extras
- treat underscore-prefixed modules as implementation details
- only add symbols to `nyc_geo_toolkit.__init__` when you are willing to support
    them as public API

## Common commands

```bash
make test           # run the non-integration pytest suite
make test-optional  # exercise optional-dependency-backed features
make lint           # Ruff + mypy + public API audit (fast)
make format         # apply Ruff and Prettier formatting fixes
make check          # full pre-push check (lint + tests, matches CI)
make docs-build     # build the docs with strict checks
make smoke-dist     # build and smoke-test an installed wheel
make ci             # full local CI-equivalent (lint + build + smoke + docs + tests)
```

**Before pushing**, run `make check` to catch everything CI will catch.
`make format` auto-fixes both Python (Ruff) and non-Python (Prettier) files.

## Public API discipline

The supported contract for this package is the top-level `nyc_geo_toolkit`
namespace.

`scripts/audit_public_api.py` enforces that contract by checking:

- every public module is represented in `docs/api.md`
- every exported symbol has a single public location
- the docs and import surface stay aligned

If you add, remove, or move a public symbol, update:

- `src/nyc_geo_toolkit/__init__.py`
- the relevant docs pages
- `tests/test_consumer_contract.py`

## Testing expectations

- `make test` runs the non-integration pytest suite
- `make test-optional` exercises pandas, geopandas, and shapely-backed helpers
- `make docs-build` validates the documentation site with strict checks
- `make smoke-dist` verifies the built wheel works when installed
- `make audit` prints the public API audit

Pytest markers:

- `unit` for fast package-development tests
- `optional` for tests that require optional dependency stacks

## Downstream compatibility

`nyc311` already consumes this package. If you change top-level loaders,
normalization behavior, or exported models, check whether downstream shims,
tests, or docs need updates too.

Backward-compatible fixes and additive improvements fit the current `0.1.x`
line. Consumer-visible contract changes should be deliberate, documented, and
accompanied by tests.

## Release quality checks

Before opening a PR, run:

```bash
make check
make docs-build
make smoke-dist
```

For a full CI-equivalent run (including docs and distribution build):

```bash
make ci
```

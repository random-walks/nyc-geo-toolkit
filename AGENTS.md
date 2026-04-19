# AGENTS.md — nyc-geo-toolkit

Canonical agent guide for this repo. Native readers: Cursor, Codex, GitHub
Copilot, Aider, Zed, Warp, Windsurf, Gemini CLI. Claude Code reads
[`CLAUDE.md`](CLAUDE.md), which layers its own conventions on top.

## What this repo is

`nyc-geo-toolkit` is the **shared geography core** for the `random-walks` NYC
OSS ecosystem. It ships canonical boundary GeoJSON (boroughs, community
districts, council districts, NTAs, ZCTAs, census tracts), normalization helpers
that turn messy input into canonical values, and dep-free geodesy primitives.

See [`README.md`](README.md) for the elevator pitch and install matrix.

## Where to start

**For new agents extending the public API:** read
[`src/nyc_geo_toolkit/__init__.py`](src/nyc_geo_toolkit/__init__.py) — `__all__`
is the complete public surface. Any new export must land in that list, survive
`scripts/audit_public_api.py`, and gain a docstring that the MkDocs API
reference page can autodoc.

**For agents adding a boundary layer or vintage:** see
[`src/nyc_geo_toolkit/_loaders.py`](src/nyc_geo_toolkit/_loaders.py) and the
catalog in [`src/nyc_geo_toolkit/_catalog.py`](src/nyc_geo_toolkit/_catalog.py).
Every vintage must cite its upstream source (Census TIGER/Line, NYC DCP, etc.)
in the CHANGELOG. Regenerate the packaged GeoJSON via the scripts under
`scripts/` and commit with a `data:` / `feat:` commit.

**For agents adding an example:** copy `examples/example-template/` (or run
`/add-example <slug>` under Claude Code), specialize the `pyproject.toml`, write
a `main.py`, smoke-test with `uv sync && uv run python main.py` from inside the
example directory.

## Hard rules

- **Zero-runtime-deps core.** `pyproject.toml`'s `[project] dependencies = []`
  stays empty. Put every new dep behind an optional extra. Adopters rely on the
  base install being tiny.
- **Optional extras model** — `[dataframes]` (pandas), `[spatial]` (geopandas,
  shapely, contextily), and `[all]` (union). New deps fold into the right extra
  AND into `all`.
- **Downstream contract.** `nyc311` + `subway-access` pin this package. Renaming
  a public function, reordering args, or dropping a field in
  `BoundaryCollection` / `BoundaryFeature` is a **breaking change** — major
  bump, downstream coordination required. See
  [`.claude/skills/downstream-compat.md`](.claude/skills/downstream-compat.md).
- **Python ≥ 3.10.** Matches the ecosystem floor.
- **MIT license.** Same as every sibling.
- **Canonical data sources only.** Every boundary vintage ships with a
  documented origin — US Census Bureau TIGER/Line, NYC Department of City
  Planning, NYC Health MODZCTA, NYC Districting Commission, etc. No hand-rolled
  boundary files.

## Conventions

- **Imports in examples / notebooks**:
  `from nyc_geo_toolkit import load_nyc_boundaries, ...`. In library code,
  absolute imports within the package
  (`from nyc_geo_toolkit._models import BoundaryCollection`).
- **Type hints**: `from __future__ import annotations` in every module; full
  type coverage, `mypy --strict` is the floor.
- **Models**: `BoundaryCollection` / `BoundaryFeature` / `BoundaryLayerSpec` are
  the typed carriers. Do not return raw dicts from public loaders.
- **Tests**: `pytest`-based under `tests/`, mirrors source layout. `-m optional`
  marker for tests that exercise optional-extra features.
- **Docs**: MkDocs + Read the Docs. Source under `docs/`. Strict mode enforced
  in CI.
- **Commit style**: conventional commits (`feat:` / `fix:` / `docs:` /
  `refactor:` / `chore:` / `ci:` / `test:`). Subject ≤ 72 chars, imperative
  mood.
- **Branch prefix**: `agentic/...` for agent-driven branches.

## Public-API audit

`scripts/audit_public_api.py` walks every module and verifies that every symbol
re-exported from the top-level package has a docstring and is included in
`__all__`. It runs as part of `make lint`. If you add a public function / class
/ constant, the audit will flag it unless it has:

1. A Google-style docstring with a one-line summary, blank line, and `Args:` /
   `Returns:` / `Raises:` blocks when non-obvious.
2. An entry in `src/nyc_geo_toolkit/__init__.py`'s `__all__`.
3. A re-export from the relevant section of the public API.

## Release cadence

Frequent and small. Patch bumps for doc / test / infra changes; minor for new
loaders, new vintages, or new helpers; major for breaking public-API changes.
See [`.claude/skills/release-bump.md`](.claude/skills/release-bump.md).

Version is derived from the git tag via `hatch-vcs`. There is no `_version.py`
to edit by hand — pushing `git tag vX.Y.Z` cuts the release, and the `cd.yml`
workflow publishes to PyPI via OIDC.

## Pre-merge checklist

- [ ] `make check` green locally
- [ ] Public-API audit clean (runs inside `make lint`)
- [ ] If touching public-API source: mental downstream-compat check
- [ ] CHANGELOG `docs/changelog.md` entry under the right version header
- [ ] New optional dep folded into the right extra + into `all`
- [ ] New example follows `examples/example-template/` pattern

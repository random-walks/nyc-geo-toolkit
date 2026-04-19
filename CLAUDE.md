# CLAUDE.md

Dense one-pager for agents working in this repo. Canonical wider guide is [`AGENTS.md`](AGENTS.md) (AGENTS.md spec format, read by Cursor / Codex / Copilot / Aider / Zed). This file layers Claude-Code-specific conventions on top.

## Ecosystem role

`nyc-geo-toolkit` is the **stable geography core** for the `random-walks` NYC OSS ecosystem:

- [`random-walks/nyc311`](https://github.com/random-walks/nyc311) — 311 service-request analytics. Consumes boundary loaders + normalization helpers.
- [`random-walks/subway-access`](https://github.com/random-walks/subway-access) — subway accessibility analytics. Consumes boundary loaders + geodesy helpers.
- [`random-walks/nyc-mesh`](https://github.com/random-walks/nyc-mesh) — community mesh network analytics.

Both active downstream packages pin something like `nyc-geo-toolkit>=0.3.0,<0.4`. **Any change to the public API touches them.** Read [`.claude/skills/downstream-compat.md`](.claude/skills/downstream-compat.md) before editing `_loaders.py` / `_models.py` / `_normalize.py` / `_geodesy.py` / `_basemap.py` / `_constants.py`.

## The two hard policies

### Zero-runtime-deps core

`pyproject.toml`'s `[project] dependencies = []` is **empty on purpose**. The base `pip install nyc-geo-toolkit` must import and produce boundary data with nothing but the standard library. Do not add a default dep to thread a convenience — put it behind an optional extra instead. Adopters (notably nyc311 + subway-access) rely on this to keep their own install small.

### Optional extras model

Three extras groups, all defined in `pyproject.toml`:

| Extra | Adds | Who uses it |
|---|---|---|
| `[dataframes]` | `pandas>=2.3.3` | `boundaries_to_dataframe`, pandas-friendly callers |
| `[spatial]` | `contextily`, `geopandas`, `shapely` | `load_nyc_boundaries_geodataframe`, `add_osm_basemap`, `to_web_mercator`, `clip_boundaries_to_bbox` |
| `[all]` | everything above | kitchen-sink install for examples + dev |

When you add a new optional dep, it goes into whichever extra(s) use it **and** into `all`. Never add it unconditionally.

## Dev commands

```
make install        # uv sync --all-groups --all-extras
make test           # full non-integration pytest
make lint           # ruff + mypy + pylint + public-API audit
make format         # ruff --fix + format + prettier
make docs           # mkdocs serve (live preview)
make docs-build     # mkdocs build --strict
make check          # ci-lint + ci-tests (pre-push)
make ci             # full local CI equivalent (lint + build + smoke + docs + tests)
```

## Pre-push rule

**Always run `make check` before pushing.** Catches ruff / mypy / pylint / public-API / test regressions before they burn a CI minute. If you're about to push a release tag, run `make ci` (the heavier version that also builds the wheel and smoke-tests the install) instead.

## Claude slash-commands (`.claude/commands/`)

- `/bump [patch|minor|major]` — add a new `## <new>` block to `docs/changelog.md`. Doesn't touch `pyproject.toml` (version derived from git tag via `hatch-vcs`).
- `/release-check` — preflight equivalent to `make ci` + CHANGELOG + git sanity. Returns `READY` / `NOT READY`.
- `/add-example <slug>` — scaffold `examples/<slug>/` from `examples/example-template/`.

## Skills (`.claude/skills/`) — always-loaded reminders

- `downstream-compat` — consult before editing public-API source files. Spells out the nyc311 / subway-access contract.
- `release-bump` — patch / minor / major rubric. Post-1.0 breaking = always major.

## Agents (`.claude/agents/`) — spawn when relevant

- `release-auditor` — read-only preflight before tagging. Runs lint / test / docs / smoke-dist / CHANGELOG + git sanity. Use before `git tag v<X.Y.Z>`.
- `example-reviewer` — verifies a new / edited `examples/<name>/` project follows the self-contained-pyproject pattern.

## Conventions

- **Branch prefix**: `agentic/...` (not `claude/...`). E.g., `agentic/v0.3.0-modernization`, `agentic/fix-lint-issues`.
- **Commits**: conventional commits (`feat:` / `fix:` / `docs:` / `refactor:` / `chore:` / `style:` / `test:` / `ci:`). Subject line ≤ 72 chars, imperative mood.
- **No `https://claude.ai/code/session_...` links** in commit messages or PR bodies.
- **Public API audit**: `scripts/audit_public_api.py` is authoritative. Any new public symbol must be exported via `src/nyc_geo_toolkit/__init__.py`'s `__all__` and the audit must pass.

## Examples pattern

Each directory under `examples/` is a **standalone uv project** with its own `pyproject.toml` and `tool.uv.sources` pointing back to `../..`. To run:

```
cd examples/<name>
uv sync
uv run python main.py
```

Artifacts land locally under `examples/<name>/artifacts/` (or `reports/`, `manuscripts/`). Never in the repo root. Never in the package source tree.

The flagship showcase is [`examples/boundary-explorer-tearsheet/`](examples/boundary-explorer-tearsheet/) — loads community districts via `load_nyc_boundaries`, builds a synthetic `factor_factory.tidy.Panel` with a `TreatmentEvent`, fits `engines.did.twfe`, renders a `jellycell.tearsheets.findings` manuscript. It's the canonical interop pattern for downstream packages (nyc311, subway-access) that want to pipe boundary data into a factor-factory analysis.

## Release flow

1. `/bump [patch|minor|major]` seeds the CHANGELOG block.
2. Fill in specific bullets with citations / data-source URLs.
3. Commit (`docs: add X.Y.Z changelog entry`).
4. `/release-check` → expect `READY to tag vX.Y.Z`.
5. `git tag vX.Y.Z && git push --tags`.
6. The `cd.yml` workflow (OIDC trusted publisher) uploads to PyPI on the `release: published` event. Cut the release on GitHub once the build job finishes and the workflow takes over from there.

Version is derived from the git tag by `hatch-vcs` — there's nothing in `pyproject.toml` to bump by hand.

## Docs

MkDocs + Read the Docs (`docs/`, served at `https://nyc-geo-toolkit.readthedocs.io`). Not Sphinx. **Do not migrate** — MkDocs builds in ~2s with `--strict` clean, and the ecosystem sibling `factor-factory` uses Sphinx because it needs API autodoc at scale. We don't.

## Out of scope (default no)

- Adding a runtime dep to the base package. Use an extra.
- Migrating off MkDocs.
- Renaming public API symbols. If you must, it's a major bump and a coordinated nyc311 + subway-access PR.
- Shipping historical boundary data from an unofficial source. Every vintage ships with a documented origin (Census TIGER/Line, NYC DCP, NYC Health MODZCTA, etc.).

## Pre-merge checklist (mirrors PR template)

- [ ] `make check` green locally
- [ ] If touching public API: downstream-compat mental check (see skill)
- [ ] CHANGELOG `docs/changelog.md` entry under the right version
- [ ] New optional dep? → folded into the right extra + into `all`
- [ ] New example? → follows `examples/example-template/` pattern (run `/example-reviewer` if unsure)

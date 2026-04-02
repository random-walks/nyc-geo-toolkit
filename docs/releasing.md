# Releasing

This guide covers the PyPI release workflow for `nyc-geo-toolkit`.

## Release discipline

- Current stable line: `0.1.x`
- Version source: git tags via Hatch VCS
- Preferred publish trigger: GitHub Release publication

Patch releases in the `0.1.x` line should stay backward-compatible. If a change
materially alters the documented public contract, consumer expectations, or
normalization semantics, cut a new minor release instead of shipping it as a
patch.

## Pre-release checks

Before tagging a release, run:

```bash
make ci
make audit
make docs-build
make smoke-dist
```

If the release touches the top-level API or shared geography behavior, also
verify downstream consumers such as `nyc311`.

## Bootstrap checklist

These one-time steps must be completed by a human account owner before the
trusted publishing flow can be used:

1. Create or verify the PyPI account that will own `nyc-geo-toolkit`, and enable
   2FA.
2. Create or verify a TestPyPI account if you want a dry run before production.
3. Add a pending trusted publisher for project `nyc-geo-toolkit` on both
   TestPyPI and PyPI using:
   - Owner: `random-walks`
   - Repository: `nyc-geo-toolkit`
   - Workflow: `.github/workflows/cd.yml`
   - Environment: `pypi`
4. In GitHub, create the `pypi` environment and add any desired deployment
   protection rules.
5. Set the repository variable `PYPI_PUBLISH_ENABLED=true` only when you are
   ready to allow publishing.

## TestPyPI dry run

1. Create the release tag, for example `0.1.3`.
2. Push the tag.
3. Run the `CD` workflow manually from that tag with:
   - `publish=true`
   - `repository=testpypi`
4. Verify installation from TestPyPI in a clean environment.

## Production release

1. Confirm the `pypi` environment and `PYPI_PUBLISH_ENABLED=true` are in place.
2. Publish a GitHub Release from the tag.

The `release.published` trigger will publish to real PyPI automatically.

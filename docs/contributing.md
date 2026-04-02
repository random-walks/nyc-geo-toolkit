# Contributing

Contributions are welcome, especially when they keep the toolkit lightweight,
explicit, and easy to reuse from other NYC data packages.

## Development setup

Full environment:

```bash
uv sync --all-groups --all-extras
```

Lean loop:

```bash
uv sync
```

## Common commands

```bash
make test
make test-optional
make lint
make docs-build
make smoke-dist
make ci
```

## Release quality checks

Before opening a PR, run:

```bash
make ci
make audit
make docs-build
make smoke-dist
```

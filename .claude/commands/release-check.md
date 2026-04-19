---
description:
  Preflight check before pushing a release tag. Runs lint, tests, strict docs
  build, dist build + twine check, wheel smoke-test, and version sanity.
  Equivalent to `make ci` with extra changelog + git sanity.
---

Execute these in order. Stop on first failure and report the offending step.

1. `make ci-lint` — ruff check + ruff format --check + mypy + pylint +
   public-API audit + nox hygiene hooks.
2. `make ci-build` — `python -m build` then `twine check --strict dist/*`.
3. `make smoke-dist` — builds in a scratch dir, installs into
   `.venv-release-check`, imports the package.
4. `make ci-docs` — `mkdocs build --strict`.
5. `make ci-tests` — full non-integration pytest run with coverage.
6. CHANGELOG sanity:
   - Read the top-most `## <version>` block from `docs/changelog.md`.
   - Confirm it matches the version about to be tagged (you may receive it as
     `$ARGUMENTS`; if empty, use the block heading itself).
   - Confirm its body contains no `TODO` / `TBD` markers.
7. Git sanity:
   - `git status --porcelain` is empty.
   - Current branch is `main` OR a `release/*` branch.
   - `git log --oneline origin/main..HEAD` — call out any local-only commits the
     human should push first.

Print the result of `git log --oneline -20` and `git diff --stat main...HEAD` at
the end so the human can eyeball what's about to go out.

Return a final one-line verdict:

- `READY to tag v<version>` — everything above green, CHANGELOG top block
  matches, worktree clean.
- `NOT READY — <reason>` — stop at the first red step and say why.

Cross-platform caveat: CI runs `tests` on ubuntu/macos/windows. This local run
is one platform — the `READY` verdict is conditional on the matrix also going
green on the tag push.

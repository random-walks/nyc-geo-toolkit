---
name: release-bump
description: One-screen rubric for deciding patch vs minor vs major on nyc-geo-toolkit. Triggers when closing a PR or about to run /bump.
---

# Release bump rubric

`nyc-geo-toolkit` follows the same **minimum-bump** policy as factor-factory / jellycell: patch bumps are cheap, hoard nothing. Cut releases frequently — downstream pins want something stable to target.

## Decision tree

```
Did the diff touch any file that shapes the public API (see .claude/skills/downstream-compat.md)?
├── Yes, but purely additive (new public function, new boundary layer, new optional kwarg) → minor
├── Yes, and breaking (renamed function, reordered args, dropped return field, renamed layer) → major (post-1.0) OR minor (pre-1.0, per SemVer convention)
└── No → continue

Is the change user-visible (new example, new doc page, new data vintage)?
├── Yes → minor
└── No → continue

Is the change a bug fix, docs tidy, internal refactor, dep bump, test-only change, CI / tooling change?
└── Yes → patch
```

## Rules of thumb

- **When in doubt, patch.** You can always cut another release tomorrow.
- **"If the change is worth merging, it's worth a bump"** — even doc-only cleanups land under a patch bump once a week, not once a quarter.
- **Major bumps are expensive.** They force downstream adopters (nyc311, subway-access) to read the CHANGELOG and possibly update their pin range. Earn them.
- **Pre-1.0:** breaking changes are minor per SemVer convention. The `0.x.y` series can churn if needed.
- **Post-1.0:** breaking public-API changes are **always** major. No exceptions.

## What goes into the CHANGELOG entry

Short. Specific. Cite the data source for new boundary vintages.

```
## 0.3.0

- add `examples/boundary-explorer-tearsheet/` — synthetic CD-level DiD
  showcase using factor-factory v1.0.2 + jellycell v1.3.5
- bump Claude Code infra to parity with factor-factory (`.claude/agents/`,
  `.claude/commands/`, `.claude/skills/`, cross-platform CI matrix)
- pin `actions/checkout` v6, `astral-sh/setup-uv@v8.1.0`,
  `actions/upload-artifact@v7`, `actions/download-artifact@v8`,
  `softprops/action-gh-release@v3`
```

Not:

```
- various improvements
- updated infra
```

## Version is derived from the git tag

`nyc-geo-toolkit` uses `hatch-vcs` — there's no `_version.py` to bump by hand (well, there is one, but it's generated at build time from the tag). The real "version bump" happens when you push `git tag v<X.Y.Z>`. The `/bump` command just updates `docs/changelog.md` to match.

## Final step

After running `/bump`, review the generated CHANGELOG section. Rewrite any thin "stuff" entries into specific claims with citations / data-source URLs. Then `git commit`, tag, push. The OIDC release workflow handles PyPI.

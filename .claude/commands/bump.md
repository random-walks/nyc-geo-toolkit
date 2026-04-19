---
description: Roll the next version by appending a new section to docs/changelog.md. Arg = patch | minor | major (default patch). nyc-geo-toolkit uses setuptools-scm / hatch-vcs, so the version is derived from the git tag — this command does NOT write a _version.py. Consult .claude/skills/release-bump.md for the patch/minor/major rubric.
---

Run these steps in order:

1. Parse `$ARGUMENTS`. Valid values: `patch` (default if omitted), `minor`, `major`.
2. Read the most recent tag: `git describe --tags --abbrev=0`. Strip the leading `v`.
3. Compute the new version per the rubric in `.claude/skills/release-bump.md`:
   - patch → `X.Y.(Z+1)`
   - minor → `X.(Y+1).0`
   - major → `(X+1).0.0`
4. In `docs/changelog.md`:
   - Insert a new `## <new-version>` block **above** the current top-most version block.
   - Seed it with an empty `- ` bullet plus a TODO comment so the human fills in specific, citation-bearing changelog entries. Example skeleton:

     ```markdown
     ## 0.3.0

     <!-- TODO: replace with specific changelog bullets. See .claude/skills/release-bump.md. -->
     -
     ```
5. Do NOT modify `pyproject.toml` — the version is derived from the git tag at build time via `hatch-vcs` (see `[tool.hatch] version.source = "vcs"`).
6. Print a summary:
   - old version
   - new version
   - a reminder that the real version bump only takes effect when `git tag v<new>` is pushed
   - next-step hint: fill in the CHANGELOG bullets, commit with `docs: add <new> changelog entry`, then run `/release-check`, then tag.

Do NOT commit or tag — leave that to the human.

If `$ARGUMENTS` is invalid, print the usage and exit without writing anything.

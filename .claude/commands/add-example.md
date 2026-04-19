---
description:
  Scaffold a new self-contained example project under examples/. Arg = slug
  (kebab-case). Copies examples/example-template/ to examples/<slug>/ and
  specializes the metadata. Refuses if the target already exists or the slug is
  invalid.
---

Scaffold a new example at `examples/$ARGUMENTS/`. Refuse if:

- `$ARGUMENTS` is empty.
- `$ARGUMENTS` contains anything other than `[a-z0-9-]`.
- `examples/$ARGUMENTS/` already exists.

Steps:

1. Copy `examples/example-template/` recursively to `examples/$ARGUMENTS/`.
2. Rewrite the copied files:
   - `pyproject.toml`: set `name = "nyc-geo-toolkit-$ARGUMENTS"`, update
     `description` to a short sentence about what this example demonstrates.
     Keep `[tool.uv.sources]` pointing to `{ path = "../..", editable = true }`.
     Keep `dependencies = ["nyc-geo-toolkit"]` unless the human tells you which
     extras to add.
   - `README.md`: replace the placeholder text with a short stub — one paragraph
     on what the example shows, the install/run command
     (`cd examples/$ARGUMENTS && uv sync && uv run python main.py`), and a
     bullet list of expected output artifacts.
   - `main.py`: leave the boilerplate `main()` skeleton in place (three local
     dirs: `cache/`, `artifacts/`, `reports/`). Add a TODO comment at the top
     describing the example's narrative so the human knows where to write.
3. If the example needs a sibling package (e.g., `factor-factory[did]`,
   `jellycell[server]`), add it to `dependencies` in `pyproject.toml` with a
   pinned version range (e.g., `"factor-factory[did]>=1.0.2,<2"`).
4. Print a next-steps checklist for the human:
   - Fill in `main.py` — load boundaries, compute whatever the example
     demonstrates, write artifacts locally.
   - Update `README.md` with the concrete story.
   - `cd examples/$ARGUMENTS && uv sync && uv run python main.py` to smoke-test.
   - Add a row to the "Examples" section of the top-level `README.md` under
     `## Examples`.
   - Consider whether `docs/examples.md` needs an update (if the example
     demonstrates a documented flow).

Do NOT run `uv sync` / `uv run` yourself — let the human drive once they've
filled in the narrative.

If the slug is invalid, print the usage and exit without writing anything.

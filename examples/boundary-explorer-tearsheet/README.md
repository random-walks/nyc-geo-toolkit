# Boundary Explorer Tearsheet

End-to-end showcase of how downstream packages can feed `nyc-geo-toolkit`
boundary data into a [factor-factory](https://github.com/random-walks/factor-factory)
panel + DiD analysis, then render a [jellycell](https://github.com/random-walks/jellycell)
tearsheet manuscript.

This is the canonical **interop pattern** that `nyc311` and `subway-access` follow.
The three packages compose:

- **nyc-geo-toolkit** supplies the geographic scaffolding (community-district
  boundaries via `load_nyc_boundaries("community_district")`).
- **factor-factory** supplies the panel data structure
  (`factor_factory.tidy.Panel`) plus DiD estimation
  (`factor_factory.engines.did.estimate`).
- **jellycell** supplies the manuscript renderer
  (`factor_factory.jellycell.tearsheets.findings`).

## What it does

1. Loads community-district boundaries.
2. Picks a 20-CD subset (10 treated, 10 control) with a reproducible seed.
3. Synthesizes a monthly panel over 24 months with:
   - random-walk baseline outcome
   - 4.0-unit additive treatment effect on treated CDs from month 12 onward
4. Declares a `TreatmentEvent` and builds a `factor_factory.tidy.Panel`.
5. Fits `factor_factory.engines.did.estimate(panel, methods=("twfe",))`.
6. Saves `artifacts/did_results.json` and the synthetic records to
   `data/synthetic_cd_panel.json`.
7. Renders `manuscripts/FINDINGS.md` via
   `factor_factory.jellycell.tearsheets.findings(project=<dir>)`.

## Run

```bash
cd examples/boundary-explorer-tearsheet
uv sync
uv run python main.py
```

The script is self-contained and writes every output under the example
directory — nothing leaks into the repo root or the package source tree.

## Outputs

| Path | Contents |
|---|---|
| `data/synthetic_cd_panel.json` | Long-format synthetic CD-month records used to build the Panel. |
| `artifacts/did_results.json` | Serialized `DidResult` list (what jellycell reads). |
| `manuscripts/FINDINGS.md` | Jellycell-rendered tearsheet manuscript. |

## Why it's synthetic

The outcome is a random walk plus a known 4.0-unit additive treatment
effect — the "ground truth" is embedded in how we construct the data, so
the TWFE estimate should recover ≈4.0 (± SE). This makes the example a
smoke test for the whole pipeline as well as a pattern demo.

A downstream package (say, nyc311) would plug in a real outcome (call
volume, service-request counts, rat sightings, station ridership) in
place of the synthetic random walk, and leave every other step identical.

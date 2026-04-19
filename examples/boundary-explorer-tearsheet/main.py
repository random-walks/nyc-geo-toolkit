"""Showcase: load CD boundaries, synthesize a panel, fit DiD, render a tearsheet.

The three moving pieces:

- `nyc_geo_toolkit.load_nyc_boundaries` supplies the geographic
  scaffolding (community-district polygons + canonical identifiers).
- `factor_factory.tidy.Panel` + `factor_factory.engines.did.estimate`
  handle the panel data structure and TWFE DiD estimation.
- `factor_factory.jellycell.tearsheets.findings` renders the manuscript.

The outcome follows the canonical DiD data-generating process:
``y_it = alpha_i + gamma_t + beta * 1[treated_i and t >= onset] + eps_it`` — unit
intercepts alpha_i, a gentle time trend gamma_t, iid Gaussian noise eps_it, and a
known additive treatment effect beta = 4.0 on the treated CDs from month
12 onward. Entity + time fixed effects absorb alpha_i and gamma_t cleanly, so
the TWFE fit should recover an ATT of roughly 4.0. The example is both
a pattern demo and a smoke test for the full interop pipeline.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
from factor_factory.engines.did import estimate
from factor_factory.jellycell.tearsheets import findings
from factor_factory.tidy import Panel, PanelMetadata, TreatmentEvent

from nyc_geo_toolkit import load_nyc_boundaries

ROOT = Path(__file__).resolve().parent
ARTIFACTS_DIR = ROOT / "artifacts"
DATA_DIR = ROOT / "data"
MANUSCRIPTS_DIR = ROOT / "manuscripts"

SEED = 0
N_TREATED = 15
N_CONTROL = 15
N_MONTHS = 24
TREATMENT_MONTH_INDEX = 12
GROUND_TRUTH_ATT = 4.0
PANEL_START = pd.Timestamp("2022-01-31")

# Baseline outcome ~ 50; unit intercepts have small dispersion so entity FE
# absorbs them cleanly; time trend is gentle (+0.2/month); noise stddev = 1.
UNIT_INTERCEPT_MEAN = 50.0
UNIT_INTERCEPT_SD = 3.0
TIME_TREND_PER_MONTH = 0.2
NOISE_SD = 1.0


def _ensure_dirs() -> None:
    for d in (ARTIFACTS_DIR, DATA_DIR, MANUSCRIPTS_DIR):
        d.mkdir(parents=True, exist_ok=True)


def _pick_units() -> tuple[list[str], list[str]]:
    """Pick a reproducible subset of community districts.

    Returns (treated, control) — disjoint lists of canonical CD values.
    """
    cds = load_nyc_boundaries("community_district")
    values = sorted(feature.geography_value for feature in cds.features)
    rng = np.random.default_rng(SEED)
    chosen = rng.choice(values, size=N_TREATED + N_CONTROL, replace=False)
    chosen = sorted(chosen.tolist())
    return chosen[:N_TREATED], chosen[N_TREATED:]


def _synthesize_panel_df(
    treated: list[str],
    control: list[str],
) -> tuple[pd.DataFrame, list[dict[str, object]]]:
    """Build a (unit_id, period) DataFrame with a canonical DiD DGP.

    ``y_it = alpha_i + gamma_t + beta * 1[treated_i and t >= onset] + eps_it`` —
    parallel-trends-by-construction, so TWFE recovers beta cleanly.

    Returns the wide panel DataFrame (MultiIndex'd) and a long-format
    record list for archiving.
    """
    rng = np.random.default_rng(SEED)
    periods = pd.date_range(PANEL_START, periods=N_MONTHS, freq="ME")
    units = treated + control
    treatment_onset = periods[TREATMENT_MONTH_INDEX]
    unit_intercepts = {
        unit: float(rng.normal(UNIT_INTERCEPT_MEAN, UNIT_INTERCEPT_SD))
        for unit in units
    }

    rows: list[dict[str, object]] = []
    records: list[dict[str, object]] = []
    for unit in units:
        alpha_i = unit_intercepts[unit]
        noise = rng.normal(loc=0.0, scale=NOISE_SD, size=N_MONTHS)
        for month_idx, (period, eps) in enumerate(zip(periods, noise, strict=True)):
            gamma_t = TIME_TREND_PER_MONTH * month_idx
            treated_post = unit in treated and month_idx >= TREATMENT_MONTH_INDEX
            outcome = float(
                alpha_i + gamma_t + (GROUND_TRUTH_ATT if treated_post else 0.0) + eps
            )
            rows.append(
                {
                    "unit_id": unit,
                    "period": period,
                    "outcome": outcome,
                }
            )
            records.append(
                {
                    "community_district": unit,
                    "period": period.strftime("%Y-%m-%d"),
                    "outcome": round(outcome, 4),
                    "is_treated_unit": unit in treated,
                    "is_post_treatment": month_idx >= TREATMENT_MONTH_INDEX,
                }
            )

    df = (
        pd.DataFrame(rows)
        .set_index(["unit_id", "period"])
        .sort_index()
        .astype({"outcome": "float64"})
    )
    assert len(df) == len(units) * N_MONTHS
    df.attrs["treatment_onset"] = treatment_onset
    return df, records


def build_panel(treated: list[str], control: list[str]) -> Panel:
    df, _ = _synthesize_panel_df(treated, control)
    treatment_onset: pd.Timestamp = df.attrs["treatment_onset"]
    event = TreatmentEvent(
        name="synthetic_policy_v1",
        description="Synthetic CD-level policy with a 4.0-unit additive effect.",
        treated_units=tuple(treated),
        treatment_date=date(
            treatment_onset.year, treatment_onset.month, treatment_onset.day
        ),
        dimension="community_district",
        kind="binary",
    )
    metadata = PanelMetadata(
        outcome_cols=("outcome",),
        period_kind="timestamp",
        freq="ME",
        dimension="community_district",
        treatment_events=(event,),
    )
    panel = Panel(df, metadata)
    return panel.attach_treatment_columns()


def save_synthetic_records(treated: list[str], control: list[str]) -> Path:
    _, records = _synthesize_panel_df(treated, control)
    out = DATA_DIR / "synthetic_cd_panel.json"
    out.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    return out


def fit_and_save(panel: Panel) -> Path:
    results = estimate(panel, methods=("twfe",), outcome="outcome")
    out = ARTIFACTS_DIR / "did_results.json"
    payload = {
        "results": results.to_records(),
        "panel_summary": panel.summary(),
        "ground_truth_att": GROUND_TRUTH_ATT,
    }
    out.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")
    return out


def render_tearsheet() -> Path:
    return findings(
        project=str(ROOT),
        output_path=MANUSCRIPTS_DIR / "FINDINGS.md",
        overwrite=True,
    )


def main() -> None:
    _ensure_dirs()

    treated, control = _pick_units()
    print(f"Treated CDs ({len(treated)}): {treated[:3]}...")
    print(f"Control CDs ({len(control)}): {control[:3]}...")

    records_path = save_synthetic_records(treated, control)
    print(f"Wrote synthetic records → {records_path.relative_to(ROOT)}")

    panel = build_panel(treated, control)
    print(f"Built panel: {panel!r}")

    results_path = fit_and_save(panel)
    print(f"Wrote DiD results → {results_path.relative_to(ROOT)}")

    payload = json.loads(results_path.read_text(encoding="utf-8"))
    result = payload["results"][0]
    err_ses = abs(result["att"] - GROUND_TRUTH_ATT) / result["se"]
    print(
        f"Recovered ATT={result['att']:.3f} (SE={result['se']:.3f}) "
        f"vs truth={GROUND_TRUTH_ATT} → {err_ses:.2f} SE"
    )

    tearsheet_path = render_tearsheet()
    print(f"Rendered tearsheet → {tearsheet_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

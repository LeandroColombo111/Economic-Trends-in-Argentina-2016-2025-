"""Pipeline orchestration for the economic trends dataset."""
from __future__ import annotations

from typing import Dict

import pandas as pd

from .config import DEFAULT_START, DOCS_ASSETS, SERIES
from .fetch_series import fetch_one_series, save_raw
from .transform import (
    compute_pct_change,
    compute_real_wage,
    rebase_index,
    save_processed,
)


def run_pipeline(start: str | None = DEFAULT_START) -> Dict[str, str]:
    """
    Execute the ETL pipeline end-to-end and return a map of generated artifacts.
    """
    actual_start = start or DEFAULT_START
    outputs: Dict[str, str] = {}

    raw_frames: Dict[str, pd.DataFrame] = {}
    for name, spec in SERIES.items():
        df = fetch_one_series(
            spec["id"],
            start=actual_start,
            collapse=spec.get("collapse"),
            agg=spec.get("agg"),
        )
        raw_path = save_raw(df, name)
        outputs[f"raw:{name}"] = str(raw_path)
        raw_frames[name] = df

    usd_m = raw_frames["usd_official"]
    ipc_m = raw_frames["ipc_nacional"]
    ripte_m = raw_frames["ripte"]
    res_m = raw_frames["reserves_usd"]

    usd_yoy = compute_pct_change(usd_m, periods=12)
    ipc_yoy = compute_pct_change(ipc_m, periods=12)
    res_yoy = compute_pct_change(res_m, periods=12)

    usd_rebased = rebase_index(usd_m)
    ipc_rebased = rebase_index(ipc_m)
    real_wage = compute_real_wage(ripte_m, ipc_m)

    outputs["processed:usd_official_yoy"] = str(save_processed(usd_yoy, "usd_official_yoy"))
    outputs["processed:ipc_yoy"] = str(save_processed(ipc_yoy, "ipc_yoy"))
    outputs["processed:reserves_yoy"] = str(save_processed(res_yoy, "reserves_yoy"))
    outputs["processed:usd_official_rebased"] = str(save_processed(usd_rebased, "usd_official_rebased"))
    outputs["processed:ipc_rebased"] = str(save_processed(ipc_rebased, "ipc_rebased"))
    outputs["processed:real_wage"] = str(save_processed(real_wage, "real_wage"))

    DOCS_ASSETS.mkdir(parents=True, exist_ok=True)

    summary = (
        usd_m.rename(columns={"value": "usd_official"})
        .merge(
            ipc_m.rename(columns={"value": "ipc"}),
            on="date",
            how="outer",
        )
        .merge(
            res_m.rename(columns={"value": "reserves_usd"}),
            on="date",
            how="outer",
        )
        .merge(
            ripte_m.rename(columns={"value": "ripte"}),
            on="date",
            how="outer",
        )
        .merge(
            usd_yoy[["date", "pct_change"]].rename(columns={"pct_change": "usd_official_yoy"}),
            on="date",
            how="left",
        )
        .merge(
            ipc_yoy[["date", "pct_change"]].rename(columns={"pct_change": "ipc_yoy"}),
            on="date",
            how="left",
        )
        .merge(
            res_yoy[["date", "pct_change"]].rename(columns={"pct_change": "reserves_yoy"}),
            on="date",
            how="left",
        )
        .merge(
            usd_rebased[["date", "rebased_100"]].rename(columns={"rebased_100": "usd_official_rebased"}),
            on="date",
            how="left",
        )
        .merge(
            ipc_rebased[["date", "rebased_100"]].rename(columns={"rebased_100": "ipc_rebased"}),
            on="date",
            how="left",
        )
        .merge(
            real_wage[["date", "real_wage", "real_wage_yoy"]],
            on="date",
            how="left",
        )
        .sort_values("date")
    )

    summary_path = DOCS_ASSETS / "series_summary.csv"
    summary.to_csv(summary_path, index=False)
    outputs["docs:series_summary"] = str(summary_path)

    return outputs

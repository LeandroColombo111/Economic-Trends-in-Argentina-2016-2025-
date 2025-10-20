"""Data transformations for processed economic indicators."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .config import DATA_PROCESSED


def compute_pct_change(df: pd.DataFrame, periods: int = 12) -> pd.DataFrame:
    """Return a copy of ``df`` with an additional ``pct_change`` column (in %)."""
    out = df.copy()
    out["pct_change"] = out["value"].pct_change(periods=periods) * 100.0
    return out


def rebase_index(df: pd.DataFrame, base_date: str | None = None) -> pd.DataFrame:
    """
    Rebase the series to 100 at ``base_date`` (or the first observation if missing).
    """
    out = df.copy()
    if out.empty:
        out["rebased_100"] = np.nan
        return out

    base_value: float | None = None
    if base_date is not None:
        mask = out["date"] == pd.to_datetime(base_date)
        if mask.any():
            base_value = float(out.loc[mask, "value"].iloc[0])

    if base_value is None:
        base_value = float(out.iloc[0]["value"])

    out["rebased_100"] = (out["value"] / base_value) * 100.0
    return out


def compute_real_wage(ripte: pd.DataFrame, ipc: pd.DataFrame) -> pd.DataFrame:
    """
    Compute a real wage proxy by deflating RIPTE with IPC (nearest monthly match).
    """
    merged = pd.merge_asof(
        ripte.sort_values("date"),
        ipc.sort_values("date"),
        on="date",
        direction="nearest",
        suffixes=("_ripte", "_ipc"),
    )
    if merged.empty:
        return merged

    ipc_base = float(merged.iloc[0]["value_ipc"])
    merged["real_wage"] = merged["value_ripte"] / (merged["value_ipc"] / ipc_base)
    merged["real_wage_yoy"] = merged["real_wage"].pct_change(12) * 100.0
    return merged[["date", "value_ripte", "value_ipc", "real_wage", "real_wage_yoy"]]


def save_processed(df: pd.DataFrame, name: str) -> Path:
    """Save a processed artifact to data/processed and return the file path."""
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    out_path = DATA_PROCESSED / f"{name}.csv"
    df.to_csv(out_path, index=False)
    return out_path

"""Helpers to interact with the public Argentina Series API."""
from __future__ import annotations

from pathlib import Path
from urllib.parse import urlencode

import pandas as pd
import requests

from .config import BASE_SERIES_API, DATA_RAW


def build_series_url(
    series_id: str,
    start: str | None = None,
    collapse: str | None = None,
    agg: str | None = None,
) -> str:
    """Build the fully qualified API URL for a single series."""
    params = {"ids": series_id}
    if start:
        params["start_date"] = start
    if collapse:
        params["collapse"] = collapse
    if agg:
        params["collapse_aggregation"] = agg
    return f"{BASE_SERIES_API}?{urlencode(params)}"


def fetch_one_series(
    series_id: str,
    start: str | None = None,
    collapse: str | None = None,
    agg: str | None = None,
    timeout: int = 60,
) -> pd.DataFrame:
    """
    Fetch a single series from the API and return a tidy two-column DataFrame.

    The returned DataFrame has columns: date (datetime64[ns]) and value (float64).
    """
    url = build_series_url(series_id, start=start, collapse=collapse, agg=agg)
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    payload = response.json()

    data = payload.get("data", [])
    headers = payload.get("headers", [])
    if not data or len(headers) < 2:
        raise ValueError(f"Unexpected API response for series '{series_id}'")

    frame = pd.DataFrame(data, columns=[headers[0]["name"], headers[1]["name"]])
    frame.columns = ["date", "value"]
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    frame["value"] = pd.to_numeric(frame["value"], errors="coerce")
    frame = frame.dropna(subset=["date", "value"]).sort_values("date").reset_index(drop=True)
    return frame


def save_raw(df: pd.DataFrame, name: str) -> Path:
    """Persist a raw series under data/raw and return the file path."""
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    out_path = DATA_RAW / f"{name}.csv"
    df.to_csv(out_path, index=False)
    return out_path

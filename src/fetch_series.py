import json
from pathlib import Path
from urllib.parse import urlencode
import requests
import pandas as pd
from .config import DATA_RAW, BASE_SERIES_API


# NOTE: I fetch one series per call to keep the function simple to test and log.
# The API supports multiple ids in one request; I keep it atomic here.


def build_series_url(series_id: str, start: str = None, collapse: str = None, agg: str = None) -> str:
"""
I construct a robust URL for Argentina's Series API.
- Accepts single series id, optional start date, collapse granularity and aggregation.
- Keeps parameters explicit so future me can tweak behavior easily.
"""
params = {"ids": series_id}
if start:
params["start_date"] = start
if collapse:
params["collapse"] = collapse
if agg:
params["collapse_aggregation"] = agg
return f"{BASE_SERIES_API}?{urlencode(params)}"




def fetch_one_series(series_id: str, start: str = None, collapse: str = None, agg: str = None) -> pd.DataFrame:
"""
I download a single series as a DataFrame with columns: 'date' and 'value'.
The API returns 'data' plus 'headers'; I normalize into a simple tidy format.
"""
url = build_series_url(series_id, start, collapse, agg)
resp = requests.get(url, timeout=60)
resp.raise_for_status()
payload = resp.json()
# Expect payload like: {"data": [[ts, v], ...], "headers": [{"name": "indice_tiempo"}, {"name": series_id}]}
data = payload.get("data", [])
headers = payload.get("headers", [])
if not data or len(headers) < 2:
raise ValueError(f"Unexpected API shape for {series_id}")
df = pd.DataFrame(data, columns=[headers[0]["name"], headers[1]["name"]])
df.columns = ["date", "value"]
# Convert to datetime and numeric
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["value"] = pd.to_numeric(df["value"], errors="coerce")
df = df.dropna().sort_values("date").reset_index(drop=True)
return df




def save_raw(df: pd.DataFrame, name: str) -> Path:
"""
I persist the raw series exactly as received (after light normalization) under data/raw.
"""
DATA_RAW.mkdir(parents=True, exist_ok=True)
out = DATA_RAW / f"{name}.csv"
df.to_csv(out, index=False)
return out
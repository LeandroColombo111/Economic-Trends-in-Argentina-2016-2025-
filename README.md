# Argentina Economic Trends (Local ETL + GitHub Pages)


A local, reproducible pipeline that fetches Argentine macro indicators from public APIs and serves a static dashboard (English) on GitHub Pages. No databases.


## Why this project (motivation)
Argentina’s economy moves fast. I wanted a transparent and reproducible way to track
macro trends (FX, inflation, reserves, wages) from 2016–present using only open data and
code that anyone can run locally.


## What it analyzes
- Official USD/ARS exchange rate (end-of-month)
- National CPI (rebased for comparability)
- International reserves at BCRA (USD)
- Real wage proxy (RIPTE deflated by CPI)


## What it does (pipeline)
1. Downloads series from the Argentina Time Series API (datos.gob.ar).
2. Stores normalized raw CSVs under `data/raw/` for auditability.
3. Builds processed artifacts (YoY, rebased indexes, real-wage series) under `data/processed/`.
4. Exports a compact `docs/assets/series_summary.csv` for the static dashboard.
5. Hosts a static dashboard (Plotly) from `docs/index.html` (GitHub Pages-ready).


## Objectives
- Provide a clean, local ETL that can be forked, extended, or automated.
- Offer an easy-to-read dashboard that highlights medium-term trends.
- Keep everything versioned to make changes traceable over time.


## How to run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/make_dataset.py 2016-01
open docs/index.html
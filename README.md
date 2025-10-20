# Argentina Economic Trends (Local ETL + GitHub Pages)


A local, reproducible pipeline that fetches Argentine macro indicators from public APIs and serves a static dashboard (English) on GitHub Pages. No databases.


## How to run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/make_dataset.py 2016-01
open docs/index.html
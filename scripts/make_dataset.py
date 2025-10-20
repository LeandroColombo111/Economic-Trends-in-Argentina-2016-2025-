#!/usr/bin/env python3
"""
I run the full ETL pipeline end‑to‑end and prepare assets for GitHub Pages.
Usage:
python scripts/make_dataset.py [YYYY-MM]
"""
import sys
from src.pipeline import run_pipeline


if __name__ == "__main__":
start = sys.argv[1] if len(sys.argv) > 1 else None
out = run_pipeline(start=start)
print("Artifacts:", out)
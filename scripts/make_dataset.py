#!/usr/bin/env python3
"""Run the ETL pipeline and write all derived assets."""

import sys

from src.pipeline import run_pipeline


def main() -> None:
    start = sys.argv[1] if len(sys.argv) > 1 else None
    outputs = run_pipeline(start=start)
    print("Artifacts:", outputs)


if __name__ == "__main__":
    main()

"""Project-wide configuration and constants."""
from pathlib import Path
from typing import Dict, Optional, TypedDict


class SeriesConfig(TypedDict, total=False):
    """Configuration contract for a single time series request."""

    id: str
    collapse: Optional[str]
    agg: Optional[str]


ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
DOCS_ASSETS = ROOT / "docs" / "assets"

BASE_SERIES_API = "https://apis.datos.gob.ar/series/api/series"

SERIES: Dict[str, SeriesConfig] = {
    "usd_official": {
        "id": "168.1_T_CAMBIOR_D_0_0_26",
        "collapse": "month",
        "agg": "end_of_period",
    },
    "reserves_usd": {
        "id": "92.2_RESERVAS_IRES_0_0_32_40",
        "collapse": "month",
        "agg": "end_of_period",
    },
    "ipc_nacional": {
        "id": "147.3_IBIENESUYO_DICI_T_15",
        "collapse": "month",
        "agg": "avg",
    },
    "ripte": {
        "id": "sspm_32.3_RIPTE_0_0_33",
        "collapse": "month",
        "agg": "avg",
    },
}

DEFAULT_START = "2016-01"

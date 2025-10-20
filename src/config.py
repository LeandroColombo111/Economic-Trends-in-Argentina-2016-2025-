from pathlib import Path


# NOTE: All data is stored locally; docs/assets/ is used by the static dashboard.
ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
DOCS_ASSETS = ROOT / "docs" / "assets"


# Public time-series API (Argentina). See docs:
# https://datos.gob.ar/series/api (general) and
# https://datosgobar.github.io/series-tiempo-ar-api-english/ (English quick ref)
BASE_SERIES_API = "https://apis.datos.gob.ar/series/api/series"


# --- Series IDs (you can tweak/extend later) ---
SERIES = {
# Official exchange rate (MAE). Monthly collapsed from daily.
# Doc hint: BCRA exchange rate series are available via the Series API.
"usd_official": {
"id": "168.1_T_CAMBIOR_D_0_0_26",
"collapse": "month",
"agg": "end_of_period",
},
# International reserves (USD, BCRA). Monthly.
"reserves_usd": {
"id": "92.2_RESERVAS_IRES_0_0_32_40",
"collapse": "month",
"agg": "end_of_period",
},
# Consumer Price Index – National IPC (index). Monthly.
# If the ID changes, search it on datos.gob.ar Series portal.
"ipc_nacional": {
"id": "147.3_IBIENESUYO_DICI_T_15",
"collapse": "month",
"agg": "avg",
},
# Salaries – RIPTE (average taxable wage, monthly).
"ripte": {
"id": "sspm_32.3_RIPTE_0_0_33", # fallback name; replace if portal gives a different exact id
"collapse": "month",
"agg": "avg",
},
}


DEFAULT_START = "2016-01"
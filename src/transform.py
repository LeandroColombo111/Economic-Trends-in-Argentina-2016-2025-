import pandas as pd
import numpy as np
from .config import DATA_PROCESSED


# NOTE: These helpers compute derived economic indicators for the dashboard.




def compute_pct_change(df: pd.DataFrame, periods: int = 12) -> pd.DataFrame:
"""
I compute YoY (or generic) percentage change to make trends comparable.
"""
out = df.copy()
out["pct_change"] = out["value"].pct_change(periods=periods) * 100.0
return out




def rebase_index(df: pd.DataFrame, base_date: str = None) -> pd.DataFrame:
"""
I rebase any index/price-like series to 100 at a given base_date (or first row if None).
"""
out = df.copy()
if base_date:
base_val = out.loc[out["date"] == pd.to_datetime(base_date), "value"].iloc[0]
else:
base_val = out["value"].iloc[0]
out["rebased_100"] = (out["value"] / base_val) * 100.0
return out




def compute_real_wage(ripte: pd.DataFrame, ipc: pd.DataFrame) -> pd.DataFrame:
"""
I deflate nominal wages (RIPTE) by CPI index to approximate real wages.
Assumes RIPTE and IPC are monthly and aligned on 'date' after merge.
"""
merged = pd.merge_asof(ripte.sort_values("date"), ipc.sort_values("date"), on="date", direction="nearest", suffixes=("_ripte","_ipc"))
# Real wage proxy = RIPTE / (IPC / IPC_base)
ipc_base = merged["value_ipc"].iloc[0]
merged["real_wage"] = merged["value_ripte"] / (merged["value_ipc"] / ipc_base)
merged["real_wage_yoy"] = merged["real_wage"].pct_change(12) * 100.0
return merged[["date","value_ripte","value_ipc","real_wage","real_wage_yoy"]]




def save_processed(df: pd.DataFrame, name: str) -> None:
"""
I save processed datasets under data/processed for reproducible analysis.
"""
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
df.to_csv(DATA_PROCESSED / f"{name}.csv", index=False)
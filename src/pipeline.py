from dataclasses import dataclass
raw_frames = {}
for name, spec in SERIES.items():
df = fetch_one_series(spec["id"], start=start, collapse=spec.get("collapse"), agg=spec.get("agg"))
save_raw(df, name)
raw_frames[name] = df


# 2) Transform key indicators
usd_m = raw_frames["usd_official"]
ipc_m = raw_frames["ipc_nacional"]
ripte_m = raw_frames["ripte"]
res_m = raw_frames["reserves_usd"]


usd_yoy = compute_pct_change(usd_m, periods=12)
ipc_yoy = compute_pct_change(ipc_m, periods=12)
res_yoy = compute_pct_change(res_m, periods=12)


usd_rebased = rebase_index(usd_m)
ipc_rebased = rebase_index(ipc_m)


realw = compute_real_wage(ripte_m, ipc_m)


# 3) Save processed
save_processed(usd_yoy, "usd_official_yoy")
save_processed(ipc_yoy, "ipc_yoy")
save_processed(res_yoy, "reserves_yoy")
save_processed(usd_rebased, "usd_official_rebased")
save_processed(ipc_rebased, "ipc_rebased")
save_processed(realw, "real_wage")


# 4) Export dashboard-facing summary
DOCS_ASSETS.mkdir(parents=True, exist_ok=True)


summary = (
pd.DataFrame({
"date": usd_m["date"],
"usd_official": usd_m["value"],
})
.merge(ipc_m.rename(columns={"value":"ipc"}), on="date", how="outer")
.merge(res_m.rename(columns={"value":"reserves_usd"}), on="date", how="outer")
.merge(ripte_m.rename(columns={"value":"ripte"}), on="date", how="outer")
.sort_values("date")
)


summary.to_csv(DOCS_ASSETS / "series_summary.csv", index=False)


meta = {
"start": start,
"series": {k: v["id"] for k, v in SERIES.items()},
}
(DOCS_ASSETS / "meta.json").write_text(json.dumps(meta, indent=2))


outputs["summary_csv"] = str(DOCS_ASSETS / "series_summary.csv")
outputs["meta_json"] = str(DOCS_ASSETS / "meta.json")
return outputs
# Pipeline

End-to-end path from raw CRMLS/FRED exports in `data/raw/` to analysis-ready
CSVs in `data/processed/`. Each stage reads the previous stage's output,
transforms it, writes a new numbered file, and deletes its input — so
`data/processed/` only ever holds the latest-stage file per dataset.

`<name>` below is always `listings` or `sold`. Files are named
`<index>_<name>.csv`, where `<index>` is the zero-based stage number.

## Stages

| Index | Stage | Script | Reads | Writes | Deletes input? |
|---|-------|--------|-------|--------|---|
| — | Fetch listings/sold | `preprocessing/fetch_data.py` | FTP server (`CRMLSListing*`, `CRMLSSold*`) | `data/raw/CRMLSListing*.csv`, `data/raw/CRMLSSold*.csv` | no |
| — | Fetch mortgage rates | `preprocessing/mortgage/fred.py` | FRED (`MORTGAGE30US`) | `data/raw/mortgage_rates.csv` | no |
| 0 | Combine + residential filter | `preprocessing/preprocess.py` | `data/raw/CRMLS{Listing,Sold}*.csv` | `data/processed/0_<name>.csv` | no (raw files are permanent source data) |
| 1 | Prune high-null columns | `null_analysis.ipynb` | `data/processed/0_<name>.csv` | `data/processed/1_<name>.csv` | yes, `0_<name>.csv` |
| 2 | Merge mortgage rates | `preprocessing/mortgage/merge.ipynb` | `data/processed/1_<name>.csv` | `data/processed/2_<name>.csv` | yes, `1_<name>.csv` |
| 3 | Type/timeline/geo validation | `validation.ipynb` | `data/processed/2_<name>.csv` | `data/processed/3_<name>.csv` | yes, `2_<name>.csv` |
| 4 | School district join | `school_districting.ipynb` | `data/processed/3_<name>.csv`, `data/raw/DistrictAreas.geojson` | `data/processed/4_<name>.csv` | yes, `3_<name>.csv` |
| 5 | Feature engineering | `features.py` | TBD (would read `4_<name>.csv`) | TBD (would write `5_<name>.csv`) | currently an empty stub, not yet implemented |

## Naming, stage by stage

```
CRMLSListing<YYYYMM>.csv, CRMLSSold<YYYYMM>.csv     (data/raw/, one file per month)
        │  preprocess.py — concat + filter PropertyType == "Residential"
        ▼
0_listings.csv, 0_sold.csv
        │  null_analysis.ipynb — drop columns with >50% nulls
        ▼
1_listings.csv, 1_sold.csv
        │  merge.ipynb — left-join monthly mortgage rate on year_month
        ▼
2_listings.csv, 2_sold.csv
        │  validation.ipynb — date coercion, negative-value filter,
        │                     timeline flags, CA geo filter, column drops
        ▼
3_listings.csv, 3_sold.csv
        │  school_districting.ipynb — spatial join against DistrictAreas.geojson
        ▼
4_listings.csv, 4_sold.csv
        │  features.py — not yet implemented
        ▼
5_listings.csv, 5_sold.csv   (planned)
```

`data/processed/README.txt` documents the same stages from the data side.

Each notebook does all of its work against the file it read in and writes
exactly one new, higher-numbered file before deleting the one it read —
`validation.ipynb` briefly overwrites its stage-2 input in place while it
works, but the input is still deleted once the final `3_<name>.csv` is
written, so mid-pipeline state never lingers under a stale name.

## Directories

- `preprocessing/` — stages 0–2 (fetch, combine/filter, mortgage merge). See its own README.
- `tools/` — `util/` plotting & summary helpers (`distribution_summary`, `plot_distribution`, `FixedOrderFormatter`) plus a demo notebook. Not part of the data pipeline itself. See its own README.
- `extra/` — archived ad-hoc exploratory notebooks (`prices.ipynb`, `questions.ipynb`), not part of the pipeline.
- `null_analysis.ipynb`, `validation.ipynb`, `school_districting.ipynb`, `features.py` — pipeline stages 1, 3, 4, 5, at the `scripts/` root.

## Running it

```bash
# fetch raw data
python scripts/preprocessing/fetch_data.py
python scripts/preprocessing/mortgage/fred.py

# stage 0: combine + filter (all, or: listings | sold)
python scripts/preprocessing/preprocess.py

# stages 1-4, run in order:
#   scripts/null_analysis.ipynb
#   scripts/preprocessing/mortgage/merge.ipynb
#   scripts/validation.ipynb
#   scripts/school_districting.ipynb
```

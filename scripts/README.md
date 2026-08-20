# Data pipeline

This directory contains the end-to-end workflow from raw CRMLS/FRED data in
`data/raw/` to feature tables in `data/processed/`. The pipeline supports two
datasets: `listings` and `sold`.

## Run everything

From the repository root:

```bash
scripts/run_pipeline.sh
```

To reuse already-downloaded files:

```bash
scripts/run_pipeline.sh --skip-fetch
```

The script changes into `scripts/` before running notebook and Python stages.
This is why the recommended command is the shell script rather than manually
executing notebooks from arbitrary working directories.

## Stages and files

| Stage | Entry point | Input | Output |
|---:|---|---|---|
| — | `preprocessing/fetch_data.py` | CRMLS FTP | `data/raw/CRMLSListing*.csv`, `CRMLSSold*.csv` |
| — | `preprocessing/mortgage/fred.py` | FRED `MORTGAGE30US` | `data/raw/mortgage_rates.csv` |
| 0 | `preprocessing/preprocess.py` | Monthly CRMLS CSVs | `0_listings.csv`, `0_sold.csv` |
| 1 | `null_analysis.ipynb` | Stage 0 files | `1_listings.csv`, `1_sold.csv` |
| 2 | `preprocessing/mortgage/merge.ipynb` | Stage 1 files + rates | `2_listings.csv`, `2_sold.csv` |
| 3 | `validation.ipynb` | Stage 2 files | `3_listings.csv`, `3_sold.csv` |
| 4 | `school_districting.ipynb` | Stage 3 files + GeoJSON | `4_listings.csv`, `4_sold.csv` |
| 5 | `features.py` | Stage 4 files | Feature files; removes `4_<name>.csv` |
| 6 | `iqr_filter.py` | Feature files | Same feature files, filtered in place |

The numbered stages are a hand-off sequence:

```text
CRMLS exports
  → 0_<name>.csv → 1_<name>.csv → 2_<name>.csv → 3_<name>.csv
  → 4_<name>.csv → <name>_features.csv → filtered <name>_features.csv
```

Stages 1–5 delete their input after writing the next stage. Stage 6 overwrites
the feature export. Do not run a later stage until its expected input exists.

## Manual execution

```bash
python preprocessing/fetch_data.py
python preprocessing/mortgage/fred.py
python preprocessing/preprocess.py             # both datasets
python preprocessing/preprocess.py listings     # one dataset
python preprocessing/preprocess.py sold
```

Then execute these notebooks in order:

1. `null_analysis.ipynb`
2. `preprocessing/mortgage/merge.ipynb`
3. `validation.ipynb`
4. `school_districting.ipynb`

Finish with:

```bash
python features.py
python iqr_filter.py
```

## Other notebooks

- `segment_analysis.ipynb` explores the processed datasets.
- `tools/distribution_tool.ipynb` demonstrates reusable distribution helpers.
- `extra/prices.ipynb` and `extra/questions.ipynb` are archived explorations.

See [`preprocessing/README.md`](preprocessing/README.md) for source-data
configuration and [`tools/README.md`](tools/README.md) for the helper API.

# IDX Data Analysis

A reproducible pipeline for turning CRMLS real-estate exports into analysis-ready
listing and sold datasets. The project combines monthly CRMLS CSVs with FRED
30-year mortgage rates, validates and enriches the data, and produces feature
tables for Tableau and exploratory analysis.

## What it produces

- Residential listing and sold datasets for downstream analysis.
- Monthly mortgage-rate context from FRED's `MORTGAGE30US` series.
- Timeline, price, geographic, and school-district features.
- Tableau workbooks in [`workbooks/`](workbooks/).

Raw and generated CSVs are intentionally excluded from Git. See
[`data/processed/README.md`](data/processed/README.md) for the output contract.

## Project layout

```text
.
├── data/
│   ├── raw/                 # CRMLS exports, FRED rates, and DistrictAreas.geojson
│   └── processed/           # generated pipeline outputs
├── scripts/
│   ├── run_pipeline.sh      # execute the complete workflow
│   ├── preprocessing/       # FTP/FRED downloads and stage 0–2 processing
│   ├── null_analysis.ipynb  # stage 1: remove high-null columns
│   ├── validation.ipynb     # stage 3: clean and validate records
│   ├── school_districting.ipynb # stage 4: spatial school-district join
│   ├── features.py          # stage 5: derived analysis features
│   ├── iqr_filter.py        # stage 6: sequential IQR outlier filtering
│   ├── tools/               # reusable distribution-analysis helpers
│   └── extra/               # archived exploratory notebooks
└── workbooks/               # Tableau workbooks
```

More detailed documentation is available in [`scripts/README.md`](scripts/README.md),
[`scripts/preprocessing/README.md`](scripts/preprocessing/README.md), and
[`scripts/tools/README.md`](scripts/tools/README.md).

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

To execute notebook stages, also install Jupyter and the notebook-only packages:

```bash
pip install jupyter geopandas folium
```

## Configure CRMLS access

Copy the template and fill in the FTP values:

```bash
cp .env.example .env
```

The downloader reads `FTP_HOST`, `FTP_USER`, `FTP_PASS`, `LOCAL_DIR`, and
`REMOTE_DIR`. `LOCAL_DIR` defaults to `data/raw/`; `REMOTE_DIR` defaults to
`/csv`. Keep `.env` private.

## Run the pipeline

From the repository root:

```bash
scripts/run_pipeline.sh
```

Use existing files in `data/raw/` and skip both download steps with:

```bash
scripts/run_pipeline.sh --skip-fetch
```

The complete run executes the stages in order:

1. Download CRMLS listing/sold exports and monthly FRED rates.
2. Combine monthly exports and retain residential records.
3. Remove columns with more than 50% missing values.
4. Merge monthly mortgage rates.
5. Apply type, timeline, and California geographic checks.
6. Join school-district attributes using `data/raw/DistrictAreas.geojson`.
7. Add derived features and filter IQR outliers.

The pipeline runs from `scripts/`, so paths and notebook imports work regardless
of the directory from which the shell script is launched.

## Run individual stages

```bash
python scripts/preprocessing/fetch_data.py
python scripts/preprocessing/mortgage/fred.py
python scripts/preprocessing/preprocess.py             # listings and sold
python scripts/preprocessing/preprocess.py listings     # listings only
python scripts/preprocessing/preprocess.py sold        # sold only
python scripts/features.py
python scripts/iqr_filter.py
```

Stages 1–4 are notebooks and must be run in the order documented in
[`scripts/README.md`](scripts/README.md). The notebooks, `features.py`, and
`iqr_filter.py` modify or remove intermediate outputs, so keep a copy of any
dataset that must be preserved.

## Analysis helpers

The reusable plotting and summary functions in `scripts/tools/util/` are
documented in [`scripts/tools/README.md`](scripts/tools/README.md). Open
`distribution_tool.ipynb` for a working example.

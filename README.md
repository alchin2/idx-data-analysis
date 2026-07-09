# IDX Data Analysis

Tooling to turn raw CRMLS Data into analysis-ready datasets, enrich them with mortgage-rate
context, and explore them in notebooks.

## Layout

```
idx-data-analysis/
├── data/
│   ├── raw/        # source CSVs from CRMLS + FRED (gitignored)
│   └── processed/  # pipeline outputs (gitignored; see README.txt)
└── scripts/
    ├── preprocessing/   # fetch, combine, filter raw data
    │   ├── fetch_data.py    # download CRMLS CSVs from FTP
    │   ├── preprocess.py    # combine + residential filter -> combined_<name>.csv
    │   ├── utils.py         # shared path/CSV helpers
    │   └── mortgage/        # mortgage-rate fetch + merge
    │       ├── fred.py          # download monthly 30-yr rates from FRED
    │       └── merge.ipynb      # join rates onto pruned datasets
    └── tools/           # exploratory analysis notebooks + util package
```

Each subdirectory has its own README with details.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in FTP credentials
```

## Quickstart

```bash
# 1. fetch raw data
python scripts/preprocessing/fetch_data.py
python scripts/preprocessing/mortgage/fred.py

# 2. combine + filter (all, or: listings | sold)
python scripts/preprocessing/preprocess.py

# 3. prune high-null columns, then merge rates
#    run scripts/tools/null_analysis.ipynb, then
#    scripts/preprocessing/mortgage/merge.ipynb
```

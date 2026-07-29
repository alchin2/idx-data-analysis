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
    ├── null_analysis.ipynb        # prune high-null columns -> 1_<name>.csv
    ├── validation.ipynb           # type/timeline/geographic checks -> 3_<name>.csv
    ├── school_districting.ipynb   # join school district boundaries -> 4_<name>.csv
    ├── preprocessing/   # fetch, combine, filter raw data
    │   ├── fetch_data.py    # download CRMLS CSVs from FTP
    │   ├── preprocess.py    # combine + residential filter -> 0_<name>.csv
    │   ├── utils.py         # shared path/CSV helpers
    │   └── mortgage/        # mortgage-rate fetch + merge
    │       ├── fred.py          # download monthly 30-yr rates from FRED
    │       └── merge.ipynb      # join rates onto pruned datasets -> 2_<name>.csv
    ├── tools/           # distribution helpers + util package
    │   ├── distribution_tool.ipynb   # demo of the util/ helpers
    │   └── util/                     # reusable plotting/summary helpers
    └── extra/           # archived ad-hoc exploratory notebooks
        ├── prices.ipynb
        └── questions.ipynb
```

`scripts/` has its own README with the full pipeline breakdown; `preprocessing/` and
`tools/` each have their own README with details.

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

# 3. prune high-null columns, merge rates, validate, then join school districts
#    run these notebooks in order:
#      scripts/null_analysis.ipynb                -> 1_<name>.csv
#      scripts/preprocessing/mortgage/merge.ipynb -> 2_<name>.csv
#      scripts/validation.ipynb                   -> 3_<name>.csv
#      scripts/school_districting.ipynb           -> 4_<name>.csv
```

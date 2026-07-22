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
    ├── null_analysis.ipynb   # prune high-null columns -> combined_<name>_pruned.csv
    ├── validation.ipynb      # type/timeline/geographic checks -> <name>_validated.csv
    ├── preprocessing/   # fetch, combine, filter raw data
    │   ├── fetch_data.py    # download CRMLS CSVs from FTP
    │   ├── preprocess.py    # combine + residential filter -> combined_<name>.csv
    │   ├── utils.py         # shared path/CSV helpers
    │   └── mortgage/        # mortgage-rate fetch + merge
    │       ├── fred.py          # download monthly 30-yr rates from FRED
    │       └── merge.ipynb      # join rates onto pruned datasets -> <name>.csv
    ├── tools/           # distribution helpers + util package
    │   ├── distribution_tool.ipynb   # demo of the util/ helpers
    │   └── util/                     # reusable plotting/summary helpers
    └── extra/           # archived ad-hoc exploratory notebooks
        ├── prices.ipynb
        └── questions.ipynb
```

`preprocessing/` and `tools/` each have their own README with details.

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

# 3. prune high-null columns, merge rates, then validate
#    run these notebooks in order:
#      scripts/null_analysis.ipynb              -> combined_<name>_pruned.csv
#      scripts/preprocessing/mortgage/merge.ipynb -> <name>.csv
#      scripts/validation.ipynb                 -> <name>_validated.csv
```

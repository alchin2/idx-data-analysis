# Preprocessing Scripts

Scripts for fetching, cleaning, and combining raw CRMLS CSV exports into
analysis-ready datasets.

## Directory Structure

```
preprocessing/
├── fetch_data.py   # Downloads raw CRMLS CSVs from the FTP server
├── preprocess.py   # Combine + residential filter (listings, sold, or both)
├── utils.py        # Shared helpers (directory resolution, CSV processing)
└── mortgage/       # Mortgage-rate fetch + merge
    ├── fred.py         # Downloads monthly 30-yr mortgage rates from FRED
    └── merge.ipynb     # Joins rates onto the pruned datasets
```

## Usage

### 1. Fetch raw data

Fill in the `.env` file with login and directories:

```bash
cp .env.example .env
```

Download the raw CRMLS CSVs from the FTP server into `data/raw/`:

```bash
python fetch_data.py
```

This connects to the FTP server using credentials from `.env` and downloads
every `.csv` whose name starts with `CRMLSListing` or `CRMLSSold`.

Fetch the monthly mortgage rates (writes `data/raw/mortgage_rates.csv`):

```bash
python mortgage/fred.py
```

### 2. Preprocess

Run both pipelines together, or target one:

```bash
python preprocess.py           # both listings and sold
python preprocess.py listings  # listings only
python preprocess.py sold      # sold only
```

## Input / Output

| Target | Input (filename filter) | Output file |
|---|---|---|
| `listings` | `CRMLSListing*.csv` | `data/processed/combined_listings.csv` |
| `sold` | `CRMLSSold*.csv` | `data/processed/combined_sold.csv` |

Raw CSVs should be placed in `data/raw/` before running.

## What the scripts do

1. Glob all matching CSV files in `data/raw/`
2. Concatenate them into a single DataFrame
3. Filter rows where `PropertyType == "Residential"`
4. Sort by `ListingContractDate` ascending
5. Write the result to `data/processed/`

The scripts print a summary of total vs. residential record counts on completion.

## Next stages

These scripts produce the stage-1 `combined_*.csv` files. Column pruning
(`scripts/tools/null_analysis.ipynb`) and the mortgage-rate merge
(`mortgage/merge.ipynb`) run afterward. See `data/processed/README.txt` for the
full naming convention.

## Dependencies

See `requirements.txt` in the project root.

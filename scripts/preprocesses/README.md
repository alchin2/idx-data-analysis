# Preprocessing Scripts

Scripts for cleaning and combining raw CRMLS CSV exports into analysis-ready datasets. All scripts filter to **residential properties only** and write output to `data/processed/`.

## Directory Structure

```
preprocesses/
├── preprocess.py   # Main entry point — runs listings + sold in sequence
├── listing.py      # Standalone script for listings only
├── sold.py         # Standalone script for sold properties only
└── utils.py        # Shared helpers (directory resolution, CSV processing)
```

## Usage

Run both pipelines together:

```bash
python preprocess.py
```

Or run each pipeline individually:

```bash
python listing.py   # produces combined_listings.csv
python sold.py      # produces combined_sold.csv
```

## Input / Output

| Script | Input key (filename filter) | Output file |
|---|---|---|
| `listing.py` | `CRMLSListing*.csv` | `data/processed/combined_listings.csv` |
| `sold.py` | `CRMLSSold*.csv` | `data/processed/combined_sold.csv` |

Raw CSVs should be placed in `data/raw/` before running.

## What the scripts do

1. Glob all matching CSV files in `data/raw/`
2. Concatenate them into a single DataFrame
3. Filter rows where `PropertyType == "Residential"`
4. Sort by `ListingContractDate` ascending
5. Write the result to `data/processed/`

The scripts print a summary of total vs. residential record counts on completion.

## Dependencies

See `requirements.txt` in the project root. 

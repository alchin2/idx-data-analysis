# Processed datasets

The CSVs in this directory are gitignored; only this README is tracked.
Don't hand-edit them — regenerate. Don't use ad-hoc tags like "v2".

## What should be here

At the end of a clean pipeline run, exactly these files should exist:

| File | Produced by | Notes |
|---|---|---|
| `4_listings.csv` | `scripts/school_districting.ipynb` | Canonical clean listings dataset |
| `4_sold.csv` | `scripts/school_districting.ipynb` | Canonical clean sold dataset |
| `listings_features.csv` | `scripts/features.py` | `4_listings.csv` + Tableau market-indicator columns |
| `sold_features.csv` | `scripts/features.py` | `4_sold.csv` + Tableau market-indicator columns |

Everything upstream of `4_<name>.csv` (`0_<name>.csv` through `3_<name>.csv`)
is transient: each stage reads the previous stage's file, transforms it,
writes its own numbered output, and deletes the file it read. So mid-run
you'll see one numbered pair at a time; only the two above should remain
once `school_districting.ipynb` finishes.

`features.py` breaks that delete-on-read pattern on purpose — it's a
terminal export for Tableau, not a pipeline hand-off, so it reads
`4_<name>.csv` but keeps it as the reusable clean-data checkpoint.

## Full stage list (for reference)

  0_<name>.csv   concatenated raw + residential filter (preprocess.py)
  1_<name>.csv   high-null columns dropped (null_analysis.ipynb)
  2_<name>.csv   merged with monthly mortgage rates (merge.ipynb)
  3_<name>.csv   type/timeline/geographic checks applied (validation.ipynb)
  4_<name>.csv   joined with school district boundaries (school_districting.ipynb)
  <name>_features.csv   4_<name>.csv + Tableau feature columns (features.py)

See `scripts/README.md` for the full pipeline breakdown and the
`features.py` column/formula definitions.

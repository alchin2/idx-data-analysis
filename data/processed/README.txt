Processed datasets
==================

Files are named <name>_<stage>, where <name> is "listings" or "sold".
The CSVs are gitignored; only this README is tracked.

  combined_<name>.csv          concatenated raw + residential filter
  combined_<name>_pruned.csv   high-null columns dropped
  <name>_with_rates.csv        merged with monthly mortgage rates

Each stage is generated from the one before it (see the scripts/ READMEs).
Don't hand-edit; regenerate. Don't use ad-hoc tags like "v2".

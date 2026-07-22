Processed datasets
==================

Files are named <name>_<stage>, where <name> is "listings" or "sold".
The CSVs are gitignored; only this README is tracked.

  combined_<name>.csv          concatenated raw + residential filter (preprocess.py)
  combined_<name>_pruned.csv   high-null columns dropped (null_analysis.ipynb)
  <name>.csv                   merged with monthly mortgage rates (merge.ipynb)
  <name>_validated.csv         type/timeline/geographic checks applied (validation.ipynb)

Note: the validated listings file is named listing_validated.csv (singular).

Each stage is generated from the one before it (see the scripts/ READMEs).
Don't hand-edit; regenerate. Don't use ad-hoc tags like "v2".

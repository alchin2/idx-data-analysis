Processed datasets
==================

Files are named <index>_<name>.csv, where <index> is the pipeline stage
(0-4) and <name> is "listings" or "sold". The CSVs are gitignored; only
this README is tracked.

  0_<name>.csv   concatenated raw + residential filter (preprocess.py)
  1_<name>.csv   high-null columns dropped (null_analysis.ipynb)
  2_<name>.csv   merged with monthly mortgage rates (merge.ipynb)
  3_<name>.csv   type/timeline/geographic checks applied (validation.ipynb)
  4_<name>.csv   joined with school district boundaries (school_districting.ipynb)

Each stage reads the previous stage's file and deletes it after writing its
own output, so only the highest-numbered file per dataset should exist on
disk at a time.

Don't hand-edit; regenerate. Don't use ad-hoc tags like "v2".

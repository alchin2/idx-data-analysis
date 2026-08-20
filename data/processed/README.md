# Processed datasets

This directory stores generated CSVs and is ignored by Git. Regenerate the
files with the pipeline; do not hand-edit them or add version-like filenames.

## Final outputs

After a complete run, the expected final exports are:

| File | Created by | Description |
|---|---|---|
| `listings_features.csv` | `features.py` | Listing data plus derived features |
| `sold_features.csv` | `features.py` | Sold data plus derived features |

`iqr_filter.py` applies sequential IQR filters to the feature files in place.
It checks whichever of these columns are present: `price_per_sqft`,
`ClosePrice`, `price_ratio`, and `days_on_market`.

## Intermediate files

The numbered files represent pipeline hand-offs:

```text
0_<name>.csv  raw files combined and filtered to residential records
1_<name>.csv  columns with more than 50% missing values removed
2_<name>.csv  monthly mortgage rates merged
3_<name>.csv  type, timeline, and geographic validation applied
4_<name>.csv  school-district attributes joined
```

Stages 1–5 delete their input after writing the next file, so numbered outputs
are temporary. The feature files are the terminal exports used by Tableau and
analysis notebooks.

See [`scripts/README.md`](../../scripts/README.md) for the complete stage order
and commands.

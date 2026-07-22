# Analysis Tools

Shared plotting/summary helpers and a demo notebook that run against the processed
datasets in `data/processed/`.

## Directory Structure

```
tools/
├── distribution_tool.ipynb   # Demo of the distribution helpers in util/
└── util/                     # Reusable helpers
    ├── distribution.py        # distribution_summary + plot_distribution
    └── formatters.py          # FixedOrderFormatter
```

> The pipeline notebooks `null_analysis.ipynb` and `validation.ipynb` live at the
> `scripts/` root; archived ad-hoc notebooks (`prices.ipynb`, `questions.ipynb`)
> live in `scripts/extra/`.

## `util` package

The notebooks import shared helpers from the `util` package:

```python
from util import distribution_summary, plot_distribution
```

### `distribution_summary(data, columns=None, percentiles=...)`

Summarize the distribution of one or more numeric columns. Returns `count`, `min`,
`max`, `mean`, `median`, and the requested percentiles.

### `plot_distribution(data, column=None, ...)`

Plot a numeric column across three panels — the bulk (`<= pct`), the upper tail
below `extreme_cutoff`, and the extreme tail at or above it — so long-tailed values
(e.g. prices) stay readable. Uses a log y-scale by default.

### `FixedOrderFormatter(order)`

A `matplotlib` `ScalarFormatter` that pins the axis offset to a fixed power of 10,
keeping tick labels consistent across panels.

## Usage

Open any notebook from this directory so the `util` package resolves on import.
The notebooks load data relative to the repo root, e.g.:

```python
from pathlib import Path
base_dir = Path.cwd().parent.parent
data_path = base_dir / "data" / "processed"
```

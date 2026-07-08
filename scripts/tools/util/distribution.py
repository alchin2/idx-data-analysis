import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .formatters import FixedOrderFormatter


def _resolve_series(data, column=None):
    """Accept either a Series or a (DataFrame, column) pair and return (series, name)."""
    if column is not None:
        return data[column], column
    name = data.name if data.name is not None else "value"
    return data, name


def _summarize_series(series, name, percentiles):
    """Build a distribution-summary Series for a single column of values."""
    s = series.dropna()

    summary = {
        "count": s.count(),
        "min": s.min(),
        "max": s.max(),
        "mean": s.mean(),
        "median": s.median(),
    }
    for p in percentiles:
        summary[f"p{p * 100:g}"] = s.quantile(p)

    return pd.Series(summary, name=name)


def distribution_summary(data,columns=None, percentiles=(0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99)):
    """Summarize the distribution of one or more numeric columns.

    Parameters
    ----------
    data : original data
       
    columns : columns to extract
        
    percentiles : percentiles to be displayed
    """
    if isinstance(columns, (list, tuple)):
        summaries = [
            _summarize_series(data[col], col, percentiles) for col in columns
        ]
        return pd.concat(summaries, axis=1)

    series, name = _resolve_series(data, columns)
    return _summarize_series(series, name, percentiles)


def plot_distribution(data,column=None,title=None,pct=0.99,extreme_cutoff=100_000_000,bins=20,n_ticks=10,log=True,):
    """Plot the distribution of any numeric column across three tiers.

    Parameters
    ----------
    data : the original data
        
    column : column to extract
       
    title : title of plot
        Figure title. Defaults to the column/series name.
    pct : panel 1 and panel 2 cut offs

    extreme_cutoff : panel 3 cut off
        
    bins : num of histogram bins

    n_ticks : ticks on x-axis

    log : Whether to use a log scale on the y-axis.
    """
    series, name = _resolve_series(data, column)

    if title is None:
        title = f"{name} Distribution"

    s = series.dropna()

    ub = s.quantile(pct)  # threshold between bulk and upper tail

    bulk = s[s <= ub]                              # lower `pct` of the data
    upper = s[s > ub]                              # upper (1 - pct) tail
    mid = upper[upper < extreme_cutoff]            # upper tail, below cutoff
    extreme = upper[upper >= extreme_cutoff]       # extreme tail

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle(title)

    def order_of_mag(x):
        return int(np.floor(np.log10(x))) if x and x > 0 else 0

    # Panel 1
    ax1.hist(bulk, bins=bins)
    ax1.set_title(f"Lower {pct:.0%}")
    if log:
        ax1.set_yscale("log")
    if len(bulk):
        ax1.set_xticks(np.linspace(0, bulk.max(), n_ticks))
        ax1.xaxis.set_major_formatter(FixedOrderFormatter(order_of_mag(bulk.max())))

    # Panel 2
    ax2.hist(mid, bins=bins)
    ax2.set_title(f"Upper {1 - pct:.0%} (under {extreme_cutoff:,.0f})")
    if log:
        ax2.set_yscale("log")
    if len(mid):
        ax2.xaxis.set_major_formatter(FixedOrderFormatter(order_of_mag(mid.max())))

    # Panel 3
    ax3.hist(extreme, bins=max(bins // 2, 1))
    ax3.set_title(f"At or above {extreme_cutoff:,.0f}")
    if log:
        ax3.set_yscale("log")
    if len(extreme):
        ax3.xaxis.set_major_formatter(FixedOrderFormatter(order_of_mag(extreme.max())))

    return fig, (ax1, ax2, ax3)

import argparse
import pandas as pd
from pathlib import Path

NUMERIC_COLS = ["ClosePrice", "LivingArea", "DaysOnMarket"]

DATASETS = {
    "listings": "combined_listings.csv",
    "sold": "combined_sold.csv",
}


def numeric_distribution(df):
    rows = {}
    for col in NUMERIC_COLS:
        series = pd.to_numeric(df[col]).dropna()
        stats = {
            "count": series.count(),
            "min": series.min(),
            "max": series.max(),
            "mean": series.mean(),
            "median": series.median(),
        }
        rows[col] = stats

    stats_df = pd.DataFrame(rows)
    with pd.option_context(
        "display.float_format", lambda v: f"{v:,.2f}", "display.max_columns", None
    ):
        print(stats_df)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dataset",
        choices=[*DATASETS, "both"],
        default="both",
        help="Which processed dataset(s) to summarize (default: both).",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    base_dir = Path(__file__).resolve().parent.parent
    processed_dir = base_dir / "data" / "processed"

    selected = DATASETS if args.dataset == "both" else {args.dataset: DATASETS[args.dataset]}

    for name, filename in selected.items():
        source = processed_dir / filename
        print("=" * 60)
        print(f"[{name}] Reading source: {source}")
        print("=" * 60)
        df = pd.read_csv(source, low_memory=False)
        numeric_distribution(df)
        print()


if __name__ == "__main__":
    main()

import argparse
import pandas as pd
from pathlib import Path

NULL_FLAG_THRESHOLD = 0.90

DATASETS = {
    "listings": "combined_listings.csv",
    "sold": "combined_sold.csv",
}


def missing_value_report(df, threshold=NULL_FLAG_THRESHOLD):
    null_pct = (df.isnull().mean()).sort_values(ascending=False)
    flagged = null_pct[null_pct > threshold]

    if flagged.empty:
        print(f"No columns exceed {threshold:.0%} null values.")
    else:
        print(f"{len(flagged)} column(s) flagged:\n")
        print(f"{'column':<32}{'null_pct':>10}")
        print("-" * 42)
        for col, pct in flagged.items():
            print(f"{col:<32}{pct:>10.1%}")


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dataset",
        choices=[*DATASETS, "both"],
        default="both",
        help="Which processed dataset(s) to analyze (default: both).",
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
        missing_value_report(df)
        print()


if __name__ == "__main__":
    main()

import sys

from utils import get_directories, process_listings

# name -> (filename filter key, output file)
PIPELINES = {
    "listings": ("CRMLSListing", "combined_listings.csv"),
    "sold": ("CRMLSSold", "combined_sold.csv"),
}


def run_pipeline(name):
    """Combine + filter one dataset (listings or sold) and write its CSV."""
    key, output_name = PIPELINES[name]
    raw_path, processed_path = get_directories()

    print(f"\n--- Processing {name} ---\n")
    print(f"Processing {name} from raw directory: {raw_path}")
    combined, (total, residential) = process_listings(raw_path, key)

    output = processed_path / output_name
    combined.to_csv(output, index=False)

    pct = residential / total * 100 if total else 0
    print("=" * 60)
    print(
        f"Total {name} processed: {total}\n"
        f"Residential {name} saved: {residential}\n"
        f"Approximately {pct:.2f}% of total {name} are residential."
    )
    print(f"Saved to: {output}")
    print("=" * 60)


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "all"

    print("=" * 60)
    print("Preprocessing CRMLS Data")
    print("=" * 60)

    if target == "all":
        names = list(PIPELINES)
    elif target in PIPELINES:
        names = [target]
    else:
        valid = ", ".join([*PIPELINES, "all"])
        sys.exit(f"Unknown target '{target}'. Choose one of: {valid}")

    for name in names:
        run_pipeline(name)


if __name__ == "__main__":
    main()

# Listing: 838693 -> 533052
# Sold: 681599 -> 458336
# Total: 1,520,292 -> 991,388 (residential properties only)

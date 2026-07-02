import pandas as pd
from utils import get_directories

COLUMNS_TO_DROP = [
    "FireplacesTotal",
    "ElementarySchoolDistrict",
    "CoveredSpaces",
    "TaxYear",
    "BusinessType",
    "TaxAnnualAmount",
    "AboveGradeFinishedArea",
    "MiddleOrJuniorSchoolDistrict",
    "BelowGradeFinishedArea",
    "CoBuyerAgentFirstName",
    "BuilderName",
    "LotSizeDimensions",
    "BuyerAgencyCompensation",
    "BuyerAgencyCompensationType",
    "BuildingAreaTotal",
    "WaterfrontYN",
    "BasementYN"
]

DATASETS = {
    "listings": ("combined_listings.csv", "combined_listingsv2.csv"),
    "sold": ("combined_sold.csv", "combined_soldv2.csv"),
}


def prune_dataset(processed_path, source_name, output_name):
    source = processed_path / source_name
    output = processed_path / output_name

    print(f"Reading source: {source}")
    df = pd.read_csv(source, low_memory=False)

    present = [c for c in COLUMNS_TO_DROP if c in df.columns]
    pruned = df.drop(columns=present)

    print("=" * 60)
    print(f"Requested to drop : {len(COLUMNS_TO_DROP)} column(s)")
    print(f"Present & dropped : {len(present)} column(s)")
    print(f"Columns: {df.shape[1]} -> {pruned.shape[1]}")
    print("=" * 60)

    pruned.to_csv(output, index=False)
    print(f"Wrote {len(pruned):,} rows x {pruned.shape[1]} cols to:")
    print(f"  {output}")


def main():
    _, processed_path = get_directories()

    for name, (source_name, output_name) in DATASETS.items():
        print(f"\n### {name} ###")
        prune_dataset(processed_path, source_name, output_name)


if __name__ == "__main__":
    main()

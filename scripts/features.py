from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

FILES = {
    "listings": PROCESSED_DIR / "4_listings.csv",
    "sold": PROCESSED_DIR / "4_sold.csv",
}


def add_price_features(df):
    if {"ClosePrice", "OriginalListPrice"}.issubset(df.columns):
        df["price_ratio"] = df["close_to_original_list_ratio"] = df["ClosePrice"] / df["OriginalListPrice"]

    if {"ClosePrice", "LivingArea"}.issubset(df.columns):
        df["price_per_sqft"] = df["ClosePrice"] / df["LivingArea"]

    return df


def add_days_on_market(df):
    if "DaysOnMarket" in df.columns:
        df["days_on_market"] = df["DaysOnMarket"]

    return df


def add_close_date_parts(df):
    if "CloseDate" in df.columns:
        close_date = pd.to_datetime(df["CloseDate"], errors="coerce")
        df["year"] = close_date.dt.year
        df["month"] = close_date.dt.month
        df["yr_mo"] = close_date.dt.to_period("M").astype(str)
        
    return df


def add_timeline_features(df):
    if {"PurchaseContractDate", "ListingContractDate"}.issubset(df.columns):
        purchase_date = pd.to_datetime(df["PurchaseContractDate"], errors="coerce")
        listing_date = pd.to_datetime(df["ListingContractDate"], errors="coerce")
        df["listing_to_contract_days"] = (purchase_date - listing_date).dt.days

    if {"CloseDate", "PurchaseContractDate"}.issubset(df.columns):
        close_date = pd.to_datetime(df["CloseDate"], errors="coerce")
        purchase_date = pd.to_datetime(df["PurchaseContractDate"], errors="coerce")
        df["contract_to_close_days"] = (close_date - purchase_date).dt.days

    return df


FEATURE_STEPS = [
    add_price_features,
    add_days_on_market,
    add_close_date_parts,
    add_timeline_features,
]


def main():
    for name, path in FILES.items():
        df = pd.read_csv(path, low_memory=False)
        before = set(df.columns)

        for step in FEATURE_STEPS:
            df = step(df)

        output = PROCESSED_DIR / f"{name}_features.csv"
        df.to_csv(output, index=False)

        added = [c for c in df.columns if c not in before]
        print(f"[{name}] {len(df):,} rows x {df.shape[1]} cols, added: {added or 'none'}")
        print(f"[{name}] wrote {output}")


if __name__ == "__main__":
    main()

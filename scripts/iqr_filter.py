from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

FILES = {
    "listings": PROCESSED_DIR / "listings_features.csv",
    "sold": PROCESSED_DIR / "sold_features.csv",
}

COLUMNS_TO_FILTER = ["price_per_sqft","ClosePrice","price_ratio","days_on_market"]

def iqr_filter(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return df[(df[column] >= lower) & (df[column] <= upper)]

def stats(df, column):
    print("=" * 40)
    print(df[column].agg(['max', 'min', 'mean', 'median', 'std']).round(2))
    print("=" * 40)

def main():
    for key, file in FILES.items():
        df = pd.read_csv(file)
        for column in COLUMNS_TO_FILTER:
            if column in df.columns:
                df = iqr_filter(df, column)
                print(f"Before filtering {column} in {key} dataset:")
                print(stats(df, column))
                print(f"After filtering {column} in {key} dataset:")
                print(stats(df, column))
            else:
                print(f"Column '{column}' not found in {key} dataset.")
        df.to_csv(file, index=False)

if __name__ == "__main__":
    main()

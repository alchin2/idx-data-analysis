from pathlib import Path

import pandas as pd

# scripts/preprocessing/mortgage/fred.py -> repo root
RAW_DIR = Path(__file__).resolve().parents[3] / "data" / "raw"

url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
df = pd.read_csv(url, parse_dates=['observation_date'])
df.columns = ['date', 'rate']


df['year_month'] = df['date'].dt.to_period('M')

mortgage_monthly = (
    df.groupby('year_month')['rate']
    .mean()
    .reset_index()
)

RAW_DIR.mkdir(parents=True, exist_ok=True)
mortgage_monthly.to_csv(RAW_DIR / "mortgage_rates.csv", index=False)

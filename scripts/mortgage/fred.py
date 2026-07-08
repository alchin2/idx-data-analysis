import pandas as pd


url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
df = pd.read_csv(url, parse_dates=['observation_date'])
df.columns = ['date', 'rate']


df['year_month'] = df['date'].dt.to_period('M')

mortgage_monthly = (
    df.groupby('year_month')['rate']
    .mean()
    .reset_index()
)

mortgage_monthly.to_csv('data/raw/mortgage_rates.csv', index=False)
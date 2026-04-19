import pandas as pd
import pandas_datareader.data as web
from datetime import datetime

start = datetime(2009, 1, 1)
end   = datetime(2024, 12, 31)

gdp_raw = web.DataReader('GDPC1',    'fred', start, end)
cpi_raw = web.DataReader('CPIAUCSL', 'fred', start, end)

gdp_raw.index = pd.PeriodIndex(gdp_raw.index, freq='Q')
gdp_raw['gdp_growth'] = gdp_raw['GDPC1'].pct_change()
gdp_quarterly = gdp_raw[['gdp_growth']].dropna()

cpi_raw.index = pd.PeriodIndex(cpi_raw.index, freq='M')
cpi_quarterly = (
    cpi_raw.groupby(cpi_raw.index.asfreq('Q'))['CPIAUCSL']
    .last()
    .pct_change()
    .dropna()
    .rename('inflation')
    .to_frame()
)

macro = gdp_quarterly.join(cpi_quarterly, how='inner')
macro.index.name = 'quarter'
macro = macro.reset_index()
macro['quarter'] = macro['quarter'].astype(str)

macro = macro[macro['quarter'] >= '2010Q1'].reset_index(drop=True)

macro.to_csv('wrds_fred_macro.csv', index=False)

print(f"Quarters     : {len(macro)}")
print(f"Date range   : {macro['quarter'].iloc[0]} to {macro['quarter'].iloc[-1]}")
print(f"\nSample:")
print(macro.head(8).to_string(index=False))
print(f"\nSaved: wrds_fred_macro.csv")

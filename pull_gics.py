import psycopg2
import pandas as pd
import numpy as np
import os

USERNAME = os.environ['WRDS_USERNAME']
PASSWORD = os.environ['WRDS_PASSWORD']

def query(sql):
    conn = psycopg2.connect(
        host='wrds-pgdata.wharton.upenn.edu', port=9737,
        dbname='wrds', user=USERNAME, password=PASSWORD,
        sslmode='require', connect_timeout=30
    )
    cur = conn.cursor()
    cur.execute(sql)
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return pd.DataFrame(rows, columns=cols)

sector_map = {
    '10': 'Energy',
    '15': 'Materials',
    '20': 'Industrials',
    '25': 'Consumer Discretionary',
    '30': 'Consumer Staples',
    '35': 'Health Care',
    '40': 'Financials',
    '45': 'Information Technology',
    '50': 'Communication Services',
    '55': 'Utilities',
    '60': 'Real Estate'
}

def sic_to_gsector(sic):
    if pd.isna(sic):
        return None
    sic = int(sic)
    if   100  <= sic <= 999:  return '15'
    elif 1000 <= sic <= 1499: return '15'
    elif 1500 <= sic <= 1799: return '20'
    elif 1800 <= sic <= 1999: return '20'
    elif 2000 <= sic <= 2111: return '30'
    elif 2112 <= sic <= 2199: return '30'
    elif 2200 <= sic <= 2299: return '25'
    elif 2300 <= sic <= 2399: return '25'
    elif 2400 <= sic <= 2499: return '25'
    elif 2500 <= sic <= 2599: return '25'
    elif 2600 <= sic <= 2699: return '15'
    elif 2700 <= sic <= 2799: return '25'
    elif 2800 <= sic <= 2899: return '15'
    elif 2900 <= sic <= 2999: return '10'
    elif 3000 <= sic <= 3099: return '15'
    elif 3100 <= sic <= 3199: return '25'
    elif 3200 <= sic <= 3299: return '15'
    elif 3300 <= sic <= 3399: return '15'
    elif 3400 <= sic <= 3499: return '20'
    elif 3500 <= sic <= 3559: return '20'
    elif 3560 <= sic <= 3579: return '20'
    elif 3580 <= sic <= 3599: return '20'
    elif 3600 <= sic <= 3674: return '45'
    elif 3675 <= sic <= 3699: return '45'
    elif 3700 <= sic <= 3799: return '25'
    elif 3800 <= sic <= 3829: return '35'
    elif 3830 <= sic <= 3899: return '20'
    elif 3900 <= sic <= 3999: return '25'
    elif 4000 <= sic <= 4099: return '20'
    elif 4100 <= sic <= 4499: return '20'
    elif 4500 <= sic <= 4599: return '20'
    elif 4600 <= sic <= 4699: return '10'
    elif 4700 <= sic <= 4799: return '20'
    elif 4800 <= sic <= 4899: return '50'
    elif 4900 <= sic <= 4999: return '55'
    elif 5000 <= sic <= 5199: return '20'
    elif 5200 <= sic <= 5999: return '25'
    elif 6000 <= sic <= 6199: return '40'
    elif 6200 <= sic <= 6299: return '40'
    elif 6300 <= sic <= 6399: return '40'
    elif 6400 <= sic <= 6499: return '40'
    elif 6500 <= sic <= 6599: return '60'
    elif 6600 <= sic <= 6999: return '40'
    elif 7000 <= sic <= 7099: return '25'
    elif 7100 <= sic <= 7199: return '25'
    elif 7200 <= sic <= 7299: return '25'
    elif 7300 <= sic <= 7369: return '20'
    elif 7370 <= sic <= 7379: return '45'
    elif 7380 <= sic <= 7399: return '20'
    elif 7400 <= sic <= 7699: return '25'
    elif 7700 <= sic <= 7999: return '25'
    elif 8000 <= sic <= 8099: return '35'
    elif 8100 <= sic <= 8199: return '20'
    elif 8200 <= sic <= 8299: return '25'
    elif 8300 <= sic <= 8399: return '25'
    elif 8400 <= sic <= 8499: return '25'
    elif 8600 <= sic <= 8699: return '25'
    elif 8700 <= sic <= 8799: return '20'
    elif 8900 <= sic <= 8999: return '20'
    else: return None

comp_csv = pd.read_csv('wrds_compustat_quarterly.csv', low_memory=False)
crsp_csv = pd.read_csv('wrds_crsp_quarterly.csv', low_memory=False)
gvkeys   = tuple(comp_csv['gvkey'].astype(str).unique().tolist())

gics_direct = query(f"""
    SELECT gvkey, gsector, sic
    FROM comp_na_daily_all.company
    WHERE gvkey IN {gvkeys}
      AND gsector IS NOT NULL
""")
gics_direct['gvkey']       = gics_direct['gvkey'].astype(str)
gics_direct['gsector']     = gics_direct['gsector'].astype(str).str.strip()
gics_direct['sector_name'] = gics_direct['gsector'].map(sector_map)
gics_direct['source']      = 'GICS (WRDS)'

covered = set(gics_direct['gvkey'].unique())
all_gvkeys = set(comp_csv['gvkey'].astype(str).unique())
missing_gvkeys = all_gvkeys - covered

tic_to_gvkey = comp_csv[['gvkey','tic']].drop_duplicates()
tic_to_gvkey['gvkey'] = tic_to_gvkey['gvkey'].astype(str)

crsp_sic = (
    crsp_csv[['ticker','siccd']]
    .dropna(subset=['siccd'])
    .drop_duplicates(subset='ticker', keep='last')
)

sic_fallback = (
    tic_to_gvkey[tic_to_gvkey['gvkey'].isin(missing_gvkeys)]
    .merge(crsp_sic, left_on='tic', right_on='ticker', how='left')
    [['gvkey','siccd']]
    .drop_duplicates(subset='gvkey')
)

sic_fallback['gsector']     = sic_fallback['siccd'].apply(sic_to_gsector)
sic_fallback['sector_name'] = sic_fallback['gsector'].map(sector_map)
sic_fallback['sic']         = sic_fallback['siccd']
sic_fallback['source']      = 'SIC mapping (CRSP fallback)'
sic_fallback = sic_fallback[['gvkey','gsector','sic','sector_name','source']].dropna(subset=['gsector'])

gics_final = pd.concat([
    gics_direct[['gvkey','gsector','sic','sector_name','source']],
    sic_fallback
], ignore_index=True).drop_duplicates(subset='gvkey')

gics_final.to_csv('wrds_gics_sectors.csv', index=False)

total        = len(all_gvkeys)
gics_count   = len(gics_direct)
sic_count    = len(sic_fallback)
still_missing = total - len(gics_final)

print(f"Total companies in Compustat  : {total}")
print(f"  GICS codes (WRDS direct)    : {gics_count}")
print(f"  SIC mapping (CRSP fallback) : {sic_count}")
print(f"  Still no sector assigned    : {still_missing}")
print(f"\nSector distribution:")
print(gics_final['sector_name'].value_counts().to_string())
print(f"\nSaved: wrds_gics_sectors.csv")

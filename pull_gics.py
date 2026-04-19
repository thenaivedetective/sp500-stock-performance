import psycopg2
import pandas as pd
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

comp = pd.read_csv('wrds_compustat_quarterly.csv', low_memory=False)
gvkeys = tuple(comp['gvkey'].astype(str).unique().tolist())

gics = query(f"""
    SELECT gvkey, gsector, ggroup, gind, gsubind, sic
    FROM comp_na_daily_all.company
    WHERE gvkey IN {gvkeys}
""")

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

gics['sector_name'] = gics['gsector'].astype(str).map(sector_map)
gics.to_csv('wrds_gics_sectors.csv', index=False)

print(f"Companies with GICS codes : {len(gics)}")
print(f"Sector distribution:")
print(gics['sector_name'].value_counts().to_string())
print(f"\nSaved: wrds_gics_sectors.csv")

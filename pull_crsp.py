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

fundq = pd.read_csv('wrds_compustat_quarterly.csv')
tickers = tuple(fundq['tic'].dropna().unique().tolist())

msf = query(f"""
    SELECT m.permno, m.date, m.ret,
           n.ticker, n.comnam, n.exchcd, n.siccd
    FROM crsp.msf m
    JOIN crsp.msenames n
      ON m.permno = n.permno
      AND m.date BETWEEN n.namedt AND COALESCE(n.nameendt, '2024-12-31')
    WHERE m.date BETWEEN '2010-01-01' AND '2024-12-31'
    AND n.ticker IN {tickers}
    AND m.ret IS NOT NULL
    ORDER BY n.ticker, m.date
""")

msi = query("""
    SELECT date, sprtrn
    FROM crsp.msi
    WHERE date BETWEEN '2010-01-01' AND '2024-12-31'
    ORDER BY date
""")

msf['date'] = pd.to_datetime(msf['date'])
msi['date'] = pd.to_datetime(msi['date'])

msf['quarter'] = msf['date'].dt.to_period('Q')
msi['quarter'] = msi['date'].dt.to_period('Q')

def compound(returns):
    return (1 + returns).prod() - 1

stock_quarterly = (
    msf.groupby(['ticker', 'comnam', 'exchcd', 'siccd', 'quarter'])['ret']
    .apply(compound)
    .reset_index()
    .rename(columns={'ret': 'quarterly_return'})
)

spy_quarterly = (
    msi.groupby('quarter')['sprtrn']
    .apply(compound)
    .reset_index()
    .rename(columns={'sprtrn': 'spy_quarterly_return'})
)

crsp_quarterly = stock_quarterly.merge(spy_quarterly, on='quarter', how='left')

crsp_quarterly['outperformer_quarterly'] = (
    crsp_quarterly['quarterly_return'] > crsp_quarterly['spy_quarterly_return']
).astype(int)

crsp_quarterly['quarter_str'] = crsp_quarterly['quarter'].astype(str)
crsp_quarterly['year'] = crsp_quarterly['quarter'].dt.year
crsp_quarterly['q'] = crsp_quarterly['quarter'].dt.quarter

crsp_quarterly = crsp_quarterly.sort_values(['ticker', 'quarter']).reset_index(drop=True)

crsp_quarterly.to_csv('wrds_crsp_quarterly.csv', index=False)

print(f"Rows          : {len(crsp_quarterly)}")
print(f"Tickers       : {crsp_quarterly['ticker'].nunique()}")
print(f"Date range    : {crsp_quarterly['quarter'].min()} to {crsp_quarterly['quarter'].max()}")
print(f"Outperformers : {crsp_quarterly['outperformer_quarterly'].sum()} ({crsp_quarterly['outperformer_quarterly'].mean()*100:.1f}%)")
print(f"Saved         : wrds_crsp_quarterly.csv")

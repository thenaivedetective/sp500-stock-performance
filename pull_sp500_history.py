import pandas as pd
import psycopg2
import os

conn = psycopg2.connect(
    host='wrds-pgdata.wharton.upenn.edu', port=9737, dbname='wrds',
    user=os.environ['WRDS_USERNAME'], password=os.environ['WRDS_PASSWORD'],
    sslmode='require'
)

query = """
    SELECT
        h.gvkey,
        h.from   AS start_date,
        h.thru   AS end_date
    FROM comp.idxcst_his h
    WHERE h.gvkeyx = '000003'
      AND (h.thru IS NULL OR h.thru >= '2010-01-01')
      AND h.from <= '2024-12-31'
"""

df = pd.read_sql(query, conn)
conn.close()

df['start_date'] = pd.to_datetime(df['start_date'])
df['end_date']   = pd.to_datetime(df['end_date'])
df['end_date']   = df['end_date'].fillna(pd.Timestamp('2024-12-31'))

df.to_csv('wrds_sp500_history.csv', index=False)

print(f"Historical S&P 500 constituents : {df['gvkey'].nunique()} unique companies")
print(f"Date range covered              : 2010-01-01 to 2024-12-31")
print(f"\nSample:")
print(df.head(8).to_string(index=False))
print(f"\nSaved: wrds_sp500_history.csv")

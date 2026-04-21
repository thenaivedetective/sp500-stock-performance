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

sp500 = query("""
    SELECT DISTINCT gvkey
    FROM comp_na_daily_all.idxcst_his
    WHERE gvkeyx = '000003'
    AND (thru >= '2010-01-01' OR thru IS NULL)
""")

gvkeys = tuple(sp500['gvkey'].tolist())

fundq = query(f"""
    SELECT
        gvkey, tic, conm, datadate, fyearq, fqtr, exchg,
        prccq, cshoq, mkvaltq,
        revtq, cogsq, xsgaq, xrdq,
        oibdpq, oiadpq, niq, ibq, piq,
        atq, ceqq, teqq, dlttq, dlcq,
        actq, lctq, cheq, dpq, txtq
    FROM comp_na_daily_all.fundq
    WHERE gvkey IN {gvkeys}
    AND datadate BETWEEN '2010-01-01' AND '2025-12-31'
    AND indfmt = 'INDL'
    AND datafmt = 'STD'
    AND popsrc = 'D'
    AND consol = 'C'
    ORDER BY gvkey, datadate
""")

fundq['datadate'] = pd.to_datetime(fundq['datadate'])
fundq['quarter'] = fundq['datadate'].dt.to_period('Q')

fundq.to_csv('wrds_compustat_quarterly.csv', index=False)

print(f"Rows        : {len(fundq)}")
print(f"Companies   : {fundq['gvkey'].nunique()}")
print(f"Date range  : {fundq['datadate'].min().strftime('%B %Y')} to {fundq['datadate'].max().strftime('%B %Y')}")
print(f"Saved       : wrds_compustat_quarterly.csv")

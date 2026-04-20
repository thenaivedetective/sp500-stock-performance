import os
import pandas as pd
import numpy as np
import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import edgar as edgarlib

edgarlib.set_identity('Lana Gidan lgidan@binghamton.edu')
SEC_HEADERS = {'User-Agent': 'Lana Gidan lgidan@binghamton.edu'}
EDGAR_CACHE = 'cache_edgar_q1_2025.csv'

if os.path.exists(EDGAR_CACHE):
    print(f"Cache already exists: {EDGAR_CACHE}")
    df = pd.read_csv(EDGAR_CACHE)
    print(f"Rows: {len(df)}")
    exit(0)

print("Pulling Q1 2025 financials from SEC EDGAR for S&P 500...")

comp      = pd.read_csv('wrds_compustat_quarterly.csv', low_memory=False)
comp['datadate']    = pd.to_datetime(comp['datadate'])
comp['cal_quarter'] = comp['datadate'].dt.to_period('Q')
tickers_sp500 = comp[comp['cal_quarter'] == pd.Period('2024Q4')]['tic'].dropna().unique().tolist()
print(f"Tickers to pull: {len(tickers_sp500)}")

TICKER_FIX = {'BRK.B': 'BRK-B', 'BRK.A': 'BRK-A', 'BF.B': 'BF-B', 'BF.A': 'BF-A'}

FLOW_TAGS = [
    'RevenueFromContractWithCustomerExcludingAssessedTax',
    'Revenues', 'SalesRevenueNet', 'SalesRevenueGoodsNet',
]
COGS_TAGS = ['CostOfGoodsAndServicesSold', 'CostOfRevenue', 'CostOfGoodsSold']
NI_TAGS   = ['NetIncomeLoss', 'NetIncome']
OI_TAGS   = ['OperatingIncomeLoss', 'OperatingIncome']

Q1_START    = pd.Timestamp('2025-01-01')
Q1_END      = pd.Timestamp('2025-04-15')
Q1_MIN_DAYS = 75
Q1_MAX_DAYS = 105

def pick_quarterly_flow(vals):
    candidates = []
    for v in vals:
        if v.get('form') not in ('10-Q', '10-K'):
            continue
        end_dt = pd.Timestamp(v['end']) if v.get('end') else None
        if end_dt is None or not (Q1_START <= end_dt <= Q1_END):
            continue
        if v.get('start'):
            dur = (end_dt - pd.Timestamp(v['start'])).days
            if Q1_MIN_DAYS <= dur <= Q1_MAX_DAYS:
                candidates.append((end_dt, v['val']))
        elif v.get('fp') in ('Q1', 'Q2', 'Q3'):
            candidates.append((end_dt, v['val']))
    if not candidates:
        return np.nan
    return sorted(candidates, key=lambda x: x[0])[-1][1]

def pick_stock_value(vals):
    candidates = []
    for v in vals:
        if v.get('form') not in ('10-Q', '10-K', '10-Q/A', '10-K/A'):
            continue
        end_dt = pd.Timestamp(v['end']) if v.get('end') else None
        if end_dt is None or not (Q1_START <= end_dt <= Q1_END):
            continue
        candidates.append((end_dt, v['val']))
    if not candidates:
        return np.nan
    return sorted(candidates, key=lambda x: x[0])[-1][1]

def pick_shares(vals_usd, vals_shares):
    for vals in [vals_shares, vals_usd]:
        candidates = []
        for v in vals:
            if v.get('form') not in ('10-Q', '10-K', '10-Q/A', '10-K/A'):
                continue
            end_dt = pd.Timestamp(v['end']) if v.get('end') else None
            if end_dt is None or not (Q1_START <= end_dt <= Q1_END):
                continue
            candidates.append((end_dt, v['val']))
        if candidates:
            return sorted(candidates, key=lambda x: x[0])[-1][1]
    return np.nan

def get_first_match(us_facts, tags, mode='flow'):
    for tag in tags:
        if tag not in us_facts:
            continue
        units = us_facts[tag].get('units', {})
        vals  = units.get('USD', units.get('shares', []))
        if not vals:
            continue
        val = pick_quarterly_flow(vals) if mode == 'flow' else pick_stock_value(vals)
        if not np.isnan(val):
            return val
    return np.nan

def pull_edgar_q1_2025(ticker):
    yf_ticker = TICKER_FIX.get(ticker, ticker)
    try:
        co  = edgarlib.Company(yf_ticker)
        cik = str(co.cik).zfill(10)
    except Exception:
        return None
    try:
        url  = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json'
        resp = requests.get(url, headers=SEC_HEADERS, timeout=15)
        if resp.status_code != 200:
            return None
        data = resp.json()
    except Exception:
        return None
    us = data.get('facts', {}).get('us-gaap', {})
    if not us:
        return None
    rev  = get_first_match(us, FLOW_TAGS, 'flow')
    cogs = get_first_match(us, COGS_TAGS, 'flow')
    ni   = get_first_match(us, NI_TAGS,   'flow')
    oi   = get_first_match(us, OI_TAGS,   'flow')
    assets   = get_first_match(us, ['Assets'],              'stock')
    act      = get_first_match(us, ['AssetsCurrent'],       'stock')
    lct      = get_first_match(us, ['LiabilitiesCurrent'],  'stock')
    ceq      = get_first_match(us, ['StockholdersEquity'],  'stock')
    ltd      = get_first_match(us, ['LongTermDebtNoncurrent', 'LongTermDebt'], 'stock')
    cash     = get_first_match(us, ['CashAndCashEquivalentsAtCarryingValue'],  'stock')
    shr_tag  = 'CommonStockSharesOutstanding'
    shares   = np.nan
    if shr_tag in us:
        shr_usd    = us[shr_tag]['units'].get('USD', [])
        shr_shares = us[shr_tag]['units'].get('shares', [])
        shares = pick_shares(shr_usd, shr_shares)
    if pd.isna(rev) and pd.isna(assets):
        return None
    return {'tic': ticker, 'revtq': rev, 'cogsq': cogs, 'niq': ni,
            'oiadpq': oi, 'atq': assets, 'actq': act, 'lctq': lct,
            'ceqq': ceq, 'dlttq': ltd, 'cheq': cash, 'cshoq': shares}

rate_lock    = threading.Lock()
last_call    = [0.0]
MIN_INTERVAL = 0.12

def rate_limited_pull(tic):
    with rate_lock:
        elapsed = time.time() - last_call[0]
        if elapsed < MIN_INTERVAL:
            time.sleep(MIN_INTERVAL - elapsed)
        last_call[0] = time.time()
    return pull_edgar_q1_2025(tic)

edgar_rows = []
failed     = []
n          = len(tickers_sp500)
done       = [0]

with ThreadPoolExecutor(max_workers=6) as executor:
    futures = {executor.submit(rate_limited_pull, tic): tic for tic in tickers_sp500}
    for future in as_completed(futures):
        tic     = futures[future]
        done[0] += 1
        if done[0] % 100 == 0:
            print(f"  {done[0]}/{n} processed...")
        try:
            result = future.result()
            if result:
                edgar_rows.append(result)
            else:
                failed.append(tic)
        except Exception:
            failed.append(tic)

print(f"Retrieved: {len(edgar_rows)}/{n} ({len(edgar_rows)/n*100:.1f}%)")
print(f"Failed: {len(failed)}")

edgar_df = pd.DataFrame(edgar_rows)
edgar_df.to_csv(EDGAR_CACHE, index=False)
print(f"Saved to {EDGAR_CACHE}")

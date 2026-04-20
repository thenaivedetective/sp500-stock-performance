import os
import pandas as pd
import numpy as np
import requests
import time
import threading
import warnings
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor, as_completed
from tabulate import tabulate
from sklearn.metrics import roc_auc_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from statsmodels.discrete.discrete_model import Logit
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm
import edgar as edgarlib
warnings.filterwarnings('ignore')

edgarlib.set_identity('Lana Gidan lgidan@binghamton.edu')

SEC_HEADERS = {'User-Agent': 'Lana Gidan lgidan@binghamton.edu'}

print("=" * 70)
print("  TRUE OUT-OF-SAMPLE VALIDATION — SEC EDGAR + yFINANCE 2025")
print("  Training : Q1 2010 – Q3 2024  (WRDS Compustat + CRSP)")
print("  Features : Q1 2025 financial ratios  (SEC EDGAR 10-Q filings)")
print("  Labels   : Q2 2025 outperformance    (yFinance Apr–Jun 2025)")
print("  All model parameters fitted on training data ONLY")
print("  Reference: Ananthakumar & Sarkar (2017)")
print("=" * 70)

print("\n[1/6] Loading WRDS training data...")

comp      = pd.read_csv('wrds_compustat_quarterly.csv', low_memory=False)
crsp      = pd.read_csv('wrds_crsp_quarterly.csv',     low_memory=False)
gics      = pd.read_csv('wrds_gics_sectors.csv',       low_memory=False)
macro     = pd.read_csv('wrds_fred_macro.csv',         low_memory=False)
sp500hist = pd.read_csv('wrds_sp500_history.csv',      low_memory=False)

sp500hist['start_date'] = pd.to_datetime(sp500hist['start_date'])
sp500hist['end_date']   = pd.to_datetime(sp500hist['end_date'].fillna('2099-12-31'))
gics['gvkey']           = gics['gvkey'].astype(str)

numeric_cols = ['revtq','cogsq','xsgaq','xrdq','oibdpq','oiadpq','niq','ibq',
                'piq','atq','ceqq','teqq','dlttq','dlcq','actq','lctq',
                'cheq','dpq','txtq','prccq','cshoq','mkvaltq']
for c in numeric_cols:
    comp[c] = pd.to_numeric(comp[c], errors='coerce')

comp['datadate']    = pd.to_datetime(comp['datadate'])
comp['cal_quarter'] = comp['datadate'].dt.to_period('Q')
comp['gvkey']       = comp['gvkey'].astype(str)
crsp['quarter']     = pd.PeriodIndex(crsp['quarter_str'], freq='Q')
macro['quarter']    = pd.PeriodIndex(macro['quarter'], freq='Q')

comp = comp.sort_values(['gvkey', 'cal_quarter'])
comp['lag_revtq'] = comp.groupby('gvkey')['revtq'].shift(1)
comp['lag_niq']   = comp.groupby('gvkey')['niq'].shift(1)

comp['roa']            = comp['niq']    / comp['atq'].replace(0, np.nan)
comp['roe']            = comp['niq']    / comp['ceqq'].replace(0, np.nan)
comp['gross_margin']   = (comp['revtq'] - comp['cogsq']) / comp['revtq'].replace(0, np.nan)
comp['op_margin']      = comp['oiadpq'] / comp['revtq'].replace(0, np.nan)
comp['net_margin']     = comp['niq']    / comp['revtq'].replace(0, np.nan)
comp['asset_turnover'] = comp['revtq']  / comp['atq'].replace(0, np.nan)
comp['current_ratio']  = comp['actq']   / comp['lctq'].replace(0, np.nan)
comp['debt_to_equity'] = comp['dlttq']  / comp['ceqq'].replace(0, np.nan)
comp['rev_growth']     = (comp['revtq'] - comp['lag_revtq']) / comp['lag_revtq'].abs().replace(0, np.nan)
comp['ni_growth']      = (comp['niq']   - comp['lag_niq'])   / comp['lag_niq'].abs().replace(0, np.nan)
comp['pe_ratio']       = comp['prccq']  / (comp['ibq'] / comp['cshoq'].replace(0, np.nan)).replace(0, np.nan)
comp['book_to_market'] = comp['ceqq']   / comp['mkvaltq'].replace(0, np.nan)
comp['log_mkvalt']     = np.log(comp['mkvaltq'].clip(lower=1e-6))

comp = comp.merge(gics[['gvkey', 'gsector', 'sector_name']], on='gvkey', how='left')

ratio_cols = ['roa','roe','gross_margin','op_margin','net_margin','asset_turnover',
              'current_ratio','debt_to_equity','rev_growth','ni_growth',
              'pe_ratio','book_to_market','gdp_growth','inflation']

merged = comp.merge(
    crsp[['ticker','quarter','quarterly_return','spy_quarterly_return','outperformer_quarterly']],
    left_on=['tic','cal_quarter'], right_on=['ticker','quarter'], how='inner'
)
merged = merged.merge(macro, left_on='cal_quarter', right_on='quarter', how='left')

all_quarters = pd.period_range('2010Q1', '2024Q4', freq='Q')
constituent_rows = []
for _, row in sp500hist.iterrows():
    for q in all_quarters:
        q_start = q.start_time
        if row['start_date'] <= q_start <= row['end_date']:
            constituent_rows.append({'gvkey': str(row['gvkey']), 'cal_quarter': q})
constituent_panel = pd.DataFrame(constituent_rows)

merged['gvkey'] = merged['gvkey'].astype(str)
merged = merged.merge(constituent_panel, on=['gvkey','cal_quarter'], how='inner').reset_index(drop=True)
merged = merged.sort_values(['gvkey','cal_quarter']).reset_index(drop=True)
merged['outperformer_next'] = merged.groupby('gvkey')['outperformer_quarterly'].shift(-1)

merged_train = merged[merged['cal_quarter'] <= pd.Period('2024Q3')].copy()
merged_train = merged_train[merged_train['outperformer_next'].notna()].copy()

print(f"  Training rows: {len(merged_train):,}  (Q1 2010 – Q3 2024)")

print("\n[2/6] Pulling Q1 2025 macro data from FRED...")

def get_fred_quarterly(series, start, end):
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}&vintage_date={end}"
    try:
        df = pd.read_csv(url, parse_dates=['DATE'])
        df = df[(df['DATE'] >= start) & (df['DATE'] <= end)]
        df.columns = ['date', 'value']
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        return df.dropna()
    except Exception:
        return pd.DataFrame()

try:
    gdp_df  = get_fred_quarterly('GDPC1',   '2024-10-01', '2025-06-30')
    cpi_df  = get_fred_quarterly('CPIAUCSL','2024-10-01', '2025-06-30')

    if len(gdp_df) >= 2:
        gdp_q4_2024 = float(gdp_df.iloc[-2]['value'])
        gdp_q1_2025 = float(gdp_df.iloc[-1]['value'])
        gdp_growth_q1_2025 = (gdp_q1_2025 - gdp_q4_2024) / gdp_q4_2024
    else:
        gdp_growth_q1_2025 = -0.00075

    if len(cpi_df) >= 4:
        cpi_dec2024 = cpi_df[cpi_df['date'].dt.month == 12].iloc[-1]['value']
        cpi_mar2025 = cpi_df[cpi_df['date'].dt.month == 3].iloc[-1]['value']
        inflation_q1_2025 = (cpi_mar2025 - cpi_dec2024) / cpi_dec2024
    else:
        inflation_q1_2025 = 0.007

    print(f"  Q1 2025 GDP growth (quarterly): {gdp_growth_q1_2025*100:.4f}%")
    print(f"  Q1 2025 CPI inflation (quarterly): {inflation_q1_2025*100:.4f}%")
except Exception as e:
    print(f"  FRED pull failed ({e}), using fallback values")
    gdp_growth_q1_2025 = -0.00075
    inflation_q1_2025  =  0.007

print("\n[3/6] Pulling Q1 2025 financial ratios from SEC EDGAR...")

tickers_sp500 = merged[merged['cal_quarter'] == pd.Period('2024Q4')]['tic'].dropna().unique().tolist()

TICKER_FIX = {'BRK.B': 'BRK-B', 'BRK.A': 'BRK-A', 'BF.B': 'BF-B', 'BF.A': 'BF-A'}

FLOW_TAGS = [
    'RevenueFromContractWithCustomerExcludingAssessedTax',
    'Revenues',
    'SalesRevenueNet',
    'SalesRevenueGoodsNet',
]
COGS_TAGS = ['CostOfGoodsAndServicesSold', 'CostOfRevenue', 'CostOfGoodsSold']
NI_TAGS   = ['NetIncomeLoss', 'NetIncome']
OI_TAGS   = ['OperatingIncomeLoss', 'OperatingIncome']
STOCK_TAGS = [
    'Assets', 'AssetsCurrent', 'LiabilitiesCurrent', 'StockholdersEquity',
    'LongTermDebtNoncurrent', 'LongTermDebt',
    'CashAndCashEquivalentsAtCarryingValue',
    'CommonStockSharesOutstanding',
    'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest',
]

Q1_START = pd.Timestamp('2025-01-01')
Q1_END   = pd.Timestamp('2025-04-15')
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
        if mode == 'flow':
            val = pick_quarterly_flow(vals)
        else:
            val = pick_stock_value(vals)
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
    piq  = get_first_match(us, [
        'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest'
    ], 'flow')

    assets   = get_first_match(us, ['Assets'],              'stock')
    act      = get_first_match(us, ['AssetsCurrent'],       'stock')
    lct      = get_first_match(us, ['LiabilitiesCurrent'],  'stock')
    ceq      = get_first_match(us, ['StockholdersEquity'],  'stock')
    ltd      = get_first_match(us, ['LongTermDebtNoncurrent', 'LongTermDebt'], 'stock')
    cash     = get_first_match(us, ['CashAndCashEquivalentsAtCarryingValue'],  'stock')

    shr_tag = 'CommonStockSharesOutstanding'
    shares  = np.nan
    if shr_tag in us:
        shr_usd    = us[shr_tag]['units'].get('USD', [])
        shr_shares = us[shr_tag]['units'].get('shares', [])
        shares = pick_shares(shr_usd, shr_shares)

    if pd.isna(rev) and pd.isna(assets):
        return None

    return {
        'tic':    ticker,
        'revtq':  rev,
        'cogsq':  cogs,
        'niq':    ni,
        'oiadpq': oi,
        'piq':    piq,
        'atq':    assets,
        'actq':   act,
        'lctq':   lct,
        'ceqq':   ceq,
        'dlttq':  ltd,
        'cheq':   cash,
        'cshoq':  shares,
    }

EDGAR_CACHE = 'cache_edgar_q1_2025.csv'

if os.path.exists(EDGAR_CACHE):
    print(f"  Loading cached EDGAR data from {EDGAR_CACHE}...")
    edgar_df = pd.read_csv(EDGAR_CACHE)
    print(f"  Loaded {len(edgar_df)} rows from cache.")
else:
    rate_lock = threading.Lock()
    last_call = [0.0]
    MIN_INTERVAL = 0.15

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
            tic    = futures[future]
            done[0] += 1
            if done[0] % 50 == 0:
                print(f"  Progress: {done[0]}/{n} tickers processed...")
            try:
                result = future.result()
                if result:
                    edgar_rows.append(result)
                else:
                    failed.append(tic)
            except Exception:
                failed.append(tic)

    print(f"  EDGAR Q1 2025: retrieved {len(edgar_rows)}/{n} tickers "
          f"({len(edgar_rows)/n*100:.1f}%)")
    if failed:
        print(f"  Failed/missing: {len(failed)} tickers")

    edgar_df = pd.DataFrame(edgar_rows)
    edgar_df.to_csv(EDGAR_CACHE, index=False)
    print(f"  EDGAR data cached to {EDGAR_CACHE}")

print("\n[4/6] Pulling Q2 2025 returns from yFinance...")

yf_tickers_all = [TICKER_FIX.get(t, t) for t in edgar_df['tic'].tolist()] + ['SPY']
yf_tickers_all = list(set(yf_tickers_all))

raw = yf.download(
    yf_tickers_all,
    start='2025-03-01',
    end='2025-07-05',
    auto_adjust=True,
    progress=False,
    threads=True,
)

if isinstance(raw.columns, pd.MultiIndex):
    closes = raw['Close']
else:
    closes = raw[['Close']].copy()
    closes.columns = yf_tickers_all[:1]

closes.index = pd.to_datetime(closes.index)
closes_mar  = closes[(closes.index.month == 3) & (closes.index.year == 2025)]
closes_jun  = closes[(closes.index.month == 6) & (closes.index.year == 2025)]

if len(closes_mar) == 0 or len(closes_jun) == 0:
    print("  ERROR: Cannot retrieve Mar or Jun 2025 prices.")
    exit(1)

p_mar = closes_mar.iloc[-1]
p_jun = closes_jun.iloc[-1]

spy_q2_ret = float(p_jun['SPY'] / p_mar['SPY']) - 1
print(f"  SPY Q2 2025 return: {spy_q2_ret*100:+.2f}%")

yf_rev_map = {t: TICKER_FIX.get(t, t) for t in edgar_df['tic'].tolist()}
q2_labels  = {}
for orig_tic, yf_tic in yf_rev_map.items():
    p0 = p_mar.get(yf_tic, np.nan)
    p1 = p_jun.get(yf_tic, np.nan)
    if pd.isna(p0) or pd.isna(p1) or p0 == 0:
        continue
    ret = float(p1) / float(p0) - 1
    q2_labels[orig_tic] = {
        'yf_q2_return': ret,
        'outperformer_next': 1 if ret > spy_q2_ret else 0,
    }

q2_df = pd.DataFrame.from_dict(q2_labels, orient='index').reset_index()
q2_df.columns = ['tic', 'yf_q2_return', 'outperformer_next']

print(f"  Q2 2025 labels: {len(q2_df)} tickers")
print(f"  Q2 2025 outperformers: {q2_df['outperformer_next'].sum()} / {len(q2_df)} "
      f"({q2_df['outperformer_next'].mean()*100:.1f}%)")

print("\n[5/6] Building test set and computing EDGAR-based ratios...")

test_raw = edgar_df.merge(q2_df[['tic','outperformer_next']], on='tic', how='inner')

price_data = {}
for orig_tic in test_raw['tic'].tolist():
    yf_tic = TICKER_FIX.get(orig_tic, orig_tic)
    p = p_mar.get(yf_tic, np.nan)
    price_data[orig_tic] = float(p) if not pd.isna(p) else np.nan

test_raw['price_q1']   = test_raw['tic'].map(price_data)
test_raw['mkvaltq']    = test_raw['price_q1'] * (test_raw['cshoq'] / 1e6)
test_raw['log_mkvalt'] = np.log(test_raw['mkvaltq'].clip(lower=1e-6))

test_raw['roa']            = test_raw['niq']    / test_raw['atq'].replace(0, np.nan)
test_raw['roe']            = test_raw['niq']    / test_raw['ceqq'].replace(0, np.nan)
test_raw['gross_margin']   = (test_raw['revtq'] - test_raw['cogsq']) / test_raw['revtq'].replace(0, np.nan)
test_raw['op_margin']      = test_raw['oiadpq'] / test_raw['revtq'].replace(0, np.nan)
test_raw['net_margin']     = test_raw['niq']    / test_raw['revtq'].replace(0, np.nan)
test_raw['asset_turnover'] = test_raw['revtq']  / test_raw['atq'].replace(0, np.nan)
test_raw['current_ratio']  = test_raw['actq']   / test_raw['lctq'].replace(0, np.nan)
test_raw['debt_to_equity'] = test_raw['dlttq']  / test_raw['ceqq'].replace(0, np.nan)
test_raw['rev_growth']     = np.nan
test_raw['ni_growth']      = np.nan
test_raw['pe_ratio']       = test_raw['price_q1'] / (test_raw['niq'] / test_raw['cshoq'].replace(0, np.nan)).replace(0, np.nan)
test_raw['book_to_market'] = (test_raw['ceqq'] / 1e6) / test_raw['mkvaltq'].replace(0, np.nan)
test_raw['gdp_growth']     = gdp_growth_q1_2025
test_raw['inflation']      = inflation_q1_2025

gics_map = gics[['gvkey','sector_name']].copy()
tic_gvkey = comp[['gvkey','tic']].drop_duplicates()
tic_sector = tic_gvkey.merge(gics_map, on='gvkey', how='left')[['tic','sector_name']].drop_duplicates('tic')
test_raw = test_raw.merge(tic_sector, on='tic', how='left')

print(f"  Test set rows: {len(test_raw):,}")
print(f"  Sectors covered: {test_raw['sector_name'].nunique()}")
print(f"  Rows with sector: {test_raw['sector_name'].notna().sum()}")

print("\n[6/6] Fitting preprocessing on training data and running validations...")

winsor_bounds = {}
train_medians = {}
for col in ratio_cols:
    if col in merged_train.columns:
        lo = merged_train[col].quantile(0.01)
        hi = merged_train[col].quantile(0.99)
        winsor_bounds[col] = (lo, hi)
        merged_train[col]  = merged_train[col].clip(lo, hi)
        train_medians[col] = merged_train[col].median()

for col in ratio_cols:
    if col in test_raw.columns and col in winsor_bounds:
        lo, hi = winsor_bounds[col]
        test_raw[col] = test_raw[col].clip(lo, hi)

for col in ['rev_growth', 'ni_growth']:
    if col in test_raw.columns and col in train_medians:
        test_raw[col] = test_raw[col].fillna(train_medians[col])

mkvalt_33 = merged_train['mkvaltq'].quantile(0.33)
mkvalt_67 = merged_train['mkvaltq'].quantile(0.67)

def cap_label(v):
    if v >= mkvalt_67:   return 'Large Cap'
    elif v >= mkvalt_33: return 'Mid Cap'
    return 'Small Cap'

merged_train['cap_group'] = merged_train['mkvaltq'].apply(cap_label)
test_raw['cap_group']     = test_raw['mkvaltq'].apply(lambda v: cap_label(v) if pd.notna(v) else 'Unknown')

sectors = sorted(merged_train['sector_name'].dropna().unique())

cluster_models = {}
for s in sectors:
    idx    = merged_train['sector_name'] == s
    subset = merged_train.loc[idx, ratio_cols].fillna(train_medians)
    if len(subset) < 40:
        continue
    sc  = StandardScaler()
    km2 = KMeans(n_clusters=2, random_state=42, n_init=10)
    km2.fit(sc.fit_transform(subset))
    cluster_models[s] = (sc, km2)

merged_train['sector_cluster'] = -1
for s, (sc, km2) in cluster_models.items():
    idx    = merged_train['sector_name'] == s
    subset = merged_train.loc[idx, ratio_cols].fillna(train_medians)
    merged_train.loc[idx, 'sector_cluster'] = km2.predict(sc.transform(subset))

test_raw['sector_cluster'] = -1
for s, (sc, km2) in cluster_models.items():
    idx = test_raw['sector_name'] == s
    if idx.sum() == 0:
        continue
    subset = test_raw.loc[idx, ratio_cols].fillna(train_medians)
    test_raw.loc[idx, 'sector_cluster'] = km2.predict(sc.transform(subset))

def vif_filter(X_df, cutoff=2.5):
    remaining = list(X_df.columns)
    while True:
        vifs    = [variance_inflation_factor(X_df[remaining].values, i) for i in range(len(remaining))]
        max_vif = max(vifs)
        if max_vif <= cutoff:
            break
        remaining.remove(remaining[vifs.index(max_vif)])
    return remaining

all_results = []

def run_validation(config_name, group_name, train_df, test_df, feature_cols=None):
    if feature_cols is None:
        feature_cols = ratio_cols
    available = [c for c in feature_cols if c in train_df.columns and c in test_df.columns]

    train = train_df[available + ['outperformer_next']].dropna()
    test  = test_df[available  + ['outperformer_next']].dropna()

    if len(train) < 100 or train['outperformer_next'].nunique() < 2:
        return
    if len(test) < 5 or test['outperformer_next'].nunique() < 2:
        return

    X_train = train[available]
    y_train = train['outperformer_next']
    X_test  = test[available]
    y_test  = test['outperformer_next']

    scaler         = StandardScaler()
    X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=available)
    X_test_scaled  = pd.DataFrame(scaler.transform(X_test),      columns=available)

    kept          = vif_filter(X_train_scaled, cutoff=2.5)
    X_train_clean = X_train_scaled[kept]
    X_test_clean  = X_test_scaled[kept]

    pca_fit = PCA()
    pca_fit.fit(X_train_clean)
    exp_var = np.cumsum(pca_fit.explained_variance_ratio_)
    n_comp  = min(int(np.searchsorted(exp_var, 0.80)) + 1, len(kept))

    pca_final   = PCA(n_components=n_comp)
    X_train_pca = pca_final.fit_transform(X_train_clean)
    X_test_pca  = pca_final.transform(X_test_clean)

    X_train_const = sm.add_constant(X_train_pca)
    model = Logit(y_train.values, X_train_const).fit(maxiter=200, disp=False)

    y_train_prob = model.predict(X_train_const)
    train_auc    = roc_auc_score(y_train, y_train_prob)

    best_cut, best_acc_val = 0.5, 0
    for thresh in np.arange(0.30, 0.75, 0.05):
        preds = (y_train_prob >= thresh).astype(int)
        acc   = (preds == y_train.values).mean()
        if acc > best_acc_val:
            best_acc_val, best_cut = acc, thresh
    best_cut  = round(best_cut, 2)
    train_acc = round(best_acc_val * 100, 1)

    cm_tr = confusion_matrix(y_train.values, (y_train_prob >= best_cut).astype(int))
    if cm_tr.shape == (2, 2):
        tn, fp, fn, tp = cm_tr.ravel()
        train_sens = round(tp / (tp + fn) * 100, 1) if (tp + fn) > 0 else 0
        train_spec = round(tn / (tn + fp) * 100, 1) if (tn + fp) > 0 else 0
    else:
        train_sens = train_spec = 0

    X_test_const = sm.add_constant(X_test_pca, has_constant='add')
    y_test_prob  = model.predict(X_test_const)
    test_auc     = roc_auc_score(y_test, y_test_prob)
    test_acc     = round(((y_test_prob >= best_cut).astype(int) == y_test.values).mean() * 100, 1)

    cm_te = confusion_matrix(y_test.values, (y_test_prob >= best_cut).astype(int))
    if cm_te.shape == (2, 2):
        tn_t, fp_t, fn_t, tp_t = cm_te.ravel()
        test_sens = round(tp_t / (tp_t + fn_t) * 100, 1) if (tp_t + fn_t) > 0 else 0
        test_spec = round(tn_t / (tn_t + fp_t) * 100, 1) if (tn_t + fp_t) > 0 else 0
    else:
        test_sens = test_spec = 0

    auc_change = round(test_auc - train_auc, 4)
    acc_change = round(test_acc - train_acc, 1)

    if auc_change >= -0.02:
        verdict = "HOLDS UP"
    elif auc_change >= -0.05:
        verdict = "MODEST DEGRADATION"
    else:
        verdict = "SIGNIFICANT DEGRADATION"

    print(f"\n{'='*70}")
    print(f"  {group_name.upper()}  [{config_name}]")
    print(f"  Train N={len(train):,} (WRDS 2010-24) | Test N={len(test):,} (EDGAR Q1 2025 → Q2 2025)")
    print(f"{'='*70}")
    print(tabulate([
        ["AUC",         f"{train_auc:.4f}",   f"{test_auc:.4f}",  f"{auc_change:+.4f}"],
        ["Accuracy",    f"{train_acc:.1f}%",  f"{test_acc:.1f}%", f"{acc_change:+.1f}%"],
        ["Sensitivity", f"{train_sens:.1f}%", f"{test_sens:.1f}%","—"],
        ["Specificity", f"{train_spec:.1f}%", f"{test_spec:.1f}%","—"],
        ["N",           f"{len(train):,}",     f"{len(test):,}",   "—"],
        ["Cutoff",      f"{best_cut}",         f"{best_cut}",      "—"],
        ["PCA Comps",   f"{n_comp}",           f"{n_comp}",        "—"],
    ], headers=["Metric","Train (WRDS 2010-24)","Test (EDGAR Q1→Q2 2025)","Change"],
       tablefmt="github"))
    print(f"\n  Verdict: {verdict}")

    all_results.append({
        'Configuration': config_name,
        'Group':         group_name,
        'Train N':       len(train),
        'Test N':        len(test),
        'Train AUC':     round(train_auc, 4),
        'Test AUC':      round(test_auc,  4),
        'AUC Change':    auc_change,
        'Train Acc':     train_acc,
        'Test Acc':      test_acc,
        'Acc Change':    acc_change,
        'Verdict':       verdict,
    })


print("\n\n" + "=" * 70)
print("  CONFIGURATION 1: MARKET CAP SEGMENTATION")
print("=" * 70)
for cap in ['Large Cap', 'Mid Cap', 'Small Cap']:
    run_validation('Market Cap', cap,
                   merged_train[merged_train['cap_group'] == cap],
                   test_raw[test_raw['cap_group'] == cap])

print("\n\n" + "=" * 70)
print("  CONFIGURATION 2: SECTOR GICS")
print("=" * 70)
for s in sectors:
    run_validation('Sector GICS', s,
                   merged_train[merged_train['sector_name'] == s],
                   test_raw[test_raw['sector_name'] == s])

print("\n\n" + "=" * 70)
print("  CONFIGURATION 3: SECTOR + MARKET CAP COVARIATE")
print("=" * 70)
for s in sectors:
    run_validation('Sector + MktCap', f"{s} [+MktCap]",
                   merged_train[merged_train['sector_name'] == s],
                   test_raw[test_raw['sector_name'] == s],
                   feature_cols=ratio_cols + ['log_mkvalt'])

print("\n\n" + "=" * 70)
print("  CONFIGURATION 4: SECTOR + CLUSTERING (k=2)")
print("=" * 70)
for s in sectors:
    s_train = merged_train[(merged_train['sector_name'] == s) & (merged_train['sector_cluster'] >= 0)]
    s_test  = test_raw[(test_raw['sector_name'] == s) & (test_raw['sector_cluster'] >= 0)]
    for c in [0, 1]:
        run_validation('Sector + Clustering (k=2)', f"{s} — Cluster {c}",
                       s_train[s_train['sector_cluster'] == c],
                       s_test[s_test['sector_cluster'] == c])


print("\n\n" + "=" * 70)
print("  GRAND SUMMARY — TRUE OUT-OF-SAMPLE (EDGAR Q1 2025 → Q2 2025)")
print("  Q1 2025 financial ratios (10-Q filings) → Q2 2025 outperformance")
print("  All 4 configurations | All segments | Sorted by out-of-sample AUC")
print("=" * 70)

df_val = pd.DataFrame(all_results)

if len(df_val) > 0:
    df_sorted = df_val.sort_values('Test AUC', ascending=False).reset_index(drop=True)
    df_sorted.insert(0, 'Rank', range(1, len(df_sorted) + 1))
    print(tabulate(
        df_sorted[['Rank','Configuration','Group','Train N','Test N',
                   'Train AUC','Test AUC','AUC Change','Train Acc','Test Acc','Verdict']].values.tolist(),
        headers=['Rank','Config','Group','Train N','Test N',
                 'Train AUC','Test AUC','ΔAUC','Train Acc%','Test Acc%','Verdict'],
        tablefmt='github'
    ))

    print("\n── CONFIGURATION-LEVEL SUMMARY ──────────────────────────────────────")
    cfg_summary = []
    for cfg in ['Market Cap', 'Sector GICS', 'Sector + MktCap', 'Sector + Clustering (k=2)']:
        sub = df_val[df_val['Configuration'] == cfg]
        if len(sub) == 0:
            continue
        w_train = (sub['Train AUC'] * sub['Train N']).sum() / sub['Train N'].sum()
        w_test  = (sub['Test AUC']  * sub['Test N']).sum()  / sub['Test N'].sum()
        n_holds = (sub['Verdict'] == 'HOLDS UP').sum()
        cfg_summary.append([
            cfg, len(sub),
            round(w_train, 4), round(w_test, 4),
            f"{round(w_test - w_train, 4):+.4f}",
            f"{n_holds}/{len(sub)}",
            round(sub['Train Acc'].mean(), 1),
            round(sub['Test Acc'].mean(),  1),
        ])
    cfg_summary.sort(key=lambda x: x[3], reverse=True)
    for i, row in enumerate(cfg_summary):
        row.insert(0, i + 1)
    print(tabulate(cfg_summary,
        headers=['Rank','Configuration','Groups','W.Train AUC','W.Test AUC','ΔAUC',
                 'Holds Up','Avg Train Acc%','Avg Test Acc%'],
        tablefmt='github'))

    if len(df_sorted) > 0:
        best_group = df_sorted.iloc[0]
        best_acc_group = df_sorted.sort_values('Test Acc', ascending=False).iloc[0]
    overall_avg_train = df_val['Train AUC'].mean()
    overall_avg_test  = df_val['Test AUC'].mean()
    n_holds_all = (df_val['Verdict'] == 'HOLDS UP').sum()
    n_modest    = (df_val['Verdict'] == 'MODEST DEGRADATION').sum()
    n_sig_deg   = (df_val['Verdict'] == 'SIGNIFICANT DEGRADATION').sum()

    print(f"\n── OVERALL RESULTS ──────────────────────────────────────────────────")
    print(tabulate([
        ["Total groups validated",                         len(df_val)],
        ["Feature quarter",                                "Q1 2025 (Jan–Mar 2025, SEC EDGAR 10-Q)"],
        ["Label quarter",                                  "Q2 2025 (Apr–Jun 2025, yFinance)"],
        ["SPY Q2 2025 return",                             f"{spy_q2_ret*100:+.2f}%"],
        ["Q1 2025 GDP growth (quarterly)",                 f"{gdp_growth_q1_2025*100:.4f}%"],
        ["Q1 2025 CPI inflation (quarterly)",              f"{inflation_q1_2025*100:.4f}%"],
        ["Test set size",                                  f"{len(test_raw):,} stocks"],
        ["Avg in-sample AUC (2010-24)",                    f"{overall_avg_train:.4f}"],
        ["Avg out-of-sample AUC (Q2 2025)",                f"{overall_avg_test:.4f}"],
        ["Avg AUC change",                                 f"{overall_avg_test - overall_avg_train:+.4f}"],
        ["Holds Up  (ΔAUC ≥ -0.02)",                       f"{n_holds_all}/{len(df_val)}"],
        ["Modest Degradation   (ΔAUC -0.02 to -0.05)",    f"{n_modest}/{len(df_val)}"],
        ["Significant Degradation (ΔAUC < -0.05)",         f"{n_sig_deg}/{len(df_val)}"],
        ["Best out-of-sample group",                       f"{best_group['Group']}"],
        ["Best out-of-sample AUC",                         f"{best_group['Test AUC']:.4f}"],
        ["Best out-of-sample accuracy",                    f"{best_acc_group['Test Acc']:.1f}%"],
        ["Paper benchmark accuracy",                       "71.2%"],
    ], tablefmt="github"))

    if overall_avg_test >= overall_avg_train - 0.02:
        gen_verdict = "GENERALIZES WELL"
    elif overall_avg_test >= overall_avg_train - 0.05:
        gen_verdict = "MODEST OVERFITTING"
    else:
        gen_verdict = "OVERFITTING DETECTED"

    print(f"\n── METHODOLOGY NOTES ──────────────────────────────────────────────────")
    print(f"  Overall generalization : {gen_verdict}")
    print(f"  Training horizon       : Q1 2010 – Q3 2024 (WRDS Compustat + CRSP)")
    print(f"  Feature source         : SEC EDGAR XBRL (data.sec.gov/api/xbrl/companyfacts)")
    print(f"  Label source           : yFinance adjusted closing prices")
    print(f"  Method                 : VIF≤2.5 → PCA≥80% → Logistic Regression")
    print(f"  Winsorization          : 1st-99th percentile from training only")
    print(f"  Cluster assignment     : KMeans fitted on 2010-24, applied to Q1 2025")
    print(f"  Market cap thresholds  : Computed from training data only")
    print(f"  Forward-looking        : Q[t] ratios → Q[t+1] outperformance")
    print(f"  Note: rev_growth/ni_growth set to NaN (no Q4 2024 EDGAR baseline)")
    print("=" * 70 + "\n")

    df_val.to_csv('results_edgar.txt', index=False, sep='\t')
    print("  Results saved to: results_edgar.txt")
else:
    print("  No groups had sufficient data for validation.")

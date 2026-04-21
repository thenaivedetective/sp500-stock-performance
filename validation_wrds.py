import pandas as pd
import numpy as np
import warnings
import yfinance as yf
from tabulate import tabulate
from sklearn.metrics import roc_auc_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from statsmodels.discrete.discrete_model import Logit
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm
warnings.filterwarnings('ignore')

print("=" * 70)
print("  TRUE OUT-OF-SAMPLE VALIDATION — PURE WRDS (NO EDGAR)")
print("  Training : Q1 2010 – Q3 2024  (WRDS Compustat + CRSP)")
print("  Features : Q4 2024 financial ratios  (WRDS Compustat)")
print("  Labels   : Q1 2025 outperformance    (yFinance Jan–Mar 2025)")
print("  All model parameters fitted on training data ONLY")
print("  Reference: Ananthakumar & Sarkar (2017)")
print("=" * 70)

print("\n[1/5] Loading WRDS data...")
comp      = pd.read_csv('wrds_compustat_quarterly.csv', low_memory=False)
crsp      = pd.read_csv('wrds_crsp_quarterly.csv', low_memory=False)
gics      = pd.read_csv('wrds_gics_sectors.csv', low_memory=False)
macro     = pd.read_csv('wrds_fred_macro.csv', low_memory=False)
sp500hist = pd.read_csv('wrds_sp500_history.csv', low_memory=False)

sp500hist['start_date'] = pd.to_datetime(sp500hist['start_date'])
sp500hist['end_date']   = pd.to_datetime(sp500hist['end_date'])

comp['datadate']    = pd.to_datetime(comp['datadate'])
comp['cal_quarter'] = comp['datadate'].dt.to_period('Q')
crsp['quarter']     = pd.PeriodIndex(crsp['quarter_str'], freq='Q')
macro['quarter']    = pd.PeriodIndex(macro['quarter'], freq='Q')

numeric_cols = ['revtq','cogsq','xsgaq','xrdq','oibdpq','oiadpq','niq','ibq',
                'piq','atq','ceqq','teqq','dlttq','dlcq','actq','lctq',
                'cheq','dpq','txtq','prccq','cshoq','mkvaltq']
for c in numeric_cols:
    comp[c] = pd.to_numeric(comp[c], errors='coerce')

comp = comp.sort_values(['gvkey','cal_quarter'])
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

gics['gvkey'] = gics['gvkey'].astype(str)
comp['gvkey']  = comp['gvkey'].astype(str)
comp = comp.merge(gics[['gvkey','sector_name']], on='gvkey', how='left')

ratio_cols = ['roa','roe','gross_margin','op_margin','net_margin','asset_turnover',
              'current_ratio','debt_to_equity','rev_growth','ni_growth',
              'pe_ratio','book_to_market','gdp_growth','inflation']

ratio_labels = {
    'roa':'ROA', 'roe':'ROE', 'gross_margin':'Gross Margin',
    'op_margin':'Op Margin', 'net_margin':'Net Margin',
    'asset_turnover':'Asset Turnover', 'current_ratio':'Current Ratio',
    'debt_to_equity':'Debt/Equity', 'rev_growth':'Rev Growth',
    'ni_growth':'NI Growth', 'pe_ratio':'P/E Ratio',
    'book_to_market':'Book/Market', 'gdp_growth':'GDP Growth',
    'inflation':'Inflation', 'log_mkvalt':'Log MktCap',
}

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

train_df = merged[merged['cal_quarter'] <= pd.Period('2024Q3', 'Q')].copy()
print(f"  Training rows : {len(train_df):,}  (Q1 2010 – Q3 2024)")

print("\n[2/5] Pulling Q1 2025 macro data from FRED...")
try:
    import pandas_datareader.data as web
    from datetime import datetime
    gdp_raw = web.DataReader('GDP', 'fred', datetime(2024, 9, 1), datetime(2025, 6, 30))
    gdp_q4_2024 = float(gdp_raw.loc['2024-10-01':'2024-12-31'].iloc[-1])
    gdp_q3_2024 = float(gdp_raw.loc['2024-07-01':'2024-09-30'].iloc[-1])
    gdp_growth_q4 = (gdp_q4_2024 - gdp_q3_2024) / gdp_q3_2024 * 100
    cpi_raw = web.DataReader('CPIAUCSL', 'fred', datetime(2024, 9, 1), datetime(2025, 6, 30))
    cpi_dec = float(cpi_raw.loc['2024-12-01':'2024-12-31'].iloc[-1])
    cpi_sep = float(cpi_raw.loc['2024-09-01':'2024-09-30'].iloc[-1])
    inflation_q4 = (cpi_dec - cpi_sep) / cpi_sep * 100
except Exception:
    gdp_growth_q4 = 0.7
    inflation_q4  = 0.6
print(f"  Q4 2024 GDP growth    : {gdp_growth_q4:.4f}%")
print(f"  Q4 2024 CPI inflation : {inflation_q4:.4f}%")

print("\n[3/5] Building Q4 2024 test set from WRDS Compustat...")
test_q = pd.Period('2024Q4', 'Q')
comp_q4 = comp[comp['cal_quarter'] == test_q].copy()
comp_q4['gdp_growth'] = gdp_growth_q4
comp_q4['inflation']  = inflation_q4

tickers_q4 = comp_q4['tic'].dropna().unique().tolist()
print(f"  Tickers with Q4 2024 Compustat data: {len(tickers_q4)}")

print("\n[4/5] Pulling Q1 2025 returns from yFinance (Jan–Mar 2025)...")
TICKER_FIX = {
    'BRK.B':'BRK-B','BF.B':'BF-B','GEV':'GEV',
    'GEHC':'GEHC','CEG':'CEG','SOLV':'SOLV',
}

yf_tickers = [TICKER_FIX.get(t, t) for t in tickers_q4] + ['SPY']
raw = yf.download(yf_tickers, start='2024-12-01', end='2025-04-01',
                  auto_adjust=True, progress=False)

if isinstance(raw.columns, pd.MultiIndex):
    closes = raw['Close']
else:
    closes = raw[['Close']].copy()
    closes.columns = yf_tickers[:1]

closes.index = pd.to_datetime(closes.index)
closes_dec = closes[(closes.index.month == 12) & (closes.index.year == 2024)]
closes_mar = closes[(closes.index.month == 3)  & (closes.index.year == 2025)]

if len(closes_dec) == 0 or len(closes_mar) == 0:
    print("  ERROR: Cannot retrieve Dec 2024 or Mar 2025 prices.")
    exit(1)

p_dec = closes_dec.iloc[-1]
p_mar = closes_mar.iloc[-1]

spy_q1_ret = float(p_mar['SPY'] / p_dec['SPY']) - 1
print(f"  SPY Q1 2025 return: {spy_q1_ret*100:+.2f}%")

yf_rev_map = {t: TICKER_FIX.get(t, t) for t in tickers_q4}
q1_labels  = {}
for orig_tic, yf_tic in yf_rev_map.items():
    p0 = p_dec.get(yf_tic, np.nan)
    p1 = p_mar.get(yf_tic, np.nan)
    if pd.isna(p0) or pd.isna(p1) or p0 == 0:
        continue
    ret = float(p1) / float(p0) - 1
    q1_labels[orig_tic] = {
        'yf_q1_return':     ret,
        'outperformer_next': 1 if ret > spy_q1_ret else 0,
    }

q1_df = pd.DataFrame.from_dict(q1_labels, orient='index').reset_index()
q1_df.columns = ['tic', 'yf_q1_return', 'outperformer_next']
print(f"  Q1 2025 labels      : {len(q1_df)} tickers")
print(f"  Q1 2025 outperformers: {q1_df['outperformer_next'].sum()} / {len(q1_df)} "
      f"({q1_df['outperformer_next'].mean()*100:.1f}%)")

print("\n[5/5] Fitting preprocessing on training data and running validations...")
test_raw = comp_q4.merge(q1_df[['tic','outperformer_next']], on='tic', how='inner')
test_raw = test_raw.merge(gics[['gvkey','sector_name']].rename(
    columns={'sector_name':'sector_name_gics'}), on='gvkey', how='left')
if 'sector_name' not in test_raw.columns:
    test_raw['sector_name'] = test_raw['sector_name_gics']
elif 'sector_name_gics' in test_raw.columns:
    test_raw['sector_name'] = test_raw['sector_name'].fillna(test_raw['sector_name_gics'])

print(f"  Test set rows     : {len(test_raw):,}")
print(f"  Sectors covered   : {test_raw['sector_name'].nunique()}")

merged_train = train_df.copy()

winsor_bounds = {}
train_medians = {}
for col in ratio_cols:
    if col not in merged_train.columns:
        continue
    lo = merged_train[col].quantile(0.01)
    hi = merged_train[col].quantile(0.99)
    winsor_bounds[col] = (lo, hi)
    merged_train[col]  = merged_train[col].clip(lo, hi)
    train_medians[col] = merged_train[col].median()

for col in ratio_cols:
    if col in test_raw.columns and col in winsor_bounds:
        lo, hi = winsor_bounds[col]
        test_raw[col] = test_raw[col].clip(lo, hi)

mkvalt_33 = merged_train['mkvaltq'].quantile(0.33)
mkvalt_67 = merged_train['mkvaltq'].quantile(0.67)

def cap_label(v):
    if v >= mkvalt_67:   return 'Large Cap'
    elif v >= mkvalt_33: return 'Mid Cap'
    return 'Small Cap'

merged_train['cap_group'] = merged_train['mkvaltq'].apply(cap_label)
test_raw['cap_group']     = test_raw['mkvaltq'].apply(
    lambda v: cap_label(v) if pd.notna(v) else 'Unknown')

merged_train['log_mkvalt'] = np.log(merged_train['mkvaltq'].clip(lower=1e-6))
test_raw['log_mkvalt']     = np.log(test_raw['mkvaltq'].clip(lower=1e-6))

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
    removed   = []
    while True:
        vifs    = [variance_inflation_factor(X_df[remaining].values, i)
                   for i in range(len(remaining))]
        max_vif = max(vifs)
        if max_vif <= cutoff:
            break
        worst = remaining[vifs.index(max_vif)]
        removed.append(worst)
        remaining.remove(worst)
    return remaining

all_results = []

def run_validation(config_name, group_name, train, test, feature_cols=None):
    if feature_cols is None:
        feature_cols = ratio_cols
    available = [c for c in feature_cols if c in train.columns and c in test.columns]
    train_df2 = train[available + ['outperformer_next']].dropna()
    test_df2  = test[available + ['outperformer_next']].dropna()
    if len(train_df2) < 100 or len(test_df2) < 5:
        return
    if train_df2['outperformer_next'].nunique() < 2 or test_df2['outperformer_next'].nunique() < 2:
        return

    X_tr = train_df2[available]
    y_tr = train_df2['outperformer_next']
    X_te = test_df2[available]
    y_te = test_df2['outperformer_next']

    scaler   = StandardScaler().fit(X_tr)
    X_tr_sc  = pd.DataFrame(scaler.transform(X_tr), columns=available)
    X_te_sc  = pd.DataFrame(scaler.transform(X_te), columns=available)

    kept    = vif_filter(X_tr_sc, cutoff=2.5)
    X_tr_vif = X_tr_sc[kept]
    X_te_vif = X_te_sc[kept]

    pca     = PCA()
    pca.fit(X_tr_vif)
    exp_var = np.cumsum(pca.explained_variance_ratio_)
    n_comp  = min(int(np.searchsorted(exp_var, 0.80)) + 1, len(kept))

    pca_final = PCA(n_components=n_comp).fit(X_tr_vif)
    X_tr_pca  = pca_final.transform(X_tr_vif)
    X_te_pca  = pca_final.transform(X_te_vif)

    model = Logit(y_tr.values, sm.add_constant(X_tr_pca)).fit(maxiter=200, disp=False)

    best_cut, best_acc = 0.5, 0
    for thresh in np.arange(0.30, 0.75, 0.05):
        preds = (model.predict(sm.add_constant(X_tr_pca)) >= thresh).astype(int)
        acc   = (preds == y_tr.values).mean()
        if acc > best_acc:
            best_acc, best_cut = acc, thresh

    train_auc  = roc_auc_score(y_tr, model.predict(sm.add_constant(X_tr_pca)))

    y_te_prob  = model.predict(sm.add_constant(X_te_pca))
    test_auc   = roc_auc_score(y_te, y_te_prob)

    preds_te   = (y_te_prob >= best_cut).astype(int)
    test_acc   = round((preds_te == y_te.values).mean() * 100, 1)
    auc_change = round(test_auc - train_auc, 4)
    verdict    = ("HOLDS UP" if auc_change >= -0.02
                  else ("MODEST DEGRADATION" if auc_change >= -0.05
                  else "SIGNIFICANT DEGRADATION"))

    cm = confusion_matrix(y_te.values, preds_te)
    tn, fp, fn, tp = cm.ravel() if cm.shape == (2,2) else (0,0,0,len(y_te))
    sensitivity = round(tp / (tp + fn) * 100, 1) if (tp + fn) > 0 else 0
    specificity = round(tn / (tn + fp) * 100, 1) if (tn + fp) > 0 else 0

    print(f"\n{'='*70}")
    print(f"  {group_name.upper()}  [{config_name}]")
    print(f"  Train N={len(train_df2):,} | Test N={len(test_df2)} | "
          f"Test Outperformers={y_te.mean()*100:.1f}%")
    print(f"{'='*70}")
    rows = [
        ["Train AUC",    f"{train_auc:.4f}", "In-sample",    "—"],
        ["Test AUC",     f"{test_auc:.4f}",  "Out-of-sample",
         "Strong" if test_auc >= 0.70 else ("Moderate" if test_auc >= 0.60 else "Weak")],
        ["AUC Change",   f"{auc_change:+.4f}", "≥ -0.02 = holds up", verdict],
        ["Test Accuracy",f"{test_acc}%",     "≥ 71.2% paper",
         "✓ Beats Paper" if test_acc >= 71.2 else "✗ Below Paper"],
        ["Sensitivity",  f"{sensitivity}%",  "Higher better", "—"],
        ["Specificity",  f"{specificity}%",  "Higher better", "—"],
        ["PCA Comps",    f"{n_comp}",         "≥80% variance", "—"],
        ["Cutoff",       f"{best_cut}",       "Optimised on train", "—"],
    ]
    print(tabulate(rows, headers=["Metric","Value","Threshold","Verdict"], tablefmt="github"))

    all_results.append({
        'Configuration': config_name,
        'Group': group_name,
        'Train N': len(train_df2),
        'Test N': len(test_df2),
        'Train AUC': round(train_auc, 4),
        'Test AUC': round(test_auc, 4),
        'AUC Change': auc_change,
        'Test Acc': test_acc,
        'Sensitivity': sensitivity,
        'Specificity': specificity,
        'Cutoff': best_cut,
        'PCA Comps': n_comp,
        'Verdict': verdict,
    })


print("\n" + "="*70)
print("  CONFIGURATION 1: MARKET CAP SEGMENTATION")
print("="*70)
for cap in ['Large Cap', 'Mid Cap', 'Small Cap']:
    run_validation('Market Cap', cap,
                   merged_train[merged_train['cap_group'] == cap],
                   test_raw[test_raw['cap_group'] == cap])

print("\n" + "="*70)
print("  CONFIGURATION 2: SECTOR GICS")
print("="*70)
for s in sectors:
    run_validation('Sector GICS', s,
                   merged_train[merged_train['sector_name'] == s],
                   test_raw[test_raw['sector_name'] == s])

print("\n" + "="*70)
print("  CONFIGURATION 3: SECTOR + MARKET CAP COVARIATE")
print("="*70)
for s in sectors:
    run_validation('Sector + MktCap', f"{s} [+MktCap]",
                   merged_train[merged_train['sector_name'] == s],
                   test_raw[test_raw['sector_name'] == s],
                   feature_cols=ratio_cols + ['log_mkvalt'])

print("\n" + "="*70)
print("  CONFIGURATION 4: SECTOR + CLUSTERING (k=2)")
print("="*70)
for s in sectors:
    for c in [0, 1]:
        run_validation('Sector + Clustering (k=2)', f"{s} — Cluster {c}",
                       merged_train[(merged_train['sector_name'] == s) &
                                    (merged_train['sector_cluster'] == c)],
                       test_raw[(test_raw['sector_name'] == s) &
                                (test_raw['sector_cluster'] == c)])

print("\n\n" + "="*70)
print("  GRAND SUMMARY — PURE WRDS OUT-OF-SAMPLE VALIDATION")
print("  Training: Q1 2010–Q3 2024 | Features: Q4 2024 | Labels: Q1 2025")
print("  All groups | Sorted by out-of-sample AUC")
print("="*70)

if not all_results:
    print("  No groups had sufficient data.")
else:
    df_all = pd.DataFrame(all_results).sort_values('Test AUC', ascending=False).reset_index(drop=True)
    df_all.insert(0, 'Rank', range(1, len(df_all)+1))

    print(tabulate(
        df_all[['Rank','Configuration','Group','Train N','Test N',
                'Train AUC','Test AUC','AUC Change','Test Acc','Verdict']].values.tolist(),
        headers=['Rank','Config','Group','Train N','Test N',
                 'Train AUC','Test AUC','ΔAUC','Acc%','Verdict'],
        tablefmt='github'
    ))

    holds_up   = (df_all['AUC Change'] >= -0.02).sum()
    modest     = ((df_all['AUC Change'] >= -0.05) & (df_all['AUC Change'] < -0.02)).sum()
    sig_deg    = (df_all['AUC Change'] < -0.05).sum()
    best_row   = df_all.iloc[0]

    config_summary = []
    for cfg in df_all['Configuration'].unique():
        sub   = df_all[df_all['Configuration'] == cfg]
        w_tr  = (sub['Train AUC'] * sub['Train N']).sum() / sub['Train N'].sum()
        w_te  = (sub['Test AUC']  * sub['Train N']).sum() / sub['Train N'].sum()
        n_hu  = (sub['AUC Change'] >= -0.02).sum()
        config_summary.append([cfg, len(sub), round(w_tr,4), round(w_te,4),
                               round(w_te-w_tr,4), f"{n_hu}/{len(sub)}"])
    config_summary.sort(key=lambda x: x[3], reverse=True)
    for i, row in enumerate(config_summary):
        row.insert(0, i+1)

    print(f"\n── CONFIGURATION-LEVEL SUMMARY ──────────────────────────────────")
    print(tabulate(config_summary,
        headers=['Rank','Configuration','Groups','W.Train AUC','W.Test AUC','ΔAUC','Holds Up'],
        tablefmt='github'))

    print(f"\n── OVERALL RESULTS ───────────────────────────────────────────────")
    summary_rows = [
        ["Total groups validated",              len(df_all)],
        ["Feature quarter",                     "Q4 2024 (WRDS Compustat)"],
        ["Label quarter",                       "Q1 2025 (Jan–Mar 2025, yFinance)"],
        ["SPY Q1 2025 return",                  f"{spy_q1_ret*100:+.2f}%"],
        ["Q4 2024 GDP growth",                  f"{gdp_growth_q4:.4f}%"],
        ["Q4 2024 CPI inflation",               f"{inflation_q4:.4f}%"],
        ["Test set size",                       f"{len(test_raw)} stocks"],
        ["Avg train AUC",                       f"{df_all['Train AUC'].mean():.4f}"],
        ["Avg test AUC",                        f"{df_all['Test AUC'].mean():.4f}"],
        ["Avg AUC change",                      f"{df_all['AUC Change'].mean():+.4f}"],
        ["Holds Up  (ΔAUC ≥ -0.02)",           f"{holds_up}/{len(df_all)}"],
        ["Modest Degradation (ΔAUC -0.02–-0.05)", f"{modest}/{len(df_all)}"],
        ["Significant Degradation (ΔAUC < -0.05)", f"{sig_deg}/{len(df_all)}"],
        ["Best out-of-sample group",            best_row['Group']],
        ["Best out-of-sample AUC",              f"{best_row['Test AUC']:.4f}"],
        ["Best out-of-sample accuracy",         f"{best_row['Test Acc']}%"],
        ["Paper benchmark accuracy",            "71.2%"],
    ]
    print(tabulate(summary_rows, tablefmt='github'))

    print(f"\n── METHODOLOGY NOTES ─────────────────────────────────────────────")
    print(f"  Data source      : 100% WRDS (Compustat + CRSP) — no EDGAR")
    print(f"  Feature source   : WRDS Compustat Q4 2024 (clean quarterly ratios)")
    print(f"  Label source     : yFinance adjusted closing prices Jan–Mar 2025")
    print(f"  Method           : VIF≤2.5 → PCA≥80% → Logistic Regression")
    print(f"  Winsorization    : 1st–99th percentile from training only")
    print(f"  Market cap ths.  : Computed from training data only")
    print(f"  Cluster assign.  : KMeans fitted on 2010–Q3 2024, applied to Q4 2024")
    print(f"  Forward-looking  : Q[t] ratios → Q[t+1] outperformance (shift=-1)")
    print(f"  Rev/NI growth    : Properly computed Q3→Q4 2024 from Compustat")
    print("="*70)

    df_all.to_csv('results_wrds.txt', sep='\t', index=False)
    print(f"\n  Results saved to: results_wrds.txt")

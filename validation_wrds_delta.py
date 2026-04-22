import pandas as pd
import numpy as np
import warnings
import sys
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

class Tee:
    def __init__(self, filepath):
        self.terminal = sys.stdout
        self.log = open(filepath, 'w', encoding='utf-8')
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
    def flush(self):
        self.terminal.flush()
        self.log.flush()

sys.stdout = Tee('results_validation_delta.txt')

print("=" * 70)
print("  TRUE OUT-OF-SAMPLE VALIDATION — WRDS + DELTA FEATURES")
print("  Training  : Q1 2010 – Q3 2024  (WRDS Compustat + CRSP)")
print("  Features  : Q1 2025 financial ratios + QoQ deltas  (WRDS Compustat)")
print("  Labels    : Q2 2025 outperformance  (yFinance Apr–Jun 2025)")
print("  All model parameters fitted on training data ONLY")
print("  Forward-looking: Q[t] ratios → Q[t+1] outperformance (shift=-1)")
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

delta_base = ['roa','roe','gross_margin','op_margin','net_margin',
              'asset_turnover','current_ratio','debt_to_equity','pe_ratio','book_to_market']
for col in delta_base:
    comp[f'delta_{col}'] = comp.groupby('gvkey')[col].diff()
delta_cols = [f'delta_{c}' for c in delta_base]

gics['gvkey'] = gics['gvkey'].astype(str)
comp['gvkey']  = comp['gvkey'].astype(str)
comp = comp.merge(gics[['gvkey','sector_name']], on='gvkey', how='left')

base_ratio_cols = ['roa','roe','gross_margin','op_margin','net_margin','asset_turnover',
                   'current_ratio','debt_to_equity','rev_growth','ni_growth',
                   'pe_ratio','book_to_market','gdp_growth','inflation']
ratio_cols = base_ratio_cols + delta_cols

ratio_labels = {
    'roa':'ROA', 'roe':'ROE',
    'gross_margin':'Gross Margin', 'op_margin':'Op Margin',
    'net_margin':'Net Margin', 'asset_turnover':'Asset Turnover',
    'current_ratio':'Current Ratio', 'debt_to_equity':'Debt/Equity',
    'rev_growth':'Rev Growth', 'ni_growth':'NI Growth',
    'pe_ratio':'P/E Ratio', 'book_to_market':'Book/Market',
    'gdp_growth':'GDP Growth', 'inflation':'Inflation',
    'log_mkvalt':'Log MktCap',
    'delta_roa':'ΔROA', 'delta_roe':'ΔROE',
    'delta_gross_margin':'ΔGross Margin', 'delta_op_margin':'ΔOp Margin',
    'delta_net_margin':'ΔNet Margin', 'delta_asset_turnover':'ΔAsset Turnover',
    'delta_current_ratio':'ΔCurrent Ratio', 'delta_debt_to_equity':'ΔDebt/Equity',
    'delta_pe_ratio':'ΔP/E Ratio', 'delta_book_to_market':'ΔBook/Market',
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
print(f"  Training rows : {len(train_df):,}  (Q1 2010 – Q3 2024, predicting Q2 2010 – Q4 2024)")

print("\n[2/5] Pulling Q2 2025 macro data (used as Q1 2025 context)...")
try:
    import pandas_datareader.data as web
    from datetime import datetime
    gdp_raw = web.DataReader('GDP', 'fred', datetime(2024, 9, 1), datetime(2025, 6, 30))
    gdp_q1  = float(gdp_raw.iloc[-1])
    gdp_q4  = float(gdp_raw.iloc[-2]) if len(gdp_raw) >= 2 else gdp_q1
    gdp_growth_q1 = (gdp_q1 - gdp_q4) / gdp_q4 * 100 if gdp_q4 != 0 else 0.8
    cpi_raw = web.DataReader('CPIAUCSL', 'fred', datetime(2024, 12, 1), datetime(2025, 6, 30))
    cpi_mar = float(cpi_raw.loc['2025-03-01':'2025-03-31'].iloc[-1])
    cpi_dec = float(cpi_raw.loc['2024-12-01':'2024-12-31'].iloc[-1])
    inflation_q1 = (cpi_mar - cpi_dec) / cpi_dec * 100 if cpi_dec != 0 else 0.7
except Exception:
    gdp_growth_q1 = 0.8
    inflation_q1  = 0.7
print(f"  Q1 2025 GDP growth    : {gdp_growth_q1:.4f}%")
print(f"  Q1 2025 CPI inflation : {inflation_q1:.4f}%")

print("\n[3/5] Building Q1 2025 test set from WRDS Compustat...")
test_q = pd.Period('2025Q1', 'Q')
comp_q1_2025 = comp[comp['cal_quarter'] == test_q].copy()
comp_q1_2025['gdp_growth'] = gdp_growth_q1
comp_q1_2025['inflation']  = inflation_q1

tickers_q1_2025 = comp_q1_2025['tic'].dropna().unique().tolist()
print(f"  Tickers with Q1 2025 Compustat data: {len(tickers_q1_2025)}")

print("\n[4/5] Pulling Q2 2025 returns from yFinance (Apr–Jun 2025)...")
TICKER_FIX = {
    'BRK.B':'BRK-B','BF.B':'BF-B','GEV':'GEV',
    'GEHC':'GEHC','CEG':'CEG','SOLV':'SOLV',
}

yf_tickers = [TICKER_FIX.get(t, t) for t in tickers_q1_2025] + ['SPY']
raw = yf.download(yf_tickers, start='2025-03-01', end='2025-07-01',
                  auto_adjust=True, progress=False)

if isinstance(raw.columns, pd.MultiIndex):
    closes = raw['Close']
else:
    closes = raw[['Close']].copy()
    closes.columns = yf_tickers[:1]

closes.index = pd.to_datetime(closes.index)
closes_mar = closes[(closes.index.month == 3) & (closes.index.year == 2025)]
closes_jun = closes[(closes.index.month == 6) & (closes.index.year == 2025)]

if len(closes_mar) == 0 or len(closes_jun) == 0:
    print("  ERROR: Cannot retrieve Mar 2025 or Jun 2025 prices.")
    exit(1)

p_mar = closes_mar.iloc[-1]
p_jun = closes_jun.iloc[-1]

spy_q2_ret = float(p_jun['SPY'] / p_mar['SPY']) - 1
print(f"  SPY Q2 2025 return (Apr–Jun 2025): {spy_q2_ret*100:+.2f}%")

yf_rev_map = {t: TICKER_FIX.get(t, t) for t in tickers_q1_2025}
q2_labels  = {}
for orig_tic, yf_tic in yf_rev_map.items():
    p0 = p_mar.get(yf_tic, np.nan)
    p1 = p_jun.get(yf_tic, np.nan)
    if pd.isna(p0) or pd.isna(p1) or p0 == 0:
        continue
    ret = float(p1) / float(p0) - 1
    q2_labels[orig_tic] = {
        'yf_q2_return':      ret,
        'outperformer_next': 1 if ret > spy_q2_ret else 0,
    }

q2_df = pd.DataFrame.from_dict(q2_labels, orient='index').reset_index()
q2_df.columns = ['tic', 'yf_q2_return', 'outperformer_next']
print(f"  Q2 2025 labels       : {len(q2_df)} tickers")
print(f"  Q2 2025 outperformers: {q2_df['outperformer_next'].sum()} / {len(q2_df)} "
      f"({q2_df['outperformer_next'].mean()*100:.1f}%)")

print("\n[5/5] Fitting all preprocessing on training data only and running validations...")
test_raw = comp_q1_2025.merge(q2_df[['tic','outperformer_next']], on='tic', how='inner')
if 'sector_name' not in test_raw.columns:
    test_raw = test_raw.merge(gics[['gvkey','sector_name']], on='gvkey', how='left')

print(f"  Test set rows     : {len(test_raw):,}")
print(f"  Sectors covered   : {test_raw['sector_name'].nunique()}")

winsor_bounds = {}
train_medians = {}
for col in ratio_cols:
    if col not in train_df.columns:
        continue
    lo = train_df[col].quantile(0.01)
    hi = train_df[col].quantile(0.99)
    winsor_bounds[col] = (lo, hi)
    train_df[col]      = train_df[col].clip(lo, hi)
    train_medians[col] = train_df[col].median()

for col in ratio_cols:
    if col in test_raw.columns and col in winsor_bounds:
        lo, hi = winsor_bounds[col]
        test_raw[col] = test_raw[col].clip(lo, hi)

mkvalt_33 = train_df['mkvaltq'].quantile(0.33)
mkvalt_67 = train_df['mkvaltq'].quantile(0.67)

def cap_label(v):
    if v >= mkvalt_67:   return 'Large Cap'
    elif v >= mkvalt_33: return 'Mid Cap'
    return 'Small Cap'

train_df['cap_group'] = train_df['mkvaltq'].apply(cap_label)
test_raw['cap_group'] = test_raw['mkvaltq'].apply(
    lambda v: cap_label(v) if pd.notna(v) else 'Unknown')

train_df['log_mkvalt'] = np.log(train_df['mkvaltq'].clip(lower=1e-6))
test_raw['log_mkvalt'] = np.log(test_raw['mkvaltq'].clip(lower=1e-6))

sectors = sorted(train_df['sector_name'].dropna().unique())

cluster_models = {}
for s in sectors:
    idx    = train_df['sector_name'] == s
    subset = train_df.loc[idx, ratio_cols].fillna(train_medians)
    if len(subset) < 40:
        continue
    sc  = StandardScaler()
    km2 = KMeans(n_clusters=2, random_state=42, n_init=10)
    km2.fit(sc.fit_transform(subset))
    cluster_models[s] = (sc, km2)

train_df['sector_cluster'] = -1
for s, (sc, km2) in cluster_models.items():
    idx    = train_df['sector_name'] == s
    subset = train_df.loc[idx, ratio_cols].fillna(train_medians)
    train_df.loc[idx, 'sector_cluster'] = km2.predict(sc.transform(subset))

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

    cm = confusion_matrix(y_te.values, preds_te)
    tn, fp, fn, tp = cm.ravel() if cm.shape == (2,2) else (0,0,0,len(y_te))
    sensitivity = round(tp / (tp + fn) * 100, 1) if (tp + fn) > 0 else 0
    specificity = round(tn / (tn + fp) * 100, 1) if (tn + fp) > 0 else 0
    precision   = round(tp / (tp + fp) * 100, 1) if (tp + fp) > 0 else 0

    verdict = ("HOLDS UP" if auc_change >= -0.02
               else ("MODEST DEGRADATION" if auc_change >= -0.05
               else "SIGNIFICANT DEGRADATION"))

    overall_sig = "SIGNIFICANT" if model.llr_pvalue < 0.05 else "NOT SIGNIFICANT"
    sig_comps   = [f"PC{i+1}" for i in range(n_comp) if model.pvalues[i+1] < 0.05]

    print(f"\n{'='*70}")
    print(f"  {group_name.upper()}  [{config_name}]")
    print(f"  Train N={len(train_df2):,} | Test N={len(test_df2)} | "
          f"Test Outperformers={y_te.mean()*100:.1f}%")
    print(f"{'='*70}")

    print(f"\n── VALIDATION METRICS ────────────────────────────────────────────")
    rows = [
        ["Train AUC",      f"{train_auc:.4f}", "In-sample",       "—"],
        ["Test AUC",       f"{test_auc:.4f}",  "Out-of-sample",
         "Strong" if test_auc >= 0.70 else ("Moderate" if test_auc >= 0.60 else "Weak")],
        ["AUC Change",     f"{auc_change:+.4f}", "≥ -0.02 = holds up", verdict],
        ["Test Accuracy",  f"{test_acc}%",     "≥ 71.2% paper",
         "✓ Beats Paper" if test_acc >= 71.2 else "✗ Below Paper"],
        ["Sensitivity",    f"{sensitivity}%",  "Higher better",   "—"],
        ["Specificity",    f"{specificity}%",  "Higher better",   "—"],
        ["Precision",      f"{precision}%",    "Higher better",   "—"],
        ["LR p-value",     f"{model.llr_pvalue:.4f}", "< 0.05",  overall_sig],
        ["McFadden R²",    f"{model.prsquared:.4f}", "Train fit",  "—"],
        ["PCA Comps",      f"{n_comp}",        "≥80% variance",   "—"],
        ["VIF Kept",       f"{len(kept)}/{len(available)}", "≤2.5 cutoff", "—"],
        ["Cutoff",         f"{best_cut:.2f}",  "Optimised on train", "—"],
        ["Sig Comps",      f"{len(sig_comps)}/{n_comp}", "p<0.05", "—"],
    ]
    print(tabulate(rows, headers=["Metric","Value","Threshold","Verdict"], tablefmt="github"))

    print(f"\n── CONFUSION MATRIX (Test Set) ───────────────────────────────────")
    print(f"  Cutoff = {best_cut:.2f} | SPY Q2 2025 = {spy_q2_ret*100:+.2f}%")
    print(f"\n  {'':32s}  Predicted: Under (0)   Predicted: Over (1)")
    print(f"  {'Actual: Underperformer (0)':32s}  TN={tn:<12}  FP={fp}")
    print(f"  {'Actual: Outperformer  (1)':32s}  FN={fn:<12}  TP={tp}")
    print(f"\n  Sensitivity (Recall) : {sensitivity}%  — of true outperformers, correctly called")
    print(f"  Specificity          : {specificity}%  — of true underperformers, correctly called")
    print(f"  Precision            : {precision}%  — of predicted outperformers, truly so")

    print(f"\n── PCA COMPONENT COEFFICIENTS (fitted on training data) ──────────")
    conf      = np.array(model.conf_int())
    coef_rows = []
    for i in range(n_comp):
        coef  = model.params[i+1]
        p     = model.pvalues[i+1]
        OR    = np.exp(coef)
        ci_lo = np.exp(conf[i+1,0])
        ci_hi = np.exp(conf[i+1,1])
        if p < 0.01:   sig = "*** p<0.01"
        elif p < 0.05: sig = "**  p<0.05"
        elif p < 0.10: sig = "*   p<0.10"
        else:          sig = "No"
        coef_rows.append([f"PC{i+1}", f"{coef:+.4f}", f"{OR:.4f}",
                          f"[{ci_lo:.3f},{ci_hi:.3f}]",
                          f"{model.tvalues[i+1]:.3f}", f"{p:.4f}", sig])
    print(tabulate(coef_rows,
        headers=["Component","Coeff","Odds Ratio","95% CI","Z-Stat","p-Value","Significant?"],
        tablefmt="github"))

    print(f"\n── PCA LOADINGS FORMULA (fitted on training data) ────────────────")
    loadings_df = pd.DataFrame(pca_final.components_.T, index=kept,
                                columns=[f"PC{i+1}" for i in range(n_comp)])
    loading_rows = []
    for feat in kept:
        row = [ratio_labels.get(feat, feat)]
        for pc in loadings_df.columns:
            val = loadings_df.loc[feat, pc]
            row.append(f"{val:+.4f}")
        loading_rows.append(row)
    print(tabulate(loading_rows,
        headers=["Predictor"] + list(loadings_df.columns), tablefmt="github"))
    print(f"\n  Top 3 contributors per component:")
    for pc in loadings_df.columns:
        top = loadings_df[pc].abs().nlargest(3).index.tolist()
        print(f"  {pc}: {', '.join([ratio_labels.get(r,r) for r in top])}")

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
        'Precision': precision,
        'TP': int(tp), 'TN': int(tn), 'FP': int(fp), 'FN': int(fn),
        'Cutoff': round(best_cut, 2),
        'PCA Comps': n_comp,
        'VIF Kept': len(kept),
        'Sig Comps': f"{len(sig_comps)}/{n_comp}",
        'LR pvalue': round(model.llr_pvalue, 4),
        'McFadden R2': round(model.prsquared, 4),
        'Verdict': verdict,
    })


print("\n" + "="*70)
print("  CONFIGURATION 1: MARKET CAP SEGMENTATION")
print("="*70)
for cap in ['Large Cap', 'Mid Cap', 'Small Cap']:
    run_validation('Market Cap', cap,
                   train_df[train_df['cap_group'] == cap],
                   test_raw[test_raw['cap_group'] == cap])

print("\n" + "="*70)
print("  CONFIGURATION 2: SECTOR GICS")
print("="*70)
for s in sectors:
    run_validation('Sector GICS', s,
                   train_df[train_df['sector_name'] == s],
                   test_raw[test_raw['sector_name'] == s])

print("\n" + "="*70)
print("  CONFIGURATION 3: SECTOR + MARKET CAP COVARIATE")
print("="*70)
for s in sectors:
    run_validation('Sector + MktCap', f"{s} [+MktCap]",
                   train_df[train_df['sector_name'] == s],
                   test_raw[test_raw['sector_name'] == s],
                   feature_cols=ratio_cols + ['log_mkvalt'])

print("\n" + "="*70)
print("  CONFIGURATION 4: SECTOR + CLUSTERING (k=2)")
print("="*70)
for s in sectors:
    for c in [0, 1]:
        run_validation('Sector + Clustering (k=2)', f"{s} — Cluster {c}",
                       train_df[(train_df['sector_name'] == s) &
                                (train_df['sector_cluster'] == c)],
                       test_raw[(test_raw['sector_name'] == s) &
                                (test_raw['sector_cluster'] == c)])

print("\n\n" + "="*70)
print("  GRAND SUMMARY — WRDS + DELTA OUT-OF-SAMPLE VALIDATION")
print("  Training: Q1 2010–Q3 2024 | Features: Q1 2025 | Labels: Q2 2025")
print("  All groups | Sorted by out-of-sample AUC")
print("="*70)

if not all_results:
    print("  No groups had sufficient data.")
else:
    df_all = pd.DataFrame(all_results).sort_values('Test AUC', ascending=False).reset_index(drop=True)
    df_all.insert(0, 'Rank', range(1, len(df_all)+1))

    print(tabulate(
        df_all[['Rank','Configuration','Group','Train N','Test N',
                'Train AUC','Test AUC','AUC Change','Test Acc',
                'Sensitivity','Specificity','Verdict']].values.tolist(),
        headers=['Rank','Config','Group','Train N','Test N',
                 'Train AUC','Test AUC','ΔAUC','Acc%','Sens%','Spec%','Verdict'],
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
        ["Total groups validated",                len(df_all)],
        ["Training period",                       "Q1 2010 – Q3 2024 (WRDS Compustat + CRSP)"],
        ["Feature quarter",                       "Q1 2025 (WRDS Compustat)"],
        ["Label quarter",                         "Q2 2025 (Apr–Jun 2025, yFinance)"],
        ["SPY Q2 2025 return",                    f"{spy_q2_ret*100:+.2f}%"],
        ["Test set size",                         f"{len(test_raw)} stocks"],
        ["Feature set",                           f"14 base ratios + 10 delta features = {len(ratio_cols)} total"],
        ["Avg train AUC",                         f"{df_all['Train AUC'].mean():.4f}"],
        ["Avg test AUC",                          f"{df_all['Test AUC'].mean():.4f}"],
        ["Avg AUC change",                        f"{df_all['AUC Change'].mean():+.4f}"],
        ["Holds Up  (ΔAUC ≥ -0.02)",             f"{holds_up}/{len(df_all)}"],
        ["Modest Degradation (ΔAUC -0.02–-0.05)",f"{modest}/{len(df_all)}"],
        ["Significant Degradation (ΔAUC < -0.05)",f"{sig_deg}/{len(df_all)}"],
        ["Best out-of-sample group",              best_row['Group']],
        ["Best out-of-sample AUC",               f"{best_row['Test AUC']:.4f}"],
        ["Best out-of-sample accuracy",          f"{best_row['Test Acc']}%"],
        ["Paper benchmark accuracy",             "71.2%"],
    ]
    print(tabulate(summary_rows, tablefmt='github'))

    print(f"\n── METHODOLOGY NOTES ─────────────────────────────────────────────")
    print(f"  Data source       : 100% WRDS (Compustat + CRSP) — no EDGAR")
    print(f"  Feature source    : WRDS Compustat Q1 2025 (clean quarterly ratios)")
    print(f"  Delta features    : Q[t] – Q[t-1] for 10 key ratios (momentum signals)")
    print(f"  Label source      : yFinance adjusted closing prices Apr–Jun 2025")
    print(f"  Method            : VIF≤2.5 → PCA≥80% → Logistic Regression")
    print(f"  Winsorization     : 1st–99th percentile from training only")
    print(f"  Market cap ths.   : Computed from training data only")
    print(f"  Cluster assignment: KMeans fitted on 2010–Q3 2024, applied to Q1 2025")
    print(f"  Forward-looking   : Q[t] ratios → Q[t+1] outperformance (shift=-1)")
    print(f"  Rev/NI growth     : Q[t-1] → Q[t] change from Compustat")
    print("="*70)

    sys.stdout.log.close()
    sys.stdout = sys.stdout.terminal
    print(f"\n  Results saved to: results_validation_delta.txt")

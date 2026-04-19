import pandas as pd
import numpy as np
import warnings
from tabulate import tabulate
from sklearn.metrics import roc_auc_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from statsmodels.discrete.discrete_model import Logit
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm
warnings.filterwarnings('ignore')

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
comp = comp.merge(gics[['gvkey','gsector','sector_name']], on='gvkey', how='left')

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

for col in ratio_cols:
    lo = merged[col].quantile(0.01)
    hi = merged[col].quantile(0.99)
    merged[col] = merged[col].clip(lo, hi)

mkvalt_33 = merged['mkvaltq'].quantile(0.33)
mkvalt_67 = merged['mkvaltq'].quantile(0.67)

def cap_label(v):
    if v >= mkvalt_67: return 'Large'
    elif v >= mkvalt_33: return 'Mid'
    return 'Small'

merged['cap_group']  = merged['mkvaltq'].apply(cap_label)
merged['log_mkvalt'] = np.log(merged['mkvaltq'].clip(lower=1e-6))
merged['gsector_num']= pd.to_numeric(merged['gsector'], errors='coerce')

print("\n" + "="*75)
print("  MODEL SELECTION — BUILDING & ASSIGNING CLUSTERS")
print("="*75)

cluster_base   = merged[ratio_cols].copy().fillna(merged[ratio_cols].median())
scaler_full    = StandardScaler()
cluster_scaled = scaler_full.fit_transform(cluster_base)

for k in [3, 4, 5]:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    merged[f'cluster_k{k}'] = km.fit_predict(cluster_scaled)
    print(f"  K-Means k={k} assigned  ({merged[f'cluster_k{k}'].value_counts().to_dict()})")

merged['sector_cluster'] = -1
sectors = sorted(merged['sector_name'].dropna().unique())
for s in sectors:
    idx    = merged['sector_name'] == s
    subset = merged.loc[idx, ratio_cols].fillna(merged[ratio_cols].median())
    if len(subset) < 40:
        continue
    sc  = StandardScaler().fit_transform(subset)
    km2 = KMeans(n_clusters=2, random_state=42, n_init=10)
    merged.loc[idx, 'sector_cluster'] = km2.fit_predict(sc)

def vif_filter(X_df, cutoff=2.5):
    remaining = list(X_df.columns)
    while True:
        vifs    = [variance_inflation_factor(X_df[remaining].values, i) for i in range(len(remaining))]
        max_vif = max(vifs)
        if max_vif <= cutoff:
            break
        remaining.remove(remaining[vifs.index(max_vif)])
    return remaining

def run_model(df_subset, feature_cols=None):
    if feature_cols is None:
        feature_cols = ratio_cols
    available = [c for c in feature_cols if c in df_subset.columns]
    df = df_subset[available + ['outperformer_next']].dropna()
    if len(df) < 100 or df['outperformer_next'].nunique() < 2:
        return None
    X = df[available]
    y = df['outperformer_next']
    scaler   = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=available)
    try:
        kept = vif_filter(X_scaled, cutoff=2.5)
    except Exception:
        return None
    if len(kept) < 2:
        return None
    X_clean   = X_scaled[kept]
    exp_var   = np.cumsum(PCA().fit(X_clean).explained_variance_ratio_)
    n_comp    = min(int(np.searchsorted(exp_var, 0.80)) + 1, len(kept))
    X_pca     = PCA(n_components=n_comp).fit_transform(X_clean)
    X_const   = sm.add_constant(X_pca)
    try:
        result = Logit(y.values, X_const).fit(maxiter=200, disp=False)
    except Exception:
        return None
    y_prob = result.predict(X_const)
    auc    = roc_auc_score(y, y_prob)
    best_acc, best_cut = 0, 0.5
    for t in np.arange(0.30, 0.75, 0.05):
        acc = (( y_prob >= t).astype(int) == y.values).mean()
        if acc > best_acc:
            best_acc, best_cut = acc, t
    n_sig = sum(1 for i in range(n_comp) if result.pvalues[i+1] < 0.05)
    return {
        'n_obs': len(df),
        'auc': round(auc, 4),
        'accuracy': round(best_acc * 100, 1),
        'lr_pvalue': result.llr_pvalue,
        'lr_stat': round(result.llr, 2),
        'n_sig': n_sig,
        'n_comp': n_comp,
        'significant': result.llr_pvalue < 0.05
    }

def aggregate(seg_results):
    valid = [r for r in seg_results if r is not None]
    if not valid:
        return None
    total  = sum(r['n_obs'] for r in valid)
    w_auc  = sum(r['auc']      * r['n_obs'] for r in valid) / total
    w_acc  = sum(r['accuracy'] * r['n_obs'] for r in valid) / total
    n_sig  = sum(1 for r in valid if r['significant'])
    return {
        'w_auc': round(w_auc, 4),
        'w_acc': round(w_acc, 1),
        'total_obs': total,
        'n_valid': len(valid),
        'n_sig': n_sig
    }

print("\n── RUNNING ALL CONFIGURATIONS ─────────────────────────────────")
summary = []

r = run_model(merged)
if r:
    print(f"  [1] Global                          AUC={r['auc']:.4f}")
    summary.append({'Configuration': 'Global (No Segmentation)',
                    'Segs': 1, 'Weighted AUC': r['auc'],
                    'Accuracy %': r['accuracy'],
                    'Sig Segs': '1/1' if r['significant'] else '0/1',
                    'Obs': r['n_obs']})

cap_res = [run_model(merged[merged['cap_group'] == c]) for c in ['Large','Mid','Small']]
agg = aggregate(cap_res)
if agg:
    print(f"  [2] Market Cap (3 groups)           AUC={agg['w_auc']:.4f}")
    summary.append({'Configuration': 'Market Cap (3 groups)',
                    'Segs': 3, 'Weighted AUC': agg['w_auc'],
                    'Accuracy %': agg['w_acc'],
                    'Sig Segs': f"{agg['n_sig']}/3",
                    'Obs': agg['total_obs']})

sec_res = [run_model(merged[merged['sector_name'] == s]) for s in sectors]
agg = aggregate(sec_res)
n_v = len([r for r in sec_res if r])
n_s = sum(1 for r in sec_res if r and r['significant'])
if agg:
    print(f"  [3] Sector GICS ({n_v} sectors)          AUC={agg['w_auc']:.4f}")
    summary.append({'Configuration': f'Sector GICS ({n_v} sectors)',
                    'Segs': n_v, 'Weighted AUC': agg['w_auc'],
                    'Accuracy %': agg['w_acc'],
                    'Sig Segs': f"{n_s}/{n_v}",
                    'Obs': agg['total_obs']})

sec_cap_res = [run_model(merged[merged['sector_name'] == s],
                         feature_cols=ratio_cols + ['log_mkvalt']) for s in sectors]
agg = aggregate(sec_cap_res)
n_v = len([r for r in sec_cap_res if r])
n_s = sum(1 for r in sec_cap_res if r and r['significant'])
if agg:
    print(f"  [4] Sector + Market Cap Covariate   AUC={agg['w_auc']:.4f}")
    summary.append({'Configuration': 'Sector + Market Cap Covariate',
                    'Segs': n_v, 'Weighted AUC': agg['w_auc'],
                    'Accuracy %': agg['w_acc'],
                    'Sig Segs': f"{n_s}/{n_v}",
                    'Obs': agg['total_obs']})

for k in [3, 4, 5]:
    km_res = [run_model(merged[merged[f'cluster_k{k}'] == c]) for c in range(k)]
    agg    = aggregate(km_res)
    n_v    = len([r for r in km_res if r])
    n_s    = sum(1 for r in km_res if r and r['significant'])
    if agg:
        print(f"  [{4+k-2}] K-Means k={k}                      AUC={agg['w_auc']:.4f}")
        summary.append({'Configuration': f'K-Means Clustering (k={k})',
                        'Segs': k, 'Weighted AUC': agg['w_auc'],
                        'Accuracy %': agg['w_acc'],
                        'Sig Segs': f"{n_s}/{k}",
                        'Obs': agg['total_obs']})

sc_res = []
for s in sectors:
    s_df = merged[(merged['sector_name'] == s) & (merged['sector_cluster'] >= 0)]
    for c in [0, 1]:
        sc_res.append(run_model(s_df[s_df['sector_cluster'] == c]))
agg = aggregate(sc_res)
n_v = len([r for r in sc_res if r])
n_s = sum(1 for r in sc_res if r and r['significant'])
if agg:
    print(f"  [8] Sector + Clustering (k=2)       AUC={agg['w_auc']:.4f}")
    summary.append({'Configuration': 'Sector + Clustering (k=2 within)',
                    'Segs': n_v, 'Weighted AUC': agg['w_auc'],
                    'Accuracy %': agg['w_acc'],
                    'Sig Segs': f"{n_s}/{n_v}",
                    'Obs': agg['total_obs']})

km3_sec_res = [run_model(merged[merged['cluster_k3'] == c],
                          feature_cols=ratio_cols + ['gsector_num']) for c in range(3)]
agg = aggregate(km3_sec_res)
n_v = len([r for r in km3_sec_res if r])
n_s = sum(1 for r in km3_sec_res if r and r['significant'])
if agg:
    print(f"  [9] K-Means k=3 + Sector Covariate  AUC={agg['w_auc']:.4f}")
    summary.append({'Configuration': 'K-Means (k=3) + Sector Covariate',
                    'Segs': n_v, 'Weighted AUC': agg['w_auc'],
                    'Accuracy %': agg['w_acc'],
                    'Sig Segs': f"{n_s}/{n_v}",
                    'Obs': agg['total_obs']})

cap_sec_res = []
for cap in ['Large','Mid','Small']:
    cap_sec_res.append(run_model(merged[merged['cap_group'] == cap],
                                  feature_cols=ratio_cols + ['gsector_num']))
agg = aggregate(cap_sec_res)
n_v = len([r for r in cap_sec_res if r])
n_s = sum(1 for r in cap_sec_res if r and r['significant'])
if agg:
    print(f"  [10] Market Cap + Sector Covariate  AUC={agg['w_auc']:.4f}")
    summary.append({'Configuration': 'Market Cap + Sector Covariate',
                    'Segs': n_v, 'Weighted AUC': agg['w_auc'],
                    'Accuracy %': agg['w_acc'],
                    'Sig Segs': f"{n_s}/{n_v}",
                    'Obs': agg['total_obs']})

df_sum = pd.DataFrame(summary).sort_values('Weighted AUC', ascending=False).reset_index(drop=True)
df_sum.insert(0, 'Rank', range(1, len(df_sum)+1))

print("\n" + "="*75)
print("  FINAL COMPARISON TABLE — ALL CONFIGURATIONS")
print("  Sorted by Weighted AUC (highest = best predictive power)")
print("  Predicting: Q[t] ratios → Q[t+1] outperformance (forward-looking)")
print("="*75)
print(tabulate(df_sum.values.tolist(),
    headers=['Rank','Configuration','Segs','W. AUC','Accuracy %','Sig Segs','Obs'],
    tablefmt='github'))

winner = df_sum.iloc[0]
print(f"\n{'='*75}")
print(f"  WINNER: {winner['Configuration']}")
print(f"  Weighted AUC : {winner['Weighted AUC']:.4f}  (higher = better predictive power)")
print(f"  Accuracy     : {winner['Accuracy %']}%")
print(f"  Sig Segments : {winner['Sig Segs']}")
print(f"  Observations : {int(winner['Obs']):,}")
print(f"  Methodology  : VIF≤2.5 → PCA≥80% → Logistic Regression")
print(f"  Horizon      : Q[t] financial ratios → Q[t+1] outperformance")
print(f"  Benchmark    : Ananthakumar & Sarkar (2017) — 71.2% accuracy")
print(f"{'='*75}\n")

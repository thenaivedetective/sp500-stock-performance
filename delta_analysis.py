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

delta_base = ['roa','roe','gross_margin','op_margin','net_margin',
              'asset_turnover','current_ratio','debt_to_equity','pe_ratio','book_to_market']
for col in delta_base:
    comp[f'delta_{col}'] = comp.groupby('gvkey')[col].diff()

delta_cols = [f'delta_{c}' for c in delta_base]

gics['gvkey'] = gics['gvkey'].astype(str)
comp['gvkey']  = comp['gvkey'].astype(str)
comp = comp.merge(gics[['gvkey','gsector','sector_name']], on='gvkey', how='left')

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

for col in ratio_cols:
    if col not in merged.columns:
        continue
    lo = merged[col].quantile(0.01)
    hi = merged[col].quantile(0.99)
    merged[col] = merged[col].clip(lo, hi)

mkvalt_33 = merged['mkvaltq'].quantile(0.33)
mkvalt_67 = merged['mkvaltq'].quantile(0.67)

def cap_label(v):
    if v >= mkvalt_67: return 'Large Cap'
    elif v >= mkvalt_33: return 'Mid Cap'
    return 'Small Cap'

merged['cap_group']  = merged['mkvaltq'].apply(cap_label)
merged['log_mkvalt'] = np.log(merged['mkvaltq'].clip(lower=1e-6))

merged['sector_cluster'] = -1
sectors = sorted(merged['sector_name'].dropna().unique())
for s in sectors:
    idx    = merged['sector_name'] == s
    subset = merged.loc[idx, base_ratio_cols].fillna(merged[base_ratio_cols].median())
    if len(subset) < 40:
        continue
    sc  = StandardScaler().fit_transform(subset)
    km2 = KMeans(n_clusters=2, random_state=42, n_init=10)
    merged.loc[idx, 'sector_cluster'] = km2.fit_predict(sc)

baseline_auc = {}
try:
    bl = pd.read_csv('results_advanced.txt', sep='\t')
    for _, row in bl.iterrows():
        key = f"{row['Configuration']}|{row['Group']}"
        baseline_auc[key] = row['AUC']
except Exception:
    pass

def vif_filter(X_df, cutoff=2.5):
    remaining = list(X_df.columns)
    removed   = []
    while True:
        vifs    = [variance_inflation_factor(X_df[remaining].values, i) for i in range(len(remaining))]
        max_vif = max(vifs)
        if max_vif <= cutoff:
            break
        worst = remaining[vifs.index(max_vif)]
        removed.append((worst, round(max_vif, 2)))
        remaining.remove(worst)
    final_vif_dict = dict(zip(remaining, [round(v, 2) for v in vifs]))
    return remaining, removed, final_vif_dict

all_results = []

def run_group(config_name, group_name, df_group, feature_cols=None):
    if feature_cols is None:
        feature_cols = ratio_cols
    available = [c for c in feature_cols if c in df_group.columns]
    df = df_group[available + ['outperformer_next']].dropna()
    if len(df) < 100 or df['outperformer_next'].nunique() < 2:
        print(f"\n  {group_name}: insufficient data ({len(df)} rows), skipping.")
        return

    X = df[available]
    y = df['outperformer_next']

    scaler   = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=available)

    initial_vifs = [variance_inflation_factor(X_scaled.values, i) for i in range(len(available))]
    kept, removed, final_vif_dict = vif_filter(X_scaled, cutoff=2.5)

    X_clean   = X_scaled[kept]
    pca       = PCA()
    pca.fit(X_clean)
    exp_var   = np.cumsum(pca.explained_variance_ratio_)
    n_comp    = min(int(np.searchsorted(exp_var, 0.80)) + 1, len(kept))
    pca_final = PCA(n_components=n_comp)
    X_pca     = pca_final.fit_transform(X_clean)

    X_const = sm.add_constant(X_pca)
    result  = Logit(y.values, X_const).fit(maxiter=200, disp=False)

    y_prob  = result.predict(X_const)
    auc     = roc_auc_score(y, y_prob)

    best_cut, best_acc = 0.5, 0
    for thresh in np.arange(0.30, 0.75, 0.05):
        preds = (y_prob >= thresh).astype(int)
        acc   = (preds == y.values).mean()
        if acc > best_acc:
            best_acc, best_cut = acc, thresh
    best_cut = round(best_cut, 2)
    best_acc = round(best_acc * 100, 1)

    preds = (y_prob >= best_cut).astype(int)
    cm    = confusion_matrix(y.values, preds)
    tn, fp, fn, tp = cm.ravel() if cm.shape == (2,2) else (0,0,0,len(y))
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0

    overall_sig  = "SIGNIFICANT" if result.llr_pvalue < 0.05 else "NOT SIGNIFICANT"
    n_sig_comps  = sum(1 for i in range(n_comp) if result.pvalues[i+1] < 0.05)
    sig_comps    = [f"PC{i+1}" for i in range(n_comp) if result.pvalues[i+1] < 0.05]

    bl_key  = f"{config_name}|{group_name}"
    bl_auc  = baseline_auc.get(bl_key, None)
    auc_delta = round(auc - bl_auc, 4) if bl_auc is not None else None
    auc_delta_str = (f"+{auc_delta:.4f}" if auc_delta >= 0 else f"{auc_delta:.4f}") if auc_delta is not None else "N/A"
    verdict = ("IMPROVED" if auc_delta and auc_delta > 0.005
               else ("SIMILAR" if auc_delta and abs(auc_delta) <= 0.005
               else ("DECLINED" if auc_delta else "N/A")))

    delta_kept  = [k for k in kept if k.startswith('delta_')]
    levels_kept = [k for k in kept if not k.startswith('delta_')]

    print(f"\n{'='*65}")
    print(f"  {group_name.upper()}")
    print(f"  N={len(df):,} | Outperformers={y.mean()*100:.1f}% | Config: {config_name}")
    print(f"  Levels kept: {len(levels_kept)} | Delta features kept: {len(delta_kept)}/{len(delta_cols)}")
    print(f"{'='*65}")

    print(f"\n── MODEL FIT ─────────────────────────────────────────────────")
    fit_rows = [
        ["AUC (with deltas)",   f"{auc:.4f}",        "≥ 0.70 good",
         "Near-Random" if auc < 0.60 else ("Moderate" if auc < 0.70 else "Strong")],
        ["Baseline AUC",        f"{bl_auc:.4f}" if bl_auc else "N/A", "Levels only", "—"],
        ["AUC Change (Δ)",      auc_delta_str,        "> 0 = improved", verdict],
        ["Accuracy",            f"{best_acc}%",       "≥ 71.2% paper",
         "✓ Beats Paper" if best_acc >= 71.2 else "✗ Below Paper"],
        ["LR p-value",          f"{result.llr_pvalue:.4f}", "< 0.05", overall_sig],
        ["McFadden R²",         f"{result.prsquared:.4f}", "≥ 0.20 good",
         "Very Weak" if result.prsquared < 0.05 else "Weak"],
        ["Sensitivity",         f"{sensitivity*100:.1f}%", "Higher better", "—"],
        ["Specificity",         f"{specificity*100:.1f}%", "Higher better", "—"],
        ["PCA Components",      f"{n_comp}",          "≥80% variance", "—"],
        ["Sig Components",      f"{n_sig_comps}/{n_comp}", "> 0", "—"],
    ]
    print(tabulate(fit_rows, headers=["Metric","Value","Threshold","Verdict"], tablefmt="github"))

    print(f"\n── DELTA FEATURES SURVIVING VIF ─────────────────────────────")
    if delta_kept:
        for d in delta_kept:
            print(f"  ✓ {ratio_labels.get(d, d)}")
    else:
        print(f"  None survived VIF filter (all removed as redundant)")

    print(f"\n── TOP LOADINGS PER PCA COMPONENT ────────────────────────────")
    loadings = pd.DataFrame(pca_final.components_.T, index=kept,
                            columns=[f"PC{i+1}" for i in range(n_comp)])
    for comp_name in loadings.columns:
        top       = loadings[comp_name].abs().nlargest(3).index.tolist()
        top_named = [ratio_labels.get(r, r) for r in top]
        is_delta  = any(t.startswith('delta_') for t in top)
        marker    = " ← delta-driven" if is_delta else ""
        print(f"  {comp_name}: {', '.join(top_named)}{marker}")

    all_results.append({
        'Configuration': config_name,
        'Group': group_name,
        'N': len(df),
        'Baseline AUC': round(bl_auc, 4) if bl_auc else None,
        'Delta AUC': round(auc, 4),
        'AUC Change': auc_delta,
        'Accuracy': best_acc,
        'LR p-value': round(result.llr_pvalue, 4),
        'Significant': result.llr_pvalue < 0.05,
        'Sig Components': f"{n_sig_comps}/{n_comp}",
        'Delta Features Kept': len(delta_kept),
        'Verdict': verdict,
    })


print("\n" + "="*65)
print("  DELTA FEATURE ANALYSIS — LEVELS + QoQ CHANGES")
print("  S&P 500 | Q1 2010 – Q4 2024 | WRDS (lanagidan9790)")
print("  Features: 14 ratio levels + 10 delta (QoQ change) features")
print("  Predicting: Q[t] ratios+deltas → Q[t+1] outperformance")
print("  Reference: Ananthakumar & Sarkar (2017) — VIF cutoff=2.5, PCA ≥80%")
print("="*65)

print("\n\n" + "="*65)
print("  CONFIGURATION 1: MARKET CAP SEGMENTATION")
print("="*65)
for cap in ['Large Cap', 'Mid Cap', 'Small Cap']:
    run_group('Market Cap Segmentation', cap, merged[merged['cap_group'] == cap])

print("\n\n" + "="*65)
print("  CONFIGURATION 2: SECTOR SEGMENTATION (GICS)")
print("="*65)
for s in sectors:
    run_group('Sector GICS', s, merged[merged['sector_name'] == s])

print("\n\n" + "="*65)
print("  CONFIGURATION 3: SECTOR + MARKET CAP COVARIATE")
print("="*65)
for s in sectors:
    run_group('Sector + Market Cap Covariate', f"{s} [+MktCap]",
              merged[merged['sector_name'] == s],
              feature_cols=ratio_cols + ['log_mkvalt'])

print("\n\n" + "="*65)
print("  CONFIGURATION 4: SECTOR + CLUSTERING (K=2)")
print("="*65)
for s in sectors:
    s_df = merged[(merged['sector_name'] == s) & (merged['sector_cluster'] >= 0)]
    for c in [0, 1]:
        run_group('Sector + Clustering (k=2)', f"{s} — Cluster {c}",
                  s_df[s_df['sector_cluster'] == c])

print("\n\n" + "="*65)
print("  GRAND SUMMARY — DELTA vs BASELINE AUC COMPARISON")
print("  All 4 configurations | Sorted by AUC Change (biggest improvement first)")
print("="*65)

df_all = pd.DataFrame(all_results)
df_all = df_all.sort_values('AUC Change', ascending=False).reset_index(drop=True)
df_all.insert(0, 'Rank', range(1, len(df_all)+1))
df_all['Sig'] = df_all['Significant'].map({True: '✓', False: '✗'})

print(tabulate(
    df_all[['Rank','Configuration','Group','N','Baseline AUC','Delta AUC',
            'AUC Change','Accuracy','Sig Components','Verdict','Sig']].values.tolist(),
    headers=['Rank','Config','Group','N','Base AUC','Delta AUC','ΔAUC',
             'Acc%','Sig Comps','Verdict','Sig?'],
    tablefmt='github'
))

improved   = (df_all['AUC Change'] > 0.005).sum()
declined   = (df_all['AUC Change'] < -0.005).sum()
similar    = len(df_all) - improved - declined
valid      = df_all['AUC Change'].notna().sum()
avg_delta  = df_all['AUC Change'].mean()
best_row   = df_all.iloc[0]
worst_row  = df_all[df_all['AUC Change'] == df_all['AUC Change'].min()].iloc[0]

print(f"\n── CONFIGURATION-LEVEL SUMMARY ───────────────────────────────")
config_summary = []
for cfg in df_all['Configuration'].unique():
    sub   = df_all[df_all['Configuration'] == cfg]
    w_auc = (sub['Delta AUC'] * sub['N']).sum() / sub['N'].sum()
    w_bl  = (sub['Baseline AUC'].fillna(sub['Delta AUC']) * sub['N']).sum() / sub['N'].sum()
    imp   = (sub['AUC Change'] > 0.005).sum()
    config_summary.append([cfg, len(sub), round(w_bl, 4), round(w_auc, 4),
                           round(w_auc - w_bl, 4), f"{imp}/{len(sub)}"])
config_summary.sort(key=lambda x: x[3], reverse=True)
for i, row in enumerate(config_summary):
    row.insert(0, i+1)
print(tabulate(config_summary,
    headers=['Rank','Configuration','Groups','Base W.AUC','Delta W.AUC','ΔAUC','Improved'],
    tablefmt='github'))

print(f"\n── OVERALL VERDICT ───────────────────────────────────────────")
print(f"  Groups improved  (ΔAUC > +0.005) : {improved}/{valid}")
print(f"  Groups similar   (|ΔAUC| ≤ 0.005): {similar}/{valid}")
print(f"  Groups declined  (ΔAUC < -0.005) : {declined}/{valid}")
print(f"  Average AUC change across all groups: {avg_delta:+.4f}")
print(f"  Best improvement : {best_row['Group']} ({best_row['AUC Change']:+.4f})")
print(f"  Worst decline    : {worst_row['Group']} ({worst_row['AUC Change']:+.4f})")
print(f"\n  Best delta AUC   : {df_all.iloc[df_all['Delta AUC'].idxmax()]['Group']} "
      f"(AUC={df_all['Delta AUC'].max():.4f})")
print(f"\n  Methodology      : VIF≤2.5 → PCA≥80% → Logistic Regression")
print(f"  Feature set      : 14 levels + 10 QoQ delta features (24 total → VIF filtered)")
print(f"  Horizon          : Q[t] ratios+deltas → Q[t+1] outperformance (shift=-1)")
print(f"  Benchmark        : Ananthakumar & Sarkar (2017) — 71.2% accuracy")
print("="*65 + "\n")

df_all.to_csv('results_delta.txt', sep='\t', index=False)
print("  Results saved to: results_delta.txt")

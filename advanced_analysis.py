import pandas as pd
import numpy as np
import warnings
from tabulate import tabulate
from sklearn.metrics import roc_auc_score, roc_curve, confusion_matrix
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
    'roa':'Return on Assets (ROA)', 'roe':'Return on Equity (ROE)',
    'gross_margin':'Gross Profit Margin', 'op_margin':'Operating Margin',
    'net_margin':'Net Profit Margin', 'asset_turnover':'Asset Turnover',
    'current_ratio':'Current Ratio', 'debt_to_equity':'Debt-to-Equity',
    'rev_growth':'Revenue Growth (QoQ)', 'ni_growth':'Net Income Growth (QoQ)',
    'pe_ratio':'P/E Ratio', 'book_to_market':'Book-to-Market',
    'gdp_growth':'GDP Growth (Quarterly)', 'inflation':'CPI Inflation (Quarterly)',
    'log_mkvalt':'Log Market Cap (Covariate)',
    'delta_roa':'ΔROA (QoQ)',
    'delta_roe':'ΔROE (QoQ)',
    'delta_gross_margin':'ΔGross Profit Margin (QoQ)',
    'delta_op_margin':'ΔOperating Margin (QoQ)',
    'delta_net_margin':'ΔNet Margin (QoQ)',
    'delta_asset_turnover':'ΔAsset Turnover (QoQ)',
    'delta_current_ratio':'ΔCurrent Ratio (QoQ)',
    'delta_debt_to_equity':'ΔDebt-to-Equity (QoQ)',
    'delta_pe_ratio':'ΔP/E Ratio (QoQ)',
    'delta_book_to_market':'ΔBook-to-Market (QoQ)',
}

merged = comp.merge(
    crsp[['ticker','quarter','quarterly_return','spy_quarterly_return','outperformer_quarterly']],
    left_on=['tic','cal_quarter'], right_on=['ticker','quarter'], how='inner'
)
merged = merged.merge(macro, left_on='cal_quarter', right_on='quarter', how='left')

merged = merged[merged['cal_quarter'] <= pd.Period('2024Q4', 'Q')]

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
    if col in merged.columns:
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
    subset = merged.loc[idx, ratio_cols].fillna(merged[ratio_cols].median())
    if len(subset) < 40:
        continue
    sc  = StandardScaler().fit_transform(subset)
    km2 = KMeans(n_clusters=2, random_state=42, n_init=10)
    merged.loc[idx, 'sector_cluster'] = km2.fit_predict(sc)

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

    overall_sig = "SIGNIFICANT" if result.llr_pvalue < 0.05 else "NOT SIGNIFICANT"
    n_sig_comps = sum(1 for i in range(n_comp) if result.pvalues[i+1] < 0.05)
    sig_comps   = [f"PC{i+1}" for i in range(n_comp) if result.pvalues[i+1] < 0.05]

    print(f"\n{'='*65}")
    print(f"  {group_name.upper()}")
    print(f"  N={len(df):,} | Next-Q Outperformers={y.mean()*100:.1f}%")
    print(f"  Predicting: Q[t] ratios → Q[t+1] outperformance")
    print(f"{'='*65}")

    print(f"\n── VIF — ALL PREDICTORS (cutoff = 2.5) ───────────────────────")
    removed_vif_dict = dict(removed)
    vif_all_rows = []
    for var, v_init in zip(available, initial_vifs):
        label = ratio_labels.get(var, var)
        if var in kept:
            vif_all_rows.append([label, f"{v_init:.2f}", f"{final_vif_dict[var]:.2f}", "✓ Kept"])
        else:
            vif_all_rows.append([label, f"{v_init:.2f}", "removed", "✗ Removed"])
    print(tabulate(vif_all_rows,
        headers=["Predictor","Initial VIF","Final VIF","Decision"], tablefmt="github"))
    print(f"  All kept predictors have Final VIF ≤ 2.5  ✓")
    print(f"\n  Predictors kept ({len(kept)}): {', '.join([ratio_labels.get(k,k) for k in kept])}")

    print(f"\n── PCA — EXPLAINED VARIANCE ──────────────────────────────────")
    pca_rows = []
    cumvar   = 0
    for i, ev in enumerate(pca_final.explained_variance_ratio_):
        cumvar += ev
        pca_rows.append([f"PC{i+1}", f"{ev*100:.1f}%", f"{cumvar*100:.1f}%"])
    print(tabulate(pca_rows, headers=["Component","Variance Explained","Cumulative"], tablefmt="github"))
    print(f"  → {n_comp} components retained (explaining ≥ 80% of variance)")

    print(f"\n── PCA COMPONENT LOADINGS (FORMULA) ──────────────────────────")
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
    print(f"\n  Top 3 loadings per component:")
    for pc in loadings_df.columns:
        top       = loadings_df[pc].abs().nlargest(3).index.tolist()
        top_named = [ratio_labels.get(r, r) for r in top]
        print(f"  {pc}: {', '.join(top_named)}")

    print(f"\n── OPTIMAL PROBABILITY CUTOFF ────────────────────────────────")
    cutoff_rows = []
    for thresh in np.arange(0.30, 0.75, 0.05):
        p    = (y_prob >= thresh).astype(int)
        acc  = (p == y.values).mean() * 100
        cm_t = confusion_matrix(y.values, p)
        if cm_t.shape == (2,2):
            tn_t,fp_t,fn_t,tp_t = cm_t.ravel()
            sens_t = tp_t/(tp_t+fn_t) if (tp_t+fn_t)>0 else 0
            spec_t = tn_t/(tn_t+fp_t) if (tn_t+fp_t)>0 else 0
        else:
            sens_t = spec_t = 0
        marker = " ← CHOSEN" if abs(thresh - best_cut) < 0.01 else ""
        cutoff_rows.append([f"{thresh:.2f}", f"{acc:.1f}%", f"{sens_t*100:.1f}%", f"{spec_t*100:.1f}%", marker])
    print(tabulate(cutoff_rows,
        headers=["Cutoff","Accuracy","Sensitivity","Specificity",""], tablefmt="github"))

    print(f"\n── MODEL FIT & OVERALL SIGNIFICANCE ─────────────────────────")
    fit_rows = [
        ["LR p-value",         f"{result.llr_pvalue:.4f}", "< 0.05",          overall_sig],
        ["LR Statistic",       f"{result.llr:.2f}",        "Higher better",   "—"],
        ["McFadden Pseudo R²", f"{result.prsquared:.4f}",  "≥ 0.20 good",
         "Very Weak" if result.prsquared < 0.05 else ("Weak" if result.prsquared < 0.10 else "Moderate")],
        ["AUC",                f"{auc:.4f}",               "≥ 0.70 good",
         "Near-Random" if auc < 0.60 else ("Moderate" if auc < 0.70 else "Strong")],
        ["Probability Cutoff", f"{best_cut}",              "Trial & Error",   "Chosen"],
        ["Overall Accuracy",   f"{best_acc}%",             "≥ 71.2% (paper)",
         "✓ Beats Paper" if best_acc >= 71.2 else "✗ Below Paper"],
        ["Sensitivity",        f"{sensitivity*100:.1f}%",  "Higher better",   "—"],
        ["Specificity",        f"{specificity*100:.1f}%",  "Higher better",   "—"],
    ]
    print(tabulate(fit_rows, headers=["Metric","Value","Threshold","Verdict"], tablefmt="github"))

    print(f"\n── CONFUSION MATRIX ──────────────────────────────────────────")
    print(f"  Cutoff = {best_cut}")
    print(f"\n  {'':30s}  Pred: Under (0)   Pred: Over (1)")
    print(f"  {'Actual: Underperformer (0)':30s}  TN={tn:<12,}  FP={fp:,}")
    print(f"  {'Actual: Outperformer  (1)':30s}  FN={fn:<12,}  TP={tp:,}")

    print(f"\n── PCA COMPONENT COEFFICIENTS & SIGNIFICANCE ─────────────────")
    conf      = np.array(result.conf_int())
    coef_rows = []
    for i in range(n_comp):
        coef  = result.params[i+1]
        p     = result.pvalues[i+1]
        OR    = np.exp(coef)
        ci_lo = np.exp(conf[i+1,0])
        ci_hi = np.exp(conf[i+1,1])
        if p < 0.01:   sig = "*** p<0.01"
        elif p < 0.05: sig = "**  p<0.05"
        elif p < 0.10: sig = "*   p<0.10"
        else:          sig = "No"
        coef_rows.append([f"PC{i+1}", f"{coef:+.4f}", f"{OR:.4f}",
                          f"[{ci_lo:.3f},{ci_hi:.3f}]",
                          f"{result.tvalues[i+1]:.3f}", f"{p:.4f}", sig])
    print(tabulate(coef_rows,
        headers=["Component","Coeff","Odds Ratio","95% CI","Z-Stat","p-Value","Significant?"],
        tablefmt="github"))

    print(f"\n── GROUP CONCLUSION ──────────────────────────────────────────")
    print(f"  Group         : {group_name}")
    print(f"  Configuration : {config_name}")
    print(f"  AUC           : {auc:.4f}")
    print(f"  Accuracy      : {best_acc}%")
    print(f"  Overall sig   : {overall_sig}")
    print(f"  Sig components: {', '.join(sig_comps) if sig_comps else 'None'} ({n_sig_comps}/{n_comp})")

    all_results.append({
        'Configuration': config_name,
        'Group': group_name,
        'N': len(df),
        'AUC': round(auc, 4),
        'Accuracy': best_acc,
        'Sensitivity': round(sensitivity*100, 1),
        'Specificity': round(specificity*100, 1),
        'TP': int(tp), 'TN': int(tn), 'FP': int(fp), 'FN': int(fn),
        'LR p-value': round(result.llr_pvalue, 4),
        'McFadden_R2': round(result.prsquared, 4),
        'Significant': result.llr_pvalue < 0.05,
        'Sig Components': f"{n_sig_comps}/{n_comp}",
        'Cutoff': best_cut,
        'PCA_Components': n_comp,
        'Features_After_VIF': len(kept),
    })


print("\n" + "="*65)
print("  ADVANCED SEGMENTATION ANALYSIS — WITH DELTA FEATURES")
print("  S&P 500 | Q1 2010 – Q4 2024 | WRDS (lanagidan9790)")
print("  Predicting: NEXT quarter outperformance using CURRENT quarter ratios")
print("  Features: 14 base ratios + 10 QoQ delta features = 24 total")
print("  Reference: Ananthakumar & Sarkar (2017) — VIF cutoff=2.5, PCA ≥80%")
print("="*65)

print("\n\n" + "="*65)
print("  CONFIGURATION 1: MARKET CAP SEGMENTATION")
print("  Groups: Large Cap | Mid Cap | Small Cap")
print("="*65)
print(f"\n── MARKET CAP THRESHOLDS ─────────────────────────────────────")
print(tabulate([
    ["Small Cap", f"< ${mkvalt_33/1000:.0f}B",  f"{(merged['cap_group']=='Small Cap').sum():,} obs"],
    ["Mid Cap",   f"${mkvalt_33/1000:.0f}B – ${mkvalt_67/1000:.0f}B", f"{(merged['cap_group']=='Mid Cap').sum():,} obs"],
    ["Large Cap", f"> ${mkvalt_67/1000:.0f}B",  f"{(merged['cap_group']=='Large Cap').sum():,} obs"],
], headers=["Group","Market Cap Range","Observations"], tablefmt="github"))

for cap in ['Large Cap', 'Mid Cap', 'Small Cap']:
    run_group('Market Cap Segmentation', cap, merged[merged['cap_group'] == cap])

print("\n\n" + "="*65)
print("  CONFIGURATION 2: SECTOR SEGMENTATION (GICS)")
print("  Groups: 11 GICS Sectors individually")
print("="*65)
print(f"\n── SECTOR COVERAGE ───────────────────────────────────────────")
sec_rows = []
for s in sectors:
    n = (merged['sector_name'] == s).sum()
    sec_rows.append([s, f"{n:,} obs"])
print(tabulate(sec_rows, headers=["Sector","Observations"], tablefmt="github"))

for s in sectors:
    run_group('Sector GICS', s, merged[merged['sector_name'] == s])

print("\n\n" + "="*65)
print("  CONFIGURATION 3: SECTOR + MARKET CAP COVARIATE")
print("  Groups: 11 GICS Sectors with Log(Market Cap) added as predictor")
print("="*65)

for s in sectors:
    run_group('Sector + Market Cap Covariate', f"{s} [+MktCap]",
              merged[merged['sector_name'] == s],
              feature_cols=ratio_cols + ['log_mkvalt'])

print("\n\n" + "="*65)
print("  CONFIGURATION 4: SECTOR + CLUSTERING (K=2 WITHIN EACH SECTOR)")
print("  Groups: 2 K-Means clusters within each of 11 GICS Sectors")
print("  Clusters built on standardized financial ratios per sector")
print("="*65)

for s in sectors:
    s_df = merged[(merged['sector_name'] == s) & (merged['sector_cluster'] >= 0)]
    for c in [0, 1]:
        run_group('Sector + Clustering (k=2)', f"{s} — Cluster {c}",
                  s_df[s_df['sector_cluster'] == c])

print("\n\n" + "="*65)
print("  GRAND COMPARISON — ALL GROUPS ACROSS ALL CONFIGURATIONS")
print("  Sorted by AUC (highest predictive power first)")
print("  Predicting: Q[t] ratios → Q[t+1] outperformance (forward-looking)")
print("="*65)

df_all = pd.DataFrame(all_results).sort_values('AUC', ascending=False).reset_index(drop=True)
df_all.insert(0, 'Rank', range(1, len(df_all)+1))
df_all['Sig'] = df_all['Significant'].map({True: '✓', False: '✗'})

print(tabulate(
    df_all[['Rank','Configuration','Group','N','AUC','Accuracy','LR p-value','Sig Components','Sig']].values.tolist(),
    headers=['Rank','Configuration','Group','N','AUC','Acc%','LR p-val','Sig Comps','Sig?'],
    tablefmt='github'
))

print("\n── CONFIGURATION-LEVEL SUMMARY ───────────────────────────────")
config_summary = []
for cfg in df_all['Configuration'].unique():
    sub   = df_all[df_all['Configuration'] == cfg]
    w_auc = (sub['AUC'] * sub['N']).sum() / sub['N'].sum()
    n_sig = sub['Significant'].sum()
    config_summary.append([cfg, len(sub), round(w_auc, 4),
                           f"{n_sig}/{len(sub)}", round(sub['Accuracy'].mean(), 1)])
config_summary.sort(key=lambda x: x[2], reverse=True)
for i, row in enumerate(config_summary):
    row.insert(0, i+1)
print(tabulate(config_summary,
    headers=['Rank','Configuration','Groups','W.AUC','Sig Groups','Avg Acc%'],
    tablefmt='github'))

best_cfg   = config_summary[0]
best_group = df_all.iloc[0]

print(f"\n{'='*65}")
print(f"  WINNER CONFIGURATION: {best_cfg[1]}")
print(f"  Weighted AUC across all groups : {best_cfg[3]:.4f}")
print(f"  Significant groups             : {best_cfg[4]}")
print(f"  Average Accuracy               : {best_cfg[5]}%")
print(f"\n  BEST INDIVIDUAL GROUP: {best_group['Group']}")
print(f"  Configuration : {best_group['Configuration']}")
print(f"  AUC           : {best_group['AUC']:.4f}")
print(f"  Accuracy      : {best_group['Accuracy']}%")
print(f"  Sig Components: {best_group['Sig Components']}")
print(f"\n  Methodology   : VIF≤2.5 → PCA≥80% → Logistic Regression")
print(f"  Features      : 14 base ratios + 10 QoQ delta features = 24 total")
print(f"  Horizon       : Q[t] ratios → Q[t+1] outperformance (shift=-1)")
print(f"  Benchmark     : Ananthakumar & Sarkar (2017) — 71.2% accuracy")
print("="*65 + "\n")

df_all.to_csv('results_advanced.txt', sep='\t', index=False)
print("  Results saved to: results_advanced.txt")

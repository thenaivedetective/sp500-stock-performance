import pandas as pd
import numpy as np
import warnings
from tabulate import tabulate
from sklearn.metrics import roc_auc_score, roc_curve, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from statsmodels.discrete.discrete_model import Logit
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm
warnings.filterwarnings('ignore')

comp = pd.read_csv('wrds_compustat_quarterly.csv', low_memory=False)
crsp = pd.read_csv('wrds_crsp_quarterly.csv', low_memory=False)
gics = pd.read_csv('wrds_gics_sectors.csv', low_memory=False)

comp['datadate']  = pd.to_datetime(comp['datadate'])
comp['cal_quarter'] = comp['datadate'].dt.to_period('Q')
crsp['quarter']   = pd.PeriodIndex(crsp['quarter_str'], freq='Q')

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
comp['rd_intensity']   = comp['xrdq']   / comp['revtq'].replace(0, np.nan)
comp['rev_growth']     = (comp['revtq'] - comp['lag_revtq']) / comp['lag_revtq'].abs().replace(0, np.nan)
comp['ni_growth']      = (comp['niq']   - comp['lag_niq'])   / comp['lag_niq'].abs().replace(0, np.nan)
comp['pe_ratio']       = comp['prccq']  / (comp['ibq'] / comp['cshoq'].replace(0, np.nan)).replace(0, np.nan)
comp['book_to_market'] = comp['ceqq']   / comp['mkvaltq'].replace(0, np.nan)

gics['gvkey'] = gics['gvkey'].astype(str)
comp['gvkey']  = comp['gvkey'].astype(str)
comp = comp.merge(gics[['gvkey','gsector','sector_name','sic']], on='gvkey', how='left')

ratio_cols = ['roa','roe','gross_margin','op_margin','net_margin','asset_turnover',
              'current_ratio','debt_to_equity','rd_intensity','rev_growth','ni_growth',
              'pe_ratio','book_to_market']

merged = comp.merge(
    crsp[['ticker','quarter','quarterly_return','spy_quarterly_return','outperformer_quarterly']],
    left_on=['tic','cal_quarter'], right_on=['ticker','quarter'], how='inner'
)

for col in ratio_cols:
    lo = merged[col].quantile(0.01)
    hi = merged[col].quantile(0.99)
    merged[col] = merged[col].clip(lo, hi)

mkvalt_33 = merged['mkvaltq'].quantile(0.33)
mkvalt_67 = merged['mkvaltq'].quantile(0.67)

def assign_cap(v):
    if v >= mkvalt_67: return 'Large Cap'
    elif v >= mkvalt_33: return 'Mid Cap'
    else: return 'Small Cap'

merged['market_cap_group'] = merged['mkvaltq'].apply(assign_cap)

ratio_labels = {
    'roa':'Return on Assets (ROA)', 'roe':'Return on Equity (ROE)',
    'gross_margin':'Gross Profit Margin', 'op_margin':'Operating Margin',
    'net_margin':'Net Profit Margin', 'asset_turnover':'Asset Turnover',
    'current_ratio':'Current Ratio', 'debt_to_equity':'Debt-to-Equity',
    'rd_intensity':'R&D Intensity', 'rev_growth':'Revenue Growth (QoQ)',
    'ni_growth':'Net Income Growth (QoQ)', 'pe_ratio':'P/E Ratio',
    'book_to_market':'Book-to-Market',
}

def vif_filter(X_df, cutoff=2.5):
    remaining = list(X_df.columns)
    removed   = []
    while True:
        vifs = [variance_inflation_factor(X_df[remaining].values, i) for i in range(len(remaining))]
        max_vif = max(vifs)
        if max_vif <= cutoff:
            break
        worst = remaining[vifs.index(max_vif)]
        removed.append((worst, round(max_vif, 2)))
        remaining.remove(worst)
    return remaining, removed

def find_best_cutoff(y_true, y_prob):
    fpr, tpr, thresholds = roc_curve(y_true, y_prob)
    best_cutoff, best_acc = 0.5, 0
    for thresh in np.arange(0.30, 0.75, 0.05):
        preds = (y_prob >= thresh).astype(int)
        acc   = (preds == y_true).mean()
        if acc > best_acc:
            best_acc    = acc
            best_cutoff = thresh
    return round(best_cutoff, 2), round(best_acc * 100, 1)

def run_group(group_name, df_group):
    df = df_group[ratio_cols + ['outperformer_quarterly']].dropna()
    if len(df) < 100:
        print(f"\n  {group_name}: insufficient data ({len(df)} rows), skipping.")
        return

    X = df[ratio_cols]
    y = df['outperformer_quarterly']

    scaler   = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=ratio_cols)

    kept, removed = vif_filter(X_scaled, cutoff=2.5)

    X_clean  = X_scaled[kept]
    pca      = PCA()
    pca.fit(X_clean)
    exp_var  = np.cumsum(pca.explained_variance_ratio_)
    n_comp   = int(np.searchsorted(exp_var, 0.80)) + 1
    pca_final = PCA(n_components=n_comp)
    X_pca    = pca_final.fit_transform(X_clean)

    X_const  = sm.add_constant(X_pca)
    result   = Logit(y.values, X_const).fit(maxiter=200, disp=False)

    y_prob   = result.predict(X_const)
    auc      = roc_auc_score(y, y_prob)
    best_cut, best_acc = find_best_cutoff(y.values, y_prob)

    preds    = (y_prob >= best_cut).astype(int)
    cm       = confusion_matrix(y.values, preds)
    tn, fp, fn, tp = cm.ravel() if cm.shape == (2,2) else (0,0,0,len(y))
    sensitivity  = tp / (tp + fn) if (tp + fn) > 0 else 0
    specificity  = tn / (tn + fp) if (tn + fp) > 0 else 0

    overall_sig = "SIGNIFICANT" if result.llr_pvalue < 0.05 else "NOT SIGNIFICANT"

    print(f"\n{'='*65}")
    print(f"  {group_name.upper()}  (N={len(df):,} | Outperformers={y.mean()*100:.1f}%)")
    print(f"{'='*65}")

    print(f"\n── VIF FILTERING (cutoff = 2.5) ─────────────────────────────")
    if removed:
        rem_rows = [[ratio_labels.get(v,v), vif] for v,vif in removed]
        print(tabulate(rem_rows, headers=["Removed Predictor","VIF at Removal"], tablefmt="github"))
    else:
        print("  No predictors removed — all VIF ≤ 2.5")
    print(f"\n  Predictors kept ({len(kept)}): {', '.join([ratio_labels.get(k,k) for k in kept])}")

    print(f"\n── PCA — EXPLAINED VARIANCE ──────────────────────────────────")
    pca_rows = []
    cumvar = 0
    for i, ev in enumerate(pca_final.explained_variance_ratio_):
        cumvar += ev
        pca_rows.append([f"PC{i+1}", f"{ev*100:.1f}%", f"{cumvar*100:.1f}%"])
    print(tabulate(pca_rows, headers=["Component","Variance Explained","Cumulative"], tablefmt="github"))
    print(f"  → {n_comp} components retained (explaining ≥ 80% of variance)")

    print(f"\n── OPTIMAL PROBABILITY CUTOFF ────────────────────────────────")
    cutoff_rows = []
    for thresh in np.arange(0.30, 0.75, 0.05):
        p      = (y_prob >= thresh).astype(int)
        acc    = (p == y.values).mean() * 100
        cm_t   = confusion_matrix(y.values, p)
        if cm_t.shape == (2,2):
            tn_t,fp_t,fn_t,tp_t = cm_t.ravel()
            sens_t = tp_t/(tp_t+fn_t) if (tp_t+fn_t)>0 else 0
            spec_t = tn_t/(tn_t+fp_t) if (tn_t+fp_t)>0 else 0
        else:
            sens_t = spec_t = 0
        marker = " ← CHOSEN" if abs(thresh - best_cut) < 0.01 else ""
        cutoff_rows.append([f"{thresh:.2f}", f"{acc:.1f}%", f"{sens_t*100:.1f}%", f"{spec_t*100:.1f}%", marker])
    print(tabulate(cutoff_rows,
        headers=["Cutoff","Accuracy","Sensitivity","Specificity",""],
        tablefmt="github"))

    print(f"\n── MODEL FIT & OVERALL SIGNIFICANCE ─────────────────────────")
    fit_rows = [
        ["LR p-value",        f"{result.llr_pvalue:.4f}", "< 0.05",    overall_sig],
        ["LR Statistic",      f"{result.llr:.2f}",        "Higher better", "—"],
        ["McFadden Pseudo R²",f"{result.prsquared:.4f}",  "≥ 0.20 good",
         "Very Weak" if result.prsquared < 0.05 else ("Weak" if result.prsquared < 0.10 else "Moderate")],
        ["AUC",               f"{auc:.4f}",               "≥ 0.70 good",
         "Near-Random" if auc < 0.60 else ("Moderate" if auc < 0.70 else "Strong")],
        ["Probability Cutoff",f"{best_cut}",              "Trial & Error", "Chosen"],
        ["Overall Accuracy",  f"{best_acc}%",             "≥ 71.2% (paper benchmark)",
         "✓ Beats Paper" if best_acc >= 71.2 else "✗ Below Paper"],
        ["Sensitivity",       f"{sensitivity*100:.1f}%",  "Higher better", "—"],
        ["Specificity",       f"{specificity*100:.1f}%",  "Higher better", "—"],
    ]
    print(tabulate(fit_rows, headers=["Metric","Value","Threshold","Verdict"], tablefmt="github"))

    print(f"\n── PCA COMPONENT COEFFICIENTS & SIGNIFICANCE ─────────────────")
    conf  = np.array(result.conf_int())
    coef_rows = []
    for i in range(n_comp):
        coef = result.params[i+1]
        p    = result.pvalues[i+1]
        OR   = np.exp(coef)
        ci_lo = np.exp(conf[i+1, 0])
        ci_hi = np.exp(conf[i+1, 1])
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

    print(f"\n── TOP RATIO LOADINGS PER PCA COMPONENT ──────────────────────")
    loadings = pd.DataFrame(pca_final.components_.T, index=kept,
                            columns=[f"PC{i+1}" for i in range(n_comp)])
    for comp_name in loadings.columns:
        top = loadings[comp_name].abs().nlargest(3).index.tolist()
        top_named = [ratio_labels.get(r, r) for r in top]
        print(f"  {comp_name}: {', '.join(top_named)}")

print("\n" + "="*65)
print("  MARKET CAP SEGMENTATION ANALYSIS")
print("  S&P 500 | Q1 2010 – Q4 2024 | WRDS (lanagidan9790)")
print("  Reference: Ananthakumar & Sarkar (2017) — VIF cutoff=2.5, Cutoff by trial & error")
print("="*65)

cap_33 = merged['mkvaltq'].quantile(0.33)
cap_67 = merged['mkvaltq'].quantile(0.67)
print(f"\n── MARKET CAP SEGMENTATION THRESHOLDS ───────────────────────")
seg_rows = [
    ["Small Cap",  f"< ${cap_33/1000:.0f}B",  f"{(merged['market_cap_group']=='Small Cap').sum():,}  obs"],
    ["Mid Cap",    f"${cap_33/1000:.0f}B – ${cap_67/1000:.0f}B", f"{(merged['market_cap_group']=='Mid Cap').sum():,}  obs"],
    ["Large Cap",  f"> ${cap_67/1000:.0f}B",  f"{(merged['market_cap_group']=='Large Cap').sum():,}  obs"],
]
print(tabulate(seg_rows, headers=["Group","Market Cap Range","Observations"], tablefmt="github"))

for group in ['Large Cap', 'Mid Cap', 'Small Cap']:
    subset = merged[merged['market_cap_group'] == group]
    run_group(group, subset)

print("\n" + "="*65)
print("  ANALYSIS COMPLETE")
print("="*65 + "\n")

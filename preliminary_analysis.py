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

comp      = pd.read_csv('wrds_compustat_quarterly.csv', low_memory=False)
crsp      = pd.read_csv('wrds_crsp_quarterly.csv', low_memory=False)
sp500hist = pd.read_csv('wrds_sp500_history.csv', low_memory=False)
macro     = pd.read_csv('wrds_fred_macro.csv', low_memory=False)

sp500hist['start_date'] = pd.to_datetime(sp500hist['start_date'])
sp500hist['end_date']   = pd.to_datetime(sp500hist['end_date'])

comp['datadate'] = pd.to_datetime(comp['datadate'])
comp['quarter']  = pd.PeriodIndex(comp['quarter'], freq='Q')
crsp['quarter']  = pd.PeriodIndex(crsp['quarter_str'], freq='Q')
macro['quarter'] = pd.PeriodIndex(macro['quarter'], freq='Q')

numeric_cols = ['revtq','cogsq','xsgaq','xrdq','oibdpq','oiadpq','niq','ibq',
                'piq','atq','ceqq','teqq','dlttq','dlcq','actq','lctq',
                'cheq','dpq','txtq','prccq','cshoq','mkvaltq']
for c in numeric_cols:
    comp[c] = pd.to_numeric(comp[c], errors='coerce')

comp = comp.sort_values(['gvkey','quarter'])
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

ratio_cols = ['roa','roe','gross_margin','op_margin','net_margin','asset_turnover',
              'current_ratio','debt_to_equity','rev_growth','ni_growth',
              'pe_ratio','book_to_market','gdp_growth','inflation']

ratio_labels = {
    'roa':'Return on Assets (ROA)', 'roe':'Return on Equity (ROE)',
    'gross_margin':'Gross Profit Margin', 'op_margin':'Operating Margin',
    'net_margin':'Net Profit Margin', 'asset_turnover':'Asset Turnover',
    'current_ratio':'Current Ratio', 'debt_to_equity':'Debt-to-Equity',
    'rev_growth':'Revenue Growth (QoQ)',
    'ni_growth':'Net Income Growth (QoQ)', 'pe_ratio':'P/E Ratio',
    'book_to_market':'Book-to-Market',
    'gdp_growth':'GDP Growth (Quarterly)',
    'inflation':'CPI Inflation (Quarterly)',
}

merged = comp.merge(
    crsp[['ticker','quarter','quarterly_return','spy_quarterly_return','outperformer_quarterly']],
    left_on=['tic','quarter'], right_on=['ticker','quarter'], how='inner'
)

all_quarters = pd.period_range('2010Q1', '2024Q4', freq='Q')
constituent_rows = []
for _, row in sp500hist.iterrows():
    for q in all_quarters:
        q_start = q.start_time
        if row['start_date'] <= q_start <= row['end_date']:
            constituent_rows.append({'gvkey': str(row['gvkey']), 'quarter': q})
constituent_panel = pd.DataFrame(constituent_rows)

merged['gvkey'] = merged['gvkey'].astype(str)
merged = merged.merge(constituent_panel, on=['gvkey','quarter'], how='inner').reset_index(drop=True)
merged = merged.merge(macro[['quarter','gdp_growth','inflation']], on='quarter', how='left')

merged = merged.sort_values(['gvkey','quarter']).reset_index(drop=True)
merged['outperformer_next'] = merged.groupby('gvkey')['outperformer_quarterly'].shift(-1)

for col in ratio_cols:
    lo = merged[col].quantile(0.01)
    hi = merged[col].quantile(0.99)
    merged[col] = merged[col].clip(lo, hi)

df = merged[ratio_cols + ['outperformer_next']].dropna()
X  = df[ratio_cols]
y  = df['outperformer_next']

scaler   = StandardScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=ratio_cols)

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

initial_vifs = [variance_inflation_factor(X_scaled.values, i) for i in range(len(ratio_cols))]
kept, removed, final_vif_dict = vif_filter(X_scaled, cutoff=2.5)
X_clean = X_scaled[kept]

pca     = PCA()
pca.fit(X_clean)
exp_var = np.cumsum(pca.explained_variance_ratio_)
n_comp  = int(np.searchsorted(exp_var, 0.80)) + 1
pca_final = PCA(n_components=n_comp)
X_pca   = pca_final.fit_transform(X_clean)

X_const = sm.add_constant(X_pca)
result  = Logit(y.values, X_const).fit(maxiter=200, disp=False)

y_prob  = result.predict(X_const)
auc     = roc_auc_score(y, y_prob)

best_cutoff, best_acc = 0.5, 0
for thresh in np.arange(0.30, 0.75, 0.05):
    preds = (y_prob >= thresh).astype(int)
    acc   = (preds == y.values).mean()
    if acc > best_acc:
        best_acc    = acc
        best_cutoff = thresh
best_cutoff = round(best_cutoff, 2)
best_acc    = round(best_acc * 100, 1)

preds = (y_prob >= best_cutoff).astype(int)
cm    = confusion_matrix(y.values, preds)
tn, fp, fn, tp = cm.ravel() if cm.shape == (2,2) else (0,0,0,len(y))
sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
specificity = tn / (tn + fp) if (tn + fp) > 0 else 0

overall_sig = "✓ SIGNIFICANT" if result.llr_pvalue < 0.05 else "✗ NOT SIGNIFICANT"

print("\n" + "="*65)
print("  PRELIMINARY GLOBAL LOGISTIC REGRESSION — NO SEGMENTATION")
print("  S&P 500 | Q1 2010 – Q4 2024 | WRDS (lanagidan9790)")
print("  Predicting: NEXT quarter outperformance using CURRENT quarter ratios")
print("  Reference: Ananthakumar & Sarkar (2017) — VIF cutoff=2.5, PCA ≥80%")
print("="*65)

print("\n── TABLE 1: SAMPLE OVERVIEW ──────────────────────────────────")
overview = [
    ["Observations",         f"{len(df):,}"],
    ["Outperformers (Y=1)",  f"{int(y.sum()):,}  ({y.mean()*100:.1f}%)"],
    ["Underperformers (Y=0)",f"{int((y==0).sum()):,}  ({(1-y.mean())*100:.1f}%)"],
    ["Date Range",           "Q1 2010 – Q4 2024"],
    ["Prediction Horizon",   "1 quarter ahead (Q[t] ratios → Q[t+1] return)"],
    ["Initial Predictors",   "12 financial ratios + 2 macro variables"],
    ["Predictors after VIF", f"{len(kept)}"],
    ["PCA Components",       f"{n_comp}  (explaining ≥ 80% variance)"],
]
print(tabulate(overview, headers=["Parameter","Value"], tablefmt="github"))

print("\n── TABLE 2: VIF — ALL PREDICTORS (cutoff = 2.5) ─────────────")
removed_vif_dict = dict(removed)
vif_all_rows = []
for var, v_init in zip(ratio_cols, initial_vifs):
    if var in kept:
        v_final = final_vif_dict.get(var, "—")
        status  = "✓ Kept"
        vif_all_rows.append([ratio_labels[var], f"{v_init:.2f}", f"{v_final:.2f}", status])
    else:
        v_at_removal = removed_vif_dict.get(var, "—")
        vif_all_rows.append([ratio_labels[var], f"{v_init:.2f}", "removed", "✗ Removed"])
print(tabulate(vif_all_rows,
    headers=["Predictor","Initial VIF","Final VIF","Decision"], tablefmt="github"))
print(f"  All kept predictors have Final VIF ≤ 2.5  ✓")
print(f"\n  Predictors kept ({len(kept)}): {', '.join([ratio_labels.get(k,k) for k in kept])}")

print("\n── TABLE 3: PCA — EXPLAINED VARIANCE ─────────────────────────")
pca_rows = []
cumvar   = 0
for i, ev in enumerate(pca_final.explained_variance_ratio_):
    cumvar += ev
    pca_rows.append([f"PC{i+1}", f"{ev*100:.1f}%", f"{cumvar*100:.1f}%"])
print(tabulate(pca_rows, headers=["Component","Variance Explained","Cumulative"], tablefmt="github"))
print(f"  → {n_comp} components retained (explaining ≥ 80% of variance)")

print("\n── TABLE 4: OPTIMAL PROBABILITY CUTOFF ───────────────────────")
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
    marker = " ← CHOSEN" if abs(thresh - best_cutoff) < 0.01 else ""
    cutoff_rows.append([f"{thresh:.2f}", f"{acc:.1f}%", f"{sens_t*100:.1f}%", f"{spec_t*100:.1f}%", marker])
print(tabulate(cutoff_rows,
    headers=["Cutoff","Accuracy","Sensitivity","Specificity",""],
    tablefmt="github"))

print("\n── TABLE 5: MODEL FIT & OVERALL SIGNIFICANCE ─────────────────")
fit_rows = [
    ["LR p-value",        f"{result.llr_pvalue:.4f}", "< 0.05",    overall_sig],
    ["LR Statistic",      f"{result.llr:.2f}",        "Higher better", "—"],
    ["McFadden Pseudo R²",f"{result.prsquared:.4f}",  "≥ 0.20 good",
     "Very Weak" if result.prsquared < 0.05 else ("Weak" if result.prsquared < 0.10 else "Moderate")],
    ["AUC",               f"{auc:.4f}",               "≥ 0.70 good",
     "Near-Random" if auc < 0.60 else ("Moderate" if auc < 0.70 else "Strong")],
    ["Probability Cutoff",f"{best_cutoff}",            "Trial & Error", "Chosen"],
    ["Overall Accuracy",  f"{best_acc}%",              "≥ 71.2% (paper benchmark)",
     "✓ Beats Paper" if best_acc >= 71.2 else "✗ Below Paper"],
    ["Sensitivity",       f"{sensitivity*100:.1f}%",  "Higher better", "—"],
    ["Specificity",       f"{specificity*100:.1f}%",  "Higher better", "—"],
]
print(tabulate(fit_rows, headers=["Metric","Value","Threshold","Verdict"], tablefmt="github"))

print("\n── TABLE 6: PCA COMPONENT COEFFICIENTS & SIGNIFICANCE ────────")
conf      = np.array(result.conf_int())
coef_rows = []
for i in range(n_comp):
    coef  = result.params[i+1]
    p     = result.pvalues[i+1]
    OR    = np.exp(coef)
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

print("\n── TABLE 7: TOP RATIO LOADINGS PER PCA COMPONENT ────────────")
loadings = pd.DataFrame(pca_final.components_.T, index=kept,
                        columns=[f"PC{i+1}" for i in range(n_comp)])
for comp_name in loadings.columns:
    top      = loadings[comp_name].abs().nlargest(3).index.tolist()
    top_named = [ratio_labels.get(r, r) for r in top]
    print(f"  {comp_name}: {', '.join(top_named)}")

print("\n── CONCLUSION ────────────────────────────────────────────────")
print(f"  Prediction    : Q[t] ratios → Q[t+1] outperformance (forward-looking)")
print(f"  Overall model : {overall_sig}")
print(f"  AUC           : {auc:.4f}  →  {'barely above random chance (0.50)' if auc < 0.60 else 'moderate discriminatory power'}")
print(f"  Pseudo R²     : {result.prsquared:.4f}  →  <1% of variance explained")
sig_comps = [f"PC{i+1}" for i in range(n_comp) if result.pvalues[i+1] < 0.05]
print(f"  Significant PCA components ({len(sig_comps)}/{n_comp}): {', '.join(sig_comps) if sig_comps else 'None'}")
print("="*65 + "\n")

summary = {
    'N': len(df),
    'Outperformers': int(y.sum()),
    'Outperformer_Rate': round(y.mean()*100, 1),
    'Predictors_After_VIF': len(kept),
    'PCA_Components': n_comp,
    'AUC': round(auc, 4),
    'Accuracy': best_acc,
    'Cutoff': best_cutoff,
    'Sensitivity': round(sensitivity*100, 1),
    'Specificity': round(specificity*100, 1),
    'LR_pvalue': round(result.llr_pvalue, 4),
    'LR_Statistic': round(result.llr, 2),
    'McFadden_R2': round(result.prsquared, 4),
    'Significant': result.llr_pvalue < 0.05,
    'Sig_Components': f"{len(sig_comps)}/{n_comp}",
    'Kept_Predictors': ', '.join([ratio_labels.get(k,k) for k in kept]),
}
pd.DataFrame([summary]).to_csv('results_preliminary.txt', sep='\t', index=False)
print("  Results saved to: results_preliminary.txt")

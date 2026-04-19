import pandas as pd
import numpy as np
import warnings
from tabulate import tabulate
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
from statsmodels.discrete.discrete_model import Logit
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm
warnings.filterwarnings('ignore')

comp = pd.read_csv('wrds_compustat_quarterly.csv', low_memory=False)
crsp = pd.read_csv('wrds_crsp_quarterly.csv', low_memory=False)

comp['datadate'] = pd.to_datetime(comp['datadate'])
comp['quarter'] = pd.PeriodIndex(comp['quarter'], freq='Q')
crsp['quarter'] = pd.PeriodIndex(crsp['quarter_str'], freq='Q')

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
comp['rd_intensity']   = comp['xrdq']   / comp['revtq'].replace(0, np.nan)
comp['rev_growth']     = (comp['revtq'] - comp['lag_revtq']) / comp['lag_revtq'].abs().replace(0, np.nan)
comp['ni_growth']      = (comp['niq']   - comp['lag_niq'])   / comp['lag_niq'].abs().replace(0, np.nan)
comp['pe_ratio']       = comp['prccq']  / (comp['ibq'] / comp['cshoq'].replace(0, np.nan)).replace(0, np.nan)
comp['book_to_market'] = comp['ceqq']   / comp['mkvaltq'].replace(0, np.nan)

ratio_cols = ['roa','roe','gross_margin','op_margin','net_margin','asset_turnover',
              'current_ratio','debt_to_equity','rev_growth','ni_growth',
              'pe_ratio','book_to_market']

merged = comp.merge(
    crsp[['ticker','quarter','quarterly_return','spy_quarterly_return','outperformer_quarterly']],
    left_on=['tic','quarter'], right_on=['ticker','quarter'], how='inner'
)

for col in ratio_cols:
    lo = merged[col].quantile(0.01)
    hi = merged[col].quantile(0.99)
    merged[col] = merged[col].clip(lo, hi)

df = merged[ratio_cols + ['outperformer_quarterly']].dropna()
X  = df[ratio_cols]
y  = df['outperformer_quarterly']

scaler   = StandardScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=ratio_cols)

vif_values = [variance_inflation_factor(X_scaled.values, i) for i in range(len(ratio_cols))]

X_const = sm.add_constant(X_scaled)
result  = Logit(y.values, X_const.values).fit(maxiter=200, disp=False)

auc       = roc_auc_score(y, result.predict(X_const.values))
pseudo_r2 = result.prsquared
lr_stat   = result.llr
lr_pval   = result.llr_pvalue
n_obs     = int(result.nobs)

ratio_labels = {
    'roa':'Return on Assets (ROA)', 'roe':'Return on Equity (ROE)',
    'gross_margin':'Gross Profit Margin', 'op_margin':'Operating Margin',
    'net_margin':'Net Profit Margin', 'asset_turnover':'Asset Turnover',
    'current_ratio':'Current Ratio', 'debt_to_equity':'Debt-to-Equity',
    'rev_growth':'Revenue Growth (QoQ)',
    'ni_growth':'Net Income Growth (QoQ)', 'pe_ratio':'P/E Ratio',
    'book_to_market':'Book-to-Market',
}

print("\n" + "="*65)
print("  PRELIMINARY GLOBAL LOGISTIC REGRESSION — NO SEGMENTATION")
print("  S&P 500 | Q1 2010 – Q4 2024 | WRDS (lanagidan9790)")
print("="*65)

print("\n── TABLE 1: SAMPLE OVERVIEW ──────────────────────────────────")
overview = [
    ["Observations",         f"{n_obs:,}"],
    ["Outperformers (Y=1)",  f"{int(y.sum()):,}  ({y.mean()*100:.1f}%)"],
    ["Underperformers (Y=0)",f"{int((y==0).sum()):,}  ({(1-y.mean())*100:.1f}%)"],
    ["Date Range",           "Q1 2010 – Q4 2024"],
    ["Predictors",           "12 financial ratios"],
]
print(tabulate(overview, headers=["Parameter","Value"], tablefmt="github"))

print("\n── TABLE 2: MODEL FIT & OVERALL SIGNIFICANCE ─────────────────")
overall_sig = "✓ SIGNIFICANT" if lr_pval < 0.05 else "✗ NOT SIGNIFICANT"
fit = [
    ["LR p-value",        f"{lr_pval:.4f}", "< 0.05",   overall_sig],
    ["LR Statistic",      f"{lr_stat:.2f}", "Higher better", "—"],
    ["McFadden Pseudo R²",f"{pseudo_r2:.4f}","≥ 0.20 good",
     "Very Weak" if pseudo_r2 < 0.05 else "Weak"],
    ["AUC",               f"{auc:.4f}",    "≥ 0.70 good",
     "Near-Random" if auc < 0.60 else "Moderate"],
]
print(tabulate(fit, headers=["Metric","Value","Threshold","Verdict"], tablefmt="github"))

print("\n── TABLE 3: VIF — MULTICOLLINEARITY CHECK ────────────────────")
vif_rows = []
for var, v in zip(ratio_cols, vif_values):
    flag = "✓ OK" if v < 5 else ("⚠ Moderate" if v < 10 else "✗ High")
    vif_rows.append([ratio_labels[var], f"{v:.2f}", flag])
print(tabulate(vif_rows, headers=["Predictor","VIF","Assessment"], tablefmt="github"))

print("\n── TABLE 4: COEFFICIENTS, ODDS RATIOS & p-VALUES ────────────")
conf = np.array(result.conf_int())
coef_rows = []
for i, var in enumerate(ratio_cols):
    coef = result.params[i+1]
    se   = result.bse[i+1]
    z    = result.tvalues[i+1]
    p    = result.pvalues[i+1]
    OR   = np.exp(coef)
    ci_lo = np.exp(conf[i+1, 0])
    ci_hi = np.exp(conf[i+1, 1])
    if p < 0.01:   sig = "*** p<0.01"
    elif p < 0.05: sig = "**  p<0.05"
    elif p < 0.10: sig = "*   p<0.10"
    else:          sig = "No"
    coef_rows.append([
        ratio_labels[var], f"{coef:+.4f}", f"{OR:.4f}",
        f"[{ci_lo:.3f}, {ci_hi:.3f}]", f"{z:.3f}", f"{p:.4f}", sig
    ])
print(tabulate(coef_rows,
    headers=["Predictor","Coeff","Odds Ratio","95% CI","Z-Stat","p-Value","Significant?"],
    tablefmt="github"))

print("\n── TABLE 5: ODDS RATIO INTERPRETATION ───────────────────────")
print("  Odds Ratio > 1 → predictor increases probability of outperforming")
print("  Odds Ratio < 1 → predictor decreases probability of outperforming")
print("  Odds Ratio = 1 → no effect\n")
or_interp = []
for i, var in enumerate(ratio_cols):
    coef = result.params[i+1]
    p    = result.pvalues[i+1]
    OR   = np.exp(coef)
    if p >= 0.05:
        direction = "No significant effect"
    elif OR > 1:
        direction = f"↑ {(OR-1)*100:.1f}% higher odds of outperforming"
    else:
        direction = f"↓ {(1-OR)*100:.1f}% lower odds of outperforming"
    or_interp.append([ratio_labels[var], f"{OR:.4f}", f"{p:.4f}", direction])
print(tabulate(or_interp,
    headers=["Predictor","Odds Ratio","p-Value","Interpretation"],
    tablefmt="github"))

print("\n── CONCLUSION ────────────────────────────────────────────────")
print(f"  Overall model : {overall_sig}")
print(f"  AUC           : {auc:.4f}  →  barely above random chance (0.50)")
print(f"  Pseudo R²     : {pseudo_r2:.4f}  →  <1% of variance explained")
sig_vars = [ratio_labels[ratio_cols[i]] for i in range(len(ratio_cols)) if result.pvalues[i+1] < 0.05]
print(f"  Significant predictors ({len(sig_vars)}/12): {', '.join(sig_vars)}")
print("="*65 + "\n")

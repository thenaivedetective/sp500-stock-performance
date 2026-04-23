import pandas as pd
import numpy as np
import warnings
import sys
from tabulate import tabulate
from sklearn.metrics import roc_auc_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
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

sys.stdout = Tee('results_validation_global.txt')

print("=" * 70)
print("  CONFIGURATION 0: GLOBAL POOLED MODEL — OUT-OF-SAMPLE VALIDATION")
print("  All S&P 500 companies, no segmentation")
print("  Training  : Q1 2010 – Q3 2024  (WRDS Compustat + CRSP)")
print("  Test Qtrs : Q1 2025, Q2 2025, Q3 2025, Q4 2025  (WRDS 2025)")
print("  Labels    : Q2–Q4 2025 + Q1 2026 outperformance  (WRDS CRSP 2025)")
print("  Forward-looking: Q[t] ratios → Q[t+1] outperformance (shift=-1)")
print("  Reference: Ananthakumar & Sarkar (2017) — benchmark 71.2% accuracy")
print("=" * 70)

print("\n[1/4] Loading WRDS training data (Q1 2010 – Q3 2024)...")
comp      = pd.read_csv('wrds_compustat_quarterly.csv', low_memory=False)
crsp      = pd.read_csv('wrds_crsp_quarterly.csv', low_memory=False)
macro     = pd.read_csv('wrds_fred_macro.csv', low_memory=False)
sp500hist = pd.read_csv('wrds_sp500_history.csv', low_memory=False)

sp500hist['start_date'] = pd.to_datetime(sp500hist['start_date'])
sp500hist['end_date']   = pd.to_datetime(sp500hist['end_date'])
comp['datadate']        = pd.to_datetime(comp['datadate'])
comp['cal_quarter']     = comp['datadate'].dt.to_period('Q')
crsp['quarter']         = pd.PeriodIndex(crsp['quarter_str'], freq='Q')
macro['quarter']        = pd.PeriodIndex(macro['quarter'], freq='Q')

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
print(f"  Training rows : {len(train_df):,}  (Q1 2010 – Q3 2024)")

print("\n[2/4] Loading WRDS 2025 data and computing test features...")
comp_2025_raw = pd.read_csv('wrds_compustat_quarterly_2025.csv', low_memory=False)
crsp_2025     = pd.read_csv('wrds_crsp_quarterly_2025.csv', low_memory=False)

comp_2025_raw['datadate'] = pd.to_datetime(comp_2025_raw['datadate'])
comp_2025_raw['gvkey']    = comp_2025_raw['gvkey'].astype(str)
crsp_2025['gvkey']        = crsp_2025['gvkey'].astype(str)

stack_cols = ['gvkey','tic','datadate','revtq','cogsq','oiadpq','niq','ibq',
              'atq','ceqq','dlttq','dlcq','actq','lctq','cheq','dpq','txtq',
              'prccq','cshoq','mkvaltq']

old_tail = comp[
    (comp['datadate'] >= pd.Timestamp('2024-07-01')) &
    (comp['datadate'] < pd.Timestamp('2025-01-01'))
][stack_cols].copy()
new_part  = comp_2025_raw[stack_cols].copy()
combined  = pd.concat([old_tail, new_part], ignore_index=True)
combined['datadate'] = pd.to_datetime(combined['datadate'])
combined  = combined.sort_values(['gvkey','datadate']).reset_index(drop=True)

for c in stack_cols[3:]:
    combined[c] = pd.to_numeric(combined[c], errors='coerce')

combined['lag_revtq'] = combined.groupby('gvkey')['revtq'].shift(1)
combined['lag_niq']   = combined.groupby('gvkey')['niq'].shift(1)

combined['roa']            = combined['niq']    / combined['atq'].replace(0, np.nan)
combined['roe']            = combined['niq']    / combined['ceqq'].replace(0, np.nan)
combined['gross_margin']   = (combined['revtq'] - combined['cogsq']) / combined['revtq'].replace(0, np.nan)
combined['op_margin']      = combined['oiadpq'] / combined['revtq'].replace(0, np.nan)
combined['net_margin']     = combined['niq']    / combined['revtq'].replace(0, np.nan)
combined['asset_turnover'] = combined['revtq']  / combined['atq'].replace(0, np.nan)
combined['current_ratio']  = combined['actq']   / combined['lctq'].replace(0, np.nan)
combined['debt_to_equity'] = combined['dlttq']  / combined['ceqq'].replace(0, np.nan)
combined['rev_growth']     = (combined['revtq'] - combined['lag_revtq']) / combined['lag_revtq'].abs().replace(0, np.nan)
combined['ni_growth']      = (combined['niq']   - combined['lag_niq'])   / combined['lag_niq'].abs().replace(0, np.nan)
combined['pe_ratio']       = combined['prccq']  / (combined['ibq'] / combined['cshoq'].replace(0, np.nan)).replace(0, np.nan)
combined['book_to_market'] = combined['ceqq']   / combined['mkvaltq'].replace(0, np.nan)

for col in delta_base:
    combined[f'delta_{col}'] = combined.groupby('gvkey')[col].diff()

combined['cal_quarter'] = combined['datadate'].dt.to_period('Q')
comp_2025_features = combined[combined['datadate'] >= pd.Timestamp('2025-01-01')].copy()

print(f"  2025 Compustat rows : {len(comp_2025_features):,}")
print(f"  2025 CRSP rows      : {len(crsp_2025):,}")

spy_by_label = {}
for cq in [1, 2, 3, 4]:
    sub = crsp_2025[crsp_2025['cal_qtr'] == cq]
    if len(sub) > 0:
        spy_by_label[cq] = float(sub['following_sp500_q_return'].iloc[0])

label_qtr_names = {1: 'Q2 2025', 2: 'Q3 2025', 3: 'Q4 2025', 4: 'Q1 2026'}
print(f"\n  SPY return per label quarter:")
for cq, name in label_qtr_names.items():
    sub  = crsp_2025[crsp_2025['cal_qtr'] == cq]
    rate = sub['Outperform'].mean() * 100 if len(sub) > 0 else 0
    print(f"    {name}: SPY {spy_by_label.get(cq,0)*100:+.2f}%  |  N={len(sub)}  |  outperform rate={rate:.1f}%")

print("\n[3/4] Setting macro values for 2025 quarters...")
try:
    import pandas_datareader.data as web
    from datetime import datetime
    gdp_raw = web.DataReader('GDP', 'fred', datetime(2024, 7, 1), datetime(2025, 12, 31))
    cpi_raw = web.DataReader('CPIAUCSL', 'fred', datetime(2024, 9, 1), datetime(2025, 12, 31))
    def get_gdp(qe_m, qe_y, qs_m, qs_y):
        try:
            ev = float(gdp_raw.loc[f'{qe_y}-{qe_m:02d}':].iloc[0])
            sv = float(gdp_raw.loc[f'{qs_y}-{qs_m:02d}':].iloc[0])
            return (ev - sv) / sv if sv != 0 else 0.005
        except Exception:
            return None
    def get_cpi(em, ey, sm2, sy):
        try:
            ev = float(cpi_raw.loc[f'{ey}-{em:02d}':].iloc[0])
            sv = float(cpi_raw.loc[f'{sy}-{sm2:02d}':].iloc[0])
            return (ev - sv) / sv if sv != 0 else 0.006
        except Exception:
            return None
    gdp_q1 = get_gdp(3,2025,12,2024) or 0.0148
    gdp_q2 = get_gdp(6,2025,3,2025)  or 0.0201
    gdp_q3 = get_gdp(9,2025,6,2025)  or 0.0104
    gdp_q4 = get_gdp(12,2025,9,2025) or 0.0060
    inf_q1 = get_cpi(3,2025,12,2024) or 0.0069
    inf_q2 = get_cpi(6,2025,3,2025)  or 0.0052
    inf_q3 = get_cpi(9,2025,6,2025)  or 0.0087
    inf_q4 = get_cpi(12,2025,9,2025) or 0.0055
except Exception:
    gdp_q1, gdp_q2, gdp_q3, gdp_q4 = 0.0148, 0.0201, 0.0104, 0.0060
    inf_q1, inf_q2, inf_q3, inf_q4  = 0.0069, 0.0052, 0.0087, 0.0055

macro_2025 = {
    pd.Period('2025Q1','Q'): {'gdp_growth': gdp_q1, 'inflation': inf_q1},
    pd.Period('2025Q2','Q'): {'gdp_growth': gdp_q2, 'inflation': inf_q2},
    pd.Period('2025Q3','Q'): {'gdp_growth': gdp_q3, 'inflation': inf_q3},
    pd.Period('2025Q4','Q'): {'gdp_growth': gdp_q4, 'inflation': inf_q4},
}
for qp, vals in macro_2025.items():
    print(f"  {qp}: GDP growth={vals['gdp_growth']:.4f}  CPI inflation={vals['inflation']:.4f}")

print("\n[4/4] Fitting preprocessing on training data and running global validation...")

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

def vif_filter(X_df, cutoff=2.5):
    remaining = list(X_df.columns)
    while True:
        vifs    = [variance_inflation_factor(X_df[remaining].values, i)
                   for i in range(len(remaining))]
        max_vif = max(vifs)
        if max_vif <= cutoff:
            break
        worst = remaining[vifs.index(max_vif)]
        remaining.remove(worst)
    return remaining

quarter_configs = [
    (pd.Period('2025Q1','Q'), 1, 'Q1 2025 Features → Q2 2025 Labels'),
    (pd.Period('2025Q2','Q'), 2, 'Q2 2025 Features → Q3 2025 Labels'),
    (pd.Period('2025Q3','Q'), 3, 'Q3 2025 Features → Q4 2025 Labels'),
    (pd.Period('2025Q4','Q'), 4, 'Q4 2025 Features → Q1 2026 Labels'),
]

all_results = []

for feat_qtr, label_cq, qtr_label in quarter_configs:
    spy_ret   = spy_by_label.get(label_cq, 0.0)
    macro_val = macro_2025.get(feat_qtr, {'gdp_growth': 0.005, 'inflation': 0.005})

    crsp_sub = crsp_2025[crsp_2025['cal_qtr'] == label_cq][['gvkey','Outperform']].copy()
    crsp_sub.columns = ['gvkey','outperformer_next']
    crsp_sub['gvkey'] = crsp_sub['gvkey'].astype(str)

    feat_sub = comp_2025_features[comp_2025_features['cal_quarter'] == feat_qtr].copy()
    feat_sub['gvkey']      = feat_sub['gvkey'].astype(str)
    feat_sub['gdp_growth'] = macro_val['gdp_growth']
    feat_sub['inflation']  = macro_val['inflation']

    for col in ratio_cols:
        if col in feat_sub.columns:
            lo, hi = winsor_bounds.get(col, (feat_sub[col].quantile(0.01), feat_sub[col].quantile(0.99)))
            feat_sub[col] = feat_sub[col].clip(lo, hi).fillna(train_medians.get(col, 0))

    test_merged = feat_sub.merge(crsp_sub, on='gvkey', how='inner')

    available  = [c for c in ratio_cols if c in train_df.columns and c in test_merged.columns]
    train_sub  = train_df[available + ['outperformer_next']].dropna()
    test_sub   = test_merged[available + ['outperformer_next']].dropna()

    if len(train_sub) < 100 or len(test_sub) < 5:
        continue
    if train_sub['outperformer_next'].nunique() < 2 or test_sub['outperformer_next'].nunique() < 2:
        continue

    X_tr = train_sub[available]
    y_tr = train_sub['outperformer_next']
    X_te = test_sub[available]
    y_te = test_sub['outperformer_next']

    scaler    = StandardScaler().fit(X_tr)
    X_tr_sc   = pd.DataFrame(scaler.transform(X_tr), columns=available)
    X_te_sc   = pd.DataFrame(scaler.transform(X_te), columns=available)

    kept      = vif_filter(X_tr_sc, cutoff=2.5)
    X_tr_vif  = X_tr_sc[kept]
    X_te_vif  = X_te_sc[kept]

    pca_tmp   = PCA().fit(X_tr_vif)
    exp_var   = np.cumsum(pca_tmp.explained_variance_ratio_)
    n_comp    = min(int(np.searchsorted(exp_var, 0.80)) + 1, len(kept))

    pca_final = PCA(n_components=n_comp).fit(X_tr_vif)
    X_tr_pca  = pca_final.transform(X_tr_vif)
    X_te_pca  = pca_final.transform(X_te_vif)

    model = Logit(y_tr.values, sm.add_constant(X_tr_pca)).fit(maxiter=200, disp=False)

    best_cut, best_acc_tr = 0.5, 0
    for thresh in np.arange(0.30, 0.75, 0.05):
        preds_tr = (model.predict(sm.add_constant(X_tr_pca)) >= thresh).astype(int)
        acc_tr   = (preds_tr == y_tr.values).mean()
        if acc_tr > best_acc_tr:
            best_acc_tr, best_cut = acc_tr, thresh

    train_auc = roc_auc_score(y_tr, model.predict(sm.add_constant(X_tr_pca)))
    y_te_prob = model.predict(sm.add_constant(X_te_pca))
    test_auc  = roc_auc_score(y_te, y_te_prob)
    preds_te  = (y_te_prob >= best_cut).astype(int)
    test_acc  = round((preds_te == y_te.values).mean() * 100, 1)
    auc_delta = round(test_auc - train_auc, 4)

    cm = confusion_matrix(y_te.values, preds_te)
    tn, fp, fn, tp = cm.ravel() if cm.shape == (2,2) else (0, 0, 0, len(y_te))
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    precision   = tp / (tp + fp) if (tp + fp) > 0 else 0

    holds_up  = auc_delta >= -0.02
    beats_ppr = test_acc >= 71.2
    sig_comps = sum(1 for i in range(n_comp) if model.pvalues[i+1] < 0.05)
    lr_sig    = model.llr_pvalue < 0.05

    print()
    print("=" * 70)
    print(f"  TEST QUARTER: {qtr_label}")
    print(f"  Test N={len(y_te)} | Outperformers={int(y_te.sum())}/{len(y_te)} ({y_te.mean()*100:.1f}%) | SPY {spy_ret*100:+.2f}%")
    print("=" * 70)
    print()
    print("── CONFIGURATION 0: GLOBAL POOLED MODEL (all companies, no segmentation)")
    print()
    print("=" * 70)
    print(f"  GLOBAL MODEL  [All S&P 500 Companies]")
    print(f"  Features: {feat_qtr} | Labels: {label_qtr_names[label_cq]} | SPY = {spy_ret*100:+.2f}%")
    print(f"  Train N={len(y_tr):,} | Test N={len(y_te)} | Test Outperformers={y_te.mean()*100:.1f}%")
    print("=" * 70)
    print()
    print("── VALIDATION METRICS ────────────────────────────────────────────")
    metrics = [
        ["Train AUC",     f"{train_auc:.4f}",  "In-sample",          "—"],
        ["Test AUC",      f"{test_auc:.4f}",   "Out-of-sample",
         "Strong" if test_auc >= 0.70 else ("Moderate" if test_auc >= 0.60 else "Weak")],
        ["AUC Change",    f"{auc_delta:+.4f}", "≥ -0.02 = holds up",
         "HOLDS UP" if holds_up else "DEGRADES"],
        ["Test Accuracy", f"{test_acc}%",       "≥ 71.2% paper",
         "✓ Beats Paper" if beats_ppr else "✗ Below Paper"],
        ["Sensitivity",   f"{sensitivity*100:.1f}%", "Higher better", "—"],
        ["Specificity",   f"{specificity*100:.1f}%", "Higher better", "—"],
        ["Precision",     f"{precision*100:.1f}%",   "Higher better", "—"],
        ["LR p-value",    f"{model.llr_pvalue:.4f}", "< 0.05",
         "SIGNIFICANT" if lr_sig else "NOT SIGNIFICANT"],
        ["McFadden R²",   f"{model.prsquared:.4f}",  "Train fit",      "—"],
        ["PCA Comps",     str(n_comp),                "≥80% variance",  "—"],
        ["VIF Kept",      f"{len(kept)}/{len(available)}", "≤2.5 cutoff", "—"],
        ["Cutoff",        f"{best_cut:.2f}",          "Optimised on train", "—"],
        ["Sig Comps",     f"{sig_comps}/{n_comp}",    "p<0.05",         "—"],
    ]
    print(tabulate(metrics, headers=["Metric","Value","Threshold","Verdict"], tablefmt="github"))

    print()
    print("── CONFUSION MATRIX (Test Set) ───────────────────────────────────")
    print(f"  Cutoff = {best_cut:.2f} | SPY {label_qtr_names[label_cq]} = {spy_ret*100:+.2f}%")
    print()
    print(f"  {'':30s}  Predicted: Under (0)   Predicted: Over (1)")
    print(f"  {'Actual: Underperformer (0)':30s}  TN={tn:<10}       FP={fp}")
    print(f"  {'Actual: Outperformer  (1)':30s}  FN={fn:<10}       TP={tp}")
    print()
    print(f"  Sensitivity (Recall) : {sensitivity*100:.1f}%  — of true outperformers, correctly called")
    print(f"  Specificity          : {specificity*100:.1f}%  — of true underperformers, correctly called")
    print(f"  Precision            : {precision*100:.1f}%  — of predicted outperformers, truly so")

    print()
    print("── PCA COMPONENT COEFFICIENTS (fitted on training data) ──────────")
    coef_rows = []
    for i in range(n_comp):
        coef  = model.params[i+1]
        pval  = model.pvalues[i+1]
        OR    = np.exp(coef)
        ci    = np.array(model.conf_int())
        ci_lo = np.exp(ci[i+1, 0])
        ci_hi = np.exp(ci[i+1, 1])
        zstat = model.tvalues[i+1]
        if pval < 0.01:   sig = "*** p<0.01"
        elif pval < 0.05: sig = "**  p<0.05"
        elif pval < 0.10: sig = "*   p<0.10"
        else:             sig = "No"
        coef_rows.append([f"PC{i+1}", f"{coef:+.4f}", f"{OR:.4f}",
                          f"[{ci_lo:.3f},{ci_hi:.3f}]",
                          f"{zstat:.3f}", f"{pval:.4f}", sig])
    print(tabulate(coef_rows,
        headers=["Component","Coeff","Odds Ratio","95% CI","Z-Stat","p-Value","Significant?"],
        tablefmt="github"))

    print()
    print("── PCA LOADINGS (Top contributor per component) ──────────────────")
    loadings_df = pd.DataFrame(pca_final.components_.T, index=kept,
                               columns=[f"PC{i+1}" for i in range(n_comp)])
    for pc in loadings_df.columns:
        top3 = loadings_df[pc].abs().nlargest(3).index.tolist()
        top3_str = ', '.join([f"{ratio_labels.get(f,f)} ({loadings_df.loc[f,pc]:+.3f})" for f in top3])
        print(f"  {pc}: {top3_str}")

    all_results.append({
        'Quarter'       : qtr_label,
        'SPY_Return'    : f"{spy_ret*100:+.2f}%",
        'Train_N'       : len(y_tr),
        'Test_N'        : len(y_te),
        'Outperf_Rate'  : f"{y_te.mean()*100:.1f}%",
        'Train_AUC'     : round(train_auc, 4),
        'Test_AUC'      : round(test_auc, 4),
        'AUC_Change'    : f"{auc_delta:+.4f}",
        'Holds_Up'      : 'YES' if holds_up else 'NO',
        'Test_Accuracy' : f"{test_acc}%",
        'Beats_Paper'   : 'YES' if beats_ppr else 'NO',
        'Sensitivity'   : f"{sensitivity*100:.1f}%",
        'Specificity'   : f"{specificity*100:.1f}%",
        'Precision'     : f"{precision*100:.1f}%",
        'LR_pvalue'     : round(model.llr_pvalue, 4),
        'LR_Sig'        : 'YES' if lr_sig else 'NO',
        'McFadden_R2'   : round(model.prsquared, 4),
        'PCA_Comps'     : n_comp,
        'VIF_Kept'      : f"{len(kept)}/{len(available)}",
        'Sig_Comps'     : f"{sig_comps}/{n_comp}",
        'Cutoff'        : best_cut,
        'TN'            : tn, 'FP': fp, 'FN': fn, 'TP': tp,
    })

print()
print("=" * 70)
print("  CONFIGURATION 0: GLOBAL MODEL — SUMMARY ACROSS ALL TEST QUARTERS")
print("=" * 70)

holds_count   = sum(1 for r in all_results if r['Holds_Up'] == 'YES')
beats_count   = sum(1 for r in all_results if r['Beats_Paper'] == 'YES')
sig_count     = sum(1 for r in all_results if r['LR_Sig'] == 'YES')
avg_test_auc  = np.mean([r['Test_AUC'] for r in all_results])
avg_train_auc = np.mean([r['Train_AUC'] for r in all_results])

summary_rows = [
    ["Total quarters tested",           str(len(all_results))],
    ["AUC holds up (ΔAUC ≥ -0.02)",     f"{holds_count}/{len(all_results)}"],
    ["Beats paper benchmark (≥ 71.2%)", f"{beats_count}/{len(all_results)}"],
    ["LR significant (p < 0.05)",       f"{sig_count}/{len(all_results)}"],
    ["Average Train AUC",               f"{avg_train_auc:.4f}"],
    ["Average Test AUC",                f"{avg_test_auc:.4f}"],
    ["Average AUC Change",              f"{avg_test_auc - avg_train_auc:+.4f}"],
]
print(tabulate(summary_rows, headers=["Metric","Value"], tablefmt="github"))

print()
print("── PER-QUARTER BREAKDOWN ─────────────────────────────────────────")
breakdown_rows = []
for r in all_results:
    breakdown_rows.append([
        r['Quarter'], r['SPY_Return'], r['Test_N'],
        r['Train_AUC'], r['Test_AUC'], r['AUC_Change'],
        r['Holds_Up'], r['Test_Accuracy'], r['Beats_Paper'],
        r['LR_Sig']
    ])
print(tabulate(breakdown_rows,
    headers=["Quarter","SPY","N","Train AUC","Test AUC","ΔAUC","Holds Up","Accuracy","Beats Paper","LR Sig"],
    tablefmt="github"))

print()
print("── CONFUSION MATRIX SUMMARY ──────────────────────────────────────")
cm_rows = []
for r in all_results:
    cm_rows.append([
        r['Quarter'], r['Test_N'],
        r['TN'], r['FP'], r['FN'], r['TP'],
        r['Sensitivity'], r['Specificity'], r['Precision'], r['Test_Accuracy']
    ])
print(tabulate(cm_rows,
    headers=["Quarter","N","TN","FP","FN","TP","Sensitivity","Specificity","Precision","Accuracy"],
    tablefmt="github"))

print()
print("── SIGNIFICANCE ASSESSMENT ───────────────────────────────────────")
print(f"  Quarters where LR model is statistically significant : {sig_count}/{len(all_results)}")
print(f"  Quarters where AUC holds up out-of-sample            : {holds_count}/{len(all_results)}")
print(f"  Quarters where accuracy beats 71.2% benchmark        : {beats_count}/{len(all_results)}")
print()
if avg_test_auc >= 0.60:
    auc_verdict = "MODERATE discriminative ability"
elif avg_test_auc >= 0.55:
    auc_verdict = "WEAK but above-random discriminative ability"
else:
    auc_verdict = "NEAR-RANDOM — model does not discriminate well globally"
print(f"  Global model average test AUC = {avg_test_auc:.4f} → {auc_verdict}")
print()
print("=" * 70)
print("  Results saved to: results_validation_global.txt")
print("=" * 70)

sys.stdout.log.close()
sys.stdout = sys.stdout.terminal
print("Done. Results saved to results_validation_global.txt")

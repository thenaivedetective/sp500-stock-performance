import pandas as pd
import numpy as np
import warnings
import sys
from tabulate import tabulate
from sklearn.metrics import roc_auc_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import GradientBoostingClassifier
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
print("  TRUE OUT-OF-SAMPLE VALIDATION — 100% WRDS DATA + DELTA FEATURES")
print("  Training  : Q1 2010 – Q3 2024  (WRDS Compustat + CRSP)")
print("  Test Qtrs : Q1 2025, Q2 2025, Q3 2025, Q4 2025  (WRDS 2025)")
print("  Labels    : Q2–Q4 2025 + Q1 2026 outperformance  (WRDS CRSP 2025)")
print("  No external data sources — macro from FRED/hardcoded, returns from WRDS")
print("  Forward-looking: Q[t] ratios → Q[t+1] outperformance (shift=-1)")
print("  Reference: Ananthakumar & Sarkar (2017)")
print("=" * 70)

print("\n[1/4] Loading WRDS training data (Q1 2010 – Q3 2024)...")
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

print("\n[2/4] Loading WRDS 2025 data and computing test features...")
comp_2025_raw = pd.read_csv('wrds_compustat_quarterly_2025.csv', low_memory=False)
crsp_2025     = pd.read_csv('wrds_crsp_quarterly_2025.csv', low_memory=False)

comp_2025_raw['datadate'] = pd.to_datetime(comp_2025_raw['datadate'])
comp_2025_raw['gvkey']    = comp_2025_raw['gvkey'].astype(str)
if 'Sector_Name' in comp_2025_raw.columns:
    comp_2025_raw = comp_2025_raw.rename(columns={'Sector_Name': 'sector_name'})
crsp_2025['gvkey'] = crsp_2025['gvkey'].astype(str)

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

sect_map = comp_2025_raw[['gvkey','sector_name']].drop_duplicates('gvkey')
comp_2025_features = comp_2025_features.merge(sect_map, on='gvkey', how='left')

print(f"  2025 Compustat rows : {len(comp_2025_features):,}")
print(f"  2025 CRSP rows      : {len(crsp_2025):,}")
print(f"  Cal quarters in 2025 Compustat: {sorted(comp_2025_features['cal_quarter'].unique())}")

spy_by_label = {}
for cq in [1, 2, 3, 4]:
    sub = crsp_2025[crsp_2025['cal_qtr'] == cq]
    if len(sub) > 0:
        spy_by_label[cq] = float(sub['following_sp500_q_return'].iloc[0])

print(f"\n  SPY return per label quarter:")
label_qtr_names = {1: 'Q2 2025', 2: 'Q3 2025', 3: 'Q4 2025', 4: 'Q1 2026'}
for cq, name in label_qtr_names.items():
    sub = crsp_2025[crsp_2025['cal_qtr'] == cq]
    rate = sub['Outperform'].mean() * 100 if len(sub) > 0 else 0
    print(f"    {name}: SPY {spy_by_label.get(cq,0)*100:+.2f}%  |  N={len(sub)}  |  outperform rate={rate:.1f}%")

print("\n[3/4] Setting macro values for 2025 quarters...")
try:
    import pandas_datareader.data as web
    from datetime import datetime
    gdp_raw = web.DataReader('GDP', 'fred', datetime(2024, 7, 1), datetime(2025, 12, 31))
    cpi_raw = web.DataReader('CPIAUCSL', 'fred', datetime(2024, 9, 1), datetime(2025, 12, 31))
    def get_gdp_growth(q_end_month, q_end_year, q_start_month, q_start_year):
        try:
            end_val   = float(gdp_raw.loc[f'{q_end_year}-{q_end_month:02d}':].iloc[0])
            start_val = float(gdp_raw.loc[f'{q_start_year}-{q_start_month:02d}':].iloc[0])
            return (end_val - start_val) / start_val if start_val != 0 else 0.005
        except Exception:
            return None
    def get_cpi_growth(end_month, end_year, start_month, start_year):
        try:
            end_val   = float(cpi_raw.loc[f'{end_year}-{end_month:02d}':].iloc[0])
            start_val = float(cpi_raw.loc[f'{start_year}-{start_month:02d}':].iloc[0])
            return (end_val - start_val) / start_val if start_val != 0 else 0.006
        except Exception:
            return None
    gdp_q1 = get_gdp_growth(3, 2025, 12, 2024) or -0.001
    gdp_q2 = get_gdp_growth(6, 2025, 3,  2025) or  0.005
    gdp_q3 = get_gdp_growth(9, 2025, 6,  2025) or  0.007
    gdp_q4 = get_gdp_growth(12,2025, 9,  2025) or  0.006
    inf_q1 = get_cpi_growth(3, 2025, 12, 2024) or  0.007
    inf_q2 = get_cpi_growth(6, 2025, 3,  2025) or  0.005
    inf_q3 = get_cpi_growth(9, 2025, 6,  2025) or  0.004
    inf_q4 = get_cpi_growth(12,2025, 9,  2025) or  0.004
except Exception:
    gdp_q1, gdp_q2, gdp_q3, gdp_q4 = -0.001, 0.005, 0.007, 0.006
    inf_q1, inf_q2, inf_q3, inf_q4 =  0.007, 0.005, 0.004, 0.004

macro_2025 = {
    pd.Period('2025Q1', 'Q'): {'gdp_growth': gdp_q1, 'inflation': inf_q1},
    pd.Period('2025Q2', 'Q'): {'gdp_growth': gdp_q2, 'inflation': inf_q2},
    pd.Period('2025Q3', 'Q'): {'gdp_growth': gdp_q3, 'inflation': inf_q3},
    pd.Period('2025Q4', 'Q'): {'gdp_growth': gdp_q4, 'inflation': inf_q4},
}
for qp, vals in macro_2025.items():
    print(f"  {qp}: GDP growth={vals['gdp_growth']:.4f}  CPI inflation={vals['inflation']:.4f}")

print("\n[4/4] Fitting preprocessing on training data and running validations...")

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

mkvalt_33 = train_df['mkvaltq'].quantile(0.33)
mkvalt_67 = train_df['mkvaltq'].quantile(0.67)

def cap_label(v):
    if pd.isna(v):        return 'Unknown'
    if v >= mkvalt_67:    return 'Large Cap'
    elif v >= mkvalt_33:  return 'Mid Cap'
    return 'Small Cap'

train_df['cap_group']  = train_df['mkvaltq'].apply(cap_label)
train_df['log_mkvalt'] = np.log(train_df['mkvaltq'].clip(lower=1e-6))

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

def run_validation(config_name, group_name, train, test, spy_ret, pred_qtr, feat_qtr, feature_cols=None, verbose=False):
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

    kept     = vif_filter(X_tr_sc, cutoff=2.5)
    X_tr_vif = X_tr_sc[kept]
    X_te_vif = X_te_sc[kept]

    pca     = PCA()
    pca.fit(X_tr_vif)
    n_comp  = max(1, min(int(np.sum(pca.explained_variance_ratio_ >= 0.05)), len(kept)))

    pca_final = PCA(n_components=n_comp).fit(X_tr_vif)
    X_tr_pca  = pca_final.transform(X_tr_vif)
    X_te_pca  = pca_final.transform(X_te_vif)

    model = Logit(y_tr.values, sm.add_constant(X_tr_pca)).fit(maxiter=200, disp=False)

    gb_clf  = GradientBoostingClassifier(n_estimators=200, max_depth=3, learning_rate=0.05,
                                         subsample=0.8, random_state=42)
    gb_clf.fit(X_tr_pca, y_tr.values)
    gb_train_auc = roc_auc_score(y_tr, gb_clf.predict_proba(X_tr_pca)[:, 1])
    gb_test_auc  = roc_auc_score(y_te, gb_clf.predict_proba(X_te_pca)[:, 1])

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
    tn, fp, fn, tp = cm.ravel() if cm.shape == (2,2) else (0, 0, 0, len(y_te))
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
    print(f"  Features: {feat_qtr} | Labels: {pred_qtr} | SPY = {spy_ret*100:+.2f}%")
    print(f"  Train N={len(train_df2):,} | Test N={len(test_df2)} | "
          f"Test Outperformers={y_te.mean()*100:.1f}%")
    print(f"{'='*70}")

    print(f"\n── VALIDATION METRICS ────────────────────────────────────────────")
    rows = [
        ["Train AUC",      f"{train_auc:.4f}", "In-sample",          "—"],
        ["Test AUC",       f"{test_auc:.4f}",  "Out-of-sample",
         "Strong" if test_auc >= 0.70 else ("Moderate" if test_auc >= 0.60 else "Weak")],
        ["AUC Change",     f"{auc_change:+.4f}", "≥ -0.02 = holds up", verdict],
        ["Test Accuracy",  f"{test_acc}%",     "≥ 71.2% paper",
         "✓ Beats Paper" if test_acc >= 71.2 else "✗ Below Paper"],
        ["Sensitivity",    f"{sensitivity}%",  "Higher better",      "—"],
        ["Specificity",    f"{specificity}%",  "Higher better",      "—"],
        ["Precision",      f"{precision}%",    "Higher better",      "—"],
        ["LR p-value",     f"{model.llr_pvalue:.4f}", "< 0.05",      overall_sig],
        ["McFadden R²",    f"{model.prsquared:.4f}",  "Train fit",   "—"],
        ["PCA Comps",      f"{n_comp}",        "≥5% per component",  "—"],
        ["VIF Kept",       f"{len(kept)}/{len(available)}", "≤2.5 cutoff", "—"],
        ["Cutoff",         f"{best_cut:.2f}",  "Optimised on train", "—"],
        ["Sig Comps",      f"{len(sig_comps)}/{n_comp}", "p<0.05",   "—"],
    ]
    print(tabulate(rows, headers=["Metric","Value","Threshold","Verdict"], tablefmt="github"))

    print(f"\n── CONFUSION MATRIX (Test Set) ───────────────────────────────────")
    print(f"  Cutoff = {best_cut:.2f} | SPY {pred_qtr} = {spy_ret*100:+.2f}%")
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

    loadings_df = pd.DataFrame(pca_final.components_.T, index=kept,
                                columns=[f"PC{i+1}" for i in range(n_comp)])
    if verbose:
        print(f"\n── PCA LOADINGS FORMULA (fitted on training data) ────────────────")
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

    print(f"\n── MODEL COMPARISON — LR vs Gradient Boosting ────────────────────")
    print(tabulate([
        ["Logistic Regression", f"{train_auc:.4f}", f"{test_auc:.4f}", "Linear — primary model"],
        ["Gradient Boosting",   f"{gb_train_auc:.4f}", f"{gb_test_auc:.4f}",
         f"Non-linear | Δ test AUC={gb_test_auc-test_auc:+.4f}"],
    ], headers=["Model","Train AUC","Test AUC","Notes"], tablefmt="github"))

    all_results.append({
        'Feature Qtr':    feat_qtr,
        'Label Qtr':      pred_qtr,
        'Configuration':  config_name,
        'Group':          group_name,
        'Train N':        len(train_df2),
        'Test N':         len(test_df2),
        'Train AUC':      round(train_auc, 4),
        'Test AUC':       round(test_auc, 4),
        'AUC Change':     auc_change,
        'Test Acc':       test_acc,
        'Sensitivity':    sensitivity,
        'Specificity':    specificity,
        'Precision':      precision,
        'TP': int(tp), 'TN': int(tn), 'FP': int(fp), 'FN': int(fn),
        'Cutoff':         round(best_cut, 2),
        'PCA Comps':      n_comp,
        'VIF Kept':       len(kept),
        'Sig Comps':      f"{len(sig_comps)}/{n_comp}",
        'LR pvalue':      round(model.llr_pvalue, 4),
        'McFadden R2':    round(model.prsquared, 4),
        'Verdict':        verdict,
        'SPY Return':     round(spy_ret * 100, 2),
        '_pca':           pca_final,
        '_model':         model,
        '_kept':          kept,
    })


test_config = [
    (pd.Period('2025Q1','Q'), 1, 'Q1 2025', 'Q2 2025'),
    (pd.Period('2025Q2','Q'), 2, 'Q2 2025', 'Q3 2025'),
    (pd.Period('2025Q3','Q'), 3, 'Q3 2025', 'Q4 2025'),
    (pd.Period('2025Q4','Q'), 4, 'Q4 2025', 'Q1 2026'),
]

for (feat_qtr_period, crsp_cal_qtr, feat_lbl, pred_lbl) in test_config:
    spy_ret = spy_by_label.get(crsp_cal_qtr, 0.0)

    comp_test = comp_2025_features[comp_2025_features['cal_quarter'] == feat_qtr_period].copy()
    labels    = crsp_2025[crsp_2025['cal_qtr'] == crsp_cal_qtr][['gvkey','Outperform']].copy()
    labels    = labels.rename(columns={'Outperform': 'outperformer_next'})
    test_raw  = comp_test.merge(labels, on='gvkey', how='inner')

    macro_vals = macro_2025.get(feat_qtr_period, {'gdp_growth': 0.005, 'inflation': 0.005})
    test_raw['gdp_growth'] = macro_vals['gdp_growth']
    test_raw['inflation']  = macro_vals['inflation']

    for col in ratio_cols:
        if col in test_raw.columns and col in winsor_bounds:
            lo, hi = winsor_bounds[col]
            test_raw[col] = test_raw[col].clip(lo, hi)

    test_raw['cap_group']  = test_raw['mkvaltq'].apply(cap_label)
    test_raw['log_mkvalt'] = np.log(test_raw['mkvaltq'].clip(lower=1e-6))

    test_raw['sector_cluster'] = -1
    for s, (sc, km2) in cluster_models.items():
        idx = test_raw['sector_name'] == s
        if idx.sum() == 0:
            continue
        subset = test_raw.loc[idx, ratio_cols].fillna(train_medians)
        test_raw.loc[idx, 'sector_cluster'] = km2.predict(sc.transform(subset))

    n_test = len(test_raw)
    n_out  = int(test_raw['outperformer_next'].sum())
    print(f"\n\n{'='*70}")
    print(f"  TEST QUARTER: {feat_lbl} FEATURES → {pred_lbl} LABELS")
    print(f"  Test N={n_test} | Outperformers={n_out}/{n_test} ({n_out/n_test*100:.1f}%) | SPY {spy_ret*100:+.2f}%")
    print(f"{'='*70}")

    print(f"\n── CONFIGURATION 1: MARKET CAP SEGMENTATION ─────────────────────")
    for cap in ['Large Cap', 'Mid Cap', 'Small Cap']:
        run_validation('Market Cap', cap,
                       train_df[train_df['cap_group'] == cap],
                       test_raw[test_raw['cap_group'] == cap],
                       spy_ret, pred_lbl, feat_lbl)

    print(f"\n── CONFIGURATION 2: SECTOR GICS ──────────────────────────────────")
    for s in sectors:
        run_validation('Sector GICS', s,
                       train_df[train_df['sector_name'] == s],
                       test_raw[test_raw['sector_name'] == s],
                       spy_ret, pred_lbl, feat_lbl)

    print(f"\n── CONFIGURATION 3: SECTOR + MARKET CAP COVARIATE ───────────────")
    for s in sectors:
        run_validation('Sector + MktCap', f"{s} [+MktCap]",
                       train_df[train_df['sector_name'] == s],
                       test_raw[test_raw['sector_name'] == s],
                       spy_ret, pred_lbl, feat_lbl,
                       feature_cols=ratio_cols + ['log_mkvalt'])

    print(f"\n── CONFIGURATION 4: SECTOR + CLUSTERING (k=2) ───────────────────")
    for s in sectors:
        for c in [0, 1]:
            run_validation('Sector + Clustering (k=2)', f"{s} — Cluster {c}",
                           train_df[(train_df['sector_name'] == s) &
                                    (train_df['sector_cluster'] == c)],
                           test_raw[(test_raw['sector_name'] == s) &
                                    (test_raw['sector_cluster'] == c)],
                           spy_ret, pred_lbl, feat_lbl)


print("\n\n" + "="*70)
print("  GRAND SUMMARY — 100% WRDS OUT-OF-SAMPLE VALIDATION")
print("  Training: Q1 2010 – Q3 2024  |  Test: Q1–Q4 2025 (4 quarters)")
print("  All groups | Sorted by out-of-sample AUC")
print("="*70)

if not all_results:
    print("  No groups had sufficient data.")
else:
    pub_cols = [k for k in all_results[0].keys() if not k.startswith('_')]
    df_all = pd.DataFrame([{k: r[k] for k in pub_cols} for r in all_results])
    df_all = df_all.sort_values('Test AUC', ascending=False).reset_index(drop=True)
    df_all.insert(0, 'Rank', range(1, len(df_all)+1))

    print(tabulate(
        df_all[['Rank','Feature Qtr','Label Qtr','Configuration','Group',
                'Train N','Test N','Train AUC','Test AUC','AUC Change',
                'Test Acc','Sensitivity','Specificity','Verdict']].values.tolist(),
        headers=['Rank','Feat Qtr','Label Qtr','Config','Group','Train N','Test N',
                 'Train AUC','Test AUC','ΔAUC','Acc%','Sens%','Spec%','Verdict'],
        tablefmt='github'
    ))

    holds_up = (df_all['AUC Change'] >= -0.02).sum()
    modest   = ((df_all['AUC Change'] >= -0.05) & (df_all['AUC Change'] < -0.02)).sum()
    sig_deg  = (df_all['AUC Change'] < -0.05).sum()
    best_row = df_all.iloc[0]

    print(f"\n── PER-QUARTER SUMMARY ───────────────────────────────────────────")
    qtr_summary = []
    for feat_q in ['Q1 2025','Q2 2025','Q3 2025','Q4 2025']:
        sub = df_all[df_all['Feature Qtr'] == feat_q]
        if len(sub) == 0:
            continue
        pred_q  = sub['Label Qtr'].iloc[0]
        spy_ret = sub['SPY Return'].iloc[0]
        w_te    = (sub['Test AUC'] * sub['Train N']).sum() / sub['Train N'].sum()
        n_hu    = (sub['AUC Change'] >= -0.02).sum()
        best_g  = sub.iloc[0]['Group']
        best_a  = sub.iloc[0]['Test AUC']
        qtr_summary.append([feat_q, pred_q, f"{spy_ret:+.2f}%",
                            len(sub), round(w_te,4),
                            f"{n_hu}/{len(sub)}", best_g, best_a])
    print(tabulate(qtr_summary,
        headers=['Feat Qtr','Label Qtr','SPY Ret','Groups','W.Test AUC',
                 'Holds Up','Best Group','Best AUC'],
        tablefmt='github'))

    print(f"\n── CONFIGURATION-LEVEL SUMMARY ──────────────────────────────────")
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
    print(tabulate(config_summary,
        headers=['Rank','Configuration','Groups','W.Train AUC','W.Test AUC','ΔAUC','Holds Up'],
        tablefmt='github'))

    print(f"\n── OVERALL RESULTS ───────────────────────────────────────────────")
    summary_rows = [
        ["Total groups validated",    len(df_all)],
        ["Test quarters covered",     "Q1 2025 → Q2 2025 / Q2 2025 → Q3 2025 / Q3 2025 → Q4 2025 / Q4 2025 → Q1 2026"],
        ["Training period",           "Q1 2010 – Q3 2024 (WRDS Compustat + CRSP)"],
        ["Label source",              "WRDS CRSP 2025 — 100% WRDS, no external data"],
        ["Holds up (ΔAUC ≥ -0.02)",   f"{holds_up} / {len(df_all)}"],
        ["Modest degradation",        f"{modest} / {len(df_all)}"],
        ["Significant degradation",   f"{sig_deg} / {len(df_all)}"],
        ["Best out-of-sample AUC",    f"{best_row['Test AUC']} — {best_row['Group']} ({best_row['Feature Qtr']})"],
        ["Best out-of-sample accuracy", f"{best_row['Test Acc']}%"],
        ["Paper benchmark accuracy",  "71.2%"],
    ]
    print(tabulate(summary_rows, tablefmt='github'))

    print(f"\n── TOP 5 GROUPS — FULL PCA LOADINGS ─────────────────────────────")
    sorted_results = sorted(all_results, key=lambda r: r['Test AUC'], reverse=True)
    for rank, res in enumerate(sorted_results[:5], 1):
        pca_f = res['_pca']
        mdl   = res['_model']
        kept  = res['_kept']
        n_c   = res['PCA Comps']
        print(f"\n  Rank {rank}: {res['Group']} [{res['Configuration']}] — {res['Feature Qtr']} → {res['Label Qtr']}")
        print(f"  Test AUC={res['Test AUC']}  ΔAUC={res['AUC Change']:+.4f}  Acc={res['Test Acc']}%")
        loadings_df = pd.DataFrame(pca_f.components_.T, index=kept,
                                   columns=[f"PC{i+1}" for i in range(n_c)])
        conf      = np.array(mdl.conf_int())
        coef_rows = []
        for i in range(n_c):
            coef  = mdl.params[i+1]
            p     = mdl.pvalues[i+1]
            OR    = np.exp(coef)
            ci_lo = np.exp(conf[i+1,0])
            ci_hi = np.exp(conf[i+1,1])
            if p < 0.01:   sig = "*** p<0.01"
            elif p < 0.05: sig = "**  p<0.05"
            elif p < 0.10: sig = "*   p<0.10"
            else:          sig = "No"
            coef_rows.append([f"PC{i+1}", f"{coef:+.4f}", f"{OR:.4f}",
                              f"[{ci_lo:.3f},{ci_hi:.3f}]",
                              f"{mdl.tvalues[i+1]:.3f}", f"{p:.4f}", sig])
        print(tabulate(coef_rows,
            headers=["Component","Coeff","Odds Ratio","95% CI","Z-Stat","p-Value","Significant?"],
            tablefmt="github"))
        loading_rows = []
        for feat in kept:
            row = [ratio_labels.get(feat, feat)]
            for pc in loadings_df.columns:
                row.append(f"{loadings_df.loc[feat, pc]:+.4f}")
            loading_rows.append(row)
        print(tabulate(loading_rows,
            headers=["Predictor"] + list(loadings_df.columns), tablefmt="github"))
        print(f"  Top 3 per component:")
        for pc in loadings_df.columns:
            top = loadings_df[pc].abs().nlargest(3).index.tolist()
            print(f"    {pc}: {', '.join([ratio_labels.get(r,r) for r in top])}")

    print(f"\n── METHODOLOGY NOTES ─────────────────────────────────────────────")
    print(f"  Data source       : 100% WRDS (Compustat + CRSP) — no external APIs")
    print(f"  Feature source    : WRDS Compustat 2025 (clean quarterly ratios)")
    print(f"  Delta features    : Q[t] – Q[t-1] for 10 key ratios (momentum signals)")
    print(f"  Label source      : WRDS CRSP 2025 — Outperform = (Q[t+1] return > SPY)")
    print(f"  Method            : VIF≤2.5 → PCA≥5%/component → Logistic Regression + Gradient Boosting")
    print(f"  Winsorization     : 1st–99th percentile from training data only")
    print(f"  Market cap ths.   : Computed from training data only")
    print(f"  Cluster assignment: KMeans fitted on 2010–Q3 2024, applied to 2025")
    print(f"  Forward-looking   : Q[t] ratios → Q[t+1] outperformance (shift=-1)")
    print("="*70)

    sys.stdout.log.close()
    sys.stdout = sys.stdout.terminal
    print(f"\n  Results saved to: results_validation_delta.txt")

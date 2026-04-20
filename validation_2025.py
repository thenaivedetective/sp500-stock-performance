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

TRAIN_END = '2021Q4'
TEST_START = '2022Q1'
TEST_END   = '2024Q4'

print("=" * 65)
print("  OUT-OF-SAMPLE TEMPORAL VALIDATION")
print(f"  Training : Q1 2010 – Q4 2021  (12 years)")
print(f"  Test     : Q1 2022 – Q4 2024  (3 years)")
print("  Configuration: Sector + Clustering (k=2)  [WINNER]")
print("  All model parameters fitted on training data ONLY")
print("  Reference: Ananthakumar & Sarkar (2017)")
print("  Note: CRSP data ends Dec 2024; 2025 returns not yet in WRDS")
print("=" * 65)

print("\n[1/4] Loading and processing full dataset...")

comp      = pd.read_csv('wrds_compustat_quarterly.csv', low_memory=False)
crsp      = pd.read_csv('wrds_crsp_quarterly.csv',     low_memory=False)
gics      = pd.read_csv('wrds_gics_sectors.csv',       low_memory=False)
macro     = pd.read_csv('wrds_fred_macro.csv',         low_memory=False)
sp500hist = pd.read_csv('wrds_sp500_history.csv',      low_memory=False)

sp500hist['start_date'] = pd.to_datetime(sp500hist['start_date'])
sp500hist['end_date']   = pd.to_datetime(sp500hist['end_date'].fillna('2099-12-31'))
gics['gvkey']           = gics['gvkey'].astype(str)

numeric_cols = ['revtq','cogsq','xsgaq','xrdq','oibdpq','oiadpq','niq','ibq',
                'piq','atq','ceqq','teqq','dlttq','dlcq','actq','lctq',
                'cheq','dpq','txtq','prccq','cshoq','mkvaltq']
for c in numeric_cols:
    comp[c] = pd.to_numeric(comp[c], errors='coerce')

comp['datadate']    = pd.to_datetime(comp['datadate'])
comp['cal_quarter'] = comp['datadate'].dt.to_period('Q')
comp['gvkey']       = comp['gvkey'].astype(str)
crsp['quarter']     = pd.PeriodIndex(crsp['quarter_str'], freq='Q')
macro['quarter']    = pd.PeriodIndex(macro['quarter'], freq='Q')

comp = comp.sort_values(['gvkey', 'cal_quarter'])
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

comp = comp.merge(gics[['gvkey', 'gsector', 'sector_name']], on='gvkey', how='left')

ratio_cols = ['roa','roe','gross_margin','op_margin','net_margin','asset_turnover',
              'current_ratio','debt_to_equity','rev_growth','ni_growth',
              'pe_ratio','book_to_market','gdp_growth','inflation']

ratio_labels = {
    'roa':'Return on Assets (ROA)', 'roe':'Return on Equity (ROE)',
    'gross_margin':'Gross Profit Margin', 'op_margin':'Operating Margin',
    'net_margin':'Net Profit Margin', 'asset_turnover':'Asset Turnover',
    'current_ratio':'Current Ratio', 'debt_to_equity':'Debt-to-Equity',
    'rev_growth':'Revenue Growth (QoQ)', 'ni_growth':'Net Income Growth (QoQ)',
    'pe_ratio':'P/E Ratio', 'book_to_market':'Book-to-Market',
    'gdp_growth':'GDP Growth (Quarterly)', 'inflation':'CPI Inflation (Quarterly)',
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

print("\n[2/4] Splitting into train / test...")

merged_train = merged[merged['cal_quarter'] <= pd.Period(TRAIN_END)].copy()
merged_test  = merged[merged['cal_quarter'] >= pd.Period(TEST_START)].copy()

winsor_bounds = {}
train_medians = {}
for col in ratio_cols:
    if col in merged_train.columns:
        lo = merged_train[col].quantile(0.01)
        hi = merged_train[col].quantile(0.99)
        winsor_bounds[col] = (lo, hi)
        merged_train[col]  = merged_train[col].clip(lo, hi)
        train_medians[col] = merged_train[col].median()

for col in ratio_cols:
    if col in merged_test.columns and col in winsor_bounds:
        lo, hi = winsor_bounds[col]
        merged_test[col] = merged_test[col].clip(lo, hi)

print(f"  Training rows : {len(merged_train):,} | With target: {merged_train['outperformer_next'].notna().sum():,}")
print(f"  Test rows     : {len(merged_test):,}  | With target: {merged_test['outperformer_next'].notna().sum():,}")
print(f"  Training period : {merged_train['cal_quarter'].min()} – {merged_train['cal_quarter'].max()}")
print(f"  Test period     : {merged_test['cal_quarter'].min()}  – {merged_test['cal_quarter'].max()}")

print("\n[3/4] Fitting KMeans on training data → assigning test data...")

sectors = sorted(merged_train['sector_name'].dropna().unique())
cluster_models = {}
for s in sectors:
    idx    = merged_train['sector_name'] == s
    subset = merged_train.loc[idx, ratio_cols].fillna(train_medians)
    if len(subset) < 40:
        continue
    sc  = StandardScaler()
    sc_fit = sc.fit_transform(subset)
    km2 = KMeans(n_clusters=2, random_state=42, n_init=10)
    km2.fit(sc_fit)
    cluster_models[s] = (sc, km2)

merged_train['sector_cluster'] = -1
for s, (sc, km2) in cluster_models.items():
    idx    = merged_train['sector_name'] == s
    subset = merged_train.loc[idx, ratio_cols].fillna(train_medians)
    merged_train.loc[idx, 'sector_cluster'] = km2.predict(sc.transform(subset))

merged_test['sector_cluster'] = -1
for s, (sc, km2) in cluster_models.items():
    idx = merged_test['sector_name'] == s
    if idx.sum() == 0:
        continue
    subset = merged_test.loc[idx, ratio_cols].fillna(train_medians)
    merged_test.loc[idx, 'sector_cluster'] = km2.predict(sc.transform(subset))

def vif_filter(X_df, cutoff=2.5):
    remaining = list(X_df.columns)
    while True:
        vifs    = [variance_inflation_factor(X_df[remaining].values, i) for i in range(len(remaining))]
        max_vif = max(vifs)
        if max_vif <= cutoff:
            break
        worst = remaining[vifs.index(max_vif)]
        remaining.remove(worst)
    return remaining

print("\n[4/4] Running validation pipeline...")

all_results = []

def run_validation(group_name, train_df, test_df):
    available = [c for c in ratio_cols if c in train_df.columns and c in test_df.columns]

    train = train_df[available + ['outperformer_next']].dropna()
    test  = test_df[available  + ['outperformer_next']].dropna()

    if len(train) < 100 or train['outperformer_next'].nunique() < 2:
        print(f"\n  {group_name}: insufficient training data ({len(train)} rows), skipping.")
        return
    if len(test) < 5 or test['outperformer_next'].nunique() < 2:
        print(f"\n  {group_name}: insufficient test data ({len(test)} rows) or single class, skipping.")
        return

    X_train = train[available]
    y_train = train['outperformer_next']
    X_test  = test[available]
    y_test  = test['outperformer_next']

    scaler         = StandardScaler()
    X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=available)
    X_test_scaled  = pd.DataFrame(scaler.transform(X_test),      columns=available)

    kept          = vif_filter(X_train_scaled, cutoff=2.5)
    X_train_clean = X_train_scaled[kept]
    X_test_clean  = X_test_scaled[kept]

    pca_fit = PCA()
    pca_fit.fit(X_train_clean)
    exp_var = np.cumsum(pca_fit.explained_variance_ratio_)
    n_comp  = min(int(np.searchsorted(exp_var, 0.80)) + 1, len(kept))

    pca_final   = PCA(n_components=n_comp)
    X_train_pca = pca_final.fit_transform(X_train_clean)
    X_test_pca  = pca_final.transform(X_test_clean)

    X_train_const = sm.add_constant(X_train_pca)
    model = Logit(y_train.values, X_train_const).fit(maxiter=200, disp=False)

    y_train_prob = model.predict(X_train_const)
    train_auc    = roc_auc_score(y_train, y_train_prob)

    best_cut, best_acc_val = 0.5, 0
    for thresh in np.arange(0.30, 0.75, 0.05):
        preds = (y_train_prob >= thresh).astype(int)
        acc   = (preds == y_train.values).mean()
        if acc > best_acc_val:
            best_acc_val, best_cut = acc, thresh
    best_cut  = round(best_cut, 2)
    train_acc = round(best_acc_val * 100, 1)

    train_preds = (y_train_prob >= best_cut).astype(int)
    cm_tr = confusion_matrix(y_train.values, train_preds)
    if cm_tr.shape == (2, 2):
        tn, fp, fn, tp = cm_tr.ravel()
        train_sens = round(tp / (tp + fn) * 100, 1) if (tp + fn) > 0 else 0
        train_spec = round(tn / (tn + fp) * 100, 1) if (tn + fp) > 0 else 0
    else:
        train_sens = train_spec = 0

    X_test_const = sm.add_constant(X_test_pca, has_constant='add')
    y_test_prob  = model.predict(X_test_const)
    test_auc     = roc_auc_score(y_test, y_test_prob)

    test_preds = (y_test_prob >= best_cut).astype(int)
    test_acc   = round((test_preds == y_test.values).mean() * 100, 1)

    cm_te = confusion_matrix(y_test.values, test_preds)
    if cm_te.shape == (2, 2):
        tn_t, fp_t, fn_t, tp_t = cm_te.ravel()
        test_sens = round(tp_t / (tp_t + fn_t) * 100, 1) if (tp_t + fn_t) > 0 else 0
        test_spec = round(tn_t / (tn_t + fp_t) * 100, 1) if (tn_t + fp_t) > 0 else 0
    else:
        test_sens = test_spec = 0

    auc_change = round(test_auc - train_auc, 4)
    acc_change = round(test_acc - train_acc,  1)

    if auc_change >= -0.02:
        verdict = "HOLDS UP"
    elif auc_change >= -0.05:
        verdict = "MODEST DEGRADATION"
    else:
        verdict = "SIGNIFICANT DEGRADATION"

    print(f"\n{'='*65}")
    print(f"  {group_name.upper()}")
    print(f"  Train N={len(train):,} (2010-21) | Test N={len(test):,} (2022-24)")
    print(f"  Train outperformers: {y_train.mean()*100:.1f}% | Test: {y_test.mean()*100:.1f}%")
    print(f"{'='*65}")
    print(f"\n── VALIDATION METRICS ────────────────────────────────────────")
    print(tabulate([
        ["AUC",         f"{train_auc:.4f}",    f"{test_auc:.4f}",  f"{auc_change:+.4f}"],
        ["Accuracy",    f"{train_acc:.1f}%",   f"{test_acc:.1f}%", f"{acc_change:+.1f}%"],
        ["Sensitivity", f"{train_sens:.1f}%",  f"{test_sens:.1f}%","—"],
        ["Specificity", f"{train_spec:.1f}%",  f"{test_spec:.1f}%","—"],
        ["N",           f"{len(train):,}",      f"{len(test):,}",   "—"],
        ["Cutoff",      f"{best_cut}",          f"{best_cut} (same)","—"],
        ["PCA Comps",   f"{n_comp}",            f"{n_comp} (same)", "—"],
        ["VIF Kept",    f"{len(kept)}/{len(available)}", "—",       "—"],
    ], headers=["Metric","In-Sample (2010-21)","Out-of-Sample (2022-24)","Change"],
       tablefmt="github"))
    print(f"\n  Verdict: {verdict}")

    all_results.append({
        'Group':      group_name,
        'Train N':    len(train),
        'Test N':     len(test),
        'Train AUC':  round(train_auc, 4),
        'Test AUC':   round(test_auc,  4),
        'AUC Change': auc_change,
        'Train Acc':  train_acc,
        'Test Acc':   test_acc,
        'Acc Change': acc_change,
        'Train Sens': train_sens,
        'Test Sens':  test_sens,
        'Train Spec': train_spec,
        'Test Spec':  test_spec,
        'Verdict':    verdict,
    })


print("\n\n" + "=" * 65)
print("  SECTOR + CLUSTERING (k=2) — OUT-OF-SAMPLE VALIDATION")
print(f"  Train: Q1 2010 – Q4 2021 | Test: Q1 2022 – Q4 2024")
print("  Predicting: Q[t] ratios → Q[t+1] outperformance")
print("=" * 65)

for s in sectors:
    s_train = merged_train[(merged_train['sector_name'] == s) & (merged_train['sector_cluster'] >= 0)]
    s_test  = merged_test[ (merged_test['sector_name']  == s) & (merged_test['sector_cluster']  >= 0)]
    for c in [0, 1]:
        run_validation(
            f"{s} — Cluster {c}",
            s_train[s_train['sector_cluster'] == c],
            s_test[ s_test['sector_cluster']  == c]
        )

print("\n\n" + "=" * 65)
print("  GRAND VALIDATION SUMMARY")
print(f"  In-Sample (2010-21) vs Out-of-Sample (2022-24)")
print("  Sorted by Out-of-Sample AUC  |  Config: Sector + Clustering (k=2)")
print("=" * 65)

df_val = pd.DataFrame(all_results)
if len(df_val) > 0:
    df_val = df_val.sort_values('Test AUC', ascending=False).reset_index(drop=True)
    df_val.insert(0, 'Rank', range(1, len(df_val) + 1))

    print(tabulate(
        df_val[['Rank','Group','Train N','Test N',
                'Train AUC','Test AUC','AUC Change',
                'Train Acc','Test Acc','Verdict']].values.tolist(),
        headers=['Rank','Group','Train N','Test N',
                 'Train AUC','Test AUC','ΔAUC',
                 'Train Acc%','Test Acc%','Verdict'],
        tablefmt='github'
    ))

    avg_train_auc = df_val['Train AUC'].mean()
    avg_test_auc  = df_val['Test AUC'].mean()
    avg_train_acc = df_val['Train Acc'].mean()
    avg_test_acc  = df_val['Test Acc'].mean()
    n_holds   = (df_val['Verdict'] == 'HOLDS UP').sum()
    n_modest  = (df_val['Verdict'] == 'MODEST DEGRADATION').sum()
    n_sig_deg = (df_val['Verdict'] == 'SIGNIFICANT DEGRADATION').sum()
    best_auc_row = df_val.iloc[0]
    best_acc_row = df_val.sort_values('Test Acc', ascending=False).iloc[0]

    print(f"\n── OVERALL VALIDATION SUMMARY ──────────────────────────────")
    print(tabulate([
        ["Groups validated",                  len(df_val)],
        ["Avg in-sample AUC    (2010-21)",    f"{avg_train_auc:.4f}"],
        ["Avg out-of-sample AUC (2022-24)",   f"{avg_test_auc:.4f}"],
        ["Avg AUC change",                    f"{avg_test_auc - avg_train_auc:+.4f}"],
        ["Avg in-sample accuracy  (2010-21)", f"{avg_train_acc:.1f}%"],
        ["Avg out-of-sample acc   (2022-24)", f"{avg_test_acc:.1f}%"],
        ["Avg accuracy change",               f"{avg_test_acc - avg_train_acc:+.1f}%"],
        ["Holds Up  (ΔAUC ≥ -0.02)",          f"{n_holds}/{len(df_val)}"],
        ["Modest Degradation",                f"{n_modest}/{len(df_val)}"],
        ["Significant Degradation",           f"{n_sig_deg}/{len(df_val)}"],
        ["Best out-of-sample AUC group",      f"{best_auc_row['Group']} (AUC={best_auc_row['Test AUC']:.4f})"],
        ["Best out-of-sample accuracy group", f"{best_acc_row['Group']} ({best_acc_row['Test Acc']:.1f}%)"],
        ["Paper benchmark accuracy",          "71.2%"],
    ], tablefmt="github"))

    print(f"\n── INTERPRETATION ───────────────────────────────────────────")
    if avg_test_auc >= avg_train_auc - 0.02:
        gen_verdict = "GENERALIZES WELL — out-of-sample performance matches in-sample"
    elif avg_test_auc >= avg_train_auc - 0.05:
        gen_verdict = "MODEST OVERFITTING — slight degradation but model still predictive"
    else:
        gen_verdict = "OVERFITTING DETECTED — significant gap between train and test"
    print(f"  Generalization: {gen_verdict}")
    print(f"\n  Training horizon  : Q1 2010 – Q4 2021 (12 years)")
    print(f"  Test horizon      : Q1 2022 – Q4 2024  (3 years, unseen)")
    print(f"  Method            : VIF≤2.5 → PCA≥80% → Logistic Regression")
    print(f"  Cluster assignment: KMeans fitted on 2010-21, applied to 2022-24")
    print(f"  Winsorization     : 1st-99th percentile bounds from 2010-21 only")
    print(f"  Predicting        : Q[t] ratios → Q[t+1] outperformance (shift=-1)")
    print(f"  Note              : CRSP returns end Dec 2024; true 2025 test pending")
    print("=" * 65 + "\n")

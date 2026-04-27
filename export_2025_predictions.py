import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from statsmodels.stats.outliers_influence import variance_inflation_factor
import warnings
warnings.filterwarnings('ignore')

comp_raw  = pd.read_csv('wrds_compustat_quarterly.csv')
crsp_raw  = pd.read_csv('wrds_crsp_quarterly.csv')
gics      = pd.read_csv('wrds_gics_sectors.csv')
sp500_hist = pd.read_csv('wrds_sp500_history.csv')
comp_2025 = pd.read_csv('wrds_compustat_quarterly_2025.csv')
crsp_2025 = pd.read_csv('wrds_crsp_quarterly_2025.csv')

comp = comp_raw.copy()
comp = comp.sort_values(['gvkey','datadate'])
comp['lag_revtq'] = comp.groupby('gvkey')['revtq'].shift(1)
comp['lag_niq']   = comp.groupby('gvkey')['niq'].shift(1)

comp['gross_margin']  = (comp['revtq'] - comp['cogsq']) / comp['revtq'].replace(0, np.nan)
comp['net_margin']    = comp['niq'] / comp['revtq'].replace(0, np.nan)
comp['roa']           = comp['niq'] / comp['atq'].replace(0, np.nan)
comp['roe']           = comp['niq'] / comp['ceqq'].replace(0, np.nan)
comp['debt_to_equity']= comp['dlttq'] / comp['ceqq'].replace(0, np.nan)
comp['current_ratio'] = comp['actq'] / comp['lctq'].replace(0, np.nan)
comp['asset_turnover']= comp['revtq'] / comp['atq'].replace(0, np.nan)
comp['rev_growth']    = (comp['revtq'] - comp['lag_revtq']) / comp['lag_revtq'].abs().replace(0, np.nan)
comp['earnings_growth']=(comp['niq'] - comp['lag_niq']) / comp['lag_niq'].abs().replace(0, np.nan)
comp['pe_ratio']      = comp['prccq'] / (comp['niq'] / comp['cshoq'].replace(0, np.nan)).replace(0, np.nan)
comp['pb_ratio']      = comp['mkvaltq'] / comp['ceqq'].replace(0, np.nan)
comp['ebitda_margin'] = comp['oibdpq'] / comp['revtq'].replace(0, np.nan)
comp['log_mkvalt']    = np.log(comp['mkvaltq'].clip(lower=1e-6))
comp['rd_intensity']  = comp['xrdq'].fillna(0) / comp['revtq'].replace(0, np.nan)

delta_cols = ['gross_margin','net_margin','roa','roe','debt_to_equity',
              'current_ratio','asset_turnover','rev_growth','pe_ratio','pb_ratio']
for col in delta_cols:
    comp[f'delta_{col}'] = comp.groupby('gvkey')[col].diff()

gics['gvkey'] = gics['gvkey'].astype(str)
comp['gvkey']  = comp['gvkey'].astype(str)
comp = comp.merge(gics[['gvkey','sector_name']], on='gvkey', how='left')

ratio_cols = [
    'gross_margin','net_margin','roa','roe','debt_to_equity','current_ratio',
    'asset_turnover','rev_growth','earnings_growth','pe_ratio','pb_ratio',
    'ebitda_margin','log_mkvalt','rd_intensity',
] + [f'delta_{c}' for c in delta_cols]

merged = comp.merge(
    crsp_raw[['ticker','quarter','quarterly_return','spy_quarterly_return','outperformer_quarterly']],
    left_on=['tic','quarter'], right_on=['ticker','quarter'], how='inner'
)
merged['cal_quarter'] = merged['quarter']

try:
    sp500_hist['gvkey'] = sp500_hist['gvkey'].astype(str)
    quarters_all = merged['cal_quarter'].unique()
    constituent_rows = []
    for q in quarters_all:
        mask = (sp500_hist['start'] <= q) & (sp500_hist['end'] >= q)
        for gv in sp500_hist[mask]['gvkey'].unique():
            constituent_rows.append({'gvkey': str(gv), 'cal_quarter': q})
    constituent_panel = pd.DataFrame(constituent_rows)
    merged['gvkey'] = merged['gvkey'].astype(str)
    merged = merged.merge(constituent_panel, on=['gvkey','cal_quarter'], how='inner').reset_index(drop=True)
except Exception:
    pass

merged = merged.sort_values(['gvkey','cal_quarter']).reset_index(drop=True)
merged['outperformer_next'] = merged.groupby('gvkey')['outperformer_quarterly'].shift(-1)

train_df = merged[merged['cal_quarter'] <= '2024Q4'].copy()

winsor_bounds = {}
for col in ratio_cols:
    if col not in train_df.columns:
        continue
    lo = train_df[col].quantile(0.01)
    hi = train_df[col].quantile(0.99)
    winsor_bounds[col] = (lo, hi)
    train_df[col] = train_df[col].clip(lo, hi)

train_medians = {col: train_df[col].median() for col in ratio_cols if col in train_df.columns}

available = [c for c in ratio_cols if c in train_df.columns]
train_clean = train_df[available + ['outperformer_next']].dropna()
X_tr = train_clean[available]
y_tr = train_clean['outperformer_next']

def vif_filter(X, threshold=2.5):
    cols = list(X.columns)
    while True:
        vif_vals = [variance_inflation_factor(X[cols].values, i) for i in range(len(cols))]
        max_vif  = max(vif_vals)
        if max_vif < threshold:
            break
        cols.pop(int(np.argmax(vif_vals)))
    return cols

kept = vif_filter(X_tr)
X_tr_kept = X_tr[kept]
scaler = StandardScaler()
X_tr_sc = scaler.fit_transform(X_tr_kept)
_pca_full = PCA().fit(X_tr_sc)
_n_comp   = max(1, int(np.sum(_pca_full.explained_variance_ratio_ >= 0.05)))
pca = PCA(n_components=_n_comp)
X_tr_pca = pca.fit_transform(X_tr_sc)

clf = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
clf.fit(X_tr_pca, y_tr)
train_probs = clf.predict_proba(X_tr_pca)[:, 1]
threshold = np.percentile(train_probs, 50)

stack_cols = ['gvkey','tic','conm','datadate','revtq','cogsq','oiadpq','niq','ibq',
              'piq','atq','ceqq','teqq','dlttq','dlcq','actq','lctq','cheq',
              'dpq','txtq','prccq','cshoq','mkvaltq','xsgaq','xrdq','oibdpq','quarter']
stack_cols_25 = [c for c in stack_cols if c in comp_2025.columns]
comp_2025_raw = comp_2025[stack_cols_25].copy()
comp_2025_raw['gvkey'] = comp_2025_raw['gvkey'].astype(str)

crsp_2025['gvkey'] = crsp_2025['gvkey'].astype(str)
crsp_2025_sub = crsp_2025[['gvkey','cal_qtr','q_return','sp500_q_return',
                             'following_q_return','following_sp500_q_return','Outperform']].copy()

comp_2025_raw['lag_revtq'] = np.nan
comp_2025_raw['lag_niq']   = np.nan
comp_2025_raw['gross_margin']   = (comp_2025_raw['revtq'] - comp_2025_raw['cogsq']) / comp_2025_raw['revtq'].replace(0, np.nan)
comp_2025_raw['net_margin']     = comp_2025_raw['niq'] / comp_2025_raw['revtq'].replace(0, np.nan)
comp_2025_raw['roa']            = comp_2025_raw['niq'] / comp_2025_raw['atq'].replace(0, np.nan)
comp_2025_raw['roe']            = comp_2025_raw['niq'] / comp_2025_raw['ceqq'].replace(0, np.nan)
comp_2025_raw['debt_to_equity'] = comp_2025_raw['dlttq'] / comp_2025_raw['ceqq'].replace(0, np.nan)
comp_2025_raw['current_ratio']  = comp_2025_raw['actq'] / comp_2025_raw['lctq'].replace(0, np.nan)
comp_2025_raw['asset_turnover'] = comp_2025_raw['revtq'] / comp_2025_raw['atq'].replace(0, np.nan)
comp_2025_raw['rev_growth']     = np.nan
comp_2025_raw['earnings_growth']= np.nan
comp_2025_raw['pe_ratio']       = comp_2025_raw['prccq'] / (comp_2025_raw['niq'] / comp_2025_raw['cshoq'].replace(0, np.nan)).replace(0, np.nan)
comp_2025_raw['pb_ratio']       = comp_2025_raw['mkvaltq'] / comp_2025_raw['ceqq'].replace(0, np.nan)
comp_2025_raw['ebitda_margin']  = comp_2025_raw['oibdpq'] / comp_2025_raw['revtq'].replace(0, np.nan)
comp_2025_raw['log_mkvalt']     = np.log(comp_2025_raw['mkvaltq'].clip(lower=1e-6))
comp_2025_raw['rd_intensity']   = comp_2025_raw['xrdq'].fillna(0) / comp_2025_raw['revtq'].replace(0, np.nan)
for col in delta_cols:
    comp_2025_raw[f'delta_{col}'] = np.nan

sect_map = gics[['gvkey','sector_name']].drop_duplicates('gvkey')
comp_2025_raw = comp_2025_raw.merge(sect_map, on='gvkey', how='left')

for col in ratio_cols:
    if col in comp_2025_raw.columns and col in winsor_bounds:
        lo, hi = winsor_bounds[col]
        comp_2025_raw[col] = comp_2025_raw[col].clip(lo, hi)
    elif col in comp_2025_raw.columns and col in train_medians:
        comp_2025_raw[col] = comp_2025_raw[col].fillna(train_medians[col])

all_preds = []

comp_q4_2024 = merged[merged['cal_quarter'] == '2024Q4'].copy()
crsp_q1_2025 = crsp_2025_sub[crsp_2025_sub['cal_qtr'] == 1][['gvkey','q_return','sp500_q_return']].copy()
crsp_q1_2025['outperformer_next'] = (crsp_q1_2025['q_return'] > crsp_q1_2025['sp500_q_return']).astype(int)
crsp_q1_2025 = crsp_q1_2025.rename(columns={'q_return': 'actual_return', 'sp500_q_return': 'spy_return'})

if not comp_q4_2024.empty and not crsp_q1_2025.empty:
    comp_q4_2024_feat = comp_q4_2024.drop(columns=['outperformer_next'], errors='ignore')
    test_q4 = comp_q4_2024_feat.merge(
        crsp_q1_2025[['gvkey','outperformer_next','actual_return','spy_return']],
        on='gvkey', how='inner'
    )
    if not test_q4.empty:
        for col in ratio_cols:
            if col in test_q4.columns:
                if col in winsor_bounds:
                    lo, hi = winsor_bounds[col]
                    test_q4[col] = test_q4[col].clip(lo, hi)
                test_q4[col] = test_q4[col].fillna(train_medians.get(col, 0))
        test_avail = [c for c in kept if c in test_q4.columns]
        if len(test_avail) == len(kept):
            X_te_sc  = scaler.transform(test_q4[kept])
            X_te_pca = pca.transform(X_te_sc)
            probs    = clf.predict_proba(X_te_pca)[:, 1]
            preds    = (probs >= threshold).astype(int)
            out = test_q4[['gvkey','tic','conm','sector_name','outperformer_next','actual_return','spy_return']].copy()
            out['feature_quarter'] = "2024 Q4"
            out['label_quarter']   = "2025 Q1"
            out['prob_outperform'] = probs.round(4)
            out['predicted']       = preds
            out['predicted_label'] = out['predicted'].map({1: 'Outperformer', 0: 'Underperformer'})
            out['actual_label']    = out['outperformer_next'].map({1: 'Outperformer', 0: 'Underperformer'})
            out['correct']         = (out['predicted'] == out['outperformer_next']).astype(int)
            all_preds.append(out)

test_quarters = [
    (1, 2),
    (2, 3),
    (3, 4),
]

for feat_qtr, label_qtr in test_quarters:
    comp_test = comp_2025_raw[comp_2025_raw['quarter'] == feat_qtr].copy()
    crsp_sub = crsp_2025_sub[crsp_2025_sub['cal_qtr'] == label_qtr].copy()
    crsp_sub = crsp_sub[['gvkey','following_q_return','following_sp500_q_return','Outperform']].copy()
    crsp_sub = crsp_sub.rename(columns={
        'Outperform': 'outperformer_next',
        'following_q_return': 'actual_return',
        'following_sp500_q_return': 'spy_return'
    })
    if crsp_sub.empty:
        continue

    test_raw = comp_test.merge(crsp_sub[['gvkey','outperformer_next','actual_return','spy_return']],
                               on='gvkey', how='inner')
    if test_raw.empty:
        continue

    for col in ratio_cols:
        if col in test_raw.columns:
            test_raw[col] = test_raw[col].fillna(train_medians.get(col, 0))

    test_avail = [c for c in kept if c in test_raw.columns]
    if len(test_avail) < len(kept):
        continue

    X_te_sc  = scaler.transform(test_raw[kept])
    X_te_pca = pca.transform(X_te_sc)
    probs    = clf.predict_proba(X_te_pca)[:, 1]
    preds    = (probs >= threshold).astype(int)

    out = test_raw[['gvkey','tic','conm','sector_name','outperformer_next','actual_return','spy_return']].copy()
    out['feature_quarter'] = f"2025 Q{feat_qtr}"
    out['label_quarter']   = f"2025 Q{label_qtr}"
    out['prob_outperform'] = probs.round(4)
    out['predicted']       = preds
    out['predicted_label'] = out['predicted'].map({1: 'Outperformer', 0: 'Underperformer'})
    out['actual_label']    = out['outperformer_next'].map({1: 'Outperformer', 0: 'Underperformer'})
    out['correct']         = (out['predicted'] == out['outperformer_next']).astype(int)
    all_preds.append(out)

if all_preds:
    final = pd.concat(all_preds, ignore_index=True)
    final = final.sort_values(['label_quarter','prob_outperform'], ascending=[True, False])
    final = final.rename(columns={
        'tic': 'Ticker', 'conm': 'Company', 'sector_name': 'Sector',
        'actual_return': 'Actual_Return_Pct', 'spy_return': 'SPY_Return_Pct',
        'prob_outperform': 'P(Outperform)', 'predicted_label': 'Predicted',
        'actual_label': 'Actual', 'correct': 'Correct',
        'feature_quarter': 'Feature_Quarter', 'label_quarter': 'Label_Quarter'
    })
    cols_out = ['Label_Quarter','Feature_Quarter','Ticker','Company','Sector',
                'Predicted','Actual','Correct','P(Outperform)','Actual_Return_Pct','SPY_Return_Pct']
    final = final[[c for c in cols_out if c in final.columns]]
    final.to_csv('predictions_2025.csv', index=False)
    print(f"Saved {len(final)} predictions to predictions_2025.csv")

    for q in sorted(final['Label_Quarter'].unique()):
        sub = final[final['Label_Quarter'] == q]
        acc = sub['Correct'].mean() * 100
        print(f"\n  {q}: {len(sub)} stocks | Accuracy = {acc:.1f}%")
        print(f"    Predicted Outperformers  : {(sub['Predicted']=='Outperformer').sum()}")
        print(f"    Predicted Underperformers: {(sub['Predicted']=='Underperformer').sum()}")
else:
    print("No predictions generated — check quarter alignment in 2025 data")

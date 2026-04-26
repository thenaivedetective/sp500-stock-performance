import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from statsmodels.stats.outliers_influence import variance_inflation_factor
import warnings
warnings.filterwarnings('ignore')

print("=" * 68)
print("  COMMUNICATION SERVICES — SECTOR MODEL 2025 PREDICTIONS")
print("  Best performing group: AUC=0.892, 72.2% accuracy (thesis)")
print("=" * 68)

comp_raw   = pd.read_csv('wrds_compustat_quarterly.csv')
crsp_raw   = pd.read_csv('wrds_crsp_quarterly.csv')
gics       = pd.read_csv('wrds_gics_sectors.csv')
sp500_hist = pd.read_csv('wrds_sp500_history.csv')
comp_2025  = pd.read_csv('wrds_compustat_quarterly_2025.csv')
crsp_2025  = pd.read_csv('wrds_crsp_quarterly_2025.csv')

def build_features(df):
    df = df.copy().sort_values(['gvkey','datadate'])
    df['lag_revtq'] = df.groupby('gvkey')['revtq'].shift(1)
    df['lag_niq']   = df.groupby('gvkey')['niq'].shift(1)
    df['gross_margin']   = (df['revtq'] - df['cogsq'])    / df['revtq'].replace(0, np.nan)
    df['net_margin']     =  df['niq']   / df['revtq'].replace(0, np.nan)
    df['roa']            =  df['niq']   / df['atq'].replace(0, np.nan)
    df['roe']            =  df['niq']   / df['ceqq'].replace(0, np.nan)
    df['debt_to_equity'] =  df['dlttq'] / df['ceqq'].replace(0, np.nan)
    df['current_ratio']  =  df['actq']  / df['lctq'].replace(0, np.nan)
    df['asset_turnover'] =  df['revtq'] / df['atq'].replace(0, np.nan)
    df['rev_growth']     = (df['revtq'] - df['lag_revtq']) / df['lag_revtq'].abs().replace(0, np.nan)
    df['earnings_growth']= (df['niq']   - df['lag_niq'])   / df['lag_niq'].abs().replace(0, np.nan)
    df['pe_ratio']       =  df['prccq'] / (df['niq'] / df['cshoq'].replace(0, np.nan)).replace(0, np.nan)
    df['pb_ratio']       =  df['mkvaltq'] / df['ceqq'].replace(0, np.nan)
    df['ebitda_margin']  =  df['oibdpq'] / df['revtq'].replace(0, np.nan)
    df['log_mkvalt']     = np.log(df['mkvaltq'].clip(lower=1e-6))
    df['rd_intensity']   =  df['xrdq'].fillna(0) / df['revtq'].replace(0, np.nan)
    delta_base = ['gross_margin','net_margin','roa','roe','debt_to_equity',
                  'current_ratio','asset_turnover','rev_growth','pe_ratio','pb_ratio']
    for col in delta_base:
        df[f'delta_{col}'] = df.groupby('gvkey')[col].diff()
    return df

ratio_cols = [
    'gross_margin','net_margin','roa','roe','debt_to_equity','current_ratio',
    'asset_turnover','rev_growth','earnings_growth','pe_ratio','pb_ratio',
    'ebitda_margin','log_mkvalt','rd_intensity',
    'delta_gross_margin','delta_net_margin','delta_roa','delta_roe',
    'delta_debt_to_equity','delta_current_ratio','delta_asset_turnover',
    'delta_rev_growth','delta_pe_ratio','delta_pb_ratio',
]

def vif_filter(X, threshold=2.5):
    cols = list(X.columns)
    while True:
        vif_vals = [variance_inflation_factor(X[cols].values, i) for i in range(len(cols))]
        max_vif  = max(vif_vals)
        if max_vif < threshold:
            break
        cols.pop(int(np.argmax(vif_vals)))
    return cols

gics['gvkey']    = gics['gvkey'].astype(str)
comp_raw         = build_features(comp_raw)
comp_raw['gvkey']= comp_raw['gvkey'].astype(str)
comp_raw         = comp_raw.merge(gics[['gvkey','sector_name']], on='gvkey', how='left')

merged = comp_raw.merge(
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

train_df   = merged[merged['cal_quarter'] <= '2024Q4'].copy()
cs_train   = train_df[train_df['sector_name'] == 'Communication Services'].copy()

print(f"\nTraining observations (Communication Services): {len(cs_train)}")

winsor_bounds = {}
train_medians = {}
for col in ratio_cols:
    if col not in cs_train.columns:
        continue
    lo = cs_train[col].quantile(0.01)
    hi = cs_train[col].quantile(0.99)
    winsor_bounds[col] = (lo, hi)
    cs_train[col]      = cs_train[col].clip(lo, hi)
    train_medians[col] = cs_train[col].median()

available = [c for c in ratio_cols if c in cs_train.columns]
cs_clean  = cs_train[available + ['outperformer_next']].dropna()
X_tr      = cs_clean[available]
y_tr      = cs_clean['outperformer_next']

print(f"Clean training samples: {len(cs_clean)}")
print(f"Outperformer rate in training: {y_tr.mean()*100:.1f}%")

kept     = vif_filter(X_tr)
scaler   = StandardScaler()
X_sc     = scaler.fit_transform(X_tr[kept])
pca      = PCA(n_components=0.95, random_state=42)
X_pca    = pca.fit_transform(X_sc)
clf      = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
clf.fit(X_pca, y_tr)

train_probs = clf.predict_proba(X_pca)[:, 1]
threshold   = np.percentile(train_probs, 50)

print(f"Features after VIF filter: {len(kept)}")
print(f"PCA components (95% variance): {X_pca.shape[1]}")

crsp_2025['gvkey']  = crsp_2025['gvkey'].astype(str)
crsp_2025_sub       = crsp_2025[['gvkey','cal_qtr','q_return','sp500_q_return','Outperform']].copy()
crsp_2025_sub       = crsp_2025_sub.rename(columns={
    'q_return': 'actual_return', 'sp500_q_return': 'spy_return', 'Outperform': 'outperformer_next'
})

comp_2025['gvkey']  = comp_2025['gvkey'].astype(str)
comp_2025f          = build_features(comp_2025)
comp_2025f['gvkey'] = comp_2025f['gvkey'].astype(str)
comp_2025f          = comp_2025f.merge(gics[['gvkey','sector_name']], on='gvkey', how='left')
cs_2025             = comp_2025f[comp_2025f['sector_name'] == 'Communication Services'].copy()

for col in ratio_cols:
    if col in cs_2025.columns and col in winsor_bounds:
        lo, hi = winsor_bounds[col]
        cs_2025[col] = cs_2025[col].clip(lo, hi)

test_quarters  = [(1,2),(2,3),(3,4)]
quarter_labels = {2:'2025-Q2', 3:'2025-Q3', 4:'2025-Q4'}
all_preds      = []
portfolio_perf = []

print("\n── 2025 QUARTER-BY-QUARTER RESULTS ──────────────────────────")
for feat_qtr, label_qtr in test_quarters:
    comp_test = cs_2025[cs_2025['quarter'] == feat_qtr].copy()
    crsp_sub  = crsp_2025_sub[crsp_2025_sub['cal_qtr'] == label_qtr].copy()
    if comp_test.empty or crsp_sub.empty:
        continue

    spy_return = crsp_sub['spy_return'].iloc[0]
    q_label    = quarter_labels[label_qtr]

    test_raw   = comp_test.merge(
        crsp_sub[['gvkey','outperformer_next','actual_return','spy_return']],
        on='gvkey', how='inner'
    )
    if test_raw.empty:
        print(f"\n  {q_label}: no matching stocks found")
        continue

    avail_kept = [c for c in kept if c in test_raw.columns]
    if len(avail_kept) < len(kept):
        continue

    for col in avail_kept:
        test_raw[col] = test_raw[col].fillna(train_medians.get(col, 0))

    X_te_sc   = scaler.transform(test_raw[kept])
    X_te_pca  = pca.transform(X_te_sc)
    probs     = clf.predict_proba(X_te_pca)[:, 1]
    preds     = (probs >= threshold).astype(int)

    test_raw['prob_outperform'] = probs.round(4)
    test_raw['predicted']       = preds
    test_raw['predicted_label'] = preds
    test_raw['label_quarter']   = q_label
    test_raw['feature_quarter'] = f"2025-Q{feat_qtr}"
    all_preds.append(test_raw)

    pred_out    = test_raw[test_raw['predicted'] == 1]
    pred_und    = test_raw[test_raw['predicted'] == 0]
    acc         = (preds == test_raw['outperformer_next'].values).mean() * 100
    port_return = pred_out['actual_return'].mean() if len(pred_out) > 0 else np.nan
    beat_spy    = port_return > spy_return if not np.isnan(port_return) else False

    print(f"\n  {q_label}  |  SPY: {spy_return*100:+.2f}%")
    print(f"    Stocks evaluated      : {len(test_raw)}")
    print(f"    Predicted outperformers : {len(pred_out)}")
    print(f"    Predicted underperformers: {len(pred_und)}")
    print(f"    Classification accuracy: {acc:.1f}%")
    print(f"    Model portfolio return : {port_return*100:+.2f}%")
    print(f"    SPY return             : {spy_return*100:+.2f}%")
    print(f"    Alpha vs SPY           : {(port_return-spy_return)*100:+.2f}%  {'▲ BEATS SPY' if beat_spy else '▼ TRAILS SPY'}")

    print(f"\n    Predicted Outperformers:")
    for _, row in pred_out.sort_values('prob_outperform', ascending=False).iterrows():
        actual_lbl = 'Outperformer' if row['outperformer_next']==1 else 'Underperformer'
        correct    = '✓' if (row['predicted']==row['outperformer_next']) else '✗'
        print(f"      {correct} {str(row.get('tic','')):<8} {str(row.get('conm','')):<35} P={row['prob_outperform']:.3f}  Actual={actual_lbl}  Return={row['actual_return']*100:+.2f}%")

    print(f"\n    Predicted Underperformers:")
    for _, row in pred_und.sort_values('prob_outperform').iterrows():
        actual_lbl = 'Outperformer' if row['outperformer_next']==1 else 'Underperformer'
        correct    = '✓' if (row['predicted']==row['outperformer_next']) else '✗'
        print(f"      {correct} {str(row.get('tic','')):<8} {str(row.get('conm','')):<35} P={row['prob_outperform']:.3f}  Actual={actual_lbl}  Return={row['actual_return']*100:+.2f}%")

    portfolio_perf.append({
        'Quarter': q_label,
        'N_Stocks': len(test_raw),
        'N_Predicted_Outperformers': len(pred_out),
        'N_Predicted_Underperformers': len(pred_und),
        'Accuracy_Pct': round(acc, 2),
        'Model_Portfolio_Return_Pct': round(port_return*100, 4),
        'SPY_Return_Pct': round(spy_return*100, 4),
        'Alpha_vs_SPY_Pct': round((port_return-spy_return)*100, 4),
        'Beat_SPY': beat_spy,
    })

if all_preds:
    final_df = pd.concat(all_preds, ignore_index=True)
    final_df['predicted_label'] = final_df['predicted'].map({1:'Outperformer',0:'Underperformer'})
    final_df['actual_label']    = final_df['outperformer_next'].map({1:'Outperformer',0:'Underperformer'})
    final_df['correct']         = (final_df['predicted'] == final_df['outperformer_next']).astype(int)
    out_cols = ['label_quarter','feature_quarter','tic','conm','sector_name',
                'predicted_label','actual_label','correct','prob_outperform','actual_return','spy_return']
    out_cols = [c for c in out_cols if c in final_df.columns]
    final_df = final_df[out_cols].rename(columns={
        'tic':'Ticker','conm':'Company','sector_name':'Sector',
        'predicted_label':'Predicted','actual_label':'Actual','correct':'Correct',
        'prob_outperform':'P(Outperform)','actual_return':'Actual_Return',
        'spy_return':'SPY_Return','label_quarter':'Label_Quarter',
        'feature_quarter':'Feature_Quarter'
    })
    final_df.to_csv('comms_services_predictions_2025.csv', index=False)
    print(f"\n  Saved → comms_services_predictions_2025.csv")

if portfolio_perf:
    perf_df = pd.DataFrame(portfolio_perf)
    perf_df.to_csv('comms_services_portfolio_vs_spy_2025.csv', index=False)
    beats     = perf_df['Beat_SPY'].sum()
    avg_alpha = perf_df['Alpha_vs_SPY_Pct'].mean()
    avg_acc   = perf_df['Accuracy_Pct'].mean()
    print("\n" + "="*68)
    print("  COMMUNICATION SERVICES — FINAL SUMMARY vs S&P 500")
    print("="*68)
    for _, row in perf_df.iterrows():
        symbol = "▲ BEATS" if row['Beat_SPY'] else "▼ TRAILS"
        print(f"  {row['Quarter']}: Model {row['Model_Portfolio_Return_Pct']:+.2f}%  vs  SPY {row['SPY_Return_Pct']:+.2f}%  |  Alpha {row['Alpha_vs_SPY_Pct']:+.2f}%  {symbol}  |  Acc {row['Accuracy_Pct']:.1f}%")
    print(f"\n  Quarters beating SPY : {beats}/{len(perf_df)}")
    print(f"  Average accuracy     : {avg_acc:.1f}%")
    print(f"  Average alpha vs SPY : {avg_alpha:+.2f}% per quarter")
    print(f"\n  Saved → comms_services_portfolio_vs_spy_2025.csv")
    print("="*68)

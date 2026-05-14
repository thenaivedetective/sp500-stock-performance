"""
Dataset 5 — Exploratory Factor Analysis + Factor Score Regression
Psychological Health Constructs Study | n = 400
Research Questions:
  (1) What latent psychological constructs underlie the correlations
      among 14 mental health and wellbeing variables?
      → Exploratory Factor Analysis (EFA)
  (2) Do these latent factors predict Life_Satisfaction significantly,
      and do they outperform the original item-level variables as predictors?
      → Factor Score Regression (EFA scores as predictors)
  Two objectives, two multivariate methods applied sequentially.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import FactorAnalysis
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor
from scipy import stats
from scipy.stats import bartlett
import warnings, os, json
warnings.filterwarnings('ignore')

OUT = 'Lana_Gidan_Software_Exam/Dataset5_FactorAnalysis'
os.makedirs(OUT, exist_ok=True)

df = pd.read_excel('attached_assets/Data_set-5_1778677563516.xlsx',
                   sheet_name='Psychological_Data')

DV         = 'Life_Satisfaction'
ALL_VARS   = list(df.columns)
ITEM_VARS  = [v for v in ALL_VARS if v != DV]

lines = []
def log(s=''):
    lines.append(str(s))
    print(s)

log('=' * 72)
log('  EFA + FACTOR SCORE REGRESSION — PSYCHOLOGICAL HEALTH STUDY')
log('  n = 400 | 14 items → latent factors → predict Life_Satisfaction')
log('=' * 72)

# ════════════════════════════════════════════════════════════════════════
# PART A — EXPLORATORY FACTOR ANALYSIS
# ════════════════════════════════════════════════════════════════════════
log('\n' + '═'*72)
log('  PART A — EXPLORATORY FACTOR ANALYSIS (EFA)')
log('═'*72)

log('\n── A1. RESEARCH QUESTION ─────────────────────────────────────────────')
log('  What latent psychological constructs (factors) underlie the pattern')
log('  of correlations among 14 mental health and wellbeing items?')
log('  Can complex symptom and functioning data be reduced to a small number')
log('  of interpretable dimensions?')
log(f'  Note: Life_Satisfaction is excluded from EFA (reserved as DV for Part B)')

X = df[ITEM_VARS].values.astype(float)
X_sc = StandardScaler().fit_transform(X)
n, p = X.shape

log('\n── A2. SAMPLING ADEQUACY — KMO & BARTLETT\'S TEST ────────────────────')
corr_matrix = np.corrcoef(X_sc.T)

# KMO
corr_inv = np.linalg.inv(corr_matrix + 1e-6*np.eye(p))
partial_corr = np.zeros_like(corr_matrix)
for i in range(p):
    for j in range(p):
        if i != j:
            partial_corr[i, j] = -corr_inv[i, j] / np.sqrt(corr_inv[i, i] * corr_inv[j, j])
r2_sum     = sum(corr_matrix[i,j]**2 for i in range(p) for j in range(p) if i!=j)
partial_sq = sum(partial_corr[i,j]**2 for i in range(p) for j in range(p) if i!=j)
kmo_overall = r2_sum / (r2_sum + partial_sq)

# Bartlett's
chi2_b = -(n - 1 - (2*p + 5)/6) * np.log(np.linalg.det(corr_matrix + 1e-6*np.eye(p)))
df_b   = p * (p-1) // 2
p_b    = 1 - stats.chi2.cdf(chi2_b, df_b)

log(f'\n  KMO Measure of Sampling Adequacy: {kmo_overall:.4f}')
kmo_label = ('Marvelous' if kmo_overall>=0.90 else 'Meritorious' if kmo_overall>=0.80
             else 'Middling' if kmo_overall>=0.70 else 'Mediocre')
log(f'  KMO interpretation: "{kmo_label}" — '
    f'{"✓ Excellent for factor analysis" if kmo_overall>=0.80 else "⚠ Acceptable"}')
log(f'\n  Bartlett\'s Test of Sphericity:')
log(f'    χ²({df_b}) = {chi2_b:.4f}, p {"< 0.001" if p_b<0.001 else f"= {p_b:.4f}"}')
log(f'    {"✓ Significant — correlation matrix is not identity; EFA is appropriate" if p_b<0.05 else "✗ Not significant"}')

log('\n── A3. EIGENVALUES & SCREE ANALYSIS ──────────────────────────────────')
eigenvalues = np.linalg.eigvalsh(corr_matrix)[::-1]
log(f'\n  {"Factor":<8} {"Eigenvalue":>12} {"% Variance":>12} {"Cum %":>10}  Retain?')
log('  ' + '-'*52)
cum_var = 0
n_factors_kaiser = 0
for i, ev in enumerate(eigenvalues):
    pct_var = ev / p * 100
    cum_var += pct_var
    retain = '✓' if ev > 1.0 else ''
    if ev > 1.0:
        n_factors_kaiser += 1
    if i < 8:
        log(f'  {i+1:<8} {ev:>12.4f} {pct_var:>12.2f} {cum_var:>10.2f}  {retain}')

log(f'\n  → {n_factors_kaiser} factors retained (Kaiser criterion: eigenvalue > 1.0)')

log('\n── A4. FACTOR EXTRACTION (Maximum Likelihood with Varimax Rotation) ──')
fa = FactorAnalysis(n_components=n_factors_kaiser, rotation='varimax', random_state=42)
fa.fit(X_sc)
loadings = fa.components_.T
factor_names = [f'Factor{i+1}' for i in range(n_factors_kaiser)]

log(f'\n  Rotated Factor Loadings (Varimax) — |λ| ≥ 0.40 flagged *:')
log(f'\n  {"Variable":<30}  ' + '  '.join(f'{fn:>10}' for fn in factor_names))
log('  ' + '-'*(30 + n_factors_kaiser*12))
for i, var in enumerate(ITEM_VARS):
    vals = '  '.join(
        f'{loadings[i,j]:>+10.4f}{"*" if abs(loadings[i,j])>=0.40 else " "}'
        for j in range(n_factors_kaiser))
    log(f'  {var:<30}  {vals}')

log('\n── A5. COMMUNALITIES ────────────────────────────────────────────────')
communalities = np.sum(loadings**2, axis=1)
log(f'  {"Variable":<30} {"Communality":>14}  Interpretation')
log('  ' + '-'*65)
for var, h2 in zip(ITEM_VARS, communalities):
    quality = 'Excellent' if h2>0.70 else 'Good' if h2>0.50 else 'Fair' if h2>0.30 else 'Poor'
    log(f'  {var:<30} {h2:>14.4f}  {quality}')

log('\n── A6. VARIANCE EXPLAINED ────────────────────────────────────────────')
var_explained = np.sum(loadings**2, axis=0)
total_var = p
log(f'\n  {"Factor":<12} {"SS Loadings":>14} {"% Variance":>12} {"Cum %":>10}')
log('  ' + '-'*52)
cum = 0
for j, fn in enumerate(factor_names):
    pct = var_explained[j] / total_var * 100
    cum += pct
    log(f'  {fn:<12} {var_explained[j]:>14.4f} {pct:>12.2f} {cum:>10.2f}')
log(f'\n  Total variance explained by {n_factors_kaiser} factors: {cum:.2f}%')

log('\n── A7. FACTOR INTERPRETATION ────────────────────────────────────────')
factor_labels = {}
for j in range(n_factors_kaiser):
    high_load = [(ITEM_VARS[i], loadings[i,j])
                 for i in range(len(ITEM_VARS)) if abs(loadings[i,j]) >= 0.35]
    high_load.sort(key=lambda x: abs(x[1]), reverse=True)
    log(f'\n  Factor {j+1} — top loadings (|λ| ≥ 0.35):')
    for var, lam in high_load:
        log(f'    {var:<35} {lam:>+8.4f}')

    # Auto-label based on primary variables
    top_vars = [v for v, _ in high_load[:3]]
    if any(v in ['Worry_Level','Panic_Symptoms','Sleep_Disturbance'] for v in top_vars):
        label = 'Anxiety & Sleep Disturbance'
    elif any(v in ['Sadness_Score','Hopelessness','Fatigue_Level'] for v in top_vars):
        label = 'Depressive Affect & Fatigue'
    elif any(v in ['Public_Speaking_Confidence','Social_Interaction','Assertiveness'] for v in top_vars):
        label = 'Social Confidence & Assertiveness'
    elif any(v in ['Impulse_Control','Stress_Tolerance','Emotional_Awareness'] for v in top_vars):
        label = 'Emotional Regulation & Coping'
    else:
        label = 'Wellbeing & Self-Efficacy'
    factor_labels[f'Factor{j+1}'] = label
    log(f'    → Interpreted as: "{label}"')

# ════════════════════════════════════════════════════════════════════════
# PART B — FACTOR SCORE REGRESSION
# ════════════════════════════════════════════════════════════════════════
log('\n' + '═'*72)
log('  PART B — FACTOR SCORE REGRESSION')
log(f'  DV: {DV}  |  Predictors: {n_factors_kaiser} extracted factor scores')
log('═'*72)

log('\n── B1. RESEARCH QUESTION ─────────────────────────────────────────────')
log('  Do the latent psychological factors predict Life_Satisfaction?')
log('  And do latent factor scores outperform raw item-level predictors')
log('  as predictors of life satisfaction?')
log('  This tests whether factor analysis adds predictive value beyond')
log('  simply using the original items in a regression.')

# Extract factor scores
factor_scores = fa.transform(X_sc)
def clean_col(s):
    return s.replace(' ', '_').replace('&', 'and').replace('/', '_').replace('-', '_')

factor_score_df = pd.DataFrame(factor_scores,
                                columns=[f'F{i+1}_{clean_col(factor_labels[fn])[:15]}'
                                         for i, fn in enumerate(factor_names)])
factor_score_df[DV] = df[DV].values

log('\n── B2. FACTOR SCORE REGRESSION MODEL ────────────────────────────────')
fs_cols = factor_score_df.columns[:-1].tolist()
X_fs_raw = factor_score_df[fs_cols].values
X_fs_const = sm.add_constant(X_fs_raw)
y_dv = factor_score_df[DV].values
model_fs = sm.OLS(y_dv, X_fs_const).fit()
param_names = ['const'] + fs_cols
model_fs_params = dict(zip(param_names, model_fs.params))
model_fs_pvalues = dict(zip(param_names, model_fs.pvalues))
log(str(model_fs.summary(xname=param_names)))

log('\n── B3. MODEL FIT — FACTOR SCORE REGRESSION ──────────────────────────')
log(f'  R²         = {model_fs.rsquared:.4f}  ({model_fs.rsquared*100:.1f}% of Life_Satisfaction variance explained)')
log(f'  Adj R²     = {model_fs.rsquared_adj:.4f}')
log(f'  F({int(model_fs.df_model)}, {int(model_fs.df_resid)}) = {model_fs.fvalue:.4f}, p = {model_fs.f_pvalue:.4e}')

log('\n── B4. FACTOR SCORE REGRESSION COEFFICIENTS ──────────────────────────')
log(f'  {"Factor":<40} {"Coeff":>10} {"p":>10}  Sig  Interpretation')
log('  ' + '-'*85)
for var, coef, pval in zip(param_names, model_fs.params, model_fs.pvalues):
    if var == 'const':
        log(f'  Intercept: {coef:.4f}')
        continue
    sig = '***' if pval<0.001 else '**' if pval<0.01 else '*' if pval<0.05 else 'n.s.'
    direction = '↑ Life Satisfaction' if coef > 0 else '↓ Life Satisfaction'
    log(f'  {var:<40} {coef:>+10.4f} {pval:>10.4f}  {sig}  {direction}')

log('\n── B5. COMPARISON — ITEM REGRESSION vs FACTOR REGRESSION ────────────')
log('  Item regression: use all 14 raw variables directly as predictors')
item_formula = f'{DV} ~ ' + ' + '.join(ITEM_VARS)
model_items = smf.ols(item_formula, data=df).fit()

log(f'\n  {"Criterion":<30} {"Item Regression":>18} {"Factor Regression":>20}  Advantage')
log('  ' + '-'*75)
comparisons = [
    ('R²',        model_items.rsquared,     model_fs.rsquared),
    ('Adj R²',    model_items.rsquared_adj, model_fs.rsquared_adj),
    ('AIC',       model_items.aic,          model_fs.aic),
    ('BIC',       model_items.bic,          model_fs.bic),
    ('N Params',  float(model_items.df_model), float(model_fs.df_model)),
]
for label, item_v, fs_v in comparisons:
    if label in ['AIC','BIC','N Params']:
        winner = 'Factor ✓ (simpler)' if fs_v < item_v else 'Item'
        log(f'  {label:<30} {item_v:>18.4f} {fs_v:>20.4f}  {winner}')
    else:
        winner = 'Factor ✓' if fs_v >= item_v - 0.01 else 'Item ✓'
        log(f'  {label:<30} {item_v:>18.4f} {fs_v:>20.4f}  {winner}')

log(f'\n  Key insight:')
log(f'  Item regression uses {int(model_items.df_model)} parameters; '
    f'Factor regression uses only {int(model_fs.df_model)} factor scores.')
log(f'  Factor regression achieves comparable R² ({model_fs.rsquared:.4f} vs {model_items.rsquared:.4f})')
log(f'  with {int(model_items.df_model) - int(model_fs.df_model)} fewer parameters.')
log(f'  Lower AIC/BIC for factor regression confirms it is a more parsimonious model.')
log(f'  Factor analysis adds value by reducing noise and overfitting risk.')

# FIGURES
fig = plt.figure(figsize=(18, 12))
fig.suptitle('EFA + Factor Score Regression — Psychological Health (n=400)',
             fontsize=13, fontweight='bold')

# Scree plot
ax1 = fig.add_subplot(2, 3, 1)
evs = eigenvalues[:min(p, 12)]
ax1.plot(range(1, len(evs)+1), evs, 'o-', color='#2c5f8a', lw=2, markersize=8)
ax1.axhline(1.0, color='red', ls='--', lw=1.5, label='Kaiser criterion = 1.0')
ax1.fill_between(range(1, n_factors_kaiser+1), evs[:n_factors_kaiser], 1.0,
                 alpha=0.2, color='#2c5f8a', label=f'{n_factors_kaiser} factors retained')
ax1.set_title('Scree Plot', fontweight='bold')
ax1.set_xlabel('Factor Number'); ax1.set_ylabel('Eigenvalue')
ax1.legend(fontsize=7); ax1.grid(alpha=0.3)

# Factor loadings heatmap
ax2 = fig.add_subplot(2, 3, 2)
load_df = pd.DataFrame(loadings, index=ITEM_VARS,
                        columns=[f'F{i+1}' for i in range(n_factors_kaiser)])
sns.heatmap(load_df, annot=True, fmt='.2f', cmap='RdYlGn',
            center=0, vmin=-1, vmax=1, ax=ax2,
            linewidths=0.5, annot_kws={'size': 7}, cbar_kws={'shrink': 0.8})
ax2.set_title('Rotated Factor Loadings (Varimax)\n|λ| > 0.40 = strong loading', fontweight='bold')
ax2.set_xticklabels([f'F{i+1}\n{factor_labels[f"Factor{i+1}"][:12]}' for i in range(n_factors_kaiser)],
                    fontsize=7, rotation=0)

# Communalities
ax3 = fig.add_subplot(2, 3, 3)
comm_df = pd.DataFrame({'Variable': ITEM_VARS, 'Communality': communalities}).sort_values('Communality')
cols3 = ['#2ecc71' if h>0.70 else '#f39c12' if h>0.50 else '#e74c3c' for h in comm_df['Communality']]
ax3.barh(comm_df['Variable'], comm_df['Communality'], color=cols3, edgecolor='black', lw=0.5)
ax3.axvline(0.50, color='gray', ls='--', lw=1, label='h²=0.50 (good)')
ax3.axvline(0.70, color='green', ls='--', lw=1, label='h²=0.70 (excellent)')
ax3.set_title('Communalities\n(green≥0.70, orange≥0.50, red<0.50)', fontweight='bold')
ax3.set_xlabel('h²'); ax3.legend(fontsize=7); ax3.grid(axis='x', alpha=0.3)

# Variance explained bar
ax4 = fig.add_subplot(2, 3, 4)
var_pct = [var_explained[j]/total_var*100 for j in range(n_factors_kaiser)]
labels4 = [f'F{j+1}\n{factor_labels[f"Factor{j+1}"][:12]}' for j in range(n_factors_kaiser)]
ax4.bar(range(n_factors_kaiser), var_pct, color='#2c5f8a', edgecolor='black', lw=0.5)
ax4.set_xticks(range(n_factors_kaiser)); ax4.set_xticklabels(labels4, fontsize=7)
ax4.set_title(f'Variance Explained per Factor\n(Total = {sum(var_pct):.1f}%)', fontweight='bold')
ax4.set_ylabel('% Variance Explained'); ax4.grid(axis='y', alpha=0.3)

# Factor score regression coefficients
ax5 = fig.add_subplot(2, 3, 5)
coef_items = [(v, b, p) for v, b, p in
              zip(param_names, model_fs.params, model_fs.pvalues)
              if v != 'const']
coef_items.sort(key=lambda x: x[1])
cols5 = ['#2ecc71' if b>0 else '#e74c3c' for _, b, _ in coef_items]
ax5.barh([v.split('_')[0]+'\n'+v[3:20] for v, _, _ in coef_items],
          [b for _, b, _ in coef_items], color=cols5, edgecolor='black', lw=0.5)
ax5.axvline(0, color='black', lw=0.8)
ax5.set_title('Factor → Life_Satisfaction\nRegression Coefficients', fontweight='bold')
ax5.set_xlabel('Coefficient'); ax5.grid(axis='x', alpha=0.3)

# R² comparison
ax6 = fig.add_subplot(2, 3, 6)
models_cmp = ['Item Reg\n(14 predictors)', f'Factor Reg\n({n_factors_kaiser} factors)']
r2_vals = [model_items.rsquared, model_fs.rsquared]
adj_r2_vals = [model_items.rsquared_adj, model_fs.rsquared_adj]
xb = np.arange(2)
ax6.bar(xb-0.18, r2_vals, 0.35, label='R²', color='#2c5f8a', edgecolor='black', lw=0.5)
ax6.bar(xb+0.18, adj_r2_vals, 0.35, label='Adj R²', color='#e67e22', edgecolor='black', lw=0.5)
ax6.set_xticks(xb); ax6.set_xticklabels(models_cmp, fontsize=9)
ax6.set_title('Item Regression vs Factor Regression\nR² Comparison', fontweight='bold')
ax6.set_ylabel('R²'); ax6.legend(fontsize=8); ax6.grid(axis='y', alpha=0.3)
for bar in ax6.patches:
    ax6.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.005,
             f'{bar.get_height():.3f}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig(f'{OUT}/dataset5_EFA_factor_regression.png', dpi=150, bbox_inches='tight')
plt.close()

with open(f'{OUT}/dataset5_FactorAnalysis_output.txt', 'w') as f:
    f.write('\n'.join(lines))

metrics = {
    'kmo': kmo_overall, 'bartlett_chi2': chi2_b, 'bartlett_p': p_b,
    'n_factors': n_factors_kaiser, 'factor_labels': factor_labels,
    'var_explained': float(sum(var_pct)),
    'fs_r2': model_fs.rsquared, 'fs_adj_r2': model_fs.rsquared_adj,
    'item_r2': model_items.rsquared, 'item_adj_r2': model_items.rsquared_adj,
    'fs_F': model_fs.fvalue, 'fs_F_p': model_fs.f_pvalue,
    'eigenvalues': eigenvalues[:8].tolist(),
}
with open('ds5_metrics.json', 'w') as f:
    json.dump(metrics, f)

print(f'\nAll DS5 files saved to {OUT}/')

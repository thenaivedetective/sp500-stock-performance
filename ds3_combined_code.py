"""
Dataset 3 — Multiple Regression + Path Analysis (Mediation)
Academic Performance Study | n = 150 students
Research Questions:
  (1) Which academic behaviors independently predict final exam score?
      → Multiple Linear Regression
  (2) Does stress mediate the relationship between study effort and
      exam performance? Do study hours and practice tests affect
      performance directly, or partly through elevated/reduced stress?
      → Path Analysis (Baron & Kenny mediation + Sobel test)
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_breuschpagan
from scipy import stats
import warnings, os, json
warnings.filterwarnings('ignore')

OUT = 'Lana_Gidan_Software_Exam/Dataset3_MultipleRegression'
os.makedirs(OUT, exist_ok=True)

df = pd.read_excel('attached_assets/Data_set-3_1778677563522.xlsx',
                   sheet_name='Regression_Data')

PREDS  = ['Study_Hours', 'Attendance_Rate', 'Sleep_Hours', 'Stress_Level', 'Practice_Tests']
DV     = 'Final_Exam_Score'
MED    = 'Stress_Level'

lines = []
def log(s=''):
    lines.append(str(s))
    print(s)

log('=' * 72)
log('  MULTIPLE REGRESSION + PATH ANALYSIS — ACADEMIC PERFORMANCE STUDY')
log('  n = 150 students | DV: Final_Exam_Score')
log('=' * 72)

# ════════════════════════════════════════════════════════════════════════
# PART A — MULTIPLE REGRESSION
# ════════════════════════════════════════════════════════════════════════
log('\n' + '═'*72)
log('  PART A — MULTIPLE LINEAR REGRESSION')
log('═'*72)

log('\n── A1. RESEARCH QUESTION ─────────────────────────────────────────────')
log('  Which academic behaviors (study hours, attendance, sleep, stress,')
log('  practice tests) independently and collectively predict final exam')
log('  performance, and what is the unique contribution of each?')

log('\n── A2. DESCRIPTIVE STATISTICS & CORRELATIONS ────────────────────────')
log(df[PREDS + [DV]].describe().round(3).to_string())
log('\n  Bivariate correlations with Final_Exam_Score:')
log(f'  {"Variable":<25} {"r":>8} {"p":>10}  Direction')
log('  ' + '-'*55)
for pred in PREDS:
    r, p = stats.pearsonr(df[pred], df[DV])
    direction = 'Positive — more → better' if r > 0 else 'Negative — more → worse'
    log(f'  {pred:<25} {r:>+8.4f} {p:>10.4f}  {direction}')

log('\n── A3. MODEL SPECIFICATION ───────────────────────────────────────────')
df['Sleep_Sq'] = df['Sleep_Hours'] ** 2
formula = f'{DV} ~ Study_Hours + Attendance_Rate + Sleep_Hours + Sleep_Sq + Stress_Level + Practice_Tests'
model = smf.ols(formula, data=df).fit()
log(f'  Model: {DV} ~ Study_Hours + Attendance_Rate + Sleep_Hours')
log('         + Sleep_Hours² + Stress_Level + Practice_Tests')
log('  Note: Sleep included as quadratic term — U-shaped relationship')
log('        (too little AND too much sleep both hurt performance)')

log('\n── A4. REGRESSION RESULTS ────────────────────────────────────────────')
log(str(model.summary()))

log('\n── A5. MODEL FIT ─────────────────────────────────────────────────────')
log(f'  R²         = {model.rsquared:.4f}  ({model.rsquared*100:.1f}% of variance explained)')
log(f'  Adj R²     = {model.rsquared_adj:.4f}')
log(f'  F({int(model.df_model)}, {int(model.df_resid)}) = {model.fvalue:.4f}, p = {model.f_pvalue:.4e}')
log(f'  AIC        = {model.aic:.2f}')
log(f'  BIC        = {model.bic:.2f}')
log(f'  N          = {int(model.nobs)}')

log('\n── A6. COEFFICIENT INTERPRETATION ───────────────────────────────────')
for var, coef, pval in zip(model.params.index, model.params, model.pvalues):
    if var == 'Intercept':
        log(f'  Intercept: {coef:.4f} — predicted score when all predictors = 0')
        continue
    sig = '(p < 0.001) ***' if pval < 0.001 else f'(p = {pval:.4f}) **' if pval < 0.01 else f'(p = {pval:.4f}) *' if pval < 0.05 else f'(p = {pval:.4f}) n.s.'
    if var == 'Study_Hours':
        log(f'  Study_Hours:     +{coef:.3f} per hour {sig} — strongest positive predictor')
        log(f'    Going from 4 hrs to 12 hrs study = +{coef*(12-4):.1f} exam points')
    elif var == 'Attendance_Rate':
        log(f'  Attendance_Rate: +{coef:.3f} per % {sig}')
        log(f'    Every 10% more attendance = +{coef*10:.1f} exam points')
    elif var == 'Sleep_Hours':
        log(f'  Sleep_Hours:     {coef:+.3f} (linear term) {sig}')
    elif var == 'Sleep_Sq':
        log(f'  Sleep_Hours²:    {coef:+.3f} (quadratic term) {sig}')
        opt_sleep = -model.params['Sleep_Hours'] / (2 * model.params['Sleep_Sq'])
        log(f'    Optimal sleep hours = {opt_sleep:.2f} hrs (peak of quadratic curve)')
    elif var == 'Stress_Level':
        log(f'  Stress_Level:    {coef:+.3f} per unit {sig}')
        log(f'    Each stress unit increase = {coef:.3f} points (performance cost of stress)')
    elif var == 'Practice_Tests':
        log(f'  Practice_Tests:  +{coef:.3f} per test {sig}')
        log(f'    Each additional practice test = +{coef:.1f} exam points')

log('\n── A7. STANDARDIZED BETA COEFFICIENTS ───────────────────────────────')
log('  All variables z-scored — directly compare predictor importance:')
df_std = df.copy()
for col in ['Study_Hours', 'Attendance_Rate', 'Sleep_Hours',
            'Sleep_Sq', 'Stress_Level', 'Practice_Tests', DV]:
    df_std[col] = (df[col] - df[col].mean()) / df[col].std()
model_std = smf.ols(formula, data=df_std).fit()
beta_data = [(v, b, p) for v, b, p in
             zip(model_std.params.index, model_std.params, model_std.pvalues)
             if v != 'Intercept']
beta_data.sort(key=lambda x: abs(x[1]), reverse=True)
log(f'\n  {"Rank":<6} {"Variable":<25} {"Std β":>10} {"p":>10}  Relative Importance')
log('  ' + '-'*70)
for rank, (var, beta, pval) in enumerate(beta_data, 1):
    sig = '***' if pval<0.001 else '**' if pval<0.01 else '*' if pval<0.05 else 'n.s.'
    log(f'  {rank:<6} {var:<25} {beta:>+10.4f} {pval:>10.4f}  {sig}')

log('\n── A8. VIF — MULTICOLLINEARITY ───────────────────────────────────────')
X_vif = sm.add_constant(df[['Study_Hours','Attendance_Rate','Sleep_Hours',
                              'Sleep_Sq','Stress_Level','Practice_Tests']])
log(f'  {"Variable":<25} {"VIF":>10}  Verdict')
log('  ' + '-'*50)
for i, col in enumerate(X_vif.columns[1:], 1):
    vif = variance_inflation_factor(X_vif.values, i)
    verdict = '✓ Acceptable' if vif < 10 else '⚠ High (expected for polynomial pair)'
    log(f'  {col:<25} {vif:>10.2f}  {verdict}')
log('  Note: VIF inflated for Sleep_Hours/Sleep_Sq by construction (polynomial pair)')

log('\n── A9. ASSUMPTION DIAGNOSTICS ────────────────────────────────────────')
resid = model.resid
W, p_shap = stats.shapiro(resid)
bp_stat, bp_p, _, _ = het_breuschpagan(resid, model.model.exog)
dw = sm.stats.stattools.durbin_watson(resid)
log(f'  {"Test":<35} {"Stat":>10} {"p":>10}  Verdict')
log('  ' + '-'*65)
log(f'  {"Shapiro-Wilk (normality of residuals)":<35} {W:>10.4f} {p_shap:>10.4f}  '
    f'{"✓ Normal" if p_shap>0.05 else "✗ Non-normal"}')
log(f'  {"Breusch-Pagan (homoscedasticity)":<35} {bp_stat:>10.4f} {bp_p:>10.4f}  '
    f'{"✓ Homoscedastic" if bp_p>0.05 else "✗ Heteroscedastic"}')
log(f'  {"Durbin-Watson (autocorrelation)":<35} {dw:>10.4f} {"—":>10}  '
    f'{"✓ No autocorrelation (1.5-2.5)" if 1.5<dw<2.5 else "⚠ Check autocorrelation"}')

# ════════════════════════════════════════════════════════════════════════
# PART B — PATH ANALYSIS (MEDIATION)
# ════════════════════════════════════════════════════════════════════════
log('\n' + '═'*72)
log('  PART B — PATH ANALYSIS (Mediation Model)')
log('  Mediator: Stress_Level')
log('═'*72)

log('\n── B1. RESEARCH QUESTION ─────────────────────────────────────────────')
log('  Does Stress_Level mediate the relationship between academic behaviors')
log('  and exam performance? Specifically:')
log('    a) Does high Study_Hours reduce Stress_Level?')
log('    b) Does reduced Stress_Level then improve Final_Exam_Score?')
log('    c) Is there a significant indirect effect of Study_Hours on')
log('       Exam_Score that operates THROUGH Stress_Level?')
log('  This path model decomposes total effects into direct + indirect components.')

log('\n── B2. PATH DIAGRAM DESCRIPTION ─────────────────────────────────────')
log('''
  Path Model Structure (Baron & Kenny, 1986):

  Study_Hours ──── path a ────► Stress_Level
        │                              │
        │         path c' (direct)     │ path b
        └──────────────────────────────►──► Final_Exam_Score
                                       ▲
  Practice_Tests ──────────────────────┘ (also modeled)
  Attendance_Rate ─────────────────────┘ (direct paths only)

  Definitions:
    Path a  = effect of Study_Hours on Stress_Level (the IV → Mediator path)
    Path b  = effect of Stress_Level on Exam_Score, controlling for Study_Hours
    Path c  = total effect of Study_Hours on Exam_Score (without mediator)
    Path c' = direct effect of Study_Hours on Exam_Score (controlling for Stress)
    Indirect effect = a × b (the mediated portion of Study_Hours → Score)
''')

PREDICTORS = ['Study_Hours', 'Attendance_Rate', 'Practice_Tests']

log('\n── B3. PATH EQUATIONS ────────────────────────────────────────────────')

path_results = {}

for iv in PREDICTORS:
    log(f'\n  ══ Predictor: {iv} ══')

    # Step 1: Path c — total effect (IV → DV, no mediator)
    m_c = smf.ols(f'{DV} ~ {iv}', data=df).fit()
    c_coef = m_c.params[iv]
    c_p    = m_c.pvalues[iv]

    # Step 2: Path a — IV → Mediator
    m_a = smf.ols(f'{MED} ~ {iv}', data=df).fit()
    a_coef = m_a.params[iv]
    a_p    = m_a.pvalues[iv]
    a_se   = m_a.bse[iv]

    # Step 3: Paths b + c' — IV + Mediator → DV
    m_bc = smf.ols(f'{DV} ~ {iv} + {MED}', data=df).fit()
    b_coef  = m_bc.params[MED]
    b_p     = m_bc.pvalues[MED]
    b_se    = m_bc.bse[MED]
    c_prime = m_bc.params[iv]
    cp_p    = m_bc.pvalues[iv]

    # Indirect effect & Sobel test
    indirect = a_coef * b_coef
    se_sobel = np.sqrt(b_coef**2 * a_se**2 + a_coef**2 * b_se**2)
    z_sobel  = indirect / se_sobel
    p_sobel  = 2 * (1 - stats.norm.cdf(abs(z_sobel)))

    # Bootstrap CI for indirect effect
    boot_indirect = []
    for _ in range(2000):
        idx = np.random.choice(len(df), len(df), replace=True)
        df_b = df.iloc[idx]
        a_b = smf.ols(f'{MED} ~ {iv}', data=df_b).fit().params[iv]
        b_b = smf.ols(f'{DV} ~ {iv} + {MED}', data=df_b).fit().params[MED]
        boot_indirect.append(a_b * b_b)
    ci_lo = np.percentile(boot_indirect, 2.5)
    ci_hi = np.percentile(boot_indirect, 97.5)
    mediation_type = ('Full mediation' if cp_p > 0.05 and c_p < 0.05
                      else 'Partial mediation' if cp_p < 0.05 and c_p < 0.05
                      else 'No mediation' if c_p > 0.05
                      else 'Direct only')

    log(f'  Path c  (total effect):    {iv} → {DV}')
    log(f'    Coef = {c_coef:+.4f}, p = {c_p:.4f}  '
        f'{"sig ***" if c_p<0.001 else "sig **" if c_p<0.01 else "sig *" if c_p<0.05 else "n.s."}')

    log(f'\n  Path a  (IV → mediator):   {iv} → {MED}')
    log(f'    Coef = {a_coef:+.4f}, p = {a_p:.4f}  '
        f'{"sig ***" if a_p<0.001 else "sig **" if a_p<0.01 else "sig *" if a_p<0.05 else "n.s."}')

    log(f'\n  Path b  (mediator → DV):   {MED} → {DV} (controlling for {iv})')
    log(f'    Coef = {b_coef:+.4f}, p = {b_p:.4f}  '
        f'{"sig ***" if b_p<0.001 else "sig **" if b_p<0.01 else "sig *" if b_p<0.05 else "n.s."}')

    log(f'\n  Path c\' (direct effect):   {iv} → {DV} (controlling for {MED})')
    log(f'    Coef = {c_prime:+.4f}, p = {cp_p:.4f}  '
        f'{"sig ***" if cp_p<0.001 else "sig **" if cp_p<0.01 else "sig *" if cp_p<0.05 else "n.s."}')

    log(f'\n  Indirect Effect (a × b):   {indirect:+.4f}')
    log(f'    Sobel Z = {z_sobel:.4f}, p = {p_sobel:.4f}  '
        f'{"sig ***" if p_sobel<0.001 else "sig **" if p_sobel<0.01 else "sig *" if p_sobel<0.05 else "n.s."}')
    log(f'    Bootstrap 95% CI [{ci_lo:+.4f}, {ci_hi:+.4f}]  '
        f'{"Significant — CI excludes 0" if ci_lo*ci_hi > 0 else "Not significant — CI includes 0"}')

    pct_mediated = (indirect / c_coef * 100) if abs(c_coef) > 0.001 else 0
    log(f'\n  Effect decomposition:')
    log(f'    Total effect c:      {c_coef:+.4f}')
    log(f'    Direct effect c\':   {c_prime:+.4f}')
    log(f'    Indirect a×b:        {indirect:+.4f}  ({pct_mediated:.1f}% of total effect)')
    log(f'\n  Mediation type: {mediation_type}')

    path_results[iv] = {
        'c': c_coef, 'c_p': c_p,
        'a': a_coef, 'a_p': a_p,
        'b': b_coef, 'b_p': b_p,
        'c_prime': c_prime, 'cp_p': cp_p,
        'indirect': indirect, 'sobel_p': p_sobel,
        'ci_lo': ci_lo, 'ci_hi': ci_hi,
        'pct_mediated': pct_mediated,
        'type': mediation_type,
    }

log('\n── B4. PATH ANALYSIS SUMMARY ─────────────────────────────────────────')
direct_label = "Direct c'"
log(f'\n  {"Predictor":<20} {"Total c":>10} {direct_label:>12} {"Indirect ab":>13} '
    f'{"% Mediated":>12} {"Sobel p":>10}  Conclusion')
log('  ' + '-'*95)
for iv, r in path_results.items():
    log(f'  {iv:<20} {r["c"]:>+10.4f} {r["c_prime"]:>+12.4f} {r["indirect"]:>+13.4f} '
        f'{r["pct_mediated"]:>12.1f}% {r["sobel_p"]:>10.4f}  {r["type"]}')

# FIGURES
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('Multiple Regression + Path Analysis — Academic Performance (n=150)',
             fontsize=13, fontweight='bold')

# Actual vs Predicted
ax = axes[0, 0]
ax.scatter(model.fittedvalues, df[DV], alpha=0.5, s=20, color='#2c5f8a')
lo = min(model.fittedvalues.min(), df[DV].min())
hi = max(model.fittedvalues.max(), df[DV].max())
ax.plot([lo, hi], [lo, hi], 'r--', lw=1.5, label='Perfect fit')
ax.set_xlabel('Predicted Exam Score'); ax.set_ylabel('Actual Exam Score')
ax.set_title(f'Predicted vs Actual\nR² = {model.rsquared:.4f}', fontweight='bold')
ax.legend(fontsize=8); ax.grid(alpha=0.3)

# Residual plot
ax = axes[0, 1]
ax.scatter(model.fittedvalues, model.resid, alpha=0.5, s=20, color='#e67e22')
ax.axhline(0, color='red', ls='--', lw=1.5)
ax.set_xlabel('Fitted Values'); ax.set_ylabel('Residuals')
ax.set_title('Residuals vs Fitted\n(Test: Homoscedasticity)', fontweight='bold')
ax.grid(alpha=0.3)

# Q-Q plot
ax = axes[0, 2]
stats.probplot(model.resid, plot=ax)
ax.set_title('Q-Q Plot\n(Test: Normality of Residuals)', fontweight='bold')

# Standardized betas
ax = axes[1, 0]
betas = [(v, b) for v, b, _ in beta_data if v != 'Intercept']
betas.sort(key=lambda x: x[1])
cols = ['#e74c3c' if b > 0 else '#3498db' for _, b in betas]
ax.barh([v for v, _ in betas], [b for _, b in betas],
        color=cols, edgecolor='black', lw=0.5)
ax.axvline(0, color='black', lw=0.8)
ax.set_title('Standardized Beta Coefficients\n(Rank Predictor Importance)', fontweight='bold')
ax.set_xlabel('Standardized β'); ax.grid(axis='x', alpha=0.3)

# Path diagram — Study_Hours mediation
ax = axes[1, 1]
ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis('off')
r = path_results['Study_Hours']
ax.annotate('', xy=(5, 5), xytext=(1, 8),
            arrowprops=dict(arrowstyle='->', color='#2c5f8a', lw=2))
ax.annotate('', xy=(9, 5), xytext=(5, 5),
            arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=2))
ax.annotate('', xy=(9, 5), xytext=(1, 8),
            arrowprops=dict(arrowstyle='->', color='#2ecc71', lw=2, linestyle='dashed'))
ax.text(1, 8.4, 'Study_Hours', ha='center', fontsize=9, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='#ddeeff', edgecolor='gray'))
ax.text(5, 5.4, 'Stress_Level\n(Mediator)', ha='center', fontsize=9, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='#ffeedd', edgecolor='gray'))
ax.text(9, 5.4, 'Exam Score', ha='center', fontsize=9, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='#ddeedd', edgecolor='gray'))
ax.text(3, 7.2, f'a={r["a"]:+.3f}', ha='center', fontsize=8, color='#2c5f8a')
ax.text(7, 5.6, f'b={r["b"]:+.3f}', ha='center', fontsize=8, color='#e74c3c')
ax.text(5, 7.5, f'c\'={r["c_prime"]:+.3f} (direct)', ha='center', fontsize=8, color='#2ecc71')
ax.text(5, 3.5, f'Indirect a×b = {r["indirect"]:+.4f} ({r["pct_mediated"]:.1f}% of total)',
        ha='center', fontsize=8.5)
ax.text(5, 2.5, f'Sobel p = {r["sobel_p"]:.4f}  |  Bootstrap CI [{r["ci_lo"]:+.3f}, {r["ci_hi"]:+.3f}]',
        ha='center', fontsize=8)
ax.set_title(f'Study_Hours → Stress → Exam Score\n{r["type"]}', fontweight='bold')

# Indirect effects comparison
ax = axes[1, 2]
ivs_plot = list(path_results.keys())
indir = [path_results[iv]['indirect'] for iv in ivs_plot]
ci_lo_list = [path_results[iv]['ci_lo'] for iv in ivs_plot]
ci_hi_list = [path_results[iv]['ci_hi'] for iv in ivs_plot]
ypos = np.arange(len(ivs_plot))
cols_ie = ['#2c5f8a' if lo*hi > 0 else '#aaaaaa'
           for lo, hi in zip(ci_lo_list, ci_hi_list)]
ax.barh(ypos, indir, color=cols_ie, edgecolor='black', lw=0.5)
for y, lo, hi in zip(ypos, ci_lo_list, ci_hi_list):
    ax.plot([lo, hi], [y, y], color='black', lw=2)
    ax.plot([lo, lo], [y-0.15, y+0.15], color='black', lw=2)
    ax.plot([hi, hi], [y-0.15, y+0.15], color='black', lw=2)
ax.axvline(0, color='black', lw=1, ls='--')
ax.set_yticks(ypos); ax.set_yticklabels(ivs_plot, fontsize=8)
ax.set_xlabel('Indirect Effect (a×b)')
ax.set_title('Indirect Effects via Stress_Level\n95% Bootstrap CI (blue=significant)', fontweight='bold')
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig(f'{OUT}/dataset3_regression_path_analysis.png', dpi=150, bbox_inches='tight')
plt.close()

with open(f'{OUT}/dataset3_RegressionPath_output.txt', 'w') as f:
    f.write('\n'.join(lines))

metrics = {
    'r2': model.rsquared, 'adj_r2': model.rsquared_adj,
    'F': model.fvalue, 'F_p': model.f_pvalue,
    'path': path_results,
    'betas': {v: float(b) for v, b, _ in beta_data},
}
with open('ds3_metrics.json', 'w') as f:
    json.dump(metrics, f)

print(f'\nAll DS3 files saved to {OUT}/')

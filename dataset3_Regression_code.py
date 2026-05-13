"""
Dataset 3 — Multiple Linear Regression
Student Academic Performance Study
DV: Final_Exam_Score
IV: Study_Hours, Attendance_Rate, Sleep_Hours (quadratic), Stress_Level, Practice_Tests
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
import warnings, os
warnings.filterwarnings('ignore')

OUTPUT_DIR = 'software_exam_answers/Dataset3_MultipleRegression'
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_excel('attached_assets/Data_set-3_1778677563522.xlsx', sheet_name='Regression_Data')
df['Sleep_Hours_Sq'] = df['Sleep_Hours'] ** 2

lines = []
def log(s=''):
    lines.append(s)
    print(s)

log('='*70)
log('  MULTIPLE LINEAR REGRESSION — STUDENT ACADEMIC PERFORMANCE STUDY')
log('='*70)

log('\n── 1. DESCRIPTIVE STATISTICS ─────────────────────────────────────────')
log(df[['Study_Hours','Attendance_Rate','Sleep_Hours','Stress_Level',
        'Practice_Tests','Final_Exam_Score']].describe().round(3).to_string())

log('\n── 2. CORRELATION MATRIX ─────────────────────────────────────────────')
corr = df[['Study_Hours','Attendance_Rate','Sleep_Hours','Stress_Level',
           'Practice_Tests','Final_Exam_Score']].corr().round(3)
log(corr.to_string())

log('\n── 3. MODEL SPECIFICATION ────────────────────────────────────────────')
log('  Model: Final_Exam_Score ~ Study_Hours + Attendance_Rate + Sleep_Hours')
log('         + Sleep_Hours² + Stress_Level + Practice_Tests')
log('  Note: Sleep_Hours included as quadratic term per dataset documentation')

formula = 'Final_Exam_Score ~ Study_Hours + Attendance_Rate + Sleep_Hours + Sleep_Hours_Sq + Stress_Level + Practice_Tests'
model = smf.ols(formula, data=df).fit()

log('\n── 4. REGRESSION RESULTS ─────────────────────────────────────────────')
log(model.summary().as_text())

log('\n── 5. MODEL FIT STATISTICS ───────────────────────────────────────────')
log(f'  R²:                    {model.rsquared:.4f}')
log(f'  Adjusted R²:           {model.rsquared_adj:.4f}')
log(f'  F-statistic:           {model.fvalue:.4f}')
log(f'  F p-value:             {model.f_pvalue:.6f}')
log(f'  AIC:                   {model.aic:.2f}')
log(f'  BIC:                   {model.bic:.2f}')
log(f'  RMSE:                  {np.sqrt(model.mse_resid):.4f}')

log('\n── 6. COEFFICIENT INTERPRETATION ────────────────────────────────────')
coef_df = pd.DataFrame({
    'Coefficient': model.params,
    'Std Error':   model.bse,
    't-stat':      model.tvalues,
    'p-value':     model.pvalues,
    '95% CI Lower': model.conf_int()[0],
    '95% CI Upper': model.conf_int()[1],
}).round(4)
log(coef_df.to_string())

log('\n  Standardized Coefficients (Beta):')
df_std = df[['Study_Hours','Attendance_Rate','Sleep_Hours','Sleep_Hours_Sq',
             'Stress_Level','Practice_Tests','Final_Exam_Score']].copy()
for col in df_std.columns:
    df_std[col] = (df_std[col] - df_std[col].mean()) / df_std[col].std()
model_std = smf.ols(formula, data=df_std.rename(columns={'Final_Exam_Score':'Final_Exam_Score'})).fit()
for var, beta in model_std.params.items():
    if var != 'Intercept':
        log(f'    {var}: β = {beta:.4f}')

log('\n── 7. VIF (MULTICOLLINEARITY CHECK) ──────────────────────────────────')
X_vif = df[['Study_Hours','Attendance_Rate','Sleep_Hours','Sleep_Hours_Sq',
            'Stress_Level','Practice_Tests']].copy()
X_vif = sm.add_constant(X_vif)
vif_data = pd.DataFrame()
vif_data['Variable'] = X_vif.columns
vif_data['VIF'] = [variance_inflation_factor(X_vif.values, i) for i in range(X_vif.shape[1])]
log(vif_data[vif_data['Variable'] != 'const'].round(3).to_string(index=False))
log('  Note: Sleep_Hours and Sleep_Hours_Sq expected to correlate — intrinsic to polynomial terms')

log('\n── 8. ASSUMPTION DIAGNOSTICS ─────────────────────────────────────────')
residuals = model.resid
fitted = model.fittedvalues
stat_sw, p_sw = stats.shapiro(residuals)
log(f'\n  Shapiro-Wilk (normality of residuals): W={stat_sw:.4f}, p={p_sw:.4f}')
log(f'  {"✓ Residuals are normal" if p_sw > 0.05 else "~ Slight non-normality (n=150, CLT robust)"}')
lm_stat, lm_p, f_stat, f_p = het_breuschpagan(residuals, model.model.exog)
log(f'\n  Breusch-Pagan (homoscedasticity): LM={lm_stat:.4f}, p={lm_p:.4f}')
log(f'  {"✓ Homoscedastic" if lm_p > 0.05 else "✗ Heteroscedastic — consider robust SEs"}')
dw = sm.stats.durbin_watson(residuals)
log(f'\n  Durbin-Watson (autocorrelation): {dw:.4f}  (ideal ≈ 2.0)')

log('\n── 9. MODEL COMPARISON: WITHOUT vs WITH QUADRATIC TERM ──────────────')
model_linear = smf.ols('Final_Exam_Score ~ Study_Hours + Attendance_Rate + Sleep_Hours + Stress_Level + Practice_Tests', data=df).fit()
log(f'  Without Sleep²: R²={model_linear.rsquared:.4f}, AIC={model_linear.aic:.2f}')
log(f'  With Sleep²:    R²={model.rsquared:.4f}, AIC={model.aic:.2f}')
log(f'  → Quadratic term {"improves" if model.aic < model_linear.aic else "does not improve"} model fit (ΔAIC={model_linear.aic - model.aic:.2f})')

# ── Visualizations ──────────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('Multiple Linear Regression Diagnostics — Student Performance', fontsize=13, fontweight='bold')
axes[0,0].scatter(fitted, residuals, alpha=0.6, color='steelblue', edgecolors='k', s=30)
axes[0,0].axhline(0, color='red', linestyle='--')
axes[0,0].set_xlabel('Fitted Values'); axes[0,0].set_ylabel('Residuals')
axes[0,0].set_title('Residuals vs Fitted'); axes[0,0].grid(alpha=0.3)
sm.qqplot(residuals, line='s', ax=axes[0,1], alpha=0.6)
axes[0,1].set_title('Normal Q-Q Plot of Residuals')
axes[0,1].grid(alpha=0.3)
axes[1,0].scatter(fitted, np.sqrt(np.abs(residuals)), alpha=0.6, color='steelblue', edgecolors='k', s=30)
axes[1,0].set_xlabel('Fitted Values'); axes[1,0].set_ylabel('√|Residuals|')
axes[1,0].set_title('Scale-Location Plot'); axes[1,0].grid(alpha=0.3)
coefs = model_std.params.drop('Intercept')
colors_bar = ['#e74c3c' if v < 0 else '#2ecc71' for v in coefs.values]
axes[1,1].barh(coefs.index, coefs.values, color=colors_bar, edgecolor='black')
axes[1,1].axvline(0, color='black', linewidth=0.8)
axes[1,1].set_xlabel('Standardized Beta')
axes[1,1].set_title('Standardized Coefficients (Beta)')
axes[1,1].grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/dataset3_regression_diagnostics.png', dpi=150, bbox_inches='tight')
plt.close()

sleep_range = np.linspace(df['Sleep_Hours'].min(), df['Sleep_Hours'].max(), 100)
pred = model.params['Intercept'] + model.params['Sleep_Hours']*sleep_range + model.params['Sleep_Hours_Sq']*sleep_range**2
fig2, ax2 = plt.subplots(figsize=(8,5))
ax2.scatter(df['Sleep_Hours'], df['Final_Exam_Score'], alpha=0.5, color='steelblue', label='Data', s=30)
ax2.plot(sleep_range, pred + df['Final_Exam_Score'].mean() - pred.mean(), 'r-', linewidth=2.5, label='Quadratic Fit')
ax2.set_xlabel('Sleep Hours'); ax2.set_ylabel('Final Exam Score')
ax2.set_title('Quadratic Relationship: Sleep Hours vs. Exam Score', fontweight='bold')
ax2.legend(); ax2.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/dataset3_sleep_quadratic.png', dpi=150, bbox_inches='tight')
plt.close()

with open(f'{OUTPUT_DIR}/dataset3_MultipleRegression_output.txt', 'w') as f:
    f.write('\n'.join(lines))

print(f'\nOutput saved to {OUTPUT_DIR}/')

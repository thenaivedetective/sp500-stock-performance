"""
Dataset 1 — Two-Way MANCOVA
Health, Exercise & Smoking Status Study
Covariate:  BMI (Quantitative)
IVs:        Exercise_Level (Low / Moderate / High)
            Smoking_Status (Smoker / Non-Smoker)
DVs:        Cardio_Fitness, Mental_Health, Energy_Level
n = 240
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.multivariate.manova import MANOVA
import statsmodels.formula.api as smf
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from scipy import stats
import warnings, os
warnings.filterwarnings('ignore')

OUTPUT_DIR = 'software_exam_answers/Dataset1_MANOVA'
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_excel('attached_assets/dataset1_1778677563523.xlsx', sheet_name='MANOVA_Data')
df['Exercise_Level'] = pd.Categorical(
    df['Exercise_Level'], categories=['Low','Moderate','High'], ordered=True)

DVS = ['Cardio_Fitness', 'Mental_Health', 'Energy_Level']

lines = []
def log(s=''):
    lines.append(str(s))
    print(s)

log('='*70)
log('  TWO-WAY MANCOVA — HEALTH, EXERCISE & SMOKING STATUS STUDY')
log('  Covariate: BMI  |  n = 240')
log('='*70)

# ── 1. Descriptive statistics ───────────────────────────────────────────────
log('\n── 1. DESCRIPTIVE STATISTICS ─────────────────────────────────────────')
log('\n  Full sample:')
log(df[['BMI'] + DVS].describe().round(3).to_string())

log('\n  BMI by group (covariate balance check):')
log(df.groupby(['Exercise_Level','Smoking_Status'])['BMI'].agg(['mean','std']).round(3).to_string())

log('\n  DV means by group:')
log(df.groupby(['Exercise_Level','Smoking_Status'])[DVS].mean().round(3).to_string())

# ── 2. Covariate check: BMI correlation with DVs ────────────────────────────
log('\n── 2. COVARIATE VALIDITY — BMI CORRELATIONS WITH DVs ────────────────')
log('  (BMI must correlate with at least one DV to justify MANCOVA)')
for dv in DVS:
    r, p = stats.pearsonr(df['BMI'], df[dv])
    log(f'  BMI vs {dv}: r = {r:.4f}, p = {p:.4f}  '
        f'{"✓ Significant — covariate justified" if p < 0.05 else "~ Non-significant"}')

# ── 3. MANCOVA ────────────────────────────────────────────────────────────
log('\n── 3. TWO-WAY MANCOVA ────────────────────────────────────────────────')
log('  Formula: DVs ~ BMI + Exercise_Level * Smoking_Status')
log('  (BMI entered first to partial out its effect before testing main effects)')

formula_mancova = ('Cardio_Fitness + Mental_Health + Energy_Level '
                   '~ BMI + C(Exercise_Level) * C(Smoking_Status)')
maov = MANOVA.from_formula(formula_mancova, data=df)
result = maov.mv_test()
log(str(result))

# ── 4. Univariate ANCOVAs ────────────────────────────────────────────────
log('\n── 4. UNIVARIATE FOLLOW-UP ANCOVAs (controlling for BMI) ────────────')
for dv in DVS:
    formula = f'{dv} ~ BMI + C(Exercise_Level) * C(Smoking_Status)'
    model = smf.ols(formula, data=df).fit()
    anova_tbl = sm.stats.anova_lm(model, typ=2)
    log(f'\n  DV: {dv}')
    log(anova_tbl.round(4).to_string())
    ss_total = anova_tbl['sum_sq'].sum()
    for eff in ['BMI','C(Exercise_Level)','C(Smoking_Status)']:
        eta = anova_tbl.loc[eff,'sum_sq'] / ss_total
        log(f'    Partial η² ({eff}): {eta:.4f}')

# ── 5. BMI regression on DVs (covariate effect) ─────────────────────────
log('\n── 5. COVARIATE EFFECT: BMI COEFFICIENTS IN EACH ANCOVA ────────────')
for dv in DVS:
    model = smf.ols(f'{dv} ~ BMI + C(Exercise_Level) * C(Smoking_Status)', data=df).fit()
    bmi_b = model.params['BMI']
    bmi_p = model.pvalues['BMI']
    log(f'  {dv}: B(BMI) = {bmi_b:.4f}, p = {bmi_p:.4f}  '
        f'{"✓ Sig." if bmi_p < 0.05 else "n.s."}')

# ── 6. Adjusted (LS) means ────────────────────────────────────────────────
log('\n── 6. ADJUSTED (LEAST-SQUARES) MEANS AT BMI GRAND MEAN ─────────────')
bmi_mean = df['BMI'].mean()
log(f'  BMI grand mean = {bmi_mean:.3f} (used to compute adjusted means)')
for dv in DVS:
    model = smf.ols(f'{dv} ~ BMI + C(Exercise_Level) * C(Smoking_Status)', data=df).fit()
    log(f'\n  Adjusted means for {dv} (BMI covariate held at {bmi_mean:.2f}):')
    combos = [('Low','Smoker'),('Low','Non-Smoker'),
              ('Moderate','Smoker'),('Moderate','Non-Smoker'),
              ('High','Smoker'),('High','Non-Smoker')]
    for ex, sm_s in combos:
        pred_df = pd.DataFrame({'BMI':[bmi_mean],
                                'Exercise_Level':[ex],
                                'Smoking_Status':[sm_s]})
        adj_mean = model.predict(pred_df)[0]
        log(f'    {ex:8s} / {sm_s:10s}: {adj_mean:.3f}')

# ── 7. Post-hoc Tukey on Exercise_Level (covariate-adjusted residuals) ──
log('\n── 7. POST-HOC TUKEY HSD — Exercise_Level (covariate-adjusted) ─────')
for dv in DVS:
    model = smf.ols(f'{dv} ~ BMI + C(Exercise_Level) * C(Smoking_Status)', data=df).fit()
    df[f'{dv}_adj'] = model.resid + model.fittedvalues - (
        model.params.get('BMI', 0) * (df['BMI'] - bmi_mean))
    tukey = pairwise_tukeyhsd(df[f'{dv}_adj'], df['Exercise_Level'], alpha=0.05)
    log(f'\n  DV: {dv}')
    log(str(tukey.summary()))

# ── 8. Assumption checks ─────────────────────────────────────────────────
log('\n── 8. ASSUMPTION CHECKS ──────────────────────────────────────────────')
log('\n  A) Homogeneity of regression slopes (BMI × Group interaction):')
log('     (Should be non-significant for MANCOVA to be valid)')
for dv in DVS:
    model_full = smf.ols(
        f'{dv} ~ BMI * C(Exercise_Level) * C(Smoking_Status)', data=df).fit()
    model_red  = smf.ols(
        f'{dv} ~ BMI + C(Exercise_Level) * C(Smoking_Status)', data=df).fit()
    fstat = ((model_red.ssr - model_full.ssr) / (model_full.df_resid - model_red.df_resid) /
             (model_full.ssr / model_full.df_resid))
    # Use F-test
    lr_result = model_full.compare_f_test(model_red)
    log(f'    {dv}: F = {lr_result[0]:.4f}, p = {lr_result[1]:.4f}  '
        f'{"✓ Slopes homogeneous" if lr_result[1] > 0.05 else "✗ Slopes heterogeneous — interpret cautiously"}')

log('\n  B) Levene test — homogeneity of variance (residuals):')
for dv in DVS:
    model = smf.ols(f'{dv} ~ BMI + C(Exercise_Level) * C(Smoking_Status)', data=df).fit()
    groups = [model.resid[df['Exercise_Level']==lv].values for lv in ['Low','Moderate','High']]
    stat, p = stats.levene(*groups)
    log(f'    {dv}: W = {stat:.4f}, p = {p:.4f}  {"✓" if p>0.05 else "✗"}')

log('\n  C) Shapiro-Wilk normality (residuals):')
for dv in DVS:
    model = smf.ols(f'{dv} ~ BMI + C(Exercise_Level) * C(Smoking_Status)', data=df).fit()
    stat, p = stats.shapiro(model.resid)
    log(f'    {dv}: W = {stat:.4f}, p = {p:.4f}  '
        f'{"✓ Normal" if p>0.05 else "~ Non-normal (n=240, CLT applies)"}')

log('\n  D) BMI linearity check:')
r_bmi, p_bmi = stats.pearsonr(df['BMI'], df['Cardio_Fitness'])
log(f'    BMI–Cardio_Fitness: r = {r_bmi:.4f}, p = {p_bmi:.4f}')

# ── 9. Comparison: MANOVA vs MANCOVA ─────────────────────────────────────
log('\n── 9. MANOVA vs MANCOVA COMPARISON ──────────────────────────────────')
log('  (Shows what adding BMI as covariate changes)')
maov_no_cov = MANOVA.from_formula(
    'Cardio_Fitness + Mental_Health + Energy_Level ~ C(Exercise_Level) * C(Smoking_Status)',
    data=df)
res_no_cov = maov_no_cov.mv_test()

log('\n  MANOVA (no covariate):')
log(str(res_no_cov))
log('\n  MANCOVA (BMI covariate) already shown in Section 3 above.')

# ── Visualizations ──────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('MANCOVA — Adjusted Group Means by Exercise Level & Smoking Status\n'
             '(BMI covariate held at grand mean)', fontsize=12, fontweight='bold')

colors_ = {'Smoker': '#e74c3c', 'Non-Smoker': '#2ecc71'}
for ax, dv in zip(axes, DVS):
    model = smf.ols(f'{dv} ~ BMI + C(Exercise_Level) * C(Smoking_Status)', data=df).fit()
    plot_data = {}
    for sm_s in ['Smoker','Non-Smoker']:
        adj_means = []
        for ex in ['Low','Moderate','High']:
            pred = model.predict(pd.DataFrame({'BMI':[bmi_mean],
                                               'Exercise_Level':[ex],
                                               'Smoking_Status':[sm_s]}))[0]
            adj_means.append(pred)
        plot_data[sm_s] = adj_means
    x = np.arange(3)
    width = 0.35
    for i, (sm_s, vals) in enumerate(plot_data.items()):
        ax.bar(x + i*width, vals, width, label=sm_s,
               color=colors_[sm_s], edgecolor='black', alpha=0.85)
    ax.set_title(dv.replace('_',' '), fontweight='bold')
    ax.set_xticks(x + width/2)
    ax.set_xticklabels(['Low','Moderate','High'])
    ax.set_xlabel('Exercise Level')
    ax.set_ylabel('Adjusted Mean Score')
    ax.legend(title='Smoking Status', fontsize=8)
    ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/dataset1_adjusted_means.png', dpi=150, bbox_inches='tight')
plt.close()

# BMI vs DVs scatterplots
fig2, axes2 = plt.subplots(1, 3, figsize=(14, 4))
fig2.suptitle('Covariate Validity: BMI vs Each Dependent Variable', fontsize=12, fontweight='bold')
for ax, dv in zip(axes2, DVS):
    for grp, color in zip(['Low','Moderate','High'], ['#e74c3c','#f39c12','#2ecc71']):
        mask = df['Exercise_Level'] == grp
        ax.scatter(df.loc[mask,'BMI'], df.loc[mask,dv],
                   alpha=0.5, s=20, color=color, label=grp)
    m, b = np.polyfit(df['BMI'], df[dv], 1)
    x_line = np.linspace(df['BMI'].min(), df['BMI'].max(), 100)
    ax.plot(x_line, m*x_line+b, 'k--', linewidth=1.5, label='Overall trend')
    r, p = stats.pearsonr(df['BMI'], df[dv])
    ax.set_title(f'{dv.replace("_"," ")}\nr={r:.3f}, p={p:.3f}', fontweight='bold')
    ax.set_xlabel('BMI')
    ax.set_ylabel('Score')
    ax.legend(title='Exercise', fontsize=7)
    ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/dataset1_BMI_covariate.png', dpi=150, bbox_inches='tight')
plt.close()

# Interaction plots (adjusted means)
fig3, axes3 = plt.subplots(1, 3, figsize=(14, 4))
fig3.suptitle('Interaction Plots — Adjusted Means (BMI covariate removed)',
              fontsize=12, fontweight='bold')
for ax, dv in zip(axes3, DVS):
    model = smf.ols(f'{dv} ~ BMI + C(Exercise_Level) * C(Smoking_Status)', data=df).fit()
    for sm_s, color in colors_.items():
        adj = [model.predict(pd.DataFrame({'BMI':[bmi_mean],'Exercise_Level':[ex],
                                           'Smoking_Status':[sm_s]}))[0]
               for ex in ['Low','Moderate','High']]
        ax.plot(['Low','Moderate','High'], adj, marker='o', label=sm_s,
                color=color, linewidth=2)
    ax.set_title(dv.replace('_',' '), fontweight='bold')
    ax.set_xlabel('Exercise Level')
    ax.set_ylabel('Adjusted Mean Score')
    ax.legend(title='Smoking Status', fontsize=8)
    ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/dataset1_interaction_adjusted.png', dpi=150, bbox_inches='tight')
plt.close()

with open(f'{OUTPUT_DIR}/dataset1_MANOVA_output.txt', 'w') as f:
    f.write('\n'.join(lines))

print(f'\nOutput saved to {OUTPUT_DIR}/')

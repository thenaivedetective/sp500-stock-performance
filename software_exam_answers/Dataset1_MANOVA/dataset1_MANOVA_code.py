"""
Dataset 1 — Two-Way MANOVA
Health, Exercise & Smoking Status Study
DV: Cardio_Fitness, Mental_Health, Energy_Level
IV: Exercise_Level (3 levels), Smoking_Status (2 levels)
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.multivariate.manova import MANOVA
import statsmodels.formula.api as smf
from statsmodels.stats.anova import AnovaRM
import statsmodels.api as sm
from scipy import stats
import warnings, os
warnings.filterwarnings('ignore')

OUTPUT_DIR = 'software_exam_answers/Dataset1_MANOVA'
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_excel('attached_assets/dataset1_1778677563523.xlsx', sheet_name='MANOVA_Data')
df['Exercise_Level'] = pd.Categorical(df['Exercise_Level'], categories=['Low','Moderate','High'], ordered=True)

lines = []
def log(s=''):
    lines.append(s)
    print(s)

log('='*70)
log('  TWO-WAY MANOVA — HEALTH, EXERCISE & SMOKING STATUS STUDY')
log('='*70)

log('\n── 1. DESCRIPTIVE STATISTICS ─────────────────────────────────────────')
dvs = ['Cardio_Fitness', 'Mental_Health', 'Energy_Level']
desc = df.groupby(['Exercise_Level','Smoking_Status'])[dvs].agg(['mean','std']).round(3)
log(desc.to_string())

log('\n── 2. TWO-WAY MANOVA ─────────────────────────────────────────────────')
log('  Formula: Cardio_Fitness + Mental_Health + Energy_Level ~')
log('           Exercise_Level * Smoking_Status')
maov = MANOVA.from_formula(
    'Cardio_Fitness + Mental_Health + Energy_Level ~ C(Exercise_Level) * C(Smoking_Status)',
    data=df)
result = maov.mv_test()
log(str(result))

log('\n── 3. UNIVARIATE FOLLOW-UP ANOVAs ────────────────────────────────────')
for dv in dvs:
    formula = f'{dv} ~ C(Exercise_Level) * C(Smoking_Status)'
    model = smf.ols(formula, data=df).fit()
    anova_tbl = sm.stats.anova_lm(model, typ=2)
    log(f'\n  DV: {dv}')
    log(anova_tbl.round(4).to_string())
    eta_sq = anova_tbl['sum_sq'] / (anova_tbl['sum_sq'].sum())
    log(f'  Partial Eta² (Exercise_Level): {eta_sq["C(Exercise_Level)"]:.4f}')
    log(f'  Partial Eta² (Smoking_Status): {eta_sq["C(Smoking_Status)"]:.4f}')

log('\n── 4. POST-HOC TUKEY HSD (Exercise_Level) ────────────────────────────')
from statsmodels.stats.multicomp import pairwise_tukeyhsd
for dv in dvs:
    tukey = pairwise_tukeyhsd(df[dv], df['Exercise_Level'], alpha=0.05)
    log(f'\n  DV: {dv}')
    log(str(tukey.summary()))

log('\n── 5. ASSUMPTION CHECKS ──────────────────────────────────────────────')
log('\n  Levene Test for Homogeneity of Variance:')
for dv in dvs:
    groups = [grp[dv].values for _, grp in df.groupby('Exercise_Level')]
    stat, p = stats.levene(*groups)
    log(f'    {dv}: W={stat:.4f}, p={p:.4f}  {"✓ Homogeneous" if p>0.05 else "✗ Heterogeneous"}')

log('\n  Shapiro-Wilk Normality Test (residuals):')
for dv in dvs:
    model = smf.ols(f'{dv} ~ C(Exercise_Level)*C(Smoking_Status)', data=df).fit()
    stat, p = stats.shapiro(model.resid)
    log(f'    {dv}: W={stat:.4f}, p={p:.4f}  {"✓ Normal" if p>0.05 else "~ Non-normal (n=240, CLT applies)"}')

log('\n── 6. GROUP MEANS SUMMARY ────────────────────────────────────────────')
gm = df.groupby(['Exercise_Level','Smoking_Status'])[dvs].mean().round(2)
log(gm.to_string())

# ── Visualizations ──────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('Two-Way MANOVA: Mean Scores by Exercise Level & Smoking Status', fontsize=13, fontweight='bold')
colors = {'Smoker': '#e74c3c', 'Non-Smoker': '#2ecc71'}
for ax, dv in zip(axes, dvs):
    means = df.groupby(['Exercise_Level','Smoking_Status'])[dv].mean().unstack()
    means.plot(kind='bar', ax=ax, color=[colors[c] for c in means.columns], width=0.7, edgecolor='black')
    ax.set_title(dv.replace('_',' '), fontweight='bold')
    ax.set_xlabel('Exercise Level')
    ax.set_ylabel('Mean Score')
    ax.set_xticklabels(['Low','Moderate','High'], rotation=0)
    ax.legend(title='Smoking Status')
    ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/dataset1_group_means.png', dpi=150, bbox_inches='tight')
plt.close()

fig2, axes2 = plt.subplots(1, 3, figsize=(15, 5))
fig2.suptitle('Interaction Plots — Exercise Level × Smoking Status', fontsize=13, fontweight='bold')
for ax, dv in zip(axes2, dvs):
    for status, grp in df.groupby('Smoking_Status'):
        means = grp.groupby('Exercise_Level')[dv].mean()
        ax.plot(['Low','Moderate','High'], [means['Low'],means['Moderate'],means['High']],
                marker='o', label=status, color=colors[status], linewidth=2)
    ax.set_title(dv.replace('_',' '), fontweight='bold')
    ax.set_xlabel('Exercise Level'); ax.set_ylabel('Mean Score')
    ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/dataset1_interaction_plots.png', dpi=150, bbox_inches='tight')
plt.close()

with open(f'{OUTPUT_DIR}/dataset1_MANOVA_output.txt', 'w') as f:
    f.write('\n'.join(lines))

print(f'\nOutput saved to {OUTPUT_DIR}/')

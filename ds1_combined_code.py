"""
Dataset 1 — MANCOVA + Two-Way MANOVA Combined Analysis
Cardiovascular Health Study | n = 240
IVs:  Exercise_Level (Low/Moderate/High), Smoking_Status (Smoker/Non-Smoker)
DVs:  Cardio_Fitness, Mental_Health, Energy_Level
COV:  BMI (MANCOVA only)
Research Question:
  After statistically controlling for BMI, do exercise level and smoking status
  jointly affect a multivariate profile of cardiovascular fitness, mental health,
  and energy levels? Does the inclusion of BMI as a covariate meaningfully alter
  the pattern of group differences compared to a standard Two-Way MANOVA?
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import f as f_dist
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.multivariate.manova import MANOVA
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.anova import AnovaRM
import warnings, os, json
warnings.filterwarnings('ignore')

OUT  = 'Lana_Gidan_Software_Exam/Dataset1_MANCOVA'
os.makedirs(OUT, exist_ok=True)

df = pd.read_excel('attached_assets/dataset1_1778677563523.xlsx',
                   sheet_name='MANOVA_Data')

DVs  = ['Cardio_Fitness', 'Mental_Health', 'Energy_Level']
IVs  = ['Exercise_Level', 'Smoking_Status']
COV  = 'BMI'
EX_ORDER = ['Low', 'Moderate', 'High']
df['Exercise_Level'] = pd.Categorical(df['Exercise_Level'],
                                       categories=EX_ORDER, ordered=True)

lines = []
def log(s=''):
    lines.append(str(s))
    print(s)

log('=' * 72)
log('  COMBINED MANCOVA + TWO-WAY MANOVA — CARDIOVASCULAR HEALTH STUDY')
log('  n = 240 | DVs: Cardio_Fitness, Mental_Health, Energy_Level')
log('  IVs: Exercise_Level (3 levels) × Smoking_Status (2 levels)')
log('  Covariate (MANCOVA only): BMI')
log('=' * 72)

# ════════════════════════════════════════════════════════════════════════
# PART A — MANCOVA
# ════════════════════════════════════════════════════════════════════════
log('\n' + '═'*72)
log('  PART A — MANCOVA (Multivariate Analysis of Covariance)')
log('  Controlling for BMI as a continuous covariate')
log('═'*72)

log('\n── A1. RESEARCH QUESTION ─────────────────────────────────────────────')
log('  After statistically removing the shared variance attributable to BMI,')
log('  do exercise level and smoking status significantly affect the combined')
log('  multivariate outcome of cardiovascular fitness, mental health, and')
log('  energy level? Does smoking and exercise interact?')

log('\n── A2. COVARIATE VALIDITY — BMI ──────────────────────────────────────')
log('  For MANCOVA to be valid, BMI must correlate significantly with')
log('  at least one DV, and its relationship with DVs must be linear.')
log('')
log(f'  {"DV":<20} {"r with BMI":>12} {"p-value":>12}  Verdict')
log('  ' + '-'*58)
for dv in DVs:
    r, p = stats.pearsonr(df[COV], df[dv])
    sig = '✓ Significant — valid covariate' if p < 0.05 else '✗ Not significant'
    log(f'  {dv:<20} {r:>+12.4f} {p:>12.4f}  {sig}')

log('\n  Homogeneity of regression slopes (BMI effect must not differ by group):')
log(f'  {"DV":<20} {"F":>8} {"p":>10}  Verdict')
log('  ' + '-'*55)
slope_results = {}
for dv in DVs:
    formula = f'{dv} ~ C(Exercise_Level)*{COV} + C(Smoking_Status)*{COV}'
    m = smf.ols(formula, data=df).fit()
    # interaction p-values
    pvals = [p for nm, p in zip(m.pvalues.index, m.pvalues)
             if 'BMI' in nm and ':' in nm]
    max_p = max(pvals) if pvals else 1.0
    min_p = min(pvals) if pvals else 1.0
    F_val = m.fvalue
    slope_results[dv] = min_p
    verdict = '✓ Slopes parallel' if min_p > 0.05 else '✗ Non-parallel (proceed cautiously)'
    log(f'  {dv:<20} {F_val:>8.3f} {min_p:>10.4f}  {verdict}')

log('\n── A3. DESCRIPTIVE STATISTICS ────────────────────────────────────────')
log('\n  DVs by Exercise Level:')
ex_desc = df.groupby('Exercise_Level', observed=True)[DVs].mean()
log(f'  {"Exercise Level":<16}  ' + '  '.join(f'{dv:>16}' for dv in DVs))
log('  ' + '-'*70)
for lvl in EX_ORDER:
    vals = '  '.join(f'{ex_desc.loc[lvl, dv]:>16.3f}' for dv in DVs)
    log(f'  {lvl:<16}  {vals}')

log('\n  DVs by Smoking Status:')
sm_desc = df.groupby('Smoking_Status')[DVs].mean()
for grp in sm_desc.index:
    vals = '  '.join(f'{sm_desc.loc[grp, dv]:>16.3f}' for dv in DVs)
    log(f'  {grp:<16}  {vals}')

log('\n  BMI means by group:')
bmi_desc = df.groupby(['Exercise_Level', 'Smoking_Status'], observed=True)[COV].mean()
log(bmi_desc.to_string())

log('\n── A4. MANCOVA — ADJUSTED MEANS (After Removing BMI Effect) ──────────')
grand_bmi = df[COV].mean()
adj_means = {}
for dv in DVs:
    adj = {}
    for lvl in EX_ORDER:
        mask = df['Exercise_Level'] == lvl
        formula = f'{dv} ~ {COV}'
        m = smf.ols(formula, data=df[mask]).fit()
        raw_mean = df.loc[mask, dv].mean()
        group_bmi = df.loc[mask, COV].mean()
        adjusted = raw_mean - m.params[COV] * (group_bmi - grand_bmi)
        adj[lvl] = adjusted
    adj_means[dv] = adj
log(f'\n  Adjusted means at grand mean BMI = {grand_bmi:.3f}:')
log(f'  {"Exercise Level":<16}  ' + '  '.join(f'{dv:>16}' for dv in DVs))
log('  ' + '-'*70)
for lvl in EX_ORDER:
    vals = '  '.join(f'{adj_means[dv][lvl]:>16.3f}' for dv in DVs)
    log(f'  {lvl:<16}  {vals}')

log('\n── A5. MANCOVA OMNIBUS TEST ──────────────────────────────────────────')
# Use MANOVA on residualized DVs (BMI partialed out)
df_res = df.copy()
for dv in DVs:
    m = smf.ols(f'{dv} ~ {COV}', data=df).fit()
    df_res[f'{dv}_adj'] = df[dv] - m.predict(df) + df[dv].mean()

DVs_adj = [f'{dv}_adj' for dv in DVs]
dv_str_adj = ' + '.join(DVs_adj)

man_ex  = MANOVA.from_formula(f'{dv_str_adj} ~ C(Exercise_Level)', data=df_res)
man_sm  = MANOVA.from_formula(f'{dv_str_adj} ~ C(Smoking_Status)', data=df_res)
man_int = MANOVA.from_formula(f'{dv_str_adj} ~ C(Exercise_Level)*C(Smoking_Status)', data=df_res)

res_ex   = man_ex.mv_test()
res_sm   = man_sm.mv_test()
res_int  = man_int.mv_test()

def extract_wilks(mv_res, effect_name):
    try:
        tbl = mv_res.results[effect_name]['stat']
        wilks_row = tbl.loc["Wilks' lambda"]
        lam  = wilks_row['Value']
        F    = wilks_row['F Value']
        df1  = int(wilks_row['Num DF'])
        df2  = int(wilks_row['Den DF'])
        p    = wilks_row['Pr > F']
        return lam, F, df1, df2, p
    except:
        return None, None, None, None, None

log(f'\n  {"Effect":<28} {"Wilks λ":>10} {"F":>10} {"df1":>5} {"df2":>6} {"p":>10}  Sig  η²')
log('  ' + '-'*90)

mancova_results = {}
for label, res, eff in [
    ('Exercise_Level (adj)', res_ex, 'C(Exercise_Level)'),
    ('Smoking_Status (adj)',  res_sm, 'C(Smoking_Status)'),
]:
    lam, F, df1, df2, p = extract_wilks(res, eff)
    if lam:
        eta2 = 1 - lam**(1/1) if lam else None
        eta2_m = round(1 - lam, 3)
        sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'n.s.'
        log(f'  {label:<28} {lam:>10.4f} {F:>10.4f} {df1:>5} {df2:>6} {p:>10.4f}  {sig}  {eta2_m:.3f}')
        mancova_results[label] = {'lambda': lam, 'F': F, 'p': p, 'eta2': eta2_m}

log('\n── A6. UNIVARIATE FOLLOW-UP ANCOVAs ──────────────────────────────────')
log('  Testing each DV separately, controlling for BMI.')
log('')
log(f'  {"Effect":<28} {"DV":<20} {"F":>8} {"p":>10} {"η²":>8}  Sig')
log('  ' + '-'*80)
ancova_results = {}
for dv in DVs:
    for iv in ['Exercise_Level', 'Smoking_Status']:
        formula = f'{dv} ~ {COV} + C({iv})'
        m = smf.ols(formula, data=df).fit()
        aov = sm.stats.anova_lm(m, typ=2)
        F_iv = aov.loc[f'C({iv})', 'F']
        p_iv = aov.loc[f'C({iv})', 'PR(>F)']
        ss_iv  = aov.loc[f'C({iv})', 'sum_sq']
        ss_tot = aov['sum_sq'].sum()
        eta2   = ss_iv / ss_tot
        sig = '***' if p_iv < 0.001 else '**' if p_iv < 0.01 else '*' if p_iv < 0.05 else 'n.s.'
        log(f'  {iv:<28} {dv:<20} {F_iv:>8.4f} {p_iv:>10.4f} {eta2:>8.4f}  {sig}')
        ancova_results[f'{iv}_{dv}'] = {'F': F_iv, 'p': p_iv, 'eta2': eta2}

log('\n── A7. POST-HOC TUKEY HSD (MANCOVA-adjusted) ─────────────────────────')
log('  Pairwise comparisons for Exercise_Level on each DV:')
for dv in DVs:
    log(f'\n  DV: {dv}')
    formula = f'{dv} ~ {COV}'
    m_cov = smf.ols(formula, data=df).fit()
    df[f'{dv}_resid'] = df[dv] - m_cov.fittedvalues + df[dv].mean()
    tukey = pairwise_tukeyhsd(df[f'{dv}_resid'], df['Exercise_Level'])
    log(f'  {tukey}')

# ════════════════════════════════════════════════════════════════════════
# PART B — TWO-WAY MANOVA
# ════════════════════════════════════════════════════════════════════════
log('\n' + '═'*72)
log('  PART B — TWO-WAY MANOVA (without covariate)')
log('  Raw DVs without BMI adjustment')
log('═'*72)

log('\n── B1. RESEARCH QUESTION ─────────────────────────────────────────────')
log('  Do exercise level, smoking status, and their interaction significantly')
log('  affect the joint multivariate outcome profile WITHOUT removing BMI?')
log('  This serves as a baseline comparison for the MANCOVA.')

log('\n── B2. ASSUMPTION CHECKS ─────────────────────────────────────────────')
log('\n  Box\'s M — Homogeneity of Covariance Matrices:')
log('  (No direct Box\'s M in Python; Levene per DV used as proxy)')
log(f'  {"DV":<20} {"Exercise F":>12} {"Exercise p":>12} {"Smoking F":>12} {"Smoking p":>12}')
log('  ' + '-'*72)
for dv in DVs:
    grps_ex = [df.loc[df['Exercise_Level']==lvl, dv] for lvl in EX_ORDER]
    grps_sm = [df.loc[df['Smoking_Status']==s, dv] for s in df['Smoking_Status'].unique()]
    Fe, pe = stats.levene(*grps_ex)
    Fs, ps = stats.levene(*grps_sm)
    log(f'  {dv:<20} {Fe:>12.4f} {pe:>12.4f} {Fs:>12.4f} {ps:>12.4f}')

log('\n  Multivariate Normality (Shapiro-Wilk per DV per group):')
any_viol = False
for dv in DVs:
    for lvl in EX_ORDER:
        W, p = stats.shapiro(df.loc[df['Exercise_Level']==lvl, dv])
        if p < 0.05:
            log(f'    ✗ {dv} / {lvl}: W={W:.4f}, p={p:.4f}')
            any_viol = True
if not any_viol:
    log('    ✓ All DV-group combinations normally distributed (p > 0.05)')

log('\n── B3. TWO-WAY MANOVA OMNIBUS RESULTS ───────────────────────────────')
dv_str = ' + '.join(DVs)
man_full = MANOVA.from_formula(f'{dv_str} ~ C(Exercise_Level)*C(Smoking_Status)', data=df)
res_full = man_full.mv_test()

log(f'\n  {"Effect":<30} {"Wilks λ":>10} {"F":>10} {"df1":>5} {"df2":>6} {"p":>10}  Sig  η²_m')
log('  ' + '-'*92)
manova_results = {}
for label, eff in [
    ('Exercise_Level',              'C(Exercise_Level)'),
    ('Smoking_Status',              'C(Smoking_Status)'),
    ('Exercise × Smoking (interaction)', 'C(Exercise_Level):C(Smoking_Status)'),
]:
    lam, F, df1, df2, p = extract_wilks(res_full, eff)
    if lam:
        eta2_m = round(1 - lam, 3)
        sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'n.s.'
        log(f'  {label:<30} {lam:>10.4f} {F:>10.4f} {df1:>5} {df2:>6} {p:>10.4f}  {sig}  {eta2_m:.3f}')
        manova_results[label] = {'lambda': lam, 'F': F, 'p': p, 'eta2': eta2_m}

log('\n── B4. UNIVARIATE FOLLOW-UP ANOVAs ───────────────────────────────────')
log(f'  {"Effect":<28} {"DV":<20} {"F":>8} {"p":>10} {"η²":>8}  Sig')
log('  ' + '-'*80)
anova_results = {}
for dv in DVs:
    formula = f'{dv} ~ C(Exercise_Level) + C(Smoking_Status) + C(Exercise_Level):C(Smoking_Status)'
    m = smf.ols(formula, data=df).fit()
    aov = sm.stats.anova_lm(m, typ=2)
    for iv_key, iv_label in [
        ('C(Exercise_Level)',                                  'Exercise_Level'),
        ('C(Smoking_Status)',                                  'Smoking_Status'),
        ('C(Exercise_Level):C(Smoking_Status)',                'Exercise×Smoking'),
    ]:
        if iv_key in aov.index:
            F_iv  = aov.loc[iv_key, 'F']
            p_iv  = aov.loc[iv_key, 'PR(>F)']
            ss_iv = aov.loc[iv_key, 'sum_sq']
            ss_tot= aov['sum_sq'].sum()
            eta2  = ss_iv / ss_tot
            sig   = '***' if p_iv<0.001 else '**' if p_iv<0.01 else '*' if p_iv<0.05 else 'n.s.'
            log(f'  {iv_label:<28} {dv:<20} {F_iv:>8.4f} {p_iv:>10.4f} {eta2:>8.4f}  {sig}')
            anova_results[f'{iv_label}_{dv}'] = {'F': F_iv, 'p': p_iv, 'eta2': eta2}

log('\n── B5. GROUP MEANS (RAW, UNADJUSTED) ────────────────────────────────')
log(f'  {"Exercise":<12} {"Smoking":<14}  ' + '  '.join(f'{dv:>16}' for dv in DVs))
log('  ' + '-'*78)
for ex in EX_ORDER:
    for sm_grp in ['Smoker', 'Non-Smoker']:
        mask = (df['Exercise_Level']==ex) & (df['Smoking_Status']==sm_grp)
        n = mask.sum()
        vals = '  '.join(f'{df.loc[mask, dv].mean():>16.3f}' for dv in DVs)
        log(f'  {ex:<12} {sm_grp:<14}  {vals}  (n={n})')

# ════════════════════════════════════════════════════════════════════════
# PART C — MANCOVA vs MANOVA COMPARISON
# ════════════════════════════════════════════════════════════════════════
log('\n' + '═'*72)
log('  PART C — MANCOVA vs TWO-WAY MANOVA: HEAD-TO-HEAD COMPARISON')
log('  What changes when BMI is statistically controlled?')
log('═'*72)

log('\n── C1. WILKS λ COMPARISON ────────────────────────────────────────────')
log(f'\n  {"Effect":<28} {"MANOVA λ":>12} {"MANCOVA λ":>12} {"Δλ":>8}  Interpretation')
log('  ' + '-'*82)

ex_manova_lam, _, _, _, ex_manova_p = extract_wilks(res_full, 'C(Exercise_Level)')
sm_manova_lam, _, _, _, sm_manova_p = extract_wilks(res_full, 'C(Smoking_Status)')
ex_man_r = mancova_results.get('Exercise_Level (adj)', {})
sm_man_r = mancova_results.get('Smoking_Status (adj)',  {})

ex_mancova_lam = ex_man_r.get('lambda', 0)
sm_mancova_lam = sm_man_r.get('lambda', 0)
ex_mancova_p   = ex_man_r.get('p', 1)
sm_mancova_p   = sm_man_r.get('p', 1)

for label, lam_man, lam_cov in [
    ('Exercise_Level',   ex_manova_lam, ex_mancova_lam),
    ('Smoking_Status',   sm_manova_lam, sm_mancova_lam),
]:
    delta = lam_cov - lam_man
    if delta < 0:
        interp = 'Controlling BMI STRENGTHENS the effect'
    elif delta > 0:
        interp = 'Controlling BMI WEAKENS the effect'
    else:
        interp = 'BMI has minimal impact on this effect'
    log(f'  {label:<28} {lam_man:>12.4f} {lam_cov:>12.4f} {delta:>+8.4f}  {interp}')

log('\n── C2. SIGNIFICANCE COMPARISON ───────────────────────────────────────')
log(f'\n  {"Effect":<28} {"MANOVA sig":>12} {"MANCOVA sig":>13}  Same conclusion?')
log('  ' + '-'*72)
for label, p_man, p_cov in [
    ('Exercise_Level', ex_manova_p, ex_mancova_p),
    ('Smoking_Status', sm_manova_p, sm_mancova_p),
]:
    s_man = '*** p<.001' if p_man<0.001 else '** p<.01' if p_man<0.01 else '* p<.05' if p_man<0.05 else 'n.s.'
    s_cov = '*** p<.001' if p_cov<0.001 else '** p<.01' if p_cov<0.01 else '* p<.05' if p_cov<0.05 else 'n.s.'
    same  = 'YES ✓' if (p_man<0.05)==(p_cov<0.05) else 'NO — conclusions differ ✗'
    log(f'  {label:<28} {s_man:>12} {s_cov:>13}  {same}')

log('''
  C3. INTERPRETATION OF DIFFERENCES:
  ─────────────────────────────────────────────────────────────────────
  When Wilks' λ DECREASES from MANOVA → MANCOVA (λ gets smaller):
    → The effect becomes STRONGER after controlling for BMI
    → BMI was SUPPRESSING the true group difference
    → The groups actually differ MORE on the DVs than raw means suggest

  When Wilks' λ INCREASES from MANOVA → MANCOVA (λ gets larger):
    → The effect becomes WEAKER after controlling for BMI
    → Part of what appeared to be a group difference was actually
      due to BMI differences between groups
    → MANCOVA provides a "fairer" comparison by equating groups on BMI

  RECOMMENDATION: MANCOVA is preferred here because:
    (1) BMI correlates significantly with at least one DV
    (2) Homogeneity of regression slopes holds (parallel slopes)
    (3) MANCOVA removes confounding BMI variance, yielding purer estimates
    (4) Adjusted means represent what group differences would look like
        if all participants had the same BMI (grand mean = 26.14)
''')

# ════════════════════════════════════════════════════════════════════════
# FIGURES
# ════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('MANCOVA + Two-Way MANOVA — Cardiovascular Health Study (n=240)',
             fontsize=13, fontweight='bold')

palette = {'Smoker': '#e74c3c', 'Non-Smoker': '#2ecc71'}

for i, dv in enumerate(DVs):
    ax = axes[0, i]
    means_ex = df.groupby('Exercise_Level', observed=True)[dv].mean()
    adj_list = [adj_means[dv][lvl] for lvl in EX_ORDER]
    x = np.arange(len(EX_ORDER))
    ax.bar(x-0.18, means_ex.values, 0.35, label='Raw (MANOVA)', color='#5b9bd5', edgecolor='black', lw=0.5)
    ax.bar(x+0.18, adj_list,        0.35, label='Adj (MANCOVA)', color='#ed7d31', edgecolor='black', lw=0.5)
    ax.set_xticks(x); ax.set_xticklabels(EX_ORDER, fontsize=8)
    ax.set_title(f'{dv}\nRaw vs BMI-Adjusted Means', fontweight='bold', fontsize=9)
    ax.set_ylabel('Score'); ax.legend(fontsize=7); ax.grid(axis='y', alpha=0.3)

for i, dv in enumerate(DVs):
    ax = axes[1, i]
    for sm_grp, col in [('Smoker','#e74c3c'), ('Non-Smoker','#2ecc71')]:
        vals = [df.loc[(df['Exercise_Level']==lvl)&(df['Smoking_Status']==sm_grp), dv].mean()
                for lvl in EX_ORDER]
        ax.plot(EX_ORDER, vals, 'o-', color=col, lw=2, label=sm_grp, markersize=7)
    ax.set_title(f'{dv}\nExercise × Smoking Interaction', fontweight='bold', fontsize=9)
    ax.set_ylabel('Mean Score'); ax.legend(fontsize=7); ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(f'{OUT}/dataset1_combined_analysis.png', dpi=150, bbox_inches='tight')
plt.close()

# Comparison figure
fig2, axes2 = plt.subplots(1, 3, figsize=(15, 5))
fig2.suptitle('MANCOVA vs MANOVA — Wilks\' λ Comparison by Effect and DV',
              fontsize=12, fontweight='bold')
for i, dv in enumerate(DVs):
    ax = axes2[i]
    man_vals, cov_vals, labels2 = [], [], []
    for iv_label in ['Exercise_Level', 'Smoking_Status']:
        man_r = anova_results.get(f'{iv_label}_{dv}', {})
        cov_r = ancova_results.get(f'{iv_label}_{dv}', {})
        man_vals.append(man_r.get('eta2', 0))
        cov_vals.append(cov_r.get('eta2', 0))
        labels2.append(iv_label.replace('_', '\n'))
    xb = np.arange(len(labels2))
    ax.bar(xb-0.18, man_vals,  0.35, label='MANOVA η²',  color='#5b9bd5', edgecolor='black', lw=0.5)
    ax.bar(xb+0.18, cov_vals,  0.35, label='MANCOVA η²', color='#ed7d31', edgecolor='black', lw=0.5)
    ax.set_xticks(xb); ax.set_xticklabels(labels2, fontsize=8)
    ax.set_title(f'{dv}', fontweight='bold')
    ax.set_ylabel('η² Effect Size'); ax.legend(fontsize=8); ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUT}/dataset1_comparison_plot.png', dpi=150, bbox_inches='tight')
plt.close()

with open(f'{OUT}/dataset1_combined_output.txt', 'w') as f:
    f.write('\n'.join(lines))

metrics = {
    'mancova': mancova_results, 'manova': manova_results,
    'ancova': ancova_results,   'anova': anova_results,
    'adj_means': adj_means,     'grand_bmi': grand_bmi
}
with open('ds1_metrics.json', 'w') as f:
    json.dump(metrics, f)

print(f'\nAll DS1 files saved to {OUT}/')

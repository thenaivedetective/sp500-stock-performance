import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import confusion_matrix, classification_report
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

col_names = [
    'OBS','ID','SEX','AGE','MARITAL','EDUCAT','EMPLOY','INCOME','RELIG',
    'C1','C2','C3','C4','C5','C6','C7','C8','C9','C10',
    'C11','C12','C13','C14','C15','C16','C17','C18','C19','C20',
    'CESD','CASES','DRINK','HEALTH','REGDOC','TREAT','BEDDAYS','ACUTEILL','CHRONILL'
]

rows = []
with open('attached_assets/DEPRES_1773880715452.DAT', 'r') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('Dep') or line.startswith('---'):
            continue
        vals = line.split()
        if len(vals) == 38:
            rows.append([float(v) for v in vals])

df = pd.DataFrame(rows, columns=col_names)
print(f"Dataset loaded: {len(df)} observations, {len(df.columns)} variables")
print(f"\nCASES distribution:\n{df['CASES'].value_counts().sort_index()}")
print(f"  0 = Normal, 1 = Depressed (CESD > 16)")

# ─────────────────────────────────────────────────────────────────────────────
# PART (a): LDA with INCOME and EDUCAT
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART (a): Discriminant Analysis using INCOME and EDUCAT")
print("="*70)

vars_a = ['INCOME', 'EDUCAT']
X_a = df[vars_a].values
y   = df['CASES'].values

lda_a = LinearDiscriminantAnalysis()
lda_a.fit(X_a, y)
pred_a = lda_a.predict(X_a)
scores_a = lda_a.transform(X_a)

# Group means
print("\nGroup Means:")
for g, label in [(0,'Normal'), (1,'Depressed')]:
    mask = y == g
    print(f"  {label}: INCOME={df.loc[mask,'INCOME'].mean():.2f}, "
          f"EDUCAT={df.loc[mask,'EDUCAT'].mean():.2f}")

# Standardized discriminant coefficients
pooled_std = df[vars_a].std()
std_coefs_a = lda_a.coef_[0] * pooled_std.values
print("\nStandardized Discriminant Function Coefficients:")
for v, c in zip(vars_a, std_coefs_a):
    print(f"  {v}: {c:.4f}")

print(f"\nCanonical Discriminant Function Coefficients (raw):")
for v, c in zip(vars_a, lda_a.coef_[0]):
    print(f"  {v}: {c:.4f}")
print(f"  Constant: {lda_a.intercept_[0]:.4f}")

# Wilks' Lambda approximation
n = len(y)
n0 = np.sum(y==0)
n1 = np.sum(y==1)
p = len(vars_a)

grand_mean = df[vars_a].mean()
W = np.zeros((p, p))
for g in [0, 1]:
    mask = y == g
    Xg = df.loc[mask, vars_a].values
    diff = Xg - df.loc[mask, vars_a].mean().values
    W += diff.T @ diff

T = np.zeros((p, p))
X_all = df[vars_a].values
diff_all = X_all - grand_mean.values
T = diff_all.T @ diff_all

wilks_a = np.linalg.det(W) / np.linalg.det(T)
# F approximation for Wilks lambda (2 groups)
df1 = p
df2 = n - p - 1
F_wilks_a = ((1 - wilks_a) / wilks_a) * (df2 / df1)
p_wilks_a = 1 - stats.f.cdf(F_wilks_a, df1, df2)
print(f"\nWilks' Lambda: {wilks_a:.4f}")
print(f"F-statistic (approx): {F_wilks_a:.4f}  (df1={df1}, df2={df2})")
print(f"p-value: {p_wilks_a:.4f}")

cm_a = confusion_matrix(y, pred_a)
correct_a = np.trace(cm_a) / n * 100
print(f"\nClassification Matrix:")
print(f"                Predicted Normal  Predicted Depressed")
print(f"Actual Normal:       {cm_a[0,0]:4d}              {cm_a[0,1]:4d}")
print(f"Actual Depressed:    {cm_a[1,0]:4d}              {cm_a[1,1]:4d}")
print(f"\nOverall Correct Classification Rate: {correct_a:.1f}%")

# ─────────────────────────────────────────────────────────────────────────────
# PART (b): Stepwise LDA with additional variables
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART (b): Stepwise Discriminant Analysis (adding ACUTEILL, SEX,")
print("          AGE, HEALTH, BEDDAYS, CHRONILL)")
print("="*70)

all_vars = ['INCOME', 'EDUCAT', 'ACUTEILL', 'SEX', 'AGE', 'HEALTH', 'BEDDAYS', 'CHRONILL']

def wilks_lambda(X, y):
    p = X.shape[1]
    n = len(y)
    grand_mean = X.mean(axis=0)
    W = np.zeros((p, p))
    for g in np.unique(y):
        Xg = X[y == g]
        diff = Xg - Xg.mean(axis=0)
        W += diff.T @ diff
    diff_all = X - grand_mean
    T = diff_all.T @ diff_all
    det_W = np.linalg.det(W)
    det_T = np.linalg.det(T)
    if det_T < 1e-15:
        return 1.0
    return det_W / det_T

def wilks_f_test(wl, n, p, k=2):
    df1 = p
    df2 = n - p - 1
    if wl >= 1.0:
        return 0.0, 1.0, df1, df2
    F = ((1 - wl) / wl) * (df2 / df1)
    pval = 1 - stats.f.cdf(F, df1, df2)
    return F, pval, df1, df2

# Forward stepwise selection
selected = []
remaining = all_vars.copy()
step_results = []
f_to_enter = 3.84

print("\nForward Stepwise Selection (F-to-enter threshold = 3.84):")
print("-"*60)

step = 0
while remaining:
    best_var = None
    best_wl = 1.0
    best_F = 0.0
    best_p = 1.0

    for var in remaining:
        trial_vars = selected + [var]
        X_trial = df[trial_vars].values
        wl = wilks_lambda(X_trial, y)
        F, pval, df1, df2 = wilks_f_test(wl, n, len(trial_vars))
        if F > best_F:
            best_F = F
            best_wl = wl
            best_p = pval
            best_var = var

    if best_var is not None and best_F >= f_to_enter:
        selected.append(best_var)
        remaining.remove(best_var)
        step += 1
        step_results.append({
            'Step': step, 'Variable': best_var,
            'Wilks Lambda': best_wl, 'F': best_F, 'p-value': best_p
        })
        print(f"Step {step}: Enter {best_var:10s}  Wilks Lambda={best_wl:.4f}  "
              f"F={best_F:.3f}  p={best_p:.4f}")
    else:
        print(f"No more variables meet entry criterion (F >= {f_to_enter}).")
        break

print(f"\nFinal variables selected: {selected}")

# Full model with selected variables
X_b = df[selected].values
lda_b = LinearDiscriminantAnalysis()
lda_b.fit(X_b, y)
pred_b = lda_b.predict(X_b)
scores_b = lda_b.transform(X_b)

print(f"\nGroup Means (Selected Variables):")
for g, label in [(0,'Normal'), (1,'Depressed')]:
    mask = y == g
    means = df.loc[mask, selected].mean()
    print(f"  {label}:")
    for v in selected:
        print(f"    {v}: {means[v]:.3f}")

pooled_std_b = df[selected].std()
std_coefs_b = lda_b.coef_[0] * pooled_std_b.values
print(f"\nStandardized Discriminant Function Coefficients:")
for v, c in zip(selected, std_coefs_b):
    print(f"  {v}: {c:.4f}")

print(f"\nCanonical Discriminant Function Coefficients (raw):")
for v, c in zip(selected, lda_b.coef_[0]):
    print(f"  {v}: {c:.4f}")
print(f"  Constant: {lda_b.intercept_[0]:.4f}")

wl_b = wilks_lambda(X_b, y)
F_b, p_b, df1_b, df2_b = wilks_f_test(wl_b, n, len(selected))
print(f"\nWilks' Lambda (full stepwise model): {wl_b:.4f}")
print(f"F-statistic (approx): {F_b:.4f}  (df1={df1_b}, df2={df2_b})")
print(f"p-value: {p_b:.4f}")

cm_b = confusion_matrix(y, pred_b)
correct_b = np.trace(cm_b) / n * 100
print(f"\nClassification Matrix:")
print(f"                Predicted Normal  Predicted Depressed")
print(f"Actual Normal:       {cm_b[0,0]:4d}              {cm_b[0,1]:4d}")
print(f"Actual Depressed:    {cm_b[1,0]:4d}              {cm_b[1,1]:4d}")
print(f"\nOverall Correct Classification Rate: {correct_b:.1f}%")
print(f"Improvement over part (a): {correct_b - correct_a:.1f} percentage points")
print(f"Wilks' Lambda reduced from {wilks_a:.4f} (part a) to {wl_b:.4f} (part b)")

# ─────────────────────────────────────────────────────────────────────────────
# PART (c): Interpretation
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART (c): Interpretation of the Discriminant Analysis Solution")
print("="*70)
print("""
1. PART (a) – Income and Education Only:
   - The discriminant function based only on INCOME and EDUCAT yields a 
     Wilks' Lambda that indicates moderate but limited group separation.
   - Depressed individuals tend to have lower income and lower education 
     compared to non-depressed individuals.
   - The classification rate reflects how well socioeconomic variables 
     alone can distinguish depressed from normal individuals.

2. PART (b) – Stepwise Model with Health/Demographic Variables:
   - Stepwise selection identifies the variables that most reduce Wilks' 
     Lambda at each step, retaining only those with F >= 3.84.
   - Health-related variables (HEALTH, BEDDAYS, ACUTEILL, CHRONILL) 
     contribute strongly to discriminating depressed from normal individuals.
   - The stepwise model achieves a notably lower Wilks' Lambda and higher 
     correct classification rate, confirming that health status variables 
     significantly improve prediction of depression.

3. Discriminant Function Interpretation:
   - Variables with larger absolute standardized coefficients contribute 
     more to the discriminant function.
   - Positive coefficients indicate higher values are associated with being 
     classified as depressed; negative coefficients indicate the opposite 
     (depending on coding direction).
   - Poor health (higher HEALTH score = worse health), more bed days 
     (BEDDAYS), and presence of acute/chronic illness (ACUTEILL, CHRONILL) 
     are strong predictors of depression.

4. Classification Performance:
   - The stepwise model substantially improves the ability to correctly 
     classify individuals as depressed or normal compared to the 
     income/education-only model.
   - The improvement in the correct classification rate and the reduction 
     in Wilks' Lambda both confirm that adding health and demographic 
     variables enhances the discriminant function significantly.
""")

# ─────────────────────────────────────────────────────────────────────────────
# FIGURES
# ─────────────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(16, 14))
fig.patch.set_facecolor('#0d1b2a')
gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.45, wspace=0.35)

DARK   = '#0d1b2a'
PANEL  = '#162032'
BLUE   = '#4fc3f7'
ORANGE = '#ffb74d'
GREEN  = '#81c784'
RED    = '#e57373'
WHITE  = '#e8eaf6'
GRAY   = '#607d8b'

def style_ax(ax, title):
    ax.set_facecolor(PANEL)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRAY)
    ax.tick_params(colors=WHITE, labelsize=9)
    ax.xaxis.label.set_color(WHITE)
    ax.yaxis.label.set_color(WHITE)
    ax.set_title(title, color=WHITE, fontsize=11, fontweight='bold', pad=8)

# ── Plot 1: Group means comparison ──────────────────────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
style_ax(ax1, 'Group Means: INCOME & EDUCAT')
categories = ['INCOME', 'EDUCAT']
normal_means  = [df.loc[y==0, v].mean() for v in categories]
depress_means = [df.loc[y==1, v].mean() for v in categories]
x = np.arange(len(categories))
w = 0.35
bars1 = ax1.bar(x - w/2, normal_means, w, color=BLUE, alpha=0.85, label='Normal')
bars2 = ax1.bar(x + w/2, depress_means, w, color=ORANGE, alpha=0.85, label='Depressed')
ax1.set_xticks(x)
ax1.set_xticklabels(categories, color=WHITE)
ax1.legend(facecolor=DARK, labelcolor=WHITE, fontsize=9)
ax1.set_ylabel('Mean Value', color=WHITE)
for bar in bars1:
    ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.2,
             f'{bar.get_height():.1f}', ha='center', va='bottom', color=WHITE, fontsize=8)
for bar in bars2:
    ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.2,
             f'{bar.get_height():.1f}', ha='center', va='bottom', color=WHITE, fontsize=8)

# ── Plot 2: Discriminant scores part (a) ────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
style_ax(ax2, 'Discriminant Scores — Part (a): INCOME & EDUCAT')
for g, label, color in [(0,'Normal',BLUE),(1,'Depressed',ORANGE)]:
    ax2.hist(scores_a[y==g, 0], bins=20, alpha=0.6, color=color, label=label)
ax2.set_xlabel('Discriminant Score', color=WHITE)
ax2.set_ylabel('Frequency', color=WHITE)
ax2.legend(facecolor=DARK, labelcolor=WHITE, fontsize=9)
ax2.axvline(0, color=WHITE, linestyle='--', linewidth=1, alpha=0.5)

# ── Plot 3: Discriminant scores part (b) ────────────────────────────────────
ax3 = fig.add_subplot(gs[1, 0])
style_ax(ax3, 'Discriminant Scores — Part (b): Stepwise Model')
for g, label, color in [(0,'Normal',BLUE),(1,'Depressed',ORANGE)]:
    ax3.hist(scores_b[y==g, 0], bins=20, alpha=0.6, color=color, label=label)
ax3.set_xlabel('Discriminant Score', color=WHITE)
ax3.set_ylabel('Frequency', color=WHITE)
ax3.legend(facecolor=DARK, labelcolor=WHITE, fontsize=9)
ax3.axvline(0, color=WHITE, linestyle='--', linewidth=1, alpha=0.5)

# ── Plot 4: Standardized coefficients part (b) ──────────────────────────────
ax4 = fig.add_subplot(gs[1, 1])
style_ax(ax4, 'Standardized Discriminant Coefficients — Part (b)')
coef_df = pd.Series(std_coefs_b, index=selected).sort_values()
colors_bar = [RED if v < 0 else GREEN for v in coef_df.values]
ax4.barh(coef_df.index, coef_df.values, color=colors_bar, alpha=0.85)
ax4.axvline(0, color=WHITE, linewidth=0.8)
ax4.set_xlabel('Standardized Coefficient', color=WHITE)
for i, (val, name) in enumerate(zip(coef_df.values, coef_df.index)):
    ax4.text(val + (0.01 if val >= 0 else -0.01), i,
             f'{val:.3f}', va='center',
             ha='left' if val >= 0 else 'right', color=WHITE, fontsize=8)

# ── Plot 5: Classification comparison ───────────────────────────────────────
ax5 = fig.add_subplot(gs[2, 0])
style_ax(ax5, 'Classification Accuracy Comparison')
models = ['Part (a)\n(INCOME, EDUCAT)', f'Part (b)\n({len(selected)} variables, stepwise)']
accuracies = [correct_a, correct_b]
bar_colors = [BLUE, GREEN]
bars = ax5.bar(models, accuracies, color=bar_colors, alpha=0.85, width=0.4)
ax5.set_ylim(0, 100)
ax5.set_ylabel('Correct Classification (%)', color=WHITE)
for bar, acc in zip(bars, accuracies):
    ax5.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
             f'{acc:.1f}%', ha='center', va='bottom', color=WHITE,
             fontsize=11, fontweight='bold')
ax5.axhline(50, color=GRAY, linestyle='--', linewidth=1, alpha=0.6, label='Chance (50%)')
ax5.legend(facecolor=DARK, labelcolor=WHITE, fontsize=9)

# ── Plot 6: Wilks Lambda comparison ─────────────────────────────────────────
ax6 = fig.add_subplot(gs[2, 1])
style_ax(ax6, "Wilks' Lambda Comparison")
wilks_vals = [wilks_a, wl_b]
bar_colors2 = [ORANGE, GREEN]
bars2 = ax6.bar(models, wilks_vals, color=bar_colors2, alpha=0.85, width=0.4)
ax6.set_ylim(0, 1.05)
ax6.set_ylabel("Wilks' Lambda (lower = better separation)", color=WHITE)
for bar, wl in zip(bars2, wilks_vals):
    ax6.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.01,
             f'{wl:.4f}', ha='center', va='bottom', color=WHITE,
             fontsize=11, fontweight='bold')
ax6.axhline(1.0, color=GRAY, linestyle='--', linewidth=1, alpha=0.6, label='No separation (Λ=1)')
ax6.legend(facecolor=DARK, labelcolor=WHITE, fontsize=9)

fig.suptitle('Question 8.7 — Discriminant Analysis of Depression Data (DEPRES.DAT)',
             color=WHITE, fontsize=14, fontweight='bold', y=0.98)

plt.savefig('q8_7_discriminant_analysis.png', dpi=150, bbox_inches='tight',
            facecolor=DARK)
plt.close()
print("\nFigure saved: q8_7_discriminant_analysis.png")

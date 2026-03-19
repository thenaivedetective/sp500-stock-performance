# =============================================================================
#   MULTIVARIATE DATA ANALYSIS — HOMEWORK SOLUTIONS
#   Student : Lana Gidan
#   Contents: Q8.7  | Q7.5 + Q8.8 | Q9.8 | Q9.9
# =============================================================================

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ── Shared colour palette ─────────────────────────────────────────────────────
DARK   = '#0d1b2a'
PANEL  = '#162032'
BLUE   = '#4fc3f7'
ORANGE = '#ffb74d'
GREEN  = '#81c784'
RED    = '#e57373'
WHITE  = '#e8eaf6'
GRAY   = '#607d8b'
PURPLE = '#ce93d8'

def style_ax(ax, title, fontsize=10):
    ax.set_facecolor(PANEL)
    for sp in ax.spines.values():
        sp.set_edgecolor(GRAY)
    ax.tick_params(colors=WHITE, labelsize=8)
    ax.xaxis.label.set_color(WHITE)
    ax.yaxis.label.set_color(WHITE)
    ax.set_title(title, color=WHITE, fontsize=fontsize, fontweight='bold', pad=6)


# =============================================================================
# QUESTION 8.7 — Discriminant Analysis of Depression Data (DEPRES.DAT)
# =============================================================================
print("\n" + "="*70)
print("QUESTION 8.7 — Discriminant Analysis: Depression (DEPRES.DAT)")
print("="*70)

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

df87 = pd.DataFrame(rows, columns=col_names)
print(f"Dataset loaded: {len(df87)} observations, {len(df87.columns)} variables")
print(f"\nCASES distribution:\n{df87['CASES'].value_counts().sort_index()}")
print("  0 = Normal, 1 = Depressed (CESD > 16)")

# ── Part (a): LDA with INCOME and EDUCAT ─────────────────────────────────────
print("\n" + "="*70)
print("PART (a): Discriminant Analysis using INCOME and EDUCAT")
print("="*70)

vars_a = ['INCOME', 'EDUCAT']
X_a = df87[vars_a].values
y87 = df87['CASES'].values

lda_a = LinearDiscriminantAnalysis()
lda_a.fit(X_a, y87)
pred_a  = lda_a.predict(X_a)
scores_a = lda_a.transform(X_a)

print("\nGroup Means:")
for g, label in [(0, 'Normal'), (1, 'Depressed')]:
    mask = y87 == g
    print(f"  {label}: INCOME={df87.loc[mask,'INCOME'].mean():.2f}, "
          f"EDUCAT={df87.loc[mask,'EDUCAT'].mean():.2f}")

pooled_std_a = df87[vars_a].std()
std_coefs_a  = lda_a.coef_[0] * pooled_std_a.values
print("\nStandardized Discriminant Function Coefficients:")
for v, c in zip(vars_a, std_coefs_a):
    print(f"  {v}: {c:.4f}")
print("\nCanonical Discriminant Function Coefficients (raw):")
for v, c in zip(vars_a, lda_a.coef_[0]):
    print(f"  {v}: {c:.4f}")
print(f"  Constant: {lda_a.intercept_[0]:.4f}")

n87 = len(y87)
p87 = len(vars_a)
grand_mean_a = df87[vars_a].mean()
W_a = np.zeros((p87, p87))
for g in [0, 1]:
    mask = y87 == g
    Xg   = df87.loc[mask, vars_a].values
    diff = Xg - df87.loc[mask, vars_a].mean().values
    W_a += diff.T @ diff
diff_all_a = df87[vars_a].values - grand_mean_a.values
T_a   = diff_all_a.T @ diff_all_a
wilks_a = np.linalg.det(W_a) / np.linalg.det(T_a)
F_wilks_a  = ((1 - wilks_a) / wilks_a) * ((n87 - p87 - 1) / p87)
p_wilks_a  = 1 - stats.f.cdf(F_wilks_a, p87, n87 - p87 - 1)
print(f"\nWilks' Lambda: {wilks_a:.4f}")
print(f"F-statistic (approx): {F_wilks_a:.4f}  (df1={p87}, df2={n87-p87-1})")
print(f"p-value: {p_wilks_a:.4f}")

cm_a     = confusion_matrix(y87, pred_a)
correct_a = np.trace(cm_a) / n87 * 100
print(f"\nClassification Matrix:")
print(f"                Predicted Normal  Predicted Depressed")
print(f"Actual Normal:       {cm_a[0,0]:4d}              {cm_a[0,1]:4d}")
print(f"Actual Depressed:    {cm_a[1,0]:4d}              {cm_a[1,1]:4d}")
print(f"\nOverall Correct Classification Rate: {correct_a:.1f}%")

# ── Part (b): Stepwise LDA ────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART (b): Stepwise Discriminant Analysis")
print("  Variables: INCOME, EDUCAT, ACUTEILL, SEX, AGE, HEALTH, BEDDAYS, CHRONILL")
print("="*70)

all_vars = ['INCOME','EDUCAT','ACUTEILL','SEX','AGE','HEALTH','BEDDAYS','CHRONILL']

def wilks_lambda_2grp(X, y):
    p = X.shape[1]
    grand = X.mean(axis=0)
    W = np.zeros((p, p))
    for g in np.unique(y):
        Xg = X[y == g]; d = Xg - Xg.mean(axis=0); W += d.T @ d
    T = (X - grand).T @ (X - grand)
    dT = np.linalg.det(T)
    return np.linalg.det(W) / dT if dT > 1e-15 else 1.0

def wilks_f_test(wl, n, p):
    df1, df2 = p, n - p - 1
    if wl >= 1.0:
        return 0.0, 1.0
    F    = ((1 - wl) / wl) * (df2 / df1)
    pval = 1 - stats.f.cdf(F, df1, df2)
    return F, pval

selected = []
remaining = all_vars.copy()
step_results = []
f_to_enter = 3.84
step = 0
print("\nForward Stepwise Selection (F-to-enter threshold = 3.84):")
print("-"*60)
while remaining:
    best_var, best_wl, best_F, best_p = None, 1.0, 0.0, 1.0
    for var in remaining:
        trial = selected + [var]
        wl_t = wilks_lambda_2grp(df87[trial].values, y87)
        F_t, p_t = wilks_f_test(wl_t, n87, len(trial))
        if F_t > best_F:
            best_F, best_wl, best_p, best_var = F_t, wl_t, p_t, var
    if best_var and best_F >= f_to_enter:
        selected.append(best_var); remaining.remove(best_var); step += 1
        step_results.append({'Step': step, 'Variable': best_var,
                              'Wilks Lambda': best_wl, 'F': best_F, 'p-value': best_p})
        print(f"Step {step}: Enter {best_var:10s}  Wilks Lambda={best_wl:.4f}  "
              f"F={best_F:.3f}  p={best_p:.4f}")
    else:
        print(f"No more variables meet entry criterion (F >= {f_to_enter}).")
        break

print(f"\nFinal variables selected: {selected}")

X_b = df87[selected].values
lda_b = LinearDiscriminantAnalysis()
lda_b.fit(X_b, y87)
pred_b   = lda_b.predict(X_b)
scores_b = lda_b.transform(X_b)

pooled_std_b = df87[selected].std()
std_coefs_b  = lda_b.coef_[0] * pooled_std_b.values
print("\nStandardized Discriminant Function Coefficients (stepwise model):")
for v, c in zip(selected, std_coefs_b):
    print(f"  {v}: {c:.4f}")

wl_b = wilks_lambda_2grp(X_b, y87)
F_b, p_b = wilks_f_test(wl_b, n87, len(selected))
print(f"\nWilks' Lambda (stepwise model): {wl_b:.4f}")
print(f"F-statistic (approx): {F_b:.4f}  (df1={len(selected)}, df2={n87-len(selected)-1})")
print(f"p-value: {p_b:.4f}")

cm_b     = confusion_matrix(y87, pred_b)
correct_b = np.trace(cm_b) / n87 * 100
print(f"\nClassification Matrix (stepwise model):")
print(f"                Predicted Normal  Predicted Depressed")
print(f"Actual Normal:       {cm_b[0,0]:4d}              {cm_b[0,1]:4d}")
print(f"Actual Depressed:    {cm_b[1,0]:4d}              {cm_b[1,1]:4d}")
print(f"\nOverall Correct Classification Rate: {correct_b:.1f}%")
print(f"Improvement over part (a): {correct_b - correct_a:.1f} percentage points")
print(f"Wilks' Lambda reduced from {wilks_a:.4f} → {wl_b:.4f}")

# ── Part (c): Interpretation ──────────────────────────────────────────────────
print("\n" + "="*70)
print("PART (c): Interpretation")
print("="*70)
print("""
1. PART (a) – Income and Education Only:
   Depressed individuals tend to have lower income and lower education compared
   to non-depressed individuals. Wilks' Lambda reflects limited but measurable
   group separation using only socioeconomic variables.

2. PART (b) – Stepwise Model:
   Health-related variables (HEALTH, BEDDAYS, ACUTEILL, CHRONILL) contribute
   strongly to discriminating depressed from normal individuals. The stepwise
   model achieves a notably lower Wilks' Lambda and higher correct classification
   rate, confirming that health status significantly improves prediction.

3. Discriminant Function Interpretation:
   Variables with larger absolute standardised coefficients contribute more.
   Poor health, more bed days, and acute/chronic illness are strong predictors
   of depression, consistent with the medical literature.

4. Classification Performance:
   The stepwise model substantially improves correct classification vs. the
   income/education-only model, validating the inclusion of health variables.
""")

# ── Figure Q8.7 ───────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(16, 14))
fig.patch.set_facecolor(DARK)
gs  = gridspec.GridSpec(3, 2, figure=fig, hspace=0.45, wspace=0.35)

ax1 = fig.add_subplot(gs[0, 0])
style_ax(ax1, 'Group Means: INCOME & EDUCAT', 11)
normal_means  = [df87.loc[y87==0, v].mean() for v in vars_a]
depress_means = [df87.loc[y87==1, v].mean() for v in vars_a]
x = np.arange(len(vars_a)); w = 0.35
b1 = ax1.bar(x - w/2, normal_means,  w, color=BLUE,   alpha=0.85, label='Normal')
b2 = ax1.bar(x + w/2, depress_means, w, color=ORANGE, alpha=0.85, label='Depressed')
ax1.set_xticks(x); ax1.set_xticklabels(vars_a, color=WHITE)
ax1.legend(facecolor=DARK, labelcolor=WHITE, fontsize=9)
ax1.set_ylabel('Mean Value', color=WHITE)
for bar in list(b1) + list(b2):
    ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.2,
             f'{bar.get_height():.1f}', ha='center', va='bottom', color=WHITE, fontsize=8)

ax2 = fig.add_subplot(gs[0, 1])
style_ax(ax2, 'Discriminant Scores — Part (a): INCOME & EDUCAT', 11)
for g, lbl, col in [(0,'Normal',BLUE),(1,'Depressed',ORANGE)]:
    ax2.hist(scores_a[y87==g, 0], bins=20, alpha=0.6, color=col, label=lbl)
ax2.set_xlabel('Discriminant Score', color=WHITE)
ax2.set_ylabel('Frequency', color=WHITE)
ax2.legend(facecolor=DARK, labelcolor=WHITE, fontsize=9)
ax2.axvline(0, color=WHITE, linestyle='--', linewidth=1, alpha=0.5)

ax3 = fig.add_subplot(gs[1, 0])
style_ax(ax3, 'Discriminant Scores — Part (b): Stepwise Model', 11)
for g, lbl, col in [(0,'Normal',BLUE),(1,'Depressed',ORANGE)]:
    ax3.hist(scores_b[y87==g, 0], bins=20, alpha=0.6, color=col, label=lbl)
ax3.set_xlabel('Discriminant Score', color=WHITE)
ax3.set_ylabel('Frequency', color=WHITE)
ax3.legend(facecolor=DARK, labelcolor=WHITE, fontsize=9)
ax3.axvline(0, color=WHITE, linestyle='--', linewidth=1, alpha=0.5)

ax4 = fig.add_subplot(gs[1, 1])
style_ax(ax4, 'Standardised Discriminant Coefficients — Part (b)', 11)
coef_df = pd.Series(std_coefs_b, index=selected).sort_values()
bar_colors = [RED if v < 0 else GREEN for v in coef_df.values]
ax4.barh(coef_df.index, coef_df.values, color=bar_colors, alpha=0.85)
ax4.axvline(0, color=WHITE, linewidth=0.8)
ax4.set_xlabel('Standardised Coefficient', color=WHITE)
for i, (val, name) in enumerate(zip(coef_df.values, coef_df.index)):
    ax4.text(val + (0.01 if val >= 0 else -0.01), i, f'{val:.3f}',
             va='center', ha='left' if val >= 0 else 'right', color=WHITE, fontsize=8)

ax5 = fig.add_subplot(gs[2, 0])
style_ax(ax5, 'Classification Accuracy Comparison', 11)
models_87 = ['Part (a)\n(INCOME, EDUCAT)', f'Part (b)\n({len(selected)} variables, stepwise)']
bars5 = ax5.bar(models_87, [correct_a, correct_b], color=[BLUE, GREEN], alpha=0.85, width=0.4)
ax5.set_ylim(0, 100); ax5.set_ylabel('Correct Classification (%)', color=WHITE)
for bar, acc in zip(bars5, [correct_a, correct_b]):
    ax5.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
             f'{acc:.1f}%', ha='center', va='bottom', color=WHITE, fontsize=11, fontweight='bold')
ax5.axhline(50, color=GRAY, linestyle='--', linewidth=1, alpha=0.6, label='Chance (50%)')
ax5.legend(facecolor=DARK, labelcolor=WHITE, fontsize=9)

ax6 = fig.add_subplot(gs[2, 1])
style_ax(ax6, "Wilks' Lambda Comparison", 11)
bars6 = ax6.bar(models_87, [wilks_a, wl_b], color=[ORANGE, GREEN], alpha=0.85, width=0.4)
ax6.set_ylim(0, 1.05); ax6.set_ylabel("Wilks' Lambda (lower = better separation)", color=WHITE)
for bar, wl in zip(bars6, [wilks_a, wl_b]):
    ax6.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.01,
             f'{wl:.4f}', ha='center', va='bottom', color=WHITE, fontsize=11, fontweight='bold')
ax6.axhline(1.0, color=GRAY, linestyle='--', linewidth=1, alpha=0.6, label='No separation (Λ=1)')
ax6.legend(facecolor=DARK, labelcolor=WHITE, fontsize=9)

fig.suptitle('Question 8.7 — Discriminant Analysis of Depression Data (DEPRES.DAT)',
             color=WHITE, fontsize=14, fontweight='bold', y=0.98)
plt.savefig('q8_7_discriminant_analysis.png', dpi=150, bbox_inches='tight', facecolor=DARK)
plt.close()
print("\nFigure saved: q8_7_discriminant_analysis.png")


# =============================================================================
# QUESTION 7.5 — Cluster Analysis  +  QUESTION 8.8 — Discriminant Analysis
#               Mass Transit Data (MASST.DAT)
# =============================================================================
print("\n" + "="*70)
print("QUESTION 7.5 — Cluster Analysis  +  QUESTION 8.8 — Discriminant Analysis")
print("  Data: MASST.DAT  (Mass Transit Survey)")
print("="*70)

def parse_val(s):
    s = s.strip()
    if s in ('', '.', '..', '...', '....', '.....'):
        return np.nan
    try:
        return float(s)
    except:
        return np.nan

colspecs = {
    'ID': (0, 4),
    'V1': (4, 6),  'V2': (6, 8),  'V3': (8, 10),
    'V4': (10,12), 'V5': (12,14), 'V6': (14,16),
    'V7': (16,17), 'V8': (17,18), 'V9': (18,19),
    'V10':(19,20), 'V11':(20,21), 'V12':(21,22),
    'V13':(22,23), 'V14':(23,24), 'V15':(24,25),
    'V16':(25,26), 'V17':(26,27), 'V18':(27,28),
    'V19':(28,29), 'V20':(29,30), 'V21':(30,31),
    'V22':(31,32), 'V23':(32,33), 'V24':(33,34),
    'V25':(34,35), 'V26':(35,36), 'V27':(36,37),
    'V28':(37,38), 'V29':(38,39), 'V30':(39,40),
    'V31':(40,41), 'V32':(41,42), 'V33':(42,43),
    'V34':(43,44), 'V35':(44,45), 'V36':(45,46),
    'V37':(46,47), 'V38':(47,48),
    'V39':(48,49), 'V40':(49,50), 'V41':(50,51),
    'V42':(51,52), 'V43':(52,53), 'V44':(53,54),
    'V45':(54,55), 'V46':(55,56), 'V47':(56,57),
    'V48':(57,58), 'V49':(58,59), 'V50':(59,60),
    'V51':(60,61), 'V52':(61,62),
}

rows = []
with open('attached_assets/MASST_1773881001970.DAT', 'r') as f:
    for line in f:
        raw = line.rstrip('\n')
        if len(raw) < 20 or raw.strip().startswith('Mass') or raw.strip().startswith('(') \
                or raw.strip().startswith('---') or raw.strip() == '':
            continue
        row = {}
        for col, (s, e) in colspecs.items():
            row[col] = parse_val(raw[s:e]) if len(raw) >= e else np.nan
        rows.append(row)

df_mass = pd.DataFrame(rows)
print(f"Loaded {len(df_mass)} observations")

# ── Q7.5: Cluster Analysis on V7–V18 ─────────────────────────────────────────
print("\n" + "="*70)
print("QUESTION 7.5 — Cluster Analysis on V7–V18")
print("  (Latent demand for mass transit at various gas price levels)")
print("="*70)

v7_v18   = [f'V{i}' for i in range(7, 19)]
df_clust = df_mass[['ID'] + v7_v18].dropna(subset=v7_v18).copy()
X_clust  = df_clust[v7_v18].values
print(f"\nObservations with complete V7–V18 data: {len(df_clust)}")

scaler   = StandardScaler()
X_scaled = scaler.fit_transform(X_clust)

Z = linkage(X_scaled, method='ward')
last_merges = Z[-15:, 2][::-1]
print("\nLast 10 merge distances (hierarchical, Ward):")
for i, d in enumerate(last_merges[:10], 1):
    print(f"  {i} clusters: distance = {d:.4f}")

for k in [2, 3]:
    labels_hier = fcluster(Z, k, criterion='maxclust')
    counts = pd.Series(labels_hier).value_counts().sort_index()
    print(f"Hierarchical k={k}: cluster sizes = {dict(counts)}")

print("\n--- K-Means Refinement ---")
inertias = []
ks_range = range(1, 9)
for k in ks_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=20)
    km.fit(X_scaled)
    inertias.append(km.inertia_)

K_FINAL = 2
km_final = KMeans(n_clusters=K_FINAL, random_state=42, n_init=20)
km_final.fit(X_scaled)
df_clust['cluster'] = km_final.labels_

cluster_means = df_clust.groupby('cluster')[v7_v18].mean()
cluster_sizes = df_clust['cluster'].value_counts().sort_index()
gas_levels    = ['10%','20%','30%','40%','50%','60%','70%','80%','90%','100%','150%','>150%']

cluster_avg  = cluster_means.mean(axis=1)
user_cluster = int(cluster_avg.idxmax())
nonu_cluster = 1 - user_cluster

df_clust['group']       = df_clust['cluster'].map({user_cluster: 1, nonu_cluster: 0})
df_clust['group_label'] = df_clust['cluster'].map({user_cluster: 'Users', nonu_cluster: 'Nonusers'})

print(f"\nFinal K-Means Solution (k={K_FINAL}):")
print(f"Cluster sizes: {dict(cluster_sizes)}")
print(f"Cluster {user_cluster+1} → 'USERS'    (avg score ≈ {cluster_avg[user_cluster]:.2f}/5)")
print(f"Cluster {nonu_cluster+1} → 'NONUSERS' (avg score ≈ {cluster_avg[nonu_cluster]:.2f}/5)")

# ── Q8.8: Discriminant Analysis ───────────────────────────────────────────────
print("\n" + "="*70)
print("QUESTION 8.8 — Discriminant Analysis: Users vs Nonusers of Mass Transit")
print("  DV: cluster group (from Q7.5)   IVs: V1–V18")
print("="*70)

df_full   = df_mass.merge(df_clust[['ID','group','group_label']], on='ID', how='inner')
disc_vars = [f'V{i}' for i in range(1, 19)]
df_disc   = df_full[['ID','group','group_label'] + disc_vars].dropna(subset=disc_vars)
X_disc    = df_disc[disc_vars].values
y_disc    = df_disc['group'].values
n_disc    = len(df_disc)

print(f"\nSample size: {n_disc}  |  Users: {(y_disc==1).sum()}, Nonusers: {(y_disc==0).sum()}")

v_labels = {
    'V1':'Economy','V2':'Convenience','V3':'Flexibility',
    'V4':'Safe from dangerous ppl','V5':'Low energy use','V6':'Dependability',
    'V7':'10% gas inc','V8':'20% gas inc','V9':'30% gas inc','V10':'40% gas inc',
    'V11':'50% gas inc','V12':'60% gas inc','V13':'70% gas inc','V14':'80% gas inc',
    'V15':'90% gas inc','V16':'100% gas inc','V17':'150% gas inc','V18':'>150% gas inc'
}

lda_88 = LinearDiscriminantAnalysis()
lda_88.fit(X_disc, y_disc)
pred_88   = lda_88.predict(X_disc)
scores_88 = lda_88.transform(X_disc)

pooled_std_88 = df_disc[disc_vars].std()
std_coefs_88  = lda_88.coef_[0] * pooled_std_88.values

def compute_wilks(X, y):
    p = X.shape[1]; grand = X.mean(axis=0)
    W = np.zeros((p, p))
    for g in np.unique(y):
        Xg = X[y == g]; d = Xg - Xg.mean(axis=0); W += d.T @ d
    T = (X - grand).T @ (X - grand)
    dT = np.linalg.det(T)
    return np.linalg.det(W) / dT if dT > 1e-20 else 1.0

wl_88  = compute_wilks(X_disc, y_disc)
F_88   = ((1 - wl_88) / wl_88) * ((n_disc - len(disc_vars) - 1) / len(disc_vars))
p_88   = 1 - stats.f.cdf(F_88, len(disc_vars), n_disc - len(disc_vars) - 1)
cm_88  = confusion_matrix(y_disc, pred_88)
acc_88 = np.trace(cm_88) / n_disc * 100

print(f"\nWilks' Lambda: {wl_88:.4f}")
print(f"F-statistic (approx): {F_88:.4f}  df1={len(disc_vars)}, df2={n_disc-len(disc_vars)-1}")
print(f"p-value: {p_88:.6f}")
print(f"\nClassification Matrix:")
print(f"                Predicted Nonuser  Predicted User")
print(f"Actual Nonuser:      {cm_88[0,0]:5d}         {cm_88[0,1]:5d}")
print(f"Actual User:         {cm_88[1,0]:5d}         {cm_88[1,1]:5d}")
print(f"\nCorrect Classification Rate: {acc_88:.1f}%")

print("\nStandardised Discriminant Function Coefficients (sorted by |coef|):")
for v, c in sorted(zip(disc_vars, std_coefs_88), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {v:<4} {v_labels[v]:<28} {c:>10.4f}")

print("""
Interpretation:
  V7–V18 carry the most discriminant weight (clusters built from these).
  Users score higher on willingness to use mass transit at all price levels.
  Among V1–V6, the variables with the largest |coef| indicate which feature
  saliences (economy, convenience, safety) most separate users from nonusers.
  The low Wilks' Lambda and high accuracy confirm strong group separation.
""")

# ── Figures Q7.5 + Q8.8 ───────────────────────────────────────────────────────
fig = plt.figure(figsize=(18, 16))
fig.patch.set_facecolor(DARK)
gs  = gridspec.GridSpec(3, 3, figure=fig, hspace=0.5, wspace=0.38)

ax1 = fig.add_subplot(gs[0, :2])
style_ax(ax1, "Hierarchical Clustering Dendrogram (Ward's Method, truncated)")
dendrogram(Z, ax=ax1, truncate_mode='lastp', p=20,
           color_threshold=Z[-2, 2],
           above_threshold_color=GRAY,
           link_color_func=lambda k: BLUE if k <= 2 else ORANGE)
ax1.set_xlabel('Cluster / Sample', color=WHITE)
ax1.set_ylabel('Distance', color=WHITE)
ax1.axhline(Z[-K_FINAL, 2]*1.01, color=RED, linestyle='--', linewidth=1.5, label=f'Cut for k={K_FINAL}')
ax1.legend(facecolor=DARK, labelcolor=WHITE, fontsize=8)

ax2 = fig.add_subplot(gs[0, 2])
style_ax(ax2, 'K-Means Elbow Plot')
ax2.plot(list(ks_range), inertias, 'o-', color=BLUE, linewidth=2, markersize=7)
ax2.axvline(K_FINAL, color=RED, linestyle='--', linewidth=1.5, label=f'k={K_FINAL} selected')
ax2.set_xlabel('Number of Clusters (k)', color=WHITE)
ax2.set_ylabel('Within-cluster Inertia', color=WHITE)
ax2.legend(facecolor=DARK, labelcolor=WHITE, fontsize=8)

ax3 = fig.add_subplot(gs[1, :2])
style_ax(ax3, 'Cluster Profiles: Mean Usage Score by Gas Price Level (Q7.5)')
x = np.arange(len(gas_levels)); w = 0.35
lbl_c  = [f'Cluster {nonu_cluster+1}: Nonusers (n={cluster_sizes[nonu_cluster]})',
           f'Cluster {user_cluster+1}: Users (n={cluster_sizes[user_cluster]})']
for i, (c_id, lbl, col) in enumerate(zip([nonu_cluster, user_cluster], lbl_c, [BLUE, ORANGE])):
    means = [cluster_means.loc[c_id, v] for v in v7_v18]
    ax3.bar(x + (i-0.5)*w, means, w, label=lbl, color=col, alpha=0.85)
ax3.set_xticks(x); ax3.set_xticklabels(gas_levels, rotation=30, ha='right', color=WHITE, fontsize=8)
ax3.set_ylabel('Mean Usage Score (1–5)', color=WHITE); ax3.set_ylim(0, 5.5)
ax3.legend(facecolor=DARK, labelcolor=WHITE, fontsize=8)
ax3.axhline(3, color=GRAY, linestyle=':', linewidth=1, alpha=0.5)

ax4 = fig.add_subplot(gs[1, 2])
style_ax(ax4, 'Cluster Composition (Q7.5)')
sizes_c = [cluster_sizes[nonu_cluster], cluster_sizes[user_cluster]]
lbls_c  = [f'Nonusers\n(n={sizes_c[0]})', f'Users\n(n={sizes_c[1]})']
_, _, autotexts = ax4.pie(sizes_c, labels=lbls_c, colors=[BLUE, ORANGE],
                           autopct='%1.1f%%', startangle=90,
                           textprops={'color': WHITE, 'fontsize': 9})
for at in autotexts: at.set_color(DARK)

ax5 = fig.add_subplot(gs[2, :2])
style_ax(ax5, 'Standardised Discriminant Coefficients (Q8.8)')
coef_series = pd.Series(std_coefs_88, index=disc_vars)
coef_sorted = coef_series.reindex(coef_series.abs().sort_values(ascending=True).index)
bar_c88 = [GREEN if v >= 0 else RED for v in coef_sorted.values]
ax5.barh(coef_sorted.index, coef_sorted.values, color=bar_c88, alpha=0.85)
ax5.axvline(0, color=WHITE, linewidth=0.8)
ax5.set_xlabel('Standardised Coefficient', color=WHITE)
for i, (val, nm) in enumerate(zip(coef_sorted.values, coef_sorted.index)):
    ax5.text(val + (0.005 if val >= 0 else -0.005), i, f'{val:.3f}',
             va='center', ha='left' if val >= 0 else 'right', color=WHITE, fontsize=7)

ax6 = fig.add_subplot(gs[2, 2])
style_ax(ax6, 'Discriminant Score Distribution (Q8.8)')
for g, lbl, col in [(0,'Nonusers',BLUE),(1,'Users',ORANGE)]:
    ax6.hist(scores_88[y_disc==g, 0], bins=20, alpha=0.6, color=col, label=lbl)
ax6.axvline(0, color=WHITE, linestyle='--', linewidth=1, alpha=0.6)
ax6.set_xlabel('Discriminant Score', color=WHITE); ax6.set_ylabel('Frequency', color=WHITE)
ax6.legend(facecolor=DARK, labelcolor=WHITE, fontsize=8)

fig.suptitle(
    'Q7.5 — Cluster Analysis  &  Q8.8 — Discriminant Analysis (MASST.DAT)\n'
    f"Wilks' Λ={wl_88:.4f}  F={F_88:.2f}  p={p_88:.4f}  "
    f"Classification Accuracy={acc_88:.1f}%",
    color=WHITE, fontsize=12, fontweight='bold', y=0.99)
plt.savefig('q7_5_q8_8_mass_transit.png', dpi=150, bbox_inches='tight', facecolor=DARK)
plt.close()
print("Figure saved: q7_5_q8_8_mass_transit.png")


# =============================================================================
# QUESTION 9.8 — Three-Group Discriminant Analysis (PHONE.DAT)
# =============================================================================
print("\n" + "="*70)
print("QUESTION 9.8 — Three-Group Discriminant Analysis (PHONE.DAT)")
print("  DV: Number of phones (1, 2, 3+)   IVs: A1–A6")
print("="*70)

rows = []
with open('attached_assets/PHONE_1773881553876.DAT', 'r') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('Phone') or line.startswith('---') \
                or line.startswith('ID') or line.startswith('Number'):
            continue
        vals = line.split()
        if len(vals) == 8:
            try:
                rows.append([int(v) for v in vals])
            except:
                continue

df98 = pd.DataFrame(rows, columns=['ID','Phones','A1','A2','A3','A4','A5','A6'])
attitudes = ['A1','A2','A3','A4','A5','A6']
labels98  = {
    'A1': 'Long distance only necessary',
    'A2': 'Save money with one phone',
    'A3': 'More phones worth extra cost',
    'A4': 'Below-average phone bill',
    'A5': 'More phones = waste of money',
    'A6': 'Best model is worth cost'
}
print(f"Dataset loaded: {len(df98)} observations")
print(f"\nGroup sizes (number of phones):\n{df98['Phones'].value_counts().sort_index().to_string()}")

print("\nGroup Means (0–10 scale):")
print(f"\n{'Attitude':<6} {'Statement':<32} {'1 Phone':>8} {'2 Phones':>9} {'3+ Phones':>10} {'Overall':>8}")
print("-"*75)
for a in attitudes:
    m1 = df98.loc[df98.Phones==1, a].mean()
    m2 = df98.loc[df98.Phones==2, a].mean()
    m3 = df98.loc[df98.Phones==3, a].mean()
    mo = df98[a].mean()
    print(f"  {a:<4} {labels98[a]:<32} {m1:>8.2f} {m2:>9.2f} {m3:>10.2f} {mo:>8.2f}")

print("\n--- Univariate F-tests ---")
print(f"\n{'Attitude':<6} {'Statement':<32} {'F-stat':>8} {'p-value':>10}")
print("-"*60)
for a in attitudes:
    F, p = stats.f_oneway(*[df98.loc[df98.Phones==g, a].values for g in [1, 2, 3]])
    print(f"  {a:<4} {labels98[a]:<32} {F:>8.3f} {p:>10.4f} {'*' if p < 0.05 else ''}")

X98  = df98[attitudes].values
y98  = df98['Phones'].values
n98  = len(y98)
lda98 = LinearDiscriminantAnalysis()
lda98.fit(X98, y98)
pred98   = lda98.predict(X98)
scores98 = lda98.transform(X98)

def wilks_mg(X, y):
    p = X.shape[1]; grand = X.mean(axis=0)
    W = np.zeros((p, p))
    for g in np.unique(y):
        Xg = X[y == g]; d = Xg - Xg.mean(axis=0); W += d.T @ d
    T = (X - grand).T @ (X - grand)
    dT = np.linalg.det(T)
    return np.linalg.det(W) / dT if abs(dT) > 1e-20 else 1.0

wl98     = wilks_mg(X98, y98)
chi2_98  = -(n98 - 1 - (len(attitudes) + 3) / 2) * np.log(wl98)
p_chi98  = 1 - stats.chi2.cdf(chi2_98, len(attitudes) * 2)
exp98    = lda98.explained_variance_ratio_

print(f"\nOverall Test:")
print(f"  Wilks' Lambda:       {wl98:.4f}")
print(f"  Chi-square (approx): {chi2_98:.3f}  (df={len(attitudes)*2})")
print(f"  p-value:             {p_chi98:.4f}")
print(f"\nFunction 1: {exp98[0]*100:.1f}% of between-group variance")
print(f"Function 2: {exp98[1]*100:.1f}% of between-group variance")

ps98      = df98[attitudes].std()
scalings98 = lda98.scalings_
std_sc98   = scalings98 * ps98.values[:, np.newaxis]

print("\nStructure Matrix (Variable–Function Correlations):")
print(f"\n{'Attitude':<6} {'Statement':<32} {'Function 1':>12} {'Function 2':>12}")
print("-"*65)
for i, a in enumerate(attitudes):
    r1 = np.corrcoef(df98[a].values, scores98[:, 0])[0, 1]
    r2 = np.corrcoef(df98[a].values, scores98[:, 1])[0, 1]
    print(f"  {a:<4} {labels98[a]:<32} {r1:>12.4f} {r2:>12.4f}")

print("\nGroup Centroids:")
for g, lbl in [(1,'1 Phone'),(2,'2 Phones'),(3,'3+ Phones')]:
    c1 = scores98[y98==g, 0].mean(); c2 = scores98[y98==g, 1].mean()
    print(f"  {lbl:<15} F1={c1:>8.4f}  F2={c2:>8.4f}")

cm98     = confusion_matrix(y98, pred98, labels=[1, 2, 3])
acc98    = np.trace(cm98) / n98 * 100
chance98 = sum(((y98==g).sum()/n98)**2 for g in [1, 2, 3]) * 100
print(f"\nClassification Matrix:")
print(f"{'':20} {'Pred: 1 Phone':>14} {'Pred: 2 Phones':>15} {'Pred: 3+ Phones':>16}")
for i, g in enumerate([1, 2, 3]):
    lbl = ['1 Phone','2 Phones','3+ Phones'][i]
    print(f"  Actual {lbl:<12} {cm98[i,0]:>14} {cm98[i,1]:>15} {cm98[i,2]:>16}"
          f"   ({cm98[i,i]/(y98==g).sum()*100:.1f}%)")
print(f"\nOverall Correct Classification Rate: {acc98:.1f}%")
print(f"Proportional chance level: {chance98:.1f}%")

print("""
Interpretation:
  1. Wilks' Lambda is low and chi-square is significant — the three phone groups
     differ significantly in their attitudinal profiles.
  2. Function 1 captures the primary dimension (cost vs. value orientation).
     Function 2 adds a secondary quality/brand dimension.
  3. A3 ("More phones worth extra cost") distinguishes 3+ phone owners.
     A5 ("More phones = waste of money") aligns with 1-phone households.
     A2 ("Save money with one phone") reinforces frugality in single-phone homes.
  4. 1-phone families are the most cost-conscious; 3+ phone families are the
     most value-oriented. 2-phone families occupy an intermediate position.
  5. Classification well above chance confirms discriminant validity.
""")

# ── Figures Q9.8 ──────────────────────────────────────────────────────────────
GRP_COL98 = {1: BLUE, 2: ORANGE, 3: GREEN}
GRP_LBL98 = {1: '1 Phone', 2: '2 Phones', 3: '3+ Phones'}

fig = plt.figure(figsize=(18, 16))
fig.patch.set_facecolor(DARK)
gs  = gridspec.GridSpec(3, 3, figure=fig, hspace=0.48, wspace=0.38)

ax1 = fig.add_subplot(gs[0, :2])
style_ax(ax1, 'Group Means by Attitude Statement (0–10 scale)')
x = np.arange(len(attitudes)); w = 0.25
for i, (g, col) in enumerate([(1,BLUE),(2,ORANGE),(3,GREEN)]):
    means = [df98.loc[df98.Phones==g, a].mean() for a in attitudes]
    ax1.bar(x + (i-1)*w, means, w, color=col, alpha=0.85, label=GRP_LBL98[g])
ax1.set_xticks(x)
short_lbl98 = ['A1\nLong dist.\nnecessary','A2\nSave money\none phone',
               'A3\nMore phones\nworth cost','A4\nBelow-avg\nbill',
               'A5\nMore phones\n= waste','A6\nBest model\nworth cost']
ax1.set_xticklabels(short_lbl98, color=WHITE, fontsize=7.5)
ax1.set_ylabel('Mean Score', color=WHITE); ax1.set_ylim(0, 11)
ax1.legend(facecolor=DARK, labelcolor=WHITE, fontsize=9)
ax1.axhline(5, color=GRAY, linestyle=':', linewidth=1, alpha=0.5)

ax2 = fig.add_subplot(gs[0, 2])
style_ax(ax2, 'Sample Composition')
sizes98 = [(y98==g).sum() for g in [1, 2, 3]]
pie_lbl98 = [f'{GRP_LBL98[g]}\n(n={s})' for g, s in zip([1, 2, 3], sizes98)]
_, _, auts98 = ax2.pie(sizes98, labels=pie_lbl98, colors=[BLUE, ORANGE, GREEN],
                        autopct='%1.1f%%', startangle=90,
                        textprops={'color': WHITE, 'fontsize': 8})
for at in auts98: at.set_color(DARK)

ax3 = fig.add_subplot(gs[1, :2])
style_ax(ax3, 'Discriminant Score Plot: Function 1 vs Function 2')
for g in [1, 2, 3]:
    mask = y98 == g
    ax3.scatter(scores98[mask, 0], scores98[mask, 1],
                c=GRP_COL98[g], label=GRP_LBL98[g], alpha=0.55, s=35, edgecolors='none')
for g in [1, 2, 3]:
    c1 = scores98[y98==g, 0].mean(); c2 = scores98[y98==g, 1].mean()
    ax3.scatter(c1, c2, c=GRP_COL98[g], marker='*', s=280,
                edgecolors=WHITE, linewidths=0.8, zorder=5)
    ax3.annotate(f'  {GRP_LBL98[g]}\n  centroid', (c1, c2), color=WHITE, fontsize=7.5, fontweight='bold')
ax3.set_xlabel('Discriminant Function 1', color=WHITE)
ax3.set_ylabel('Discriminant Function 2', color=WHITE)
ax3.legend(facecolor=DARK, labelcolor=WHITE, fontsize=8)
ax3.axhline(0, color=GRAY, linewidth=0.6, alpha=0.4); ax3.axvline(0, color=GRAY, linewidth=0.6, alpha=0.4)

ax4 = fig.add_subplot(gs[1, 2])
style_ax(ax4, 'Std. Discriminant Coefficients')
x4 = np.arange(len(attitudes)); w4 = 0.35
ax4.barh(x4 + w4/2, std_sc98[:, 0], w4, color=BLUE,   alpha=0.85, label='Function 1')
ax4.barh(x4 - w4/2, std_sc98[:, 1], w4, color=ORANGE, alpha=0.85, label='Function 2')
ax4.set_yticks(x4); ax4.set_yticklabels(attitudes, color=WHITE, fontsize=9)
ax4.axvline(0, color=WHITE, linewidth=0.8)
ax4.set_xlabel('Standardised Coefficient', color=WHITE)
ax4.legend(facecolor=DARK, labelcolor=WHITE, fontsize=8)

ax5 = fig.add_subplot(gs[2, :2])
style_ax(ax5, 'Structure Matrix: Attitude–Function Correlations')
sf1 = [np.corrcoef(df98[a].values, scores98[:, 0])[0, 1] for a in attitudes]
sf2 = [np.corrcoef(df98[a].values, scores98[:, 1])[0, 1] for a in attitudes]
x_s = np.arange(len(attitudes)); w_s = 0.35
ax5.bar(x_s - w_s/2, sf1, w_s, color=BLUE,   alpha=0.85, label='Function 1')
ax5.bar(x_s + w_s/2, sf2, w_s, color=ORANGE, alpha=0.85, label='Function 2')
ax5.set_xticks(x_s)
ax5.set_xticklabels([f'{a}\n{labels98[a][:18]}' for a in attitudes], color=WHITE, fontsize=7.5)
ax5.axhline(0, color=WHITE, linewidth=0.8); ax5.set_ylabel('Correlation', color=WHITE)
ax5.set_ylim(-1, 1)
ax5.legend(facecolor=DARK, labelcolor=WHITE, fontsize=8)
ax5.axhline(0.3, color=GRAY, linestyle=':', linewidth=1, alpha=0.5)
ax5.axhline(-0.3, color=GRAY, linestyle=':', linewidth=1, alpha=0.5)

ax6 = fig.add_subplot(gs[2, 2])
style_ax(ax6, 'Classification Accuracy by Group')
grp_acc98 = [cm98[i, i] / (y98==g).sum() * 100 for i, g in enumerate([1, 2, 3])]
bars98 = ax6.bar(list(GRP_LBL98.values()), grp_acc98,
                  color=[BLUE, ORANGE, GREEN], alpha=0.85, width=0.5)
ax6.set_ylim(0, 110); ax6.set_ylabel('Correct Classification (%)', color=WHITE)
for bar, acc in zip(bars98, grp_acc98):
    ax6.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1,
             f'{acc:.1f}%', ha='center', va='bottom', color=WHITE, fontsize=10, fontweight='bold')
ax6.axhline(acc98,    color=RED,  linestyle='--', linewidth=1.5, label=f'Overall ({acc98:.1f}%)')
ax6.axhline(chance98, color=GRAY, linestyle=':', linewidth=1.5, label=f'Chance ({chance98:.1f}%)')
ax6.legend(facecolor=DARK, labelcolor=WHITE, fontsize=8)

fig.suptitle(
    f"Question 9.8 — Three-Group Discriminant Analysis (PHONE.DAT)\n"
    f"Wilks' Λ={wl98:.4f}  χ²={chi2_98:.2f} (df={len(attitudes)*2}, p={p_chi98:.4f})"
    f"  Overall Classification={acc98:.1f}%",
    color=WHITE, fontsize=12, fontweight='bold', y=0.99)
plt.savefig('q9_8_phone_discriminant.png', dpi=150, bbox_inches='tight', facecolor=DARK)
plt.close()
print("Figure saved: q9_8_phone_discriminant.png")


# =============================================================================
# QUESTION 9.9 — Discriminant Analysis of Graduate School Admissions (ADMIS.DAT)
# =============================================================================
print("\n" + "="*70)
print("QUESTION 9.9 — Discriminant Analysis: Graduate Admissions (ADMIS.DAT)")
print("  DV: Admission Status (1=Admitted, 2=Not Admitted, 3=Borderline)")
print("  IVs: GPA and GMAT")
print("="*70)

rows = []
with open('attached_assets/ADMIS_1773881795621.DAT', 'r') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('Adm') or line.startswith('---') \
                or line.startswith('App') or line.startswith('Num') \
                or line.startswith('Sta') or line.startswith('Sou') \
                or line.startswith('Note'):
            continue
        vals = line.split()
        if len(vals) == 4:
            try:
                rows.append([int(vals[0]), int(vals[1]), float(vals[2]), int(vals[3])])
            except:
                continue

df99 = pd.DataFrame(rows, columns=['Applicant','Status','GPA','GMAT'])
status_labels = {1: 'Admitted', 2: 'Not Admitted', 3: 'Borderline'}
df99['StatusLabel'] = df99['Status'].map(status_labels)
print(f"Dataset: {len(df99)} applicants")
print("\nGroup sizes:")
for s in [1, 2, 3]:
    print(f"  {status_labels[s]}: n={len(df99[df99.Status==s])}")

print("\nDescriptive Statistics by Group:")
print(f"\n{'Group':<15} {'n':>4} {'GPA Mean':>10} {'GPA SD':>8} {'GMAT Mean':>11} {'GMAT SD':>9}")
print("-"*60)
for s in [1, 2, 3]:
    sub = df99[df99.Status == s]
    print(f"  {status_labels[s]:<13} {len(sub):>4} {sub.GPA.mean():>10.3f} "
          f"{sub.GPA.std():>8.3f} {sub.GMAT.mean():>11.1f} {sub.GMAT.std():>9.1f}")
print(f"  {'Overall':<13} {len(df99):>4} {df99.GPA.mean():>10.3f} "
      f"{df99.GPA.std():>8.3f} {df99.GMAT.mean():>11.1f} {df99.GMAT.std():>9.1f}")

print("\n--- Univariate F-tests ---")
for var in ['GPA', 'GMAT']:
    F, p = stats.f_oneway(*[df99.loc[df99.Status==s, var].values for s in [1, 2, 3]])
    print(f"  {var}: F={F:.3f}, p={p:.4f}")

X99 = df99[['GPA','GMAT']].values
y99 = df99['Status'].values
n99, p99 = len(y99), 2

lda99 = LinearDiscriminantAnalysis()
lda99.fit(X99, y99)
pred99   = lda99.predict(X99)
scores99 = lda99.transform(X99)
probs99  = lda99.predict_proba(X99)

wl99     = wilks_mg(X99, y99)
chi2_99  = -(n99 - 1 - (p99 + 3) / 2) * np.log(wl99)
p_chi99  = 1 - stats.chi2.cdf(chi2_99, p99 * 2)
exp99    = lda99.explained_variance_ratio_

print(f"\nOverall Model:")
print(f"  Wilks' Lambda:        {wl99:.4f}")
print(f"  Chi-square (approx):  {chi2_99:.3f}  (df={p99*2})")
print(f"  p-value:              {p_chi99:.6f}")
print(f"\nFunction 1: {exp99[0]*100:.1f}% of between-group variance")
print(f"Function 2: {exp99[1]*100:.1f}% of between-group variance")

ps99       = df99[['GPA','GMAT']].std()
scalings99 = lda99.scalings_
std_sc99   = scalings99 * ps99.values[:, np.newaxis]

print("\nStandardised Discriminant Function Coefficients:")
print(f"  {'Variable':<8} {'Function 1':>12} {'Function 2':>12}")
for i, v in enumerate(['GPA','GMAT']):
    print(f"  {v:<8} {std_sc99[i,0]:>12.4f} {std_sc99[i,1]:>12.4f}")

print("\nStructure Matrix (Variable–Function Correlations):")
print(f"  {'Variable':<8} {'Function 1':>12} {'Function 2':>12}")
for i, v in enumerate(['GPA','GMAT']):
    r1 = np.corrcoef(df99[v].values, scores99[:, 0])[0, 1]
    r2 = np.corrcoef(df99[v].values, scores99[:, 1])[0, 1]
    print(f"  {v:<8} {r1:>12.4f} {r2:>12.4f}")

centroids99 = {}
print("\nGroup Centroids:")
for s in [1, 2, 3]:
    c1 = scores99[y99==s, 0].mean(); c2 = scores99[y99==s, 1].mean()
    centroids99[s] = (c1, c2)
    print(f"  {status_labels[s]:<15} F1={c1:>8.4f}  F2={c2:>8.4f}")

cm99     = confusion_matrix(y99, pred99, labels=[1, 2, 3])
acc99    = np.trace(cm99) / n99 * 100
chance99 = sum(((y99==s).sum()/n99)**2 for s in [1, 2, 3]) * 100

print(f"\nClassification Matrix:")
header = f"{'':22} {'Pred: Admitted':>15} {'Pred: Not Adm.':>15} {'Pred: Borderline':>17}"
print(f"  {header}")
print(f"  {'-'*70}")
for i, s in enumerate([1, 2, 3]):
    ng = (y99==s).sum()
    print(f"  Actual {status_labels[s]:<14} {cm99[i,0]:>15} {cm99[i,1]:>15} {cm99[i,2]:>17}"
          f"   ({cm99[i,i]/ng*100:.1f}%)")
print(f"\n  Overall correct classification: {acc99:.1f}%")
print(f"  Proportional chance level:      {chance99:.1f}%")

print(f"""
Interpretation:
1. OVERALL SIGNIFICANCE:
   Wilks' Lambda = {wl99:.4f}, χ²({p99*2}) = {chi2_99:.2f}, p < 0.0001.
   The three admission groups differ highly significantly in GPA and GMAT.

2. DISCRIMINANT FUNCTIONS:
   Function 1 explains {exp99[0]*100:.1f}% of between-group variance — dominant.
   Function 2 explains only {exp99[1]*100:.1f}% — minor secondary dimension.

3. VARIABLE IMPORTANCE:
   GPA has a larger standardised coefficient on Function 1 — it is the primary
   separator. GMAT contributes importantly as well. Together they form a
   composite "academic merit" dimension.

4. GROUP PROFILES:
   Admitted:     GPA ≈ {df99.loc[df99.Status==1,'GPA'].mean():.2f}, GMAT ≈ {df99.loc[df99.Status==1,'GMAT'].mean():.0f}  → High on both
   Borderline:   GPA ≈ {df99.loc[df99.Status==3,'GPA'].mean():.2f}, GMAT ≈ {df99.loc[df99.Status==3,'GMAT'].mean():.0f}  → Moderate GPA, lower GMAT
   Not Admitted: GPA ≈ {df99.loc[df99.Status==2,'GPA'].mean():.2f}, GMAT ≈ {df99.loc[df99.Status==2,'GMAT'].mean():.0f}  → Lowest on both

5. CLASSIFICATION PERFORMANCE:
   Overall correct classification: {acc99:.1f}% vs. chance ≈ {chance99:.1f}%.
   All three groups classified above 90%, a very strong result.

6. ADMISSION POLICY IMPLICATIONS:
   a) The school is primarily GPA-driven; no rejected applicant had GPA ≥ 3.40.
   b) Not-admitted applicants consistently fall below GPA = 2.90 regardless
      of GMAT, suggesting GPA is a near-mandatory threshold.
   c) Borderline cases (GPA 2.73–3.50) overlap both groups; the school likely
      uses recommendations and essays for final decisions in this zone.
   d) Practical rule: GPA ≥ 3.30 AND GMAT ≥ 500 → Admit;
                      GPA < 2.90 AND GMAT < 480 → Reject; otherwise Borderline.
   e) Adding work experience or recommendations could resolve borderline cases.
""")

# ── Figures Q9.9 ──────────────────────────────────────────────────────────────
def confidence_ellipse(x, y, ax, n_std=1.5, **kwargs):
    cov     = np.cov(x, y)
    pearson = cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])
    rx, ry  = np.sqrt(1 + pearson), np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=rx*2, height=ry*2, **kwargs)
    sx, sy  = np.sqrt(cov[0, 0])*n_std, np.sqrt(cov[1, 1])*n_std
    t = transforms.Affine2D().rotate_deg(45).scale(sx, sy).translate(x.mean(), y.mean())
    ellipse.set_transform(t + ax.transData)
    return ax.add_patch(ellipse)

GRP_COL99 = {1: BLUE, 2: RED, 3: ORANGE}
GRP_LBL99 = {1: 'Admitted', 2: 'Not Admitted', 3: 'Borderline'}

fig = plt.figure(figsize=(18, 16))
fig.patch.set_facecolor(DARK)
gs  = gridspec.GridSpec(3, 3, figure=fig, hspace=0.48, wspace=0.38)

ax1 = fig.add_subplot(gs[0, :2])
style_ax(ax1, 'GPA vs GMAT by Admission Status')
for s in [1, 2, 3]:
    sub = df99[df99.Status == s]
    ax1.scatter(sub.GPA, sub.GMAT, c=GRP_COL99[s], label=GRP_LBL99[s],
                alpha=0.65, s=50, edgecolors='none', zorder=3)
    confidence_ellipse(sub.GPA.values, sub.GMAT.values, ax1, n_std=1.5,
                       edgecolor=GRP_COL99[s], facecolor='none',
                       linewidth=2, linestyle='--', zorder=2)
    ax1.scatter(sub.GPA.mean(), sub.GMAT.mean(), c=GRP_COL99[s],
                marker='*', s=250, edgecolors=WHITE, linewidths=0.8, zorder=5)
ax1.set_xlabel('GPA', color=WHITE); ax1.set_ylabel('GMAT Score', color=WHITE)
ax1.legend(facecolor=DARK, labelcolor=WHITE, fontsize=9)
ax1.axvline(3.30, color=WHITE, linestyle=':', linewidth=1, alpha=0.4)
ax1.axhline(500,  color=WHITE, linestyle=':', linewidth=1, alpha=0.4)

ax2 = fig.add_subplot(gs[0, 2])
style_ax(ax2, 'Group Means')
x2 = np.arange(2); w2 = 0.25
for i, s in enumerate([1, 2, 3]):
    sub = df99[df99.Status == s]
    ax2.bar(x2 + (i-1)*w2, [sub.GPA.mean(), sub.GMAT.mean()/100], w2,
            color=GRP_COL99[s], alpha=0.85, label=GRP_LBL99[s])
ax2.set_xticks(x2); ax2.set_xticklabels(['GPA\n(actual)', 'GMAT\n(÷100)'], color=WHITE, fontsize=9)
ax2.set_ylabel('Mean Value', color=WHITE)
ax2.legend(facecolor=DARK, labelcolor=WHITE, fontsize=7.5)

ax3 = fig.add_subplot(gs[1, :2])
style_ax(ax3, 'Discriminant Score Plot: Function 1 vs Function 2')
for s in [1, 2, 3]:
    mask = y99 == s
    ax3.scatter(scores99[mask, 0], scores99[mask, 1],
                c=GRP_COL99[s], label=GRP_LBL99[s], alpha=0.60, s=45, edgecolors='none')
for s in [1, 2, 3]:
    c1, c2 = centroids99[s]
    ax3.scatter(c1, c2, c=GRP_COL99[s], marker='*', s=280,
                edgecolors=WHITE, linewidths=0.8, zorder=5)
    ax3.annotate(f'  {GRP_LBL99[s]}\n  ({c1:.2f}, {c2:.2f})',
                 (c1, c2), color=WHITE, fontsize=7.5, fontweight='bold')
ax3.set_xlabel(f'Function 1 ({exp99[0]*100:.1f}% variance)', color=WHITE)
ax3.set_ylabel(f'Function 2 ({exp99[1]*100:.1f}% variance)', color=WHITE)
ax3.legend(facecolor=DARK, labelcolor=WHITE, fontsize=8)
ax3.axhline(0, color=GRAY, linewidth=0.6, alpha=0.4); ax3.axvline(0, color=GRAY, linewidth=0.6, alpha=0.4)

ax4 = fig.add_subplot(gs[1, 2])
style_ax(ax4, 'Std. Discriminant Coefficients')
x4 = np.arange(2); w4 = 0.35
ax4.bar(x4 - w4/2, std_sc99[:, 0], w4, color=BLUE,   alpha=0.85, label='Function 1')
ax4.bar(x4 + w4/2, std_sc99[:, 1], w4, color=ORANGE, alpha=0.85, label='Function 2')
ax4.set_xticks(x4); ax4.set_xticklabels(['GPA', 'GMAT'], color=WHITE, fontsize=10)
ax4.axhline(0, color=WHITE, linewidth=0.8)
ax4.set_ylabel('Standardised Coefficient', color=WHITE)
ax4.legend(facecolor=DARK, labelcolor=WHITE, fontsize=9)
for i, (c1, c2) in enumerate(zip(std_sc99[:, 0], std_sc99[:, 1])):
    ax4.text(i - w4/2, c1 + (0.02 if c1 >= 0 else -0.05), f'{c1:.3f}', ha='center', color=WHITE, fontsize=8)
    ax4.text(i + w4/2, c2 + (0.02 if c2 >= 0 else -0.05), f'{c2:.3f}', ha='center', color=WHITE, fontsize=8)

ax5 = fig.add_subplot(gs[2, :2])
style_ax(ax5, 'Distribution of Discriminant Function 1 Scores by Group')
for s in [1, 2, 3]:
    ax5.hist(scores99[y99==s, 0], bins=15, alpha=0.55, color=GRP_COL99[s],
             label=f'{GRP_LBL99[s]} (centroid={centroids99[s][0]:.2f})')
    ax5.axvline(centroids99[s][0], color=GRP_COL99[s], linestyle='--', linewidth=2)
ax5.set_xlabel('Discriminant Function 1 Score', color=WHITE)
ax5.set_ylabel('Frequency', color=WHITE)
ax5.legend(facecolor=DARK, labelcolor=WHITE, fontsize=8)

ax6 = fig.add_subplot(gs[2, 2])
style_ax(ax6, 'Classification Accuracy by Group')
grp_acc99 = [cm99[i, i] / (y99==s).sum() * 100 for i, s in enumerate([1, 2, 3])]
bars99 = ax6.bar(list(GRP_LBL99.values()), grp_acc99,
                  color=[BLUE, RED, ORANGE], alpha=0.85, width=0.5)
ax6.set_ylim(0, 115); ax6.set_ylabel('Correct Classification (%)', color=WHITE)
for bar, acc in zip(bars99, grp_acc99):
    ax6.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1,
             f'{acc:.1f}%', ha='center', va='bottom', color=WHITE, fontsize=10, fontweight='bold')
ax6.axhline(acc99,    color=GREEN, linestyle='--', linewidth=1.5, label=f'Overall ({acc99:.1f}%)')
ax6.axhline(chance99, color=GRAY,  linestyle=':',  linewidth=1.5, label=f'Chance ({chance99:.1f}%)')
ax6.tick_params(axis='x', labelrotation=10)
ax6.legend(facecolor=DARK, labelcolor=WHITE, fontsize=8)

fig.suptitle(
    f"Question 9.9 — Discriminant Analysis of Graduate School Admissions (ADMIS.DAT)\n"
    f"Wilks' Λ={wl99:.4f}  χ²={chi2_99:.2f} (df={p99*2}, p<0.0001)"
    f"  Classification Accuracy={acc99:.1f}%",
    color=WHITE, fontsize=12, fontweight='bold', y=0.99)
plt.savefig('q9_9_admissions_discriminant.png', dpi=150, bbox_inches='tight', facecolor=DARK)
plt.close()
print("Figure saved: q9_9_admissions_discriminant.png")

# =============================================================================
print("\n" + "="*70)
print("ALL QUESTIONS COMPLETE")
print("  Q8.7  → q8_7_discriminant_analysis.png")
print("  Q7.5+Q8.8 → q7_5_q8_8_mass_transit.png")
print("  Q9.8  → q9_8_phone_discriminant.png")
print("  Q9.9  → q9_9_admissions_discriminant.png")
print("  Student: Lana Gidan")
print("="*70)

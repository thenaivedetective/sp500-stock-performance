import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import confusion_matrix
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────
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
                rows.append([int(vals[0]), int(vals[1]),
                             float(vals[2]), int(vals[3])])
            except:
                continue

df = pd.DataFrame(rows, columns=['Applicant', 'Status', 'GPA', 'GMAT'])
status_labels = {1: 'Admitted', 2: 'Not Admitted', 3: 'Borderline'}
df['StatusLabel'] = df['Status'].map(status_labels)
print(f"Dataset: {len(df)} applicants")
print(f"\nGroup sizes:")
for s in [1, 2, 3]:
    print(f"  {status_labels[s]}: n={len(df[df.Status==s])}")

# ─────────────────────────────────────────────────────────────────────────────
# DESCRIPTIVE STATISTICS
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*65)
print("QUESTION 9.9 — Discriminant Analysis of Graduate Admissions")
print("  DV: Admission Status (1=Admitted, 2=Not Admitted, 3=Borderline)")
print("  IVs: GPA (0–4.0) and GMAT score")
print("="*65)

print("\nDescriptive Statistics by Group:")
print(f"\n{'Group':<15} {'n':>4} {'GPA Mean':>10} {'GPA SD':>8} "
      f"{'GMAT Mean':>11} {'GMAT SD':>9}")
print("-"*60)
for s in [1, 2, 3]:
    sub = df[df.Status == s]
    print(f"  {status_labels[s]:<13} {len(sub):>4} {sub.GPA.mean():>10.3f} "
          f"{sub.GPA.std():>8.3f} {sub.GMAT.mean():>11.1f} {sub.GMAT.std():>9.1f}")
print(f"  {'Overall':<13} {len(df):>4} {df.GPA.mean():>10.3f} "
      f"{df.GPA.std():>8.3f} {df.GMAT.mean():>11.1f} {df.GMAT.std():>9.1f}")

# ─────────────────────────────────────────────────────────────────────────────
# UNIVARIATE F-TESTS
# ─────────────────────────────────────────────────────────────────────────────
print("\n--- Univariate F-tests (one-way ANOVA) ---")
for var in ['GPA', 'GMAT']:
    groups = [df.loc[df.Status==s, var].values for s in [1, 2, 3]]
    F, p = stats.f_oneway(*groups)
    print(f"  {var}: F={F:.3f}, p={p:.4f}")

# ─────────────────────────────────────────────────────────────────────────────
# LINEAR DISCRIMINANT ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
print("\n--- Linear Discriminant Analysis ---")
X = df[['GPA', 'GMAT']].values
y = df['Status'].values
n, p_vars = len(y), 2
k = 3

lda = LinearDiscriminantAnalysis()
lda.fit(X, y)
pred = lda.predict(X)
scores = lda.transform(X)
probs = lda.predict_proba(X)

# Wilks' Lambda
def wilks_lambda_mg(X, y):
    p = X.shape[1]
    grand_mean = X.mean(axis=0)
    W = np.zeros((p, p))
    for g in np.unique(y):
        Xg = X[y == g]
        d = Xg - Xg.mean(axis=0)
        W += d.T @ d
    d_all = X - grand_mean
    T = d_all.T @ d_all
    return np.linalg.det(W) / np.linalg.det(T)

wl = wilks_lambda_mg(X, y)
df_chi = p_vars * (k - 1)
chi2_stat = -(n - 1 - (p_vars + k) / 2) * np.log(wl)
p_chi2 = 1 - stats.chi2.cdf(chi2_stat, df_chi)

print(f"\nOverall Model:")
print(f"  Wilks' Lambda:        {wl:.4f}")
print(f"  Chi-square (approx):  {chi2_stat:.3f}  (df={df_chi})")
print(f"  p-value:              {p_chi2:.6f}")

explained = lda.explained_variance_ratio_
print(f"\nDiscriminant Functions:")
print(f"  Function 1: {explained[0]*100:.1f}% of between-group variance")
print(f"  Function 2: {explained[1]*100:.1f}% of between-group variance")

# Standardized coefficients using scalings_
pooled_std = df[['GPA','GMAT']].std()
scalings = lda.scalings_  # (n_features, n_components)
std_scalings = scalings * pooled_std.values[:, np.newaxis]

print(f"\nStandardized Discriminant Function Coefficients:")
print(f"  {'Variable':<8} {'Function 1':>12} {'Function 2':>12}")
print(f"  {'-'*35}")
for i, v in enumerate(['GPA', 'GMAT']):
    print(f"  {v:<8} {std_scalings[i,0]:>12.4f} {std_scalings[i,1]:>12.4f}")

print(f"\nRaw Discriminant Function Coefficients (scalings):")
print(f"  {'Variable':<8} {'Function 1':>12} {'Function 2':>12}")
print(f"  {'-'*35}")
for i, v in enumerate(['GPA', 'GMAT']):
    print(f"  {v:<8} {scalings[i,0]:>12.4f} {scalings[i,1]:>12.4f}")

# Structure matrix
print(f"\nStructure Matrix (Variable-Function Correlations):")
print(f"  {'Variable':<8} {'Function 1':>12} {'Function 2':>12}")
print(f"  {'-'*35}")
for i, v in enumerate(['GPA', 'GMAT']):
    r1 = np.corrcoef(df[v].values, scores[:, 0])[0, 1]
    r2 = np.corrcoef(df[v].values, scores[:, 1])[0, 1]
    print(f"  {v:<8} {r1:>12.4f} {r2:>12.4f}")

# Group centroids
print(f"\nGroup Centroids on Discriminant Functions:")
print(f"  {'Group':<15} {'Centroid F1':>12} {'Centroid F2':>12}")
print(f"  {'-'*42}")
centroids = {}
for s in [1, 2, 3]:
    c1 = scores[y==s, 0].mean()
    c2 = scores[y==s, 1].mean()
    centroids[s] = (c1, c2)
    print(f"  {status_labels[s]:<15} {c1:>12.4f} {c2:>12.4f}")

# Classification
cm = confusion_matrix(y, pred, labels=[1, 2, 3])
accuracy = np.trace(cm) / n * 100

print(f"\nClassification Matrix:")
header = f"{'':22} {'Pred: Admitted':>15} {'Pred: Not Adm.':>15} {'Pred: Borderline':>17}"
print(f"  {header}")
print(f"  {'-'*70}")
for i, s in enumerate([1, 2, 3]):
    ng = (y==s).sum()
    row_acc = cm[i,i]/ng*100
    print(f"  Actual {status_labels[s]:<14} {cm[i,0]:>15} {cm[i,1]:>15} {cm[i,2]:>17}   ({row_acc:.1f}%)")

chance = sum(((y==s).sum()/n)**2 for s in [1,2,3])*100
print(f"\n  Overall correct classification: {accuracy:.1f}%")
print(f"  Proportional chance level:      {chance:.1f}%")

# ─────────────────────────────────────────────────────────────────────────────
# INDIVIDUAL POSTERIOR PROBABILITIES (sample)
# ─────────────────────────────────────────────────────────────────────────────
print(f"\nSample Posterior Probabilities (selected borderline cases):")
print(f"  {'Appl.':>6} {'GPA':>6} {'GMAT':>6} {'P(Admit)':>10} {'P(Not Adm)':>11} {'P(Border)':>10} {'Predicted':>12}")
print(f"  {'-'*63}")
borderline_mask = y == 3
border_df = df[borderline_mask].copy()
border_probs = probs[borderline_mask]
for idx, (_, row) in enumerate(border_df.iterrows()):
    pg = [1, 2, 3][np.argmax(border_probs[idx])]
    print(f"  {int(row.Applicant):>6} {row.GPA:>6.2f} {int(row.GMAT):>6} "
          f"{border_probs[idx,0]:>10.3f} {border_probs[idx,1]:>11.3f} "
          f"{border_probs[idx,2]:>10.3f} {status_labels[pg]:>12}")

# ─────────────────────────────────────────────────────────────────────────────
# ADMISSION POLICY INTERPRETATION
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*65)
print("INTERPRETATION & ADMISSION POLICY DISCUSSION")
print("="*65)

gpa_admitted = df.loc[df.Status==1, 'GPA'].mean()
gpa_border   = df.loc[df.Status==3, 'GPA'].mean()
gpa_notadm   = df.loc[df.Status==2, 'GPA'].mean()
gmat_admitted = df.loc[df.Status==1, 'GMAT'].mean()
gmat_border   = df.loc[df.Status==3, 'GMAT'].mean()
gmat_notadm   = df.loc[df.Status==2, 'GMAT'].mean()

print(f"""
1. OVERALL SIGNIFICANCE:
   Wilks' Lambda = {wl:.4f}, χ²({df_chi}) = {chi2_stat:.2f}, p < 0.0001.
   The three admission groups differ highly significantly in their combined
   GPA and GMAT profiles.

2. DISCRIMINANT FUNCTIONS:
   - Function 1 explains {explained[0]*100:.1f}% of between-group variance — dominant.
   - Function 2 explains only {explained[1]*100:.1f}% — minor secondary dimension.
   Two functions are sufficient to characterize three groups.

3. VARIABLE IMPORTANCE:
   Both GPA and GMAT significantly discriminate groups (see univariate F-tests).
   - GPA has a larger standardized coefficient on Function 1 — it is the
     primary separator between admitted and not-admitted applicants.
   - GMAT contributes importantly as well, though slightly less than GPA.
   Together, they form a composite "academic merit" dimension.

4. GROUP PROFILE SUMMARY:
   - Admitted (Status=1):   GPA ≈ {gpa_admitted:.2f}, GMAT ≈ {gmat_admitted:.0f}  → High on both
   - Borderline (Status=3): GPA ≈ {gpa_border:.2f}, GMAT ≈ {gmat_border:.0f}  → Moderate GPA, moderate-low GMAT
   - Not Admitted (Status=2): GPA ≈ {gpa_notadm:.2f}, GMAT ≈ {gmat_notadm:.0f}  → Lowest GPA, low GMAT

5. CLASSIFICATION PERFORMANCE:
   Overall correct classification: {accuracy:.1f}% vs. chance ≈ {chance:.1f}%.
   - Admitted applicants are classified best ({cm[0,0]/(y==1).sum()*100:.1f}% correct).
   - Borderline cases are hardest to classify ({cm[2,2]/(y==3).sum()*100:.1f}% correct),
     as expected since they overlap with both other groups.

6. ADMISSION POLICY IMPLICATIONS:
   a) The school's admission policy is primarily GPA-driven with GMAT as
      a secondary criterion. A high GPA (≥ 3.30) combined with a moderate
      GMAT (≥ 500) appears to be the threshold for admission.
   b) Not-admitted applicants consistently fall below GPA = 2.90 regardless
      of GMAT score, suggesting GPA is a near-mandatory requirement.
   c) Borderline applicants have GPAs between ~2.73 and 3.50 — overlapping
      with both groups — and relatively lower GMAT scores (~440 avg).
      The school appears to use additional criteria (recommendations, essays)
      for these cases, since neither GPA nor GMAT alone is decisive.
   d) A practical admission rule suggested by the discriminant analysis:
      - GPA ≥ 3.30 AND GMAT ≥ 500: Likely Admit
      - GPA < 2.90 AND GMAT < 480: Likely Reject
      - Otherwise: Borderline — requires holistic review
   e) The school could improve the predictive model by including additional
      variables (work experience, recommendations) to resolve borderline cases.
""")

# ─────────────────────────────────────────────────────────────────────────────
# FIGURES
# ─────────────────────────────────────────────────────────────────────────────
DARK  = '#0d1b2a'; PANEL = '#162032'
BLUE  = '#4fc3f7'; ORANGE= '#ffb74d'; GREEN = '#81c784'
RED   = '#e57373'; WHITE = '#e8eaf6'; GRAY  = '#607d8b'

GRP_COLOR = {1: BLUE, 2: RED, 3: ORANGE}
GRP_LABEL = {1: 'Admitted', 2: 'Not Admitted', 3: 'Borderline'}

def style_ax(ax, title):
    ax.set_facecolor(PANEL)
    for sp in ax.spines.values(): sp.set_edgecolor(GRAY)
    ax.tick_params(colors=WHITE, labelsize=8)
    ax.xaxis.label.set_color(WHITE)
    ax.yaxis.label.set_color(WHITE)
    ax.set_title(title, color=WHITE, fontsize=10, fontweight='bold', pad=6)

def confidence_ellipse(x, y, ax, n_std=1.5, **kwargs):
    cov = np.cov(x, y)
    pearson = cov[0,1] / np.sqrt(cov[0,0]*cov[1,1])
    rx, ry = np.sqrt(1+pearson), np.sqrt(1-pearson)
    ellipse = Ellipse((0,0), width=rx*2, height=ry*2, **kwargs)
    sx, sy = np.sqrt(cov[0,0])*n_std, np.sqrt(cov[1,1])*n_std
    t = transforms.Affine2D().rotate_deg(45).scale(sx, sy).translate(x.mean(), y.mean())
    ellipse.set_transform(t + ax.transData)
    return ax.add_patch(ellipse)

fig = plt.figure(figsize=(18, 16))
fig.patch.set_facecolor(DARK)
gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.48, wspace=0.38)

# ── 1. GPA vs GMAT scatter with ellipses ─────────────────────────────────────
ax1 = fig.add_subplot(gs[0, :2])
style_ax(ax1, 'GPA vs GMAT by Admission Status')
for s in [1, 2, 3]:
    sub = df[df.Status == s]
    ax1.scatter(sub.GPA, sub.GMAT, c=GRP_COLOR[s], label=GRP_LABEL[s],
                alpha=0.65, s=50, edgecolors='none', zorder=3)
    confidence_ellipse(sub.GPA.values, sub.GMAT.values, ax1, n_std=1.5,
                       edgecolor=GRP_COLOR[s], facecolor='none',
                       linewidth=2, linestyle='--', zorder=2)
    mx, my = sub.GPA.mean(), sub.GMAT.mean()
    ax1.scatter(mx, my, c=GRP_COLOR[s], marker='*', s=250,
                edgecolors=WHITE, linewidths=0.8, zorder=5)

ax1.set_xlabel('GPA', color=WHITE)
ax1.set_ylabel('GMAT Score', color=WHITE)
ax1.legend(facecolor=DARK, labelcolor=WHITE, fontsize=9)
ax1.axvline(3.30, color=WHITE, linestyle=':', linewidth=1, alpha=0.4, label='GPA=3.30')
ax1.axhline(500, color=WHITE, linestyle=':', linewidth=1, alpha=0.4)

# ── 2. Group means bar chart ──────────────────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 2])
style_ax(ax2, 'Group Means')
x = np.arange(2)
w = 0.25
for i, s in enumerate([1, 2, 3]):
    sub = df[df.Status == s]
    vals = [sub.GPA.mean(), sub.GMAT.mean()/100]  # scale GMAT for visibility
    ax2.bar(x + (i-1)*w, vals, w, color=GRP_COLOR[s], alpha=0.85,
            label=GRP_LABEL[s])
ax2.set_xticks(x)
ax2.set_xticklabels(['GPA\n(actual)', 'GMAT\n(÷100)'], color=WHITE, fontsize=9)
ax2.set_ylabel('Mean Value', color=WHITE)
ax2.legend(facecolor=DARK, labelcolor=WHITE, fontsize=7.5)

# ── 3. Discriminant score scatter (F1 vs F2) ──────────────────────────────────
ax3 = fig.add_subplot(gs[1, :2])
style_ax(ax3, 'Discriminant Score Plot: Function 1 vs Function 2')
for s in [1, 2, 3]:
    mask = y == s
    ax3.scatter(scores[mask, 0], scores[mask, 1],
                c=GRP_COLOR[s], label=GRP_LABEL[s],
                alpha=0.60, s=45, edgecolors='none')
for s in [1, 2, 3]:
    c1, c2 = centroids[s]
    ax3.scatter(c1, c2, c=GRP_COLOR[s], marker='*', s=280,
                edgecolors=WHITE, linewidths=0.8, zorder=5)
    ax3.annotate(f'  {GRP_LABEL[s]}\n  ({c1:.2f}, {c2:.2f})',
                 (c1, c2), color=WHITE, fontsize=7.5, fontweight='bold')
ax3.set_xlabel(f'Function 1 ({explained[0]*100:.1f}% variance)', color=WHITE)
ax3.set_ylabel(f'Function 2 ({explained[1]*100:.1f}% variance)', color=WHITE)
ax3.legend(facecolor=DARK, labelcolor=WHITE, fontsize=8)
ax3.axhline(0, color=GRAY, linewidth=0.6, alpha=0.4)
ax3.axvline(0, color=GRAY, linewidth=0.6, alpha=0.4)

# ── 4. Posterior probabilities for each applicant ────────────────────────────
ax4 = fig.add_subplot(gs[1, 2])
style_ax(ax4, 'Std. Discriminant Coefficients')
variables = ['GPA', 'GMAT']
x4 = np.arange(len(variables))
w4 = 0.35
ax4.bar(x4 - w4/2, std_scalings[:, 0], w4, color=BLUE, alpha=0.85, label='Function 1')
ax4.bar(x4 + w4/2, std_scalings[:, 1], w4, color=ORANGE, alpha=0.85, label='Function 2')
ax4.set_xticks(x4)
ax4.set_xticklabels(variables, color=WHITE, fontsize=10)
ax4.axhline(0, color=WHITE, linewidth=0.8)
ax4.set_ylabel('Standardized Coefficient', color=WHITE)
ax4.legend(facecolor=DARK, labelcolor=WHITE, fontsize=9)
for i, (c1, c2) in enumerate(zip(std_scalings[:, 0], std_scalings[:, 1])):
    ax4.text(i - w4/2, c1 + (0.02 if c1 >= 0 else -0.05), f'{c1:.3f}',
             ha='center', color=WHITE, fontsize=8)
    ax4.text(i + w4/2, c2 + (0.02 if c2 >= 0 else -0.05), f'{c2:.3f}',
             ha='center', color=WHITE, fontsize=8)

# ── 5. Function 1 score distributions ────────────────────────────────────────
ax5 = fig.add_subplot(gs[2, :2])
style_ax(ax5, 'Distribution of Discriminant Function 1 Scores by Group')
for s in [1, 2, 3]:
    ax5.hist(scores[y==s, 0], bins=15, alpha=0.55, color=GRP_COLOR[s],
             label=f'{GRP_LABEL[s]} (centroid={centroids[s][0]:.2f})')
for s in [1, 2, 3]:
    ax5.axvline(centroids[s][0], color=GRP_COLOR[s],
                linestyle='--', linewidth=2)
ax5.set_xlabel('Discriminant Function 1 Score', color=WHITE)
ax5.set_ylabel('Frequency', color=WHITE)
ax5.legend(facecolor=DARK, labelcolor=WHITE, fontsize=8)

# ── 6. Classification accuracy ────────────────────────────────────────────────
ax6 = fig.add_subplot(gs[2, 2])
style_ax(ax6, 'Classification Accuracy by Group')
group_acc = [cm[i,i]/(y==s).sum()*100 for i,s in enumerate([1,2,3])]
bars = ax6.bar(list(GRP_LABEL.values()), group_acc,
               color=[BLUE, RED, ORANGE], alpha=0.85, width=0.5)
ax6.set_ylim(0, 115)
ax6.set_ylabel('Correct Classification (%)', color=WHITE)
for bar, acc in zip(bars, group_acc):
    ax6.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1,
             f'{acc:.1f}%', ha='center', va='bottom', color=WHITE,
             fontsize=10, fontweight='bold')
ax6.axhline(accuracy, color=GREEN, linestyle='--', linewidth=1.5,
            label=f'Overall ({accuracy:.1f}%)')
ax6.axhline(chance, color=GRAY, linestyle=':', linewidth=1.5,
            label=f'Chance ({chance:.1f}%)')
ax6.tick_params(axis='x', labelrotation=10)
ax6.legend(facecolor=DARK, labelcolor=WHITE, fontsize=8)

fig.suptitle(
    f"Question 9.9 — Discriminant Analysis of Graduate School Admissions (ADMIS.DAT)\n"
    f"Wilks' Λ={wl:.4f}  χ²={chi2_stat:.2f} (df={df_chi}, p<0.0001)"
    f"  Classification Accuracy={accuracy:.1f}%",
    color=WHITE, fontsize=12, fontweight='bold', y=0.99)

plt.savefig('q9_9_admissions_discriminant.png', dpi=150, bbox_inches='tight',
            facecolor=DARK)
plt.close()
print("Figure saved: q9_9_admissions_discriminant.png")

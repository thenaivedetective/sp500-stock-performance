import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import confusion_matrix
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────
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

cols = ['ID', 'Phones', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6']
df = pd.DataFrame(rows, columns=cols)
print(f"Dataset loaded: {len(df)} observations")
print(f"\nGroup sizes (number of phones):")
print(df['Phones'].value_counts().sort_index().to_string())

attitudes = ['A1','A2','A3','A4','A5','A6']
labels = {
    'A1': 'Long distance only necessary',
    'A2': 'Save money with one phone',
    'A3': 'More phones worth extra cost',
    'A4': 'Below-average phone bill',
    'A5': 'More phones = waste of money',
    'A6': 'Best model is worth cost'
}

# ─────────────────────────────────────────────────────────────────────────────
# DESCRIPTIVE STATISTICS BY GROUP
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("QUESTION 9.8 — Three-Group Discriminant Analysis (PHONE.DAT)")
print("  DV: Number of phones (1, 2, 3+)   IVs: A1–A6")
print("="*70)

print("\nGroup Means (0–10 scale):")
print(f"\n{'Attitude':<6} {'Statement':<32} {'1 Phone':>8} {'2 Phones':>9} {'3+ Phones':>10} {'Overall':>8}")
print("-"*75)
for a in attitudes:
    m1 = df.loc[df['Phones']==1, a].mean()
    m2 = df.loc[df['Phones']==2, a].mean()
    m3 = df.loc[df['Phones']==3, a].mean()
    mo = df[a].mean()
    print(f"  {a:<4} {labels[a]:<32} {m1:>8.2f} {m2:>9.2f} {m3:>10.2f} {mo:>8.2f}")

print("\nGroup Standard Deviations:")
print(f"\n{'Attitude':<6} {'Statement':<32} {'1 Phone':>8} {'2 Phones':>9} {'3+ Phones':>10}")
print("-"*65)
for a in attitudes:
    s1 = df.loc[df['Phones']==1, a].std()
    s2 = df.loc[df['Phones']==2, a].std()
    s3 = df.loc[df['Phones']==3, a].std()
    print(f"  {a:<4} {labels[a]:<32} {s1:>8.2f} {s2:>9.2f} {s3:>10.2f}")

# ─────────────────────────────────────────────────────────────────────────────
# ONE-WAY ANOVA for each attitude (univariate tests)
# ─────────────────────────────────────────────────────────────────────────────
print("\n--- Univariate F-tests (one-way ANOVA per attitude) ---")
print(f"\n{'Attitude':<6} {'Statement':<32} {'F-stat':>8} {'p-value':>10}")
print("-"*60)
for a in attitudes:
    groups = [df.loc[df['Phones']==g, a].values for g in [1, 2, 3]]
    F, p = stats.f_oneway(*groups)
    sig = '*' if p < 0.05 else ''
    print(f"  {a:<4} {labels[a]:<32} {F:>8.3f} {p:>10.4f} {sig}")
print("  (* p < 0.05)")

# ─────────────────────────────────────────────────────────────────────────────
# MULTIVARIATE DISCRIMINANT ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
print("\n--- Multivariate Linear Discriminant Analysis ---")
X = df[attitudes].values
y = df['Phones'].values
n = len(y)
p = len(attitudes)
k = 3  # number of groups

lda = LinearDiscriminantAnalysis()
lda.fit(X, y)
pred = lda.predict(X)
scores = lda.transform(X)  # discriminant scores (n x 2 functions)

# ── Wilks' Lambda for full model ─────────────────────────────────────────────
def wilks_lambda_multigroup(X, y, groups):
    p = X.shape[1]
    grand_mean = X.mean(axis=0)
    n_total = len(y)
    W = np.zeros((p, p))
    for g in groups:
        Xg = X[y == g]
        d = Xg - Xg.mean(axis=0)
        W += d.T @ d
    d_all = X - grand_mean
    T = d_all.T @ d_all
    dW = np.linalg.det(W)
    dT = np.linalg.det(T)
    return dW / dT if abs(dT) > 1e-20 else 1.0

groups = [1, 2, 3]
wl = wilks_lambda_multigroup(X, y, groups)

# Chi-square approximation for Wilks' lambda (Box 1949)
s = k - 1  # number of discriminant functions
df_chi = p * s
chi2_stat = -(n - 1 - (p + k) / 2) * np.log(wl)
p_chi2 = 1 - stats.chi2.cdf(chi2_stat, df_chi)

print(f"\nOverall Test of Discriminant Functions:")
print(f"  Wilks' Lambda:       {wl:.4f}")
print(f"  Chi-square (approx): {chi2_stat:.3f}  (df={df_chi})")
print(f"  p-value:             {p_chi2:.4f}")

# ── Eigenvalues and explained variance ──────────────────────────────────────
explained = lda.explained_variance_ratio_
print(f"\nDiscriminant Functions:")
print(f"  Function 1: eigenvalue contribution = {explained[0]*100:.1f}%")
print(f"  Function 2: eigenvalue contribution = {explained[1]*100:.1f}%")

# ── Standardized discriminant coefficients ────────────────────────────────
pooled_std = df[attitudes].std()
std_coefs = lda.coef_ * pooled_std.values  # shape (n_classes, n_features)

print("\nStandardized Discriminant Function Coefficients:")
print(f"\n{'Attitude':<6} {'Statement':<32} {'Function 1':>12} {'Function 2':>12}")
print("-"*65)
for i, a in enumerate(attitudes):
    # LDA coef_: shape is (n_classes, n_features), but we want the 2 discriminant functions
    # sklearn's LDA scalings_ gives the discriminant function coefficients
    pass

# Use scalings_ for the actual discriminant function coefficients
scalings = lda.scalings_  # shape (n_features, n_components)
std_scalings = scalings * pooled_std.values[:, np.newaxis]

print(f"\n{'Attitude':<6} {'Statement':<32} {'Function 1':>12} {'Function 2':>12}")
print("-"*65)
for i, a in enumerate(attitudes):
    c1 = std_scalings[i, 0]
    c2 = std_scalings[i, 1]
    print(f"  {a:<4} {labels[a]:<32} {c1:>12.4f} {c2:>12.4f}")

# ── Structure matrix (correlations of variables with discriminant functions) ──
print("\nStructure Matrix (Variable-Function Correlations):")
print(f"\n{'Attitude':<6} {'Statement':<32} {'Function 1':>12} {'Function 2':>12}")
print("-"*65)
# Compute correlations between original variables and discriminant scores
for i, a in enumerate(attitudes):
    r1 = np.corrcoef(df[a].values, scores[:, 0])[0, 1]
    r2 = np.corrcoef(df[a].values, scores[:, 1])[0, 1]
    print(f"  {a:<4} {labels[a]:<32} {r1:>12.4f} {r2:>12.4f}")

# ── Group centroids ───────────────────────────────────────────────────────────
print("\nGroup Centroids (discriminant function scores):")
print(f"\n{'Group':<15} {'Centroid F1':>12} {'Centroid F2':>12}")
print("-"*42)
for g, lbl in [(1,'1 Phone'),(2,'2 Phones'),(3,'3+ Phones')]:
    c1 = scores[y==g, 0].mean()
    c2 = scores[y==g, 1].mean()
    print(f"  {lbl:<15} {c1:>12.4f} {c2:>12.4f}")

# ── Classification results ────────────────────────────────────────────────────
cm = confusion_matrix(y, pred, labels=[1, 2, 3])
accuracy = np.trace(cm) / n * 100
print(f"\nClassification Matrix:")
print(f"{'':20} {'Pred: 1 Phone':>14} {'Pred: 2 Phones':>15} {'Pred: 3+ Phones':>16}")
for i, g in enumerate([1, 2, 3]):
    lbl = ['1 Phone','2 Phones','3+ Phones'][i]
    n_g = (y == g).sum()
    row_acc = cm[i, i] / n_g * 100
    print(f"  Actual {lbl:<12} {cm[i,0]:>14} {cm[i,1]:>15} {cm[i,2]:>16}   ({row_acc:.1f}% correct)")

print(f"\nOverall Correct Classification Rate: {accuracy:.1f}%")

# Chance level
n_g = [(y==g).sum() for g in [1,2,3]]
chance = sum((ng/n)**2 for ng in n_g) * 100
print(f"Press's Q statistic (vs chance = proportional): "
      f"chance level ≈ {chance:.1f}%")

# ─────────────────────────────────────────────────────────────────────────────
# INTERPRETATION
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("INTERPRETATION")
print("="*70)
print("""
1. OVERALL SIGNIFICANCE:
   The Wilks' Lambda and chi-square test assess whether the three groups
   (1 phone, 2 phones, 3+ phones) differ significantly in their attitudinal
   profiles. A significant result confirms that attitudes meaningfully
   differentiate multi-phone households from single-phone households.

2. DISCRIMINANT FUNCTIONS:
   Two discriminant functions are extracted (k-1 = 2 for three groups).
   - Function 1 captures the primary dimension of group separation.
   - Function 2 captures residual separation after removing Function 1.
   The percent of variance explained indicates which function is more important.

3. VARIABLE IMPORTANCE (Structure Matrix):
   - A3 ("More phones worth extra cost"): Higher scores for 3+ phone owners —
     they believe extra phones provide value.
   - A5 ("More phones = waste of money"): Higher scores for 1-phone owners —
     they view extra phones as unnecessary expense.
   - A2 ("Save money with one phone"): Aligns with 1-phone group.
   - A6 ("Best model worth cost"): Distinguishes quality-seekers who may own
     more expensive, newer telephone models.
   - A1 ("Long distance only necessary") and A4 ("Below-average bill"):
     Relate to cost-consciousness but show weaker group differentiation.

4. GROUP DIFFERENCES:
   - 1-Phone families: More cost-conscious, view multiple phones as wasteful,
     tend to score higher on frugality attitudes (A2, A5).
   - 3+ Phone families: More favorable attitude toward phone ownership, view
     multiple phones as worthwhile (A3), and tend toward quality-seeking (A6).
   - 2-Phone families: Show intermediate attitudes between the two extremes.

5. CLASSIFICATION PERFORMANCE:
   The correct classification rate indicates how well attitudes alone can
   assign families to their actual phone-ownership group. A rate substantially
   above the proportional chance level confirms discriminant validity.
""")

# ─────────────────────────────────────────────────────────────────────────────
# FIGURES
# ─────────────────────────────────────────────────────────────────────────────
DARK  = '#0d1b2a'; PANEL = '#162032'
BLUE  = '#4fc3f7'; ORANGE= '#ffb74d'; GREEN = '#81c784'
RED   = '#e57373'; WHITE = '#e8eaf6'; GRAY  = '#607d8b'
PURPLE= '#ce93d8'

GROUP_COLORS = {1: BLUE, 2: ORANGE, 3: GREEN}
GROUP_LABELS = {1: '1 Phone', 2: '2 Phones', 3: '3+ Phones'}

def style_ax(ax, title):
    ax.set_facecolor(PANEL)
    for sp in ax.spines.values(): sp.set_edgecolor(GRAY)
    ax.tick_params(colors=WHITE, labelsize=8)
    ax.xaxis.label.set_color(WHITE)
    ax.yaxis.label.set_color(WHITE)
    ax.set_title(title, color=WHITE, fontsize=10, fontweight='bold', pad=6)

fig = plt.figure(figsize=(18, 16))
fig.patch.set_facecolor(DARK)
gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.48, wspace=0.38)

# ── 1. Group Means per Attitude ──────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0, :2])
style_ax(ax1, 'Group Means by Attitude Statement (0–10 scale)')
x = np.arange(len(attitudes))
w = 0.25
for i, (g, col) in enumerate([(1,BLUE),(2,ORANGE),(3,GREEN)]):
    means = [df.loc[df['Phones']==g, a].mean() for a in attitudes]
    bars = ax1.bar(x + (i-1)*w, means, w, color=col,
                   alpha=0.85, label=GROUP_LABELS[g])
ax1.set_xticks(x)
short_lbl = ['A1\nLong dist.\nnecessary','A2\nSave money\none phone',
             'A3\nMore phones\nworth cost','A4\nBelow-avg\nbill',
             'A5\nMore phones\n= waste','A6\nBest model\nworth cost']
ax1.set_xticklabels(short_lbl, color=WHITE, fontsize=7.5)
ax1.set_ylabel('Mean Score', color=WHITE)
ax1.set_ylim(0, 11)
ax1.legend(facecolor=DARK, labelcolor=WHITE, fontsize=9)
ax1.axhline(5, color=GRAY, linestyle=':', linewidth=1, alpha=0.5)

# ── 2. Sample sizes pie ──────────────────────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 2])
style_ax(ax2, 'Sample Composition')
sizes = [(y==g).sum() for g in [1,2,3]]
pie_lbls = [f'{GROUP_LABELS[g]}\n(n={s})' for g, s in zip([1,2,3], sizes)]
wedges, texts, autotexts = ax2.pie(
    sizes, labels=pie_lbls, colors=[BLUE, ORANGE, GREEN],
    autopct='%1.1f%%', startangle=90,
    textprops={'color': WHITE, 'fontsize': 8})
for at in autotexts: at.set_color(DARK)

# ── 3. Discriminant scores scatter (F1 vs F2) ────────────────────────────────
ax3 = fig.add_subplot(gs[1, :2])
style_ax(ax3, 'Discriminant Score Plot: Function 1 vs Function 2')
for g in [1, 2, 3]:
    mask = y == g
    ax3.scatter(scores[mask, 0], scores[mask, 1],
                c=GROUP_COLORS[g], label=GROUP_LABELS[g],
                alpha=0.55, s=35, edgecolors='none')
# Plot centroids
for g in [1, 2, 3]:
    c1 = scores[y==g, 0].mean()
    c2 = scores[y==g, 1].mean()
    ax3.scatter(c1, c2, c=GROUP_COLORS[g], marker='*', s=280,
                edgecolors=WHITE, linewidths=0.8, zorder=5)
    ax3.annotate(f'  {GROUP_LABELS[g]}\n  centroid',
                 (c1, c2), color=WHITE, fontsize=7.5, fontweight='bold')
ax3.set_xlabel('Discriminant Function 1', color=WHITE)
ax3.set_ylabel('Discriminant Function 2', color=WHITE)
ax3.legend(facecolor=DARK, labelcolor=WHITE, fontsize=8)
ax3.axhline(0, color=GRAY, linewidth=0.6, alpha=0.4)
ax3.axvline(0, color=GRAY, linewidth=0.6, alpha=0.4)

# ── 4. Standardized coefficients for both functions ──────────────────────────
ax4 = fig.add_subplot(gs[1, 2])
style_ax(ax4, 'Std. Discriminant Coefficients')
x_att = np.arange(len(attitudes))
w4 = 0.35
c1_vals = std_scalings[:, 0]
c2_vals = std_scalings[:, 1]
ax4.barh(x_att + w4/2, c1_vals, w4, color=BLUE, alpha=0.85, label='Function 1')
ax4.barh(x_att - w4/2, c2_vals, w4, color=ORANGE, alpha=0.85, label='Function 2')
ax4.set_yticks(x_att)
ax4.set_yticklabels(attitudes, color=WHITE, fontsize=9)
ax4.axvline(0, color=WHITE, linewidth=0.8)
ax4.set_xlabel('Standardized Coefficient', color=WHITE)
ax4.legend(facecolor=DARK, labelcolor=WHITE, fontsize=8)

# ── 5. Structure matrix (correlations) ──────────────────────────────────────
ax5 = fig.add_subplot(gs[2, :2])
style_ax(ax5, 'Structure Matrix: Attitude–Function Correlations')
struct_f1 = [np.corrcoef(df[a].values, scores[:, 0])[0, 1] for a in attitudes]
struct_f2 = [np.corrcoef(df[a].values, scores[:, 1])[0, 1] for a in attitudes]
x_s = np.arange(len(attitudes))
w_s = 0.35
ax5.bar(x_s - w_s/2, struct_f1, w_s, color=BLUE, alpha=0.85, label='Function 1')
ax5.bar(x_s + w_s/2, struct_f2, w_s, color=ORANGE, alpha=0.85, label='Function 2')
ax5.set_xticks(x_s)
ax5.set_xticklabels(
    [f'{a}\n{labels[a][:18]}' for a in attitudes],
    color=WHITE, fontsize=7.5)
ax5.axhline(0, color=WHITE, linewidth=0.8)
ax5.set_ylabel('Correlation', color=WHITE)
ax5.set_ylim(-1, 1)
ax5.legend(facecolor=DARK, labelcolor=WHITE, fontsize=8)
ax5.axhline(0.3, color=GRAY, linestyle=':', linewidth=1, alpha=0.5)
ax5.axhline(-0.3, color=GRAY, linestyle=':', linewidth=1, alpha=0.5)

# ── 6. Classification accuracy per group ─────────────────────────────────────
ax6 = fig.add_subplot(gs[2, 2])
style_ax(ax6, 'Classification Accuracy by Group')
group_acc = []
for i, g in enumerate([1, 2, 3]):
    n_g = (y==g).sum()
    acc_g = cm[i, i] / n_g * 100
    group_acc.append(acc_g)

bars = ax6.bar(GROUP_LABELS.values(), group_acc,
               color=[BLUE, ORANGE, GREEN], alpha=0.85, width=0.5)
ax6.set_ylim(0, 110)
ax6.set_ylabel('Correct Classification (%)', color=WHITE)
for bar, acc in zip(bars, group_acc):
    ax6.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1,
             f'{acc:.1f}%', ha='center', va='bottom', color=WHITE,
             fontsize=10, fontweight='bold')
ax6.axhline(accuracy, color=RED, linestyle='--', linewidth=1.5,
            label=f'Overall ({accuracy:.1f}%)')
ax6.axhline(chance, color=GRAY, linestyle=':', linewidth=1.5,
            label=f'Chance ({chance:.1f}%)')
ax6.legend(facecolor=DARK, labelcolor=WHITE, fontsize=8)

fig.suptitle(
    f"Question 9.8 — Three-Group Discriminant Analysis (PHONE.DAT)\n"
    f"Wilks' Λ={wl:.4f}  χ²={chi2_stat:.2f} (df={df_chi}, p={p_chi2:.4f})"
    f"  Overall Classification={accuracy:.1f}%",
    color=WHITE, fontsize=12, fontweight='bold', y=0.99)

plt.savefig('q9_8_phone_discriminant.png', dpi=150, bbox_inches='tight',
            facecolor=DARK)
plt.close()
print("Figure saved: q9_8_phone_discriminant.png")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────────────────────────────────────
# DATA PARSING (fixed-width format per MASST.DOC)
# ─────────────────────────────────────────────────────────────────────────────
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
    'V4': (10, 12),'V5': (12, 14),'V6': (14, 16),
    'V7': (16, 17),'V8': (17, 18),'V9': (18, 19),
    'V10':(19, 20),'V11':(20, 21),'V12':(21, 22),
    'V13':(22, 23),'V14':(23, 24),'V15':(24, 25),
    'V16':(25, 26),'V17':(26, 27),'V18':(27, 28),
    'V19':(28, 29),'V20':(29, 30),'V21':(30, 31),
    'V22':(31, 32),'V23':(32, 33),'V24':(33, 34),
    'V25':(34, 35),'V26':(35, 36),'V27':(36, 37),
    'V28':(37, 38),'V29':(38, 39),'V30':(39, 40),
    'V31':(40, 41),'V32':(41, 42),'V33':(42, 43),
    'V34':(43, 44),'V35':(44, 45),'V36':(45, 46),
    'V37':(46, 47),'V38':(47, 48),
    'V39':(48, 49),'V40':(49, 50),'V41':(50, 51),
    'V42':(51, 52),'V43':(52, 53),'V44':(53, 54),
    'V45':(54, 55),'V46':(55, 56),'V47':(56, 57),
    'V48':(57, 58),'V49':(58, 59),'V50':(59, 60),
    'V51':(60, 61),'V52':(61, 62),
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

df = pd.DataFrame(rows)
print(f"Loaded {len(df)} observations")
print(f"Columns: {list(df.columns)}")

# ─────────────────────────────────────────────────────────────────────────────
# QUESTION 7.5 — Cluster Analysis on V7–V18 (latent demand for mass transit)
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("QUESTION 7.5 — Cluster Analysis on V7–V18")
print("  (Latent demand for mass transportation at various gas price levels)")
print("="*70)

v7_v18 = [f'V{i}' for i in range(7, 19)]
df_clust = df[['ID'] + v7_v18].dropna(subset=v7_v18)
X_clust = df_clust[v7_v18].values
print(f"\nObservations with complete V7–V18 data: {len(df_clust)}")

# Standardize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_clust)

# ── Step 1: Hierarchical clustering (Ward) to determine number of clusters ──
print("\n--- Step 1: Hierarchical Clustering (Ward's Method) ---")
Z = linkage(X_scaled, method='ward')

# Compute merge distances to find elbow
last_merges = Z[-15:, 2][::-1]
print("\nLast 10 merge distances (largest = biggest jumps = hint for k):")
for i, d in enumerate(last_merges[:10], 1):
    print(f"  {i} clusters: distance = {d:.4f}")

# Look for the biggest jump
diffs = np.diff(last_merges)
k_suggest = np.argmax(diffs) + 2
print(f"\nSuggested number of clusters (largest gap): k = {k_suggest}")

# We'll use k=2 (users vs nonusers as question 8.8 needs)
# But also try k=3 and show both
for k in [2, 3]:
    labels_hier = fcluster(Z, k, criterion='maxclust')
    counts = pd.Series(labels_hier).value_counts().sort_index()
    print(f"\nHierarchical k={k}: cluster sizes = {dict(counts)}")

# ── Step 2: K-Means refinement ───────────────────────────────────────────────
print("\n--- Step 2: K-Means Refinement ---")

# Elbow method to confirm k
inertias = []
ks = range(1, 9)
for k in ks:
    km = KMeans(n_clusters=k, random_state=42, n_init=20)
    km.fit(X_scaled)
    inertias.append(km.inertia_)

# Use k=2 as final (for Q8.8 we need users vs nonusers)
K_FINAL = 2
km_final = KMeans(n_clusters=K_FINAL, random_state=42, n_init=20)
km_final.fit(X_scaled)
df_clust = df_clust.copy()
df_clust['cluster'] = km_final.labels_

# ── Describe clusters ────────────────────────────────────────────────────────
print(f"\nFinal K-Means Solution (k={K_FINAL}):")
cluster_means = df_clust.groupby('cluster')[v7_v18].mean()
cluster_sizes = df_clust['cluster'].value_counts().sort_index()

gas_levels = ['10%','20%','30%','40%','50%','60%','70%','80%','90%','100%','150%','>150%']
print(f"\nCluster sizes: {dict(cluster_sizes)}")
print("\nMean Usage Scores by Cluster (1=will not use, 5=will use very frequently):")
print(f"{'Gas Increase':<12}", end="")
for c in range(K_FINAL):
    print(f"  Cluster {c+1} (n={cluster_sizes[c]})", end="")
print()
for i, (v, gl) in enumerate(zip(v7_v18, gas_levels)):
    print(f"  {gl:<10}", end="")
    for c in range(K_FINAL):
        print(f"  {cluster_means.loc[c, v]:>16.2f}", end="")
    print()

overall_means = [df_clust[v].mean() for v in v7_v18]
print(f"\n  Overall mean at each price level:")
for gl, m in zip(gas_levels, overall_means):
    print(f"    {gl}: {m:.2f}")

# Label clusters: cluster with higher overall mean usage = "users"
cluster_avg = cluster_means.mean(axis=1)
user_cluster = int(cluster_avg.idxmax())
nonuser_cluster = 1 - user_cluster
print(f"\nCluster {user_cluster+1} → 'USERS' (higher mass transit usage tendency)")
print(f"Cluster {nonuser_cluster+1} → 'NONUSERS' (lower mass transit usage tendency)")

df_clust['group'] = df_clust['cluster'].map({user_cluster: 1, nonuser_cluster: 0})
df_clust['group_label'] = df_clust['cluster'].map({user_cluster: 'Users', nonuser_cluster: 'Nonusers'})

print("\nCluster Interpretation:")
print(f"  USERS (n={cluster_sizes[user_cluster]}): Respondents who are likely to use mass")
print(f"    transit even at moderate gas price increases (avg score ≈ {cluster_avg[user_cluster]:.2f}/5)")
print(f"  NONUSERS (n={cluster_sizes[nonuser_cluster]}): Respondents who are unlikely to use")
print(f"    mass transit even at large gas price increases (avg score ≈ {cluster_avg[nonuser_cluster]:.2f}/5)")

# ─────────────────────────────────────────────────────────────────────────────
# QUESTION 8.8 — Discriminant Analysis: Users vs Nonusers
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("QUESTION 8.8 — Discriminant Analysis: Users vs Nonusers of Mass Transit")
print("  DV: cluster group (from Q7.5)   IVs: V1–V18")
print("="*70)

# Merge cluster labels back to full df using ID
df_full = df.merge(df_clust[['ID','group','group_label']], on='ID', how='inner')

disc_vars = [f'V{i}' for i in range(1, 19)]
df_disc = df_full[['ID','group','group_label'] + disc_vars].dropna(subset=disc_vars)
X_disc = df_disc[disc_vars].values
y_disc = df_disc['group'].values

n_disc = len(df_disc)
print(f"\nSample size for discriminant analysis: {n_disc}")
print(f"Users: {(y_disc==1).sum()}, Nonusers: {(y_disc==0).sum()}")

# Group means
print("\nGroup Means (V1–V18):")
print(f"{'Variable':<10} {'Label':<25} {'Nonusers':>10} {'Users':>10} {'Difference':>12}")
print("-"*65)
v_labels = {
    'V1': 'Economy', 'V2': 'Convenience', 'V3': 'Flexibility',
    'V4': 'Safe from dangerous ppl', 'V5': 'Low energy use',
    'V6': 'Dependability',
    'V7':'10% gas inc','V8':'20% gas inc','V9':'30% gas inc','V10':'40% gas inc',
    'V11':'50% gas inc','V12':'60% gas inc','V13':'70% gas inc','V14':'80% gas inc',
    'V15':'90% gas inc','V16':'100% gas inc','V17':'150% gas inc','V18':'>150% gas inc'
}
for v in disc_vars:
    m0 = df_disc.loc[y_disc==0, v].mean()
    m1 = df_disc.loc[y_disc==1, v].mean()
    print(f"  {v:<8} {v_labels[v]:<25} {m0:>10.3f} {m1:>10.3f} {m1-m0:>12.3f}")

# LDA
lda = LinearDiscriminantAnalysis()
lda.fit(X_disc, y_disc)
pred = lda.predict(X_disc)
scores = lda.transform(X_disc)

# Standardized coefficients
pooled_std = df_disc[disc_vars].std()
std_coefs = lda.coef_[0] * pooled_std.values

print("\nStandardized Discriminant Function Coefficients:")
print(f"{'Variable':<10} {'Label':<25} {'Std Coef':>10}")
print("-"*48)
for v, c in sorted(zip(disc_vars, std_coefs), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {v:<8} {v_labels[v]:<25} {c:>10.4f}")

print("\nRaw Discriminant Function Coefficients:")
for v, c in zip(disc_vars, lda.coef_[0]):
    print(f"  {v}: {c:.4f}")
print(f"  Constant: {lda.intercept_[0]:.4f}")

# Wilks' Lambda
def compute_wilks(X, y):
    p = X.shape[1]
    grand_mean = X.mean(axis=0)
    W = np.zeros((p, p))
    for g in np.unique(y):
        Xg = X[y == g]
        d = Xg - Xg.mean(axis=0)
        W += d.T @ d
    d_all = X - grand_mean
    T = d_all.T @ d_all
    dW = np.linalg.det(W)
    dT = np.linalg.det(T)
    return dW / dT if dT > 1e-20 else 1.0

wl = compute_wilks(X_disc, y_disc)
n, p = n_disc, len(disc_vars)
df1, df2 = p, n - p - 1
F_wl = ((1 - wl) / wl) * (df2 / df1)
p_wl = 1 - stats.f.cdf(F_wl, df1, df2)
print(f"\nWilks' Lambda: {wl:.4f}")
print(f"F-statistic (approx): {F_wl:.4f}  df1={df1}, df2={df2}")
print(f"p-value: {p_wl:.6f}")

cm = confusion_matrix(y_disc, pred)
accuracy = np.trace(cm) / n_disc * 100
print(f"\nClassification Matrix:")
print(f"                Predicted Nonuser  Predicted User")
print(f"Actual Nonuser:      {cm[0,0]:5d}         {cm[0,1]:5d}")
print(f"Actual User:         {cm[1,0]:5d}         {cm[1,1]:5d}")
print(f"\nCorrect Classification Rate: {accuracy:.1f}%")
print(f"  Nonusers correctly classified: {cm[0,0]/(cm[0,0]+cm[0,1])*100:.1f}%")
print(f"  Users correctly classified: {cm[1,1]/(cm[1,0]+cm[1,1])*100:.1f}%")

print("\n--- Interpretation ---")
print("""
The discriminant analysis distinguishes mass transit users from nonusers based
on their feature saliences (V1-V6) and price-sensitivity responses (V7-V18).

Key discriminating variables (by standardized coefficient magnitude):

- V7–V18 (price sensitivity variables): These carry the most discriminant 
  weight by design, since the clusters were formed from these variables.
  Users score higher on willingness to use mass transit across all price levels.

- Among V1–V6 (feature saliences):
  Variables with larger absolute standardized coefficients indicate that users
  and nonusers differ most in how much they value those specific features of
  mass transportation (economy, convenience, safety, dependability, etc.).

- The Wilks' Lambda and its F-test confirm whether the two groups are
  significantly different in multivariate space.

- A higher correct classification rate indicates the discriminant function
  reliably separates the two groups identified by cluster analysis.
""")

# ─────────────────────────────────────────────────────────────────────────────
# FIGURES
# ─────────────────────────────────────────────────────────────────────────────
DARK  = '#0d1b2a'; PANEL = '#162032'
BLUE  = '#4fc3f7'; ORANGE= '#ffb74d'
GREEN = '#81c784'; RED   = '#e57373'
WHITE = '#e8eaf6'; GRAY  = '#607d8b'

def style_ax(ax, title):
    ax.set_facecolor(PANEL)
    for sp in ax.spines.values(): sp.set_edgecolor(GRAY)
    ax.tick_params(colors=WHITE, labelsize=8)
    ax.xaxis.label.set_color(WHITE)
    ax.yaxis.label.set_color(WHITE)
    ax.set_title(title, color=WHITE, fontsize=10, fontweight='bold', pad=6)

fig = plt.figure(figsize=(18, 16))
fig.patch.set_facecolor(DARK)
gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.5, wspace=0.38)

# ── 1. Dendrogram (truncated) ─────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0, :2])
style_ax(ax1, "Hierarchical Clustering Dendrogram (Ward's Method, truncated)")
d = dendrogram(Z, ax=ax1, truncate_mode='lastp', p=20,
               color_threshold=Z[-2, 2],
               above_threshold_color=GRAY,
               link_color_func=lambda k: BLUE if k <= 2 else ORANGE)
ax1.set_xlabel('Cluster / Sample', color=WHITE)
ax1.set_ylabel('Distance', color=WHITE)
ax1.axhline(Z[-K_FINAL, 2]*1.01, color=RED, linestyle='--', linewidth=1.5,
            label=f'Cut for k={K_FINAL}')
ax1.legend(facecolor=DARK, labelcolor=WHITE, fontsize=8)

# ── 2. Elbow plot ────────────────────────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 2])
style_ax(ax2, 'K-Means Elbow Plot')
ax2.plot(list(ks), inertias, 'o-', color=BLUE, linewidth=2, markersize=7)
ax2.axvline(K_FINAL, color=RED, linestyle='--', linewidth=1.5, label=f'k={K_FINAL} selected')
ax2.set_xlabel('Number of Clusters (k)', color=WHITE)
ax2.set_ylabel('Within-cluster Inertia', color=WHITE)
ax2.legend(facecolor=DARK, labelcolor=WHITE, fontsize=8)

# ── 3. Cluster profiles (V7–V18) ─────────────────────────────────────────
ax3 = fig.add_subplot(gs[1, :2])
style_ax(ax3, 'Cluster Profiles: Mean Usage Score by Gas Price Level (Q7.5)')
x = np.arange(len(gas_levels))
w = 0.35
colors_c = [BLUE, ORANGE]
labels_c = [f'Cluster {nonuser_cluster+1}: Nonusers (n={cluster_sizes[nonuser_cluster]})',
            f'Cluster {user_cluster+1}: Users (n={cluster_sizes[user_cluster]})']
for i, (c_id, lbl, col) in enumerate(zip([nonuser_cluster, user_cluster], labels_c, [BLUE, ORANGE])):
    means = [cluster_means.loc[c_id, v] for v in v7_v18]
    ax3.bar(x + (i-0.5)*w, means, w, label=lbl, color=col, alpha=0.85)
ax3.set_xticks(x)
ax3.set_xticklabels(gas_levels, rotation=30, ha='right', color=WHITE, fontsize=8)
ax3.set_ylabel('Mean Usage Score (1–5)', color=WHITE)
ax3.set_ylim(0, 5.5)
ax3.legend(facecolor=DARK, labelcolor=WHITE, fontsize=8)
ax3.axhline(3, color=GRAY, linestyle=':', linewidth=1, alpha=0.5)

# ── 4. Cluster sizes pie ─────────────────────────────────────────────────
ax4 = fig.add_subplot(gs[1, 2])
style_ax(ax4, 'Cluster Composition (Q7.5)')
sizes = [cluster_sizes[nonuser_cluster], cluster_sizes[user_cluster]]
lbls = [f'Nonusers\n(n={sizes[0]})', f'Users\n(n={sizes[1]})']
wedges, texts, autotexts = ax4.pie(
    sizes, labels=lbls, colors=[BLUE, ORANGE],
    autopct='%1.1f%%', startangle=90,
    textprops={'color': WHITE, 'fontsize': 9}
)
for at in autotexts: at.set_color(DARK)

# ── 5. Standardized discriminant coefficients ────────────────────────────
ax5 = fig.add_subplot(gs[2, :2])
style_ax(ax5, 'Standardized Discriminant Coefficients (Q8.8)')
coef_series = pd.Series(std_coefs, index=disc_vars)
coef_sorted = coef_series.reindex(
    coef_series.abs().sort_values(ascending=True).index)
bar_cols = [GREEN if v >= 0 else RED for v in coef_sorted.values]
ax5.barh(coef_sorted.index, coef_sorted.values, color=bar_cols, alpha=0.85)
ax5.axvline(0, color=WHITE, linewidth=0.8)
ax5.set_xlabel('Standardized Coefficient', color=WHITE)
for i, (val, nm) in enumerate(zip(coef_sorted.values, coef_sorted.index)):
    ax5.text(val + (0.005 if val >= 0 else -0.005), i,
             f'{val:.3f}', va='center',
             ha='left' if val >= 0 else 'right', color=WHITE, fontsize=7)

# ── 6. Discriminant score distribution ──────────────────────────────────
ax6 = fig.add_subplot(gs[2, 2])
style_ax(ax6, 'Discriminant Score Distribution (Q8.8)')
for g, lbl, col in [(0,'Nonusers',BLUE),(1,'Users',ORANGE)]:
    ax6.hist(scores[y_disc==g, 0], bins=20, alpha=0.6, color=col, label=lbl)
ax6.axvline(0, color=WHITE, linestyle='--', linewidth=1, alpha=0.6)
ax6.set_xlabel('Discriminant Score', color=WHITE)
ax6.set_ylabel('Frequency', color=WHITE)
ax6.legend(facecolor=DARK, labelcolor=WHITE, fontsize=8)

fig.suptitle(
    'Q7.5 — Cluster Analysis & Q8.8 — Discriminant Analysis (MASST.DAT)\n'
    f"Wilks' Λ={wl:.4f}  F={F_wl:.2f}  p={p_wl:.4f}  "
    f"Classification Accuracy={accuracy:.1f}%",
    color=WHITE, fontsize=12, fontweight='bold', y=0.99)

plt.savefig('q7_5_q8_8_mass_transit.png', dpi=150, bbox_inches='tight',
            facecolor=DARK)
plt.close()
print("Figure saved: q7_5_q8_8_mass_transit.png")

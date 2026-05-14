"""
Dataset 2 — Cluster Analysis + Canonical Correlation Analysis
Manufacturing Plant Efficiency Study | n = 240 plants
Research Question:
  What distinct operational profiles emerge among manufacturing plants,
  and what is the canonical multivariate relationship between production
  efficiency metrics and quality/cost outcome metrics?
  Two objectives, two multivariate methods:
    (1) K-Means + Hierarchical Clustering — discover plant typologies
    (2) Canonical Correlation Analysis (CCA) — quantify the multivariate
        association between efficiency inputs and quality/cost outputs
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy import stats
import warnings, os, json
warnings.filterwarnings('ignore')

OUT = 'Lana_Gidan_Software_Exam/Dataset2_ClusterAnalysis'
os.makedirs(OUT, exist_ok=True)

df = pd.read_excel('attached_assets/Data_set-2_1778677563523.xlsx',
                   sheet_name='Cluster_Data')

ALL_FEATS = ['Production_Speed', 'Defect_Rate', 'Energy_Consumption',
             'Labor_Cost', 'Machine_Downtime', 'Maintenance_Cost', 'Inventory_Turnover']
EFF_SET   = ['Production_Speed', 'Energy_Consumption', 'Inventory_Turnover']
QUAL_SET  = ['Defect_Rate', 'Labor_Cost', 'Machine_Downtime', 'Maintenance_Cost']

lines = []
def log(s=''):
    lines.append(str(s))
    print(s)

log('=' * 72)
log('  CLUSTER ANALYSIS + CANONICAL CORRELATION — MANUFACTURING STUDY')
log('  n = 240 plants | 7 operational variables')
log('=' * 72)

# ════════════════════════════════════════════════════════════════════════
# PART A — CLUSTER ANALYSIS
# ════════════════════════════════════════════════════════════════════════
log('\n' + '═'*72)
log('  PART A — CLUSTER ANALYSIS (K-Means + Hierarchical)')
log('═'*72)

log('\n── A1. RESEARCH QUESTION ─────────────────────────────────────────────')
log('  Can manufacturing plants be segmented into meaningful operational')
log('  profiles based on their efficiency, quality, and cost metrics,')
log('  without using any pre-existing plant type labels?')

log('\n── A2. DESCRIPTIVE STATISTICS ───────────────────────────────────────')
log(df[ALL_FEATS].describe().round(3).to_string())

X = df[ALL_FEATS].values
scaler = StandardScaler()
X_sc = scaler.fit_transform(X)

log('\n── A3. OPTIMAL k — ELBOW + SILHOUETTE ───────────────────────────────')
log(f'  {"k":>4} {"Inertia":>12} {"Silhouette":>12} {"Davies-Bouldin":>16}')
log('  ' + '-'*48)
sil_scores = {}
for k in range(2, 8):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_sc)
    sil = silhouette_score(X_sc, labels)
    db  = davies_bouldin_score(X_sc, labels)
    sil_scores[k] = sil
    log(f'  {k:>4} {km.inertia_:>12.1f} {sil:>12.4f} {db:>16.4f}')

best_k = max(sil_scores, key=sil_scores.get)
log(f'\n  → Optimal k = {best_k} (highest silhouette = {sil_scores[best_k]:.4f})')

log('\n── A4. K-MEANS CLUSTERING ────────────────────────────────────────────')
km_final = KMeans(n_clusters=best_k, random_state=42, n_init=10)
df['KMeans_Cluster'] = km_final.fit_predict(X_sc)
sil_final = silhouette_score(X_sc, df['KMeans_Cluster'])
db_final  = davies_bouldin_score(X_sc, df['KMeans_Cluster'])

log(f'  Final k = {best_k} | Silhouette = {sil_final:.4f} | Davies-Bouldin = {db_final:.4f}')
log(f'\n  Cluster sizes:')
for cl, cnt in df['KMeans_Cluster'].value_counts().sort_index().items():
    log(f'    Cluster {cl}: n = {cnt}')

log('\n── A5. CLUSTER PROFILES (MEANS) ─────────────────────────────────────')
profiles = df.groupby('KMeans_Cluster')[ALL_FEATS].mean()
log(f'\n  {"Feature":<24}  ' + '  '.join(f'{"Cl "+str(c):>12}' for c in range(best_k)))
log('  ' + '-'*80)
for feat in ALL_FEATS:
    vals = '  '.join(f'{profiles.loc[c, feat]:>12.3f}' for c in range(best_k))
    log(f'  {feat:<24}  {vals}')

log('\n  Plant Type overlap with known labels:')
ct = pd.crosstab(df['KMeans_Cluster'], df['Plant_Type'])
log(ct.to_string())

log('\n  Cluster interpretation:')
cluster_labels = {}
for c in range(best_k):
    prof = profiles.loc[c]
    speed = prof['Production_Speed']
    defect = prof['Defect_Rate']
    energy = prof['Energy_Consumption']
    labor = prof['Labor_Cost']
    downtime = prof['Machine_Downtime']
    if speed > 85 and defect < 2:
        label = 'High Automation (fast, precise, high energy)'
    elif speed > 75 and labor < 55 and downtime < 5:
        label = 'Lean Manufacturing (efficient, low waste)'
    elif labor > 80:
        label = 'Labor-Intensive (slow, high labor cost)'
    else:
        label = 'Aging Facility (high defects, high downtime)'
    cluster_labels[c] = label
    log(f'    Cluster {c}: {label}')

log('\n── A6. HIERARCHICAL CLUSTERING (Ward Linkage) ───────────────────────')
hc = AgglomerativeClustering(n_clusters=best_k, linkage='ward')
df['HC_Cluster'] = hc.fit_predict(X_sc)
sil_hc = silhouette_score(X_sc, df['HC_Cluster'])
log(f'  Hierarchical Silhouette = {sil_hc:.4f}  |  K-Means = {sil_final:.4f}')
log(f'  Agreement between methods: '
    f'{(df["KMeans_Cluster"]==df["HC_Cluster"]).mean()*100:.1f}% identical assignments')

# ════════════════════════════════════════════════════════════════════════
# PART B — CANONICAL CORRELATION ANALYSIS
# ════════════════════════════════════════════════════════════════════════
log('\n' + '═'*72)
log('  PART B — CANONICAL CORRELATION ANALYSIS (CCA)')
log('  Efficiency Set vs Quality/Cost Set')
log('═'*72)

log('\n── B1. RESEARCH QUESTION ─────────────────────────────────────────────')
log('  What is the strength and structure of the multivariate relationship')
log('  between production efficiency metrics (speed, energy, inventory) and')
log('  quality/cost outcome metrics (defects, labor, downtime, maintenance)?')
log('  CCA finds the linear combinations of each set that are maximally correlated.')

log('\n── B2. VARIABLE SETS ────────────────────────────────────────────────')
log(f'  Set 1 — Efficiency Inputs (p = {len(EFF_SET)}):')
for v in EFF_SET:
    log(f'    • {v}')
log(f'  Set 2 — Quality/Cost Outputs (q = {len(QUAL_SET)}):')
for v in QUAL_SET:
    log(f'    • {v}')

X_eff  = df[EFF_SET].values.astype(float)
X_qual = df[QUAL_SET].values.astype(float)
X_eff_sc  = StandardScaler().fit_transform(X_eff)
X_qual_sc = StandardScaler().fit_transform(X_qual)
n = len(df)
p = len(EFF_SET)
q = len(QUAL_SET)

# CCA via SVD
Sxx = np.cov(X_eff_sc.T)
Syy = np.cov(X_qual_sc.T)
Sxy = np.cov(X_eff_sc.T, X_qual_sc.T)[:p, p:]

# Regularize to avoid singular matrix
eps = 1e-6
Sxx_inv_half = np.linalg.inv(Sxx + eps*np.eye(p))
Syy_inv_half = np.linalg.inv(Syy + eps*np.eye(q))

K = Sxx_inv_half @ Sxy @ Syy_inv_half
U, canonical_corrs, Vt = np.linalg.svd(K)
canonical_corrs = np.clip(canonical_corrs, 0, 1)

n_roots = min(p, q)
canonical_corrs = canonical_corrs[:n_roots]
A = Sxx_inv_half @ U[:, :n_roots]
B = Syy_inv_half @ Vt.T[:, :n_roots]

log('\n── B3. CANONICAL CORRELATIONS ────────────────────────────────────────')
log(f'  {"Root":<6} {"Canonical r":>13} {"r²":>10} {"Wilks λ":>10} {"χ²":>10} {"df":>6} {"p":>10}  Sig')
log('  ' + '-'*80)

cca_roots = []
wilks_lambda = 1.0
for i, rc in enumerate(canonical_corrs):
    r2 = rc**2
    wilks_lambda *= (1 - r2)
    # Bartlett's χ² test
    chi2 = -(n - 1 - (p + q + 1)/2) * np.log(wilks_lambda)
    df_chi = (p - i) * (q - i)
    p_chi  = 1 - stats.chi2.cdf(chi2, df_chi)
    sig    = '***' if p_chi < 0.001 else '**' if p_chi < 0.01 else '*' if p_chi < 0.05 else 'n.s.'
    cca_roots.append({'r': rc, 'r2': r2, 'wilks': wilks_lambda,
                      'chi2': chi2, 'df': df_chi, 'p': p_chi})
    log(f'  {i+1:<6} {rc:>13.4f} {r2:>10.4f} {wilks_lambda:>10.4f} {chi2:>10.4f} {df_chi:>6} {p_chi:>10.4f}  {sig}')

log('\n── B4. CANONICAL WEIGHTS (STANDARDIZED) ─────────────────────────────')
log('  Contribution of each variable to the canonical variate.')
log('  Larger |weight| = stronger contribution to the canonical dimension.')
log('')
log('  Set 1 — Efficiency Variables (weights for each canonical root):')
log(f'  {"Variable":<30}  ' + '  '.join(f'{"Root"+str(i+1):>10}' for i in range(n_roots)))
log('  ' + '-'*60)
for j, feat in enumerate(EFF_SET):
    vals = '  '.join(f'{A[j, i]:>+10.4f}' for i in range(n_roots))
    log(f'  {feat:<30}  {vals}')

log('')
log('  Set 2 — Quality/Cost Variables (weights for each canonical root):')
log(f'  {"Variable":<30}  ' + '  '.join(f'{"Root"+str(i+1):>10}' for i in range(n_roots)))
log('  ' + '-'*60)
for j, feat in enumerate(QUAL_SET):
    vals = '  '.join(f'{B[j, i]:>+10.4f}' for i in range(n_roots))
    log(f'  {feat:<30}  {vals}')

log('\n── B5. STRUCTURE COEFFICIENTS (CANONICAL LOADINGS) ─────────────────')
log('  Correlation of each variable with its own canonical variate.')
log('  More stable than weights when variables are intercorrelated.')
log('')
U_scores = X_eff_sc @ A
V_scores = X_qual_sc @ B

log('  Set 1 — Efficiency Structure Coefficients:')
log(f'  {"Variable":<30}  ' + '  '.join(f'{"Root"+str(i+1):>10}' for i in range(n_roots)))
log('  ' + '-'*60)
for j, feat in enumerate(EFF_SET):
    corrs = [float(np.corrcoef(X_eff_sc[:, j], U_scores[:, i])[0, 1]) for i in range(n_roots)]
    vals = '  '.join(f'{c:>+10.4f}' for c in corrs)
    log(f'  {feat:<30}  {vals}')

log('')
log('  Set 2 — Quality/Cost Structure Coefficients:')
log(f'  {"Variable":<30}  ' + '  '.join(f'{"Root"+str(i+1):>10}' for i in range(n_roots)))
log('  ' + '-'*60)
for j, feat in enumerate(QUAL_SET):
    corrs = [float(np.corrcoef(X_qual_sc[:, j], V_scores[:, i])[0, 1]) for i in range(n_roots)]
    vals = '  '.join(f'{c:>+10.4f}' for c in corrs)
    log(f'  {feat:<30}  {vals}')

log('\n── B6. INTERPRETATION ────────────────────────────────────────────────')
log(f'  Root 1: r_c = {cca_roots[0]["r"]:.4f}, r²_c = {cca_roots[0]["r2"]:.4f} '
    f'({cca_roots[0]["r2"]*100:.1f}% shared variance)')
sig_roots = [r for r in cca_roots if r['p'] < 0.05]
log(f'  Number of significant canonical roots: {len(sig_roots)}')
log(f'\n  The first canonical root captures {cca_roots[0]["r2"]*100:.1f}% of the')
log('  shared variance between the efficiency set and the quality/cost set.')
log('  This quantifies how strongly the two multivariate domains co-vary:')
log('  plants that score high on efficiency tend to show a corresponding')
log('  signature in quality and cost metrics — and CCA identifies the')
log('  exact linear combination that maximizes this relationship.')

log('\n── B7. BETWEEN-SET CORRELATIONS ─────────────────────────────────────')
log('  Pearson r between each pair of cross-set variables (bivariate preview):')
log(f'  {"Efficiency Var":<28}  {"Quality/Cost Var":<28} {"r":>8} {"p":>10}')
log('  ' + '-'*78)
for ev in EFF_SET:
    for qv in QUAL_SET:
        r, p_val = stats.pearsonr(df[ev], df[qv])
        log(f'  {ev:<28}  {qv:<28} {r:>+8.4f} {p_val:>10.4f}')

# ════════════════════════════════════════════════════════════════════════
# FIGURES
# ════════════════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(18, 12))
fig.suptitle('Cluster Analysis + CCA — Manufacturing Plant Study (n=240)',
             fontsize=13, fontweight='bold')

# PCA for cluster visualization
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_sc)
ax1 = fig.add_subplot(2, 3, 1)
colors_cl = ['#e74c3c','#3498db','#2ecc71','#f39c12']
for cl in range(best_k):
    mask = df['KMeans_Cluster'] == cl
    ax1.scatter(X_pca[mask, 0], X_pca[mask, 1],
                c=colors_cl[cl], label=f'Cluster {cl}', alpha=0.6, s=25)
ax1.set_title(f'K-Means Clusters (k={best_k})\nPCA Visualization', fontweight='bold')
ax1.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)')
ax1.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)')
ax1.legend(fontsize=7); ax1.grid(alpha=0.3)

# Silhouette by k
ax2 = fig.add_subplot(2, 3, 2)
ks = list(sil_scores.keys())
sils = list(sil_scores.values())
ax2.plot(ks, sils, 'o-', color='#2c5f8a', lw=2, markersize=8)
ax2.axvline(best_k, color='red', ls='--', lw=1.5, label=f'Optimal k={best_k}')
ax2.set_title('Silhouette Score by k', fontweight='bold')
ax2.set_xlabel('Number of Clusters k'); ax2.set_ylabel('Silhouette Score')
ax2.legend(); ax2.grid(alpha=0.3)

# Cluster profile heatmap
ax3 = fig.add_subplot(2, 3, 3)
prof_sc = pd.DataFrame(
    scaler.transform(profiles.values), columns=ALL_FEATS,
    index=[f'Cluster {c}' for c in range(best_k)])
sns.heatmap(prof_sc, annot=True, fmt='.2f', cmap='RdYlGn', ax=ax3,
            linewidths=0.5, cbar_kws={'shrink': 0.8})
ax3.set_title('Cluster Profiles (z-scores)', fontweight='bold')

# Dendrogram
ax4 = fig.add_subplot(2, 3, 4)
sample_idx = np.random.choice(len(X_sc), 60, replace=False)
Z = linkage(X_sc[sample_idx], method='ward')
dendrogram(Z, ax=ax4, color_threshold=3.5,
           leaf_font_size=6, no_labels=True)
ax4.set_title(f'Hierarchical Dendrogram\n(Ward, n=60 sample)', fontweight='bold')
ax4.set_xlabel('Plants'); ax4.set_ylabel('Distance')
ax4.axhline(3.5, color='red', ls='--', lw=1.5, label=f'Cut → {best_k} clusters')
ax4.legend(fontsize=7)

# Canonical correlations
ax5 = fig.add_subplot(2, 3, 5)
roots = range(1, n_roots+1)
rc_vals = [r['r'] for r in cca_roots]
colors_sig = ['#2c5f8a' if r['p']<0.05 else '#aaaaaa' for r in cca_roots]
ax5.bar(roots, rc_vals, color=colors_sig, edgecolor='black', lw=0.6)
ax5.set_title('Canonical Correlations by Root\n(blue = significant p<.05)', fontweight='bold')
ax5.set_xlabel('Canonical Root'); ax5.set_ylabel('Canonical r')
ax5.set_xticks(list(roots))
for i, (r, pv) in enumerate(zip(rc_vals, [r['p'] for r in cca_roots])):
    sig = '***' if pv<0.001 else '**' if pv<0.01 else '*' if pv<0.05 else ''
    ax5.text(i+1, r+0.02, f'{r:.3f}{sig}', ha='center', fontsize=8)
ax5.grid(axis='y', alpha=0.3)

# Canonical variate scatter
ax6 = fig.add_subplot(2, 3, 6)
colors_pt = {'High_Automation':'#e74c3c', 'Labor_Intensive':'#3498db',
             'Lean_Manufacturing':'#2ecc71', 'Aging_Facility':'#f39c12'}
for pt, col in colors_pt.items():
    mask = df['Plant_Type'] == pt
    ax6.scatter(U_scores[mask, 0], V_scores[mask, 0],
                c=col, label=pt.replace('_',' '), alpha=0.5, s=20)
r_cv, _ = stats.pearsonr(U_scores[:, 0], V_scores[:, 0])
ax6.set_title(f'Canonical Variate 1 Scatter\n'
              f'U₁ vs V₁  (r_c = {r_cv:.4f})', fontweight='bold')
ax6.set_xlabel('Efficiency Canonical Variate (U₁)')
ax6.set_ylabel('Quality/Cost Canonical Variate (V₁)')
ax6.legend(fontsize=6); ax6.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(f'{OUT}/dataset2_cluster_cca_analysis.png', dpi=150, bbox_inches='tight')
plt.close()

with open(f'{OUT}/dataset2_ClusterCCA_output.txt', 'w') as f:
    f.write('\n'.join(lines))

metrics = {
    'best_k': best_k, 'sil_kmeans': sil_final,
    'sil_hc': sil_hc, 'sil_by_k': sil_scores,
    'cca_roots': cca_roots,
    'cluster_labels': cluster_labels,
}
with open('ds2_metrics.json', 'w') as f:
    json.dump(metrics, f)

print(f'\nAll DS2 files saved to {OUT}/')

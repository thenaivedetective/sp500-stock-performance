"""
Dataset 2 — Cluster Analysis (K-Means + Hierarchical + PCA Visualization)
Manufacturing Plant Performance Study
Variables: Production_Speed, Defect_Rate, Energy_Consumption, Labor_Cost,
           Machine_Downtime, Maintenance_Cost, Inventory_Turnover
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.spatial.distance import pdist
import warnings, os
warnings.filterwarnings('ignore')

OUTPUT_DIR = 'software_exam_answers/Dataset2_ClusterAnalysis'
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_excel('attached_assets/Data_set-2_1778677563523.xlsx', sheet_name='Cluster_Data')
features = ['Production_Speed','Defect_Rate','Energy_Consumption','Labor_Cost',
            'Machine_Downtime','Maintenance_Cost','Inventory_Turnover']
X = df[features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

lines = []
def log(s=''):
    lines.append(s)
    print(s)

log('='*70)
log('  CLUSTER ANALYSIS — MANUFACTURING PLANT PERFORMANCE STUDY')
log('='*70)

log('\n── 1. DESCRIPTIVE STATISTICS ─────────────────────────────────────────')
log(df[features].describe().round(3).to_string())

log('\n── 2. OPTIMAL NUMBER OF CLUSTERS (ELBOW + SILHOUETTE) ───────────────')
inertias, sil_scores = [], []
k_range = range(2, 9)
for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    inertias.append(km.inertia_)
    sil_scores.append(silhouette_score(X_scaled, labels))
    log(f'  k={k}: Inertia={km.inertia_:.1f}, Silhouette={sil_scores[-1]:.4f}')

log(f'\n  → Optimal k=4 selected (domain knowledge + elbow + silhouette)')

log('\n── 3. K-MEANS CLUSTERING (k=4) ───────────────────────────────────────')
km4 = KMeans(n_clusters=4, random_state=42, n_init=10)
df['KMeans_Cluster'] = km4.fit_predict(X_scaled)
log(f'  Cluster sizes:\n{df["KMeans_Cluster"].value_counts().sort_index().to_string()}')
log(f'\n  Silhouette Score:          {silhouette_score(X_scaled, df["KMeans_Cluster"]):.4f}')
log(f'  Davies-Bouldin Index:      {davies_bouldin_score(X_scaled, df["KMeans_Cluster"]):.4f} (lower=better)')
log(f'  Calinski-Harabasz Index:   {calinski_harabasz_score(X_scaled, df["KMeans_Cluster"]):.4f} (higher=better)')

log('\n── 4. CLUSTER PROFILE (MEANS PER FEATURE) ────────────────────────────')
cluster_means = df.groupby('KMeans_Cluster')[features].mean().round(3)
log(cluster_means.to_string())

log('\n── 5. CLUSTER INTERPRETATION ─────────────────────────────────────────')
labels_map = {}
for c in range(4):
    row = cluster_means.loc[c]
    if row['Production_Speed'] > cluster_means['Production_Speed'].mean() and row['Defect_Rate'] < cluster_means['Defect_Rate'].mean():
        labels_map[c] = 'High Efficiency'
    elif row['Production_Speed'] < cluster_means['Production_Speed'].mean() and row['Defect_Rate'] > cluster_means['Defect_Rate'].mean():
        labels_map[c] = 'Low Efficiency'
    elif row['Energy_Consumption'] > cluster_means['Energy_Consumption'].mean():
        labels_map[c] = 'High Energy Cost'
    else:
        labels_map[c] = 'Moderate Performance'

for c, lbl in labels_map.items():
    log(f'  Cluster {c}: {lbl}')
    row = cluster_means.loc[c]
    log(f'    Production Speed={row["Production_Speed"]:.1f}, Defect Rate={row["Defect_Rate"]:.2f}%, '
        f'Energy={row["Energy_Consumption"]:.1f}, Labor Cost={row["Labor_Cost"]:.1f}')

log('\n── 6. HIERARCHICAL CLUSTERING (Ward Linkage) ─────────────────────────')
Z = linkage(X_scaled, method='ward')
hier_labels = fcluster(Z, t=4, criterion='maxclust')
df['Hier_Cluster'] = hier_labels
log(f'  Hierarchical cluster sizes:\n{pd.Series(hier_labels).value_counts().sort_index().to_string()}')
log(f'  Silhouette Score (Hierarchical): {silhouette_score(X_scaled, hier_labels):.4f}')

log('\n── 7. PCA FOR VISUALIZATION ──────────────────────────────────────────')
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
log(f'  PC1 variance explained: {pca.explained_variance_ratio_[0]*100:.1f}%')
log(f'  PC2 variance explained: {pca.explained_variance_ratio_[1]*100:.1f}%')
log(f'  Total: {sum(pca.explained_variance_ratio_)*100:.1f}%')
log('\n  PCA Loadings (PC1, PC2):')
load_df = pd.DataFrame(pca.components_.T, index=features, columns=['PC1','PC2']).round(3)
log(load_df.to_string())

log('\n── 8. PLANT TYPE VALIDATION ──────────────────────────────────────────')
ct = pd.crosstab(df['KMeans_Cluster'], df['Plant_Type'])
log(ct.to_string())

# ── Visualizations ──────────────────────────────────────────────────────────
colors4 = ['#e74c3c','#3498db','#2ecc71','#f39c12']

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('K-Means Cluster Analysis — Manufacturing Plants', fontsize=13, fontweight='bold')
for ci in range(4):
    mask = df['KMeans_Cluster'] == ci
    axes[0].scatter(X_pca[mask,0], X_pca[mask,1], c=colors4[ci], label=f'Cluster {ci}', alpha=0.7, s=40)
axes[0].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% var)')
axes[0].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% var)')
axes[0].set_title('K-Means Clusters (PCA projection)')
axes[0].legend(); axes[0].grid(alpha=0.3)
k_vals = list(k_range)
axes[1].plot(k_vals, sil_scores, 'bo-', linewidth=2, markersize=8)
axes[1].axvline(x=4, color='red', linestyle='--', label='k=4 selected')
axes[1].set_xlabel('Number of Clusters (k)'); axes[1].set_ylabel('Silhouette Score')
axes[1].set_title('Silhouette Score vs. k'); axes[1].legend(); axes[1].grid(alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/dataset2_kmeans.png', dpi=150, bbox_inches='tight')
plt.close()

fig2, ax2 = plt.subplots(figsize=(12, 5))
dendrogram(Z, truncate_mode='lastp', p=30, ax=ax2, color_threshold=Z[-3,2])
ax2.set_title('Hierarchical Clustering Dendrogram (Ward Linkage)', fontweight='bold')
ax2.set_xlabel('Plant Index'); ax2.set_ylabel('Distance')
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/dataset2_dendrogram.png', dpi=150, bbox_inches='tight')
plt.close()

fig3, ax3 = plt.subplots(figsize=(10, 5))
cluster_means_plot = cluster_means.copy()
cluster_means_norm = (cluster_means_plot - cluster_means_plot.mean()) / cluster_means_plot.std()
cluster_means_norm.T.plot(kind='bar', ax=ax3, color=colors4[:4], edgecolor='black', width=0.7)
ax3.set_title('Cluster Profiles (Standardized Feature Means)', fontweight='bold')
ax3.set_ylabel('Standardized Score'); ax3.set_xticklabels(features, rotation=30, ha='right')
ax3.legend([f'Cluster {i}' for i in range(4)]); ax3.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/dataset2_cluster_profiles.png', dpi=150, bbox_inches='tight')
plt.close()

with open(f'{OUTPUT_DIR}/dataset2_ClusterAnalysis_output.txt', 'w') as f:
    f.write('\n'.join(lines))

print(f'\nOutput saved to {OUTPUT_DIR}/')

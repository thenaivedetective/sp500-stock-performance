"""
Generate SAS-equivalent figures for each homework question.
White background, clean academic style matching PROC SGPLOT output.
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import warnings; warnings.filterwarnings('ignore')

# SAS-style aesthetics
SAS_COLORS = ['#1F77B4', '#FF7F0E', '#2CA02C']  # blue, orange, green
BG = 'white'
GRID = '#dddddd'

def sas_style(ax, title='', xlabel='', ylabel=''):
    ax.set_facecolor(BG)
    ax.figure.patch.set_facecolor(BG)
    ax.grid(True, color=GRID, linewidth=0.7, linestyle='-')
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_edgecolor('#999999')
        spine.set_linewidth(0.8)
    if title:  ax.set_title(title, fontsize=10, fontweight='bold', pad=6)
    if xlabel: ax.set_xlabel(xlabel, fontsize=9)
    if ylabel: ax.set_ylabel(ylabel, fontsize=9)
    ax.tick_params(labelsize=8)

# =============================================================================
# Load all data (same logic as generate_pdf.py)
# =============================================================================

# ── Q8.7 ─────────────────────────────────────────────────────────────────────
col_names = [
    'OBS','ID','SEX','AGE','MARITAL','EDUCAT','EMPLOY','INCOME','RELIG',
    'C1','C2','C3','C4','C5','C6','C7','C8','C9','C10',
    'C11','C12','C13','C14','C15','C16','C17','C18','C19','C20',
    'CESD','CASES','DRINK','HEALTH','REGDOC','TREAT','BEDDAYS','ACUTEILL','CHRONILL'
]
rows = []
with open('attached_assets/DEPRES_1773880715452.DAT') as f:
    for line in f:
        v = line.strip().split()
        if len(v) == 38:
            rows.append([float(x) for x in v])
df87 = pd.DataFrame(rows, columns=col_names)
y87  = df87['CASES'].values

# ── Q7.5 / Q8.8 ──────────────────────────────────────────────────────────────
def parse_val(s):
    s = s.strip()
    if s in ('', '.', '..', '...', '....', '.....'): return np.nan
    try: return float(s)
    except: return np.nan

colspecs = {
    'ID':(0,4),'V1':(4,6),'V2':(6,8),'V3':(8,10),'V4':(10,12),
    'V5':(12,14),'V6':(14,16),
    'V7':(16,17),'V8':(17,18),'V9':(18,19),'V10':(19,20),'V11':(20,21),
    'V12':(21,22),'V13':(22,23),'V14':(23,24),'V15':(24,25),'V16':(25,26),
    'V17':(26,27),'V18':(27,28),
}
rows_m = []
with open('attached_assets/MASST_1773881001970.DAT') as f:
    for line in f:
        raw = line.rstrip('\n')
        if len(raw) < 20 or raw.strip().startswith('Mass') or \
           raw.strip().startswith('(') or raw.strip().startswith('---') or \
           raw.strip() == '': continue
        row = {}
        for col, (s, e) in colspecs.items():
            row[col] = parse_val(raw[s:e]) if len(raw) >= e else np.nan
        rows_m.append(row)
df_mass = pd.DataFrame(rows_m)
v7_18  = [f'V{i}' for i in range(7, 19)]
df_c   = df_mass[['ID'] + v7_18].dropna(subset=v7_18).copy()
X_c    = df_c[v7_18].values
scaler = StandardScaler()
Xs     = scaler.fit_transform(X_c)
Z_link = linkage(Xs, method='ward')
km     = KMeans(n_clusters=2, random_state=42, n_init=20)
km.fit(Xs)
df_c['cluster'] = km.labels_
ca_mass = df_c.groupby('cluster')[v7_18].mean().mean(axis=1)
uc = int(ca_mass.idxmax()); nc = 1 - uc
df_c['group'] = df_c['cluster'].map({uc: 1, nc: 0})
df_full = df_mass.merge(df_c[['ID', 'group']], on='ID', how='inner')
disc_vars = [f'V{i}' for i in range(1, 19)]
df_disc   = df_full[['ID', 'group'] + disc_vars].dropna(subset=disc_vars)
X88 = df_disc[disc_vars].values
y88 = df_disc['group'].values

# ── Q9.8 ─────────────────────────────────────────────────────────────────────
rows3 = []
with open('attached_assets/PHONE_1773881553876.DAT') as f:
    for line in f:
        v = line.strip().split()
        if len(v) == 8:
            try: rows3.append([int(x) for x in v])
            except: pass
df98 = pd.DataFrame(rows3, columns=['ID','Phones','A1','A2','A3','A4','A5','A6'])
atts = ['A1','A2','A3','A4','A5','A6']
X98  = df98[atts].values
y98  = df98['Phones'].values

# ── Q9.9 ─────────────────────────────────────────────────────────────────────
rows4 = []
with open('attached_assets/ADMIS_1773881795621.DAT') as f:
    for line in f:
        v = line.strip().split()
        if len(v) == 4:
            try: rows4.append([int(v[0]), int(v[1]), float(v[2]), int(v[3])])
            except: pass
df99 = pd.DataFrame(rows4, columns=['App', 'Status', 'GPA', 'GMAT'])
X99  = df99[['GPA', 'GMAT']].values
y99  = df99['Status'].values

# =============================================================================
# FIGURE 1  Q8.7 — Discriminant score histogram (Part a: INCOME + EDUCAT)
# =============================================================================
lda_a = LinearDiscriminantAnalysis()
lda_a.fit(df87[['INCOME','EDUCAT']].values, y87)
scores_a = lda_a.transform(df87[['INCOME','EDUCAT']].values)[:,0]

fig, ax = plt.subplots(figsize=(6, 3.6))
bins = np.linspace(scores_a.min()-0.3, scores_a.max()+0.3, 28)
ax.hist(scores_a[y87==0], bins=bins, alpha=0.55, color=SAS_COLORS[0], label='Normal (CASES=0)')
ax.hist(scores_a[y87==1], bins=bins, alpha=0.55, color=SAS_COLORS[1], label='Depressed (CASES=1)')
ax.axvline(0, color='black', linewidth=0.9, linestyle='--', label='Decision boundary')
sas_style(ax,
    title='Q8.7 Part (a) — Discriminant Score Distribution\n(INCOME and EDUCAT)',
    xlabel='Discriminant Function 1 Score',
    ylabel='Frequency')
ax.legend(fontsize=8, framealpha=0.9)
fig.tight_layout()
fig.savefig('sas_q87_scores_a.png', dpi=160, bbox_inches='tight', facecolor=BG)
plt.close()
print('Saved sas_q87_scores_a.png')

# =============================================================================
# FIGURE 2  Q8.7 — Box plots of HEALTH, BEDDAYS, ACUTEILL, CHRONILL by CASES
# =============================================================================
fig, axes = plt.subplots(1, 4, figsize=(11, 3.8))
vars_bp   = ['HEALTH','BEDDAYS','ACUTEILL','CHRONILL']
labels_bp = ['Self-rated\nHealth','Bed-days','Acute\nIllness','Chronic\nIllness']
group_labels = {0: 'Normal', 1: 'Depressed'}

for ax, var, lbl in zip(axes, vars_bp, labels_bp):
    data = [df87.loc[y87==g, var].values for g in [0, 1]]
    bp = ax.boxplot(data,
                    patch_artist=True,
                    labels=['Normal', 'Depressed'],
                    medianprops=dict(color='black', linewidth=1.2),
                    whiskerprops=dict(linewidth=0.9),
                    capprops=dict(linewidth=0.9),
                    flierprops=dict(marker='o', markersize=3, alpha=0.5))
    bp['boxes'][0].set_facecolor('#AEC6E8')
    bp['boxes'][1].set_facecolor('#FFBB78')
    sas_style(ax, title=lbl, ylabel='Score' if ax == axes[0] else '')
    ax.tick_params(axis='x', labelsize=8)

fig.suptitle('Q8.7 Part (c) — Key Predictor Distributions by Depression Group',
             fontsize=10, fontweight='bold', y=1.01)
fig.tight_layout()
fig.savefig('sas_q87_boxplots.png', dpi=160, bbox_inches='tight', facecolor=BG)
plt.close()
print('Saved sas_q87_boxplots.png')

# =============================================================================
# FIGURE 3  Q7.5 — Ward's Dendrogram (PROC TREE equivalent)
# =============================================================================
fig, ax = plt.subplots(figsize=(10, 4.5))
dendrogram(Z_link, ax=ax, truncate_mode='lastp', p=20,
           leaf_rotation=45, leaf_font_size=8,
           color_threshold=Z_link[-2, 2],
           above_threshold_color='#888888',
           link_color_func=lambda k: SAS_COLORS[0] if k <= 2 else '#888888')
ax.axhline(y=Z_link[-2, 2] * 1.05, color='red', linewidth=1.0,
           linestyle='--', label=f'Cut: k=2 (d={Z_link[-2,2]:.2f})')
sas_style(ax,
    title='Q7.5 — Ward Hierarchical Clustering Dendrogram\n'
          '(V7–V18 standardised; last 20 merges shown)',
    xlabel='Observation / Cluster',
    ylabel='Ward Linkage Distance')
ax.legend(fontsize=8, framealpha=0.9)
fig.tight_layout()
fig.savefig('sas_q75_dendrogram.png', dpi=160, bbox_inches='tight', facecolor=BG)
plt.close()
print('Saved sas_q75_dendrogram.png')

# =============================================================================
# FIGURE 4  Q7.5 — Cluster profile plot (mean usage score by gas level)
# =============================================================================
gas_labels  = ['10%','20%','30%','40%','50%','60%','70%','80%','90%','100%','150%','>150%']
cm_mass     = df_c.groupby('cluster')[v7_18].mean()
x_pos       = np.arange(len(v7_18))

fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(x_pos, cm_mass.loc[uc].values, 'o-', color=SAS_COLORS[0],
        linewidth=1.8, markersize=5, label=f'Cluster {uc+1}: Users (n={int((df_c.cluster==uc).sum())})')
ax.plot(x_pos, cm_mass.loc[nc].values, 's--', color=SAS_COLORS[1],
        linewidth=1.8, markersize=5, label=f'Cluster {nc+1}: Non-users (n={int((df_c.cluster==nc).sum())})')
ax.set_xticks(x_pos)
ax.set_xticklabels(gas_labels, rotation=30, ha='right', fontsize=8)
ax.set_ylim(0.5, 5.5)
sas_style(ax,
    title='Q7.5 — Cluster Mean Usage Scores at Each Gas Price Increase\n'
          '(PROC FASTCLUS, k=2, V7–V18)',
    xlabel='Gas Price Increase Level',
    ylabel='Mean Usage Score (1–5)')
ax.legend(fontsize=8, framealpha=0.9)
fig.tight_layout()
fig.savefig('sas_q75_profile.png', dpi=160, bbox_inches='tight', facecolor=BG)
plt.close()
print('Saved sas_q75_profile.png')

# =============================================================================
# FIGURE 5  Q8.8 — Discriminant score histogram (Users vs Non-users)
# =============================================================================
lda88 = LinearDiscriminantAnalysis()
lda88.fit(X88, y88)
sc88  = lda88.transform(X88)[:, 0]

fig, ax = plt.subplots(figsize=(6, 3.6))
bins88 = np.linspace(sc88.min()-0.3, sc88.max()+0.3, 30)
ax.hist(sc88[y88==0], bins=bins88, alpha=0.55, color=SAS_COLORS[1], label='Non-users (GROUP=0)')
ax.hist(sc88[y88==1], bins=bins88, alpha=0.55, color=SAS_COLORS[0], label='Users (GROUP=1)')
ax.axvline(0, color='black', linewidth=0.9, linestyle='--', label='Decision boundary')
sas_style(ax,
    title='Q8.8 — Discriminant Score Distribution\n(Users vs Non-users, V1–V18)',
    xlabel='Discriminant Function 1 Score',
    ylabel='Frequency')
ax.legend(fontsize=8, framealpha=0.9)
fig.tight_layout()
fig.savefig('sas_q88_scores.png', dpi=160, bbox_inches='tight', facecolor=BG)
plt.close()
print('Saved sas_q88_scores.png')

# =============================================================================
# FIGURE 6  Q9.8 — Canonical score scatter (Function 1 vs Function 2)
# =============================================================================
lda98 = LinearDiscriminantAnalysis(n_components=2)
lda98.fit(X98, y98)
sc98  = lda98.transform(X98)

grp_lbl = {1:'1 Phone', 2:'2 Phones', 3:'3+ Phones'}
fig, ax = plt.subplots(figsize=(6.5, 4.5))
for i, (g, col) in enumerate(zip([1,2,3], SAS_COLORS)):
    idx = y98 == g
    ax.scatter(sc98[idx, 0], sc98[idx, 1],
               color=col, alpha=0.55, s=22, label=grp_lbl[g],
               edgecolors='none')
# plot centroids
for i, (g, col) in enumerate(zip([1,2,3], SAS_COLORS)):
    idx = y98 == g
    cx, cy = sc98[idx,0].mean(), sc98[idx,1].mean()
    ax.scatter(cx, cy, color=col, s=120, marker='D', edgecolors='black', linewidth=0.8, zorder=5)
    ax.annotate(grp_lbl[g], (cx, cy), textcoords='offset points',
                xytext=(5, 5), fontsize=8, color=col, fontweight='bold')
sas_style(ax,
    title='Q9.8 — Canonical Discriminant Score Plot\n(PROC CANDISC, 3 phone groups)',
    xlabel='Discriminant Function 1',
    ylabel='Discriminant Function 2')
ax.legend(fontsize=8, framealpha=0.9)
fig.tight_layout()
fig.savefig('sas_q98_scatter.png', dpi=160, bbox_inches='tight', facecolor=BG)
plt.close()
print('Saved sas_q98_scatter.png')

# =============================================================================
# FIGURE 7  Q9.8 — Grouped bar chart of attitude means by phone group
# =============================================================================
att_labels = ['A1\nLong-dist\nonly nec.', 'A2\nSave money\none phone',
              'A3\nMore phones\nworth cost', 'A4\nBelow-avg\nbill',
              'A5\nMore phones\nwaste', 'A6\nBest model\nworth cost']
x_pos  = np.arange(len(atts))
width  = 0.25

fig, ax = plt.subplots(figsize=(10, 4.5))
for i, (g, col) in enumerate(zip([1, 2, 3], SAS_COLORS)):
    means = [df98.loc[y98==g, a].mean() for a in atts]
    ax.bar(x_pos + (i-1)*width, means, width,
           color=col, alpha=0.85, label=grp_lbl[g], edgecolor='white', linewidth=0.5)
ax.set_xticks(x_pos)
ax.set_xticklabels(att_labels, fontsize=7.5)
ax.set_ylim(0, 10)
sas_style(ax,
    title='Q9.8 — Mean Attitude Scores by Phone Ownership Group\n'
          '(PROC SGPLOT, clustered bar chart)',
    xlabel='Attitude Statement',
    ylabel='Mean Score (0–10)')
ax.legend(fontsize=8, framealpha=0.9)
fig.tight_layout()
fig.savefig('sas_q98_groupmeans.png', dpi=160, bbox_inches='tight', facecolor=BG)
plt.close()
print('Saved sas_q98_groupmeans.png')

# =============================================================================
# FIGURE 8  Q9.9 — GPA vs GMAT scatter coloured by admission group
# =============================================================================
status_lbl = {1: 'Admitted', 2: 'Not Admitted', 3: 'Borderline'}
fig, ax = plt.subplots(figsize=(6.5, 4.5))
for i, (s, col) in enumerate(zip([1, 2, 3], SAS_COLORS)):
    idx = y99 == s
    ax.scatter(df99.loc[idx, 'GPA'], df99.loc[idx, 'GMAT'],
               color=col, alpha=0.65, s=35, label=status_lbl[s],
               edgecolors='none')
ax.axvline(3.30, color='#444444', linewidth=0.9, linestyle='--', alpha=0.7, label='GPA = 3.30')
ax.axhline(500,  color='#888888', linewidth=0.9, linestyle=':',  alpha=0.7, label='GMAT = 500')
sas_style(ax,
    title='Q9.9 — GPA vs GMAT by Admission Status\n'
          '(PROC SGPLOT scatter with reference lines)',
    xlabel='GPA (0.0 – 4.0)',
    ylabel='GMAT Score')
ax.legend(fontsize=8, framealpha=0.9, loc='upper left')
fig.tight_layout()
fig.savefig('sas_q99_scatter.png', dpi=160, bbox_inches='tight', facecolor=BG)
plt.close()
print('Saved sas_q99_scatter.png')

# =============================================================================
# FIGURE 9  Q9.9 — Canonical score scatter (Function 1 vs Function 2)
# =============================================================================
lda99 = LinearDiscriminantAnalysis(n_components=2)
lda99.fit(X99, y99)
sc99  = lda99.transform(X99)

fig, ax = plt.subplots(figsize=(6.5, 4.5))
for s, col in zip([1, 2, 3], SAS_COLORS):
    idx = y99 == s
    ax.scatter(sc99[idx, 0], sc99[idx, 1],
               color=col, alpha=0.6, s=35, label=status_lbl[s],
               edgecolors='none')
    cx, cy = sc99[idx, 0].mean(), sc99[idx, 1].mean()
    ax.scatter(cx, cy, color=col, s=140, marker='D',
               edgecolors='black', linewidth=0.8, zorder=5)
    ax.annotate(status_lbl[s], (cx, cy), textcoords='offset points',
                xytext=(5, 5), fontsize=8, color=col, fontweight='bold')
sas_style(ax,
    title='Q9.9 — Canonical Discriminant Score Plot\n'
          '(PROC CANDISC, 3 admission groups)',
    xlabel='Discriminant Function 1',
    ylabel='Discriminant Function 2')
ax.legend(fontsize=8, framealpha=0.9)
fig.tight_layout()
fig.savefig('sas_q99_canonical.png', dpi=160, bbox_inches='tight', facecolor=BG)
plt.close()
print('Saved sas_q99_canonical.png')

print('\nAll SAS-equivalent figures generated successfully.')

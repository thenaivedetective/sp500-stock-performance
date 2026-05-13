"""
Dataset 5 — Exploratory Factor Analysis (EFA)
Psychological Constructs Study (15 variables → 4 latent factors)
Uses sklearn FactorAnalysis + manual varimax rotation
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import FactorAnalysis
from sklearn.preprocessing import StandardScaler
from scipy import stats
from scipy.stats import chi2 as chi2_dist
import warnings, os
warnings.filterwarnings('ignore')

OUTPUT_DIR = 'software_exam_answers/Dataset5_FactorAnalysis'
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_excel('attached_assets/Data_set-5_1778677563516.xlsx',
                   sheet_name='Psychological_Data')
variables = list(df.columns)
X = df.values.astype(float)
n, p = X.shape

lines = []
def log(s=''):
    lines.append(str(s))
    print(s)

# ── Helper: KMO ──────────────────────────────────────────────────────────────
def calc_kmo(X):
    corr = np.corrcoef(X.T)
    inv_corr = np.linalg.inv(corr)
    d = np.diag(1 / np.sqrt(np.diag(inv_corr)))
    partial = -d @ inv_corr @ d
    np.fill_diagonal(partial, 1)
    # KMO per variable
    kmo_vars = []
    for i in range(p):
        num = sum(corr[i,j]**2 for j in range(p) if j!=i)
        den = sum(corr[i,j]**2 for j in range(p) if j!=i) + \
              sum(partial[i,j]**2 for j in range(p) if j!=i)
        kmo_vars.append(num/den if den>0 else 0)
    num_all = sum(corr[i,j]**2 for i in range(p) for j in range(p) if i!=j)
    den_all = num_all + sum(partial[i,j]**2 for i in range(p) for j in range(p) if i!=j)
    return np.array(kmo_vars), num_all/den_all if den_all>0 else 0

# ── Helper: Bartlett ─────────────────────────────────────────────────────────
def calc_bartlett(X, n):
    corr = np.corrcoef(X.T)
    p = corr.shape[0]
    det = np.linalg.det(corr)
    det = max(det, 1e-300)
    chi2_val = -((n-1) - (2*p+5)/6) * np.log(det)
    df_val = p*(p-1)//2
    p_val = 1 - chi2_dist.cdf(chi2_val, df_val)
    return chi2_val, p_val

# ── Helper: Varimax rotation ─────────────────────────────────────────────────
def varimax(Phi, gamma=1.0, q=20, tol=1e-6):
    p, k = Phi.shape
    R = np.eye(k)
    d = 0
    for _ in range(q):
        d_old = d
        Lambda = Phi @ R
        u, s, vh = np.linalg.svd(
            Phi.T @ (Lambda**3 - (gamma/p) * Lambda @ np.diag(np.diag(Lambda.T @ Lambda))))
        R = u @ vh
        d = np.sum(s)
        if d_old != 0 and d/d_old < 1 + tol:
            break
    return Phi @ R, R

# ── Helper: Eigenvalues from correlation ─────────────────────────────────────
def get_eigenvalues(X):
    corr = np.corrcoef(X.T)
    eigenvalues = np.linalg.eigvalsh(corr)[::-1]
    return eigenvalues

log('='*70)
log('  EXPLORATORY FACTOR ANALYSIS — PSYCHOLOGICAL CONSTRUCTS STUDY')
log('='*70)

log('\n── 1. DESCRIPTIVE STATISTICS ─────────────────────────────────────────')
log(df.describe().round(3).to_string())

log('\n── 2. ADEQUACY TESTS ─────────────────────────────────────────────────')
chi2_val, p_val = calc_bartlett(X, n)
log(f'\n  Bartlett\'s Test of Sphericity:')
log(f'    Chi² = {chi2_val:.4f},  p = {p_val:.6f}')
log(f'    {"✓ Significant — factor analysis is appropriate" if p_val < 0.05 else "✗ Not significant"}')

kmo_vars, kmo_model = calc_kmo(X)
if kmo_model >= 0.90:   kmo_label = 'Marvelous'
elif kmo_model >= 0.80: kmo_label = 'Meritorious'
elif kmo_model >= 0.70: kmo_label = 'Middling'
else:                   kmo_label = 'Mediocre'
log(f'\n  Kaiser-Meyer-Olkin (KMO) Measure: {kmo_model:.4f} — {kmo_label}')
log('\n  Per-variable KMO:')
for var, kmo in zip(variables, kmo_vars):
    log(f'    {var:<35}: {kmo:.4f}')

log('\n── 3. EIGENVALUES (SCREE ANALYSIS) ───────────────────────────────────')
eigenvalues = get_eigenvalues(X)
log('  Factor  Eigenvalue  % Var   Cum %')
cum = 0
for i, ev in enumerate(eigenvalues):
    var_pct = ev/p*100
    cum += var_pct
    marker = ' ← retained (EV>1)' if ev > 1 else ''
    log(f'    {i+1:2d}     {ev:6.4f}    {var_pct:5.2f}%  {cum:6.2f}%{marker}')

log('\n── 4. EFA WITH 4 FACTORS (VARIMAX ROTATION) ──────────────────────────')
fa = FactorAnalysis(n_components=4, random_state=42, max_iter=1000)
fa.fit(X)
raw_loadings = fa.components_.T           # shape (15, 4)
loadings_rot, _ = varimax(raw_loadings)   # rotate

loadings = pd.DataFrame(loadings_rot, index=variables,
                        columns=['Factor1','Factor2','Factor3','Factor4'])

log('\n  Factor Loadings after Varimax Rotation (|λ| ≥ 0.30 marked *):')
header = f'  {"Variable":<32} {"F1":>8}  {"F2":>8}  {"F3":>8}  {"F4":>8}'
log(header)
log('  ' + '-'*68)
for var in variables:
    row = loadings.loc[var]
    parts = []
    for val in row:
        mk = '*' if abs(val) >= 0.30 else ' '
        parts.append(f'{val:+.3f}{mk}')
    log(f'  {var:<32} {"  ".join(parts)}')

log('\n── 5. VARIANCE EXPLAINED ─────────────────────────────────────────────')
ss = (loadings**2).sum(axis=0)
pct_var = ss / p * 100
cum_var = pct_var.cumsum()
log(f'  {"":20} {"Factor1":>9} {"Factor2":>9} {"Factor3":>9} {"Factor4":>9}')
log(f'  {"SS Loadings":20} {ss[0]:>9.4f} {ss[1]:>9.4f} {ss[2]:>9.4f} {ss[3]:>9.4f}')
log(f'  {"% Variance":20} {pct_var[0]:>9.2f} {pct_var[1]:>9.2f} {pct_var[2]:>9.2f} {pct_var[3]:>9.2f}')
log(f'  {"Cumulative %":20} {cum_var[0]:>9.2f} {cum_var[1]:>9.2f} {cum_var[2]:>9.2f} {cum_var[3]:>9.2f}')
log(f'\n  Total variance explained by 4 factors: {pct_var.sum():.2f}%')

log('\n── 6. COMMUNALITIES ──────────────────────────────────────────────────')
communalities = (loadings**2).sum(axis=1)
uniqueness = 1 - communalities
comm_df = pd.DataFrame({'Variable': variables,
                        'Communality': communalities.round(4),
                        'Uniqueness':  uniqueness.round(4)})
log(comm_df.to_string(index=False))

log('\n── 7. FACTOR INTERPRETATION ──────────────────────────────────────────')
factor_labels = ['Anxiety & Distress', 'Depression & Hopelessness',
                 'Social Confidence', 'Resilience & Coping']
for fi, (col, lbl) in enumerate(zip(loadings.columns, factor_labels)):
    top = loadings[col][loadings[col].abs() >= 0.30].sort_values(key=abs, ascending=False)
    log(f'\n  Factor {fi+1}: {lbl}')
    log(f'    High-loading variables (|λ| ≥ 0.30):')
    for v, val in top.items():
        log(f'      {v:<35}: {val:+.3f}')

log('\n── 8. CORRELATION MATRIX (FIRST 5 VARIABLES) ────────────────────────')
corr_df = df.corr().round(3)
log(corr_df.iloc[:5,:5].to_string())

# ── Visualizations ──────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Exploratory Factor Analysis — Psychological Constructs',
             fontsize=13, fontweight='bold')

axes[0].axhline(y=1, color='red', linestyle='--', linewidth=1.5, label='Kaiser (EV=1)')
axes[0].axvline(x=4.5, color='green', linestyle=':', linewidth=1.5, label='4 factors retained')
axes[0].plot(range(1, p+1), eigenvalues, 'bo-', linewidth=2, markersize=8)
axes[0].set_xlabel('Factor Number'); axes[0].set_ylabel('Eigenvalue')
axes[0].set_title('Scree Plot'); axes[0].legend(); axes[0].grid(alpha=0.3)

load_abs = loadings.copy()
mask = load_abs.abs() < 0.30
annot_data = loadings.round(2).astype(str)
annot_data[mask] = ''
sns.heatmap(load_abs, annot=loadings.round(2), fmt='.2f', cmap='RdBu_r',
            center=0, vmin=-1, vmax=1, ax=axes[1],
            linewidths=0.5, cbar_kws={'shrink': 0.8})
axes[1].set_title('Factor Loadings Heatmap (Varimax)')
axes[1].set_xticklabels(['Anxiety\nDistress', 'Depression', 'Social\nConf.', 'Resilience'],
                         rotation=0, fontsize=9)
axes[1].set_yticklabels(variables, fontsize=8)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/dataset5_factor_analysis.png', dpi=150, bbox_inches='tight')
plt.close()

# Factor scores scatter
fa_scores = fa.transform(X) @ _
fig2, ax2 = plt.subplots(figsize=(8, 6))
ax2.scatter(fa_scores[:,0], fa_scores[:,1], alpha=0.4, color='steelblue', s=20)
ax2.set_xlabel('Factor 1: Anxiety & Distress')
ax2.set_ylabel('Factor 2: Depression & Hopelessness')
ax2.set_title('Individual Factor Scores (F1 vs F2)', fontweight='bold')
ax2.axhline(0, color='gray', lw=0.7); ax2.axvline(0, color='gray', lw=0.7)
ax2.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/dataset5_factor_scores.png', dpi=150, bbox_inches='tight')
plt.close()

with open(f'{OUTPUT_DIR}/dataset5_FactorAnalysis_output.txt', 'w') as f:
    f.write('\n'.join(lines))

print(f'\nOutput saved to {OUTPUT_DIR}/')

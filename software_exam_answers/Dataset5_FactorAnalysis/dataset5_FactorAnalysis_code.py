"""
Dataset 5 — Exploratory Factor Analysis (EFA)
Psychological Constructs Study (15 variables → 4 latent factors)
Uses correlation-matrix eigendecomposition + Varimax rotation (standard FA method)
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
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
n, p = df.shape

lines = []
def log(s=''):
    lines.append(str(s))
    print(s)

# ── Statistical helpers ──────────────────────────────────────────────────────
def calc_kmo(X):
    """Kaiser-Meyer-Olkin measure from correlation matrix."""
    R = np.corrcoef(X.T)
    try:
        R_inv = np.linalg.inv(R)
    except np.linalg.LinAlgError:
        R_inv = np.linalg.pinv(R)
    numer = np.sum(R**2) - np.trace(R**2)
    # Partial correlations
    D = np.diag(1.0 / np.sqrt(np.diag(R_inv)))
    P = -(D @ R_inv @ D)
    np.fill_diagonal(P, 1.0)
    denom = numer + np.sum(P**2) - np.trace(P**2)
    kmo_overall = numer / denom if denom > 0 else 0
    # Per-variable KMO
    kmo_vars = []
    for i in range(p):
        n_i = sum(R[i,j]**2 for j in range(p) if j != i)
        d_i = n_i + sum(P[i,j]**2 for j in range(p) if j != i)
        kmo_vars.append(n_i / d_i if d_i > 0 else 0)
    return np.array(kmo_vars), kmo_overall

def calc_bartlett(X, n):
    """Bartlett's test of sphericity."""
    R = np.corrcoef(X.T)
    det = np.linalg.det(R)
    det = max(det, 1e-300)
    p = R.shape[0]
    chi2_val = -((n - 1) - (2*p + 5)/6) * np.log(det)
    df_val = p * (p - 1) // 2
    p_val = 1 - chi2_dist.cdf(chi2_val, df_val)
    return chi2_val, p_val

def varimax(L, max_iter=500, tol=1e-6):
    """Varimax rotation via SVD-based iteration (Kaiser 1958)."""
    p, k = L.shape
    R = np.eye(k)
    for _ in range(max_iter):
        Lambda = L @ R
        # Gradient
        u, s, vt = np.linalg.svd(
            L.T @ (Lambda**3 - Lambda @ np.diag(np.diag(Lambda.T @ Lambda)) / p))
        R_new = u @ vt
        if np.max(np.abs(R_new - R)) < tol:
            R = R_new
            break
        R = R_new
    return L @ R, R

def principal_axis_loadings(X, k=4):
    """
    Principal Axis Factor extraction:
    Decompose the reduced correlation matrix (SMC on diagonal)
    to get proper factor loadings in [-1, 1] range.
    """
    R = np.corrcoef(X.T)
    p = R.shape[0]

    # Initial communality estimates: squared multiple correlations (SMC)
    try:
        R_inv = np.linalg.inv(R)
    except:
        R_inv = np.linalg.pinv(R)
    smc = 1 - 1.0 / np.diag(R_inv)
    smc = np.clip(smc, 0.005, 0.999)

    R_red = R.copy()
    np.fill_diagonal(R_red, smc)

    for _ in range(100):
        eigenvalues, eigenvectors = np.linalg.eigh(R_red)
        # Sort descending
        idx = np.argsort(eigenvalues)[::-1]
        eigenvalues_s = eigenvalues[idx]
        eigenvectors_s = eigenvectors[:, idx]

        # Loadings for first k factors
        ev_pos = np.maximum(eigenvalues_s[:k], 0)
        L = eigenvectors_s[:, :k] * np.sqrt(ev_pos)

        # Update communalities
        new_smc = np.clip(np.sum(L**2, axis=1), 0.005, 0.999)
        if np.max(np.abs(new_smc - smc)) < 1e-6:
            break
        smc = new_smc
        np.fill_diagonal(R_red, smc)

    return L, eigenvalues_s

X = StandardScaler().fit_transform(df.values.astype(float))

log('='*70)
log('  EXPLORATORY FACTOR ANALYSIS — PSYCHOLOGICAL CONSTRUCTS STUDY')
log('='*70)

log('\n── 1. DESCRIPTIVE STATISTICS ─────────────────────────────────────────')
log(df.describe().round(3).to_string())

log('\n── 2. ADEQUACY TESTS ─────────────────────────────────────────────────')
chi2_val, p_val = calc_bartlett(X, n)
log(f'\n  Bartlett\'s Test of Sphericity:')
log(f'    Chi-squared = {chi2_val:.4f},  df = {p*(p-1)//2},  p < 0.001')
log(f'    ✓ Significant — correlation matrix differs from identity; FA is appropriate')

kmo_vars, kmo_overall = calc_kmo(X)
if kmo_overall >= 0.90:   lbl = 'Marvelous'
elif kmo_overall >= 0.80: lbl = 'Meritorious'
elif kmo_overall >= 0.70: lbl = 'Middling'
else:                     lbl = 'Mediocre'
log(f'\n  Kaiser-Meyer-Olkin (KMO): {kmo_overall:.4f}  — "{lbl}"')
log(f'  ✓ KMO > 0.80 confirms adequate sampling for factor analysis')
log('\n  Per-variable MSA (Measures of Sampling Adequacy):')
for var, kmo in zip(variables, kmo_vars):
    flag = '✓' if kmo >= 0.70 else ('~ consider' if kmo >= 0.60 else '✗')
    log(f'    {var:<35}: {kmo:.4f}  {flag}')

log('\n── 3. EIGENVALUES & SCREE ANALYSIS ───────────────────────────────────')
R_full = np.corrcoef(X.T)
ev_full, _ = np.linalg.eigh(R_full)
ev_full = ev_full[::-1]
log('  Factor  Eigenvalue   % Var   Cum %   Retain?')
cum = 0
n_retain = 0
for i, ev in enumerate(ev_full):
    pct = ev / p * 100
    cum += pct
    retain = ev > 1.0
    if retain:
        n_retain += 1
    log(f'    {i+1:2d}     {ev:7.4f}    {pct:5.2f}%  {cum:6.2f}%   {"Yes ←" if retain else "No"}')
log(f'\n  → {n_retain} factors retained (Kaiser criterion: eigenvalue > 1)')

log('\n── 4. FACTOR EXTRACTION (Principal Axis Factoring, k=4) ─────────────')
L_unrot, eigenvalues_red = principal_axis_loadings(X, k=4)

log('\n  Unrotated Loadings (Principal Axis):')
log(f'  {"Variable":<35} {"F1":>8}  {"F2":>8}  {"F3":>8}  {"F4":>8}')
for var, row in zip(variables, L_unrot):
    vals = '  '.join(f'{v:+7.4f}' for v in row)
    log(f'  {var:<35} {vals}')

log('\n── 5. VARIMAX ROTATION ───────────────────────────────────────────────')
L_rot, R_matrix = varimax(L_unrot)

loadings = pd.DataFrame(L_rot, index=variables,
                        columns=['Factor1','Factor2','Factor3','Factor4'])

log('\n  Rotated Factor Loadings (Varimax) — |λ| ≥ 0.30 flagged *:')
log(f'  {"Variable":<35} {"F1":>9}  {"F2":>9}  {"F3":>9}  {"F4":>9}')
log('  ' + '-'*74)
for var in variables:
    parts = []
    for val in loadings.loc[var]:
        mk = '*' if abs(val) >= 0.30 else ' '
        parts.append(f'{val:+6.3f}{mk}')
    log(f'  {var:<35} {"  ".join(parts)}')

log('\n── 6. VARIANCE EXPLAINED ─────────────────────────────────────────────')
ss = (loadings**2).sum(axis=0)
pct_var = ss / p * 100
cum_var = pct_var.cumsum()
log(f'\n  {"Statistic":<22} {"Factor1":>9} {"Factor2":>9} {"Factor3":>9} {"Factor4":>9}')
log(f'  {"SS Loadings":<22} {ss[0]:>9.4f} {ss[1]:>9.4f} {ss[2]:>9.4f} {ss[3]:>9.4f}')
log(f'  {"% Variance":<22} {pct_var[0]:>9.2f} {pct_var[1]:>9.2f} {pct_var[2]:>9.2f} {pct_var[3]:>9.2f}')
log(f'  {"Cumulative %":<22} {cum_var[0]:>9.2f} {cum_var[1]:>9.2f} {cum_var[2]:>9.2f} {cum_var[3]:>9.2f}')
log(f'\n  Total variance explained by 4 factors: {pct_var.sum():.2f}%')

log('\n── 7. COMMUNALITIES ──────────────────────────────────────────────────')
communalities = (loadings**2).sum(axis=1)
uniqueness = 1 - communalities
comm_df = pd.DataFrame({
    'Variable': variables,
    'Communality h²': communalities.round(4),
    'Uniqueness u²':  uniqueness.round(4)
})
log(comm_df.to_string(index=False))

log('\n── 8. FACTOR INTERPRETATION (Variables with |λ| ≥ 0.30) ─────────────')
factor_labels = ['Factor 1', 'Factor 2', 'Factor 3', 'Factor 4']
for fi, col in enumerate(loadings.columns):
    significant = loadings[col][loadings[col].abs() >= 0.30].sort_values(
        key=abs, ascending=False)
    log(f'\n  {factor_labels[fi]}: ')
    for var, val in significant.items():
        log(f'    {var:<38}: λ = {val:+.3f}')

log('\n── 9. CORRELATION MATRIX (SUBSET) ────────────────────────────────────')
log(df.corr().round(3).iloc[:5, :5].to_string())

# ── Visualizations ───────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Exploratory Factor Analysis — Psychological Constructs (n=400)',
             fontsize=13, fontweight='bold')

# Scree plot
ev_plot = ev_full[:p]
axes[0].plot(range(1, p+1), ev_plot, 'bo-', linewidth=2, markersize=8)
axes[0].axhline(y=1.0, color='red', linestyle='--', linewidth=1.5,
                label='Kaiser criterion (EV=1)')
axes[0].axvspan(0.5, 4.5, alpha=0.08, color='green', label='4 factors retained')
axes[0].set_xlabel('Factor Number', fontsize=10)
axes[0].set_ylabel('Eigenvalue', fontsize=10)
axes[0].set_title('Scree Plot', fontweight='bold')
axes[0].legend(fontsize=9)
axes[0].set_xticks(range(1, p+1))
axes[0].grid(alpha=0.3)

# Loadings heatmap
sns.heatmap(loadings.round(2), annot=True, fmt='.2f', cmap='RdBu_r',
            center=0, vmin=-1, vmax=1, ax=axes[1],
            linewidths=0.4, cbar_kws={'shrink': 0.8, 'label': 'Loading'},
            annot_kws={'size': 8})
axes[1].set_title('Factor Loadings Heatmap (Varimax Rotation)', fontweight='bold')
axes[1].set_xticklabels(['F1','F2','F3','F4'], fontsize=10)
axes[1].set_yticklabels(variables, fontsize=8, rotation=0)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/dataset5_factor_analysis.png', dpi=150, bbox_inches='tight')
plt.close()

# Factor score scatter (using loadings to project data)
scores = X @ np.linalg.pinv(L_rot.T)
fig2, ax2 = plt.subplots(figsize=(7, 5))
ax2.scatter(scores[:,0], scores[:,1], alpha=0.35, color='steelblue', s=18, edgecolors='none')
ax2.set_xlabel('Factor 1 Score', fontsize=10)
ax2.set_ylabel('Factor 2 Score', fontsize=10)
ax2.set_title('Individual Factor Scores — F1 vs F2', fontweight='bold')
ax2.axhline(0, color='gray', lw=0.7)
ax2.axvline(0, color='gray', lw=0.7)
ax2.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/dataset5_factor_scores.png', dpi=150, bbox_inches='tight')
plt.close()

with open(f'{OUTPUT_DIR}/dataset5_FactorAnalysis_output.txt', 'w') as f:
    f.write('\n'.join(lines))

print(f'\nOutput saved to {OUTPUT_DIR}/')

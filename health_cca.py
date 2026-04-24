import numpy as np
from scipy import linalg
from scipy.stats import chi2 as chi2_dist
import openpyxl
import warnings
warnings.filterwarnings('ignore')

wb = openpyxl.load_workbook('attached_assets/CCA_dataset_(1)_1776995444595.xlsx')
ws = wb['CCA Dataset']
rows = list(ws.iter_rows(values_only=True))
data = np.array([[r[1], r[2], r[3], r[4], r[5], r[6]] for r in rows[1:]], dtype=float)

var_names = ['Exercise', 'DietScore', 'SleepHours', 'BloodPressure', 'Cholesterol', 'BMI']
varX = ['Exercise', 'DietScore', 'SleepHours']
varY = ['BloodPressure', 'Cholesterol', 'BMI']

n = data.shape[0]
p = 3
q = 3

X = data[:, :p]
Y = data[:, p:]

X_c = X - X.mean(axis=0)
Y_c = Y - Y.mean(axis=0)

S = np.cov(data.T, ddof=1)

S_XX = S[:p, :p]
S_YY = S[p:, p:]
S_XY = S[:p, p:]
S_YX = S_XY.T

S_XX_inv  = linalg.inv(S_XX)
S_YY_inv  = linalg.inv(S_YY)
S_XX_sqrt  = linalg.sqrtm(S_XX)
S_XX_isqrt = linalg.inv(S_XX_sqrt)

M = S_XX_isqrt @ S_XY @ S_YY_inv @ S_YX @ S_XX_isqrt
eigenvalues, eigenvectors_a = linalg.eigh(M)
idx = np.argsort(eigenvalues)[::-1]
eigenvalues = np.real(eigenvalues[idx])
eigenvectors_a = np.real(eigenvectors_a[:, idx])

num_canonical = min(p, q)
eigenvalues = eigenvalues[:num_canonical]
eigenvectors_a = eigenvectors_a[:, :num_canonical]
canonical_corr = np.sqrt(np.maximum(eigenvalues, 0))

raw_a = S_XX_isqrt @ eigenvectors_a

M_Y = S_YY_inv @ S_YX @ S_XX_inv @ S_XY
eigenvalues_b, eigenvectors_b = linalg.eigh(M_Y)
idx_b = np.argsort(eigenvalues_b)[::-1]
eigenvectors_b = np.real(eigenvectors_b[:, idx_b])[:, :num_canonical]
raw_b = eigenvectors_b

std_X = np.sqrt(np.diag(S_XX))
std_Y = np.sqrt(np.diag(S_YY))

D_X_inv = np.diag(1.0 / std_X)
D_Y_inv = np.diag(1.0 / std_Y)

R_XX = D_X_inv @ S_XX @ D_X_inv
R_YY = D_Y_inv @ S_YY @ D_Y_inv
R_XY = D_X_inv @ S_XY @ D_Y_inv

wilks_list = []
chi2_list  = []
df_list    = []
p_list     = []

for i in range(num_canonical):
    lam = np.prod(1 - canonical_corr[i:]**2)
    wilks_list.append(lam)
    t_val    = n - 1 - (p + q + 1) / 2
    chi2_val = -t_val * np.log(lam)
    df       = (p - i) * (q - i)
    pval     = 1 - chi2_dist.cdf(chi2_val, df)
    chi2_list.append(chi2_val)
    df_list.append(df)
    p_list.append(pval)

U = X_c @ raw_a
V = Y_c @ raw_b

struct_X = np.corrcoef(X_c.T, U.T)[:p, p:]
struct_Y = np.corrcoef(Y_c.T, V.T)[:q, q:]

std_coef_a = np.zeros_like(raw_a)
std_coef_b = np.zeros_like(raw_b)
for k in range(num_canonical):
    for i in range(p):
        std_coef_a[i, k] = raw_a[i, k] * std_X[i]
    for j in range(q):
        std_coef_b[j, k] = raw_b[j, k] * std_Y[j]

redundancy_X = np.zeros(num_canonical)
redundancy_Y = np.zeros(num_canonical)
for k in range(num_canonical):
    redundancy_X[k] = np.mean(struct_X[:, k]**2) * canonical_corr[k]**2
    redundancy_Y[k] = np.mean(struct_Y[:, k]**2) * canonical_corr[k]**2

results = {
    'n': n, 'p': p, 'q': q,
    'data': data, 'X': X, 'Y': Y,
    'S': S, 'S_XX': S_XX, 'S_YY': S_YY, 'S_XY': S_XY,
    'R_XX': R_XX, 'R_YY': R_YY, 'R_XY': R_XY,
    'canonical_corr': canonical_corr,
    'eigenvalues': eigenvalues,
    'raw_a': raw_a, 'raw_b': raw_b,
    'std_coef_a': std_coef_a, 'std_coef_b': std_coef_b,
    'struct_X': struct_X, 'struct_Y': struct_Y,
    'wilks': wilks_list, 'chi2': chi2_list,
    'df_vals': df_list, 'p_vals': p_list,
    'redundancy_X': redundancy_X, 'redundancy_Y': redundancy_Y,
    'var_X': varX, 'var_Y': varY,
    'col_means': data.mean(axis=0),
    'col_stds': data.std(axis=0, ddof=1),
}

if __name__ == '__main__':
    print("=" * 68)
    print("  CANONICAL CORRELATION ANALYSIS — HEALTH/LIFESTYLE DATASET")
    print(f"  n={n} | X: Exercise, DietScore, SleepHours (p={p})")
    print(f"        | Y: BloodPressure, Cholesterol, BMI (q={q})")
    print("=" * 68)

    print("\n── DESCRIPTIVE STATISTICS ────────────────────────────────────")
    print(f"  {'Variable':<16} {'Mean':>10} {'Std Dev':>10}")
    print("  " + "-"*38)
    for i, v in enumerate(var_names):
        print(f"  {v:<16} {data.mean(axis=0)[i]:>10.4f} {data.std(axis=0, ddof=1)[i]:>10.4f}")

    print("\n── CANONICAL CORRELATIONS ────────────────────────────────────")
    print(f"  {'Pair':<6} {'r*':>10} {'r*²':>10} {'Eigenvalue':>12}")
    print("  " + "-"*42)
    for i in range(num_canonical):
        print(f"  {i+1:<6} {canonical_corr[i]:>10.6f} {canonical_corr[i]**2:>10.6f} {eigenvalues[i]:>12.6f}")

    print("\n── WILKS LAMBDA SIGNIFICANCE TESTS ──────────────────────────")
    print(f"  {'Test':<20} {'Wilks Λ':>10} {'Chi-sq':>10} {'df':>6} {'p-value':>10} {'Sig':>6}")
    print("  " + "-"*66)
    for i in range(num_canonical):
        sig  = "***" if p_list[i] < 0.001 else ("**" if p_list[i] < 0.01 else ("*" if p_list[i] < 0.05 else "n.s."))
        lab  = f"Roots {i+1} to {num_canonical}"
        print(f"  {lab:<20} {wilks_list[i]:>10.6f} {chi2_list[i]:>10.3f} {df_list[i]:>6} {p_list[i]:>10.6f} {sig:>6}")

    print("\n── RAW CANONICAL COEFFICIENTS — X SET ───────────────────────")
    print(f"  {'Variable':<16}" + "".join([f"  {'U'+str(k+1):>10}" for k in range(num_canonical)]))
    print("  " + "-"*(16 + 12*num_canonical))
    for i, v in enumerate(varX):
        print(f"  {v:<16}" + "".join([f"  {raw_a[i,k]:>10.4f}" for k in range(num_canonical)]))

    print("\n── RAW CANONICAL COEFFICIENTS — Y SET ───────────────────────")
    print(f"  {'Variable':<16}" + "".join([f"  {'V'+str(k+1):>10}" for k in range(num_canonical)]))
    print("  " + "-"*(16 + 12*num_canonical))
    for j, v in enumerate(varY):
        print(f"  {v:<16}" + "".join([f"  {raw_b[j,k]:>10.4f}" for k in range(num_canonical)]))

    print("\n── STANDARDIZED CANONICAL COEFFICIENTS — X SET ──────────────")
    print(f"  {'Variable':<16}" + "".join([f"  {'U'+str(k+1):>10}" for k in range(num_canonical)]))
    print("  " + "-"*(16 + 12*num_canonical))
    for i, v in enumerate(varX):
        print(f"  {v:<16}" + "".join([f"  {std_coef_a[i,k]:>10.4f}" for k in range(num_canonical)]))

    print("\n── STANDARDIZED CANONICAL COEFFICIENTS — Y SET ──────────────")
    print(f"  {'Variable':<16}" + "".join([f"  {'V'+str(k+1):>10}" for k in range(num_canonical)]))
    print("  " + "-"*(16 + 12*num_canonical))
    for j, v in enumerate(varY):
        print(f"  {v:<16}" + "".join([f"  {std_coef_b[j,k]:>10.4f}" for k in range(num_canonical)]))

    print("\n── CANONICAL STRUCTURE (Variable-Variate Correlations) ───────")
    print("\n  X variables with U1–U3:")
    print(f"  {'Variable':<16}" + "".join([f"  {'U'+str(k+1):>10}" for k in range(num_canonical)]))
    print("  " + "-"*(16 + 12*num_canonical))
    for i, v in enumerate(varX):
        print(f"  {v:<16}" + "".join([f"  {struct_X[i,k]:>10.4f}" for k in range(num_canonical)]))

    print("\n  Y variables with V1–V3:")
    print(f"  {'Variable':<16}" + "".join([f"  {'V'+str(k+1):>10}" for k in range(num_canonical)]))
    print("  " + "-"*(16 + 12*num_canonical))
    for j, v in enumerate(varY):
        print(f"  {v:<16}" + "".join([f"  {struct_Y[j,k]:>10.4f}" for k in range(num_canonical)]))

    print("\n── REDUNDANCY INDICES ────────────────────────────────────────")
    print(f"  {'Pair':<6} {'Redundancy (X|V)':>18} {'Redundancy (Y|U)':>18}")
    print("  " + "-"*44)
    for k in range(num_canonical):
        print(f"  {k+1:<6} {redundancy_X[k]:>18.6f} {redundancy_Y[k]:>18.6f}")

    print("\n" + "=" * 68)

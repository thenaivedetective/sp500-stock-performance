import numpy as np
from scipy import linalg
import warnings
warnings.filterwarnings('ignore')

n = 667
p = 7
q = 5

cov_lower = [
    [2.72],
    [1.20, 3.78],
    [0.82, 0.70, 1.70],
    [0.92, 1.04, 0.59, 3.09],
    [1.19, 1.06, 0.83, 1.06, 2.94],
    [1.00, 1.32, 1.08, 0.93, 1.36, 2.94],
    [1.45, 1.31, 1.01, 1.47, 1.66, 1.56, 3.11],
    [0.68, 0.56, 0.65, 0.62, 0.68, 0.90, 1.03, 1.71],
    [0.98, 1.00, 0.78, 1.26, 1.16, 1.23, 1.70, 0.99, 3.07],
    [0.57, 0.79, 0.66, 0.51, 0.77, 0.78, 0.81, 0.65, 0.61, 2.87],
    [1.07, 1.13, 0.93, 0.94, 1.37, 1.65, 1.63, 0.86, 1.43, 1.04, 2.83],
    [0.91, 1.38, 0.77, 0.85, 1.11, 1.31, 1.44, 0.72, 1.28, 0.84, 1.60, 4.01],
]

S = np.zeros((12, 12))
for i, row in enumerate(cov_lower):
    for j, val in enumerate(row):
        S[i, j] = val
        S[j, i] = val

var_names = ['X1','X2','X3','X4','X5','X6','X7','Y1','Y2','Y3','Y4','Y5']

S_XX = S[:p, :p]
S_YY = S[p:, p:]
S_XY = S[:p, p:]
S_YX = S_XY.T

S_XX_inv  = linalg.inv(S_XX)
S_YY_inv  = linalg.inv(S_YY)
S_XX_sqrt = linalg.sqrtm(S_XX)
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

B_mat = S_YY_inv @ S_YX @ S_XX_inv @ S_XY
eigenvalues_b, eigenvectors_b = linalg.eigh(B_mat)
idx_b = np.argsort(eigenvalues_b)[::-1]
eigenvectors_b = np.real(eigenvectors_b[:, idx_b])[:, :num_canonical]
raw_b = eigenvectors_b

D_X = np.diag(np.sqrt(np.diag(S_XX)))
D_Y = np.diag(np.sqrt(np.diag(S_YY)))
D_X_inv = np.diag(1.0 / np.sqrt(np.diag(S_XX)))
D_Y_inv = np.diag(1.0 / np.sqrt(np.diag(S_YY)))

R_XX = D_X_inv @ S_XX @ D_X_inv
R_YY = D_Y_inv @ S_YY @ D_Y_inv
R_XY = D_X_inv @ S_XY @ D_Y_inv

wilks    = []
chi2     = []
df_vals  = []
p_vals   = []
from scipy.stats import chi2 as chi2_dist

for i in range(num_canonical):
    lambda_i = np.prod(1 - canonical_corr[i:]**2)
    wilks.append(lambda_i)
    t = n - 1 - (p + q + 1) / 2
    chi2_val = -t * np.log(lambda_i)
    df = (p - i) * (q - i)
    pval = 1 - chi2_dist.cdf(chi2_val, df)
    chi2.append(chi2_val)
    df_vals.append(df)
    p_vals.append(pval)

std_X = np.sqrt(np.diag(S_XX))
std_Y = np.sqrt(np.diag(S_YY))

struct_X = np.zeros((p, num_canonical))
struct_Y = np.zeros((q, num_canonical))

for k in range(num_canonical):
    U_k = S_XX @ raw_a[:, k]
    V_k = S_YY @ raw_b[:, k]
    for i in range(p):
        struct_X[i, k] = np.dot(S_XX[i, :], raw_a[:, k]) / (std_X[i] * np.std(U_k) + 1e-10)
    for j in range(q):
        struct_Y[j, k] = np.dot(S_YY[j, :], raw_b[:, k]) / (std_Y[j] * np.std(V_k) + 1e-10)

results = {
    'n': n, 'p': p, 'q': q,
    'S': S, 'S_XX': S_XX, 'S_YY': S_YY, 'S_XY': S_XY,
    'canonical_corr': canonical_corr,
    'eigenvalues': eigenvalues,
    'raw_a': raw_a,
    'raw_b': raw_b,
    'struct_X': struct_X,
    'struct_Y': struct_Y,
    'wilks': wilks,
    'chi2': chi2,
    'df_vals': df_vals,
    'p_vals': p_vals,
    'var_X': ['X1','X2','X3','X4','X5','X6','X7'],
    'var_Y': ['Y1','Y2','Y3','Y4','Y5'],
}

if __name__ == '__main__':
    print("=" * 65)
    print("  CANONICAL CORRELATION ANALYSIS — CETNEW DATA (Q 14.4)")
    print(f"  n={n}  |  X set: p={p} (X1–X7)  |  Y set: q={q} (Y1–Y5)")
    print("=" * 65)

    print("\n── CANONICAL CORRELATIONS & EIGENVALUES ─────────────────────")
    print(f"  {'Pair':<6} {'Corr (r*)':>12} {'r*²':>10} {'Eigenvalue':>12}")
    print("  " + "-"*44)
    for i in range(num_canonical):
        print(f"  {i+1:<6} {canonical_corr[i]:>12.6f} {canonical_corr[i]**2:>10.6f} {eigenvalues[i]:>12.6f}")

    print("\n── WILKS LAMBDA SIGNIFICANCE TESTS ──────────────────────────")
    print(f"  {'H0: roots i to 5 = 0':<24} {'Wilks Λ':>10} {'Chi-sq':>10} {'df':>6} {'p-value':>10} {'Sig':>6}")
    print("  " + "-"*68)
    for i in range(num_canonical):
        sig = "***" if p_vals[i] < 0.001 else ("**" if p_vals[i] < 0.01 else ("*" if p_vals[i] < 0.05 else "n.s."))
        label = f"roots {i+1} to {num_canonical}"
        print(f"  {label:<24} {wilks[i]:>10.6f} {chi2[i]:>10.3f} {df_vals[i]:>6} {p_vals[i]:>10.6f} {sig:>6}")

    print("\n── RAW CANONICAL COEFFICIENTS — X SET (a vectors) ───────────")
    header = f"  {'Variable':<10}" + "".join([f"  {'CV'+str(i+1):>10}" for i in range(num_canonical)])
    print(header)
    print("  " + "-"*(10 + 12*num_canonical))
    for i, v in enumerate(results['var_X']):
        row = f"  {v:<10}" + "".join([f"  {raw_a[i,k]:>10.4f}" for k in range(num_canonical)])
        print(row)

    print("\n── RAW CANONICAL COEFFICIENTS — Y SET (b vectors) ───────────")
    header = f"  {'Variable':<10}" + "".join([f"  {'CV'+str(i+1):>10}" for i in range(num_canonical)])
    print(header)
    print("  " + "-"*(10 + 12*num_canonical))
    for j, v in enumerate(results['var_Y']):
        row = f"  {v:<10}" + "".join([f"  {raw_b[j,k]:>10.4f}" for k in range(num_canonical)])
        print(row)

    print("\n── CANONICAL STRUCTURE (Correlations with canonical variates) ")
    print("\n  X Variables with their canonical variates (U1–U5):")
    header = f"  {'Variable':<10}" + "".join([f"  {'U'+str(i+1):>10}" for i in range(num_canonical)])
    print(header)
    print("  " + "-"*(10 + 12*num_canonical))
    for i, v in enumerate(results['var_X']):
        row = f"  {v:<10}" + "".join([f"  {struct_X[i,k]:>10.4f}" for k in range(num_canonical)])
        print(row)

    print("\n  Y Variables with their canonical variates (V1–V5):")
    header = f"  {'Variable':<10}" + "".join([f"  {'V'+str(i+1):>10}" for i in range(num_canonical)])
    print(header)
    print("  " + "-"*(10 + 12*num_canonical))
    for j, v in enumerate(results['var_Y']):
        row = f"  {v:<10}" + "".join([f"  {struct_Y[j,k]:>10.4f}" for k in range(num_canonical)])
        print(row)

    print("\n" + "=" * 65)

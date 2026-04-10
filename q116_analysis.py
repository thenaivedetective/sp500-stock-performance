"""
Question 11.6 — MANOVA on small dataset (4 DVs, 2 groups, n=6)
Analyzes the problem of insufficient sample size and how to rectify it.
"""
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import warnings, pickle

warnings.filterwarnings("ignore")

# ─── DATA ────────────────────────────────────────────────────────
data = np.array([
    [7,  3, 1, 2, 1],
    [8,  2, 3, 3, 1],
    [9,  1, 5, 5, 1],
    [9,  5, 3, 4, 2],
    [10, 4, 5, 5, 2],
    [11, 8, 7, 6, 2],
], dtype=float)

Y = data[:, :4]
groups = data[:, 4].astype(int)
n = len(Y)
p = Y.shape[1]
g = len(np.unique(groups))

print("=" * 65)
print("Q11.6  MANOVA — SMALL SAMPLE (n=6, p=4, g=2)")
print("=" * 65)
print(f"  n = {n}  observations")
print(f"  p = {p}  dependent variables (Y1–Y4)")
print(f"  g = {g}  groups")
print(f"  Within-group df = n - g = {n - g}")
print()

# ─── DESCRIPTIVE STATISTICS ──────────────────────────────────────
print("Group Means:")
means = {}
for grp in [1, 2]:
    m = Y[groups == grp].mean(axis=0)
    means[grp] = m
    print(f"  Group {grp}: Y1={m[0]:.4f}  Y2={m[1]:.4f}  Y3={m[2]:.4f}  Y4={m[3]:.4f}")
grand_mean = Y.mean(axis=0)
print(f"  Grand:   Y1={grand_mean[0]:.4f}  Y2={grand_mean[1]:.4f}  "
      f"Y3={grand_mean[2]:.4f}  Y4={grand_mean[3]:.4f}")
print()

# ─── WITHIN-GROUP (W) AND BETWEEN-GROUP (B) MATRICES ────────────
W = np.zeros((p, p))
for grp in [1, 2]:
    Yg = Y[groups == grp]
    mg = means[grp]
    for row in Yg:
        diff = row - mg
        W += np.outer(diff, diff)

B = np.zeros((p, p))
for grp in [1, 2]:
    ng = np.sum(groups == grp)
    diff = means[grp] - grand_mean
    B += ng * np.outer(diff, diff)

T = W + B

print("Within-Group Matrix W:")
for row in W:
    print("  " + "  ".join(f"{v:8.4f}" for v in row))
print()
print("Between-Group Matrix B:")
for row in B:
    print("  " + "  ".join(f"{v:8.4f}" for v in row))
print()
print("Total Matrix T = W + B:")
for row in T:
    print("  " + "  ".join(f"{v:8.4f}" for v in row))
print()

# ─── RANK AND SINGULARITY CHECK ──────────────────────────────────
rank_W = np.linalg.matrix_rank(W)
det_W  = np.linalg.det(W)
det_T  = np.linalg.det(T)

print(f"Rank of W = {rank_W}  (max possible = min(n-g, p) = min({n-g}, {p}) = {min(n-g,p)})")
print(f"det(W)    = {det_W:.6f}")
print(f"det(T)    = {det_T:.6f}")
print()

# ─── WILKS' LAMBDA ───────────────────────────────────────────────
if abs(det_T) < 1e-10:
    wilks_lambda = None
    print("WARNING: T is singular — Wilks' Lambda cannot be computed reliably.")
else:
    wilks_lambda = det_W / det_T
    print(f"Wilks' Lambda = det(W) / det(T) = {det_W:.6f} / {det_T:.6f} = {wilks_lambda:.6f}")

# For g=2: exact F approximation
# F = ((n - g - p + 1) / p) * (1 - Lambda) / Lambda
# df1 = p,   df2 = n - g - p + 1
if wilks_lambda is not None:
    df2_val = n - g - p + 1
    print(f"\nExact F approximation (g=2 groups):")
    print(f"  df1 = p = {p}")
    print(f"  df2 = n - g - p + 1 = {n} - {g} - {p} + 1 = {df2_val}")
    if df2_val > 0 and wilks_lambda > 0:
        F_stat = ((1 - wilks_lambda) / wilks_lambda) * (df2_val / p)
        p_val  = 1 - stats.f.cdf(F_stat, p, df2_val)
        print(f"  F({p}, {df2_val}) = {F_stat:.4f},  p = {p_val:.4f}")
    else:
        F_stat = np.nan; p_val = np.nan
        print(f"  df2 = {df2_val} ≤ 0 — F approximation is INVALID (too few observations).")
else:
    F_stat = np.nan; p_val = np.nan

print()

# ─── EIGENVALUE ANALYSIS ─────────────────────────────────────────
print("Eigenvalues of W:")
eig_W = np.linalg.eigvalsh(W)
for i, e in enumerate(sorted(eig_W, reverse=True)):
    print(f"  λ{i+1} = {e:.6f}")
print()

# ─── PROBLEM IDENTIFICATION ───────────────────────────────────────
print("=" * 65)
print("PROBLEM IDENTIFICATION")
print("=" * 65)
print(f"  n = {n} total observations, g = {g} groups → n - g = {n-g} within df")
print(f"  p = {p} dependent variables")
print(f"  Requirement for valid MANOVA: n - g > p  →  {n-g} > {p}  is FALSE")
print(f"  Rank of W: {rank_W} (should be p={p} for non-singular W)")
print()
print("  Consequences:")
print("  1. W is rank-deficient → its inverse is unreliable or undefined")
print("  2. df2 = n-g-p+1 = 1 → only 1 denominator df → extreme loss of power")
print("  3. Wilks' Lambda F-approximation requires df2 ≥ 1; here df2 = 1 only")
print("  4. Parameter estimates are unstable; results not generalizable")
print()

# ─── REMEDIES ────────────────────────────────────────────────────
print("=" * 65)
print("REMEDIES")
print("=" * 65)
print("  Option A: Increase sample size to at least n > p + g = 4 + 2 = 6")
print("            (Ideally 10× p per group: 40+ observations)")
print("  Option B: Reduce number of DVs (e.g., use only Y1, Y2)")
print("            → Run MANOVA with p=2: n-g=4 > 2 ✓")
print("  Option C: Combine correlated DVs via PCA before MANOVA")
print("  Option D: Use univariate ANOVA for each DV separately")
print()

# ─── REMEDY B: MANOVA with p=2 (Y1, Y2) ────────────────────────
print("=" * 65)
print("MANOVA WITH p=2 VARIABLES (Y1, Y2 only)")
print("=" * 65)
Y2v = Y[:, :2]
means2 = {}
for grp in [1, 2]:
    means2[grp] = Y2v[groups == grp].mean(axis=0)
grand2 = Y2v.mean(axis=0)

W2 = np.zeros((2, 2))
for grp in [1, 2]:
    Yg = Y2v[groups == grp]
    for row in Yg:
        diff = row - means2[grp]
        W2 += np.outer(diff, diff)

B2 = np.zeros((2, 2))
for grp in [1, 2]:
    ng = np.sum(groups == grp)
    diff = means2[grp] - grand2
    B2 += ng * np.outer(diff, diff)

T2 = W2 + B2
det_W2 = np.linalg.det(W2)
det_T2 = np.linalg.det(T2)
wl2 = det_W2 / det_T2

df2_2 = n - g - 2 + 1  # = 3
F2    = ((1 - wl2) / wl2) * (df2_2 / 2)
pv2   = 1 - stats.f.cdf(F2, 2, df2_2)

print(f"  Wilks' Lambda (Y1,Y2) = {wl2:.6f}")
print(f"  F(2, {df2_2}) = {F2:.4f},  p = {pv2:.4f}")
print(f"  {'Significant at α=0.05' if pv2 < 0.05 else 'Not significant at α=0.05'}")
print()

# ─── REMEDY C: UNIVARIATE ANOVAs ─────────────────────────────────
print("=" * 65)
print("UNIVARIATE ANOVA (each DV separately)")
print("=" * 65)
univ_results = []
for j in range(p):
    g1 = Y[groups==1, j]; g2 = Y[groups==2, j]
    F, pv = stats.f_oneway(g1, g2)
    univ_results.append({"var": f"Y{j+1}", "F": F, "p": pv,
                          "sig": pv < 0.05})
    print(f"  Y{j+1}: F(1, {n-g}) = {F:.4f},  p = {pv:.4f}  "
          f"{'*' if pv < 0.05 else ''}")
print()

# ─── PLOTS ───────────────────────────────────────────────────────
os_path = "q116_plots"
import os; os.makedirs(os_path, exist_ok=True)

fig, axes = plt.subplots(2, 2, figsize=(14, 10), facecolor="white")
fig.suptitle("Question 11.6 — MANOVA Analysis", fontsize=15, fontweight="bold", y=0.98)

colors = {1: "#1A3A6B", 2: "#B82020"}
markers = {1: "o", 2: "s"}
labels = {1: "Group 1", 2: "Group 2"}

# Panel 1: Y1 vs Y2 scatter
ax = axes[0, 0]
for grp in [1, 2]:
    mask = groups == grp
    ax.scatter(Y[mask, 0], Y[mask, 1], color=colors[grp],
               marker=markers[grp], s=120, label=labels[grp], zorder=3)
    ax.scatter(means[grp][0], means[grp][1], color=colors[grp],
               marker="*", s=350, edgecolors="black", lw=0.8, zorder=4)
ax.set_xlabel("Y₁", fontsize=11)
ax.set_ylabel("Y₂", fontsize=11)
ax.set_title("Scatter: Y₁ vs Y₂ (★ = group mean)", fontsize=11)
ax.legend(fontsize=10); ax.grid(True, alpha=0.3); ax.set_facecolor("#F8F9FA")

# Panel 2: bar chart of group means
ax = axes[0, 1]
x = np.arange(4)
w = 0.35
b1 = ax.bar(x - w/2, means[1], w, label="Group 1", color=colors[1], alpha=0.85)
b2 = ax.bar(x + w/2, means[2], w, label="Group 2", color=colors[2], alpha=0.85)
ax.set_xticks(x); ax.set_xticklabels(["Y₁","Y₂","Y₃","Y₄"], fontsize=11)
ax.set_ylabel("Mean", fontsize=11)
ax.set_title("Group Means by Variable", fontsize=11)
ax.legend(fontsize=10); ax.grid(True, axis="y", alpha=0.3)
ax.set_facecolor("#F8F9FA")

# Panel 3: Univariate F-statistics
ax = axes[1, 0]
var_names = [r["var"] for r in univ_results]
F_vals    = [r["F"]   for r in univ_results]
bar_cols  = [colors[2] if r["sig"] else "#888888" for r in univ_results]
bars = ax.bar(var_names, F_vals, color=bar_cols, alpha=0.85, edgecolor="white")
for bar, r in zip(bars, univ_results):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.05,
            f"p={r['p']:.3f}", ha="center", va="bottom", fontsize=9)
ax.axhline(stats.f.ppf(0.95, 1, n-g), color="#1A3A6B", lw=1.5,
           linestyle="--", label="F critical (α=0.05)")
ax.set_ylabel("F-statistic", fontsize=11)
ax.set_title("Univariate F-Tests (each DV separately)", fontsize=11)
ax.legend(fontsize=9); ax.grid(True, axis="y", alpha=0.3)
ax.set_facecolor("#F8F9FA")

# Panel 4: W matrix heatmap + rank annotation
ax = axes[1, 1]
im = ax.imshow(W, cmap="Blues", aspect="auto")
for i in range(4):
    for j in range(4):
        ax.text(j, i, f"{W[i,j]:.2f}", ha="center", va="center",
                fontsize=10, color="black")
ax.set_xticks(range(4)); ax.set_yticks(range(4))
ax.set_xticklabels(["Y₁","Y₂","Y₃","Y₄"])
ax.set_yticklabels(["Y₁","Y₂","Y₃","Y₄"])
ax.set_title(f"Within-Group Matrix W  (Rank = {rank_W})", fontsize=11)
plt.colorbar(im, ax=ax, shrink=0.8)

plt.tight_layout()
out_plot = f"{os_path}/q116_results.png"
fig.savefig(out_plot, dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print(f"Saved plot: {out_plot}")

# ─── SAVE RESULTS ────────────────────────────────────────────────
results = {
    "n": n, "p": p, "g": g,
    "rank_W": rank_W, "det_W": det_W, "det_T": det_T,
    "wilks_lambda": wilks_lambda,
    "F_stat": F_stat, "p_val": p_val,
    "df1": p, "df2": n - g - p + 1,
    "W": W.tolist(), "B": B.tolist(), "T": T.tolist(),
    "means": {k: v.tolist() for k,v in means.items()},
    "grand_mean": grand_mean.tolist(),
    "univ_results": univ_results,
    "wl2": wl2, "F2": F2, "pv2": pv2,
    "eig_W": sorted(eig_W.tolist(), reverse=True),
}
with open("q116_results.pkl","wb") as f:
    pickle.dump(results, f)
print("Saved: q116_results.pkl")
print("\nANALYSIS COMPLETE")

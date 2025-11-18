import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("="*80)
print("RESEARCH QUESTION 2 — KL DIVERGENCE BETWEEN PARTICIPANTS")
print("="*80)

# ------------------------------------------------------------
# STEP 1: LOAD DATA
# ------------------------------------------------------------
df1 = pd.read_csv("FS1987-intraday.csv")
df2 = pd.read_csv("FS2116-intraday.csv")

print(f"FS1987 rows: {len(df1):,}")
print(f"FS2116 rows: {len(df2):,}")

# ------------------------------------------------------------
# STEP 2: EXTRACT ACTIVITY LEVELS (Fitbit's Provided Column)
# ------------------------------------------------------------
df1["activity_level"] = df1["activities_calories_level"]
df2["activity_level"] = df2["activities_calories_level"]

# Valid activity labels must be 0,1,2,3
valid_levels = [0,1,2,3]
df1 = df1[df1["activity_level"].isin(valid_levels)]
df2 = df2[df2["activity_level"].isin(valid_levels)]

# ------------------------------------------------------------
# STEP 3: COMPUTE DISTRIBUTIONS
# ------------------------------------------------------------
def compute_distribution(series):
    """Return probability distribution over activity levels 0–3."""
    counts = series.value_counts().reindex([0,1,2,3], fill_value=0)
    probs = counts / counts.sum()
    return probs.values

P = compute_distribution(df1["activity_level"])   # FS1987
Q = compute_distribution(df2["activity_level"])   # FS2116

print("\nFS1987 Distribution (P):", P)
print("FS2116 Distribution (Q):", Q)

# ------------------------------------------------------------
# STEP 4: KL DIVERGENCE FUNCTION
# ------------------------------------------------------------
def kl_divergence(P, Q):
    """
    Compute KL(P || Q)
    Add tiny smoothing (eps) to avoid log(0).
    """
    eps = 1e-12
    P = np.array(P) + eps
    Q = np.array(Q) + eps
    return np.sum(P * np.log2(P / Q))

KL_PQ = kl_divergence(P, Q)   # KL(P || Q)
KL_QP = kl_divergence(Q, P)   # KL(Q || P)

# Symmetric KL (optional)
KL_sym = KL_PQ + KL_QP

# ------------------------------------------------------------
# STEP 5: PRINT RESULTS
# ------------------------------------------------------------
print("\n" + "="*80)
print("KL DIVERGENCE RESULTS")
print("="*80)
print(f"KL(P || Q)  = {KL_PQ:.4f} bits  (FS1987 vs FS2116)")
print(f"KL(Q || P)  = {KL_QP:.4f} bits  (FS2116 vs FS1987)")
print(f"Symmetric KL = {KL_sym:.4f} bits")
print("="*80)

# ------------------------------------------------------------
# STEP 6: INTERPRETATION
# ------------------------------------------------------------
def interpret_kl(value):
    if value < 0.05:
        return "Almost identical activity profiles"
    elif value < 0.15:
        return "Slightly different lifestyles"
    elif value < 0.30:
        return "Moderately different activity behaviors"
    else:
        return "Strongly different lifestyle patterns"

print("\nINTERPRETATION:")
print(f"  Interpretation of KL(P || Q):   {interpret_kl(KL_PQ)}")
print(f"  Interpretation of KL(Q || P):   {interpret_kl(KL_QP)}")
print(f"  Interpretation of Symmetric KL: {interpret_kl(KL_sym)}")

# ------------------------------------------------------------
# STEP 7: OPTIONAL VISUALIZATION
# ------------------------------------------------------------
plt.figure(figsize=(8,5))
labels = ["Sedentary (0)", "Light (1)", "Moderate (2)", "Vigorous (3)"]

x = np.arange(len(labels))
width = 0.35

plt.bar(x - width/2, P, width, label='FS1987')
plt.bar(x + width/2, Q, width, label='FS2116')

plt.xticks(x, labels)
plt.ylabel("Probability")
plt.title("Activity Level Distributions (For KL Divergence)")
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("kl_activity_distributions.png", dpi=300)

print("\n✓ Saved plot: kl_activity_distributions.png")
print("\nKL Divergence Analysis Complete.\n")
print("="*80)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use("seaborn-v0_8-whitegrid")

print("="*80)
print("RQ2 — TEMPORAL PREDICTABILITY USING MUTUAL INFORMATION")
print("="*80)

# ------------------------------------------------------------
# Load data
# ------------------------------------------------------------
df1 = pd.read_csv("FS1987-intraday.csv")
df2 = pd.read_csv("FS2116-intraday.csv")

df1["activity"] = df1["activities_calories_level"]
df2["activity"] = df2["activities_calories_level"]

valid = [0,1,2,3]
df1 = df1[df1["activity"].isin(valid)]
df2 = df2[df2["activity"].isin(valid)]

# ------------------------------------------------------------
# Function to compute MI between X_t and X_(t+1)
# ------------------------------------------------------------
def compute_mutual_information(series):
    series = series.values
    X = series[:-1]
    Y = series[1:]

    # 4 activity levels
    matrix = np.zeros((4,4))

    for x,y in zip(X,Y):
        matrix[int(x), int(y)] += 1

    joint = matrix / matrix.sum()

    px = joint.sum(axis=1).reshape(4,1)
    py = joint.sum(axis=0).reshape(1,4)

    eps = 1e-12
    ratio = (joint + eps) / (px * py + eps)

    MI = np.sum(joint * np.log2(ratio))

    return MI, joint, px.flatten()

# ------------------------------------------------------------
# Compute MI for both participants
# ------------------------------------------------------------
MI_1987, joint1987, dist1987 = compute_mutual_information(df1["activity"])
MI_2116, joint2116, dist2116 = compute_mutual_information(df2["activity"])

print(f"FS1987 Mutual Information: {MI_1987:.4f} bits")
print(f"FS2116 Mutual Information: {MI_2116:.4f} bits")
print(f"Difference: {abs(MI_1987 - MI_2116):.4f} bits")

# ------------------------------------------------------------
# Save heatmaps
# ------------------------------------------------------------
plt.figure(figsize=(6,5))
sns.heatmap(joint1987, annot=True, cmap="Blues", fmt=".3f")
plt.title("FS1987 Transition Joint Distribution")
plt.savefig("FS1987_transition_matrix.png", dpi=300)

plt.figure(figsize=(6,5))
sns.heatmap(joint2116, annot=True, cmap="Reds", fmt=".3f")
plt.title("FS2116 Transition Joint Distribution")
plt.savefig("FS2116_transition_matrix.png", dpi=300)

print("\n✓ Saved heatmaps for transition matrices.")
print("✓ Mutual Information Analysis Complete.")
print("="*80)

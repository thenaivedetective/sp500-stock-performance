"""
Homework Analysis — Questions 10.4, 10.5, 10.6, 11.5
Multivariate Statistics
Uses: pandas, statsmodels, sklearn, scipy, matplotlib, seaborn
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from statsmodels.formula.api import logit
import statsmodels.api as sm
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (confusion_matrix, classification_report,
                             roc_curve, auc, accuracy_score)
from sklearn.preprocessing import LabelEncoder, StandardScaler
from scipy import stats
import warnings, os
warnings.filterwarnings("ignore")

os.makedirs("hw_plots", exist_ok=True)
RESULTS = {}   # store all numeric results for PDF

# ════════════════════════════════════════════════════════════════════
# DATA LOADING HELPERS
# ════════════════════════════════════════════════════════════════════

def load_admis():
    rows = []
    with open("attached_assets/ADMIS_(1)_1775863218416.DAT") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("Admission") or \
               line.startswith("-----") or line.startswith("Applicant") \
               or line.startswith("Number") or line.startswith("Source") \
               or line.startswith("Note"):
                continue
            parts = line.split()
            if len(parts) == 4:
                try:
                    rows.append({
                        "app_num":  int(parts[0]),
                        "adm_status": int(parts[1]),
                        "gpa":      float(parts[2]),
                        "gmat":     int(parts[3]),
                    })
                except ValueError:
                    pass
    return pd.DataFrame(rows)


def load_depres():
    cols = (["OBS","ID","SEX","AGE","MARITAL","EDUCAT","EMPLOY","INCOME","RELIG"] +
            [f"C{i}" for i in range(1,21)] +
            ["CESD","CASES","DRINK","HEALTH","REGDOC","TREAT",
             "BEDDAYS","ACUTEILL","CHRONILL"])
    rows = []
    with open("attached_assets/DEPRES_1775863218416.DAT") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("Depress") or line.startswith("---"):
                continue
            parts = line.split()
            if len(parts) == 38:
                try:
                    rows.append([int(x) if "." not in x else float(x)
                                 for x in parts])
                except ValueError:
                    pass
    return pd.DataFrame(rows, columns=cols)


def load_phone():
    rows = []
    with open("attached_assets/PHONE_(1)_1775863218414.DAT") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("Phone") or \
               line.startswith("---") or line.startswith("ID") \
               or line.startswith("Number"):
                continue
            parts = line.split()
            if len(parts) == 8:
                try:
                    rows.append({
                        "id":      int(parts[0]),
                        "n_phones":int(parts[1]),
                        "A1":int(parts[2]),"A2":int(parts[3]),
                        "A3":int(parts[4]),"A4":int(parts[5]),
                        "A5":int(parts[6]),"A6":int(parts[7]),
                    })
                except ValueError:
                    pass
    return pd.DataFrame(rows)


# ════════════════════════════════════════════════════════════════════
# QUESTION 10.4 — ADMISSIONS LOGISTIC REGRESSION
# ════════════════════════════════════════════════════════════════════
print("\n" + "="*65)
print("Q10.4  ADMISSIONS — LOGISTIC REGRESSION")
print("="*65)

admis = load_admis()
print(f"Total records: {len(admis)}")

# Keep only admitted (1) and not-admitted (2)
df_a = admis[admis["adm_status"].isin([1, 2])].copy()
# 0 = admitted, 1 = not-admitted
df_a["admit"] = (df_a["adm_status"] == 2).astype(int)

# GPA category
def gpa_cat(g):
    if g < 2.50:  return 1
    elif g <= 3.00: return 2
    elif g <= 3.50: return 3
    else:           return 4

df_a["gpa_cat"] = df_a["gpa"].apply(gpa_cat)
print(f"\nAdmitted: {(df_a['admit']==0).sum()}   Not-admitted: {(df_a['admit']==1).sum()}")
print("\nGPA Category distribution:")
print(df_a.groupby("gpa_cat")["admit"].value_counts().unstack(fill_value=0))

# ── Dummy coding (reference = GPA category 1) ─────────────────────
df_a["gpa2"] = (df_a["gpa_cat"]==2).astype(int)
df_a["gpa3"] = (df_a["gpa_cat"]==3).astype(int)
df_a["gpa4"] = (df_a["gpa_cat"]==4).astype(int)

# NOTE: GPA category creates near-perfect separation (all GPA Cat 3,4
# are admitted; all Cat 1 are not admitted). statsmodels coefficients
# diverge under perfect separation, so we use sklearn LR (L2 penalty,
# C=1) which provides stable, regularized estimates.

X1 = df_a[["gpa2","gpa3","gpa4"]].values
X2 = df_a[["gpa2","gpa3","gpa4","gmat"]].values
y_a = df_a["admit"].values

# Scale GMAT for numerical stability
scaler_a = StandardScaler()
X2s = X2.copy().astype(float)
X2s[:, 3] = scaler_a.fit_transform(X2[:,3].reshape(-1,1)).ravel()

# ── Model 1: GPA category only ────────────────────────────────────
lr1 = LogisticRegression(C=1.0, solver="lbfgs", max_iter=1000)
lr1.fit(X1, y_a)
pred1     = lr1.predict(X1)
prob1     = lr1.predict_proba(X1)[:,1]
cm1       = confusion_matrix(y_a, pred1)
acc1      = accuracy_score(y_a, pred1)
fpr1,tpr1,_ = roc_curve(y_a, prob1)
auc1      = auc(fpr1, tpr1)
coef1_names = ["Intercept","gpa2","gpa3","gpa4"]
coef1_vals  = np.concatenate([[lr1.intercept_[0]], lr1.coef_[0]])
RESULTS["q104_acc1"] = acc1
RESULTS["q104_auc1"] = auc1
RESULTS["q104_mod1_params"] = dict(zip(coef1_names, coef1_vals))

print("\n--- Model 1: GPA Category Only (sklearn L2-penalized LR) ---")
print(f"  Perfect separation detected — regularized (C=1) estimates used")
for n,v in zip(coef1_names, coef1_vals):
    print(f"  {n:12s}  coef={v:8.4f}")
print(f"\nModel 1 Accuracy: {acc1:.4f}  AUC: {auc1:.4f}")
print(f"Confusion Matrix:\n{cm1}")

# ── Model 2: GPA + GMAT ───────────────────────────────────────────
lr2 = LogisticRegression(C=1.0, solver="lbfgs", max_iter=1000)
lr2.fit(X2s, y_a)
pred2     = lr2.predict(X2s)
prob2     = lr2.predict_proba(X2s)[:,1]
cm2       = confusion_matrix(y_a, pred2)
acc2      = accuracy_score(y_a, pred2)
fpr2,tpr2,_ = roc_curve(y_a, prob2)
auc2      = auc(fpr2, tpr2)
coef2_names = ["Intercept","gpa2","gpa3","gpa4","gmat(std)"]
coef2_vals  = np.concatenate([[lr2.intercept_[0]], lr2.coef_[0]])
RESULTS["q104_acc2"] = acc2
RESULTS["q104_auc2"] = auc2
RESULTS["q104_mod2_params"] = dict(zip(coef2_names, coef2_vals))

print("\n--- Model 2: GPA Category + GMAT ---")
for n,v in zip(coef2_names, coef2_vals):
    print(f"  {n:12s}  coef={v:8.4f}")
print(f"\nModel 2 Accuracy: {acc2:.4f}  AUC: {auc2:.4f}")
print(f"Confusion Matrix:\n{cm2}")

# ── Plot Q10.4 ────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.patch.set_facecolor("#0D1B2E")
for ax in axes: ax.set_facecolor("#1A2F4A")

# ROC curves
axes[0].plot(fpr1, tpr1, color="#60A5FA", lw=2, label=f"GPA only (AUC={auc1:.3f})")
axes[0].plot(fpr2, tpr2, color="#10B981", lw=2, label=f"GPA+GMAT (AUC={auc2:.3f})")
axes[0].plot([0,1],[0,1], "k--", lw=1)
axes[0].set_xlabel("False Positive Rate", color="white")
axes[0].set_ylabel("True Positive Rate", color="white")
axes[0].set_title("ROC Curves — Q10.4", color="white", fontweight="bold")
axes[0].legend(facecolor="#1A2F4A", labelcolor="white")
axes[0].tick_params(colors="white"); axes[0].spines["bottom"].set_color("#334155")
axes[0].spines["left"].set_color("#334155"); axes[0].spines["top"].set_color("#334155")
axes[0].spines["right"].set_color("#334155")

# Confusion matrix model 2
sns.heatmap(cm2, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Admitted","Not Adm"],
            yticklabels=["Admitted","Not Adm"],
            ax=axes[1], cbar=False,
            annot_kws={"color":"white","fontsize":14})
axes[1].set_title("Confusion Matrix — Model 2\n(GPA + GMAT)", color="white", fontweight="bold")
axes[1].set_xlabel("Predicted", color="white"); axes[1].set_ylabel("Actual", color="white")
axes[1].tick_params(colors="white")

# Coefficients model 2
p2_names = coef2_names[1:]  # drop intercept
p2_vals  = coef2_vals[1:]
colors2 = ["#EF4444" if v > 0 else "#10B981" for v in p2_vals]
bars = axes[2].barh(p2_names, p2_vals, color=colors2)
axes[2].axvline(0, color="white", lw=0.8, ls="--")
axes[2].set_title("Model 2 Coefficients\n(L2-regularized)", color="white", fontweight="bold")
axes[2].tick_params(colors="white"); axes[2].set_xlabel("Coefficient", color="white")
axes[2].spines["bottom"].set_color("#334155"); axes[2].spines["left"].set_color("#334155")
axes[2].spines["top"].set_color("#334155"); axes[2].spines["right"].set_color("#334155")
for bar, val in zip(bars, p2_vals):
    axes[2].text(val + (0.05 if val > 0 else -0.05), bar.get_y()+bar.get_height()/2,
                 f"{val:.3f}", va="center", ha="left" if val > 0 else "right",
                 color="white", fontsize=9)

plt.tight_layout()
plt.savefig("hw_plots/q104_results.png", dpi=150, bbox_inches="tight",
            facecolor="#0D1B2E")
plt.close()
print("  Saved: hw_plots/q104_results.png")


# ════════════════════════════════════════════════════════════════════
# QUESTION 10.5 — CHOLESTEROL & HEART DISEASE
# ════════════════════════════════════════════════════════════════════
print("\n" + "="*65)
print("Q10.5  CHOLESTEROL — HAND CALCULATIONS + LOGISTIC REGRESSION")
print("="*65)

# Data from Table Q10.2
chol_data = pd.DataFrame({
    "level":    ["<200", "200-219", "220-259", ">259"],
    "midpoint": [185,    209.5,     239.5,     270],
    "present":  [6,      10,        30,        45],
    "absent":   [5,       6,         5,         7],
})
chol_data["total"]     = chol_data["present"] + chol_data["absent"]
chol_data["prob"]      = chol_data["present"] / chol_data["total"]
chol_data["odds"]      = chol_data["prob"]    / (1 - chol_data["prob"])
chol_data["log_odds"]  = np.log(chol_data["odds"])

print("\n(a) Probabilities and Log-Odds (hand calculations):")
print(chol_data[["level","present","absent","total","prob","odds","log_odds"]].to_string(index=False))
RESULTS["q105_table"] = chol_data.to_dict(orient="records")

# (b) Hand LR: simple linear regression of log_odds on midpoint
from numpy.polynomial import polynomial as P
x = chol_data["midpoint"].values
y = chol_data["log_odds"].values
b1 = (np.cov(x, y, bias=False)[0,1]) / np.var(x, ddof=1)
b0 = y.mean() - b1 * x.mean()
print(f"\n(b) Hand LR:  intercept={b0:.4f}  slope={b1:.6f}")
print(f"   Equation:  log-odds = {b0:.4f} + {b1:.6f} × Cholesterol")
RESULTS["q105_b0"] = b0; RESULTS["q105_b1"] = b1

# (c) Software LR with dummy variables
rows_chol = []
for _, row in chol_data.iterrows():
    for _ in range(int(row["present"])):
        rows_chol.append({"chol": row["level"], "hd": 1})
    for _ in range(int(row["absent"])):
        rows_chol.append({"chol": row["level"], "hd": 0})
df_c = pd.DataFrame(rows_chol)
df_c["c200_219"] = (df_c["chol"]=="200-219").astype(int)
df_c["c220_259"] = (df_c["chol"]=="220-259").astype(int)
df_c["c_gt259"]  = (df_c["chol"]==">259").astype(int)

mod_c = logit("hd ~ c200_219 + c220_259 + c_gt259", data=df_c).fit(disp=False)
print("\n(c) Software LR (dummy variables, ref = <200):")
print(mod_c.summary2())
RESULTS["q105_sw_params"] = mod_c.params.to_dict()
RESULTS["q105_sw_pvalues"] = mod_c.pvalues.to_dict()

# (d) Classification table
pred_c = (mod_c.predict(df_c) >= 0.5).astype(int)
cm_c   = confusion_matrix(df_c["hd"], pred_c)
acc_c  = accuracy_score(df_c["hd"], pred_c)
RESULTS["q105_acc"] = acc_c
print(f"\n(d) Classification Accuracy: {acc_c:.4f}")
print(f"Confusion Matrix:\n{cm_c}")

# ── Plot Q10.5 ────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.patch.set_facecolor("#0D1B2E")
for ax in axes: ax.set_facecolor("#1A2F4A")

# Prob & log-odds by cholesterol level
x_pos = np.arange(4)
axes[0].bar(x_pos - 0.2, chol_data["prob"], 0.35, color="#2563EB",
            label="P(Disease)")
axes[0].set_xticks(x_pos)
axes[0].set_xticklabels(chol_data["level"], color="white")
axes[0].set_title("Probability of Heart Disease\nby Cholesterol Level",
                  color="white", fontweight="bold")
axes[0].set_ylabel("Probability", color="white")
axes[0].tick_params(colors="white"); axes[0].set_ylim(0,1)
axes[0].legend(facecolor="#1A2F4A", labelcolor="white")
for spine in axes[0].spines.values(): spine.set_color("#334155")

# Log-odds with fitted line
x_fit = np.linspace(170, 285, 100)
y_fit = b0 + b1 * x_fit
axes[1].scatter(chol_data["midpoint"], chol_data["log_odds"],
                color="#F59E0B", s=100, zorder=5, label="Observed log-odds")
axes[1].plot(x_fit, y_fit, color="#60A5FA", lw=2, label="Fitted line (hand)")
axes[1].set_xlabel("Cholesterol Midpoint", color="white")
axes[1].set_ylabel("Log-Odds", color="white")
axes[1].set_title("Log-Odds vs Cholesterol\n(Hand Calculation)",
                  color="white", fontweight="bold")
axes[1].tick_params(colors="white")
axes[1].legend(facecolor="#1A2F4A", labelcolor="white")
for spine in axes[1].spines.values(): spine.set_color("#334155")

# Confusion matrix
sns.heatmap(cm_c, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Absent","Present"],
            yticklabels=["Absent","Present"],
            ax=axes[2], cbar=False, annot_kws={"color":"white","fontsize":14})
axes[2].set_title(f"Classification Table\nAccuracy={acc_c:.1%}",
                  color="white", fontweight="bold")
axes[2].set_xlabel("Predicted", color="white"); axes[2].set_ylabel("Actual", color="white")
axes[2].tick_params(colors="white")

plt.tight_layout()
plt.savefig("hw_plots/q105_results.png", dpi=150, bbox_inches="tight",
            facecolor="#0D1B2E")
plt.close()
print("  Saved: hw_plots/q105_results.png")


# ════════════════════════════════════════════════════════════════════
# QUESTION 10.6 — DEPRESSION DATA: LOGISTIC REGRESSION vs LDA
# ════════════════════════════════════════════════════════════════════
print("\n" + "="*65)
print("Q10.6  DEPRESSION — LOGISTIC REGRESSION vs DISCRIMINANT ANALYSIS")
print("="*65)

depres = load_depres()
print(f"Rows: {len(depres)},  CASES distribution: {depres['CASES'].value_counts().to_dict()}")

# Predictors: demographic + health variables
pred_cols = ["SEX","AGE","MARITAL","EDUCAT","EMPLOY","INCOME","RELIG",
             "DRINK","HEALTH","REGDOC","TREAT","BEDDAYS","ACUTEILL","CHRONILL"]
df_d = depres[pred_cols + ["CASES"]].dropna()
X_d = df_d[pred_cols]
y_d = df_d["CASES"]

# Logistic Regression
formula_d = "CASES ~ " + " + ".join(pred_cols)
mod_d = logit(formula_d, data=df_d).fit(disp=False, maxiter=200)
print("\nLogistic Regression Summary:")
print(mod_d.summary2())
pred_d_lr = (mod_d.predict(df_d) >= 0.5).astype(int)
cm_d_lr   = confusion_matrix(y_d, pred_d_lr)
acc_d_lr  = accuracy_score(y_d, pred_d_lr)
fpr_d,tpr_d,_ = roc_curve(y_d, mod_d.predict(df_d))
auc_d_lr  = auc(fpr_d, tpr_d)
RESULTS["q106_lr_acc"] = acc_d_lr
RESULTS["q106_lr_auc"] = auc_d_lr
RESULTS["q106_lr_params"] = mod_d.params.to_dict()
RESULTS["q106_lr_pvalues"] = mod_d.pvalues.to_dict()

print(f"\nLR Accuracy: {acc_d_lr:.4f}  AUC: {auc_d_lr:.4f}")

# Linear Discriminant Analysis
lda_d = LinearDiscriminantAnalysis()
lda_d.fit(X_d, y_d)
pred_d_lda = lda_d.predict(X_d)
cm_d_lda   = confusion_matrix(y_d, pred_d_lda)
acc_d_lda  = accuracy_score(y_d, pred_d_lda)
fpr_dl,tpr_dl,_ = roc_curve(y_d, lda_d.predict_proba(X_d)[:,1])
auc_d_lda  = auc(fpr_dl, tpr_dl)
RESULTS["q106_lda_acc"] = acc_d_lda
RESULTS["q106_lda_auc"] = auc_d_lda

print(f"LDA Accuracy: {acc_d_lda:.4f}  AUC: {auc_d_lda:.4f}")
print(f"\nLR Confusion Matrix:\n{cm_d_lr}")
print(f"\nLDA Confusion Matrix:\n{cm_d_lda}")

# Significant predictors
sig = mod_d.pvalues[mod_d.pvalues < 0.05].drop("Intercept", errors="ignore")
RESULTS["q106_sig_vars"] = sig.index.tolist()
print(f"\nSignificant predictors (p<0.05): {list(sig.index)}")

# ── Plot Q10.6 ────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.patch.set_facecolor("#0D1B2E")
for ax in axes.flat: ax.set_facecolor("#1A2F4A")

# LR Confusion Matrix
sns.heatmap(cm_d_lr, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Normal","Depressed"],
            yticklabels=["Normal","Depressed"],
            ax=axes[0,0], cbar=False, annot_kws={"color":"white","fontsize":13})
axes[0,0].set_title(f"LR Confusion Matrix\nAccuracy={acc_d_lr:.1%}",
                    color="white", fontweight="bold")
axes[0,0].set_xlabel("Predicted", color="white"); axes[0,0].set_ylabel("Actual", color="white")
axes[0,0].tick_params(colors="white")

# LDA Confusion Matrix
sns.heatmap(cm_d_lda, annot=True, fmt="d", cmap="Greens",
            xticklabels=["Normal","Depressed"],
            yticklabels=["Normal","Depressed"],
            ax=axes[0,1], cbar=False, annot_kws={"color":"white","fontsize":13})
axes[0,1].set_title(f"LDA Confusion Matrix\nAccuracy={acc_d_lda:.1%}",
                    color="white", fontweight="bold")
axes[0,1].set_xlabel("Predicted", color="white"); axes[0,1].set_ylabel("Actual", color="white")
axes[0,1].tick_params(colors="white")

# ROC Comparison
axes[1,0].plot(fpr_d,  tpr_d,  color="#60A5FA", lw=2, label=f"LR  (AUC={auc_d_lr:.3f})")
axes[1,0].plot(fpr_dl, tpr_dl, color="#10B981", lw=2, label=f"LDA (AUC={auc_d_lda:.3f})")
axes[1,0].plot([0,1],[0,1], "k--", lw=1)
axes[1,0].set_xlabel("False Positive Rate", color="white")
axes[1,0].set_ylabel("True Positive Rate",  color="white")
axes[1,0].set_title("ROC Curve: LR vs LDA", color="white", fontweight="bold")
axes[1,0].legend(facecolor="#1A2F4A", labelcolor="white")
axes[1,0].tick_params(colors="white")
for spine in axes[1,0].spines.values(): spine.set_color("#334155")

# Significant LR coefficients
sig_params = mod_d.params.drop("Intercept")
sig_colors = ["#EF4444" if v > 0 else "#10B981" for v in sig_params]
axes[1,1].barh(sig_params.index, sig_params.values, color=sig_colors)
axes[1,1].axvline(0, color="white", lw=0.8, ls="--")
axes[1,1].set_title("LR Coefficients (Depression Model)", color="white", fontweight="bold")
axes[1,1].tick_params(colors="white"); axes[1,1].set_xlabel("Coefficient", color="white")
for spine in axes[1,1].spines.values(): spine.set_color("#334155")

plt.tight_layout()
plt.savefig("hw_plots/q106_results.png", dpi=150, bbox_inches="tight",
            facecolor="#0D1B2E")
plt.close()
print("  Saved: hw_plots/q106_results.png")


# ════════════════════════════════════════════════════════════════════
# QUESTION 11.5 — MANOVA: DEPRES.DAT and PHONE.DAT
# ════════════════════════════════════════════════════════════════════
print("\n" + "="*65)
print("Q11.5  MANOVA — DEPRESSION + PHONE DATA")
print("="*65)

# ── MANOVA helper using Wilks' Lambda ─────────────────────────────
def wilks_lambda(X, groups):
    """Compute Wilks' Lambda and approximate F-test."""
    X = np.array(X, dtype=float)
    groups = np.array(groups)
    unique = np.unique(groups)
    k = len(unique)
    n = len(X)
    p = X.shape[1]
    grand_mean = X.mean(axis=0)

    # Between-group scatter
    B = np.zeros((p, p))
    for g in unique:
        Xg = X[groups == g]
        diff = Xg.mean(axis=0) - grand_mean
        B += len(Xg) * np.outer(diff, diff)

    # Within-group scatter
    W = np.zeros((p, p))
    for g in unique:
        Xg = X[groups == g]
        diff = Xg - Xg.mean(axis=0)
        W += diff.T @ diff

    T = B + W
    lam = np.linalg.det(W) / np.linalg.det(T)

    # Approximate F (Rao's approximation)
    df_h = (k - 1) * p
    df_e = (n - k) * p
    s = np.sqrt((p**2 * (k-1)**2 - 4) / (p**2 + (k-1)**2 - 5)) if (p**2 + (k-1)**2) > 5 else 1
    dff  = (n - 1 - (p + k)/2) * s - (p*(k-1) - 2)/2
    dfe2 = p*(k-1)
    Fapprox = (1 - lam**(1/s)) / (lam**(1/s)) * (dff / dfe2)
    return lam, Fapprox, dfe2, dff

# ── PART A: Depression data — CASES as grouping, C1-C20 as DVs ────
c_cols = [f"C{i}" for i in range(1, 21)]
df_manova_d = depres[c_cols + ["CASES"]].dropna()
X_md = df_manova_d[c_cols].values
y_md = df_manova_d["CASES"].values

lam_d, F_d, df1_d, df2_d = wilks_lambda(X_md, y_md)
print(f"\nMANOVA — DEPRES (DVs=C1-C20, Group=CASES):")
print(f"  Wilks' Lambda = {lam_d:.6f}")
print(f"  Approx F({df1_d:.0f},{df2_d:.1f}) = {F_d:.4f}")
RESULTS["q115_dep_lambda"] = lam_d
RESULTS["q115_dep_F"] = F_d
RESULTS["q115_dep_df"] = (df1_d, df2_d)

# Univariate F-tests (one-way ANOVA for each DV)
print("\n  Univariate F-tests (each CES-D item):")
univ_results_d = []
for col in c_cols:
    grps = [df_manova_d[col][df_manova_d["CASES"]==g].values
            for g in sorted(df_manova_d["CASES"].unique())]
    f_stat, p_val = stats.f_oneway(*grps)
    univ_results_d.append({"variable": col, "F": f_stat, "p-value": p_val,
                            "significant": p_val < 0.05})
    print(f"    {col}: F={f_stat:.3f}  p={p_val:.4f}{'  *' if p_val<0.05 else ''}")
RESULTS["q115_dep_univ"] = univ_results_d

# LDA comparison — Depression
lda_dep = LinearDiscriminantAnalysis()
lda_dep.fit(X_md, y_md)
pred_dep_lda = lda_dep.predict(X_md)
acc_dep_lda  = accuracy_score(y_md, pred_dep_lda)
RESULTS["q115_dep_lda_acc"] = acc_dep_lda
print(f"\n  LDA Accuracy (C1-C20 → CASES): {acc_dep_lda:.4f}")

# Group means for each C item
group_means_d = df_manova_d.groupby("CASES")[c_cols].mean()
RESULTS["q115_dep_group_means"] = group_means_d.to_dict()

# ── PART B: Phone data — n_phones as grouping, A1-A6 as DVs ───────
phone = load_phone()
a_cols = ["A1","A2","A3","A4","A5","A6"]
df_manova_p = phone[a_cols + ["n_phones"]].dropna()
X_mp = df_manova_p[a_cols].values
y_mp = df_manova_p["n_phones"].values

lam_p, F_p, df1_p, df2_p = wilks_lambda(X_mp, y_mp)
print(f"\nMANOVA — PHONE (DVs=A1-A6, Group=n_phones):")
print(f"  Wilks' Lambda = {lam_p:.6f}")
print(f"  Approx F({df1_p:.0f},{df2_p:.1f}) = {F_p:.4f}")
RESULTS["q115_ph_lambda"] = lam_p
RESULTS["q115_ph_F"] = F_p
RESULTS["q115_ph_df"] = (df1_p, df2_p)

# Univariate F-tests
print("\n  Univariate F-tests (each attitude item):")
univ_results_p = []
for col in a_cols:
    grps = [df_manova_p[col][df_manova_p["n_phones"]==g].values
            for g in sorted(df_manova_p["n_phones"].unique())]
    f_stat, p_val = stats.f_oneway(*grps)
    univ_results_p.append({"variable": col, "F": f_stat, "p-value": p_val,
                            "significant": p_val < 0.05})
    print(f"    {col}: F={f_stat:.3f}  p={p_val:.4f}{'  *' if p_val<0.05 else ''}")
RESULTS["q115_ph_univ"] = univ_results_p

# LDA comparison — Phone
le = LabelEncoder()
y_mp_enc = le.fit_transform(y_mp)
lda_ph = LinearDiscriminantAnalysis()
lda_ph.fit(X_mp, y_mp_enc)
pred_ph_lda = lda_ph.predict(X_mp)
acc_ph_lda  = accuracy_score(y_mp_enc, pred_ph_lda)
RESULTS["q115_ph_lda_acc"] = acc_ph_lda
print(f"\n  LDA Accuracy (A1-A6 → n_phones): {acc_ph_lda:.4f}")

# Group means
group_means_p = df_manova_p.groupby("n_phones")[a_cols].mean()
RESULTS["q115_ph_group_means"] = group_means_p.to_dict()

# ── Plot Q11.5 ────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.patch.set_facecolor("#0D1B2E")
for ax in axes.flat: ax.set_facecolor("#1A2F4A")

# Heatmap: group means for C1-C20 by CASES
sns.heatmap(group_means_d, ax=axes[0,0], cmap="RdBu_r", cbar=True,
            linewidths=0.5, annot=False)
axes[0,0].set_title("DEPRES: Mean CES-D Items by CASES Group\n(0=Normal, 1=Depressed)",
                     color="white", fontweight="bold")
axes[0,0].set_xlabel("CES-D Items", color="white"); axes[0,0].set_ylabel("CASES", color="white")
axes[0,0].tick_params(colors="white")

# Univariate F-stats — Depression
df_univ_d = pd.DataFrame(univ_results_d)
bar_colors_d = ["#EF4444" if s else "#334155" for s in df_univ_d["significant"]]
axes[0,1].bar(df_univ_d["variable"], df_univ_d["F"], color=bar_colors_d)
axes[0,1].axhline(3.84, color="#F59E0B", lw=1.5, ls="--", label="F crit (p=0.05)")
axes[0,1].set_title("DEPRES: Univariate F-statistics\n(Red = Significant p<0.05)",
                     color="white", fontweight="bold")
axes[0,1].set_xlabel("CES-D Item", color="white"); axes[0,1].set_ylabel("F Statistic", color="white")
axes[0,1].tick_params(axis="x", rotation=45, labelcolor="white")
axes[0,1].tick_params(axis="y", colors="white")
axes[0,1].legend(facecolor="#1A2F4A", labelcolor="white")
for spine in axes[0,1].spines.values(): spine.set_color("#334155")

# Group means — Phone
group_means_p.T.plot(ax=axes[1,0], marker="o",
                      color=["#60A5FA","#10B981","#F59E0B"])
axes[1,0].set_title("PHONE: Attitude Item Means by\nNumber of Phones Owned",
                     color="white", fontweight="bold")
axes[1,0].set_xlabel("Attitude Item", color="white"); axes[1,0].set_ylabel("Mean Score", color="white")
axes[1,0].legend(title="# Phones", facecolor="#1A2F4A", labelcolor="white",
                 title_fontsize=9)
axes[1,0].tick_params(colors="white")
for spine in axes[1,0].spines.values(): spine.set_color("#334155")

# Univariate F-stats — Phone
df_univ_p = pd.DataFrame(univ_results_p)
bar_colors_p = ["#EF4444" if s else "#334155" for s in df_univ_p["significant"]]
axes[1,1].bar(df_univ_p["variable"], df_univ_p["F"], color=bar_colors_p)
axes[1,1].axhline(3.08, color="#F59E0B", lw=1.5, ls="--", label="F crit (p=0.05)")
axes[1,1].set_title("PHONE: Univariate F-statistics\n(Red = Significant p<0.05)",
                     color="white", fontweight="bold")
axes[1,1].set_xlabel("Attitude Item", color="white"); axes[1,1].set_ylabel("F Statistic", color="white")
axes[1,1].tick_params(colors="white")
axes[1,1].legend(facecolor="#1A2F4A", labelcolor="white")
for spine in axes[1,1].spines.values(): spine.set_color("#334155")

plt.tight_layout()
plt.savefig("hw_plots/q115_results.png", dpi=150, bbox_inches="tight",
            facecolor="#0D1B2E")
plt.close()
print("  Saved: hw_plots/q115_results.png")

print("\n" + "="*65)
print("ALL ANALYSES COMPLETE")
print("="*65)

import pickle
with open("hw_results.pkl","wb") as f:
    pickle.dump(RESULTS, f)
print("Results saved to hw_results.pkl")

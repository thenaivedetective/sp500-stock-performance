"""
Trains LDA and Logistic Regression on origination-time features only
(no post-outcome leakage) and saves models + scaler to disk.
"""
import pandas as pd
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib, os

print("Loading clean dataset...")
df = pd.read_csv("lending_club_clean.csv")
print(f"  Shape: {df.shape}")

# ── Origination-time features only (known at loan application) ────
ORIG_FEATURES = [
    "loan_amnt",       # How much they borrowed
    "term",            # 36 or 60 months
    "int_rate",        # Interest rate
    "installment",     # Monthly payment
    "grade",           # LendingClub grade (A=0 ... G=6)
    "emp_length",      # Years employed
    "annual_inc",      # Annual income
    "dti",             # Debt-to-income ratio
    "fico_range_low",  # FICO score (low end)
    "inq_last_6mths",  # Recent credit inquiries
    "open_acc",        # Open accounts
    "pub_rec",         # Public derogatory records
    "revol_util",      # Revolving utilization %
    "total_acc",       # Total accounts
    "delinq_2yrs",     # Delinquencies in past 2 years
]
ORIG_FEATURES = [f for f in ORIG_FEATURES if f in df.columns]
print(f"  Using {len(ORIG_FEATURES)} origination features: {ORIG_FEATURES}")

X = df[ORIG_FEATURES].copy()
y = df["default"].copy()

# Drop any rows with NaN in these features
mask = X.notna().all(axis=1)
X = X[mask].reset_index(drop=True)
y = y[mask].reset_index(drop=True)
print(f"  After NaN drop: {len(X)} rows")

# ── Balance classes (2:1 good:bad) ───────────────────────────────
n_bad  = (y == 1).sum()
n_good = min((y == 0).sum(), n_bad * 2)
idx_bad  = y[y == 1].index
idx_good = y[y == 0].sample(n=n_good, random_state=42).index
idx_use  = idx_bad.append(idx_good)
X_bal = X.loc[idx_use].reset_index(drop=True)
y_bal = y.loc[idx_use].reset_index(drop=True)
print(f"  Balanced: {len(X_bal)} rows  (Good={n_good} / Bad={n_bad})")

# ── Scale ─────────────────────────────────────────────────────────
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_bal)

# ── Train/test split ──────────────────────────────────────────────
Xtr, Xte, ytr, yte = train_test_split(
    X_scaled, y_bal, test_size=0.3, random_state=42, stratify=y_bal
)

# ── LDA ───────────────────────────────────────────────────────────
print("\nTraining LDA...")
lda = LinearDiscriminantAnalysis()
lda.fit(Xtr, ytr)
lda_acc = lda.score(Xte, yte)
print(f"  LDA accuracy: {lda_acc:.3f}")

# ── Logistic Regression ───────────────────────────────────────────
print("Training Logistic Regression...")
lr = LogisticRegression(max_iter=1000, random_state=42, solver="liblinear")
lr.fit(Xtr, ytr)
lr_acc = lr.score(Xte, yte)
print(f"  LR  accuracy: {lr_acc:.3f}")

# ── Save ──────────────────────────────────────────────────────────
os.makedirs("models", exist_ok=True)
joblib.dump(lda,    "models/lda_model.pkl")
joblib.dump(lr,     "models/lr_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")

# Save feature list and stats for the UI
feature_stats = {
    "features": ORIG_FEATURES,
    "means":    scaler.mean_.tolist(),
    "stds":     scaler.scale_.tolist(),
    "lda_acc":  round(lda_acc * 100, 1),
    "lr_acc":   round(lr_acc  * 100, 1),
}
import json
with open("models/feature_stats.json", "w") as f:
    json.dump(feature_stats, f, indent=2)

print("\nSaved: models/lda_model.pkl, lr_model.pkl, scaler.pkl, feature_stats.json")
print("Done.")

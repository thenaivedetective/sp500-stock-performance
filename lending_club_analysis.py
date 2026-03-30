# -*- coding: utf-8 -*-
"""
LendingClub Credit Risk Analysis
Techniques:
  - Interdependence: Factor Analysis
  - Dependence:      Linear Discriminant Analysis + Logistic Regression
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import FactorAnalysis
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (classification_report, confusion_matrix,
                              roc_auc_score, roc_curve)
from scipy import stats
import os

os.makedirs("results", exist_ok=True)

# ══════════════════════════════════════════════════════════
# STEP 1: LOAD RAW DATA
# ══════════════════════════════════════════════════════════

print("=" * 65)
print("STEP 1: LOADING RAW DATA")
print("=" * 65)

df_raw = pd.read_csv("lending_club_raw.csv", low_memory=False)
print(f"Raw shape: {df_raw.shape[0]:,} rows × {df_raw.shape[1]} columns")

# ══════════════════════════════════════════════════════════
# STEP 2: DATA CLEANING
# ══════════════════════════════════════════════════════════

print("\n" + "=" * 65)
print("STEP 2: DATA CLEANING")
print("=" * 65)

df = df_raw.copy()

# ── 2a. Drop columns with >40% missing values ──────────────
missing_pct = df.isnull().mean()
cols_to_drop_missing = missing_pct[missing_pct > 0.40].index.tolist()
df.drop(columns=cols_to_drop_missing, inplace=True)
print(f"\n[1] Dropped {len(cols_to_drop_missing)} columns with >40% missing values")

# ── 2b. Drop irrelevant / identifier columns ───────────────
irrelevant = ['id', 'member_id', 'url', 'desc', 'title', 'zip_code',
              'addr_state', 'earliest_cr_line', 'issue_d', 'last_pymnt_d',
              'next_pymnt_d', 'last_credit_pull_d', 'pymnt_plan',
              'funded_amnt_inv', 'out_prncp_inv', 'total_pymnt_inv',
              'emp_title', 'policy_code', 'sub_grade', 'application_type']
irrelevant_present = [c for c in irrelevant if c in df.columns]
df.drop(columns=irrelevant_present, inplace=True)
print(f"[2] Dropped {len(irrelevant_present)} irrelevant/identifier columns")

# ── 2c. Create binary target variable from loan_status ─────
print(f"\n[3] loan_status value counts (before recoding):")
print(df['loan_status'].value_counts().to_string())

bad_statuses = ['Charged Off', 'Default',
                'Late (31-120 days)', 'Late (16-30 days)',
                'Does not meet the credit policy. Status:Charged Off']
good_statuses = ['Fully Paid',
                 'Does not meet the credit policy. Status:Fully Paid']

df = df[df['loan_status'].isin(bad_statuses + good_statuses)].copy()
df['default'] = df['loan_status'].apply(lambda x: 1 if x in bad_statuses else 0)
df.drop(columns=['loan_status'], inplace=True)
print(f"\n    After removing ambiguous statuses: {len(df):,} rows")
print(f"    Default distribution:")
print(f"      Good (0): {(df['default']==0).sum():,} ({(df['default']==0).mean()*100:.1f}%)")
print(f"      Bad  (1): {(df['default']==1).sum():,} ({(df['default']==1).mean()*100:.1f}%)")

# ── 2d. Parse text fields ──────────────────────────────────
# int_rate: "12.5%" → 12.5
if 'int_rate' in df.columns:
    df['int_rate'] = df['int_rate'].astype(str).str.replace('%', '').str.strip().astype(float)

# revol_util: "45.2%" → 45.2
if 'revol_util' in df.columns:
    df['revol_util'] = df['revol_util'].astype(str).str.replace('%', '').str.strip()
    df['revol_util'] = pd.to_numeric(df['revol_util'], errors='coerce')

# term: " 36 months" → 36
if 'term' in df.columns:
    df['term'] = df['term'].astype(str).str.extract(r'(\d+)').astype(float)

# emp_length: "10+ years" → 10, "< 1 year" → 0
if 'emp_length' in df.columns:
    df['emp_length'] = df['emp_length'].astype(str)
    df['emp_length'] = df['emp_length'].str.replace('10+ years', '10')
    df['emp_length'] = df['emp_length'].str.replace('< 1 year', '0')
    df['emp_length'] = df['emp_length'].str.extract(r'(\d+)')
    df['emp_length'] = pd.to_numeric(df['emp_length'], errors='coerce')

print(f"\n[4] Parsed text fields: int_rate, revol_util, term, emp_length → numeric")

# ── 2e. Encode remaining categorical columns ───────────────
cat_cols = df.select_dtypes(include='object').columns.tolist()
if 'default' in cat_cols:
    cat_cols.remove('default')
for col in cat_cols:
    df[col] = LabelEncoder().fit_transform(df[col].astype(str))
print(f"[5] Label-encoded {len(cat_cols)} categorical columns: {cat_cols}")

# ── 2f. Remove outliers (annual_inc, loan_amnt) ────────────
for col in ['annual_inc', 'loan_amnt', 'revol_bal']:
    if col in df.columns:
        q1, q99 = df[col].quantile(0.01), df[col].quantile(0.99)
        df = df[(df[col] >= q1) & (df[col] <= q99)]
print(f"[6] Removed outliers (1st–99th percentile) in annual_inc, loan_amnt, revol_bal")

# ── 2g. Drop rows with any remaining missing values ────────
before = len(df)
df.dropna(inplace=True)
print(f"[7] Dropped {before - len(df):,} rows with remaining missing values")

print(f"\n✔  Clean dataset: {len(df):,} rows × {df.shape[1]} columns")

# Save cleaned data
df.to_csv("lending_club_clean.csv", index=False)
print("    Saved: lending_club_clean.csv")

# ══════════════════════════════════════════════════════════
# STEP 3: EXPLORATORY OVERVIEW
# ══════════════════════════════════════════════════════════

print("\n" + "=" * 65)
print("STEP 3: EXPLORATORY OVERVIEW")
print("=" * 65)

y = df['default']
X_all = df.drop(columns=['default'])

num_cols = X_all.select_dtypes(include=[np.number]).columns.tolist()
print(f"\nNumeric features available: {len(num_cols)}")
print(f"Feature names: {num_cols}")

# Correlation heatmap of top features
top_corr_cols = (df[num_cols + ['default']]
                 .corr()['default']
                 .abs()
                 .drop('default')
                 .nlargest(15)
                 .index.tolist())

fig, ax = plt.subplots(figsize=(10, 8))
corr_data = df[top_corr_cols + ['default']].corr()
sns.heatmap(corr_data, annot=True, fmt='.2f', cmap='coolwarm',
            center=0, linewidths=0.4, ax=ax, annot_kws={"size": 7})
ax.set_title('Correlation Heatmap — Top 15 Features vs Default', fontsize=12)
plt.tight_layout()
plt.savefig("results/correlation_heatmap.png", dpi=150)
plt.close()
print("\nCorrelation heatmap saved.")

# ══════════════════════════════════════════════════════════
# STEP 4: FACTOR ANALYSIS (Interdependence)
# ══════════════════════════════════════════════════════════

print("\n" + "=" * 65)
print("STEP 4: FACTOR ANALYSIS (Interdependence Technique)")
print("=" * 65)

# Select 20 most meaningful financial features for Factor Analysis
fa_features = [
    'loan_amnt', 'term', 'int_rate', 'installment', 'grade',
    'emp_length', 'annual_inc', 'dti', 'fico_range_low',
    'inq_last_6mths', 'open_acc', 'pub_rec', 'revol_bal',
    'revol_util', 'total_acc', 'delinq_2yrs', 'mort_acc',
    'total_bc_limit', 'tot_cur_bal', 'bc_util'
]
fa_features = [f for f in fa_features if f in df.columns]

# Use a 50k sample for FA computation speed
fa_sample = df[fa_features].sample(n=50000, random_state=42)
X_num = fa_sample.copy()
scaler_fa = StandardScaler()
X_num_scaled = pd.DataFrame(scaler_fa.fit_transform(X_num), columns=fa_features)
num_cols_fa = fa_features
print(f"Using {len(fa_features)} key financial features for Factor Analysis (50k sample)")

# Bartlett's Test
corr_matrix = np.corrcoef(X_num_scaled.T)
n, p = X_num_scaled.shape
chi2_stat = -(n - 1 - (2*p + 5)/6) * np.log(np.linalg.det(corr_matrix) + 1e-10)
df_bart = p * (p - 1) / 2
p_bart = 1 - stats.chi2.cdf(chi2_stat, df_bart)
print(f"\nBartlett's Test of Sphericity:")
print(f"  Chi-square = {chi2_stat:,.2f},  p-value = {p_bart:.6f}")
print(f"  → {'PASS ✔ Factor Analysis is appropriate' if p_bart < 0.05 else 'FAIL ✘'}")

# Eigenvalues → number of factors
eigenvalues, _ = np.linalg.eigh(corr_matrix)
eigenvalues = np.sort(eigenvalues)[::-1]
n_factors = min(6, max(3, sum(eigenvalues > 1)))
print(f"\nEigenvalues: {np.round(eigenvalues[:10], 3)}  ...")
print(f"Factors with eigenvalue > 1: {n_factors}")

# Scree Plot
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(range(1, len(eigenvalues)+1), eigenvalues, marker='o',
        color='steelblue', linewidth=2, markersize=5)
ax.axhline(y=1, color='red', linestyle='--', linewidth=1.5, label='Eigenvalue = 1')
ax.set_xlabel('Factor Number', fontsize=11)
ax.set_ylabel('Eigenvalue', fontsize=11)
ax.set_title('Scree Plot — Factor Analysis (LendingClub)', fontsize=12)
ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("results/fa_scree_plot.png", dpi=150)
plt.close()
print("\nScree plot saved.")

# Fit Factor Analysis
fa = FactorAnalysis(n_components=n_factors, random_state=42, max_iter=1000)
fa.fit(X_num_scaled)

loadings = pd.DataFrame(fa.components_.T, index=fa_features,
                        columns=[f'F{i+1}' for i in range(n_factors)])

# Variance explained
ss_loadings = (loadings**2).sum(axis=0)
prop_var    = ss_loadings / p
cum_var     = prop_var.cumsum()

print(f"\nFactor Loadings (showing |loading| > 0.30):")
for factor in loadings.columns:
    sig = loadings[factor][loadings[factor].abs() > 0.30].sort_values(key=abs, ascending=False)
    print(f"\n  {factor} (explains {prop_var[factor]*100:.1f}% variance):")
    for var, val in sig.items():
        print(f"    {var:<30} {val:+.3f}")

print(f"\nVariance Explained Summary:")
for i, factor in enumerate(loadings.columns):
    print(f"  {factor}: SS={ss_loadings[factor]:.3f} | "
          f"Prop={prop_var[factor]*100:.1f}% | Cum={cum_var[factor]*100:.1f}%")

# Loadings heatmap
fig, ax = plt.subplots(figsize=(max(8, n_factors*2), max(8, len(num_cols)*0.5)))
sns.heatmap(loadings, annot=True, fmt='.2f', cmap='RdYlGn', center=0,
            linewidths=0.4, ax=ax, annot_kws={"size": 8})
ax.set_title(f'Factor Loadings Heatmap ({n_factors} Factors — Varimax)', fontsize=12)
plt.tight_layout()
plt.savefig("results/fa_loadings_heatmap.png", dpi=150)
plt.close()
print("\nFactor loadings heatmap saved.")

# ══════════════════════════════════════════════════════════
# STEP 5: PREPARE FOR DEPENDENCE TECHNIQUES
# ══════════════════════════════════════════════════════════

scaler_dep = StandardScaler()
X_scaled = pd.DataFrame(scaler_dep.fit_transform(X_all[num_cols]), columns=num_cols)
y_reset = y.reset_index(drop=True)

# Downsample majority class for balanced training
n_bad  = (y_reset == 1).sum()
n_good = (y_reset == 0).sum()
print(f"\n[Balancing] Good={n_good:,}  Bad={n_bad:,}")
idx_bad  = y_reset[y_reset == 1].index
idx_good = y_reset[y_reset == 0].sample(n=min(n_bad * 2, n_good), random_state=42).index
idx_use  = idx_bad.append(idx_good)
X_bal = X_scaled.loc[idx_use].reset_index(drop=True)
y_bal = y_reset.loc[idx_use].reset_index(drop=True)
print(f"[Balancing] Balanced set: {len(X_bal):,} rows  "
      f"(Good={( y_bal==0).sum():,} / Bad={(y_bal==1).sum():,})")

X_train, X_test, y_train, y_test = train_test_split(
    X_bal, y_bal, test_size=0.3, random_state=42, stratify=y_bal)

# ══════════════════════════════════════════════════════════
# STEP 6: LINEAR DISCRIMINANT ANALYSIS (Dependence)
# ══════════════════════════════════════════════════════════

print("\n" + "=" * 65)
print("STEP 6: LINEAR DISCRIMINANT ANALYSIS (Dependence Technique)")
print("=" * 65)

lda = LinearDiscriminantAnalysis()
lda.fit(X_train, y_train)
y_pred_lda  = lda.predict(X_test)
y_prob_lda  = lda.predict_proba(X_test)[:, 1]

print(f"\nLDA Classification Report:")
print(classification_report(y_test, y_pred_lda, target_names=['Good', 'Default']))
print(f"AUC-ROC: {roc_auc_score(y_test, y_prob_lda):.4f}")

lda_coef = pd.Series(lda.coef_[0], index=num_cols).sort_values(key=abs, ascending=False)
print(f"\nTop 10 LDA Discriminant Coefficients:")
print(lda_coef.head(10).round(4).to_string())

# Confusion matrix
fig, ax = plt.subplots(figsize=(5, 4))
cm = confusion_matrix(y_test, y_pred_lda)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Good','Default'], yticklabels=['Good','Default'], ax=ax)
ax.set_xlabel('Predicted'); ax.set_ylabel('Actual')
ax.set_title('LDA Confusion Matrix')
plt.tight_layout()
plt.savefig("results/lda_confusion_matrix.png", dpi=150)
plt.close()

# LDA projection
X_lda_proj = lda.transform(X_scaled.reset_index(drop=True))
fig, ax = plt.subplots(figsize=(9, 5))
for label, color, name in zip([0, 1], ['steelblue', 'tomato'], ['Good Credit', 'Default']):
    mask = y_reset == label
    ax.hist(X_lda_proj[mask, 0], bins=60, alpha=0.6, color=color, label=name, density=True)
ax.set_xlabel('LDA Discriminant Score'); ax.set_ylabel('Density')
ax.set_title('LDA Projection: Good vs Default Borrowers')
ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("results/lda_projection.png", dpi=150)
plt.close()
print("LDA plots saved.")

# ══════════════════════════════════════════════════════════
# STEP 7: LOGISTIC REGRESSION (Dependence)
# ══════════════════════════════════════════════════════════

print("\n" + "=" * 65)
print("STEP 7: LOGISTIC REGRESSION (Dependence Technique)")
print("=" * 65)

lr = LogisticRegression(max_iter=1000, random_state=42, C=0.1)
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)
y_prob_lr = lr.predict_proba(X_test)[:, 1]

print(f"\nLogistic Regression Classification Report:")
print(classification_report(y_test, y_pred_lr, target_names=['Good', 'Default']))
print(f"AUC-ROC: {roc_auc_score(y_test, y_prob_lr):.4f}")

lr_coef = pd.Series(lr.coef_[0], index=num_cols).sort_values(key=abs, ascending=False)
print(f"\nTop 10 Logistic Regression Coefficients (magnitude):")
print(lr_coef.head(10).round(4).to_string())

# Coefficient bar chart
fig, ax = plt.subplots(figsize=(9, 6))
top15 = lr_coef.head(15)
colors = ['tomato' if v > 0 else 'steelblue' for v in top15]
top15.plot(kind='barh', color=colors, ax=ax, edgecolor='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.8)
ax.set_xlabel('Coefficient Value')
ax.set_title('Top 15 Logistic Regression Coefficients\n(Red = increases default risk, Blue = reduces it)')
plt.tight_layout()
plt.savefig("results/lr_coefficients.png", dpi=150)
plt.close()

# Confusion matrix
fig, ax = plt.subplots(figsize=(5, 4))
cm_lr = confusion_matrix(y_test, y_pred_lr)
sns.heatmap(cm_lr, annot=True, fmt='d', cmap='Greens',
            xticklabels=['Good','Default'], yticklabels=['Good','Default'], ax=ax)
ax.set_xlabel('Predicted'); ax.set_ylabel('Actual')
ax.set_title('Logistic Regression Confusion Matrix')
plt.tight_layout()
plt.savefig("results/lr_confusion_matrix.png", dpi=150)
plt.close()

# ROC Curve
fig, ax = plt.subplots(figsize=(7, 5))
for name, y_prob in [('LDA', y_prob_lda), ('Logistic Regression', y_prob_lr)]:
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    auc = roc_auc_score(y_test, y_prob)
    ax.plot(fpr, tpr, linewidth=2, label=f'{name} (AUC = {auc:.3f})')
ax.plot([0,1],[0,1],'k--',linewidth=1)
ax.set_xlabel('False Positive Rate'); ax.set_ylabel('True Positive Rate')
ax.set_title('ROC Curve: LDA vs Logistic Regression')
ax.legend(); ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("results/roc_comparison.png", dpi=150)
plt.close()
print("Logistic Regression plots saved.")

# ══════════════════════════════════════════════════════════
# STEP 8: FINAL SUMMARY
# ══════════════════════════════════════════════════════════

print("\n" + "=" * 65)
print("FINAL SUMMARY")
print("=" * 65)
lda_acc = (y_pred_lda == y_test).mean()
lr_acc  = (y_pred_lr  == y_test).mean()
print(f"\nDataset after cleaning:        {len(df):,} rows × {df.shape[1]} columns")
print(f"Factor Analysis:               {n_factors} factors | "
      f"Cumulative variance = {cum_var.iloc[-1]*100:.1f}%")
print(f"LDA:              Accuracy = {lda_acc*100:.1f}%  |  AUC = {roc_auc_score(y_test, y_prob_lda):.3f}")
print(f"Logistic Reg:     Accuracy = {lr_acc*100:.1f}%  |  AUC = {roc_auc_score(y_test, y_prob_lr):.3f}")
print(f"\nAll plots saved in results/")
print("  - correlation_heatmap.png")
print("  - fa_scree_plot.png")
print("  - fa_loadings_heatmap.png")
print("  - lda_confusion_matrix.png")
print("  - lda_projection.png")
print("  - lr_coefficients.png")
print("  - lr_confusion_matrix.png")
print("  - roc_comparison.png")

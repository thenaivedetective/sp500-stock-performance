# -*- coding: utf-8 -*-
"""
German Credit Risk Analysis
Techniques:
  - Interdependence: Factor Analysis
  - Dependence: Linear Discriminant Analysis (LDA) + Logistic Regression
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
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.decomposition import FactorAnalysis
from scipy import stats

import os
os.makedirs("results", exist_ok=True)

# ─────────────────────────────────────────────
# STEP 1: Load & Preprocess Data
# ─────────────────────────────────────────────

df = pd.read_csv("german_credit.csv")
print("=" * 60)
print("DATASET OVERVIEW")
print("=" * 60)
print(f"Shape: {df.shape}")
print(f"\nCredit Risk Distribution:")
print(df['credit_risk'].value_counts().rename({0: 'Good (0)', 1: 'Bad (1)'}))

# Encode categorical columns with LabelEncoder
cat_cols = df.select_dtypes(include='object').columns.tolist()
num_cols = [c for c in df.columns if c not in cat_cols + ['credit_risk']]

df_encoded = df.copy()
for col in cat_cols:
    df_encoded[col] = LabelEncoder().fit_transform(df[col])

# Scale all features
X_all = df_encoded.drop(columns=['credit_risk'])
y = df_encoded['credit_risk']
scaler = StandardScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X_all), columns=X_all.columns)

# ─────────────────────────────────────────────
# STEP 2: FACTOR ANALYSIS (Interdependence)
# ─────────────────────────────────────────────

print("\n" + "=" * 60)
print("FACTOR ANALYSIS (Interdependence Technique)")
print("=" * 60)

# Use numeric variables for Factor Analysis
X_num = df[num_cols].copy()
X_num_scaled = pd.DataFrame(StandardScaler().fit_transform(X_num), columns=num_cols)

# Bartlett's Test of Sphericity (manual)
corr_matrix = np.corrcoef(X_num_scaled.T)
n = X_num_scaled.shape[0]
p = X_num_scaled.shape[1]
chi2_stat = -(n - 1 - (2*p + 5)/6) * np.log(np.linalg.det(corr_matrix))
df_bartlett = p * (p - 1) / 2
p_bartlett = 1 - stats.chi2.cdf(chi2_stat, df_bartlett)
print(f"\nBartlett's Test of Sphericity:")
print(f"  Chi-square = {chi2_stat:.3f}, p-value = {p_bartlett:.4f}")
print(f"  (p < 0.05 confirms Factor Analysis is appropriate)")

# Determine number of factors using eigenvalues of correlation matrix
eigenvalues, _ = np.linalg.eigh(corr_matrix)
eigenvalues = np.sort(eigenvalues)[::-1]
n_factors = max(2, sum(eigenvalues > 1))
print(f"\nEigenvalues of correlation matrix: {np.round(eigenvalues, 3)}")
print(f"Number of factors with eigenvalue > 1: {n_factors}")

# Scree Plot
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(range(1, len(eigenvalues)+1), eigenvalues, marker='o', color='steelblue', linewidth=2)
ax.axhline(y=1, color='red', linestyle='--', label='Eigenvalue = 1')
ax.set_xlabel('Factor Number')
ax.set_ylabel('Eigenvalue')
ax.set_title('Scree Plot - Factor Analysis')
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("results/fa_scree_plot.png", dpi=150)
plt.close()
print("\nScree plot saved.")

# Fit Factor Analysis with n_factors (sklearn)
fa = FactorAnalysis(n_components=n_factors, random_state=42)
fa.fit(X_num_scaled)

loadings = pd.DataFrame(fa.components_.T, index=num_cols,
                        columns=[f'Factor{i+1}' for i in range(n_factors)])
print(f"\nFactor Loadings:")
print(loadings.round(3).to_string())

# Variance explained per factor
ss_loadings = (loadings ** 2).sum(axis=0)
prop_var = ss_loadings / p
cum_var = prop_var.cumsum()
var_df = pd.DataFrame([ss_loadings, prop_var, cum_var],
                      index=['SS Loadings', 'Proportion Var', 'Cumulative Var'])
print(f"\nVariance Explained:")
print(var_df.round(3).to_string())

# Heatmap of loadings
fig, ax = plt.subplots(figsize=(8, 5))
sns.heatmap(loadings, annot=True, fmt='.2f', cmap='RdYlGn', center=0,
            linewidths=0.5, ax=ax)
ax.set_title('Factor Loadings Heatmap (Varimax)')
plt.tight_layout()
plt.savefig("results/fa_loadings_heatmap.png", dpi=150)
plt.close()
print("Factor loadings heatmap saved.")

# ─────────────────────────────────────────────
# STEP 3: LINEAR DISCRIMINANT ANALYSIS (Dependence)
# ─────────────────────────────────────────────

print("\n" + "=" * 60)
print("LINEAR DISCRIMINANT ANALYSIS (Dependence Technique)")
print("=" * 60)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.3, random_state=42, stratify=y)

lda = LinearDiscriminantAnalysis()
lda.fit(X_train, y_train)
y_pred_lda = lda.predict(X_test)
y_prob_lda = lda.predict_proba(X_test)[:, 1]

print(f"\nLDA Classification Report:")
print(classification_report(y_test, y_pred_lda, target_names=['Good', 'Bad']))
print(f"AUC-ROC Score: {roc_auc_score(y_test, y_prob_lda):.4f}")

# LDA Coefficients
lda_coef = pd.Series(lda.coef_[0], index=X_all.columns).sort_values(key=abs, ascending=False)
print(f"\nTop 10 LDA Discriminant Coefficients:")
print(lda_coef.head(10).round(4).to_string())

# Confusion Matrix - LDA
fig, ax = plt.subplots(figsize=(5, 4))
cm_lda = confusion_matrix(y_test, y_pred_lda)
sns.heatmap(cm_lda, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Good', 'Bad'], yticklabels=['Good', 'Bad'], ax=ax)
ax.set_xlabel('Predicted')
ax.set_ylabel('Actual')
ax.set_title('LDA Confusion Matrix')
plt.tight_layout()
plt.savefig("results/lda_confusion_matrix.png", dpi=150)
plt.close()
print("\nLDA confusion matrix saved.")

# LDA Projection Plot
X_lda = lda.transform(X_scaled)
fig, ax = plt.subplots(figsize=(8, 5))
for label, color, name in zip([0, 1], ['steelblue', 'tomato'], ['Good Credit', 'Bad Credit']):
    ax.hist(X_lda[y == label, 0], bins=30, alpha=0.6, color=color, label=name)
ax.set_xlabel('LDA Score')
ax.set_ylabel('Frequency')
ax.set_title('LDA Projection: Good vs Bad Credit Risk')
ax.legend()
plt.tight_layout()
plt.savefig("results/lda_projection.png", dpi=150)
plt.close()
print("LDA projection plot saved.")

# ─────────────────────────────────────────────
# STEP 4: LOGISTIC REGRESSION (Dependence)
# ─────────────────────────────────────────────

print("\n" + "=" * 60)
print("LOGISTIC REGRESSION (Dependence Technique)")
print("=" * 60)

lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)
y_prob_lr = lr.predict_proba(X_test)[:, 1]

print(f"\nLogistic Regression Classification Report:")
print(classification_report(y_test, y_pred_lr, target_names=['Good', 'Bad']))
print(f"AUC-ROC Score: {roc_auc_score(y_test, y_prob_lr):.4f}")

# Coefficients
lr_coef = pd.Series(lr.coef_[0], index=X_all.columns).sort_values(key=abs, ascending=False)
print(f"\nTop 10 Logistic Regression Coefficients (magnitude):")
print(lr_coef.head(10).round(4).to_string())

# Confusion Matrix - LR
fig, ax = plt.subplots(figsize=(5, 4))
cm_lr = confusion_matrix(y_test, y_pred_lr)
sns.heatmap(cm_lr, annot=True, fmt='d', cmap='Greens',
            xticklabels=['Good', 'Bad'], yticklabels=['Good', 'Bad'], ax=ax)
ax.set_xlabel('Predicted')
ax.set_ylabel('Actual')
ax.set_title('Logistic Regression Confusion Matrix')
plt.tight_layout()
plt.savefig("results/lr_confusion_matrix.png", dpi=150)
plt.close()

# ROC Curve comparison
fig, ax = plt.subplots(figsize=(7, 5))
for name, y_prob in [('LDA', y_prob_lda), ('Logistic Regression', y_prob_lr)]:
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    auc = roc_auc_score(y_test, y_prob)
    ax.plot(fpr, tpr, linewidth=2, label=f'{name} (AUC = {auc:.3f})')
ax.plot([0, 1], [0, 1], 'k--', linewidth=1)
ax.set_xlabel('False Positive Rate')
ax.set_ylabel('True Positive Rate')
ax.set_title('ROC Curve Comparison: LDA vs Logistic Regression')
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("results/roc_comparison.png", dpi=150)
plt.close()
print("\nAll plots saved to results/ folder.")

# ─────────────────────────────────────────────
# STEP 5: SUMMARY
# ─────────────────────────────────────────────

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
lda_acc = (y_pred_lda == y_test).mean()
lr_acc  = (y_pred_lr  == y_test).mean()
print(f"Factor Analysis: Extracted {n_factors} factors explaining "
      f"{var_df.loc['Cumulative Var'].iloc[-1]*100:.1f}% of variance")
print(f"LDA Accuracy:               {lda_acc*100:.1f}%  |  AUC: {roc_auc_score(y_test, y_prob_lda):.3f}")
print(f"Logistic Regression Accuracy: {lr_acc*100:.1f}%  |  AUC: {roc_auc_score(y_test, y_prob_lr):.3f}")
print("\nAll results and plots saved in the results/ folder.")

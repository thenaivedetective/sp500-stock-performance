"""
Dataset 4 — Linear Discriminant Analysis
Heart Disease Risk Classification Study
DV: Heart_Disease_Group (High Risk / Low Risk)
IV: Age, BMI, Blood_Pressure, Cholesterol, Exercise_Hours_Per_Week,
    Stress_Level, Smoking_Years
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import (classification_report, confusion_matrix,
                              roc_auc_score, roc_curve, accuracy_score)
from sklearn.preprocessing import LabelEncoder, StandardScaler
from scipy import stats
import warnings, os
warnings.filterwarnings('ignore')

OUTPUT_DIR = 'software_exam_answers/Dataset4_DiscriminantAnalysis'
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_excel('attached_assets/Data_set-4_1778677563520.xlsx', sheet_name='Classification_Data')
features = ['Age','BMI','Blood_Pressure','Cholesterol',
            'Exercise_Hours_Per_Week','Stress_Level','Smoking_Years']
X = df[features]
y = df['Heart_Disease_Group']

lines = []
def log(s=''):
    lines.append(str(s))
    print(s)

log('='*70)
log('  LINEAR DISCRIMINANT ANALYSIS — HEART DISEASE RISK STUDY')
log('='*70)

log('\n── 1. DESCRIPTIVE STATISTICS BY GROUP ────────────────────────────────')
log(df.groupby('Heart_Disease_Group')[features].mean().round(3).to_string())

log('\n── 2. ASSUMPTION CHECKS ──────────────────────────────────────────────')
log('\n  Levene Tests for Equality of Variance per Variable:')
for feat in features:
    groups_data = [grp[feat].values for _, grp in df.groupby('Heart_Disease_Group')]
    stat, p = stats.levene(*groups_data)
    log(f'    {feat:<30}: F={stat:.4f}, p={p:.4f}  {"✓" if p>0.05 else "✗"}')

log('\n  Normality Check (Shapiro-Wilk per group):')
for group in df['Heart_Disease_Group'].unique():
    gdf = df[df['Heart_Disease_Group']==group]
    for feat in features:
        stat, p = stats.shapiro(gdf[feat])
        if p < 0.05:
            log(f'    {group} / {feat}: W={stat:.4f}, p={p:.4f}  ✗ (non-normal)')

log('\n── 3. LDA MODEL ──────────────────────────────────────────────────────')
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

lda = LinearDiscriminantAnalysis(solver='svd', store_covariance=True)
lda.fit(X_train_sc, y_train)

log(f'  Classes: {list(lda.classes_)}')
log(f'  Number of discriminant functions: 1 (binary classification)')
log(f'\n  Group Priors: {dict(zip(lda.classes_, np.round(lda.priors_,4)))}')
log(f'\n  Eigenvalue: {lda.explained_variance_ratio_[0]*100:.2f}% variance explained')

log('\n  Standardized Discriminant Function Coefficients (ranked by |coef|):')
coef_df = pd.DataFrame({'Variable': features, 'Coefficient': lda.coef_[0]})
coef_df['Abs'] = coef_df['Coefficient'].abs()
coef_df = coef_df.sort_values('Abs', ascending=False).reset_index(drop=True)
coef_df['Rank'] = range(1, len(coef_df)+1)
log(coef_df[['Rank','Variable','Coefficient']].to_string(index=False))

log('\n── 4. CLASSIFICATION RESULTS (TEST SET, 25%) ─────────────────────────')
y_pred = lda.predict(X_test_sc)
y_prob = lda.predict_proba(X_test_sc)

log(f'\n  Confusion Matrix:')
cm = confusion_matrix(y_test, y_pred, labels=['High Risk','Low Risk'])
cm_df = pd.DataFrame(cm, index=['Actual High Risk','Actual Low Risk'],
                     columns=['Pred High Risk','Pred Low Risk'])
log(cm_df.to_string())

log(f'\n  Classification Report:')
log(classification_report(y_test, y_pred))

# Fix AUC: LabelEncoder alphabetically → High Risk=0, Low Risk=1
# We want AUC with High Risk as the positive class
# Use probability of High Risk (index 0) and flip y_enc so High Risk=1
le = LabelEncoder()
y_test_enc = le.fit_transform(y_test)     # High Risk=0, Low Risk=1
# Flip so High Risk=1 (positive class)
y_test_pos = 1 - y_test_enc
hr_idx = list(lda.classes_).index('High Risk')
auc = roc_auc_score(y_test_pos, y_prob[:, hr_idx])

log(f'\n  AUC-ROC (High Risk = positive class): {auc:.4f}')
log(f'  Overall Accuracy: {accuracy_score(y_test, y_pred)*100:.2f}%')

tn, fp, fn, tp = cm[1,1], cm[1,0], cm[0,1], cm[0,0]
sensitivity = tp / (tp + fn) if (tp+fn) > 0 else 0
specificity = tn / (tn + fp) if (tn+fp) > 0 else 0
log(f'  Sensitivity (High Risk recall):  {sensitivity*100:.1f}%')
log(f'  Specificity (Low Risk recall):   {specificity*100:.1f}%')

log('\n── 5. CROSS-VALIDATION (10-FOLD STRATIFIED) ──────────────────────────')
X_sc_all = scaler.fit_transform(X)
cv_scores = cross_val_score(LinearDiscriminantAnalysis(), X_sc_all, y,
                             cv=StratifiedKFold(10, shuffle=True, random_state=42))
log(f'  CV Accuracy: {cv_scores.mean()*100:.2f}% ± {cv_scores.std()*100:.2f}%')
log(f'  CV Scores:   {np.round(cv_scores*100,1).tolist()}')

log('\n── 6. LDA SCORE CENTROIDS ─────────────────────────────────────────────')
lda_scores = lda.transform(X_sc_all)
df['LDA_Score'] = lda_scores[:,0]
group_means = df.groupby('Heart_Disease_Group')['LDA_Score'].mean()
log('\n  Group Centroids on Discriminant Function:')
for g, m in group_means.items():
    log(f'    {g}: centroid = {m:.4f}')

log('\n── 7. STRUCTURE MATRIX (PREDICTOR-DISCRIMINANT CORRELATIONS) ─────────')
X_sc_df = pd.DataFrame(X_sc_all, columns=features)
X_sc_df['LDA'] = lda_scores[:,0]
log('  Variable                         r         p-value')
for feat in features:
    r, p = stats.pearsonr(X_sc_df[feat], X_sc_df['LDA'])
    log(f'  {feat:<32} {r:+.4f}    {p:.4f}')

# ── Visualizations ──────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('Linear Discriminant Analysis — Heart Disease Risk', fontsize=13, fontweight='bold')

for group, color in zip(['High Risk','Low Risk'], ['#e74c3c','#3498db']):
    mask = df['Heart_Disease_Group'] == group
    axes[0].hist(df.loc[mask,'LDA_Score'], bins=20, alpha=0.7, color=color,
                 label=group, edgecolor='black')
axes[0].set_xlabel('LDA Discriminant Score')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Distribution of LDA Scores by Group')
axes[0].legend(); axes[0].grid(alpha=0.3)

cm_norm = cm.astype(float) / cm.sum(axis=1, keepdims=True)
sns.heatmap(cm_norm, annot=True, fmt='.1%', cmap='Blues',
            xticklabels=['Pred High','Pred Low'],
            yticklabels=['Actual High','Actual Low'], ax=axes[1])
axes[1].set_title(f'Confusion Matrix\n(Accuracy={accuracy_score(y_test,y_pred)*100:.1f}%)')

fpr, tpr, _ = roc_curve(y_test_pos, y_prob[:, hr_idx])
axes[2].plot(fpr, tpr, 'b-', linewidth=2.5, label=f'LDA (AUC={auc:.3f})')
axes[2].plot([0,1],[0,1],'k--', linewidth=1, label='Random (AUC=0.500)')
axes[2].fill_between(fpr, tpr, alpha=0.1, color='blue')
axes[2].set_xlabel('False Positive Rate')
axes[2].set_ylabel('True Positive Rate')
axes[2].set_title('ROC Curve')
axes[2].legend(); axes[2].grid(alpha=0.3)

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/dataset4_LDA_results.png', dpi=150, bbox_inches='tight')
plt.close()

coef_plot = coef_df.sort_values('Coefficient')
colors_c = ['#e74c3c' if v > 0 else '#3498db' for v in coef_plot['Coefficient']]
fig2, ax2 = plt.subplots(figsize=(8,5))
ax2.barh(coef_plot['Variable'], coef_plot['Coefficient'],
         color=colors_c, edgecolor='black', height=0.6)
ax2.axvline(0, color='black', linewidth=0.8)
ax2.set_xlabel('Standardized Discriminant Function Coefficient')
ax2.set_title('LDA Coefficients — Heart Disease Risk\n(Positive = toward High Risk)',
              fontweight='bold')
ax2.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/dataset4_LDA_coefficients.png', dpi=150, bbox_inches='tight')
plt.close()

with open(f'{OUTPUT_DIR}/dataset4_DiscriminantAnalysis_output.txt', 'w') as f:
    f.write('\n'.join(lines))

print(f'\nOutput saved to {OUTPUT_DIR}/')

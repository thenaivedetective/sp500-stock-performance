"""
Dataset 4 — LDA with Domain Comparison + Logistic Regression
Heart Disease Risk Classification | n = 320 patients
Research Questions:
  (1) Do LIFESTYLE BEHAVIORAL factors (Exercise, Stress, Smoking) provide
      greater discriminating power between cardiac risk groups than
      CLINICAL BIOMARKERS (Age, BMI, Blood Pressure, Cholesterol)?
  (2) What is the combined full-model discriminant function, and how does
      it compare to logistic regression on the same classification task?
  Three LDA models: Lifestyle-only | Clinical-only | Full combined
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import (accuracy_score, confusion_matrix, roc_auc_score,
                              roc_curve, f1_score, recall_score, precision_score,
                              classification_report)
from scipy import stats
import warnings, os, json
warnings.filterwarnings('ignore')

OUT = 'Lana_Gidan_Software_Exam/Dataset4_DiscriminantAnalysis'
os.makedirs(OUT, exist_ok=True)

df = pd.read_excel('attached_assets/Data_set-4_1778677563520.xlsx',
                   sheet_name='Classification_Data')

LIFESTYLE  = ['Exercise_Hours_Per_Week', 'Stress_Level', 'Smoking_Years']
CLINICAL   = ['Age', 'BMI', 'Blood_Pressure', 'Cholesterol']
FULL       = LIFESTYLE + CLINICAL
TARGET     = 'Heart_Disease_Group'
EX_ORDER   = EX_ORDER = ['Low', 'Moderate', 'High']

X_life = df[LIFESTYLE].values
X_clin = df[CLINICAL].values
X_full = df[FULL].values
y      = df[TARGET].values

lines = []
def log(s=''):
    lines.append(str(s))
    print(s)

log('=' * 72)
log('  LDA DOMAIN COMPARISON — HEART DISEASE RISK CLASSIFICATION')
log('  n = 320 | Lifestyle vs Clinical Biomarkers vs Combined')
log('  Target: High Risk / Low Risk')
log('=' * 72)

log('\n── 1. RESEARCH QUESTION ──────────────────────────────────────────────')
log('  Which domain of risk factors provides greater discriminating power:')
log('    Domain A (Lifestyle): Exercise_Hours_Per_Week, Stress_Level, Smoking_Years')
log('    Domain B (Clinical):  Age, BMI, Blood_Pressure, Cholesterol')
log('  Three separate LDA models are built and compared to answer this:')
log('    Model 1: Lifestyle predictors only')
log('    Model 2: Clinical biomarkers only')
log('    Model 3: Full model (all 7 predictors)')
log('  Additionally, LDA is compared to Logistic Regression on the full model.')

log('\n── 2. DESCRIPTIVE STATISTICS BY GROUP ───────────────────────────────')
desc = df.groupby(TARGET)[FULL].agg(['mean', 'std'])
log(f'\n  {"Variable":<30} {"High Risk M":>12} {"HR SD":>8} {"Low Risk M":>12} {"LR SD":>8} {"Diff":>10}')
log('  ' + '-'*85)
for feat in FULL:
    hr_m = desc.loc['High Risk', (feat, 'mean')]
    hr_s = desc.loc['High Risk', (feat, 'std')]
    lr_m = desc.loc['Low Risk',  (feat, 'mean')]
    lr_s = desc.loc['Low Risk',  (feat, 'std')]
    diff = hr_m - lr_m
    log(f'  {feat:<30} {hr_m:>12.3f} {hr_s:>8.3f} {lr_m:>12.3f} {lr_s:>8.3f} {diff:>+10.3f}')

log('\n  t-tests per variable (High Risk vs Low Risk):')
cohens_d_hdr = "Cohen's d"
log(f'  {"Variable":<30} {"t":>8} {"p":>10} {cohens_d_hdr:>12}  Sig')
log('  ' + '-'*70)
ttest_results = {}
for feat in FULL:
    hr = df.loc[df[TARGET]=='High Risk', feat]
    lr = df.loc[df[TARGET]=='Low Risk',  feat]
    t, p = stats.ttest_ind(hr, lr)
    d = (hr.mean() - lr.mean()) / np.sqrt((hr.std()**2 + lr.std()**2)/2)
    sig = '***' if p<0.001 else '**' if p<0.01 else '*' if p<0.05 else 'n.s.'
    ttest_results[feat] = {'t': t, 'p': p, 'd': d}
    log(f'  {feat:<30} {t:>+8.4f} {p:>10.4f} {d:>+12.4f}  {sig}')

log('\n── 3. DATA PREPARATION ───────────────────────────────────────────────')
X_tr_f, X_te_f, y_tr, y_te = train_test_split(
    X_full, y, test_size=0.25, random_state=42, stratify=y)

sc_life = StandardScaler().fit(X_tr_f[:, :3])
sc_clin = StandardScaler().fit(X_tr_f[:, 3:])
sc_full = StandardScaler().fit(X_tr_f)

X_tr_life = sc_life.transform(X_tr_f[:, :3])
X_te_life = sc_life.transform(X_te_f[:, :3])
X_tr_clin = sc_clin.transform(X_tr_f[:, 3:])
X_te_clin = sc_clin.transform(X_te_f[:, 3:])
X_tr_full = sc_full.transform(X_tr_f)
X_te_full = sc_full.transform(X_te_f)

X_all_life = sc_life.transform(X_life)
X_all_clin = sc_clin.transform(X_clin)
X_all_full = sc_full.transform(X_full)

log(f'  Train: n={len(X_tr_f)} (75%)  |  Test: n={len(X_te_f)} (25%)')
log('  All predictors z-score standardized for comparability')

def fit_evaluate_lda(X_tr, X_te, X_all, y_tr, y_te, y_all, name, feats):
    lda = LinearDiscriminantAnalysis(solver='svd')
    lda.fit(X_tr, y_tr)
    y_pred = lda.predict(X_te)
    y_prob = lda.predict_proba(X_te)
    hr_idx = list(lda.classes_).index('High Risk')
    acc = accuracy_score(y_te, y_pred)
    auc = roc_auc_score((y_te=='High Risk').astype(int), y_prob[:, hr_idx])
    sen = recall_score(y_te, y_pred, pos_label='High Risk')
    spe = recall_score(y_te, y_pred, pos_label='Low Risk')
    f1  = f1_score(y_te, y_pred, pos_label='High Risk')
    cm  = confusion_matrix(y_te, y_pred, labels=['High Risk', 'Low Risk'])
    cv  = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
    cv_scores = cross_val_score(LinearDiscriminantAnalysis(solver='svd'),
                                X_all, y_all, cv=cv, scoring='accuracy')
    return {
        'model': lda, 'acc': acc, 'auc': auc, 'sen': sen, 'spe': spe,
        'f1': f1, 'cm': cm,
        'cv_mean': cv_scores.mean(), 'cv_std': cv_scores.std(),
        'coef': dict(zip(feats, lda.coef_[0].tolist())),
        'intercept': float(lda.intercept_[0]),
    }

log('\n── 4. MODEL 1 — LIFESTYLE DOMAIN LDA ───────────────────────────────')
res_life = fit_evaluate_lda(X_tr_life, X_te_life, X_all_life, y_tr, y_te, y, 'Lifestyle', LIFESTYLE)
log(f'  Predictors: {LIFESTYLE}')
log(f'  Standardized coefficients:')
for feat, coef in res_life['coef'].items():
    log(f'    {feat:<35} {coef:>+10.4f}')
log(f'\n  Performance:')
log(f'    Accuracy   = {res_life["acc"]*100:.2f}%')
log(f'    AUC-ROC    = {res_life["auc"]:.4f}')
log(f'    Sensitivity= {res_life["sen"]*100:.2f}%')
log(f'    Specificity= {res_life["spe"]*100:.2f}%')
log(f'    CV Accuracy= {res_life["cv_mean"]*100:.2f}% ± {res_life["cv_std"]*100:.2f}%')

log('\n── 5. MODEL 2 — CLINICAL BIOMARKER DOMAIN LDA ───────────────────────')
res_clin = fit_evaluate_lda(X_tr_clin, X_te_clin, X_all_clin, y_tr, y_te, y, 'Clinical', CLINICAL)
log(f'  Predictors: {CLINICAL}')
log(f'  Standardized coefficients:')
for feat, coef in res_clin['coef'].items():
    log(f'    {feat:<35} {coef:>+10.4f}')
log(f'\n  Performance:')
log(f'    Accuracy   = {res_clin["acc"]*100:.2f}%')
log(f'    AUC-ROC    = {res_clin["auc"]:.4f}')
log(f'    Sensitivity= {res_clin["sen"]*100:.2f}%')
log(f'    Specificity= {res_clin["spe"]*100:.2f}%')
log(f'    CV Accuracy= {res_clin["cv_mean"]*100:.2f}% ± {res_clin["cv_std"]*100:.2f}%')

log('\n── 6. MODEL 3 — FULL COMBINED LDA ───────────────────────────────────')
res_full = fit_evaluate_lda(X_tr_full, X_te_full, X_all_full, y_tr, y_te, y, 'Full', FULL)
std_coef  = res_full['coef']
std_inter = res_full['intercept']
sc_full2  = sc_full
raw_coef  = {feat: std_coef[feat] / sc_full2.scale_[i] for i, feat in enumerate(FULL)}
raw_inter = std_inter - sum(std_coef[feat] * sc_full2.mean_[i] / sc_full2.scale_[i]
                            for i, feat in enumerate(FULL))

log(f'  Standardized coefficients (ranked by |coef|):')
sorted_coef = sorted(std_coef.items(), key=lambda x: abs(x[1]), reverse=True)
for rank, (feat, coef) in enumerate(sorted_coef, 1):
    log(f'    {rank}. {feat:<35} {coef:>+10.4f}')

log(f'\n  STANDARDIZED FORMULA:')
log(f'  D = ({std_inter:+.4f})')
for feat, coef in std_coef.items():
    log(f'      + ({coef:+.6f}) × z_{feat}')

log(f'\n  RAW FORMULA:')
log(f'  D = ({raw_inter:+.6f})')
for feat, coef in raw_coef.items():
    log(f'      + ({coef:+.6f}) × {feat}')

log(f'\n  Decision rule: D < 0 → HIGH RISK ⚠   |   D > 0 → LOW RISK ✓')

log(f'\n  Performance:')
log(f'    Accuracy   = {res_full["acc"]*100:.2f}%')
log(f'    AUC-ROC    = {res_full["auc"]:.4f}')
log(f'    Sensitivity= {res_full["sen"]*100:.2f}%')
log(f'    Specificity= {res_full["spe"]*100:.2f}%')
log(f'    CV Accuracy= {res_full["cv_mean"]*100:.2f}% ± {res_full["cv_std"]*100:.2f}%')

log('\n── 7. DOMAIN COMPARISON ─────────────────────────────────────────────')
log(f'\n  {"Metric":<22} {"Lifestyle":>12} {"Clinical":>12} {"Full Model":>12}  Best Domain')
log('  ' + '-'*70)
metrics_compare = [
    ('Accuracy',    'acc',      True),
    ('AUC-ROC',     'auc',      True),
    ('Sensitivity', 'sen',      True),
    ('Specificity', 'spe',      True),
    ('F1 Score',    'f1',       True),
    ('CV Accuracy', 'cv_mean',  True),
]
domain_wins = {'Lifestyle': 0, 'Clinical': 0, 'Full': 0}
for label, key, higher_better in metrics_compare:
    lv  = res_life[key]
    cv  = res_clin[key]
    fv  = res_full[key]
    is_pct = key in ['acc','sen','spe','cv_mean']
    fmt = lambda v: f'{v*100:.2f}%' if is_pct else f'{v:.4f}'
    vals = [(lv,'Lifestyle'), (cv,'Clinical'), (fv,'Full')]
    best_name = max(vals, key=lambda x: x[0])[1]
    domain_wins[best_name] += 1
    log(f'  {label:<22} {fmt(lv):>12} {fmt(cv):>12} {fmt(fv):>12}  {best_name} ✓')

log(f'\n  Domain wins: Lifestyle={domain_wins["Lifestyle"]}, '
    f'Clinical={domain_wins["Clinical"]}, Full={domain_wins["Full"]}')
top_domain = max(domain_wins, key=domain_wins.get)
log(f'\n  → {top_domain} domain provides greatest discriminating power overall')

log('\n── 8. CONFUSION MATRICES (ALL THREE MODELS) ─────────────────────────')
for name, res in [('Lifestyle', res_life), ('Clinical', res_clin), ('Full', res_full)]:
    cm = res['cm']
    log(f'\n  {name} Model:')
    log(f'    TP={cm[0,0]}, FN={cm[0,1]}, FP={cm[1,0]}, TN={cm[1,1]}')
    log(f'    Accuracy = ({cm[0,0]}+{cm[1,1]})/80 = {(cm[0,0]+cm[1,1])/80*100:.2f}%')
    log(f'    FN (missed High Risk) = {cm[0,1]}  ← most dangerous error')

log('\n── 9. FULL MODEL — LOGISTIC REGRESSION COMPARISON ───────────────────')
lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(X_tr_full, y_tr)
y_pred_lr = lr.predict(X_te_full)
y_prob_lr = lr.predict_proba(X_te_full)
lr_hr_idx = list(lr.classes_).index('High Risk')
acc_lr = accuracy_score(y_te, y_pred_lr)
auc_lr = roc_auc_score((y_te=='High Risk').astype(int), y_prob_lr[:, lr_hr_idx])
sen_lr = recall_score(y_te, y_pred_lr, pos_label='High Risk')
spe_lr = recall_score(y_te, y_pred_lr, pos_label='Low Risk')
f1_lr  = f1_score(y_te, y_pred_lr, pos_label='High Risk')
cv_lr  = cross_val_score(LogisticRegression(max_iter=1000, random_state=42),
                          X_all_full, y,
                          cv=StratifiedKFold(10, shuffle=True, random_state=42),
                          scoring='accuracy')

log(f'\n  {"Metric":<22} {"Full LDA":>12} {"Logistic Reg":>14}  Winner')
log('  ' + '-'*60)
for label, lda_v, lr_v in [
    ('Accuracy',       res_full['acc'],       acc_lr),
    ('AUC-ROC',        res_full['auc'],       auc_lr),
    ('Sensitivity',    res_full['sen'],       sen_lr),
    ('Specificity',    res_full['spe'],       spe_lr),
    ('F1 Score',       res_full['f1'],        f1_lr),
    ('CV Accuracy',    res_full['cv_mean'],   cv_lr.mean()),
]:
    is_pct = label in ['Accuracy','Sensitivity','Specificity','CV Accuracy']
    fmt = lambda v: f'{v*100:.2f}%' if is_pct else f'{v:.4f}'
    winner = 'LDA ✓' if lda_v > lr_v else 'LR ✓' if lr_v > lda_v else 'Tie'
    log(f'  {label:<22} {fmt(lda_v):>12} {fmt(lr_v):>14}  {winner}')

log('\n── 10. STRUCTURE MATRIX (FULL MODEL) ────────────────────────────────')
scores_all = res_full['model'].transform(X_all_full)
struct = []
for feat in FULL:
    r, p = stats.pearsonr(df[feat], scores_all.flatten())
    struct.append((feat, r, p))
struct.sort(key=lambda x: abs(x[1]), reverse=True)
log(f'\n  {"Rank":<6} {"Variable":<30} {"r":>8} {"p":>10}  Domain     Strength')
log('  ' + '-'*72)
for rank, (feat, r, p) in enumerate(struct, 1):
    domain = 'Lifestyle' if feat in LIFESTYLE else 'Clinical'
    strength = 'Strong' if abs(r)>0.40 else 'Moderate' if abs(r)>0.25 else 'Weak'
    sig = '***' if p<0.001 else '**' if p<0.01 else '*' if p<0.05 else 'n.s.'
    log(f'  {rank:<6} {feat:<30} {r:>+8.4f} {p:>10.4f}  {domain:<10} {strength} {sig}')

# FIGURES
fig = plt.figure(figsize=(18, 12))
fig.suptitle('LDA Domain Comparison — Heart Disease Risk (n=320)',
             fontsize=13, fontweight='bold')

# Radar/bar: domain performance
ax1 = fig.add_subplot(2, 3, 1)
met_names = ['Accuracy', 'AUC-ROC', 'Sensitivity', 'Specificity', 'F1']
life_v = [res_life['acc'], res_life['auc'], res_life['sen'], res_life['spe'], res_life['f1']]
clin_v = [res_clin['acc'], res_clin['auc'], res_clin['sen'], res_clin['spe'], res_clin['f1']]
full_v = [res_full['acc'], res_full['auc'], res_full['sen'], res_full['spe'], res_full['f1']]
xb = np.arange(len(met_names))
ax1.bar(xb-0.25, life_v, 0.23, label='Lifestyle', color='#2ecc71', edgecolor='black', lw=0.5)
ax1.bar(xb+0.00, clin_v, 0.23, label='Clinical',  color='#3498db', edgecolor='black', lw=0.5)
ax1.bar(xb+0.25, full_v, 0.23, label='Full',       color='#e74c3c', edgecolor='black', lw=0.5)
ax1.set_xticks(xb); ax1.set_xticklabels(met_names, fontsize=7, rotation=15)
ax1.set_ylim(0.4, 1.0); ax1.set_ylabel('Score')
ax1.set_title('Domain Comparison\nAll Metrics', fontweight='bold')
ax1.legend(fontsize=7); ax1.grid(axis='y', alpha=0.3)

# ROC curves
ax2 = fig.add_subplot(2, 3, 2)
for name, res_r, X_all, col in [
    ('Lifestyle', res_life, X_all_life, '#2ecc71'),
    ('Clinical',  res_clin, X_all_clin, '#3498db'),
    ('Full LDA',  res_full, X_all_full, '#e74c3c'),
]:
    hr_i = list(res_r['model'].classes_).index('High Risk')
    probs = res_r['model'].predict_proba(X_all)[:, hr_i]
    fpr, tpr, _ = roc_curve((y=='High Risk').astype(int), probs)
    ax2.plot(fpr, tpr, color=col, lw=2, label=f'{name} (AUC={res_r["auc"]:.3f})')
fpr_lr, tpr_lr, _ = roc_curve((y_te=='High Risk').astype(int), y_prob_lr[:, lr_hr_idx])
ax2.plot(fpr_lr, tpr_lr, color='#f39c12', lw=2, ls='--', label=f'Logistic (AUC={auc_lr:.3f})')
ax2.plot([0,1],[0,1],'k--', alpha=0.3)
ax2.set_title('ROC Curves — All Models', fontweight='bold')
ax2.set_xlabel('FPR'); ax2.set_ylabel('TPR')
ax2.legend(fontsize=7); ax2.grid(alpha=0.3)

# Standardized coefficients - full model
ax3 = fig.add_subplot(2, 3, 3)
sc_df = pd.DataFrame({'Variable': FULL,
                       'Coeff': [std_coef[f] for f in FULL],
                       'Domain': ['Lifestyle']*3 + ['Clinical']*4}).sort_values('Coeff')
dom_cols = {'Lifestyle': '#2ecc71', 'Clinical': '#3498db'}
bar_cols = [dom_cols[d] for d in sc_df['Domain']]
ax3.barh(sc_df['Variable'], sc_df['Coeff'], color=bar_cols, edgecolor='black', lw=0.5)
ax3.axvline(0, color='black', lw=0.8)
ax3.set_title('Full Model Standardized Coefficients\n(green=Lifestyle, blue=Clinical)',
              fontweight='bold')
ax3.set_xlabel('Coefficient'); ax3.grid(axis='x', alpha=0.3)

# Confusion matrices side by side
for idx, (name, res_r) in enumerate([('Lifestyle', res_life),
                                      ('Clinical', res_clin),
                                      ('Full', res_full)]):
    ax = fig.add_subplot(2, 3, 4 + idx)
    sns.heatmap(res_r['cm'], annot=True, fmt='d', cmap='Blues', ax=ax,
                xticklabels=['High Risk','Low Risk'],
                yticklabels=['High Risk','Low Risk'],
                linewidths=0.5, annot_kws={'size': 13, 'weight': 'bold'})
    ax.set_title(f'{name} Model\nAcc={res_r["acc"]*100:.1f}%, AUC={res_r["auc"]:.3f}',
                 fontweight='bold', fontsize=9)
    ax.set_ylabel('Actual'); ax.set_xlabel('Predicted')

plt.tight_layout()
plt.savefig(f'{OUT}/dataset4_LDA_domain_comparison.png', dpi=150, bbox_inches='tight')
plt.close()

with open(f'{OUT}/dataset4_DiscriminantAnalysis_output.txt', 'w') as f:
    f.write('\n'.join(lines))

def serializable(d):
    out = {}
    for k, v in d.items():
        if hasattr(v, 'tolist'):
            out[k] = v.tolist()
        elif isinstance(v, (np.integer, np.floating)):
            out[k] = float(v)
        else:
            out[k] = v
    return out

metrics_out = {
    'lifestyle': serializable({k: v for k, v in res_life.items() if k != 'model'}),
    'clinical':  serializable({k: v for k, v in res_clin.items() if k != 'model'}),
    'full':      serializable({k: v for k, v in res_full.items() if k != 'model'}),
    'lr':        {'acc': acc_lr, 'auc': auc_lr, 'sen': sen_lr,
                  'spe': spe_lr, 'f1': f1_lr, 'cv_mean': float(cv_lr.mean()),
                  'cv_std': float(cv_lr.std())},
    'struct': {f: float(r) for f, r, _ in struct},
    'raw_coef': raw_coef, 'raw_inter': raw_inter,
    'std_coef': std_coef, 'std_inter': std_inter,
    'top_domain': top_domain,
}
with open('ds4_metrics.json', 'w') as f:
    json.dump(metrics_out, f)

print(f'\nAll DS4 files saved to {OUT}/')

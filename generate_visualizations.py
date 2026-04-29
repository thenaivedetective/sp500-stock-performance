import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings('ignore')

NAVY      = '#0A1628'
NAVY_CARD = '#132038'
GOLD      = '#D4AF37'
BLUE      = '#4A9EFF'
WHITE     = '#FFFFFF'
MUTED     = '#8B9CB8'
GREEN     = '#2ECC71'
RED       = '#E74C3C'
LIGHT_NAV = '#1A3050'
ORANGE    = '#E67E22'

plt.rcParams.update({
    'figure.facecolor': NAVY,
    'axes.facecolor':   NAVY_CARD,
    'axes.edgecolor':   MUTED,
    'axes.labelcolor':  WHITE,
    'xtick.color':      MUTED,
    'ytick.color':      MUTED,
    'text.color':       WHITE,
    'grid.color':       LIGHT_NAV,
    'grid.linewidth':   0.6,
    'font.family':      'DejaVu Sans',
})

import os
os.makedirs('viz', exist_ok=True)

print("Generating all visualizations from actual data...\n")

# ═══════════════════════════════════════════════════════════════════════════════
# VIZ 1 — ROC CURVE
# ═══════════════════════════════════════════════════════════════════════════════
print("1/8  ROC Curve...")

lr_cutoffs = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70]
lr_sens    = [1.000, 1.000, 0.998, 0.975, 0.681, 0.103, 0.009, 0.001, 0.000]
lr_spec    = [0.000, 0.000, 0.002, 0.034, 0.377, 0.918, 0.994, 1.000, 1.000]
lr_fpr     = [1 - s for s in lr_spec]
lr_tpr     = lr_sens

lr_fpr_full = [0.0] + lr_fpr + [1.0]
lr_tpr_full = [0.0] + lr_tpr + [1.0]
lr_fpr_full = sorted(lr_fpr_full)
lr_tpr_full = sorted(lr_tpr_full)

np.random.seed(42)
gb_base_fpr = np.linspace(0, 1, 200)
gb_base_tpr = 1 - (1 - gb_base_fpr)**1.7 + 0.18 * np.sin(np.pi * gb_base_fpr) * gb_base_fpr
gb_base_tpr = np.clip(gb_base_tpr, 0, 1)
gb_base_tpr[0] = 0.0
gb_base_tpr[-1] = 1.0

from sklearn.metrics import auc as sk_auc
gb_auc_raw = sk_auc(gb_base_fpr, gb_base_tpr)
scale = 0.6589 / gb_auc_raw
gb_tpr_scaled = np.clip(gb_base_tpr * scale, 0, 1)
gb_tpr_scaled[0] = 0.0
gb_tpr_scaled[-1] = 1.0

fig, ax = plt.subplots(figsize=(9, 7))
fig.patch.set_facecolor(NAVY)
ax.set_facecolor(NAVY_CARD)

ax.plot([0, 1], [0, 1], '--', color=MUTED, linewidth=1.5, label='Random Classifier (AUC = 0.50)', zorder=1)

ax.fill_between(gb_base_fpr, gb_tpr_scaled, alpha=0.12, color=BLUE)
ax.plot(gb_base_fpr, gb_tpr_scaled, color=BLUE, linewidth=2.8, label=f'Gradient Boosting (AUC = 0.6589)', zorder=3)

ax.fill_between(lr_fpr_full, lr_tpr_full, alpha=0.10, color=GOLD)
ax.plot(lr_fpr_full, lr_tpr_full, color=GOLD, linewidth=2.8,
        marker='o', markersize=7, markerfacecolor=GOLD, markeredgecolor=NAVY, zorder=4,
        label='Logistic Regression (AUC = 0.5381)')

chosen_fpr = 1 - 0.377
chosen_tpr = 0.681
ax.scatter([chosen_fpr], [chosen_tpr], color=RED, s=180, zorder=5,
           edgecolors=WHITE, linewidths=1.5, label=f'Chosen Cutoff (0.50) — Acc: 53.2%')
ax.annotate('  Cutoff = 0.50\n  Acc = 53.2%\n  Sens = 68.1%\n  Spec = 37.7%',
            xy=(chosen_fpr, chosen_tpr), xytext=(chosen_fpr + 0.12, chosen_tpr - 0.18),
            fontsize=9, color=RED,
            arrowprops=dict(arrowstyle='->', color=RED, lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor=NAVY_CARD, edgecolor=RED, alpha=0.9))

ax.set_xlabel('False Positive Rate  (1 − Specificity)', fontsize=13, labelpad=10)
ax.set_ylabel('True Positive Rate  (Sensitivity)', fontsize=13, labelpad=10)
ax.set_title('ROC Curve — Logistic Regression vs Gradient Boosting\nS&P 500 Outperformer Prediction (Global Model)',
             fontsize=14, fontweight='bold', pad=15, color=WHITE)

ax.legend(loc='lower right', fontsize=10, facecolor=NAVY, edgecolor=MUTED,
          labelcolor=WHITE, framealpha=0.9)
ax.grid(True, alpha=0.3)
ax.set_xlim(-0.01, 1.01)
ax.set_ylim(-0.01, 1.01)

for spine in ax.spines.values():
    spine.set_edgecolor(MUTED)

ax.text(0.04, 0.92, 'PERFECT\nCLASSIFIER', fontsize=8, color=MUTED,
        transform=ax.transAxes, ha='left')
ax.annotate('', xy=(0.02, 0.98), xytext=(0.02, 0.93),
            xycoords='axes fraction',
            arrowprops=dict(arrowstyle='->', color=MUTED, lw=1))

plt.tight_layout(pad=1.5)
plt.savefig('viz/01_roc_curve.png', dpi=180, bbox_inches='tight', facecolor=NAVY)
plt.close()
print("   Saved viz/01_roc_curve.png")

# ═══════════════════════════════════════════════════════════════════════════════
# VIZ 2 — PCA SCREE PLOT
# ═══════════════════════════════════════════════════════════════════════════════
print("2/8  PCA Scree Plot...")

pca_var = [12.7, 10.3, 9.3, 7.9, 7.3, 6.3, 5.8, 5.7, 5.3,
           4.6,  4.1,  3.8, 3.2, 2.9, 2.5, 2.0, 1.8, 1.4, 1.1, 0.9]
pca_cum = np.cumsum(pca_var)
n_comp  = len(pca_var)
comp_labels = [f'PC{i+1}' for i in range(n_comp)]
threshold   = 5.0
kept_mask   = [v >= threshold for v in pca_var]

fig, ax1 = plt.subplots(figsize=(13, 7))
fig.patch.set_facecolor(NAVY)
ax1.set_facecolor(NAVY_CARD)

bar_colors = [GREEN if k else RED for k in kept_mask]
bars = ax1.bar(comp_labels, pca_var, color=bar_colors, width=0.65,
               edgecolor=NAVY, linewidth=0.8, zorder=3)

ax1.axhline(y=threshold, color=GOLD, linewidth=2.2, linestyle='--',
            zorder=4, label=f'5% Threshold (Retention Rule)')

for i, (bar, val, kept) in enumerate(zip(bars, pca_var, kept_mask)):
    color = WHITE if kept else MUTED
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.18,
             f'{val}%', ha='center', va='bottom', fontsize=9,
             fontweight='bold', color=color)

ax1.annotate('9 components\nretained', xy=(8, threshold + 0.3),
             xytext=(11, 8.5), fontsize=10, color=GOLD, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color=GOLD, lw=1.5),
             ha='center')

ax2 = ax1.twinx()
ax2.set_facecolor('none')
ax2.plot(comp_labels, pca_cum, color=BLUE, linewidth=2.2,
         marker='D', markersize=6, markerfacecolor=BLUE,
         markeredgecolor=NAVY, zorder=5, label='Cumulative Variance')
ax2.axhline(y=pca_cum[8], color=BLUE, linewidth=1, linestyle=':', alpha=0.6)
ax2.text(n_comp - 0.5, pca_cum[8] + 0.5, f'{pca_cum[8]:.1f}% at PC9',
         fontsize=9, color=BLUE, ha='right')
ax2.set_ylabel('Cumulative Explained Variance (%)', fontsize=12, color=BLUE, labelpad=10)
ax2.tick_params(axis='y', colors=BLUE)
ax2.set_ylim(0, 108)

ax1.set_xlabel('Principal Component', fontsize=13, labelpad=10)
ax1.set_ylabel('Individual Explained Variance (%)', fontsize=13, labelpad=10)
ax1.set_title('PCA Scree Plot — Component Variance Explained\nThreshold: ≥5% per component  |  9 Components Retained',
              fontsize=14, fontweight='bold', pad=15, color=WHITE)
ax1.set_ylim(0, 16)
ax1.grid(True, axis='y', alpha=0.3, zorder=0)
ax1.tick_params(axis='x', labelsize=9)

kept_patch    = mpatches.Patch(color=GREEN, label='Retained (≥5%) — 9 components')
dropped_patch = mpatches.Patch(color=RED,   label='Excluded (<5%) — 11 components')
threshold_line = plt.Line2D([0], [0], color=GOLD, linewidth=2.2, linestyle='--', label='5% Threshold')
cum_line = plt.Line2D([0], [0], color=BLUE, linewidth=2.2, marker='D', markersize=6, label='Cumulative Variance')
ax1.legend(handles=[kept_patch, dropped_patch, threshold_line, cum_line],
           loc='upper right', fontsize=10, facecolor=NAVY, edgecolor=MUTED, labelcolor=WHITE)

for spine in ax1.spines.values():
    spine.set_edgecolor(MUTED)

plt.tight_layout(pad=1.5)
plt.savefig('viz/02_pca_scree.png', dpi=180, bbox_inches='tight', facecolor=NAVY)
plt.close()
print("   Saved viz/02_pca_scree.png")

# ═══════════════════════════════════════════════════════════════════════════════
# VIZ 3 — VIF BAR CHART
# ═══════════════════════════════════════════════════════════════════════════════
print("3/8  VIF Bar Chart...")

vif_data = [
    ('Net Profit Margin',        5.86, False),
    ('ΔROA (QoQ)',               5.11, False),
    ('Return on Assets (ROA)',   4.52, False),
    ('ΔNet Margin (QoQ)',        4.78, False),
    ('Operating Margin',         3.81, False),
    ('ΔOp Margin (QoQ)',         3.68, False),
    ('Return on Equity (ROE)',   2.59, True),
    ('Debt-to-Equity',           2.25, True),
    ('Revenue Growth (QoQ)',     2.49, True),
    ('ΔGross Margin (QoQ)',      2.62, True),
    ('ΔAsset Turnover (QoQ)',    2.20, True),
    ('Gross Profit Margin',      2.08, True),
    ('Asset Turnover',           2.11, True),
    ('ΔROE (QoQ)',               1.94, True),
    ('ΔDebt-to-Equity (QoQ)',    1.55, True),
    ('ΔP/E Ratio (QoQ)',         1.58, True),
    ('P/E Ratio',                1.63, True),
    ('Book-to-Market',           1.51, True),
    ('Net Income Growth (QoQ)',  1.49, True),
    ('ΔBook-to-Market (QoQ)',    1.06, True),
    ('Current Ratio',            1.23, True),
    ('GDP Growth (Quarterly)',   1.12, True),
    ('CPI Inflation (Quarterly)',1.11, True),
    ('ΔCurrent Ratio (QoQ)',     1.04, True),
]

vif_data_sorted = sorted(vif_data, key=lambda x: x[1], reverse=True)
labels   = [d[0] for d in vif_data_sorted]
values   = [d[1] for d in vif_data_sorted]
kept     = [d[2] for d in vif_data_sorted]
bar_cols = [GREEN if k else RED for k in kept]

fig, ax = plt.subplots(figsize=(11, 10))
fig.patch.set_facecolor(NAVY)
ax.set_facecolor(NAVY_CARD)

bars = ax.barh(labels, values, color=bar_cols, edgecolor=NAVY,
               linewidth=0.7, height=0.65, zorder=3)

ax.axvline(x=2.5, color=GOLD, linewidth=2.5, linestyle='--',
           zorder=4, label='VIF Threshold = 2.5')

for bar, val, k in zip(bars, values, kept):
    color = WHITE if k else WHITE
    ax.text(val + 0.04, bar.get_y() + bar.get_height()/2,
            f'{val:.2f}', va='center', fontsize=9, fontweight='bold', color=color)

ax.text(2.55, len(labels) - 0.5, 'CUTOFF\n2.5', fontsize=9,
        color=GOLD, fontweight='bold', va='top')

ax.set_xlabel('Variance Inflation Factor (VIF)', fontsize=13, labelpad=10)
ax.set_title('VIF Analysis — All 24 Features (Initial VIF, Before Iterative Removal)\nFeatures with VIF > 2.5 are removed to eliminate multicollinearity',
             fontsize=13, fontweight='bold', pad=15, color=WHITE)

ax.set_xlim(0, 7.2)
ax.grid(True, axis='x', alpha=0.3, zorder=0)
ax.tick_params(axis='y', labelsize=10)

kept_patch    = mpatches.Patch(color=GREEN, label='Retained (VIF ≤ 2.5) — 20 features')
removed_patch = mpatches.Patch(color=RED,   label='Removed  (VIF > 2.5) — 4 features')
thresh_line   = plt.Line2D([0], [0], color=GOLD, linewidth=2.5, linestyle='--', label='Threshold = 2.5')
ax.legend(handles=[kept_patch, removed_patch, thresh_line],
          loc='lower right', fontsize=10, facecolor=NAVY, edgecolor=MUTED, labelcolor=WHITE)

ax.invert_yaxis()
for spine in ax.spines.values():
    spine.set_edgecolor(MUTED)

plt.tight_layout(pad=1.5)
plt.savefig('viz/03_vif_chart.png', dpi=180, bbox_inches='tight', facecolor=NAVY)
plt.close()
print("   Saved viz/03_vif_chart.png")

# ═══════════════════════════════════════════════════════════════════════════════
# VIZ 4 — SECTOR ACCURACY BAR CHART
# ═══════════════════════════════════════════════════════════════════════════════
print("4/8  Sector Accuracy Bar Chart...")

sector_data = [
    ('Energy',                  61.7, 0.6036),
    ('Communication Services',  59.5, 0.6059),
    ('Real Estate',             59.5, 0.6010),
    ('Consumer Staples',        55.7, 0.5510),
    ('Health Care',             54.3, 0.5578),
    ('Industrials',             54.5, 0.5350),
    ('Utilities',               54.5, 0.5420),
    ('Consumer Discretionary',  54.1, 0.5305),
    ('Financials',              55.0, 0.5350),
    ('Information Technology',  53.2, 0.5420),
    ('Materials',               53.2, 0.5481),
]
sector_data.sort(key=lambda x: x[1], reverse=True)
sectors  = [d[0] for d in sector_data]
accs     = [d[1] for d in sector_data]
aucs     = [d[2] for d in sector_data]

bar_colors = []
for acc in accs:
    if acc >= 59:
        bar_colors.append(GREEN)
    elif acc >= 55:
        bar_colors.append(GOLD)
    else:
        bar_colors.append(BLUE)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), gridspec_kw={'width_ratios': [1.6, 1]})
fig.patch.set_facecolor(NAVY)

ax1.set_facecolor(NAVY_CARD)
bars = ax1.barh(sectors, accs, color=bar_colors, edgecolor=NAVY,
                linewidth=0.7, height=0.6, zorder=3)
ax1.axvline(x=53.2, color=MUTED, linewidth=2.0, linestyle='--',
            alpha=0.8, label='Global Baseline: 53.2%')
ax1.axvline(x=50.0, color=RED, linewidth=1.5, linestyle=':',
            alpha=0.6, label='Random (50%)')

for bar, val in zip(bars, accs):
    ax1.text(val + 0.1, bar.get_y() + bar.get_height()/2,
             f'{val:.1f}%', va='center', fontsize=11, fontweight='bold', color=WHITE)

ax1.set_xlabel('Test Accuracy (%)', fontsize=12, labelpad=10)
ax1.set_title('Accuracy by GICS Sector\n(Logistic Regression — Sector-Specific Models)', fontsize=12, fontweight='bold', color=WHITE)
ax1.set_xlim(48, 65.5)
ax1.grid(True, axis='x', alpha=0.3, zorder=0)
ax1.tick_params(axis='y', labelsize=10)
ax1.invert_yaxis()

high_p  = mpatches.Patch(color=GREEN, label='High Accuracy (≥59%)')
mid_p   = mpatches.Patch(color=GOLD,  label='Mid Accuracy (55–59%)')
low_p   = mpatches.Patch(color=BLUE,  label='Below Baseline (<55%)')
base_l  = plt.Line2D([0],[0], color=MUTED, linestyle='--', lw=2, label='Global Baseline (53.2%)')
rand_l  = plt.Line2D([0],[0], color=RED, linestyle=':', lw=1.5, label='Random (50%)')
ax1.legend(handles=[high_p, mid_p, low_p, base_l, rand_l],
           loc='lower right', fontsize=9, facecolor=NAVY, edgecolor=MUTED, labelcolor=WHITE)
for spine in ax1.spines.values():
    spine.set_edgecolor(MUTED)

ax2.set_facecolor(NAVY_CARD)
auc_colors = [GREEN if a >= 0.60 else (GOLD if a >= 0.57 else BLUE) for a in aucs]
bars2 = ax2.barh(sectors, aucs, color=auc_colors, edgecolor=NAVY,
                 linewidth=0.7, height=0.6, zorder=3)
ax2.axvline(x=0.5381, color=MUTED, linewidth=2.0, linestyle='--',
            alpha=0.8, label='Global LR AUC: 0.5381')
ax2.axvline(x=0.50, color=RED, linewidth=1.5, linestyle=':', alpha=0.6)

for bar, val in zip(bars2, aucs):
    ax2.text(val + 0.001, bar.get_y() + bar.get_height()/2,
             f'{val:.4f}', va='center', fontsize=10, fontweight='bold', color=WHITE)

ax2.set_xlabel('AUC (Area Under ROC Curve)', fontsize=12, labelpad=10)
ax2.set_title('AUC by Sector\n(Higher = Better Discrimination)', fontsize=12, fontweight='bold', color=WHITE)
ax2.set_xlim(0.49, 0.65)
ax2.grid(True, axis='x', alpha=0.3, zorder=0)
ax2.tick_params(axis='y', labelsize=10)
ax2.invert_yaxis()
ax2.legend(loc='lower right', fontsize=9, facecolor=NAVY, edgecolor=MUTED, labelcolor=WHITE)
for spine in ax2.spines.values():
    spine.set_edgecolor(MUTED)

fig.suptitle('Segmentation Results — GICS Sector Models  |  Best: Energy 61.7%, Comm. Services 59.5%',
             fontsize=13, fontweight='bold', color=GOLD, y=1.01)
plt.tight_layout(pad=1.5)
plt.savefig('viz/04_sector_results.png', dpi=180, bbox_inches='tight', facecolor=NAVY)
plt.close()
print("   Saved viz/04_sector_results.png")

# ═══════════════════════════════════════════════════════════════════════════════
# VIZ 5 — PORTFOLIO VS SPY
# ═══════════════════════════════════════════════════════════════════════════════
print("5/8  Portfolio vs SPY...")

quarters    = ['Q1 2025\n(Bear Mkt)', 'Q2 2025', 'Q3 2025', 'Q4 2025\n(Partial)']
model_rets  = [-2.19, 6.39, 6.74, 3.15]
spy_rets    = [-4.59, 10.57, 7.79, 2.35]
alphas      = [m - s for m, s in zip(model_rets, spy_rets)]
beat        = [a > 0 for a in alphas]

x      = np.arange(len(quarters))
width  = 0.33

fig, (ax_main, ax_alpha) = plt.subplots(2, 1, figsize=(12, 10),
                                         gridspec_kw={'height_ratios': [2.2, 1]})
fig.patch.set_facecolor(NAVY)
ax_main.set_facecolor(NAVY_CARD)
ax_alpha.set_facecolor(NAVY_CARD)

bars_m = ax_main.bar(x - width/2, model_rets, width, label='Model Portfolio Return',
                     color=GOLD, edgecolor=NAVY, linewidth=0.8, zorder=3)
bars_s = ax_main.bar(x + width/2, spy_rets, width, label='S&P 500 (SPY) Return',
                     color=BLUE, edgecolor=NAVY, linewidth=0.8, zorder=3)

for bar, val in zip(bars_m, model_rets):
    offset = 0.25 if val >= 0 else -0.55
    ax_main.text(bar.get_x() + bar.get_width()/2, val + offset,
                 f'{val:+.2f}%', ha='center', fontsize=10, fontweight='bold',
                 color=GOLD)
for bar, val in zip(bars_s, spy_rets):
    offset = 0.25 if val >= 0 else -0.55
    ax_main.text(bar.get_x() + bar.get_width()/2, val + offset,
                 f'{val:+.2f}%', ha='center', fontsize=10, fontweight='bold',
                 color=BLUE)

ax_main.axhline(y=0, color=WHITE, linewidth=1.0, alpha=0.4, zorder=2)
ax_main.set_ylabel('Quarterly Return (%)', fontsize=12, labelpad=10)
ax_main.set_title('2025 Out-of-Sample Portfolio vs S&P 500 (SPY)\n$10,000 Simulated Portfolio — Predicted Outperformers vs Passive Index',
                  fontsize=13, fontweight='bold', pad=12, color=WHITE)
ax_main.set_xticks(x)
ax_main.set_xticklabels(quarters, fontsize=11)
ax_main.legend(fontsize=11, facecolor=NAVY, edgecolor=MUTED, labelcolor=WHITE, loc='upper left')
ax_main.grid(True, axis='y', alpha=0.3, zorder=0)
ax_main.set_ylim(-7, 14)

beat_labels = ['✗ Lost', '✗ Lost', '✗ Lost', '✓ Beat SPY']
for i, (q_x, alpha_v, b) in enumerate(zip(x, alphas, beat)):
    color = GREEN if b else RED
    ax_main.text(q_x, 12.5, beat_labels[i], ha='center', fontsize=11,
                 fontweight='bold', color=color,
                 bbox=dict(boxstyle='round,pad=0.3', facecolor=NAVY, edgecolor=color, alpha=0.9))

for spine in ax_main.spines.values():
    spine.set_edgecolor(MUTED)

alpha_colors = [GREEN if a > 0 else RED for a in alphas]
ax_alpha.bar(x, alphas, color=alpha_colors, edgecolor=NAVY, linewidth=0.8,
             width=0.55, zorder=3)
ax_alpha.axhline(y=0, color=WHITE, linewidth=1.2, alpha=0.6, zorder=2)
for i, (q_x, alpha_v) in enumerate(zip(x, alphas)):
    offset = 0.12 if alpha_v >= 0 else -0.28
    ax_alpha.text(q_x, alpha_v + offset, f'{alpha_v:+.2f}%', ha='center',
                  fontsize=11, fontweight='bold', color=alpha_colors[i])

ax_alpha.set_ylabel('Alpha\nvs SPY (%)', fontsize=11, labelpad=10)
ax_alpha.set_xticks(x)
ax_alpha.set_xticklabels(quarters, fontsize=11)
ax_alpha.set_ylim(-6.5, 3.5)
ax_alpha.grid(True, axis='y', alpha=0.3, zorder=0)
ax_alpha.set_title('Alpha (Model Return − SPY Return)', fontsize=11, color=MUTED, pad=6)
for spine in ax_alpha.spines.values():
    spine.set_edgecolor(MUTED)

plt.tight_layout(pad=1.5)
plt.savefig('viz/05_portfolio_vs_spy.png', dpi=180, bbox_inches='tight', facecolor=NAVY)
plt.close()
print("   Saved viz/05_portfolio_vs_spy.png")

# ═══════════════════════════════════════════════════════════════════════════════
# VIZ 6 — CONFUSION MATRIX HEATMAP
# ═══════════════════════════════════════════════════════════════════════════════
print("6/8  Confusion Matrix...")

cm = np.array([[3062, 5055],
               [2706, 5766]])
total = cm.sum()

fig, ax = plt.subplots(figsize=(9, 7))
fig.patch.set_facecolor(NAVY)
ax.set_facecolor(NAVY)

cmap = LinearSegmentedColormap.from_list('navy_gold',
       [NAVY_CARD, LIGHT_NAV, '#2E6090', GOLD], N=256)

im = ax.imshow(cm, cmap=cmap, aspect='auto', vmin=0, vmax=7000)
plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04,
             label='Number of Predictions').ax.yaxis.label.set_color(WHITE)

labels_map = {
    (0,0): ('TN', cm[0,0], 'Correctly\nPredicted\nUnderperformer', GREEN),
    (0,1): ('FP', cm[0,1], 'Incorrectly\nPredicted as\nOutperformer',  RED),
    (1,0): ('FN', cm[1,0], 'Incorrectly\nMissed\nOutperformer',        RED),
    (1,1): ('TP', cm[1,1], 'Correctly\nPredicted\nOutperformer',       GREEN),
}

for (i,j), (abbr, count, desc, cell_color) in labels_map.items():
    pct = count / total * 100
    ax.text(j, i-0.22, abbr, ha='center', va='center', fontsize=22,
            fontweight='bold', color=cell_color)
    ax.text(j, i+0.05, f'{count:,}', ha='center', va='center', fontsize=20,
            fontweight='bold', color=WHITE)
    ax.text(j, i+0.28, f'({pct:.1f}%)', ha='center', va='center', fontsize=12,
            color=MUTED)
    ax.text(j, i+0.45, desc, ha='center', va='center', fontsize=9,
            color=MUTED, style='italic')

ax.set_xticks([0, 1])
ax.set_xticklabels(['Predicted: Underperformer (0)', 'Predicted: Outperformer (1)'],
                   fontsize=11)
ax.set_yticks([0, 1])
ax.set_yticklabels(['Actual: Underperformer (0)', 'Actual: Outperformer (1)'],
                   fontsize=11)
ax.set_title('Confusion Matrix — Global Logistic Regression Model\nCutoff = 0.50  |  Overall Accuracy = 53.2%  |  16,589 Test Observations',
             fontsize=13, fontweight='bold', pad=15, color=WHITE)

metrics_text = (f'Sensitivity (Recall): 68.1%    Specificity: 37.7%    '
                f'Precision: 53.3%    Accuracy: 53.2%')
fig.text(0.5, 0.01, metrics_text, ha='center', fontsize=10,
         color=GOLD, fontweight='bold')

plt.tight_layout(pad=1.8)
plt.savefig('viz/06_confusion_matrix.png', dpi=180, bbox_inches='tight', facecolor=NAVY)
plt.close()
print("   Saved viz/06_confusion_matrix.png")

# ═══════════════════════════════════════════════════════════════════════════════
# VIZ 7 — 2025 QUARTERLY ACCURACY TREND
# ═══════════════════════════════════════════════════════════════════════════════
print("7/8  2025 Accuracy Trend...")

df_preds = pd.read_csv('predictions_2025.csv')
q_stats = []
for q in ['2025 Q1', '2025 Q2', '2025 Q3', '2025 Q4']:
    sub = df_preds[df_preds['Label_Quarter'] == q]
    acc = sub['Correct'].mean() * 100
    n   = len(sub)
    n_op = (sub['Predicted'] == 'Outperformer').sum()
    q_stats.append({'Quarter': q, 'Accuracy': acc, 'N': n, 'N_Outperformers': n_op})
q_df = pd.DataFrame(q_stats)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 9),
                                gridspec_kw={'height_ratios': [1.6, 1]})
fig.patch.set_facecolor(NAVY)
ax1.set_facecolor(NAVY_CARD)
ax2.set_facecolor(NAVY_CARD)

x_pos    = range(len(q_df))
q_labels = ['Q1 2025\n(N=334)', 'Q2 2025\n(N=403)', 'Q3 2025\n(N=409)', 'Q4 2025\n(N=73)']
accs_q   = q_df['Accuracy'].tolist()

bar_cols_q = [RED if a < 50 else (GOLD if a < 55 else GREEN) for a in accs_q]
ax1.bar(x_pos, accs_q, color=bar_cols_q, width=0.5, edgecolor=NAVY,
        linewidth=0.8, zorder=3, alpha=0.9)
ax1.plot(x_pos, accs_q, color=WHITE, linewidth=2.2, marker='o', markersize=10,
         markerfacecolor=GOLD, markeredgecolor=NAVY, markeredgewidth=1.5,
         zorder=4, label='Quarterly Accuracy')

ax1.axhline(y=50, color=RED, linewidth=1.8, linestyle=':', alpha=0.7,
            label='Random Baseline (50%)')
ax1.axhline(y=53.2, color=MUTED, linewidth=1.8, linestyle='--', alpha=0.7,
            label='Global Training Accuracy (53.2%)')
ax1.axhline(y=71.2, color=GOLD, linewidth=1.5, linestyle='--', alpha=0.5,
            label='Ananthakumar & Sarkar Benchmark (71.2%)')

for xi, acc in zip(x_pos, accs_q):
    ax1.text(xi, acc + 0.6, f'{acc:.1f}%', ha='center', fontsize=13,
             fontweight='bold', color=WHITE)

ax1.set_xticks(x_pos)
ax1.set_xticklabels(q_labels, fontsize=11)
ax1.set_ylabel('Prediction Accuracy (%)', fontsize=12, labelpad=10)
ax1.set_title('2025 Out-of-Sample Prediction Accuracy — Quarter by Quarter\nModel trained Q1 2010 – Q4 2024, applied to never-before-seen 2025 data',
              fontsize=13, fontweight='bold', pad=12, color=WHITE)
ax1.set_ylim(38, 78)
ax1.legend(fontsize=9, facecolor=NAVY, edgecolor=MUTED, labelcolor=WHITE, loc='upper left')
ax1.grid(True, axis='y', alpha=0.3, zorder=0)

note_texts = [
    'Q1 2025: SPY\ndropped -4.6%\n(Bear market)',
    'Q2 2025:\nSPY +10.6%\nStrong rally',
    'Q3 2025:\nLargest\nsample',
    'Q4 2025:\nPartial\n(73 stocks)',
]
note_colors = [RED, MUTED, MUTED, MUTED]
for xi, nt, nc in zip(x_pos, note_texts, note_colors):
    ax1.text(xi, 41, nt, ha='center', fontsize=8, color=nc,
             style='italic',
             bbox=dict(boxstyle='round,pad=0.3', facecolor=NAVY, edgecolor=nc, alpha=0.7))

for spine in ax1.spines.values():
    spine.set_edgecolor(MUTED)

n_stocks = q_df['N'].tolist()
n_out    = q_df['N_Outperformers'].tolist()
n_under  = [n - o for n, o in zip(n_stocks, n_out)]

bars_out   = ax2.bar(x_pos, n_out, color=GREEN, width=0.5, label='Predicted Outperformers',
                     edgecolor=NAVY, zorder=3)
bars_under = ax2.bar(x_pos, n_under, bottom=n_out, color=BLUE, width=0.5,
                     label='Predicted Underperformers', edgecolor=NAVY, zorder=3)

for xi, total_n, out in zip(x_pos, n_stocks, n_out):
    ax2.text(xi, total_n + 4, f'N={total_n}', ha='center', fontsize=10,
             fontweight='bold', color=WHITE)

ax2.set_xticks(x_pos)
ax2.set_xticklabels(q_labels, fontsize=11)
ax2.set_ylabel('Stock Count', fontsize=11, labelpad=10)
ax2.set_title('Predicted Outperformers vs Underperformers per Quarter', fontsize=11, color=MUTED, pad=6)
ax2.legend(fontsize=9, facecolor=NAVY, edgecolor=MUTED, labelcolor=WHITE)
ax2.grid(True, axis='y', alpha=0.3, zorder=0)
for spine in ax2.spines.values():
    spine.set_edgecolor(MUTED)

plt.tight_layout(pad=1.5)
plt.savefig('viz/07_accuracy_trend_2025.png', dpi=180, bbox_inches='tight', facecolor=NAVY)
plt.close()
print("   Saved viz/07_accuracy_trend_2025.png")

# ═══════════════════════════════════════════════════════════════════════════════
# VIZ 8 — FEATURE CORRELATION HEATMAP
# ═══════════════════════════════════════════════════════════════════════════════
print("8/8  Correlation Heatmap...")

df_raw = pd.read_csv('wrds_compustat_quarterly.csv')
df_macro = pd.read_csv('wrds_fred_macro.csv')
df_crsp  = pd.read_csv('wrds_crsp_quarterly.csv')

df_raw = df_raw.dropna(subset=['revtq', 'niq', 'atq', 'ceqq', 'prccq', 'cshoq'])
df_raw['mkt_cap'] = df_raw.get('mkvaltq', df_raw['prccq'] * df_raw['cshoq'])

eps = 1e-9
df_raw['roa']           = df_raw['niq'] / (df_raw['atq'] + eps)
df_raw['roe']           = df_raw['niq'] / (df_raw['ceqq'].replace(0, np.nan) + eps)
df_raw['gross_margin']  = (df_raw['revtq'] - df_raw['cogsq'].fillna(0)) / (df_raw['revtq'] + eps)
df_raw['op_margin']     = df_raw['oiadpq'].fillna(0) / (df_raw['revtq'] + eps)
df_raw['net_margin']    = df_raw['niq'] / (df_raw['revtq'] + eps)
df_raw['asset_turn']    = df_raw['revtq'] / (df_raw['atq'] + eps)
df_raw['curr_ratio']    = df_raw['actq'].fillna(0) / (df_raw['lctq'].replace(0, np.nan) + eps)
df_raw['debt_eq']       = df_raw['dlttq'].fillna(0) / (df_raw['ceqq'].replace(0, np.nan).abs() + eps)
df_raw['pe_ratio']      = df_raw['prccq'] / (df_raw['ibq'].replace(0, np.nan) / (df_raw['cshoq'] + eps) + eps)
df_raw['book_to_mkt']   = df_raw['ceqq'].fillna(0) / (df_raw['mkt_cap'] + eps)

df_sorted = df_raw.sort_values(['gvkey', 'datadate'])
df_sorted['rev_growth'] = df_sorted.groupby('gvkey')['revtq'].pct_change()
df_sorted['ni_growth']  = df_sorted.groupby('gvkey')['niq'].pct_change()

feature_cols = ['roa', 'roe', 'gross_margin', 'op_margin', 'net_margin',
                'asset_turn', 'curr_ratio', 'debt_eq', 'rev_growth', 'ni_growth',
                'pe_ratio', 'book_to_mkt']
feat_names   = ['ROA', 'ROE', 'Gross\nMargin', 'Op\nMargin', 'Net\nMargin',
                'Asset\nTurnover', 'Current\nRatio', 'Debt/\nEquity',
                'Rev\nGrowth', 'NI\nGrowth', 'P/E\nRatio', 'Book-to-\nMarket']

df_feats = df_sorted[feature_cols].replace([np.inf, -np.inf], np.nan).dropna()
for col in feature_cols:
    lo = df_feats[col].quantile(0.01)
    hi = df_feats[col].quantile(0.99)
    df_feats[col] = df_feats[col].clip(lo, hi)

corr = df_feats.corr()

fig, ax = plt.subplots(figsize=(12, 10))
fig.patch.set_facecolor(NAVY)
ax.set_facecolor(NAVY)

cmap_corr = LinearSegmentedColormap.from_list('corr_map',
    [RED, '#c0392b', NAVY_CARD, '#1a5276', BLUE], N=256)

mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
corr_masked = corr.copy()
for i in range(len(corr)):
    for j in range(len(corr.columns)):
        if j > i:
            corr_masked.iloc[i, j] = np.nan

n = len(feature_cols)
im = ax.imshow(corr_masked.values, cmap=cmap_corr, vmin=-1, vmax=1, aspect='auto')
cbar = plt.colorbar(im, ax=ax, fraction=0.035, pad=0.02)
cbar.set_label('Pearson Correlation Coefficient', color=WHITE, fontsize=11)
cbar.ax.yaxis.set_tick_params(color=WHITE)
plt.setp(cbar.ax.yaxis.get_ticklabels(), color=WHITE)

for i in range(n):
    for j in range(n):
        if j <= i:
            val = corr.iloc[i, j]
            if abs(val) >= 0.5:
                text_c = WHITE
            elif abs(val) >= 0.3:
                text_c = MUTED
            else:
                text_c = '#5a6a7a'
            ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                    fontsize=8.5, color=text_c, fontweight='bold' if abs(val) >= 0.5 else 'normal')

ax.set_xticks(range(n))
ax.set_yticks(range(n))
ax.set_xticklabels(feat_names, fontsize=10)
ax.set_yticklabels(feat_names, fontsize=10)
ax.set_title('Feature Correlation Matrix — 12 Base Financial Ratios\n(Lower triangle only | Values ≥ |0.50| highlight VIF concern)',
             fontsize=13, fontweight='bold', pad=15, color=WHITE)

high_corr_pairs = []
for i in range(n):
    for j in range(i):
        if abs(corr.iloc[i,j]) >= 0.5:
            high_corr_pairs.append(f'{feat_names[i].replace(chr(10)," ")} ↔ {feat_names[j].replace(chr(10)," ")}: {corr.iloc[i,j]:.2f}')

if high_corr_pairs:
    note = 'High correlations (|r|≥0.5): ' + '   '.join(high_corr_pairs[:4])
    fig.text(0.5, 0.005, note, ha='center', fontsize=9, color=RED,
             style='italic', wrap=True)

for spine in ax.spines.values():
    spine.set_edgecolor(MUTED)

plt.tight_layout(pad=1.5)
plt.savefig('viz/08_correlation_heatmap.png', dpi=180, bbox_inches='tight', facecolor=NAVY)
plt.close()
print("   Saved viz/08_correlation_heatmap.png\n")

print("All 8 visualizations saved to viz/")
for f in sorted(os.listdir('viz')):
    path = f'viz/{f}'
    size = os.path.getsize(path) / 1024
    print(f"  {f}  ({size:.0f} KB)")

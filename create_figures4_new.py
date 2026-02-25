import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

os.makedirs("figures4_new", exist_ok=True)

PURPLE = '#6B2D7B'
TEAL = '#2A9D8F'
WARM = '#E76F51'
DARK = '#264653'
GOLD = '#E9C46A'
LIGHT_PURPLE = '#D4B8E0'
LIGHT_TEAL = '#A8DADC'
BG = '#FAFAFA'

# ============================================================
# FIG 1: UWES-9 Item Mean Scores with subscale coloring
# ============================================================
fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

items = ['Item 1\n(Vigor)', 'Item 2\n(Vigor)', 'Item 3\n(Dedic.)', 'Item 4\n(Dedic.)',
         'Item 5\n(Vigor)', 'Item 6\n(Absorp.)', 'Item 7\n(Dedic.)', 'Item 8\n(Absorp.)',
         'Item 9\n(Absorp.)']
means = [3.93, 4.08, 4.10, 4.01, 3.89, 3.89, 4.62, 4.43, 3.64]
sds = [1.30, 1.22, 1.32, 1.44, 1.49, 1.49, 1.32, 1.31, 1.64]
colors = [PURPLE, PURPLE, TEAL, TEAL, PURPLE, WARM, TEAL, WARM, WARM]

bars = ax.bar(range(9), means, yerr=sds, color=colors, edgecolor='black', linewidth=0.8,
              width=0.6, capsize=5, error_kw={'linewidth': 1.5})
for i, (bar, m) in enumerate(zip(bars, means)):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + sds[i] + 0.08,
            f'{m:.2f}', ha='center', fontsize=11, fontweight='bold')

ax.set_xticks(range(9))
ax.set_xticklabels(items, fontsize=10)
ax.set_ylabel('Mean Score (0-6 scale)', fontsize=13, fontweight='bold')
ax.set_title('UWES-9 Item Mean Scores by Subscale (n = 702 Women)\nSource: Willmer et al. (2019), Table 2',
             fontsize=14, fontweight='bold', color=DARK)
ax.set_ylim(0, 7)
ax.axhline(y=4.06, color='black', linestyle='--', linewidth=1.5, alpha=0.6)
ax.text(8.5, 4.15, 'Overall\nMean = 4.06', fontsize=9, color='black', ha='right')
ax.grid(True, alpha=0.3, axis='y')

legend_elements = [mpatches.Patch(facecolor=PURPLE, label='Vigor'),
                   mpatches.Patch(facecolor=TEAL, label='Dedication'),
                   mpatches.Patch(facecolor=WARM, label='Absorption')]
ax.legend(handles=legend_elements, fontsize=11, loc='upper left')

plt.tight_layout()
plt.savefig('figures4_new/item_means.png', dpi=200, bbox_inches='tight')
plt.close()
print("Fig 1: Item means")

# ============================================================
# FIG 2: Factor Loadings (EFA, 1-factor) - Table 3
# ============================================================
fig, ax = plt.subplots(figsize=(12, 7))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

items_short = ['UWES1\n(V)', 'UWES2\n(V)', 'UWES3\n(D)', 'UWES4\n(D)',
               'UWES5\n(V)', 'UWES6\n(A)', 'UWES7\n(D)', 'UWES8\n(A)', 'UWES9\n(A)']
loadings = [0.78, 0.81, 0.93, 0.90, 0.81, 0.86, 0.78, 0.79, 0.65]
colors_load = [PURPLE, PURPLE, TEAL, TEAL, PURPLE, WARM, TEAL, WARM, WARM]

bars = ax.barh(range(8, -1, -1), loadings, color=colors_load, edgecolor='black',
               linewidth=0.8, height=0.6)
for i, (bar, v) in enumerate(zip(bars, loadings)):
    ax.text(v + 0.01, bar.get_y() + bar.get_height()/2, f'{v:.2f}',
            va='center', fontsize=12, fontweight='bold')

ax.set_yticks(range(8, -1, -1))
ax.set_yticklabels(items_short, fontsize=10)
ax.set_xlabel('Factor Loading', fontsize=13, fontweight='bold')
ax.set_title('EFA Factor Loadings: One-Factor Solution (n = 341)\nAll loadings > 0.65 | Source: Willmer et al. (2019), Table 3',
             fontsize=14, fontweight='bold', color=DARK)
ax.set_xlim(0, 1.1)
ax.axvline(x=0.70, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
ax.text(0.71, -0.3, 'Strong loading\nthreshold (0.70)', fontsize=9, color='red')
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('figures4_new/factor_loadings.png', dpi=200, bbox_inches='tight')
plt.close()
print("Fig 2: Factor loadings")

# ============================================================
# FIG 3: KMO & Bartlett's Test Summary
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.axis('off')

ax.text(0.5, 0.95, 'Sampling Adequacy & Sphericity Tests',
        ha='center', va='center', fontsize=18, fontweight='bold', color=DARK,
        transform=ax.transAxes)

table_data = [
    ['Test', 'Value', 'Interpretation'],
    ['KMO Measure', '0.922', 'Marvellous (> 0.90)'],
    ["Bartlett's Test p-value", '< 0.001', 'Significant'],
    ["Cronbach's Alpha", '0.947', 'Excellent (> 0.90)'],
    ['Inter-item Correlation', '0.524 - 0.849', 'High'],
    ['Subscale Correlation (V-D-A)', '0.79 - 0.84', 'Very High'],
    ['EFA Variance Explained', '> 70%', 'One factor dominant'],
    ['EFA Chi-squared (df=27)', '332.43', 'Significant'],
]

table = ax.table(cellText=table_data, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1, 2.0)

for (i, j), cell in table.get_celld().items():
    if i == 0:
        cell.set_facecolor(PURPLE)
        cell.set_text_props(color='white', fontweight='bold', fontsize=13)
    elif i % 2 == 0:
        cell.set_facecolor(LIGHT_PURPLE)
    else:
        cell.set_facecolor('white')
    cell.set_edgecolor('#CCCCCC')

ax.text(0.5, 0.02, 'Source: Willmer et al. (2019) | n = 702 women | UWES-9',
        ha='center', fontsize=10, color='gray', transform=ax.transAxes)

plt.tight_layout()
plt.savefig('figures4_new/kmo_bartlett.png', dpi=200, bbox_inches='tight')
plt.close()
print("Fig 3: KMO & Bartlett")

# ============================================================
# FIG 4: Subscale Mean Scores Comparison
# ============================================================
fig, ax = plt.subplots(figsize=(10, 7))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

subscales = ['Total UWES', 'Vigor', 'Dedication', 'Absorption']
sub_means = [4.06, 3.96, 4.24, 3.98]
sub_sds = [1.18, 1.19, 1.25, 1.32]
sub_colors = [DARK, PURPLE, TEAL, WARM]

bars = ax.bar(subscales, sub_means, yerr=sub_sds, color=sub_colors, edgecolor='black',
              linewidth=0.8, width=0.5, capsize=6, error_kw={'linewidth': 1.5})
for bar, m, sd in zip(bars, sub_means, sub_sds):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + sd + 0.08,
            f'{m:.2f}\n(SD={sd:.2f})', ha='center', fontsize=11, fontweight='bold')

ax.set_ylabel('Mean Score (0-6 scale)', fontsize=13, fontweight='bold')
ax.set_title('UWES-9 Subscale Mean Scores (n = 702 Women)\nDedication highest, Vigor & Absorption similar\nSource: Willmer et al. (2019), Table 1',
             fontsize=14, fontweight='bold', color=DARK)
ax.set_ylim(0, 6.5)
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('figures4_new/subscale_means.png', dpi=200, bbox_inches='tight')
plt.close()
print("Fig 4: Subscale means")

# ============================================================
# FIG 5: CFA Standardized Coefficients Comparison (3 models)
# ============================================================
fig, ax = plt.subplots(figsize=(14, 8))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

items_cfa = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5',
             'Item 6', 'Item 7', 'Item 8', 'Item 9']
one_f = [0.79, 0.82, 0.92, 0.90, 0.81, 0.87, 0.76, 0.81, 0.69]
two_f = [0.80, 0.83, 0.92, 0.90, 0.76, 0.89, 0.77, 0.83, 0.76]
three_f = [0.89, 0.92, 0.94, 0.93, 0.74, 0.99, 0.75, 0.84, 0.73]

x = np.arange(9)
w = 0.25
bars1 = ax.bar(x - w, one_f, w, label='One-Factor', color=PURPLE, edgecolor='black', linewidth=0.5)
bars2 = ax.bar(x, two_f, w, label='Two-Factor', color=TEAL, edgecolor='black', linewidth=0.5)
bars3 = ax.bar(x + w, three_f, w, label='Three-Factor', color=WARM, edgecolor='black', linewidth=0.5)

for bars in [bars1, bars2, bars3]:
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.01, f'{h:.2f}',
                ha='center', fontsize=8, fontweight='bold')

ax.set_xticks(x)
ax.set_xticklabels(items_cfa, fontsize=11)
ax.set_ylabel('Standardized Coefficient', fontsize=13, fontweight='bold')
ax.set_title('CFA Standardized Coefficients: Three Model Comparison (n = 342)\nSource: Willmer et al. (2019), Table 4',
             fontsize=14, fontweight='bold', color=DARK)
ax.set_ylim(0, 1.15)
ax.legend(fontsize=12, loc='lower right')
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('figures4_new/cfa_coefficients.png', dpi=200, bbox_inches='tight')
plt.close()
print("Fig 5: CFA coefficients")

# ============================================================
# FIG 6: Goodness-of-Fit Comparison (Table 5)
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.patch.set_facecolor(BG)
fig.suptitle('CFA Goodness-of-Fit Statistics: Three Model Comparison\nSource: Willmer et al. (2019), Table 5',
             fontsize=15, fontweight='bold', color=DARK)

models = ['One-Factor', 'Two-Factor', 'Three-Factor']
colors_m = [PURPLE, TEAL, WARM]

# RMSEA
rmsea = [0.181, 0.192, 0.167]
bars = axes[0,0].bar(models, rmsea, color=colors_m, edgecolor='black', width=0.4)
axes[0,0].axhline(y=0.08, color='green', linestyle='--', linewidth=2, label='Good fit < 0.08')
axes[0,0].axhline(y=0.10, color='orange', linestyle='--', linewidth=1.5, label='Acceptable < 0.10')
for b, v in zip(bars, rmsea): axes[0,0].text(b.get_x()+b.get_width()/2, v+0.003, f'{v:.3f}', ha='center', fontsize=11, fontweight='bold')
axes[0,0].set_title('RMSEA (lower = better)', fontsize=12, fontweight='bold')
axes[0,0].set_ylim(0, 0.25)
axes[0,0].legend(fontsize=8)
axes[0,0].set_facecolor(BG)

# CFI
cfi = [0.895, 0.882, 0.920]
bars = axes[0,1].bar(models, cfi, color=colors_m, edgecolor='black', width=0.4)
axes[0,1].axhline(y=0.95, color='green', linestyle='--', linewidth=2, label='Good fit > 0.95')
for b, v in zip(bars, cfi): axes[0,1].text(b.get_x()+b.get_width()/2, v+0.003, f'{v:.3f}', ha='center', fontsize=11, fontweight='bold')
axes[0,1].set_title('CFI (higher = better)', fontsize=12, fontweight='bold')
axes[0,1].set_ylim(0.8, 1.0)
axes[0,1].legend(fontsize=8)
axes[0,1].set_facecolor(BG)

# TLI
tli = [0.860, 0.837, 0.880]
bars = axes[1,0].bar(models, tli, color=colors_m, edgecolor='black', width=0.4)
axes[1,0].axhline(y=0.95, color='green', linestyle='--', linewidth=2, label='Good fit > 0.95')
for b, v in zip(bars, tli): axes[1,0].text(b.get_x()+b.get_width()/2, v+0.003, f'{v:.3f}', ha='center', fontsize=11, fontweight='bold')
axes[1,0].set_title('TLI (higher = better)', fontsize=12, fontweight='bold')
axes[1,0].set_ylim(0.75, 1.0)
axes[1,0].legend(fontsize=8)
axes[1,0].set_facecolor(BG)

# SRMR
srmr = [0.046, 0.049, 0.065]
bars = axes[1,1].bar(models, srmr, color=colors_m, edgecolor='black', width=0.4)
axes[1,1].axhline(y=0.08, color='green', linestyle='--', linewidth=2, label='Good fit < 0.08')
for b, v in zip(bars, srmr): axes[1,1].text(b.get_x()+b.get_width()/2, v+0.001, f'{v:.3f}', ha='center', fontsize=11, fontweight='bold')
axes[1,1].set_title('SRMR (lower = better)', fontsize=12, fontweight='bold')
axes[1,1].set_ylim(0, 0.1)
axes[1,1].legend(fontsize=8)
axes[1,1].set_facecolor(BG)

plt.tight_layout()
plt.savefig('figures4_new/goodness_of_fit.png', dpi=200, bbox_inches='tight')
plt.close()
print("Fig 6: Goodness of fit")

# ============================================================
# FIG 7: One-Factor CFA Path Diagram (Figure 1 from paper)
# ============================================================
fig, ax = plt.subplots(figsize=(12, 10))
fig.patch.set_facecolor(BG)
ax.set_xlim(0, 12)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_facecolor(BG)

ax.text(6, 9.5, 'One-Factor CFA Model: Work Engagement',
        ha='center', fontsize=16, fontweight='bold', color=DARK)
ax.text(6, 9.1, 'All items load on single latent factor | n = 342 | Source: Figure 1, Willmer et al. (2019)',
        ha='center', fontsize=10, color='gray')

ellipse = mpatches.Ellipse((6, 7.5), 4.5, 1.5, facecolor=PURPLE, edgecolor='black', linewidth=2, alpha=0.9)
ax.add_patch(ellipse)
ax.text(6, 7.5, 'Work\nEngagement', ha='center', va='center', fontsize=14,
        fontweight='bold', color='white')

item_labels = ['Item 1 (V)\n"Bursting\nwith energy"', 'Item 2 (V)\n"Strong &\nvigorous"',
               'Item 3 (D)\n"Enthusiastic"', 'Item 4 (D)\n"Inspires me"',
               'Item 5 (V)\n"Feel like\ngoing to work"', 'Item 6 (A)\n"Happy working\nintensely"',
               'Item 7 (D)\n"Proud of\nmy work"', 'Item 8 (A)\n"Carried\naway"',
               'Item 9 (A)\n"Immersed\nin work"']
coefs_1f = [0.79, 0.82, 0.92, 0.90, 0.81, 0.87, 0.76, 0.81, 0.69]
item_colors = [PURPLE, PURPLE, TEAL, TEAL, PURPLE, WARM, TEAL, WARM, WARM]

for i in range(9):
    x_pos = 1.2 + i * 1.15
    rect = mpatches.FancyBboxPatch((x_pos - 0.5, 1.5), 1.0, 1.8,
                                    boxstyle="round,pad=0.08", facecolor=item_colors[i],
                                    edgecolor='black', linewidth=1.5, alpha=0.85)
    ax.add_patch(rect)
    ax.text(x_pos, 2.4, item_labels[i], ha='center', va='center', fontsize=7,
            fontweight='bold', color='white')

    ax.annotate('', xy=(x_pos, 3.3), xytext=(6, 6.7),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))
    ax.text((x_pos + 6) / 2 - 0.3, (3.3 + 6.7) / 2 + 0.2,
            f'{coefs_1f[i]:.2f}', fontsize=9, fontweight='bold', color=DARK,
            bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none', alpha=0.8))

ax.text(6, 0.8, 'Chi2 = 633.90 (df=27)  |  RMSEA = 0.181  |  CFI = 0.895  |  TLI = 0.860  |  SRMR = 0.046',
        ha='center', fontsize=11, fontweight='bold', color=DARK)

plt.tight_layout()
plt.savefig('figures4_new/one_factor_model.png', dpi=200, bbox_inches='tight')
plt.close()
print("Fig 7: One-factor model")

# ============================================================
# FIG 8: Three-Factor CFA Path Diagram (Figure 3 from paper)
# ============================================================
fig, ax = plt.subplots(figsize=(14, 10))
fig.patch.set_facecolor(BG)
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_facecolor(BG)

ax.text(7, 9.5, 'Three-Factor CFA Model: Vigor, Dedication, Absorption',
        ha='center', fontsize=16, fontweight='bold', color=DARK)
ax.text(7, 9.1, 'Theoretical structure of UWES-9 | n = 342 | Source: Figure 3, Willmer et al. (2019)',
        ha='center', fontsize=10, color='gray')

factor_info = [
    ('Vigor', PURPLE, 2.5, 7.0, ['Item 1\n0.89', 'Item 2\n0.92', 'Item 5\n0.74']),
    ('Dedication', TEAL, 7.0, 7.0, ['Item 3\n0.94', 'Item 4\n0.93', 'Item 7\n0.75']),
    ('Absorption', WARM, 11.5, 7.0, ['Item 6\n0.99', 'Item 8\n0.84', 'Item 9\n0.73']),
]

for fname, fcol, fx, fy, fitems in factor_info:
    ellipse = mpatches.Ellipse((fx, fy), 3.0, 1.3, facecolor=fcol, edgecolor='black', linewidth=2, alpha=0.9)
    ax.add_patch(ellipse)
    ax.text(fx, fy, fname, ha='center', va='center', fontsize=13, fontweight='bold', color='white')

    for j, item_text in enumerate(fitems):
        ix = fx - 1.5 + j * 1.5
        iy = 3.5
        rect = mpatches.FancyBboxPatch((ix - 0.55, iy - 0.7), 1.1, 1.4,
                                        boxstyle="round,pad=0.08", facecolor=fcol,
                                        edgecolor='black', linewidth=1.5, alpha=0.7)
        ax.add_patch(rect)
        ax.text(ix, iy, item_text, ha='center', va='center', fontsize=9,
                fontweight='bold', color='white')
        ax.annotate('', xy=(ix, iy + 0.7), xytext=(fx, fy - 0.65),
                    arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))

correlations = [('Vigor', 'Dedication', 2.5, 7.0, 7.0, 7.0, '0.79-0.84'),
                ('Dedication', 'Absorption', 7.0, 7.0, 11.5, 7.0, '0.79-0.84')]
for _, _, x1, y1, x2, y2, label in correlations:
    ax.annotate('', xy=(x2-1.0, y2+0.6), xytext=(x1+1.0, y1+0.6),
                arrowprops=dict(arrowstyle='<->', color=DARK, lw=2, connectionstyle='arc3,rad=-0.3'))
    ax.text((x1+x2)/2, 8.3, label, ha='center', fontsize=10, fontweight='bold', color=DARK)

ax.annotate('', xy=(11.5-0.5, 7.7), xytext=(2.5+0.5, 7.7),
            arrowprops=dict(arrowstyle='<->', color=DARK, lw=2, connectionstyle='arc3,rad=-0.4'))

ax.text(7, 1.8, 'Chi2 = 247.76 (df=24)  |  RMSEA = 0.167  |  CFI = 0.920  |  TLI = 0.880  |  SRMR = 0.065',
        ha='center', fontsize=11, fontweight='bold', color=DARK)
ax.text(7, 1.2, 'High inter-factor correlations (0.79-0.84) suggest factors are not clearly distinct',
        ha='center', fontsize=10, color='gray')

plt.tight_layout()
plt.savefig('figures4_new/three_factor_model.png', dpi=200, bbox_inches='tight')
plt.close()
print("Fig 8: Three-factor model")

# ============================================================
# FIG 9: Skewness and Kurtosis
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.patch.set_facecolor(BG)

items_sk = [f'Item {i+1}' for i in range(9)]
skew = [-0.798, -0.921, -0.900, -0.808, -0.805, -0.711, -1.262, -1.159, -0.560]
kurt = [0.294, 0.678, 0.568, 0.266, 0.113, -0.046, 1.645, 1.474, -0.497]

bars1 = axes[0].barh(range(8,-1,-1), skew, color=[PURPLE]*3+[TEAL]*2+[WARM]+[TEAL]+[WARM]*2,
                      edgecolor='black', linewidth=0.5, height=0.5)
axes[0].axvline(x=-2, color='red', linestyle='--', linewidth=1.5, alpha=0.5)
axes[0].axvline(x=2, color='red', linestyle='--', linewidth=1.5, alpha=0.5)
axes[0].set_yticks(range(8,-1,-1))
axes[0].set_yticklabels(items_sk, fontsize=10)
axes[0].set_title('Skewness\n(Acceptable: -2 to +2)', fontsize=12, fontweight='bold', color=DARK)
axes[0].set_xlim(-2.5, 1)
axes[0].set_facecolor(BG)
for i, v in enumerate(skew):
    axes[0].text(v - 0.08 if v < 0 else v + 0.08, 8-i, f'{v:.3f}',
                 va='center', ha='right' if v < 0 else 'left', fontsize=9, fontweight='bold')

bars2 = axes[1].barh(range(8,-1,-1), kurt, color=[PURPLE]*3+[TEAL]*2+[WARM]+[TEAL]+[WARM]*2,
                      edgecolor='black', linewidth=0.5, height=0.5)
axes[1].axvline(x=-7, color='red', linestyle='--', linewidth=1.5, alpha=0.5)
axes[1].axvline(x=7, color='red', linestyle='--', linewidth=1.5, alpha=0.5)
axes[1].set_yticks(range(8,-1,-1))
axes[1].set_yticklabels(items_sk, fontsize=10)
axes[1].set_title('Kurtosis\n(Acceptable: -7 to +7)', fontsize=12, fontweight='bold', color=DARK)
axes[1].set_xlim(-2, 3)
axes[1].set_facecolor(BG)
for i, v in enumerate(kurt):
    axes[1].text(v + 0.05, 8-i, f'{v:.3f}', va='center', fontsize=9, fontweight='bold')

fig.suptitle('Item Distribution Properties (n = 702)\nSource: Willmer et al. (2019), Table 2',
             fontsize=14, fontweight='bold', color=DARK, y=1.02)
plt.tight_layout()
plt.savefig('figures4_new/skewness_kurtosis.png', dpi=200, bbox_inches='tight')
plt.close()
print("Fig 9: Skewness & Kurtosis")

# ============================================================
# FIG 10: Demographics Pie Charts
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
fig.patch.set_facecolor(BG)
fig.suptitle('Sample Demographics (n = 702 Women, Mean Age = 31.8)\nSource: Willmer et al. (2019), Table 1',
             fontsize=14, fontweight='bold', color=DARK)

marital = [530, 159, 9]
marital_labels = ['Married/\nCohabiting\n(76%)', 'Single\n(23%)', 'Divorced\n(1%)']
marital_colors = [PURPLE, TEAL, WARM]
axes[0].pie(marital, labels=marital_labels, colors=marital_colors, autopct='',
            startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
axes[0].set_title('Marital Status', fontsize=12, fontweight='bold', color=DARK)

edu = [425, 152, 75, 21, 9]
edu_labels = ['University\n2+ yrs (61%)', 'Upper Sec.\n3 yrs (22%)', 'University\n<2 yrs (11%)',
              'Upper Sec.\n<3 yrs (3%)', 'Compulsory\n(1%)']
edu_colors = [PURPLE, TEAL, WARM, GOLD, LIGHT_TEAL]
axes[1].pie(edu, labels=edu_labels, colors=edu_colors, autopct='',
            startangle=90, textprops={'fontsize': 9, 'fontweight': 'bold'})
axes[1].set_title('Education Level', fontsize=12, fontweight='bold', color=DARK)

age_data = ['26-30', '31-34', '35-37']
age_vals = [280, 322, 100]
axes[2].bar(age_data, age_vals, color=[PURPLE, TEAL, WARM], edgecolor='black', width=0.5)
for i, v in enumerate(age_vals):
    axes[2].text(i, v+5, str(v), ha='center', fontsize=12, fontweight='bold')
axes[2].set_title('Age Distribution (est.)', fontsize=12, fontweight='bold', color=DARK)
axes[2].set_ylabel('Count', fontsize=11)
axes[2].set_facecolor(BG)
axes[2].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('figures4_new/demographics.png', dpi=200, bbox_inches='tight')
plt.close()
print("Fig 10: Demographics")

# ============================================================
# FIG 11: Goodness-of-Fit Summary Table (Table 5)
# ============================================================
fig, ax = plt.subplots(figsize=(14, 5))
fig.patch.set_facecolor(BG)
ax.axis('off')

ax.text(0.5, 0.97, 'CFA Goodness-of-Fit: All Three Models (Table 5)',
        ha='center', va='center', fontsize=16, fontweight='bold', color=DARK,
        transform=ax.transAxes)

gof_data = [
    ['Fit Statistic', 'One-Factor', 'Two-Factor', 'Three-Factor', 'Good Fit Threshold'],
    ['Chi2 (df)', '633.90 (27)', '354.49 (26)', '247.76 (24)', 'Non-significant preferred'],
    ['RMSEA', '0.181', '0.192', '0.167', '< 0.08'],
    ['RMSEA 90% CI', '0.169-0.194', '0.175-0.192', '0.154-0.180', '--'],
    ['AIC', '16221.47', '8246.29', '8143.56', 'Lower = better'],
    ['BIC', '16343.70', '8353.66', '8258.60', 'Lower = better'],
    ['CFI', '0.895', '0.882', '0.920', '> 0.95'],
    ['TLI', '0.860', '0.837', '0.880', '> 0.95'],
    ['SRMR', '0.046', '0.049', '0.065', '< 0.08'],
]

table = ax.table(cellText=gof_data, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 1.8)

for (i, j), cell in table.get_celld().items():
    if i == 0:
        cell.set_facecolor(PURPLE)
        cell.set_text_props(color='white', fontweight='bold', fontsize=11)
    elif j == 4:
        cell.set_facecolor('#FFF3E0')
    cell.set_edgecolor('#CCCCCC')

plt.tight_layout()
plt.savefig('figures4_new/gof_table.png', dpi=200, bbox_inches='tight')
plt.close()
print("Fig 11: GoF table")

print("\nAll 11 figures generated!")

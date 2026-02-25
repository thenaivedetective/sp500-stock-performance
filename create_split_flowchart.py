import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import numpy as np

PURPLE = '#6B2D7B'
TEAL = '#2A9D8F'
WARM = '#E76F51'
DARK = '#264653'
GOLD = '#E9C46A'
WHITE = '#FFFFFF'
BG = '#FAFAFA'
LIGHT_PURPLE = '#E8D5F0'
LIGHT_TEAL = '#D4F0EB'

fig, ax = plt.subplots(figsize=(14, 9))
fig.patch.set_facecolor(BG)
ax.set_xlim(0, 14)
ax.set_ylim(0, 9)
ax.axis('off')
ax.set_facecolor(BG)

ax.text(7, 8.7, 'Split-Sample Research Design', ha='center', fontsize=20, fontweight='bold', color=DARK)
ax.text(7, 8.35, 'Willmer et al. (2019) | Rigorous EFA + CFA Validation Protocol', ha='center', fontsize=12, color='gray')

top_box = mpatches.FancyBboxPatch((4.0, 6.8), 6.0, 1.2, boxstyle="round,pad=0.15",
                                    facecolor=PURPLE, edgecolor='black', linewidth=2)
ax.add_patch(top_box)
ax.text(7, 7.55, 'Total Sample', ha='center', fontsize=16, fontweight='bold', color=WHITE)
ax.text(7, 7.15, 'N = 702 Women (Ages 26-37)', ha='center', fontsize=13, color=GOLD)
ax.text(7, 6.85, '19 excluded (missing data) = 683 complete cases', ha='center', fontsize=10, color='#D4B8E0')

ax.annotate('', xy=(4.5, 5.7), xytext=(7, 6.8),
            arrowprops=dict(arrowstyle='->', color=DARK, lw=3))
ax.annotate('', xy=(9.5, 5.7), xytext=(7, 6.8),
            arrowprops=dict(arrowstyle='->', color=DARK, lw=3))

ax.text(7, 6.3, 'Randomly Split', ha='center', fontsize=11, fontweight='bold', color=DARK,
        bbox=dict(boxstyle='round,pad=0.3', facecolor=GOLD, edgecolor='none', alpha=0.9))

efa_box = mpatches.FancyBboxPatch((1.5, 4.3), 5.0, 1.4, boxstyle="round,pad=0.15",
                                    facecolor=TEAL, edgecolor='black', linewidth=2)
ax.add_patch(efa_box)
ax.text(4.0, 5.2, 'Group 1: EFA', ha='center', fontsize=15, fontweight='bold', color=WHITE)
ax.text(4.0, 4.75, 'n = 341 Women', ha='center', fontsize=13, color=WHITE)
ax.text(4.0, 4.45, 'Discover the underlying structure', ha='center', fontsize=10, color='#D4F0EB')

cfa_box = mpatches.FancyBboxPatch((7.5, 4.3), 5.0, 1.4, boxstyle="round,pad=0.15",
                                    facecolor=WARM, edgecolor='black', linewidth=2)
ax.add_patch(cfa_box)
ax.text(10.0, 5.2, 'Group 2: CFA', ha='center', fontsize=15, fontweight='bold', color=WHITE)
ax.text(10.0, 4.75, 'n = 342 Women', ha='center', fontsize=13, color=WHITE)
ax.text(10.0, 4.45, 'Test & validate those structures', ha='center', fontsize=10, color='#FDDDD4')

ax.annotate('', xy=(4.0, 3.5), xytext=(4.0, 4.3),
            arrowprops=dict(arrowstyle='->', color=DARK, lw=2.5))
ax.annotate('', xy=(10.0, 3.5), xytext=(10.0, 4.3),
            arrowprops=dict(arrowstyle='->', color=DARK, lw=2.5))

efa_detail = mpatches.FancyBboxPatch((1.2, 1.5), 5.6, 2.0, boxstyle="round,pad=0.15",
                                      facecolor=LIGHT_TEAL, edgecolor=TEAL, linewidth=2)
ax.add_patch(efa_detail)
ax.text(4.0, 3.2, 'EFA Methods:', ha='center', fontsize=12, fontweight='bold', color=DARK)
efa_items = [
    'ML extraction, Eigenvalues > 1',
    'Scree Plot analysis',
    "Velicer's MAP test",
    'Parallel Analysis',
    'Promax rotation (forced 3-factor)',
]
for i, item in enumerate(efa_items):
    ax.text(4.0, 2.8 - i*0.3, item, ha='center', fontsize=10, color=DARK)

efa_result = mpatches.FancyBboxPatch((1.8, 0.4), 4.4, 0.8, boxstyle="round,pad=0.15",
                                      facecolor=TEAL, edgecolor='black', linewidth=1.5)
ax.add_patch(efa_result)
ax.text(4.0, 0.9, 'Result: 1-Factor Solution', ha='center', fontsize=12, fontweight='bold', color=WHITE)
ax.text(4.0, 0.55, '> 70% variance | All loadings 0.65-0.93', ha='center', fontsize=9, color='#D4F0EB')
ax.annotate('', xy=(4.0, 1.2), xytext=(4.0, 1.5),
            arrowprops=dict(arrowstyle='->', color=DARK, lw=2))

cfa_detail = mpatches.FancyBboxPatch((7.2, 1.5), 5.6, 2.0, boxstyle="round,pad=0.15",
                                      facecolor='#FDDDD4', edgecolor=WARM, linewidth=2)
ax.add_patch(cfa_detail)
ax.text(10.0, 3.2, 'CFA Models Tested:', ha='center', fontsize=12, fontweight='bold', color=DARK)
cfa_items = [
    'Model 1: One-Factor (Work Engagement)',
    'Model 2: Two-Factor (V+D / A)',
    'Model 3: Three-Factor (V / D / A)',
    'ML estimation, standardized coefs.',
    'Goodness-of-fit: RMSEA, CFI, TLI, SRMR',
]
for i, item in enumerate(cfa_items):
    ax.text(10.0, 2.8 - i*0.3, item, ha='center', fontsize=10, color=DARK)

cfa_result = mpatches.FancyBboxPatch((7.8, 0.4), 4.4, 0.8, boxstyle="round,pad=0.15",
                                      facecolor='#C0392B', edgecolor='black', linewidth=1.5)
ax.add_patch(cfa_result)
ax.text(10.0, 0.9, 'Result: No Good Fit', ha='center', fontsize=12, fontweight='bold', color=WHITE)
ax.text(10.0, 0.55, 'RMSEA 0.167-0.192 | CFI/TLI < 0.95', ha='center', fontsize=9, color='#F5B7B1')
ax.annotate('', xy=(10.0, 1.2), xytext=(10.0, 1.5),
            arrowprops=dict(arrowstyle='->', color=DARK, lw=2))

plt.tight_layout()
plt.savefig('figures4_new/split_sample_flowchart.png', dpi=200, bbox_inches='tight')
plt.close()
print("Split-sample flowchart created!")

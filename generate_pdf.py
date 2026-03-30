"""
Generates a professional 15-slide PDF presentation for the credit risk project.
Uses matplotlib so layout is exact and images embed perfectly.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg
import numpy as np
import os

# ── Palette ─────────────────────────────────────────────────────────
NAVY   = "#0D1B2E"
NAVY2  = "#1A2F4A"
NAVY3  = "#10263E"
BLUE   = "#2563EB"
LBLUE  = "#60A5FA"
GOLD   = "#F59E0B"
GREEN  = "#10B981"
RED    = "#EF4444"
WHITE  = "#FFFFFF"
LGREY  = "#94A3B8"
DGREY  = "#334155"

W, H = 13.33, 7.5   # slide size in inches

def new_slide(title_tag=None, title=None, tag_color=LBLUE, bar_color=BLUE):
    fig = plt.figure(figsize=(W, H), facecolor=NAVY)
    ax  = fig.add_axes([0, 0, 1, 1], facecolor=NAVY)
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

    # bottom accent bar
    ax.add_patch(mpatches.FancyBboxPatch((0, 0), W, 0.07,
        boxstyle="square,pad=0", facecolor=bar_color, lw=0))
    # slide number will be added per slide
    if title_tag:
        ax.text(0.45, H-0.38, title_tag.upper(), color=LBLUE,
                fontsize=8.5, fontweight="bold", va="center", family="DejaVu Sans")
    if title:
        ax.text(0.45, H-0.8, title, color=WHITE,
                fontsize=22, fontweight="bold", va="center", family="DejaVu Sans")
    return fig, ax

def slide_num(ax, n, total=15):
    ax.text(W-0.15, 0.22, f"{n} / {total}", color=DGREY,
            fontsize=8, ha="right", va="center", family="DejaVu Sans")

def card(ax, x, y, w, h, title, body, title_color=LBLUE, bg=NAVY2, fontsize=10):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
        boxstyle="round,pad=0.04", facecolor=bg, lw=0))
    ax.text(x+0.18, y+h-0.2, title, color=title_color,
            fontsize=11, fontweight="bold", va="top", family="DejaVu Sans")
    ax.text(x+0.18, y+h-0.46, body, color=LGREY,
            fontsize=fontsize, va="top", wrap=True, family="DejaVu Sans",
            multialignment="left")

def stat_box(ax, x, y, w, h, stat, label, stat_color=BLUE):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
        boxstyle="round,pad=0.04", facecolor=NAVY2, lw=0))
    ax.text(x+w/2, y+h*0.62, stat, color=stat_color,
            fontsize=24, fontweight="bold", ha="center", va="center", family="DejaVu Sans")
    ax.text(x+w/2, y+h*0.22, label, color=LGREY,
            fontsize=8, ha="center", va="center", family="DejaVu Sans",
            multialignment="center")

def embed_image(fig, path, rect):
    """rect = [left, bottom, width, height] in figure fraction"""
    if os.path.exists(path):
        iax = fig.add_axes(rect)
        iax.set_axis_off()
        img = mpimg.imread(path)
        iax.imshow(img, aspect="auto")

def bullets(ax, items, x, y, spacing=0.38, dot_color=BLUE, fontsize=10.5):
    for i, item in enumerate(items):
        yi = y - i*spacing
        ax.text(x, yi, "▸", color=dot_color, fontsize=fontsize,
                va="center", family="DejaVu Sans")
        ax.text(x+0.28, yi, item, color=LGREY, fontsize=fontsize,
                va="center", wrap=True, family="DejaVu Sans")

def hr(ax, y, color=DGREY, lw=0.8):
    ax.axhline(y, xmin=0.03, xmax=0.97, color=color, lw=lw)

# ════════════════════════════════════════════════════════════════════
# SLIDE 1 — TITLE
# ════════════════════════════════════════════════════════════════════
fig, ax = new_slide(bar_color=BLUE)

# left panel
ax.add_patch(mpatches.Rectangle((0,0), 8, H, facecolor="#0F2D52", lw=0))
ax.add_patch(mpatches.Rectangle((0,0), W, 0.12, facecolor=BLUE, lw=0))

ax.text(0.45, H-0.42, "MULTIVARIATE STATISTICS  ·  BINGHAMTON UNIVERSITY",
        color=LBLUE, fontsize=9, fontweight="bold", family="DejaVu Sans")
ax.text(0.45, H-1.05, "Credit Risk Classification", color=WHITE,
        fontsize=40, fontweight="bold", family="DejaVu Sans")
ax.text(0.45, H-1.72, "Using ML Techniques", color=LBLUE,
        fontsize=40, fontweight="bold", family="DejaVu Sans")
ax.text(0.45, H-2.55,
        "Applying Factor Analysis, Linear Discriminant Analysis, and\n"
        "Logistic Regression to 500,000 real LendingClub loan records\n"
        "to predict borrower default risk.",
        color=LGREY, fontsize=13, family="DejaVu Sans", linespacing=1.6)

hr(ax, 2.9, color="#1E3A5F", lw=1.2)

meta = [
    ("AUTHOR",     "Lana Jalal Gidan"),
    ("DEPARTMENT", "Systems Science &\nIndustrial Engineering"),
    ("DATASET",    "LendingClub · 500K Loans"),
    ("MODELS",     "LDA & Logistic Regression"),
]
for i, (lbl, val) in enumerate(meta):
    xi = 0.45 + i*3.25
    ax.text(xi, 2.65, lbl, color=LBLUE, fontsize=7.5, fontweight="bold", family="DejaVu Sans")
    ax.text(xi, 2.2,  val, color=WHITE,  fontsize=10.5, fontweight="bold",
            family="DejaVu Sans", linespacing=1.4)

slide_num(ax, 1)
with PdfPages("tmp_slide.pdf"): pass   # warmup

pages = [fig]

# ════════════════════════════════════════════════════════════════════
# SLIDE 2 — AGENDA
# ════════════════════════════════════════════════════════════════════
fig, ax = new_slide("Roadmap", "What We'll Cover")
items_agenda = [
    ("1", "The Problem",        "What is credit risk?"),
    ("2", "Dataset",            "LendingClub · 500k real loans"),
    ("3", "Data Cleaning",      "From messy 151 cols to 76 clean features"),
    ("4", "Factor Analysis",    "Interdependence technique — 6 latent factors"),
    ("5", "LDA",                "Maximally separating good vs default"),
    ("6", "Logistic Regression","Probability-based binary classification"),
    ("7", "Model Comparison",   "ROC · Accuracy · AUC"),
    ("8", "Live Predictor",     "Interactive demo — real-time prediction"),
]
col_x = [0.3, 6.75]
for i, (num, title, sub) in enumerate(items_agenda):
    col = i % 2; row = i // 2
    x = col_x[col]; y = H - 1.55 - row * 1.35
    ax.add_patch(FancyBboxPatch((x, y-0.95), 5.9, 1.15,
        boxstyle="round,pad=0.04", facecolor=NAVY2, lw=0))
    ax.add_patch(mpatches.Rectangle((x, y-0.95), 0.06, 1.15, facecolor=BLUE, lw=0))
    ax.text(x+0.25, y-0.37, num, color=WHITE, fontsize=22, fontweight="bold",
            va="center", family="DejaVu Sans")
    ax.add_patch(mpatches.Rectangle((x+0.65, y-0.95), 0.04, 1.15,
        facecolor=NAVY3, lw=0))
    ax.text(x+0.82, y-0.22, title, color=WHITE, fontsize=12.5,
            fontweight="bold", va="center", family="DejaVu Sans")
    ax.text(x+0.82, y-0.65, sub,   color=LGREY, fontsize=10,
            va="center", family="DejaVu Sans")
slide_num(ax, 2); pages.append(fig)

# ════════════════════════════════════════════════════════════════════
# SLIDE 3 — THE PROBLEM
# ════════════════════════════════════════════════════════════════════
fig, ax = new_slide("Context", "What Is Credit Risk?")
card(ax, 0.35, 4.6, 5.8, 1.55, "■  The Loan",
     "A bank lends you money today. You promise to repay\n"
     "over time with interest. The bank earns interest;\nyou get capital.")
card(ax, 0.35, 2.9, 5.8, 1.55, "▲  The Risk",
     "The borrower might DEFAULT — stop paying. Banks lend\n"
     "billions, so even a small default rate means massive\nlosses.",
     title_color=GOLD, bg="#1A1710")
card(ax, 0.35, 1.2, 5.8, 1.55, "◆  The Goal",
     "Before lending, predict: 'Will this person repay?'\n"
     "A good model lets banks charge fair rates and\navoid bad loans.",
     title_color=GREEN, bg="#101F1A")

stat_box(ax, 6.5, 5.1, 3.1, 1.4, "$82B+", "US consumer loan\nlosses per year",   RED)
stat_box(ax, 9.8, 5.1, 3.1, 1.4, "~71%",  "Realistic model\naccuracy",           GREEN)
card(ax, 6.5, 2.8, 6.4, 2.1, "Why Multivariate Statistics?",
     "A FICO score is just one number. Default risk depends on\n"
     "DOZENS of factors interacting simultaneously.\n"
     "Multivariate methods see the full picture.", fontsize=11)
card(ax, 6.5, 1.2, 6.4, 1.45, "Two Technique Types Used",
     "Interdependence: Factor Analysis (no outcome variable)\n"
     "Dependence: LDA & Logistic Regression (predict default)", fontsize=11)
slide_num(ax, 3); pages.append(fig)

# ════════════════════════════════════════════════════════════════════
# SLIDE 4 — DATASET
# ════════════════════════════════════════════════════════════════════
fig, ax = new_slide("Data", "The LendingClub Dataset")
stat_box(ax, 0.35, 5.5, 2.95, 1.4, "500K", "Real loan records",    BLUE)
stat_box(ax, 3.45, 5.5, 2.95, 1.4, "151",  "Features per loan",    LBLUE)
stat_box(ax, 6.55, 5.5, 2.95, 1.4,"20.9%", "Default rate",         RED)
stat_box(ax, 9.65, 5.5, 2.95, 1.4, "$15K", "Avg loan amount",      GOLD)

ax.text(0.35, 5.28, "Variables include:", color=LBLUE, fontsize=11, fontweight="bold")
bullets(ax, [
    "Loan info: amount, term, interest rate, monthly installment",
    "Borrower info: income, employment length, debt-to-income ratio",
    "Credit history: FICO score, open accounts, delinquencies",
    "LendingClub grade: A (safest) → G (riskiest)",
    "Outcome: Did they fully repay or default/charge off?",
], 0.35, 4.9, spacing=0.42, fontsize=10.5)

# Status table
ax.text(6.55, 5.28, "Loan Status Breakdown", color=LBLUE, fontsize=11, fontweight="bold")
rows = [
    ("Fully Paid",        "312,340",  GREEN),
    ("Charged Off",       " 78,824",  RED),
    ("Late 31–120 days",  "  2,977",  RED),
    ("Current",           "104,240",  LGREY),
    ("In Grace Period",   "  1,046",  LGREY),
]
for i, (status, count, col) in enumerate(rows):
    y = 4.78 - i*0.56
    bg_c = NAVY2 if i%2==0 else NAVY3
    ax.add_patch(FancyBboxPatch((6.55, y-0.22), 6.42, 0.52,
        boxstyle="square,pad=0", facecolor=bg_c, lw=0))
    ax.text(6.78, y+0.04, status, color=LGREY, fontsize=11, va="center")
    ax.text(12.7, y+0.04, count,  color=col,   fontsize=11, va="center",
            ha="right", fontweight="bold")

card(ax, 0.35, 1.15, 12.62, 1.4,
     "Target Variable",
     "loan_status is mapped to binary: 0 = Fully Paid (good loan), "
     "1 = Charged Off / Defaulted (bad loan).\n"
     "Records in ambiguous states (Current, Late) are excluded to avoid label noise.",
     fontsize=11)
slide_num(ax, 4); pages.append(fig)

# ════════════════════════════════════════════════════════════════════
# SLIDE 5 — CLEANING
# ════════════════════════════════════════════════════════════════════
fig, ax = new_slide("Preprocessing", "Data Cleaning Pipeline")
steps = [
    ("1", "Dropped 58 columns",       "with >40% missing values — hardship/settlement fields"),
    ("2", "Dropped 17 columns",       "irrelevant identifiers and free-text descriptions"),
    ("3", "Engineered target",        "coded loan_status → binary: 0 = paid, 1 = default"),
    ("4", "Parsed text fields",       '"13.5%" → 13.5  |  "36 months" → 36  |  "10+ years" → 10'),
    ("5", "Label-encoded categories", "grade, home_ownership, purpose → numeric"),
    ("6", "Removed outliers",         "cut top/bottom 1% of income, loan amount, revolving balance"),
    ("7", "Dropped remaining NaNs",   "listwise deletion for complete-case analysis"),
]
for i, (num, title, sub) in enumerate(steps):
    y = H - 1.55 - i * 0.72
    ax.add_patch(FancyBboxPatch((0.35, y-0.3), 0.56, 0.56,
        boxstyle="round,pad=0.04", facecolor=BLUE, lw=0))
    ax.text(0.63, y, num, color=WHITE, fontsize=16, fontweight="bold",
            ha="center", va="center", family="DejaVu Sans")
    ax.text(1.1, y+0.08, title, color=WHITE, fontsize=12, fontweight="bold",
            va="center", family="DejaVu Sans")
    ax.text(1.1, y-0.18, sub,   color=LGREY, fontsize=10, va="center", family="DejaVu Sans")

# Result box
ax.add_patch(FancyBboxPatch((7.3, 5.0), 5.6, 1.75,
    boxstyle="round,pad=0.04", facecolor=NAVY2, lw=0))
ax.text(10.1, 6.55, "Before  →  After", color=LGREY, fontsize=11,
        ha="center", va="center", family="DejaVu Sans")
ax.text(8.5,  5.9,  "500K × 151", color=LGREY, fontsize=20, fontweight="bold",
        ha="center", va="center", family="DejaVu Sans")
ax.text(10.1, 5.9,  "→", color=BLUE, fontsize=22, fontweight="bold",
        ha="center", va="center")
ax.text(11.7, 5.9,  "292K × 76", color=WHITE, fontsize=20, fontweight="bold",
        ha="center", va="center", family="DejaVu Sans")
ax.text(10.1, 5.25, "↓ 42% fewer rows  |  ↓ 50% fewer columns",
        color=LGREY, fontsize=9, ha="center", va="center")

card(ax, 7.3, 3.2, 5.6, 1.65, "◆️  Class Imbalance Handling",
     "79% good loans vs 21% defaults.\nBalanced training at 2:1 ratio via undersampling\n"
     "so the model learns real patterns, not just 'always predict good'.",
     title_color=GOLD, bg="#1A1710", fontsize=10.5)
card(ax, 7.3, 1.35, 5.6, 1.65, "▶  Z-Score Standardization",
     "All features scaled to mean=0, std=1.\nRequired before LDA (assumes equal covariance)\n"
     "and Logistic Regression for fair coefficient comparison.",
     title_color=GREEN, bg="#101F1A", fontsize=10.5)
slide_num(ax, 5); pages.append(fig)

# ════════════════════════════════════════════════════════════════════
# SLIDE 6 — FACTOR ANALYSIS METHOD
# ════════════════════════════════════════════════════════════════════
fig, ax = new_slide("Interdependence Technique", "Factor Analysis")
card(ax, 0.35, 5.0, 6.1, 1.7, "◉  What It Does",
     "Groups many correlated variables into a smaller number of\n"
     "hidden (latent) FACTORS. No outcome variable — purely\n"
     "about structure in the data.", fontsize=11)
card(ax, 0.35, 3.25, 6.1, 1.6, "★  The Analogy",
     "You can't measure 'intelligence' directly — but you see it\n"
     "reflected in test scores across math, reading, and logic.\n"
     "FA finds that hidden dimension automatically.",
     title_color=GOLD, bg="#1A1710", fontsize=11)
card(ax, 0.35, 1.35, 6.1, 1.75, "✓  Bartlett's Test — PASSED",
     "χ² = 657,867   |   p < 0.001\n"
     "Variables are significantly correlated → FA is appropriate.\n"
     "20 features used on a 50,000-row sample (sklearn FactorAnalysis).",
     title_color=GREEN, bg="#101F1A", fontsize=11)

ax.text(6.85, H-1.1, "The 6 Factors Found", color=LBLUE, fontsize=12, fontweight="bold")
factors = [
    ("F1", "Loan Size & Cost",       "14.6%"),
    ("F2", "Credit Risk Pricing",    "13.7%"),
    ("F3", "Credit Utilization",     "10.0%"),
    ("F4", "Credit Breadth",          "9.4%"),
    ("F5", "Credit Limit Stress",     "3.9%"),
    ("F6", "Wealth & Assets",         "4.8%"),
]
for i, (f, name, pct) in enumerate(factors):
    y = H - 1.75 - i*0.72
    bg_c = NAVY2 if i%2==0 else NAVY3
    ax.add_patch(FancyBboxPatch((6.85, y-0.28), 6.12, 0.62,
        boxstyle="square,pad=0", facecolor=bg_c, lw=0))
    ax.text(7.15, y+0.04, f,    color=BLUE,  fontsize=12, va="center", fontweight="bold")
    ax.text(7.65, y+0.04, name, color=WHITE, fontsize=11.5, va="center")
    ax.text(12.7, y+0.04, pct,  color=GOLD,  fontsize=12, va="center",
            ha="right", fontweight="bold")

ax.add_patch(FancyBboxPatch((6.85, 1.1), 6.12, 0.9,
    boxstyle="round,pad=0.04", facecolor="#101F1A", lw=0))
ax.text(9.91, 1.75, "Total Variance Explained", color=LGREY, fontsize=9, ha="center")
ax.text(9.91, 1.3, "56.5%", color=GREEN, fontsize=26, fontweight="bold", ha="center")
slide_num(ax, 6); pages.append(fig)

# ════════════════════════════════════════════════════════════════════
# SLIDE 7 — FACTOR ANALYSIS CHARTS
# ════════════════════════════════════════════════════════════════════
fig, ax = new_slide("Interdependence Technique · Results",
                    "Factor Analysis — Visual Results")

ax.text(0.35, H-1.28, "Scree Plot — How Many Factors?",
        color=LBLUE, fontsize=11.5, fontweight="bold")
ax.text(6.85, H-1.28, "Factor Loadings Heatmap",
        color=LBLUE, fontsize=11.5, fontweight="bold")

# Embed images using sub-axes for clean rendering
embed_image(fig, "results/fa_scree_plot.png",
            [0.025, 0.13, 0.475, 0.73])
embed_image(fig, "results/fa_loadings_heatmap.png",
            [0.515, 0.13, 0.475, 0.73])

ax.text(0.35, 0.52, "The 'elbow' at factor 6 confirms we retain 6 factors (eigenvalue > 1).",
        color=LGREY, fontsize=9, style="italic")
ax.text(6.85, 0.52, "Warm = strong positive loading.  Cool = strong negative loading.",
        color=LGREY, fontsize=9, style="italic")
slide_num(ax, 7); pages.append(fig)

# ════════════════════════════════════════════════════════════════════
# SLIDE 8 — LDA METHOD
# ════════════════════════════════════════════════════════════════════
fig, ax = new_slide("Dependence Technique 1", "Linear Discriminant Analysis (LDA)")
card(ax, 0.35, 4.95, 6.0, 1.75, "◆  What It Does",
     "Finds the linear combination of variables that MAXIMALLY\n"
     "SEPARATES two groups — Good Borrowers vs. Defaulters.\n"
     "Produces one 'discriminant score' per borrower.", fontsize=11)
card(ax, 0.35, 3.2, 6.0, 1.6, "★  The Intuition",
     "Borrowers are dots in multi-dimensional space.\n"
     "LDA finds the direction where blue (good) and red\n"
     "(default) groups overlap as little as possible.",
     title_color=GOLD, bg="#1A1710", fontsize=11)
ax.text(0.35, 3.0, "Assumptions:", color=LBLUE, fontsize=11, fontweight="bold")
bullets(ax, [
    "Variables roughly normally distributed within each class",
    "Equal covariance matrices across both classes",
    "Linear decision boundary between the two groups",
], 0.35, 2.62, spacing=0.42, fontsize=10.5)

ax.text(6.75, H-1.28, "LDA Projection — Class Separation",
        color=LBLUE, fontsize=11.5, fontweight="bold")
embed_image(fig, "results/lda_projection.png",
            [0.505, 0.12, 0.49, 0.74])
ax.text(6.75, 0.52,
        "Two peaks = two classes.  Minimal overlap = strong separation.",
        color=LGREY, fontsize=9, style="italic")
slide_num(ax, 8); pages.append(fig)

# ════════════════════════════════════════════════════════════════════
# SLIDE 9 — LDA RESULTS
# ════════════════════════════════════════════════════════════════════
fig, ax = new_slide("Dependence Technique 1 · Results",
                    "LDA — Performance Results")
stat_box(ax, 0.35, 5.5,  2.95, 1.4, "97.3%", "Accuracy",  BLUE)
stat_box(ax, 3.45, 5.5,  2.95, 1.4, "0.997", "AUC-ROC",   GREEN)
stat_box(ax, 6.55, 5.5,  2.95, 1.4, "0.975", "Precision",  GOLD)
stat_box(ax, 9.65, 5.5,  2.95, 1.4, "0.960", "F1-Score",  LBLUE)

ax.text(0.35, 5.3, "Top Discriminant Variables:", color=LBLUE, fontsize=11, fontweight="bold")
bullets(ax, [
    "FICO Score — single most powerful separator between classes",
    "Interest Rate — encodes the lender's own risk assessment",
    "Debt Settlement Flag — red flag indicating financial distress",
    "Installment Amount — higher monthly burden = more default risk",
], 0.35, 4.92, spacing=0.42, fontsize=10.5)

ax.text(6.75, 5.3, "Confusion Matrix",
        color=LBLUE, fontsize=11.5, fontweight="bold")
embed_image(fig, "results/lda_confusion_matrix.png",
            [0.505, 0.12, 0.49, 0.68])

card(ax, 0.35, 1.1, 5.8, 1.65,
     "Interpretation",
     "97.3% accuracy means 97 out of 100 borrowers are classified\n"
     "correctly. AUC = 0.997 means near-perfect discrimination\n"
     "between good and bad borrowers at every threshold.", fontsize=11)
slide_num(ax, 9); pages.append(fig)

# ════════════════════════════════════════════════════════════════════
# SLIDE 10 — LR METHOD
# ════════════════════════════════════════════════════════════════════
fig, ax = new_slide("Dependence Technique 2", "Logistic Regression")
card(ax, 0.35, 5.0, 6.1, 1.7, "▶  What It Does",
     "Predicts the PROBABILITY of default — a number between\n"
     "0% and 100%. Uses the sigmoid (S-shaped) function.\n"
     "If probability > 50% → predict Default.", fontsize=11)

# comparison table
ax.text(0.35, 4.75, "LDA  vs  Logistic Regression:", color=LBLUE, fontsize=11, fontweight="bold")
rows_lr = [
    ("LDA",                "Logistic Regression"),
    ("Assumes normality",  "No distribution assumption"),
    ("Max class separation","Maximises likelihood"),
    ("Discriminant score", "Outputs probability (0–1)"),
]
for i, (a, b) in enumerate(rows_lr):
    y = 4.25 - i*0.62
    bg_c = BLUE if i==0 else (NAVY2 if i%2==1 else NAVY3)
    col  = WHITE
    ax.add_patch(FancyBboxPatch((0.35, y-0.26), 2.9, 0.56,
        boxstyle="square,pad=0", facecolor=bg_c, lw=0))
    ax.add_patch(FancyBboxPatch((3.3, y-0.26), 3.1, 0.56,
        boxstyle="square,pad=0", facecolor=bg_c, lw=0))
    ax.text(0.55, y+0.02, a, color=col, fontsize=10.5, va="center",
            fontweight="bold" if i==0 else "normal")
    ax.text(3.5, y+0.02, b, color=col, fontsize=10.5, va="center",
            fontweight="bold" if i==0 else "normal")

card(ax, 0.35, 1.3, 6.1, 1.5, "✓  Why LR Wins Here",
     "Financial variables are NOT normally distributed —\n"
     "incomes and balances are right-skewed. LR's weaker\n"
     "assumptions make it more robust and it outperforms LDA.",
     title_color=GREEN, bg="#101F1A", fontsize=11)

ax.text(6.75, H-1.28, "Top Coefficients — What Drives Default?",
        color=LBLUE, fontsize=11.5, fontweight="bold")
embed_image(fig, "results/lr_coefficients.png",
            [0.505, 0.12, 0.49, 0.74])
ax.text(6.75, 0.52, "Blue bar = lowers default risk   |   Red bar = raises default risk",
        color=LGREY, fontsize=9, style="italic")
slide_num(ax, 10); pages.append(fig)

# ════════════════════════════════════════════════════════════════════
# SLIDE 11 — LR RESULTS
# ════════════════════════════════════════════════════════════════════
fig, ax = new_slide("Dependence Technique 2 · Results",
                    "Logistic Regression — Performance Results")
stat_box(ax, 0.35, 5.5, 2.95, 1.4, "99.6%",  "Accuracy",  BLUE)
stat_box(ax, 3.45, 5.5, 2.95, 1.4, "0.9997", "AUC-ROC",   GREEN)
stat_box(ax, 6.55, 5.5, 2.95, 1.4, "0.998",  "Precision",  GOLD)
stat_box(ax, 9.65, 5.5, 2.95, 1.4, "0.995",  "F1-Score",  LBLUE)

card(ax, 0.35, 3.55, 5.8, 1.8, "★  LR Outperforms LDA",
     "LR beats LDA by +2.3% accuracy and +0.003 AUC.\n"
     "Consistent with theory: LDA's normality assumptions\n"
     "are violated by skewed financial variables.", title_color=GOLD, bg="#1A1710", fontsize=11)
bullets(ax, [
    "Precision 0.998 — almost zero false alarms on defaults",
    "Recall 0.993 — almost zero missed defaults",
    "F1 = 0.995 — excellent precision-recall balance",
    "AUC = 0.9997 — near-perfect discriminative ability",
], 0.35, 3.3, spacing=0.42, fontsize=10.5)

ax.text(6.75, 5.3, "Confusion Matrix",
        color=LBLUE, fontsize=11.5, fontweight="bold")
embed_image(fig, "results/lr_confusion_matrix.png",
            [0.505, 0.12, 0.49, 0.68])
slide_num(ax, 11); pages.append(fig)

# ════════════════════════════════════════════════════════════════════
# SLIDE 12 — ROC COMPARISON
# ════════════════════════════════════════════════════════════════════
fig, ax = new_slide("Model Comparison",
                    "LDA vs Logistic Regression — ROC Comparison")
embed_image(fig, "results/roc_comparison.png",
            [0.025, 0.12, 0.495, 0.73])

card(ax, 6.75, 5.25, 6.22, 1.5, "▲  What Is the ROC Curve?",
     "Plots True Positive Rate (catching actual defaults)\n"
     "vs. False Positive Rate (wrongly flagging good loans)\n"
     "at every possible decision threshold.", fontsize=11)

ax.text(6.75, 5.0, "Results Summary:", color=LBLUE, fontsize=11, fontweight="bold")
rows_roc = [
    ("Model",                "Accuracy", "AUC-ROC"),
    ("LDA",                  "97.3%",    "0.997"),
    ("Logistic Regression",  "99.6%",    "0.9997"),
]
for i, (m, acc, auc_v) in enumerate(rows_roc):
    y = 4.42 - i*0.66
    bg_c = BLUE if i==0 else (NAVY2 if i%2==1 else NAVY3)
    ax.add_patch(FancyBboxPatch((6.75, y-0.28), 6.22, 0.6,
        boxstyle="square,pad=0", facecolor=bg_c, lw=0))
    col = WHITE if i==0 else LGREY
    ax.text(6.95, y+0.02, m,     color=col,  fontsize=11, va="center",
            fontweight="bold" if i==0 else "normal")
    ax.text(10.5, y+0.02, acc,   color=(GREEN if i>0 else col), fontsize=11,
            va="center", ha="center", fontweight="bold" if i>0 else "normal")
    ax.text(12.4, y+0.02, auc_v, color=(GREEN if i>0 else col), fontsize=11,
            va="center", ha="center", fontweight="bold" if i>0 else "normal")

card(ax, 6.75, 1.25, 6.22, 1.65, "■  AUC Interpretation",
     "AUC = 1.0 → perfect model.\n"
     "AUC = 0.5 → random guessing (coin flip).\n"
     "Both models are at 0.997+ → exceptional discrimination.",
     title_color=GREEN, bg="#101F1A", fontsize=11)
slide_num(ax, 12); pages.append(fig)

# ════════════════════════════════════════════════════════════════════
# SLIDE 13 — LIVE PREDICTOR INFO
# ════════════════════════════════════════════════════════════════════
fig, ax = new_slide(bar_color=GOLD)
ax.text(0.45, H-0.42, "★  INTERACTIVE DEMO",
        color=GOLD, fontsize=9, fontweight="bold", family="DejaVu Sans")
ax.text(0.45, H-0.88, "Live Credit Risk Predictor", color=WHITE,
        fontsize=26, fontweight="bold", family="DejaVu Sans")
ax.text(0.45, H-1.4,
        "The web app lets you enter any borrower's data and get an instant risk assessment "
        "from the trained model.",
        color=LGREY, fontsize=13, family="DejaVu Sans")

presets = [
    ("✓", "Ideal Borrower",     "FICO 790 · Income $120K\nDTI 8% · RevUtil 12% · Grade A",    GREEN, "Will Repay"),
    ("◆", "Average Borrower",   "FICO 700 · Income $65K\nDTI 18% · RevUtil 45% · Grade C",   LBLUE, "Will Repay"),
    ("▲", "Risky Borrower",     "FICO 620 · Income $42K\nDTI 32% · RevUtil 78% · Grade E",    GOLD, "Borderline"),
    ("▲","Very High Risk",      "FICO 560 · Income $28K\nDTI 40% · RevUtil 95% · Grade G",     RED, "Default Risk"),
]
for i, (icon, name, details, col, verdict) in enumerate(presets):
    x = 0.35 + i*3.26
    ax.add_patch(FancyBboxPatch((x, 2.1), 3.0, 3.3,
        boxstyle="round,pad=0.06", facecolor=NAVY2, lw=0))
    ax.text(x+1.5, 5.08, icon,    color=col,   fontsize=24, ha="center", va="center")
    ax.text(x+1.5, 4.6,  name,    color=col,   fontsize=12, ha="center", va="center",
            fontweight="bold")
    ax.text(x+1.5, 4.05, details, color=LGREY, fontsize=9.5, ha="center", va="center",
            multialignment="center")
    ax.add_patch(FancyBboxPatch((x+0.2, 2.25), 2.6, 0.52,
        boxstyle="round,pad=0.04", facecolor=col, lw=0))
    ax.text(x+1.5, 2.52, verdict, color=NAVY, fontsize=12, ha="center", va="center",
            fontweight="bold")

ax.text(0.35, 1.85, "The live predictor lets you:", color=LBLUE, fontsize=11, fontweight="bold")
bullets(ax, [
    "Toggle between Logistic Regression and LDA with one click",
    "Enter any custom loan values across all 15 origination features",
    "See probability bars, risk tier, and top 3 risk drivers instantly",
], 0.35, 1.48, spacing=0.38, fontsize=10.5)
slide_num(ax, 13); pages.append(fig)

# ════════════════════════════════════════════════════════════════════
# SLIDE 14 — DATA LEAKAGE
# ════════════════════════════════════════════════════════════════════
fig, ax = new_slide(bar_color=RED)
ax.text(0.45, H-0.42, "CRITICAL ANALYSIS",
        color=RED, fontsize=9, fontweight="bold")
ax.text(0.45, H-0.88, "Key Limitation: Data Leakage", color=WHITE,
        fontsize=26, fontweight="bold")
ax.text(0.45, H-1.42,
        "The full-dataset models (97–99%) include variables only known AFTER the loan resolves.",
        color=LGREY, fontsize=13)

leaks = [
    ("total_rec_prncp",        "Total principal recovered — only exists after the loan ends"),
    ("recoveries",             "Money recovered post-default — populated only IF there was a default"),
    ("collection_recovery_fee","Fee charged to recover defaulted funds — post-event only"),
    ("last_pymnt_amnt",        "Last payment amount — known only after payment history unfolds"),
]
for i, (var, desc) in enumerate(leaks):
    y = H - 2.1 - i*0.85
    ax.add_patch(FancyBboxPatch((0.35, y-0.48), 5.9, 0.75,
        boxstyle="round,pad=0.04", facecolor="#1F1010", lw=0))
    ax.text(0.7, y-0.08, "●  " + var, color=RED, fontsize=11, va="center", fontweight="bold")
    ax.text(0.7, y-0.38, desc,          color=LGREY, fontsize=10, va="center")

card(ax, 6.65, 3.85, 6.3, 1.95, "★  The Analogy",
     "Trying to predict if a student will fail — and using\n"
     "their final exam score as a predictor. Of course the\n"
     "model is perfect. You're using the answer to predict\n"
     "the answer.",
     title_color=GOLD, bg="#1A1710", fontsize=11)
card(ax, 6.65, 1.9, 6.3, 1.8, "✓  Our Live Predictor Fixes This",
     "The interactive predictor uses ONLY 15 origination-time\n"
     "features — variables known at application time.\n"
     "That is why accuracy is ~71%, not 99%. Honest.",
     title_color=GREEN, bg="#101F1A", fontsize=11)
card(ax, 6.65, 1.0, 6.3, 0.8, "◉  What Real Banks Do",
     "Only application-time data · Must comply with ECOA · "
     "Models are audited for discriminatory patterns.",
     title_color=LBLUE, fontsize=10)
slide_num(ax, 14); pages.append(fig)

# ════════════════════════════════════════════════════════════════════
# SLIDE 15 — CONCLUSION
# ════════════════════════════════════════════════════════════════════
fig, ax = new_slide("Conclusion", "Summary & Takeaways")
cards_c = [
    ("■", "Real Data, Real Cleaning",
     "500K messy records → 292K clean rows\nthrough a rigorous 7-step pipeline.", WHITE),
    ("◆", "Factor Analysis",
     "6 latent factors explain 56.5%\nof variance in loan characteristics.", LBLUE),
    ("■", "LDA",
     "Separated good from default borrowers:\n97.3% accuracy, AUC = 0.997.", BLUE),
    ("▶", "Logistic Regression",
     "Outperformed LDA: 99.6% accuracy,\nAUC = 0.9997. Better fit for skewed data.", GREEN),
    ("▲", "Data Leakage",
     "High full-model accuracy partly due to\npost-outcome variables. Honest model ≈71%.", RED),
    ("»", "Live Predictor",
     "Interactive web app: enter loan values\nand watch the trained model decide.", GOLD),
]
positions = [(0.35, 3.1), (4.55, 3.1), (8.75, 3.1),
             (0.35, 1.0), (4.55, 1.0), (8.75, 1.0)]
for (x, y), (icon, title, txt, col) in zip(positions, cards_c):
    ax.add_patch(FancyBboxPatch((x, y), 3.8, 1.9,
        boxstyle="round,pad=0.05", facecolor=NAVY2, lw=0))
    ax.text(x+0.3, y+1.65, icon,  color=col,   fontsize=20, va="center")
    ax.text(x+0.3, y+1.32, title, color=col,   fontsize=11, va="center", fontweight="bold")
    ax.text(x+0.3, y+0.72, txt,   color=LGREY, fontsize=10, va="center",
            multialignment="left", linespacing=1.45)

# Stats banner
ax.add_patch(mpatches.Rectangle((0, 5.2), W, 1.3, facecolor=NAVY2, lw=0))
stats_banner = [
    ("292K", "Clean Records"),
    ("6",    "Latent Factors"),
    ("56.5%","Variance Explained"),
    ("0.997","LDA AUC"),
    ("0.9997","LR AUC"),
]
for i, (v, l) in enumerate(stats_banner):
    x = 1.3 + i*2.5
    ax.text(x, 6.15, v, color=WHITE, fontsize=22, fontweight="bold", ha="center")
    ax.text(x, 5.55, l, color=LGREY, fontsize=9, ha="center")

ax.text(W/2, H-1.15, "Thank You", color=WHITE, fontsize=28, fontweight="bold", ha="center")
ax.text(W/2, H-1.65, "Lana Jalal Gidan  ·  lgidan@binghamton.edu  ·  SSIE Department",
        color=LGREY, fontsize=11, ha="center")
slide_num(ax, 15); pages.append(fig)

# ── Save all pages ────────────────────────────────────────────────
out_path = "Gidan_CreditRisk_Presentation.pdf"
with PdfPages(out_path) as pdf:
    for fig in pages:
        pdf.savefig(fig, bbox_inches="tight", dpi=150,
                    facecolor=fig.get_facecolor())
        plt.close(fig)
print(f"Saved: {out_path}  ({len(pages)} slides)")

"""
Generates a professional academic-style PDF report for homework questions 10.4, 10.5, 10.6, 11.5
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.lines import Line2D
import matplotlib.image as mpimg
import pickle, numpy as np, os

with open("hw_results.pkl","rb") as f:
    R = pickle.load(f)

# ── Academic colour palette (clean, minimal) ─────────────────────
BLACK   = "#111111"
DARK    = "#222222"
MID     = "#444444"
GREY    = "#666666"
LGREY   = "#999999"
RULE    = "#CCCCCC"
BGLIGHT = "#F5F7FA"
BGBOX   = "#EEF2F6"
ACCENT  = "#1A3A6B"   # deep academic blue
ACCENT2 = "#2E6DA4"
RED2    = "#B82020"
GREEN2  = "#1A6B35"
WHITE   = "#FFFFFF"

W, H = 11.0, 8.5   # letter landscape
pages = []

SERIF = "DejaVu Serif"
SANS  = "DejaVu Sans"

def new_page():
    fig = plt.figure(figsize=(W, H), facecolor=WHITE)
    ax  = fig.add_axes([0, 0, 1, 1], facecolor=WHITE)
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    # top rule
    ax.add_patch(Rectangle((0.5, H-0.35), W-1.0, 0.028, facecolor=ACCENT, lw=0))
    # bottom rule
    ax.add_patch(Rectangle((0.5, 0.32),   W-1.0, 0.028, facecolor=ACCENT, lw=0))
    return fig, ax

def pnum(ax, n, tot):
    ax.text(W/2, 0.18, f"— {n} —", color=LGREY, fontsize=8.5,
            ha="center", va="center", family=SERIF)
    ax.text(W-0.5, 0.18, f"of {tot}", color=LGREY, fontsize=7.5,
            ha="right", va="center", family=SERIF)

def section(ax, label, x, y, w=9.5):
    ax.add_patch(Rectangle((x, y-0.02), w, 0.38, facecolor=BGLIGHT, lw=0))
    ax.add_patch(Rectangle((x, y-0.02), 0.06, 0.38, facecolor=ACCENT, lw=0))
    ax.text(x+0.18, y+0.17, label, color=ACCENT, fontsize=12,
            fontweight="bold", va="center", family=SERIF)

def body(ax, text, x, y, w=9.5, fs=9.5, color=DARK, ls=1.6):
    ax.text(x, y, text, color=color, fontsize=fs, va="top",
            wrap=True, family=SERIF, multialignment="left",
            linespacing=ls, transform=ax.transData)

def kv_row(ax, x, y, w, key, val, shade=False, hdr=False):
    h = 0.34
    bg = BGBOX if shade else WHITE
    if hdr: bg = ACCENT
    ax.add_patch(Rectangle((x, y), w, h, facecolor=bg, lw=0))
    ax.add_patch(Rectangle((x, y), w, h, facecolor="none",
                            edgecolor=RULE, lw=0.6))
    kcol = WHITE if hdr else ACCENT
    vcol = WHITE if hdr else DARK
    ax.text(x+0.15, y+h/2, key, color=kcol, fontsize=9,
            va="center", family=SERIF, fontweight="bold" if hdr else "normal")
    ax.text(x+w-0.15, y+h/2, val, color=vcol, fontsize=9,
            va="center", ha="right", family=SERIF, fontweight="bold" if hdr else "normal")

def embed(fig, path, rect):
    if os.path.exists(path):
        iax = fig.add_axes(rect)
        iax.set_axis_off()
        iax.imshow(mpimg.imread(path), aspect="auto")

def hline(ax, y, x0=0.5, x1=10.5):
    ax.add_patch(Rectangle((x0, y), x1-x0, 0.012, facecolor=RULE, lw=0))

TOTAL_PAGES = 12

# ════════════════════════════════════════════════════════════════
# PAGE 1 — TITLE / COVER
# ════════════════════════════════════════════════════════════════
fig, ax = new_page()

ax.add_patch(Rectangle((0.5, H-2.2), W-1.0, 1.75, facecolor=ACCENT, lw=0))
ax.text(W/2, H-0.75,
        "MULTIVARIATE STATISTICS",
        color=WHITE, fontsize=11, ha="center", va="center",
        family=SERIF, style="italic")
ax.text(W/2, H-1.2,
        "Homework Solutions",
        color=WHITE, fontsize=26, fontweight="bold", ha="center", va="center",
        family=SERIF)
ax.text(W/2, H-1.75,
        "Questions 10.4  ·  10.5  ·  10.6  ·  11.5",
        color="#B8D0F0", fontsize=12, ha="center", va="center", family=SERIF)

ax.text(W/2, H-2.6, "Logistic Regression Analysis and MANOVA",
        color=DARK, fontsize=13, ha="center", va="center", family=SERIF, style="italic")

hline(ax, H-2.95)

info = [
    ("Author",    "Lana Jalal Gidan"),
    ("Email",     "lgidan@binghamton.edu"),
    ("Department","Systems Science and Industrial Engineering"),
    ("University","Binghamton University"),
    ("Course",    "Multivariate Statistics"),
    ("Date",      "April 2026"),
]
for i, (k, v) in enumerate(info):
    y = H - 3.45 - i * 0.45
    ax.text(2.8, y, f"{k}:", color=LGREY, fontsize=10, ha="right",
            va="center", family=SERIF, style="italic")
    ax.text(3.0, y, v,      color=DARK,  fontsize=10, ha="left",
            va="center", family=SERIF)

hline(ax, H-6.2)
ax.text(W/2, H-6.55,
        "Statistical Software: Python 3.11 (statsmodels, scikit-learn, scipy, matplotlib)  "
        "and SAS (PROC LOGISTIC, PROC DISCRIM, PROC GLM)",
        color=GREY, fontsize=8.5, ha="center", family=SERIF)

ax.text(W/2, H-7.0,
        "Data Sources: ADMIS.DAT · DEPRES.DAT · PHONE.DAT · Table Q10.2",
        color=GREY, fontsize=8.5, ha="center", family=SERIF)

pnum(ax, 1, TOTAL_PAGES); pages.append(fig)

# ════════════════════════════════════════════════════════════════
# PAGE 2 — Q10.4 DATA DESCRIPTION & SETUP
# ════════════════════════════════════════════════════════════════
fig, ax = new_page()
ax.text(0.5, H-0.6, "Question 10.4   Admissions Data — Logistic Regression",
        color=ACCENT, fontsize=14, fontweight="bold", family=SERIF)
hline(ax, H-0.75)

section(ax, "10.4.1   Data Preparation", 0.5, H-1.28, w=10.0)
body(ax,
     "The ADMIS.DAT file contains 85 MBA applicants classified as: (1) Admitted, (2) Not Admitted, "
     "and (3) Borderline. Following the question instructions, only admitted and not-admitted applicants "
     "are retained (n = 59). A new binary variable admit is created: 0 = Admitted, 1 = Not Admitted. "
     "GPA scores are recoded into four ordinal categories as specified in the table below.",
     0.5, H-1.85, fs=9.5)

section(ax, "10.4.2   GPA Category Recoding", 0.5, H-2.95, w=10.0)
# Table
col_w = [1.6, 1.8, 1.6, 1.6, 1.6]
col_x = [0.5, 2.1, 3.9, 5.5, 7.1]
hdrs  = ["GPA Category", "GPA Range", "Admitted (n)", "Not Admitted (n)", "Total (n)"]
rows_gpa = [
    ("1 (Reference)", "< 2.50",     "0",  "15", "15"),
    ("2",             "2.51 – 3.00","1",  "13", "14"),
    ("3",             "3.01 – 3.50","22",  "0", "22"),
    ("4",             "> 3.50",     "8",   "0",  "8"),
    ("Total",         "—",         "31",  "28", "59"),
]
y0 = H-3.52
for j, (hdr, cw) in enumerate(zip(hdrs, col_w)):
    ax.add_patch(Rectangle((col_x[j], y0-0.01), cw, 0.36,
                            facecolor=ACCENT, lw=0))
    ax.add_patch(Rectangle((col_x[j], y0-0.01), cw, 0.36,
                            facecolor="none", edgecolor=RULE, lw=0.6))
    ax.text(col_x[j]+cw/2, y0+0.17, hdr, color=WHITE, fontsize=9,
            ha="center", va="center", family=SERIF, fontweight="bold")
for i, row in enumerate(rows_gpa):
    y_r = y0 - 0.37*(i+1)
    bg = BGBOX if i % 2 == 0 else WHITE
    if i == len(rows_gpa)-1: bg = BGLIGHT
    for j, (val, cw) in enumerate(zip(row, col_w)):
        ax.add_patch(Rectangle((col_x[j], y_r-0.01), cw, 0.36,
                                facecolor=bg, lw=0))
        ax.add_patch(Rectangle((col_x[j], y_r-0.01), cw, 0.36,
                                facecolor="none", edgecolor=RULE, lw=0.6))
        fw = "bold" if i == len(rows_gpa)-1 else "normal"
        ax.text(col_x[j]+cw/2, y_r+0.17, val, color=DARK, fontsize=9,
                ha="center", va="center", family=SERIF, fontweight=fw)

section(ax, "10.4.3   Dummy Variable Coding", 0.5, H-5.65, w=10.0)
body(ax,
     "With four GPA categories, three dummy variables are created using Category 1 (GPA < 2.50) "
     "as the reference group: GPA2 = 1 if Category 2, else 0;  GPA3 = 1 if Category 3, else 0; "
     "GPA4 = 1 if Category 4, else 0. "
     "Note: GPA category produces near-perfect separation (all Category 3 and 4 applicants were "
     "admitted; all Category 1 were rejected). Under perfect separation, maximum likelihood "
     "estimates diverge to ±∞. A ridge-penalized logistic regression (L2, C = 1) is applied "
     "to yield stable, interpretable coefficients.",
     0.5, H-6.2, fs=9.5)

pnum(ax, 2, TOTAL_PAGES); pages.append(fig)

# ════════════════════════════════════════════════════════════════
# PAGE 3 — Q10.4 MODEL RESULTS
# ════════════════════════════════════════════════════════════════
fig, ax = new_page()
ax.text(0.5, H-0.6, "Question 10.4   Admissions — Model Results",
        color=ACCENT, fontsize=14, fontweight="bold", family=SERIF)
hline(ax, H-0.75)

section(ax, "10.4.4   Model 1: GPA Category Only", 0.5, H-1.28, w=10.0)

# Coefficient table Model 1
m1p = R["q104_mod1_params"]
rows_m1 = [
    ("Variable",       "Coefficient", "Direction"),
    ("Intercept",      f"{m1p['Intercept']:.4f}", "—"),
    ("GPA2 (2.51–3.00)",f"{m1p['gpa2']:.4f}", "Higher risk vs Cat 1"),
    ("GPA3 (3.01–3.50)",f"{m1p['gpa3']:.4f}", "Strong protection"),
    ("GPA4 (> 3.50)",   f"{m1p['gpa4']:.4f}", "Strong protection"),
]
col_xm = [0.5, 4.2, 6.5]
col_wm = [3.6, 2.2, 3.8]
for j,(hdr,cw) in enumerate(zip(rows_m1[0],col_wm)):
    ax.add_patch(Rectangle((col_xm[j],H-1.84),cw,0.34,facecolor=ACCENT,lw=0))
    ax.add_patch(Rectangle((col_xm[j],H-1.84),cw,0.34,facecolor="none",edgecolor=RULE,lw=0.6))
    ax.text(col_xm[j]+cw/2,H-1.67,hdr,color=WHITE,fontsize=9,ha="center",va="center",
            family=SERIF,fontweight="bold")
for i,row in enumerate(rows_m1[1:]):
    yr=H-2.18-i*0.35; bg=BGBOX if i%2==0 else WHITE
    for j,(val,cw) in enumerate(zip(row,col_wm)):
        ax.add_patch(Rectangle((col_xm[j],yr),cw,0.34,facecolor=bg,lw=0))
        ax.add_patch(Rectangle((col_xm[j],yr),cw,0.34,facecolor="none",edgecolor=RULE,lw=0.6))
        ax.text(col_xm[j]+cw/2,yr+0.17,val,color=DARK,fontsize=9,ha="center",va="center",
                family=SERIF)

acc1=R["q104_acc1"]; auc1=R["q104_auc1"]
body(ax, f"Model 1 Classification Accuracy: {acc1:.1%}    Area Under ROC Curve (AUC): {auc1:.4f}",
     0.5, H-3.1, fs=9.5, color=ACCENT2)

section(ax, "10.4.5   Model 2: GPA Category + GMAT Score", 0.5, H-3.55, w=10.0)
m2p = R["q104_mod2_params"]
rows_m2 = [
    ("Variable",        "Coefficient", "Interpretation"),
    ("Intercept",       f"{m2p['Intercept']:.4f}", "—"),
    ("GPA2 (2.51–3.00)",f"{m2p['gpa2']:.4f}",     "Higher risk vs Cat 1 (less strong with GMAT)"),
    ("GPA3 (3.01–3.50)",f"{m2p['gpa3']:.4f}",     "Strongly reduces P(rejection)"),
    ("GPA4 (> 3.50)",   f"{m2p['gpa4']:.4f}",     "Strongly reduces P(rejection)"),
    ("GMAT (std.)",     f"{m2p['gmat(std)']:.4f}", "Higher GMAT → lower P(rejection)"),
]
for j,(hdr,cw) in enumerate(zip(rows_m2[0],col_wm)):
    ax.add_patch(Rectangle((col_xm[j],H-4.12),cw,0.34,facecolor=ACCENT,lw=0))
    ax.add_patch(Rectangle((col_xm[j],H-4.12),cw,0.34,facecolor="none",edgecolor=RULE,lw=0.6))
    ax.text(col_xm[j]+cw/2,H-3.95,hdr,color=WHITE,fontsize=9,ha="center",va="center",
            family=SERIF,fontweight="bold")
for i,row in enumerate(rows_m2[1:]):
    yr=H-4.46-i*0.35; bg=BGBOX if i%2==0 else WHITE
    for j,(val,cw) in enumerate(zip(row,col_wm)):
        ax.add_patch(Rectangle((col_xm[j],yr),cw,0.34,facecolor=bg,lw=0))
        ax.add_patch(Rectangle((col_xm[j],yr),cw,0.34,facecolor="none",edgecolor=RULE,lw=0.6))
        ax.text(col_xm[j]+cw/2,yr+0.17,val,color=DARK,fontsize=9,ha="center",va="center",
                family=SERIF)

acc2=R["q104_acc2"]; auc2=R["q104_auc2"]
body(ax, f"Model 2 Classification Accuracy: {acc2:.1%}    Area Under ROC Curve (AUC): {auc2:.4f}",
     0.5, H-6.45, fs=9.5, color=ACCENT2)

section(ax, "10.4.6   Discussion", 0.5, H-6.9, w=10.0)
body(ax,
     "GPA category alone achieves 98.3% classification accuracy, demonstrating it is the dominant "
     "predictor of admission status. The negative coefficients on GPA3 and GPA4 confirm that higher "
     "GPA categories substantially reduce the log-odds of rejection. Adding GMAT raises the AUC to "
     "1.000 (perfect discrimination), and GMAT's negative coefficient confirms that higher scores "
     "improve admission prospects. However, overall accuracy decreases marginally (96.6%) due to two "
     "additional misclassifications, suggesting GMAT provides limited incremental gain beyond GPA "
     "category in this sample.",
     0.5, H-7.45, fs=9.5)

pnum(ax, 3, TOTAL_PAGES); pages.append(fig)

# ════════════════════════════════════════════════════════════════
# PAGE 4 — Q10.4 FIGURES
# ════════════════════════════════════════════════════════════════
fig, ax = new_page()
ax.text(0.5, H-0.6, "Question 10.4   Admissions — Figures",
        color=ACCENT, fontsize=14, fontweight="bold", family=SERIF)
hline(ax, H-0.75)
body(ax,
     "Figure 10.4: (Left) ROC curves for Model 1 and Model 2.  "
     "(Centre) Confusion matrix for Model 2 (GPA + GMAT).  "
     "(Right) Estimated coefficients for Model 2.",
     0.5, H-1.05, fs=9.5, color=GREY)
embed(fig, "hw_plots/q104_results.png", [0.04, 0.1, 0.93, 0.73])
ax.add_patch(Rectangle((0.4, 0.4), W-0.8, 6.6, facecolor="none",
                        edgecolor=RULE, lw=0.8))
pnum(ax, 4, TOTAL_PAGES); pages.append(fig)

# ════════════════════════════════════════════════════════════════
# PAGE 5 — Q10.5 HAND CALCULATIONS
# ════════════════════════════════════════════════════════════════
fig, ax = new_page()
ax.text(0.5, H-0.6, "Question 10.5   Cholesterol & Heart Disease — Logistic Regression",
        color=ACCENT, fontsize=14, fontweight="bold", family=SERIF)
hline(ax, H-0.75)

section(ax, "10.5.1   Data Description", 0.5, H-1.28, w=10.0)
body(ax,
     "Table Q10.2 presents cross-sectional data on 114 males aged 40–65, classified by blood "
     "cholesterol level (four groups) and heart disease status (Present/Absent). "
     "Total cases: Present = 91, Absent = 23, n = 114.",
     0.5, H-1.85, fs=9.5)

section(ax, "10.5.2(a)   Probabilities, Odds, and Log-Odds (Hand Calculations)", 0.5, H-2.42, w=10.0)

# Main table
hdrs_c = ["Cholesterol Level","Present","Absent","Total",
           "P(Disease)","Odds","Log-Odds"]
col_xc = [0.5, 2.5, 3.5, 4.5, 5.5, 7.0, 8.5]
col_wc = [2.0, 1.0, 1.0, 1.0, 1.5, 1.5, 1.7]
rows_c5 = [
    ("<200",    "6",  "5", "11", "0.5455","1.2000","0.1823"),
    ("200–219","10",  "6", "16", "0.6250","1.6667","0.5108"),
    ("220–259","30",  "5", "35", "0.8571","6.0000","1.7918"),
    (">259",   "45",  "7", "52", "0.8654","6.4286","1.8608"),
]
y0c = H-2.97
for j,(hdr,cw) in enumerate(zip(hdrs_c,col_wc)):
    ax.add_patch(Rectangle((col_xc[j],y0c-0.01),cw,0.34,facecolor=ACCENT,lw=0))
    ax.add_patch(Rectangle((col_xc[j],y0c-0.01),cw,0.34,facecolor="none",edgecolor=RULE,lw=0.6))
    ax.text(col_xc[j]+cw/2,y0c+0.16,hdr,color=WHITE,fontsize=8.5,ha="center",va="center",
            family=SERIF,fontweight="bold")
for i,row in enumerate(rows_c5):
    yr=y0c-0.35*(i+1); bg=BGBOX if i%2==0 else WHITE
    for j,(val,cw) in enumerate(zip(row,col_wc)):
        ax.add_patch(Rectangle((col_xc[j],yr),cw,0.34,facecolor=bg,lw=0))
        ax.add_patch(Rectangle((col_xc[j],yr),cw,0.34,facecolor="none",edgecolor=RULE,lw=0.6))
        col_v = ACCENT2 if j >= 4 else DARK
        ax.text(col_xc[j]+cw/2,yr+0.16,val,color=col_v,fontsize=9,ha="center",va="center",
                family=SERIF)

section(ax, "10.5.2(b)   Hand Logistic Regression via Simple Linear Regression on Log-Odds",
        0.5, H-4.55, w=10.0)
b0=R["q105_b0"]; b1=R["q105_b1"]
body(ax,
     "Using cholesterol group midpoints (<200=185, 200–219=209.5, 220–259=239.5, >259=270), "
     "a simple linear regression of the log-odds on the midpoint yields:",
     0.5, H-5.1, fs=9.5)
ax.add_patch(Rectangle((1.5, H-5.65), 7.5, 0.44, facecolor=BGBOX, lw=0))
ax.add_patch(Rectangle((1.5, H-5.65), 7.5, 0.44, facecolor="none", edgecolor=RULE, lw=0.8))
ax.text(5.25, H-5.43,
        f"logit[ P(Disease) ]  =  {b0:.4f}  +  {b1:.6f}  ×  Cholesterol",
        color=DARK, fontsize=11, ha="center", va="center", family=SERIF, style="italic")
body(ax,
     f"Interpretation: The slope ({b1:.6f}) is positive and statistically meaningful, indicating "
     "that each unit increase in cholesterol is associated with an increase in the log-odds of "
     "heart disease. The intercept (−3.9181) represents the log-odds when cholesterol = 0.",
     0.5, H-6.3, fs=9.5)

section(ax, "10.5.3(c,d)   Software LR Results & Classification Table",
        0.5, H-6.85, w=10.0)
pc=R["q105_sw_params"]; pvc=R["q105_sw_pvalues"]
rows_sw=[("Intercept","Ref: <200",f"{pc['Intercept']:.4f}",f"{pvc['Intercept']:.4f}","No"),
         ("200–219",  "vs <200",   f"{pc['c200_219']:.4f}", f"{pvc['c200_219']:.4f}","No"),
         ("220–259",  "vs <200",   f"{pc['c220_259']:.4f}", f"{pvc['c220_259']:.4f}","Yes*"),
         (">259",     "vs <200",   f"{pc['c_gt259']:.4f}",  f"{pvc['c_gt259']:.4f}", "Yes*")]
col_xs=[0.5,2.8,4.9,6.8,8.6]
col_ws=[2.3,2.1,1.9,1.8,1.6]
hdrss=["Term","Reference","Coefficient","p-value","Significant"]
yr0=H-7.40
for j,(h,cw) in enumerate(zip(hdrss,col_ws)):
    ax.add_patch(Rectangle((col_xs[j],yr0-0.01),cw,0.34,facecolor=ACCENT,lw=0))
    ax.add_patch(Rectangle((col_xs[j],yr0-0.01),cw,0.34,facecolor="none",edgecolor=RULE,lw=0.6))
    ax.text(col_xs[j]+cw/2,yr0+0.16,h,color=WHITE,fontsize=9,ha="center",va="center",
            family=SERIF,fontweight="bold")
for i,row in enumerate(rows_sw):
    yr=yr0-0.35*(i+1); bg=BGBOX if i%2==0 else WHITE
    for j,(val,cw) in enumerate(zip(row,col_ws)):
        ax.add_patch(Rectangle((col_xs[j],yr),cw,0.34,facecolor=bg,lw=0))
        ax.add_patch(Rectangle((col_xs[j],yr),cw,0.34,facecolor="none",edgecolor=RULE,lw=0.6))
        vc = GREEN2 if (j==4 and "Yes" in val) else DARK
        ax.text(col_xs[j]+cw/2,yr+0.16,val,color=vc,fontsize=9,ha="center",va="center",
                family=SERIF)

pnum(ax, 5, TOTAL_PAGES); pages.append(fig)

# ════════════════════════════════════════════════════════════════
# PAGE 6 — Q10.5 FIGURES + DISCUSSION
# ════════════════════════════════════════════════════════════════
fig, ax = new_page()
ax.text(0.5, H-0.6, "Question 10.5   Cholesterol — Figures and Discussion",
        color=ACCENT, fontsize=14, fontweight="bold", family=SERIF)
hline(ax, H-0.75)
body(ax,
     "Figure 10.5: (Left) Observed P(Disease) by cholesterol group.  "
     "(Centre) Log-odds with fitted regression line (hand calculation).  "
     "(Right) Confusion matrix for software LR model.",
     0.5, H-1.05, fs=9.5, color=GREY)
embed(fig, "hw_plots/q105_results.png", [0.04, 0.32, 0.93, 0.50])
ax.add_patch(Rectangle((0.4, 0.38), W-0.8, 4.35, facecolor="none",
                        edgecolor=RULE, lw=0.8))
section(ax, "10.5.4   Discussion of Classification Table", 0.5, H-1.22, w=10.0)
body(ax,
     "The software logistic regression model yields an overall accuracy of 79.8%. However, the "
     "classification table shows the model predicts all subjects as having heart disease present — "
     "a consequence of severe class imbalance (91 present vs. 23 absent). In such settings, raw "
     "accuracy is misleading; the model has 100% sensitivity but 0% specificity. "
     "The classification table should therefore be interpreted with caution: it should be "
     "accompanied by the AUC, sensitivity/specificity trade-off, and ideally a ROC curve. "
     "A lower decision threshold (e.g., 0.35) or balanced resampling would improve specificity.",
     0.5, H-1.80, fs=9.5)
pnum(ax, 6, TOTAL_PAGES); pages.append(fig)

# ════════════════════════════════════════════════════════════════
# PAGE 7 — Q10.6 LR SETUP + RESULTS
# ════════════════════════════════════════════════════════════════
fig, ax = new_page()
ax.text(0.5, H-0.6, "Question 10.6   Depression Data — Logistic Regression",
        color=ACCENT, fontsize=14, fontweight="bold", family=SERIF)
hline(ax, H-0.75)

section(ax, "10.6.1   Dataset and Model Specification", 0.5, H-1.28, w=10.0)
body(ax,
     "The DEPRES.DAT file contains 294 subjects. The dependent variable is CASES (0 = Normal, "
     "1 = Depressed, defined as CESD > 16; distribution: 244 normal, 50 depressed). "
     "Fourteen demographic and health predictors are entered simultaneously: "
     "SEX, AGE, MARITAL, EDUCAT, EMPLOY, INCOME, RELIG, DRINK, HEALTH, REGDOC, TREAT, "
     "BEDDAYS, ACUTEILL, and CHRONILL.",
     0.5, H-1.85, fs=9.5)

section(ax, "10.6.2   Logistic Regression Coefficients", 0.5, H-2.42, w=10.0)
lp=R["q106_lr_params"]; lpv=R["q106_lr_pvalues"]
var_list=[("SEX","Female sex raises P(depression)"),
          ("AGE","Older age slightly protective"),
          ("MARITAL","Marital status (not sig.)"),
          ("EDUCAT","Education level (not sig.)"),
          ("EMPLOY","Employment status (not sig.)"),
          ("INCOME","Higher income lowers risk"),
          ("RELIG","Religion raises odds (cultural context)"),
          ("DRINK","Drinking lowers odds (not sig.)"),
          ("HEALTH","Poorer health raises risk (not sig.)"),
          ("REGDOC","Regular doctor (not sig.)"),
          ("TREAT","Treatment (not sig.)"),
          ("BEDDAYS","Days in bed raises risk"),
          ("ACUTEILL","Acute illness (not sig.)"),
          ("CHRONILL","Chronic illness (not sig.)")]
col_xd=[0.5,2.8,4.6,6.4,8.2]
col_wd=[2.3,1.8,1.8,1.8,1.8]
hdrsd=["Variable","Coefficient","p-value","Significant","Interpretation"]
y0d=H-2.97
for j,(h,cw) in enumerate(zip(hdrsd,col_wd)):
    ax.add_patch(Rectangle((col_xd[j],y0d-0.01),cw,0.3,facecolor=ACCENT,lw=0))
    ax.add_patch(Rectangle((col_xd[j],y0d-0.01),cw,0.3,facecolor="none",edgecolor=RULE,lw=0.6))
    ax.text(col_xd[j]+cw/2,y0d+0.14,h,color=WHITE,fontsize=8.5,ha="center",va="center",
            family=SERIF,fontweight="bold")
for i,(vname,interp) in enumerate(var_list):
    coef=lp.get(vname,0); pval=lpv.get(vname,1)
    sig="Yes*" if pval<0.05 else "No"
    row=(vname,f"{coef:.4f}",f"{pval:.4f}",sig,interp)
    yr=y0d-0.31*(i+1); bg=BGBOX if i%2==0 else WHITE
    for j,(val,cw) in enumerate(zip(row,col_wd)):
        ax.add_patch(Rectangle((col_xd[j],yr),cw,0.3,facecolor=bg,lw=0))
        ax.add_patch(Rectangle((col_xd[j],yr),cw,0.3,facecolor="none",edgecolor=RULE,lw=0.6))
        vc = RED2 if (j==3 and "Yes" in val) else (GREY if j==4 else DARK)
        fs2 = 8.0 if j==4 else 8.5
        ax.text(col_xd[j]+cw/2,yr+0.14,val,color=vc,fontsize=fs2,ha="center",va="center",
                family=SERIF)

pnum(ax, 7, TOTAL_PAGES); pages.append(fig)

# ════════════════════════════════════════════════════════════════
# PAGE 8 — Q10.6 LR vs LDA COMPARISON + FIGURES
# ════════════════════════════════════════════════════════════════
fig, ax = new_page()
ax.text(0.5, H-0.6, "Question 10.6   Depression — LR vs. Discriminant Analysis",
        color=ACCENT, fontsize=14, fontweight="bold", family=SERIF)
hline(ax, H-0.75)

section(ax, "10.6.3   Classification Performance Comparison", 0.5, H-1.28, w=10.0)
# Comparison table
comp_hdrs = ["Method","Overall Accuracy","AUC-ROC","Normal Correct","Depressed Correct"]
comp_rows = [
    ("Logistic Regression",
     f"{R['q106_lr_acc']:.1%}", f"{R['q106_lr_auc']:.4f}", "240/244 (98.4%)", "7/50 (14.0%)"),
    ("Linear Discriminant Analysis",
     f"{R['q106_lda_acc']:.1%}",f"{R['q106_lda_auc']:.4f}","237/244 (97.1%)","7/50 (14.0%)"),
]
col_xc2=[0.5,3.1,4.9,6.5,8.2]
col_wc2=[2.6,1.8,1.6,1.7,1.8]
y0c2=H-1.84
for j,(h,cw) in enumerate(zip(comp_hdrs,col_wc2)):
    ax.add_patch(Rectangle((col_xc2[j],y0c2-0.01),cw,0.34,facecolor=ACCENT,lw=0))
    ax.add_patch(Rectangle((col_xc2[j],y0c2-0.01),cw,0.34,facecolor="none",edgecolor=RULE,lw=0.6))
    ax.text(col_xc2[j]+cw/2,y0c2+0.16,h,color=WHITE,fontsize=8.5,ha="center",va="center",
            family=SERIF,fontweight="bold")
for i,row in enumerate(comp_rows):
    yr=y0c2-0.35*(i+1); bg=BGBOX if i%2==0 else WHITE
    for j,(val,cw) in enumerate(zip(row,col_wc2)):
        ax.add_patch(Rectangle((col_xc2[j],yr),cw,0.34,facecolor=bg,lw=0))
        ax.add_patch(Rectangle((col_xc2[j],yr),cw,0.34,facecolor="none",edgecolor=RULE,lw=0.6))
        ax.text(col_xc2[j]+cw/2,yr+0.16,val,color=DARK,fontsize=9,ha="center",va="center",
                family=SERIF)

section(ax, "10.6.4   Interpretation and Discussion", 0.5, H-3.02, w=10.0)
body(ax,
     "The logistic regression model achieves 84.0% overall accuracy (AUC = 0.779), marginally "
     "outperforming LDA (83.0%, AUC = 0.776). Both methods correctly identify most normal subjects "
     "(>97%) but perform poorly on the depressed group (14% sensitivity), reflecting class imbalance "
     "(244 vs. 50). The four significant LR predictors — SEX (p=0.038), INCOME (p=0.044), "
     "RELIG (p=0.028), and BEDDAYS (p=0.029) — are consistent with epidemiological literature: "
     "female sex, financial stress, lack of religious social support, and physical illness "
     "confinement all elevate depression risk.\n\n"
     "LDA yields nearly identical results, supporting the assumption that a linear boundary "
     "adequately separates the groups. LR is preferred here as it imposes no multivariate "
     "normality assumptions — an important consideration given the mix of binary and ordinal "
     "predictors.",
     0.5, H-3.60, fs=9.5)

body(ax, "Figure 10.6: Confusion matrices (LR and LDA), ROC curves, and LR coefficient plot.",
     0.5, H-5.10, fs=9.5, color=GREY)
embed(fig, "hw_plots/q106_results.png", [0.04, 0.1, 0.93, 0.48])
ax.add_patch(Rectangle((0.4, 0.38), W-0.8, 4.1, facecolor="none", edgecolor=RULE, lw=0.8))

pnum(ax, 8, TOTAL_PAGES); pages.append(fig)

# ════════════════════════════════════════════════════════════════
# PAGE 9 — Q11.5 MANOVA THEORY + DEPRESSION RESULTS
# ════════════════════════════════════════════════════════════════
fig, ax = new_page()
ax.text(0.5, H-0.6, "Question 11.5   MANOVA — Depression and Phone Data",
        color=ACCENT, fontsize=14, fontweight="bold", family=SERIF)
hline(ax, H-0.75)

section(ax, "11.5.1   Method Overview", 0.5, H-1.28, w=10.0)
body(ax,
     "Multivariate Analysis of Variance (MANOVA) extends one-way ANOVA to test whether group "
     "centroids (vectors of means across multiple dependent variables) differ simultaneously. "
     "Wilks' Lambda (Λ) is the primary test statistic: Λ = |W| / |W+B|, where W is the within-group "
     "scatter matrix and B is the between-group scatter matrix. Λ ranges from 0 (perfect separation) "
     "to 1 (no separation). An approximate F-statistic is computed via Rao's approximation.",
     0.5, H-1.85, fs=9.5)

section(ax, "11.5.2   Part A: Depression Data (Group = CASES, DVs = C1–C20)", 0.5, H-2.55, w=10.0)

lam_d=R["q115_dep_lambda"]; F_d=R["q115_dep_F"]; dfd=R["q115_dep_df"]
# Summary stats
smry=[("Test Statistic","Wilks' Lambda","Value",f"{lam_d:.6f}"),
      ("Approx. F-ratio",f"F({dfd[0]:.0f}, {dfd[1]:.0f})","p-value","< 0.0001"),
      ("LDA Accuracy","C1-C20 → CASES","","f{R[q115_dep_lda_acc]:.1%}")]
col_xs9=[0.5,3.0,5.5,7.5]
col_ws9=[2.5,2.5,2.0,2.5]
for j,h in enumerate(["Measure","Detail","","Value"]):
    ax.add_patch(Rectangle((col_xs9[j],H-3.1),col_ws9[j],0.32,facecolor=ACCENT,lw=0))
    ax.add_patch(Rectangle((col_xs9[j],H-3.1),col_ws9[j],0.32,facecolor="none",edgecolor=RULE,lw=0.6))
    ax.text(col_xs9[j]+col_ws9[j]/2,H-2.95,h,color=WHITE,fontsize=9,ha="center",va="center",
            family=SERIF,fontweight="bold")
summary_rows=[
    ("Wilks' Lambda",      "Overall MANOVA test",  "Λ =",     f"{lam_d:.6f}"),
    ("Approx. F-statistic",f"F({dfd[0]:.0f},{dfd[1]:.0f})", "p =","< 0.0001"),
    ("LDA Accuracy","(C1-C20 → CASES)","",f"{R['q115_dep_lda_acc']:.2%}"),
    ("Univariate Sig.","All 20 CES-D items","p <","0.0001"),
]
for i,row in enumerate(summary_rows):
    yr=H-3.42-i*0.34; bg=BGBOX if i%2==0 else WHITE
    for j,(val,cw) in enumerate(zip(row,col_ws9)):
        ax.add_patch(Rectangle((col_xs9[j],yr),cw,0.32,facecolor=bg,lw=0))
        ax.add_patch(Rectangle((col_xs9[j],yr),cw,0.32,facecolor="none",edgecolor=RULE,lw=0.6))
        vc=RED2 if (j==2) else DARK
        ax.text(col_xs9[j]+cw/2,yr+0.15,val,color=vc,fontsize=9,ha="center",va="center",
                family=SERIF)

body(ax,
     "Wilks' Lambda = 0.297 indicates strong group separation (far below 1.0). "
     "The approximate F(20, 273) = 32.31 (p < .0001) provides overwhelming evidence that "
     "the two CASES groups (Normal vs. Depressed) differ significantly on the combined set "
     "of 20 CES-D depression items. All 20 univariate F-tests are also highly significant "
     "(all p < .0001), confirming that every individual depression symptom item contributes "
     "to the group differentiation. LDA using C1-C20 achieves 97.96% classification accuracy, "
     "which markedly exceeds the 84% obtained using only demographic and health predictors "
     "(Q10.6). This highlights the superior discriminative power of symptom items over "
     "background characteristics.",
     0.5, H-5.4, fs=9.5)

section(ax, "11.5.3   Part B: Phone Data (Group = n_phones, DVs = A1–A6)", 0.5, H-6.15, w=10.0)
lam_p=R["q115_ph_lambda"]; F_p=R["q115_ph_F"]; dfp=R["q115_ph_df"]
body(ax,
     f"Wilks' Lambda = {lam_p:.4f},  F({dfp[0]:.0f}, {dfp[1]:.0f}) = {F_p:.2f},  "
     f"p < .0001.  LDA accuracy: {R['q115_ph_lda_acc']:.1%}.\n"
     "Strong evidence that the three phone-ownership groups (1, 2, or 3 phones) differ "
     "significantly across the six attitude items (A1–A6). All six univariate F-tests are "
     "highly significant (all p < .0001).",
     0.5, H-6.72, fs=9.5)

pnum(ax, 9, TOTAL_PAGES); pages.append(fig)

# ════════════════════════════════════════════════════════════════
# PAGE 10 — Q11.5 UNIVARIATE F-TESTS TABLE
# ════════════════════════════════════════════════════════════════
fig, ax = new_page()
ax.text(0.5, H-0.6, "Question 11.5   MANOVA — Univariate F-Test Tables",
        color=ACCENT, fontsize=14, fontweight="bold", family=SERIF)
hline(ax, H-0.75)

section(ax, "11.5.4   Univariate F-Tests — CES-D Items (Depression, CASES grouping)", 0.5, H-1.28, w=10.0)
du = R["q115_dep_univ"]
col_xu=[0.5,2.2,3.9,5.6,7.3,9.0]
col_wu=[1.7,1.7,1.7,1.7,1.7,1.2]
hdrsu=["Item","F-stat","p-value","Sig.","Item","F-stat"]
y0u=H-1.84
for j,(h,cw) in enumerate(zip(hdrsu,col_wu)):
    ax.add_patch(Rectangle((col_xu[j],y0u-0.01),cw,0.3,facecolor=ACCENT,lw=0))
    ax.add_patch(Rectangle((col_xu[j],y0u-0.01),cw,0.3,facecolor="none",edgecolor=RULE,lw=0.6))
    ax.text(col_xu[j]+cw/2,y0u+0.14,h,color=WHITE,fontsize=9,ha="center",va="center",
            family=SERIF,fontweight="bold")
# 2 columns of 10 items
for i in range(10):
    r1=du[i]; r2=du[i+10] if i+10<len(du) else {}
    yr=y0u-0.3*(i+1); bg=BGBOX if i%2==0 else WHITE
    vals1=[r1["variable"],f"{r1['F']:.3f}",f"{r1['p-value']:.4f}","*" if r1["significant"] else ""]
    vals2=[r2.get("variable",""),f"{r2.get('F',0):.3f}"] if r2 else ["",""]
    for j,(val,cw) in enumerate(zip(vals1+vals2,col_wu)):
        ax.add_patch(Rectangle((col_xu[j],yr),cw,0.29,facecolor=bg,lw=0))
        ax.add_patch(Rectangle((col_xu[j],yr),cw,0.29,facecolor="none",edgecolor=RULE,lw=0.6))
        vc=RED2 if (j==3 and val=="*") else DARK
        ax.text(col_xu[j]+cw/2,yr+0.13,val,color=vc,fontsize=9,ha="center",va="center",
                family=SERIF)

section(ax, "11.5.5   Univariate F-Tests — Attitude Items (Phone, n_phones grouping)",
        0.5, H-5.1, w=10.0)
pu = R["q115_ph_univ"]
hdrsp=["Item","CES-D Scale Label","F-statistic","p-value","Significant"]
phone_labels={"A1":"Call LD only when necessary","A2":"One phone sufficient",
              "A3":"Multiple phones worthwhile","A4":"Avg. bill smaller",
              "A5":"Multi-phone wasteful","A6":"Get best model"}
col_xp=[0.5,1.8,5.5,7.3,8.9]
col_wp=[1.3,3.7,1.8,1.6,1.3]
y0p=H-5.65
for j,(h,cw) in enumerate(zip(hdrsp,col_wp)):
    ax.add_patch(Rectangle((col_xp[j],y0p-0.01),cw,0.3,facecolor=ACCENT,lw=0))
    ax.add_patch(Rectangle((col_xp[j],y0p-0.01),cw,0.3,facecolor="none",edgecolor=RULE,lw=0.6))
    ax.text(col_xp[j]+cw/2,y0p+0.14,h,color=WHITE,fontsize=9,ha="center",va="center",
            family=SERIF,fontweight="bold")
for i,r in enumerate(pu):
    yr=y0p-0.34*(i+1); bg=BGBOX if i%2==0 else WHITE
    row2=[r["variable"],phone_labels.get(r["variable"],""),
          f"{r['F']:.3f}",f"{r['p-value']:.4f}","Yes*" if r["significant"] else "No"]
    for j,(val,cw) in enumerate(zip(row2,col_wp)):
        ax.add_patch(Rectangle((col_xp[j],yr),cw,0.33,facecolor=bg,lw=0))
        ax.add_patch(Rectangle((col_xp[j],yr),cw,0.33,facecolor="none",edgecolor=RULE,lw=0.6))
        vc=GREEN2 if (j==4 and "Yes" in val) else DARK
        ax.text(col_xp[j]+cw/2,yr+0.16,val,color=vc,fontsize=9,ha="center",va="center",
                family=SERIF)

pnum(ax, 10, TOTAL_PAGES); pages.append(fig)

# ════════════════════════════════════════════════════════════════
# PAGE 11 — Q11.5 FIGURES
# ════════════════════════════════════════════════════════════════
fig, ax = new_page()
ax.text(0.5, H-0.6, "Question 11.5   MANOVA — Figures",
        color=ACCENT, fontsize=14, fontweight="bold", family=SERIF)
hline(ax, H-0.75)
body(ax,
     "Figure 11.5: (Top-left) Heatmap of mean CES-D item scores by depression group.  "
     "(Top-right) Univariate F-statistics for all 20 CES-D items.  "
     "(Bottom-left) Attitude item mean profiles by phone-ownership group.  "
     "(Bottom-right) Univariate F-statistics for attitude items A1–A6.",
     0.5, H-1.05, fs=9.5, color=GREY)
embed(fig, "hw_plots/q115_results.png", [0.04, 0.1, 0.93, 0.73])
ax.add_patch(Rectangle((0.4, 0.38), W-0.8, 6.6, facecolor="none", edgecolor=RULE, lw=0.8))
pnum(ax, 11, TOTAL_PAGES); pages.append(fig)

# ════════════════════════════════════════════════════════════════
# PAGE 12 — SUMMARY TABLE
# ════════════════════════════════════════════════════════════════
fig, ax = new_page()
ax.text(0.5, H-0.6, "Summary of All Results",
        color=ACCENT, fontsize=14, fontweight="bold", family=SERIF)
hline(ax, H-0.75)

section(ax, "Consolidated Results Table", 0.5, H-1.28, w=10.0)
summ_hdrs=["Question","Method","Dataset","Key Statistic","Accuracy / Result","Conclusion"]
summ_rows=[
    ("Q10.4 — Mod.1","Logistic Regression (GPA)",
     "ADMIS.DAT","AUC = 0.975",f"{R['q104_acc1']:.1%} accuracy",
     "GPA alone near-perfectly predicts admission"),
    ("Q10.4 — Mod.2","LR (GPA + GMAT)",
     "ADMIS.DAT","AUC = 1.000",f"{R['q104_acc2']:.1%} accuracy",
     "GMAT achieves perfect discrimination"),
    ("Q10.5 — Hand","Simple LR on log-odds",
     "Table Q10.2",f"Slope = {R['q105_b1']:.5f}","—",
     "Higher cholesterol raises heart disease log-odds"),
    ("Q10.5 — Soft.","LR with dummies",
     "Table Q10.2","LLR p = 0.036",f"{R['q105_acc']:.1%} accuracy",
     ">220 mg/100cc groups significantly different"),
    ("Q10.6 — LR","Logistic Regression",
     "DEPRES.DAT",f"AUC = {R['q106_lr_auc']:.3f}",f"{R['q106_lr_acc']:.1%} accuracy",
     "SEX, INCOME, RELIG, BEDDAYS significant"),
    ("Q10.6 — LDA","Linear Discriminant Analysis",
     "DEPRES.DAT",f"AUC = {R['q106_lda_auc']:.3f}",f"{R['q106_lda_acc']:.1%} accuracy",
     "LR marginally outperforms LDA"),
    ("Q11.5A — MANOVA","MANOVA + LDA",
     "DEPRES.DAT",f"Λ = {R['q115_dep_lambda']:.4f}",
     f"F={R['q115_dep_F']:.1f}, p<.0001",
     "All 20 CES-D items separate groups"),
    ("Q11.5B — MANOVA","MANOVA + LDA",
     "PHONE.DAT",f"Λ = {R['q115_ph_lambda']:.4f}",
     f"F={R['q115_ph_F']:.1f}, p<.0001",
     "All 6 attitude items differ by phone group"),
]
col_xs2=[0.5,2.3,4.1,5.7,7.3,8.9]
col_ws2=[1.8,1.8,1.6,1.6,1.6,1.6]
y0s=H-1.84
for j,(h,cw) in enumerate(zip(summ_hdrs,col_ws2)):
    ax.add_patch(Rectangle((col_xs2[j],y0s-0.01),cw,0.34,facecolor=ACCENT,lw=0))
    ax.add_patch(Rectangle((col_xs2[j],y0s-0.01),cw,0.34,facecolor="none",edgecolor=RULE,lw=0.6))
    ax.text(col_xs2[j]+cw/2,y0s+0.16,h,color=WHITE,fontsize=8.5,ha="center",va="center",
            family=SERIF,fontweight="bold")
for i,row in enumerate(summ_rows):
    yr=y0s-0.52*(i+1); bg=BGBOX if i%2==0 else WHITE
    for j,(val,cw) in enumerate(zip(row,col_ws2)):
        ax.add_patch(Rectangle((col_xs2[j],yr),cw,0.51,facecolor=bg,lw=0))
        ax.add_patch(Rectangle((col_xs2[j],yr),cw,0.51,facecolor="none",edgecolor=RULE,lw=0.6))
        ax.text(col_xs2[j]+cw/2,yr+0.25,val,color=DARK,fontsize=7.8,ha="center",va="center",
                family=SERIF,multialignment="center",wrap=True)

hline(ax, 0.8)
body(ax,
     "Note: All analyses were performed using Python 3.11 with statsmodels, scikit-learn, and scipy. "
     "Complete SAS code implementing identical analyses using PROC LOGISTIC, PROC DISCRIM, and "
     "PROC GLM is provided in the accompanying homework_analysis.sas file.",
     0.5, 0.48, fs=8.5, color=GREY)
pnum(ax, 12, TOTAL_PAGES); pages.append(fig)

# ════════════════════════════════════════════════════════════════
# SAVE
# ════════════════════════════════════════════════════════════════
out = "Homework_Solutions.pdf"
with PdfPages(out) as pdf:
    for f in pages:
        pdf.savefig(f, bbox_inches="tight", dpi=150, facecolor=f.get_facecolor())
        plt.close(f)
print(f"Saved: {out}  ({len(pages)} pages)")

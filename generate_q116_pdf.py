"""
Generates an academic-style PDF report for Question 11.6 — MANOVA small sample
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg
import pickle, numpy as np, os

with open("q116_results.pkl","rb") as f:
    R = pickle.load(f)

# ── Academic palette ──────────────────────────────────────────────
BLACK  = "#111111"; DARK   = "#222222"; MID  = "#444444"
GREY   = "#666666"; LGREY  = "#999999"; RULE = "#CCCCCC"
BGLIGHT= "#F5F7FA"; BGBOX  = "#EEF2F6"; WHITE= "#FFFFFF"
ACCENT = "#1A3A6B"; ACCENT2= "#2E6DA4"
RED2   = "#B82020"; GREEN2 = "#1A6B35"; AMBER= "#B87020"

W_pg, H_pg = 11.0, 8.5
SERIF = "DejaVu Serif"
pages = []
TOTAL_PAGES = 5

def new_page():
    fig = plt.figure(figsize=(W_pg, H_pg), facecolor=WHITE)
    ax  = fig.add_axes([0,0,1,1], facecolor=WHITE)
    ax.set_xlim(0,W_pg); ax.set_ylim(0,H_pg); ax.axis("off")
    ax.add_patch(Rectangle((0.5, H_pg-0.35), W_pg-1.0, 0.028, facecolor=ACCENT, lw=0))
    ax.add_patch(Rectangle((0.5, 0.32),      W_pg-1.0, 0.028, facecolor=ACCENT, lw=0))
    return fig, ax

def pnum(ax, n, tot):
    ax.text(W_pg/2, 0.18, f"— {n} —", color=LGREY, fontsize=8.5,
            ha="center", va="center", family=SERIF)
    ax.text(W_pg-0.5, 0.18, f"of {tot}", color=LGREY, fontsize=7.5,
            ha="right",  va="center", family=SERIF)

def section(ax, label, x, y, w=10.0):
    ax.add_patch(Rectangle((x, y-0.02), w, 0.38, facecolor=BGLIGHT, lw=0))
    ax.add_patch(Rectangle((x, y-0.02), 0.06, 0.38, facecolor=ACCENT, lw=0))
    ax.text(x+0.18, y+0.17, label, color=ACCENT, fontsize=12,
            fontweight="bold", va="center", family=SERIF)

def body(ax, text, x, y, fs=9.5, color=DARK, ls=1.6, w=9.5):
    ax.text(x, y, text, color=color, fontsize=fs, va="top",
            family=SERIF, multialignment="left", linespacing=ls)

def hline(ax, y, x0=0.5, x1=10.5):
    ax.add_patch(Rectangle((x0, y), x1-x0, 0.012, facecolor=RULE, lw=0))

def table_hdr(ax, col_x, col_w, hdrs, y0, row_h=0.34):
    for j,(h,cw) in enumerate(zip(hdrs, col_w)):
        ax.add_patch(Rectangle((col_x[j], y0-0.01), cw, row_h, facecolor=ACCENT, lw=0))
        ax.add_patch(Rectangle((col_x[j], y0-0.01), cw, row_h,
                                facecolor="none", edgecolor=RULE, lw=0.6))
        ax.text(col_x[j]+cw/2, y0+row_h/2-0.01, h, color=WHITE,
                fontsize=8.5, ha="center", va="center",
                family=SERIF, fontweight="bold")

def table_row(ax, col_x, col_w, vals, y0, row_h=0.34,
              shade=False, vcols=None):
    bg = BGBOX if shade else WHITE
    for j,(val,cw) in enumerate(zip(vals, col_w)):
        ax.add_patch(Rectangle((col_x[j], y0), cw, row_h, facecolor=bg, lw=0))
        ax.add_patch(Rectangle((col_x[j], y0), cw, row_h,
                                facecolor="none", edgecolor=RULE, lw=0.6))
        vc = vcols[j] if vcols else DARK
        ax.text(col_x[j]+cw/2, y0+row_h/2, val, color=vc,
                fontsize=8.8, ha="center", va="center", family=SERIF)

def embed(fig, path, rect):
    if os.path.exists(path):
        iax = fig.add_axes(rect); iax.set_axis_off()
        iax.imshow(mpimg.imread(path), aspect="auto")

# ════════════════════════════════════════════════════════════════
# PAGE 1 — TITLE
# ════════════════════════════════════════════════════════════════
fig, ax = new_page()
ax.add_patch(Rectangle((0.5, H_pg-2.2), W_pg-1.0, 1.75, facecolor=ACCENT, lw=0))
ax.text(W_pg/2, H_pg-0.75, "MULTIVARIATE STATISTICS",
        color=WHITE, fontsize=11, ha="center", va="center",
        family=SERIF, style="italic")
ax.text(W_pg/2, H_pg-1.2, "Homework Solutions — Question 11.6",
        color=WHITE, fontsize=26, fontweight="bold", ha="center",
        va="center", family=SERIF)
ax.text(W_pg/2, H_pg-1.78,
        "MANOVA with Small Sample: Problem Identification and Rectification",
        color="#B8D0F0", fontsize=12, ha="center", va="center", family=SERIF)

hline(ax, H_pg-2.98)

info = [
    ("Author",     "Lana Jalal Gidan"),
    ("Email",      "lgidan@binghamton.edu"),
    ("Department", "Systems Science and Industrial Engineering"),
    ("University", "Binghamton University"),
    ("Course",     "Multivariate Statistics"),
    ("Date",       "April 2026"),
]
for i,(k,v) in enumerate(info):
    y = H_pg-3.45-i*0.45
    ax.text(2.8, y, f"{k}:", color=LGREY, fontsize=10, ha="right",
            va="center", family=SERIF, style="italic")
    ax.text(3.0, y, v,       color=DARK,  fontsize=10, ha="left",
            va="center", family=SERIF)

hline(ax, H_pg-6.2)

# summary boxes
boxes = [
    ("n = 6","Total observations\n(3 per group)",   ACCENT),
    ("p = 4","Dependent variables\n(Y₁, Y₂, Y₃, Y₄)",AMBER),
    ("g = 2","Groups",                               GREEN2),
    ("Rank W = 3","Within-group matrix\nrank-deficient",RED2),
]
for i,(val,lbl,col) in enumerate(boxes):
    x = 1.0 + i*2.5
    ax.add_patch(Rectangle((x, H_pg-7.5), 2.2, 1.1, facecolor=BGBOX, lw=0))
    ax.add_patch(Rectangle((x, H_pg-6.45),2.2, 0.06,facecolor=col, lw=0))
    ax.text(x+1.1, H_pg-6.95, val, color=col,  fontsize=16, fontweight="bold",
            ha="center", va="center", family=SERIF)
    ax.text(x+1.1, H_pg-7.3,  lbl, color=GREY, fontsize=9,
            ha="center", va="center", family=SERIF, multialignment="center")

pnum(ax, 1, TOTAL_PAGES); pages.append(fig)

# ════════════════════════════════════════════════════════════════
# PAGE 2 — DATA + MATRICES
# ════════════════════════════════════════════════════════════════
fig, ax = new_page()
ax.text(0.5, H_pg-0.6, "Question 11.6   Data, Group Means, and SSCP Matrices",
        color=ACCENT, fontsize=14, fontweight="bold", family=SERIF)
hline(ax, H_pg-0.75)

section(ax, "11.6.1   Raw Data", 0.5, H_pg-1.28)
# Data table
col_x = [0.5,1.9,3.1,4.3,5.5,6.9]; col_w=[1.4,1.2,1.2,1.2,1.4,1.6]
table_hdr(ax, col_x, col_w, ["Obs.","Y₁","Y₂","Y₃","Y₄","Group"], H_pg-1.84)
raw = [(1,7,3,1,2,1),(2,8,2,3,3,1),(3,9,1,5,5,1),
       (4,9,5,3,4,2),(5,10,4,5,5,2),(6,11,8,7,6,2)]
for i,row in enumerate(raw):
    gcol = ACCENT if row[5]==1 else RED2
    table_row(ax, col_x, col_w,
              [str(v) for v in row], H_pg-2.18-i*0.33,
              shade=(i%2==0),
              vcols=[DARK,DARK,DARK,DARK,DARK,gcol])

section(ax, "11.6.2   Group Means and Grand Mean", 0.5, H_pg-4.18)
col_xm=[0.5,2.3,3.9,5.5,7.1]; col_wm=[1.8,1.6,1.6,1.6,1.6]
table_hdr(ax, col_xm, col_wm, ["","Ȳ₁","Ȳ₂","Ȳ₃","Ȳ₄"], H_pg-4.74)
m1 = R["means"][1]; m2 = R["means"][2]; gm = R["grand_mean"]
for i,(lbl,m) in enumerate([("Group 1", m1),("Group 2", m2),("Grand Mean", gm)]):
    table_row(ax, col_xm, col_wm,
              [lbl] + [f"{v:.4f}" for v in m],
              H_pg-5.08-i*0.34, shade=(i%2==0))

section(ax, "11.6.3   Within-Group Matrix W and Between-Group Matrix B", 0.5, H_pg-6.08)

W = np.array(R["W"]); B = np.array(R["B"])
ax.text(0.5, H_pg-6.65, "Within-Group Matrix W:", color=ACCENT2,
        fontsize=10, fontweight="bold", family=SERIF)
ax.text(5.8, H_pg-6.65, "Between-Group Matrix B:", color=ACCENT2,
        fontsize=10, fontweight="bold", family=SERIF)
col_xw=[0.5,1.8,2.9,4.0,5.1]; col_ww=[1.3,1.1,1.1,1.1,0.5]
col_xb=[5.8,7.1,8.2,9.3,10.4]; col_wb=[1.3,1.1,1.1,1.1,0.2]
row_labels=["Y₁","Y₂","Y₃","Y₄"]
for j,lbl in enumerate(["","Y₁","Y₂","Y₃","Y₄"]):
    ax.add_patch(Rectangle((col_xw[j],H_pg-7.02),col_ww[j],0.3,facecolor=ACCENT,lw=0))
    ax.add_patch(Rectangle((col_xw[j],H_pg-7.02),col_ww[j],0.3,facecolor="none",edgecolor=RULE,lw=0.6))
    ax.text(col_xw[j]+col_ww[j]/2,H_pg-6.87,lbl,color=WHITE,fontsize=8.5,ha="center",
            va="center",family=SERIF,fontweight="bold")
    ax.add_patch(Rectangle((col_xb[j],H_pg-7.02),col_wb[j],0.3,facecolor=ACCENT,lw=0))
    ax.add_patch(Rectangle((col_xb[j],H_pg-7.02),col_wb[j],0.3,facecolor="none",edgecolor=RULE,lw=0.6))
    if j < len(row_labels):
        ax.text(col_xb[j]+col_wb[j]/2,H_pg-6.87,["","Y₁","Y₂","Y₃","Y₄"][j],
                color=WHITE,fontsize=8.5,ha="center",va="center",family=SERIF,fontweight="bold")
for i in range(4):
    yr = H_pg-7.32-i*0.3
    bg = BGBOX if i%2==0 else WHITE
    # W
    ax.add_patch(Rectangle((col_xw[0],yr),col_ww[0],0.29,facecolor=ACCENT2,lw=0))
    ax.add_patch(Rectangle((col_xw[0],yr),col_ww[0],0.29,facecolor="none",edgecolor=RULE,lw=0.6))
    ax.text(col_xw[0]+col_ww[0]/2,yr+0.14,row_labels[i],color=WHITE,fontsize=8.5,
            ha="center",va="center",family=SERIF,fontweight="bold")
    for j in range(4):
        ax.add_patch(Rectangle((col_xw[j+1],yr),col_ww[j+1],0.29,facecolor=bg,lw=0))
        ax.add_patch(Rectangle((col_xw[j+1],yr),col_ww[j+1],0.29,facecolor="none",edgecolor=RULE,lw=0.6))
        ax.text(col_xw[j+1]+col_ww[j+1]/2,yr+0.14,f"{W[i,j]:.2f}",color=DARK,
                fontsize=8.5,ha="center",va="center",family=SERIF)
    # B
    ax.add_patch(Rectangle((col_xb[0],yr),col_wb[0],0.29,facecolor=ACCENT2,lw=0))
    ax.add_patch(Rectangle((col_xb[0],yr),col_wb[0],0.29,facecolor="none",edgecolor=RULE,lw=0.6))
    ax.text(col_xb[0]+col_wb[0]/2,yr+0.14,row_labels[i],color=WHITE,fontsize=8.5,
            ha="center",va="center",family=SERIF,fontweight="bold")
    for j in range(3):
        ax.add_patch(Rectangle((col_xb[j+1],yr),col_wb[j+1],0.29,facecolor=bg,lw=0))
        ax.add_patch(Rectangle((col_xb[j+1],yr),col_wb[j+1],0.29,facecolor="none",edgecolor=RULE,lw=0.6))
        ax.text(col_xb[j+1]+col_wb[j+1]/2,yr+0.14,f"{B[i,j]:.2f}",color=DARK,
                fontsize=8.5,ha="center",va="center",family=SERIF)

pnum(ax, 2, TOTAL_PAGES); pages.append(fig)

# ════════════════════════════════════════════════════════════════
# PAGE 3 — PROBLEM IDENTIFICATION
# ════════════════════════════════════════════════════════════════
fig, ax = new_page()
ax.text(0.5, H_pg-0.6, "Question 11.6   MANOVA Results and Problem Identification",
        color=ACCENT, fontsize=14, fontweight="bold", family=SERIF)
hline(ax, H_pg-0.75)

section(ax, "11.6.4   MANOVA Test Results (Full Model, p = 4)", 0.5, H_pg-1.28)

wl = R["wilks_lambda"]; rk = R["rank_W"]
det_W = R["det_W"]; det_T = R["det_T"]
col_xr=[0.5,4.5,7.0,9.2]; col_wr=[4.0,2.5,2.2,1.4]
table_hdr(ax, col_xr, col_wr, ["Quantity","Value","Formula","df"],H_pg-1.84)
manova_rows=[
    ("Rank of W (within-group matrix)",f"{rk}  ← singular!","rank(W)",f"should = {R['p']}"),
    ("det(W)",f"{det_W:.6f}","det(E)","—"),
    ("det(T)",f"{det_T:.6f}","det(E+H)","—"),
    ("Wilks' Lambda  Λ","0.000000  ← degenerate","det(W)/det(T)","—"),
    ("df₂ = n − g − p + 1",f"{R['df2']}  (should be > 0)","exact formula","—"),
    ("F-approximation","INVALID — df₂ = 1","F(p, df₂)","p=4, df₂=1"),
]
for i,row in enumerate(manova_rows):
    vc2 = RED2 if ("singular" in row[1] or "degenerate" in row[1] or "INVALID" in row[1]) else DARK
    table_row(ax, col_xr, col_wr, row,
              H_pg-2.18-i*0.34, shade=(i%2==0),
              vcols=[DARK, vc2, GREY, GREY])

section(ax, "11.6.5   Identification of the Problem", 0.5, H_pg-4.3)
ax.add_patch(Rectangle((0.5, H_pg-4.88), 10.0, 1.6, facecolor="#FEF3E2", lw=0))
ax.add_patch(Rectangle((0.5, H_pg-4.88), 0.06, 1.6, facecolor=AMBER,    lw=0))
body(ax,
     "The fundamental problem is that the sample size is too small relative to the number of "
     "dependent variables.\n\n"
     "MANOVA requires: n − g  >  p  (within-group degrees of freedom must exceed the number of DVs)\n\n"
     "Here:  n − g  =  6 − 2  =  4,   p  =  4   ⟹   4 > 4  is FALSE\n\n"
     "Consequences:\n"
     "  (1)  The within-group matrix W is rank-deficient (rank 3 instead of 4); its determinant = 0.\n"
     "  (2)  Wilks' Lambda = det(W)/det(T) = 0 — a degenerate result, not a true test statistic.\n"
     "  (3)  The denominator degrees of freedom df₂ = n − g − p + 1 = 1 makes the F-test "
     "essentially powerless.\n"
     "  (4)  Statistical conclusions drawn from this analysis are unreliable and "
     "not generalizable.",
     0.55, H_pg-5.0, fs=9.5, color=DARK)

section(ax, "11.6.6   Eigenvalues of W (Confirming Singularity)", 0.5, H_pg-6.62)
col_xe=[0.5,2.8,5.0,7.2]; col_we=[2.3,2.2,2.2,3.3]
table_hdr(ax, col_xe, col_we, ["Eigenvalue","Value","Non-zero?","Interpretation"], H_pg-7.18)
eigs = R["eig_W"]
interps=["Non-zero — valid variance dimension",
         "Non-zero — valid variance dimension",
         "Near-zero — minimal variance",
         "Exactly zero — SINGULAR (confirms rank deficiency)"]
for i,(e,interp) in enumerate(zip(eigs,interps)):
    vc = RED2 if e < 0.001 else DARK
    yn = "No  " if e < 0.001 else "Yes "
    yc = RED2 if e < 0.001 else GREEN2
    table_row(ax, col_xe, col_we,
              [f"λ{i+1}", f"{e:.6f}", yn, interp],
              H_pg-7.52-i*0.34, shade=(i%2==0),
              vcols=[DARK, vc, yc, GREY])

pnum(ax, 3, TOTAL_PAGES); pages.append(fig)

# ════════════════════════════════════════════════════════════════
# PAGE 4 — REMEDIES + UNIVARIATE + REDUCED MANOVA
# ════════════════════════════════════════════════════════════════
fig, ax = new_page()
ax.text(0.5, H_pg-0.6, "Question 11.6   How to Rectify the Problem",
        color=ACCENT, fontsize=14, fontweight="bold", family=SERIF)
hline(ax, H_pg-0.75)

section(ax, "11.6.7   Recommended Remedies", 0.5, H_pg-1.28)
remedies = [
    ("A", "Increase Sample Size",
     "Collect more observations so that n − g > p.  The minimum requirement is n > g + p = 6,\n"
     "but a practical rule of thumb is at least 10 × p observations per group (i.e., 40+ per group,\n"
     "80+ total). This is the most statistically principled remedy."),
    ("B", "Reduce Number of DVs",
     "Use a subset of p′ < p dependent variables such that n − g > p′.  For example, using\n"
     "only Y₁ and Y₂ gives p′ = 2, and n − g = 4 > 2 (ok).  Variable selection should be guided\n"
     "by theory, not by which variables give significant results (to avoid data dredging)."),
    ("C", "Dimension Reduction via PCA",
     "Apply Principal Component Analysis to Y₁–Y₄ first, retaining fewer components\n"
     "(e.g., 2 components) that explain most of the variance.  Then run MANOVA on the\n"
     "component scores.  This preserves information while satisfying n − g > p."),
    ("D", "Univariate ANOVAs",
     "Run separate one-way ANOVAs for each dependent variable.  While this approach ignores\n"
     "the multivariate structure and inflates Type I error, it remains valid for each DV\n"
     "individually when MANOVA is infeasible.  Apply Bonferroni correction for multiple tests."),
]
y_box = H_pg-1.82
for opt,title,desc in remedies:
    ax.add_patch(Rectangle((0.5, y_box), 10.0, 1.1, facecolor=BGBOX, lw=0))
    ax.add_patch(Rectangle((0.5, y_box), 0.45, 1.1, facecolor=ACCENT, lw=0))
    ax.text(0.72, y_box+0.72, opt, color=WHITE, fontsize=13, fontweight="bold",
            ha="center", va="center", family=SERIF)
    ax.text(1.1, y_box+0.88, f"Option {opt}: {title}",
            color=ACCENT, fontsize=10.5, fontweight="bold", family=SERIF)
    ax.text(1.1, y_box+0.55, desc, color=DARK, fontsize=8.8, va="top",
            family=SERIF, linespacing=1.5)
    y_box -= 1.15

section(ax, "11.6.8   Remedy B Applied: MANOVA with p=2 (Y₁, Y₂ only)", 0.5, H_pg-6.7)
col_xb2=[0.5,3.5,5.4,7.2,9.0]; col_wb2=[3.0,1.9,1.8,1.8,1.5]
table_hdr(ax, col_xb2, col_wb2,
          ["Quantity","Value","df₁","df₂","p-value"], H_pg-7.26)
sig_str = "p = 0.1277 (Not sig. at α=0.05)"
table_row(ax, col_xb2, col_wb2,
          ["Wilks' Lambda (Y₁,Y₂)", f"{R['wl2']:.6f}", "2",
           "3", f"{R['pv2']:.4f}"],
          H_pg-7.6, shade=True,
          vcols=[DARK,DARK,DARK,DARK,
                 RED2 if R["pv2"]<0.05 else GREY])
body(ax,
     f"F(2, 3) = {R['F2']:.4f},  p = {R['pv2']:.4f}.  With only p=2 DVs the test is now "
     "technically valid (df₂ = 3 > 0), but the result is not significant — reflecting the\n"
     "very small sample size and low power.",
     0.5, H_pg-8.0, fs=9.5, color=GREY)

pnum(ax, 4, TOTAL_PAGES); pages.append(fig)

# ════════════════════════════════════════════════════════════════
# PAGE 5 — FIGURES + UNIVARIATE TABLE + SUMMARY
# ════════════════════════════════════════════════════════════════
fig, ax = new_page()
ax.text(0.5, H_pg-0.6, "Question 11.6   Figures and Univariate ANOVA Summary",
        color=ACCENT, fontsize=14, fontweight="bold", family=SERIF)
hline(ax, H_pg-0.75)

body(ax,
     "Figure 11.6: (Top-left) Scatter of Y₁ vs Y₂ by group.  "
     "(Top-right) Group means by variable.  "
     "(Bottom-left) Univariate F-statistics per variable.  "
     "(Bottom-right) Heatmap of within-group matrix W with rank annotation.",
     0.5, H_pg-1.02, fs=9.5, color=GREY)
embed(fig, "q116_plots/q116_results.png", [0.04, 0.36, 0.93, 0.53])
ax.add_patch(Rectangle((0.4, 0.38+2.62), W_pg-0.8, 4.5,
                        facecolor="none", edgecolor=RULE, lw=0.8))

section(ax, "11.6.9   Univariate ANOVA (Remedy D)", 0.5, H_pg-1.22)
col_xu=[0.5,2.0,3.8,5.6,7.4,9.2]; col_wu=[1.5,1.8,1.8,1.8,1.8,1.4]
table_hdr(ax, col_xu, col_wu,
          ["Variable","F(1,4)","p-value","Bonf. threshold","Significant?","Direction"],
          H_pg-1.78)
univ = R["univ_results"]
dirs=["G2 > G1","G2 > G1","G2 > G1","G2 > G1"]
for i,(r,d) in enumerate(zip(univ,dirs)):
    sig_b = r["p"] < (0.05/4)
    table_row(ax, col_xu, col_wu,
              [r["var"], f"{r['F']:.4f}", f"{r['p']:.4f}",
               "0.0125", "Yes*" if sig_b else "No", d],
              H_pg-2.12-i*0.34, shade=(i%2==0),
              vcols=[DARK,DARK,DARK,GREY,
                     RED2 if sig_b else DARK, GREY])

section(ax, "11.6.10   Conclusion and Summary", 0.5, H_pg-3.52)
ax.add_patch(Rectangle((0.5, H_pg-4.1), 10.0, 0.5, facecolor=BGLIGHT, lw=0))
ax.add_patch(Rectangle((0.5, H_pg-4.1), 0.06, 0.5, facecolor=ACCENT,  lw=0))
body(ax,
     "The MANOVA cannot be validly executed in its standard form because the within-group matrix W is "
     "rank-deficient\n(rank 3 instead of 4), yielding Wilks' Lambda = 0 and a degenerate F-test with "
     "df₂ = 1.  The root cause is an\ninadequate sample size: n − g = 4 does not exceed p = 4.  "
     "Univariate ANOVAs show marginal trends for Y₁ (p=0.071) and\nY₂ (p=0.051), consistent with "
     "group separation, but none survive Bonferroni correction (α = 0.0125).  The primary\n"
     "remedy is to collect a substantially larger sample (≥ 40 per group); alternatively, "
     "reduce p to 2 or apply PCA\nbefore running MANOVA.",
     0.55, H_pg-4.18, fs=9.5, color=DARK)

pnum(ax, 5, TOTAL_PAGES); pages.append(fig)

# ════════════════════════════════════════════════════════════════
# SAVE
# ════════════════════════════════════════════════════════════════
out = "Q116_Solutions.pdf"
with PdfPages(out) as pdf:
    for f in pages:
        pdf.savefig(f, bbox_inches="tight", dpi=150, facecolor=f.get_facecolor())
        plt.close(f)
print(f"Saved: {out}  ({len(pages)} pages)")

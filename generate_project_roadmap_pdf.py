import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_pdf import PdfPages

WHITE  = "#FFFFFF"; BLACK  = "#111111"; DARK   = "#222222"
GREY   = "#666666"; LGREY  = "#999999"; RULE   = "#CCCCCC"
BGLIGHT= "#F5F7FA"; BGBOX  = "#EEF2F6"
ACCENT = "#1A3A6B"; ACCENT2= "#2E6DA4"
RED2   = "#B82020"; GREEN2 = "#1A6B35"; AMBER  = "#B87020"
SERIF  = "DejaVu Serif"
W, H   = 11.0, 8.5
pages  = []

def new_page():
    fig = plt.figure(figsize=(W, H), facecolor=WHITE)
    ax  = fig.add_axes([0,0,1,1], facecolor=WHITE)
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    ax.add_patch(Rectangle((0.5, H-0.35), W-1.0, 0.028, facecolor=ACCENT, lw=0))
    ax.add_patch(Rectangle((0.5, 0.32),   W-1.0, 0.028, facecolor=ACCENT, lw=0))
    return fig, ax

def hline(ax, y, x0=0.5, x1=10.5):
    ax.add_patch(Rectangle((x0, y), x1-x0, 0.012, facecolor=RULE, lw=0))

def section(ax, label, x, y, w=10.0, color=ACCENT):
    ax.add_patch(Rectangle((x, y-0.02), w, 0.38, facecolor=BGLIGHT, lw=0))
    ax.add_patch(Rectangle((x, y-0.02), 0.06, 0.38, facecolor=color, lw=0))
    ax.text(x+0.18, y+0.17, label, color=color, fontsize=11.5,
            fontweight="bold", va="center", family=SERIF)

def body(ax, text, x, y, fs=9.5, color=DARK, ls=1.65):
    ax.text(x, y, text, color=color, fontsize=fs, va="top",
            family=SERIF, multialignment="left", linespacing=ls)

def pnum(ax, n, tot):
    ax.text(W/2, 0.18, f"— {n} —", color=LGREY, fontsize=8.5,
            ha="center", va="center", family=SERIF)

def table_hdr(ax, col_x, col_w, hdrs, y0, rh=0.34):
    for j,(h,cw) in enumerate(zip(hdrs,col_w)):
        ax.add_patch(Rectangle((col_x[j],y0-0.01),cw,rh,facecolor=ACCENT,lw=0))
        ax.add_patch(Rectangle((col_x[j],y0-0.01),cw,rh,facecolor="none",edgecolor=RULE,lw=0.6))
        ax.text(col_x[j]+cw/2,y0+rh/2-0.01,h,color=WHITE,fontsize=9,
                ha="center",va="center",family=SERIF,fontweight="bold")

def table_row(ax, col_x, col_w, vals, y0, rh=0.34, shade=False, vcols=None):
    bg = BGBOX if shade else WHITE
    for j,(val,cw) in enumerate(zip(vals,col_w)):
        ax.add_patch(Rectangle((col_x[j],y0),cw,rh,facecolor=bg,lw=0))
        ax.add_patch(Rectangle((col_x[j],y0),cw,rh,facecolor="none",edgecolor=RULE,lw=0.6))
        vc = vcols[j] if vcols else DARK
        ax.text(col_x[j]+cw/2,y0+rh/2,val,color=vc,fontsize=8.8,
                ha="center",va="center",family=SERIF)

TOTAL = 3

# ══════════════════════════════════════════════════════════════════
# PAGE 1 — COVER + BASELINE vs NOVEL
# ══════════════════════════════════════════════════════════════════
fig, ax = new_page()

# Header banner
ax.add_patch(Rectangle((0.5, H-2.1), W-1.0, 1.65, facecolor=ACCENT, lw=0))
ax.text(W/2, H-0.72, "MULTIVARIATE STATISTICS — TERM PROJECT",
        color="#B8D0F0", fontsize=10, ha="center", family=SERIF, style="italic")
ax.text(W/2, H-1.18, "Publication Roadmap",
        color=WHITE, fontsize=28, fontweight="bold", ha="center", family=SERIF)
ax.text(W/2, H-1.72,
        "S&P 500 Stock Outperformer Classification Using Financial Ratios",
        color="#B8D0F0", fontsize=12, ha="center", family=SERIF)

info = [("Authors","Lana Gidan  ·  Matthew Golubow  ·  Shahd Tarman  (Group 15)"),
        ("Affiliation","Systems Science & Industrial Engineering, Binghamton University"),
        ("Inspiration","Ananthakumar & Sarkar (2017), IEEE DASC/PiCom/DataCom")]
for i,(k,v) in enumerate(info):
    y = H-2.65-i*0.40
    ax.text(2.5,y,f"{k}:",color=LGREY,fontsize=9.5,ha="right",va="center",
            family=SERIF,style="italic")
    ax.text(2.65,y,v,color=DARK,fontsize=9.5,ha="left",va="center",family=SERIF)

hline(ax, H-3.58)

section(ax, "What the 2017 Paper Did — and Why Replication Alone Is Not Enough",
        0.5, H-4.05, color=RED2)
body(ax,
     "Ananthakumar & Sarkar (2017) applied basic logistic regression to annual S&P 500 data "
     "and demonstrated that financial ratios\ncould distinguish outperformers from "
     "underperformers. This was a meaningful contribution in 2017. However, simply "
     "replicating the\nsame method on updated data in 2025 does not constitute a novel "
     "academic contribution and would not pass peer review.\nA publishable paper must "
     "answer a question that has not been answered before, or answer an old question "
     "with meaningfully better data, methods, or scope.",
     0.5, H-4.62, fs=9.5)

hline(ax, H-5.55)
section(ax, "Core Research Question (Your Novel Angle)", 0.5, H-6.02)
ax.add_patch(Rectangle((0.5, H-6.65), W-1.0, 0.54, facecolor=BGBOX, lw=0))
ax.add_patch(Rectangle((0.5, H-6.65), 0.06, 0.54, facecolor=ACCENT2, lw=0))
body(ax,
     "Can quarterly financial ratios — combined with rigorous class-imbalance correction, "
     "multicollinearity screening (VIF), and comparison\nacross multiple classification "
     "models — reliably predict S&P 500 stock outperformance across different market "
     "regimes\n(pre-COVID, COVID crisis, post-COVID recovery)?",
     0.6, H-6.22, fs=10, color=ACCENT)

hline(ax, H-7.1)
body(ax,
     "This question is novel because: (1) the 2017 paper used annual data — quarterly "
     "data has not been studied for this problem; (2) no prior study\nhas tested "
     "this framework across the COVID regime break; (3) multi-model comparison "
     "with proper class-imbalance handling has not been applied\nto this specific "
     "outperformer classification task.",
     0.5, H-7.30, fs=9, color=GREY)

pnum(ax, 1, TOTAL); pages.append(fig)

# ══════════════════════════════════════════════════════════════════
# PAGE 2 — FOUR NOVEL ANGLES + DATA REQUIREMENTS
# ══════════════════════════════════════════════════════════════════
fig, ax = new_page()
ax.text(0.5, H-0.6, "Publication Roadmap — Novel Contributions and Data Requirements",
        color=ACCENT, fontsize=13, fontweight="bold", family=SERIF)
hline(ax, H-0.75)

section(ax, "Four Publishable Research Angles (Choose One or Combine)", 0.5, H-1.28)

angles = [
    (ACCENT,  "1",
     "Temporal / Regime Analysis",
     "Train on pre-COVID (2015–2019), test on COVID crash (2020), retest on recovery "
     "(2021–2023).\nAsk: does the model's predictive power break down during market "
     "crises? This is practically\nimportant and not covered in the literature."),
    (GREEN2,  "2",
     "Quarterly vs Annual Data Comparison",
     "The 2017 paper used annual ratios. Compare model accuracy when trained on quarterly\n"
     "vs annual data. Ask: does higher frequency financial data improve outperformer\n"
     "prediction? No study has made this comparison for S&P 500 classification."),
    (AMBER,   "3",
     "Sector-Specific Models",
     "Build one logistic regression model per GICS sector (Technology, Healthcare,\n"
     "Financials, etc.). Ask: do different financial ratios matter in different industries?\n"
     "A P/E ratio means something very different for a tech firm vs a utility company."),
    (RED2,    "4",
     "Multi-Model Comparison with Portfolio Backtesting  ← Most Publishable",
     "Compare LR, LDA, Random Forest, and XGBoost on the same dataset. Apply SMOTE\n"
     "for class imbalance. Report AUC, F1, and simulate an actual portfolio of the\n"
     "top predicted outperformers each quarter and measure returns vs SPY benchmark."),
]
y_box = H-1.85
for col,num,title,desc in angles:
    ax.add_patch(Rectangle((0.5,y_box),W-1.0,1.08,facecolor=BGBOX,lw=0))
    ax.add_patch(Rectangle((0.5,y_box),0.45,1.08,facecolor=col,lw=0))
    ax.text(0.72,y_box+0.65,num,color=WHITE,fontsize=14,fontweight="bold",
            ha="center",va="center",family=SERIF)
    ax.text(1.1,y_box+0.86,title,color=col,fontsize=10.5,
            fontweight="bold",family=SERIF)
    ax.text(1.1,y_box+0.55,desc,color=DARK,fontsize=8.8,
            va="top",family=SERIF,linespacing=1.5)
    y_box -= 1.13

section(ax, "Data Requirements — Honest Assessment", 0.5, H-6.73, color=AMBER)
cx=[0.5,3.2,5.7,8.1]; cw=[2.7,2.5,2.4,2.4]
table_hdr(ax,cx,cw,["Current Data Source","Problem","Fix Required","Priority"],H-7.29)
rows=[
    ("Yahoo Finance (annual,\n110 stocks)",
     "Incomplete ratios,\nsmall sample, no quarterly",
     "Supplement with\nSEC EDGAR quarterly",
     "Done"),
    ("SEC EDGAR quarterly\n(108 stocks, 3,069 rows)",
     "Missing quarterly\nstock price/return data",
     "Add quarterly returns\nvia yfinance",
     "Next step"),
    ("No WRDS / Compustat",
     "Reviewers expect\ngold-standard data",
     "Register at WRDS via\nBinghamton University",
     "Important"),
]
for i,row in enumerate(rows):
    vc3 = GREEN2 if row[3]=="Done" else (RED2 if row[3]=="Important" else AMBER)
    table_row(ax,cx,cw,row,H-7.63-i*0.52,rh=0.51,shade=(i%2==0),
              vcols=[DARK,DARK,DARK,vc3])

pnum(ax, 2, TOTAL); pages.append(fig)

# ══════════════════════════════════════════════════════════════════
# PAGE 3 — WHAT I CAN BUILD + NEXT STEPS
# ══════════════════════════════════════════════════════════════════
fig, ax = new_page()
ax.text(0.5, H-0.6, "Publication Roadmap — Deliverables and Next Steps",
        color=ACCENT, fontsize=13, fontweight="bold", family=SERIF)
hline(ax, H-0.75)

section(ax, "What Can Be Built for This Project", 0.5, H-1.28)

deliverables = [
    (GREEN2, "Full Data Pipeline",
     "Merge quarterly SEC EDGAR financials + quarterly stock returns (yfinance) "
     "into one clean, analysis-ready dataset. Add WRDS/Compustat once access is granted."),
    (GREEN2, "Multicollinearity Screening (VIF)",
     "Calculate Variance Inflation Factors for all financial ratios. Remove or combine "
     "variables with VIF > 10 before modeling to ensure stable logistic regression coefficients."),
    (GREEN2, "Class Imbalance Correction (SMOTE)",
     "Apply Synthetic Minority Oversampling Technique so the model learns equally from "
     "outperformers and underperformers — prevents the model from always predicting the majority class."),
    (GREEN2, "Four Competing Models",
     "Train Logistic Regression, Linear Discriminant Analysis, Random Forest, and XGBoost "
     "on identical data. Report Accuracy, AUC-ROC, Precision, Recall, and F1 for each."),
    (GREEN2, "Portfolio Backtesting",
     "Simulate buying the top-N predicted outperformers at the start of each quarter. "
     "Track portfolio return vs SPY benchmark. Compute Sharpe ratio and max drawdown."),
    (GREEN2, "Publication-Quality Report",
     "Academic PDF covering: Abstract, Literature Review, Methodology, Results, Discussion, "
     "Conclusion — in the format expected by IEEE or a finance journal."),
]
y_d = H-1.85
for col,title,desc in deliverables:
    ax.add_patch(Rectangle((0.5,y_d),W-1.0,0.68,facecolor=BGBOX,lw=0))
    ax.add_patch(Rectangle((0.5,y_d),0.06,0.68,facecolor=col,lw=0))
    ax.text(0.8,y_d+0.52,title,color=col,fontsize=10,fontweight="bold",family=SERIF)
    ax.text(0.8,y_d+0.16,desc,color=DARK,fontsize=8.8,family=SERIF,linespacing=1.4)
    y_d -= 0.73

section(ax, "Recommended Next Steps — In Order", 0.5, H-6.7, color=AMBER)
steps = [
    ("1","Register for WRDS","Go to wrds-web.wharton.upenn.edu with your @binghamton.edu email. "
     "Request access to Compustat. Approval takes 1–3 days.","WRDS"),
    ("2","Decide on research angle","Choose which of the four novel angles to pursue "
     "(Regime analysis recommended as most impactful).","Decision"),
    ("3","Merge quarterly returns","Add quarterly stock return data to the existing SEC EDGAR "
     "dataset to create the outperformer label per quarter.","Data"),
    ("4","Begin full analysis","VIF screening → SMOTE → model training → backtesting → paper.","Analysis"),
]
cx2=[0.5,0.95,2.1,8.55]; cw2=[0.45,1.15,6.45,1.5]
y_s = H-7.25
for num,title,desc,tag in steps:
    ax.add_patch(Rectangle((0.5,y_s),W-1.0,0.62,facecolor=BGLIGHT,lw=0))
    ax.add_patch(Rectangle((0.5,y_s),0.42,0.62,facecolor=ACCENT,lw=0))
    ax.text(0.71,y_s+0.31,num,color=WHITE,fontsize=12,fontweight="bold",
            ha="center",va="center",family=SERIF)
    ax.text(1.0,y_s+0.47,title,color=ACCENT,fontsize=10,fontweight="bold",family=SERIF)
    ax.text(1.0,y_s+0.14,desc,color=DARK,fontsize=8.8,family=SERIF)
    tc = GREEN2 if tag=="Data" else (AMBER if tag=="Decision" else ACCENT2)
    ax.add_patch(Rectangle((9.1,y_s+0.16),1.3,0.32,facecolor=tc,lw=0))
    ax.text(9.75,y_s+0.32,tag,color=WHITE,fontsize=8.5,ha="center",
            va="center",family=SERIF,fontweight="bold")
    y_s -= 0.67

pnum(ax, 3, TOTAL); pages.append(fig)

# ── SAVE ─────────────────────────────────────────────────────────
out = "Project_Publication_Roadmap.pdf"
with PdfPages(out) as pdf:
    for f in pages:
        pdf.savefig(f, bbox_inches="tight", dpi=150, facecolor=f.get_facecolor())
        plt.close(f)
print(f"Saved: {out}  ({len(pages)} pages)")

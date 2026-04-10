"""
Generates a comprehensive PDF report for the homework questions 10.4, 10.5, 10.6, 11.5
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg
import pickle, numpy as np, os

with open("hw_results.pkl","rb") as f:
    R = pickle.load(f)

NAVY  = "#0D1B2E"; NAVY2 = "#1A2F4A"; NAVY3 = "#10263E"
BLUE  = "#2563EB"; LBLUE = "#60A5FA"; GOLD  = "#F59E0B"
GREEN = "#10B981"; RED   = "#EF4444"; WHITE = "#FFFFFF"
LGREY = "#94A3B8"; DGREY = "#334155"

W, H = 13.33, 7.5
pages = []

def new_slide(tag=None, title=None, bar=BLUE):
    fig = plt.figure(figsize=(W,H), facecolor=NAVY)
    ax  = fig.add_axes([0,0,1,1], facecolor=NAVY)
    ax.set_xlim(0,W); ax.set_ylim(0,H); ax.axis("off")
    ax.add_patch(mpatches.Rectangle((0,0),W,0.07,facecolor=bar,lw=0))
    if tag:
        ax.text(0.4,H-0.4,tag.upper(),color=LBLUE,fontsize=8.5,
                fontweight="bold",family="DejaVu Sans")
    if title:
        ax.text(0.4,H-0.85,title,color=WHITE,fontsize=21,
                fontweight="bold",family="DejaVu Sans")
    return fig, ax

def card(ax,x,y,w,h,title,body,tc=LBLUE,bg=NAVY2,fs=10):
    ax.add_patch(FancyBboxPatch((x,y),w,h,
        boxstyle="round,pad=0.05",facecolor=bg,lw=0))
    ax.text(x+0.2,y+h-0.22,title,color=tc,fontsize=11.5,
            fontweight="bold",va="top",family="DejaVu Sans")
    ax.text(x+0.2,y+h-0.52,body,color=LGREY,fontsize=fs,
            va="top",wrap=True,family="DejaVu Sans",multialignment="left",
            linespacing=1.55)

def bullets(ax,items,x,y,sp=0.38,fs=10.5,dc=BLUE):
    for i,item in enumerate(items):
        yi=y-i*sp
        ax.text(x,yi,"▸",color=dc,fontsize=fs,va="center")
        ax.text(x+0.28,yi,item,color=LGREY,fontsize=fs,va="center",
                wrap=True,family="DejaVu Sans")

def embed(fig,path,rect):
    if os.path.exists(path):
        iax=fig.add_axes(rect); iax.set_axis_off()
        iax.imshow(mpimg.imread(path),aspect="auto")

def stat(ax,x,y,w,h,val,lbl,vc=BLUE):
    ax.add_patch(FancyBboxPatch((x,y),w,h,
        boxstyle="round,pad=0.04",facecolor=NAVY2,lw=0))
    ax.text(x+w/2,y+h*0.63,val,color=vc,fontsize=22,fontweight="bold",
            ha="center",va="center",family="DejaVu Sans")
    ax.text(x+w/2,y+h*0.22,lbl,color=LGREY,fontsize=8.5,ha="center",
            va="center",family="DejaVu Sans",multialignment="center")

def pnum(ax,n,tot=10):
    ax.text(W-0.15,0.22,f"{n}/{tot}",color=DGREY,fontsize=8,
            ha="right",va="center",family="DejaVu Sans")

# ════════════════════════════════════════════════════════════════
# PAGE 1 — COVER
# ════════════════════════════════════════════════════════════════
fig,ax = new_slide(bar=BLUE)
ax.add_patch(mpatches.Rectangle((0,0),W,0.12,facecolor=BLUE,lw=0))
ax.text(W/2,H-0.5,"MULTIVARIATE STATISTICS — HOMEWORK SOLUTIONS",
        color=LBLUE,fontsize=9.5,fontweight="bold",ha="center")
ax.text(W/2,H-1.3,"Questions 10.4 · 10.5 · 10.6 · 11.5",
        color=WHITE,fontsize=30,fontweight="bold",ha="center")
ax.text(W/2,H-2.1,"Logistic Regression and MANOVA Analysis",
        color=LGREY,fontsize=14,ha="center")

items_cov = [
    ("Q10.4","Admissions Data","LR with GPA category (dummy-coded) + GMAT","#2563EB"),
    ("Q10.5","Cholesterol Data","Hand calculations + LR with dummy cholesterol levels","#10B981"),
    ("Q10.6","Depression Data","LR vs Discriminant Analysis (CASES as outcome)","#F59E0B"),
    ("Q11.5","MANOVA","Depression (C1-C20) + Phone (A1-A6) with LDA comparison","#EF4444"),
]
for i,(q,ds,desc,col) in enumerate(items_cov):
    x=0.4+i*3.2; y=3.0
    ax.add_patch(FancyBboxPatch((x,y),2.9,2.3,
        boxstyle="round,pad=0.05",facecolor=NAVY2,lw=0))
    ax.add_patch(mpatches.Rectangle((x,y+2.2),2.9,0.1,facecolor=col,lw=0))
    ax.text(x+1.45,y+1.95,q,color=col,fontsize=16,fontweight="bold",ha="center")
    ax.text(x+1.45,y+1.6,ds,color=WHITE,fontsize=10.5,fontweight="bold",ha="center")
    ax.text(x+1.45,y+0.5,desc,color=LGREY,fontsize=9,ha="center",
            multialignment="center",linespacing=1.4)

ax.add_patch(mpatches.Rectangle((0,1.4),W,0.65,facecolor=NAVY2,lw=0))
ax.text(0.4,1.72,"Tools: Python (statsmodels · sklearn · scipy · matplotlib · seaborn)"
        "   |   SAS (PROC LOGISTIC · PROC DISCRIM · PROC GLM)",
        color=LGREY,fontsize=9.5,va="center")
pnum(ax,1); pages.append(fig)

# ════════════════════════════════════════════════════════════════
# PAGE 2 — Q10.4 SETUP
# ════════════════════════════════════════════════════════════════
fig,ax = new_slide("Question 10.4","Admissions Data — Logistic Regression Setup")
card(ax,0.35,5.05,8.4,1.75,"Dataset: ADMIS.DAT",
     "85 applicants: 31 admitted (status=1), 28 not-admitted (status=2).\n"
     "Borderline (status=3) excluded — analysis uses only clear decisions.\n"
     "New variable: admit = 0 (admitted), 1 (not-admitted).",fs=11)
card(ax,0.35,3.35,8.4,1.55,"GPA Category Recoding",
     "GPA < 2.50 → Category 1     |     2.51–3.00 → Category 2\n"
     "3.01–3.50 → Category 3      |     > 3.50 → Category 4\n"
     "Dummy coded with Category 1 as reference (3 dummies: GPA2, GPA3, GPA4).",
     tc=GOLD,bg="#1A1710",fs=11)
card(ax,0.35,1.5,8.4,1.7,"Perfect Separation Note",
     "GPA category perfectly separates the two classes:\n"
     "All Cat 3 & 4 applicants were admitted; all Cat 1 were not admitted.\n"
     "Maximum Likelihood estimates diverge — L2-penalized LR (C=1) used for stable coefficients.",
     tc=RED,bg="#1F1010",fs=11)

# GPA cat table
ax.text(9.15,6.65,"GPA Category Split",color=LBLUE,fontsize=11.5,fontweight="bold")
rows_t=[("Category","GPA Range","Admitted","Not Adm"),
        ("1","< 2.50","0","15"),
        ("2","2.51–3.00","1","13"),
        ("3","3.01–3.50","22","0"),
        ("4","> 3.50","8","0")]
for i,(c1,c2,c3,c4) in enumerate(rows_t):
    y=6.15-i*0.68
    bg=BLUE if i==0 else (NAVY2 if i%2 else NAVY3)
    col=WHITE
    ax.add_patch(FancyBboxPatch((9.1,y-0.28),4.1,0.6,
        boxstyle="square,pad=0",facecolor=bg,lw=0))
    ax.text(9.3, y+0.04,c1,color=col,fontsize=10.5,va="center",fontweight="bold" if i==0 else "normal")
    ax.text(10.1,y+0.04,c2,color=col,fontsize=10.5,va="center")
    ax.text(11.5,y+0.04,c3,color=(GREEN if i>0 else col),fontsize=10.5,va="center",ha="center")
    ax.text(12.7,y+0.04,c4,color=(RED   if i>0 else col),fontsize=10.5,va="center",ha="center")
pnum(ax,2); pages.append(fig)

# ════════════════════════════════════════════════════════════════
# PAGE 3 — Q10.4 RESULTS
# ════════════════════════════════════════════════════════════════
fig,ax = new_slide("Question 10.4","Admissions — Model Results & Interpretation")
stat(ax,0.35,5.5,2.85,1.4,f"{R['q104_acc1']:.1%}","Model 1 Accuracy\n(GPA only)",BLUE)
stat(ax,3.35,5.5,2.85,1.4,f"{R['q104_auc1']:.3f}","Model 1 AUC",LBLUE)
stat(ax,6.35,5.5,2.85,1.4,f"{R['q104_acc2']:.1%}","Model 2 Accuracy\n(GPA+GMAT)",GREEN)
stat(ax,9.35,5.5,2.85,1.4,f"{R['q104_auc2']:.3f}","Model 2 AUC",GOLD)

card(ax,0.35,3.5,6.1,1.85,"Effect of GPA Category",
     "GPA category is the dominant predictor — it alone achieves 98.3% accuracy.\n"
     "Coefficients for GPA3 and GPA4 are strongly negative (lower P(not-admitted)),\n"
     "confirming higher GPA strongly predicts admission. GPA2 slightly increases risk\n"
     "vs Category 1 baseline.",fs=10.5)
card(ax,6.55,3.5,6.42,1.85,"Effect of Adding GMAT",
     "Model 2 adds GMAT score. AUC improves to 1.000 (perfect discrimination).\n"
     "GMAT coefficient is negative: higher GMAT → lower P(not-admitted).\n"
     "However, accuracy drops slightly (96.6%) due to 2 misclassifications.\n"
     "Overall, GMAT provides marginal improvement over GPA category alone.",
     tc=GOLD,bg="#1A1710",fs=10.5)
card(ax,0.35,1.5,12.62,1.85,"Interpretation",
     "GPA category alone provides near-perfect classification (98.3%), supporting it as the primary admissions criterion.\n"
     "Adding GMAT achieves a perfect AUC = 1.000, meaning the combined model perfectly ranks applicants by default risk.\n"
     "The GPA-only model is simpler and nearly as accurate. Both models confirm: higher GPA category → dramatically lower\n"
     "probability of rejection.",
     tc=GREEN,bg="#101F1A",fs=10.5)
pnum(ax,3); pages.append(fig)

# ════════════════════════════════════════════════════════════════
# PAGE 4 — Q10.4 PLOTS
# ════════════════════════════════════════════════════════════════
fig,ax = new_slide("Question 10.4","Admissions — Visualizations")
ax.text(0.35,H-1.15,"ROC Curves, Confusion Matrix, and Coefficients",
        color=LGREY,fontsize=12)
embed(fig,"hw_plots/q104_results.png",[0.025,0.1,0.96,0.73])
pnum(ax,4); pages.append(fig)

# ════════════════════════════════════════════════════════════════
# PAGE 5 — Q10.5 HAND CALCULATIONS
# ════════════════════════════════════════════════════════════════
fig,ax = new_slide("Question 10.5","Cholesterol & Heart Disease — Hand Calculations",bar=GREEN)

ax.text(0.35,H-1.15,
        "114 males (40–65 yrs) classified by blood cholesterol and whether they developed heart disease.",
        color=LGREY,fontsize=11)

# Table header
hdrs=[("Cholesterol","<200","200–219","220–259",">259")]
rows_c=[
    ("Present (HD)",     "6",   "10",   "30",    "45"),
    ("Absent",           "5",    "6",    "5",     "7"),
    ("Total",           "11",   "16",   "35",    "52"),
    ("P(Disease)",   "0.545", "0.625","0.857",  "0.865"),
    ("Odds",         "1.200", "1.667","6.000",  "6.429"),
    ("Log-Odds",     "0.182", "0.511","1.792",  "1.861"),
]
ax.text(0.35,6.5,"(a) Probabilities and Log-Odds:",color=LBLUE,fontsize=11.5,fontweight="bold")
col_x=[0.35,2.4,4.3,6.2,8.1]
col_labels=["","< 200","200–219","220–259","> 259"]
for j,lbl in enumerate(col_labels):
    ax.add_patch(FancyBboxPatch((col_x[j] if j>0 else 0.35,6.08),
        1.85 if j>0 else 1.95,0.55,boxstyle="square,pad=0",facecolor=BLUE,lw=0))
    ax.text((col_x[j]+0.95) if j>0 else 1.3,6.35,lbl,
            color=WHITE,fontsize=10.5,fontweight="bold",ha="center",va="center")
for i,(label,*vals) in enumerate(rows_c):
    y_row=5.45-i*0.62
    bg=NAVY2 if i%2==0 else NAVY3
    ax.add_patch(FancyBboxPatch((0.35,y_row-0.25),1.95,0.55,
        boxstyle="square,pad=0",facecolor=BLUE,lw=0))
    ax.text(1.3,y_row+0.02,label,color=WHITE,fontsize=10,ha="center",va="center",fontweight="bold")
    for j,v in enumerate(vals):
        ax.add_patch(FancyBboxPatch((col_x[j+1],y_row-0.25),1.85,0.55,
            boxstyle="square,pad=0",facecolor=bg,lw=0))
        col_v = GREEN if (label=="P(Disease)" or label=="Log-Odds") else LGREY
        ax.text(col_x[j+1]+0.925,y_row+0.02,v,color=col_v,
                fontsize=10.5,ha="center",va="center")

ax.text(0.35,2.2,"(b) Hand Logistic Regression Equation:",color=LBLUE,fontsize=11.5,fontweight="bold")
b0=R["q105_b0"]; b1=R["q105_b1"]
ax.add_patch(FancyBboxPatch((0.35,1.3),9.5,0.78,
    boxstyle="round,pad=0.05",facecolor=NAVY2,lw=0))
ax.text(5.1,1.69,
        f"log-odds  =  {b0:.4f}  +  {b1:.6f} × Cholesterol",
        color=WHITE,fontsize=14,fontweight="bold",ha="center",va="center",
        family="DejaVu Sans")

card(ax,10.0,1.3,3.15,5.45,"Interpretation",
     "▸ All cholesterol groups\n"
     "  above <200 have higher\n"
     "  disease probability.\n\n"
     "▸ Log-odds increase nearly\n"
     "  linearly with cholesterol\n"
     "  level — clear dose-response.\n\n"
     "▸ Slope > 0 confirms higher\n"
     "  cholesterol raises heart\n"
     "  disease risk.",fs=10)
pnum(ax,5); pages.append(fig)

# ════════════════════════════════════════════════════════════════
# PAGE 6 — Q10.5 SOFTWARE RESULTS
# ════════════════════════════════════════════════════════════════
fig,ax = new_slide("Question 10.5","Cholesterol — Software LR Results & Visualizations",bar=GREEN)
ax.text(0.35,H-1.15,"(c) Software Logistic Regression with dummy variables  |  (d) Classification Table",
        color=LGREY,fontsize=11)
embed(fig,"hw_plots/q105_results.png",[0.025,0.1,0.64,0.72])

params_c = R["q105_sw_params"]; pvals_c = R["q105_sw_pvalues"]
ax.text(8.6,6.5,"Coefficient Table:",color=LBLUE,fontsize=11.5,fontweight="bold")
rows_sw=[("Term","Coef","p-value"),
         ("Intercept",f"{params_c['Intercept']:.4f}",f"{pvals_c['Intercept']:.4f}"),
         ("200-219",  f"{params_c['c200_219']:.4f}", f"{pvals_c['c200_219']:.4f}"),
         ("220-259",  f"{params_c['c220_259']:.4f}", f"{pvals_c['c220_259']:.4f}"),
         ("> 259",    f"{params_c['c_gt259']:.4f}",  f"{pvals_c['c_gt259']:.4f}"),]
for i,(a,b,c) in enumerate(rows_sw):
    y_r=6.0-i*0.68
    bg=BLUE if i==0 else (NAVY2 if i%2 else NAVY3)
    ax.add_patch(FancyBboxPatch((8.55,y_r-0.28),4.6,0.6,boxstyle="square,pad=0",facecolor=bg,lw=0))
    sig="*" if (i>0 and float(c)<0.05) else ""
    ax.text(8.75, y_r+0.02,a,color=WHITE,fontsize=10.5,va="center")
    ax.text(10.65,y_r+0.02,b,color=(GREEN if i>0 else WHITE),fontsize=10.5,va="center",ha="center")
    ax.text(12.3, y_r+0.02,c+sig,color=(RED if (i>0 and float(c)<0.05) else LGREY),
            fontsize=10.5,va="center",ha="center")

card(ax,8.55,1.25,4.6,2.15,"(d) Classification Table Discussion",
     f"Accuracy = {R['q105_acc']:.1%}\n"
     "Model correctly classifies all 91 disease-present\n"
     "cases but misses all 23 disease-absent — high recall,\n"
     "zero specificity. This reflects the class imbalance\n"
     "(80% disease present). Classification table should be\n"
     "interpreted with caution: AUC is more informative.",
     tc=GOLD,bg="#1A1710",fs=10)
pnum(ax,6); pages.append(fig)

# ════════════════════════════════════════════════════════════════
# PAGE 7 — Q10.6 SETUP + RESULTS
# ════════════════════════════════════════════════════════════════
fig,ax = new_slide("Question 10.6","Depression Data — LR vs Discriminant Analysis")
ax.text(0.35,H-1.15,
        "294 subjects. Dependent variable: CASES (0=Normal, 1=Depressed where CESD>16).",
        color=LGREY,fontsize=11)

stat(ax,0.35,5.5,2.85,1.35,f"{R['q106_lr_acc']:.1%}","LR Accuracy",BLUE)
stat(ax,3.35,5.5,2.85,1.35,f"{R['q106_lr_auc']:.3f}","LR AUC",LBLUE)
stat(ax,6.35,5.5,2.85,1.35,f"{R['q106_lda_acc']:.1%}","LDA Accuracy",GREEN)
stat(ax,9.35,5.5,2.85,1.35,f"{R['q106_lda_auc']:.3f}","LDA AUC",GOLD)

sig_vars = R["q106_sig_vars"]
card(ax,0.35,3.55,6.1,1.78,"Significant Predictors (LR, p < 0.05)",
     f"▸ SEX (p=0.038) — females significantly more likely to be depressed\n"
     f"▸ INCOME (p=0.044) — higher income reduces depression risk\n"
     f"▸ RELIG (p=0.028) — religious affiliation has protective effect\n"
     f"▸ BEDDAYS (p=0.029) — days spent in bed raises depression risk",
     tc=RED,bg="#1F1010",fs=10.5)
card(ax,6.55,3.55,6.42,1.78,"LR vs LDA Comparison",
     f"LR: Accuracy={R['q106_lr_acc']:.1%}, AUC={R['q106_lr_auc']:.3f}\n"
     f"LDA: Accuracy={R['q106_lda_acc']:.1%}, AUC={R['q106_lda_auc']:.3f}\n"
     "Both methods perform similarly. LR slightly outperforms LDA on accuracy\n"
     "and AUC, consistent with LR's weaker distributional assumptions.",
     tc=GOLD,bg="#1A1710",fs=10.5)
card(ax,0.35,1.55,12.62,1.85,"Interpretation",
     "The logistic regression model explains depression with an overall accuracy of 84.0%. "
     "The four significant predictors\n"
     "align with established clinical literature: female sex, low income, lack of religious "
     "support, and health-related bed\n"
     "days are all established risk factors for depression. "
     "LDA matches LR closely (83.0%), suggesting the linear\n"
     "decision boundary is appropriate here despite slight class imbalance (244 normal, 50 depressed).",
     tc=GREEN,bg="#101F1A",fs=10.5)
pnum(ax,7); pages.append(fig)

# ════════════════════════════════════════════════════════════════
# PAGE 8 — Q10.6 PLOTS
# ════════════════════════════════════════════════════════════════
fig,ax = new_slide("Question 10.6","Depression — Visualizations")
ax.text(0.35,H-1.15,
        "Confusion matrices (LR vs LDA), ROC curves, and significant coefficient bar chart.",
        color=LGREY,fontsize=12)
embed(fig,"hw_plots/q106_results.png",[0.025,0.1,0.96,0.73])
pnum(ax,8); pages.append(fig)

# ════════════════════════════════════════════════════════════════
# PAGE 9 — Q11.5 MANOVA RESULTS
# ════════════════════════════════════════════════════════════════
fig,ax = new_slide("Question 11.5","MANOVA — Depression & Phone Data",bar=GOLD)
ax.text(0.35,H-1.15,
        "MANOVA tests whether group means on multiple dependent variables differ simultaneously.",
        color=LGREY,fontsize=11)

# Depression MANOVA
ax.text(0.35,5.9,"Part A: Depression Data (DVs = C1-C20, Group = CASES)",
        color=LBLUE,fontsize=12,fontweight="bold")
lam_d=R["q115_dep_lambda"]; F_d=R["q115_dep_F"]; df_d=R["q115_dep_df"]
stat(ax,0.35,4.3,2.85,1.42,f"{lam_d:.4f}","Wilks' Lambda\n(Depression)",RED)
stat(ax,3.35,4.3,2.85,1.42,f"{F_d:.2f}",f"Approx F({df_d[0]:.0f},{df_d[1]:.0f})",RED)
stat(ax,6.35,4.3,2.85,1.42,"p < .0001","MANOVA p-value",RED)
stat(ax,9.35,4.3,2.85,1.42,f"{R['q115_dep_lda_acc']:.1%}","LDA Accuracy\n(C1-C20→CASES)",GREEN)

card(ax,0.35,2.6,12.62,1.55,
     "Interpretation — Depression MANOVA",
     "Wilks' Lambda = 0.297 (far from 1) and F(20,273)=32.31 (p<.0001): the two groups "
     "(normal vs depressed)\n"
     "differ significantly on the combined set of 20 CES-D items. ALL 20 items show "
     "significant univariate F-tests (p<.0001),\n"
     "meaning every individual depression symptom distinguishes the groups. "
     "LDA achieves 97.96% accuracy using C1-C20.",
     tc=GREEN,bg="#101F1A",fs=10.5)

# Phone MANOVA
ax.text(0.35,2.2,"Part B: Phone Data (DVs = A1-A6, Group = n_phones)",
        color=LBLUE,fontsize=12,fontweight="bold")
lam_p=R["q115_ph_lambda"]; F_p=R["q115_ph_F"]; df_p=R["q115_ph_df"]
stat(ax,0.35,0.7,2.85,1.38,f"{lam_p:.4f}","Wilks' Lambda\n(Phone)",GOLD)
stat(ax,3.35,0.7,2.85,1.38,f"{F_p:.2f}",f"Approx F({df_p[0]:.0f},{df_p[1]:.0f})",GOLD)
stat(ax,6.35,0.7,2.85,1.38,"p < .0001","MANOVA p-value",GOLD)
stat(ax,9.35,0.7,2.85,1.38,f"{R['q115_ph_lda_acc']:.1%}","LDA Accuracy\n(A1-A6→phones)",BLUE)
pnum(ax,9); pages.append(fig)

# ════════════════════════════════════════════════════════════════
# PAGE 10 — Q11.5 PLOTS + FINAL
# ════════════════════════════════════════════════════════════════
fig,ax = new_slide("Question 11.5","MANOVA — Visualizations & LDA Comparison",bar=GOLD)
ax.text(0.35,H-1.15,
        "Group mean heatmap, univariate F-statistics, attitude profiles, and MANOVA vs LDA comparison.",
        color=LGREY,fontsize=11)
embed(fig,"hw_plots/q115_results.png",[0.025,0.1,0.96,0.73])
pnum(ax,10); pages.append(fig)

# ════════════════════════════════════════════════════════════════
# SAVE
# ════════════════════════════════════════════════════════════════
out="Homework_Solutions.pdf"
with PdfPages(out) as pdf:
    for f in pages:
        pdf.savefig(f,bbox_inches="tight",dpi=150,facecolor=f.get_facecolor())
        plt.close(f)
print(f"Saved: {out}  ({len(pages)} pages)")

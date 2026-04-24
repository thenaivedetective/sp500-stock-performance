from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable, PageBreak)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from health_cca import results
import numpy as np

doc = SimpleDocTemplate(
    "health_cca_results.pdf",
    pagesize=letter,
    rightMargin=0.75*inch,
    leftMargin=0.75*inch,
    topMargin=0.75*inch,
    bottomMargin=0.75*inch
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle('Title', parent=styles['Title'],
    fontSize=15, spaceAfter=6, alignment=TA_CENTER,
    textColor=colors.HexColor('#1a3a5c'))

h1_style = ParagraphStyle('H1', parent=styles['Heading1'],
    fontSize=12, spaceBefore=14, spaceAfter=4,
    textColor=colors.HexColor('#1a3a5c'))

h2_style = ParagraphStyle('H2', parent=styles['Heading2'],
    fontSize=10, spaceBefore=10, spaceAfter=3,
    textColor=colors.HexColor('#2c5f8a'))

body_style = ParagraphStyle('Body', parent=styles['Normal'],
    fontSize=9, spaceAfter=4, leading=13, alignment=TA_JUSTIFY)

def hr():
    return HRFlowable(width="100%", thickness=0.5,
                      color=colors.HexColor('#1a3a5c'), spaceAfter=4)

def make_table(data, col_widths, header=True):
    style = [
        ('FONTNAME',  (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE',  (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.white, colors.HexColor('#f0f4f8')]),
        ('GRID',      (0,0), (-1,-1), 0.3, colors.HexColor('#cccccc')),
        ('VALIGN',    (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING',  (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING',   (0,0), (-1,-1), 3),
        ('BOTTOMPADDING',(0,0), (-1,-1), 3),
    ]
    if header:
        style += [
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a3a5c')),
            ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
            ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE',   (0,0), (-1,0), 8),
        ]
    return Table(data, colWidths=col_widths, style=TableStyle(style))

r   = results
n, p, q = r['n'], r['p'], r['q']
rc   = r['canonical_corr']
ev   = r['eigenvalues']
wl   = r['wilks']
ch   = r['chi2']
dfs  = r['df_vals']
pvs  = r['p_vals']
ra   = r['raw_a']
rb   = r['raw_b']
sa   = r['std_coef_a']
sb   = r['std_coef_b']
sX   = r['struct_X']
sY   = r['struct_Y']
rdX  = r['redundancy_X']
rdY  = r['redundancy_Y']
varX = r['var_X']
varY = r['var_Y']
means = r['col_means']
stds  = r['col_stds']
nc   = len(rc)
all_vars = varX + varY

story = []

story.append(Paragraph("Canonical Correlation Analysis", title_style))
story.append(Paragraph("Health and Lifestyle Dataset", title_style))
story.append(Paragraph(
    "Examining the Relationship Between Lifestyle Behaviors and Health Outcomes",
    ParagraphStyle('sub', parent=styles['Normal'], fontSize=10,
                   alignment=TA_CENTER, spaceAfter=4,
                   textColor=colors.HexColor('#2c5f8a'))))
story.append(Paragraph(
    "Lana Gidan | Applied Multivariate Data Analysis",
    ParagraphStyle('auth', parent=styles['Normal'], fontSize=9,
                   alignment=TA_CENTER, spaceAfter=8, textColor=colors.grey)))
story.append(hr())

story.append(Paragraph("1. Introduction and Study Context", h1_style))
story.append(Paragraph(
    "This analysis investigates the relationship between lifestyle behavioral patterns and "
    "physiological health outcomes using Canonical Correlation Analysis (CCA). The dataset "
    f"contains <b>{n} subjects</b> measured on six variables, partitioned into two sets: "
    "a <b>lifestyle set (X)</b> with three behavioral indicators, and a <b>health outcomes "
    "set (Y)</b> with three physiological measures.",
    body_style))

story.append(Paragraph("Variable Sets", h2_style))
vd = [
    ["Set", "Variables", "Description", "Count"],
    ["X — Lifestyle", "Exercise, DietScore, SleepHours",
     "Behavioral/lifestyle indicators", "p = 3"],
    ["Y — Health", "BloodPressure, Cholesterol, BMI",
     "Physiological health outcomes", "q = 3"],
]
story.append(make_table(vd, [0.9*inch, 2.2*inch, 2.4*inch, 0.8*inch]))
story.append(Spacer(1,6))
story.append(Paragraph(
    f"With min(p, q) = min(3, 3) = <b>3 canonical variate pairs</b>, CCA will identify up to "
    "three independent dimensions of association between lifestyle behaviors and health outcomes.",
    body_style))

story.append(Paragraph("2. Descriptive Statistics", h1_style))
story.append(hr())
desc = [["Variable", "Set", "Mean", "Std Dev", "Role"]]
roles = ["Lifestyle"]*3 + ["Health"]*3
descs = ["Exercise frequency","Diet quality score","Sleep hours/night",
         "Systolic BP (mmHg)","Total cholesterol (mg/dL)","Body mass index"]
for i, v in enumerate(all_vars):
    desc.append([v, roles[i], f"{means[i]:.3f}", f"{stds[i]:.3f}", descs[i]])
story.append(make_table(desc, [1.1*inch, 0.8*inch, 0.8*inch, 0.8*inch, 2.4*inch]))
story.append(Spacer(1,6))
story.append(Paragraph(
    "Subjects averaged about 4.5 exercise sessions, a diet score of 6.7, and 6.6 hours of "
    "sleep per night. Health-wise, the average systolic blood pressure was 126.3 mmHg, "
    "cholesterol was 197.2 mg/dL, and BMI was 22.3 — all near healthy reference ranges, "
    "with meaningful individual variation captured by the standard deviations.",
    body_style))

story.append(Paragraph("3. Canonical Correlations", h1_style))
story.append(hr())
story.append(Paragraph(
    "The three canonical correlations and their squared values are shown below. "
    "r*² represents the proportion of shared variance between each canonical variate pair.",
    body_style))
interp = ["Very Strong", "Strong", "Negligible"]
cc_d = [["Pair", "Canonical Corr (r*)", "r*²", "Eigenvalue", "Interpretation"]]
for i in range(nc):
    cc_d.append([f"r*{i+1}", f"{rc[i]:.6f}", f"{rc[i]**2:.6f}",
                 f"{ev[i]:.6f}", interp[i]])
story.append(make_table(cc_d, [0.5*inch, 1.4*inch, 1.1*inch, 1.1*inch, 1.8*inch]))
story.append(Spacer(1,6))

story.append(Paragraph(
    f"<b>r*\u2081 = {rc[0]:.4f} (r*\u2081² = {rc[0]**2:.4f}):</b> This is an exceptionally strong "
    f"canonical correlation. The first pair of canonical variates shares {rc[0]**2*100:.1f}% of "
    "variance, indicating a very powerful relationship between the dominant lifestyle factor "
    "and the dominant health outcome factor.", body_style))
story.append(Paragraph(
    f"<b>r*\u2082 = {rc[1]:.4f} (r*\u2082² = {rc[1]**2:.4f}):</b> The second canonical correlation is "
    "also strong, capturing an additional {:.1f}% of shared variance along a second, independent "
    "dimension of the lifestyle–health relationship.".format(rc[1]**2*100), body_style))
story.append(Paragraph(
    f"<b>r*\u2083 = {rc[2]:.4f} (r*\u2083² = {rc[2]**2:.4f}):</b> The third correlation is negligible "
    f"({rc[2]**2*100:.2f}% shared variance) and will be confirmed as non-significant by the "
    "Wilks' Lambda tests.", body_style))

story.append(Paragraph("4. Significance Tests — Wilks' Lambda", h1_style))
story.append(hr())
t_mult = n - 1 - (p + q + 1)/2
story.append(Paragraph(
    f"Wilks' Lambda tests each successive set of roots jointly. The Bartlett chi-square "
    f"approximation uses multiplier t = n − 1 − (p+q+1)/2 = {t_mult:.1f}.",
    body_style))

wl_d = [["Test (H\u2080)", "Wilks \u039b", "Chi-Square", "df", "p-value", "Decision"]]
for i in range(nc):
    if pvs[i] < 0.001:   sig = "Reject H\u2080 (***)"
    elif pvs[i] < 0.01:  sig = "Reject H\u2080 (**)"
    elif pvs[i] < 0.05:  sig = "Reject H\u2080 (*)"
    else:                sig = "Fail to Reject"
    wl_d.append([f"Roots {i+1}\u2013{nc} = 0", f"{wl[i]:.6f}",
                 f"{ch[i]:.3f}", str(dfs[i]), f"{pvs[i]:.6f}", sig])
story.append(make_table(wl_d, [1.3*inch, 0.9*inch, 1.0*inch, 0.4*inch, 0.9*inch, 1.4*inch]))
story.append(Spacer(1,6))

findings_sig = [
    (f"Roots 1–3 (all roots): Λ = {wl[0]:.4f}, χ²({dfs[0]}) = {ch[0]:.3f}, p < 0.001",
     "The overall multivariate relationship between lifestyle behaviors and health outcomes "
     "is highly significant. There is overwhelming evidence that the two variable sets are "
     "related."),
    (f"Roots 2–3: Λ = {wl[1]:.4f}, χ²({dfs[1]}) = {ch[1]:.3f}, p < 0.001",
     "Even after the first canonical dimension is removed, the remaining relationship "
     "is still highly significant. A second independent lifestyle–health dimension exists."),
    (f"Root 3 only: Λ = {wl[2]:.4f}, χ²({dfs[2]}) = {ch[2]:.3f}, p = {pvs[2]:.4f}",
     "The third root is not significant (p > 0.05). Only two canonical dimensions carry "
     "meaningful information; the third should be discarded from interpretation."),
]
for title, text in findings_sig:
    story.append(Paragraph(f"<b>{title}</b>", body_style))
    story.append(Paragraph(text, ParagraphStyle('ind', parent=body_style,
        leftIndent=12, spaceAfter=6)))

story.append(PageBreak())

story.append(Paragraph("5. Canonical Coefficients", h1_style))
story.append(hr())

story.append(Paragraph("5.1 Raw Canonical Coefficients — X Set (a vectors)", h2_style))
story.append(Paragraph(
    "Raw coefficients form the canonical variates from original (unstandardized) variables. "
    "They are scale-dependent and should not be compared across variables directly.",
    body_style))
raw_x_d = [["Variable"] + [f"U{k+1}" for k in range(nc)]]
for i, v in enumerate(varX):
    raw_x_d.append([v] + [f"{ra[i,k]:.4f}" for k in range(nc)])
story.append(make_table(raw_x_d, [1.3*inch]+[1.1*inch]*nc))
story.append(Spacer(1,6))

story.append(Paragraph("5.2 Raw Canonical Coefficients — Y Set (b vectors)", h2_style))
raw_y_d = [["Variable"] + [f"V{k+1}" for k in range(nc)]]
for j, v in enumerate(varY):
    raw_y_d.append([v] + [f"{rb[j,k]:.4f}" for k in range(nc)])
story.append(make_table(raw_y_d, [1.3*inch]+[1.1*inch]*nc))
story.append(Spacer(1,6))

story.append(Paragraph("5.3 Standardized Canonical Coefficients — X Set", h2_style))
story.append(Paragraph(
    "Standardized coefficients allow direct comparison of variable importance within each "
    "canonical variate. Larger absolute values indicate stronger contribution.",
    body_style))
std_x_d = [["Variable"] + [f"U{k+1}" for k in range(nc)]]
for i, v in enumerate(varX):
    std_x_d.append([v] + [f"{sa[i,k]:.4f}" for k in range(nc)])
story.append(make_table(std_x_d, [1.3*inch]+[1.1*inch]*nc))
story.append(Spacer(1,4))
story.append(Paragraph(
    f"For U\u2081: Exercise ({sa[0,0]:.4f}) and DietScore ({sa[1,0]:.4f}) are the dominant "
    f"contributors to the first lifestyle canonical variate, while SleepHours ({sa[2,0]:.4f}) "
    "contributes minimally. For U\u2082: DietScore reverses sign and dominates, with Exercise "
    "remaining positive — this second dimension contrasts diet versus exercise patterns. "
    "SleepHours dominates U\u2083 exclusively.", body_style))

story.append(Paragraph("5.4 Standardized Canonical Coefficients — Y Set", h2_style))
std_y_d = [["Variable"] + [f"V{k+1}" for k in range(nc)]]
for j, v in enumerate(varY):
    std_y_d.append([v] + [f"{sb[j,k]:.4f}" for k in range(nc)])
story.append(make_table(std_y_d, [1.3*inch]+[1.1*inch]*nc))
story.append(Spacer(1,4))
story.append(Paragraph(
    "All three health variables contribute negatively to V\u2081 with large coefficients, "
    "forming a composite 'poor health' dimension. For V\u2082, Cholesterol dominates with a "
    "large negative coefficient, contrasting with BloodPressure being positive — this "
    "dimension separates cholesterol from blood pressure patterns.", body_style))

story.append(Paragraph("6. Canonical Structure Coefficients", h1_style))
story.append(hr())
story.append(Paragraph(
    "Structure coefficients (canonical loadings) are correlations between original variables "
    "and canonical variates. They indicate how much each variable 'loads onto' each dimension. "
    "Loadings with |r| \u2265 0.30 are considered substantively meaningful.",
    body_style))

story.append(Paragraph("6.1 X Variables with Canonical Variates U\u2081–U\u2083", h2_style))
sx_d = [["Variable"] + [f"U{k+1}" for k in range(nc)]]
for i, v in enumerate(varX):
    sx_d.append([v] + [f"{sX[i,k]:.4f}" for k in range(nc)])
story.append(make_table(sx_d, [1.3*inch]+[1.1*inch]*nc))
story.append(Spacer(1,4))
story.append(Paragraph(
    f"Exercise (U\u2081 loading = {sX[0,0]:.4f}) and DietScore ({sX[1,0]:.4f}) load strongly "
    "and positively on U\u2081. SleepHours loads minimally on U\u2081 and U\u2082 but dominates "
    f"U\u2083 ({sX[2,2]:.4f}), confirming that the three lifestyle variables contribute to "
    "three distinct canonical dimensions.", body_style))

story.append(Paragraph("6.2 Y Variables with Canonical Variates V\u2081–V\u2083", h2_style))
sy_d = [["Variable"] + [f"V{k+1}" for k in range(nc)]]
for j, v in enumerate(varY):
    sy_d.append([v] + [f"{sY[j,k]:.4f}" for k in range(nc)])
story.append(make_table(sy_d, [1.3*inch]+[1.1*inch]*nc))
story.append(Spacer(1,4))
story.append(Paragraph(
    f"All three health variables load very strongly (negatively) on V\u2081 "
    f"(BloodPressure: {sY[0,0]:.4f}, Cholesterol: {sY[1,0]:.4f}, BMI: {sY[2,0]:.4f}). "
    "This confirms that V\u2081 captures an overall poor-health composite. On V\u2082, "
    f"Cholesterol loads most strongly ({sY[1,1]:.4f}), distinguishing it from the others. "
    "V\u2083 is non-significant and should not be interpreted.", body_style))

story.append(Paragraph("7. Redundancy Analysis", h1_style))
story.append(hr())
story.append(Paragraph(
    "Redundancy indices measure how much variance in one variable set is explained by "
    "the canonical variates of the opposite set. This extends CCA by quantifying "
    "predictive usefulness.",
    body_style))
rd_d = [["Pair", "Redundancy (X explained by V)", "Redundancy (Y explained by U)"]]
for k in range(nc):
    rd_d.append([f"Pair {k+1}", f"{rdX[k]:.6f} ({rdX[k]*100:.2f}%)",
                 f"{rdY[k]:.6f} ({rdY[k]*100:.2f}%)"])
story.append(make_table(rd_d, [0.8*inch, 2.3*inch, 2.3*inch]))
story.append(Spacer(1,6))
story.append(Paragraph(
    f"The health outcomes (Y) are explained remarkably well by the lifestyle canonical "
    f"variates: Pair 1 alone accounts for {rdY[0]*100:.1f}% of Y-set variance, and "
    f"Pair 2 adds another {rdY[1]*100:.1f}%. Together, Pairs 1 and 2 explain "
    f"{(rdY[0]+rdY[1])*100:.1f}% of total health outcome variance through lifestyle "
    "canonical variates — a very high redundancy indicating strong predictive power. "
    "Conversely, the lifestyle variables are somewhat less explained by the health "
    f"variates ({(rdX[0]+rdX[1])*100:.1f}% combined), which is typical since lifestyle "
    "behaviors have more independent variation.", body_style))

story.append(PageBreak())

story.append(Paragraph("8. Overall Interpretation and Conclusions", h1_style))
story.append(hr())

conclusions = [
    ("<b>1. Two significant canonical dimensions:</b>",
     "Canonical pairs 1 and 2 are both highly statistically significant (p < 0.001). "
     "The third pair is not significant (p = 0.72) and is discarded. This means lifestyle "
     "behaviors relate to health outcomes through two independent channels."),
    (f"<b>2. First canonical dimension (r*\u2081 = {rc[0]:.4f}):</b>",
     "This dimension represents an overall healthy lifestyle → good health outcomes axis. "
     "Higher Exercise and DietScore jointly predict lower BloodPressure, Cholesterol, and "
     "BMI. This is the dominant pathway — it accounts for the vast majority of the "
     "shared variance between the two variable sets."),
    (f"<b>3. Second canonical dimension (r*\u2082 = {rc[1]:.4f}):</b>",
     "This dimension is also significant and represents a contrast between DietScore and "
     "Exercise: higher diet quality (with lower exercise) is associated with lower "
     "Cholesterol specifically. This second dimension adds independent information about "
     "the diet–cholesterol pathway that is not captured by the first dimension."),
    ("<b>4. SleepHours operates independently:</b>",
     "SleepHours loads primarily on U\u2083 (the non-significant third dimension), indicating "
     "that sleep has minimal association with blood pressure, cholesterol, and BMI in this "
     "dataset — at least independently from exercise and diet effects. Its contribution "
     "to the two significant dimensions is near zero."),
    ("<b>5. Health outcomes are strongly predicted by lifestyle:</b>",
     f"The combined redundancy of Y given U is {(rdY[0]+rdY[1])*100:.1f}%, meaning that "
     "the two significant lifestyle canonical variates collectively account for over "
     f"{(rdY[0]+rdY[1])*100:.0f}% of the variance in the health outcome set. This is a "
     "remarkably strong predictive relationship."),
    ("<b>6. Practical implication:</b>",
     "Interventions targeting both exercise frequency and diet quality simultaneously would "
     "have the broadest impact on all three health outcomes (blood pressure, cholesterol, "
     "and BMI). Diet quality specifically has an additional independent effect on cholesterol "
     "beyond its joint role with exercise."),
]
for title, text in conclusions:
    story.append(Paragraph(title, body_style))
    story.append(Paragraph(text, ParagraphStyle('ind', parent=body_style,
        leftIndent=12, spaceAfter=6)))

story.append(Spacer(1, 8))
story.append(hr())
story.append(Paragraph(
    "Report prepared for: Applied Multivariate Data Analysis | Lana Gidan | "
    "Binghamton University | Health/Lifestyle CCA Dataset",
    ParagraphStyle('footer', parent=styles['Normal'],
        fontSize=7.5, alignment=TA_CENTER, textColor=colors.grey)))

doc.build(story)
print("PDF saved: health_cca_results.pdf")

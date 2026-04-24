from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable, PageBreak)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import numpy as np
from cetnew_cca import results

doc = SimpleDocTemplate(
    "cetnew_cca_results.pdf",
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
    textColor=colors.HexColor('#1a3a5c'),
    borderPad=2)

h2_style = ParagraphStyle('H2', parent=styles['Heading2'],
    fontSize=10, spaceBefore=10, spaceAfter=3,
    textColor=colors.HexColor('#2c5f8a'))

body_style = ParagraphStyle('Body', parent=styles['Normal'],
    fontSize=9, spaceAfter=4, leading=13, alignment=TA_JUSTIFY)

mono_style = ParagraphStyle('Mono', parent=styles['Normal'],
    fontSize=8, fontName='Courier', spaceAfter=2, leading=11)

def hr(): return HRFlowable(width="100%", thickness=0.5,
                             color=colors.HexColor('#1a3a5c'), spaceAfter=4)

def section_table(data, col_widths, header_row=True):
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
    if header_row:
        style += [
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a3a5c')),
            ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
            ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE',   (0,0), (-1,0), 8),
        ]
    return Table(data, colWidths=col_widths, style=TableStyle(style))

r = results
n, p, q = r['n'], r['p'], r['q']
rc       = r['canonical_corr']
ev       = r['eigenvalues']
wilks    = r['wilks']
chi2     = r['chi2']
df_vals  = r['df_vals']
p_vals   = r['p_vals']
raw_a    = r['raw_a']
raw_b    = r['raw_b']
sX       = r['struct_X']
sY       = r['struct_Y']
varX     = r['var_X']
varY     = r['var_Y']
num_can  = len(rc)

story = []

story.append(Paragraph("Canonical Correlation Analysis", title_style))
story.append(Paragraph("CETNEW Data — Question 14.4", title_style))
story.append(Paragraph(
    "Consumer Ethnocentric Tendencies and Attitudes Toward Importing Products",
    ParagraphStyle('sub', parent=styles['Normal'], fontSize=10,
                   alignment=TA_CENTER, spaceAfter=4,
                   textColor=colors.HexColor('#2c5f8a'))))
story.append(Paragraph(
    "Lana Gidan | Applied Multivariate Data Analysis",
    ParagraphStyle('auth', parent=styles['Normal'], fontSize=9,
                   alignment=TA_CENTER, spaceAfter=8,
                   textColor=colors.grey)))
story.append(hr())

story.append(Paragraph("1. Introduction and Study Context", h1_style))
story.append(Paragraph(
    "This analysis examines the relationship between consumer ethnocentric tendencies (CET) "
    "and attitudes toward importing foreign products. The study involves <b>667 subjects</b> "
    "whose ethnocentric tendencies were measured using <b>seven indicators (X\u2081–X\u2087)</b>, "
    "and whose attitudinal responses toward importing were captured through <b>five measures "
    "(Y\u2081–Y\u2085)</b>. The data are provided as a covariance matrix in CETNEW.DAT.",
    body_style))
story.append(Paragraph(
    "Canonical Correlation Analysis (CCA) is the appropriate multivariate method here because "
    "it identifies the maximum correlations between linear combinations of the X set and linear "
    "combinations of the Y set. Rather than examining each X–Y pair in isolation, CCA finds the "
    "directions in both variable spaces that are most correlated, providing a structural model "
    "of how CET collectively relates to consumer attitudes.", body_style))
story.append(Spacer(1, 4))

story.append(Paragraph("Variable Sets", h2_style))
var_data = [
    ["Set", "Variables", "Role", "Count"],
    ["X (Predictor)", "X\u2081, X\u2082, X\u2083, X\u2084, X\u2085, X\u2086, X\u2087",
     "Ethnocentric tendency indicators (CET)", "p = 7"],
    ["Y (Criterion)", "Y\u2081, Y\u2082, Y\u2083, Y\u2084, Y\u2085",
     "Attitudinal measures toward imports", "q = 5"],
]
story.append(section_table(var_data, [0.8*inch, 2.2*inch, 2.8*inch, 0.9*inch]))
story.append(Spacer(1, 6))

story.append(Paragraph(
    "The number of canonical variate pairs is min(p, q) = min(7, 5) = <b>5 pairs</b>. "
    "Each pair (U\u1d4f, V\u1d4f) represents a dimension of association between the two variable sets, "
    "with the first pair capturing the strongest association.", body_style))

story.append(Paragraph("2. Canonical Correlations", h1_style))
story.append(hr())
story.append(Paragraph(
    "The five canonical correlations (r*) and their squared values are presented below. "
    "The squared canonical correlation (r*²) indicates the proportion of shared variance "
    "between the k-th pair of canonical variates.", body_style))

cc_data = [["Pair", "Canonical Corr (r*)", "Squared (r*²)", "Eigenvalue", "Interpretation"]]
interp = ["Very Strong", "Weak", "Weak", "Very Weak", "Negligible"]
for i in range(num_can):
    cc_data.append([
        f"r*{i+1}",
        f"{rc[i]:.6f}",
        f"{rc[i]**2:.6f}",
        f"{ev[i]:.6f}",
        interp[i]
    ])
story.append(section_table(cc_data, [0.5*inch, 1.4*inch, 1.3*inch, 1.2*inch, 1.6*inch]))
story.append(Spacer(1, 6))

story.append(Paragraph(
    f"<b>The first canonical correlation r*\u2081 = {rc[0]:.4f}</b> is by far the largest, "
    f"with r*\u2081² = {rc[0]**2:.4f}, meaning that the first pair of canonical variates shares "
    f"<b>{rc[0]**2*100:.1f}% of variance</b>. This is a strong association by social science standards. "
    "The remaining four canonical correlations are all substantially smaller (below 0.23), "
    "indicating that the dominant relationship is captured almost entirely by the first canonical "
    "variate pair.", body_style))

story.append(Paragraph("3. Significance Tests (Wilks' Lambda)", h1_style))
story.append(hr())
story.append(Paragraph(
    "Wilks' Lambda (Λ) tests whether the remaining canonical correlations (from the i-th root "
    "onward) are jointly equal to zero. A small Λ indicates strong association. The chi-square "
    "approximation is: χ² = −[n − 1 − (p + q + 1)/2] × ln(Λ), "
    f"giving a multiplier of {n - 1 - (p + q + 1)/2:.1f} for this study.", body_style))

wl_data = [["Test (H\u2080)", "Wilks Λ", "Chi-Square", "df", "p-value", "Significance"]]
labels = [f"Roots {i+1} to {num_can} = 0" for i in range(num_can)]
for i in range(num_can):
    if p_vals[i] < 0.001:   sig = "*** (p < 0.001)"
    elif p_vals[i] < 0.01:  sig = "** (p < 0.01)"
    elif p_vals[i] < 0.05:  sig = "* (p < 0.05)"
    else:                    sig = "n.s. (p > 0.05)"
    wl_data.append([
        labels[i], f"{wilks[i]:.6f}", f"{chi2[i]:.3f}",
        str(df_vals[i]), f"{p_vals[i]:.6f}", sig
    ])
story.append(section_table(wl_data,
    [1.5*inch, 0.9*inch, 1.0*inch, 0.5*inch, 0.9*inch, 1.3*inch]))
story.append(Spacer(1, 6))

story.append(Paragraph("<b>Interpretation of significance tests:</b>", h2_style))
story.append(Paragraph(
    f"• <b>Roots 1 to 5 (all roots):</b> Λ = {wilks[0]:.4f}, χ²({df_vals[0]}) = {chi2[0]:.3f}, "
    f"p < 0.001 — The overall relationship between the CET indicators and the attitudinal "
    "measures is highly significant. There is strong evidence that CET collectively affects "
    "attitudes toward importing products.", body_style))
story.append(Paragraph(
    f"• <b>Roots 2 to 5:</b> Λ = {wilks[1]:.4f}, χ²({df_vals[1]}) = {chi2[1]:.3f}, "
    f"p < 0.001 — Even after removing the first canonical dimension, the remaining "
    "association is still statistically significant.", body_style))
story.append(Paragraph(
    f"• <b>Roots 3 to 5:</b> Λ = {wilks[2]:.4f}, χ²({df_vals[2]}) = {chi2[2]:.3f}, "
    f"p = {p_vals[2]:.4f} — Still significant, though the association is much weaker.", body_style))
story.append(Paragraph(
    f"• <b>Roots 4 to 5:</b> Λ = {wilks[3]:.4f}, χ²({df_vals[3]}) = {chi2[3]:.3f}, "
    f"p = {p_vals[3]:.4f} — Marginally significant at the 5% level.", body_style))
story.append(Paragraph(
    f"• <b>Root 5 only:</b> Λ = {wilks[4]:.4f}, χ²({df_vals[4]}) = {chi2[4]:.3f}, "
    f"p = {p_vals[4]:.4f} — <b>Not significant.</b> The fifth canonical dimension does "
    "not contribute meaningful additional association beyond chance.", body_style))
story.append(Paragraph(
    "<b>Conclusion:</b> Four of the five canonical variate pairs are statistically significant "
    "(p < 0.05). However, practical significance is dominated by the first pair, which accounts "
    f"for {rc[0]**2*100:.1f}% of shared variance. Pairs 2–4 are statistically detectable "
    "largely because of the large sample size (n = 667) — their effect sizes (r*² < 0.055) "
    "are small and should be interpreted cautiously.", body_style))

story.append(PageBreak())

story.append(Paragraph("4. Raw Canonical Coefficients", h1_style))
story.append(hr())
story.append(Paragraph(
    "Raw canonical coefficients define the linear combinations of original variables that "
    "form the canonical variates. For the X set: U\u1d4f = a\u2081X\u2081 + a\u2082X\u2082 + … + a\u2087X\u2087. "
    "These coefficients are sensitive to the original scales and should be interpreted "
    "alongside the canonical structure coefficients.", body_style))

story.append(Paragraph("4.1 X Set (Ethnocentric Tendency Indicators)", h2_style))
hdr_x = ["Variable"] + [f"U{k+1}" for k in range(num_can)]
raw_x_data = [hdr_x]
for i, v in enumerate(varX):
    raw_x_data.append([v] + [f"{raw_a[i,k]:.4f}" for k in range(num_can)])
story.append(section_table(raw_x_data,
    [0.6*inch] + [1.0*inch]*num_can))
story.append(Spacer(1, 6))

story.append(Paragraph(
    "For the first canonical variate U\u2081, all X coefficients are negative, indicating that "
    "higher ethnocentric tendencies on all seven indicators jointly move in the same direction "
    "along the first canonical dimension. X\u2087 and X\u2086 have the largest absolute coefficients "
    f"({raw_a[6,0]:.4f} and {raw_a[5,0]:.4f}), suggesting they contribute most to U\u2081.", body_style))

story.append(Paragraph("4.2 Y Set (Attitudinal Measures)", h2_style))
hdr_y = ["Variable"] + [f"V{k+1}" for k in range(num_can)]
raw_y_data = [hdr_y]
for j, v in enumerate(varY):
    raw_y_data.append([v] + [f"{raw_b[j,k]:.4f}" for k in range(num_can)])
story.append(section_table(raw_y_data,
    [0.6*inch] + [1.0*inch]*num_can))
story.append(Spacer(1, 6))

story.append(Paragraph(
    "For V\u2081, all Y coefficients are also negative, consistent with the direction of U\u2081. "
    f"Y\u2084 has the largest absolute coefficient ({raw_b[3,0]:.4f}), followed by Y\u2082 "
    f"({raw_b[1,0]:.4f}), indicating these attitudinal measures are most strongly weighted "
    "in the first canonical dimension.", body_style))

story.append(Paragraph("5. Canonical Structure Coefficients", h1_style))
story.append(hr())
story.append(Paragraph(
    "Canonical structure coefficients (also called canonical loadings) are the correlations "
    "between the original variables and the canonical variates. They are more interpretable "
    "than raw coefficients because they are scale-free. Variables with |loading| > 0.30 "
    "are considered meaningful contributors to a canonical dimension.", body_style))

story.append(Paragraph("5.1 X Variables with Canonical Variates U\u2081–U\u2085", h2_style))
hdr_sx = ["Variable"] + [f"U{k+1}" for k in range(num_can)]
struct_x_data = [hdr_sx]
for i, v in enumerate(varX):
    row = [v]
    for k in range(num_can):
        val = sX[i, k]
        cell = f"{val:.4f}"
        row.append(cell)
    struct_x_data.append(row)
story.append(section_table(struct_x_data,
    [0.6*inch] + [1.0*inch]*num_can))
story.append(Spacer(1, 4))

story.append(Paragraph(
    "All seven X variables load strongly and in the same direction on U\u2081, confirming that "
    "the first canonical variate captures a general ethnocentric tendency factor. X\u2087 "
    f"(loading = {sX[6,0]:.4f}) and X\u2086 ({sX[5,0]:.4f}) are the strongest contributors. "
    "This means that consumers high on all seven CET indicators form a coherent attitudinal "
    "profile captured by U\u2081.", body_style))

story.append(Paragraph("5.2 Y Variables with Canonical Variates V\u2081–V\u2085", h2_style))
hdr_sy = ["Variable"] + [f"V{k+1}" for k in range(num_can)]
struct_y_data = [hdr_sy]
for j, v in enumerate(varY):
    row = [v]
    for k in range(num_can):
        val = sY[j, k]
        row.append(f"{val:.4f}")
    struct_y_data.append(row)
story.append(section_table(struct_y_data,
    [0.6*inch] + [1.0*inch]*num_can))
story.append(Spacer(1, 4))

story.append(Paragraph(
    "All five Y variables load strongly on V\u2081. Y\u2084 and Y\u2082 show the highest loadings, "
    "indicating that these two attitudinal measures are most strongly associated with the "
    "dominant CET dimension. V\u2081 represents a broad negative attitude toward imported "
    "products — consumers high on CET (high U\u2081) are most negative toward imports (high V\u2081 "
    "in the negative direction as defined by the sign of the coefficients).", body_style))

story.append(PageBreak())

story.append(Paragraph("6. Structural Model and Overall Interpretation", h1_style))
story.append(hr())

story.append(Paragraph("6.1 Structural Model Diagram", h2_style))
story.append(Paragraph(
    "The structural model proposed by the study is:", body_style))

model_data = [
    ["CET Indicators (X\u2081–X\u2087)", "→", "Attitudinal Measures (Y\u2081–Y\u2085)"],
    ["Ethnocentric tendency", "", "Attitudes toward importing products"],
    ["General CET factor (U\u2081)", "r* = 0.7597", "General attitude factor (V\u2081)"],
]
model_style = TableStyle([
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,0), (-1,-1), 9),
    ('FONTNAME', (0,2), (2,2), 'Helvetica-Bold'),
    ('TEXTCOLOR', (1,2), (1,2), colors.HexColor('#c0392b')),
    ('FONTSIZE', (0,2), (2,2), 10),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('BOX', (0,2), (2,2), 1.0, colors.HexColor('#1a3a5c')),
    ('BACKGROUND', (0,2), (0,2), colors.HexColor('#e8f0f7')),
    ('BACKGROUND', (2,2), (2,2), colors.HexColor('#e8f0f7')),
])
story.append(Table(model_data,
    colWidths=[2.2*inch, 1.5*inch, 2.2*inch],
    style=model_style))
story.append(Spacer(1, 8))

story.append(Paragraph("6.2 Summary of Findings", h2_style))

findings = [
    ("<b>1. Strong primary association:</b>",
     f"The first canonical correlation r*\u2081 = {rc[0]:.4f} (r*\u2081² = {rc[0]**2:.4f}) "
     "is statistically significant (p < 0.001) and practically meaningful. This means that "
     f"{rc[0]**2*100:.1f}% of the variance in the dominant attitude canonical variate is "
     "explained by the dominant CET canonical variate. CET strongly affects attitudes "
     "toward importing products."),
    ("<b>2. Four significant dimensions:</b>",
     "Four of the five canonical variate pairs are statistically significant (p < 0.05). "
     "However, only the first pair has a practically meaningful effect size. Pairs 2–4 "
     f"have r*² values below 0.055, which are small effects detectable only due to the "
     "large sample size (n = 667)."),
    ("<b>3. General CET factor dominates:</b>",
     "All seven X indicators load in the same direction on U\u2081, forming a general "
     "ethnocentric tendency construct. Similarly, all five Y indicators load consistently "
     "on V\u2081. This confirms that CET operates as a unified psychological disposition "
     "that uniformly affects consumer attitudes toward imports."),
    ("<b>4. Fifth canonical dimension not significant:</b>",
     f"Root 5 (r*\u2085 = {rc[4]:.4f}) is not significant (p = {p_vals[4]:.4f}). "
     "The fifth canonical variate pair should be dropped from interpretation as it "
     "represents noise rather than a real dimension of association."),
    ("<b>5. Practical conclusion:</b>",
     "Consumers with stronger ethnocentric tendencies (higher X\u2081–X\u2087 scores) "
     "hold more negative attitudes toward imported products (Y\u2081–Y\u2085). The "
     "structural model CET → Attitudes is confirmed and statistically robust with n = 667."),
]
for title, text in findings:
    story.append(Paragraph(title, body_style))
    story.append(Paragraph(text, ParagraphStyle('ind', parent=body_style,
        leftIndent=12, spaceAfter=6)))

story.append(Paragraph("7. SAS and Python Implementation Notes", h1_style))
story.append(hr())
story.append(Paragraph(
    "Two code files accompany this report:", body_style))
story.append(Paragraph(
    "<b>cetnew_cca.sas</b> — Uses PROC IML to manually construct the covariance matrix "
    "and compute canonical correlations via eigenvalue decomposition, followed by PROC CANCORR "
    "with a TYPE=COV input dataset. PROC CANCORR provides standardized coefficients, "
    "canonical structure, and redundancy indices automatically.", body_style))
story.append(Paragraph(
    "<b>cetnew_cca.py</b> — Uses NumPy and SciPy for all matrix operations. The covariance "
    "matrix is constructed from the lower triangular CETNEW.DAT values, submatrices S_XX, "
    "S_YY, S_XY are extracted, and canonical correlations are obtained as the square roots "
    "of the eigenvalues of S_XX^{-1/2} S_XY S_YY^{-1} S_YX S_XX^{-1/2}. Wilks' Lambda "
    "and chi-square tests are computed using the Bartlett approximation with "
    f"multiplier t = n − 1 − (p+q+1)/2 = {n - 1 - (p + q + 1)/2:.1f}.", body_style))

story.append(Spacer(1, 8))
story.append(hr())
story.append(Paragraph(
    "Report prepared for: Applied Multivariate Data Analysis | Lana Gidan | "
    "Binghamton University | Question 14.4 — CETNEW Data",
    ParagraphStyle('footer', parent=styles['Normal'],
        fontSize=7.5, alignment=TA_CENTER, textColor=colors.grey)))

doc.build(story)
print("PDF saved: cetnew_cca_results.pdf")

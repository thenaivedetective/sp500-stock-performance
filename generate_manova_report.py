"""
Generate PDF report for Dataset 1 — Two-Way MANOVA (standard, no covariate).
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                  TableStyle, Image, HRFlowable)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import os

W = letter[0] - 1.7 * inch

def make_doc(path):
    doc = SimpleDocTemplate(path, pagesize=letter,
                            leftMargin=0.85*inch, rightMargin=0.85*inch,
                            topMargin=0.85*inch, bottomMargin=0.85*inch)
    SS = getSampleStyleSheet()
    def add(name, **kw):
        if name not in SS:
            SS.add(ParagraphStyle(name, **kw))
    add('CTitle',    parent=SS['Title'],  fontSize=17,
        textColor=colors.HexColor('#1a3a5c'), spaceAfter=4, alignment=TA_CENTER)
    add('CSubtitle', parent=SS['Normal'], fontSize=10.5, fontName='Helvetica-Oblique',
        textColor=colors.HexColor('#2c5f8a'), spaceAfter=10, alignment=TA_CENTER)
    add('SHead',     parent=SS['Normal'], fontSize=11, fontName='Helvetica-Bold',
        textColor=colors.white, backColor=colors.HexColor('#1a3a5c'),
        spaceBefore=12, spaceAfter=5, leftIndent=-6, borderPad=5)
    add('RQ',        parent=SS['Normal'], fontSize=10, fontName='Helvetica-Bold',
        textColor=colors.HexColor('#0a2740'), backColor=colors.HexColor('#dceefb'),
        borderColor=colors.HexColor('#2c5f8a'), borderWidth=1,
        borderPad=8, spaceAfter=8, spaceBefore=4, leading=15)
    add('Body',      parent=SS['Normal'], fontSize=9.5, spaceAfter=4,
        leading=14, alignment=TA_JUSTIFY)
    add('Bul',       parent=SS['Normal'], fontSize=9.5, spaceAfter=3,
        leftIndent=14, leading=13)
    add('Sub',       parent=SS['Normal'], fontSize=9.5, fontName='Helvetica-Bold',
        spaceAfter=3, spaceBefore=6, textColor=colors.HexColor('#1a3a5c'))
    add('Note',      parent=SS['Normal'], fontSize=8.5, fontName='Helvetica-Oblique',
        textColor=colors.HexColor('#555555'), spaceAfter=4, leading=12)
    return doc, SS

def hbar(SS, txt):
    return [Paragraph(f'  {txt}', SS['SHead']), Spacer(1, 3)]

def rq_box(SS, txt):
    return [Paragraph(f'Research Question:  {txt}', SS['RQ']), Spacer(1, 4)]

def tbl(data, widths, hdr=colors.HexColor('#1a3a5c')):
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,0),  hdr),
        ('TEXTCOLOR',     (0,0),(-1,0),  colors.white),
        ('FONTNAME',      (0,0),(-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0,0),(-1,0),  9),
        ('FONTSIZE',      (0,1),(-1,-1), 8.5),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [colors.white, colors.HexColor('#eef3f8')]),
        ('GRID',          (0,0),(-1,-1), 0.4, colors.HexColor('#bbbbbb')),
        ('ALIGN',         (0,0),(-1,-1), 'CENTER'),
        ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0),(-1,-1), 3),
        ('BOTTOMPADDING', (0,0),(-1,-1), 3),
        ('LEFTPADDING',   (0,0),(-1,-1), 5),
    ]))
    return [t, Spacer(1, 6)]

def img(path, w=None, h=None):
    if not os.path.exists(path):
        return []
    w = w or W
    h = h or w * 0.42
    return [Image(path, width=w, height=h), Spacer(1, 5)]

def report_ds1_manova():
    folder = 'Lana_Gidan_Software_Exam/Dataset1_MANCOVA'
    path = f'{folder}/dataset1_MANOVA_twoway_report.pdf'
    doc, SS = make_doc(path)
    s = []

    s.append(Paragraph('Dataset 1: Two-Way MANOVA', SS['CTitle']))
    s.append(Paragraph(
        'Health, Exercise Level &amp; Smoking Status Study  |  n = 240',
        SS['CSubtitle']))
    s.append(HRFlowable(width='100%', thickness=2, color=colors.HexColor('#1a3a5c')))
    s.append(Spacer(1, 8))

    # ── 1. Research Question ──────────────────────────────────────────────────
    s += hbar(SS, '1. Research Question')
    s += rq_box(SS,
        'Do exercise participation level (Low / Moderate / High) and smoking status '
        '(Smoker / Non-Smoker) independently and jointly affect three health outcomes '
        '— cardiovascular fitness, mental health, and energy level — when assessed '
        'simultaneously in a multivariate framework?')

    # ── 2. Variables ──────────────────────────────────────────────────────────
    s += hbar(SS, '2. Variables')
    s += tbl([
        ['Role',           'Variable',       'Type / Levels',          'Description'],
        ['IV — Factor 1',  'Exercise_Level', 'Categorical — 3 levels', 'Low / Moderate / High'],
        ['IV — Factor 2',  'Smoking_Status', 'Categorical — 2 levels', 'Smoker / Non-Smoker'],
        ['DV 1',           'Cardio_Fitness', 'Continuous',             'Cardiovascular fitness score  (M=57.0, SD=12.6)'],
        ['DV 2',           'Mental_Health',  'Continuous',             'Mental wellbeing score  (M=64.5, SD=10.6)'],
        ['DV 3',           'Energy_Level',   'Continuous',             'Energy level score  (M=58.1, SD=13.0)'],
    ], [1.0*inch, 1.2*inch, 1.5*inch, 3.0*inch])

    # ── 3. Methodology ────────────────────────────────────────────────────────
    s += hbar(SS, '3. Methodology — Two-Way MANOVA')
    s.append(Paragraph(
        'Multivariate Analysis of Variance (MANOVA) is chosen because there are three '
        'continuous dependent variables measured on the same participants, and the DVs '
        'are expected to be correlated. Analyzing each DV separately with three '
        'independent ANOVAs would inflate Type I error and ignore the multivariate '
        'nature of health outcomes. Two-Way MANOVA tests the joint effect of both '
        'independent variables (Exercise_Level and Smoking_Status) and their '
        'interaction on the full DV vector simultaneously. '
        'Four multivariate test statistics are reported: Wilks\' Lambda, Pillai\'s '
        'Trace, Hotelling-Lawley Trace, and Roy\'s Greatest Root. '
        'Wilks\' Lambda is emphasized as the primary criterion (most widely used). '
        'Statistically significant omnibus effects are followed up with univariate '
        'ANOVAs (Type II SS) and Tukey HSD post-hoc comparisons for Exercise_Level '
        '(3 levels). Partial η² quantifies effect size per DV. '
        'The design is fully balanced (40 participants per cell, 6 cells).', SS['Body']))

    # ── 4. Descriptive Statistics ─────────────────────────────────────────────
    s += hbar(SS, '4. Descriptive Statistics — Cell Means')
    s += tbl([
        ['Exercise Level', 'Smoking Status', 'Cardio Fitness', 'Mental Health', 'Energy Level'],
        ['Low',      'Non-Smoker', '47.31', '54.72', '46.66'],
        ['Low',      'Smoker',     '40.18', '50.02', '41.23'],
        ['Moderate', 'Non-Smoker', '62.15', '70.17', '61.59'],
        ['Moderate', 'Smoker',     '53.36', '64.88', '55.28'],
        ['High',     'Non-Smoker', '73.15', '75.24', '75.14'],
        ['High',     'Smoker',     '66.08', '71.74', '68.68'],
    ], [1.1*inch, 1.1*inch, 1.2*inch, 1.2*inch, 1.1*inch])
    s.append(Paragraph(
        'Cell sizes are perfectly balanced: n = 40 per cell (6 cells × 40 = 240). '
        'The pattern is consistent across all three DVs: higher exercise level → '
        'higher scores; non-smokers consistently outperform smokers within each '
        'exercise group. No clear crossing of lines suggests no meaningful interaction.',
        SS['Note']))

    # ── 5. MANOVA Omnibus ─────────────────────────────────────────────────────
    s += hbar(SS, '5. Two-Way MANOVA — Omnibus Results')
    s += tbl([
        ['Effect',             "Wilks' λ", 'Pillai\'s Trace', 'F',       'Num df', 'Den df', 'p-value',  'Verdict'],
        ['Exercise_Level',     '0.2371',   '0.8360',          '81.48',   '6',      '464',    '< 0.001',  '✓ Significant'],
        ['Smoking_Status',     '0.8688',   '0.1312',          '11.68',   '3',      '232',    '< 0.001',  '✓ Significant'],
        ['Exercise × Smoking', '0.9863',   '0.0137',          '0.53',    '6',      '464',    '0.783',    '✗ Not significant'],
    ], [1.3*inch, 0.65*inch, 0.85*inch, 0.6*inch, 0.55*inch, 0.55*inch, 0.75*inch, 1.1*inch])
    s.append(Paragraph(
        '<b>Interpretation:</b> Both main effects are significant. '
        'Exercise_Level produces a very large multivariate effect '
        '(Wilks\' λ = 0.237, F(6,464) = 81.48, p &lt; 0.001; η²_m = 0.763). '
        'Smoking_Status produces a medium effect '
        '(Wilks\' λ = 0.869, F(3,232) = 11.68, p &lt; 0.001; η²_m = 0.131). '
        'The interaction is not significant '
        '(Wilks\' λ = 0.986, F(6,464) = 0.53, p = 0.783), meaning the effect '
        'of exercise on health outcomes is consistent regardless of smoking status. '
        'All four test statistics agree — the results are robust.', SS['Body']))

    # ── 6. Univariate ANOVAs ──────────────────────────────────────────────────
    s += hbar(SS, '6. Univariate Follow-Up ANOVAs (Type II SS)')
    s += tbl([
        ['DV',             'F (Exercise)',  'η² (Exercise)',  'F (Smoking)',  'η² (Smoking)', 'Interaction p'],
        ['Cardio_Fitness', '423.93***',    '0.710 (large)',  '111.31***',   '0.093 (med.)', 'p = 0.549 n.s.'],
        ['Mental_Health',  '346.73***',    '0.713 (large)',  '44.38***',    '0.046 (small)','p = 0.550 n.s.'],
        ['Energy_Level',   '532.25***',    '0.775 (large)',  '75.03***',    '0.055 (small)','p = 0.813 n.s.'],
    ], [1.15*inch, 0.95*inch, 1.1*inch, 0.9*inch, 1.1*inch, 1.15*inch])
    s.append(Paragraph(
        '*** p &lt; 0.001.  Partial η² benchmarks (Cohen, 1988): '
        'small = 0.01, medium = 0.06, large = 0.14. '
        'Exercise_Level explains 71–78% of variance in each DV — an exceptionally '
        'large effect. Smoking_Status has a medium effect on Cardio_Fitness '
        '(η² = 0.093) and smaller but significant effects on Mental Health and '
        'Energy Level. No interaction term reaches significance for any DV.',
        SS['Note']))

    # ── 7. Post-Hoc Tukey ─────────────────────────────────────────────────────
    s += hbar(SS, '7. Post-Hoc Tukey HSD — Exercise Level Pairwise Comparisons')
    s += tbl([
        ['DV',            'Comparison',         'Mean Diff.',  'p-value',  'Significant?'],
        ['Cardio_Fitness','High vs Low',          '+25.87',    '< 0.001',  'Yes ✓'],
        ['Cardio_Fitness','High vs Moderate',     '+11.86',    '< 0.001',  'Yes ✓'],
        ['Cardio_Fitness','Moderate vs Low',      '+14.01',    '< 0.001',  'Yes ✓'],
        ['Mental_Health', 'High vs Low',          '+21.12',    '< 0.001',  'Yes ✓'],
        ['Mental_Health', 'High vs Moderate',      '+5.97',    '< 0.001',  'Yes ✓'],
        ['Mental_Health', 'Moderate vs Low',      '+15.16',    '< 0.001',  'Yes ✓'],
        ['Energy_Level',  'High vs Low',          '+27.96',    '< 0.001',  'Yes ✓'],
        ['Energy_Level',  'High vs Moderate',     '+13.48',    '< 0.001',  'Yes ✓'],
        ['Energy_Level',  'Moderate vs Low',      '+14.49',    '< 0.001',  'Yes ✓'],
    ], [1.1*inch, 1.35*inch, 0.85*inch, 0.8*inch, 0.85*inch])
    s.append(Paragraph(
        'All 9 pairwise comparisons are statistically significant (all p &lt; 0.001, '
        'family-wise error rate controlled). The ordering is perfectly monotonic: '
        'High &gt; Moderate &gt; Low for every DV. '
        'The Tukey HSD test is appropriate because of the balanced design (equal n per group) '
        'and controls experiment-wise Type I error at α = 0.05.', SS['Body']))

    # ── 8. Smoking Status ─────────────────────────────────────────────────────
    s += hbar(SS, '8. Smoking Status — Mean Differences')
    s += tbl([
        ['DV',            'Non-Smoker M', 'Smoker M', 'Difference', 't',       'p-value',  'Sig?'],
        ['Cardio_Fitness','60.87',        '53.20',    '+7.67',      't=10.55', '< 0.001',  'Yes ✓'],
        ['Mental_Health', '66.71',        '62.21',    '+4.51',      't=6.66',  '< 0.001',  'Yes ✓'],
        ['Energy_Level',  '61.13',        '55.06',    '+6.06',      't=8.66',  '< 0.001',  'Yes ✓'],
    ], [1.15*inch, 0.95*inch, 0.75*inch, 0.85*inch, 0.75*inch, 0.75*inch, 0.7*inch])
    s.append(Paragraph(
        'Non-smokers score significantly higher than smokers on all three health outcomes '
        '(Bonferroni-corrected α = 0.017). The largest gap is in Cardio_Fitness '
        '(7.67 points), followed by Energy_Level (6.06 points) and Mental_Health '
        '(4.51 points). These differences are consistent across all exercise levels '
        '(no interaction), meaning smoking is independently harmful to health '
        'regardless of how much someone exercises.', SS['Body']))

    # ── 9. Assumption Checks ──────────────────────────────────────────────────
    s += hbar(SS, '9. Assumption Checks — All Passed')
    s += tbl([
        ['Test',                                        'Result',                           'Verdict'],
        ['Multivariate normality (Mardia skewness)',    'χ²(10) = 14.66, p = 0.145',        '✓ MVN assumption met'],
        ['Shapiro-Wilk — Cardio_Fitness residuals',     'W = 0.9971, p = 0.940',            '✓ Normal'],
        ['Shapiro-Wilk — Mental_Health residuals',      'W = 0.9955, p = 0.706',            '✓ Normal'],
        ['Shapiro-Wilk — Energy_Level residuals',       'W = 0.9938, p = 0.423',            '✓ Normal'],
        ['Levene (Cardio_Fitness, by Exercise)',         'W = 1.032, p = 0.358',             '✓ Homogeneous variances'],
        ['Levene (Mental_Health, by Exercise)',          'W = 0.602, p = 0.549',             '✓ Homogeneous variances'],
        ['Levene (Energy_Level, by Exercise)',           'W = 0.691, p = 0.502',             '✓ Homogeneous variances'],
        ['Cell size balance',                           'n = 40 per cell (6 cells)',         '✓ Perfectly balanced design'],
    ], [2.35*inch, 2.0*inch, 2.3*inch])
    s.append(Paragraph(
        'All MANOVA assumptions are fully satisfied. '
        'The balanced design (equal n per cell) makes MANOVA robust and '
        'ensures Type II SS for the ANOVA table is appropriate. '
        'The perfectly normal residuals and homogeneous variances strengthen '
        'confidence in all inferential results.', SS['Body']))

    # ── 10. Effect Size Summary ───────────────────────────────────────────────
    s += hbar(SS, '10. Multivariate Effect Size Summary')
    s += tbl([
        ['Effect',          "Wilks' λ", 'η²_m = 1 − λ', 'Benchmark',    'Interpretation'],
        ['Exercise_Level',  '0.2371',   '0.763',         'Large > 0.14', 'Very large — dominant predictor'],
        ['Smoking_Status',  '0.8688',   '0.131',         'Medium ≈ 0.06','Medium — clinically meaningful'],
        ['Interaction',     '0.9863',   '0.014',         'Small < 0.06', 'Negligible — effects are additive'],
    ], [1.2*inch, 0.8*inch, 0.95*inch, 1.15*inch, 2.55*inch])

    # ── 11. Figures ───────────────────────────────────────────────────────────
    s += hbar(SS, '11. Figures')
    s += img(f'{folder}/dataset1_MANOVA_group_means.png')
    s += img(f'{folder}/dataset1_MANOVA_interaction.png')
    s += img(f'{folder}/dataset1_MANOVA_boxplots.png')

    # ── 12. Conclusions ───────────────────────────────────────────────────────
    s += hbar(SS, '12. Conclusions')
    for pt in [
        '<b>Research question answered — YES.</b> Both Exercise_Level and Smoking_Status '
        'significantly affect all three health outcomes simultaneously. '
        'The two-way MANOVA is globally significant for both main effects (p &lt; 0.001). '
        'The interaction is not significant (p = 0.783), confirming the two factors '
        'act independently and additively.',

        '<b>Exercise Level is the dominant predictor</b> (Wilks\' λ = 0.237, '
        'η²_m = 0.763 — very large effect). Every step up in exercise level '
        'produces a significant improvement in all three DVs. Tukey HSD confirms '
        'all three pairwise comparisons are significant (all p &lt; 0.001): '
        'High &gt; Moderate &gt; Low. For Cardio_Fitness, High exercisers '
        'score 25.9 points above Low exercisers; for Energy_Level, the gap is 28.0 points.',

        '<b>Smoking Status has an independent, significant negative effect</b> '
        '(Wilks\' λ = 0.869, η²_m = 0.131 — medium effect). Smokers score '
        '7.7 points lower in cardiovascular fitness, 4.5 points lower in mental '
        'health, and 6.1 points lower in energy level, independent of exercise level.',

        '<b>No interaction effect (p = 0.783):</b> The benefit of exercise is '
        'equally strong for both smokers and non-smokers. The lines in the '
        'interaction plots are nearly parallel across all three DVs, '
        'confirming a purely additive relationship.',

        '<b>All MANOVA assumptions are fully satisfied:</b> multivariate normality '
        '(Mardia χ² p = 0.145), univariate normality (all Shapiro-Wilk p &gt; 0.42), '
        'homogeneity of variances (all Levene p &gt; 0.35), and a perfectly balanced '
        'design (n = 40 per cell). These results are reliable and valid for inference.'
    ]:
        s.append(Paragraph(f'• {pt}', SS['Bul']))
        s.append(Spacer(1, 3))

    doc.build(s)
    print(f'Saved: {path}')


if __name__ == '__main__':
    report_ds1_manova()

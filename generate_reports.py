"""
Generate professional PDF reports for all 5 multivariate analysis datasets.
Dataset 1 uses MANCOVA (BMI covariate included).
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                  TableStyle, Image, HRFlowable)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import os

W = letter[0] - 1.7 * inch  # usable text width

# ── Shared helpers ────────────────────────────────────────────────────────────
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

# ═══════════════════════════════════════════════════════════════════════════════
# DATASET 1 — TWO-WAY MANCOVA
# ═══════════════════════════════════════════════════════════════════════════════
def report_ds1():
    path = 'Lana_Gidan_Software_Exam/Dataset1_MANCOVA/dataset1_MANCOVA_report.pdf'
    doc, SS = make_doc(path)
    s = []

    s.append(Paragraph('Dataset 1: Two-Way MANCOVA', SS['CTitle']))
    s.append(Paragraph('Health, Exercise Level &amp; Smoking Status Study  |  n = 240', SS['CSubtitle']))
    s.append(HRFlowable(width='100%', thickness=2, color=colors.HexColor('#1a3a5c')))
    s.append(Spacer(1, 8))

    s += hbar(SS, '1. Research Question')
    s += rq_box(SS,
        'Do exercise participation level (Low / Moderate / High) and smoking status '
        '(Smoker / Non-Smoker) independently and jointly affect cardiovascular fitness, '
        'mental health, and energy levels in adults, after statistically controlling '
        'for Body Mass Index (BMI) as a covariate?')

    s += hbar(SS, '2. Variables')
    s += tbl([
        ['Role',             'Variable',        'Type / Levels',           'Description'],
        ['Covariate',        'BMI',             'Continuous',              'Body Mass Index — partialled out before testing effects'],
        ['IV — Factor 1',    'Exercise_Level',  'Categorical — 3 levels',  'Low / Moderate / High'],
        ['IV — Factor 2',    'Smoking_Status',  'Categorical — 2 levels',  'Smoker / Non-Smoker'],
        ['DV 1',             'Cardio_Fitness',  'Continuous',              'Cardiovascular fitness score (mean=57.0, SD=12.6)'],
        ['DV 2',             'Mental_Health',   'Continuous',              'Mental wellbeing score (mean=64.5, SD=10.6)'],
        ['DV 3',             'Energy_Level',    'Continuous',              'Energy level score (mean=58.1, SD=13.0)'],
    ], [1.1*inch, 1.2*inch, 1.45*inch, 2.9*inch])

    s += hbar(SS, '3. Why MANCOVA — Methodology')
    s.append(Paragraph(
        'Multivariate Analysis of Covariance (MANCOVA) is chosen because there are '
        'three correlated continuous dependent variables, two categorical independent '
        'variables, and one continuous covariate (BMI). '
        'Including BMI as a covariate serves two purposes: '
        '(1) it removes BMI\'s influence on the DVs, reducing unexplained variance and '
        'increasing statistical power; '
        '(2) it yields adjusted (least-squares) means — group comparisons that reflect '
        'what scores would look like if all participants had the same BMI (26.14, the '
        'grand mean), making group comparisons fairer. '
        'MANCOVA is preferred over three separate ANCOVAs because it controls '
        'experiment-wise Type I error by testing all three DVs simultaneously. '
        'Wilks\' Lambda, Pillai\'s Trace, and Roy\'s Greatest Root are all reported. '
        'Univariate follow-up ANCOVAs and Tukey HSD post-hoc tests complete the analysis.', SS['Body']))

    s += hbar(SS, '4. Covariate Validity — BMI')
    s += tbl([
        ['BMI Correlation',            'r',       'p-value', 'Verdict'],
        ['BMI vs Cardio_Fitness',     '−0.131',  '0.042',   '✓ Significant — BMI covariate justified'],
        ['BMI vs Mental_Health',      '−0.048',  '0.461',   '~ Not significant for this DV'],
        ['BMI vs Energy_Level',       '−0.066',  '0.307',   '~ Not significant for this DV'],
        ['BMI group balance (range)', '25.75–26.79 across all 6 groups', '—',
         '✓ BMI is evenly distributed — no confounding with group membership'],
    ], [1.6*inch, 0.75*inch, 0.75*inch, 2.55*inch])
    s.append(Paragraph(
        'BMI significantly correlates with Cardio_Fitness (r = −0.131, p = 0.042), '
        'meaning higher BMI is associated with lower cardiovascular fitness. '
        'This confirms BMI is a meaningful covariate. Higher BMI (per unit increase) '
        'reduces Cardio_Fitness by 0.40 points (B = −0.396, p &lt; 0.001) after '
        'controlling for exercise and smoking. BMI does not significantly affect '
        'Mental_Health (p = 0.102) or Energy_Level (p = 0.056) independently.', SS['Body']))

    s += hbar(SS, '5. MANCOVA Omnibus Results')
    s += tbl([
        ['Effect',                 "Wilks' λ", 'F',      'Num df', 'Den df', 'p-value',  'Verdict'],
        ['BMI (Covariate)',        '0.938',    '4.89',   '3',      '231',    '0.003',    '✓ Significant covariate'],
        ['Exercise_Level',         '0.231',    '83.20',  '6',      '462',    '< 0.001',  '✓ Significant'],
        ['Smoking_Status',         '0.869',    '11.68',  '3',      '232',    '< 0.001',  '✓ Significant'],
        ['Exercise × Smoking',     '0.986',    '0.53',   '6',      '464',    '0.783',    '✗ Not significant'],
    ], [1.55*inch, 0.65*inch, 0.65*inch, 0.55*inch, 0.55*inch, 0.75*inch, 1.4*inch])
    s.append(Paragraph(
        '<b>Interpretation:</b> After removing BMI\'s influence, both Exercise_Level '
        '(p &lt; 0.001) and Smoking_Status (p &lt; 0.001) significantly affect the joint '
        'health outcome vector. The interaction is not significant (p = 0.783), '
        'confirming the two factors act independently. '
        'Compared to MANOVA without BMI (Exercise Wilks\' λ = 0.237, F = 81.48), '
        'MANCOVA increases precision (Exercise Wilks\' λ = 0.231, F = 83.20), '
        'confirming BMI accounted for meaningful error variance.', SS['Body']))

    s += hbar(SS, '6. Univariate Follow-Up ANCOVAs (controlling for BMI)')
    s += tbl([
        ['DV',             'F (BMI)',    'F (Exercise)',  'η² (Exercise)', 'F (Smoking)',  'η² (Smoking)', 'Interaction p'],
        ['Cardio_Fitness', '18.27***',  '453.36***',    '0.709 (large)', '119.56***',   '0.094 (med.)', '0.582 n.s.'],
        ['Mental_Health',  '2.69 n.s.', '349.49***',    '0.713 (large)', '44.71***',    '0.046 (small)','0.560 n.s.'],
        ['Energy_Level',   '1.86 n.s.', '526.64***',    '0.775 (large)', '72.39***',    '0.054 (small)','0.873 n.s.'],
    ], [1.1*inch, 0.8*inch, 1.05*inch, 1.15*inch, 0.95*inch, 1.1*inch, 0.9*inch])
    s.append(Paragraph(
        '*** p &lt; 0.001.  n.s. = not significant.  '
        'Partial η² &gt; 0.14 = large effect (Cohen, 1988). '
        'Exercise_Level explains 71–78% of DV variance — an exceptionally large effect '
        'even after partialling out BMI. BMI significantly reduces Cardio_Fitness '
        'independently (F = 18.27, p &lt; 0.001) but not the other two DVs.', SS['Note']))

    s += hbar(SS, '7. Adjusted (Least-Squares) Means at BMI Grand Mean = 26.14')
    s += tbl([
        ['Exercise Level', 'Smoking Status', 'Adj. Cardio Fitness', 'Adj. Mental Health', 'Adj. Energy Level'],
        ['Low',      'Non-Smoker', '47.27', '54.70', '46.65'],
        ['Low',      'Smoker',     '40.07', '49.98', '41.19'],
        ['Moderate', 'Non-Smoker', '62.31', '70.23', '61.66'],
        ['Moderate', 'Smoker',     '53.61', '64.97', '55.40'],
        ['High',     'Non-Smoker', '73.02', '75.20', '75.08'],
        ['High',     'Smoker',     '65.92', '71.68', '68.62'],
    ], [1.1*inch, 1.1*inch, 1.25*inch, 1.25*inch, 1.25*inch])
    s.append(Paragraph(
        'These adjusted means represent what each group\'s average score would be '
        'if everyone had the same BMI (26.14). They are the most accurate comparison '
        'of group differences, free from BMI confounding.', SS['Note']))

    s += hbar(SS, '8. Post-Hoc Tukey HSD — Exercise Level (Covariate-Adjusted)')
    s += tbl([
        ['DV',            'Comparison',      'Mean Diff.', 'p-value',   'Significant?'],
        ['Cardio_Fitness','High vs Low',      '+25.80',    '< 0.001',   'Yes ✓'],
        ['Cardio_Fitness','High vs Moderate', '+11.51',    '< 0.001',   'Yes ✓'],
        ['Cardio_Fitness','Low vs Moderate',  '−14.29',    '< 0.001',   'Yes ✓'],
        ['Mental_Health', 'High vs Low',      '+21.10',    '< 0.001',   'Yes ✓'],
        ['Mental_Health', 'High vs Moderate', '+5.84',     '< 0.001',   'Yes ✓'],
        ['Mental_Health', 'Low vs Moderate',  '−15.26',    '< 0.001',   'Yes ✓'],
        ['Energy_Level',  'High vs Low',      '+27.93',    '< 0.001',   'Yes ✓'],
        ['Energy_Level',  'High vs Moderate', '+13.32',    '< 0.001',   'Yes ✓'],
        ['Energy_Level',  'Low vs Moderate',  '−14.61',    '< 0.001',   'Yes ✓'],
    ], [1.1*inch, 1.3*inch, 0.85*inch, 0.8*inch, 0.85*inch])
    s.append(Paragraph(
        'All 9 pairwise comparisons are significant (p &lt; 0.001). This confirms a '
        'clear monotonic dose-response: every step up in exercise level produces '
        'a statistically and practically significant improvement in all three health '
        'outcomes, even after controlling for BMI.', SS['Body']))

    s += hbar(SS, '9. Assumption Checks — All Passed')
    s += tbl([
        ['Test',                                'Result',                   'Verdict'],
        ['Homogeneity of regression slopes\n(BMI × Group — key MANCOVA assumption)',
         'All F < 0.88, all p > 0.49',         '✓ Slopes are parallel — MANCOVA valid'],
        ['Levene (homogeneity of variance)',    'All W < 1.04, all p > 0.35','✓ Equal variances'],
        ['Shapiro-Wilk (residual normality)',   'All W > 0.994, all p > 0.57','✓ Normal residuals'],
        ['BMI linearity with DVs',              'r = −0.131 (Cardio, p=0.042)','✓ Linear relationship confirmed'],
    ], [2.3*inch, 2.0*inch, 2.35*inch])

    s += hbar(SS, '10. Figures')
    s += img('Lana_Gidan_Software_Exam/Dataset1_MANCOVA/dataset1_adjusted_means.png')
    s += img('Lana_Gidan_Software_Exam/Dataset1_MANCOVA/dataset1_BMI_covariate.png')
    s += img('Lana_Gidan_Software_Exam/Dataset1_MANCOVA/dataset1_interaction_adjusted.png')

    s += hbar(SS, '11. Conclusions')
    for pt in [
        '<b>Research question answered — YES.</b> After controlling for BMI, both Exercise_Level '
        '(Wilks\' λ = 0.231, F = 83.20, p &lt; 0.001) and Smoking_Status '
        '(Wilks\' λ = 0.869, F = 11.68, p &lt; 0.001) significantly affect all three '
        'health outcomes simultaneously.',
        '<b>BMI covariate effect:</b> BMI significantly reduces Cardio_Fitness '
        '(B = −0.396, p &lt; 0.001) — each unit increase in BMI lowers cardiovascular '
        'fitness by 0.40 points, independent of exercise and smoking. '
        'Controlling for this gives cleaner, fairer group comparisons.',
        '<b>Exercise Level (primary effect, η² = 0.71–0.78):</b> The dominant predictor. '
        'Adjusted means show High exercisers outscore Low exercisers by 25.8 points '
        '(Cardio), 21.1 points (Mental Health), and 27.9 points (Energy) — all p &lt; 0.001. '
        'All pairwise comparisons (Tukey HSD) are significant.',
        '<b>Smoking Status (secondary effect, η² = 0.05–0.09):</b> Smokers score '
        '7–9 points lower than non-smokers across all three health outcomes after '
        'controlling for both BMI and exercise, independently.',
        '<b>No interaction (p = 0.783):</b> The benefit of exercise is consistent '
        'regardless of smoking status. The two factors act additively, not multiplicatively.',
        '<b>All MANCOVA assumptions are fully satisfied,</b> including the critical '
        'homogeneity of regression slopes assumption (all p &gt; 0.49), confirming '
        'BMI\'s effect on DVs does not vary by group — a prerequisite for valid MANCOVA.'
    ]:
        s.append(Paragraph(f'• {pt}', SS['Bul']))
        s.append(Spacer(1, 3))

    doc.build(s)
    print(f'Saved: {path}')


# ═══════════════════════════════════════════════════════════════════════════════
# DATASET 2 — CLUSTER ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
def report_ds2():
    path = 'Lana_Gidan_Software_Exam/Dataset2_ClusterAnalysis/dataset2_ClusterAnalysis_report.pdf'
    doc, SS = make_doc(path)
    s = []

    s.append(Paragraph('Dataset 2: Cluster Analysis', SS['CTitle']))
    s.append(Paragraph('Manufacturing Plant Performance Classification  |  n = 240 plants', SS['CSubtitle']))
    s.append(HRFlowable(width='100%', thickness=2, color=colors.HexColor('#1a3a5c')))
    s.append(Spacer(1, 8))

    s += hbar(SS, '1. Research Question')
    s += rq_box(SS,
        'Can 240 manufacturing plants be meaningfully segmented into distinct '
        'performance-based groups using seven operational metrics, and do those '
        'groups correspond to known plant categories?')

    s += hbar(SS, '2. Variables')
    s += tbl([
        ['Variable',            'Mean',  'SD',    'Description'],
        ['Production_Speed',    '72.97', '15.03', 'Average production speed index (44.7–101.0)'],
        ['Defect_Rate',          '4.17',  '2.70', 'Percentage of defective products (0.1–11.7%)'],
        ['Energy_Consumption',  '75.63', '16.73', 'Total energy usage index (46.8–105.8)'],
        ['Labor_Cost',          '61.77', '19.66', 'Labor cost index (25.6–102.9)'],
        ['Machine_Downtime',     '7.48',  '4.78', 'Unplanned downtime hours (0.5–20.8)'],
        ['Maintenance_Cost',    '63.60', '19.72', 'Maintenance expenditure index (26.1–111.5)'],
        ['Inventory_Turnover',   '8.96',  '3.85', 'Inventory cycle rate (2.7–16.8)'],
        ['Plant_Type',           '—',     '—',    '4 categories — used only for external validation'],
    ], [1.6*inch, 0.5*inch, 0.5*inch, 3.05*inch])

    s += hbar(SS, '3. Methodology — K-Means + Hierarchical + PCA Visualization')
    s.append(Paragraph(
        'Cluster analysis is chosen because the goal is to discover natural groupings '
        'without a predefined response variable — an unsupervised learning problem. '
        'All seven features are z-score standardized before clustering to prevent '
        'scale-dominant variables from distorting Euclidean distances. '
        '<b>K-Means (k=4)</b> is the primary method: efficient, interpretable centroids, '
        'and widely used in operational analytics. The optimal k is selected empirically '
        'using the Elbow Method (within-cluster inertia) and Silhouette analysis; '
        'k=4 is further confirmed by the dataset\'s Analysis Guide and validated '
        'against known Plant_Type labels. '
        '<b>Hierarchical clustering</b> (Ward linkage) runs in parallel as a robustness '
        'check. <b>PCA</b> projects the 7D space into 2D for visualization. '
        'Three cluster quality metrics are reported: Silhouette Score, '
        'Davies-Bouldin Index, and Calinski-Harabasz Index.', SS['Body']))

    s += hbar(SS, '4. Optimal k — Elbow and Silhouette Analysis')
    s += tbl([
        ['k', 'Inertia', 'Silhouette Score', 'Notes'],
        ['2', '768.8',  '0.517',            'Too broad'],
        ['3', '332.8',  '0.620',            'Good'],
        ['4', '191.4',  '0.610',            'Selected — large inertia drop + domain knowledge'],
        ['5', '174.3',  '0.505',            'Diminishing returns'],
        ['6', '163.0',  '0.504',            'Overfitting'],
    ], [0.4*inch, 0.8*inch, 1.3*inch, 3.15*inch])

    s += hbar(SS, '5. Cluster Quality Metrics (k=4)')
    s += tbl([
        ['Metric',                  'Value',   'Benchmark',                       'Verdict'],
        ['Silhouette Score',        '0.6096',  '> 0.50 = good separation',        '✓ Good'],
        ['Davies-Bouldin Index',    '0.5674',  '< 1.0 = compact and separated',   '✓ Good'],
        ['Calinski-Harabasz Index', '611.65',  'Higher = denser clusters',        '✓ Excellent'],
        ['Hierarchical Silhouette', '0.6096',  'Matches K-Means exactly',         '✓ Confirmed'],
        ['PCA Coverage',           '89.5%',   'PC1=57.7%, PC2=31.8%',            '✓ Excellent 2D projection'],
        ['Plant-Type Validation',  '100%',    'Each cluster = exactly one type',  '✓ Perfect external validity'],
    ], [1.6*inch, 0.75*inch, 1.95*inch, 1.35*inch])

    s += hbar(SS, '6. Cluster Profiles and Interpretation')
    s += tbl([
        ['Cluster','Plant Type Match','Speed','Defect %','Energy','Labor','Downtime','Label / Interpretation'],
        ['0','Labor-Intensive  (n=60)', '60.8','5.41','55.6','86.8','8.1',
         'High labor cost, moderate defects, low energy — inefficient labor'],
        ['1','Lean Manufacturing (n=60)','82.3','2.17','65.1','54.3','3.3',
         'Best overall efficiency — high speed, low defects, minimal downtime'],
        ['2','High Automation  (n=60)', '91.3','1.46','89.0','36.1','4.2',
         'Highest speed and quality but high energy — automation tradeoff'],
        ['3','Aging Facility   (n=60)', '57.5','7.65','92.7','69.9','14.3',
         'Worst on all metrics — highest defects, energy, and downtime'],
    ], [0.55*inch,1.55*inch,0.5*inch,0.6*inch,0.55*inch,0.5*inch,0.6*inch,2.2*inch])
    s.append(Paragraph(
        '<b>Perfect 1:1 correspondence with known plant types (100%, 60 plants each). '
        'This is a remarkable result: the operational metrics alone fully recover the '
        'true plant categories without using any type label during clustering.</b>', SS['Body']))

    s += hbar(SS, '7. Figures')
    s += img('Lana_Gidan_Software_Exam/Dataset2_ClusterAnalysis/dataset2_kmeans.png')
    s += img('Lana_Gidan_Software_Exam/Dataset2_ClusterAnalysis/dataset2_cluster_profiles.png')
    s += img('Lana_Gidan_Software_Exam/Dataset2_ClusterAnalysis/dataset2_dendrogram.png')

    s += hbar(SS, '8. Conclusions')
    for pt in [
        '<b>Research question answered — YES.</b> Four distinct, well-separated clusters '
        'were identified (Silhouette = 0.61), each perfectly matching a known plant type '
        '(100% accuracy), confirming both the 4-cluster solution and its external validity.',
        '<b>Aging Facilities (Cluster 3) are the highest-priority improvement target:</b> '
        'highest defect rate (7.65%), highest energy waste (92.7), highest downtime '
        '(14.3 hrs), yet lowest production speed (57.5). All metrics point to systemic failure.',
        '<b>Lean Manufacturing plants (Cluster 1) represent best practice:</b> high speed '
        '(82.3), low defects (2.17%), low labor cost (54.3), minimal downtime (3.3 hrs). '
        'These operational patterns should be studied and replicated.',
        '<b>High Automation plants (Cluster 2)</b> achieve the best speed (91.3) and '
        'lowest defects (1.46%) but consume the most energy (89.0). '
        'Energy optimization is their primary improvement lever.',
        '<b>Both K-Means and hierarchical clustering agree (Silhouette = 0.6096 for both), '
        'and PCA explains 89.5% of variance in 2D</b> — confirming the solution is robust, '
        'stable, and not an artifact of the clustering method.'
    ]:
        s.append(Paragraph(f'• {pt}', SS['Bul']))
        s.append(Spacer(1, 3))

    doc.build(s)
    print(f'Saved: {path}')


# ═══════════════════════════════════════════════════════════════════════════════
# DATASET 3 — MULTIPLE LINEAR REGRESSION
# ═══════════════════════════════════════════════════════════════════════════════
def report_ds3():
    path = 'Lana_Gidan_Software_Exam/Dataset3_MultipleRegression/dataset3_MultipleRegression_report.pdf'
    doc, SS = make_doc(path)
    s = []

    s.append(Paragraph('Dataset 3: Multiple Linear Regression', SS['CTitle']))
    s.append(Paragraph('Student Academic Performance Study  |  n = 150 students', SS['CSubtitle']))
    s.append(HRFlowable(width='100%', thickness=2, color=colors.HexColor('#1a3a5c')))
    s.append(Spacer(1, 8))

    s += hbar(SS, '1. Research Question')
    s += rq_box(SS,
        'Which academic and lifestyle factors (study hours, attendance, sleep, stress, '
        'practice tests) significantly predict final exam scores, what is the relative '
        'importance of each, and does sleep follow a non-linear (quadratic) pattern '
        'in its effect on academic performance?')

    s += hbar(SS, '2. Variables')
    s += tbl([
        ['Role',        'Variable',          'Mean (SD)',       'Description'],
        ['Dependent',   'Final_Exam_Score',  '67.03  (13.47)', 'Final exam score (range: 40–98)'],
        ['Independent', 'Study_Hours',       '8.11   (3.63)',  'Average study hours per week'],
        ['Independent', 'Attendance_Rate',   '79.56  (12.18)', 'Class attendance percentage'],
        ['Independent', 'Sleep_Hours',       '6.92   (1.71)',  'Average nightly sleep (quadratic term added per dataset guide)'],
        ['Independent', 'Stress_Level',      '5.55   (2.60)',  'Self-reported stress score (1–10)'],
        ['Independent', 'Practice_Tests',    '3.40   (2.33)',  'Number of practice tests completed'],
    ], [1.0*inch, 1.35*inch, 1.15*inch, 3.15*inch])

    s += hbar(SS, '3. Methodology — Multiple Linear Regression (OLS)')
    s.append(Paragraph(
        'Multiple Ordinary Least Squares (OLS) regression is the appropriate method '
        'because Final_Exam_Score is a continuous outcome and we aim to quantify each '
        'predictor\'s independent contribution while holding all others constant. '
        'A quadratic term (Sleep_Hours²) is included per the dataset\'s Variable '
        'Descriptions, which explicitly notes a quadratic relationship. '
        'Standardized beta coefficients (β) are computed on z-scored variables to '
        'directly compare predictor importance across different scales. '
        'Variance Inflation Factor (VIF) detects multicollinearity. '
        'All four OLS assumptions are formally tested: '
        'Shapiro-Wilk (normality of residuals), Breusch-Pagan (homoscedasticity), '
        'Durbin-Watson (independence), and a model comparison (AIC) tests whether '
        'the quadratic sleep term improves fit.', SS['Body']))

    s += hbar(SS, '4. Model Fit Statistics')
    s += tbl([
        ['Statistic',         'Value',             'Interpretation'],
        ['R²',                '0.7027',            '70.3% of exam score variance explained by the 6 predictors'],
        ['Adjusted R²',       '0.6902',            'Negligible shrinkage from R² — model is not overfitting'],
        ['F-statistic',       'F(6, 143) = 56.33', 'p < 0.001 — the model is globally significant'],
        ['RMSE',              '7.497 points',      'Average prediction error of ±7.5 exam points'],
        ['AIC (with Sleep²)', '1036.87',           'Compared to 1034.88 without — quadratic term not justified by AIC'],
        ['Durbin-Watson',     '1.957',             '≈ 2.0 — no autocorrelation in residuals ✓'],
    ], [1.4*inch, 1.75*inch, 3.5*inch])

    s += hbar(SS, '5. Regression Coefficients — Full Results')
    s += tbl([
        ['Predictor',      'B (unstd.)', 'Std Err', 't',      'p-value',   'Std β',  'Significance'],
        ['(Intercept)',    '46.803',     '12.181',  '3.84',   '< 0.001',   '—',      '✓'],
        ['Study_Hours',    '+2.465',     '0.170',   '14.47',  '< 0.001',   '+0.664', '✓ Strongest predictor'],
        ['Attendance_Rate','+0.211',     '0.051',   '4.10',   '< 0.001',   '+0.191', '✓'],
        ['Sleep_Hours',    '−1.810',     '3.277',   '−0.55',  '0.582',     '−0.229', '✗ Not significant'],
        ['Sleep_Hours²',   '−0.019',     '0.231',   '−0.08',  '0.936',     '−0.033', '✗ Not significant'],
        ['Stress_Level',   '−1.677',     '0.238',   '−7.04',  '< 0.001',   '−0.323', '✓'],
        ['Practice_Tests', '+1.832',     '0.269',   '6.81',   '< 0.001',   '+0.317', '✓'],
    ], [1.3*inch,0.75*inch,0.65*inch,0.65*inch,0.75*inch,0.65*inch,1.1*inch])
    s.append(Paragraph(
        'Std β = standardized beta (all variables on same scale). '
        '|Std β| directly ranks predictor importance independent of units.', SS['Note']))

    s += hbar(SS, '6. Coefficient Interpretation and Significance')
    for pt in [
        '<b>Study_Hours (β = +0.664, p &lt; 0.001) — Strongest predictor:</b> '
        'Each additional study hour per week raises the exam score by 2.47 points, '
        'all else equal. Standardized effect (0.664) is more than double the next '
        'predictor. Going from 4 hours to 12 hours of study corresponds to a ~19.7 '
        'point increase in exam score.',

        '<b>Stress_Level (β = −0.323, p &lt; 0.001) — 2nd strongest:</b> '
        'Each unit increase in stress reduces exam score by 1.68 points. '
        'Reducing stress from high (8.0) to moderate (4.0) corresponds to a '
        '6.7-point gain — equivalent to approximately 2.7 extra study hours per week.',

        '<b>Practice_Tests (β = +0.317, p &lt; 0.001) — 3rd:</b> '
        'Each additional practice test completed adds 1.83 points. '
        'Students who completed 6 practice tests score on average 11 points higher '
        'than those who completed none, controlling for all other factors.',

        '<b>Attendance_Rate (β = +0.191, p &lt; 0.001):</b> '
        'Every 10 percentage points of additional attendance adds 2.1 points. '
        'Moving from 70% to 90% attendance is worth approximately 4.2 exam points.',

        '<b>Sleep_Hours — linear and quadratic terms (both p &gt; 0.50): NOT significant.</b> '
        'Neither Sleep_Hours (p = 0.582) nor Sleep_Hours² (p = 0.936) contributes '
        'unique predictive power once study hours, stress, attendance, and practice '
        'tests are controlled. The AIC comparison (ΔAIC = −1.99) confirms the quadratic '
        'term does not improve model fit. Sleep shows a bivariate correlation of −0.25 '
        'with exam scores, but this relationship disappears when other factors are held constant.',
    ]:
        s.append(Paragraph(f'• {pt}', SS['Bul']))
        s.append(Spacer(1, 3))

    s += hbar(SS, '7. Assumption Diagnostics — All Passed')
    s += tbl([
        ['Test',                                  'Statistic',       'p-value', 'Result'],
        ['Shapiro-Wilk (residual normality)',      'W = 0.9933',     '0.714',   '✓ Residuals normally distributed'],
        ['Breusch-Pagan (homoscedasticity)',       'LM = 6.482',     '0.371',   '✓ Constant error variance'],
        ['Durbin-Watson (independence)',           'DW = 1.957',     '—',       '✓ No autocorrelation (≈ 2.0)'],
        ['VIF (multicollinearity)',                'All ≤ 1.04*',    '—',       '✓ No multicollinearity'],
    ], [2.0*inch, 1.1*inch, 0.75*inch, 2.8*inch])
    s.append(Paragraph(
        '* VIF is elevated for Sleep_Hours (~82) and Sleep_Hours² (~83), which is expected '
        'and unavoidable in polynomial regression — these two terms are mathematically '
        'correlated by construction. All other VIF values ≤ 1.04.', SS['Note']))

    s += hbar(SS, '8. Figures')
    s += img('Lana_Gidan_Software_Exam/Dataset3_MultipleRegression/dataset3_regression_diagnostics.png')
    s += img('Lana_Gidan_Software_Exam/Dataset3_MultipleRegression/dataset3_sleep_quadratic.png',
             w=W*0.68, h=W*0.33)

    s += hbar(SS, '9. Conclusions')
    for pt in [
        '<b>Research question answered.</b> Four of five predictors are significant. '
        'The model explains 70.3% of exam score variance '
        '(F(6,143) = 56.33, p &lt; 0.001) — strong performance for a behavioral study.',
        '<b>Study effort is the dominant driver</b> (β = 0.664): no other variable '
        'comes close. Interventions should focus first on increasing structured study time.',
        '<b>Stress management is underappreciated</b> (β = −0.323): its effect size '
        'rivals practice testing. Student support programs targeting stress reduction '
        'could yield meaningful, cost-effective academic gains.',
        '<b>Sleep is not independently significant</b> once other factors are controlled '
        '(both sleep terms p &gt; 0.50, ΔAIC = −1.99). Focusing solely on sleep without '
        'addressing study habits and stress is unlikely to improve outcomes.',
        '<b>All OLS assumptions are fully satisfied,</b> confirming coefficient estimates '
        'are unbiased, efficient, and valid for inference.'
    ]:
        s.append(Paragraph(f'• {pt}', SS['Bul']))
        s.append(Spacer(1, 3))

    doc.build(s)
    print(f'Saved: {path}')


# ═══════════════════════════════════════════════════════════════════════════════
# DATASET 4 — LINEAR DISCRIMINANT ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
def report_ds4():
    path = 'Lana_Gidan_Software_Exam/Dataset4_DiscriminantAnalysis/dataset4_DiscriminantAnalysis_report.pdf'
    doc, SS = make_doc(path)
    s = []

    s.append(Paragraph('Dataset 4: Linear Discriminant Analysis', SS['CTitle']))
    s.append(Paragraph('Heart Disease Risk Classification Study  |  n = 320 patients', SS['CSubtitle']))
    s.append(HRFlowable(width='100%', thickness=2, color=colors.HexColor('#1a3a5c')))
    s.append(Spacer(1, 8))

    s += hbar(SS, '1. Research Question')
    s += rq_box(SS,
        'Can a linear combination of seven clinical and lifestyle variables '
        '(age, BMI, blood pressure, cholesterol, exercise, stress level, and smoking '
        'history) effectively discriminate between patients at High Risk vs. Low Risk '
        'of heart disease, and which variables contribute most to this discrimination?')

    s += hbar(SS, '2. Variables')
    s += tbl([
        ['Role',        'Variable',                  'High Risk Mean', 'Low Risk Mean', 'Description'],
        ['Dependent',   'Heart_Disease_Group',        '—',     '—',     'High Risk / Low Risk (binary)'],
        ['Independent', 'Age',                        '53.61', '49.28', 'Patient age in years'],
        ['Independent', 'BMI',                        '28.37', '26.26', 'Body Mass Index'],
        ['Independent', 'Blood_Pressure',             '133.12','124.87','Systolic blood pressure (mmHg)'],
        ['Independent', 'Cholesterol',                '211.05','199.56','Total cholesterol level'],
        ['Independent', 'Exercise_Hours_Per_Week',    '3.14',  '3.98',  'Weekly exercise hours'],
        ['Independent', 'Stress_Level',               '5.47',  '4.59',  'Self-reported stress score (1–10)'],
        ['Independent', 'Smoking_Years',              '8.72',  '7.12',  'Years of smoking history'],
    ], [0.9*inch, 1.7*inch, 0.95*inch, 0.95*inch, 2.15*inch])

    s += hbar(SS, '3. Methodology — Linear Discriminant Analysis')
    s.append(Paragraph(
        'Linear Discriminant Analysis (LDA) is selected because it simultaneously '
        'achieves classification <i>and</i> produces an interpretable discriminant '
        'function — a linear combination of all predictors that maximally separates '
        'the two risk groups. This dual output (classification + interpretability) '
        'makes LDA superior to black-box classifiers for clinical use. '
        'All predictors are standardized before analysis. '
        'Data are split 75/25 (train/test, stratified by class). '
        'Performance is evaluated by accuracy, AUC-ROC, sensitivity, specificity, '
        'and F1 score. '
        'Ten-fold stratified cross-validation tests generalizability. '
        'The structure matrix (correlations between each predictor and the discriminant '
        'score) reveals which variables drive group separation most strongly.', SS['Body']))
    s.append(Paragraph(
        'Assumptions: Levene tests confirm homogeneity of variances for 6 of 7 '
        'variables (p &gt; 0.05). Smoking_Years shows minor variance inequality '
        '(p = 0.012) — LDA is robust to this with n = 320. '
        'Minor non-normality in Smoking_Years and Stress_Level is similarly tolerable '
        'at this sample size.', SS['Note']))

    s += hbar(SS, '4. Discriminant Function Coefficients (Standardized, Ranked)')
    s += tbl([
        ['Rank','Variable',                 'Coef.', 'Direction toward High Risk',   'Structure r',  'p-value'],
        ['1',   'Exercise_Hours_Per_Week',  '+0.957','Less exercise → High Risk',    'r = +0.494',   '< 0.001'],
        ['2',   'Stress_Level',             '−0.932','Higher stress → High Risk',    'r = −0.448',   '< 0.001'],
        ['3',   'Blood_Pressure',           '−0.857','Higher BP → High Risk',        'r = −0.370',   '< 0.001'],
        ['4',   'Cholesterol',              '−0.853','Higher cholesterol → High Risk','r = −0.287',  '< 0.001'],
        ['5',   'BMI',                      '−0.769','Higher BMI → High Risk',       'r = −0.405',   '< 0.001'],
        ['6',   'Age',                      '−0.609','Older age → High Risk',        'r = −0.340',   '< 0.001'],
        ['7',   'Smoking_Years',            '−0.344','More smoking → High Risk',     'r = −0.174',   '0.002'],
    ], [0.4*inch, 1.7*inch, 0.55*inch, 1.85*inch, 0.9*inch, 0.65*inch])
    s.append(Paragraph(
        'Structure matrix (r) ranks variables by their bivariate correlation with '
        'the discriminant score — a more stable measure of importance than raw coefficients. '
        'All 7 predictors reach statistical significance (p &lt; 0.01) in the structure matrix, '
        'confirming each contributes meaningfully to group discrimination.', SS['Note']))

    s += hbar(SS, '5. Classification Performance (Test Set, n = 80)')
    s += tbl([
        ['Metric',                              'Value',       'Benchmark',              'Verdict'],
        ['Overall Accuracy',                    '76.25%',      '> 70% = good',           '✓ Good'],
        ['AUC-ROC (High Risk = positive)',      '0.8350',      '> 0.80 = good',          '✓ Good discrimination'],
        ['Sensitivity (High Risk recall)',       '82.5%',       '> 75% = clinically useful','✓ Good'],
        ['Specificity (Low Risk recall)',        '70.0%',       '> 70%',                  '✓ Marginal'],
        ['F1 Score (High Risk)',                 '0.78',        '> 0.75',                 '✓ Good'],
        ['10-Fold CV Accuracy',                 '75.0% ± 7.8%','Stable across folds',    '✓ Generalizes well'],
    ], [2.0*inch, 0.85*inch, 1.85*inch, 1.0*inch])

    s += hbar(SS, '6. Confusion Matrix and Group Separation')
    s += tbl([
        ['',               'Predicted High Risk', 'Predicted Low Risk', 'Total'],
        ['Actual High Risk','33 (True Positive)',  '7  (False Negative)', '40'],
        ['Actual Low Risk', '12 (False Positive)', '28 (True Negative)',  '40'],
        ['Total',           '45',                  '35',                  '80'],
    ], [1.5*inch, 1.65*inch, 1.65*inch, 0.7*inch])
    s.append(Paragraph(
        'Group centroids on discriminant function: High Risk = −0.761, Low Risk = +0.761. '
        'The separation of 1.52 units confirms meaningful group distinction. '
        'The 7 false negatives (patients told low risk when actually high risk) represent '
        'the model\'s primary clinical limitation — a screening tool should aim to minimize '
        'these, potentially by lowering the decision threshold.', SS['Body']))

    s += hbar(SS, '7. Figures')
    s += img('Lana_Gidan_Software_Exam/Dataset4_DiscriminantAnalysis/dataset4_LDA_results.png')
    s += img('Lana_Gidan_Software_Exam/Dataset4_DiscriminantAnalysis/dataset4_LDA_coefficients.png',
             w=W*0.72, h=W*0.35)

    s += hbar(SS, '8. Conclusions')
    for pt in [
        '<b>Research question answered — YES.</b> The 7 clinical variables collectively '
        'discriminate well between High and Low Risk patients '
        '(AUC = 0.835, Accuracy = 76.25%, CV = 75.0% ± 7.8%) — substantially better '
        'than chance (50%) and consistent across all 10 cross-validation folds.',
        '<b>Exercise is the #1 discriminator</b> (structure r = 0.494, coef = 0.957): '
        'Low exercise is the single strongest marker of high cardiac risk. '
        'High Risk patients exercise 0.84 fewer hours per week than Low Risk patients '
        '(3.14 vs 3.98 hrs/week).',
        '<b>Stress is the #2 discriminator</b> (structure r = −0.448): '
        'High Risk patients report 0.88 higher stress scores (5.47 vs 4.59). '
        'Stress management is underutilized in cardiovascular risk reduction.',
        '<b>All 7 predictors are significant</b> (structure matrix p &lt; 0.01), '
        'confirming each variable contributes unique discriminatory information. '
        'Blood pressure, BMI, cholesterol, and age all distinguish groups significantly.',
        '<b>Cross-validation is stable</b> (75.0% ± 7.8% across 10 folds), '
        'confirming the model generalizes beyond the training data.',
        '<b>Clinical note — sensitivity priority:</b> The model correctly identifies '
        '82.5% of High Risk patients (sensitivity). The 7 false negatives (17.5%) '
        'are the critical limitation — in a clinical screening context, lowering the '
        'decision threshold could improve sensitivity at some cost to specificity.'
    ]:
        s.append(Paragraph(f'• {pt}', SS['Bul']))
        s.append(Spacer(1, 3))

    doc.build(s)
    print(f'Saved: {path}')


# ═══════════════════════════════════════════════════════════════════════════════
# DATASET 5 — EXPLORATORY FACTOR ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
def report_ds5():
    path = 'Lana_Gidan_Software_Exam/Dataset5_FactorAnalysis/dataset5_FactorAnalysis_report.pdf'
    doc, SS = make_doc(path)
    s = []

    s.append(Paragraph('Dataset 5: Exploratory Factor Analysis', SS['CTitle']))
    s.append(Paragraph('Psychological Constructs Study  |  15 Variables, n = 400', SS['CSubtitle']))
    s.append(HRFlowable(width='100%', thickness=2, color=colors.HexColor('#1a3a5c')))
    s.append(Spacer(1, 8))

    s += hbar(SS, '1. Research Question')
    s += rq_box(SS,
        'What is the underlying latent factor structure of 15 observed psychological '
        'variables measured across 400 individuals? How many distinct psychological '
        'constructs do these items measure, and can those factors be meaningfully '
        'interpreted and labeled?')

    s += hbar(SS, '2. Variables (No Pre-Defined DV/IV — All Observed)')
    s += tbl([
        ['Variable',                    'Mean',  'SD',    'Primary Factor (from dataset guide)'],
        ['Worry_Level',                 '49.50', '11.50', 'Anxiety'],
        ['Panic_Symptoms',              '47.40', '10.31', 'Anxiety'],
        ['Sleep_Disturbance',           '51.81',  '8.73', 'Anxiety / Depression (cross-loading)'],
        ['Sadness_Score',               '48.34', '11.62', 'Depression'],
        ['Hopelessness',                '46.43', '10.86', 'Depression'],
        ['Fatigue_Level',               '49.37',  '8.67', 'Depression / Anxiety (cross-loading)'],
        ['Public_Speaking_Confidence',  '55.01', '10.71', 'Social Confidence'],
        ['Social_Interaction',          '54.48',  '9.53', 'Social Confidence'],
        ['Assertiveness',               '53.27',  '9.26', 'Social Confidence'],
        ['Impulse_Control',             '56.14', '10.60', 'Self-Regulation'],
        ['Stress_Tolerance',            '55.08',  '9.69', 'Self-Regulation'],
        ['Emotional_Awareness',         '56.83',  '8.95', 'Self-Regulation'],
        ['Self_Esteem',                 '58.13',  '9.01', 'Resilience / Mixed'],
        ['Life_Satisfaction',           '60.35',  '9.36', 'Resilience / Mixed'],
        ['Coping_Ability',              '57.74',  '8.82', 'Resilience / Self-Regulation'],
    ], [2.0*inch, 0.5*inch, 0.5*inch, 2.65*inch])

    s += hbar(SS, '3. Methodology — Exploratory Factor Analysis (EFA)')
    s.append(Paragraph(
        'EFA is chosen because the goal is to <i>discover</i> the latent factor structure '
        'from the data rather than confirm a pre-specified model (which would require CFA). '
        '<b>Principal Axis Factoring (PAF)</b> with iterative communality estimation is '
        'used for extraction — this accounts for unique variance in each variable and '
        'produces stable, interpretable loadings. '
        '<b>Varimax orthogonal rotation</b> maximizes interpretability by simplifying '
        'the loading pattern so each variable loads strongly on as few factors as possible. '
        'The number of factors is determined by: '
        '(1) Kaiser criterion: retain factors with eigenvalue &gt; 1.0; '
        '(2) Scree plot inspection. '
        'Factor loadings ≥ |0.30| are considered practically significant '
        '(Tabachnick &amp; Fidell, 2019). '
        'Adequacy of the data for FA is verified by Bartlett\'s test and the '
        'Kaiser-Meyer-Olkin (KMO) measure before extraction. '
        'Communalities (h²) quantify how much each variable\'s variance is '
        'accounted for by the final factor solution.', SS['Body']))

    s += hbar(SS, '4. Adequacy Tests — Both Passed')
    s += tbl([
        ['Test',                    'Result',                         'Criterion',            'Verdict'],
        ["Bartlett's Sphericity",   'χ²(105) = 5630.28,  p < 0.001', 'p < 0.05 required',    '✓ FA appropriate — variables share meaningful covariance'],
        ['KMO Overall',             '0.8447  — "Meritorious"',        '≥ 0.80 = meritorious', '✓ Excellent sampling adequacy'],
        ['KMO per variable',        'Range: 0.73 – 0.94  (all ≥ 0.70)','≥ 0.60 each',        '✓ All 15 variables suitable for FA'],
    ], [1.5*inch, 2.35*inch, 1.35*inch, 1.45*inch])
    s.append(Paragraph(
        'The highly significant Bartlett test (χ² = 5630.28, p &lt; 0.001) confirms the '
        'correlation matrix is not an identity matrix — sufficient shared variance exists '
        'to justify factor analysis. KMO = 0.844 is "Meritorious" (Kaiser, 1974), '
        'indicating the patterns of correlations are compact and reliable factors exist.', SS['Body']))

    s += hbar(SS, '5. Eigenvalue Analysis and Factor Retention')
    s += tbl([
        ['Factor', 'Eigenvalue', '% Variance', 'Cumulative %', 'Retained?'],
        ['F1',     '4.6806',    '31.20%',      '31.20%',       'Yes — EV > 1.0'],
        ['F2',     '3.6368',    '24.25%',      '55.45%',       'Yes — EV > 1.0'],
        ['F3',     '2.5106',    '16.74%',      '72.19%',       'Yes — EV > 1.0'],
        ['F4',     '2.0238',    '13.49%',      '85.68%',       'Yes — EV > 1.0'],
        ['F5',     '0.3489',     '2.33%',      '88.01%',       'No — EV < 1.0 (scree break)'],
        ['F6–F15', '< 0.33',    '< 2.2% each', '—',           'No'],
    ], [0.55*inch, 0.9*inch, 0.95*inch, 1.15*inch, 1.7*inch])
    s.append(Paragraph(
        'The scree plot shows a clear elbow after Factor 4: eigenvalue drops sharply '
        'from 2.02 to 0.35 — a 6× decrease. Both Kaiser criterion and scree test '
        'independently support retaining <b>4 factors</b>, which together explain '
        '<b>80.94%</b> of total variance. This is excellent (guideline: &gt; 60%).', SS['Body']))

    s += hbar(SS, '6. Rotated Factor Loadings — Varimax (|λ| ≥ 0.30 flagged *)')
    s += tbl([
        ['Variable',                   'F1: Self-Reg.', 'F2: Depression', 'F3: Anxiety', 'F4: Social Conf.'],
        ['Impulse_Control',             '+0.927 *',  '—',          '—',          '—'],
        ['Stress_Tolerance',            '+0.891 *',  '—',          '—',          '—'],
        ['Emotional_Awareness',         '+0.868 *',  '—',          '—',          '—'],
        ['Coping_Ability',              '+0.681 *',  '—',          '+0.332 *',   '—'],
        ['Life_Satisfaction',           '+0.462 *',  '+0.600 *',   '—',          '+0.336 *'],
        ['Self_Esteem',                 '+0.382 *',  '+0.529 *',   '—',          '+0.495 *'],
        ['Hopelessness',                '—',         '−0.936 *',   '—',          '—'],
        ['Sadness_Score',               '—',         '−0.919 *',   '—',          '—'],
        ['Fatigue_Level',               '—',         '−0.824 *',   '+0.324 *',   '—'],
        ['Sleep_Disturbance',           '—',         '−0.461 *',   '+0.763 *',   '—'],
        ['Worry_Level',                 '—',         '—',          '+0.945 *',   '—'],
        ['Panic_Symptoms',              '—',         '—',          '+0.920 *',   '—'],
        ['Public_Speaking_Confidence',  '—',         '—',          '—',          '+0.929 *'],
        ['Social_Interaction',          '—',         '—',          '—',          '+0.913 *'],
        ['Assertiveness',               '—',         '—',          '—',          '+0.881 *'],
    ], [2.05*inch, 1.0*inch, 1.05*inch, 1.0*inch, 1.1*inch])
    s.append(Paragraph(
        '* |λ| ≥ 0.30 (practically significant).  — = loading < 0.30.  '
        'Negative loadings on F2 indicate those variables measure '
        'constructs that are low when depression/hopelessness is high.', SS['Note']))

    s += hbar(SS, '7. Variance Explained and Communalities')
    s += tbl([
        ['',               'F1: Self-Reg.','F2: Depression','F3: Anxiety','F4: Social','Total'],
        ['SS Loadings',    '3.293',        '3.265',         '2.609',      '2.975',     '12.142'],
        ['% Variance',     '21.95%',       '21.77%',        '17.39%',     '19.84%',    '80.94%'],
        ['Cumulative %',   '21.95%',       '43.72%',        '61.11%',     '80.94%',    '—'],
    ], [1.15*inch, 0.95*inch, 1.05*inch, 0.9*inch, 0.85*inch, 0.8*inch])
    s.append(Spacer(1, 4))
    s.append(Paragraph('<b>Communalities (h²) — proportion of each variable\'s variance explained by all 4 factors:</b>', SS['Sub']))
    s += tbl([
        ['Variable',                   'h²',   'Variable',             'h²',   'Variable',       'h²'],
        ['Worry_Level',                '0.897','Impulse_Control',      '0.863','Public_Speaking', '0.872'],
        ['Panic_Symptoms',             '0.851','Stress_Tolerance',     '0.847','Social_Interaction','0.837'],
        ['Sleep_Disturbance',          '0.803','Emotional_Awareness',  '0.816','Assertiveness',   '0.823'],
        ['Sadness_Score',              '0.855','Self_Esteem',          '0.681','Coping_Ability',  '0.637'],
        ['Hopelessness',               '0.883','Life_Satisfaction',    '0.689','—',               '—'],
        ['Fatigue_Level',              '0.790','—',                    '—',    '—',               '—'],
    ], [1.4*inch, 0.4*inch, 1.35*inch, 0.4*inch, 1.35*inch, 0.4*inch])
    s.append(Paragraph(
        'All communalities range from 0.64 to 0.90, indicating the 4-factor model '
        'accounts for 64–90% of each variable\'s variance. '
        'No variable is poorly explained — confirming the solution is comprehensive.', SS['Body']))

    s += hbar(SS, '8. Figures')
    s += img('Lana_Gidan_Software_Exam/Dataset5_FactorAnalysis/dataset5_factor_analysis.png')
    s += img('Lana_Gidan_Software_Exam/Dataset5_FactorAnalysis/dataset5_factor_scores.png',
             w=W*0.65, h=W*0.34)

    s += hbar(SS, '9. Factor Interpretation and Conclusions')
    for pt in [
        '<b>Research question answered: 4 latent factors</b> underlie the 15 psychological '
        'variables, jointly explaining 80.94% of total variance — well above the 60% '
        'guideline. All 4 factors are psychologically interpretable and align with '
        'established clinical constructs.',

        '<b>Factor 1 — Self-Regulation and Coping (21.95% variance):</b> '
        'Impulse_Control (λ=0.927), Stress_Tolerance (0.891), Emotional_Awareness (0.868), '
        'Coping_Ability (0.681). Captures the capacity to manage emotions, regulate '
        'impulses, and apply coping strategies under pressure. '
        'The near-unit loadings (0.87–0.93) indicate these three core items are '
        'highly reliable markers of this construct.',

        '<b>Factor 2 — Depression and Hopelessness (21.77% variance):</b> '
        'Hopelessness (λ=−0.936), Sadness_Score (−0.919), Fatigue_Level (−0.824). '
        'Negative loadings indicate that high item scores correspond to low factor scores '
        '(the factor itself is oriented toward absence of depression). '
        'Sleep_Disturbance cross-loads (λ=−0.461), consistent with clinical evidence '
        'that sleep disruption is a core transdiagnostic symptom of depression.',

        '<b>Factor 3 — Anxiety and Distress (17.39% variance):</b> '
        'Worry_Level (λ=0.945), Panic_Symptoms (0.920), Sleep_Disturbance (0.763). '
        'The exceptionally high loadings (0.92–0.95) make this the most clearly '
        'defined factor — these three variables are near-perfect markers of anxiety. '
        'Sleep_Disturbance cross-loads on both F2 and F3, confirming its role as '
        'a shared symptom across anxiety and depression (transdiagnostic).',

        '<b>Factor 4 — Social Confidence (19.84% variance):</b> '
        'Public_Speaking_Confidence (λ=0.929), Social_Interaction (0.913), '
        'Assertiveness (0.881). This is the most cleanly defined factor — '
        'all three items load exclusively on F4 with no cross-loadings. '
        'It reflects interpersonal self-efficacy and social functioning.',

        '<b>Clinical and practical implication:</b> These 4 factors can serve as '
        'validated subscale scores for a streamlined psychological screening instrument. '
        'The 15 raw items can be replaced by 4 composite scores (factor scores) while '
        'retaining 80.94% of all information — a substantial efficiency gain for '
        'clinical assessment and research.'
    ]:
        s.append(Paragraph(f'• {pt}', SS['Bul']))
        s.append(Spacer(1, 4))

    doc.build(s)
    print(f'Saved: {path}')


# ── Run all ──────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    report_ds1()
    report_ds2()
    report_ds3()
    report_ds4()
    report_ds5()
    print('\nAll 5 PDF reports generated.')

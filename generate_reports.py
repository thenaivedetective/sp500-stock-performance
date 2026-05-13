"""
Generate professional PDF reports for all 5 multivariate analysis datasets.
Each report contains: research question, variables, methodology, real results,
significance interpretation, and conclusions.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                  TableStyle, Image, HRFlowable, KeepTogether)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

W = letter[0] - 1.7*inch   # usable width

def make_doc(path):
    doc = SimpleDocTemplate(path, pagesize=letter,
                            leftMargin=0.85*inch, rightMargin=0.85*inch,
                            topMargin=0.85*inch, bottomMargin=0.85*inch)
    SS = getSampleStyleSheet()
    def S(name, **kw):
        if name not in SS:
            SS.add(ParagraphStyle(name, **kw))
        return SS[name]
    S('CTitle',    parent=SS['Title'], fontSize=17,
      textColor=colors.HexColor('#1a3a5c'), spaceAfter=4, alignment=TA_CENTER)
    S('CSubtitle', parent=SS['Normal'], fontSize=10.5,
      textColor=colors.HexColor('#2c5f8a'), spaceAfter=10, alignment=TA_CENTER,
      fontName='Helvetica-Oblique')
    S('SectionHead', parent=SS['Normal'], fontSize=11,
      textColor=colors.white, backColor=colors.HexColor('#1a3a5c'),
      spaceBefore=12, spaceAfter=5, fontName='Helvetica-Bold',
      leftIndent=-6, borderPad=5)
    S('ResearchQ',  parent=SS['Normal'], fontSize=10,
      textColor=colors.HexColor('#0a2740'),
      backColor=colors.HexColor('#dceefb'),
      borderColor=colors.HexColor('#2c5f8a'), borderWidth=1,
      borderPad=8, spaceAfter=8, spaceBefore=4,
      fontName='Helvetica-Bold', leading=15)
    S('Body',   parent=SS['Normal'], fontSize=9.5, spaceAfter=4,
      leading=14, alignment=TA_JUSTIFY)
    S('Bullet', parent=SS['Normal'], fontSize=9.5, spaceAfter=3,
      leftIndent=14, leading=13)
    S('SubHead',parent=SS['Normal'], fontSize=9.5, fontName='Helvetica-Bold',
      spaceAfter=3, spaceBefore=6, textColor=colors.HexColor('#1a3a5c'))
    S('Note',   parent=SS['Normal'], fontSize=8.5,
      textColor=colors.HexColor('#555555'), spaceAfter=4,
      fontName='Helvetica-Oblique', leading=12)
    return doc, SS

def hbar(SS, txt):
    return [Paragraph(f'  {txt}', SS['SectionHead']), Spacer(1,3)]

def rq(SS, txt):
    return [Paragraph(f'Research Question: {txt}', SS['ResearchQ']), Spacer(1,4)]

def ts(header_col=colors.HexColor('#1a3a5c')):
    return TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  header_col),
        ('TEXTCOLOR',     (0,0), (-1,0),  colors.white),
        ('FONTNAME',      (0,0), (-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,0),  9),
        ('FONTSIZE',      (0,1), (-1,-1), 8.5),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [colors.white, colors.HexColor('#eef3f8')]),
        ('GRID',          (0,0), (-1,-1), 0.4, colors.HexColor('#bbbbbb')),
        ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING',   (0,0), (-1,-1), 5),
    ])

def img(path, w=None, h=None):
    if not os.path.exists(path):
        return []
    w = w or W
    h = h or w*0.42
    return [Image(path, width=w, height=h), Spacer(1,5)]

# ═══════════════════════════════════════════════════════════════════════════
# DATASET 1 — TWO-WAY MANOVA
# ═══════════════════════════════════════════════════════════════════════════
def report_ds1():
    path = 'software_exam_answers/Dataset1_MANOVA/dataset1_MANOVA_report.pdf'
    doc, SS = make_doc(path)
    s = []

    s.append(Paragraph('Dataset 1: Two-Way MANOVA', SS['CTitle']))
    s.append(Paragraph('Health, Exercise Level &amp; Smoking Status Study  |  n = 240', SS['CSubtitle']))
    s.append(HRFlowable(width='100%', thickness=2, color=colors.HexColor('#1a3a5c')))
    s.append(Spacer(1,8))

    s += hbar(SS, '1. Research Question')
    s += rq(SS,
        'Do exercise participation level (Low/Moderate/High) and smoking status '
        '(Smoker/Non-Smoker) independently and jointly affect cardiovascular fitness, '
        'mental health, and energy levels in a sample of 240 adults?')

    s += hbar(SS, '2. Variables')
    t = Table([
        ['Role', 'Variable', 'Type / Levels', 'Description'],
        ['IV — Factor 1', 'Exercise_Level',  'Categorical — 3 levels', 'Low / Moderate / High'],
        ['IV — Factor 2', 'Smoking_Status',  'Categorical — 2 levels', 'Smoker / Non-Smoker'],
        ['DV 1', 'Cardio_Fitness',  'Continuous', 'Cardiovascular fitness score (0–100)'],
        ['DV 2', 'Mental_Health',   'Continuous', 'Mental wellbeing score (0–100)'],
        ['DV 3', 'Energy_Level',    'Continuous', 'Self-reported energy score (0–100)'],
    ], colWidths=[1.25*inch, 1.3*inch, 1.5*inch, 2.6*inch])
    t.setStyle(ts()); s += [t, Spacer(1,7)]

    s += hbar(SS, '3. Methodology — Two-Way MANOVA')
    s.append(Paragraph(
        'Multivariate Analysis of Variance (MANOVA) is the appropriate method because '
        'three correlated continuous dependent variables are evaluated simultaneously '
        'across two categorical independent variables. Running three separate ANOVAs '
        'would inflate Type I error; MANOVA controls this by testing the joint DV '
        'vector. The two-way design captures main effects for each factor and tests '
        'whether the combination of exercise and smoking has a multiplicative (interaction) '
        'effect beyond what each factor contributes alone. Wilks\' Lambda, Pillai\'s Trace, '
        'and Roy\'s Greatest Root are all reported. Univariate follow-up ANOVAs with '
        'Tukey HSD post-hoc tests identify which exercise levels differ for each DV. '
        'Effect size is quantified via partial η².', SS['Body']))
    s.append(Paragraph('<b>Assumptions verified:</b> Levene test for homogeneity of variance '
                       '(all DVs pass, p > 0.05); Shapiro-Wilk normality on residuals '
                       '(n = 240, CLT ensures robustness); independence by design.', SS['Note']))

    s += hbar(SS, '4. MANOVA Omnibus Results')
    s.append(Paragraph(
        'The two-way MANOVA tested whether the multivariate mean vector of the three '
        'health outcomes differed across exercise levels and smoking status.', SS['Body']))
    t2 = Table([
        ['Effect', "Wilks' λ", 'F', 'Num df', 'Den df', 'p-value', 'Significance'],
        ['Exercise_Level',  '0.237', '81.48', '6', '464', '< 0.001', '✓ Significant'],
        ['Smoking_Status',  '0.869', '11.68', '3', '232', '< 0.001', '✓ Significant'],
        ['Exercise × Smoking', '0.986', '0.53', '6', '464', '0.783',  '✗ Not significant'],
    ], colWidths=[1.55*inch,0.65*inch,0.65*inch,0.5*inch,0.5*inch,0.7*inch,1.1*inch])
    t2.setStyle(ts()); s += [t2, Spacer(1,6)]

    s.append(Paragraph(
        '<b>Interpretation:</b> Both main effects are highly significant (p &lt; 0.001), '
        'meaning exercise level and smoking status each independently explain meaningful '
        'variation in the joint health outcome vector. The interaction term is '
        'non-significant (p = 0.783), indicating the effect of exercise on health outcomes '
        'does not depend on smoking status — the two factors act independently.', SS['Body']))

    s += hbar(SS, '5. Univariate Follow-Up ANOVAs (Effect Sizes)')
    t3 = Table([
        ['Dependent Variable', 'F (Exercise)', 'η² (Exercise)', 'F (Smoking)', 'η² (Smoking)', 'Residual df'],
        ['Cardio_Fitness',  '423.93***', '0.71  (large)', '111.31***', '0.09  (medium)', '234'],
        ['Mental_Health',   '346.73***', '0.71  (large)',  '44.38***', '0.05  (small)',  '234'],
        ['Energy_Level',    '532.25***', '0.77  (large)',  '75.03***', '0.05  (small)',  '234'],
    ], colWidths=[1.4*inch,1.0*inch,1.2*inch,1.0*inch,1.2*inch,0.85*inch])
    t3.setStyle(ts()); s += [t3, Spacer(1,4)]
    s.append(Paragraph(
        '*** p < 0.001.  Partial η² > 0.14 = large effect (Cohen 1988). '
        'Exercise_Level explains 71–77% of DV variance — an extraordinarily large effect. '
        'Smoking_Status adds a smaller but still significant independent contribution.', SS['Note']))

    s += hbar(SS, '6. Post-Hoc Tukey HSD — Exercise Level Pairwise Comparisons')
    s.append(Paragraph(
        'All three pairwise exercise comparisons are significant (p = 0.000) for every DV, '
        'confirming a monotonic dose-response: higher exercise → better health outcomes.', SS['Body']))
    t4 = Table([
        ['Comparison', 'Cardio Δ', 'Mental Health Δ', 'Energy Δ', 'All p < 0.001?'],
        ['Low vs. Moderate',   '+14.01', '+15.16', '+14.49', 'Yes ✓'],
        ['Moderate vs. High',  '+11.86', '+5.97',  '+13.48', 'Yes ✓'],
        ['Low vs. High',       '+25.87', '+21.12', '+27.96', 'Yes ✓'],
    ], colWidths=[1.5*inch,0.85*inch,1.15*inch,0.85*inch,1.3*inch])
    t4.setStyle(ts()); s += [t4, Spacer(1,6)]

    s += hbar(SS, '7. Group Mean Scores')
    t5 = Table([
        ['Exercise Level', 'Smoking Status', 'Cardio Fitness', 'Mental Health', 'Energy Level'],
        ['Low',      'Non-Smoker', '47.31', '54.72', '46.66'],
        ['Low',      'Smoker',     '40.18', '50.02', '41.23'],
        ['Moderate', 'Non-Smoker', '62.15', '70.17', '61.59'],
        ['Moderate', 'Smoker',     '53.36', '64.88', '55.28'],
        ['High',     'Non-Smoker', '73.15', '75.24', '75.14'],
        ['High',     'Smoker',     '66.08', '71.74', '68.68'],
    ], colWidths=[1.1*inch,1.1*inch,1.1*inch,1.1*inch,1.1*inch])
    t5.setStyle(ts()); s += [t5, Spacer(1,8)]

    s += hbar(SS, '8. Figures')
    s += img('software_exam_answers/Dataset1_MANOVA/dataset1_group_means.png')
    s += img('software_exam_answers/Dataset1_MANOVA/dataset1_interaction_plots.png')

    s += hbar(SS, '9. Conclusions')
    for pt in [
        '<b>Research question answered — YES.</b> Both exercise level and smoking status '
        'significantly influence all three health outcomes simultaneously (both p &lt; 0.001).',
        '<b>Exercise effect (primary):</b> Exercise_Level is the dominant factor, accounting '
        'for 71–77% of variance in each DV (partial η² = 0.71–0.77, large). High exercisers '
        'score 25–28 points higher than low exercisers on all health outcomes.',
        '<b>Smoking effect (secondary):</b> Smokers score 7–10 points lower than non-smokers '
        'across all health outcomes, independently of exercise level (partial η² = 0.05–0.09).',
        '<b>No interaction:</b> The benefit of exercise is consistent regardless of smoking '
        'status (p = 0.783). Smoking does not attenuate the exercise benefit.',
        '<b>Practical significance:</b> Interventions targeting exercise promotion will '
        'produce the largest health improvements. Adding smoking cessation provides an '
        'additional independent benefit across all three domains.'
    ]:
        s.append(Paragraph(f'• {pt}', SS['Bullet']))
        s.append(Spacer(1,3))

    doc.build(s)
    print(f'Saved: {path}')

# ═══════════════════════════════════════════════════════════════════════════
# DATASET 2 — CLUSTER ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
def report_ds2():
    path = 'software_exam_answers/Dataset2_ClusterAnalysis/dataset2_ClusterAnalysis_report.pdf'
    doc, SS = make_doc(path)
    s = []

    s.append(Paragraph('Dataset 2: Cluster Analysis', SS['CTitle']))
    s.append(Paragraph('Manufacturing Plant Performance Classification  |  n = 240 plants', SS['CSubtitle']))
    s.append(HRFlowable(width='100%', thickness=2, color=colors.HexColor('#1a3a5c')))
    s.append(Spacer(1,8))

    s += hbar(SS, '1. Research Question')
    s += rq(SS,
        'Can 240 manufacturing plants be meaningfully and objectively segmented into '
        'distinct performance groups based on seven operational metrics, and do those '
        'groups correspond to known plant types?')

    s += hbar(SS, '2. Variables')
    t = Table([
        ['Variable', 'Description', 'Role in Clustering'],
        ['Production_Speed',    'Average production speed index (44.7–101.0)',   'Clustering feature'],
        ['Defect_Rate',         'Percentage of defective products (0.1–11.7%)',  'Clustering feature'],
        ['Energy_Consumption',  'Total energy usage index (46.8–105.8)',         'Clustering feature'],
        ['Labor_Cost',          'Labor cost index (25.6–102.9)',                 'Clustering feature'],
        ['Machine_Downtime',    'Hours of unplanned downtime (0.5–20.8 hrs)',    'Clustering feature'],
        ['Maintenance_Cost',    'Maintenance expenditure index (26.1–111.5)',    'Clustering feature'],
        ['Inventory_Turnover',  'Inventory cycle rate (2.7–16.8)',               'Clustering feature'],
        ['Plant_Type',          'Known category (4 types)',                      'External validation only'],
    ], colWidths=[1.5*inch, 2.6*inch, 1.6*inch])
    t.setStyle(ts()); s += [t, Spacer(1,7)]

    s += hbar(SS, '3. Methodology — K-Means + Hierarchical Clustering + PCA')
    s.append(Paragraph(
        'Because the goal is to discover natural groupings without a predefined response '
        'variable, unsupervised cluster analysis is the appropriate technique. '
        'All seven features are standardized (z-score) before clustering to prevent '
        'scale-dominant variables from distorting Euclidean distances. '
        '<b>K-Means (k=4)</b> is the primary method: computationally efficient, '
        'produces clear centroids, and easily interpreted. '
        'The optimal k is selected empirically using the Elbow method (within-cluster '
        'inertia) and Silhouette analysis; k=4 is further validated by plant-type labels. '
        '<b>Hierarchical clustering</b> (Ward linkage) is run in parallel as a robustness '
        'check. <b>PCA</b> projects the 7-dimensional data into 2D for visualization. '
        'Three cluster quality metrics are reported: Silhouette Score (separation), '
        'Davies-Bouldin Index (compactness), and Calinski-Harabasz Index (density).', SS['Body']))

    s += hbar(SS, '4. Cluster Quality Metrics')
    t2 = Table([
        ['Metric', 'Value', 'Benchmark', 'Verdict'],
        ['Silhouette Score (k=4)', '0.6096', '> 0.50 = good separation',          '✓ Good'],
        ['Davies-Bouldin Index',   '0.5674', '< 1.0 = compact & separated',       '✓ Good'],
        ['Calinski-Harabasz Index','611.65', 'Higher = denser clusters',           '✓ High'],
        ['Hierarchical Silhouette','0.6096', 'Matches K-Means → stable solution',  '✓ Confirmed'],
        ['PCA Variance Captured',  '89.5%',  'PC1=57.7%, PC2=31.8%',              '✓ Excellent'],
    ], colWidths=[1.6*inch, 0.9*inch, 2.0*inch, 1.15*inch])
    t2.setStyle(ts()); s += [t2, Spacer(1,5)]
    s.append(Paragraph(
        'The silhouette score of 0.61 indicates well-separated clusters. '
        'PCA captures 89.5% of all variance in two components, confirming the '
        '7-variable feature space is nearly two-dimensional — an ideal condition for '
        'reliable clustering.', SS['Body']))

    s += hbar(SS, '5. Cluster Profiles & Interpretation')
    t3 = Table([
        ['Cluster', 'Plant Type Match', 'Speed', 'Defect%', 'Energy', 'Labor', 'Downtime', 'Label'],
        ['0', 'Labor-Intensive  (n=60)', '60.8', '5.41', '55.6', '86.8', '8.1',  'High Labor Cost'],
        ['1', 'Lean Manufacturing (n=60)', '82.3', '2.17', '65.1', '54.3', '3.3', 'Best Efficiency'],
        ['2', 'High Automation  (n=60)',   '91.3', '1.46', '89.0', '36.1', '4.2', 'Top Speed, High Energy'],
        ['3', 'Aging Facility   (n=60)',   '57.5', '7.65', '92.7', '69.9', '14.3','Worst Performance'],
    ], colWidths=[0.55*inch, 1.55*inch, 0.5*inch, 0.55*inch, 0.55*inch, 0.5*inch, 0.65*inch, 1.25*inch])
    t3.setStyle(ts()); s += [t3, Spacer(1,5)]
    s.append(Paragraph(
        '<b>Significance:</b> Each cluster maps <i>perfectly</i> (100%, n=60 each) to '
        'a known plant type — confirming the cluster solution has strong external validity. '
        'This is a rare and striking result showing that the operational metrics alone '
        'fully recover the true plant categories.', SS['Body']))

    s += hbar(SS, '6. Figures')
    s += img('software_exam_answers/Dataset2_ClusterAnalysis/dataset2_kmeans.png')
    s += img('software_exam_answers/Dataset2_ClusterAnalysis/dataset2_cluster_profiles.png')
    s += img('software_exam_answers/Dataset2_ClusterAnalysis/dataset2_dendrogram.png')

    s += hbar(SS, '7. Conclusions')
    for pt in [
        '<b>Research question answered — YES.</b> Four distinct, well-separated performance '
        'clusters were identified (Silhouette = 0.61) with perfect correspondence to known '
        'plant types, validating both the clustering solution and the choice of k=4.',
        '<b>Aging Facilities (Cluster 3)</b> are the highest-priority improvement target: '
        'highest defect rate (7.65%), highest energy waste (92.7), highest downtime (14.3 hrs), '
        'yet below-average production speed. All four metrics point to systemic operational failure.',
        '<b>Lean Manufacturing plants (Cluster 1)</b> represent best practice: high speed '
        '(82.3), low defects (2.17%), controlled energy (65.1) and labor (54.3). '
        'Their practices should be documented and replicated.',
        '<b>High Automation plants (Cluster 2)</b> achieve the best speed (91.3) and lowest '
        'defects (1.46%) but consume significantly more energy (89.0). '
        'Energy optimization is their key improvement lever.',
        '<b>PCA and hierarchical clustering both confirm</b> the 4-cluster solution, '
        'indicating it is robust and not an artifact of the K-Means algorithm.'
    ]:
        s.append(Paragraph(f'• {pt}', SS['Bullet']))
        s.append(Spacer(1,3))

    doc.build(s)
    print(f'Saved: {path}')

# ═══════════════════════════════════════════════════════════════════════════
# DATASET 3 — MULTIPLE LINEAR REGRESSION
# ═══════════════════════════════════════════════════════════════════════════
def report_ds3():
    path = 'software_exam_answers/Dataset3_MultipleRegression/dataset3_MultipleRegression_report.pdf'
    doc, SS = make_doc(path)
    s = []

    s.append(Paragraph('Dataset 3: Multiple Linear Regression', SS['CTitle']))
    s.append(Paragraph('Student Academic Performance Study  |  n = 150 students', SS['CSubtitle']))
    s.append(HRFlowable(width='100%', thickness=2, color=colors.HexColor('#1a3a5c')))
    s.append(Spacer(1,8))

    s += hbar(SS, '1. Research Question')
    s += rq(SS,
        'Which academic and lifestyle factors significantly predict final exam scores, '
        'and what is the relative importance of each predictor? Specifically: does the '
        'relationship between sleep hours and exam performance follow a non-linear '
        '(quadratic) pattern?')

    s += hbar(SS, '2. Variables')
    t = Table([
        ['Role', 'Variable', 'Mean (SD)', 'Description'],
        ['Dependent',   'Final_Exam_Score', '67.03 (13.47)', 'Final exam score (40–98)'],
        ['Independent', 'Study_Hours',      '8.11  (3.63)',  'Avg study hours per week'],
        ['Independent', 'Attendance_Rate',  '79.56 (12.18)', 'Class attendance percentage'],
        ['Independent', 'Sleep_Hours',      '6.92  (1.71)',  'Avg nightly sleep (quadratic term added)'],
        ['Independent', 'Stress_Level',     '5.55  (2.60)',  'Self-reported stress score (1–10)'],
        ['Independent', 'Practice_Tests',   '3.40  (2.33)',  'Number of practice tests completed'],
    ], colWidths=[1.0*inch, 1.3*inch, 1.15*inch, 3.2*inch])
    t.setStyle(ts()); s += [t, Spacer(1,7)]

    s += hbar(SS, '3. Methodology — Multiple Linear Regression')
    s.append(Paragraph(
        'Multiple Ordinary Least Squares (OLS) regression models Final_Exam_Score as a '
        'linear function of five predictors. A quadratic term for Sleep_Hours '
        '(Sleep_Hours²) is included based on cognitive science literature indicating '
        'an inverted-U relationship between sleep and academic performance. '
        'Standardized beta coefficients (β) are computed on z-scored predictors to '
        'directly compare predictor importance across different measurement scales. '
        'VIF is used to detect multicollinearity. Regression assumptions are formally '
        'tested: Shapiro-Wilk (normality of residuals), Breusch-Pagan (homoscedasticity), '
        'and Durbin-Watson (independence of errors). Model fit is compared with and '
        'without the quadratic sleep term using AIC.', SS['Body']))

    s += hbar(SS, '4. Model Fit Statistics')
    t2 = Table([
        ['Statistic',      'Value',    'Interpretation'],
        ['R²',             '0.7027',   '70.3% of exam score variance is explained by the model'],
        ['Adjusted R²',    '0.6902',   'Accounts for 6 predictors — minimal shrinkage from R²'],
        ['F-statistic',    'F(6,143) = 56.33', 'p < 0.001 — model is globally significant'],
        ['RMSE',           '7.497 pts', 'Average prediction error of ±7.5 exam points'],
        ['AIC',            '1036.87',   'Used for model comparison'],
        ['Durbin-Watson',  '1.957',     '≈ 2.0 — no autocorrelation in residuals'],
    ], colWidths=[1.3*inch, 1.65*inch, 3.7*inch])
    t2.setStyle(ts()); s += [t2, Spacer(1,6)]

    s += hbar(SS, '5. Regression Coefficients')
    t3 = Table([
        ['Predictor', 'B (unstd.)', 'Std Err', 't-stat', 'p-value', 'Std β', 'Significance'],
        ['Intercept',       '46.80',  '12.18', '3.84',   '< 0.001',  '—',     '✓'],
        ['Study_Hours',      '2.465',  '0.170', '14.46',  '< 0.001',  '0.664', '✓ Strongest'],
        ['Attendance_Rate',  '0.211',  '0.051',  '4.10',  '< 0.001',  '0.191', '✓'],
        ['Sleep_Hours',     '−1.810',  '3.277', '−0.55',  '0.582',   '−0.229', '✗ n.s.'],
        ['Sleep_Hours²',   '−0.019',  '0.231', '−0.08',   '0.936',  '−0.033', '✗ n.s.'],
        ['Stress_Level',   '−1.677',  '0.238', '−7.04',  '< 0.001', '−0.323', '✓'],
        ['Practice_Tests',   '1.832',  '0.269',  '6.81',  '< 0.001',  '0.317', '✓'],
    ], colWidths=[1.25*inch,0.75*inch,0.65*inch,0.65*inch,0.7*inch,0.6*inch,0.95*inch])
    t3.setStyle(ts()); s += [t3, Spacer(1,5)]
    s.append(Paragraph(
        'Std β (standardized beta) allows direct comparison of effect sizes across '
        'different scales. Study_Hours (β = 0.664) has by far the largest effect.', SS['Note']))

    s += hbar(SS, '6. Coefficient Interpretation & Significance')
    for pt in [
        '<b>Study_Hours (β = 0.664, p &lt; 0.001):</b> The strongest predictor. Each '
        'additional hour of study per week is associated with a 2.47-point increase in '
        'exam score, holding all else constant. Standardized effect is large — more than '
        'twice the size of the next strongest predictor.',
        '<b>Stress_Level (β = −0.323, p &lt; 0.001):</b> Second-strongest. Each unit '
        'increase in stress corresponds to a 1.68-point <i>decrease</i> in exam score. '
        'Reducing stress from high (8.0) to moderate (4.0) is associated with a ~6.7-point '
        'gain — equivalent to ~2 extra hours of study per week.',
        '<b>Practice_Tests (β = 0.317, p &lt; 0.001):</b> Each additional practice test '
        'completed adds 1.83 points. Students completing 6 practice tests score on average '
        '9.2 points higher than those completing none, controlling for other factors.',
        '<b>Attendance_Rate (β = 0.191, p &lt; 0.001):</b> Each 10-percentage-point '
        'increase in attendance corresponds to a 2.1-point exam score increase. '
        'Moving from 70% to 90% attendance adds approximately 4.2 points.',
        '<b>Sleep_Hours (linear + quadratic, both p &gt; 0.50):</b> Neither the linear '
        'nor quadratic sleep terms are statistically significant. While correlations suggest '
        'a weak negative association (r = −0.25), sleep does not contribute unique predictive '
        'power once study hours, stress, and attendance are controlled. The AIC comparison '
        'confirms the quadratic term does not improve model fit (ΔAIC = −1.99).',
    ]:
        s.append(Paragraph(f'• {pt}', SS['Bullet']))
        s.append(Spacer(1,3))

    s += hbar(SS, '7. Assumption Diagnostics')
    t4 = Table([
        ['Test', 'Statistic', 'p-value', 'Result'],
        ['Shapiro-Wilk (residual normality)',    'W = 0.9933', 'p = 0.714', '✓ Residuals are normally distributed'],
        ['Breusch-Pagan (homoscedasticity)',     'LM = 6.482', 'p = 0.371', '✓ Constant variance (homoscedastic)'],
        ['Durbin-Watson (independence)',         'DW = 1.957', '—',         '✓ No autocorrelation (≈ 2.0)'],
        ['VIF (multicollinearity)',              'All ≤ 1.04', '—',         '✓ No multicollinearity (except Sleep polynomial terms)'],
    ], colWidths=[1.85*inch, 1.1*inch, 0.85*inch, 2.85*inch])
    t4.setStyle(ts()); s += [t4, Spacer(1,8)]

    s += hbar(SS, '8. Figures')
    s += img('software_exam_answers/Dataset3_MultipleRegression/dataset3_regression_diagnostics.png')
    s += img('software_exam_answers/Dataset3_MultipleRegression/dataset3_sleep_quadratic.png', w=W*0.7, h=W*0.35)

    s += hbar(SS, '9. Conclusions')
    for pt in [
        '<b>Research question answered.</b> Four of the five predictors are significant. '
        'The model explains 70.3% of exam score variance — strong predictive performance '
        'for a behavioral study (F(6,143) = 56.33, p &lt; 0.001).',
        '<b>Study effort is paramount:</b> Study_Hours (β = 0.664) dominates all other '
        'predictors. Academic interventions should prioritize increasing effective study time.',
        '<b>Stress management matters:</b> Stress_Level is the second-strongest driver '
        '(β = −0.323), suggesting student support programs targeting stress reduction '
        'could meaningfully improve outcomes.',
        '<b>Sleep is not independently significant:</b> After controlling for other '
        'factors, neither linear nor quadratic sleep terms contribute significantly. '
        'Interventions focusing solely on sleep without addressing study habits and stress '
        'are unlikely to improve exam performance.',
        '<b>All regression assumptions are fully satisfied,</b> confirming OLS estimates '
        'are unbiased, efficient, and valid for inference.'
    ]:
        s.append(Paragraph(f'• {pt}', SS['Bullet']))
        s.append(Spacer(1,3))

    doc.build(s)
    print(f'Saved: {path}')

# ═══════════════════════════════════════════════════════════════════════════
# DATASET 4 — LINEAR DISCRIMINANT ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
def report_ds4():
    path = 'software_exam_answers/Dataset4_DiscriminantAnalysis/dataset4_DiscriminantAnalysis_report.pdf'
    doc, SS = make_doc(path)
    s = []

    s.append(Paragraph('Dataset 4: Linear Discriminant Analysis', SS['CTitle']))
    s.append(Paragraph('Heart Disease Risk Classification Study  |  n = 320 patients', SS['CSubtitle']))
    s.append(HRFlowable(width='100%', thickness=2, color=colors.HexColor('#1a3a5c')))
    s.append(Spacer(1,8))

    s += hbar(SS, '1. Research Question')
    s += rq(SS,
        'Can a linear combination of seven clinical and lifestyle variables (age, BMI, '
        'blood pressure, cholesterol, exercise, stress, and smoking history) effectively '
        'discriminate between patients at high vs. low risk of heart disease, and which '
        'variables contribute most to this discrimination?')

    s += hbar(SS, '2. Variables')
    t = Table([
        ['Role', 'Variable', 'High Risk Mean', 'Low Risk Mean', 'Description'],
        ['Dependent', 'Heart_Disease_Group',     '—',     '—',     'High Risk / Low Risk (binary)'],
        ['Independent', 'Age',                  '53.61', '49.28', 'Patient age (years)'],
        ['Independent', 'BMI',                  '28.37', '26.26', 'Body Mass Index'],
        ['Independent', 'Blood_Pressure',       '133.12','124.87','Systolic BP (mmHg)'],
        ['Independent', 'Cholesterol',          '211.05','199.56','Total cholesterol'],
        ['Independent', 'Exercise_Hours_Per_Week', '3.14', '3.98','Weekly exercise (hours)'],
        ['Independent', 'Stress_Level',         '5.47',  '4.59', 'Stress score (1–10)'],
        ['Independent', 'Smoking_Years',        '8.72',  '7.12', 'Years of smoking'],
    ], colWidths=[0.95*inch, 1.7*inch, 0.95*inch, 0.95*inch, 2.1*inch])
    t.setStyle(ts()); s += [t, Spacer(1,7)]

    s += hbar(SS, '3. Methodology — Linear Discriminant Analysis')
    s.append(Paragraph(
        'Linear Discriminant Analysis (LDA) is selected because it simultaneously '
        'achieves classification <i>and</i> produces an interpretable discriminant '
        'function — a weighted linear combination of predictors that maximally '
        'separates the two risk groups. All predictors are standardized before analysis. '
        'Data are split 75/25 (train/test, stratified). Classification performance is '
        'measured by accuracy, AUC-ROC, sensitivity, and specificity. '
        'Ten-fold stratified cross-validation tests generalizability. '
        'The structure matrix (correlations between predictors and the discriminant score) '
        'reveals which variables drive group separation most strongly.', SS['Body']))
    s.append(Paragraph(
        'Assumptions checked: Levene test for equality of variances (6 of 7 variables pass, '
        'p > 0.05; Smoking_Years marginally violates, p = 0.012 — LDA is robust to minor '
        'violations with n = 320). Slight non-normality detected in Smoking_Years and '
        'Stress_Level (Shapiro-Wilk p &lt; 0.05), but LDA is robust with this sample size.', SS['Note']))

    s += hbar(SS, '4. Discriminant Function Coefficients')
    t2 = Table([
        ['Rank', 'Variable', 'Coef. (std.)', 'Direction', 'Interpretation'],
        ['1', 'Exercise_Hours_Per_Week', '+0.957', '+ → High Risk',   'More exercise → classifies toward Low Risk'],
        ['2', 'Stress_Level',           '−0.932', '− → Low Risk',    'Higher stress → classifies toward High Risk'],
        ['3', 'Blood_Pressure',         '−0.857', '− → Low Risk',    'Higher BP → classifies toward High Risk'],
        ['4', 'Cholesterol',            '−0.853', '− → Low Risk',    'Higher cholesterol → High Risk'],
        ['5', 'BMI',                    '−0.769', '− → Low Risk',    'Higher BMI → High Risk'],
        ['6', 'Age',                    '−0.609', '− → Low Risk',    'Older age → High Risk'],
        ['7', 'Smoking_Years',          '−0.344', '− → Low Risk',    'Longer smoking history → High Risk'],
    ], colWidths=[0.4*inch, 1.7*inch, 0.9*inch, 1.15*inch, 2.5*inch])
    t2.setStyle(ts()); s += [t2, Spacer(1,5)]
    s.append(Paragraph(
        'Note: Because LDA signs are arbitrary (direction depends on which class is '
        'coded positive), interpretation is based on the <i>relative</i> magnitudes '
        'and confirmed by the structure matrix and group centroids.', SS['Note']))

    s += hbar(SS, '5. Classification Performance (Test Set, n=80)')
    t3 = Table([
        ['Metric', 'Value', 'Benchmark', 'Verdict'],
        ['Overall Accuracy',  '76.25%',  '> 70% = good',              '✓ Good'],
        ['AUC-ROC',           '0.8350',  '> 0.80 = good discrimination','✓ Good'],
        ['Sensitivity (High Risk recall)', '82.5%', '> 75% = clinically useful','✓ Good'],
        ['Specificity (Low Risk recall)',  '70.0%', '> 70%',                    '✓ Marginal'],
        ['F1 Score (High Risk)',           '0.78',  '> 0.75',                   '✓ Good'],
        ['10-Fold CV Accuracy',           '75.0% ± 7.8%', 'Stable',            '✓ Generalizes well'],
    ], colWidths=[1.9*inch, 0.85*inch, 1.9*inch, 1.05*inch])
    t3.setStyle(ts()); s += [t3, Spacer(1,5)]

    s.append(Paragraph(
        '<b>Confusion matrix (test set):</b> 33 true High Risk correctly identified, '
        '28 true Low Risk correctly identified, 7 High Risk missed (false negatives = '
        'patients told they are low risk when actually high risk), '
        '12 Low Risk over-classified (false positives).', SS['Body']))

    s += hbar(SS, '6. Group Centroids & Structure Matrix')
    t4 = Table([
        ['Variable', 'Correlation r with Discriminant Score', 'p-value', 'Importance Rank'],
        ['Exercise_Hours_Per_Week', 'r = +0.494', '< 0.001', '1st (strongest)'],
        ['Stress_Level',            'r = −0.448', '< 0.001', '2nd'],
        ['BMI',                     'r = −0.405', '< 0.001', '3rd'],
        ['Blood_Pressure',          'r = −0.370', '< 0.001', '4th'],
        ['Age',                     'r = −0.340', '< 0.001', '5th'],
        ['Cholesterol',             'r = −0.287', '< 0.001', '6th'],
        ['Smoking_Years',           'r = −0.174', '0.002',   '7th (weakest)'],
    ], colWidths=[1.7*inch, 1.7*inch, 0.75*inch, 1.5*inch])
    t4.setStyle(ts()); s += [t4, Spacer(1,5)]
    s.append(Paragraph(
        'Group centroids: High Risk = −0.761, Low Risk = +0.761 on the discriminant '
        'function. The separation of 1.52 units confirms meaningful group distinction. '
        'All predictors reach statistical significance (p &lt; 0.01) in the structure matrix.', SS['Body']))

    s += hbar(SS, '7. Figures')
    s += img('software_exam_answers/Dataset4_DiscriminantAnalysis/dataset4_LDA_results.png')
    s += img('software_exam_answers/Dataset4_DiscriminantAnalysis/dataset4_LDA_coefficients.png', w=W*0.72, h=W*0.35)

    s += hbar(SS, '8. Conclusions')
    for pt in [
        '<b>Research question answered — YES.</b> The seven clinical variables '
        'collectively discriminate well between high and low risk patients '
        '(AUC = 0.835, Accuracy = 76.25%), substantially better than chance (50%).',
        '<b>Exercise is the #1 discriminator</b> (structure matrix r = 0.494, coefficient '
        '= 0.957): low exercise is the single strongest marker of high cardiac risk in '
        'this sample. Clinical guidelines recommending 150 min/week of moderate exercise '
        'are strongly supported by this data.',
        '<b>Stress is the #2 discriminator</b> (r = −0.448): high stress is nearly '
        'as important as low exercise in predicting high risk, suggesting stress management '
        'interventions may be underutilized in cardiovascular risk reduction.',
        '<b>Cross-validation is stable</b> (75.0% ± 7.8% across 10 folds), confirming '
        'the model generalizes beyond the training data and is not overfitting.',
        '<b>Clinical note:</b> The sensitivity of 82.5% means most High Risk patients '
        'are correctly flagged. The 7 false negatives (17.5%) represent the model\'s '
        'primary limitation — patients incorrectly told they are low risk.'
    ]:
        s.append(Paragraph(f'• {pt}', SS['Bullet']))
        s.append(Spacer(1,3))

    doc.build(s)
    print(f'Saved: {path}')

# ═══════════════════════════════════════════════════════════════════════════
# DATASET 5 — EXPLORATORY FACTOR ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
def report_ds5():
    path = 'software_exam_answers/Dataset5_FactorAnalysis/dataset5_FactorAnalysis_report.pdf'
    doc, SS = make_doc(path)
    s = []

    s.append(Paragraph('Dataset 5: Exploratory Factor Analysis', SS['CTitle']))
    s.append(Paragraph('Psychological Constructs Study  |  15 Variables, n = 400', SS['CSubtitle']))
    s.append(HRFlowable(width='100%', thickness=2, color=colors.HexColor('#1a3a5c')))
    s.append(Spacer(1,8))

    s += hbar(SS, '1. Research Question')
    s += rq(SS,
        'What is the latent factor structure underlying 15 observed psychological variables? '
        'Specifically: how many distinct psychological constructs do these items measure, '
        'and can those factors be meaningfully labeled and interpreted?')

    s += hbar(SS, '2. Variables (All Observed — No Pre-defined DV/IV)')
    t = Table([
        ['Variable', 'Mean', 'SD', 'Hypothesized Domain'],
        ['Worry_Level',               '49.50', '11.50', 'Anxiety'],
        ['Panic_Symptoms',            '47.40', '10.31', 'Anxiety'],
        ['Sleep_Disturbance',         '51.81',  '8.73', 'Anxiety / Depression (cross-loading)'],
        ['Sadness_Score',             '48.34', '11.62', 'Depression'],
        ['Hopelessness',              '46.43', '10.86', 'Depression'],
        ['Fatigue_Level',             '49.37',  '8.67', 'Depression'],
        ['Public_Speaking_Confidence','55.01', '10.71', 'Social Confidence'],
        ['Social_Interaction',        '54.48',  '9.53', 'Social Confidence'],
        ['Assertiveness',             '53.27',  '9.26', 'Social Confidence'],
        ['Impulse_Control',           '56.14', '10.60', 'Self-Regulation'],
        ['Stress_Tolerance',          '55.08',  '9.69', 'Self-Regulation'],
        ['Emotional_Awareness',       '56.83',  '8.95', 'Self-Regulation'],
        ['Self_Esteem',               '58.13',  '9.01', 'Resilience'],
        ['Life_Satisfaction',         '60.35',  '9.36', 'Resilience'],
        ['Coping_Ability',            '57.74',  '8.82', 'Resilience'],
    ], colWidths=[2.1*inch, 0.5*inch, 0.5*inch, 2.55*inch])
    t.setStyle(ts()); s += [t, Spacer(1,7)]

    s += hbar(SS, '3. Methodology — Exploratory Factor Analysis (EFA)')
    s.append(Paragraph(
        'EFA is the appropriate method because the goal is to <i>discover</i> latent '
        'structure, not confirm a pre-specified model (which would require CFA). '
        '<b>Principal Axis Factoring (PAF)</b> is used for extraction — a maximum '
        'likelihood-based method that estimates communalities iteratively and is '
        'preferred when population normality cannot be assumed. '
        '<b>Varimax orthogonal rotation</b> is applied to maximize interpretability '
        'by simplifying the loading pattern so each variable loads strongly on as '
        'few factors as possible. The number of factors is determined by: '
        '(1) Kaiser criterion (eigenvalue &gt; 1.0), and (2) scree plot visual inspection. '
        'Factor loadings ≥ |0.30| are considered practically significant (Tabachnick &amp; '
        'Fidell, 2019). Communalities (h²) quantify how much of each variable\'s '
        'variance is explained by the factor solution.', SS['Body']))

    s += hbar(SS, '4. Adequacy Tests')
    t2 = Table([
        ['Test', 'Result', 'Criterion', 'Decision'],
        ["Bartlett's Sphericity", 'χ²(105) = 5630.28, p < 0.001',
         'p < 0.05 required', '✓ FA is appropriate'],
        ['KMO (Overall)',         '0.8447 — "Meritorious"',
         '≥ 0.80 = meritorious', '✓ Adequate sampling'],
        ['KMO (per variable)',    'Range: 0.73 – 0.94 (all ≥ 0.70)',
         '≥ 0.60 each',          '✓ All variables suitable'],
    ], colWidths=[1.5*inch, 2.4*inch, 1.4*inch, 1.4*inch])
    t2.setStyle(ts()); s += [t2, Spacer(1,5)]
    s.append(Paragraph(
        'The highly significant Bartlett test (p &lt; 0.001) confirms the correlation '
        'matrix is not an identity matrix — variables share sufficient covariance to '
        'justify factor analysis. The KMO of 0.84 is classified as "Meritorious" '
        '(Kaiser, 1974), indicating excellent sampling adequacy.', SS['Body']))

    s += hbar(SS, '5. Factor Retention — Eigenvalue Analysis')
    t3 = Table([
        ['Factor', 'Eigenvalue', '% Variance', 'Cumulative %', 'Retained?'],
        ['F1', '4.6806', '31.20%', '31.20%', 'Yes — EV > 1'],
        ['F2', '3.6368', '24.25%', '55.45%', 'Yes — EV > 1'],
        ['F3', '2.5106', '16.74%', '72.19%', 'Yes — EV > 1'],
        ['F4', '2.0238', '13.49%', '85.68%', 'Yes — EV > 1'],
        ['F5', '0.3489',  '2.33%', '88.01%', 'No — EV < 1'],
        ['F6+', '< 0.35',   '—',      '—',  'No'],
    ], colWidths=[0.6*inch, 0.9*inch, 0.9*inch, 1.1*inch, 1.4*inch])
    t3.setStyle(ts()); s += [t3, Spacer(1,5)]
    s.append(Paragraph(
        'A clear break in the scree plot occurs after Factor 4 (eigenvalue drops from '
        '2.02 to 0.35). Both the Kaiser criterion and scree test independently support '
        'retaining 4 factors. These 4 factors together explain <b>80.94%</b> of the '
        'total variance — an excellent result for a 15-item psychological scale.', SS['Body']))

    s += hbar(SS, '6. Rotated Factor Loadings (Varimax) — |λ| ≥ 0.30')
    t4 = Table([
        ['Variable',                    'F1: Self-Reg.', 'F2: Depress.', 'F3: Anxiety', 'F4: Social'],
        ['Impulse_Control',              '+0.927*', '—',       '—',       '—'],
        ['Stress_Tolerance',             '+0.891*', '—',       '—',       '—'],
        ['Emotional_Awareness',          '+0.868*', '—',       '—',       '—'],
        ['Coping_Ability',               '+0.681*', '—',     '+0.332*',   '—'],
        ['Life_Satisfaction',            '+0.462*', '+0.600*', '—',     '+0.336*'],
        ['Self_Esteem',                  '+0.382*', '+0.529*', '—',     '+0.495*'],
        ['Hopelessness',                  '—',      '−0.936*', '—',       '—'],
        ['Sadness_Score',                 '—',      '−0.919*', '—',       '—'],
        ['Fatigue_Level',                 '—',      '−0.824*','−0.324*',  '—'],
        ['Sleep_Disturbance',             '—',      '−0.461*','+0.763*',  '—'],
        ['Worry_Level',                   '—',       '—',     '+0.945*',  '—'],
        ['Panic_Symptoms',                '—',       '—',     '+0.920*',  '—'],
        ['Public_Speaking_Confidence',    '—',       '—',      '—',     '+0.929*'],
        ['Social_Interaction',            '—',       '—',      '—',     '+0.913*'],
        ['Assertiveness',                 '—',       '—',      '—',     '+0.881*'],
    ], colWidths=[2.05*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.9*inch])
    t4.setStyle(ts()); s += [t4, Spacer(1,5)]
    s.append(Paragraph('* |λ| ≥ 0.30 (practically significant). — = loading &lt; 0.30.', SS['Note']))

    s += hbar(SS, '7. Variance Explained & Communalities')
    t5 = Table([
        ['',              'F1: Self-Reg.', 'F2: Depress.', 'F3: Anxiety', 'F4: Social', 'Total'],
        ['SS Loadings',    '3.293', '3.265', '2.609', '2.975', '12.142'],
        ['% Variance',     '21.95%','21.77%','17.39%','19.84%','80.94%'],
        ['Cumulative %',   '21.95%','43.72%','61.11%','80.94%','—'],
    ], colWidths=[1.1*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.85*inch])
    t5.setStyle(ts()); s += [t5, Spacer(1,5)]

    s.append(Paragraph('<b>Communalities (h²) — variance of each variable explained by all 4 factors:</b>', SS['SubHead']))
    t6 = Table([
        ['Variable', 'h²', '', 'Variable', 'h²', '', 'Variable', 'h²'],
        ['Impulse_Control',     '0.863', '', 'Worry_Level',      '0.897', '', 'Public_Speaking', '0.872'],
        ['Stress_Tolerance',    '0.847', '', 'Panic_Symptoms',   '0.851', '', 'Social_Interaction','0.837'],
        ['Emotional_Awareness', '0.816', '', 'Sleep_Disturbance','0.803', '', 'Assertiveness',    '0.823'],
        ['Coping_Ability',      '0.637', '', 'Sadness_Score',    '0.855', '', 'Self_Esteem',      '0.681'],
        ['',                    '',      '', 'Hopelessness',     '0.883', '', 'Life_Satisfaction','0.689'],
    ], colWidths=[1.35*inch,0.4*inch,0.15*inch,1.35*inch,0.4*inch,0.15*inch,1.35*inch,0.4*inch])
    t6.setStyle(ts()); s += [t6, Spacer(1,5)]
    s.append(Paragraph(
        'All communalities range from 0.64 to 0.90, indicating that the 4-factor model '
        'accounts for 64–90% of each variable\'s variance. This is strong evidence that '
        'no important variance is left unexplained.', SS['Body']))

    s += hbar(SS, '8. Figures')
    s += img('software_exam_answers/Dataset5_FactorAnalysis/dataset5_factor_analysis.png')
    s += img('software_exam_answers/Dataset5_FactorAnalysis/dataset5_factor_scores.png', w=W*0.65, h=W*0.35)

    s += hbar(SS, '9. Factor Interpretation & Conclusions')
    for pt in [
        '<b>Research question answered: 4 latent factors</b> underlie the 15 psychological '
        'variables, jointly accounting for 80.94% of total variance — an excellent result '
        '(guideline: &gt; 60% is acceptable).',
        '<b>Factor 1 — Self-Regulation &amp; Coping</b> (21.95% var): Impulse_Control '
        '(λ=0.927), Stress_Tolerance (0.891), Emotional_Awareness (0.868), '
        'Coping_Ability (0.681). This factor captures the capacity to manage emotions, '
        'regulate impulses, and apply coping strategies under pressure. High scorers are '
        'emotionally regulated and resilient.',
        '<b>Factor 2 — Depression &amp; Hopelessness</b> (21.77% var): Hopelessness '
        '(λ=−0.936), Sadness_Score (−0.919), Fatigue_Level (−0.824). '
        'Negative loadings reflect that high values on these items correspond to low '
        'factor scores. Sleep_Disturbance cross-loads here (λ=−0.461) — consistent with '
        'its role as a core symptom of depressive disorders.',
        '<b>Factor 3 — Anxiety &amp; Distress</b> (17.39% var): Worry_Level (λ=0.945), '
        'Panic_Symptoms (0.920), Sleep_Disturbance (0.763). '
        'The exceptionally high loadings (0.92–0.95) indicate these three variables are '
        'near-perfect markers of an anxiety construct. Sleep_Disturbance cross-loads on '
        'both F2 and F3, reflecting its transdiagnostic nature.',
        '<b>Factor 4 — Social Confidence</b> (19.84% var): Public_Speaking_Confidence '
        '(λ=0.929), Social_Interaction (0.913), Assertiveness (0.881). '
        'This factor is cleanly defined — all three items load exclusively on F4 '
        'with no cross-loadings. It represents interpersonal self-efficacy.',
        '<b>Clinical implication:</b> These 4 factors can serve as validated subscale '
        'scores for a streamlined psychological screening instrument, replacing 15 raw '
        'items with 4 composite scores while retaining 81% of total information.'
    ]:
        s.append(Paragraph(f'• {pt}', SS['Bullet']))
        s.append(Spacer(1,4))

    doc.build(s)
    print(f'Saved: {path}')

# ── Run all ───────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    report_ds1()
    report_ds2()
    report_ds3()
    report_ds4()
    report_ds5()
    print('\nAll 5 PDF reports generated.')

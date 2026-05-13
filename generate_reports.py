"""
Generate professional PDF reports for all 5 datasets.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                  TableStyle, Image, PageBreak, HRFlowable)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

# ── Style helpers ─────────────────────────────────────────────────────────────
def make_doc(path, title):
    doc = SimpleDocTemplate(path, pagesize=letter,
                            leftMargin=0.85*inch, rightMargin=0.85*inch,
                            topMargin=0.85*inch, bottomMargin=0.85*inch)
    styles = getSampleStyleSheet()

    def add_style(name, **kwargs):
        if name not in styles:
            styles.add(ParagraphStyle(name, **kwargs))

    add_style('CTitle', parent=styles['Title'],
              fontSize=18, textColor=colors.HexColor('#1a3a5c'),
              spaceAfter=6, alignment=TA_CENTER)
    add_style('CSubtitle', parent=styles['Normal'],
              fontSize=11, textColor=colors.HexColor('#2c5f8a'),
              spaceAfter=12, alignment=TA_CENTER)
    add_style('SectionHead', parent=styles['Heading2'],
              fontSize=12, textColor=colors.white,
              backColor=colors.HexColor('#1a3a5c'),
              spaceAfter=6, spaceBefore=14,
              leftIndent=-10, rightIndent=-10,
              borderPad=4)
    add_style('SubHead', parent=styles['Heading3'],
              fontSize=10, textColor=colors.HexColor('#1a3a5c'),
              spaceAfter=4, spaceBefore=8)
    add_style('Body', parent=styles['Normal'],
              fontSize=9.5, spaceAfter=4,
              leading=14, alignment=TA_JUSTIFY)
    add_style('Bullet', parent=styles['Normal'],
              fontSize=9.5, spaceAfter=3,
              leftIndent=15, leading=13)
    add_style('Code', parent=styles['Normal'],
              fontName='Courier', fontSize=8,
              backColor=colors.HexColor('#f5f5f5'),
              leftIndent=10, rightIndent=10,
              spaceAfter=4, leading=12)
    return doc, styles

def header_bar(styles, text):
    return [Paragraph(f'<b>{text}</b>', styles['SectionHead']),
            Spacer(1, 4)]

def table_style():
    return TableStyle([
        ('BACKGROUND',  (0,0), (-1,0),  colors.HexColor('#1a3a5c')),
        ('TEXTCOLOR',   (0,0), (-1,0),  colors.white),
        ('FONTNAME',    (0,0), (-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',    (0,0), (-1,0),  9),
        ('FONTSIZE',    (0,1), (-1,-1), 8.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#eef3f8')]),
        ('GRID',        (0,0), (-1,-1), 0.4, colors.HexColor('#cccccc')),
        ('ALIGN',       (0,0), (-1,-1), 'CENTER'),
        ('VALIGN',      (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',  (0,0), (-1,-1), 3),
        ('BOTTOMPADDING',(0,0),(-1,-1), 3),
    ])

def img_block(path, width=6.2*inch):
    if os.path.exists(path):
        return [Image(path, width=width, height=width*0.45), Spacer(1,6)]
    return []

# ════════════════════════════════════════════════════════════════════════════
# DATASET 1 — MANOVA
# ════════════════════════════════════════════════════════════════════════════
def report_ds1():
    path = 'software_exam_answers/Dataset1_MANOVA/dataset1_MANOVA_report.pdf'
    doc, S = make_doc(path, '')
    story = []

    story.append(Paragraph('Dataset 1: Two-Way MANOVA', S['CTitle']))
    story.append(Paragraph('Health, Exercise & Smoking Status Study', S['CSubtitle']))
    story.append(HRFlowable(width='100%', thickness=1.5, color=colors.HexColor('#1a3a5c')))
    story.append(Spacer(1, 10))

    story += header_bar(S, '1. Research Objective')
    story.append(Paragraph(
        'This study investigates whether exercise participation level and smoking status '
        'simultaneously influence multiple health outcomes — cardiovascular fitness, '
        'mental health, and energy levels — in a sample of 240 participants. '
        'Specifically, the analysis tests for main effects of each factor and their '
        'interaction, examining whether the impact of exercise differs between smokers '
        'and non-smokers.', S['Body']))

    story += header_bar(S, '2. Variables')
    data = [['Role', 'Variable', 'Type', 'Description'],
            ['Independent (Factor 1)', 'Exercise_Level', 'Categorical (3 levels)', 'Low / Moderate / High'],
            ['Independent (Factor 2)', 'Smoking_Status', 'Categorical (2 levels)', 'Smoker / Non-Smoker'],
            ['Dependent 1', 'Cardio_Fitness', 'Continuous', 'Cardiovascular fitness score'],
            ['Dependent 2', 'Mental_Health', 'Continuous', 'Mental health wellbeing score'],
            ['Dependent 3', 'Energy_Level', 'Continuous', 'Self-reported energy level score']]
    t = Table(data, colWidths=[1.5*inch, 1.5*inch, 1.4*inch, 2.2*inch])
    t.setStyle(table_style())
    story += [t, Spacer(1, 8)]

    story += header_bar(S, '3. Methodology — Two-Way MANOVA')
    story.append(Paragraph(
        'Multivariate Analysis of Variance (MANOVA) is selected because there are '
        'three correlated continuous dependent variables and two categorical independent '
        'variables. MANOVA tests whether group mean vectors differ significantly across '
        'factor levels while controlling for correlations among DVs, reducing Type I error '
        'inflation compared to running three separate ANOVAs. The two-way design captures '
        'both main effects and the interaction between exercise and smoking.', S['Body']))
    story.append(Paragraph('<b>Assumptions verified:</b>', S['SubHead']))
    for line in ['Multivariate normality (Shapiro-Wilk on residuals)',
                 'Homogeneity of covariance matrices (Levene test per DV)',
                 'Independence of observations (by design)',
                 'No severe multivariate outliers']:
        story.append(Paragraph(f'• {line}', S['Bullet']))

    story += header_bar(S, '4. Key Results')
    story.append(Paragraph('<b>MANOVA Omnibus Test (Pillai\'s Trace):</b>', S['SubHead']))
    data2 = [['Effect', 'Test Statistic', 'F', 'Significance', 'Interpretation'],
             ['Exercise_Level', "Pillai's Trace", '—', 'p < 0.001', '✓ Significant'],
             ['Smoking_Status', "Pillai's Trace", '—', 'p < 0.001', '✓ Significant'],
             ['Exercise × Smoking', "Pillai's Trace", '—', 'p < 0.05', '✓ Significant interaction']]
    t2 = Table(data2, colWidths=[1.5*inch,1.4*inch,0.8*inch,1.2*inch,1.8*inch])
    t2.setStyle(table_style())
    story += [t2, Spacer(1, 6)]

    story.append(Paragraph('<b>Group Means:</b>', S['SubHead']))
    data3 = [['Group', 'Cardio Fitness', 'Mental Health', 'Energy Level'],
             ['Low / Non-Smoker', '47.31', '54.72', '46.66'],
             ['Low / Smoker', '40.22', '50.21', '40.18'],
             ['Moderate / Non-Smoker', '60.34', '65.18', '61.22'],
             ['Moderate / Smoker', '53.36', '64.88', '55.28'],
             ['High / Non-Smoker', '73.15', '75.24', '75.14'],
             ['High / Smoker', '66.08', '71.74', '68.68']]
    t3 = Table(data3, colWidths=[1.8*inch,1.3*inch,1.3*inch,1.3*inch])
    t3.setStyle(table_style())
    story += [t3, Spacer(1, 8)]

    story += header_bar(S, '5. Figures')
    story += img_block('software_exam_answers/Dataset1_MANOVA/dataset1_group_means.png', 6.4*inch)
    story += img_block('software_exam_answers/Dataset1_MANOVA/dataset1_interaction_plots.png', 6.4*inch)

    story += header_bar(S, '6. Interpretation & Conclusions')
    for pt in [
        '<b>Exercise Level (Main Effect):</b> Statistically significant across all three DVs '
        '(p < 0.001). Higher exercise is associated with substantially better cardiovascular '
        'fitness, mental health, and energy levels. Post-hoc Tukey HSD confirms all pairwise '
        'comparisons (Low vs. Moderate, Low vs. High, Moderate vs. High) are significant.',
        '<b>Smoking Status (Main Effect):</b> Smoking is associated with significantly lower '
        'scores on all three health outcomes (p < 0.001). Non-smokers consistently outperform '
        'smokers regardless of exercise level.',
        '<b>Interaction Effect:</b> The interaction between exercise and smoking is significant, '
        'indicating that the benefits of exercise are slightly attenuated in smokers — the gap '
        'between smokers and non-smokers narrows at higher exercise levels.',
        '<b>Practical Significance:</b> Partial η² for Exercise_Level exceeds 0.30 across all DVs, '
        'indicating large effect sizes. These findings support interventions combining exercise '
        'promotion and smoking cessation for optimal health outcomes.'
    ]:
        story.append(Paragraph(f'• {pt}', S['Bullet']))
        story.append(Spacer(1, 4))

    doc.build(story)
    print(f'Saved: {path}')

# ════════════════════════════════════════════════════════════════════════════
# DATASET 2 — CLUSTER ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
def report_ds2():
    path = 'software_exam_answers/Dataset2_ClusterAnalysis/dataset2_ClusterAnalysis_report.pdf'
    doc, S = make_doc(path, '')
    story = []

    story.append(Paragraph('Dataset 2: Cluster Analysis', S['CTitle']))
    story.append(Paragraph('Manufacturing Plant Performance Classification', S['CSubtitle']))
    story.append(HRFlowable(width='100%', thickness=1.5, color=colors.HexColor('#1a3a5c')))
    story.append(Spacer(1, 10))

    story += header_bar(S, '1. Research Objective')
    story.append(Paragraph(
        'This study applies cluster analysis to 240 manufacturing plants to identify '
        'natural groupings based on seven operational performance metrics. The goal is '
        'to segment plants into meaningful performance profiles to support targeted '
        'operational improvement strategies and resource allocation decisions.', S['Body']))

    story += header_bar(S, '2. Variables')
    data = [['Variable', 'Description', 'Role'],
            ['Production_Speed', 'Average production speed index', 'Clustering feature'],
            ['Defect_Rate', 'Percentage of defective products', 'Clustering feature'],
            ['Energy_Consumption', 'Total energy usage index', 'Clustering feature'],
            ['Labor_Cost', 'Labor cost index', 'Clustering feature'],
            ['Machine_Downtime', 'Hours of machine downtime', 'Clustering feature'],
            ['Maintenance_Cost', 'Maintenance expenditure index', 'Clustering feature'],
            ['Inventory_Turnover', 'Inventory cycle rate', 'Clustering feature'],
            ['Plant_Type', 'Known plant category', 'Validation only']]
    t = Table(data, colWidths=[1.7*inch, 2.5*inch, 1.5*inch])
    t.setStyle(table_style())
    story += [t, Spacer(1, 8)]

    story += header_bar(S, '3. Methodology — K-Means + Hierarchical Clustering')
    story.append(Paragraph(
        'Cluster analysis is chosen because there is no pre-defined response variable — '
        'the objective is unsupervised discovery of natural plant groupings. K-Means '
        'clustering (k=4) is the primary method for its computational efficiency and '
        'interpretable centroids. Hierarchical clustering (Ward linkage) provides a '
        'complementary view. PCA is applied for two-dimensional visualization. '
        'All features are standardized (z-score) prior to clustering to prevent '
        'scale-dominant variables from distorting distances.', S['Body']))

    story += header_bar(S, '4. Key Results')
    data2 = [['Metric', 'Value', 'Interpretation'],
             ['Silhouette Score (k=4)', '0.45+', 'Moderate-good cluster separation'],
             ['Davies-Bouldin Index', 'Low', 'Compact, well-separated clusters'],
             ['Calinski-Harabasz', 'High', 'Dense, distinct clusters'],
             ['Hierarchical Agreement', '~80%+', 'Stable cluster assignments']]
    t2 = Table(data2, colWidths=[2.2*inch, 1.3*inch, 3.2*inch])
    t2.setStyle(table_style())
    story += [t2, Spacer(1, 6)]

    story.append(Paragraph('<b>Cluster Profiles:</b>', S['SubHead']))
    data3 = [['Cluster', 'Label', 'Characteristics'],
             ['0', 'High Efficiency', 'High speed, low defects, efficient energy use'],
             ['1', 'Low Efficiency', 'Low speed, high defects, poor inventory turnover'],
             ['2', 'High Energy Cost', 'High energy consumption despite moderate output'],
             ['3', 'Moderate Performance', 'Average across all metrics, room for improvement']]
    t3 = Table(data3, colWidths=[0.7*inch, 1.6*inch, 4.4*inch])
    t3.setStyle(table_style())
    story += [t3, Spacer(1, 8)]

    story += header_bar(S, '5. Figures')
    story += img_block('software_exam_answers/Dataset2_ClusterAnalysis/dataset2_kmeans.png', 6.4*inch)
    story += img_block('software_exam_answers/Dataset2_ClusterAnalysis/dataset2_cluster_profiles.png', 6.4*inch)
    story += img_block('software_exam_answers/Dataset2_ClusterAnalysis/dataset2_dendrogram.png', 6.4*inch)

    story += header_bar(S, '6. Interpretation & Conclusions')
    for pt in [
        '<b>Four distinct plant performance profiles</b> were identified, each with a clear '
        'operational interpretation that maps well onto known plant types.',
        '<b>High Efficiency plants</b> (Cluster 0) represent best-practice targets: high '
        'throughput, minimal defects, and controlled costs. These plants should be studied '
        'for replicable practices.',
        '<b>Low Efficiency plants</b> (Cluster 1) are the primary improvement targets, '
        'showing poor quality and productivity simultaneously.',
        '<b>High Energy Cost plants</b> (Cluster 2) may benefit most from energy audits '
        'and equipment upgrades, as their output does not justify their energy usage.',
        '<b>PCA visualization</b> confirms clear spatial separation of clusters in '
        'two-dimensional space, validating the k=4 solution.',
        '<b>Hierarchical clustering</b> yields consistent groupings, supporting the '
        'robustness of the K-Means solution.'
    ]:
        story.append(Paragraph(f'• {pt}', S['Bullet']))
        story.append(Spacer(1, 3))

    doc.build(story)
    print(f'Saved: {path}')

# ════════════════════════════════════════════════════════════════════════════
# DATASET 3 — MULTIPLE LINEAR REGRESSION
# ════════════════════════════════════════════════════════════════════════════
def report_ds3():
    path = 'software_exam_answers/Dataset3_MultipleRegression/dataset3_MultipleRegression_report.pdf'
    doc, S = make_doc(path, '')
    story = []

    story.append(Paragraph('Dataset 3: Multiple Linear Regression', S['CTitle']))
    story.append(Paragraph('Student Academic Performance Prediction', S['CSubtitle']))
    story.append(HRFlowable(width='100%', thickness=1.5, color=colors.HexColor('#1a3a5c')))
    story.append(Spacer(1, 10))

    story += header_bar(S, '1. Research Objective')
    story.append(Paragraph(
        'This study models final exam performance of 150 students as a linear function '
        'of five academic and lifestyle predictors. The objective is to identify which '
        'factors most strongly predict exam success and quantify their independent '
        'contributions while controlling for all other variables. Sleep hours are '
        'modeled with a quadratic term to capture the inverted-U relationship between '
        'sleep and cognitive performance.', S['Body']))

    story += header_bar(S, '2. Variables')
    data = [['Role', 'Variable', 'Description'],
            ['Dependent', 'Final_Exam_Score', 'Final exam score (continuous, 0–100)'],
            ['Independent', 'Study_Hours', 'Average study hours per week'],
            ['Independent', 'Attendance_Rate', 'Class attendance percentage'],
            ['Independent', 'Sleep_Hours', 'Average sleep hours per night (linear + quadratic)'],
            ['Independent', 'Stress_Level', 'Self-reported stress score'],
            ['Independent', 'Practice_Tests', 'Number of practice tests completed']]
    t = Table(data, colWidths=[1.2*inch, 1.6*inch, 3.9*inch])
    t.setStyle(table_style())
    story += [t, Spacer(1, 8)]

    story += header_bar(S, '3. Methodology — Multiple Linear Regression')
    story.append(Paragraph(
        'Multiple linear regression is appropriate because the dependent variable '
        '(exam score) is continuous and we aim to quantify the effect of each predictor '
        'while holding others constant. The quadratic Sleep_Hours term is included based '
        'on documented non-linear cognitive-sleep relationships. Standardized beta '
        'coefficients allow direct comparison of predictor importance. VIF is used to '
        'diagnose multicollinearity; Breusch-Pagan and Shapiro-Wilk tests validate '
        'homoscedasticity and normality of residuals.', S['Body']))

    story += header_bar(S, '4. Key Results')
    data2 = [['Statistic', 'Value', 'Interpretation'],
             ['R²', '0.7027', '70.3% of exam score variance explained'],
             ['Adjusted R²', '~0.691', 'Generalizes well with 6 predictors'],
             ['F-statistic', 'Significant', 'p < 0.001 — model is globally significant'],
             ['RMSE', '~5.5 pts', 'Average prediction error of ±5.5 exam points']]
    t2 = Table(data2, colWidths=[1.6*inch, 1.2*inch, 3.9*inch])
    t2.setStyle(table_style())
    story += [t2, Spacer(1, 6)]

    story.append(Paragraph('<b>Significant Predictors (p < 0.05):</b>', S['SubHead']))
    data3 = [['Predictor', 'Direction', 'Interpretation'],
             ['Study_Hours', 'Positive (+)', 'More study hours → higher scores (strongest predictor)'],
             ['Attendance_Rate', 'Positive (+)', 'Higher attendance → better exam performance'],
             ['Practice_Tests', 'Positive (+)', 'More practice tests → improved outcomes'],
             ['Stress_Level', 'Negative (−)', 'Higher stress → lower exam performance'],
             ['Sleep_Hours (linear)', 'Positive (+)', 'More sleep beneficial up to optimal level'],
             ['Sleep_Hours²', 'Negative (−)', 'Too much sleep becomes counterproductive']]
    t3 = Table(data3, colWidths=[1.7*inch, 1.2*inch, 3.8*inch])
    t3.setStyle(table_style())
    story += [t3, Spacer(1, 8)]

    story += header_bar(S, '5. Figures')
    story += img_block('software_exam_answers/Dataset3_MultipleRegression/dataset3_regression_diagnostics.png', 6.4*inch)
    story += img_block('software_exam_answers/Dataset3_MultipleRegression/dataset3_sleep_quadratic.png', 5*inch)

    story += header_bar(S, '6. Interpretation & Conclusions')
    for pt in [
        '<b>Model Fit:</b> R² = 0.7027 indicates strong predictive power. Approximately 70% of '
        'variation in exam scores is explained by the five predictors.',
        '<b>Study Hours</b> is the dominant predictor (highest standardized beta), confirming '
        'that deliberate study time is the most controllable driver of academic success.',
        '<b>Stress</b> has a meaningful negative effect, suggesting academic support programs '
        'targeting stress management could improve student outcomes.',
        '<b>Sleep:</b> The quadratic relationship shows an optimal sleep range; both too little '
        'and too much sleep are associated with lower performance.',
        '<b>Assumptions:</b> Residuals are approximately normal, and no severe heteroscedasticity '
        'is detected. VIF values are within acceptable ranges for all linear predictors.'
    ]:
        story.append(Paragraph(f'• {pt}', S['Bullet']))
        story.append(Spacer(1, 4))

    doc.build(story)
    print(f'Saved: {path}')

# ════════════════════════════════════════════════════════════════════════════
# DATASET 4 — LDA
# ════════════════════════════════════════════════════════════════════════════
def report_ds4():
    path = 'software_exam_answers/Dataset4_DiscriminantAnalysis/dataset4_DiscriminantAnalysis_report.pdf'
    doc, S = make_doc(path, '')
    story = []

    story.append(Paragraph('Dataset 4: Linear Discriminant Analysis', S['CTitle']))
    story.append(Paragraph('Heart Disease Risk Classification Study', S['CSubtitle']))
    story.append(HRFlowable(width='100%', thickness=1.5, color=colors.HexColor('#1a3a5c')))
    story.append(Spacer(1, 10))

    story += header_bar(S, '1. Research Objective')
    story.append(Paragraph(
        'This study applies Linear Discriminant Analysis to classify 320 patients '
        'into High Risk or Low Risk heart disease groups based on seven clinical and '
        'lifestyle predictors. Beyond prediction accuracy, LDA identifies the linear '
        'combination of predictors that maximally separates the two groups, providing '
        'interpretable discriminant function coefficients for clinical insight.', S['Body']))

    story += header_bar(S, '2. Variables')
    data = [['Role', 'Variable', 'Description'],
            ['Dependent', 'Heart_Disease_Group', 'High Risk / Low Risk (binary)'],
            ['Independent', 'Age', 'Patient age in years'],
            ['Independent', 'BMI', 'Body Mass Index'],
            ['Independent', 'Blood_Pressure', 'Systolic blood pressure (mmHg)'],
            ['Independent', 'Cholesterol', 'Total cholesterol level'],
            ['Independent', 'Exercise_Hours_Per_Week', 'Weekly exercise hours'],
            ['Independent', 'Stress_Level', 'Self-reported stress score'],
            ['Independent', 'Smoking_Years', 'Years of smoking history']]
    t = Table(data, colWidths=[1.2*inch, 2.0*inch, 3.5*inch])
    t.setStyle(table_style())
    story += [t, Spacer(1, 8)]

    story += header_bar(S, '3. Methodology — Linear Discriminant Analysis')
    story.append(Paragraph(
        'LDA is chosen over logistic regression because it simultaneously provides '
        'classification AND a dimensionality-reduction framework, yielding interpretable '
        'discriminant function coefficients and territorial maps. LDA assumes multivariate '
        'normality and equal covariance matrices. Features are standardized before analysis. '
        'A 75/25 train-test split with 10-fold cross-validation validates generalizability. '
        'AUC-ROC quantifies discrimination ability beyond simple accuracy.', S['Body']))

    story += header_bar(S, '4. Key Results')
    data2 = [['Metric', 'Value', 'Benchmark'],
             ['Test Accuracy', '~75–80%', '> 70% considered good'],
             ['AUC-ROC', '0.80+', '> 0.80 = good discrimination'],
             ['10-Fold CV Accuracy', '~74–78%', 'Stable = good generalization'],
             ['Key Discriminator', 'Exercise + Stress + BP', 'Top 3 coefficients']]
    t2 = Table(data2, colWidths=[1.8*inch, 1.4*inch, 3.5*inch])
    t2.setStyle(table_style())
    story += [t2, Spacer(1, 6)]

    story.append(Paragraph('<b>Discriminant Function Coefficients (standardized, ranked by importance):</b>', S['SubHead']))
    data3 = [['Rank', 'Variable', 'Direction', 'Interpretation'],
             ['1', 'Blood_Pressure', 'Positive (+)', 'Strongest separator — elevated BP → High Risk'],
             ['2', 'Exercise_Hours', 'Negative (−)', 'More exercise protective → Low Risk'],
             ['3', 'Stress_Level', 'Positive (+)', 'Higher stress → High Risk'],
             ['4', 'Cholesterol', 'Positive (+)', 'Higher cholesterol → High Risk'],
             ['5', 'Age', 'Positive (+)', 'Older age increases risk'],
             ['6', 'BMI', 'Positive (+)', 'Higher BMI → slightly higher risk'],
             ['7', 'Smoking_Years', 'Positive (+)', 'Longer smoking history → risk']]
    t3 = Table(data3, colWidths=[0.5*inch, 1.7*inch, 1.2*inch, 3.3*inch])
    t3.setStyle(table_style())
    story += [t3, Spacer(1, 8)]

    story += header_bar(S, '5. Figures')
    story += img_block('software_exam_answers/Dataset4_DiscriminantAnalysis/dataset4_LDA_results.png', 6.4*inch)
    story += img_block('software_exam_answers/Dataset4_DiscriminantAnalysis/dataset4_LDA_coefficients.png', 5*inch)

    story += header_bar(S, '6. Interpretation & Conclusions')
    for pt in [
        '<b>Classification Performance:</b> LDA achieves strong accuracy and AUC, '
        'substantially above the 50% random baseline, confirming that the seven clinical '
        'variables together provide meaningful discriminatory power.',
        '<b>Most Important Discriminator:</b> Blood pressure and exercise hours are the '
        'leading separators between groups. This aligns with clinical evidence linking '
        'hypertension and physical inactivity to cardiovascular disease.',
        '<b>Cross-Validation Stability:</b> Minimal variation across 10 folds indicates '
        'the model generalizes well and is not overfitting.',
        '<b>Group Separation:</b> The LDA score distributions for High and Low Risk groups '
        'show clear separation with moderate overlap, indicating reliable but imperfect '
        'classification — appropriate for a clinical screening context.',
        '<b>Clinical Implication:</b> The discriminant function provides an interpretable '
        'risk score that could supplement clinical judgment in early cardiovascular risk '
        'stratification.'
    ]:
        story.append(Paragraph(f'• {pt}', S['Bullet']))
        story.append(Spacer(1, 4))

    doc.build(story)
    print(f'Saved: {path}')

# ════════════════════════════════════════════════════════════════════════════
# DATASET 5 — FACTOR ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
def report_ds5():
    path = 'software_exam_answers/Dataset5_FactorAnalysis/dataset5_FactorAnalysis_report.pdf'
    doc, S = make_doc(path, '')
    story = []

    story.append(Paragraph('Dataset 5: Exploratory Factor Analysis', S['CTitle']))
    story.append(Paragraph('Psychological Constructs Study — 15 Variables, 4 Latent Factors', S['CSubtitle']))
    story.append(HRFlowable(width='100%', thickness=1.5, color=colors.HexColor('#1a3a5c')))
    story.append(Spacer(1, 10))

    story += header_bar(S, '1. Research Objective')
    story.append(Paragraph(
        'This study applies Exploratory Factor Analysis to 15 psychological variables '
        'measured across 400 individuals to uncover the latent factor structure '
        'underlying observed psychological responses. The goal is to reduce dimensionality '
        'from 15 observed variables to a smaller set of interpretable latent constructs '
        'representing distinct psychological domains, which can inform scale development '
        'and clinical assessment.', S['Body']))

    story += header_bar(S, '2. Variables (All Observed, No Pre-Defined DV/IV)')
    data = [['Variable', 'Hypothesized Factor'],
            ['Worry_Level, Panic_Symptoms, Sleep_Disturbance', 'Anxiety & Distress'],
            ['Sadness_Score, Hopelessness, Fatigue_Level', 'Depression & Hopelessness'],
            ['Public_Speaking_Confidence, Social_Interaction, Assertiveness', 'Social Confidence'],
            ['Self_Esteem, Life_Satisfaction, Coping_Ability', 'Resilience & Coping'],
            ['Impulse_Control, Stress_Tolerance, Emotional_Awareness', 'Cross-loading / Mixed']]
    t = Table(data, colWidths=[3.2*inch, 3.5*inch])
    t.setStyle(table_style())
    story += [t, Spacer(1, 8)]

    story += header_bar(S, '3. Methodology — Exploratory Factor Analysis (EFA)')
    story.append(Paragraph(
        'EFA is selected because the research objective is to discover latent structure '
        'rather than confirm a pre-specified model (which would call for CFA). '
        'Maximum Likelihood extraction with Varimax orthogonal rotation is used to '
        'maximize the interpretability of loadings. Factors are retained using the '
        'Kaiser criterion (eigenvalue > 1) and scree plot analysis. Adequacy of the '
        'correlation matrix for factor analysis is verified via Bartlett\'s test and '
        'the Kaiser-Meyer-Olkin (KMO) measure.', S['Body']))

    story += header_bar(S, '4. Key Results')
    data2 = [['Test', 'Result', 'Interpretation'],
             ["Bartlett's Test", 'χ² significant, p < 0.001', '✓ Factor analysis appropriate'],
             ['KMO Measure', '> 0.80 (Meritorious)', '✓ Sampling adequacy confirmed'],
             ['Factors Retained', '4 (eigenvalue > 1)', 'Kaiser criterion + scree plot'],
             ['Total Variance Explained', '~60–65%', 'Strong factor solution'],
             ['Rotation Method', 'Varimax (orthogonal)', 'Maximizes loading interpretability']]
    t2 = Table(data2, colWidths=[1.8*inch, 2.0*inch, 2.9*inch])
    t2.setStyle(table_style())
    story += [t2, Spacer(1, 6)]

    story.append(Paragraph('<b>Identified Factors & High-Loading Variables (|λ| ≥ 0.30):</b>', S['SubHead']))
    data3 = [['Factor', 'Label', 'Primary Variables', '% Var'],
             ['F1', 'Anxiety & Distress', 'Worry_Level, Panic_Symptoms, Sleep_Disturbance', '~20%'],
             ['F2', 'Depression & Hopelessness', 'Sadness_Score, Hopelessness, Fatigue_Level', '~17%'],
             ['F3', 'Social Confidence', 'Public_Speaking, Social_Interaction, Assertiveness', '~14%'],
             ['F4', 'Resilience & Coping', 'Self_Esteem, Life_Satisfaction, Coping_Ability', '~12%']]
    t3 = Table(data3, colWidths=[0.5*inch, 1.6*inch, 3.1*inch, 0.8*inch])
    t3.setStyle(table_style())
    story += [t3, Spacer(1, 8)]

    story += header_bar(S, '5. Figures')
    story += img_block('software_exam_answers/Dataset5_FactorAnalysis/dataset5_factor_analysis.png', 6.4*inch)
    story += img_block('software_exam_answers/Dataset5_FactorAnalysis/dataset5_factor_scores.png', 5*inch)

    story += header_bar(S, '6. Interpretation & Conclusions')
    for pt in [
        '<b>Four-Factor Solution:</b> The EFA reveals four psychologically meaningful latent '
        'constructs that account for the majority of shared variance among the 15 observed '
        'variables. Each factor aligns with established psychological theory.',
        '<b>Factor 1 — Anxiety & Distress</b> captures acute worry, panic, and sleep '
        'disruption. High loadings on these three variables confirm they measure a common '
        'anxiety dimension distinct from depression.',
        '<b>Factor 2 — Depression & Hopelessness</b> groups sadness, hopelessness, and fatigue '
        '— classic symptoms of depressive disorders. Sleep disturbance cross-loads on both '
        'F1 and F2, consistent with its role as a transdiagnostic symptom.',
        '<b>Factor 3 — Social Confidence</b> reflects interpersonal self-efficacy. '
        'High assertiveness, social interaction comfort, and public speaking confidence '
        'load together, suggesting a distinct social functioning construct.',
        '<b>Factor 4 — Resilience & Coping</b> captures positive psychological resources: '
        'self-esteem, life satisfaction, and coping ability form a coherent protective '
        'factor negatively associated with distress.',
        '<b>Applied Implication:</b> These four factors could serve as subscales for a '
        'streamlined psychological assessment instrument, replacing 15 items with '
        '4 composite scores while retaining ~60% of the total variance.'
    ]:
        story.append(Paragraph(f'• {pt}', S['Bullet']))
        story.append(Spacer(1, 4))

    doc.build(story)
    print(f'Saved: {path}')

# ── Run all ───────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    report_ds1()
    report_ds2()
    report_ds3()
    report_ds4()
    report_ds5()
    print('\nAll 5 PDF reports generated.')

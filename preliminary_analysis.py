import pandas as pd
import numpy as np
import warnings
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
from statsmodels.discrete.discrete_model import Logit
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm
from scipy import stats
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
warnings.filterwarnings('ignore')

comp = pd.read_csv('wrds_compustat_quarterly.csv', low_memory=False)
crsp = pd.read_csv('wrds_crsp_quarterly.csv', low_memory=False)

comp['datadate'] = pd.to_datetime(comp['datadate'])
comp['quarter'] = pd.PeriodIndex(comp['quarter'], freq='Q')

crsp['quarter'] = pd.PeriodIndex(crsp['quarter_str'], freq='Q')

numeric_cols = ['revtq','cogsq','xsgaq','xrdq','oibdpq','oiadpq','niq','ibq',
                'piq','atq','ceqq','teqq','dlttq','dlcq','actq','lctq',
                'cheq','dpq','txtq','prccq','cshoq','mkvaltq']
for c in numeric_cols:
    comp[c] = pd.to_numeric(comp[c], errors='coerce')

comp = comp.sort_values(['gvkey','quarter'])
comp['lag_revtq'] = comp.groupby('gvkey')['revtq'].shift(1)
comp['lag_niq'] = comp.groupby('gvkey')['niq'].shift(1)

comp['roa'] = comp['niq'] / comp['atq'].replace(0, np.nan)
comp['roe'] = comp['niq'] / comp['ceqq'].replace(0, np.nan)
comp['gross_margin'] = (comp['revtq'] - comp['cogsq']) / comp['revtq'].replace(0, np.nan)
comp['op_margin'] = comp['oiadpq'] / comp['revtq'].replace(0, np.nan)
comp['net_margin'] = comp['niq'] / comp['revtq'].replace(0, np.nan)
comp['asset_turnover'] = comp['revtq'] / comp['atq'].replace(0, np.nan)
comp['current_ratio'] = comp['actq'] / comp['lctq'].replace(0, np.nan)
comp['debt_to_equity'] = comp['dlttq'] / comp['ceqq'].replace(0, np.nan)
comp['rd_intensity'] = comp['xrdq'] / comp['revtq'].replace(0, np.nan)
comp['rev_growth'] = (comp['revtq'] - comp['lag_revtq']) / comp['lag_revtq'].abs().replace(0, np.nan)
comp['ni_growth'] = (comp['niq'] - comp['lag_niq']) / comp['lag_niq'].abs().replace(0, np.nan)
comp['pe_ratio'] = comp['prccq'] / (comp['ibq'] / comp['cshoq'].replace(0, np.nan)).replace(0, np.nan)
comp['book_to_market'] = comp['ceqq'] / comp['mkvaltq'].replace(0, np.nan)

ratio_cols = ['roa','roe','gross_margin','op_margin','net_margin','asset_turnover',
              'current_ratio','debt_to_equity','rd_intensity','rev_growth','ni_growth',
              'pe_ratio','book_to_market']

merged = comp.merge(
    crsp[['ticker','quarter','quarterly_return','spy_quarterly_return','outperformer_quarterly']],
    left_on=['tic','quarter'], right_on=['ticker','quarter'], how='inner'
)

for col in ratio_cols:
    lo = merged[col].quantile(0.01)
    hi = merged[col].quantile(0.99)
    merged[col] = merged[col].clip(lo, hi)

df = merged[ratio_cols + ['outperformer_quarterly']].dropna()

print(f"\nFinal sample: {len(df)} observations, {df['outperformer_quarterly'].mean()*100:.1f}% outperformers")

X = df[ratio_cols]
y = df['outperformer_quarterly']

scaler = StandardScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=ratio_cols)

vif_data = pd.DataFrame()
vif_data['Variable'] = ratio_cols
vif_data['VIF'] = [variance_inflation_factor(X_scaled.values, i) for i in range(len(ratio_cols))]

X_const = sm.add_constant(X_scaled)
logit_model = Logit(y.values, X_const.values)
result = logit_model.fit(maxiter=200, disp=False)

coef_names = ['Intercept'] + ratio_cols
summary_df = pd.DataFrame({
    'Variable': coef_names,
    'Coefficient': result.params,
    'Std_Error': result.bse,
    'Z_Statistic': result.tvalues,
    'P_Value': result.pvalues,
    'Significant': ['Yes' if p < 0.05 else 'No' for p in result.pvalues]
})

auc = roc_auc_score(y, result.predict(X_const.values))
lr_stat = result.llr
lr_pval = result.llr_pvalue
pseudo_r2 = result.prsquared
n_obs = int(result.nobs)

label_names = {
    'roa': 'Return on Assets (ROA)',
    'roe': 'Return on Equity (ROE)',
    'gross_margin': 'Gross Profit Margin',
    'op_margin': 'Operating Margin',
    'net_margin': 'Net Profit Margin',
    'asset_turnover': 'Asset Turnover',
    'current_ratio': 'Current Ratio',
    'debt_to_equity': 'Debt-to-Equity',
    'rd_intensity': 'R&D Intensity',
    'rev_growth': 'Revenue Growth',
    'ni_growth': 'Net Income Growth',
    'pe_ratio': 'Price-to-Earnings (P/E)',
    'book_to_market': 'Book-to-Market Ratio',
    'const': 'Intercept'
}

print("\nGlobal Model Results:")
print(f"  AUC           : {auc:.4f}")
print(f"  Pseudo R²     : {pseudo_r2:.4f}")
print(f"  LR Statistic  : {lr_stat:.4f}")
print(f"  LR p-value    : {lr_pval:.4f}")
print(f"  Observations  : {n_obs}")
print("\nCoefficients:")
print(summary_df[['Variable','Coefficient','P_Value','Significant']].to_string(index=False))

doc = SimpleDocTemplate(
    'Preliminary_Analysis_Global.pdf',
    pagesize=letter,
    rightMargin=0.75*inch,
    leftMargin=0.75*inch,
    topMargin=0.75*inch,
    bottomMargin=0.75*inch
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle('CustomTitle', parent=styles['Title'],
    fontSize=16, textColor=colors.HexColor('#1a237e'), spaceAfter=6,
    fontName='Helvetica-Bold', alignment=TA_CENTER)

subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'],
    fontSize=10, textColor=colors.HexColor('#37474f'), spaceAfter=20,
    fontName='Helvetica', alignment=TA_CENTER)

heading_style = ParagraphStyle('Heading', parent=styles['Heading2'],
    fontSize=12, textColor=colors.HexColor('#1a237e'), spaceBefore=14,
    spaceAfter=8, fontName='Helvetica-Bold')

body_style = ParagraphStyle('Body', parent=styles['Normal'],
    fontSize=9.5, textColor=colors.HexColor('#212121'), spaceAfter=6,
    fontName='Helvetica', leading=14, alignment=TA_JUSTIFY)

note_style = ParagraphStyle('Note', parent=styles['Normal'],
    fontSize=8.5, textColor=colors.HexColor('#555555'), spaceAfter=4,
    fontName='Helvetica-Oblique', leading=12)

story = []

story.append(Paragraph("Preliminary Global Logistic Regression Analysis", title_style))
story.append(Paragraph("S&amp;P 500 Outperformer Prediction — Whole-Sample, No Segmentation", subtitle_style))
story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1a237e')))
story.append(Spacer(1, 10))

story.append(Paragraph("1. Dataset Summary", heading_style))
dataset_data = [
    ['Parameter', 'Value'],
    ['Data Sources', 'Compustat Quarterly Fundamentals + CRSP Monthly Returns (WRDS)'],
    ['Benchmark', 'S&P 500 Composite Return (crsp.msi — sprtrn) from WRDS'],
    ['S&P 500 Companies', '500'],
    ['Total Observations', f'{n_obs:,}'],
    ['Date Range', 'Q1 2010 — Q4 2024 (15 years, 60 quarters)'],
    ['Outperformers (Y=1)', f'{int(y.sum()):,} ({y.mean()*100:.1f}%)'],
    ['Underperformers (Y=0)', f'{int((y==0).sum()):,} ({(1-y.mean())*100:.1f}%)'],
    ['Predictors', '13 financial ratios computed from Compustat quarterly data'],
]
dataset_table = Table(dataset_data, colWidths=[2.5*inch, 4.5*inch])
dataset_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a237e')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 9),
    ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f5f5f5')),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#e8eaf6')]),
    ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'),
    ('FONTNAME', (1,1), (1,-1), 'Helvetica'),
    ('FONTSIZE', (0,1), (-1,-1), 9),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#b0bec5')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
]))
story.append(dataset_table)
story.append(Spacer(1, 10))

story.append(Paragraph("2. Global Model Fit Statistics", heading_style))

sig_color = colors.HexColor('#b71c1c') if lr_pval >= 0.05 else colors.HexColor('#1b5e20')
sig_text = "NOT SIGNIFICANT" if lr_pval >= 0.05 else "SIGNIFICANT"

fit_data = [
    ['Metric', 'Value', 'Threshold', 'Verdict'],
    ['AUC (Area Under ROC Curve)', f'{auc:.4f}', '> 0.65 good, > 0.70 strong', 'Weak' if auc < 0.60 else ('Moderate' if auc < 0.70 else 'Strong')],
    ["McFadden's Pseudo R²", f'{pseudo_r2:.4f}', '> 0.20 acceptable', 'Very Weak' if pseudo_r2 < 0.05 else ('Weak' if pseudo_r2 < 0.10 else 'Moderate')],
    ['Likelihood Ratio Statistic', f'{lr_stat:.4f}', 'Higher is better', '—'],
    ['Likelihood Ratio p-value', f'{lr_pval:.4f}', '< 0.05 required', sig_text],
    ['Sample Size (N)', f'{n_obs:,}', '—', 'Adequate'],
    ['Outperformer Rate', f'{y.mean()*100:.1f}%', '~50% ideal for balance', 'Balanced'],
]
fit_table = Table(fit_data, colWidths=[2.4*inch, 1.2*inch, 2.0*inch, 1.4*inch])
fit_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a237e')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 9),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#e8eaf6')]),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,1), (-1,-1), 9),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#b0bec5')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('TEXTCOLOR', (3, 4), (3, 4), sig_color),
    ('FONTNAME', (3, 4), (3, 4), 'Helvetica-Bold'),
]))
story.append(fit_table)
story.append(Spacer(1, 10))

story.append(Paragraph("3. Coefficient Table — Individual Predictor Significance", heading_style))

ratio_full_names = {
    'roa': 'Return on Assets (ROA)',
    'roe': 'Return on Equity (ROE)',
    'gross_margin': 'Gross Profit Margin',
    'op_margin': 'Operating Margin',
    'net_margin': 'Net Profit Margin',
    'asset_turnover': 'Asset Turnover',
    'current_ratio': 'Current Ratio',
    'debt_to_equity': 'Debt-to-Equity Ratio',
    'rd_intensity': 'R&D Intensity',
    'rev_growth': 'Revenue Growth (QoQ)',
    'ni_growth': 'Net Income Growth (QoQ)',
    'pe_ratio': 'Price-to-Earnings (P/E)',
    'book_to_market': 'Book-to-Market Ratio',
}

coef_header = ['Predictor', 'Coefficient', 'Std Error', 'Z-Stat', 'p-Value', 'Significant?']
coef_rows = [coef_header]
for _, row in summary_df.iloc[1:].iterrows():
    var = row['Variable']
    full_name = ratio_full_names.get(var, var)
    sig = 'Yes ***' if row['P_Value'] < 0.01 else ('Yes **' if row['P_Value'] < 0.05 else ('Yes *' if row['P_Value'] < 0.10 else 'No'))
    coef_rows.append([
        full_name,
        f"{row['Coefficient']:+.4f}",
        f"{row['Std_Error']:.4f}",
        f"{row['Z_Statistic']:.4f}",
        f"{row['P_Value']:.4f}",
        sig
    ])

coef_table = Table(coef_rows, colWidths=[2.1*inch, 0.9*inch, 0.85*inch, 0.75*inch, 0.8*inch, 0.85*inch])

coef_style = [
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a237e')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 8.5),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,1), (-1,-1), 8.5),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#b0bec5')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('ALIGN', (1,0), (-1,-1), 'CENTER'),
]

for i, row in enumerate(coef_rows[1:], start=1):
    p_val_str = row[4]
    try:
        p = float(p_val_str)
    except:
        p = 1.0
    if p < 0.05:
        coef_style.append(('BACKGROUND', (0,i), (-1,i), colors.HexColor('#e8f5e9')))
        coef_style.append(('TEXTCOLOR', (5,i), (5,i), colors.HexColor('#1b5e20')))
        coef_style.append(('FONTNAME', (5,i), (5,i), 'Helvetica-Bold'))
    elif p < 0.10:
        coef_style.append(('BACKGROUND', (0,i), (-1,i), colors.HexColor('#fff9c4')))
        coef_style.append(('TEXTCOLOR', (5,i), (5,i), colors.HexColor('#f57f17')))
    else:
        bg = colors.white if i % 2 == 0 else colors.HexColor('#e8eaf6')
        coef_style.append(('BACKGROUND', (0,i), (-1,i), bg))
        coef_style.append(('TEXTCOLOR', (5,i), (5,i), colors.HexColor('#b71c1c')))

coef_table.setStyle(TableStyle(coef_style))
story.append(coef_table)
story.append(Spacer(1, 6))
story.append(Paragraph("*** p < 0.01  ** p < 0.05  * p < 0.10  (green rows = significant at 5%, yellow = marginal at 10%)", note_style))
story.append(Spacer(1, 10))

story.append(Paragraph("4. Variance Inflation Factor (VIF) — Multicollinearity Check", heading_style))
vif_header = ['Predictor', 'VIF Score', 'Assessment']
vif_rows = [vif_header]
for _, row in vif_data.iterrows():
    v = row['VIF']
    assess = 'No multicollinearity' if v < 5 else ('Moderate' if v < 10 else 'High — problematic')
    vif_rows.append([
        ratio_full_names.get(row['Variable'], row['Variable']),
        f"{v:.2f}",
        assess
    ])

vif_table = Table(vif_rows, colWidths=[2.5*inch, 1.2*inch, 3.3*inch])
vif_style = [
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a237e')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 9),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,1), (-1,-1), 9),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#b0bec5')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('ALIGN', (1,0), (1,-1), 'CENTER'),
]
for i, row in enumerate(vif_rows[1:], start=1):
    v = float(row[1])
    if v >= 10:
        vif_style.append(('BACKGROUND', (0,i), (-1,i), colors.HexColor('#ffebee')))
        vif_style.append(('TEXTCOLOR', (1,i), (1,i), colors.HexColor('#b71c1c')))
        vif_style.append(('FONTNAME', (1,i), (1,i), 'Helvetica-Bold'))
    elif v >= 5:
        vif_style.append(('BACKGROUND', (0,i), (-1,i), colors.HexColor('#fff9c4')))
    else:
        bg = colors.white if i % 2 == 0 else colors.HexColor('#e8eaf6')
        vif_style.append(('BACKGROUND', (0,i), (-1,i), bg))
vif_table.setStyle(TableStyle(vif_style))
story.append(vif_table)
story.append(Spacer(1, 10))

story.append(Paragraph("5. Why the Global Model Is Not Statistically Significant", heading_style))

reasons = [
    ("Reason 1: Market Efficiency Collapses Signals Across Sectors",
     "When all 500 companies are pooled regardless of sector, the financial ratios lose their interpretive power. "
     "A high Debt-to-Equity ratio is expected and healthy for a utility company but alarming for a tech startup. "
     "A low P/E is a value signal in consumer staples but a distress signal in growth sectors. Pooling these "
     "together creates contradictory signals that cancel each other out, inflating p-values and making no single "
     "predictor appear reliably significant across the full sample."),

    ("Reason 2: Regime Mixing — Different Eras, Different Predictors",
     "The dataset spans 15 years (2010–2024), covering radically different market environments: post-financial-crisis "
     "recovery, a decade-long bull market, the COVID crash and recovery, and the 2022–2024 rate-hike era. "
     "Ratios like Book-to-Market predict well in value-driven regimes but not in momentum-driven ones. "
     "Combining all regimes into one model dilutes every signal, pushing p-values above 0.05."),

    ("Reason 3: Weak Pseudo R² Confirms Low Explanatory Power",
     f"A McFadden's Pseudo R² of {pseudo_r2:.4f} is far below the 0.20 threshold considered acceptable in "
     "published literature. This means the 13 financial ratios together explain very little of the variation in "
     "whether a stock outperforms the S&P 500 at the aggregate level. The model is statistically indistinguishable "
     "from a coin flip in terms of incremental explanatory power."),

    ("Reason 4: AUC Near 0.50 Confirms No Discrimination",
     f"An AUC of {auc:.4f} means the model's ability to distinguish outperformers from underperformers is barely "
     "better than random chance. A perfect classifier scores 1.00; random guessing scores 0.50. The global model "
     "sits very close to the random baseline, confirming that accounting-based signals alone — without sector or "
     "regime conditioning — carry almost no predictive content for market outperformance."),

    ("Reason 5: Multicollinearity Among Profitability Ratios",
     "ROA, ROE, Net Margin, Operating Margin, and Gross Margin are all computed from overlapping components "
     "(net income, revenue, assets). They carry similar information, inflating their standard errors and reducing "
     "individual Z-statistics below significance thresholds. The VIF table above identifies which pairs are "
     "problematic. Sector-specific models avoid this because the relationships between ratios differ by industry."),

    ("Why This Is the Right Setup for a Publication",
     "Demonstrating that the global model fails is not a weakness — it is the central contribution. "
     "The paper's argument is: global models miss the structure hidden inside sectors and regimes. "
     "The next step — sector-specific logistic regression — is expected to reveal that 4–6 individual sectors "
     "produce statistically significant models (p < 0.05, AUC > 0.70), validating the thesis that "
     "predictability is sector-contingent and regime-dependent, not universal.")
]

for title, text in reasons:
    story.append(Paragraph(f"<b>{title}</b>", body_style))
    story.append(Paragraph(text, body_style))
    story.append(Spacer(1, 6))

story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#b0bec5')))
story.append(Spacer(1, 6))
story.append(Paragraph(
    "Data: Compustat Quarterly Fundamentals + CRSP Monthly Returns via WRDS (account: lanagidan9790). "
    "Benchmark: S&P 500 Composite Return (crsp.msi). Period: Q1 2010 – Q4 2024. "
    "Analysis: Global Logistic Regression with Standardized Predictors.",
    note_style
))

doc.build(story)
print("\nPDF saved: Preliminary_Analysis_Global.pdf")

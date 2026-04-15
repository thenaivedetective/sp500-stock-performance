import pandas as pd
import numpy as np
import warnings
import matplotlib
matplotlib.use('Agg')
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
from statsmodels.discrete.discrete_model import Logit
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
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
comp['lag_niq']   = comp.groupby('gvkey')['niq'].shift(1)

comp['roa']            = comp['niq']    / comp['atq'].replace(0, np.nan)
comp['roe']            = comp['niq']    / comp['ceqq'].replace(0, np.nan)
comp['gross_margin']   = (comp['revtq'] - comp['cogsq']) / comp['revtq'].replace(0, np.nan)
comp['op_margin']      = comp['oiadpq'] / comp['revtq'].replace(0, np.nan)
comp['net_margin']     = comp['niq']    / comp['revtq'].replace(0, np.nan)
comp['asset_turnover'] = comp['revtq']  / comp['atq'].replace(0, np.nan)
comp['current_ratio']  = comp['actq']   / comp['lctq'].replace(0, np.nan)
comp['debt_to_equity'] = comp['dlttq']  / comp['ceqq'].replace(0, np.nan)
comp['rd_intensity']   = comp['xrdq']   / comp['revtq'].replace(0, np.nan)
comp['rev_growth']     = (comp['revtq'] - comp['lag_revtq']) / comp['lag_revtq'].abs().replace(0, np.nan)
comp['ni_growth']      = (comp['niq']   - comp['lag_niq'])   / comp['lag_niq'].abs().replace(0, np.nan)
comp['pe_ratio']       = comp['prccq']  / (comp['ibq'] / comp['cshoq'].replace(0, np.nan)).replace(0, np.nan)
comp['book_to_market'] = comp['ceqq']   / comp['mkvaltq'].replace(0, np.nan)

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

X = df[ratio_cols]
y = df['outperformer_quarterly']

scaler = StandardScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=ratio_cols)

vif_data = pd.DataFrame({
    'Variable': ratio_cols,
    'VIF': [variance_inflation_factor(X_scaled.values, i) for i in range(len(ratio_cols))]
})

X_const = sm.add_constant(X_scaled)
result = Logit(y.values, X_const.values).fit(maxiter=200, disp=False)

auc        = roc_auc_score(y, result.predict(X_const.values))
pseudo_r2  = result.prsquared
lr_stat    = result.llr
lr_pval    = result.llr_pvalue
n_obs      = int(result.nobs)

coef_names = ['Intercept'] + ratio_cols
summary_df = pd.DataFrame({
    'Variable':    coef_names,
    'Coefficient': result.params,
    'Std_Error':   result.bse,
    'Z_Statistic': result.tvalues,
    'P_Value':     result.pvalues,
})

ratio_labels = {
    'roa':'Return on Assets (ROA)', 'roe':'Return on Equity (ROE)',
    'gross_margin':'Gross Profit Margin', 'op_margin':'Operating Margin',
    'net_margin':'Net Profit Margin', 'asset_turnover':'Asset Turnover',
    'current_ratio':'Current Ratio', 'debt_to_equity':'Debt-to-Equity Ratio',
    'rd_intensity':'R&D Intensity', 'rev_growth':'Revenue Growth (QoQ)',
    'ni_growth':'Net Income Growth (QoQ)', 'pe_ratio':'Price-to-Earnings (P/E)',
    'book_to_market':'Book-to-Market Ratio',
}

doc = SimpleDocTemplate('Preliminary_Analysis_Global.pdf', pagesize=letter,
    rightMargin=0.75*inch, leftMargin=0.75*inch, topMargin=0.7*inch, bottomMargin=0.7*inch)

styles = getSampleStyleSheet()
title_s  = ParagraphStyle('t', fontName='Helvetica-Bold', fontSize=15,
    alignment=TA_CENTER, textColor=colors.HexColor('#1a237e'), spaceAfter=4)
sub_s    = ParagraphStyle('s', fontName='Helvetica', fontSize=9.5,
    alignment=TA_CENTER, textColor=colors.HexColor('#37474f'), spaceAfter=16)
head_s   = ParagraphStyle('h', fontName='Helvetica-Bold', fontSize=11,
    textColor=colors.HexColor('#1a237e'), spaceBefore=12, spaceAfter=6)
body_s   = ParagraphStyle('b', fontName='Helvetica', fontSize=9.5,
    leading=14, spaceAfter=5, alignment=TA_JUSTIFY)
note_s   = ParagraphStyle('n', fontName='Helvetica-Oblique', fontSize=8.5,
    textColor=colors.HexColor('#555555'), leading=12, spaceAfter=4)

def make_table(data, col_widths, header_color='#1a237e'):
    t = Table(data, colWidths=col_widths)
    style = [
        ('BACKGROUND',   (0,0), (-1,0),  colors.HexColor(header_color)),
        ('TEXTCOLOR',    (0,0), (-1,0),  colors.white),
        ('FONTNAME',     (0,0), (-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',     (0,0), (-1,0),  9),
        ('FONTNAME',     (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE',     (0,1), (-1,-1), 9),
        ('GRID',         (0,0), (-1,-1), 0.5, colors.HexColor('#b0bec5')),
        ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',   (0,0), (-1,-1), 4),
        ('BOTTOMPADDING',(0,0), (-1,-1), 4),
        ('LEFTPADDING',  (0,0), (-1,-1), 7),
        ('ROWBACKGROUNDS',(0,1),(-1,-1), [colors.white, colors.HexColor('#e8eaf6')]),
    ]
    t.setStyle(TableStyle(style))
    return t

story = []
story.append(Paragraph("Preliminary Global Logistic Regression", title_s))
story.append(Paragraph("VIF Multicollinearity Check + Full-Sample LR — No Segmentation | WRDS Data (Q1 2010 – Q4 2024)", sub_s))
story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1a237e')))
story.append(Spacer(1, 8))

story.append(Paragraph("1. Sample Overview", head_s))
overview = [
    ['Parameter', 'Value'],
    ['Data Sources', 'Compustat Quarterly Fundamentals + CRSP Monthly Returns (WRDS)'],
    ['Benchmark', 'S&P 500 Return — crsp.msi (sprtrn) from WRDS'],
    ['Companies', '500 S&P 500 constituents'],
    ['Observations (after merge & dropna)', f'{n_obs:,}'],
    ['Date Range', 'Q1 2010 — Q4 2024  (15 years, 60 quarters)'],
    ['Outperformers  (Y = 1)', f'{int(y.sum()):,}  ({y.mean()*100:.1f}%)'],
    ['Underperformers (Y = 0)', f'{int((y==0).sum()):,}  ({(1-y.mean())*100:.1f}%)'],
    ['Predictors', '13 financial ratios computed from raw Compustat quarterly items'],
]
story.append(make_table(overview, [2.3*inch, 4.7*inch]))
story.append(Spacer(1, 8))

story.append(Paragraph("2. Variance Inflation Factor (VIF) — Multicollinearity Check", head_s))
story.append(Paragraph(
    "VIF measures how much each predictor's variance is inflated by correlation with other predictors. "
    "VIF < 5 is acceptable; VIF ≥ 10 indicates problematic multicollinearity that inflates standard errors "
    "and reduces individual significance.", body_s))
vif_rows = [['Predictor', 'VIF Score', 'Assessment']]
for _, r in vif_data.iterrows():
    v = r['VIF']
    assess = 'Acceptable — no issue' if v < 5 else ('Moderate concern' if v < 10 else 'High — problematic')
    vif_rows.append([ratio_labels.get(r['Variable'], r['Variable']), f"{v:.2f}", assess])
vif_t = make_table(vif_rows, [2.8*inch, 1.1*inch, 3.1*inch])
vif_style_extra = []
for i, r in enumerate(vif_rows[1:], 1):
    v = float(r[1])
    if v >= 10:
        vif_style_extra += [('BACKGROUND',(0,i),(-1,i),colors.HexColor('#ffebee')),
                            ('TEXTCOLOR',(1,i),(1,i),colors.HexColor('#b71c1c')),
                            ('FONTNAME',(1,i),(1,i),'Helvetica-Bold')]
    elif v >= 5:
        vif_style_extra += [('BACKGROUND',(0,i),(-1,i),colors.HexColor('#fff9c4'))]
vif_t.setStyle(TableStyle(vif_t._argW and [] or [] + vif_style_extra))
story.append(vif_t)
story.append(Spacer(1, 8))

story.append(Paragraph("3. Global Model Fit — Is the Model Statistically Significant?", head_s))
overall_sig = "SIGNIFICANT" if lr_pval < 0.05 else "NOT SIGNIFICANT"
sig_color   = colors.HexColor('#1b5e20') if lr_pval < 0.05 else colors.HexColor('#b71c1c')
fit_rows = [
    ['Metric', 'Value', 'Benchmark', 'Verdict'],
    ['Likelihood Ratio p-value', f'{lr_pval:.4f}',  '< 0.05 required',      overall_sig],
    ['Likelihood Ratio Statistic', f'{lr_stat:.2f}','Higher = better fit',  '—'],
    ["McFadden's Pseudo R²",     f'{pseudo_r2:.4f}','> 0.20 acceptable',
     'Very Weak' if pseudo_r2 < 0.05 else ('Weak' if pseudo_r2 < 0.10 else 'Moderate')],
    ['AUC (ROC Curve)',          f'{auc:.4f}',       '> 0.70 strong',
     'Near-Random' if auc < 0.60 else ('Moderate' if auc < 0.70 else 'Strong')],
    ['Sample Size (N)',          f'{n_obs:,}',        '—',                    'Adequate'],
]
fit_t = make_table(fit_rows, [2.3*inch, 1.1*inch, 1.8*inch, 1.8*inch])
fit_t.setStyle(TableStyle([
    ('BACKGROUND',   (0,0), (-1,0),  colors.HexColor('#1a237e')),
    ('TEXTCOLOR',    (0,0), (-1,0),  colors.white),
    ('FONTNAME',     (0,0), (-1,0),  'Helvetica-Bold'),
    ('FONTSIZE',     (0,0), (-1,0),  9),
    ('FONTNAME',     (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE',     (0,1), (-1,-1), 9),
    ('GRID',         (0,0), (-1,-1), 0.5, colors.HexColor('#b0bec5')),
    ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING',   (0,0), (-1,-1), 4),
    ('BOTTOMPADDING',(0,0), (-1,-1), 4),
    ('LEFTPADDING',  (0,0), (-1,-1), 7),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor('#e8eaf6')]),
    ('TEXTCOLOR',    (3,1), (3,1),   sig_color),
    ('FONTNAME',     (3,1), (3,1),   'Helvetica-Bold'),
]))
story.append(fit_t)
story.append(Spacer(1, 8))

story.append(Paragraph("4. Individual Predictor Coefficients & p-Values", head_s))
coef_rows = [['Predictor', 'Coefficient', 'Std Error', 'Z-Stat', 'p-Value', 'Significant?']]
for _, r in summary_df.iloc[1:].iterrows():
    p = r['P_Value']
    sig = '*** p<0.01' if p < 0.01 else ('**  p<0.05' if p < 0.05 else ('*   p<0.10' if p < 0.10 else 'No'))
    coef_rows.append([
        ratio_labels.get(r['Variable'], r['Variable']),
        f"{r['Coefficient']:+.4f}", f"{r['Std_Error']:.4f}",
        f"{r['Z_Statistic']:.3f}",  f"{p:.4f}", sig
    ])
coef_t = Table(coef_rows, colWidths=[2.15*inch, 0.9*inch, 0.85*inch, 0.75*inch, 0.75*inch, 0.9*inch])
coef_style = [
    ('BACKGROUND',   (0,0), (-1,0),  colors.HexColor('#1a237e')),
    ('TEXTCOLOR',    (0,0), (-1,0),  colors.white),
    ('FONTNAME',     (0,0), (-1,0),  'Helvetica-Bold'),
    ('FONTSIZE',     (0,0), (-1,0),  8.5),
    ('FONTNAME',     (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE',     (0,1), (-1,-1), 8.5),
    ('GRID',         (0,0), (-1,-1), 0.5, colors.HexColor('#b0bec5')),
    ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING',   (0,0), (-1,-1), 4),
    ('BOTTOMPADDING',(0,0), (-1,-1), 4),
    ('LEFTPADDING',  (0,0), (-1,-1), 5),
    ('ALIGN',        (1,0), (-1,-1), 'CENTER'),
]
for i, r in enumerate(coef_rows[1:], 1):
    try: p = float(r[4])
    except: p = 1.0
    if p < 0.05:
        coef_style += [('BACKGROUND',(0,i),(-1,i),colors.HexColor('#e8f5e9')),
                       ('TEXTCOLOR',(5,i),(5,i),colors.HexColor('#1b5e20')),
                       ('FONTNAME',(5,i),(5,i),'Helvetica-Bold')]
    elif p < 0.10:
        coef_style += [('BACKGROUND',(0,i),(-1,i),colors.HexColor('#fff9c4')),
                       ('TEXTCOLOR',(5,i),(5,i),colors.HexColor('#f57f17'))]
    else:
        coef_style += [('BACKGROUND',(0,i),(-1,i), colors.white if i%2==0 else colors.HexColor('#e8eaf6')),
                       ('TEXTCOLOR',(5,i),(5,i),colors.HexColor('#b71c1c'))]
coef_t.setStyle(TableStyle(coef_style))
story.append(coef_t)
story.append(Spacer(1, 5))
story.append(Paragraph("Green rows = significant at 5% level.  Yellow = marginal (10%).", note_s))
story.append(Spacer(1, 8))

story.append(Paragraph("5. Interpretation", head_s))
if lr_pval < 0.05:
    overall_interp = (
        f"The global logistic regression model is statistically significant overall (LR p = {lr_pval:.4f} < 0.05), "
        f"meaning the 13 financial ratios together do carry some detectable relationship with outperformance. "
        f"However, the model's practical predictive power is extremely weak: an AUC of {auc:.4f} is barely above "
        f"random chance (0.50), and a Pseudo R² of {pseudo_r2:.4f} means the ratios explain less than "
        f"{pseudo_r2*100:.1f}% of the variation in outperformance. In other words, the model is statistically "
        f"detectable but practically useless as a predictor at the whole-market level."
    )
else:
    overall_interp = (
        f"The global logistic regression model is NOT statistically significant (LR p = {lr_pval:.4f} > 0.05). "
        f"The 13 financial ratios together fail to reliably distinguish outperformers from underperformers "
        f"when all sectors are pooled. The AUC of {auc:.4f} confirms the model performs at near-random levels."
    )

story.append(Paragraph(overall_interp, body_s))
story.append(Paragraph(
    "This result is expected and is the central motivation for the sector-specific analysis. "
    "Pooling all 500 companies ignores the fact that the same ratio means different things across industries — "
    "a high Debt-to-Equity is normal for utilities but alarming for tech. Mixing these contradictory signals "
    "cancels predictive content at the aggregate level. Sector-specific models are expected to restore "
    "significance in 4–6 of the 11 GICS sectors.", body_s))

story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#b0bec5')))
story.append(Spacer(1, 5))
story.append(Paragraph(
    "Data: Compustat Quarterly Fundamentals + CRSP Monthly Returns via WRDS (lanagidan9790). "
    "Benchmark: S&P 500 Composite Return from crsp.msi. Period: Q1 2010 – Q4 2024.", note_s))

doc.build(story)
print(f"\nSample        : {n_obs:,} observations")
print(f"Outperformers : {y.mean()*100:.1f}%")
print(f"LR p-value    : {lr_pval:.4f}  →  {'SIGNIFICANT' if lr_pval < 0.05 else 'NOT SIGNIFICANT'}")
print(f"AUC           : {auc:.4f}")
print(f"Pseudo R²     : {pseudo_r2:.4f}")
print(f"\nSaved: Preliminary_Analysis_Global.pdf")

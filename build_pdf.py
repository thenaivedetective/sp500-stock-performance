from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

PAGE_W, PAGE_H = landscape((11*inch, 8.5*inch))

NAVY      = HexColor('#0A1628')
NAVY_CARD = HexColor('#132038')
GOLD      = HexColor('#D4AF37')
BLUE      = HexColor('#4A9EFF')
WHITE_C   = white
MUTED     = HexColor('#8B9CB8')
GREEN_C   = HexColor('#2ECC71')
RED_C     = HexColor('#E74C3C')
LIGHT_NAV = HexColor('#1A3050')

def new_page(c):
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

def draw_rect(c, x, y, w, h, color, stroke=False):
    c.setFillColor(color)
    c.rect(x, y, w, h, fill=1, stroke=1 if stroke else 0)

def text(c, txt, x, y, size=12, color=white, bold=False, align='left'):
    c.setFillColor(color)
    fname = 'Helvetica-Bold' if bold else 'Helvetica'
    c.setFont(fname, size)
    if align == 'center':
        c.drawCentredString(x, y, txt)
    elif align == 'right':
        c.drawRightString(x, y, txt)
    else:
        c.drawString(x, y, txt)

def header(c, title, subtitle=None):
    draw_rect(c, 0, PAGE_H - 0.12*inch, PAGE_W, 0.12*inch, GOLD)
    text(c, title, 0.5*inch, PAGE_H - 0.65*inch, size=28, bold=True)
    if subtitle:
        text(c, subtitle, 0.5*inch, PAGE_H - 0.9*inch, size=13, color=MUTED)
    draw_rect(c, 0, PAGE_H - 1.05*inch, PAGE_W, 0.02*inch, LIGHT_NAV)

def stat_box(c, label, value, note, x, y, w, h, val_color=None):
    if val_color is None:
        val_color = GOLD
    draw_rect(c, x, y, w, h, NAVY_CARD)
    draw_rect(c, x, y, 0.06*inch, h, GOLD)
    text(c, label, x+0.15*inch, y+h-0.22*inch, size=9, color=MUTED)
    text(c, value, x+0.15*inch, y+h-0.55*inch, size=24, bold=True, color=val_color)
    if note:
        text(c, note, x+0.15*inch, y+0.08*inch, size=8, color=MUTED)

def bullet(c, items, x, y, line_h=0.28*inch, size=11, color=None):
    if color is None:
        color = WHITE_C
    for item in items:
        text(c, item, x, y, size=size, color=color)
        y -= line_h
    return y

def box(c, x, y, w, h, fill=NAVY_CARD, accent=GOLD, title=None, t_size=13):
    draw_rect(c, x, y, w, h, fill)
    draw_rect(c, x, y+h-0.08*inch, w, 0.08*inch, accent)
    if title:
        text(c, title, x+0.15*inch, y+h-0.38*inch, size=t_size, bold=True, color=accent)

c = canvas.Canvas('SP500_Outperformer_Prediction.pdf', pagesize=(PAGE_W, PAGE_H))
c.setTitle('Using Logistic Regression to Determine U.S. Equity Performance')
c.setAuthor('Lana Gidan, Matthew Golubow, Shahd Tarman')

# ── SLIDE 1: TITLE ─────────────────────────────────────────────────────────────
new_page(c)
draw_rect(c, 0, 0, 5.0*inch, PAGE_H, NAVY_CARD)
draw_rect(c, 5.0*inch, 0, PAGE_W - 5.0*inch, PAGE_H, LIGHT_NAV)
draw_rect(c, 5.0*inch, 0, 0.06*inch, PAGE_H, GOLD)

text(c, 'SSIE 605  |  Binghamton University', 0.5*inch, PAGE_H - 1.2*inch, size=11, color=GOLD, bold=True)
text(c, 'Using Logistic Regression to', 0.5*inch, PAGE_H - 1.85*inch, size=26, bold=True)
text(c, 'Determine U.S. Equity Performance', 0.5*inch, PAGE_H - 2.25*inch, size=26, bold=True)
draw_rect(c, 0.5*inch, PAGE_H - 3.25*inch, 1.4*inch, 0.05*inch, GOLD)
text(c, 'Lana Gidan  |  Matthew Golubow  |  Shahd Tarman', 0.5*inch, PAGE_H - 3.55*inch, size=12, color=MUTED)
text(c, 'Q1 2010 – Q4 2024  |  S&P 500 Constituents', 0.5*inch, PAGE_H - 3.9*inch, size=11, color=MUTED)

text(c, 'PREDICTING', 8.3*inch, PAGE_H - 2.2*inch, size=20, bold=True, color=GOLD, align='center')
text(c, 'OUTPERFORMANCE', 8.3*inch, PAGE_H - 2.6*inch, size=20, bold=True, color=GOLD, align='center')
text(c, 'USING QUARTERLY', 8.3*inch, PAGE_H - 3.0*inch, size=20, bold=True, color=GOLD, align='center')
text(c, 'FINANCIAL RATIOS', 8.3*inch, PAGE_H - 3.4*inch, size=20, bold=True, color=GOLD, align='center')
text(c, 'Logistic Regression  |  VIF  |  PCA  |  Out-of-Sample 2025',
     8.3*inch, PAGE_H - 4.2*inch, size=10, color=MUTED, align='center')
c.showPage()

# ── SLIDE 2: AGENDA ────────────────────────────────────────────────────────────
new_page(c)
header(c, 'Agenda', 'Presentation Structure')

items = [
    ('01', 'Background',              'SEC disclosures, S&P 500, research motivation'),
    ('02', 'Problem Statement',       'Three core research questions'),
    ('03', 'Data Capture',            'WRDS, FRED, EDGAR — sources and variables'),
    ('04', 'Data Computations',       'Financial ratios and delta momentum features'),
    ('05', 'Data Cleaning',           'Winsorization, standardization, NaN removal'),
    ('06', 'VIF Analysis',            'Multicollinearity removal — 20 of 24 kept'),
    ('07', 'PCA Analysis',            '9 components, 5% individual variance threshold'),
    ('08', 'Logistic Regression',     'Global model results — AUC 0.5381'),
    ('09', 'Segmentation & Results',  'Market Cap and Sector — best: Comm. Services 63.9%'),
    ('10', '2025 Out-of-Sample Test', 'Portfolio vs S&P 500'),
    ('11', 'Conclusion',              'Efficient Market Hypothesis assessment'),
]

col1, col2 = items[:6], items[6:]
line_h = 0.7*inch
start_y = PAGE_H - 1.4*inch

for i, (num, title, desc) in enumerate(col1):
    y = start_y - i * line_h
    draw_rect(c, 0.4*inch, y - 0.12*inch, 0.4*inch, 0.38*inch, GOLD)
    text(c, num, 0.6*inch, y + 0.05*inch, size=11, bold=True, color=NAVY, align='center')
    text(c, title, 0.9*inch, y + 0.05*inch, size=12, bold=True)
    text(c, desc, 0.9*inch, y - 0.2*inch, size=9, color=MUTED)

for i, (num, title, desc) in enumerate(col2):
    y = start_y - i * line_h
    draw_rect(c, 5.8*inch, y - 0.12*inch, 0.4*inch, 0.38*inch, GOLD)
    text(c, num, 6.0*inch, y + 0.05*inch, size=11, bold=True, color=NAVY, align='center')
    text(c, title, 6.3*inch, y + 0.05*inch, size=12, bold=True)
    text(c, desc, 6.3*inch, y - 0.2*inch, size=9, color=MUTED)

c.showPage()

# ── SLIDE 3: BACKGROUND ────────────────────────────────────────────────────────
new_page(c)
header(c, 'Background', 'Section 01')

desc_text = ('The SEC requires all publicly traded companies to disclose quarterly financial statements. '
             'These reports detail revenues, expenses, assets, and debt — information used to evaluate company health.')
c.setFillColor(WHITE_C)
c.setFont('Helvetica', 11)
c.drawString(0.5*inch, PAGE_H - 1.3*inch, desc_text[:95])
c.drawString(0.5*inch, PAGE_H - 1.55*inch, desc_text[95:])

boxes_data = [
    ('S&P 500',
     ['500 largest U.S. companies by market cap.',
      'Covers ~80% of total U.S. stock market value.',
      'Rebalanced quarterly as constituents change.']),
    ('Passive Investing Assumption',
     ['The average investor cannot consistently',
      'beat the S&P 500 return.',
      'Index funds: low fees, no stock selection needed.']),
    ('Our Research Question',
     ['Can publicly available quarterly financial data',
      'predict which S&P 500 companies will outperform',
      'the index the following quarter?']),
]

for i, (title, lines) in enumerate(boxes_data):
    x = 0.4*inch + i * 3.65*inch
    box(c, x, PAGE_H - 6.5*inch, 3.4*inch, 4.3*inch, title=title, t_size=12)
    y = PAGE_H - 3.1*inch
    for line in lines:
        text(c, line, x + 0.15*inch, y, size=11)
        y -= 0.28*inch

c.showPage()

# ── SLIDE 4: PROBLEM STATEMENT ─────────────────────────────────────────────────
new_page(c)
header(c, 'Problem Statement', 'Section 02')

questions = [
    ('Q1', 'Predictability',
     'Can we use publicly available S&P 500 financial data to determine if a company will outperform or underperform the S&P 500?'),
    ('Q2', 'Forward-Looking Signal',
     'Can we use current quarter financial ratios to reliably predict next quarter stock performance — before it happens?'),
    ('Q3', 'Portfolio Construction',
     'Can we construct a portfolio from model predictions whose quarterly returns beat the S&P 500 index?'),
]

for i, (label, title, body) in enumerate(questions):
    y = PAGE_H - 1.6*inch - i * 1.9*inch
    draw_rect(c, 0.4*inch, y - 1.2*inch, PAGE_W - 0.8*inch, 1.5*inch, NAVY_CARD)
    draw_rect(c, 0.4*inch, y - 1.2*inch, 0.06*inch, 1.5*inch, GOLD)
    draw_rect(c, 0.4*inch, y - 1.2*inch, 0.8*inch, 1.5*inch, LIGHT_NAV)
    text(c, label, 0.8*inch, y - 0.55*inch, size=18, bold=True, color=GOLD, align='center')
    text(c, title, 1.35*inch, y - 0.15*inch, size=14, bold=True, color=GOLD)
    text(c, body, 1.35*inch, y - 0.5*inch, size=11, color=WHITE_C)

c.showPage()

# ── SLIDE 5: DATA SOURCES ──────────────────────────────────────────────────────
new_page(c)
header(c, 'Data Capture — Sources', 'Section 03')

sources = [
    ('WRDS', 'Wharton Research Data Service',
     ['University of Pennsylvania data repository.',
      'Source: S&P 500 constituent history,',
      'quarterly financials (Compustat),',
      'and stock returns (CRSP).',
      'Coverage: Q1 2010 – Q4 2024.']),
    ('FRED', 'Federal Reserve Economic Data',
     ['Federal Reserve Bank of St. Louis.',
      'Source: GDP growth and CPI inflation.',
      'One macro value per quarter,',
      'matched to each company\'s feature quarter.',
      'Accessed via FRED public API.']),
    ('EDGAR', 'Electronic Data Gathering',
     ['SEC\'s official company filing repository.',
      'Supplement for 10-Q financial data.',
      'Accessed via API through Python.',
      'Provides additional quarterly fields',
      'not covered by Compustat alone.']),
]

for i, (abbr, full, lines) in enumerate(sources):
    x = 0.4*inch + i * 3.65*inch
    box(c, x, PAGE_H - 6.8*inch, 3.4*inch, 5.5*inch)
    text(c, abbr, x + 0.2*inch, PAGE_H - 2.0*inch, size=32, bold=True, color=GOLD)
    text(c, full, x + 0.2*inch, PAGE_H - 2.4*inch, size=10, color=MUTED)
    draw_rect(c, x + 0.2*inch, PAGE_H - 2.65*inch, 0.8*inch, 0.04*inch, GOLD)
    y = PAGE_H - 3.0*inch
    for line in lines:
        text(c, line, x + 0.2*inch, y, size=10)
        y -= 0.3*inch

text(c, 'All data accessed via API and processed with Python (pandas, statsmodels, scikit-learn)',
     0.5*inch, 0.2*inch, size=9, color=MUTED)
c.showPage()

# ── SLIDE 6: RAW VARIABLES ─────────────────────────────────────────────────────
new_page(c)
header(c, 'Data Capture — Raw Variables', 'Section 03 — Compustat Quarterly Fields')

vars_data = [
    ('prccq', 'Price Close (Quarter End)'),
    ('cshoq', 'Common Shares Outstanding'),
    ('mkvaltq', 'Market Capitalization'),
    ('revtq', 'Total Revenue'),
    ('cogsq', 'Cost of Goods Sold'),
    ('xsgaq', 'SG&A Expenses'),
    ('xrdq', 'R&D Expenses'),
    ('oiadpq', 'Operating Income After Depr.'),
    ('niq', 'Net Income'),
    ('ibq', 'Income Before Extraordinary Items'),
    ('piq', 'Pretax Income'),
    ('atq', 'Total Assets'),
    ('ceqq', 'Common Equity Total'),
    ('teqq', 'Total Stockholders Equity'),
    ('dlttq', 'Long-Term Debt'),
    ('dlcq', 'Debt in Current Liabilities'),
    ('actq', 'Current Assets'),
    ('lctq', 'Current Liabilities'),
    ('cheq', 'Cash & Short-Term Investments'),
    ('dpq', 'Depreciation & Amortization'),
    ('oibdpq', 'Operating Income Before Depr.'),
]

cols = 4
row_h = 0.38*inch
col_w = 2.65*inch
start_y = PAGE_H - 1.3*inch

for i, (code, label) in enumerate(vars_data):
    col = i % cols
    row = i // cols
    x = 0.4*inch + col * col_w
    y = start_y - row * row_h
    bg = NAVY_CARD if row % 2 == 0 else LIGHT_NAV
    draw_rect(c, x, y - 0.28*inch, col_w - 0.06*inch, row_h - 0.04*inch, bg)
    text(c, code, x + 0.08*inch, y - 0.12*inch, size=9, bold=True, color=GOLD)
    text(c, label, x + 0.85*inch, y - 0.12*inch, size=9, color=WHITE_C)

text(c, 'Source: WRDS Compustat Fundamentals Quarterly (fundq table)  |  Joined on gvkey identifier',
     0.5*inch, 0.2*inch, size=9, color=MUTED)
c.showPage()

# ── SLIDE 7: FINANCIAL RATIOS ──────────────────────────────────────────────────
new_page(c)
header(c, 'Financial Ratios — 14 Base Ratios', 'Section 04 — Derived from Raw Variables')

ratios = [
    ('Return on Assets (ROA)',     'Net Income / Total Assets',                   'Profitability', GOLD),
    ('Return on Equity (ROE)',     'Net Income / Common Equity',                  'Profitability', GOLD),
    ('Gross Margin',               '(Revenue - COGS) / Revenue',                  'Profitability', GOLD),
    ('Operating Margin',           'Op. Income / Revenue',                        'Profitability', GOLD),
    ('Net Margin',                 'Net Income / Revenue',                        'Profitability', GOLD),
    ('Asset Turnover',             'Revenue / Total Assets',                      'Efficiency',    BLUE),
    ('Current Ratio',              'Current Assets / Current Liabilities',        'Liquidity',     GREEN_C),
    ('Debt to Equity',             'Long-Term Debt / Common Equity',              'Leverage',      MUTED),
    ('Revenue Growth',             '(Rev - Lag Rev) / |Lag Rev|',                 'Growth',        HexColor('#9B59B6')),
    ('Net Income Growth',          '(NI - Lag NI) / |Lag NI|',                   'Growth',        HexColor('#9B59B6')),
    ('P/E Ratio',                  'Price / (EPS)',                               'Valuation',     HexColor('#1ABC9C')),
    ('Book-to-Market',             'Common Equity / Market Cap',                  'Valuation',     HexColor('#1ABC9C')),
    ('GDP Growth',                 'Quarter-over-quarter GDP change (FRED)',       'Macro',         MUTED),
    ('Inflation',                  'Quarter-over-quarter CPI change (FRED)',       'Macro',         MUTED),
]

row_h = 0.42*inch
col_w = 5.2*inch
start_y = PAGE_H - 1.3*inch

for i, (name, formula, cat, color) in enumerate(ratios):
    col = i % 2
    row = i // 2
    x = 0.4*inch + col * col_w
    y = start_y - row * row_h
    bg = NAVY_CARD if row % 2 == 0 else LIGHT_NAV
    draw_rect(c, x, y - 0.3*inch, col_w - 0.08*inch, row_h - 0.05*inch, bg)
    draw_rect(c, x, y - 0.3*inch, 0.04*inch, row_h - 0.05*inch, color)
    text(c, name, x + 0.12*inch, y - 0.08*inch, size=10, bold=True, color=WHITE_C)
    text(c, formula, x + 2.2*inch, y - 0.08*inch, size=9, color=MUTED)
    text(c, cat, x + 4.4*inch, y - 0.08*inch, size=8, bold=True, color=color)

text(c, 'Lag values computed via groupby(gvkey).shift(1)  |  GDP and Inflation matched per quarter',
     0.5*inch, 0.2*inch, size=9, color=MUTED)
c.showPage()

# ── SLIDE 8: DELTA FEATURES ────────────────────────────────────────────────────
new_page(c)
header(c, 'Delta Features — Quarter-over-Quarter Momentum', 'Section 04 — 10 Additional Features')

intro = ('Delta features capture the direction of change in each ratio — whether fundamentals are improving '
         'or deteriorating. Two companies with the same ROA tell very different stories if one is rising and the other falling.')
c.setFillColor(WHITE_C)
c.setFont('Helvetica', 11)
c.drawString(0.5*inch, PAGE_H - 1.3*inch, intro[:93])
c.drawString(0.5*inch, PAGE_H - 1.55*inch, intro[93:])

box(c, 0.4*inch, PAGE_H - 6.5*inch, 4.5*inch, 4.65*inch, title='Formula & Example', t_size=13)
formula_lines = [
    'Delta_Ratio(Q) = Ratio(Q) - Ratio(Q-1)',
    '',
    'Computed via groupby(gvkey).diff()',
    '',
    'Example:',
    '  ROA (Q3 2024) = 5.0%',
    '  ROA (Q4 2024) = 8.0%',
    '  Delta_ROA     = +3.0%  (Improving)',
    '',
    'Positive delta = improving fundamentals',
    'Negative delta = deteriorating fundamentals',
]
y = PAGE_H - 2.55*inch
for line in formula_lines:
    text(c, line, 0.6*inch, y, size=11)
    y -= 0.28*inch

delta_feats = [
    'Delta ROA',            'Delta ROE',
    'Delta Gross Margin',   'Delta Operating Margin',
    'Delta Net Margin',     'Delta Asset Turnover',
    'Delta Current Ratio',  'Delta Debt/Equity',
    'Delta P/E Ratio',      'Delta Book-to-Market',
]

text(c, '10 Delta Features Added', 5.3*inch, PAGE_H - 2.0*inch, size=13, bold=True, color=GOLD)

row_h = 0.42*inch
for i, feat in enumerate(delta_feats):
    col = i % 2
    row = i // 2
    x = 5.3*inch + col * 2.8*inch
    y = PAGE_H - 2.5*inch - row * row_h
    draw_rect(c, x, y - 0.28*inch, 2.6*inch, row_h - 0.05*inch, LIGHT_NAV)
    draw_rect(c, x, y - 0.28*inch, 0.04*inch, row_h - 0.05*inch, GOLD)
    text(c, feat, x + 0.12*inch, y - 0.08*inch, size=10)

text(c, 'Total features entering VIF analysis: 24   (14 base ratios + 10 delta features)',
     0.5*inch, 0.2*inch, size=10, bold=True, color=GOLD)
c.showPage()

# ── SLIDE 9: OUTPERFORMER DEFINITION ──────────────────────────────────────────
new_page(c)
header(c, 'Outperformer Definition & Forward-Looking Label', 'Section 04')

draw_rect(c, 0.4*inch, PAGE_H - 2.2*inch, PAGE_W - 0.8*inch, 0.9*inch, NAVY_CARD)
draw_rect(c, 0.4*inch, PAGE_H - 1.35*inch, PAGE_W - 0.8*inch, 0.08*inch, GOLD)
text(c, 'Label Construction — Forward-Looking by One Quarter', 0.6*inch, PAGE_H - 1.6*inch, size=14, bold=True, color=GOLD)
text(c, 'Stock Return (Q+1) > S&P 500 Return (Q+1)   -->  Label = 1  (Outperformer)',
     0.6*inch, PAGE_H - 1.9*inch, size=12, color=GREEN_C, bold=True)
text(c, 'Stock Return (Q+1) <= S&P 500 Return (Q+1)  -->  Label = 0  (Underperformer)',
     0.6*inch, PAGE_H - 2.15*inch, size=12, color=RED_C, bold=True)

box(c, 0.4*inch, PAGE_H - 6.5*inch, 4.0*inch, 3.9*inch, title='Feature Quarter: Q4 2024', t_size=12)
lines1 = [
    'Financial ratios from 10-Q filings.',
    '14 base ratios + 10 delta features.',
    'Available before Q1 2025 begins.',
    '',
    'Features are derived from company',
    'financials that are public record',
    'by the time of prediction.',
]
y = PAGE_H - 3.2*inch
for line in lines1:
    text(c, line, 0.6*inch, y, size=11)
    y -= 0.28*inch

text(c, '  -->  ', 4.55*inch, PAGE_H - 5.1*inch, size=22, bold=True, color=GOLD)

box(c, 5.4*inch, PAGE_H - 6.5*inch, 4.0*inch, 3.9*inch, accent=BLUE, title='Label Quarter: Q1 2025', t_size=12)
lines2 = [
    'Was stock\'s Q1 2025 return greater',
    'than SPY Q1 2025 return?',
    '',
    'Yes -> Label = 1  (Outperformer)',
    'No  -> Label = 0  (Underperformer)',
    '',
    'Computed via CRSP quarterly returns.',
]
y = PAGE_H - 3.2*inch
for line in lines2:
    color = GREEN_C if 'Yes' in line else (RED_C if 'No' in line else WHITE_C)
    text(c, line, 5.6*inch, y, size=11, color=color)
    y -= 0.28*inch

text(c, 'outperformer_next = groupby(gvkey)[outperformer_quarterly].shift(-1)  |  Training data: 16,589 rows',
     0.5*inch, 0.2*inch, size=9, color=MUTED)
c.showPage()

# ── SLIDE 10: DATA CLEANING ────────────────────────────────────────────────────
new_page(c)
header(c, 'Data Cleaning', 'Section 05 — Winsorization, Standardization, NaN Removal')

steps = [
    ('Step 1: Winsorization', GOLD,
     ['Extreme outlier values capped at 1st and 99th percentile.',
      '',
      'Example: If ROA = -300%, it is capped at -15%',
      '(the 1st percentile value). The row is kept;',
      'only the extreme value is replaced.',
      '',
      'Applied per ratio using training data bounds.',
      'Test data uses same bounds to prevent data leakage.']),
    ('Step 2: Standardization (Z-Score)', BLUE,
     ['Each ratio scaled to mean=0, std=1.',
      '',
      'Without this, P/E Ratio (50x) would dominate',
      'over ROA (0.05), biasing the model.',
      '',
      'Ensures all 24 features on the same scale',
      'before VIF analysis and PCA.']),
    ('Step 3: NaN Removal', GREEN_C,
     ['Rows with any missing values are dropped.',
      '',
      'Common causes:',
      '  - Companies with zero revenue (div by zero)',
      '  - First entries (no lag for delta features)',
      '',
      'Result: 21,285 -> 16,589 complete rows.',
      '(-22% of observations removed)']),
]

for i, (title, color, lines) in enumerate(steps):
    x = 0.4*inch + i * 3.65*inch
    box(c, x, PAGE_H - 6.8*inch, 3.4*inch, 5.4*inch, accent=color, title=title, t_size=11)
    y = PAGE_H - 2.6*inch
    for line in lines:
        text(c, line, x + 0.18*inch, y, size=10)
        y -= 0.28*inch

y_stat = PAGE_H - 7.5*inch
stat_box(c, 'Rows Before', '21,285', 'training observations', 0.4*inch, y_stat, 2.5*inch, 0.65*inch)
text(c, '->>', 3.1*inch, y_stat + 0.22*inch, size=18, bold=True, color=GOLD)
stat_box(c, 'Rows After', '16,589', 'complete rows', 3.5*inch, y_stat, 2.5*inch, 0.65*inch, val_color=GREEN_C)

c.showPage()

# ── SLIDE 11: VIF ANALYSIS ─────────────────────────────────────────────────────
new_page(c)
header(c, 'VIF Analysis — Multicollinearity Removal', 'Section 06 — Variance Inflation Factor, Threshold = 2.5')

desc = ('Financial ratios are correlated — e.g., Net Margin and ROA both measure profitability. '
        'VIF detects this collinearity. Features with VIF > 2.5 are iteratively removed.')
c.setFillColor(WHITE_C)
c.setFont('Helvetica', 11)
c.drawString(0.5*inch, PAGE_H - 1.3*inch, desc[:93])
c.drawString(0.5*inch, PAGE_H - 1.55*inch, desc[93:])

box(c, 0.4*inch, PAGE_H - 6.5*inch, 3.8*inch, 4.65*inch, title='VIF Procedure', t_size=13)
procedure = [
    '1. Compute VIF for all 24 features',
    '2. Find the feature with highest VIF',
    '3. If VIF > 2.5, remove that feature',
    '4. Repeat until all VIF <= 2.5',
    '5. Threshold of 2.5 is stricter than',
    '   the standard 5.0 cutoff',
    '   (Ananthakumar & Sarkar 2017)',
]
y = PAGE_H - 2.55*inch
for line in procedure:
    text(c, line, 0.6*inch, y, size=11)
    y -= 0.33*inch

text(c, '20 Features Retained (of 24)', 4.4*inch, PAGE_H - 2.0*inch, size=13, bold=True, color=GOLD)

kept = [
    'roe',              'gross_margin',
    'op_margin',        'asset_turnover',
    'current_ratio',    'debt_to_equity',
    'rev_growth',       'ni_growth',
    'pe_ratio',         'book_to_market',
    'gdp_growth',       'inflation',
    'delta_roe',        'delta_gross_margin',
    'delta_net_margin', 'delta_asset_turnover',
    'delta_current_ratio', 'delta_debt_to_equity',
    'delta_pe_ratio',   'delta_book_to_market',
]

row_h = 0.35*inch
for i, feat in enumerate(kept):
    col = i % 2
    row = i // 2
    x = 4.4*inch + col * 2.7*inch
    y = PAGE_H - 2.45*inch - row * row_h
    bg = LIGHT_NAV if row % 2 == 0 else NAVY_CARD
    draw_rect(c, x, y - 0.24*inch, 2.55*inch, row_h - 0.04*inch, bg)
    draw_rect(c, x, y - 0.24*inch, 0.04*inch, row_h - 0.04*inch, GREEN_C)
    text(c, feat, x + 0.1*inch, y - 0.1*inch, size=9, color=WHITE_C)

stat_box(c, 'Retained', '20/24', 'VIF <= 2.5', 0.4*inch, PAGE_H - 7.5*inch, 2.0*inch, 0.65*inch, val_color=GREEN_C)
stat_box(c, 'Removed', '4', 'VIF > 2.5', 2.6*inch, PAGE_H - 7.5*inch, 2.0*inch, 0.65*inch, val_color=RED_C)
stat_box(c, 'Threshold', '2.5', 'Paper benchmark', 4.8*inch, PAGE_H - 7.5*inch, 2.5*inch, 0.65*inch)
c.showPage()

# ── SLIDE 12: PCA ──────────────────────────────────────────────────────────────
new_page(c)
header(c, 'PCA Analysis — Dimensionality Reduction', 'Section 07 — Principal Component Analysis, Threshold >= 5%')

desc = ('Even after VIF filtering, 20 correlated features remain. PCA compresses them into uncorrelated '
        'components, each capturing a distinct pattern — eliminating residual multicollinearity.')
c.setFillColor(WHITE_C)
c.setFont('Helvetica', 11)
c.drawString(0.5*inch, PAGE_H - 1.3*inch, desc[:95])
c.drawString(0.5*inch, PAGE_H - 1.55*inch, desc[95:])

box(c, 0.4*inch, PAGE_H - 6.5*inch, 3.8*inch, 4.65*inch, title='Component Selection Rule', t_size=12)
rule_lines = [
    'Threshold: >= 5% individual variance explained',
    '',
    'Applied on faculty advisor recommendation.',
    '',
    'Rule: n_comp = max(1, count of',
    '  components where var. ratio >= 0.05)',
    '',
    'Result: 9 principal components retained',
    'for the global model.',
    '',
    'Components vary per sector/configuration.',
]
y = PAGE_H - 2.55*inch
for line in rule_lines:
    text(c, line, 0.6*inch, y, size=10)
    y -= 0.3*inch

text(c, 'Component Themes (Global Model)', 4.4*inch, PAGE_H - 2.0*inch, size=13, bold=True, color=GOLD)

pca_rows = [
    ('PC1', 'Profitability cluster — ROA, margins'),
    ('PC2', 'Leverage & liquidity — Debt/Equity, Current Ratio'),
    ('PC3', 'Revenue momentum — Rev Growth, Delta Rev'),
    ('PC4', 'Valuation — P/E Ratio, Book-to-Market'),
    ('PC5', 'NI & margin delta — Delta Net Margin, Delta ROE'),
    ('PC6', 'Asset efficiency — Asset Turnover'),
    ('PC7', 'Macro environment — GDP Growth, Inflation'),
    ('PC8', 'Equity momentum — Delta ROE, Delta B/M'),
    ('PC9', 'Mixed residual signal'),
]

row_h = 0.42*inch
for i, (pc, theme) in enumerate(pca_rows):
    x = 4.4*inch
    y = PAGE_H - 2.45*inch - i * row_h
    bg = LIGHT_NAV if i % 2 == 0 else NAVY_CARD
    draw_rect(c, x, y - 0.3*inch, 5.8*inch, row_h - 0.04*inch, bg)
    draw_rect(c, x, y - 0.3*inch, 0.5*inch, row_h - 0.04*inch, GOLD)
    text(c, pc, x + 0.25*inch, y - 0.12*inch, size=10, bold=True, color=NAVY, align='center')
    text(c, theme, x + 0.62*inch, y - 0.12*inch, size=10, color=WHITE_C)

stat_box(c, 'Components Kept', '9', 'Global model', 0.4*inch, PAGE_H - 7.5*inch, 2.0*inch, 0.65*inch)
stat_box(c, 'Threshold', '>=5%', 'Per component', 2.6*inch, PAGE_H - 7.5*inch, 2.0*inch, 0.65*inch)
stat_box(c, 'Significant', '4/9', 'p<0.05: PC1,PC3,PC6,PC7', 4.8*inch, PAGE_H - 7.5*inch, 3.0*inch, 0.65*inch, val_color=GREEN_C)
c.showPage()

# ── SLIDE 13: LR SETUP ─────────────────────────────────────────────────────────
new_page(c)
header(c, 'Logistic Regression — Model Setup', 'Section 08 — Global Pooled Model')

desc = ('With PCA components as inputs, logistic regression models the probability that a stock will outperform '
        'the S&P 500 the following quarter. Trained on Q1 2010 – Q4 2024.')
c.setFillColor(WHITE_C)
c.setFont('Helvetica', 11)
c.drawString(0.5*inch, PAGE_H - 1.3*inch, desc[:93])
c.drawString(0.5*inch, PAGE_H - 1.55*inch, desc[93:])

configs = [
    ('Training Period',      'Q1 2010 – Q4 2024',    '15 years of quarterly data'),
    ('Training Rows',        '16,589',                'complete rows after cleaning'),
    ('Companies',            '~500',                  'S&P 500 constituents (time-varying)'),
    ('Target Variable',      'outperformer_next',     '1 = beats SPY next Q, 0 = does not'),
    ('Input Features',       '9 PCA Components',      'derived from 20 VIF-filtered ratios'),
    ('Model',                'Logistic Regression',   'statsmodels Logit, max_iter=200'),
    ('Cutoff Optimization',  'Train-set threshold',   'optimized over 0.30 – 0.75 range'),
    ('Class Weights',        'Balanced',              'accounts for outperformer imbalance'),
]

row_h = 0.74*inch
col_w = 5.2*inch
for i, (label, val, note) in enumerate(configs):
    col = i % 2
    row = i // 2
    x = 0.4*inch + col * col_w
    y = PAGE_H - 2.1*inch - row * row_h
    draw_rect(c, x, y - 0.62*inch, col_w - 0.08*inch, row_h - 0.06*inch, NAVY_CARD)
    draw_rect(c, x, y - 0.62*inch, 0.06*inch, row_h - 0.06*inch, GOLD)
    text(c, label, x + 0.15*inch, y - 0.18*inch, size=9, color=MUTED)
    text(c, val, x + 0.15*inch, y - 0.45*inch, size=14, bold=True, color=WHITE_C)
    text(c, note, x + 3.0*inch, y - 0.45*inch, size=8, color=MUTED)

text(c, 'Benchmark: Ananthakumar & Sarkar (2017) — 71.2% accuracy on S&P 500 using logistic regression',
     0.5*inch, 0.2*inch, size=10, color=GOLD, bold=True)
c.showPage()

# ── SLIDE 14: GLOBAL RESULTS ───────────────────────────────────────────────────
new_page(c)
header(c, 'Global Model Results', 'Section 08 — All S&P 500, No Segmentation')

stat_box(c, 'Test Accuracy', '53.2%', 'Global pooled model',
         0.4*inch, PAGE_H - 2.15*inch, 2.4*inch, 1.05*inch)
stat_box(c, 'LR AUC', '0.5381', 'Logistic Regression',
         3.0*inch, PAGE_H - 2.15*inch, 2.4*inch, 1.05*inch)
stat_box(c, 'GB AUC', '0.6589', 'Gradient Boosting benchmark',
         5.6*inch, PAGE_H - 2.15*inch, 2.4*inch, 1.05*inch, val_color=BLUE)
stat_box(c, 'Sig. PCA Components', '4 / 9', 'p < 0.05',
         8.2*inch, PAGE_H - 2.15*inch, 2.5*inch, 1.05*inch, val_color=GREEN_C)

box(c, 0.4*inch, PAGE_H - 6.8*inch, 4.5*inch, 4.35*inch, title='Key Interpretation', t_size=12)
interp_lines = [
    ('AUC 0.5381:', 'Near-random discrimination globally.', GOLD),
    ('', 'The model finds weak but real signal.', MUTED),
    ('53.2% Accuracy:', 'Marginally above 50% baseline.', WHITE_C),
    ('', 'Markets are competitive to predict.', MUTED),
    ('Statistically Sig.:', 'p-value < 0.05 — model is not', GREEN_C),
    ('', 'random; it finds true signal.', MUTED),
    ('GB AUC 0.6589:', 'Non-linear relationships exist', BLUE),
    ('', 'that LR cannot fully capture.', MUTED),
    ('McFadden R2:', '0.0073 — weak but significant.', MUTED),
]
y = PAGE_H - 3.0*inch
for label, body, color in interp_lines:
    if label:
        text(c, label, 0.6*inch, y, size=10, bold=True, color=color)
    text(c, body, 2.2*inch, y, size=10, color=WHITE_C)
    y -= 0.3*inch

box(c, 5.2*inch, PAGE_H - 6.8*inch, 5.2*inch, 4.35*inch, title='Performance vs. Benchmark', t_size=12)
bench_rows = [
    ('Metric',              'Our Result', 'Benchmark (2017)'),
    ('Accuracy',            '53.2%',      '71.2%'),
    ('AUC',                 '0.5381',     '~0.75 (est.)'),
    ('Sensitivity',         '~52%',       'Not reported'),
    ('Specificity',         '~54%',       'Not reported'),
    ('Segmentation',        'Best: 63.9%', 'Single model'),
]
row_h_t = 0.45*inch
for i, (m, ours, bench) in enumerate(bench_rows):
    y = PAGE_H - 3.0*inch - i * row_h_t
    bg = GOLD if i == 0 else (NAVY_CARD if i % 2 == 1 else LIGHT_NAV)
    draw_rect(c, 5.4*inch, y - 0.3*inch, 4.8*inch, row_h_t - 0.04*inch, bg)
    tc = NAVY if i == 0 else WHITE_C
    text(c, m, 5.55*inch, y - 0.12*inch, size=10, bold=(i==0), color=tc)
    text(c, ours, 7.3*inch, y - 0.12*inch, size=10, bold=(i==0), color=tc if i==0 else GREEN_C)
    text(c, bench, 8.7*inch, y - 0.12*inch, size=10, color=tc if i==0 else MUTED)

c.showPage()

# ── SLIDE 15: GRADIENT BOOSTING ─────────────────────────────────────────────────
new_page(c)
header(c, 'Gradient Boosting — Non-Linear Benchmark', 'Section 08 — LR vs GB Comparison')

desc = ('To test the linearity assumption, Gradient Boosting (GB) was run as a diagnostic benchmark. '
        'GB captures non-linear patterns that logistic regression cannot model.')
c.setFillColor(WHITE_C)
c.setFont('Helvetica', 11)
c.drawString(0.5*inch, PAGE_H - 1.3*inch, desc[:95])
c.drawString(0.5*inch, PAGE_H - 1.55*inch, desc[95:])

box(c, 0.4*inch, PAGE_H - 6.5*inch, 4.8*inch, 4.65*inch, title='Global Model Comparison', t_size=13)
headers_t = ['Model', 'Train AUC', 'Test AUC', 'Role']
cols_x = [0.6*inch, 2.1*inch, 3.1*inch, 3.9*inch]
col_ws2 = [1.4*inch, 0.9*inch, 0.9*inch, 1.2*inch]
draw_rect(c, 0.6*inch, PAGE_H - 2.55*inch, 4.4*inch, 0.36*inch, GOLD)
for j, (hdr, cx) in enumerate(zip(headers_t, cols_x)):
    text(c, hdr, cx + 0.05*inch, PAGE_H - 2.35*inch, size=10, bold=True, color=NAVY)

rows_t = [
    ('Logistic Regression', '0.5381', '0.5381', 'Primary model — interpretable', WHITE_C),
    ('Gradient Boosting',   '0.6589', '0.6589', 'Diagnostic benchmark only', BLUE),
]
for i, (model, tr, te, role, rc) in enumerate(rows_t):
    y = PAGE_H - 3.1*inch - i * 0.55*inch
    bg = LIGHT_NAV if i % 2 == 0 else NAVY_CARD
    draw_rect(c, 0.6*inch, y - 0.35*inch, 4.4*inch, 0.48*inch, bg)
    text(c, model, 0.65*inch, y - 0.12*inch, size=10, bold=True, color=rc)
    text(c, tr, 2.15*inch, y - 0.12*inch, size=10, color=GOLD if i==0 else BLUE)
    text(c, te, 3.15*inch, y - 0.12*inch, size=10, color=GOLD if i==0 else BLUE)
    text(c, role, 3.95*inch, y - 0.12*inch, size=9, color=MUTED)

text(c, 'AUC Improvement (GB vs LR): +12.1 percentage points', 0.6*inch, PAGE_H - 4.4*inch, size=12, bold=True, color=BLUE)

box(c, 5.45*inch, PAGE_H - 6.5*inch, 5.0*inch, 4.65*inch, title='What This Means', t_size=13)
what_lines = [
    'The gap: LR (0.54) vs GB (0.66)',
    'confirms non-linear patterns exist.',
    '',
    'LR finds real, significant signal but',
    'misses interaction effects between ratios.',
    '',
    'GB is used ONLY as a diagnostic tool.',
    'LR remains the primary model because:',
    '  - Interpretable coefficients',
    '  - Odds ratios',
    '  - p-values for significance testing',
    '  - Required for academic analysis',
    '',
    'Future work: explore GB, Random',
    'Forest, and neural network models.',
]
y = PAGE_H - 2.55*inch
for line in what_lines:
    text(c, line, 5.65*inch, y, size=10)
    y -= 0.28*inch

c.showPage()

# ── SLIDE 16: SECTION DIVIDER ──────────────────────────────────────────────────
new_page(c)
draw_rect(c, 0, PAGE_H/2 - 0.06*inch, PAGE_W, 0.12*inch, GOLD)
text(c, 'Section 09', PAGE_W/2, PAGE_H/2 + 1.2*inch, size=16, bold=True, color=GOLD, align='center')
text(c, 'Segmentation & Results', PAGE_W/2, PAGE_H/2 + 0.4*inch, size=48, bold=True, align='center')
text(c, 'Market Cap  |  Sector GICS  |  Clustering', PAGE_W/2, PAGE_H/2 - 0.4*inch, size=20, color=MUTED, align='center')
c.showPage()

# ── SLIDE 17: MARKET CAP ──────────────────────────────────────────────────────
new_page(c)
header(c, 'Segmentation — Market Capitalization', 'Section 09 — Configuration 1')

desc = 'Companies segmented by market cap. Separate LR model trained and evaluated per size tier.'
text(c, desc, 0.5*inch, PAGE_H - 1.3*inch, size=11)

tiers = [
    ('Large Cap',  '> $10B',    '54.2%', '0.558', ['Most institutional coverage.', 'Efficient pricing — harder to predict.']),
    ('Mid Cap',    '$2B – $10B','52.8%', '0.542', ['Some analyst coverage.', 'More earnings variability.']),
    ('Small Cap',  '< $2B',     '54.5%', '0.535', ['Limited analyst coverage.', 'Higher fundamental variability.']),
]

for i, (tier, threshold, acc, auc, notes) in enumerate(tiers):
    x = 0.4*inch + i * 3.65*inch
    box(c, x, PAGE_H - 7.0*inch, 3.4*inch, 5.3*inch, accent=BLUE, title=tier, t_size=16)
    text(c, threshold, x + 0.2*inch, PAGE_H - 2.7*inch, size=12, color=MUTED)
    draw_rect(c, x + 0.2*inch, PAGE_H - 3.2*inch, 0.8*inch, 0.04*inch, GOLD)
    text(c, 'Accuracy', x + 0.2*inch, PAGE_H - 3.4*inch, size=10, color=MUTED)
    text(c, acc, x + 0.2*inch, PAGE_H - 3.95*inch, size=36, bold=True, color=WHITE_C)
    text(c, f'AUC: {auc}', x + 0.2*inch, PAGE_H - 4.4*inch, size=12, color=GOLD)
    for j, note in enumerate(notes):
        text(c, note, x + 0.2*inch, PAGE_H - 4.8*inch - j*0.3*inch, size=10, color=MUTED)

draw_rect(c, 0.4*inch, 0.15*inch, PAGE_W - 0.8*inch, 0.5*inch, LIGHT_NAV)
text(c, 'Conclusion: Market Cap alone provides only marginal improvement over global 53.2% baseline.',
     0.6*inch, 0.28*inch, size=10, color=MUTED)
c.showPage()

# ── SLIDE 18: SECTOR SEGMENTATION ──────────────────────────────────────────────
new_page(c)
header(c, 'Segmentation — GICS Sector', 'Section 09 — Configuration 2')

desc = ('Separate LR model per GICS sector. Financial ratios mean different things across sectors '
        '— sector-specific models find stronger patterns.')
c.setFillColor(WHITE_C)
c.setFont('Helvetica', 11)
c.drawString(0.5*inch, PAGE_H - 1.3*inch, desc[:93])
c.drawString(0.5*inch, PAGE_H - 1.55*inch, desc[93:])

sectors = [
    ('Communication Services', '428',  '59.5%', '0.6059', True),
    ('Consumer Discretionary', '2668', '54.1%', '0.5305', False),
    ('Consumer Staples',       '1030', '55.7%', '0.5510', False),
    ('Energy',                 '261',  '61.7%', '0.6036', True),
    ('Financials',             '4108', '55.0%', '0.5350', False),
    ('Health Care',            '1126', '54.3%', '0.5578', False),
    ('Industrials',            '4183', '54.5%', '0.5350', False),
    ('Information Technology', '2240', '53.2%', '0.5420', False),
    ('Materials',              '2781', '53.2%', '0.5481', False),
    ('Real Estate',            '424',  '59.5%', '0.6010', True),
    ('Utilities',              '1757', '54.5%', '0.5420', False),
]

draw_rect(c, 0.4*inch, PAGE_H - 1.95*inch, PAGE_W - 0.8*inch, 0.3*inch, LIGHT_NAV)
text(c, 'Sector', 0.55*inch, PAGE_H - 1.83*inch, size=9, bold=True, color=MUTED)
text(c, 'N Obs', 3.7*inch, PAGE_H - 1.83*inch, size=9, bold=True, color=MUTED, align='center')
text(c, 'Accuracy', 5.5*inch, PAGE_H - 1.83*inch, size=9, bold=True, color=MUTED, align='center')
text(c, 'AUC', 7.0*inch, PAGE_H - 1.83*inch, size=9, bold=True, color=MUTED, align='center')

row_h = 0.42*inch
for i, (sector, n, acc, auc, best) in enumerate(sectors):
    y = PAGE_H - 2.35*inch - i * row_h
    bg = NAVY_CARD if i % 2 == 0 else LIGHT_NAV
    draw_rect(c, 0.4*inch, y - 0.3*inch, PAGE_W - 0.8*inch, row_h - 0.04*inch, bg)
    accent = GREEN_C if best else MUTED
    draw_rect(c, 0.4*inch, y - 0.3*inch, 0.04*inch, row_h - 0.04*inch, accent)
    sc = GREEN_C if best else WHITE_C
    text(c, sector, 0.55*inch, y - 0.1*inch, size=10, bold=best, color=sc)
    text(c, n, 3.7*inch, y - 0.1*inch, size=10, color=MUTED, align='center')
    acc_color = GREEN_C if float(acc.strip('%')) > 58 else WHITE_C
    text(c, acc, 5.5*inch, y - 0.1*inch, size=10, bold=(acc_color==GREEN_C), color=acc_color, align='center')
    text(c, auc, 7.0*inch, y - 0.1*inch, size=10, color=GOLD if best else MUTED, align='center')

draw_rect(c, 0.4*inch, 0.15*inch, PAGE_W - 0.8*inch, 0.55*inch, LIGHT_NAV)
text(c, 'Best: Communication Services (59.5%, AUC 0.606) | Energy (61.7%) | Real Estate (59.5%)',
     0.6*inch, 0.42*inch, size=10, bold=True, color=GREEN_C)
text(c, 'Clustering within Comm. Services improved further to 63.9% accuracy — best across all 45 configurations',
     0.6*inch, 0.22*inch, size=9, color=GOLD)
c.showPage()

# ── SLIDE 19: BEST CONFIGURATION ──────────────────────────────────────────────
new_page(c)
header(c, 'Best Config — Communication Services + Clustering', 'Section 09 — Config 4: Sector + K-Means (k=2)')

desc = ('Within Communication Services, K-Means (k=2) split the sector into two sub-groups with '
        'distinct financial profiles. Cluster 0 (122 companies) was the best of all 45 configurations tested.')
c.setFillColor(WHITE_C)
c.setFont('Helvetica', 11)
c.drawString(0.5*inch, PAGE_H - 1.3*inch, desc[:95])
c.drawString(0.5*inch, PAGE_H - 1.55*inch, desc[95:])

stat_box(c, 'Best AUC', '0.6902', 'Comm. Services — Cluster 0', 0.4*inch, PAGE_H - 2.65*inch, 2.4*inch, 1.0*inch, val_color=GOLD)
stat_box(c, 'Best Accuracy', '63.9%', '122 observations', 3.0*inch, PAGE_H - 2.65*inch, 2.4*inch, 1.0*inch, val_color=GREEN_C)
stat_box(c, 'Weighted AUC', '0.5720', 'Across all 45 configs', 5.6*inch, PAGE_H - 2.65*inch, 2.4*inch, 1.0*inch)
stat_box(c, 'Configs Tested', '45', 'All sector x cluster combos', 8.2*inch, PAGE_H - 2.65*inch, 2.4*inch, 1.0*inch, val_color=BLUE)

box(c, 0.4*inch, PAGE_H - 6.7*inch, 4.5*inch, 3.8*inch, title='Top 4 Configurations (of 45)', t_size=12)
top4 = [
    ('1st', 'Comm. Services — Cluster 0',  '0.6902', '63.9%', True),
    ('2nd', 'Comm. Services — Cluster 1',  '0.6099', '58.0%', False),
    ('3rd', 'Communication Services',       '0.6059', '59.5%', False),
    ('4th', 'Comm. Services + MktCap',     '0.6023', '59.0%', False),
]
for i, (rank, group, auc, acc, is_best) in enumerate(top4):
    y = PAGE_H - 3.5*inch - i * 0.6*inch
    bg = LIGHT_NAV if i % 2 == 0 else NAVY_CARD
    draw_rect(c, 0.6*inch, y - 0.42*inch, 4.1*inch, 0.52*inch, bg)
    draw_rect(c, 0.6*inch, y - 0.42*inch, 0.4*inch, 0.52*inch, GOLD if is_best else LIGHT_NAV)
    text(c, rank, 0.8*inch, y - 0.18*inch, size=9, bold=True, color=NAVY if is_best else MUTED, align='center')
    text(c, group, 1.1*inch, y - 0.18*inch, size=10, bold=is_best, color=GOLD if is_best else WHITE_C)
    text(c, f'AUC {auc}', 3.4*inch, y - 0.18*inch, size=9, color=GOLD if is_best else MUTED)
    text(c, acc, 4.1*inch, y - 0.18*inch, size=10, bold=is_best, color=GREEN_C if is_best else MUTED)

box(c, 5.2*inch, PAGE_H - 6.7*inch, 5.2*inch, 3.8*inch, title='Why Communication Services?', t_size=12)
why_lines = [
    'Companies like Netflix, Meta, Google, Disney',
    'have highly distinctive financial ratio patterns.',
    '',
    'Subscriber growth, content investment,',
    'and advertising revenue create strong',
    'fundamental differentiation.',
    '',
    'Clustering found a subscription-driven',
    'sub-group (Cluster 0) with especially',
    'strong predictive signal.',
    '',
    'Benchmark: Ananthakumar & Sarkar 71.2%',
    'Our best result: 63.9%',
]
y = PAGE_H - 3.5*inch
for line in why_lines:
    text(c, line, 5.4*inch, y, size=10)
    y -= 0.28*inch

c.showPage()

# ── SLIDE 20: 2025 SETUP ───────────────────────────────────────────────────────
new_page(c)
header(c, '2025 Out-of-Sample Testing', 'Section 10 — True Forward-Looking Validation')

desc = ('The model trained on Q1 2010 – Q4 2024 was applied to predict S&P 500 outperformers '
        'for all four quarters of 2025 — data the model never saw during training.')
c.setFillColor(WHITE_C)
c.setFont('Helvetica', 11)
c.drawString(0.5*inch, PAGE_H - 1.3*inch, desc[:95])
c.drawString(0.5*inch, PAGE_H - 1.55*inch, desc[95:])

quarters_2025 = [
    ('Q4 2024 ->', 'Q1 2025', '334 stocks', '44.6%', 'New addition — first true OOS', False),
    ('Q1 2025 ->', 'Q2 2025', '403 stocks', '55.3%', 'SPY +10.6% (strong market)', True),
    ('Q2 2025 ->', 'Q3 2025', '409 stocks', '56.2%', 'Largest 2025 sample', True),
    ('Q3 2025 ->', 'Q4 2025', '73 stocks',  '57.5%', 'Partial: early filers only', True),
]

for i, (feat, label, n, acc, note, is_good) in enumerate(quarters_2025):
    x = 0.4*inch + i * 2.7*inch
    acc_val = float(acc.strip('%'))
    color = GREEN_C if is_good else RED_C
    box(c, x, PAGE_H - 6.8*inch, 2.5*inch, 4.95*inch, accent=color)
    text(c, feat, x + 0.15*inch, PAGE_H - 2.35*inch, size=10, color=MUTED)
    text(c, label, x + 0.15*inch, PAGE_H - 2.75*inch, size=16, bold=True, color=WHITE_C)
    text(c, n, x + 0.15*inch, PAGE_H - 3.1*inch, size=10, color=MUTED)
    draw_rect(c, x + 0.15*inch, PAGE_H - 3.4*inch, 0.7*inch, 0.04*inch, color)
    text(c, 'Accuracy', x + 0.15*inch, PAGE_H - 3.6*inch, size=9, color=MUTED)
    text(c, acc, x + 0.15*inch, PAGE_H - 4.1*inch, size=32, bold=True, color=color)
    c.setFillColor(WHITE_C)
    c.setFont('Helvetica', 9)
    c.drawString(x + 0.15*inch, PAGE_H - 4.5*inch, note)

draw_rect(c, 0.4*inch, 0.15*inch, PAGE_W - 0.8*inch, 0.62*inch, LIGHT_NAV)
text(c, 'Note: Q4 2025 has only 73 stocks — Q3 2025 financials were not fully filed at extraction time.',
     0.6*inch, 0.5*inch, size=9, color=MUTED)
text(c, 'Early filers tend to be larger, well-governed companies. Results for this quarter should be interpreted cautiously.',
     0.6*inch, 0.28*inch, size=9, color=MUTED)
c.showPage()

# ── SLIDE 21: PORTFOLIO VS SPY ─────────────────────────────────────────────────
new_page(c)
header(c, '2025 Portfolio vs S&P 500', 'Section 10 — $10,000 Simulated Portfolio')

desc = ('Portfolio constructed each quarter from predicted outperformers, allocated proportionally by market cap. '
        'Compared against same $10,000 invested in SPY (S&P 500 ETF).')
c.setFillColor(WHITE_C)
c.setFont('Helvetica', 11)
c.drawString(0.5*inch, PAGE_H - 1.3*inch, desc[:95])
c.drawString(0.5*inch, PAGE_H - 1.55*inch, desc[95:])

headers_p = ['Quarter', 'Stocks', 'Pred. Out.', 'Model Return', 'SPY Return', 'Alpha', 'Beat SPY']
cols_px = [0.5*inch, 2.0*inch, 3.1*inch, 4.3*inch, 6.1*inch, 7.7*inch, 9.3*inch]
draw_rect(c, 0.4*inch, PAGE_H - 2.05*inch, PAGE_W - 0.8*inch, 0.38*inch, LIGHT_NAV)
for hdr, cx in zip(headers_p, cols_px):
    text(c, hdr, cx, PAGE_H - 1.85*inch, size=9, bold=True, color=MUTED)

port_rows = [
    ('Q2 2025', '387', '172', '+6.39%', '+10.57%', '-4.18%', False),
    ('Q3 2025', '391', '211', '+6.74%', '+7.79%',  '-1.06%', False),
    ('Q4 2025', '72',  '33',  '+3.15%', '+2.35%',  '+0.81%', True),
]

for i, (q, n, pred, mr, sr, alpha, beat) in enumerate(port_rows):
    y = PAGE_H - 2.7*inch - i * 0.85*inch
    bg = NAVY_CARD if i % 2 == 0 else LIGHT_NAV
    draw_rect(c, 0.4*inch, y - 0.6*inch, PAGE_W - 0.8*inch, 0.78*inch, bg)
    vals = [q, n, pred, mr, sr, alpha]
    colors_p = [WHITE_C, MUTED, BLUE, GOLD, WHITE_C, GREEN_C if beat else RED_C]
    for val, cx, col in zip(vals, cols_px, colors_p):
        text(c, val, cx, y - 0.2*inch, size=13, bold=True, color=col)
    beat_txt = 'YES' if beat else 'NO'
    text(c, beat_txt, cols_px[6], y - 0.2*inch, size=13, bold=True, color=GREEN_C if beat else RED_C)

draw_rect(c, 0.4*inch, 0.15*inch, PAGE_W - 0.8*inch, 1.05*inch, NAVY_CARD)
draw_rect(c, 0.4*inch, 1.2*inch, PAGE_W - 0.8*inch, 0.06*inch, GOLD)
text(c, 'Summary', 0.6*inch, 1.02*inch, size=11, bold=True, color=GOLD)
text(c, 'Q2 & Q3 2025: Model underperformed SPY by -4.2% and -1.1%. Q4 2025: Beat SPY by +0.8% (partial, 72 stocks).',
     0.6*inch, 0.72*inch, size=10)
text(c, 'Overall: model did not consistently beat passive S&P 500 investing — consistent with efficient market theory.',
     0.6*inch, 0.45*inch, size=10)
text(c, 'Q1 2025: SPY returned -4.6% (bear market quarter); Model returned -2.2% — less negative, but accuracy was 44.6%.',
     0.6*inch, 0.22*inch, size=9, color=MUTED)
c.showPage()

# ── SLIDE 22: CONCLUSION ───────────────────────────────────────────────────────
new_page(c)
header(c, 'Conclusion', 'Section 11 — Findings and Efficient Market Hypothesis Assessment')

findings = [
    ('Finding 1: Logistic Regression Finds Weak Signal', GOLD,
     ['Global model achieves 53.2% accuracy, AUC 0.5381 — statistically significant (p<0.05).',
      'Quarterly financial ratios contain predictive information; effect is real but modest.']),
    ('Finding 2: Segmentation Improves Performance', GREEN_C,
     ['Sector segmentation consistently outperforms global pooling.',
      'Comm. Services + Clustering: 63.9% accuracy, AUC 0.6902 — best of all 45 configurations.']),
    ('Finding 3: Non-Linear Signal Exists', BLUE,
     ['Gradient Boosting achieves AUC 0.6589 vs LR\'s 0.5381 globally.',
      'Non-linear patterns (interaction effects) exist that LR cannot capture.',
      'Future work: explore GB, Random Forest, and neural networks.']),
    ('Finding 4: Portfolio Does Not Beat SPY Consistently', RED_C,
     ['2025 portfolio underperformed in Q2 (-4.2%) and Q3 (-1.1%), beat narrowly in Q4 (+0.8%).',
      'Consistent with semi-strong form efficient market hypothesis.']),
]

for i, (title, color, lines) in enumerate(findings):
    col = i % 2
    row = i // 2
    x = 0.4*inch + col * 5.3*inch
    y = PAGE_H - 2.0*inch - row * 2.1*inch
    h = 1.85*inch
    draw_rect(c, x, y - h, 5.0*inch, h, NAVY_CARD)
    draw_rect(c, x, y - h, 0.06*inch, h, color)
    text(c, title, x + 0.18*inch, y - 0.25*inch, size=11, bold=True, color=color)
    draw_rect(c, x + 0.18*inch, y - 0.55*inch, 0.6*inch, 0.04*inch, color)
    line_y = y - 0.75*inch
    for line in lines:
        text(c, line, x + 0.18*inch, line_y, size=10)
        line_y -= 0.28*inch

draw_rect(c, 0.4*inch, 0.15*inch, PAGE_W - 0.8*inch, 0.7*inch, LIGHT_NAV)
draw_rect(c, 0.4*inch, 0.85*inch, PAGE_W - 0.8*inch, 0.08*inch, GOLD)
text(c, 'EMH Verdict: We PARTIALLY SUPPORT the efficient market hypothesis.',
     0.6*inch, 0.65*inch, size=12, bold=True, color=GOLD)
text(c, 'Markets are hard to beat with public data, but are not perfectly efficient — sector-specific patterns yield significant predictive power.',
     0.6*inch, 0.38*inch, size=10, color=WHITE_C)

c.showPage()

# ── SLIDE 23: THANK YOU ────────────────────────────────────────────────────────
new_page(c)
draw_rect(c, 0, 0, 4.8*inch, PAGE_H, NAVY_CARD)
draw_rect(c, 4.8*inch, 0, PAGE_W - 4.8*inch, PAGE_H, LIGHT_NAV)
draw_rect(c, 4.8*inch, 0, 0.06*inch, PAGE_H, GOLD)

text(c, 'Thank You', 0.5*inch, PAGE_H - 2.2*inch, size=52, bold=True)
draw_rect(c, 0.5*inch, PAGE_H - 3.0*inch, 2.0*inch, 0.06*inch, GOLD)
text(c, 'Questions welcome', 0.5*inch, PAGE_H - 3.4*inch, size=18, color=MUTED)

text(c, 'Lana Gidan', 0.5*inch, PAGE_H - 4.2*inch, size=13, bold=True)
text(c, 'Matthew Golubow', 0.5*inch, PAGE_H - 4.55*inch, size=13, bold=True)
text(c, 'Shahd Tarman', 0.5*inch, PAGE_H - 4.9*inch, size=13, bold=True)
text(c, 'SSIE 605  |  Binghamton University', 0.5*inch, PAGE_H - 5.5*inch, size=11, color=MUTED)

text(c, 'Key Statistics', 7.5*inch, PAGE_H - 1.4*inch, size=13, bold=True, color=GOLD, align='center')

key_stats = [
    ('Training Period', 'Q1 2010 – Q4 2024'),
    ('Training Rows', '16,589 complete observations'),
    ('Features', '24  (14 base + 10 delta)'),
    ('VIF Filtered', '20 of 24 retained (threshold 2.5)'),
    ('PCA Components', '9  (global model, >=5% each)'),
    ('Global LR AUC', '0.5381'),
    ('Global LR Accuracy', '53.2%'),
    ('Best Accuracy', '63.9% — Comm. Services Cluster 0'),
    ('Best AUC', '0.6902 — Comm. Services Cluster 0'),
    ('2025 Predictions', '1,219 stocks across 4 quarters'),
    ('Benchmark (2017)', 'Ananthakumar & Sarkar — 71.2%'),
]

row_h = 0.48*inch
for i, (label, val) in enumerate(key_stats):
    y = PAGE_H - 1.95*inch - i * row_h
    bg = NAVY_CARD if i % 2 == 0 else NAVY
    draw_rect(c, 5.1*inch, y - 0.34*inch, 5.5*inch, row_h - 0.04*inch, bg)
    text(c, label, 5.25*inch, y - 0.12*inch, size=9, color=MUTED)
    text(c, val, 7.4*inch, y - 0.12*inch, size=9, bold=True)

c.save()
print('PDF saved: SP500_Outperformer_Prediction.pdf')
import os
print(f'PDF size: {os.path.getsize("SP500_Outperformer_Prediction.pdf")/1024:.0f} KB')
print(f'PPTX size: {os.path.getsize("SP500_Outperformer_Prediction.pptx")/1024:.0f} KB')

import textwrap
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    HRFlowable, KeepTogether, Image as RLImage
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# ── Colours ───────────────────────────────────────────────────────────────────
BG_DARK  = colors.HexColor('#0d1b2a')
ACCENT   = colors.HexColor('#4fc3f7')
ORANGE   = colors.HexColor('#ffb74d')
GREEN    = colors.HexColor('#81c784')
WHITE    = colors.HexColor('#e8eaf6')
GRAY     = colors.HexColor('#607d8b')
CODE_BG  = colors.HexColor('#162032')

# ── Document setup ─────────────────────────────────────────────────────────────
OUTPUT = 'multivariate_homework_lana_gidan.pdf'
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2.2*cm, bottomMargin=2.2*cm,
    title='Multivariate Data Analysis — Homework',
    author='Lana Gidan',
)

W, H = A4
styles = getSampleStyleSheet()

# ── Custom paragraph styles ───────────────────────────────────────────────────
cover_title = ParagraphStyle(
    'CoverTitle',
    fontName='Helvetica-Bold',
    fontSize=22,
    textColor=ACCENT,
    alignment=TA_CENTER,
    spaceAfter=10,
    leading=28,
)
cover_sub = ParagraphStyle(
    'CoverSub',
    fontName='Helvetica',
    fontSize=13,
    textColor=WHITE,
    alignment=TA_CENTER,
    spaceAfter=6,
)
cover_name = ParagraphStyle(
    'CoverName',
    fontName='Helvetica-Bold',
    fontSize=16,
    textColor=ORANGE,
    alignment=TA_CENTER,
    spaceAfter=6,
)
section_heading = ParagraphStyle(
    'SectionHeading',
    fontName='Helvetica-Bold',
    fontSize=14,
    textColor=ACCENT,
    spaceBefore=18,
    spaceAfter=6,
)
sub_heading = ParagraphStyle(
    'SubHeading',
    fontName='Helvetica-Bold',
    fontSize=11,
    textColor=ORANGE,
    spaceBefore=10,
    spaceAfter=4,
)
body_style = ParagraphStyle(
    'Body',
    fontName='Helvetica',
    fontSize=9.5,
    textColor=colors.black,
    leading=14,
    spaceAfter=5,
    alignment=TA_JUSTIFY,
)
code_style = ParagraphStyle(
    'Code',
    fontName='Courier',
    fontSize=7.5,
    textColor=colors.HexColor('#c5cae9'),
    backColor=CODE_BG,
    leading=11,
    spaceAfter=0,
    spaceBefore=0,
    leftIndent=6,
    rightIndent=6,
)

def hr(color=ACCENT, thickness=1.2):
    return HRFlowable(width='100%', thickness=thickness, color=color, spaceAfter=6, spaceBefore=4)

def heading(text):
    return Paragraph(text, section_heading)

def subheading(text):
    return Paragraph(text, sub_heading)

def body(text):
    return Paragraph(text, body_style)

def code_block(filepath):
    """Read a Python file and return a list of Code paragraphs."""
    items = []
    with open(filepath, 'r') as f:
        raw = f.read()

    # Escape XML special chars
    raw = raw.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    lines = raw.split('\n')
    chunk = []
    for line in lines:
        # Wrap long lines
        if len(line) > 110:
            wrapped = textwrap.wrap(line, width=110, subsequent_indent='    ')
            chunk.extend(wrapped)
        else:
            chunk.append(line)

    CHUNK_SIZE = 60
    for i in range(0, len(chunk), CHUNK_SIZE):
        block = '\n'.join(chunk[i:i+CHUNK_SIZE])
        items.append(Paragraph(block.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style))
        items.append(Spacer(1, 2))
    return items

def embed_image(path, max_width=16*cm, max_height=14*cm):
    """Embed a PNG/JPG figure, scaled to fit."""
    from PIL import Image as PILImage
    img = PILImage.open(path)
    iw, ih = img.size
    scale = min(max_width / iw, max_height / ih)
    return RLImage(path, width=iw*scale, height=ih*scale)

# ── Build story ────────────────────────────────────────────────────────────────
story = []

# ── Cover page ─────────────────────────────────────────────────────────────────
story.append(Spacer(1, 3*cm))
story.append(Paragraph('Multivariate Data Analysis', cover_title))
story.append(Paragraph('Homework Solutions', cover_title))
story.append(Spacer(1, 1.2*cm))
story.append(hr())
story.append(Spacer(1, 0.8*cm))
story.append(Paragraph('Student', cover_sub))
story.append(Paragraph('Lana Gidan', cover_name))
story.append(Spacer(1, 1.5*cm))
story.append(hr(GRAY, 0.5))
story.append(Spacer(1, 0.6*cm))

questions_meta = [
    ('Q 8.7',  'Depression Discriminant Analysis',
     'Two-stage discriminant analysis on DEPRES.DAT using (a) INCOME & EDUCAT\n'
     'and (b) stepwise selection of 8 variables. Examines which socioeconomic\n'
     'and health variables best separate depressed from normal individuals.'),
    ('Q 7.5',  'Mass Transit Cluster Analysis',
     'Ward hierarchical clustering followed by K-Means refinement (k=2)\n'
     'on MASST.DAT (V7–V18) to identify latent mass-transit users vs non-users\n'
     'based on willingness to use transit at increasing gas price levels.'),
    ('Q 8.8',  'Mass Transit Discriminant Analysis',
     'Discriminant analysis on MASST.DAT using cluster membership from Q7.5\n'
     'as the dependent variable and V1–V18 as predictors. Validates and\n'
     'characterises the user / non-user distinction.'),
    ('Q 9.8',  'Phone Ownership Discriminant Analysis',
     'Three-group discriminant analysis on PHONE.DAT distinguishing\n'
     '1-phone, 2-phone, and 3+-phone households using six attitude statements\n'
     'about telephone ownership and cost.'),
    ('Q 9.9',  'Graduate Admissions Discriminant Analysis',
     'Three-group discriminant analysis on ADMIS.DAT separating Admitted,\n'
     'Not Admitted, and Borderline applicants using GPA and GMAT scores.\n'
     'Includes admission policy implications.'),
]

story.append(Paragraph('Contents', sub_heading))
story.append(Spacer(1, 0.3*cm))
for code, title, desc in questions_meta:
    story.append(Paragraph(f'<b><font color="#4fc3f7">{code}</font></b> — {title}', body_style))
story.append(PageBreak())

# ─────────────────────────────────────────────────────────────────────────────
# Q 8.7
# ─────────────────────────────────────────────────────────────────────────────
story.append(heading('Question 8.7 — Discriminant Analysis of Depression (DEPRES.DAT)'))
story.append(hr())
story.append(subheading('Overview'))
story.append(body(
    'This question performs a two-stage discriminant analysis on the depression dataset. '
    '<b>Part (a)</b> uses only INCOME and EDUCAT as predictors. '
    '<b>Part (b)</b> applies forward stepwise selection across eight variables (INCOME, EDUCAT, '
    'ACUTEILL, SEX, AGE, HEALTH, BEDDAYS, CHRONILL) to identify the most discriminating subset. '
    '<b>Part (c)</b> interprets the results.'
))
story.append(subheading('Key Results'))
story.append(body(
    '• Part (a): Wilks\' Λ = 0.9724 — moderate group separation with socioeconomic variables only.<br/>'
    '• Part (b): Wilks\' Λ = 0.8798 — significantly lower after adding health-related variables.<br/>'
    '• The stepwise model achieves a higher correct classification rate, confirming that health status '
    '(HEALTH, BEDDAYS, ACUTEILL, CHRONILL) is a stronger predictor of depression than income or education alone.<br/>'
    '• The discriminant function coefficient magnitudes show poor health, more bed-days, '
    'and presence of acute/chronic illness are the dominant separators.'
))
story.append(Spacer(1, 0.4*cm))
story.append(subheading('Figure'))
story.append(embed_image('q8_7_discriminant_analysis.png'))
story.append(PageBreak())

# ─────────────────────────────────────────────────────────────────────────────
# Q 7.5 + Q 8.8
# ─────────────────────────────────────────────────────────────────────────────
story.append(heading('Question 7.5 — Cluster Analysis on Mass Transit Data (MASST.DAT)'))
story.append(hr())
story.append(subheading('Overview'))
story.append(body(
    'Ward\'s hierarchical clustering followed by K-Means refinement (k = 2) is applied to variables '
    'V7–V18, which measure respondents\' willingness to use mass transit at increasing gas price levels '
    '(10% through >150% increase). The goal is to identify latent <b>Users</b> versus <b>Non-users</b>.'
))
story.append(subheading('Key Results'))
story.append(body(
    '• Two clear clusters emerge: Users (n ≈ 340) and Non-users (n ≈ 198).<br/>'
    '• Users maintain higher average usage scores across all price levels, '
    'indicating price-inelastic demand for mass transit.<br/>'
    '• Non-users show near-uniformly low scores, suggesting attitudinal rather than price-driven resistance.'
))
story.append(Spacer(1, 0.4*cm))
story.append(heading('Question 8.8 — Discriminant Analysis: Users vs Non-users (MASST.DAT)'))
story.append(hr())
story.append(subheading('Overview'))
story.append(body(
    'Using the cluster membership from Q7.5 as the dependent variable, a discriminant analysis is run '
    'with V1–V18 as predictors (V1–V6 = feature saliences; V7–V18 = price-sensitivity responses).'
))
story.append(subheading('Key Results'))
story.append(body(
    '• Wilks\' Λ = 0.1706 — very strong group separation.<br/>'
    '• Overall correct classification: 97.3%.<br/>'
    '• V7–V18 carry the largest discriminant weights by design. Among V1–V6, '
    'economy and dependability are the most differentiating feature saliences.<br/>'
    '• The result validates that the two clusters represent genuinely distinct attitudinal groups.'
))
story.append(Spacer(1, 0.4*cm))
story.append(subheading('Figure'))
story.append(embed_image('q7_5_q8_8_mass_transit.png'))
story.append(PageBreak())

# ─────────────────────────────────────────────────────────────────────────────
# Q 9.8
# ─────────────────────────────────────────────────────────────────────────────
story.append(heading('Question 9.8 — Three-Group Discriminant Analysis (PHONE.DAT)'))
story.append(hr())
story.append(subheading('Overview'))
story.append(body(
    'Three-group discriminant analysis on PHONE.DAT distinguishes households that own 1, 2, or 3+ '
    'telephones using six attitude statements (A1–A6) scored on a 0–10 scale.'
))
story.append(subheading('Key Results'))
story.append(body(
    '• Wilks\' Λ = 0.3246; χ²(12) = 275.07, p < 0.0001 — highly significant overall model.<br/>'
    '• Function 1 explains 94.9% of between-group variance — one dimension dominates.<br/>'
    '• Overall correct classification: 80%, well above the proportional chance level (≈ 36%).<br/>'
    '• A3 ("More phones worth extra cost") most strongly distinguishes 3+-phone owners. '
    'A5 ("More phones = waste of money") most strongly aligns with 1-phone households.<br/>'
    '• 1-phone families: cost-conscious and frugal. 3+-phone families: value quality and convenience. '
    '2-phone families occupy an intermediate position.'
))
story.append(Spacer(1, 0.4*cm))
story.append(subheading('Figure'))
story.append(embed_image('q9_8_phone_discriminant.png'))
story.append(PageBreak())

# ─────────────────────────────────────────────────────────────────────────────
# Q 9.9
# ─────────────────────────────────────────────────────────────────────────────
story.append(heading('Question 9.9 — Graduate Admissions Discriminant Analysis (ADMIS.DAT)'))
story.append(hr())
story.append(subheading('Overview'))
story.append(body(
    'Three-group discriminant analysis on ADMIS.DAT classifies 85 graduate applicants into '
    '<b>Admitted</b> (n=31), <b>Not Admitted</b> (n=28), and <b>Borderline</b> (n=26) using '
    'GPA and GMAT as predictors.'
))
story.append(subheading('Key Results'))
story.append(body(
    '• Wilks\' Λ = 0.1264; χ²(4) = 168.58, p < 0.0001 — extremely strong separation.<br/>'
    '• Function 1 explains 96.7% of between-group variance; GPA is the dominant predictor.<br/>'
    '• Overall correct classification: 91.8% vs. chance ≈ 33.5%.<br/>'
    '• Group profiles: Admitted (GPA ≈ 3.40, GMAT ≈ 561), Borderline (GPA ≈ 2.99, GMAT ≈ 446), '
    'Not Admitted (GPA ≈ 2.48, GMAT ≈ 447).'
))
story.append(subheading('Admission Policy Implications'))
story.append(body(
    '• The school is primarily <b>GPA-driven</b>; no rejected applicant had GPA ≥ 3.40.<br/>'
    '• Practical admission rule: GPA ≥ 3.30 AND GMAT ≥ 500 → Admit; '
    'GPA < 2.90 AND GMAT < 480 → Reject; otherwise Borderline (requires holistic review).<br/>'
    '• Borderline applicants share overlapping GPA and GMAT ranges with both other groups, '
    'suggesting the school uses additional criteria (recommendations, essays) for these cases.<br/>'
    '• Adding work experience or recommendation scores would likely improve the model\'s '
    'resolution of borderline cases.'
))
story.append(Spacer(1, 0.4*cm))
story.append(subheading('Figure'))
story.append(embed_image('q9_9_admissions_discriminant.png'))
story.append(PageBreak())

# ─────────────────────────────────────────────────────────────────────────────
# Full combined code listing
# ─────────────────────────────────────────────────────────────────────────────
story.append(heading('Complete Python Code — multivariate_homework_lana_gidan.py'))
story.append(hr())
story.append(body(
    'The following is the complete, self-contained Python script that reproduces all '
    'analyses and figures above. Run it from the project root directory with the '
    'data files in the attached_assets/ folder.'
))
story.append(Spacer(1, 0.3*cm))
story += code_block('multivariate_homework_lana_gidan.py')

# ── Build PDF ──────────────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    # Dark header bar
    canvas.setFillColor(BG_DARK)
    canvas.rect(0, H - 1.4*cm, W, 1.4*cm, fill=1, stroke=0)
    canvas.setFont('Helvetica-Bold', 8)
    canvas.setFillColor(ACCENT)
    canvas.drawString(2*cm, H - 0.9*cm, 'Multivariate Data Analysis — Lana Gidan')
    # Footer
    canvas.setFillColor(BG_DARK)
    canvas.rect(0, 0, W, 1.2*cm, fill=1, stroke=0)
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(GRAY)
    canvas.drawCentredString(W/2, 0.5*cm, f'Page {doc.page}')
    canvas.restoreState()

doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"PDF saved: {OUTPUT}")

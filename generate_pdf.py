import textwrap
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    HRFlowable, Image as RLImage
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

OUTPUT = 'multivariate_homework_lana_gidan.pdf'
W, H = A4

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=2.5*cm, rightMargin=2.5*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
    title='Multivariate Data Analysis Homework',
    author='Lana Gidan',
)

BLACK = colors.black
GRAY  = colors.HexColor('#555555')
LGRAY = colors.HexColor('#aaaaaa')
CODE_BG = colors.HexColor('#f4f4f4')

title_style = ParagraphStyle('Title',
    fontName='Times-Bold', fontSize=16,
    textColor=BLACK, alignment=TA_CENTER,
    spaceAfter=6, leading=22)

subtitle_style = ParagraphStyle('Subtitle',
    fontName='Times-Roman', fontSize=12,
    textColor=BLACK, alignment=TA_CENTER,
    spaceAfter=4)

author_style = ParagraphStyle('Author',
    fontName='Times-Bold', fontSize=13,
    textColor=BLACK, alignment=TA_CENTER,
    spaceAfter=4)

q_heading = ParagraphStyle('QHeading',
    fontName='Times-Bold', fontSize=13,
    textColor=BLACK, spaceBefore=14, spaceAfter=5)

part_heading = ParagraphStyle('PartHeading',
    fontName='Times-Bold', fontSize=11,
    textColor=BLACK, spaceBefore=8, spaceAfter=3)

body_style = ParagraphStyle('Body',
    fontName='Times-Roman', fontSize=10.5,
    textColor=BLACK, leading=15, spaceAfter=6,
    alignment=TA_JUSTIFY)

code_style = ParagraphStyle('Code',
    fontName='Courier', fontSize=7,
    textColor=BLACK, backColor=CODE_BG,
    leading=10, spaceAfter=0, spaceBefore=0,
    leftIndent=4, rightIndent=4)

fig_caption = ParagraphStyle('Caption',
    fontName='Times-Italic', fontSize=9,
    textColor=GRAY, alignment=TA_CENTER,
    spaceBefore=3, spaceAfter=8)

def thin_hr():
    return HRFlowable(width='100%', thickness=0.5,
                      color=LGRAY, spaceAfter=6, spaceBefore=4)

def embed_image(path, max_width=14*cm, max_height=13*cm):
    from PIL import Image as PILImage
    img = PILImage.open(path)
    iw, ih = img.size
    scale = min(max_width / iw, max_height / ih)
    return RLImage(path, width=iw*scale, height=ih*scale)

def code_block(filepath):
    items = []
    with open(filepath, 'r') as f:
        raw = f.read()
    raw = raw.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    lines = raw.split('\n')
    chunk = []
    for line in lines:
        if len(line) > 115:
            wrapped = textwrap.wrap(line, width=115, subsequent_indent='    ')
            chunk.extend(wrapped)
        else:
            chunk.append(line)
    CHUNK = 65
    for i in range(0, len(chunk), CHUNK):
        block = '\n'.join(chunk[i:i+CHUNK])
        items.append(Paragraph(
            block.replace('\n', '<br/>').replace(' ', '&nbsp;'),
            code_style))
        items.append(Spacer(1, 1))
    return items

story = []

# ── Cover ──────────────────────────────────────────────────────────────────────
story.append(Spacer(1, 4*cm))
story.append(Paragraph('Multivariate Data Analysis', title_style))
story.append(Paragraph('Homework Assignment', subtitle_style))
story.append(Spacer(1, 1.5*cm))
story.append(thin_hr())
story.append(Spacer(1, 0.8*cm))
story.append(Paragraph('Submitted by', subtitle_style))
story.append(Paragraph('Lana Gidan', author_style))
story.append(Spacer(1, 2*cm))
story.append(thin_hr())
story.append(PageBreak())

# ── Q 8.7 ─────────────────────────────────────────────────────────────────────
story.append(Paragraph('Question 8.7 — Discriminant Analysis (DEPRES.DAT)', q_heading))
story.append(thin_hr())

story.append(Paragraph(
    'Part (a): Discriminant analysis was performed using INCOME and EDUCAT as predictors '
    'to classify individuals as depressed (CESD > 16) or normal. '
    'The resulting Wilks\' Lambda was 0.9724, indicating modest but statistically significant '
    'group separation. Depressed individuals tended to have lower income and lower education '
    'compared to normal individuals.',
    body_style))

story.append(Paragraph(
    'Part (b): A forward stepwise procedure was applied across eight candidate variables '
    '(INCOME, EDUCAT, ACUTEILL, SEX, AGE, HEALTH, BEDDAYS, CHRONILL) using an F-to-enter '
    'threshold of 3.84. Health-related variables entered first and contributed the most '
    'to reducing Wilks\' Lambda, which fell to 0.8798 in the final stepwise model — a '
    'substantial improvement over part (a). The correct classification rate also increased '
    'considerably, confirming that health status variables are stronger predictors of '
    'depression than socioeconomic factors alone.',
    body_style))

story.append(Paragraph(
    'Part (c): The standardised discriminant function coefficients show that poor self-rated '
    'health (HEALTH), number of bed-days (BEDDAYS), acute illness (ACUTEILL), and chronic '
    'illness (CHRONILL) carry the largest weights, consistent with the well-established '
    'link between physical health and depression. INCOME and EDUCAT contribute secondary '
    'discriminating power. The stepwise model is both statistically and practically superior '
    'to the two-variable model.',
    body_style))

story.append(Spacer(1, 0.3*cm))
story.append(embed_image('q8_7_discriminant_analysis.png'))
story.append(Paragraph(
    'Figure 8.7 — Group means, discriminant score distributions, and model comparison '
    'for the depression discriminant analysis.',
    fig_caption))
story.append(PageBreak())

# ── Q 7.5 ─────────────────────────────────────────────────────────────────────
story.append(Paragraph('Question 7.5 — Cluster Analysis (MASST.DAT)', q_heading))
story.append(thin_hr())

story.append(Paragraph(
    'Variables V7 through V18 measure respondents\' stated willingness to use mass transit '
    'at gas price increases ranging from 10% to over 150%. Ward\'s hierarchical clustering '
    'was applied to the standardised data, and the resulting dendrogram and merge-distance '
    'profile both suggested a two-cluster solution. K-Means clustering (k = 2, 20 random '
    'starts) was then used to refine the partition.',
    body_style))

story.append(Paragraph(
    'The two clusters correspond naturally to Users (n = 340) and Non-users (n = 198) of '
    'mass transit. Users maintain consistently higher average usage-intention scores across '
    'all price levels, reflecting price-inelastic demand. Non-users show near-uniformly low '
    'scores regardless of gas price, suggesting an attitudinal barrier rather than a purely '
    'economic one. These groups form the dependent variable for Question 8.8.',
    body_style))

story.append(Spacer(1, 0.5*cm))

# ── Q 8.8 ─────────────────────────────────────────────────────────────────────
story.append(Paragraph('Question 8.8 — Discriminant Analysis: Users vs Non-users (MASST.DAT)', q_heading))
story.append(thin_hr())

story.append(Paragraph(
    'Using cluster membership from Question 7.5 as the dependent variable, a linear '
    'discriminant analysis was conducted with V1–V18 as predictors (V1–V6 capture feature '
    'saliences such as economy, convenience, and dependability; V7–V18 capture price-'
    'sensitivity responses). The analysis yielded Wilks\' Lambda = 0.1706 with an overall '
    'correct classification rate of 97.3%, confirming that the two clusters are highly '
    'distinct in multivariate space.',
    body_style))

story.append(Paragraph(
    'The price-sensitivity variables (V7–V18) carry the largest standardised discriminant '
    'weights, as expected given that the clusters were formed from these variables. Among '
    'the feature-salience variables (V1–V6), economy and dependability show the strongest '
    'differentiation between users and non-users, suggesting that potential transit users '
    'are especially sensitive to cost and reliability.',
    body_style))

story.append(Spacer(1, 0.3*cm))
story.append(embed_image('q7_5_q8_8_mass_transit.png'))
story.append(Paragraph(
    'Figure 7.5 / 8.8 — Dendrogram, K-Means elbow plot, cluster profiles, '
    'and discriminant analysis results for the mass transit data.',
    fig_caption))
story.append(PageBreak())

# ── Q 9.8 ─────────────────────────────────────────────────────────────────────
story.append(Paragraph('Question 9.8 — Three-Group Discriminant Analysis (PHONE.DAT)', q_heading))
story.append(thin_hr())

story.append(Paragraph(
    'A three-group discriminant analysis was performed on PHONE.DAT to distinguish '
    'households owning 1, 2, or 3+ telephones based on six attitude statements (A1–A6) '
    'scored on a 0–10 scale. The overall Wilks\' Lambda was 0.3246 (χ²(12) = 275.07, '
    'p < 0.0001), confirming highly significant multivariate group differences.',
    body_style))

story.append(Paragraph(
    'Two discriminant functions were extracted; Function 1 accounts for 94.9% of between-'
    'group variance and is therefore the dominant dimension. The overall correct '
    'classification rate was 80%, well above the proportional chance level of approximately '
    '36%.',
    body_style))

story.append(Paragraph(
    'The structure matrix shows that A3 ("More phones are worth the extra cost") is the '
    'strongest positive correlate of Function 1, distinguishing 3+-phone households. '
    'A5 ("More phones = waste of money") and A2 ("One phone saves money") are the '
    'strongest negative correlates, aligning with 1-phone households. A6 ("Best model '
    'is worth the cost") adds a secondary quality-seeking dimension. In summary, '
    '1-phone families are cost-conscious and frugal, 3+-phone families are value-'
    'oriented, and 2-phone families occupy an intermediate position.',
    body_style))

story.append(Spacer(1, 0.3*cm))
story.append(embed_image('q9_8_phone_discriminant.png'))
story.append(Paragraph(
    'Figure 9.8 — Group means, discriminant score scatter, structure matrix, '
    'and classification accuracy for the phone ownership analysis.',
    fig_caption))
story.append(PageBreak())

# ── Q 9.9 ─────────────────────────────────────────────────────────────────────
story.append(Paragraph('Question 9.9 — Graduate Admissions Discriminant Analysis (ADMIS.DAT)', q_heading))
story.append(thin_hr())

story.append(Paragraph(
    'Three-group discriminant analysis was applied to ADMIS.DAT to classify 85 graduate '
    'applicants into Admitted (n = 31), Not Admitted (n = 28), and Borderline (n = 26) '
    'categories using GPA and GMAT as predictors. The overall Wilks\' Lambda was 0.1264 '
    '(χ²(4) = 168.58, p < 0.0001), indicating extremely strong separation among the '
    'three groups.',
    body_style))

story.append(Paragraph(
    'Function 1 explains 96.7% of between-group variance. GPA carries a larger standardised '
    'coefficient than GMAT on Function 1, making it the primary separator. Together, GPA '
    'and GMAT form a composite academic merit dimension. The overall correct classification '
    'rate was 91.8% against a chance level of approximately 33.5%, with all three groups '
    'classified above 90%.',
    body_style))

story.append(Paragraph(
    'The group centroids on Function 1 fall at –2.77 (Admitted), +0.27 (Borderline), '
    'and +2.82 (Not Admitted), showing a clear ordering. Mean profiles are: Admitted '
    '(GPA ≈ 3.40, GMAT ≈ 561), Borderline (GPA ≈ 2.99, GMAT ≈ 446), Not Admitted '
    '(GPA ≈ 2.48, GMAT ≈ 447). The near-identical GMAT averages for Borderline and '
    'Not Admitted groups indicate that GPA is the decisive factor separating these two groups.',
    body_style))

story.append(Paragraph('Admission Policy Implications', part_heading))
story.append(Paragraph(
    'The analysis suggests the school operates with GPA as a near-mandatory threshold: '
    'no rejected applicant had a GPA at or above 3.40. A practical classification rule '
    'derived from the discriminant functions is: admit when GPA ≥ 3.30 and GMAT ≥ 500; '
    'reject when GPA < 2.90 and GMAT < 480; treat all remaining cases as borderline '
    'requiring holistic review. Since GPA and GMAT alone leave considerable overlap in '
    'the borderline range, incorporating additional variables such as work experience '
    'or letters of recommendation would likely resolve these ambiguous cases.',
    body_style))

story.append(Spacer(1, 0.3*cm))
story.append(embed_image('q9_9_admissions_discriminant.png'))
story.append(Paragraph(
    'Figure 9.9 — GPA vs GMAT scatter, discriminant score distributions, '
    'standardised coefficients, and classification accuracy for the admissions analysis.',
    fig_caption))
story.append(PageBreak())

# ── Code listing ───────────────────────────────────────────────────────────────
story.append(Paragraph('Python Code', q_heading))
story.append(thin_hr())
story.append(Paragraph(
    'The complete self-contained script below reproduces all analyses and figures. '
    'Data files should be placed in the attached_assets/ folder.',
    body_style))
story.append(Spacer(1, 0.2*cm))
story += code_block('multivariate_homework_lana_gidan.py')

# ── Page template ──────────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 8)
    canvas.setFillColor(GRAY)
    canvas.drawString(2.5*cm, 1.5*cm, 'Lana Gidan — Multivariate Data Analysis Homework')
    canvas.drawRightString(W - 2.5*cm, 1.5*cm, f'Page {doc.page}')
    canvas.restoreState()

doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f'PDF saved: {OUTPUT}')

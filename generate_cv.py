from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib import colors

doc = SimpleDocTemplate(
    'Lana_Gidan_CV.pdf',
    pagesize=letter,
    rightMargin=0.75*inch,
    leftMargin=0.75*inch,
    topMargin=0.6*inch,
    bottomMargin=0.6*inch
)

name_style = ParagraphStyle('name', fontName='Helvetica-Bold', fontSize=13,
    alignment=TA_CENTER, spaceAfter=2)
contact_style = ParagraphStyle('contact', fontName='Helvetica', fontSize=9,
    alignment=TA_CENTER, spaceAfter=2)
section_style = ParagraphStyle('section', fontName='Helvetica-Bold', fontSize=10,
    spaceBefore=10, spaceAfter=2, textColor=colors.black)
job_title_style = ParagraphStyle('jobtitle', fontName='Helvetica-Bold', fontSize=9.5,
    spaceBefore=5, spaceAfter=1)
date_right_style = ParagraphStyle('dateright', fontName='Helvetica', fontSize=9.5,
    alignment=TA_LEFT, spaceAfter=1)
body_style = ParagraphStyle('body', fontName='Helvetica', fontSize=9.5,
    spaceAfter=1, leading=13)
bullet_style = ParagraphStyle('bullet', fontName='Helvetica', fontSize=9.5,
    spaceAfter=2, leading=13, leftIndent=18, firstLineIndent=-10)
italic_style = ParagraphStyle('italic', fontName='Helvetica-Oblique', fontSize=9.5,
    spaceAfter=1, leading=13)

def hr():
    return HRFlowable(width="100%", thickness=0.8, color=colors.black, spaceAfter=4, spaceBefore=2)

def section(text):
    return [Paragraph(text.upper(), section_style), hr()]

def bullet(text):
    return Paragraph(f"\u2022  {text}", bullet_style)

def two_col(left, right):
    return Paragraph(
        f'<font name="Helvetica-Bold">{left}</font>'
        f'<font name="Helvetica" size="9.5"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</font>'
        f'<font name="Helvetica">{right}</font>',
        body_style
    )

story = []

story.append(Paragraph("Lana Gidan", name_style))
story.append(Paragraph("Binghamton, NY", contact_style))
story.append(Paragraph(
    "Phone: +16145127578 | Email: lgidan@binghamton.edu | "
    "<link href='http://www.linkedin.com/in/lanagidan'>www.linkedin.com/in/lanagidan</link> | "
    "<link href='https://binghamton.joinhandshake.com/profiles/lg9790'>https://binghamton.joinhandshake.com/profiles/lg9790</link>",
    contact_style))
story.append(Spacer(1, 6))

story += section("Education")

story.append(two_col("M.S., Industrial and Systems Engineering", "Aug 2025 – Present"))
story.append(Paragraph("GPA: 4.00/4.00", italic_style))
story.append(Paragraph("Binghamton University, State University of New York, Binghamton, NY", body_style))
story.append(Paragraph(
    "Relevant Coursework: Applied Probability and Statistics, Computational tools (LateX, Python, R, Net Logo)",
    body_style))
story.append(Spacer(1, 4))

story.append(two_col("B.S., Industrial Engineering", "Sep 2019 – June 2024"))
story.append(Paragraph("The University of Jordan – ABET Accredited, Amman, Jordan", body_style))
story.append(Paragraph(
    "Relevant Coursework: Applied Statistics, Data Mining (Logistics Regression, Statistical Data analysis and "
    "Techniques, Predictive Modeling), Discrete Event and Monte Carlo Simulation, Supply Chain And Logistics, "
    "Project Management, Stochastic And Deterministic Operations Research",
    body_style))

story += section("Professional Experience")

story.append(two_col("Design for Reliability and Lifecycle Engineering Internship", "Feb 2025 – Mar 2025"))
story.append(Paragraph("Owens Corning R&amp;D Center, Granville, OH, USA", body_style))
story.append(bullet("Conducted literature review on blade wear detection"))
story.append(bullet(
    "Utilized Isograph software to perform Monte Carlo simulations for maintenance strategy optimization, "
    "supporting cost reduction and reliability analysis."))
story.append(Spacer(1, 4))

story.append(two_col("ISO Quality Auditing and Risk Management Intern", "Oct 2023 – Dec 2023"))
story.append(Paragraph("Royal Scientific Society, Amman, Jordan", body_style))
story.append(bullet(
    "Assisted in the preparation of the annual ISO internal audit report, including documentation and "
    "reporting of non-conformities, using Excel, Power BI, and PowerPoint."))
story.append(bullet(
    "Performed risk analysis and SWOT assessment to identify organizational risks, weaknesses, and "
    "improvement areas in alignment with ISO quality requirements."))

story += section("Academic Projects")

story.append(two_col("Predicting S&amp;P 500 Stock Outperformers using Multivariate Data Analysis", "April 2026 – Present"))
story.append(bullet(
    "Predicted S&amp;P 500 stock outperformers using sector-specific logistic regression and 15 years of "
    "Compustat/CRSP data, with portfolio backtesting across multiple market regimes."))
story.append(Spacer(1, 4))

story.append(bullet(
    "Information-Theoretic Analysis of Children's Proximity Networks: Applied Shannon entropy, KL divergence, "
    "and mutual information to wearable-sensor data using Python to analyze social interaction diversity, "
    "similarity, and dyadic preferences."))
story.append(bullet(
    "Statistical Analysis of Quiz Score Distributions Across Different Forms: Applied Minitab and Excel for "
    "exploratory and inferential statistical analysis, including ANOVA, to evaluate quiz score distributions "
    "and performance differences across exam forms."))

story += section("Computer Skills")

story.append(Paragraph("<b>Programming Languages:</b> Python, RStudio", body_style))
story.append(Paragraph("<b>Tools &amp; Libraries:</b> Microsoft Visio, Pandas, Sci-kit Learn, Matplotlib", body_style))
story.append(Paragraph(
    "<b>Modeling &amp; Simulation:</b> Discrete Event Simulation Using Arena and Monte Carlo Simulation Using Microsoft Excel",
    body_style))
story.append(Paragraph("<b>General Applications:</b> MS Office", body_style))
story.append(Paragraph(
    "<b>Statistical Analysis &amp; Data Mining:</b> SPSS, Minitab",
    body_style))

doc.build(story)
print("Saved: Lana_Gidan_CV.pdf")

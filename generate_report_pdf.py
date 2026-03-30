from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, Image, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from PIL import Image as PILImage
import os

OUTPUT = "LendingClub_Analysis_Report.pdf"
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=letter,
    leftMargin=0.85*inch,
    rightMargin=0.85*inch,
    topMargin=0.9*inch,
    bottomMargin=0.9*inch,
)

# ── Colour palette ──────────────────────────────────────────────
NAVY   = colors.HexColor("#1B2A4A")
BLUE   = colors.HexColor("#2E6DA4")
LBLUE  = colors.HexColor("#D6E8F7")
GOLD   = colors.HexColor("#C8972B")
LGOLD  = colors.HexColor("#FEF3DC")
RED    = colors.HexColor("#B03A2E")
GREEN  = colors.HexColor("#1E7E34")
LGREY  = colors.HexColor("#F5F5F5")
DGREY  = colors.HexColor("#555555")
WHITE  = colors.white

# ── Styles ───────────────────────────────────────────────────────
base = getSampleStyleSheet()

def style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=base[parent])
    for k, v in kw.items():
        setattr(s, k, v)
    return s

S_COVER_TITLE = style("cover_title", fontSize=28, textColor=WHITE,
                      alignment=TA_CENTER, leading=34, spaceAfter=8,
                      fontName="Helvetica-Bold")
S_COVER_SUB   = style("cover_sub",   fontSize=14, textColor=LBLUE,
                      alignment=TA_CENTER, leading=18, spaceAfter=4,
                      fontName="Helvetica")
S_COVER_INFO  = style("cover_info",  fontSize=11, textColor=WHITE,
                      alignment=TA_CENTER, leading=16,
                      fontName="Helvetica")

S_PART        = style("part",   fontSize=18, textColor=WHITE,
                      fontName="Helvetica-Bold", alignment=TA_CENTER,
                      spaceAfter=4, leading=22)
S_H1          = style("h1",     fontSize=15, textColor=NAVY,
                      fontName="Helvetica-Bold", spaceBefore=18,
                      spaceAfter=6, leading=19)
S_H2          = style("h2",     fontSize=12, textColor=BLUE,
                      fontName="Helvetica-Bold", spaceBefore=12,
                      spaceAfter=4, leading=16)
S_BODY        = style("body",   fontSize=10, textColor=colors.black,
                      leading=15, spaceAfter=6, alignment=TA_JUSTIFY)
S_TERM        = style("term",   fontSize=10, textColor=NAVY,
                      fontName="Helvetica-Bold", leading=14,
                      spaceAfter=2)
S_DEF         = style("def_",   fontSize=10, textColor=DGREY,
                      leading=14, spaceAfter=8, leftIndent=12,
                      alignment=TA_JUSTIFY)
S_BULLET      = style("bullet", fontSize=10, textColor=colors.black,
                      leading=15, spaceAfter=3, leftIndent=16,
                      bulletIndent=4)
S_CALLOUT     = style("callout", fontSize=10, textColor=NAVY,
                      leading=15, spaceAfter=0, alignment=TA_JUSTIFY,
                      fontName="Helvetica-Oblique")
S_CAPTION     = style("caption", fontSize=8.5, textColor=DGREY,
                      alignment=TA_CENTER, leading=12, spaceAfter=4)
S_RESULT      = style("result", fontSize=11, textColor=GREEN,
                      fontName="Helvetica-Bold", alignment=TA_CENTER,
                      leading=16, spaceAfter=2)

# ── Helper builders ──────────────────────────────────────────────
def hr(color=BLUE, thickness=1, space=6):
    return HRFlowable(width="100%", thickness=thickness,
                      color=color, spaceAfter=space, spaceBefore=space)

def part_banner(text):
    data = [[Paragraph(text, S_PART)]]
    t = Table(data, colWidths=[6.3*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), NAVY),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("RIGHTPADDING",  (0,0), (-1,-1), 12),
        ("ROUNDEDCORNERS", [6]),
    ]))
    return t

def callout_box(text, bg=LGOLD, border=GOLD):
    data = [[Paragraph(text, S_CALLOUT)]]
    t = Table(data, colWidths=[6.3*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), bg),
        ("LINEAFTER",     (0,0), (0,-1), 4, border),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 14),
        ("RIGHTPADDING",  (0,0), (-1,-1), 10),
    ]))
    return t

def info_box(text, bg=LBLUE, border=BLUE):
    data = [[Paragraph(text, S_BODY)]]
    t = Table(data, colWidths=[6.3*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), bg),
        ("LINEAFTER",     (0,0), (0,-1), 4, border),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 14),
        ("RIGHTPADDING",  (0,0), (-1,-1), 10),
    ]))
    return t

def result_box(lines):
    rows = [[Paragraph(l, S_RESULT)] for l in lines]
    t = Table(rows, colWidths=[6.3*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), colors.HexColor("#EAF7EE")),
        ("LINEBEFORE",    (0,0), (0,-1), 4, GREEN),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 14),
    ]))
    return t

def term_def(term, definition):
    return [Paragraph(term, S_TERM), Paragraph(definition, S_DEF)]

def fancy_table(headers, rows, col_widths):
    data = [headers] + rows
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1,  0), NAVY),
        ("TEXTCOLOR",     (0, 0), (-1,  0), WHITE),
        ("FONTNAME",      (0, 0), (-1,  0), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1,  0), 9),
        ("ALIGN",         (0, 0), (-1, -1), "LEFT"),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("FONTSIZE",      (0, 1), (-1, -1), 9),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LGREY]),
        ("GRID",          (0, 0), (-1, -1), 0.4, colors.HexColor("#CCCCCC")),
        ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
    ]))
    return t

def add_image(path, width=5.5*inch, caption=None, max_height=7.5*inch):
    items = []
    if os.path.exists(path):
        pil = PILImage.open(path)
        w_px, h_px = pil.size
        height = width * h_px / w_px
        if height > max_height:
            height = max_height
            width = height * w_px / h_px
        img = Image(path, width=width, height=height)
        img.hAlign = "CENTER"
        items.append(Spacer(1, 6))
        items.append(img)
        if caption:
            items.append(Paragraph(caption, S_CAPTION))
    return items

def b(text):
    return f"<b>{text}</b>"

def bullet(text):
    return Paragraph(f"• {text}", S_BULLET)

# ═══════════════════════════════════════════════════════════════
# BUILD STORY
# ═══════════════════════════════════════════════════════════════
story = []
sp = lambda n=1: Spacer(1, n * 10)

# ── COVER PAGE ──────────────────────────────────────────────────
cover_data = [[
    Paragraph("Multivariate Statistical Analysis", S_COVER_TITLE),
    Paragraph("of Real-World Credit Risk Data", S_COVER_TITLE),
    Spacer(1, 16),
    Paragraph("LendingClub Loan Dataset  ·  500,000 Real Loan Records", S_COVER_SUB),
    Spacer(1, 24),
    Paragraph("Prepared for:", S_COVER_INFO),
    Paragraph("Lana Gidan  —  Binghamton University", S_COVER_INFO),
    Spacer(1, 8),
    Paragraph("Course: Multivariate Statistics", S_COVER_INFO),
    Spacer(1, 24),
    Paragraph("Techniques Applied:", S_COVER_INFO),
    Paragraph("Factor Analysis  ·  Linear Discriminant Analysis  ·  Logistic Regression", S_COVER_SUB),
]]
cover_table = Table(cover_data, colWidths=[6.3*inch])
cover_table.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), NAVY),
    ("TOPPADDING",    (0,0), (-1,-1), 40),
    ("BOTTOMPADDING", (0,0), (-1,-1), 40),
    ("LEFTPADDING",   (0,0), (-1,-1), 30),
    ("RIGHTPADDING",  (0,0), (-1,-1), 30),
    ("ALIGN",         (0,0), (-1,-1), "CENTER"),
]))
story.append(cover_table)
story.append(PageBreak())

# ── TABLE OF CONTENTS ───────────────────────────────────────────
story.append(Paragraph("Table of Contents", S_H1))
story.append(hr())
toc_items = [
    ("PART 1", "Context — What Is Credit Risk and Why Does It Matter?"),
    ("PART 2", "The Dataset — Real LendingClub Loan Data"),
    ("PART 3", "Step-by-Step: What We Did and Why"),
    ("PART 4", "Step 1 — Loading the Raw Data"),
    ("PART 5", "Step 2 — Cleaning the Data"),
    ("PART 6", "Step 3 — Exploring the Data"),
    ("PART 7", "Step 4 — Factor Analysis (Interdependence Technique)"),
    ("PART 8", "Step 5 — Preparing for Predictions"),
    ("PART 9", "Step 6 — Linear Discriminant Analysis"),
    ("PART 10","Step 7 — Logistic Regression"),
    ("PART 11","Results Summary & Key Limitation"),
    ("PART 12","Glossary of All Terms"),
]
for part, title in toc_items:
    story.append(Paragraph(f"<b>{part}</b>   {title}", S_BODY))
story.append(PageBreak())

# ────────────────────────────────────────────────────────────────
# PART 1 — CONTEXT
# ────────────────────────────────────────────────────────────────
story.append(part_banner("PART 1 — Context: What Is Credit Risk and Why Does It Matter?"))
story.append(sp(2))

story.append(Paragraph("What Is a Loan?", S_H1))
story.append(Paragraph(
    "A loan is when a bank or lending company gives you money today, and you promise to pay it "
    "back over time — usually with extra money on top called interest. For example, if you borrow "
    "$10,000 and the interest rate is 10%, you end up paying back more than $10,000 by the time "
    "the loan is done.", S_BODY))

story.append(Paragraph("What Is Credit Risk?", S_H1))
story.append(Paragraph(
    "Before a bank lends you money, they ask themselves one big question: <i>\"Will this person "
    "actually pay us back?\"</i> Credit risk is the risk that the borrower will NOT pay the money back. "
    "This is called a <b>default</b>.", S_BODY))
story.append(callout_box(
    "Real-world example: Imagine you lend your friend $100. There's a chance they forget, lose "
    "their job, or simply never pay you back. That's the 'risk' of lending. Banks face this at "
    "a massive scale — they lend billions of dollars, so even a small percentage of people not "
    "paying back is a huge financial problem."))
story.append(sp())

story.append(Paragraph("What Is LendingClub?", S_H1))
story.append(Paragraph(
    "LendingClub is a real American company — a peer-to-peer lending platform. Instead of going "
    "to a traditional bank, people can apply for loans through LendingClub's website. The company "
    "then matches borrowers (people who need money) with investors (people who have money and want "
    "to earn interest). Every loan application generates a detailed record — and that's exactly "
    "what our dataset is.", S_BODY))

story.append(Paragraph("What Is Multivariate Statistics?", S_H1))
story.append(Paragraph(
    "Regular statistics looks at one thing at a time — for example, does income affect loan "
    "default? Multivariate statistics looks at many things at the same time — income, credit "
    "score, debt level, loan size, number of accounts, and dozens more, all together. This is "
    "much more powerful because real-life decisions depend on many factors at once, not just one.", S_BODY))
story.append(PageBreak())

# ────────────────────────────────────────────────────────────────
# PART 2 — THE DATASET
# ────────────────────────────────────────────────────────────────
story.append(part_banner("PART 2 — The Dataset: Real LendingClub Loan Records"))
story.append(sp(2))

story.append(Paragraph("Where Did the Data Come From?", S_H1))
story.append(Paragraph(
    "The dataset comes from LendingClub's public records — real loan applications and their "
    "outcomes. This is actual financial data, not made up numbers. It was downloaded from "
    "Kaggle (a popular data science platform that hosts public datasets).", S_BODY))
story.append(Paragraph("What's in the Dataset?", S_H1))

raw_stats = [
    [b("500,000"), "Real loan records (rows)"],
    [b("151"),     "Pieces of information per loan (columns)"],
    [b("Real people"), "Actual US borrowers from LendingClub"],
]
t = Table(raw_stats, colWidths=[1.8*inch, 4.5*inch])
t.setStyle(TableStyle([
    ("FONTNAME",      (0,0), (0,-1), "Helvetica-Bold"),
    ("FONTSIZE",      (0,0), (-1,-1), 11),
    ("TEXTCOLOR",     (0,0), (0,-1), NAVY),
    ("TOPPADDING",    (0,0), (-1,-1), 7),
    ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ("LEFTPADDING",   (0,0), (-1,-1), 10),
    ("ROWBACKGROUNDS",(0,0),(-1,-1),[WHITE, LGREY]),
    ("GRID",          (0,0),(-1,-1), 0.4, colors.HexColor("#CCCCCC")),
]))
story.append(t)
story.append(sp())

story.append(Paragraph("What Kind of Information Did Each Row Contain?", S_H2))
story.append(Paragraph(
    "Each row represents one loan application. Here are some examples of the 151 columns:", S_BODY))
examples = [
    ("loan_amnt",         "How much money the borrower asked for (e.g., $15,000)"),
    ("int_rate",          "The interest rate on the loan (e.g., 13.5%)"),
    ("annual_inc",        "The borrower's yearly income (e.g., $60,000)"),
    ("fico_range_low",    "The borrower's credit score — a number from 300–850 that rates creditworthiness"),
    ("dti",               "Debt-to-Income ratio — how much of their income already goes to debts"),
    ("emp_length",        "How many years they've been employed"),
    ("grade",             "LendingClub's own letter grade for the loan (A = safest, G = riskiest)"),
    ("loan_status",       "The OUTCOME — did they pay it back or default?"),
    ("revol_util",        "Revolving credit utilization — what % of their credit cards are maxed out"),
    ("open_acc",          "Number of open credit accounts they have"),
]
story.append(fancy_table(
    [b("Column Name"), b("What It Means")],
    [[k, v] for k, v in examples],
    [1.8*inch, 4.5*inch]
))
story.append(PageBreak())

# ────────────────────────────────────────────────────────────────
# PART 3 — OVERVIEW OF WHAT WE DID
# ────────────────────────────────────────────────────────────────
story.append(part_banner("PART 3 — Overview: What We Did and Why"))
story.append(sp(2))

story.append(Paragraph("The Two Types of Techniques We Used", S_H1))
story.append(Paragraph(
    "This project required us to use two categories of multivariate statistical methods:", S_BODY))

two_types = [
    [b("Interdependence Technique"), b("Dependence Technique")],
    ["Does NOT have an outcome variable to predict.\nJust asks: how do these variables relate to each other?\nWhich ones cluster together?",
     "HAS an outcome variable (default = yes or no).\nAsks: which variables PREDICT that outcome?\nHow accurately can we classify borrowers?"],
    ["We used: Factor Analysis", "We used: LDA + Logistic Regression"],
]
t = Table(two_types, colWidths=[3.15*inch, 3.15*inch])
t.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0), NAVY),
    ("TEXTCOLOR",     (0,0), (-1,0), WHITE),
    ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",      (0,0), (-1,-1), 9),
    ("ALIGN",         (0,0), (-1,-1), "CENTER"),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",    (0,0), (-1,-1), 8),
    ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ("BACKGROUND",    (0,1), (0,-1), LBLUE),
    ("BACKGROUND",    (1,1), (1,-1), LGOLD),
    ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#AAAAAA")),
    ("FONTNAME",      (0,1), (-1,-1), "Helvetica"),
]))
story.append(t)
story.append(sp(2))

story.append(Paragraph("The 7-Step Process", S_H1))
steps = [
    ("Step 1", "Load the raw data",                  "Read the 500,000-row file into Python"),
    ("Step 2", "Clean the data",                     "Remove junk columns, fix messy formats, define 'default'"),
    ("Step 3", "Explore the data",                   "Look at basic statistics and correlations"),
    ("Step 4", "Factor Analysis",                    "Find hidden groupings among the financial variables"),
    ("Step 5", "Prepare for predictions",            "Scale the data and balance the classes"),
    ("Step 6", "Linear Discriminant Analysis (LDA)", "Find the line that best separates good vs. bad borrowers"),
    ("Step 7", "Logistic Regression",                "Estimate the probability of default for each borrower"),
]
story.append(fancy_table(
    [b("Step"), b("Name"), b("What It Does")],
    steps,
    [0.6*inch, 2.2*inch, 3.5*inch]
))
story.append(PageBreak())

# ────────────────────────────────────────────────────────────────
# PART 4 — STEP 1: LOADING
# ────────────────────────────────────────────────────────────────
story.append(part_banner("PART 4 — Step 1: Loading the Raw Data"))
story.append(sp(2))

story.append(Paragraph("What We Did", S_H1))
story.append(Paragraph(
    "We loaded the raw LendingClub CSV file into Python using a library called pandas — "
    "think of it like opening a giant spreadsheet inside a program. The raw file had:", S_BODY))
story.append(result_box(["500,000 rows  ·  151 columns"]))
story.append(sp())

story.append(callout_box(
    "Quick explanation: A CSV file (Comma-Separated Values) is like a plain-text spreadsheet. "
    "Each line is a row, and each piece of data is separated by commas. Python reads this and "
    "turns it into an in-memory table we can work with."))
story.append(PageBreak())

# ────────────────────────────────────────────────────────────────
# PART 5 — STEP 2: CLEANING
# ────────────────────────────────────────────────────────────────
story.append(part_banner("PART 5 — Step 2: Cleaning the Data"))
story.append(sp(2))

story.append(Paragraph("Why Do We Need to Clean Data?", S_H1))
story.append(Paragraph(
    "Real-world data is always messy. It has missing values, columns that don't mean anything "
    "useful, numbers stored as text, and extreme outliers that distort the analysis. Statistical "
    "methods assume the data is reasonably clean — garbage in, garbage out. Cleaning is often "
    "the most time-consuming part of any data science project.", S_BODY))
story.append(sp())

story.append(Paragraph("What We Did — Sub-Step by Sub-Step", S_H1))

story.append(Paragraph("Sub-Step 1: Dropped 58 Columns with Too Much Missing Data", S_H2))
story.append(Paragraph(
    "58 out of 151 columns were missing data in more than 40% of rows. Columns like "
    "'hardship_payoff_balance_amount' or 'settlement_date' only exist when something unusual "
    "happened to a loan. If 60% of rows have no value there, the column is useless for analysis "
    "and we removed it.", S_BODY))
story.append(callout_box(
    "Think of it this way: if you asked 100 people their middle name and 60 of them said 'I don't have one,' "
    "that question doesn't tell you much. Better to skip it."))
story.append(sp())

story.append(Paragraph("Sub-Step 2: Dropped 17 Irrelevant Columns", S_H2))
story.append(Paragraph(
    "Some columns have no statistical value — things like a unique ID number for each loan, "
    "a web URL for the loan listing, or free-text descriptions borrowers wrote. These don't "
    "carry patterns we can learn from, so they were removed.", S_BODY))
story.append(sp())

story.append(Paragraph("Sub-Step 3: Defined the Target Variable (Default = 0 or 1)", S_H2))
story.append(Paragraph(
    "The 'loan_status' column tells us what happened to each loan. We had to decide: "
    "which statuses mean the borrower defaulted, and which mean they were fine?", S_BODY))

status_table = [
    [b("Loan Status"),       b("What It Means"),                              b("We Coded It As")],
    ["Fully Paid",           "Borrower paid back everything",                  "0  (Good)"],
    ["Charged Off",          "Bank gave up collecting — total loss",           "1  (Default)"],
    ["Default",              "Stopped paying",                                 "1  (Default)"],
    ["Late (31–120 days)",   "More than a month behind on payments",           "1  (Default)"],
    ["Late (16–30 days)",    "Two weeks to a month behind",                    "1  (Default)"],
    ["Current",              "Still paying — outcome unknown",                 "Excluded"],
    ["In Grace Period",      "Just missed one payment — could go either way",  "Excluded"],
]
story.append(fancy_table(
    status_table[0], status_table[1:],
    [1.8*inch, 2.8*inch, 1.5*inch]
))
story.append(sp())
story.append(Paragraph(
    f"After this filtering: {b('394,712 rows remained')} — 79.1% good loans, 20.9% defaults.", S_BODY))
story.append(sp())

story.append(Paragraph("Sub-Step 4: Parsed Text Fields into Numbers", S_H2))
story.append(Paragraph(
    "Some columns were stored as text even though they represent numbers:", S_BODY))
parse_examples = [
    [b("Column"),       b("Raw Value (text)"),  b("Converted To")],
    ["int_rate",        '"13.56%"',             "13.56  (number)"],
    ["term",            '"36 months"',          "36  (number)"],
    ["emp_length",      '"10+ years"',          "10  (number)"],
    ["revol_util",      '"45.2%"',              "45.2  (number)"],
]
story.append(fancy_table(parse_examples[0], parse_examples[1:], [1.5*inch, 2.3*inch, 2.5*inch]))
story.append(sp())

story.append(Paragraph("Sub-Step 5: Label-Encoded Categorical Columns", S_H2))
story.append(Paragraph(
    "Statistical models need numbers, not words. So we converted text categories to numbers:", S_BODY))
story.append(bullet("grade: A→0, B→1, C→2, D→3, E→4, F→5, G→6"))
story.append(bullet("home_ownership: RENT→0, OWN→1, MORTGAGE→2, etc."))
story.append(bullet("purpose: debt_consolidation→0, credit_card→1, etc."))
story.append(sp())

story.append(Paragraph("Sub-Step 6: Removed Outliers", S_H2))
story.append(Paragraph(
    "An outlier is an extreme value that doesn't represent typical behavior. For example, "
    "one borrower might have reported an annual income of $9,000,000 — this would be real but "
    "so unusual that it distorts the whole analysis. We removed the top and bottom 1% of "
    "values for income, loan amount, and revolving balance.", S_BODY))
story.append(callout_box(
    "Think of it like this: if you're measuring the average height of students in a class "
    "and a professional basketball player walks in, their height would make the 'average' "
    "misleading. Removing extreme outliers gives us a more honest picture."))
story.append(sp())

story.append(Paragraph("Sub-Step 7: Dropped Remaining Missing Rows", S_H2))
story.append(Paragraph(
    "After all the above steps, any row that still had missing values was removed. "
    "This is called 'listwise deletion.'", S_BODY))

story.append(Paragraph("Final Clean Dataset:", S_H2))
story.append(result_box(["292,561 rows  ·  76 columns"]))
story.append(PageBreak())

# ────────────────────────────────────────────────────────────────
# PART 6 — STEP 3: EDA
# ────────────────────────────────────────────────────────────────
story.append(part_banner("PART 6 — Step 3: Exploring the Data"))
story.append(sp(2))

story.append(Paragraph("What Is Exploratory Data Analysis?", S_H1))
story.append(Paragraph(
    "Before we run any statistical technique, we look at the data to understand its structure. "
    "This is called Exploratory Data Analysis (EDA). Think of it like studying a map before "
    "starting a road trip — you want to know what you're working with.", S_BODY))

story.append(Paragraph("The Correlation Heatmap", S_H2))
story.append(Paragraph(
    "We created a grid (heatmap) showing how every pair of variables is related to each other. "
    "Each cell shows a correlation coefficient:", S_BODY))
story.append(bullet("Dark blue = strongly move TOGETHER (e.g., loan amount and installment — bigger loan → bigger monthly payment)"))
story.append(bullet("Dark red = move in OPPOSITE directions (e.g., FICO score and interest rate — better credit → lower rate)"))
story.append(bullet("White/light = no meaningful relationship"))
story.append(PageBreak())
story += add_image("results/correlation_heatmap.png", width=4.5*inch,
                   caption="Figure 1: Correlation heatmap of all 75 numeric variables. Dark colors indicate strong relationships.")
story.append(PageBreak())

# ────────────────────────────────────────────────────────────────
# PART 7 — STEP 4: FACTOR ANALYSIS
# ────────────────────────────────────────────────────────────────
story.append(part_banner("PART 7 — Step 4: Factor Analysis (Interdependence Technique)"))
story.append(sp(2))

story.append(Paragraph("What Is Factor Analysis?", S_H1))
story.append(Paragraph(
    "Imagine you have 20 questions about someone's finances. Many of those questions are "
    "measuring the SAME underlying thing — you just don't know it yet. Factor Analysis is a "
    "technique that finds these hidden underlying concepts (called factors or latent variables) "
    "that explain the patterns in your data.", S_BODY))
story.append(callout_box(
    "Real-life analogy: You can't directly measure someone's 'intelligence.' But you can see "
    "their test scores in math, reading, science, and logic. Factor Analysis would look at all "
    "those scores together and say: 'These all seem to be driven by one underlying factor — "
    "let's call it General Intelligence.' The factor is hidden; the test scores are what you observe."))
story.append(sp())

story.append(Paragraph("Why Did We Use It?", S_H2))
story.append(Paragraph(
    "We had 20 financial variables. Many of them overlap — for example, loan amount and monthly "
    "installment are obviously related. Factor Analysis helped us reduce these 20 variables into "
    "6 underlying financial concepts, making the data easier to understand and interpret.", S_BODY))

story.append(Paragraph("Pre-Check: Bartlett's Test of Sphericity", S_H1))
story.append(Paragraph(
    "Before running Factor Analysis, we must verify the data is actually suitable for it. "
    "Bartlett's Test checks whether the variables are correlated at all. If they're all "
    "completely independent, there are no hidden factors to find.", S_BODY))
story.append(info_box(
    "<b>Result:</b>   Chi-square = 657,867   |   p-value = 0.000   →   PASS ✓<br/>"
    "The variables ARE significantly correlated. Factor Analysis is appropriate."))
story.append(sp())

story.append(Paragraph("How Many Factors? — Eigenvalues and the Scree Plot", S_H1))
story.append(Paragraph(
    "An eigenvalue is a number that tells us how much of the total variance a factor captures. "
    "The standard rule (called the Kaiser criterion) is: keep any factor with an eigenvalue "
    "greater than 1. We found 6 such factors.", S_BODY))
story.append(callout_box(
    "Why eigenvalue > 1? A factor with eigenvalue = 1 explains exactly as much variance as "
    "one original variable. If a factor explains less than that, it's not worth keeping — "
    "we'd just be adding complexity without gaining insight."))
story += add_image("results/fa_scree_plot.png", width=5.2*inch,
                   caption="Figure 2: Scree plot showing eigenvalues. We retain factors above the dotted line (eigenvalue > 1).")

story.append(Paragraph("The 6 Factors We Found", S_H1))
story.append(Paragraph(
    "After running the analysis, here is what each factor represents. Each factor is defined "
    "by which variables load onto it most strongly (a 'loading' is just a correlation between "
    "a variable and the factor):", S_BODY))

factors_data = [
    [b("Factor"), b("Name We Gave It"), b("Variance Explained"), b("Key Variables (loadings)")],
    ["F1", "Loan Size & Cost",       "14.6%",
     "loan_amnt (+0.94), installment (+0.90), term (+0.47), int_rate (+0.47)"],
    ["F2", "Credit Risk Pricing",    "13.7%",
     "int_rate (+0.87), grade (+0.86), fico_range_low (−0.44), annual_inc (−0.38)"],
    ["F3", "Credit Utilization",     "10.0%",
     "revol_util (+0.90), bc_util (+0.84), fico_range_low (−0.38)"],
    ["F4", "Credit Breadth",         "9.4%",
     "open_acc (+0.75), total_acc (+0.69), revol_bal (+0.52), dti (+0.32)"],
    ["F5", "Credit Limit Stress",    "3.9%",
     "total_bc_limit (−0.50), revol_bal (−0.39), total_acc (+0.36)"],
    ["F6", "Wealth & Assets",        "4.8%",
     "mort_acc (+0.62), tot_cur_bal (+0.53), annual_inc (+0.33)"],
]
story.append(fancy_table(factors_data[0], factors_data[1:],
                         [0.4*inch, 1.5*inch, 1.2*inch, 3.2*inch]))
story.append(sp())

story.append(Paragraph("How to Read the Loadings (+ and −)", S_H2))
story.append(bullet("A + loading means: as the factor increases, the variable increases too"))
story.append(bullet("A − loading means: as the factor increases, the variable decreases"))
story.append(bullet("Example (F2 — Risk Pricing): higher int_rate (+0.87) AND higher grade (+0.86) go together WITH lower fico_range_low (−0.44). This makes perfect sense — riskier borrowers get higher interest rates, worse letter grades, and have lower credit scores."))
story.append(sp())

story.append(Paragraph("Factor Loadings Heatmap", S_H2))
story += add_image("results/fa_loadings_heatmap.png", width=5.2*inch,
                   caption="Figure 3: Factor loadings heatmap. Darker blue = stronger positive loading. Darker red = stronger negative loading.")

story.append(Paragraph("Summary of Factor Analysis Results", S_H2))
story.append(result_box([
    "6 Factors Extracted   |   56.5% of Total Variance Explained",
    "Bartlett's Test: Chi-square = 657,867   p = 0.000   PASS ✓",
]))
story.append(PageBreak())

# ────────────────────────────────────────────────────────────────
# PART 8 — STEP 5: PREPARE
# ────────────────────────────────────────────────────────────────
story.append(part_banner("PART 8 — Step 5: Preparing for the Predictive Techniques"))
story.append(sp(2))

story.append(Paragraph("Standardization (Z-Score Scaling)", S_H1))
story.append(Paragraph(
    "Before running LDA or Logistic Regression, all variables must be on the same scale. "
    "Otherwise, a variable measured in dollars (0–500,000) would completely overpower a "
    "variable measured in years (0–10) simply because its numbers are bigger.", S_BODY))
story.append(Paragraph(
    "We standardized every variable using Z-scores. This converts every variable to have "
    "mean = 0 and standard deviation = 1.", S_BODY))
story.append(callout_box(
    "Formula:  Z = (Value − Mean) ÷ Standard Deviation\n\n"
    "Example: If the average annual income is $60,000 with a standard deviation of $30,000, "
    "then someone earning $90,000 gets a Z-score of +1.0 — they are exactly 1 standard "
    "deviation above average. Someone earning $30,000 gets −1.0."))
story.append(sp())

story.append(Paragraph("Handling Class Imbalance", S_H1))
story.append(Paragraph(
    "Our data had 79.1% good loans and only 20.9% defaults. This is called a class imbalance. "
    "If we train a model on this unbalanced data, it could cheat: just predict 'good' for "
    "every single loan and be right 79% of the time — without learning anything useful.", S_BODY))
story.append(Paragraph(
    "To fix this, we balanced the training data using undersampling:", S_BODY))
story.append(bullet("Kept all 62,328 default loans"))
story.append(bullet("Randomly selected 124,656 good loans (2× the bad ones)"))
story.append(bullet("Final balanced training set: 186,984 rows at a 2:1 ratio"))
story.append(sp())

story.append(Paragraph("Train / Test Split", S_H1))
story.append(Paragraph(
    "We split the balanced data into two parts. The model only ever 'learns' from the training "
    "set. Then we test it on the held-out test set — data it has never seen. This tells us "
    "if the model has genuinely learned patterns, or if it just memorized the training data.", S_BODY))
story.append(info_box("70% Training (131,889 rows)   |   30% Testing (56,095 rows)"))
story.append(PageBreak())

# ────────────────────────────────────────────────────────────────
# PART 9 — LDA
# ────────────────────────────────────────────────────────────────
story.append(part_banner("PART 9 — Step 6: Linear Discriminant Analysis (LDA)"))
story.append(sp(2))

story.append(Paragraph("What Is LDA?", S_H1))
story.append(Paragraph(
    "Linear Discriminant Analysis (LDA) is a technique that finds the linear combination of "
    "variables that BEST SEPARATES two (or more) groups. In our case, the two groups are: "
    "Good borrowers (did not default) and Bad borrowers (defaulted).", S_BODY))
story.append(callout_box(
    "Intuition: Imagine you have a scatter plot of borrowers, with each dot representing one "
    "person plotted using many financial variables. Some dots are blue (good) and some are red "
    "(default). LDA finds the AXIS (a direction in that space) where — if you projected all "
    "dots onto that single line — the blue group and the red group would be as far apart as "
    "possible with as little overlap as possible."))
story.append(sp())

story.append(Paragraph("How It Works Mathematically", S_H2))
story.append(Paragraph(
    "LDA finds the linear discriminant function — a weighted combination of all your variables. "
    "Each variable gets a discriminant coefficient. Variables with larger coefficients are more "
    "important for separating the groups. The output is a single discriminant score for each "
    "person. If your score is above a threshold → classified as Good. Below → classified as Default.", S_BODY))

story.append(Paragraph("Assumptions of LDA", S_H2))
story.append(bullet("The data within each class is roughly normally distributed"))
story.append(bullet("Both classes have similar covariance structures (spread)"))
story.append(bullet("The boundary between classes is linear (a straight line, or plane in higher dimensions)"))
story.append(sp())

story.append(Paragraph("LDA Results", S_H1))
story.append(result_box([
    "Accuracy: 97.3%   |   AUC-ROC: 0.997",
    "Correctly classified 97 out of every 100 test loans",
]))
story.append(sp())

lda_report = [
    [b(""),          b("Precision"), b("Recall"), b("F1-Score"), b("Support")],
    ["Good (0)",     "0.97",        "0.99",      "0.98",        "37,397"],
    ["Default (1)",  "0.98",        "0.93",      "0.96",        "18,699"],
    ["Accuracy",     "",            "",          "0.97",        "56,096"],
]
story.append(fancy_table(lda_report[0], lda_report[1:], [1.5*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch]))
story.append(sp())

story.append(Paragraph("Key Terms in the Classification Report", S_H2))
for term, dfn in [
    ("Precision",   "Of all the loans the model flagged as Default, what % were actually defaults? High precision = few false alarms."),
    ("Recall",      "Of all the ACTUAL defaults, what % did the model catch? High recall = few missed defaults."),
    ("F1-Score",    "The harmonic mean of Precision and Recall — a balanced single number combining both."),
    ("Support",     "The number of loans in that category in the test set."),
]:
    story.extend(term_def(term, dfn))

story.append(Paragraph("The LDA Confusion Matrix", S_H2))
story += add_image("results/lda_confusion_matrix.png", width=4.2*inch,
                   caption="Figure 4: LDA Confusion Matrix. Diagonal cells are correct predictions.")

story.append(Paragraph("The LDA Projection Plot", S_H2))
story.append(Paragraph(
    "This chart shows how well LDA separates the two groups. It plots the distribution of "
    "discriminant scores for Good borrowers (blue) and Defaulters (red). The less they overlap, "
    "the better the separation.", S_BODY))
story += add_image("results/lda_projection.png", width=5.2*inch,
                   caption="Figure 5: LDA projection — good borrowers vs. defaulters on the discriminant axis.")

story.append(Paragraph("Top LDA Discriminant Coefficients", S_H2))
lda_coefs = [
    [b("Variable"),              b("Coefficient"), b("Meaning")],
    ["fico_range_low",          "+30.99",          "FICO score is the single most powerful separator"],
    ["fico_range_high",         "−30.72",          "Counterbalances fico_low (collinear variables)"],
    ["total_rec_prncp",         "−4.94",           "More principal recovered → less likely to default"],
    ["last_fico_range_high",    "−3.48",           "More recent credit score also matters"],
    ["total_pymnt",             "−3.20",           "More total payments → good sign"],
    ["installment",             "+2.11",           "Higher monthly payment → more burden → riskier"],
    ["debt_settlement_flag",    "+1.19",           "If they entered debt settlement → red flag"],
]
story.append(fancy_table(lda_coefs[0], lda_coefs[1:], [1.8*inch, 1.2*inch, 3.3*inch]))
story.append(PageBreak())

# ────────────────────────────────────────────────────────────────
# PART 10 — LOGISTIC REGRESSION
# ────────────────────────────────────────────────────────────────
story.append(part_banner("PART 10 — Step 7: Logistic Regression"))
story.append(sp(2))

story.append(Paragraph("What Is Logistic Regression?", S_H1))
story.append(Paragraph(
    "Logistic Regression predicts the PROBABILITY of a binary outcome. In our case, it "
    "estimates: 'What is the probability that this borrower will default?' The output is "
    "always between 0 and 1 (0% to 100%). If the predicted probability is above 0.5, we "
    "classify the borrower as likely to default.", S_BODY))
story.append(callout_box(
    "Example output: 'Borrower A has a 3% chance of defaulting → classify as Good. "
    "Borrower B has an 87% chance of defaulting → classify as Default.'"))
story.append(sp())

story.append(Paragraph("How Is It Different from LDA?", S_H2))
diff_data = [
    [b("LDA"),                         b("Logistic Regression")],
    ["Assumes normally distributed data within each class",
     "No distribution assumption — more flexible"],
    ["Finds a discriminant axis to separate groups",
     "Estimates probability using a sigmoid (S-shaped) curve"],
    ["Maximizes between-group separation",
     "Maximizes likelihood of observing the actual outcomes"],
    ["Works best when the normality assumption holds",
     "Works well even with non-normal, real-world data"],
]
t = Table(diff_data, colWidths=[3.15*inch, 3.15*inch])
t.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0), NAVY),
    ("TEXTCOLOR",     (0,0), (-1,0), WHITE),
    ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",      (0,0), (-1,-1), 9),
    ("ALIGN",         (0,0), (-1,-1), "LEFT"),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",    (0,0), (-1,-1), 7),
    ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, LGREY]),
    ("GRID",          (0,0),(-1,-1), 0.4, colors.HexColor("#AAAAAA")),
    ("FONTNAME",      (0,1),(-1,-1), "Helvetica"),
]))
story.append(t)
story.append(sp())

story.append(Paragraph("Logistic Regression Results", S_H1))
story.append(result_box([
    "Accuracy: 99.6%   |   AUC-ROC: 0.9997",
    "Correctly classified nearly 100% of test loans",
]))
story.append(sp())

lr_report = [
    [b(""),          b("Precision"), b("Recall"), b("F1-Score"), b("Support")],
    ["Good (0)",     "0.99",        "1.00",      "1.00",        "37,397"],
    ["Default (1)",  "1.00",        "0.99",      "0.99",        "18,699"],
    ["Accuracy",     "",            "",          "1.00",        "56,096"],
]
story.append(fancy_table(lr_report[0], lr_report[1:], [1.5*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch]))
story.append(sp())

story.append(Paragraph("Top Logistic Regression Coefficients", S_H2))
lr_coefs = [
    [b("Variable"),              b("Coefficient"), b("Effect")],
    ["total_rec_prncp",         "−8.18",           "More repaid principal → much lower default probability"],
    ["total_pymnt",             "−6.45",           "More payments made → lower default probability"],
    ["loan_amnt / funded_amnt", "+4.21",           "Larger loan → higher default probability"],
    ["installment",             "+3.98",           "Higher monthly payment → higher default probability"],
    ["recoveries",              "+3.13",           "Money recovered after default → obviously indicates default"],
    ["last_pymnt_amnt",         "−3.07",           "Larger last payment → good sign"],
    ["last_fico_range_high",    "−1.79",           "Better recent credit score → lower default probability"],
    ["debt_settlement_flag",    "+1.77",           "Entered debt settlement → strong default indicator"],
]
story.append(fancy_table(lr_coefs[0], lr_coefs[1:], [1.9*inch, 1.2*inch, 3.2*inch]))
story.append(sp())

story.append(Paragraph("The Logistic Regression Coefficient Chart", S_H2))
story += add_image("results/lr_coefficients.png", width=5.2*inch,
                   caption="Figure 6: Top 10 Logistic Regression coefficients. Blue = reduces default probability. Red = increases it.")

story.append(Paragraph("The ROC Curve Comparison", S_H1))
story.append(Paragraph(
    "The ROC (Receiver Operating Characteristic) curve plots how well each model performs "
    "at every possible decision threshold. The x-axis is the False Positive Rate (how often "
    "we wrongly flag a good loan as bad). The y-axis is the True Positive Rate (how often "
    "we correctly catch actual defaults).", S_BODY))
story.append(Paragraph(
    "A perfect model goes straight up to the top-left corner. AUC (Area Under the Curve) = 1.0 "
    "is perfect. AUC = 0.5 is random guessing (the diagonal line).", S_BODY))
story += add_image("results/roc_comparison.png", width=5.2*inch,
                   caption="Figure 7: ROC curve — LDA (blue) vs. Logistic Regression (orange). Both hug the top-left corner.")
story.append(PageBreak())

# ────────────────────────────────────────────────────────────────
# PART 11 — SUMMARY & LIMITATION
# ────────────────────────────────────────────────────────────────
story.append(part_banner("PART 11 — Results Summary & Important Limitation"))
story.append(sp(2))

story.append(Paragraph("Overall Results at a Glance", S_H1))
summary_data = [
    [b("Metric"),               b("Value")],
    ["Raw dataset size",        "500,000 rows × 151 columns"],
    ["Clean dataset size",      "292,561 rows × 76 columns"],
    ["Default rate in data",    "20.9%"],
    ["FA: factors extracted",   "6 factors"],
    ["FA: variance explained",  "56.5%"],
    ["LDA: accuracy",           "97.3%"],
    ["LDA: AUC-ROC",            "0.997"],
    ["LR: accuracy",            "99.6%"],
    ["LR: AUC-ROC",             "0.9997"],
]
t = Table(summary_data, colWidths=[3.0*inch, 3.3*inch])
t.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0), NAVY),
    ("TEXTCOLOR",     (0,0), (-1,0), WHITE),
    ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",      (0,0), (-1,-1), 10),
    ("ALIGN",         (0,0), (-1,-1), "LEFT"),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",    (0,0), (-1,-1), 7),
    ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ("LEFTPADDING",   (0,0), (-1,-1), 10),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, LGREY]),
    ("GRID",          (0,0),(-1,-1), 0.5, colors.HexColor("#CCCCCC")),
    ("FONTNAME",      (0,1),(-1,-1), "Helvetica"),
]))
story.append(t)
story.append(sp(2))

story.append(Paragraph("Output Files Generated", S_H1))
files_data = [
    [b("File"),                      b("What It Shows")],
    ["correlation_heatmap.png",      "Pairwise correlations between all 75 variables"],
    ["fa_scree_plot.png",            "Eigenvalues — how many factors to keep"],
    ["fa_loadings_heatmap.png",      "Which variables load onto which factors"],
    ["lda_confusion_matrix.png",     "LDA prediction accuracy table"],
    ["lda_projection.png",           "How well LDA separates the two groups"],
    ["lr_coefficients.png",          "Which variables matter most in Logistic Regression"],
    ["lr_confusion_matrix.png",      "Logistic Regression accuracy table"],
    ["roc_comparison.png",           "LDA vs. Logistic Regression performance comparison"],
]
story.append(fancy_table(files_data[0], files_data[1:], [2.4*inch, 3.9*inch]))
story.append(sp(2))

story.append(Paragraph("Important Limitation — Data Leakage", S_H1))
story.append(Paragraph(
    "The model accuracy numbers (97–99%) are unusually high. The reason is a problem called "
    "data leakage — some variables in the dataset reveal the outcome AFTER the fact:", S_BODY))

leakage_data = [
    [b("Leaky Variable"),       b("Why It's a Problem")],
    ["total_rec_prncp",         "Total principal recovered — only known after the loan ends"],
    ["total_pymnt",             "Total amount paid — only known after payments occur"],
    ["recoveries",              "Money recovered after default — only exists IF there was a default"],
    ["collection_recovery_fee", "Fee charged to recover defaulted funds — post-default only"],
    ["last_pymnt_amnt",         "Last payment amount — known only after payment history unfolds"],
    ["debt_settlement_flag",    "Flagged after a debt settlement was reached — post-default"],
]
story.append(fancy_table(leakage_data[0], leakage_data[1:], [2.0*inch, 4.3*inch]))
story.append(sp())

story.append(callout_box(
    "Think of it this way: Imagine you're trying to predict whether a student will fail a class "
    "before the semester ends — but one of your 'predictors' is their final exam score. Of course "
    "the model will be perfect — you're cheating by using the answer! These post-outcome variables "
    "essentially tell the model whether the loan defaulted before it even has to predict it."))
story.append(sp())

story.append(Paragraph("What This Means for Your Paper", S_H2))
story.append(Paragraph(
    "This is actually a great point to discuss in your report. It shows you understand the "
    "real-world difference between:", S_BODY))
story.append(bullet("Prediction at origination: Only use variables known when the loan is APPLIED FOR (income, FICO score, DTI, loan amount, grade). This is what banks actually do."))
story.append(bullet("Outcome analysis: Use all variables including what happened after — useful for understanding defaults in retrospect, but not for real-time prediction."))
story.append(Paragraph(
    "In a real credit scoring system, you would only use variables available at the time of "
    "application. Acknowledging this limitation demonstrates critical thinking and statistical "
    "maturity.", S_BODY))
story.append(PageBreak())

# ────────────────────────────────────────────────────────────────
# PART 12 — GLOSSARY
# ────────────────────────────────────────────────────────────────
story.append(part_banner("PART 12 — Glossary: Every Term Explained"))
story.append(sp(2))

glossary = [
    ("AUC-ROC",
     "Area Under the ROC Curve. Measures overall model quality on a 0–1 scale. "
     "1.0 = perfect. 0.5 = random guessing. Higher is better."),
    ("Bartlett's Test of Sphericity",
     "A statistical test that checks if the correlation matrix is significantly different "
     "from an identity matrix (no correlations). You need to pass this test before Factor "
     "Analysis makes sense. p < 0.05 means PASS."),
    ("Binary Target Variable",
     "An outcome with only two possible values — in our case, 0 (good loan) or 1 (default). "
     "Also called a dichotomous variable."),
    ("Chi-square statistic",
     "A number from Bartlett's Test. Larger chi-square = stronger evidence that the "
     "variables are correlated. Ours was 657,867 — extremely large, meaning very strong "
     "correlation structure."),
    ("Class Imbalance",
     "When one category in your outcome variable is much more common than the other. "
     "In our data, 79% good vs. 21% default is imbalanced. Models trained on imbalanced "
     "data tend to ignore the minority class."),
    ("Classification Report",
     "A table showing Precision, Recall, F1-Score, and Support for each class. "
     "It gives a complete picture of how a classification model performs."),
    ("Coefficient (Regression)",
     "A number that tells you how much — and in which direction — a variable affects the outcome. "
     "Positive = increases the outcome (e.g., larger loan → higher default probability). "
     "Negative = decreases it."),
    ("Confusion Matrix",
     "A 2×2 table showing: True Positives, True Negatives, False Positives, False Negatives. "
     "The diagonal (top-left and bottom-right) contains correct predictions."),
    ("Correlation",
     "A number between −1 and +1 measuring how strongly two variables move together. "
     "+1 = perfectly together, −1 = perfectly opposite, 0 = no relationship."),
    ("CSV (file format)",
     "Comma-Separated Values. A plain-text file format for storing spreadsheet-like data. "
     "Each row is a line; each column is separated by a comma."),
    ("Data Leakage",
     "When information that would not be available at prediction time 'leaks' into the model. "
     "This makes accuracy look artificially high. Classic example: using post-outcome "
     "variables to predict that very outcome."),
    ("Default",
     "When a borrower stops making loan payments and cannot or will not repay the debt. "
     "The bank may 'charge off' the loan — writing it off as a loss."),
    ("Dependence Technique",
     "A multivariate method that has a designated outcome (dependent) variable to predict. "
     "Examples: LDA, Logistic Regression. Asks 'what predicts Y?'"),
    ("Discriminant Coefficient",
     "In LDA, the weight assigned to each variable in the discriminant function. "
     "Variables with larger coefficients contribute more to separating the groups."),
    ("Discriminant Score",
     "A single number assigned to each observation by LDA. It summarizes all the variables "
     "into one number that best separates the two classes. Also called the discriminant function value."),
    ("DTI (Debt-to-Income Ratio)",
     "Total monthly debt payments ÷ monthly gross income. Example: $1,500 in debt payments "
     "on a $5,000 monthly income = DTI of 30%. Higher DTI = more financial strain."),
    ("Eigenvalue",
     "A number measuring how much variance a factor captures. Used to decide how many factors "
     "to retain. The standard rule: keep factors with eigenvalue > 1 (Kaiser criterion)."),
    ("Exploratory Data Analysis (EDA)",
     "The first step in any analysis — looking at the data broadly through summary statistics "
     "and visualizations before applying formal methods."),
    ("F1-Score",
     "The harmonic mean of Precision and Recall. Useful when you want a single number that "
     "balances both. F1 = 2 × (Precision × Recall) / (Precision + Recall)."),
    ("Factor",
     "A hidden (latent) variable that explains the pattern of correlations among observed variables. "
     "You can't measure it directly — it's inferred from the data."),
    ("Factor Analysis (FA)",
     "A multivariate technique that reduces many observed variables into a smaller number of "
     "underlying factors (latent constructs). Used when you don't have a specific outcome to predict."),
    ("Factor Loadings",
     "The correlations between each original variable and each factor. High loading (close to "
     "+1 or −1) means the variable is strongly associated with that factor."),
    ("False Negative",
     "A default that the model classified as Good (missed a real default). In banking, "
     "this is often the more dangerous error."),
    ("False Positive",
     "A good loan that the model classified as Default (false alarm). This costs the bank "
     "potential business by denying a creditworthy customer."),
    ("FICO Score",
     "A standardized credit score (300–850) used in the US to summarize creditworthiness. "
     "Higher = better. Most lenders want 670+. Below 580 is considered poor credit."),
    ("Grade (LendingClub)",
     "LendingClub's own letter rating from A (safest) to G (riskiest), assigned to each loan. "
     "It determines the interest rate the borrower is charged."),
    ("Heatmap",
     "A grid visualization where colors represent values — typically used to display "
     "correlation matrices. Darker colors = stronger relationships."),
    ("Interdependence Technique",
     "A multivariate method with no designated outcome variable. Just asks: how do these "
     "variables relate to each other? Example: Factor Analysis, Cluster Analysis."),
    ("Interest Rate (int_rate)",
     "The annual percentage charged on top of the loan amount. Example: 13.5% on a $10,000 "
     "loan means you pay $1,350 per year in interest charges."),
    ("Kaiser Criterion",
     "The rule of thumb: retain factors with eigenvalue > 1. Named after Henry Kaiser who "
     "proposed it in the 1960s."),
    ("Label Encoding",
     "Converting text categories to numbers so statistical methods can use them. "
     "Example: A=0, B=1, C=2, D=3."),
    ("Latent Variable",
     "A variable you cannot directly observe or measure — you infer it from observed data. "
     "Factors in Factor Analysis are latent variables."),
    ("LDA — Linear Discriminant Analysis",
     "A technique that finds a linear combination of variables maximally separating two or "
     "more groups. Outputs a discriminant score and a class prediction."),
    ("Logistic Regression",
     "A regression method for predicting binary outcomes. Uses the sigmoid function to output "
     "probabilities between 0 and 1."),
    ("Missing Values",
     "Cells in the dataset with no recorded value (blank or NaN). Most statistical techniques "
     "cannot handle them — you must either remove the row/column or impute a value."),
    ("Multivariate Statistics",
     "Statistical methods that analyze multiple variables simultaneously. More powerful than "
     "analyzing one variable at a time because it captures relationships among variables."),
    ("Outlier",
     "An extreme value that is much higher or lower than the rest of the data. Can distort "
     "statistical results. We removed the top and bottom 1% of certain variables."),
    ("Overfitting",
     "When a model learns the training data TOO well — including its noise — and fails to "
     "generalize to new data. This is why we always test on held-out data."),
    ("p-value",
     "The probability of seeing your result by random chance if there were no real effect. "
     "p < 0.05 means the result is statistically significant. p = 0.000 means extremely significant."),
    ("Precision",
     "Of all loans predicted as Default, what fraction were actually defaults? "
     "High precision = few false alarms."),
    ("Recall (Sensitivity)",
     "Of all actual defaults, what fraction did the model correctly identify? "
     "High recall = few missed defaults."),
    ("Revolving Credit Utilization (revol_util)",
     "What percentage of your revolving credit (like credit cards) you are currently using. "
     "Example: $4,500 balance on a $10,000 limit = 45% utilization. Higher = more financially stressed."),
    ("ROC Curve",
     "Receiver Operating Characteristic curve. Plots True Positive Rate vs. False Positive Rate "
     "at every threshold. The area under it (AUC) measures overall model quality."),
    ("Scree Plot",
     "A line chart of eigenvalues in descending order. You look for the 'elbow' where the "
     "curve flattens — factors before the elbow are worth keeping."),
    ("Sigmoid Function",
     "An S-shaped mathematical function that converts any number into a value between 0 and 1. "
     "Used in Logistic Regression to output probabilities."),
    ("Standardization (Z-score scaling)",
     "Transforming variables to have mean = 0 and standard deviation = 1. Ensures all "
     "variables contribute equally regardless of their original units."),
    ("Train/Test Split",
     "Dividing the dataset into a training portion (model learns from it) and a test portion "
     "(model is evaluated on data it has never seen). We used 70% train / 30% test."),
    ("Undersampling",
     "Reducing the majority class to balance a dataset. We randomly selected fewer good loans "
     "so the model sees a more balanced mix of good and default."),
    ("Variance Explained",
     "How much of the total variability in the data a factor accounts for. Expressed as a "
     "percentage. Higher = more important factor."),
]

for term, dfn in glossary:
    story.extend(term_def(term, dfn))

# ── BUILD PDF ────────────────────────────────────────────────────
doc.build(story)
print(f"PDF saved: {OUTPUT}")

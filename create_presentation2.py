import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

DARK_BLUE = RGBColor(0, 32, 96)
MEDIUM_BLUE = RGBColor(0, 70, 140)
LIGHT_BLUE = RGBColor(0, 112, 192)
ACCENT_GOLD = RGBColor(255, 192, 0)
WHITE = RGBColor(255, 255, 255)
BLACK = RGBColor(0, 0, 0)
DARK_GRAY = RGBColor(50, 50, 50)
LIGHT_GRAY = RGBColor(240, 240, 240)

os.makedirs("figures2", exist_ok=True)

def add_slide_background(slide, color=DARK_BLUE):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_title_bar(slide, title_text, subtitle_text=None):
    left = Inches(0)
    top = Inches(0)
    width = Inches(10)
    height = Inches(1.2)
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = DARK_BLUE
    shape.line.fill.background()
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.LEFT
    tf.margin_left = Inches(0.5)
    tf.margin_top = Inches(0.15)
    if subtitle_text:
        p2 = tf.add_paragraph()
        p2.text = subtitle_text
        p2.font.size = Pt(14)
        p2.font.color.rgb = ACCENT_GOLD
        p2.alignment = PP_ALIGN.LEFT

def add_content_box(slide, left, top, width, height, items, font_size=14, bullet=False):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    first = True
    for item in items:
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        if isinstance(item, tuple):
            text, size, bold, color = item
            p.text = text
            p.font.size = Pt(size)
            p.font.bold = bold
            p.font.color.rgb = color
        elif item == "":
            p.text = ""
            p.font.size = Pt(6)
        else:
            prefix = "\u2022 " if bullet else ""
            p.text = f"{prefix}{item}"
            p.font.size = Pt(font_size)
            p.font.color.rgb = DARK_GRAY

def add_table(slide, left, top, width, height, data, col_widths=None):
    rows = len(data)
    cols = len(data[0])
    table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table
    if col_widths:
        for i, w in enumerate(col_widths):
            table.columns[i].width = Inches(w)
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            cell = table.cell(i, j)
            cell.text = str(val)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            for paragraph in cell.text_frame.paragraphs:
                paragraph.font.size = Pt(11)
                paragraph.alignment = PP_ALIGN.CENTER
                if i == 0:
                    paragraph.font.bold = True
                    paragraph.font.color.rgb = WHITE
            if i == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = DARK_BLUE
            elif i % 2 == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(220, 230, 241)

print("Generating all visualizations...")

def create_research_framework():
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')

    dimensions = [
        ('Benefits &\nSalary', 1.5, 7.0),
        ("Management's\nAttitude", 1.5, 5.5),
        ('Supervision', 1.5, 4.0),
        ('Communication', 1.5, 2.5),
        ('Nature of\nWork', 1.5, 1.0),
        ("Colleagues'\nSupport", 4.5, 4.0),
    ]

    for name, x, y in dimensions:
        rect = plt.Rectangle((x-0.9, y-0.4), 1.8, 0.8,
                            facecolor='#004080', edgecolor='#002060',
                            linewidth=2, alpha=0.9, zorder=2)
        ax.add_patch(rect)
        ax.text(x, y, name, ha='center', va='center', fontsize=9,
               color='white', fontweight='bold', zorder=3)

    rect_target = plt.Rectangle((7.0, 3.6), 2.2, 0.9,
                               facecolor='#FFC000', edgecolor='#CC9900',
                               linewidth=3, alpha=0.95, zorder=2)
    ax.add_patch(rect_target)
    ax.text(8.1, 4.05, 'Job\nSatisfaction', ha='center', va='center', fontsize=13,
           color='#002060', fontweight='bold', zorder=3)

    for name, x, y in dimensions:
        ax.annotate('', xy=(7.0, 4.05), xytext=(x+0.9, y),
                   arrowprops=dict(arrowstyle='->', color='#004080',
                                 lw=2, connectionstyle='arc3,rad=0.1'))

    ax.text(5.0, 7.8, 'Hypothesized Model: Six Dimensions of Job Satisfaction',
           fontsize=12, ha='center', fontweight='bold', color='#002060')
    ax.text(5.0, 0.2, 'Based on Tsounis & Sarafis (2022), using Spector JSS framework',
           fontsize=8, ha='center', fontstyle='italic', color='gray')
    fig.suptitle('Research Framework: Employee Job Satisfaction',
                fontsize=14, fontweight='bold', color='#002060', y=0.98)
    plt.tight_layout()
    plt.savefig('figures2/research_framework.png', dpi=200, bbox_inches='tight')
    plt.close()

def create_cronbach_alpha():
    dimensions = ['Benefits &\nSalary', "Mgmt's\nAttitude", 'Supervision',
                  'Communication', 'Nature of\nWork', "Colleagues'\nSupport", 'Overall\nScale']
    alphas = [0.81, 0.72, 0.78, 0.67, 0.61, 0.70, 0.81]
    colors = ['#006600' if a >= 0.70 else '#CC6600' for a in alphas]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(dimensions, alphas, color=colors, alpha=0.85, edgecolor='#002060', width=0.6)
    ax.axhline(y=0.70, color='red', linestyle='--', linewidth=2, label='Threshold (α = 0.70)')
    ax.set_ylabel("Cronbach's Alpha (α)", fontsize=12, fontweight='bold')
    ax.set_title("Reliability Analysis: Cronbach's Alpha by Dimension\n(Tsounis & Sarafis, 2022)",
                fontsize=13, fontweight='bold', color='#004080')
    ax.set_ylim(0, 1.0)
    ax.legend(fontsize=10)
    ax.grid(True, axis='y', alpha=0.3)

    for bar, val in zip(bars, alphas):
        ax.text(bar.get_x() + bar.get_width()/2., val + 0.02,
               f'{val:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=10)

    plt.tight_layout()
    plt.savefig('figures2/cronbach_alpha.png', dpi=200, bbox_inches='tight')
    plt.close()

def create_model_fit():
    indices = ['SRMR', 'RMSEA', 'IFI', 'CFI']
    values = [0.050, 0.055, 0.906, 0.906]
    thresholds = [0.08, 0.06, 0.90, 0.90]
    status = ['Good', 'Good', 'Acceptable', 'Acceptable']
    colors = ['#006600', '#006600', '#006600', '#006600']

    fig, axes = plt.subplots(1, 4, figsize=(9, 3.5))
    for i, (idx, val, thresh, stat, col) in enumerate(zip(indices, values, thresholds, status, colors)):
        ax = axes[i]
        ax.barh([idx], [val], color=col, alpha=0.8, height=0.5, edgecolor='#002060')
        if idx in ['SRMR', 'RMSEA']:
            ax.axvline(x=thresh, color='red', linestyle='--', linewidth=2)
            ax.set_xlim(0, max(val, thresh) * 1.5)
        else:
            ax.axvline(x=thresh, color='red', linestyle='--', linewidth=2)
            ax.set_xlim(0, 1.1)
        ax.text(val + 0.005, 0, f'{val:.3f}', va='center', fontweight='bold', fontsize=11)
        ax.set_title(f'{idx}\n({stat})', fontsize=11, fontweight='bold', color='#004080')
        ax.tick_params(left=False, labelleft=False)

    fig.suptitle('CFA Model Fit Indices (Tsounis & Sarafis, 2022)',
                fontsize=13, fontweight='bold', color='#002060', y=1.02)
    plt.tight_layout()
    plt.savefig('figures2/model_fit.png', dpi=200, bbox_inches='tight')
    plt.close()

def create_scree_plot():
    eigenvalues = [8.2, 3.1, 2.4, 1.9, 1.5, 1.1, 0.85, 0.72, 0.58]
    factors = range(1, len(eigenvalues)+1)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(factors, eigenvalues, 'bo-', markersize=10, linewidth=2.5,
           markeredgecolor='#002060', markerfacecolor='#004080')
    ax.axhline(y=1.0, color='red', linestyle='--', linewidth=2, label='Kaiser Criterion (eigenvalue = 1)')
    ax.fill_between(factors[:6], eigenvalues[:6], alpha=0.15, color='#004080')

    for i, (f, e) in enumerate(zip(factors, eigenvalues)):
        offset = 0.25 if i < 6 else -0.25
        ax.text(f, e + offset, f'{e:.1f}', ha='center', fontweight='bold',
               fontsize=10, color='#002060')

    ax.set_xlabel('Factor Number', fontsize=12, fontweight='bold')
    ax.set_ylabel('Eigenvalue', fontsize=12, fontweight='bold')
    ax.set_title('Scree Plot: Eigenvalue by Factor (Illustrative)\nBased on 6-factor solution from Tsounis & Sarafis (2022)',
                fontsize=12, fontweight='bold', color='#004080')
    ax.set_xticks(list(factors))
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('figures2/scree_plot.png', dpi=200, bbox_inches='tight')
    plt.close()

def create_variance_explained():
    dimensions = ['Benefits &\nSalary', "Mgmt's\nAttitude", 'Supervision',
                  'Communication', 'Nature of\nWork', "Colleagues'\nSupport"]
    variance = [22.8, 8.6, 6.7, 5.3, 4.2, 3.1]
    cumulative = np.cumsum(variance)
    colors = ['#004080', '#0060A0', '#0070C0', '#3090D0', '#60B0E0', '#90C8E8']

    fig, ax1 = plt.subplots(figsize=(8, 4.5))

    bars = ax1.bar(dimensions, variance, color=colors, alpha=0.85, edgecolor='#002060', width=0.6)
    ax1.set_ylabel('% Variance Explained', fontsize=12, fontweight='bold', color='#004080')
    ax1.set_ylim(0, 30)

    ax2 = ax1.twinx()
    ax2.plot(dimensions, cumulative, 'ro-', markersize=8, linewidth=2.5,
            markeredgecolor='#CC0000', markerfacecolor='#FF3333')
    ax2.set_ylabel('Cumulative %', fontsize=12, fontweight='bold', color='#CC0000')
    ax2.set_ylim(0, 65)

    for bar, val in zip(bars, variance):
        ax1.text(bar.get_x() + bar.get_width()/2., val + 0.5,
                f'{val:.1f}%', ha='center', fontweight='bold', fontsize=9, color='#004080')

    for i, (d, c) in enumerate(zip(dimensions, cumulative)):
        ax2.text(i, c + 1.5, f'{c:.1f}%', ha='center', fontweight='bold',
                fontsize=9, color='#CC0000')

    ax1.set_title('Variance Explained by Each Factor (Illustrative)\nTotal: 50.7% cumulative variance',
                 fontsize=12, fontweight='bold', color='#004080')
    ax1.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('figures2/variance_explained.png', dpi=200, bbox_inches='tight')
    plt.close()

def create_jss_dimensions():
    dimensions = ['Pay', 'Promotion', 'Supervision', 'Benefits',
                  'Contingent\nRewards', 'Operating\nProcedures',
                  'Coworkers', 'Nature of\nWork', 'Communication']
    items = [4, 4, 4, 4, 4, 4, 4, 4, 4]
    alpha_ranges = [0.72, 0.72, 0.85, 0.71, 0.79, 0.60, 0.66, 0.83, 0.75]
    colors = ['#006600' if a >= 0.70 else '#CC6600' for a in alpha_ranges]

    fig, ax = plt.subplots(figsize=(9, 4.5))
    bars = ax.barh(dimensions, alpha_ranges, color=colors, alpha=0.85, edgecolor='#002060', height=0.6)
    ax.axvline(x=0.70, color='red', linestyle='--', linewidth=2, label='Threshold (α = 0.70)')

    for bar, val in zip(bars, alpha_ranges):
        ax.text(val + 0.01, bar.get_y() + bar.get_height()/2.,
               f'α = {val:.2f}', ha='left', va='center', fontweight='bold',
               fontsize=10, color='#002060')

    ax.set_xlabel("Cronbach's Alpha", fontsize=12, fontweight='bold')
    ax.set_title("Spector's JSS: 9 Dimensions Reliability (Typical Ranges)\n(Based on Spector, 1985; 36 items, 4 per dimension)",
                fontsize=11, fontweight='bold', color='#004080')
    ax.set_xlim(0, 1.05)
    ax.legend(fontsize=10)
    ax.grid(True, axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig('figures2/jss_dimensions.png', dpi=200, bbox_inches='tight')
    plt.close()

def create_satisfaction_factors():
    factors = ['Working\nConditions', 'Relations with\nSuperiors', 'Salary\nSatisfaction']
    means = [6.8, 5.9, 4.7]
    colors = ['#006600', '#004080', '#CC6600']

    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(factors, means, color=colors, alpha=0.85, edgecolor='#002060', width=0.5)

    for bar, val in zip(bars, means):
        ax.text(bar.get_x() + bar.get_width()/2., val + 0.15,
               f'{val:.1f}/10', ha='center', fontweight='bold', fontsize=13, color='#002060')

    ax.set_ylabel('Satisfaction Score (1-10 scale)', fontsize=12, fontweight='bold')
    ax.set_title('Employee Satisfaction Index: Three Key Factors\n(Dziuba et al., 2020)',
                fontsize=13, fontweight='bold', color='#004080')
    ax.set_ylim(0, 10)
    ax.axhline(y=5.0, color='gray', linestyle=':', linewidth=1, alpha=0.5)
    ax.text(2.5, 5.15, 'Neutral (5.0)', fontsize=9, color='gray', fontstyle='italic')
    ax.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('figures2/satisfaction_factors.png', dpi=200, bbox_inches='tight')
    plt.close()

def create_fa_procedure():
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')

    steps = [
        (1.5, 7.0, 'Step 1:\nDefine Variables', '#004080'),
        (5.0, 7.0, 'Step 2:\nCorrelation Matrix', '#004080'),
        (8.5, 7.0, 'Step 3:\nKMO & Bartlett Test', '#004080'),
        (1.5, 4.5, 'Step 4:\nFactor Extraction\n(PCA)', '#006600'),
        (5.0, 4.5, 'Step 5:\nRotation\n(Varimax)', '#006600'),
        (8.5, 4.5, 'Step 6:\nFactor Loadings', '#006600'),
        (3.25, 2.0, 'Step 7:\nReliability\n(Cronbach α)', '#CC6600'),
        (6.75, 2.0, 'Step 8:\nCFA Validation\n& Interpretation', '#CC6600'),
    ]

    for x, y, text, color in steps:
        rect = plt.Rectangle((x-1.2, y-0.6), 2.4, 1.2,
                            facecolor=color, edgecolor='#002060',
                            linewidth=2, alpha=0.9, zorder=2)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=9,
               color='white', fontweight='bold', zorder=3)

    arrows = [
        ((2.7, 7.0), (3.8, 7.0)),
        ((6.2, 7.0), (7.3, 7.0)),
        ((8.5, 6.4), (8.5, 5.7)),
        ((7.3, 4.5), (6.2, 4.5)),
        ((3.8, 4.5), (2.7, 4.5)),
        ((1.5, 3.9), (2.3, 2.6)),
        ((5.0, 3.9), (5.8, 2.6)),
    ]

    for start, end in arrows:
        ax.annotate('', xy=end, xytext=start,
                   arrowprops=dict(arrowstyle='->', color='#002060', lw=2))

    ax.text(5.0, 1.0, 'Applied to Employee Job Satisfaction (Tsounis & Sarafis, 2022)',
           fontsize=9, ha='center', fontstyle='italic', color='gray')

    fig.suptitle('Factor Analysis Procedure: Step-by-Step',
                fontsize=14, fontweight='bold', color='#002060', y=0.98)
    plt.tight_layout()
    plt.savefig('figures2/fa_procedure.png', dpi=200, bbox_inches='tight')
    plt.close()

create_research_framework()
create_cronbach_alpha()
create_model_fit()
create_scree_plot()
create_variance_explained()
create_jss_dimensions()
create_satisfaction_factors()
create_fa_procedure()

print("All visualizations created!\n")
print("Building PowerPoint presentation...")

prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)

slide = prs.slides.add_slide(prs.slide_layouts[6])
add_slide_background(slide, DARK_BLUE)

shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(1.5), Inches(9), Inches(4.5))
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(0, 40, 110)
shape.line.fill.background()
tf = shape.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Factor Analysis in Marketing Analytics"
p.font.size = Pt(36)
p.font.bold = True
p.font.color.rgb = WHITE
p.alignment = PP_ALIGN.CENTER
p2 = tf.add_paragraph()
p2.text = "Employee Job Satisfaction in Corporate Organizations"
p2.font.size = Pt(22)
p2.font.color.rgb = ACCENT_GOLD
p2.alignment = PP_ALIGN.CENTER

info_box = slide.shapes.add_textbox(Inches(1), Inches(3.5), Inches(8), Inches(3.5))
tf2 = info_box.text_frame
tf2.word_wrap = True
lines = [
    ("Presented by: Lana Jalal Gidan", 18, True, WHITE),
    ("Binghamton University", 16, False, RGBColor(180, 200, 255)),
    ("SSIE-605: Applied Multivariate Data Analysis", 14, False, ACCENT_GOLD),
    ("Professor Susan Lu", 14, False, RGBColor(180, 200, 255)),
]
for i, (text, size, bold, color) in enumerate(lines):
    if i == 0:
        p = tf2.paragraphs[0]
    else:
        p = tf2.add_paragraph()
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.alignment = PP_ALIGN.CENTER

slide = prs.slides.add_slide(prs.slide_layouts[6])
add_slide_background(slide, WHITE)
add_title_bar(slide, "Agenda")

agenda_items = [
    ("1.", "Problem Statement", "Why Study Job Satisfaction?"),
    ("2.", "Article Information", "Key Research Papers"),
    ("3.", "Factor Analysis Overview", "What is Factor Analysis?"),
    ("4.", "FA Procedure", "Step-by-Step Methodology"),
    ("5.", "Case Study", "Job Satisfaction in Healthcare"),
    ("6.", "Spector's JSS Framework", "9 Dimensions of Satisfaction"),
    ("7.", "EFA & CFA Results", "Statistical Findings"),
    ("8.", "Supporting Study", "Satisfaction & Work Performance"),
    ("9.", "Discussion & Implications", "Key Findings"),
    ("10.", "Comments, Limitations & Improvements", "Critical Analysis"),
    ("11.", "Conclusion & References", "Summary"),
]

for i, (num, title, desc) in enumerate(agenda_items):
    y_pos = 1.4 + i * 0.5
    left_box = slide.shapes.add_textbox(Inches(0.5), Inches(y_pos), Inches(0.5), Inches(0.45))
    tf = left_box.text_frame
    p = tf.paragraphs[0]
    p.text = num
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE

    mid_box = slide.shapes.add_textbox(Inches(1.0), Inches(y_pos), Inches(4.0), Inches(0.45))
    tf = mid_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = MEDIUM_BLUE

    right_box = slide.shapes.add_textbox(Inches(5.2), Inches(y_pos), Inches(4.5), Inches(0.45))
    tf = right_box.text_frame
    p = tf.paragraphs[0]
    p.text = desc
    p.font.size = Pt(13)
    p.font.color.rgb = DARK_GRAY

slide = prs.slides.add_slide(prs.slide_layouts[6])
add_slide_background(slide, WHITE)
add_title_bar(slide, "Problem Statement")

items = [
    ("Why Study Employee Job Satisfaction?", 18, True, DARK_BLUE),
    "",
    "Job satisfaction directly affects employee productivity, turnover, absenteeism, and organizational performance",
    "",
    "In large corporate organizations, understanding what drives employee satisfaction helps managers make better decisions about workplace policies",
    "",
    ("Key Questions:", 16, True, MEDIUM_BLUE),
    "What are the underlying dimensions of job satisfaction?",
    "Which factors matter most to employees?",
    "Can Factor Analysis reveal hidden patterns in satisfaction data?",
    "",
    ("Business Impact:", 16, True, RGBColor(0, 128, 0)),
    "Dissatisfied employees cost U.S. companies an estimated $450-$550 billion per year in lost productivity",
    "High turnover costs 50-200% of an employee's annual salary to replace",
    "Factor Analysis helps organizations target the right areas for improvement",
]
add_content_box(slide, Inches(0.5), Inches(1.4), Inches(9.0), Inches(5.5), items, font_size=14, bullet=True)

slide = prs.slides.add_slide(prs.slide_layouts[6])
add_slide_background(slide, WHITE)
add_title_bar(slide, "Article Information")

items = [
    ("Primary Study:", 16, True, DARK_BLUE),
    "",
    ('Tsounis, A. & Sarafis, P. (2022). "Determining Dimensions of Job Satisfaction in Healthcare Using Factor Analysis."', 12, False, DARK_GRAY),
    ("BMC Psychology, 10, Article 240.", 12, False, DARK_GRAY),
    ("DOI: 10.1186/s40359-022-00941-2", 11, True, LIGHT_BLUE),
    "",
    ("Method: EFA + CFA | Sample: 590 employees | Instrument: Spector JSS (36 items)", 11, False, RGBColor(0, 128, 0)),
    "",
    ("Supporting Study 1:", 16, True, DARK_BLUE),
    "",
    ('Spector, P.E. (1985). "Measurement of Human Service Staff Satisfaction: Development of the Job Satisfaction Survey."', 12, False, DARK_GRAY),
    ("American Journal of Community Psychology, 13, 693-713.", 12, False, DARK_GRAY),
    ("DOI: 10.1007/BF00929796", 11, True, LIGHT_BLUE),
    "",
    ("Supporting Study 2:", 16, True, DARK_BLUE),
    "",
    ('Dziuba, S.T. et al. (2020). "Employees\' Job Satisfaction and Their Work Performance as Elements Influencing Work Safety."', 12, False, DARK_GRAY),
    ("CzOTO, 2(1), 18-25.", 12, False, DARK_GRAY),
    ("DOI: 10.2478/czoto-2020-0003", 11, True, LIGHT_BLUE),
]
add_content_box(slide, Inches(0.3), Inches(1.4), Inches(9.4), Inches(5.8), items, font_size=12, bullet=False)

slide = prs.slides.add_slide(prs.slide_layouts[6])
add_slide_background(slide, WHITE)
add_title_bar(slide, "What is Factor Analysis?")

items = [
    ("Definition:", 16, True, DARK_BLUE),
    "Factor Analysis is a statistical method that reduces a large number of survey questions into a smaller number of meaningful groups (called factors or dimensions)",
    "",
    ("Simple Example:", 16, True, MEDIUM_BLUE),
    "Imagine a job satisfaction survey with 36 questions. Instead of analyzing all 36 individually, Factor Analysis groups them into a few key themes like 'Pay,' 'Supervision,' and 'Work Environment'",
    "",
    ("Two Main Types:", 16, True, RGBColor(0, 128, 0)),
    "",
    ("EFA (Exploratory):", 14, True, MEDIUM_BLUE),
    "Discovers which questions group together (explores the data)",
    "Used when you do not know the structure in advance",
    "",
    ("CFA (Confirmatory):", 14, True, MEDIUM_BLUE),
    "Tests whether a proposed grouping actually fits the data",
    "Used to validate a structure found through EFA",
    "",
    ("Job Satisfaction = f(Pay, Promotion, Supervision, Benefits, ...)", 12, True, RGBColor(0, 100, 0)),
]
add_content_box(slide, Inches(0.3), Inches(1.4), Inches(9.4), Inches(5.8), items, font_size=13, bullet=False)

slide = prs.slides.add_slide(prs.slide_layouts[6])
add_slide_background(slide, WHITE)
add_title_bar(slide, "FA Procedure: Step-by-Step")

slide.shapes.add_picture('figures2/fa_procedure.png', Inches(0.3), Inches(1.4), Inches(9.4), Inches(5.5))

slide = prs.slides.add_slide(prs.slide_layouts[6])
add_slide_background(slide, WHITE)
add_title_bar(slide, "EFA vs CFA: Key Differences")

table_data = [
    ['Aspect', 'EFA (Exploratory)', 'CFA (Confirmatory)'],
    ['Purpose', 'Discover factor structure', 'Validate known structure'],
    ['Hypothesis', 'No prior hypothesis', 'Tests specific hypothesis'],
    ['Factor Loadings', 'All items load on all factors', 'Items assigned to specific factors'],
    ['Output', 'Which items group together', 'Does the model fit the data?'],
    ['When to Use', 'New survey / unknown structure', 'Validating previous EFA results'],
    ['Fit Indices', 'KMO, Bartlett Test', 'CFI, RMSEA, SRMR, IFI'],
    ['In This Study', 'Found 6 dimensions', 'Confirmed 6-factor model'],
]
add_table(slide, Inches(0.3), Inches(1.5), Inches(9.4), Inches(5.0), table_data,
         col_widths=[1.8, 3.8, 3.8])

slide = prs.slides.add_slide(prs.slide_layouts[6])
add_slide_background(slide, WHITE)
add_title_bar(slide, "Case Study: Job Satisfaction in Large Organizations",
             "Tsounis & Sarafis (2022)")

items_left = [
    ("Study Context:", 16, True, DARK_BLUE),
    "Large organizational setting with multiple departments",
    "590 employees surveyed",
    "",
    ("Why This Matters for Corporate:", 14, True, MEDIUM_BLUE),
    "Large organizations face similar satisfaction challenges",
    "Same dimensions apply: pay, supervision, management, communication",
    "Results are generalizable to corporate settings",
    "",
    ("Survey Instrument:", 14, True, MEDIUM_BLUE),
    "Spector's Job Satisfaction Survey (JSS)",
    "36 items across 9 original dimensions",
    "6-point Likert scale (1 = strongly disagree to 6 = strongly agree)",
]
add_content_box(slide, Inches(0.3), Inches(1.4), Inches(5.0), Inches(5.5), items_left, font_size=13, bullet=False)

items_right = [
    ("Study Details:", 16, True, DARK_BLUE),
    "",
    ("Sample Size:", 13, True, MEDIUM_BLUE),
    "n = 590 employees",
    "",
    ("Response Rate:", 13, True, MEDIUM_BLUE),
    "High participation across departments",
    "",
    ("Analysis Methods:", 13, True, MEDIUM_BLUE),
    "Exploratory Factor Analysis (EFA)",
    "Confirmatory Factor Analysis (CFA)",
    "Cronbach's Alpha reliability testing",
    "Split-half reliability",
    "",
    ("Software:", 13, True, MEDIUM_BLUE),
    "SPSS for EFA",
    "AMOS for CFA",
]
add_content_box(slide, Inches(5.5), Inches(1.4), Inches(4.3), Inches(5.5), items_right, font_size=12, bullet=False)

slide = prs.slides.add_slide(prs.slide_layouts[6])
add_slide_background(slide, WHITE)
add_title_bar(slide, "Research Framework: Six Dimensions")

slide.shapes.add_picture('figures2/research_framework.png', Inches(0.3), Inches(1.4), Inches(5.2), Inches(5.0))

items = [
    ("Six Dimensions Extracted:", 15, True, DARK_BLUE),
    "",
    ("1. Benefits & Salary", 13, True, MEDIUM_BLUE),
    "Compensation, bonuses, fairness of pay",
    "",
    ("2. Management's Attitude", 13, True, MEDIUM_BLUE),
    "How management treats and values employees",
    "",
    ("3. Supervision", 13, True, MEDIUM_BLUE),
    "Quality and fairness of direct supervisors",
    "",
    ("4. Communication", 13, True, MEDIUM_BLUE),
    "Information flow within the organization",
    "",
    ("5. Nature of Work", 13, True, MEDIUM_BLUE),
    "The work itself: meaningful, interesting tasks",
    "",
    ("6. Colleagues' Support", 13, True, MEDIUM_BLUE),
    "Relationships with coworkers, teamwork",
]
add_content_box(slide, Inches(5.6), Inches(1.4), Inches(4.2), Inches(5.5), items, font_size=12, bullet=False)

slide = prs.slides.add_slide(prs.slide_layouts[6])
add_slide_background(slide, WHITE)
add_title_bar(slide, "Step 1: Sampling Adequacy Tests")

items = [
    ("Before running Factor Analysis, we must check if the data is suitable:", 14, False, DARK_GRAY),
    "",
    ("KMO Test (Kaiser-Meyer-Olkin):", 16, True, DARK_BLUE),
    "",
    ("KMO = 0.912 (Superb)", 20, True, RGBColor(0, 128, 0)),
    "",
    "KMO measures whether the correlations between variables are strong enough for Factor Analysis",
    "Values above 0.90 are considered 'superb' (Kaiser, 1974)",
    "This means the 36 survey items are highly suitable for factor analysis",
    "",
    ("Bartlett's Test of Sphericity:", 16, True, DARK_BLUE),
    "",
    ("Chi-square = 31,831.572, df = 528, p = 0.000", 14, True, RGBColor(0, 128, 0)),
    "",
    "Tests whether the correlation matrix is significantly different from an identity matrix",
    "p < 0.001 confirms that correlations exist between variables",
    "",
    ("Conclusion: Data is excellent for Factor Analysis", 14, True, RGBColor(0, 100, 0)),
]
add_content_box(slide, Inches(0.3), Inches(1.4), Inches(9.2), Inches(5.8), items, font_size=13, bullet=False)

slide = prs.slides.add_slide(prs.slide_layouts[6])
add_slide_background(slide, WHITE)
add_title_bar(slide, "Step 2: Factor Extraction - Scree Plot")

slide.shapes.add_picture('figures2/scree_plot.png', Inches(0.2), Inches(1.4), Inches(5.3), Inches(4.8))

items = [
    ("How Many Factors?", 15, True, DARK_BLUE),
    "",
    ("Kaiser Criterion:", 13, True, MEDIUM_BLUE),
    "Keep factors with eigenvalue > 1.0",
    "6 factors exceeded this threshold",
    "",
    ("Extraction Method:", 13, True, MEDIUM_BLUE),
    "Principal Component Analysis (PCA)",
    "Varimax rotation (orthogonal)",
    "",
    ("Factor Loading Threshold:", 13, True, MEDIUM_BLUE),
    "Items with loadings >= 0.50 retained",
    "",
    ("Result:", 13, True, RGBColor(0, 128, 0)),
    "6 clear factors emerged from the 36 items",
    "",
    ("Note: Eigenvalues are illustrative;", 9, False, DARK_GRAY),
    ("6-factor solution directly reported", 9, False, DARK_GRAY),
]
add_content_box(slide, Inches(5.6), Inches(1.4), Inches(4.2), Inches(5.5), items, font_size=12, bullet=False)

slide = prs.slides.add_slide(prs.slide_layouts[6])
add_slide_background(slide, WHITE)
add_title_bar(slide, "Step 3: Reliability Analysis (Cronbach's Alpha)")

slide.shapes.add_picture('figures2/cronbach_alpha.png', Inches(0.2), Inches(1.5), Inches(5.5), Inches(4.5))

items = [
    ("What is Cronbach's Alpha?", 14, True, DARK_BLUE),
    "Measures how consistently the survey items within each dimension measure the same thing",
    "",
    ("Interpretation:", 13, True, MEDIUM_BLUE),
    "α >= 0.70 = Acceptable reliability",
    "α >= 0.80 = Good reliability",
    "",
    ("Results:", 13, True, RGBColor(0, 128, 0)),
    "Overall scale: α = 0.81 (Good)",
    "Range: 0.61 to 0.81",
    "",
    ("5 of 6 dimensions meet", 12, True, MEDIUM_BLUE),
    ("the 0.70 threshold", 12, True, MEDIUM_BLUE),
    "",
    ("Source: Tsounis & Sarafis (2022)", 10, True, LIGHT_BLUE),
]
add_content_box(slide, Inches(5.8), Inches(1.5), Inches(4.0), Inches(5.0), items, font_size=11, bullet=False)

slide = prs.slides.add_slide(prs.slide_layouts[6])
add_slide_background(slide, WHITE)
add_title_bar(slide, "Step 4: CFA Model Fit Assessment")

slide.shapes.add_picture('figures2/model_fit.png', Inches(0.2), Inches(1.5), Inches(5.5), Inches(4.0))

items = [
    ("What are Fit Indices?", 14, True, DARK_BLUE),
    "They tell us how well the proposed 6-factor model fits the actual data",
    "",
    ("Results:", 13, True, RGBColor(0, 128, 0)),
    "",
    ("SRMR = 0.050", 13, True, MEDIUM_BLUE),
    "Good (threshold: < 0.08)",
    "",
    ("RMSEA = 0.055", 13, True, MEDIUM_BLUE),
    "Good (threshold: < 0.06)",
    "",
    ("IFI = 0.906", 13, True, MEDIUM_BLUE),
    "Acceptable (threshold: > 0.90)",
    "",
    ("CFI = 0.906", 13, True, MEDIUM_BLUE),
    "Acceptable (threshold: > 0.90)",
    "",
    ("Conclusion: The 6-factor model", 12, True, RGBColor(0, 100, 0)),
    ("fits the data well", 12, True, RGBColor(0, 100, 0)),
]
add_content_box(slide, Inches(5.8), Inches(1.5), Inches(4.0), Inches(5.5), items, font_size=11, bullet=False)

table_data = [
    ['Index', 'Value', 'Threshold', 'Result'],
    ['SRMR', '0.050', '< 0.08', 'Good'],
    ['RMSEA', '0.055', '< 0.06', 'Good'],
    ['IFI', '0.906', '> 0.90', 'Acceptable'],
    ['CFI', '0.906', '> 0.90', 'Acceptable'],
]
add_table(slide, Inches(0.3), Inches(5.6), Inches(5.3), Inches(1.5), table_data,
         col_widths=[1.3, 1.3, 1.3, 1.4])

slide = prs.slides.add_slide(prs.slide_layouts[6])
add_slide_background(slide, WHITE)
add_title_bar(slide, "Step 5: Variance Explained")

slide.shapes.add_picture('figures2/variance_explained.png', Inches(0.3), Inches(1.5), Inches(9.4), Inches(5.0))

note_box = slide.shapes.add_textbox(Inches(0.5), Inches(6.6), Inches(9.0), Inches(0.5))
tf = note_box.text_frame
p = tf.paragraphs[0]
p.text = "Illustrative variance distribution based on the 6-factor solution reported in Tsounis & Sarafis (2022). Factor 1 (Benefits & Salary) explains the most variance."
p.font.size = Pt(9)
p.font.color.rgb = DARK_GRAY
p.font.italic = True

slide = prs.slides.add_slide(prs.slide_layouts[6])
add_slide_background(slide, WHITE)
add_title_bar(slide, "Spector's JSS: The Original 9-Dimension Framework",
             "Spector (1985)")

slide.shapes.add_picture('figures2/jss_dimensions.png', Inches(0.2), Inches(1.5), Inches(5.5), Inches(4.8))

items = [
    ("The JSS Framework:", 15, True, DARK_BLUE),
    "",
    "36 items total (4 per dimension)",
    "6-point Likert scale",
    "Half items are reverse-scored",
    "",
    ("9 Original Dimensions:", 13, True, MEDIUM_BLUE),
    "Pay, Promotion, Supervision, Benefits,",
    "Contingent Rewards, Operating Procedures,",
    "Coworkers, Nature of Work, Communication",
    "",
    ("Tsounis & Sarafis (2022) found", 12, True, RGBColor(0, 128, 0)),
    ("6 dimensions (some merged)", 12, True, RGBColor(0, 128, 0)),
    "",
    ("Widely used: validated in 30+", 11, False, DARK_GRAY),
    ("languages across multiple cultures", 11, False, DARK_GRAY),
    ("Chart shows typical α ranges", 9, False, DARK_GRAY),
]
add_content_box(slide, Inches(5.8), Inches(1.5), Inches(4.0), Inches(5.2), items, font_size=11, bullet=False)

slide = prs.slides.add_slide(prs.slide_layouts[6])
add_slide_background(slide, WHITE)
add_title_bar(slide, "Supporting Study: Satisfaction & Work Performance",
             "Dziuba et al. (2020)")

slide.shapes.add_picture('figures2/satisfaction_factors.png', Inches(0.2), Inches(1.5), Inches(5.3), Inches(4.5))

items = [
    ("Study Overview:", 14, True, DARK_BLUE),
    "300 employees in a large corporate enterprise",
    "Survey with 20 satisfaction statements",
    "1-10 satisfaction scale",
    "",
    ("Three Key Factors:", 14, True, MEDIUM_BLUE),
    "",
    ("1. Working Conditions:", 13, True, RGBColor(0, 100, 0)),
    "Highest satisfaction (6.8/10)",
    "",
    ("2. Relations with Superiors:", 13, True, RGBColor(0, 64, 128)),
    "Moderate satisfaction (5.9/10)",
    "",
    ("3. Salary Satisfaction:", 13, True, RGBColor(200, 100, 0)),
    "Lowest satisfaction (4.7/10)",
    "",
    ("Key Finding:", 12, True, RGBColor(0, 128, 0)),
    "Satisfied employees perform better",
    "and feel safer at work",
    "",
    ("DOI: 10.2478/czoto-2020-0003", 10, True, LIGHT_BLUE),
]
add_content_box(slide, Inches(5.6), Inches(1.4), Inches(4.2), Inches(5.8), items, font_size=11, bullet=False)

slide = prs.slides.add_slide(prs.slide_layouts[6])
add_slide_background(slide, WHITE)
add_title_bar(slide, "Factor Interpretation & Business Implications")

items_left = [
    ("What Each Factor Means for Organizations:", 15, True, DARK_BLUE),
    "",
    ("Factor 1: Benefits & Salary", 14, True, RGBColor(0, 64, 128)),
    "Largest factor - explains the most variance",
    "Fair compensation is the foundation of satisfaction",
    "Organizations must ensure competitive pay structures",
    "",
    ("Factor 2: Management's Attitude", 14, True, RGBColor(0, 64, 128)),
    "How leadership treats employees matters greatly",
    "Respectful, supportive management boosts morale",
    "",
    ("Factor 3: Supervision", 14, True, RGBColor(0, 64, 128)),
    "Quality of direct supervisors impacts daily work experience",
    "Good supervisors provide guidance without micromanaging",
]
add_content_box(slide, Inches(0.3), Inches(1.4), Inches(4.8), Inches(5.5), items_left, font_size=12, bullet=False)

items_right = [
    ("", 6, False, DARK_GRAY),
    "",
    ("Factor 4: Communication", 14, True, RGBColor(0, 64, 128)),
    "Clear information flow reduces confusion",
    "Employees need to feel informed about decisions",
    "",
    ("Factor 5: Nature of Work", 14, True, RGBColor(0, 64, 128)),
    "Meaningful, interesting work increases engagement",
    "Task variety and autonomy are important",
    "",
    ("Factor 6: Colleagues' Support", 14, True, RGBColor(0, 64, 128)),
    "Positive coworker relationships create a supportive environment",
    "Teamwork and collaboration drive satisfaction",
    "",
    ("Actionable Insight:", 14, True, RGBColor(0, 128, 0)),
    "Organizations should invest in all 6 areas,",
    "but prioritize pay fairness and management quality",
]
add_content_box(slide, Inches(5.3), Inches(1.4), Inches(4.5), Inches(5.5), items_right, font_size=12, bullet=False)

slide = prs.slides.add_slide(prs.slide_layouts[6])
add_slide_background(slide, WHITE)
add_title_bar(slide, "Discussion & Key Findings")

items = [
    ("Finding 1: Job Satisfaction is Multidimensional", 15, True, RGBColor(0, 100, 0)),
    "It is not just about money. Six distinct dimensions emerged from the analysis, showing that satisfaction comes from multiple sources: pay, management, supervision, communication, work itself, and coworkers",
    "",
    ("Finding 2: Benefits & Salary is the Largest Factor", 15, True, RGBColor(0, 64, 128)),
    "Compensation remains the biggest driver of satisfaction. Organizations that underpay will struggle to satisfy employees regardless of other factors",
    "",
    ("Finding 3: The JSS Framework is Robust", 15, True, MEDIUM_BLUE),
    "Spector's 36-item JSS instrument, originally with 9 dimensions, showed a stable 6-factor structure in the studied population, with good reliability (overall α = 0.81) and model fit (CFI = 0.906)",
    "",
    ("Finding 4: Satisfaction Directly Affects Performance", 15, True, RGBColor(200, 100, 0)),
    "Dziuba et al. (2020) confirmed that satisfied employees perform better and feel safer at work. Salary satisfaction was the weakest area (4.7/10), suggesting room for improvement",
]
add_content_box(slide, Inches(0.3), Inches(1.4), Inches(9.2), Inches(5.8), items, font_size=13, bullet=False)

slide = prs.slides.add_slide(prs.slide_layouts[6])
add_slide_background(slide, WHITE)
add_title_bar(slide, "Comments")

items = [
    ("Strengths of This Analysis:", 16, True, DARK_BLUE),
    "",
    "Both EFA and CFA were used, providing a thorough validation of the factor structure",
    "",
    "Large sample size (n = 590) ensures statistical power and reliable factor estimates",
    "",
    "The KMO value of 0.912 is superb, indicating excellent suitability for factor analysis",
    "",
    "The JSS is a well-established, free instrument validated across 30+ countries",
    "",
    ("Observations:", 16, True, MEDIUM_BLUE),
    "",
    "The original 9-factor JSS consolidated into 6 factors, suggesting some dimensions overlap in this context",
    "",
    "Two dimensions (Nature of Work and Communication) showed lower reliability, which could be improved with revised items",
    "",
    "The Dziuba et al. (2020) study reinforces the practical importance of satisfaction research by linking it directly to employee performance and safety",
]
add_content_box(slide, Inches(0.3), Inches(1.4), Inches(9.2), Inches(5.8), items, font_size=13, bullet=False)

slide = prs.slides.add_slide(prs.slide_layouts[6])
add_slide_background(slide, WHITE)
add_title_bar(slide, "Limitations")

items = [
    ("Study-Specific Limitations:", 16, True, DARK_BLUE),
    "",
    "The primary study focused on healthcare organizations; results may differ in purely corporate settings",
    "",
    "Cross-sectional design: data collected at one point in time, so we cannot determine cause-and-effect relationships",
    "",
    "Self-reported data may contain social desirability bias (employees may not answer honestly)",
    "",
    "Two dimensions showed Cronbach's alpha below the 0.70 threshold (Nature of Work = 0.61, Communication = 0.67)",
    "",
    ("General Limitations:", 16, True, MEDIUM_BLUE),
    "",
    "Factor Analysis assumes linear relationships between variables",
    "Results are population-specific and may not generalize to all industries",
    "The JSS uses a fixed 36-item format that may miss industry-specific satisfaction factors",
]
add_content_box(slide, Inches(0.3), Inches(1.4), Inches(9.2), Inches(5.8), items, font_size=13, bullet=False)

slide = prs.slides.add_slide(prs.slide_layouts[6])
add_slide_background(slide, WHITE)
add_title_bar(slide, "Suggested Improvements")

items = [
    ("Methodological Improvements:", 16, True, DARK_BLUE),
    "Use probability sampling (stratified random) for better generalizability across departments",
    "Include multiple organizations to compare factor structures across different corporate settings",
    "Apply longitudinal design to track how satisfaction changes over time (before and after policy changes)",
    "Revise items with low factor loadings to improve the Nature of Work and Communication dimensions",
    "",
    ("Extended Scope:", 16, True, MEDIUM_BLUE),
    "Add modern work dimensions: remote work satisfaction, work-life balance, technology tools",
    "Include demographic analysis: compare satisfaction across age groups, departments, and tenure levels",
    "Add objective performance metrics alongside self-reported satisfaction for stronger conclusions",
    "Study the impact of post-pandemic hybrid work policies on satisfaction dimensions",
    "",
    ("Advanced Analytics:", 16, True, RGBColor(0, 128, 0)),
    "Apply Multi-Group Analysis (MGA) to compare satisfaction across different demographics",
    "Use Structural Equation Modeling (SEM) to test causal pathways between satisfaction and outcomes",
    "Incorporate text analysis from employee reviews for richer qualitative insights",
    "Test mediation effects: does supervision quality mediate the relationship between management attitude and overall satisfaction?",
]
add_content_box(slide, Inches(0.3), Inches(1.4), Inches(9.2), Inches(5.8), items, font_size=13, bullet=False)

slide = prs.slides.add_slide(prs.slide_layouts[6])
add_slide_background(slide, WHITE)
add_title_bar(slide, "Conclusion")

items = [
    ("Summary:", 18, True, DARK_BLUE),
    "",
    "Factor Analysis successfully identified six key dimensions of employee job satisfaction: Benefits & Salary, Management's Attitude, Supervision, Communication, Nature of Work, and Colleagues' Support",
    "",
    "The KMO value of 0.912 confirmed excellent data suitability, and the CFA model fit indices (SRMR = 0.050, RMSEA = 0.055, CFI = 0.906) validated the six-factor structure",
    "",
    "Benefits and salary emerged as the most important dimension, followed by management quality and supervision",
    "",
    "The findings apply directly to corporate organizations: understanding these dimensions helps managers create targeted improvement programs",
    "",
    ("Key Takeaway:", 16, True, RGBColor(0, 128, 0)),
    "Employee job satisfaction is not a single concept - it has multiple dimensions. Organizations that address all six areas will see better performance, lower turnover, and a healthier workplace",
]
add_content_box(slide, Inches(0.3), Inches(1.4), Inches(9.2), Inches(5.5), items, font_size=14, bullet=False)

slide = prs.slides.add_slide(prs.slide_layouts[6])
add_slide_background(slide, WHITE)
add_title_bar(slide, "References")

items = [
    ("Primary Sources:", 14, True, DARK_BLUE),
    "",
    '1. Tsounis, A. & Sarafis, P. (2022). "Determining Dimensions of Job Satisfaction in Healthcare Using Factor Analysis." BMC Psychology, 10, Article 240.',
    "   DOI: 10.1186/s40359-022-00941-2",
    "",
    '2. Spector, P.E. (1985). "Measurement of Human Service Staff Satisfaction: Development of the Job Satisfaction Survey." American Journal of Community Psychology, 13, 693-713.',
    "   DOI: 10.1007/BF00929796",
    "",
    '3. Dziuba, S.T., Ingaldi, M., & Zhuravskaya, M. (2020). "Employees\' Job Satisfaction and Their Work Performance as Elements Influencing Work Safety." CzOTO, 2(1), 18-25.',
    "   DOI: 10.2478/czoto-2020-0003",
    "",
    ("Additional References:", 14, True, DARK_BLUE),
    "",
    '4. Shrestha, N. (2021). "Factor Analysis as a Tool for Survey Analysis." American Journal of Applied Mathematics and Statistics, 9(1), 4-11.',
    "   DOI: 10.12691/ajams-9-1-2",
    "",
    '5. Kaiser, H.F. (1974). "An Index of Factorial Simplicity." Psychometrika, 39, 31-36.',
]
add_content_box(slide, Inches(0.3), Inches(1.4), Inches(9.4), Inches(5.8), items, font_size=11, bullet=False)

slide = prs.slides.add_slide(prs.slide_layouts[6])
add_slide_background(slide, DARK_BLUE)

shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1), Inches(2), Inches(8), Inches(3.5))
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(0, 40, 110)
shape.line.fill.background()
tf = shape.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Thank You!"
p.font.size = Pt(44)
p.font.bold = True
p.font.color.rgb = WHITE
p.alignment = PP_ALIGN.CENTER

p2 = tf.add_paragraph()
p2.text = ""
p2.font.size = Pt(10)

p3 = tf.add_paragraph()
p3.text = "Questions & Discussion"
p3.font.size = Pt(24)
p3.font.color.rgb = ACCENT_GOLD
p3.alignment = PP_ALIGN.CENTER

p4 = tf.add_paragraph()
p4.text = ""
p4.font.size = Pt(10)

p5 = tf.add_paragraph()
p5.text = "Lana Jalal Gidan"
p5.font.size = Pt(18)
p5.font.color.rgb = WHITE
p5.alignment = PP_ALIGN.CENTER

p6 = tf.add_paragraph()
p6.text = "SSIE-605 | Binghamton University | Professor Susan Lu"
p6.font.size = Pt(14)
p6.font.color.rgb = RGBColor(180, 200, 255)
p6.alignment = PP_ALIGN.CENTER

output_file = "Factor_Analysis_JobSatisfaction_Presentation.pptx"
prs.save(output_file)

slide_titles = []
for i, slide in enumerate(prs.slides, 1):
    title = ""
    for shape in slide.shapes:
        if shape.has_text_frame:
            title = shape.text_frame.paragraphs[0].text
            break
    slide_titles.append(f"  Slide {i}: {title[:60]}")

print(f"\n{'='*80}")
print(f"PRESENTATION SAVED: {output_file}")
print(f"Total Slides: {len(prs.slides)}")
print(f"{'='*80}")
print(f"\nSlide Summary:")
for t in slide_titles:
    print(t)

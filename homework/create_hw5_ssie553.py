from fpdf import FPDF
import os

FONT_REG  = '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
FONT_MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'

class PDF(FPDF):
    def header(self):
        self.set_font('DV', 'B', 10)
        self.set_text_color(0, 51, 102)
        self.cell(0, 7, 'SSIE 553 \u2013 Homework 5  |  Lana Jalal Gidan  |  Spring 2026', align='C', new_x='LMARGIN', new_y='NEXT')
        self.set_draw_color(0, 51, 102)
        self.set_line_width(0.4)
        self.line(15, self.get_y(), 195, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-13)
        self.set_font('DV', '', 9)
        self.set_text_color(130, 130, 130)
        self.cell(0, 6, f'Page {self.page_no()}', align='C')

    def section_title(self, txt):
        self.set_font('DV', 'B', 12)
        self.set_fill_color(0, 51, 102)
        self.set_text_color(255, 255, 255)
        self.cell(0, 9, txt, fill=True, new_x='LMARGIN', new_y='NEXT')
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def sub_title(self, txt):
        self.set_x(self.l_margin)
        self.set_font('DV', 'B', 11)
        self.set_text_color(0, 70, 150)
        self.multi_cell(0, 7, txt)
        self.set_x(self.l_margin)
        self.set_text_color(0, 0, 0)
        self.ln(1)

    def body(self, txt):
        self.set_x(self.l_margin)
        self.set_font('DV', '', 10.5)
        self.multi_cell(0, 6.5, txt)
        self.ln(1)

    def step(self, label, txt):
        self.set_x(self.l_margin)
        self.set_font('DV', 'B', 10.5)
        self.set_text_color(140, 0, 0)
        self.multi_cell(0, 6.5, label)
        self.set_x(self.l_margin)
        self.set_text_color(0, 0, 0)
        self.set_font('DV', '', 10.5)
        self.multi_cell(0, 6.5, txt)
        self.ln(1)

    def box_text(self, txt):
        self.set_x(self.l_margin)
        self.set_fill_color(238, 244, 255)
        self.set_draw_color(80, 100, 190)
        self.set_line_width(0.4)
        self.set_font('DV', '', 10.5)
        self.multi_cell(0, 6.5, txt, border=1, fill=True)
        self.set_line_width(0.2)
        self.set_draw_color(0, 0, 0)
        self.ln(2)

    def result_box(self, txt):
        self.set_x(self.l_margin)
        self.set_fill_color(218, 238, 218)
        self.set_draw_color(0, 110, 0)
        self.set_line_width(0.5)
        self.set_font('DV', 'B', 10.5)
        self.multi_cell(0, 7, txt, border=1, fill=True)
        self.set_line_width(0.2)
        self.set_draw_color(0, 0, 0)
        self.ln(2)

pdf = PDF()
pdf.add_font('DV',  '',  FONT_REG)
pdf.add_font('DV',  'B', FONT_BOLD)
pdf.add_font('DVm', '',  FONT_MONO)
pdf.set_margins(15, 20, 15)
pdf.set_auto_page_break(auto=True, margin=18)

# ===============================================================
# TITLE PAGE
# ===============================================================
pdf.add_page()
pdf.set_font('DV', 'B', 20)
pdf.set_text_color(0, 51, 102)
pdf.ln(18)
pdf.cell(0, 12, 'SSIE 553 \u2013 Homework 5', align='C', new_x='LMARGIN', new_y='NEXT')
pdf.set_font('DV', 'B', 14)
pdf.set_text_color(0, 80, 160)
pdf.cell(0, 10, 'Linear Programming Duality', align='C', new_x='LMARGIN', new_y='NEXT')
pdf.ln(8)
pdf.set_font('DV', '', 12)
pdf.set_text_color(0, 0, 0)
info = [
    ('Student:',     'Lana Jalal Gidan'),
    ('Course:',      'SSIE 553 \u2013 Operations Research'),
    ('Professor:',   'Neha Patankar'),
    ('Institution:', 'Binghamton University, Watson College'),
    ('Due Date:',    'March 23, 2026'),
]
for label, val in info:
    pdf.set_font('DV', 'B', 12)
    pdf.cell(42, 9, label)
    pdf.set_font('DV', '', 12)
    pdf.cell(0, 9, val, new_x='LMARGIN', new_y='NEXT')
pdf.ln(10)
pdf.set_draw_color(0, 51, 102)
pdf.set_line_width(0.8)
pdf.line(15, pdf.get_y(), 195, pdf.get_y())
pdf.ln(5)
pdf.set_font('DV', '', 11)
pdf.set_text_color(80, 80, 80)
pdf.multi_cell(0, 7,
    'This homework covers LP duality theory: constructing dual problems, '
    'graphical solutions, weak duality, complementary slackness, and '
    'shadow price interpretation.', align='C')

# ===============================================================
# DUALITY BACKGROUND
# ===============================================================
pdf.add_page()
pdf.section_title('Background: LP Duality Rules')
pdf.body(
    'Every Linear Program (primal) has a corresponding dual problem. '
    'The duality relationship is symmetric: the dual of the dual is the primal. '
    'Below are the complete transformation rules used throughout this homework.')

pdf.sub_title('Rules for MAX Primal \u2192 MIN Dual:')
pdf.body(
    'Primal (MAX): Max c\u1d40x,  s.t. Ax \u2264 b (or \u2265 or =),  x \u2265 0\n\n'
    'Row \u2192 Dual variable correspondence:\n'
    '  \u2022 Primal constraint \u2264   \u2192  Dual variable y_i \u2265 0\n'
    '  \u2022 Primal constraint \u2265   \u2192  Dual variable y_i \u2264 0\n'
    '  \u2022 Primal constraint =    \u2192  Dual variable y_i unrestricted (urs)\n\n'
    'Column \u2192 Dual constraint correspondence:\n'
    '  \u2022 Primal x_j \u2265 0  \u2192  Dual constraint j: (col j of A)\u1d40 y \u2265 c_j\n'
    '  \u2022 Primal x_j urs  \u2192  Dual constraint j: (col j of A)\u1d40 y = c_j\n\n'
    'Dual Objective: MIN b\u1d40y')

pdf.sub_title('Rules for MIN Primal \u2192 MAX Dual:')
pdf.body(
    'Primal (MIN): Min c\u1d40y,  s.t. Ay \u2265 b (or \u2264 or =),  y \u2265 0\n\n'
    'Row \u2192 Dual variable correspondence:\n'
    '  \u2022 Primal constraint \u2265   \u2192  Dual variable x_i \u2265 0\n'
    '  \u2022 Primal constraint \u2264   \u2192  Dual variable x_i \u2264 0\n'
    '  \u2022 Primal constraint =    \u2192  Dual variable x_i unrestricted (urs)\n\n'
    'Column \u2192 Dual constraint correspondence:\n'
    '  \u2022 Primal y_j \u2265 0  \u2192  Dual constraint j: (col j of A)\u1d40 x \u2264 c_j\n'
    '  \u2022 Primal y_j urs  \u2192  Dual constraint j: (col j of A)\u1d40 x = c_j\n\n'
    'Dual Objective: MAX b\u1d40x')

pdf.result_box(
    'Key Theorem \u2013 Strong Duality:\n'
    '  If the primal has an optimal solution x*, the dual also has an optimal y*,\n'
    '  and their objectives are equal: c\u1d40x* = b\u1d40y*.\n\n'
    'Weak Duality: For any primal feasible x and dual feasible y:\n'
    '  c\u1d40x \u2264 b\u1d40y   (MAX primal / MIN dual)')

# ===============================================================
# QUESTION 1
# ===============================================================
pdf.add_page()
pdf.section_title('Question 1: Determine the Dual of Each LP')

# ---- Q1(i) ----
pdf.sub_title('Part (i)  [10 pts]')
pdf.box_text(
    'PRIMAL (MAX):\n'
    '  Max  z = 2x\u2081 + x\u2082\n'
    '  s.t.\n'
    '    -x\u2081 + x\u2082  \u2264  1   ...(1)\n'
    '     x\u2081 + x\u2082  \u2264  3   ...(2)\n'
    '     x\u2081 - 2x\u2082 \u2264  4   ...(3)\n'
    '     x\u2081, x\u2082 \u2265 0')

pdf.step('Step 1 \u2013 Assign dual variables (each \u2264 constraint \u2192 y_i \u2265 0):',
    '  Constraint (1) is \u2264  \u2192  y\u2081 \u2265 0\n'
    '  Constraint (2) is \u2264  \u2192  y\u2082 \u2265 0\n'
    '  Constraint (3) is \u2264  \u2192  y\u2083 \u2265 0')

pdf.step('Step 2 \u2013 Dual objective (MIN; RHS values become obj. coefficients):',
    '  MIN  w = 1\u00b7y\u2081 + 3\u00b7y\u2082 + 4\u00b7y\u2083')

pdf.step('Step 3 \u2013 Dual constraints (each x_j \u2265 0 \u2192 constraint \u2265 c_j):',
    'For x\u2081 (\u2265 0): read coefficients of x\u2081 down each row: (-1), (+1), (+1)\n'
    '  \u21d2  -y\u2081 + y\u2082 + y\u2083 \u2265 2   [c\u2081 = 2]\n\n'
    'For x\u2082 (\u2265 0): coefficients of x\u2082 in rows: (+1), (+1), (-2)\n'
    '  \u21d2   y\u2081 + y\u2082 - 2y\u2083 \u2265 1   [c\u2082 = 1]')

pdf.result_box(
    'DUAL (Part i):\n'
    '  Min  w = y\u2081 + 3y\u2082 + 4y\u2083\n'
    '  s.t.\n'
    '    -y\u2081 + y\u2082 + y\u2083  \u2265 2\n'
    '     y\u2081 + y\u2082 - 2y\u2083 \u2265 1\n'
    '     y\u2081, y\u2082, y\u2083 \u2265 0')

# ---- Q1(ii) ----
pdf.sub_title('Part (ii)  [10 pts]')
pdf.box_text(
    'PRIMAL (MIN):\n'
    '  Min  w = y\u2081 - y\u2082\n'
    '  s.t.\n'
    '    2y\u2081 + y\u2082  \u2265 4   ...(5)\n'
    '     y\u2081 + y\u2082  \u2265 1   ...(6)\n'
    '     y\u2081 + 2y\u2082 \u2265 3   ...(7)\n'
    '     y\u2081, y\u2082 \u2265 0')

pdf.step('Step 1 \u2013 Assign dual variables (MIN primal \u2192 MAX dual; \u2265 \u2192 x_i \u2265 0):',
    '  Constraint (5) is \u2265  \u2192  x\u2081 \u2265 0\n'
    '  Constraint (6) is \u2265  \u2192  x\u2082 \u2265 0\n'
    '  Constraint (7) is \u2265  \u2192  x\u2083 \u2265 0')

pdf.step('Step 2 \u2013 Dual objective (MAX; RHS becomes obj. coeff.):',
    '  MAX  z = 4x\u2081 + 1\u00b7x\u2082 + 3x\u2083')

pdf.step('Step 3 \u2013 Dual constraints (each y_j \u2265 0 \u2192 constraint \u2264 c_j):',
    'For y\u2081 (\u2265 0): coefficients in rows: 2, 1, 1\n'
    '  \u21d2  2x\u2081 + x\u2082 + x\u2083 \u2264 1   [c\u2081 = 1]\n\n'
    'For y\u2082 (\u2265 0): coefficients in rows: 1, 1, 2\n'
    '  \u21d2   x\u2081 + x\u2082 + 2x\u2083 \u2264 -1  [c\u2082 = -1]')

pdf.result_box(
    'DUAL (Part ii):\n'
    '  Max  z = 4x\u2081 + x\u2082 + 3x\u2083\n'
    '  s.t.\n'
    '    2x\u2081 + x\u2082 +  x\u2083 \u2264  1\n'
    '     x\u2081 + x\u2082 + 2x\u2083 \u2264 -1\n'
    '     x\u2081, x\u2082, x\u2083 \u2265 0')

pdf.add_page()
# ---- Q1(iii) ----
pdf.sub_title('Part (iii)  [10 pts]')
pdf.box_text(
    'PRIMAL (MAX) \u2013 mixed constraints and unrestricted variables:\n'
    '  Max  z = 4x\u2081 - x\u2082 + 2x\u2083\n'
    '  s.t.\n'
    '     x\u2081 +  x\u2082          \u2264 5   ...(9)\n'
    '    2x\u2081 +  x\u2082          \u2264 7   ...(10)\n'
    '           2x\u2082 + x\u2083 \u2265 6   ...(11)\n'
    '     x\u2081        + x\u2083 = 4   ...(12)\n'
    '     x\u2081 \u2265 0;  x\u2082, x\u2083 unrestricted (urs)')

pdf.step('Step 1 \u2013 Assign dual variables:',
    '  Constraint (9)  is \u2264  \u2192  y\u2081 \u2265 0\n'
    '  Constraint (10) is \u2264  \u2192  y\u2082 \u2265 0\n'
    '  Constraint (11) is \u2265  \u2192  y\u2083 \u2264 0\n'
    '  Constraint (12) is =   \u2192  y\u2084 unrestricted (urs)')

pdf.step('Step 2 \u2013 Dual objective:',
    '  MIN  w = 5y\u2081 + 7y\u2082 + 6y\u2083 + 4y\u2084')

pdf.step('Step 3 \u2013 Dual constraints:',
    'For x\u2081 (\u2265 0) \u2192 constraint \u2265 c\u2081 = 4:\n'
    '  Coefficients in (9),(10),(11),(12): 1, 2, 0, 1\n'
    '  \u21d2  y\u2081 + 2y\u2082 + 0\u00b7y\u2083 + y\u2084 \u2265 4\n\n'
    'For x\u2082 (urs) \u2192 constraint = c\u2082 = -1:\n'
    '  Coefficients in (9),(10),(11),(12): 1, 1, 2, 0\n'
    '  \u21d2  y\u2081 + y\u2082 + 2y\u2083 = -1\n\n'
    'For x\u2083 (urs) \u2192 constraint = c\u2083 = 2:\n'
    '  Coefficients in (9),(10),(11),(12): 0, 0, 1, 1\n'
    '  \u21d2  y\u2083 + y\u2084 = 2')

pdf.result_box(
    'DUAL (Part iii):\n'
    '  Min  w = 5y\u2081 + 7y\u2082 + 6y\u2083 + 4y\u2084\n'
    '  s.t.\n'
    '    y\u2081 + 2y\u2082        + y\u2084  \u2265  4\n'
    '    y\u2081 +  y\u2082 + 2y\u2083        =  -1\n'
    '                y\u2083 + y\u2084  =   2\n'
    '    y\u2081, y\u2082 \u2265 0;  y\u2083 \u2264 0;  y\u2084 urs')

pdf.ln(3)
# ---- Q1(iv) ----
pdf.sub_title('Part (iv)  [10 pts]')
pdf.box_text(
    'PRIMAL (MIN) \u2013 mixed constraints and unrestricted variables:\n'
    '  Min  w = 4y\u2081 + 2y\u2082 - y\u2083\n'
    '  s.t.\n'
    '     y\u2081 + 2y\u2082          \u2264  6   ...(14)\n'
    '     y\u2081 -  y\u2082 + 2y\u2083  =  8   ...(15)\n'
    '     y\u2081 \u2265 0;  y\u2082, y\u2083 unrestricted (urs)')

pdf.step('Step 1 \u2013 Assign dual variables (MIN \u2192 MAX dual):',
    '  Constraint (14) is \u2264  \u2192  x\u2081 \u2264 0\n'
    '  Constraint (15) is =   \u2192  x\u2082 unrestricted (urs)')

pdf.step('Step 2 \u2013 Dual objective:',
    '  MAX  z = 6x\u2081 + 8x\u2082')

pdf.step('Step 3 \u2013 Dual constraints:',
    'For y\u2081 (\u2265 0) \u2192 constraint \u2264 c\u2081 = 4:\n'
    '  Coefficients in (14),(15): 1, 1\n'
    '  \u21d2  x\u2081 + x\u2082 \u2264 4\n\n'
    'For y\u2082 (urs) \u2192 constraint = c\u2082 = 2:\n'
    '  Coefficients in (14),(15): 2, -1\n'
    '  \u21d2  2x\u2081 - x\u2082 = 2\n\n'
    'For y\u2083 (urs) \u2192 constraint = c\u2083 = -1:\n'
    '  Coefficients in (14),(15): 0, 2\n'
    '  \u21d2  2x\u2082 = -1')

pdf.result_box(
    'DUAL (Part iv):\n'
    '  Max  z = 6x\u2081 + 8x\u2082\n'
    '  s.t.\n'
    '     x\u2081 + x\u2082  \u2264  4\n'
    '    2x\u2081 - x\u2082  =  2\n'
    '         2x\u2082  = -1\n'
    '     x\u2081 \u2264 0;  x\u2082 urs')

# ===============================================================
# QUESTION 2
# ===============================================================
pdf.add_page()
pdf.section_title('Question 2: Dual Construction + Graphical Solution  [10 pts]')

pdf.sub_title('Part (i) \u2013 Construct the Dual')
pdf.box_text(
    'PRIMAL (MAX):\n'
    '  Max  z = 2x\u2081 + 3x\u2082 + 6x\u2083\n'
    '  s.t.\n'
    '    x\u2081       + x\u2083 \u2264 3   ...(19)\n'
    '         x\u2082 + x\u2083 \u2264 5   ...(20)\n'
    '    x\u2081, x\u2082, x\u2083 \u2265 0')

pdf.step('Step 1 \u2013 Assign dual variables:',
    '  Constraint (19) is \u2264  \u2192  y\u2081 \u2265 0\n'
    '  Constraint (20) is \u2264  \u2192  y\u2082 \u2265 0')

pdf.step('Step 2 \u2013 Dual objective (MIN):',
    '  MIN  w = 3y\u2081 + 5y\u2082')

pdf.step('Step 3 \u2013 Dual constraints (x_j \u2265 0 \u2192 \u2265 c_j):',
    'Column x\u2081: coefficients (19)\u21921, (20)\u21920  \u21d2  y\u2081 \u2265 2\n'
    'Column x\u2082: coefficients (19)\u21920, (20)\u21921  \u21d2  y\u2082 \u2265 3\n'
    'Column x\u2083: coefficients (19)\u21921, (20)\u21921  \u21d2  y\u2081 + y\u2082 \u2265 6')

pdf.result_box(
    'DUAL:\n'
    '  Min  w = 3y\u2081 + 5y\u2082\n'
    '  s.t.\n'
    '    y\u2081        \u2265 2\n'
    '         y\u2082  \u2265 3\n'
    '    y\u2081 + y\u2082  \u2265 6\n'
    '    y\u2081, y\u2082 \u2265 0')

pdf.sub_title('Part (ii) \u2013 Solve the Dual Graphically')
pdf.step('Step 1 \u2013 Identify constraint boundaries in the y\u2081-y\u2082 plane:',
    'L1: y\u2081 = 2          (vertical line; feasible region to the right)\n'
    'L2: y\u2082 = 3          (horizontal line; feasible region above)\n'
    'L3: y\u2081 + y\u2082 = 6    (diagonal line; feasible region above)\n\n'
    'Note: if y\u2081 \u2265 2 and y\u2082 \u2265 3, then y\u2081+y\u2082 \u2265 5, but we need \u2265 6.\n'
    'So L3 is NOT redundant; it cuts off the corner near (2, 3).')

pdf.step('Step 2 \u2013 Find corner (extreme) points of the feasible region:',
    'Corner A: intersection of L1 and L3\n'
    '  y\u2081 = 2  and  y\u2081 + y\u2082 = 6  \u21d2  y\u2082 = 4\n'
    '  \u21d2  Corner A = (2, 4)\n\n'
    'Corner B: intersection of L2 and L3\n'
    '  y\u2082 = 3  and  y\u2081 + y\u2082 = 6  \u21d2  y\u2081 = 3\n'
    '  \u21d2  Corner B = (3, 3)\n\n'
    'The feasible region extends to the upper-right beyond these corners\n'
    '(the objective increases in that direction, so the minimum is at a corner).')

pdf.step('Step 3 \u2013 Evaluate dual objective at each corner:',
    'Objective: w = 3y\u2081 + 5y\u2082\n\n'
    '  Corner A = (2, 4):  w = 3(2) + 5(4) = 6 + 20 = 26\n'
    '  Corner B = (3, 3):  w = 3(3) + 5(3) = 9 + 15 = 24\n\n'
    'Minimum w = 24 at Corner B = (y\u2081*, y\u2082*) = (3, 3).')

pdf.result_box(
    'DUAL OPTIMAL SOLUTION:\n'
    '  y\u2081* = 3,  y\u2082* = 3,  w* = 24\n\n'
    'SHADOW PRICES (dual variables = shadow prices of primal constraints):\n'
    '  Shadow price of constraint (19) [x\u2081 + x\u2083 \u2264 3]:  \u03c0\u2081 = y\u2081* = 3\n'
    '  Shadow price of constraint (20) [x\u2082 + x\u2083 \u2264 5]:  \u03c0\u2082 = y\u2082* = 3\n\n'
    'Interpretation: Each additional unit of RHS in constraint (19) or (20)\n'
    'increases the primal optimal profit by 3 units.\n\n'
    'Verification via Strong Duality:\n'
    '  Primal solution: x\u2081=0, x\u2082=2, x\u2083=3  \u2192  z = 0+6+18 = 24 = w*  \[OK]')

# ===============================================================
# QUESTION 3
# ===============================================================
pdf.add_page()
pdf.section_title('Question 3: Infeasible Primal / Unbounded Dual  [15 pts]')

pdf.sub_title('Part (i) \u2013 Primal Has No Feasible Solution (Graphical Proof)')
pdf.box_text(
    'PRIMAL (MAX):\n'
    '  Max  z = x\u2081 + 2x\u2082\n'
    '  s.t.\n'
    '    -x\u2081 + x\u2082  \u2264 -2   ...(24)   equivalently: x\u2082 \u2264 x\u2081 - 2\n'
    '     4x\u2081 + x\u2082  \u2264  4   ...(25)   equivalently: x\u2082 \u2264 4 - 4x\u2081\n'
    '     x\u2081, x\u2082 \u2265 0')

pdf.step('Step 1 \u2013 Derive implied lower bound on x\u2081:',
    'From constraint (24): x\u2082 \u2264 x\u2081 - 2\n'
    'From non-negativity:   x\u2082 \u2265 0\n'
    'Combining:  0 \u2264 x\u2082 \u2264 x\u2081 - 2\n'
    'This requires:  x\u2081 - 2 \u2265 0  \u21d2  x\u2081 \u2265 2')

pdf.step('Step 2 \u2013 Substitute x\u2081 \u2265 2 into constraint (25):',
    'From (25): x\u2082 \u2264 4 - 4x\u2081\n'
    'If x\u2081 \u2265 2:  4 - 4x\u2081 \u2264 4 - 4(2) = 4 - 8 = -4\n'
    'So: x\u2082 \u2264 -4 < 0\n\n'
    'But x\u2082 \u2265 0 is required. This is a CONTRADICTION.')

pdf.step('Step 3 \u2013 Graphical interpretation:',
    'On the y-axis (x\u2082 axis):\n'
    '  Region from (24) with x\u2082\u22650: starts at x\u2081=2, allowing x\u2082 between 0 and x\u2081-2.\n'
    '  Region from (25): for x\u2081\u22652, x\u2082 must be \u2264 4-4x\u2081 \u2264 -4 (below x-axis).\n'
    'These two half-planes do not intersect in the first quadrant (x\u2081,x\u2082 \u2265 0).')

pdf.result_box(
    'CONCLUSION (Part i):\n'
    '  The primal feasible region is EMPTY. No (x\u2081, x\u2082) with x\u2081,x\u2082 \u2265 0 can\n'
    '  simultaneously satisfy constraints (24) and (25).\n'
    '  The primal problem has NO FEASIBLE SOLUTION.')

pdf.sub_title('Part (ii) \u2013 Construct the Dual')
pdf.step('Step 1 \u2013 Assign dual variables:',
    '  Constraint (24) is \u2264  \u2192  y\u2081 \u2265 0\n'
    '  Constraint (25) is \u2264  \u2192  y\u2082 \u2265 0')

pdf.step('Step 2 \u2013 Dual objective:',
    '  MIN  w = -2y\u2081 + 4y\u2082')

pdf.step('Step 3 \u2013 Dual constraints:',
    'Column x\u2081: coeff in (24)\u2192-1, (25)\u21924  \u21d2  -y\u2081 + 4y\u2082 \u2265 1\n'
    'Column x\u2082: coeff in (24)\u21921, (25)\u21921  \u21d2   y\u2081 +  y\u2082 \u2265 2')

pdf.result_box(
    'DUAL:\n'
    '  Min  w = -2y\u2081 + 4y\u2082\n'
    '  s.t.\n'
    '    -y\u2081 + 4y\u2082  \u2265 1\n'
    '     y\u2081 +  y\u2082  \u2265 2\n'
    '     y\u2081, y\u2082 \u2265 0')

pdf.sub_title('Part (iii) \u2013 Dual is Unbounded (Graphical Proof)')
pdf.step('Step 1 \u2013 Confirm the dual is feasible:',
    'Try (y\u2081, y\u2082) = (1, 1):\n'
    '  Constraint (i):  -1 + 4(1) = 3 \u2265 1  \[OK]\n'
    '  Constraint (ii):  1 + 1 = 2 \u2265 2  \[OK]\n'
    '  y\u2081, y\u2082 \u2265 0  \[OK]\n'
    '  w = -2(1) + 4(1) = 2\n\n'
    'The dual is feasible.')

pdf.step('Step 2 \u2013 Find a ray along which w \u2192 -\u221e:',
    'Let y\u2081 \u2192 +\u221e and set y\u2082 = (1 + y\u2081)/4  (minimum from constraint i)\n\n'
    'Objective along this ray:\n'
    '  w = -2y\u2081 + 4 \u00d7 (1+y\u2081)/4 = -2y\u2081 + 1 + y\u2081 = -y\u2081 + 1\n'
    '  As y\u2081 \u2192 +\u221e:  w \u2192 -\u221e\n\n'
    'Check constraint (ii) along this ray:\n'
    '  y\u2081 + y\u2082 = y\u2081 + (1+y\u2081)/4 = (5y\u2081+1)/4 \u2192 +\u221e \u2265 2  \[OK]\n'
    'Check y\u2082 \u2265 0: y\u2082 = (1+y\u2081)/4 > 0  \[OK]')

pdf.step('Step 3 \u2013 Graphical interpretation:',
    'On the y\u2081-y\u2082 plane, the feasible region is unbounded in the direction\n'
    'of increasing y\u2081 (to the right). The objective contours w = -2y\u2081 + 4y\u2082\n'
    'have gradient (-2, 4), meaning the objective DECREASES as y\u2081 increases\n'
    '(for fixed w, moving right reduces w). Since we can move y\u2081\u2192\u221e while\n'
    'staying feasible, w\u2192-\u221e and the problem is UNBOUNDED.')

pdf.result_box(
    'CONCLUSION (Part iii):\n'
    '  The dual is UNBOUNDED (w \u2192 -\u221e along the ray y\u2081\u2192\u221e, y\u2082=(1+y\u2081)/4).\n\n'
    'This is consistent with LP Duality Theory:\n'
    '  Primal INFEASIBLE  \u21d2  Dual is either INFEASIBLE or UNBOUNDED.\n'
    '  Here the dual is feasible but unbounded, confirming the primal\n'
    '  has no feasible solution.')

# ===============================================================
# QUESTION 4
# ===============================================================
pdf.add_page()
pdf.section_title('Question 4: Weak Duality and Complementary Slackness  [20 pts]')

pdf.box_text(
    'PRIMAL (MAX):\n'
    '  Max  z = 2x\u2081 + 5x\u2082 + 4x\u2083\n'
    '  s.t.\n'
    '     x\u2081 + 2x\u2082 + 4x\u2083  \u2264 10   ...(29)\n'
    '    3x\u2081 + 3x\u2082 + 2x\u2083  \u2264 10   ...(30)\n'
    '     x\u2081, x\u2082, x\u2083 \u2265 0')

pdf.sub_title('Part (i) \u2013 Construct the Dual')
pdf.step('Step 1 \u2013 Assign dual variables:',
    '  Constraint (29) is \u2264  \u2192  y\u2081 \u2265 0\n'
    '  Constraint (30) is \u2264  \u2192  y\u2082 \u2265 0')

pdf.step('Step 2 \u2013 Dual objective:',
    '  MIN  w = 10y\u2081 + 10y\u2082')

pdf.step('Step 3 \u2013 Dual constraints:',
    'Column x\u2081: coeff (29)\u21921, (30)\u21923  \u21d2  y\u2081 + 3y\u2082 \u2265 2\n'
    'Column x\u2082: coeff (29)\u21922, (30)\u21923  \u21d2  2y\u2081 + 3y\u2082 \u2265 5\n'
    'Column x\u2083: coeff (29)\u21924, (30)\u21922  \u21d2  4y\u2081 + 2y\u2082 \u2265 4')

pdf.result_box(
    'DUAL:\n'
    '  Min  w = 10y\u2081 + 10y\u2082\n'
    '  s.t.\n'
    '     y\u2081 + 3y\u2082  \u2265 2\n'
    '    2y\u2081 + 3y\u2082  \u2265 5\n'
    '    4y\u2081 + 2y\u2082  \u2265 4\n'
    '     y\u2081, y\u2082 \u2265 0')

pdf.sub_title('Part (ii) \u2013 Weak Duality: Optimal Primal Value \u2264 25')
pdf.step('Weak Duality Theorem:',
    'For ANY primal feasible x and ANY dual feasible y:\n'
    '    z = c\u1d40x  \u2264  b\u1d40y = w\n\n'
    'Therefore: optimal z* \u2264 (value of any feasible dual solution).\n'
    'We find a dual feasible solution with w = 25.')

pdf.step('Find a feasible dual solution:',
    'Try y\u2081 = 5/2 = 2.5,  y\u2082 = 0:\n\n'
    '  Constraint 1:  y\u2081 + 3y\u2082 = 2.5 + 0 = 2.5 \u2265 2  \[OK]\n'
    '  Constraint 2: 2y\u2081 + 3y\u2082 = 5.0 + 0 = 5.0 \u2265 5  \[OK]\n'
    '  Constraint 3: 4y\u2081 + 2y\u2082 = 10.0 + 0 = 10  \u2265 4  \[OK]\n'
    '  y\u2081, y\u2082 \u2265 0: 2.5 \u2265 0, 0 \u2265 0  \[OK]\n\n'
    '  Dual objective: w = 10(2.5) + 10(0) = 25')

pdf.result_box(
    'CONCLUSION (Part ii):\n'
    '  (y\u2081, y\u2082) = (2.5, 0) is dual feasible with w = 25.\n'
    '  By Weak Duality:  z*  \u2264  w = 25\n'
    '  \u21d2 The optimal primal objective value cannot exceed 25.  \[OK]')

pdf.sub_title('Part (iii) \u2013 Basic Solution (x\u2082, x\u2083 basic) + Complementary Slackness')

pdf.step('Step 1 \u2013 Set up basis matrix B = [A\u2082 | A\u2083]:',
    'Non-basic variable: x\u2081 = 0.\n'
    'Basis columns from constraint matrix (rows = constraints (29),(30)):\n\n'
    '  A\u2082 = column of x\u2082 = [2, 3]\u1d40\n'
    '  A\u2083 = column of x\u2083 = [4, 2]\u1d40\n\n'
    '       [ 2   4 ]\n'
    '  B  = [ 3   2 ]\n\n'
    '  det(B) = (2)(2) \u2212 (4)(3) = 4 \u2212 12 = \u22128')

pdf.step('Step 2 \u2013 Compute B\u207b\u00b9:',
    'For 2\u00d72 matrix [[a,b],[c,d]]:  B\u207b\u00b9 = (1/det) \u00d7 [[d,\u2212b],[\u2212c,a]]\n\n'
    '  B\u207b\u00b9 = (1/\u22128) \u00d7 [[ 2, \u22124], [\u22123,  2]]\n\n'
    '         = [ [\u22121/4,  1/2],\n'
    '             [ 3/8, \u22121/4] ]')

pdf.step('Step 3 \u2013 Compute basic variable values x_B = B\u207b\u00b9b  (b = [10, 10]\u1d40):',
    '  x\u2082 = (\u22121/4)(10) + (1/2)(10) = \u22122.5 + 5.0 = 2.5\n'
    '  x\u2083 = ( 3/8)(10) + (\u22121/4)(10) = 3.75 \u2212 2.5 = 1.25\n\n'
    'Full primal solution: x\u2081 = 0,  x\u2082 = 2.5,  x\u2083 = 1.25\n\n'
    'Primal objective:\n'
    '  z = 2(0) + 5(2.5) + 4(1.25) = 0 + 12.5 + 5.0 = 17.5')

pdf.step('Step 4 \u2013 Derive dual solution: y* = c_B \u00d7 B\u207b\u00b9:',
    'c_B = [c\u2082, c\u2083] = [5, 4]  (objective coefficients of basic variables)\n\n'
    '  y\u2081* = c_B \u00b7 (col 1 of B\u207b\u00b9)\n'
    '       = 5(\u22121/4) + 4(3/8)\n'
    '       = \u22125/4 + 12/8 = \u221210/8 + 12/8 = 2/8 = 0.25\n\n'
    '  y\u2082* = c_B \u00b7 (col 2 of B\u207b\u00b9)\n'
    '       = 5(1/2) + 4(\u22121/4)\n'
    '       = 5/2 \u2212 1 = 3/2 = 1.5\n\n'
    'Dual solution: y\u2081* = 0.25,  y\u2082* = 1.5\n'
    'Dual objective: w = 10(0.25) + 10(1.5) = 2.5 + 15 = 17.5')

pdf.step('Step 5 \u2013 Verify Complementary Slackness (CS):',
    'CS Condition A: y_i* \u00d7 (primal slack of constraint i) = 0 for all i\n\n'
    '  Constraint (29): x\u2081+2x\u2082+4x\u2083 = 0 + 5 + 5 = 10  \u21d2 slack = 10\u221210 = 0\n'
    '    y\u2081* = 0.25 > 0;  slack = 0  \u21d2  0.25 \u00d7 0 = 0  \[OK]\n\n'
    '  Constraint (30): 3x\u2081+3x\u2082+2x\u2083 = 0 + 7.5 + 2.5 = 10  \u21d2 slack = 0\n'
    '    y\u2082* = 1.5 > 0;  slack = 0  \u21d2  1.5 \u00d7 0 = 0  \[OK]\n\n'
    'CS Condition B: x_j* \u00d7 (dual slack of constraint j) = 0 for all j\n\n'
    '  For x\u2081: dual constraint is y\u2081+3y\u2082 \u2265 2\n'
    '    LHS = 0.25 + 4.5 = 4.75  \u21d2 dual slack = 4.75\u22122 = 2.75\n'
    '    x\u2081* = 0  \u21d2  0 \u00d7 2.75 = 0  \[OK]\n\n'
    '  For x\u2082: dual constraint is 2y\u2081+3y\u2082 \u2265 5\n'
    '    LHS = 0.5 + 4.5 = 5.0  \u21d2 dual slack = 0\n'
    '    x\u2082* = 2.5 > 0;  dual slack = 0  \u21d2  2.5 \u00d7 0 = 0  \[OK]\n\n'
    '  For x\u2083: dual constraint is 4y\u2081+2y\u2082 \u2265 4\n'
    '    LHS = 1.0 + 3.0 = 4.0  \u21d2 dual slack = 0\n'
    '    x\u2083* = 1.25 > 0;  dual slack = 0  \u21d2  1.25 \u00d7 0 = 0  \[OK]')

pdf.result_box(
    'CONCLUSION (Part iii):\n'
    '  Primal: x\u2081=0, x\u2082=2.5, x\u2083=1.25  \u21d2  z = 17.5\n'
    '  Dual:   y\u2081=0.25, y\u2082=1.5         \u21d2  w = 17.5\n\n'
    '  Since z = w = 17.5 (objectives are equal), and all Complementary\n'
    '  Slackness conditions are satisfied, BOTH solutions are OPTIMAL.\n\n'
    '  The true optimal is 17.5 (within the bound of \u2264 25 shown in Part ii).')

# ===============================================================
# QUESTION 5
# ===============================================================
pdf.add_page()
pdf.section_title('Question 5: Shadow Prices and Willingness-to-Pay  [15 pts]')

pdf.box_text(
    'LP:\n'
    '  Max  z = 3x\u2081 + 7x\u2082 + 5x\u2083\n'
    '  s.t.\n'
    '     x\u2081 + x\u2082 + x\u2083  \u2264 50    ... Sugar Capacity\n'
    '    2x\u2081 + 3x\u2082 + x\u2083  \u2264 100   ... Chocolate Capacity\n'
    '     x\u2081, x\u2082, x\u2083 \u2265 0\n\n'
    'Optimal basis: {x\u2083, x\u2082}   (ordered: x\u2083 first, x\u2082 second)\n\n'
    '         [ 3/2   -1/2 ]\n'
    '  B\u207b\u00b9 =  [-1/2    1/2 ]')

pdf.sub_title('Part (i) \u2013 Determine Shadow Prices')
pdf.step('Step 1 \u2013 Identify basis columns and verify B\u207b\u00b9:',
    'The basis is ordered {x\u2083, x\u2082}.\n'
    'From the constraint matrix (rows = Sugar, Chocolate constraints):\n\n'
    '  A\u2083 = [1, 1]\u1d40  (x\u2083 has coefficient 1 in both constraints)\n'
    '  A\u2082 = [1, 3]\u1d40  (x\u2082 has coefficient 1 in sugar, 3 in chocolate)\n\n'
    '       [ 1  1 ]\n'
    '  B  = [ 1  3 ]\n\n'
    '  det(B) = (1)(3) \u2212 (1)(1) = 3 \u2212 1 = 2\n\n'
    '  B\u207b\u00b9 = (1/2)\u00d7[[ 3, \u22121],[\u22121, 1]] = [[ 3/2, \u22121/2],[\u22121/2, 1/2]]\n\n'
    '  This matches the given B\u207b\u00b9.  \[OK]')

pdf.step('Step 2 \u2013 Compute shadow prices: y* = c_B \u00d7 B\u207b\u00b9:',
    'c_B = [c\u2083, c\u2082] = [5, 7]  (objective coefficients in basis order)\n\n'
    '  y\u2081* = c_B \u00b7 (column 1 of B\u207b\u00b9)    [shadow price of Sugar]\n'
    '       = 5(3/2) + 7(\u22121/2)\n'
    '       = 15/2 \u2212 7/2 = 8/2 = 4\n\n'
    '  y\u2082* = c_B \u00b7 (column 2 of B\u207b\u00b9)    [shadow price of Chocolate]\n'
    '       = 5(\u22121/2) + 7(1/2)\n'
    '       = \u22125/2 + 7/2 = 2/2 = 1')

pdf.result_box(
    'SHADOW PRICES:\n'
    '  y\u2081* = 4 cents per oz  (Sugar Capacity constraint)\n'
    '  y\u2082* = 1 cent  per oz  (Chocolate Capacity constraint)\n\n'
    'Interpretation:\n'
    '  Sugar shadow price = 4: Each additional 1 oz of sugar (beyond the\n'
    '  current 50 oz limit) allows Company X to increase its total profit\n'
    '  by 4 cents, at the current optimal basis.\n\n'
    '  Chocolate shadow price = 1: Each additional 1 oz of chocolate (beyond\n'
    '  the current 100 oz limit) increases total profit by 1 cent at the\n'
    '  current optimal basis.\n\n'
    '  Sugar is the more valuable (binding) resource in this solution,\n'
    '  as it has a higher marginal value (4 > 1).')

pdf.sub_title('Part (ii) \u2013 Maximum Willingness-to-Pay for 1 Extra oz of Sugar')
pdf.step('Reasoning using shadow prices:',
    'The shadow price y\u2081* = 4 is the marginal value of 1 additional oz of sugar.\n\n'
    'If Company X pays a price P per extra oz of sugar, the net benefit is:\n'
    '  Net benefit = marginal value \u2212 cost = 4 \u2212 P\n\n'
    'Company X will purchase extra sugar as long as it does not lose money:\n'
    '  4 \u2212 P \u2265 0  \u21d2  P \u2264 4\n\n'
    'The break-even point is at P = 4. Paying more than 4 cents per oz\n'
    'would reduce the company\u2019s net profit.')

pdf.result_box(
    'ANSWER (Part ii):\n'
    '  Maximum willingness-to-pay for 1 extra oz of Sugar = 4 cents\n\n'
    '  Company X should not pay more than 4 cents per additional oz of sugar.')

pdf.sub_title('Part (iii) \u2013 Maximum Willingness-to-Pay for 1 Extra oz of Chocolate')
pdf.step('Reasoning using shadow prices:',
    'The shadow price y\u2082* = 1 is the marginal value of 1 additional oz of chocolate.\n\n'
    'If Company X pays a price P per extra oz of chocolate, the net benefit is:\n'
    '  Net benefit = 1 \u2212 P\n\n'
    'Company X will purchase extra chocolate as long as:\n'
    '  1 \u2212 P \u2265 0  \u21d2  P \u2264 1')

pdf.result_box(
    'ANSWER (Part iii):\n'
    '  Maximum willingness-to-pay for 1 extra oz of Chocolate = 1 cent\n\n'
    '  Company X should not pay more than 1 cent per additional oz of chocolate.\n'
    '  Chocolate is less valuable at the margin than sugar in this solution.')

# ===============================================================
# SUMMARY PAGE
# ===============================================================
pdf.add_page()
pdf.section_title('Summary of All Results')

rows = [
    ('Q1(i)',    'Dual of MAX 2x\u2081+x\u2082',
     'Min y\u2081+3y\u2082+4y\u2083  s.t.  -y\u2081+y\u2082+y\u2083\u22652, y\u2081+y\u2082-2y\u2083\u22651'),
    ('Q1(ii)',   'Dual of MIN y\u2081-y\u2082',
     'Max 4x\u2081+x\u2082+3x\u2083  s.t.  2x\u2081+x\u2082+x\u2083\u22641, x\u2081+x\u2082+2x\u2083\u2264-1'),
    ('Q1(iii)',  'Dual of MAX 4x\u2081-x\u2082+2x\u2083',
     'Min 5y\u2081+7y\u2082+6y\u2083+4y\u2084  (see full solution for constraints)'),
    ('Q1(iv)',   'Dual of MIN 4y\u2081+2y\u2082-y\u2083',
     'Max 6x\u2081+8x\u2082  s.t. x\u2081+x\u2082\u22644, 2x\u2081-x\u2082=2, 2x\u2082=-1'),
    ('Q2(i)',    'Dual of Q2 MAX primal',
     'Min 3y\u2081+5y\u2082  s.t. y\u2081\u22652, y\u2082\u22653, y\u2081+y\u2082\u22656'),
    ('Q2(ii)',   'Graphical dual optimal',
     'y\u2081*=3, y\u2082*=3, w*=24; shadow prices \u03c0\u2081=3, \u03c0\u2082=3'),
    ('Q3(i)',    'Primal infeasibility',
     'INFEASIBLE: x\u2081\u22652 required, but then x\u2082\u2264-4<0. Empty region.'),
    ('Q3(ii)',   'Dual of Q3 MAX',
     'Min -2y\u2081+4y\u2082  s.t. -y\u2081+4y\u2082\u22651, y\u2081+y\u2082\u22652'),
    ('Q3(iii)',  'Dual unbounded',
     'Ray y\u2081\u2192\u221e, y\u2082=(1+y\u2081)/4 is feasible and gives w\u2192-\u221e. UNBOUNDED.'),
    ('Q4(i)',    'Dual of Q4 MAX',
     'Min 10y\u2081+10y\u2082  s.t. y\u2081+3y\u2082\u22652, 2y\u2081+3y\u2082\u22655, 4y\u2081+2y\u2082\u22654'),
    ('Q4(ii)',   'Weak duality proof',
     '(y\u2081,y\u2082)=(2.5,0) feasible, w=25 \u21d2 optimal primal \u226425'),
    ('Q4(iii)',  'CS & optimality',
     'x*=(0,2.5,1.25) z=17.5; y*=(0.25,1.5) w=17.5. z=w \u21d2 BOTH OPTIMAL'),
    ('Q5(i)',    'Shadow prices',
     'y\u2081*=4 cents/oz (Sugar), y\u2082*=1 cent/oz (Chocolate)'),
    ('Q5(ii)',   'WTP for Sugar',
     'Maximum willingness-to-pay = 4 cents per oz'),
    ('Q5(iii)',  'WTP for Chocolate',
     'Maximum willingness-to-pay = 1 cent per oz'),
]

W = 180  # usable width
for q, label, result in rows:
    pdf.set_x(pdf.l_margin)
    pdf.set_font('DV', 'B', 9.5)
    pdf.set_fill_color(220, 230, 255)
    pdf.cell(18, 7, q, border=1, fill=True)
    pdf.set_fill_color(240, 243, 255)
    pdf.cell(50, 7, label, border=1, fill=True)
    pdf.set_font('DV', '', 9.5)
    pdf.set_fill_color(255, 255, 255)
    pdf.multi_cell(W - 68, 7, result, border=1)

pdf.ln(5)
pdf.set_font('DV', '', 10)
pdf.set_text_color(80, 80, 80)
pdf.multi_cell(0, 6,
    'Prepared by: Lana Jalal Gidan  |  SSIE 553, Spring 2026  |  Professor Neha Patankar\n'
    'Binghamton University, Thomas J. Watson College of Engineering and Applied Science')

out = 'homework/SSIE553_Homework5_Lana_Jalal_Gidan.pdf'
pdf.output(out)
print(f'Saved: {out}')

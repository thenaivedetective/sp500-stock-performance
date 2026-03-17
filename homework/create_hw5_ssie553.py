from fpdf import FPDF

FONT_REG  = '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'

class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-13)
        self.set_font('DV', '', 9)
        self.set_text_color(130, 130, 130)
        self.cell(0, 6, f'Page {self.page_no()}', align='C')

pdf = PDF()
pdf.add_font('DV', '',  FONT_REG)
pdf.add_font('DV', 'B', FONT_BOLD)
pdf.set_margins(20, 20, 20)
pdf.set_auto_page_break(auto=True, margin=18)

def title(txt):
    pdf.set_x(pdf.l_margin)
    pdf.set_font('DV', 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 7, txt)
    pdf.ln(1)

def heading(txt):
    pdf.set_x(pdf.l_margin)
    pdf.set_font('DV', 'B', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 7, txt)
    pdf.ln(1)

def text(txt):
    pdf.set_x(pdf.l_margin)
    pdf.set_font('DV', '', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 7, txt)
    pdf.ln(1)

def bold(txt):
    pdf.set_x(pdf.l_margin)
    pdf.set_font('DV', 'B', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 7, txt)
    pdf.ln(1)

def hr():
    pdf.set_draw_color(180, 180, 180)
    pdf.set_line_width(0.3)
    pdf.line(pdf.l_margin, pdf.get_y(), 190, pdf.get_y())
    pdf.set_draw_color(0, 0, 0)
    pdf.ln(3)

# =====================================================================
# HEADER
# =====================================================================
pdf.add_page()
pdf.set_font('DV', 'B', 13)
pdf.cell(0, 8, 'Homework 5  -  SSIE 553', new_x='LMARGIN', new_y='NEXT', align='C')
pdf.set_font('DV', '', 11)
pdf.cell(0, 7, 'Lana Jalal Gidan  |  Spring 2026  |  Prof. Neha Patankar', new_x='LMARGIN', new_y='NEXT', align='C')
pdf.ln(4)
hr()

# =====================================================================
# QUESTION 1(i)
# =====================================================================
title('Question 1(i)')
text(
    'Primal:\n'
    '  Max  z = 2x1 + x2\n'
    '  s.t.\n'
    '    -x1 + x2  <= 1   ...(1)\n'
    '     x1 + x2  <= 3   ...(2)\n'
    '     x1 - 2x2 <= 4   ...(3)\n'
    '     x1, x2 >= 0'
)

heading('Step 1: Identify dual variables')
text(
    'Since all primal constraints are (<=) and the objective is MAX, '
    'the dual is a MIN problem. Each <= constraint produces one dual variable >= 0:\n'
    '  Constraint (1) is <=  =>  y1 >= 0\n'
    '  Constraint (2) is <=  =>  y2 >= 0\n'
    '  Constraint (3) is <=  =>  y3 >= 0'
)

heading('Step 2: Write the dual objective')
text(
    'The dual objective is MIN, and the RHS values of the primal constraints '
    'become the objective coefficients of the dual:\n\n'
    '  MIN  w = 1*y1 + 3*y2 + 4*y3'
)

heading('Step 3: Write dual constraints (one per primal variable)')
text(
    'Each primal variable xj >= 0 generates a dual constraint of the form:\n'
    '  (column j of A)^T * y >= cj\n\n'
    'For x1 (c1 = 2): read coefficients of x1 in rows (1),(2),(3): -1, +1, +1\n'
    '  => -y1 + y2 + y3 >= 2\n\n'
    'For x2 (c2 = 1): coefficients of x2 in rows (1),(2),(3): +1, +1, -2\n'
    '  => y1 + y2 - 2y3 >= 1'
)

bold('DUAL PROBLEM:')
text(
    '  Min  w = y1 + 3y2 + 4y3\n'
    '  s.t.\n'
    '    -y1 + y2 + y3  >= 2\n'
    '     y1 + y2 - 2y3 >= 1\n'
    '     y1, y2, y3 >= 0'
)
hr()

# =====================================================================
# QUESTION 1(ii)
# =====================================================================
title('Question 1(ii)')
text(
    'Primal:\n'
    '  Min  w = y1 - y2\n'
    '  s.t.\n'
    '    2y1 + y2  >= 4   ...(5)\n'
    '     y1 + y2  >= 1   ...(6)\n'
    '     y1 + 2y2 >= 3   ...(7)\n'
    '     y1, y2 >= 0'
)

heading('Step 1: Identify dual variables')
text(
    'The primal is MIN, so its dual is MAX. Each >= constraint produces one '
    'dual variable >= 0:\n'
    '  Constraint (5) is >=  =>  x1 >= 0\n'
    '  Constraint (6) is >=  =>  x2 >= 0\n'
    '  Constraint (7) is >=  =>  x3 >= 0'
)

heading('Step 2: Write the dual objective')
text(
    'The dual is MAX and the RHS values of the primal become the dual '
    'objective coefficients:\n\n'
    '  MAX  z = 4x1 + 1*x2 + 3x3'
)

heading('Step 3: Write dual constraints (one per primal variable)')
text(
    'Each primal variable yj >= 0 generates a dual constraint of the form:\n'
    '  (column j of A)^T * x <= cj\n\n'
    'For y1 (c1 = 1): coefficients of y1 in rows (5),(6),(7): 2, 1, 1\n'
    '  => 2x1 + x2 + x3 <= 1\n\n'
    'For y2 (c2 = -1): coefficients of y2 in rows (5),(6),(7): 1, 1, 2\n'
    '  => x1 + x2 + 2x3 <= -1'
)

bold('DUAL PROBLEM:')
text(
    '  Max  z = 4x1 + x2 + 3x3\n'
    '  s.t.\n'
    '    2x1 + x2 +  x3 <= 1\n'
    '     x1 + x2 + 2x3 <= -1\n'
    '     x1, x2, x3 >= 0'
)
hr()

# =====================================================================
# QUESTION 1(iii)
# =====================================================================
pdf.add_page()
title('Question 1(iii)')
text(
    'Primal:\n'
    '  Max  z = 4x1 - x2 + 2x3\n'
    '  s.t.\n'
    '     x1 +  x2          <= 5   ...(9)\n'
    '    2x1 +  x2          <= 7   ...(10)\n'
    '          2x2 + x3 >= 6   ...(11)\n'
    '     x1        + x3 = 4   ...(12)\n'
    '     x1 >= 0;  x2, x3 unrestricted (urs)'
)

heading('Step 1: Assign dual variables')
text(
    'For a MAX primal, the sign of each dual variable depends on the constraint type:\n'
    '  Constraint (9)  is <=  =>  y1 >= 0\n'
    '  Constraint (10) is <=  =>  y2 >= 0\n'
    '  Constraint (11) is >=  =>  y3 <= 0\n'
    '  Constraint (12) is =   =>  y4 unrestricted (urs)'
)

heading('Step 2: Write the dual objective')
text('  MIN  w = 5y1 + 7y2 + 6y3 + 4y4')

heading('Step 3: Write dual constraints')
text(
    'The type of dual constraint depends on the primal variable sign:\n'
    '  xj >= 0  =>  dual constraint is >=\n'
    '  xj urs   =>  dual constraint is =\n\n'
    'For x1 (>= 0, c1 = 4): coefficients in rows (9),(10),(11),(12): 1, 2, 0, 1\n'
    '  => y1 + 2y2 + 0*y3 + y4 >= 4\n\n'
    'For x2 (urs, c2 = -1): coefficients in rows (9),(10),(11),(12): 1, 1, 2, 0\n'
    '  => y1 + y2 + 2y3 = -1\n\n'
    'For x3 (urs, c3 = 2): coefficients in rows (9),(10),(11),(12): 0, 0, 1, 1\n'
    '  => y3 + y4 = 2'
)

bold('DUAL PROBLEM:')
text(
    '  Min  w = 5y1 + 7y2 + 6y3 + 4y4\n'
    '  s.t.\n'
    '    y1 + 2y2         + y4  >= 4\n'
    '    y1 +  y2 + 2y3        =  -1\n'
    '                y3 + y4   =   2\n'
    '    y1, y2 >= 0;  y3 <= 0;  y4 urs'
)
hr()

# =====================================================================
# QUESTION 1(iv)
# =====================================================================
title('Question 1(iv)')
text(
    'Primal:\n'
    '  Min  w = 4y1 + 2y2 - y3\n'
    '  s.t.\n'
    '     y1 + 2y2          <= 6   ...(14)\n'
    '     y1 -  y2 + 2y3  =  8   ...(15)\n'
    '     y1 >= 0;  y2, y3 unrestricted (urs)'
)

heading('Step 1: Assign dual variables')
text(
    'Primal is MIN so dual is MAX. Dual variable sign depends on constraint type:\n'
    '  Constraint (14) is <=  =>  x1 <= 0\n'
    '  Constraint (15) is =   =>  x2 unrestricted (urs)'
)

heading('Step 2: Write the dual objective')
text('  MAX  z = 6x1 + 8x2')

heading('Step 3: Write dual constraints')
text(
    'Each primal variable yj generates one dual constraint:\n'
    '  yj >= 0  =>  constraint <= cj\n'
    '  yj urs   =>  constraint = cj\n\n'
    'For y1 (>= 0, c1 = 4): coefficients in rows (14),(15): 1, 1\n'
    '  => x1 + x2 <= 4\n\n'
    'For y2 (urs, c2 = 2): coefficients in rows (14),(15): 2, -1\n'
    '  => 2x1 - x2 = 2\n\n'
    'For y3 (urs, c3 = -1): coefficients in rows (14),(15): 0, 2\n'
    '  => 2x2 = -1'
)

bold('DUAL PROBLEM:')
text(
    '  Max  z = 6x1 + 8x2\n'
    '  s.t.\n'
    '     x1 + x2  <= 4\n'
    '    2x1 - x2  = 2\n'
    '         2x2  = -1\n'
    '     x1 <= 0;  x2 urs'
)
hr()

# =====================================================================
# QUESTION 2
# =====================================================================
pdf.add_page()
title('Question 2')
text(
    'Primal:\n'
    '  Max  z = 2x1 + 3x2 + 6x3\n'
    '  s.t.\n'
    '    x1       + x3 <= 3   ...(19)\n'
    '         x2 + x3 <= 5   ...(20)\n'
    '    x1, x2, x3 >= 0'
)

heading('Part (i): Construct the Dual')

heading('Step 1: Assign dual variables')
text(
    '  Constraint (19) is <=  =>  y1 >= 0\n'
    '  Constraint (20) is <=  =>  y2 >= 0'
)

heading('Step 2: Dual objective')
text('  MIN  w = 3y1 + 5y2')

heading('Step 3: Dual constraints')
text(
    'For x1 (c1 = 2): coefficients in (19),(20): 1, 0  =>  y1 >= 2\n'
    'For x2 (c2 = 3): coefficients in (19),(20): 0, 1  =>  y2 >= 3\n'
    'For x3 (c3 = 6): coefficients in (19),(20): 1, 1  =>  y1 + y2 >= 6'
)

bold('DUAL PROBLEM:')
text(
    '  Min  w = 3y1 + 5y2\n'
    '  s.t.\n'
    '    y1        >= 2\n'
    '         y2   >= 3\n'
    '    y1 + y2   >= 6\n'
    '    y1, y2 >= 0'
)

heading('Part (ii): Solve the Dual Graphically')

heading('Step 1: Identify constraint boundary lines in the y1-y2 plane')
text(
    'L1: y1 = 2         (vertical line; feasible region is to the right: y1 >= 2)\n'
    'L2: y2 = 3         (horizontal line; feasible region is above: y2 >= 3)\n'
    'L3: y1 + y2 = 6    (diagonal line; feasible region is above: y1+y2 >= 6)\n\n'
    'Note: if y1 >= 2 and y2 >= 3, then y1 + y2 >= 5, but we need >= 6.\n'
    'So constraint L3 is active near the lower-left part of the feasible region\n'
    'and is NOT redundant.'
)

heading('Step 2: Find the corner (extreme) points of the feasible region')
text(
    'Corner A: intersection of L1 (y1=2) and L3 (y1+y2=6):\n'
    '  y1 = 2,  2 + y2 = 6  =>  y2 = 4\n'
    '  => Corner A = (y1, y2) = (2, 4)\n\n'
    'Corner B: intersection of L2 (y2=3) and L3 (y1+y2=6):\n'
    '  y2 = 3,  y1 + 3 = 6  =>  y1 = 3\n'
    '  => Corner B = (y1, y2) = (3, 3)\n\n'
    'Beyond these two corners the feasible region continues to the upper-right\n'
    '(larger y1 and y2), but the objective MIN 3y1+5y2 increases in that direction,\n'
    'so the minimum must lie at one of these two corners.'
)

heading('Step 3: Evaluate the objective at each corner')
text(
    'Objective: w = 3y1 + 5y2\n\n'
    '  Corner A = (2, 4):  w = 3(2) + 5(4) = 6 + 20 = 26\n'
    '  Corner B = (3, 3):  w = 3(3) + 5(3) = 9 + 15 = 24\n\n'
    '  Minimum w = 24 occurs at Corner B = (3, 3).'
)

bold('DUAL OPTIMAL SOLUTION:')
text(
    '  y1* = 3,  y2* = 3,  w* = 24\n\n'
    'Shadow prices of the primal constraints:\n'
    '  Shadow price of constraint (19) [x1 + x3 <= 3]  =  y1* = 3\n'
    '  Shadow price of constraint (20) [x2 + x3 <= 5]  =  y2* = 3\n\n'
    'Interpretation: Each 1-unit increase in the RHS of constraint (19) or (20)\n'
    'increases the optimal primal profit by 3 units.\n\n'
    'Verification via Strong Duality:\n'
    '  Primal solution: x1=0, x2=2, x3=3\n'
    '  z = 2(0) + 3(2) + 6(3) = 0 + 6 + 18 = 24 = w*  [OK]'
)
hr()

# =====================================================================
# QUESTION 3
# =====================================================================
pdf.add_page()
title('Question 3')
text(
    'Primal:\n'
    '  Max  z = x1 + 2x2\n'
    '  s.t.\n'
    '    -x1 + x2  <= -2   ...(24)\n'
    '     4x1 + x2  <=  4   ...(25)\n'
    '     x1, x2 >= 0'
)

heading('Part (i): Show the primal has no feasible solution (graphically)')

heading('Step 1: Rewrite constraints in slope-intercept form')
text(
    'Constraint (24): -x1 + x2 <= -2  =>  x2 <= x1 - 2\n'
    'Constraint (25):  4x1 + x2 <=  4  =>  x2 <= 4 - 4x1\n'
    'Non-negativity:  x1 >= 0,  x2 >= 0'
)

heading('Step 2: Derive the implied lower bound on x1')
text(
    'From (24) and x2 >= 0:\n'
    '  0 <= x2 <= x1 - 2\n'
    '  This requires  x1 - 2 >= 0  =>  x1 >= 2'
)

heading('Step 3: Substitute x1 >= 2 into constraint (25)')
text(
    'From (25): x2 <= 4 - 4x1\n'
    'If x1 >= 2:  4 - 4x1 <= 4 - 4(2) = -4\n'
    '  So x2 <= -4\n\n'
    'But x2 >= 0 is required.  CONTRADICTION: x2 cannot be both >= 0 and <= -4.'
)

bold('CONCLUSION:')
text(
    'The primal feasible region is EMPTY. Graphically, constraint (24) with x2 >= 0\n'
    'forces x1 >= 2, but constraint (25) then forces x2 <= -4, which violates\n'
    'x2 >= 0. The two half-planes do not intersect in the first quadrant.\n'
    'The primal has NO FEASIBLE SOLUTION.'
)

heading('Part (ii): Construct the Dual')

heading('Step 1: Assign dual variables')
text(
    '  Constraint (24) is <=  =>  y1 >= 0\n'
    '  Constraint (25) is <=  =>  y2 >= 0'
)

heading('Step 2: Dual objective')
text('  MIN  w = -2y1 + 4y2')

heading('Step 3: Dual constraints')
text(
    'For x1 (c1 = 1): coefficients in (24),(25): -1, 4  =>  -y1 + 4y2 >= 1\n'
    'For x2 (c2 = 2): coefficients in (24),(25):  1, 1  =>   y1 +  y2 >= 2'
)

bold('DUAL PROBLEM:')
text(
    '  Min  w = -2y1 + 4y2\n'
    '  s.t.\n'
    '    -y1 + 4y2  >= 1\n'
    '     y1 +  y2  >= 2\n'
    '     y1, y2 >= 0'
)

heading('Part (iii): Show the dual is unbounded (graphically)')

heading('Step 1: Confirm the dual is feasible')
text(
    'Try (y1, y2) = (1, 1):\n'
    '  -1 + 4(1) = 3 >= 1  [OK]\n'
    '   1 + 1    = 2 >= 2  [OK]\n'
    '   y1, y2 >= 0  [OK]\n'
    'The dual is feasible. w = -2(1) + 4(1) = 2.'
)

heading('Step 2: Construct a direction along which w -> -infinity')
text(
    'Let y1 -> +inf and set y2 = (1 + y1)/4  (satisfying constraint (i) with equality).\n\n'
    'Evaluate the objective along this ray:\n'
    '  w = -2y1 + 4 * (1 + y1)/4\n'
    '    = -2y1 + 1 + y1\n'
    '    = -y1 + 1\n'
    '  As y1 -> +inf:  w -> -inf\n\n'
    'Check constraint (ii) along this ray:\n'
    '  y1 + y2 = y1 + (1+y1)/4 = (5y1 + 1)/4 -> +inf >= 2  [OK]\n\n'
    'Check y1, y2 >= 0: y2 = (1+y1)/4 > 0  [OK]\n\n'
    'All constraints remain satisfied as y1 -> +inf, yet w -> -inf.'
)

bold('CONCLUSION:')
text(
    'The dual is UNBOUNDED (w -> -infinity along the feasible ray y1->inf, y2=(1+y1)/4).\n\n'
    'This is consistent with LP Duality Theory:\n'
    '  Primal INFEASIBLE  =>  Dual is either INFEASIBLE or UNBOUNDED.\n'
    '  Here the dual is feasible but unbounded, confirming the primal\n'
    '  has no feasible solution.'
)
hr()

# =====================================================================
# QUESTION 4
# =====================================================================
pdf.add_page()
title('Question 4')
text(
    'Primal:\n'
    '  Max  z = 2x1 + 5x2 + 4x3\n'
    '  s.t.\n'
    '     x1 + 2x2 + 4x3 <= 10   ...(29)\n'
    '    3x1 + 3x2 + 2x3 <= 10   ...(30)\n'
    '     x1, x2, x3 >= 0'
)

heading('Part (i): Construct the Dual')

heading('Step 1: Assign dual variables')
text(
    '  Constraint (29) is <=  =>  y1 >= 0\n'
    '  Constraint (30) is <=  =>  y2 >= 0'
)

heading('Step 2: Dual objective')
text('  MIN  w = 10y1 + 10y2')

heading('Step 3: Dual constraints')
text(
    'For x1 (c1 = 2): coefficients in (29),(30): 1, 3  =>   y1 + 3y2 >= 2\n'
    'For x2 (c2 = 5): coefficients in (29),(30): 2, 3  =>  2y1 + 3y2 >= 5\n'
    'For x3 (c3 = 4): coefficients in (29),(30): 4, 2  =>  4y1 + 2y2 >= 4'
)

bold('DUAL PROBLEM:')
text(
    '  Min  w = 10y1 + 10y2\n'
    '  s.t.\n'
    '     y1 + 3y2  >= 2\n'
    '    2y1 + 3y2  >= 5\n'
    '    4y1 + 2y2  >= 4\n'
    '     y1, y2 >= 0'
)

heading('Part (ii): Weak Duality - Show Optimal Primal Value Cannot Exceed 25')

text(
    'Weak Duality Theorem states:\n'
    'For any primal feasible x and any dual feasible y:\n'
    '  z = c^T x  <=  b^T y = w\n\n'
    'Therefore, the optimal primal value z* <= value of ANY feasible dual solution.\n\n'
    'We find a feasible dual solution with w = 25.\n\n'
    'Try (y1, y2) = (2.5, 0):\n'
    '  Constraint 1:  y1 + 3y2 = 2.5 + 0 = 2.5 >= 2  [OK]\n'
    '  Constraint 2: 2y1 + 3y2 = 5.0 + 0 = 5.0 >= 5  [OK]\n'
    '  Constraint 3: 4y1 + 2y2 = 10.0 + 0 = 10  >= 4  [OK]\n'
    '  y1, y2 >= 0: 2.5 >= 0, 0 >= 0  [OK]\n\n'
    'This point (2.5, 0) is dual feasible.\n'
    'Dual objective value:  w = 10(2.5) + 10(0) = 25\n\n'
    'By Weak Duality:  z*  <=  w = 25\n'
    'Therefore, the optimal primal objective value cannot exceed 25.'
)

heading('Part (iii): Basic Solution with x2, x3 Basic; Complementary Slackness')

heading('Step 1: Set up the basis matrix B = [A2 | A3]')
text(
    'Non-basic variable: x1 = 0.\n'
    'Basis matrix formed from columns of x2 and x3 in the constraint matrix:\n\n'
    '  A2 = column of x2 = [2, 3]^T  (from constraints (29) and (30))\n'
    '  A3 = column of x3 = [4, 2]^T\n\n'
    '       | 2   4 |\n'
    '  B  = | 3   2 |\n\n'
    '  det(B) = (2)(2) - (4)(3) = 4 - 12 = -8'
)

heading('Step 2: Compute B_inverse')
text(
    'For a 2x2 matrix [[a, b], [c, d]]:\n'
    '  B_inv = (1/det) * [[d, -b], [-c, a]]\n\n'
    '  B_inv = (1 / -8) * [[ 2, -4], [-3,  2]]\n\n'
    '        = | -1/4    1/2 |\n'
    '          |  3/8   -1/4 |'
)

heading('Step 3: Compute basic variable values  x_B = B_inv * b,  where b = [10, 10]^T')
text(
    '  x2 = (-1/4)(10) + (1/2)(10) = -2.5 + 5.0 = 2.5\n'
    '  x3 = ( 3/8)(10) + (-1/4)(10) = 3.75 - 2.5 = 1.25\n\n'
    'Full primal basic solution:\n'
    '  x1 = 0,  x2 = 2.5,  x3 = 1.25\n\n'
    'Primal objective value:\n'
    '  z = 2(0) + 5(2.5) + 4(1.25) = 0 + 12.5 + 5.0 = 17.5'
)

heading('Step 4: Derive the dual solution  y* = c_B * B_inv')
text(
    'c_B = [c2, c3] = [5, 4]  (objective coefficients of the basic variables)\n\n'
    '  y1* = c_B * (column 1 of B_inv)\n'
    '       = 5(-1/4) + 4(3/8)\n'
    '       = -5/4 + 12/8 = -10/8 + 12/8 = 2/8 = 0.25\n\n'
    '  y2* = c_B * (column 2 of B_inv)\n'
    '       = 5(1/2) + 4(-1/4)\n'
    '       = 5/2 - 1 = 3/2 = 1.5\n\n'
    'Dual solution:  y1* = 0.25,  y2* = 1.5\n'
    'Dual objective: w = 10(0.25) + 10(1.5) = 2.5 + 15 = 17.5'
)

heading('Step 5: Check Complementary Slackness (CS) conditions')
text(
    'CS Condition A - Primal: y_i* * (primal slack of constraint i) = 0\n\n'
    '  Constraint (29): x1+2x2+4x3 = 0 + 5 + 5 = 10  =>  slack = 10-10 = 0\n'
    '    y1* = 0.25 > 0  and  slack = 0:   0.25 * 0 = 0  [OK]\n\n'
    '  Constraint (30): 3x1+3x2+2x3 = 0 + 7.5 + 2.5 = 10  =>  slack = 0\n'
    '    y2* = 1.5 > 0   and  slack = 0:   1.5 * 0 = 0  [OK]\n\n'
    'CS Condition B - Dual: x_j* * (dual slack of constraint j) = 0\n\n'
    '  Dual constraint for x1:  y1 + 3y2 >= 2\n'
    '    LHS = 0.25 + 3(1.5) = 0.25 + 4.5 = 4.75  =>  dual slack = 4.75 - 2 = 2.75\n'
    '    x1* = 0  =>  0 * 2.75 = 0  [OK]\n\n'
    '  Dual constraint for x2:  2y1 + 3y2 >= 5\n'
    '    LHS = 2(0.25) + 3(1.5) = 0.5 + 4.5 = 5.0  =>  dual slack = 5 - 5 = 0\n'
    '    x2* = 2.5 > 0  and  dual slack = 0:  2.5 * 0 = 0  [OK]\n\n'
    '  Dual constraint for x3:  4y1 + 2y2 >= 4\n'
    '    LHS = 4(0.25) + 2(1.5) = 1.0 + 3.0 = 4.0  =>  dual slack = 4 - 4 = 0\n'
    '    x3* = 1.25 > 0  and  dual slack = 0:  1.25 * 0 = 0  [OK]'
)

bold('CONCLUSION:')
text(
    'All complementary slackness conditions are satisfied.\n'
    'Since z = w = 17.5 (primal objective equals dual objective),\n'
    'by the Strong Duality Theorem, BOTH solutions are OPTIMAL:\n\n'
    '  Primal optimal: x1=0, x2=2.5, x3=1.25  =>  z* = 17.5\n'
    '  Dual optimal:   y1=0.25, y2=1.5          =>  w* = 17.5'
)
hr()

# =====================================================================
# QUESTION 5
# =====================================================================
pdf.add_page()
title('Question 5')
text(
    'LP:\n'
    '  Max  z = 3x1 + 7x2 + 5x3\n'
    '  s.t.\n'
    '     x1 + x2 + x3  <= 50    (Sugar capacity)\n'
    '    2x1 + 3x2 + x3  <= 100   (Chocolate capacity)\n'
    '     x1, x2, x3 >= 0\n\n'
    'Optimal basis: {x3, x2}  (ordered: x3 first, x2 second)\n\n'
    '         | 3/2   -1/2 |\n'
    '  B_inv = | -1/2   1/2 |'
)

heading('Part (i): Shadow prices for each constraint')

heading('Step 1: Identify basis columns and verify B_inv')
text(
    'The basis is ordered {x3, x2}. Reading the constraint matrix column by column:\n\n'
    '  A3 = column of x3 = [1, 1]^T  (coefficient 1 in sugar, 1 in chocolate)\n'
    '  A2 = column of x2 = [1, 3]^T  (coefficient 1 in sugar, 3 in chocolate)\n\n'
    '       | 1   1 |\n'
    '  B  = | 1   3 |\n\n'
    '  det(B) = (1)(3) - (1)(1) = 3 - 1 = 2\n\n'
    '  B_inv = (1/2) * [[ 3, -1], [-1, 1]] = [[ 3/2, -1/2], [-1/2, 1/2]]\n\n'
    '  This matches the given B_inv.  [OK]'
)

heading('Step 2: Compute shadow prices  y* = c_B * B_inv')
text(
    'c_B = [c3, c2] = [5, 7]  (objective coefficients in basis order x3, x2)\n\n'
    'Shadow price of the Sugar constraint (y1*):\n'
    '  y1* = c_B * (column 1 of B_inv)\n'
    '       = 5(3/2) + 7(-1/2)\n'
    '       = 15/2 - 7/2 = 8/2 = 4\n\n'
    'Shadow price of the Chocolate constraint (y2*):\n'
    '  y2* = c_B * (column 2 of B_inv)\n'
    '       = 5(-1/2) + 7(1/2)\n'
    '       = -5/2 + 7/2 = 2/2 = 1'
)

bold('SHADOW PRICES:')
text(
    '  y1* = 4 cents per oz  (Sugar)\n'
    '  y2* = 1 cent  per oz  (Chocolate)\n\n'
    'Interpretation:\n'
    '  Sugar (y1* = 4):  Each additional 1 oz of sugar beyond the current 50 oz\n'
    '  limit increases the company\'s optimal total profit by 4 cents, at the\n'
    '  current optimal basis. Sugar is the more valuable resource here.\n\n'
    '  Chocolate (y2* = 1):  Each additional 1 oz of chocolate beyond the\n'
    '  current 100 oz limit increases total profit by 1 cent at the current\n'
    '  optimal basis. Chocolate is less binding than sugar at the optimum.\n\n'
    '  Note: These shadow prices are valid only while the current basis remains\n'
    '  optimal (within the allowable range of RHS changes).'
)

heading('Part (ii): Maximum willingness-to-pay for 1 extra oz of Sugar')
text(
    'The shadow price y1* = 4 is the marginal value of one additional oz of sugar.\n'
    'If the company pays a price P per extra oz of sugar, the net gain is:\n\n'
    '  Net gain = marginal value - cost = 4 - P\n\n'
    'The company is willing to pay as long as it does not lose money:\n'
    '  4 - P >= 0  =>  P <= 4\n\n'
    'At P = 4 the company breaks even; at P > 4 it loses money.'
)

bold('ANSWER:')
text('  Maximum willingness-to-pay for 1 extra oz of Sugar = 4 cents per oz.')

heading('Part (iii): Maximum willingness-to-pay for 1 extra oz of Chocolate')
text(
    'The shadow price y2* = 1 is the marginal value of one additional oz of chocolate.\n'
    'If the company pays a price P per extra oz of chocolate, the net gain is:\n\n'
    '  Net gain = 1 - P\n\n'
    'The company is willing to pay as long as:\n'
    '  1 - P >= 0  =>  P <= 1'
)

bold('ANSWER:')
text('  Maximum willingness-to-pay for 1 extra oz of Chocolate = 1 cent per oz.')

# =====================================================================
# OUTPUT
# =====================================================================
out = 'homework/SSIE553_Homework5_Lana_Jalal_Gidan.pdf'
pdf.output(out)
print(f'Saved: {out}')

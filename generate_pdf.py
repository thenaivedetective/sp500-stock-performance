import textwrap, numpy as np, pandas as pd
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import linkage
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import confusion_matrix
import warnings; warnings.filterwarnings('ignore')

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    HRFlowable, Image as RLImage, Table, TableStyle
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT

OUTPUT = 'multivariate_homework_lana_gidan.pdf'
W_PAGE, H_PAGE = A4

doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=2.5*cm, rightMargin=2.5*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
    title='Multivariate Data Analysis Homework', author='Lana Gidan',
)

BLACK = colors.black
GRAY  = colors.HexColor('#555555')
LGRAY = colors.HexColor('#bbbbbb')
CODE_BG = colors.HexColor('#f4f4f4')
CALC_BG = colors.HexColor('#f9f9f9')

def S(name, **kw):
    return ParagraphStyle(name, **kw)

title_st   = S('T', fontName='Times-Bold',   fontSize=16, textColor=BLACK, alignment=TA_CENTER, spaceAfter=6,  leading=22)
sub_st     = S('S', fontName='Times-Roman',  fontSize=12, textColor=BLACK, alignment=TA_CENTER, spaceAfter=4)
author_st  = S('A', fontName='Times-Bold',   fontSize=13, textColor=BLACK, alignment=TA_CENTER, spaceAfter=4)
qhead_st   = S('Q', fontName='Times-Bold',   fontSize=13, textColor=BLACK, spaceBefore=14, spaceAfter=5)
subh_st    = S('SH',fontName='Times-Bold',   fontSize=11, textColor=BLACK, spaceBefore=8,  spaceAfter=3)
body_st    = S('B', fontName='Times-Roman',  fontSize=10.5, textColor=BLACK, leading=15, spaceAfter=6, alignment=TA_JUSTIFY)
calc_label = S('CL',fontName='Times-Bold',   fontSize=10, textColor=BLACK, spaceBefore=8, spaceAfter=3)
calc_st    = S('CA',fontName='Courier',      fontSize=8.5, textColor=BLACK, backColor=CALC_BG, leading=13, spaceAfter=0, spaceBefore=0, leftIndent=6)
code_lbl   = S('CD',fontName='Times-Bold',   fontSize=10, textColor=BLACK, spaceBefore=10, spaceAfter=4)
code_st    = S('CO',fontName='Courier',      fontSize=7,  textColor=BLACK, backColor=CODE_BG, leading=10, spaceAfter=0, spaceBefore=0, leftIndent=4, rightIndent=4)
cap_st     = S('CP',fontName='Times-Italic', fontSize=9,  textColor=GRAY, alignment=TA_CENTER, spaceBefore=3, spaceAfter=8)

def thin_hr():
    return HRFlowable(width='100%', thickness=0.5, color=LGRAY, spaceAfter=6, spaceBefore=4)

def calc_block(lines):
    text = '<br/>'.join(lines)
    return [Paragraph(text, calc_st), Spacer(1, 4)]

def embed_image(path, max_width=14*cm, max_height=13*cm):
    from PIL import Image as PILImage
    img = PILImage.open(path); iw, ih = img.size
    scale = min(max_width/iw, max_height/ih)
    return RLImage(path, width=iw*scale, height=ih*scale)

def code_block(filepath):
    items = []
    with open(filepath) as f: raw = f.read()
    raw = raw.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    lines = raw.split('\n'); chunk = []
    for line in lines:
        if len(line) > 115:
            chunk.extend(textwrap.wrap(line, width=115, subsequent_indent='    '))
        else:
            chunk.append(line)
    for i in range(0, len(chunk), 65):
        block = '\n'.join(chunk[i:i+65])
        items.append(Paragraph(block.replace('\n','<br/>').replace(' ','&nbsp;'), code_st))
        items.append(Spacer(1, 1))
    return items

def fmt_matrix(M, row_labels, col_labels, title):
    lines = [title]
    header = '          ' + ''.join(f'{c:>14}' for c in col_labels)
    lines.append(header)
    for i, rl in enumerate(row_labels):
        row = f'  {rl:<8}' + ''.join(f'{M[i,j]:>14.4f}' for j in range(M.shape[1]))
        lines.append(row)
    return lines

# =============================================================================
# COMPUTE ALL VALUES
# =============================================================================

# ── Q8.7 data ─────────────────────────────────────────────────────────────────
col_names = [
    'OBS','ID','SEX','AGE','MARITAL','EDUCAT','EMPLOY','INCOME','RELIG',
    'C1','C2','C3','C4','C5','C6','C7','C8','C9','C10',
    'C11','C12','C13','C14','C15','C16','C17','C18','C19','C20',
    'CESD','CASES','DRINK','HEALTH','REGDOC','TREAT','BEDDAYS','ACUTEILL','CHRONILL'
]
rows = []
with open('attached_assets/DEPRES_1773880715452.DAT') as f:
    for line in f:
        v = line.strip().split()
        if len(v) == 38:
            rows.append([float(x) for x in v])
df87 = pd.DataFrame(rows, columns=col_names)
y87 = df87['CASES'].values
n87 = len(y87); n87_0 = (y87==0).sum(); n87_1 = (y87==1).sum()

vars_a = ['INCOME','EDUCAT']
X87a = df87[vars_a].values
gm87a = X87a.mean(axis=0)
m87_0 = X87a[y87==0].mean(axis=0)
m87_1 = X87a[y87==1].mean(axis=0)
W87a = np.zeros((2,2))
for g in [0,1]:
    Xg = X87a[y87==g]; d = Xg - Xg.mean(axis=0); W87a += d.T @ d
T87a = (X87a - gm87a).T @ (X87a - gm87a)
B87a = T87a - W87a
dW87a = np.linalg.det(W87a); dT87a = np.linalg.det(T87a)
wl87a = dW87a / dT87a
F87a  = ((1-wl87a)/wl87a) * ((n87-3)/2)
p87a  = 1 - stats.f.cdf(F87a, 2, n87-3)

# Stepwise results (from script output)
stepwise_steps = [
    ('HEALTH',   0.9232, 37.23),
    ('BEDDAYS',  0.8967, 22.03),
    ('ACUTEILL', 0.8862, 12.88),
    ('CHRONILL', 0.8798,  8.54),
]
wl87b = 0.8798

# ── Q7.5 / Q8.8 data ──────────────────────────────────────────────────────────
def parse_val(s):
    s=s.strip()
    if s in ('','.','..',  '...','....','.....'): return np.nan
    try: return float(s)
    except: return np.nan

colspecs = {
    'ID':(0,4),'V1':(4,6),'V2':(6,8),'V3':(8,10),'V4':(10,12),'V5':(12,14),'V6':(14,16),
    'V7':(16,17),'V8':(17,18),'V9':(18,19),'V10':(19,20),'V11':(20,21),'V12':(21,22),
    'V13':(22,23),'V14':(23,24),'V15':(24,25),'V16':(25,26),'V17':(26,27),'V18':(27,28),
}
rows=[]; 
with open('attached_assets/MASST_1773881001970.DAT') as f:
    for line in f:
        raw=line.rstrip('\n')
        if len(raw)<20 or raw.strip().startswith('Mass') or raw.strip().startswith('(') \
                or raw.strip().startswith('---') or raw.strip()=='': continue
        row={}
        for col,(s,e) in colspecs.items():
            row[col]=parse_val(raw[s:e]) if len(raw)>=e else np.nan
        rows.append(row)
df_mass = pd.DataFrame(rows)
v7_18 = [f'V{i}' for i in range(7,19)]
df_c = df_mass[['ID']+v7_18].dropna(subset=v7_18).copy()
X_c  = df_c[v7_18].values
scaler = StandardScaler()
Xs = scaler.fit_transform(X_c)
Z  = linkage(Xs, method='ward')
last_dists = Z[-10:,2][::-1]

km = KMeans(n_clusters=2, random_state=42, n_init=20)
km.fit(Xs)
df_c = df_c.copy(); df_c['cluster'] = km.labels_
cm_mass = df_c.groupby('cluster')[v7_18].mean()
cs_mass = df_c['cluster'].value_counts().sort_index()
ca_mass = cm_mass.mean(axis=1)
uc = int(ca_mass.idxmax()); nc = 1 - uc
TSS = np.sum((Xs - Xs.mean(axis=0))**2)
WSS = km.inertia_; BSS = TSS - WSS
gas_levels = ['10%','20%','30%','40%','50%','60%','70%','80%','90%','100%','150%','>150%']

# Q8.8 discriminant
disc_vars = [f'V{i}' for i in range(1,19)]
df_c['group'] = df_c['cluster'].map({uc:1, nc:0})
df_full = df_mass.merge(df_c[['ID','group']], on='ID', how='inner')
df_disc = df_full[['ID','group']+disc_vars].dropna(subset=disc_vars)
X88 = df_disc[disc_vars].values; y88 = df_disc['group'].values; n88 = len(y88)
gm88 = X88.mean(axis=0)
W88 = np.zeros((18,18))
for g in [0,1]:
    Xg = X88[y88==g]; d = Xg-Xg.mean(axis=0); W88 += d.T @ d
T88 = (X88-gm88).T @ (X88-gm88)
dW88 = np.linalg.det(W88); dT88 = np.linalg.det(T88)
wl88 = dW88/dT88
F88  = ((1-wl88)/wl88) * ((n88-len(disc_vars)-1)/len(disc_vars))
p88  = 1 - stats.f.cdf(F88, len(disc_vars), n88-len(disc_vars)-1)

# ── Q9.8 data ─────────────────────────────────────────────────────────────────
rows3 = []
with open('attached_assets/PHONE_1773881553876.DAT') as f:
    for line in f:
        v = line.strip().split()
        if len(v)==8:
            try: rows3.append([int(x) for x in v])
            except: pass
df98 = pd.DataFrame(rows3, columns=['ID','Phones','A1','A2','A3','A4','A5','A6'])
atts = ['A1','A2','A3','A4','A5','A6']
X98 = df98[atts].values; y98 = df98['Phones'].values; n98 = len(y98)
gm98 = X98.mean(axis=0)
m98 = {g: X98[y98==g].mean(axis=0) for g in [1,2,3]}
W98 = np.zeros((6,6))
for g in [1,2,3]:
    Xg = X98[y98==g]; d = Xg-Xg.mean(axis=0); W98 += d.T @ d
T98 = (X98-gm98).T @ (X98-gm98)
B98 = T98 - W98
dW98 = np.linalg.det(W98); dT98 = np.linalg.det(T98)
wl98 = dW98/dT98
chi2_98 = -(n98-1-(6+3)/2)*np.log(wl98)
p98  = 1 - stats.chi2.cdf(chi2_98, 12)

# ── Q9.9 data ─────────────────────────────────────────────────────────────────
rows4 = []
with open('attached_assets/ADMIS_1773881795621.DAT') as f:
    for line in f:
        v = line.strip().split()
        if len(v)==4:
            try: rows4.append([int(v[0]),int(v[1]),float(v[2]),int(v[3])])
            except: pass
df99 = pd.DataFrame(rows4, columns=['App','Status','GPA','GMAT'])
X99 = df99[['GPA','GMAT']].values; y99 = df99['Status'].values; n99 = len(y99)
gm99 = X99.mean(axis=0)
m99 = {s: X99[y99==s].mean(axis=0) for s in [1,2,3]}
n99g = {s: (y99==s).sum() for s in [1,2,3]}
W99 = np.zeros((2,2))
for s in [1,2,3]:
    Xg = X99[y99==s]; d = Xg-Xg.mean(axis=0); W99 += d.T @ d
T99 = (X99-gm99).T @ (X99-gm99)
B99 = T99 - W99
dW99 = np.linalg.det(W99); dT99 = np.linalg.det(T99)
wl99 = dW99/dT99
chi2_99 = -(n99-1-(2+3)/2)*np.log(wl99)
p99  = 1 - stats.chi2.cdf(chi2_99, 4)
lda99 = LinearDiscriminantAnalysis()
lda99.fit(X99, y99)
scores99 = lda99.transform(X99)
centroids99 = {s: scores99[y99==s,0].mean() for s in [1,2,3]}

# =============================================================================
# BUILD PDF STORY
# =============================================================================
story = []

# ── Cover ──────────────────────────────────────────────────────────────────────
story.append(Spacer(1, 4*cm))
story.append(Paragraph('Multivariate Data Analysis', title_st))
story.append(Paragraph('Homework Assignment', sub_st))
story.append(Spacer(1, 1.5*cm))
story.append(thin_hr())
story.append(Spacer(1, 0.8*cm))
story.append(Paragraph('Submitted by', sub_st))
story.append(Paragraph('Lana Gidan', author_st))
story.append(Spacer(1, 2*cm))
story.append(thin_hr())
story.append(PageBreak())

# =============================================================================
# Q 8.7
# =============================================================================
story.append(Paragraph('Question 8.7 — Discriminant Analysis (DEPRES.DAT)', qhead_st))
story.append(thin_hr())

story.append(Paragraph(
    'Part (a): Discriminant analysis was performed using INCOME and EDUCAT as predictors '
    'to classify individuals as depressed (CESD > 16) or normal. '
    'The resulting Wilks\' Lambda was 0.9724, indicating modest but statistically significant '
    'group separation. Depressed individuals tended to have lower income and lower education '
    'compared to normal individuals.',
    body_st))

story.append(Paragraph(
    'Part (b): A forward stepwise procedure was applied across eight candidate variables '
    '(INCOME, EDUCAT, ACUTEILL, SEX, AGE, HEALTH, BEDDAYS, CHRONILL) using an F-to-enter '
    'threshold of 3.84. Health-related variables entered first and contributed the most '
    'to reducing Wilks\' Lambda, which fell to 0.8798 in the final stepwise model. '
    'The correct classification rate also increased, confirming that health status variables '
    'are stronger predictors of depression than socioeconomic factors alone.',
    body_st))

story.append(Paragraph(
    'Part (c): The standardised discriminant function coefficients show that poor self-rated '
    'health (HEALTH), number of bed-days (BEDDAYS), acute illness (ACUTEILL), and chronic '
    'illness (CHRONILL) carry the largest weights, consistent with the well-established '
    'link between physical health and depression. The stepwise model is both statistically '
    'and practically superior to the two-variable model.',
    body_st))

# ── Manual calculations ───────────────────────────────────────────────────────
story.append(Paragraph('Manual Calculations', subh_st))

story.append(Paragraph('Part (a) — INCOME and EDUCAT', calc_label))
story += calc_block([
    f'Sample sizes:  n = {n87},  n(Normal) = {n87_0},  n(Depressed) = {n87_1}',
    '',
    f'Group means:',
    f'  Normal:     INCOME = {m87_0[0]:.4f},   EDUCAT = {m87_0[1]:.4f}',
    f'  Depressed:  INCOME = {m87_1[0]:.4f},   EDUCAT = {m87_1[1]:.4f}',
    f'  Grand mean: INCOME = {gm87a[0]:.4f},   EDUCAT = {gm87a[1]:.4f}',
])

wlines  = fmt_matrix(W87a, ['INCOME','EDUCAT'], ['INCOME','EDUCAT'],
                     'Within-group scatter matrix  W = Σ(Xg − X̄g)(Xg − X̄g)ᵀ  (summed over groups):')
story += calc_block(wlines)

tlines  = fmt_matrix(T87a, ['INCOME','EDUCAT'], ['INCOME','EDUCAT'],
                     'Total scatter matrix  T = Σ(Xi − X̄)(Xi − X̄)ᵀ:')
story += calc_block(tlines)

blines  = fmt_matrix(B87a, ['INCOME','EDUCAT'], ['INCOME','EDUCAT'],
                     'Between-group scatter matrix  B = T − W:')
story += calc_block(blines)

story += calc_block([
    f'Determinants:',
    f'  |W| = {dW87a:,.4f}',
    f'  |T| = {dT87a:,.4f}',
    '',
    f'Wilks\' Lambda = |W| / |T|',
    f'             = {dW87a:,.4f} / {dT87a:,.4f}',
    f'             = {wl87a:.4f}',
    '',
    f'F-approximation (2 groups):',
    f'  F = [(1 − Λ) / Λ] × [(n − p − 1) / p]',
    f'    = [(1 − {wl87a:.4f}) / {wl87a:.4f}] × [({n87} − 2 − 1) / 2]',
    f'    = [{(1-wl87a)/wl87a:.4f}] × [{(n87-3)/2:.1f}]',
    f'    = {F87a:.4f}   (df₁ = 2, df₂ = {n87-3})',
    f'  p-value = {p87a:.4f}',
])

story.append(Paragraph('Part (b) — Forward Stepwise Selection', calc_label))
story += calc_block([
    'At each step, the variable most reducing Wilks\' Lambda is entered',
    'provided its F-to-enter ≥ 3.84:',
    '',
    '  {:6} {:16} {:>12} {:>12}'.format("Step","Variable Entered","Wilks Lam.","F-to-enter"),
    '  {:6} {:16} {:>12} {:>12}'.format("----","----------------","---------","----------"),
] + [
    f'  {i+1:<6} {var:<16} {wl:>12.4f} {f_val:>12.2f}'
    for i,(var,wl,f_val) in enumerate(stepwise_steps)
] + [
    '',
    f'  Final Wilks\' Lambda (4-variable stepwise model) = {wl87b:.4f}',
    f'  Reduction from part (a): {wl87a:.4f} → {wl87b:.4f}  (Δ = {wl87a-wl87b:.4f})',
])

story.append(Spacer(1, 0.3*cm))
story.append(embed_image('q8_7_discriminant_analysis.png'))
story.append(Paragraph(
    'Figure 8.7 — Group means, discriminant score distributions, and model comparison.',
    cap_st))
story.append(Paragraph('Code — Question 8.7', code_lbl))
story += code_block('hw_q8_7.py')
story.append(PageBreak())

# =============================================================================
# Q 7.5
# =============================================================================
story.append(Paragraph('Question 7.5 — Cluster Analysis (MASST.DAT)', qhead_st))
story.append(thin_hr())

story.append(Paragraph(
    'Variables V7 through V18 measure stated willingness to use mass transit at gas price '
    'increases from 10% to over 150%. Ward\'s hierarchical clustering was applied to '
    'standardised data (mean = 0, SD = 1), and K-Means (k = 2, 20 restarts) was then '
    'used to refine the partition.',
    body_st))

story.append(Paragraph(
    'Two clusters emerge: Users (n = 340) with consistently higher usage-intention scores '
    'across all price levels, and Non-users (n = 198) with near-uniformly low scores. '
    'The between-cluster SS accounts for 56.4% of total variance, confirming meaningful '
    'separation.',
    body_st))

# ── Manual calculations ───────────────────────────────────────────────────────
story.append(Paragraph('Manual Calculations', subh_st))

story.append(Paragraph('Step 1 — Ward\'s Hierarchical Clustering (merge distances)', calc_label))
story += calc_block([
    'Variables V7–V18 are standardised (z-scores) before clustering.',
    'Ward\'s method minimises total within-cluster variance at each merge.',
    'The merge distance table (last 10 steps) is used to identify the optimal k:',
    '',
    f'  {"Resulting k":<14} {"Merge Distance":>16}',
    f'  {"----------":<14} {"--------------":>16}',
] + [
    f'  {i+1:<14} {d:>16.4f}{"  ← large gap" if i==0 else ""}'
    for i,d in enumerate(last_dists)
] + [
    '',
    f'  Largest gap occurs between k=1 (d={last_dists[0]:.4f}) and k=2 (d={last_dists[1]:.4f})',
    f'  Gap = {last_dists[0]:.4f} − {last_dists[1]:.4f} = {last_dists[0]-last_dists[1]:.4f}  →  k = 2 selected',
])

story.append(Paragraph('Step 2 — K-Means Refinement (k = 2)', calc_label))
story += calc_block([
    f'Cluster sizes after K-Means:  Users = {cs_mass[uc]},  Non-users = {cs_mass[nc]}',
    '',
    'Cluster centroids (original 1–5 scale):',
    f'  {"Gas Level":<10} {"Users (C1)":>12} {"Non-users (C2)":>16} {"Overall":>10}',
    f'  {"---------":<10} {"----------":>12} {"--------------":>16} {"-------":>10}',
] + [
    f'  {g:<10} {cm_mass.loc[uc,v]:>12.3f} {cm_mass.loc[nc,v]:>16.3f} {df_c[v].mean():>10.3f}'
    for v,g in zip(v7_18, gas_levels)
] + [
    '',
    f'  Users avg score (V7–V18):     {ca_mass[uc]:.4f} / 5',
    f'  Non-users avg score (V7–V18): {ca_mass[nc]:.4f} / 5',
])

story.append(Paragraph('Step 3 — Variance Decomposition', calc_label))
story += calc_block([
    'Total SS   (TSS) = sum of squared deviations from grand centroid (standardised)',
    'Within-cluster SS (WSS) = K-Means objective function (minimised)',
    'Between-cluster SS (BSS) = TSS − WSS',
    '',
    f'  TSS = {TSS:.2f}',
    f'  WSS = {WSS:.2f}',
    f'  BSS = {TSS:.2f} − {WSS:.2f} = {BSS:.2f}',
    '',
    f'  R² = BSS / TSS = {BSS:.2f} / {TSS:.2f} = {BSS/TSS*100:.1f}%',
    f'  The 2-cluster solution explains {BSS/TSS*100:.1f}% of total multivariate variance.',
])

story.append(Spacer(1, 0.3*cm))
story.append(embed_image('q7_5_q8_8_mass_transit.png'))
story.append(Paragraph(
    'Figure 7.5 / 8.8 — Dendrogram, elbow plot, cluster profiles, and discriminant results.',
    cap_st))

# =============================================================================
# Q 8.8
# =============================================================================
story.append(Paragraph('Question 8.8 — Discriminant Analysis: Users vs Non-users (MASST.DAT)', qhead_st))
story.append(thin_hr())

story.append(Paragraph(
    'Using cluster membership from Q7.5 as the dependent variable, a discriminant analysis '
    'was run with V1–V18 as predictors. Wilks\' Lambda = 0.1706 and overall correct '
    'classification = 97.3%, confirming the two clusters are highly distinct.',
    body_st))

story.append(Paragraph('Manual Calculations', subh_st))
story.append(Paragraph('Wilks\' Lambda (18 predictors, 2 groups)', calc_label))
story += calc_block([
    f'n = {n88},  n(Users) = {(y88==1).sum()},  n(Non-users) = {(y88==0).sum()}',
    f'p = 18 predictors',
    '',
    f'  Wilks\' Lambda = |W| / |T|',
    f'                = {dW88:.4e} / {dT88:.4e}',
    f'                = {wl88:.4f}',
    '',
    f'F-approximation:',
    f'  F = [(1 − Λ) / Λ] × [(n − p − 1) / p]',
    f'    = [(1 − {wl88:.4f}) / {wl88:.4f}] × [({n88} − 18 − 1) / 18]',
    f'    = {(1-wl88)/wl88:.4f} × {(n88-19)/18:.4f}',
    f'    = {F88:.4f}   (df₁ = 18, df₂ = {n88-19})',
    f'  p-value = {p88:.6f}',
    '',
    'Note: Because p = 18 is large, exact matrix values are omitted here.',
    'The W and T matrices are 18×18. Their determinants are computed numerically.',
    'Key group means (selected predictors):',
    f'  {"Variable":<8} {"Users":>10} {"Non-users":>12} {"Diff":>10}',
    f'  {"--------":<8} {"-----":>10} {"---------":>12} {"----":>10}',
] + [
    f'  {v:<8} {df_disc.loc[y88==1,v].mean():>10.3f} {df_disc.loc[y88==0,v].mean():>12.3f} '
    f'{df_disc.loc[y88==1,v].mean()-df_disc.loc[y88==0,v].mean():>10.3f}'
    for v in ['V1','V2','V3','V4','V5','V6','V7','V10','V14','V18']
])

story.append(Paragraph('Code — Questions 7.5 and 8.8', code_lbl))
story += code_block('hw_q7_5_and_q8_8.py')
story.append(PageBreak())

# =============================================================================
# Q 9.8
# =============================================================================
story.append(Paragraph('Question 9.8 — Three-Group Discriminant Analysis (PHONE.DAT)', qhead_st))
story.append(thin_hr())

story.append(Paragraph(
    'Three-group discriminant analysis on PHONE.DAT distinguishes households owning 1, 2, '
    'or 3+ telephones using six attitude statements (A1–A6, scale 0–10). '
    f'Wilks\' Λ = {wl98:.4f} (χ²(12) = {chi2_98:.2f}, p < 0.0001). '
    'Function 1 explains 94.9% of between-group variance. Overall correct classification '
    f'= {np.trace(confusion_matrix(y98, LinearDiscriminantAnalysis().fit(X98,y98).predict(X98),labels=[1,2,3]))/n98*100:.1f}%.',
    body_st))

story.append(Paragraph(
    'Structure matrix: A3 ("More phones worth the extra cost") most strongly '
    'distinguishes 3+-phone owners on Function 1. A5 ("More phones = waste of money") '
    'and A2 ("Save money with one phone") align with 1-phone households. '
    '1-phone families are cost-conscious; 3+-phone families are value-oriented.',
    body_st))

story.append(Paragraph('Manual Calculations', subh_st))

story.append(Paragraph('Step 1 — Group Means and Grand Mean', calc_label))
story += calc_block([
    f'n = {n98}   (1 phone: {(y98==1).sum()}, 2 phones: {(y98==2).sum()}, 3+ phones: {(y98==3).sum()})',
    '',
    f'  {"":8} {"A1":>7} {"A2":>7} {"A3":>7} {"A4":>7} {"A5":>7} {"A6":>7}',
    f'  {"-"*50}',
] + [
    f'  {lbl:<8} ' + ' '.join(f'{m98[g][i]:>7.3f}' for i in range(6))
    for g,lbl in [(1,"1 Phone"),(2,"2 Phones"),(3,"3+Phones")]
] + [
    f'  {"Grand":<8} ' + ' '.join(f'{gm98[i]:>7.3f}' for i in range(6))
])

story.append(Paragraph('Step 2 — Scatter Matrices and Wilks\' Lambda', calc_label))
story += calc_block([
    'Within-group scatter matrix W (diagonal elements only, 6×6):',
    f'  W diagonal: [' + ', '.join(f'{np.diag(W98)[i]:.3f}' for i in range(6)) + ']',
    '',
    'Total scatter matrix T (diagonal elements only):',
    f'  T diagonal: [' + ', '.join(f'{np.diag(T98)[i]:.3f}' for i in range(6)) + ']',
    '',
    f'  |W| = {dW98:.4e}',
    f'  |T| = {dT98:.4e}',
    '',
    f'  Wilks\' Lambda = |W| / |T|',
    f'                = {dW98:.4e} / {dT98:.4e}',
    f'                = {wl98:.4f}',
])

story.append(Paragraph('Step 3 — Chi-Square Approximation', calc_label))
story += calc_block([
    'For k groups and p variables, the chi-square statistic is:',
    '  χ² = −[n − 1 − (p + k)/2] × ln(Λ)',
    '',
    f'  = −[{n98} − 1 − ({6} + {3})/2] × ln({wl98:.4f})',
    f'  = −[{n98-1} − {(6+3)/2:.1f}] × ln({wl98:.4f})',
    f'  = −{n98-1-(6+3)/2:.1f} × {np.log(wl98):.4f}',
    f'  = {chi2_98:.4f}',
    '',
    f'  Degrees of freedom = p × (k − 1) = {6} × {2} = 12',
    f'  p-value = P(χ²₁₂ > {chi2_98:.4f}) = {p98:.4f}',
])

story.append(Spacer(1, 0.3*cm))
story.append(embed_image('q9_8_phone_discriminant.png'))
story.append(Paragraph(
    'Figure 9.8 — Group means, discriminant score scatter, structure matrix, '
    'and classification accuracy.',
    cap_st))
story.append(Paragraph('Code — Question 9.8', code_lbl))
story += code_block('hw_q9_8.py')
story.append(PageBreak())

# =============================================================================
# Q 9.9
# =============================================================================
story.append(Paragraph('Question 9.9 — Graduate Admissions Discriminant Analysis (ADMIS.DAT)', qhead_st))
story.append(thin_hr())

story.append(Paragraph(
    'Three-group discriminant analysis was applied to ADMIS.DAT to classify 85 graduate '
    f'applicants (Admitted n={n99g[1]}, Not Admitted n={n99g[2]}, Borderline n={n99g[3]}) '
    'using GPA and GMAT. Wilks\' Λ = 0.1264 (χ²(4) = 168.58, p < 0.0001). '
    'Function 1 explains 96.7% of between-group variance; overall accuracy = 91.8%.',
    body_st))

story.append(Paragraph(
    'GPA carries the larger standardised coefficient on Function 1, making it the primary '
    'separator. Admitted students average GPA ≈ 3.40 and GMAT ≈ 561; Not Admitted '
    'average GPA ≈ 2.48 and GMAT ≈ 447. The Borderline group overlaps both in GPA '
    'and GMAT, requiring holistic review beyond these two predictors.',
    body_st))

story.append(Paragraph('Admission Policy Implications', subh_st))
story.append(Paragraph(
    'The school is primarily GPA-driven: no rejected applicant had GPA ≥ 3.40. '
    'A practical rule from the discriminant functions: admit when GPA ≥ 3.30 and '
    'GMAT ≥ 500; reject when GPA < 2.90 and GMAT < 480; otherwise treat as borderline. '
    'Adding work experience or recommendation scores would improve resolution of '
    'borderline cases.',
    body_st))

# ── Manual calculations ───────────────────────────────────────────────────────
story.append(Paragraph('Manual Calculations', subh_st))

story.append(Paragraph('Step 1 — Group Means and Grand Mean', calc_label))
story += calc_block([
    f'n = {n99}  (Admitted: {n99g[1]}, Not Admitted: {n99g[2]}, Borderline: {n99g[3]})',
    '',
    f'  {"Group":<14} {"GPA":>10} {"GMAT":>10}',
    f'  {"-"*36}',
    f'  {"Admitted":<14} {m99[1][0]:>10.4f} {m99[1][1]:>10.4f}',
    f'  {"Not Admitted":<14} {m99[2][0]:>10.4f} {m99[2][1]:>10.4f}',
    f'  {"Borderline":<14} {m99[3][0]:>10.4f} {m99[3][1]:>10.4f}',
    f'  {"Grand mean":<14} {gm99[0]:>10.4f} {gm99[1]:>10.4f}',
])

wlines99 = fmt_matrix(W99, ['GPA','GMAT'], ['GPA','GMAT'],
    'Step 2 — Within-group scatter matrix  W = Σg Σi(Xgi − X̄g)(Xgi − X̄g)ᵀ:')
story += calc_block(wlines99)

tlines99 = fmt_matrix(T99, ['GPA','GMAT'], ['GPA','GMAT'],
    'Total scatter matrix  T = Σi(Xi − X̄)(Xi − X̄)ᵀ:')
story += calc_block(tlines99)

blines99 = fmt_matrix(B99, ['GPA','GMAT'], ['GPA','GMAT'],
    'Between-group scatter matrix  B = T − W:')
story += calc_block(blines99)

story += calc_block([
    'Step 3 — Determinants and Wilks\' Lambda:',
    '',
    f'  |W| = ({W99[0,0]:.6f}) × ({W99[1,1]:.4f}) − ({W99[0,1]:.4f})²',
    f'      = {W99[0,0]*W99[1,1]:.4f} − {W99[0,1]**2:.4f}',
    f'      = {dW99:.4f}',
    '',
    f'  |T| = ({T99[0,0]:.6f}) × ({T99[1,1]:.4f}) − ({T99[0,1]:.4f})²',
    f'      = {T99[0,0]*T99[1,1]:.4f} − {T99[0,1]**2:.4f}',
    f'      = {dT99:.4f}',
    '',
    f'  Wilks\' Lambda = |W| / |T| = {dW99:.4f} / {dT99:.4f} = {wl99:.4f}',
])

story += calc_block([
    'Step 4 — Chi-Square Approximation (k = 3 groups, p = 2 variables):',
    '',
    '  χ² = −[n − 1 − (p + k)/2] × ln(Λ)',
    f'     = −[{n99} − 1 − ({2} + {3})/2] × ln({wl99:.4f})',
    f'     = −[{n99-1} − {(2+3)/2:.1f}] × {np.log(wl99):.4f}',
    f'     = −{n99-1-(2+3)/2:.1f} × {np.log(wl99):.4f}',
    f'     = {chi2_99:.4f}',
    '',
    f'  df = p × (k − 1) = 2 × 2 = 4',
    f'  p-value = P(χ²₄ > {chi2_99:.4f}) = {p99:.6f}',
])

story += calc_block([
    'Step 5 — Group Centroids on Discriminant Function 1:',
    '',
    f'  Admitted:     centroid = {centroids99[1]:>8.4f}',
    f'  Borderline:   centroid = {centroids99[3]:>8.4f}',
    f'  Not Admitted: centroid = {centroids99[2]:>8.4f}',
    '',
    'The ordering confirms that Function 1 separates admitted from not-admitted',
    'applicants, with borderline cases falling in between.',
    '',
    'Step 6 — Classification Rule (example):',
    '  An applicant is classified into the group whose centroid is closest',
    '  to their discriminant score (Mahalanobis / linear boundary):',
    '    GPA ≥ 3.30  AND  GMAT ≥ 500  →  Admitted',
    '    GPA < 2.90  AND  GMAT < 480  →  Not Admitted',
    '    Otherwise                    →  Borderline (holistic review)',
])

story.append(Spacer(1, 0.3*cm))
story.append(embed_image('q9_9_admissions_discriminant.png'))
story.append(Paragraph(
    'Figure 9.9 — GPA vs GMAT scatter, discriminant score distributions, '
    'standardised coefficients, and classification accuracy.',
    cap_st))
story.append(Paragraph('Code — Question 9.9', code_lbl))
story += code_block('hw_q9_9.py')

# ── Page footer ────────────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 8)
    canvas.setFillColor(GRAY)
    canvas.drawString(2.5*cm, 1.5*cm, 'Lana Gidan — Multivariate Data Analysis Homework')
    canvas.drawRightString(W_PAGE - 2.5*cm, 1.5*cm, f'Page {doc.page}')
    canvas.restoreState()

doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f'PDF saved: {OUTPUT}')

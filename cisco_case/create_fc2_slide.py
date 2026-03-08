import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(figsize=(33, 13))
ax.set_xlim(0, 33)
ax.set_ylim(0, 13)
ax.axis('off')
fig.patch.set_facecolor('white')

CISCO_BLUE = '#049FD9'
DARK_BLUE = '#204F69'
NAVY = '#002060'
GREEN = '#27AE60'
ORANGE = '#D35400'
PURPLE = '#8E44AD'

def draw_box(x, y, w, h, text, fc, fs=9, tc='white'):
    b = mpatches.FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.08",
                                 facecolor=fc, edgecolor='black', linewidth=2)
    ax.add_patch(b)
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, fontweight='bold', color=tc, wrap=True)

def draw_diamond(x, y, s, text, fc='#F39C12', tc='black', fs=9):
    half = s / 2
    pts = np.array([[x, y+half], [x+half, y], [x, y-half], [x-half, y], [x, y+half]])
    ax.fill(pts[:,0], pts[:,1], fc=fc, ec='black', lw=2, zorder=5)
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, fontweight='bold', color=tc, zorder=6)

def draw_oval(x, y, w, h, text, fc, tc='white', fs=10):
    e = mpatches.Ellipse((x, y), w, h, facecolor=fc, edgecolor='black', linewidth=2)
    ax.add_patch(e)
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, fontweight='bold', color=tc)

def draw_cylinder(x, y, w, h, text, fc, tc='white', fs=9):
    eh = h * 0.18
    bb = y - h/2
    bt = y + h/2 - eh
    r = mpatches.FancyBboxPatch((x-w/2, bb), w, bt-bb, boxstyle='square,pad=0',
                                 facecolor=fc, edgecolor='black', linewidth=2)
    ax.add_patch(r)
    et = mpatches.Ellipse((x, bt), w, eh*2, facecolor=fc, edgecolor='black', linewidth=2, zorder=5)
    ax.add_patch(et)
    eb = mpatches.Arc((x, bb), w, eh*2, angle=0, theta1=180, theta2=360, edgecolor='black', linewidth=2)
    ax.add_patch(eb)
    ax.text(x, y-0.1, text, ha='center', va='center', fontsize=fs, fontweight='bold', color=tc, zorder=6)

def arr(x1, y1, x2, y2, color='#333333', lw=2.5):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw))

# ===================== TITLE =====================
ax.text(16.5, 12.4, 'Solution 2: VIBE \u2014 Voice & Language Intelligence Layer',
        ha='center', fontsize=20, fontweight='bold', color=NAVY)
ax.text(16.5, 11.8, 'Real-Time Voice + Language AI  |  DNN Audio Pipeline  |  100+ Languages  |  Type-to-Speak',
        ha='center', fontsize=11, color='#666666')

# ===================== ROW 1: AUDIO PIPELINE =====================
r1y = 9.8

ax.text(8.5, 11.0, 'Audio Intelligence Front-End',
        ha='center', fontsize=13, fontweight='bold', color=CISCO_BLUE, fontstyle='italic')
ax.text(25.5, 11.0, 'NLP Processing',
        ha='center', fontsize=13, fontweight='bold', color=CISCO_BLUE, fontstyle='italic')

# Start oval
draw_oval(1.5, r1y, 2.2, 1.2, 'VIBE\nToggle ON', DARK_BLUE, fs=9)
arr(2.6, r1y, 3.4, r1y)

draw_box(4.5, r1y, 1.8, 1.2, 'Mode\nSelect', DARK_BLUE, fs=9)
arr(5.4, r1y, 6.2, r1y)

draw_box(7.5, r1y, 2.2, 1.2, 'Mic Audio\nCapture', CISCO_BLUE, fs=9)
arr(8.6, r1y, 9.5, r1y)

draw_box(10.8, r1y, 2.2, 1.2, 'DNN Noise\nRemoval\n150+ types', DARK_BLUE, fs=8)
arr(11.9, r1y, 12.8, r1y)

draw_box(14, r1y, 2.0, 1.2, 'Voice\nBoost\n+ EQ', CISCO_BLUE, fs=9)
arr(15, r1y, 15.8, r1y)

draw_box(17, r1y, 2.2, 1.2, 'ASR\nMulti-Accent\nTranscription', DARK_BLUE, fs=8)
arr(18.1, r1y, 18.8, r1y)

# Translate diamond
draw_diamond(20, r1y, 1.5, 'Translate\n?', '#F39C12', 'black', 9)

# YES arrow
ax.text(21.1, r1y+0.3, 'YES', fontsize=9, fontweight='bold', color=GREEN)
arr(20.75, r1y, 22.2, r1y, GREEN)

draw_box(23.8, r1y, 2.8, 1.2, 'Translate\n+ Simple Mode\n(jargon\u2192plain)', ORANGE, fs=8)
arr(25.2, r1y, 26.0, r1y)

draw_box(27.2, r1y, 2.0, 1.2, 'Neural\nTTS\n3 Personas', PURPLE, fs=8)
arr(28.2, r1y, 29.0, r1y)

draw_box(30.2, r1y, 2.0, 1.2, 'Delivered\nto All\nUsers', GREEN, fs=9)

# NO arrow going down
ax.text(20.3, r1y-1.1, 'NO', fontsize=9, fontweight='bold', color='#CC0000')
arr(20, r1y-0.75, 20, r1y-1.8, '#CC0000')

# ===================== ROW 2: TYPE-TO-SPEAK + Q&A =====================
r2y = 5.8

# Type-to-Speak dashed box
tts_box = mpatches.FancyBboxPatch((1.5, 4.7), 12.5, 3.0, boxstyle="round,pad=0.15",
                                    facecolor='none', edgecolor=CISCO_BLUE, linewidth=2, linestyle='--')
ax.add_patch(tts_box)
ax.text(5.5, 7.4, 'Type-to-Speak Mode', ha='center', fontsize=13, fontweight='bold',
        color=CISCO_BLUE, fontstyle='italic')

draw_box(3.5, r2y, 2.5, 1.3, 'User Types\nin Any\nLanguage', ORANGE, fs=9)
arr(4.75, r2y, 5.8, r2y)

draw_box(7.2, r2y, 2.5, 1.3, 'Detect Lang\n+ Translate\n+ Polish', DARK_BLUE, fs=9)
arr(8.45, r2y, 9.5, r2y)

draw_box(11, r2y, 2.5, 1.3, 'VIBE Speaks\n"Spoken by\nVIBE for [User]"', GREEN, fs=8)
arr(12.25, r2y, 14.5, r2y)

# Q&A dashed box
qa_box = mpatches.FancyBboxPatch((15.5, 4.7), 12.5, 3.0, boxstyle="round,pad=0.15",
                                   facecolor='none', edgecolor=CISCO_BLUE, linewidth=2, linestyle='--')
ax.add_patch(qa_box)
ax.text(21, 7.4, 'Q&A Close-Loop', ha='center', fontsize=13, fontweight='bold',
        color=CISCO_BLUE, fontstyle='italic')

# Arrow from NO down to Q&A area
arr(20, r2y+1.8, 20, r2y+0.8)

draw_box(17.5, r2y, 2.8, 1.3, 'User Asks\nin Native\nLanguage', PURPLE, fs=9)
arr(18.9, r2y, 20.0, r2y)

draw_box(21.5, r2y, 2.5, 1.3, 'Translate\nAnswer +\nSimplify', CISCO_BLUE, fs=9)
arr(22.75, r2y, 23.8, r2y)

draw_box(25, r2y, 2.0, 1.3, 'VIBE\nSummary\nPack', DARK_BLUE, fs=9)
arr(26.0, r2y, 28.5, r2y)

# Splunk cylinder
draw_cylinder(30, r2y, 2.5, 2.0, 'Splunk\nAudit\nTrail', PURPLE, fs=9)

# Arrow from row 1 end down to Splunk
arr(31.2, r1y-0.6, 31.2, r2y+1.5, '#999999', 1.5)

# ===================== LEGEND (horizontal, below flowchart) =====================
ly = 2.8
lx = 0.5

ax.text(lx, ly, 'LEGEND:', fontsize=11, fontweight='bold', color=NAVY)

# Start/End oval
e = mpatches.Ellipse((lx+3.0, ly+0.05), 1.0, 0.5, facecolor=DARK_BLUE, edgecolor='black', lw=1.5)
ax.add_patch(e)
ax.text(lx+4.0, ly, 'Start/End', fontsize=10, color='#333333', va='center')

# Process box
b = mpatches.FancyBboxPatch((lx+5.8, ly-0.2), 1.0, 0.5, boxstyle="round,pad=0.05",
                              facecolor=CISCO_BLUE, edgecolor='black', lw=1.5)
ax.add_patch(b)
ax.text(lx+7.3, ly, 'Process', fontsize=10, color='#333333', va='center')

# Decision diamond
ddx = lx + 9.5
pts = np.array([[ddx, ly+0.3], [ddx+0.3, ly], [ddx, ly-0.3], [ddx-0.3, ly], [ddx, ly+0.3]])
ax.fill(pts[:,0], pts[:,1], fc='#F39C12', ec='black', lw=1.5)
ax.text(ddx+0.6, ly, 'Decision', fontsize=10, color='#333333', va='center')

# Data I/O cylinder
cyl_x = lx + 12.5
cyl_r = mpatches.FancyBboxPatch((cyl_x-0.4, ly-0.25), 0.8, 0.35, boxstyle='square,pad=0',
                                  facecolor=PURPLE, edgecolor='black', lw=1.5)
ax.add_patch(cyl_r)
cyl_e = mpatches.Ellipse((cyl_x, ly+0.1), 0.8, 0.3, facecolor=PURPLE, edgecolor='black', lw=1.5)
ax.add_patch(cyl_e)
ax.text(cyl_x+0.8, ly, 'Data I/O', fontsize=10, color='#333333', va='center')

# ===================== IMPACT BAR =====================
ax.text(16.5, 1.5, 'IMPACT:  95%+ noise reduction  |  98% ASR accuracy  |  <1s translation  |  +40% non-native participation  |  All TTS labeled',
        ha='center', fontsize=11, fontweight='bold', color=DARK_BLUE)

plt.tight_layout()
plt.savefig('cisco_case/figures/fc2_slide.png', dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print("fc2_slide.png created successfully")

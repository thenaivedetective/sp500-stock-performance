import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# Define color palette
CISCO_BLUE = '#049FD9'
DARK_BLUE = '#204F69'
NAVY = '#002060'
GREEN = '#27AE60'
ORANGE = '#D35400'
PURPLE = '#8E44AD'
TEAL = '#1A5276'
KPI_FC = '#FFF3E0'
TS_FC = '#E8F4FD'
TEXT_DARK = '#333333'
TEXT_LIGHT = '#666666'

# Custom drawing functions
def draw_box(x, y, w, h, text, fc, fs=8, tc='white'):
    b = mpatches.FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.08",
                                  facecolor=fc, edgecolor='black', linewidth=1.5)
    ax.add_patch(b)
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, fontweight='bold', color=tc, wrap=True)

def draw_diamond(x, y, s, text, fc='#F39C12', tc='black', fs=8):
    half = s / 2
    pts = np.array([[x, y+half], [x+half, y], [x, y-half], [x-half, y], [x, y+half]])
    ax.fill(pts[:,0], pts[:,1], fc=fc, ec='black', lw=1.5, zorder=5)
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, fontweight='bold', color=tc, zorder=6)

def draw_oval(x, y, w, h, text, fc, tc='white', fs=9):
    e = mpatches.Ellipse((x, y), w, h, facecolor=fc, edgecolor='black', linewidth=1.5)
    ax.add_patch(e)
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, fontweight='bold', color=tc)

def draw_para(x, y, w, h, text, fc, tc='white', fs=8):
    sk = 0.2
    xs = [x-w/2+sk, x+w/2+sk, x+w/2-sk, x-w/2-sk]
    ys = [y-h/2, y-h/2, y+h/2, y+h/2]
    poly = plt.Polygon(list(zip(xs, ys)), facecolor=fc, edgecolor='black', linewidth=1.5)
    ax.add_patch(poly)
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, fontweight='bold', color=tc)

def arr(x1, y1, x2, y2, color='#333333', lw=2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw))

def dashed_box(x, y, w, h, color):
    r = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                                  facecolor='white', edgecolor=color, linewidth=2,
                                  linestyle='--', alpha=0.85)
    ax.add_patch(r)

# MAIN SCRIPT
fig, ax = plt.subplots(figsize=(36, 20))
ax.set_xlim(0, 36)
ax.set_ylim(0, 20)
ax.axis('off')
fig.patch.set_facecolor('white')

# ==================== MAIN TITLE & SUBTITLE ====================
ax.text(18, 19.5, 'Solution 2: VIBE \u2014 Voice & Language Intelligence Layer',
        ha='center', fontsize=18, fontweight='bold', color=NAVY)
ax.text(18, 19.0, 'Voice Boost  |  Live Translation  |  Type-to-Speak  |  Simple Mode  |  Real-Time In-Meeting AI',
        ha='center', fontsize=10, color=TEXT_LIGHT)

# ==================== ROW A: USER ENTRY & ONBOARDING ====================
dashed_box(0.5, 15.5, 28, 3.2, TEAL)
ax.text(14, 18.5, 'A: USER ENTRY & ONBOARDING', ha='center', fontsize=11,
        fontweight='bold', color=TEAL, fontstyle='italic')

r1y = 16.8
draw_oval(2.5, r1y, 2.5, 0.9, 'START\nUser Joins Meeting', NAVY, fs=7)
arr(3.75, r1y, 5.0, r1y)
draw_box(6.5, r1y, 2.8, 0.9, '1. Enable VIBE\nin Meeting Controls\nZero configuration', TEAL, fs=7)
arr(7.9, r1y, 9.0, r1y)
draw_box(10.5, r1y, 2.5, 0.9, '2. Select Modes\nVoice Boost | Translation\nType-to-Speak | Simple', CISCO_BLUE, fs=7)
arr(11.75, r1y, 12.8, r1y)
draw_box(14.3, r1y, 2.5, 0.9, '3. Select Language\nNative: 100+ supported\nTech Level: Tech/Non-Tech', GREEN, fs=7)
arr(15.55, r1y, 16.5, r1y)
draw_box(18, r1y, 2.5, 0.9, 'Voice Preset\nClear | Loud | Warm\nBroadcast-style', CISCO_BLUE, fs=7)
arr(19.25, r1y, 20.5, r1y)

# Branching point
draw_diamond(21.5, r1y, 1.2, 'Speaking\nor\nTyping?', '#F39C12', 'black', 7)

# Paths labels
ax.text(19.0, r1y-0.8, 'SPEAKING', fontsize=8, fontweight='bold', color=GREEN)
ax.text(24.0, r1y-0.8, 'TYPING', fontsize=8, fontweight='bold', color=CISCO_BLUE)

# Path indicators
arr(21.0, r1y-0.3, 19, r1y-0.8, GREEN, 1)
arr(22.0, r1y-0.3, 24, r1y-0.8, CISCO_BLUE, 1)

# KPIs & Targets box (top right)
kpi_box = mpatches.FancyBboxPatch((29.5, 15.8), 6.0, 3.0, boxstyle="round,pad=0.1",
                                    facecolor=KPI_FC, edgecolor=ORANGE, linewidth=2)
ax.add_patch(kpi_box)
ax.text(32.5, 18.5, 'KPIs & TARGETS', ha='center', fontsize=10, fontweight='bold', color=ORANGE)
kpi_items = ['Noise reduction: 95%+', 'ASR accuracy: 98%', 'Translation latency: <1s',
             'TTS naturalness: 4.5/5', 'Type-to-speak: <2s']
for i, kpi in enumerate(kpi_items):
    ax.text(29.9, 18.0 - i*0.35, kpi, fontsize=7, color=TEXT_DARK, va='center')

# ==================== ROW B & C: SPEAK PATH + TYPE-TO-SPEAK ====================
# Left: B - Live Audio Speak Path
dashed_box(0.5, 9.5, 17, 5.8, GREEN)
ax.text(9, 15.0, 'B: LIVE AUDIO SPEAK PATH', ha='center', fontsize=10,
        fontweight='bold', color=GREEN, fontstyle='italic')

r2y = 13.2
draw_para(2.5, r2y, 3.0, 0.9, '1. Audio Captured\nPer-speaker via AI Codec', '#2C3E50', fs=7)
arr(4.0, r2y, 5.0, r2y)
draw_box(6.8, r2y, 3.0, 0.9, '2. DNN Noise Removal\n150+ noise types\nEcho Cancel + Auto Gain', GREEN, fs=7)
arr(8.3, r2y, 9.3, r2y)
draw_box(11, r2y, 3.0, 0.9, '3. Voice Boost & EQ\nPreset: Clear/Loud/Warm\nAdaptive + normalization', GREEN, fs=7)
arr(12.5, r2y, 13.5, r2y)
draw_box(15.3, r2y, 3.0, 0.9, '4. ASR (Speech-to-Text)\nReal-time transcription\nFiller word removal', CISCO_BLUE, fs=7)

r2by = 11.5
draw_box(3, r2by, 3.0, 0.9, '5. NLP Processing\nSimple Mode: jargon\u2192plain\nTranslation + intent tagging', CISCO_BLUE, fs=7)
arr(15.3, r2y-0.45, 15.3, 11.9)
arr(15.3, 11.9, 4.5, r2by)
draw_box(7.5, r2by, 3.0, 0.9, '6. Text-to-Speech\nVIBE Voice neural TTS\nEmotional tone matching', GREEN, fs=7)
arr(4.5, r2by, 6.0, r2by)
draw_para(12, r2by, 3.0, 0.9, '7. Delivered to All\nCleaned + boosted voice\nPer-user captions', '#2C3E50', fs=7)
arr(9.0, r2by, 10.5, r2by)

# Right: C - Type-to-Speak Path
dashed_box(18, 9.5, 13.5, 5.8, CISCO_BLUE)
ax.text(24.75, 15.0, 'C: TYPE-TO-SPEAK PATH', ha='center', fontsize=10,
        fontweight='bold', color=CISCO_BLUE, fontstyle='italic')

r2cy = 13.2
draw_box(20.5, r2cy, 3.0, 0.9, '1. User Types in Panel\nAny language supported\nDraft visible before send', CISCO_BLUE, fs=7)
arr(22.0, r2cy, 23.0, r2cy)
draw_box(24.8, r2cy, 3.0, 0.9, '2. NLP Processing\nDetect lang + translate\nPolish mode: draft\u2192fluent', TEAL, fs=7)
arr(26.3, r2cy, 27.3, r2cy)
draw_box(29, r2cy, 3.0, 0.9, '3. VIBE Agent Speaks\nNeural TTS message\n"Spoken by VIBE for [User]"', GREEN, fs=7)

r2dy = 11.5
draw_box(21, r2dy, 3.0, 0.9, '4. Caption & Chat Sync\n"from [User] via VIBE"\nChat logs side-by-side', CISCO_BLUE, fs=7)
arr(29, r2cy-0.45, 29, 11.9)
arr(29, 11.9, 22.5, r2dy)

# Tech Stack box (far right, center height)
ts_box = mpatches.FancyBboxPatch((32, 10.0), 3.5, 4.8, boxstyle="round,pad=0.1",
                                    facecolor=TS_FC, edgecolor=NAVY, linewidth=2)
ax.add_patch(ts_box)
ax.text(33.75, 14.5, 'TECH STACK', ha='center', fontsize=9, fontweight='bold', color=NAVY)
ts_items = [('ASR', 'Whisper / Cisco AI'), ('NLP', 'Custom LLM + Rules'),
            ('TTS', 'Neural Voice Synth'), ('MT', 'Neural Machine Trans.'),
            ('DSP', 'DNN Noise + EQ'), ('Codec', 'Webex AI Codec')]
for i, (label, desc) in enumerate(ts_items):
    ty = 14.0 - i * 0.6
    ax.text(32.3, ty, label, fontsize=7, fontweight='bold', color=NAVY, va='center')
    ax.text(33.3, ty, desc, fontsize=6, color=TEXT_DARK, va='center')

# ==================== ROW D: Q&A CLOSE-LOOP ====================
dashed_box(0.5, 4.5, 35, 4.8, PURPLE)
ax.text(18, 9.0, 'D: Q&A CLOSE-LOOP (Non-Native / Non-Tech Users)', ha='center',
        fontsize=10, fontweight='bold', color=PURPLE, fontstyle='italic')

r3y = 6.8
draw_box(3, r3y, 3.0, 0.9, '1. User Asks\nin Own Language\nVoice or Type-to-Speak', PURPLE, fs=7)
arr(4.5, r3y, 6.0, r3y)
draw_box(7.8, r3y, 3.2, 0.9, '2. ASR + Translation\nPresenter sees translated\nquestion in English', PURPLE, fs=7)
arr(9.4, r3y, 10.5, r3y)
draw_box(12.5, r3y, 3.5, 0.9, '3. Presenter Answers\nin English, VIBE captures\n"Simplified answer" tag', CISCO_BLUE, fs=7)
arr(14.25, r3y, 15.5, r3y)
draw_box(17.5, r3y, 3.5, 0.9, '4. Translation + Simplification\nBack to User in native lang\nSimple Mode adds analogies', PURPLE, fs=7)
arr(19.25, r3y, 20.5, r3y)
draw_para(22, r3y, 2.5, 0.9, 'Audio Output\nAnswer in native lang', '#2C3E50', fs=7)
draw_para(26, r3y, 3.0, 0.9, 'Text Output\nSimplified + analogy\nin caption pane', '#2C3E50', fs=7)
arr(23.25, r3y, 24.5, r3y)

# Integration with Splunk
arr(17.5, r3y-0.45, 17.5, 5.0, NAVY, 1.5)
ax.text(17.5, 4.8, 'To Splunk', color=NAVY, fontsize=6, ha='center')

# ==================== ROW E: END & LOGGING ====================
dashed_box(0.5, 0.5, 35, 3.8, ORANGE)
ax.text(18, 4.0, 'E: END & LOGGING', ha='center', fontsize=10,
        fontweight='bold', color=ORANGE, fontstyle='italic')

r4y = 2.3
draw_oval(2.5, r4y, 2.5, 0.9, 'Meeting Ends', ORANGE, fs=8)
arr(3.75, r4y, 5.0, r4y)
draw_box(7, r4y, 3.5, 0.9, 'VIBE Transcript\nOriginal + English + Simplified\nTimestamps + speaker IDs', ORANGE, fs=7)
arr(8.75, r4y, 10.0, r4y)
draw_box(12, r4y, 3.5, 0.9, 'VIBE Summary Pack\nKey Q&A in native language\nDownloadable per-user', ORANGE, fs=7)
arr(13.75, r4y, 15.0, r4y)
draw_box(17, r4y, 3.5, 0.9, 'Splunk Observability\nVoice clarity score trend\nTranslation accuracy log', NAVY, fs=7, tc='#FFD700')
arr(18.75, r4y, 20.0, r4y)
draw_box(22, r4y, 3.5, 0.9, 'Privacy Guarantee\n"Spoken by VIBE for [User]"\nFull audit | Zero retention', NAVY, fs=7)

# End state
draw_oval(27, r4y, 2.5, 0.9, 'Session Complete', NAVY, fs=8)
arr(23.75, r4y, 25.75, r4y)

# Output handling
fig.patch.set_facecolor('white')
output_dir = 'cisco_case/figures'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
output_path = os.path.join(output_dir, 'fc2_landscape.png')

plt.tight_layout()
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print(f"{output_path} created successfully")
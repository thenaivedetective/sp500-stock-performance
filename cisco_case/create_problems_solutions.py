import matplotlib
matplotlib.use('Agg')
from fpdf import FPDF
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

os.makedirs("cisco_case/figures", exist_ok=True)

def draw_oval(ax, cx, cy, w, h, text, color='#002060', tc='white', fs=10):
    e = mpatches.Ellipse((cx, cy), w, h, facecolor=color, edgecolor='black', linewidth=2)
    ax.add_patch(e)
    ax.text(cx, cy, text, ha='center', va='center', fontsize=fs, fontweight='bold', color=tc)

def draw_rect(ax, cx, cy, w, h, text, color='#0070C0', tc='white', fs=10):
    r = mpatches.FancyBboxPatch((cx-w/2, cy-h/2), w, h, boxstyle="round,pad=0.08",
                                 facecolor=color, edgecolor='black', linewidth=2)
    ax.add_patch(r)
    ax.text(cx, cy, text, ha='center', va='center', fontsize=fs, fontweight='bold', color=tc, wrap=True)

def draw_diamond(ax, cx, cy, size, text, color='#F39C12', tc='black', fs=9):
    half = size / 2
    xs = [cx, cx+half, cx, cx-half]
    ys = [cy+half, cy, cy-half, cy]
    poly = plt.Polygon(list(zip(xs, ys)), facecolor=color, edgecolor='black', linewidth=2)
    ax.add_patch(poly)
    ax.text(cx, cy, text, ha='center', va='center', fontsize=fs, fontweight='bold', color=tc)

def draw_para(ax, cx, cy, w, h, text, color='#27AE60', tc='white', fs=10):
    sk = 0.3
    xs = [cx-w/2+sk, cx+w/2+sk, cx+w/2-sk, cx-w/2-sk]
    ys = [cy-h/2, cy-h/2, cy+h/2, cy+h/2]
    poly = plt.Polygon(list(zip(xs, ys)), facecolor=color, edgecolor='black', linewidth=2)
    ax.add_patch(poly)
    ax.text(cx, cy, text, ha='center', va='center', fontsize=fs, fontweight='bold', color=tc)

def draw_cyl(ax, cx, cy, w, h, text, color='#8E44AD', tc='white', fs=9):
    eh = h*0.18
    bb = cy - h/2
    bt = cy + h/2 - eh
    r = mpatches.FancyBboxPatch((cx-w/2, bb), w, bt-bb, boxstyle='square,pad=0',
                                 facecolor=color, edgecolor='black', linewidth=2)
    ax.add_patch(r)
    et = mpatches.Ellipse((cx, bt), w, eh*2, facecolor=color, edgecolor='black', linewidth=2, zorder=5)
    ax.add_patch(et)
    eb = mpatches.Arc((cx, bb), w, eh*2, angle=0, theta1=180, theta2=360, edgecolor='black', linewidth=2)
    ax.add_patch(eb)
    ax.text(cx, cy-0.1, text, ha='center', va='center', fontsize=fs, fontweight='bold', color=tc, zorder=6)

def draw_dashed_box(ax, x, y, w, h, title, color='#0050A0'):
    r = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                                 facecolor='white', edgecolor=color, linewidth=2.5,
                                 linestyle='--', alpha=0.85)
    ax.add_patch(r)
    ax.text(x + w/2, y + h - 0.3, title, ha='center', va='center',
            fontsize=11, fontweight='bold', color=color)

def arrow(ax, x1, y1, x2, y2, color='#333333', lw=2.5):
    ax.annotate('', xy=(x2,y2), xytext=(x1,y1), arrowprops=dict(arrowstyle='->', color=color, lw=lw))

def draw_symbol_directory(ax, x, y, w, h):
    bg = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                                  facecolor='#F8F9FA', edgecolor='#002060', linewidth=2.5, zorder=10)
    ax.add_patch(bg)
    ax.text(x + w/2, y + h - 0.3, 'SYMBOL DIRECTORY', ha='center', fontsize=10,
            fontweight='bold', color='#002060', zorder=11)

    cx = x + 1.0
    tx = x + 2.2

    sy = y + h - 0.9
    sp = 0.62

    e = mpatches.Ellipse((cx, sy), 1.0, 0.35, facecolor='#002060', edgecolor='black', linewidth=1.5, zorder=11)
    ax.add_patch(e)
    ax.text(tx, sy, '= Start / End (Terminator)', fontsize=7.5, va='center', color='#333333', zorder=11)

    sy -= sp
    r = mpatches.FancyBboxPatch((cx-0.5, sy-0.14), 1.0, 0.28, boxstyle="round,pad=0.04",
                                 facecolor='#0070C0', edgecolor='black', linewidth=1.5, zorder=11)
    ax.add_patch(r)
    ax.text(tx, sy, '= Process / Action Step', fontsize=7.5, va='center', color='#333333', zorder=11)

    sy -= sp
    hs = 0.25
    dxs = [cx, cx+hs, cx, cx-hs]
    dys = [sy+hs, sy, sy-hs, sy]
    dp = plt.Polygon(list(zip(dxs, dys)), facecolor='#F39C12', edgecolor='black', linewidth=1.5, zorder=11)
    ax.add_patch(dp)
    ax.text(tx, sy, '= Decision Gate (Yes/No)', fontsize=7.5, va='center', color='#333333', zorder=11)

    sy -= sp
    sk = 0.12
    pxs = [cx-0.5+sk, cx+0.5+sk, cx+0.5-sk, cx-0.5-sk]
    pys = [sy-0.14, sy-0.14, sy+0.14, sy+0.14]
    pp = plt.Polygon(list(zip(pxs, pys)), facecolor='#27AE60', edgecolor='black', linewidth=1.5, zorder=11)
    ax.add_patch(pp)
    ax.text(tx, sy, '= Data Input / Output', fontsize=7.5, va='center', color='#333333', zorder=11)

    sy -= sp
    cr = mpatches.FancyBboxPatch((cx-0.5, sy-0.18), 1.0, 0.3, boxstyle='square,pad=0',
                                  facecolor='#8E44AD', edgecolor='black', linewidth=1.5, zorder=11)
    ax.add_patch(cr)
    ce = mpatches.Ellipse((cx, sy+0.12), 1.0, 0.16, facecolor='#8E44AD', edgecolor='black', linewidth=1.5, zorder=12)
    ax.add_patch(ce)
    ax.text(tx, sy, '= Database / Storage', fontsize=7.5, va='center', color='#333333', zorder=11)

    sy -= sp
    dr = mpatches.FancyBboxPatch((cx-0.5, sy-0.14), 1.0, 0.28, boxstyle="round,pad=0.04",
                                  facecolor='white', edgecolor='#0050A0', linewidth=1.5, linestyle='--', zorder=11)
    ax.add_patch(dr)
    ax.text(tx, sy, '= Phase / Group Boundary', fontsize=7.5, va='center', color='#333333', zorder=11)

    sy -= sp * 0.8
    ax.annotate('', xy=(cx+0.4, sy), xytext=(cx-0.4, sy),
                arrowprops=dict(arrowstyle='->', color='#333333', lw=2, zorder=11))
    ax.text(tx, sy, '= Flow Direction', fontsize=7.5, va='center', color='#333333', zorder=11)


# ============================================================
# FLOWCHART 1: Enhanced Agentic AI - Prepare-Perceive-Reason-Act-Follow-Up
# ============================================================
fig, ax = plt.subplots(figsize=(22, 44))
ax.set_xlim(0, 22)
ax.set_ylim(0, 44)
ax.axis('off')

ax.text(11, 43.3, 'Solution 1: Webex AI Meeting Prep & Workflow Orchestrator',
        ha='center', fontsize=21, fontweight='bold', color='#002060')
ax.text(11, 42.7, 'Prepare \u2192 Perceive \u2192 Reason \u2192 Act \u2192 Follow-Up  |  Full Meeting Lifecycle AI',
        ha='center', fontsize=13, color='#555555')

draw_symbol_directory(ax, 15.5, 26.0, 5.5, 4.8)

lane_colors = ['#E8F4FD', '#FFF3E0', '#F3E5F5']
lane_labels = ['WEBEX CLOUD', 'CISCO SECURE DATA FABRIC', 'THIRD-PARTY APPS']
lane_sublabels = ['(AI Codec + NLP + Agent Runtime)', '(Splunk + Zero-Trust Identity)', '(Jira, Salesforce, SAP, etc.)']
lane_xs = [(0.3, 7.0), (7.5, 14.5), (15.0, 21.7)]

for i, ((x1, x2), color, label, sublabel) in enumerate(zip(lane_xs, lane_colors, lane_labels, lane_sublabels)):
    rect = mpatches.FancyBboxPatch((x1, 1.0), x2 - x1, 40.5, boxstyle="round,pad=0.1",
                                    facecolor=color, edgecolor='#999999', linewidth=1.5, alpha=0.5)
    ax.add_patch(rect)
    ax.text((x1 + x2) / 2, 41.2, label, ha='center', fontsize=13, fontweight='bold', color='#002060')
    ax.text((x1 + x2) / 2, 40.8, sublabel, ha='center', fontsize=9, color='#666666')

WX = 3.65
DF = 11.0
TP = 18.35

draw_oval(ax, WX, 39.8, 4.5, 1.0, 'START\nMeeting Scheduled', '#002060', 'white', 11)
arrow(ax, WX, 39.25, WX, 38.6)

draw_dashed_box(ax, 0.5, 34.2, 6.3, 4.2, 'PREPARE: AI Meeting Prep', '#0050A0')

draw_rect(ax, WX, 37.9, 5.5, 1.0,
          'Context Ingestion\nIngest title, participants, docs,\nCRM records, past transcripts', '#1A5276', 'white', 9)
arrow(ax, WX, 37.35, WX, 36.7)

draw_rect(ax, WX, 36.1, 5.5, 1.0,
          'AI Generates Agenda + Insights\nPrep checklist, key metrics,\npredicted Q&A for presenter', '#1A5276', 'white', 9)
arrow(ax, WX, 35.55, WX, 34.9)

draw_rect(ax, WX, 34.3, 5.5, 1.0,
          'Auto-Slide Generation\nFirst-draft deck from CRM data,\nJira issues, financial metrics', '#0070C0', 'white', 9)

arrow(ax, WX + 2.8, 37.9, TP - 2.5, 37.9, '#333333')
draw_para(ax, TP, 37.9, 5.0, 1.0,
          'PULL CONTEXT\nCRM pipeline, Jira backlog,\nCalendar history', '#D35400', 'white', 9)

arrow(ax, WX + 2.8, 36.1, DF - 2.5, 36.1, '#333333')
draw_cyl(ax, DF, 36.1, 5.0, 1.2,
         'Cisco Secure Data Fabric\nZero-Trust data retrieval\nSplunk audit logging', '#8E44AD', 'white', 9)

arrow(ax, WX, 33.75, WX, 33.1)

draw_oval(ax, WX, 32.5, 4.5, 1.0, 'Meeting\nBegins Live', '#27AE60', 'white', 11)
arrow(ax, WX, 31.95, WX, 31.3)

draw_dashed_box(ax, 0.5, 25.0, 6.3, 6.1, 'PERCEIVE: AI Codec ML Pipeline', '#0050A0')

draw_para(ax, WX, 30.7, 5.2, 0.9,
          'Raw Audio/Video Input\nMicrophone + Camera streams', '#2C3E50', 'white', 9)
arrow(ax, WX, 30.2, WX, 29.6)

draw_rect(ax, WX, 29.0, 5.5, 1.0,
          'DNN Noise Removal\n150+ noise types in real-time\n+ Echo Cancellation', '#1A5276', 'white', 9)
arrow(ax, WX, 28.45, WX, 27.8)

draw_rect(ax, WX, 27.2, 5.5, 1.0,
          'AI Codec: Neural Speech Synthesis\nCompresses to ~1 kbps\nRMM: Super Resolution + Voice Isolation', '#1A5276', 'white', 9)
arrow(ax, WX, 26.65, WX, 26.0)

draw_rect(ax, WX, 25.4, 5.5, 1.0,
          'NLP Engine: Speech-to-Text\nReal-time transcription + translation\nTask intent + decision detection', '#0070C0', 'white', 9)
arrow(ax, WX, 24.85, WX, 24.0)

draw_diamond(ax, WX, 23.0, 2.0, 'NLP detects\nTask Intent?', '#F39C12', 'black', 10)

ax.text(1.0, 23.0, 'NO', fontsize=12, fontweight='bold', color='#E74C3C', ha='center')
arrow(ax, WX - 1.0, 23.0, 1.5, 23.0, '#E74C3C', 2)
arrow(ax, 1.0, 23.0, 1.0, 30.7, '#E74C3C', 2)
arrow(ax, 1.0, 30.7, WX - 2.8, 30.7, '#E74C3C', 2)
ax.text(1.0, 26.8, 'Continue\nMonitoring', fontsize=9, fontweight='bold', color='#E74C3C', ha='center',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#E74C3C', alpha=0.9))

ax.text(WX + 1.7, 23.7, 'YES', fontsize=12, fontweight='bold', color='#27AE60', ha='center')
arrow(ax, WX + 1.0, 23.0, DF - 2.5, 23.0, '#27AE60', 2.5)

draw_para(ax, DF, 23.0, 5.0, 1.1,
          'REASON: Fetch Context\nA2A Protocol retrieves\nproject data from systems', '#27AE60', 'white', 10)

arrow(ax, DF + 2.8, 23.0, TP - 2.2, 23.0, '#333333')

draw_para(ax, TP, 23.0, 5.0, 1.1,
          'EXTERNAL SYSTEMS\nJira / Salesforce / SAP\nServiceNow / GitHub', '#D35400', 'white', 9)

arrow(ax, DF, 22.35, DF, 21.2)

draw_cyl(ax, DF, 20.4, 5.0, 1.5,
         'CISCO SECURE DATA FABRIC\nSplunk Observability\nZero-Trust Identity Layer', '#8E44AD', 'white', 9)

arrow(ax, DF, 19.55, DF, 18.5)

draw_rect(ax, DF, 17.8, 5.0, 1.2,
          'ACT: DRAFT\nAI Agent generates task draft\nusing retrieved context\n+ LLM-based planning', '#0070C0', 'white', 10)

arrow(ax, DF - 2.8, 17.8, WX + 1.5, 16.3, '#333333')

draw_diamond(ax, WX, 15.3, 2.0, 'Human-in-Loop\nApprove?', '#F39C12', 'black', 10)

ax.text(WX + 1.7, 14.3, 'REJECT', fontsize=11, fontweight='bold', color='#E74C3C', ha='center')
arrow(ax, WX + 1.0, 15.3, DF - 2.8, 17.2, '#E74C3C', 2)

ax.text(WX + 1.7, 16.1, 'APPROVE', fontsize=11, fontweight='bold', color='#27AE60', ha='center')
arrow(ax, WX + 1.0, 15.3, TP - 2.5, 15.3, '#27AE60', 2.5)

draw_rect(ax, TP, 15.3, 5.0, 1.2,
          'EXECUTE\nAgent pushes data via\nsecure API to external app', '#E74C3C', 'white', 10)

arrow(ax, TP, 14.65, TP, 13.8)

draw_rect(ax, DF, 13.0, 5.5, 1.0,
          'Splunk Logs Execution\nPerformance metrics + audit trail\nAnomaly detection on agent actions', '#8E44AD', 'white', 9)
arrow(ax, TP, 13.0, DF + 2.8, 13.0, '#333333')

arrow(ax, DF, 12.45, DF, 11.8)

draw_rect(ax, DF, 11.1, 5.5, 1.0,
          'CONFIRM\nStatus posted to Webex Chat:\n"Task WEBAPP-2026-347 created"', '#0070C0', 'white', 9)
arrow(ax, DF - 2.8, 11.1, WX + 2.0, 11.1, '#333333')

arrow(ax, DF, 10.55, DF, 9.8)

draw_dashed_box(ax, 0.5, 3.8, 6.3, 5.8, 'FOLLOW-UP: Post-Meeting AI', '#0050A0')

draw_oval(ax, WX, 9.2, 4.5, 1.0, 'Meeting\nEnds', '#27AE60', 'white', 11)
arrow(ax, DF - 2.8, 9.2, WX + 2.5, 9.2, '#333333')
arrow(ax, WX, 8.65, WX, 8.0)

draw_rect(ax, WX, 7.4, 5.5, 1.0,
          'Unanswered Q Detection\nIdentify deferred questions\nfrom transcript + predicted Q&A', '#1A5276', 'white', 9)
arrow(ax, WX, 6.85, WX, 6.2)

draw_rect(ax, WX, 5.6, 5.5, 1.0,
          'AI Drafts Follow-Up Answers\nOwner reviews, edits, approves\nMulti-channel delivery', '#0070C0', 'white', 9)
arrow(ax, WX, 5.05, WX, 4.4)

draw_rect(ax, WX, 3.8, 5.5, 1.0,
          'Q&A Tracker Dashboard\nWeekly digest to participants\nResolution rate monitoring', '#0070C0', 'white', 9)

arrow(ax, WX + 2.8, 7.4, DF - 2.5, 7.4, '#333333')
draw_cyl(ax, DF, 7.4, 5.0, 1.2,
         'Splunk Observability\nFollow-up completion tracking\nSLA monitoring + alerts', '#8E44AD', 'white', 9)

arrow(ax, WX + 2.8, 5.6, TP - 2.5, 5.6, '#333333')
draw_rect(ax, TP, 5.6, 5.0, 1.0,
          'Deliver Answers via\nWebex Spaces / Email /\nIntegrated Chat Tools', '#D35400', 'white', 9)

arrow(ax, WX, 3.25, WX, 2.6)
draw_oval(ax, WX, 2.0, 4.5, 0.9, 'END\nAll Loops Closed')

mr = mpatches.FancyBboxPatch((0.3, 1.0), 21.4, 0.6, boxstyle='round,pad=0.05',
                               facecolor='#002060', edgecolor='black', linewidth=2)
ax.add_patch(mr)
ax.text(11, 1.3, 'IMPACT: 15 min saved/meeting  |  25% meeting-to-action  |  '
        '40% workflow automation  |  85% task accuracy  |  90%+ Q&A resolution',
        ha='center', va='center', fontsize=9, fontweight='bold', color='white')

plt.tight_layout()
plt.savefig('cisco_case/figures/flowchart_1_agentic_ai.png', dpi=200, bbox_inches='tight')
plt.close()
print("Flowchart 1 created")

# ============================================================
# FLOWCHART 2: VIBE / VEL - Voice & Language Intelligence Layer
# (Complete rebuild with all details from reference PDF)
# ============================================================
fig, ax = plt.subplots(figsize=(22, 58))
ax.set_xlim(0, 22)
ax.set_ylim(0, 58)
ax.axis('off')

ax.text(11, 57.3, 'Solution 2: VIBE - Voice & Language Intelligence Layer',
        ha='center', fontsize=21, fontweight='bold', color='#002060')
ax.text(11, 56.7, 'Voice Boost | Live Translation | Type-to-Speak | Simple Mode  |  Real-Time In-Meeting AI',
        ha='center', fontsize=13, color='#555555')

draw_symbol_directory(ax, 0.3, 51.5, 6.5, 4.8)

ts_box = mpatches.FancyBboxPatch((15.2, 50.2), 6.5, 6.5, boxstyle="round,pad=0.1",
                                   facecolor='#E8F4FD', edgecolor='#002060', linewidth=2.5)
ax.add_patch(ts_box)
ax.text(18.45, 56.35, 'TECH STACK', ha='center', fontsize=11, fontweight='bold', color='#002060')
ts_items = [
    ('ASR', 'Whisper / Cisco AI'),
    ('NLP', 'Custom LLM + Rules'),
    ('TTS', 'Neural Voice Synthesis'),
    ('MT', 'Neural Machine Translation'),
    ('DSP', 'DNN Noise + EQ'),
    ('Codec', 'Webex AI Codec'),
]
for i, (label, desc) in enumerate(ts_items):
    ty = 55.5 - i * 0.8
    ax.text(15.6, ty, label, fontsize=9, fontweight='bold', color='#002060', va='center')
    ax.text(17.0, ty, desc, fontsize=8, color='#333333', va='center')

kpi_box = mpatches.FancyBboxPatch((7.5, 53.2), 6.8, 3.5, boxstyle="round,pad=0.1",
                                    facecolor='#FFF3E0', edgecolor='#D35400', linewidth=2.5)
ax.add_patch(kpi_box)
ax.text(10.9, 56.35, 'KPIs & TARGETS', ha='center', fontsize=11, fontweight='bold', color='#D35400')
kpi_items = [
    'Noise reduction: 95%+',
    'ASR accuracy: 98%',
    'Translation latency: <1s',
    'TTS naturalness: 4.5/5',
    'Type-to-speak: <2s',
]
for i, kpi in enumerate(kpi_items):
    ky = 55.5 - i * 0.7
    ax.text(7.9, ky, kpi, fontsize=9, color='#333333', va='center')

lang_box = mpatches.FancyBboxPatch((7.5, 50.2), 6.8, 2.7, boxstyle="round,pad=0.1",
                                     facecolor='#F3E5F5', edgecolor='#8E44AD', linewidth=2.5)
ax.add_patch(lang_box)
ax.text(10.9, 52.55, 'LANGUAGES', ha='center', fontsize=11, fontweight='bold', color='#8E44AD')
ax.text(10.9, 51.8, 'Hindi  |  Spanish  |  Mandarin  |  French', ha='center', fontsize=9, color='#333333')
ax.text(10.9, 51.2, 'Arabic  |  Portuguese  |  Japanese  |  Korean', ha='center', fontsize=9, color='#333333')
ax.text(10.9, 50.6, '+ 90 more via Neural Machine Translation', ha='center', fontsize=9, fontweight='bold', color='#8E44AD')

draw_oval(ax, 11, 49.2, 7.0, 0.9, 'START - USER JOINS WEBEX MEETING', '#002060', 'white', 12)
arrow(ax, 11, 48.7, 11, 48.1)

p_onb = mpatches.FancyBboxPatch((2.0, 42.5), 18.0, 5.4, boxstyle="round,pad=0.15",
                                  facecolor='#1A5276', edgecolor='#1A5276', linewidth=2, alpha=0.08)
ax.add_patch(p_onb)
ax.text(2.5, 47.5, 'A: USER ENTRY & ONBOARDING', fontsize=13, fontweight='bold', color='#1A5276')

draw_rect(ax, 11, 47.4, 12.0, 0.9,
          '1. User Enables VIBE in Meeting Controls  |  Toggle appears in controls bar  |  Zero configuration required', '#1A5276', 'white', 10)
arrow(ax, 11, 46.9, 11, 46.3)

draw_rect(ax, 5.5, 45.5, 5.5, 1.2,
          '2. Select Active Modes\nVoice Boost | Live Translation\nType-to-Speak | Simple Mode', '#1A5276', 'white', 10)

draw_rect(ax, 11, 45.5, 5.0, 1.2,
          '3. Select Language\nNative: 100+ supported\nTech Level: Tech / Non-Tech', '#0070C0', 'white', 10)

draw_rect(ax, 16.5, 45.5, 5.0, 1.2,
          'Voice Preset Selection\nClear | Loud | Warm\nBroadcast-style', '#0070C0', 'white', 10)

arrow(ax, 11, 46.3, 5.5, 46.15, '#333333')
arrow(ax, 11, 46.3, 16.5, 46.15, '#333333')

arrow(ax, 5.5, 44.85, 5.5, 44.2)
arrow(ax, 16.5, 44.85, 16.5, 44.2)
arrow(ax, 5.5, 44.2, 10.5, 43.7, '#333333')
arrow(ax, 16.5, 44.2, 11.5, 43.7, '#333333')

draw_diamond(ax, 11, 42.7, 2.2, 'User is\nSpeaking\nor Typing?', '#F39C12', 'black', 10)

ax.text(4.5, 42.7, 'SPEAKING', fontsize=12, fontweight='bold', color='#27AE60', ha='center')
arrow(ax, 11 - 1.1, 42.7, 5.2, 42.7, '#27AE60', 2.5)
arrow(ax, 5.2, 42.7, 5.2, 41.8)

ax.text(17.5, 42.7, 'TYPING', fontsize=12, fontweight='bold', color='#0070C0', ha='center')
arrow(ax, 11 + 1.1, 42.7, 16.8, 42.7, '#0070C0', 2.5)
arrow(ax, 16.8, 42.7, 16.8, 41.8)

p_speak = mpatches.FancyBboxPatch((0.5, 28.0), 10.0, 13.6, boxstyle="round,pad=0.15",
                                    facecolor='#27AE60', edgecolor='#27AE60', linewidth=2, alpha=0.08)
ax.add_patch(p_speak)
ax.text(1.0, 41.2, 'B: LIVE AUDIO SPEAK PATH', fontsize=13, fontweight='bold', color='#27AE60')

draw_para(ax, 5.2, 41.0, 6.0, 0.9,
          '1. Microphone Audio Captured\nPer-speaker separation via AI Codec', '#2C3E50', 'white', 9)
arrow(ax, 5.2, 40.5, 5.2, 39.8)

draw_rect(ax, 5.2, 39.2, 6.0, 1.0,
          '2. Audio Intelligence Front-End\nDNN Noise Removal (150+ types)\nEcho Cancel + Auto Gain + Room Detect', '#27AE60', 'white', 9)
arrow(ax, 5.2, 38.65, 5.2, 38.0)

draw_rect(ax, 5.2, 37.4, 6.0, 1.0,
          '3. Voice Boost & EQ Engine\nPreset: Clear / Loud / Warm / Broadcast\nAdaptive to environment + normalization', '#27AE60', 'white', 9)
arrow(ax, 5.2, 36.85, 5.2, 36.2)

draw_rect(ax, 5.2, 35.6, 6.0, 1.0,
          '4. Speech-to-Text (ASR)\nReal-time transcription + diarization\nFiller word removal (um/uh/like)', '#0070C0', 'white', 9)
arrow(ax, 5.2, 35.05, 5.2, 34.3)

draw_rect(ax, 5.2, 33.5, 6.0, 1.4,
          '5. NLP Layer - Conditional Processing\nSimple Mode: jargon -> plain language\nTranslation: native -> English/target\nAlways: intent tagging + clarity scoring', '#0070C0', 'white', 9)
arrow(ax, 5.2, 32.75, 5.2, 32.1)

draw_rect(ax, 5.2, 31.4, 6.0, 1.2,
          '6. Text-to-Speech: VIBE Voice\nNeural TTS with user persona\nEmotional tone matching\nConsistent voice identity per session', '#27AE60', 'white', 9)
arrow(ax, 5.2, 30.75, 5.2, 30.1)

draw_para(ax, 5.2, 29.4, 6.0, 1.2,
          '7. Delivered to All Participants\nCleaned + boosted + translated voice\nPer-user captions in their language\nEach attendee controls own caption', '#2C3E50', 'white', 9)

p_type = mpatches.FancyBboxPatch((11.5, 33.0), 10.0, 8.6, boxstyle="round,pad=0.15",
                                   facecolor='#0070C0', edgecolor='#0070C0', linewidth=2, alpha=0.08)
ax.add_patch(p_type)
ax.text(12.0, 41.2, 'C: TYPE-TO-SPEAK PATH', fontsize=13, fontweight='bold', color='#0070C0')

draw_rect(ax, 16.8, 41.0, 6.0, 0.9,
          '1. User Switches to Type-to-Speak\nTrigger: muted / noisy / mic issue / shy', '#0070C0', 'white', 9)
arrow(ax, 16.8, 40.5, 16.8, 39.8)

draw_rect(ax, 16.8, 39.2, 6.0, 1.0,
          '2. User Types in VIBE Panel\nAny language - paste code/data/tables\nDraft visible only to user before send', '#0070C0', 'white', 9)
arrow(ax, 16.8, 38.65, 16.8, 38.0)

draw_rect(ax, 16.8, 37.4, 6.0, 1.0,
          '3. NLP Processing\nDetect language + translate to meeting lang\nPolish mode: draft -> fluent speech', '#1A5276', 'white', 9)
arrow(ax, 16.8, 36.85, 16.8, 36.2)

draw_rect(ax, 16.8, 35.6, 6.0, 1.0,
          '4. VIBE Agent Speaks for User\nNeural TTS speaks typed message\nLabel: "Spoken by VIBE for [User]"', '#27AE60', 'white', 9)
arrow(ax, 16.8, 35.05, 16.8, 34.3)

draw_rect(ax, 16.8, 33.6, 6.0, 1.0,
          '5. Caption & Chat Sync\n"from [User] via VIBE" tag in transcript\nChat logs typed + spoken side-by-side', '#0070C0', 'white', 9)

arrow(ax, 5.2, 28.75, 5.2, 27.8)
arrow(ax, 16.8, 33.05, 16.8, 27.8)
arrow(ax, 16.8, 27.8, 11.5, 27.3, '#333333')
arrow(ax, 5.2, 27.8, 10.5, 27.3, '#333333')

p_qa = mpatches.FancyBboxPatch((0.5, 18.5), 21.0, 8.5, boxstyle="round,pad=0.15",
                                 facecolor='#8E44AD', edgecolor='#8E44AD', linewidth=2, alpha=0.08)
ax.add_patch(p_qa)
ax.text(1.0, 26.6, 'D: Q&A CLOSE-LOOP (NON-NATIVE / NON-TECH USERS)', fontsize=13, fontweight='bold', color='#8E44AD')

draw_rect(ax, 5.5, 26.4, 6.0, 1.0,
          '1. User Asks in Own Language\nVoice or Type-to-Speak - any language\ne.g. Hindi, Spanish, Mandarin', '#8E44AD', 'white', 10)
arrow(ax, 5.5, 25.85, 5.5, 25.2)

draw_rect(ax, 5.5, 24.5, 6.0, 1.2,
          '2. ASR + Translation to English\nPresenter sees: "[Priya] asked\n(translated): How does the\nAPI integration work?"', '#8E44AD', 'white', 9)
arrow(ax, 8.5, 24.5, 12.5, 24.5, '#333333')

draw_rect(ax, 16.5, 24.5, 6.0, 1.2,
          '3. Presenter Answers in English\nVIBE captures answer in real-time\nCan tag: "Simplified answer"\nto trigger extra NLP', '#0070C0', 'white', 9)
arrow(ax, 16.5, 23.85, 16.5, 23.0)
arrow(ax, 16.5, 23.0, 11.5, 22.5, '#333333')

draw_rect(ax, 11, 21.8, 8.0, 1.2,
          '4. Translation + Simplification Back to User\nEnglish -> native language | Simple Mode adds analogy\ne.g. "API = power outlet - device does not need to know how electricity works"', '#8E44AD', 'white', 9)
arrow(ax, 11, 21.15, 11, 20.5)

draw_rect(ax, 5.5, 19.8, 5.5, 1.2,
          'Audio Output\nAnswer spoken in native\nlanguage via VIBE voice\nPrivate to user', '#27AE60', 'white', 9)
draw_rect(ax, 16.5, 19.8, 5.5, 1.2,
          'Text Output\nSimplified text + analogy\nin user caption pane\nBookmarkable for summary', '#0070C0', 'white', 9)
arrow(ax, 11 - 2.0, 20.5, 5.5, 20.45, '#333333')
arrow(ax, 11 + 2.0, 20.5, 16.5, 20.45, '#333333')

arrow(ax, 5.5, 19.15, 5.5, 18.3)
arrow(ax, 16.5, 19.15, 16.5, 18.3)
arrow(ax, 5.5, 18.3, 10.5, 17.7, '#333333')
arrow(ax, 16.5, 18.3, 11.5, 17.7, '#333333')

p_end = mpatches.FancyBboxPatch((0.5, 10.5), 21.0, 7.0, boxstyle="round,pad=0.15",
                                  facecolor='#D35400', edgecolor='#D35400', linewidth=2, alpha=0.08)
ax.add_patch(p_end)
ax.text(1.0, 17.1, 'E: END & LOGGING', fontsize=13, fontweight='bold', color='#D35400')

draw_oval(ax, 11, 17.0, 5.0, 0.8, 'MEETING ENDS', '#D35400', 'white', 12)
arrow(ax, 11, 16.55, 11, 15.8)
arrow(ax, 11, 15.8, 5.5, 15.25, '#333333')
arrow(ax, 11, 15.8, 16.5, 15.25, '#333333')

draw_rect(ax, 5.5, 14.5, 5.5, 1.2,
          'VIBE Transcript\nOriginal language layer\nEnglish translation layer\nSimplified text layer\nTimestamps + speaker IDs', '#D35400', 'white', 8)

draw_rect(ax, 11, 14.5, 5.5, 1.2,
          'VIBE Summary Pack\nKey Q&A in native language\nSimple explanations + examples\nDownloadable per-user\nShareable via Webex/email', '#D35400', 'white', 8)

draw_rect(ax, 16.5, 14.5, 5.5, 1.2,
          'Session Analytics\nVoice clarity score trend\nTranslation accuracy log\nQ&A resolution rate\nVIBE usage breakdown', '#D35400', 'white', 8)

arrow(ax, 5.5, 13.85, 5.5, 13.2)
arrow(ax, 11, 13.85, 11, 13.2)
arrow(ax, 16.5, 13.85, 16.5, 13.2)

splunk_vibe = mpatches.FancyBboxPatch((0.8, 12.0), 20.4, 1.5, boxstyle="round,pad=0.1",
                                        facecolor='#002060', edgecolor='black', linewidth=2.5, alpha=0.95)
ax.add_patch(splunk_vibe)
ax.text(11, 13.1, 'SPLUNK OBSERVABILITY & GOVERNANCE FOR VIBE',
        ha='center', fontsize=11, fontweight='bold', color='#FFD700')
ax.text(11, 12.4, 'Voice quality metrics per session  |  Translation accuracy tracking  |  TTS usage audit trail  |  Q&A resolution analytics  |  Anomaly detection on VIBE actions',
        ha='center', fontsize=8, fontweight='bold', color='white')

arrow(ax, 11, 11.95, 11, 11.3)

draw_cyl(ax, 11, 10.5, 10.0, 1.5,
         'PRIVACY GUARANTEE: Transparency & Trust Layer - Always Active\n"Spoken by VIBE for [User]" on every TTS | Full audit trail | Zero data retention option\nVIBE never impersonates: voice persona is distinct from user\'s actual voice', '#002060', 'white', 9)

arrow(ax, 11, 9.65, 11, 9.1)
draw_oval(ax, 11, 8.6, 6.0, 0.9, 'END - VIBE SESSION COMPLETE', '#002060', 'white', 12)

comp_box = mpatches.FancyBboxPatch((0.5, 0.5), 21.0, 7.8, boxstyle="round,pad=0.1",
                                     facecolor='#F8F9FA', edgecolor='#002060', linewidth=2.5)
ax.add_patch(comp_box)
ax.text(11, 7.9, 'VIBE / VEL - COMPONENT ARCHITECTURE OVERVIEW', ha='center',
        fontsize=13, fontweight='bold', color='#002060')

col_w = 4.8
col_h = 5.5
col_x = [1.0, 6.0, 11.0, 16.0]
col_titles = ['Audio Layer', 'AI / NLP Layer', 'Type-to-Speak Layer', 'Output & Splunk Logging']
col_colors = ['#27AE60', '#0070C0', '#1A5276', '#D35400']
col_items = [
    ['Webex AI Codec', 'DNN Noise Removal', 'Echo Cancellation', 'Auto Gain Control', 'Voice Boost EQ', 'Per-Speaker Separation'],
    ['ASR (Whisper/Cisco)', 'Neural Machine Translation', 'Jargon Simplification LLM', 'Intent & Domain Detection', 'Neural TTS Synthesis', 'VIBE Persona Voice Model'],
    ['Text Input Panel (UI)', 'Language Detection', 'Polish / Simplify Mode', 'TTS Agent Voice', 'Caption + Chat Sync', '"via VIBE" Tag'],
    ['Per-User Caption Stream', 'VIBE Transcript (3 layers)', 'Splunk VIBE Dashboard', 'Session Analytics to Splunk', 'Audit Log (all actions)', 'Zero-Retention Option'],
]

for cx_off, title, color, items in zip(col_x, col_titles, col_colors, col_items):
    cb = mpatches.FancyBboxPatch((cx_off, 1.0), col_w, col_h + 0.5, boxstyle="round,pad=0.08",
                                   facecolor=color, edgecolor='black', linewidth=1.5, alpha=0.15)
    ax.add_patch(cb)
    ax.text(cx_off + col_w/2, 6.8, title, ha='center', fontsize=10, fontweight='bold', color=color)
    for j, item in enumerate(items):
        ax.text(cx_off + col_w/2, 6.0 - j * 0.75, item, ha='center', fontsize=8, color='#333333')

plt.tight_layout()
plt.savefig('cisco_case/figures/flowchart_2_vibe.png', dpi=200, bbox_inches='tight')
plt.close()
print("Flowchart 2 (VIBE) created")

# ============================================================
# FLOWCHART 3: Secure AI Agent Marketplace - 3-Lane Architecture
# Developer Journey | Admin Journey | User Journey + Splunk
# ============================================================
fig, ax = plt.subplots(figsize=(22, 56))
ax.set_xlim(0, 22)
ax.set_ylim(0, 56)
ax.axis('off')

ax.text(11, 55.3, 'Solution 3: Webex Secure AI Agent Marketplace',
        ha='center', fontsize=21, fontweight='bold', color='#002060')
ax.text(11, 54.7, 'Build \u2192 Certify \u2192 Deploy \u2192 Monitor  |  Three-Lane Architecture  |  100s of Third-Party Integrations',
        ha='center', fontsize=12, color='#555555')

draw_symbol_directory(ax, 0.3, 49.5, 6.5, 4.8)

DX = 3.8
AX = 11.0
UX = 18.2
LW = 6.0

lane_specs = [
    (DX, '#E8F4FD', '#1A5276', 'DEVELOPER\nJOURNEY', '(Build & Certify)'),
    (AX, '#FFF3E0', '#D35400', 'ADMIN\nJOURNEY', '(Deploy & Control)'),
    (UX, '#F3E5F5', '#8E44AD', 'USER\nJOURNEY', '(Discover & Use)'),
]

for cx, bg_color, title_color, title, subtitle in lane_specs:
    rect = mpatches.FancyBboxPatch((cx - LW/2, 4.0), LW, 45.5, boxstyle="round,pad=0.1",
                                    facecolor=bg_color, edgecolor='#999999', linewidth=1.5, alpha=0.5)
    ax.add_patch(rect)
    ax.text(cx, 49.2, title, ha='center', fontsize=13, fontweight='bold', color=title_color, va='center')
    ax.text(cx, 48.2, subtitle, ha='center', fontsize=9, color='#666666')

draw_oval(ax, DX, 47.0, 5.2, 0.8, 'Developer Decides\nto Build Agent', '#1A5276', 'white', 10)
arrow(ax, DX, 46.55, DX, 45.9)

draw_rect(ax, DX, 45.3, 5.2, 1.0,
          '1. Register on Dev Portal\nAccept Cisco terms & SDK\nagreement, choose category', '#1A5276', 'white', 9)
arrow(ax, DX, 44.75, DX, 44.1)

draw_rect(ax, DX, 43.5, 5.2, 1.0,
          '2. Download SDK & Templates\nPython / JS SDK | Templates:\nListener, Executor, Retriever, Sender', '#1A5276', 'white', 9)
arrow(ax, DX, 42.95, DX, 42.3)

draw_rect(ax, DX, 41.7, 5.2, 1.0,
          '3. Build Agent Logic\nWebex Meeting API: transcription,\ncontext | A2A Protocol: external\ntool integration', '#0070C0', 'white', 8)
arrow(ax, DX, 41.15, DX, 40.5)

draw_rect(ax, DX, 39.9, 5.2, 1.0,
          '4. Test in Webex Sandbox\nSimulated meeting | Tests: latency,\naccuracy, error handling, load', '#0070C0', 'white', 9)
arrow(ax, DX, 39.35, DX, 38.5)

draw_diamond(ax, DX, 37.5, 1.8, 'Tests\nPass?', '#F39C12', 'black', 9)

ax.text(DX - 2.0, 37.5, 'NO', fontsize=10, fontweight='bold', color='#E74C3C')
arrow(ax, DX - 0.9, 37.5, DX - 2.5, 37.5, '#E74C3C', 2)
arrow(ax, DX - 2.5, 37.5, DX - 2.5, 41.7, '#E74C3C', 2)
arrow(ax, DX - 2.5, 41.7, DX - 2.8, 41.7, '#E74C3C', 2)
ax.text(DX + 1.5, 37.5, 'YES', fontsize=10, fontweight='bold', color='#27AE60')
arrow(ax, DX, 36.6, DX, 35.9)

draw_rect(ax, DX, 35.3, 5.2, 1.0,
          '5. Submit for Certification\nAgent code + config + docs\nuploaded to Cisco pipeline', '#1A5276', 'white', 9)
arrow(ax, DX, 34.75, DX, 34.1)

draw_dashed_box(ax, DX - 2.8, 28.0, 5.6, 5.8, 'CISCO CERTIFICATION', '#27AE60')

draw_rect(ax, DX, 33.3, 5.0, 0.9,
          '6a. Static Code Analysis\nVulnerabilities, backdoors,\ndata-leak patterns', '#27AE60', 'white', 8)
arrow(ax, DX, 32.8, DX, 32.2)

draw_rect(ax, DX, 31.6, 5.0, 0.9,
          '6b. Permission Review\nDeclared vs actual data access\nZero-trust enforcement', '#27AE60', 'white', 8)
arrow(ax, DX, 31.1, DX, 30.5)

draw_rect(ax, DX, 29.9, 5.0, 0.9,
          '6c. Performance + Compliance\nLatency, load, SOC2, HIPAA,\nFedRAMP, GDPR checks', '#27AE60', 'white', 8)
arrow(ax, DX, 29.4, DX, 28.6)

draw_diamond(ax, DX, 27.5, 1.8, 'Cisco\nCertified?', '#F39C12', 'black', 9)

ax.text(DX - 2.0, 27.5, 'FAIL', fontsize=10, fontweight='bold', color='#E74C3C')
arrow(ax, DX - 0.9, 27.5, DX - 2.5, 27.5, '#E74C3C', 2)

ax.text(DX + 1.5, 27.5, 'PASS', fontsize=10, fontweight='bold', color='#27AE60')
arrow(ax, DX, 26.6, DX, 25.9)

draw_rect(ax, DX, 25.3, 5.2, 1.0,
          'Cisco Verified Agent Badge\nListed in Webex AI Agent Store\nName, vendor, badge, ratings', '#27AE60', 'white', 9)

arrow(ax, DX + 2.6, 25.3, AX - 2.5, 25.3, '#333333', 2)

draw_oval(ax, AX, 47.0, 5.2, 0.8, 'Enterprise IT Admin\nBrowses Agent Store', '#D35400', 'white', 10)
arrow(ax, AX, 46.55, AX, 45.9)

draw_rect(ax, AX, 45.3, 5.2, 1.0,
          '1. Browse & Filter Agents\nIndustry: Healthcare, Finance,\nGov, Mfg | Compliance level', '#D35400', 'white', 9)
arrow(ax, AX, 44.75, AX, 44.1)

draw_rect(ax, AX, 43.5, 5.2, 1.0,
          '2. Review Agent Details\nVendor, use case, Cisco Verified\nbadge, ratings, pricing, data scope', '#D35400', 'white', 9)
arrow(ax, AX, 42.95, AX, 42.3)

draw_rect(ax, AX, 41.7, 5.2, 1.0,
          '3. Configure Scope & Permissions\nAssign to: orgs, teams, users\nData: read-only / limited / full write', '#0070C0', 'white', 9)
arrow(ax, AX, 41.15, AX, 40.5)

draw_rect(ax, AX, 39.9, 5.2, 1.0,
          '4. Set Approval Workflows\nHigh-risk writes -> manager approval\nUsage quotas & budget caps', '#0070C0', 'white', 9)
arrow(ax, AX, 39.35, AX, 38.5)

draw_diamond(ax, AX, 37.5, 1.8, 'Admin\nApproves?', '#F39C12', 'black', 9)

ax.text(AX - 2.0, 37.5, 'NO', fontsize=10, fontweight='bold', color='#E74C3C')
arrow(ax, AX - 0.9, 37.5, AX - 2.0, 37.5, '#E74C3C', 2)

ax.text(AX + 1.5, 37.5, 'YES', fontsize=10, fontweight='bold', color='#27AE60')
arrow(ax, AX, 36.6, AX, 35.9)

draw_rect(ax, AX, 35.3, 5.2, 1.0,
          '5. Activate in Webex Cloud\nIsolated container deployment\nZero-trust identity layer controls', '#D35400', 'white', 9)
arrow(ax, AX, 34.75, AX, 34.1)

draw_rect(ax, AX, 33.5, 5.2, 1.0,
          '6. Pilot Rollout\nDeploy to pilot group first\nMeasure: time saved, ticket rate,\nuser satisfaction', '#D35400', 'white', 9)
arrow(ax, AX, 32.95, AX, 32.3)

draw_rect(ax, AX, 31.7, 5.2, 1.0,
          '7. Monitor Agent Activity\nPer-agent dashboard: invocations,\nsuccess rate, errors\nUsage by org / team / user', '#8E44AD', 'white', 9)
arrow(ax, AX, 31.15, AX, 30.4)

draw_diamond(ax, AX, 29.4, 1.8, 'Anomaly /\nAlert?', '#F39C12', 'black', 9)

ax.text(AX + 1.5, 29.4, 'YES', fontsize=10, fontweight='bold', color='#E74C3C')
arrow(ax, AX + 0.9, 29.4, AX + 2.0, 29.4, '#E74C3C', 2)
ax.text(AX + 2.5, 29.4, 'Kill-Switch\n(instant disable)', fontsize=8, fontweight='bold', color='#E74C3C', ha='left',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#FADBD8', edgecolor='#E74C3C', linewidth=1.5))

ax.text(AX - 2.0, 29.4, 'NO', fontsize=10, fontweight='bold', color='#27AE60')
arrow(ax, AX - 0.9, 29.4, AX - 2.0, 29.4, '#27AE60', 2)

arrow(ax, AX, 28.5, AX, 27.8)

draw_rect(ax, AX, 27.2, 5.2, 1.0,
          '8. Adjust Scope or Quotas\nUpdate permissions, budget caps\nFull audit trail retained', '#D35400', 'white', 9)

arrow(ax, AX + 2.6, 35.3, UX - 2.5, 35.3, '#333333', 2)

draw_oval(ax, UX, 47.0, 5.2, 0.8, 'User Discovers\nAgents in Webex', '#8E44AD', 'white', 10)
arrow(ax, UX, 46.55, UX, 45.9)

draw_rect(ax, UX, 45.3, 5.2, 1.0,
          '1. "AI Agents" Tab in Webex\nIn-meeting suggestion banner\nBrowse by use case / industry', '#8E44AD', 'white', 9)
arrow(ax, UX, 44.75, UX, 44.1)

draw_rect(ax, UX, 43.5, 5.2, 1.0,
          '2. Reviews & Installs Agent\nSees permissions: "Can read\ntranscript, can create Jira tickets"\nAccepts Cisco data notice', '#8E44AD', 'white', 9)
arrow(ax, UX, 42.95, UX, 42.3)

draw_rect(ax, UX, 41.7, 5.2, 1.0,
          '3. Uses Agent in Live Meeting\nPresenter says: "Create a Jira\nticket for the login bug"\nAgent listens in real-time', '#0070C0', 'white', 9)
arrow(ax, UX, 41.15, UX, 40.5)

draw_rect(ax, UX, 39.9, 5.2, 1.0,
          '4. Agent Detects Intent & Drafts\nDetects task from transcript\nPulls Jira project + sprint context\nDrafts full ticket inline in Webex', '#0070C0', 'white', 9)
arrow(ax, UX, 39.35, UX, 38.5)

draw_diamond(ax, UX, 37.5, 1.8, 'Approve\nDraft?', '#F39C12', 'black', 9)

ax.text(UX - 2.0, 37.5, 'REJECT', fontsize=10, fontweight='bold', color='#E74C3C')
arrow(ax, UX - 0.9, 37.5, UX - 2.0, 37.5, '#E74C3C', 2)

ax.text(UX + 1.5, 37.5, 'APPROVE', fontsize=10, fontweight='bold', color='#27AE60')
arrow(ax, UX, 36.6, UX, 35.9)

draw_rect(ax, UX, 35.3, 5.2, 1.0,
          '5. In-Meeting Approval Card\nComplete draft shown inline\nApprove | Edit | Reject controls', '#27AE60', 'white', 9)
arrow(ax, UX, 34.75, UX, 34.1)

draw_rect(ax, UX, 33.5, 5.2, 1.0,
          '6. Agent Executes Action\nAuthenticated API call to Jira /\nSalesforce / DocuSign / ServiceNow\nSplunk logs full execution chain', '#E74C3C', 'white', 9)
arrow(ax, UX, 32.95, UX, 32.3)

draw_rect(ax, UX, 31.7, 5.2, 1.0,
          '7. Webex Confirms in Chat\n"Jira ticket WEBAPP-2026-347\ncreated. Assigned to Sarah Chen.\nPriority: High."', '#0070C0', 'white', 9)
arrow(ax, UX, 31.15, UX, 30.5)

draw_rect(ax, UX, 29.9, 5.2, 1.0,
          '8. User Manages Agents\n"My Agents" panel: disable,\nupdate, downgrade, view usage', '#8E44AD', 'white', 9)

splunk_box = mpatches.FancyBboxPatch((0.8, 18.0), 20.4, 5.5, boxstyle="round,pad=0.15",
                                       facecolor='#002060', edgecolor='black', linewidth=2.5, alpha=0.95)
ax.add_patch(splunk_box)
ax.text(11, 23.1, 'SPLUNK OBSERVABILITY & GOVERNANCE - MONITORING ALL THREE LANES IN REAL TIME',
        ha='center', fontsize=12, fontweight='bold', color='#FFD700')

sp_cols = [
    ('Real-Time Metrics', ['Agent invocations/hour', 'Success/error rate per agent', 'API latency percentiles', 'Usage by org/team/user', 'Active agent count']),
    ('Anomaly Detection', ['Unusual data-access volume', 'Permission scope violations', 'Performance regression alerts', 'Unauthorized API attempts', 'Cross-tenant data flags']),
    ('Governance Controls', ['Instant kill-switch per agent', 'Full audit trail retained', 'Policy enforcement rules', 'Manager approval routing', 'Compliance report export']),
    ('Billing & Revenue', ['Usage tracked per agent', 'Pay-per-use or subscription', '70/30 revenue split', 'Monthly invoice generation', 'Developer payout dashboard']),
]

for i, (title, items) in enumerate(sp_cols):
    sx = 1.5 + i * 5.1
    ax.text(sx + 2.0, 22.3, title, ha='center', fontsize=10, fontweight='bold', color='#FFD700')
    for j, item in enumerate(items):
        ax.text(sx + 2.0, 21.5 - j * 0.65, item, ha='center', fontsize=8, color='white')

agent_box = mpatches.FancyBboxPatch((0.8, 10.5), 20.4, 7.0, boxstyle="round,pad=0.15",
                                      facecolor='#F8F9FA', edgecolor='#002060', linewidth=2.5)
ax.add_patch(agent_box)
ax.text(11, 17.1, 'AGENT EXAMPLES & INDUSTRY COVERAGE', ha='center',
        fontsize=13, fontweight='bold', color='#002060')

ax.text(4.0, 16.2, 'Agent Templates', ha='center', fontsize=11, fontweight='bold', color='#1A5276')
templates = ['CRM Updater', 'Ticket Creator', 'Doc Generator', 'Calendar Scheduler', 'Contract Flow (DocuSign)', 'VIBE Voice Agent (1st-party)']
for j, t in enumerate(templates):
    ax.text(4.0, 15.5 - j * 0.7, t, ha='center', fontsize=9, color='#333333')

ax.text(11.0, 16.2, 'Industry Filters', ha='center', fontsize=11, fontweight='bold', color='#D35400')
industries = ['Healthcare', 'Finance', 'Government', 'Manufacturing', 'Sales / HR / Engineering', 'Support / ITSM']
for j, ind in enumerate(industries):
    ax.text(11.0, 15.5 - j * 0.7, ind, ha='center', fontsize=9, color='#333333')

ax.text(18.0, 16.2, 'Live Agent Examples', ha='center', fontsize=11, fontweight='bold', color='#8E44AD')
live_agents = ['Jira Sprint Agent', 'Salesforce Update Agent', 'DocuSign Flow Agent', 'ServiceNow Incident Agent', 'GitHub PR Agent', 'Slack Notification Agent']
for j, la in enumerate(live_agents):
    ax.text(18.0, 15.5 - j * 0.7, la, ha='center', fontsize=9, color='#333333')

arch_box = mpatches.FancyBboxPatch((0.8, 4.5), 20.4, 5.5, boxstyle="round,pad=0.15",
                                     facecolor='#F8F9FA', edgecolor='#002060', linewidth=2.5)
ax.add_patch(arch_box)
ax.text(11, 9.6, 'PLATFORM ARCHITECTURE STACK', ha='center',
        fontsize=13, fontweight='bold', color='#002060')

arch_cols = [
    ('Developer Platform', '#1A5276', ['Webex AI Agent Dev Portal', 'Python / JS SDK', 'Webex Meeting API', 'A2A Protocol support', 'Sandbox environment', 'Certification submission UI']),
    ('Security & Compliance', '#27AE60', ['Cisco Zero Trust Identity', 'Isolated container execution', 'Static code analysis pipeline', 'SOC2/HIPAA/FedRAMP/GDPR', 'Cisco Verified Agent badge', 'Splunk SIEM integration']),
    ('User Experience Layer', '#8E44AD', ['Webex AI Agents tab (store)', 'In-meeting agent suggestions', 'In-meeting approval cards', '"AI" label on all agent actions', 'My Agents management panel', 'Chat confirmation threads']),
]

for i, (title, color, items) in enumerate(arch_cols):
    acx = 1.5 + i * 7.0
    ax.text(acx + 3.0, 9.0, title, ha='center', fontsize=10, fontweight='bold', color=color)
    for j, item in enumerate(items):
        ax.text(acx + 3.0, 8.3 - j * 0.6, item, ha='center', fontsize=8, color='#333333')

mr = mpatches.FancyBboxPatch((0.8, 1.5), 20.4, 2.5, boxstyle='round,pad=0.1',
                               facecolor='#002060', edgecolor='black', linewidth=2)
ax.add_patch(mr)
ax.text(11, 3.4, 'PROJECTED IMPACT', ha='center', fontsize=12, fontweight='bold', color='#FFD700')
ax.text(11, 2.7, '500+ certified agents Year 1  |  $150M GMV by FY2028  |  3x ecosystem growth  |  85% renewal rate',
        ha='center', fontsize=10, fontweight='bold', color='white')
ax.text(11, 2.1, 'New revenue stream: $50M annual marketplace commission by FY2029  |  Hundreds of third-party integrations',
        ha='center', fontsize=9, fontweight='bold', color='white')

plt.tight_layout()
plt.savefig('cisco_case/figures/flowchart_3_marketplace.png', dpi=200, bbox_inches='tight')
plt.close()
print("Flowchart 3 (Marketplace - 3 Lane) created")


# ============================================================
# NOW CREATE THE PDF DOCUMENT
# ============================================================

class PDF(FPDF):
    def header(self):
        pass
    def footer(self):
        self.set_y(-15)
        self.set_font('Times', 'I', 10)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

pdf = PDF('P', 'mm', 'Letter')
pdf.set_auto_page_break(auto=True, margin=25)
pdf.set_left_margin(25.4)
pdf.set_right_margin(25.4)

W = 215.9 - 25.4 - 25.4
LH = 5
INDENT = 10
LM = 25.4

def heading(pdf, text):
    pdf.set_left_margin(LM)
    pdf.set_font('Times', 'B', 14)
    pdf.cell(0, LH+1, text, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(LH)

def subheading(pdf, text):
    pdf.set_left_margin(LM)
    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, LH, text, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

def body(pdf, text):
    pdf.set_left_margin(LM)
    pdf.set_x(LM)
    pdf.set_font('Times', '', 12)
    pdf.multi_cell(0, LH, text)
    pdf.ln(1)

def body_bold(pdf, text):
    pdf.set_left_margin(LM)
    pdf.set_x(LM)
    pdf.set_font('Times', 'B', 12)
    pdf.multi_cell(0, LH, text)
    pdf.ln(1)

def bullet(pdf, text):
    pdf.set_font('Times', '', 12)
    pdf.set_left_margin(LM)
    pdf.set_x(LM + INDENT)
    pdf.set_left_margin(LM + INDENT)
    pdf.multi_cell(0, LH, f'- {text}')
    pdf.set_left_margin(LM)

def sub_bullet(pdf, text):
    pdf.set_font('Times', '', 12)
    pdf.set_left_margin(LM)
    pdf.set_x(LM + INDENT * 2)
    pdf.set_left_margin(LM + INDENT * 2)
    pdf.multi_cell(0, LH, f'- {text}')
    pdf.set_left_margin(LM)

def source_note(pdf, text):
    pdf.set_left_margin(LM)
    pdf.set_x(LM)
    pdf.set_font('Times', 'I', 11)
    pdf.multi_cell(0, LH, text)
    pdf.ln(1)

# ============================================================
# COVER PAGE
# ============================================================
pdf.add_page()
pdf.ln(30)
pdf.set_font('Times', 'B', 16)
pdf.cell(0, 8, 'Repositioning Cisco Webex for the Next Phase of Hybrid Work', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(4)
pdf.set_font('Times', 'B', 14)
pdf.cell(0, 7, 'Three Strategic Problems & AI-Powered Solutions', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)
pdf.set_font('Times', '', 12)
pdf.cell(0, LH, 'Spring 2026 Cisco x WiB x SWE Case Competition', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(LH * 4)
pdf.set_font('Times', 'B', 12)
pdf.cell(0, LH, 'Team Members:', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(LH)
pdf.set_font('Times', '', 12)
for name in ['Lana Jalal Gidan', 'Krishianjan Lanka', 'Nur Ali', 'Zoe Zimmermann']:
    pdf.cell(0, LH, name, align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(LH * 3)
pdf.set_font('Times', '', 12)
pdf.cell(0, LH, 'Watson College of Engineering and Applied Science', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, LH, 'Binghamton University', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(LH)
pdf.cell(0, LH, 'March 2026', align='C', new_x="LMARGIN", new_y="NEXT")

# ============================================================
# EXECUTIVE SUMMARY
# ============================================================
pdf.add_page()
heading(pdf, 'Executive Summary')

body(pdf, 'Cisco Webex faces three critical strategic problems that prevent it from competing effectively against Microsoft Teams and Zoom in the next phase of hybrid work. This document identifies each problem with specificity, proposes a targeted AI-powered solution backed by Cisco\'s existing capabilities, provides detailed technical flowcharts, and assesses the technical feasibility, constraints, scalability, implementation risks, and system-level trade-offs of each solution.')

body(pdf, 'The three problems and their corresponding solutions are:')

bullet(pdf, 'Problem 1: Webex AI cannot execute or operationalize meetings. The AI Assistant is passive: it summarizes and transcribes but does not prepare users beforehand, execute tasks during meetings, or follow up afterward. Solution: Deploy the Webex AI Meeting Prep & Workflow Orchestrator, a Prepare-Perceive-Reason-Act-Follow-Up system that covers the full meeting lifecycle with agentic AI and human-in-the-loop verification.')

bullet(pdf, 'Problem 2: Webex meetings exclude non-native speakers and non-technical participants. Language barriers, technical jargon, poor audio quality, and inability to speak in noisy or sensitive environments create participation gaps that reduce meeting value. Solution: Build VIBE (Voice & Language Intelligence Layer), a real-time in-meeting AI layer that boosts voice, translates between languages, simplifies jargon, and enables type-to-speak.')

bullet(pdf, 'Problem 3: Webex has a weaker, less strategic developer ecosystem. Teams has 2,000+ integrations, Zoom has 2,500+, and neither has launched a dedicated AI agent development platform. Solution: Launch the Secure AI Agent Marketplace with a developer SDK, Cisco security certification pipeline, and enterprise deployment infrastructure supporting hundreds of third-party integrations.')

pdf.ln(2)
body(pdf, 'Each solution leverages Cisco\'s existing competitive advantages: the $7.98 billion R&D budget, the $28 billion Splunk acquisition for enterprise data observability, FedRAMP/HIPAA/SOC 2 Type II security certifications, and the Webex AI Codec\'s proven ML engineering capabilities.')

# ============================================================
# PROBLEM 1
# ============================================================
pdf.add_page()
heading(pdf, 'Problem 1: Webex AI Cannot Execute or Operationalize Meetings')

subheading(pdf, 'Problem Definition')
body(pdf, 'The Webex AI Assistant is still primarily passive: it generates meeting summaries, real-time transcription, and language translation. These features are now baseline across collaboration platforms and do not meaningfully change how work gets done. Webex AI tells users what happened in a meeting, but it neither prepares them effectively beforehand nor acts on the decisions made during the meeting.')

body(pdf, 'This creates a measurable productivity gap across the full meeting lifecycle:')
bullet(pdf, 'Before meetings, users manually prepare slides, agendas, and talking points, often under time pressure and without structured guidance on what stakeholders actually care about.')
bullet(pdf, 'During meetings, when a manager says "Create a Jira ticket for the login bug Sarah found" or "Update the Salesforce opportunity for ACME," nothing happens automatically.')
bullet(pdf, 'After meetings, presenters must recall details, open multiple tools (Jira, Salesforce, ServiceNow), create or update items by hand, and send follow-up answers to questions they could not address live.')
body(pdf, 'Each of these steps takes time and introduces errors from memory decay and context switching. Manually creating a single Jira ticket from meeting notes can take 8-12 minutes; preparing an entire deck for a stakeholder meeting can take hours. Across dozens of meetings per week, this compounds into lost time and missed follow-ups.')

subheading(pdf, 'Competitive Gap Analysis')
body(pdf, 'Microsoft Teams with Copilot can draft Word documents from meeting context, create PowerPoint presentations, generate Excel formulas, and build Power Automate workflows that connect across the Microsoft Graph. Copilot uses organizational context from emails, files, calendars, and chats to proactively suggest content and automate steps before and after meetings.')

body(pdf, 'Zoom AI Companion 2.0 similarly includes early agentic features: it drafts documents in Zoom Docs, automatically generates action items with assignees, updates CRM records through Zoom Revenue Accelerator, and drives workflow automation inside the Zoom ecosystem at no additional cost to paid users.')

body(pdf, 'In contrast, Webex AI is largely descriptive. It can summarize and transcribe but does not proactively help users prepare for meetings, execute tasks in third-party systems, or close the loop on unanswered questions. The gap is not incremental; it is categorical. Competitors have AI that prepares and does work. Webex has AI that describes work, leaving humans to manually perform everything around the meeting.')

subheading(pdf, 'Business Impact of the Problem')
bullet(pdf, 'User engagement stagnation: Users treat Webex as a "join and talk" tool rather than a productivity engine. Because Webex does not help them prepare, execute, or follow up, they spend less time in the product and more time in surrounding tools, reducing stickiness and increasing churn risk.')
bullet(pdf, 'Enterprise deal losses: In RFPs, IT decision-makers increasingly compare end-to-end AI workflows, not just summaries. When buyers see Copilot and Zoom AI Companion drafting content and taking actions while Webex AI remains passive, Webex loses competitive evaluations.')
bullet(pdf, 'Revenue ceiling: Without differentiated, action-oriented AI, Webex\'s collaboration revenue faces a growth ceiling as the market shifts toward platforms that can reduce prep time, automate task execution, and tie into enterprise workflows.')
pdf.ln(2)

subheading(pdf, 'Solution 1: Webex AI Meeting Prep & Workflow Orchestrator')

body(pdf, 'Transform the Webex AI Assistant from a passive summarization tool into an agentic AI system that: (1) prepares users before the meeting with agendas, insights, auto-generated slides, and predicted questions; (2) perceives task intents and decisions during the meeting from live conversation; (3) reasons over enterprise context using secure integrations and organizational rules; (4) acts by drafting complete task artifacts and executing approved actions across third-party platforms; and (5) follows up on unanswered questions after the meeting with structured, trackable responses. The system operates on a Prepare-Perceive-Reason-Act-Follow-Up architecture with mandatory human-in-the-loop verification for all external actions.')

body_bold(pdf, 'PREPARE Phase: AI Meeting Prep & Slide Assistant')
body(pdf, 'Before the meeting begins, Webex AI proactively assists the presenter:')
bullet(pdf, 'Context Ingestion: When a meeting is scheduled, Webex ingests the title, invite description, participant list, and attached documents, and where authorized, relevant records from CRM, project tools, and past meeting transcripts.')
bullet(pdf, 'Insight & Agenda Suggestions: The AI generates key insights and metrics likely to matter to the invited stakeholders, along with a suggested agenda (sections such as "Status," "Risks," "Decisions Needed," "Q&A").')
bullet(pdf, 'Prep Checklist: The agent creates a structured checklist (e.g., "Upload latest metrics deck," "Confirm owner for customer escalation," "Prepare answer on Q3 budget impact").')
bullet(pdf, 'Auto-Slide Generation: If the presenter opts in, Webex AI generates a first-draft slide deck using meeting context and enterprise data (CRM pipeline, Jira issues, financial metrics), organized into the proposed agenda.')
bullet(pdf, 'Predicted Q&A: The AI predicts likely questions based on role, history, and topic, and suggests draft answers the presenter can review, refine, or reject.')
pdf.ln(1)

body_bold(pdf, 'PERCEIVE Phase: Webex AI Codec ML Pipeline')
body(pdf, 'During the live meeting, the existing Webex AI Codec serves as the perception layer:')
bullet(pdf, 'Deep Neural Network (DNN) Noise Removal: Real-time models remove background noise (keyboards, dogs, construction, etc.), isolating clean speech.')
bullet(pdf, 'Neural Speech Synthesis Codec: Cleaned audio is compressed using a neural codec to maintain high quality even on low bandwidth.')
bullet(pdf, 'Real-Time Media Models (RMM): AI upscales low-resolution video, separates individual speakers, and detects gestures/reactions.')
bullet(pdf, 'NLP Engine: Speech is converted to text with real-time transcription and translation. The NLP layer identifies task-related statements, decisions, commitments, and live occurrences of predicted questions from the PREPARE phase.')
pdf.ln(1)

body_bold(pdf, 'REASON Phase: Context Retrieval and Task Planning')
bullet(pdf, 'Context Retrieval via Agent-to-Agent (A2A) Protocols: Webex AI communicates with external system agents (Jira, Salesforce, GitHub, ServiceNow) through standardized protocols to retrieve relevant context.')
bullet(pdf, 'Cisco Secure Data Fabric & Observability: All retrieval passes through Cisco\'s zero-trust identity and access layer. Every call is monitored via Splunk observability tools.')
bullet(pdf, 'LLM-Based Task and Answer Planning: A large language model synthesizes live meeting context, retrieved system data, and organizational policies to generate complete task drafts or follow-up plans.')
pdf.ln(1)

body_bold(pdf, 'ACT Phase: In-Meeting Human Verification and Execution')
bullet(pdf, 'In-Meeting Draft Cards: The user sees a non-disruptive overlay showing the fully drafted task artifact or follow-up response.')
bullet(pdf, 'Approve / Edit / Reject Controls: The user can approve, edit, or reject each draft.')
bullet(pdf, 'Secure Execution & Logging: On approval, the agent executes through authenticated API calls. Every step is logged for auditing and compliance.')
bullet(pdf, 'Meeting Chat Confirmation: Webex posts a concise confirmation back into the meeting chat.')
pdf.ln(1)

body_bold(pdf, 'FOLLOW-UP Phase: Structured Q&A and Post-Meeting Delivery')
bullet(pdf, 'Unanswered Question Detection: The system identifies questions that were asked but not answered or explicitly deferred.')
bullet(pdf, 'Q&A Follow-Up Drafts: For each unanswered question, the AI drafts a suggested response and presents it to the owner for approval/edit.')
bullet(pdf, 'Multi-Channel Delivery: Approved answers are sent to participants via Webex spaces, email, or integrated systems, optionally simplified for non-technical speakers.')
bullet(pdf, 'Visibility & Observability: All follow-up actions are logged and visible through Splunk dashboards.')
pdf.ln(1)

subheading(pdf, 'Why This Enhanced Solution Wins')
body(pdf, 'This solution brings Webex from a passive summarization tool to an agentic AI system that covers the full meeting lifecycle. Where Microsoft Copilot and Zoom AI Companion focus primarily on content generation and partial task execution inside their own ecosystems, Webex differentiates by owning the full Prepare-Perceive-Reason-Act-Follow-Up loop with strong guardrails and regulated-industry readiness.')

subheading(pdf, 'Expected Impact')
bullet(pdf, 'Reduces manual post-meeting data entry by 15 minutes per meeting')
bullet(pdf, '25% meeting-to-action conversion rate (vs. current ~5% industry average)')
bullet(pdf, '40% workflow automation rate within 12 months of deployment')
bullet(pdf, '85% task completion accuracy with human-in-the-loop verification')
bullet(pdf, '90%+ Q&A resolution rate through structured post-meeting follow-up')
pdf.ln(2)
source_note(pdf, 'Sources: Cisco FY2024 10-K; Webex AI Codec documentation; MarketsandMarkets Agentic AI Market Report 2024; Microsoft Copilot & Zoom AI Companion product documentation.')

subheading(pdf, 'Solution 1 Flowchart: Prepare-Perceive-Reason-Act-Follow-Up')
body(pdf, 'The following flowchart details the complete five-phase architecture including pre-meeting AI prep, the AI Codec ML pipeline, data fabric integration, human-in-the-loop verification, cross-platform task execution, and post-meeting Q&A follow-up.')
pdf.ln(2)

img_w = W
pdf.image('cisco_case/figures/flowchart_1_agentic_ai.png', x=pdf.l_margin, w=img_w)

# ============================================================
# PROBLEM 2: VIBE
# ============================================================
pdf.add_page()
heading(pdf, 'Problem 2: Webex Meetings Exclude Non-Native and Non-Technical Participants')

subheading(pdf, 'Problem Definition')
body(pdf, 'Hybrid and global workforces are now the norm. Enterprises routinely run meetings with participants spread across countries, languages, and technical backgrounds. Yet collaboration platforms treat meetings as though everyone speaks fluent English, understands technical jargon, has a quiet environment, and can always speak aloud. This creates systemic exclusion:')

bullet(pdf, 'Language barriers: Non-native English speakers struggle to follow fast-paced discussions, miss nuances, and hesitate to ask questions.')
bullet(pdf, 'Technical jargon: In cross-functional meetings, technical terminology alienates non-technical participants. When an engineer says "the API rate limiter is throttling at the gateway," a sales leader hears noise, not information.')
bullet(pdf, 'Poor audio quality: Users in noisy environments produce audio that degrades the experience for all participants and makes AI transcription inaccurate.')
bullet(pdf, 'Inability to speak: Some participants cannot speak aloud due to noise, broken microphones, speech difficulties, or social anxiety in large meetings. These users are effectively silenced.')

subheading(pdf, 'Competitive Gap Analysis')
body(pdf, 'Microsoft Teams offers live captions and basic translation, but these are read-only text overlays that do not address voice quality, jargon simplification, or the inability to speak. Zoom provides similar caption-based translation. Neither platform offers a comprehensive voice intelligence layer that cleans, boosts, translates, simplifies, and speaks on behalf of users in real-time.')

subheading(pdf, 'Business Impact of the Problem')
bullet(pdf, 'Reduced meeting ROI: When 30-40% of participants cannot fully engage due to language or audio barriers, meetings produce lower-quality decisions.')
bullet(pdf, 'Global team friction: Language barriers are the number one obstacle to effective cross-border collaboration.')
bullet(pdf, 'Accessibility gaps: Users with speech difficulties or social anxiety are systematically excluded from verbal participation.')
bullet(pdf, 'Competitive vulnerability: As enterprises prioritize DEI in technology procurement, platforms that do not solve participation barriers will lose.')
pdf.ln(2)

subheading(pdf, 'Solution 2: VIBE - Voice & Language Intelligence Layer')

body(pdf, 'VIBE is a real-time, in-meeting voice and language AI layer that boosts and cleans voice quality, translates between native and English in both speech and text, simplifies technical jargon for non-technical users, and enables type-to-speak so VIBE speaks on the user\'s behalf. All inside Webex. No deepfake risk. Every action is auditable and transparent.')

body_bold(pdf, 'A: User Entry & Onboarding')
bullet(pdf, 'Toggle Activation: A VIBE toggle appears in the meeting controls bar. Zero configuration required.')
bullet(pdf, 'Mode Selection: Voice Boost, Live Translation, Type-to-Speak, and/or Simple Mode (jargon simplification). One or more modes active simultaneously.')
bullet(pdf, 'Language & Profile: Native language (Hindi, Spanish, Mandarin, French, Arabic, Portuguese, Japanese, Korean, +90 more), tech level (Technical/Non-Technical), voice preset (Clear, Loud, Warm, Broadcast-style).')
pdf.ln(1)

body_bold(pdf, 'B: Live Audio Path - When User Speaks')
bullet(pdf, 'Microphone Audio Captured: Raw PCM stream with per-speaker separation via Webex AI Codec.')
bullet(pdf, 'Audio Intelligence Front-End: DNN noise removal for 150+ noise types, echo cancellation, auto gain control, smart room detection with reverb and acoustic fingerprint adjustment.')
bullet(pdf, 'Voice Boost & EQ Engine: Applies selected preset, adapts to environment, normalizes waveform for consistent output.')
bullet(pdf, 'Speech-to-Text (ASR): Real-time transcription with multi-accent support, per-speaker diarization, filler word removal.')
bullet(pdf, 'NLP Layer - Conditional Processing: Simple Mode rewrites jargon to plain language with analogies (e.g., "API" becomes "a waiter between kitchen and table"). Translation converts native language to English or target. Always-active intent tagging and clarity scoring.')
bullet(pdf, 'Text-to-Speech: VIBE Voice with consistent persona, emotional tone matching.')
bullet(pdf, 'Delivered to All Participants: Cleaned, boosted, translated VIBE voice with per-user captions in their own language.')
pdf.ln(1)

body_bold(pdf, 'C: Type-to-Speak Path - When User Cannot Speak')
bullet(pdf, 'Triggers: Muted, too noisy, broken mic, speech difficulty, large-meeting shyness. Auto-suggest when VIBE detects prolonged silence + high ambient noise.')
bullet(pdf, 'User types in VIBE Panel in any language. Can paste code, data, tables. Drafts visible only to user before send.')
bullet(pdf, 'NLP Processing: Detect language, translate to meeting language, apply "Polish mode" to convert draft into fluent spoken-style language.')
bullet(pdf, 'VIBE Agent Speaks: Neural TTS speaks typed message aloud. Label: "Spoken by VIBE for [UserName]." Three voice personas per session.')
bullet(pdf, 'Caption & Chat Sync: "from [UserName] via VIBE" tag in transcript. Chat logs typed input + spoken output side-by-side.')
pdf.ln(1)

body_bold(pdf, 'D: Q&A Close-Loop for Non-Native / Non-Technical Users')
bullet(pdf, 'User Asks in Own Language via voice or type-to-speak.')
bullet(pdf, 'ASR + Translation to English for the presenter.')
bullet(pdf, 'Presenter answers in English; VIBE captures answer in real-time.')
bullet(pdf, 'Translation + Simplification back to user: English answer translated to native language. Simple Mode adds analogy and concrete example.')
pdf.ln(1)

body_bold(pdf, 'E: End & Logging')
bullet(pdf, 'VIBE Transcript: Original language layer, English translation layer, simplified text layer, timestamps + speaker IDs, Type-to-Speak logs marked.')
bullet(pdf, 'VIBE Summary Pack: Key Q&A in native language with simple explanations, downloadable per-user, shareable via Webex/email.')
bullet(pdf, 'Session Analytics (Splunk-Powered): Voice clarity score trend, translation accuracy log, Q&A resolution rate, VIBE usage breakdown. All session data flows into Splunk for enterprise-wide observability, anomaly detection, and compliance reporting.')
pdf.ln(1)

body_bold(pdf, 'Privacy Guarantee: Transparency & Trust Layer')
bullet(pdf, 'Every VIBE-synthesized voice is labeled: "Spoken by VIBE for [User]." No hidden AI speech.')
bullet(pdf, 'Full audit trail: every VIBE action (boost, translate, TTS, simplify) logged with user consent timestamps and streamed to Splunk for centralized governance.')
bullet(pdf, 'Splunk VIBE Dashboard: Enterprise IT teams monitor voice quality metrics, translation accuracy, TTS usage patterns, and anomalous VIBE behavior across all meetings in real-time.')
bullet(pdf, 'Zero data retention option: transcript deleted on meeting end if user opts out.')
bullet(pdf, 'VIBE never impersonates: voice persona is distinct from user\'s actual voice.')
pdf.ln(1)

subheading(pdf, 'Why This Solution Wins')
body(pdf, 'No collaboration platform today offers a unified, real-time voice and language intelligence layer. Teams and Zoom provide basic captions and translation as passive overlays. VIBE goes far beyond by actively improving voice quality, translating with TTS delivery, simplifying jargon with analogies, and enabling silent users to speak through AI. Combined with Cisco\'s AI Codec technology and Splunk-powered observability for enterprise-wide monitoring of voice quality, translation accuracy, and compliance, VIBE creates a participation experience that makes every meeting truly inclusive and governable at scale.')

subheading(pdf, 'Expected Impact')
bullet(pdf, 'Noise reduction effectiveness: 95%+ across 150+ noise types')
bullet(pdf, 'ASR accuracy: 98% real-time transcription accuracy')
bullet(pdf, 'Translation latency: <1 second end-to-end')
bullet(pdf, 'TTS naturalness: 4.5/5 user rating target')
bullet(pdf, 'Type-to-speak delivery: <2 seconds from send to spoken output')
bullet(pdf, '40% increase in non-native speaker participation rates')
pdf.ln(2)
source_note(pdf, 'Sources: Cisco Webex AI Codec documentation; Microsoft Work Trend Index 2024; Gartner DEI in Technology Procurement Report 2024.')

subheading(pdf, 'Solution 2 Flowchart: VIBE - Voice & Language Intelligence Layer')
body(pdf, 'The following flowchart details the complete VIBE architecture including user onboarding, the live audio speak path, type-to-speak path, cross-language Q&A close-loop, session logging, privacy guarantee, tech stack, KPIs, and component architecture overview.')
pdf.ln(2)

pdf.image('cisco_case/figures/flowchart_2_vibe.png', x=pdf.l_margin, w=img_w)

# ============================================================
# PROBLEM 3
# ============================================================
pdf.add_page()
heading(pdf, 'Problem 3: Webex Has a Weaker, Less Strategic Developer Ecosystem')

subheading(pdf, 'Problem Definition')
body(pdf, 'Integration ecosystems are the hidden engines of collaboration platforms. Microsoft Teams offers over 2,000 integrations through its App Marketplace; Zoom supports over 2,500 third-party integrations. These platforms have become "glue layers" that connect nearly every SaaS tool an enterprise uses. Webex, while improving its integration catalog, still lags in scale, depth, and strategic positioning.')

body(pdf, 'Beyond raw connector count, there is a second, more critical gap: intelligence. Today\'s integrations are mostly static, one-off connectors that perform simple, predefined actions. The next competitive frontier is AI-driven agents: intelligent, multi-step integrations that can observe, reason, and act autonomously inside a meeting. Yet no platform has launched a dedicated, enterprise-grade AI agent marketplace.')

body(pdf, 'For Webex, this uneven ecosystem creates several problems:')
bullet(pdf, 'Reduced daily utility: Many users treat Webex as a "meetings-only" layer, reducing stickiness.')
bullet(pdf, 'Developer disinterest: Without a compelling differentiator, Webex struggles to attract high-quality AI builders.')
bullet(pdf, 'Procurement friction: A smaller ecosystem makes Webex an easier "tie-breaking loss" in enterprise evaluations.')
bullet(pdf, 'Limited new revenue streams: Webex relies on per-seat licensing with no material marketplace-style revenue.')

subheading(pdf, 'Competitive Landscape and Market Context')
bullet(pdf, 'Microsoft Teams: Large app catalog on Microsoft 365 stack. Copilot operates inside Office apps but no formal AI agent marketplace with third-party AI agents.')
bullet(pdf, 'Zoom: Strong app marketplace with deep coverage. AI Companion provides early agentic behaviors but no fully open, certified AI agent ecosystem.')
bullet(pdf, 'Webex: Growing but smaller integration footprint, strong security capabilities, but no dedicated AI agent platform.')

subheading(pdf, 'Business Impact of the Problem')
bullet(pdf, 'Reduced daily utility and engagement')
bullet(pdf, 'Developer investment flows to Teams and Zoom')
bullet(pdf, 'Enterprise adoption friction in procurement decisions')
bullet(pdf, 'Revenue limitation without marketplace monetization')
pdf.ln(2)

subheading(pdf, 'Solution 3: Webex Secure AI Agent Marketplace')

body(pdf, 'Cisco will launch the Webex Secure AI Agent Marketplace, the industry\'s first enterprise-grade AI agent marketplace where any third-party developer can host AI agents inside Webex under strict Cisco-defined security, data, and UX rules. Like Apple and Google enforce standards for iOS/Android apps, Cisco enforces standards for AI agents in Webex. Developers build, Cisco certifies, admins control, users benefit. The marketplace operates on a four-stage lifecycle: Build, Certify, Deploy, Monitor.')

body_bold(pdf, 'Stage 1: BUILD - AI Agent SDK & Developer Environment')
bullet(pdf, 'Agent SDK (Python / JavaScript): Pre-built components for common patterns: Meeting Listener, Task Executor, Data Retriever, Notification Sender.')
bullet(pdf, 'Agent Templates: CRM Updater, Ticket Creator, Doc Generator, Calendar Scheduler, Contract Flow (DocuSign), VIBE Voice Agent (first-party). Templates reduce development time by 60%.')
bullet(pdf, 'Sandbox Environment: Simulated meetings, API calls, and data flows. Tests: latency, accuracy, error handling, load performance.')
bullet(pdf, 'API & A2A Reference: Meeting lifecycle, real-time transcription feeds, user-context APIs, Agent-to-Agent protocols for cross-tool orchestration with Jira, Salesforce, Slack, SAP, DocuSign, ServiceNow, GitHub.')
pdf.ln(1)

body_bold(pdf, 'Stage 2: CERTIFY - Cisco Security & Compliance Pipeline')
bullet(pdf, 'Static Code Analysis: Scanning for vulnerabilities, backdoors, data-exfiltration patterns, insecure API usage.')
bullet(pdf, 'Permission & Scope Validation: Declared vs actual data access verification. Zero-trust minimum-privilege enforcement.')
bullet(pdf, 'Performance & Reliability Testing: Latency benchmarks (<200ms), load testing (1,000+ concurrent users), CPU/memory profiling, failure-recovery validation.')
bullet(pdf, 'Compliance Checks: SOC 2, HIPAA, FedRAMP, GDPR automated checks based on declared data-handling practices.')
bullet(pdf, 'Cisco Trust Badge: "Cisco Verified Agent" badge signals enterprise-grade security and compliance standards.')
pdf.ln(1)

body_bold(pdf, 'Stage 3: DEPLOY - Enterprise-Grade Management & Deployment')
bullet(pdf, 'Marketplace Discovery: Admins browse by industry vertical (healthcare, finance, government, manufacturing), use case (sales, support, HR, engineering), and security/compliance level.')
bullet(pdf, 'Configuration & Scoping: Assign to orgs/teams/users. Data access levels: read-only, limited write, full write. Approval workflows for high-risk actions. Usage quotas and budget caps.')
bullet(pdf, 'Sandboxed Execution: Isolated containers in Webex Cloud with zero-trust identity layer, network egress filtering, and rate limits.')
bullet(pdf, 'Pilot Rollout & A/B Testing: Deploy to pilot groups first, measure time saved, ticket rate, user satisfaction before organization-wide activation.')
pdf.ln(1)

body_bold(pdf, 'Stage 4: MONITOR - Splunk-Powered Observability & Governance')
bullet(pdf, 'Real-Time Dashboards: Per-agent metrics (invocations/hour, success/error rate, API latency). Aggregated usage by org/team/user. Active agent count.')
bullet(pdf, 'Anomaly Detection: ML-based detection of unusual data-access patterns, permission violations, performance regressions, unauthorized API attempts, cross-tenant data flags.')
bullet(pdf, 'Kill-Switch & Audit Trail: Instant agent deactivation with full audit trail retained. Scope and quota adjustment.')
bullet(pdf, 'Billing & Revenue: Usage tracked per agent. Pay-per-use or subscription models. 70/30 revenue split (developer-favoring). Monthly invoice generation.')
pdf.ln(1)

subheading(pdf, 'User Journey Within Webex')
body(pdf, 'The marketplace integrates seamlessly into the Webex user experience:')
bullet(pdf, 'Users discover agents through the "AI Agents" tab in Webex or via in-meeting suggestion banners.')
bullet(pdf, 'Users review agent permissions (e.g., "Can read transcript, can create Jira tickets") and accept Cisco\'s data notice before installation.')
bullet(pdf, 'During live meetings, agents detect task intents from the transcript, pull context from connected systems, and draft complete actions inline in Webex.')
bullet(pdf, 'Users see in-meeting approval cards with Approve, Edit, or Reject controls before any action is executed.')
bullet(pdf, 'On approval, agents execute via authenticated API calls. Webex confirms in chat (e.g., "Jira ticket WEBAPP-2026-347 created. Assigned to Sarah Chen. Priority: High.").')
bullet(pdf, 'Users manage agents through a "My Agents" panel: disable, update, downgrade, or view usage history.')
pdf.ln(1)

subheading(pdf, 'Why This Solution Wins')
bullet(pdf, 'Trust-First AI: Cisco\'s security certifications and Splunk observability create governance that neither Microsoft nor Zoom can match for regulated industries.')
bullet(pdf, 'Platform-Level Differentiation: Webex competes on "who has the most intelligent, safest AI agent ecosystem" rather than "who has more connectors."')
bullet(pdf, 'New Revenue & Network Effects: Per-seat plus per-agent monetization creates a self-reinforcing flywheel: more agents lead to more value, more users, more developers.')

subheading(pdf, 'Expected Impact')
bullet(pdf, '500+ certified AI agents in the marketplace within Year 1')
bullet(pdf, '$150 million in GMV by FY2028')
bullet(pdf, '3x growth in Webex developer activity within 18 months')
bullet(pdf, '85% enterprise renewal rate driven by agent-based stickiness')
bullet(pdf, 'New annual marketplace commission revenue: $50 million by FY2029')
pdf.ln(2)
source_note(pdf, 'Sources: Cisco FY2024 10-K; Splunk platform documentation; Salesforce AppExchange economics model; MarketsandMarkets Agentic AI Market Report 2024.')

subheading(pdf, 'Solution 3 Flowchart: Secure AI Agent Marketplace')
body(pdf, 'The following flowchart details the three-lane architecture (Developer Journey, Admin Journey, User Journey), the Cisco certification pipeline, Splunk observability layer, agent examples, industry coverage, and platform architecture stack.')
pdf.ln(2)

pdf.image('cisco_case/figures/flowchart_3_marketplace.png', x=pdf.l_margin, w=img_w)

# ============================================================
# TECHNICAL FEASIBILITY, CONSTRAINTS & SCALABILITY ASSESSMENT
# ============================================================
pdf.add_page()
heading(pdf, 'Technical Feasibility, Constraints & Scalability Assessment')

body(pdf, 'This section assesses the technical feasibility, key constraints, and scalability considerations for each of the three proposed solutions.')

subheading(pdf, 'Solution 1: AI Meeting Prep & Workflow Orchestrator')

body_bold(pdf, 'Technical Feasibility')
bullet(pdf, 'The Webex AI Codec already exists in production and processes millions of meeting minutes daily. Extending the NLP layer to detect task intents is an incremental ML advancement.')
bullet(pdf, 'LLM-based task planning is technically proven. Fine-tuning a model on enterprise meeting transcripts achieves high accuracy for task detection and drafting.')
bullet(pdf, 'A2A protocols for cross-system integration rely on mature REST/GraphQL APIs.')
bullet(pdf, 'The PREPARE phase leverages retrieval-augmented generation (RAG), a well-established pattern.')

body_bold(pdf, 'Key Constraints')
bullet(pdf, 'Latency: Real-time task detection requires the NLP pipeline to process audio-to-intent in under 2 seconds.')
bullet(pdf, 'LLM hallucination risk: Mitigated by human-in-the-loop approval and confidence thresholds.')
bullet(pdf, 'Enterprise data access: Organizations with strict governance may limit what Webex AI can ingest.')

body_bold(pdf, 'Scalability')
bullet(pdf, 'Cisco\'s cloud infrastructure supports 600+ million meeting minutes per month.')
bullet(pdf, 'The A2A protocol is stateless and horizontally scalable.')
bullet(pdf, 'Splunk observability handles petabytes per day.')
pdf.ln(2)

subheading(pdf, 'Solution 2: VIBE - Voice & Language Intelligence Layer')

body_bold(pdf, 'Technical Feasibility')
bullet(pdf, 'DNN noise removal and voice processing are already core Webex AI Codec capabilities.')
bullet(pdf, 'ASR at 98% accuracy is achievable using Whisper or Cisco\'s proprietary ASR. 100+ language support via neural machine translation models deployed at scale.')
bullet(pdf, 'Neural TTS with natural voice personas is technically mature (Google Cloud TTS, Amazon Polly, open-source models).')
bullet(pdf, 'Simple Mode jargon simplification is a well-understood NLP task with strong performance from current models.')

body_bold(pdf, 'Key Constraints')
bullet(pdf, 'End-to-end latency: The full pipeline (ASR + translation + simplification + TTS) must complete in under 2 seconds. Pipeline parallelization and model optimization are required.')
bullet(pdf, 'Translation accuracy for domain-specific terms: Custom terminology dictionaries per organization needed.')
bullet(pdf, 'Bandwidth: Per-user VIBE audio streams increase requirements. Mitigated by neural codec compression (1 kbps).')

body_bold(pdf, 'Scalability')
bullet(pdf, 'VIBE processing is per-user and per-meeting, naturally parallelizable.')
bullet(pdf, 'Neural machine translation models deploy as auto-scaling microservices.')
bullet(pdf, 'Splunk ingests VIBE telemetry (voice quality, translation accuracy, TTS events) across all meetings for centralized analytics and anomaly detection at enterprise scale.')
bullet(pdf, 'Zero data retention option simplifies storage scalability.')
pdf.ln(2)

subheading(pdf, 'Solution 3: Secure AI Agent Marketplace')

body_bold(pdf, 'Technical Feasibility')
bullet(pdf, 'SDK development is standard engineering. Extending existing Webex APIs into a structured agent SDK is feasible within 6-9 months.')
bullet(pdf, 'The certification pipeline leverages existing Cisco capabilities: static analysis, zero-trust networking, and Splunk observability.')
bullet(pdf, 'Sandboxed agent execution using containerized environments is a proven pattern (AWS Lambda, Cloudflare Workers).')

body_bold(pdf, 'Key Constraints')
bullet(pdf, 'Certification throughput: Automated scanning handles volume; manual review of edge cases may create bottlenecks.')
bullet(pdf, 'Agent quality control: The certification bar must balance trust with developer accessibility.')
bullet(pdf, 'Cross-system compatibility: Agents depend on third-party APIs remaining stable.')

body_bold(pdf, 'Scalability')
bullet(pdf, 'Agent execution scales horizontally via isolated containers with defined resource limits.')
bullet(pdf, 'Splunk monitoring handles millions of agent events per day.')
bullet(pdf, 'The marketplace catalog scales trivially as a CDN-backed web application.')

# ============================================================
# IMPLEMENTATION RISKS & SYSTEM-LEVEL TRADE-OFFS
# ============================================================
pdf.add_page()
heading(pdf, 'Implementation Risks & System-Level Trade-Offs')

body(pdf, 'This section identifies key implementation risks and system-level trade-offs for each solution.')

subheading(pdf, 'Solution 1: AI Meeting Prep & Workflow Orchestrator')

body_bold(pdf, 'Implementation Risks')
bullet(pdf, 'AI hallucination in task drafts: Mitigated by mandatory human-in-the-loop approval and confidence scoring.')
bullet(pdf, 'Over-automation backlash: Mitigated by progressive disclosure and user-controlled sensitivity settings.')
bullet(pdf, 'Data privacy and compliance: All data access passes through zero-trust data fabric with explicit consent.')
bullet(pdf, 'Integration fragility: Mitigated by circuit-breaker patterns and graceful degradation.')

body_bold(pdf, 'System-Level Trade-Offs')
bullet(pdf, 'Accuracy vs. speed: More context retrieval improves quality but increases latency.')
bullet(pdf, 'Automation vs. control: Human-in-the-loop reduces speed but is essential for trust in regulated industries.')
bullet(pdf, 'Breadth vs. depth of integration: Prioritize top 10-15 enterprise tools for deep integration; use generic connectors for long-tail.')
pdf.ln(2)

subheading(pdf, 'Solution 2: VIBE')

body_bold(pdf, 'Implementation Risks')
bullet(pdf, 'Deepfake perception risk: Mitigated by mandatory on-screen labeling, meeting-start notification, and admin controls.')
bullet(pdf, 'Translation errors in high-stakes contexts: Mitigated by custom terminology dictionaries and confidence scoring with visual warnings.')
bullet(pdf, 'User adoption resistance: VIBE is fully opt-in with per-user control; no organizational mandate required.')
bullet(pdf, 'Compute cost: VIBE processing activates only for users who enable it; adaptive quality scaling for large meetings.')

body_bold(pdf, 'System-Level Trade-Offs')
bullet(pdf, 'Latency vs. quality: Larger models improve accuracy but increase inference time.')
bullet(pdf, 'Privacy vs. personalization: Zero-data-retention limits personalization for privacy-conscious users.')
bullet(pdf, 'Simplification vs. accuracy: Over-simplification may distort meaning. Original text always provided alongside simplified version.')
pdf.ln(2)

subheading(pdf, 'Solution 3: AI Agent Marketplace')

body_bold(pdf, 'Implementation Risks')
bullet(pdf, 'Marketplace cold-start problem: Mitigated by seeding 20-30 first-party agents, ISV partnerships, and developer grants.')
bullet(pdf, 'Security certification bottleneck: Automated scanning handles 90%+; manual review reserved for sensitive-data agents.')
bullet(pdf, 'Agent misbehavior in production: Mitigated by kill-switch, sandboxed execution, and Splunk anomaly detection.')
bullet(pdf, 'Revenue model uncertainty: Start with generous developer split; adjust as marketplace matures.')

body_bold(pdf, 'System-Level Trade-Offs')
bullet(pdf, 'Openness vs. security: Trust-first approach grows slower but builds stronger enterprise trust. Correct for Cisco\'s brand.')
bullet(pdf, 'First-party vs. third-party agents: Recommended 15-20% first-party for core use cases; 80%+ from developer community.')
bullet(pdf, 'Platform lock-in vs. portability: Adopt open standards (A2A protocol) to reduce perceived lock-in while maintaining differentiation.')

# ============================================================
# INTEGRATED STRATEGY & CONCLUSION
# ============================================================
pdf.add_page()
heading(pdf, 'Integrated Strategy: How the Three Solutions Work Together')

body(pdf, 'The three solutions are designed as an integrated system, not independent initiatives:')

bullet(pdf, 'Solution 1 (AI Meeting Prep & Workflow Orchestrator) provides the core intelligence: AI that can prepare, perceive, reason, act, and follow up across the full meeting lifecycle.')
bullet(pdf, 'Solution 2 (VIBE) ensures every participant can fully engage regardless of language, technical background, or environment. VIBE makes the input to Solution 1 richer and more inclusive.')
bullet(pdf, 'Solution 3 (AI Agent Marketplace) scales the intelligence: the marketplace enables hundreds of developers to build vertical-specific agents and provides the deployment and governance infrastructure for regulated industries.')
pdf.ln(2)

body(pdf, 'The combined impact makes Webex indispensable rather than interchangeable. Users stay on Webex not because the video quality is marginally better, but because leaving means losing their AI agents, their automated workflows, the productivity gains that accumulate over time, and the inclusive communication layer that makes global teamwork seamless.')

subheading(pdf, 'Combined Projected Impact')

tw = W
c1 = tw * 0.45
c2 = tw * 0.55
pdf.set_font('Times', 'B', 12)
pdf.cell(c1, LH, 'Metric', border=1, align='C')
pdf.cell(c2, LH, 'Projected Value', border=1, align='C')
pdf.ln()
pdf.set_font('Times', '', 12)

metrics = [
    ('Daily Active Usage Increase', '+35% within 12 months of full deployment'),
    ('Meeting-to-Action Conversion', '25% (vs. current ~5% industry average)'),
    ('Post-Meeting Follow-Up Time', 'Reduced from 45 min to 5 min per meeting'),
    ('Action Item Completion Rate', '92% on-time (vs. 27% industry baseline)'),
    ('Non-Native Speaker Participation', '+40% increase in active contribution'),
    ('Translation Latency', '<1 second end-to-end for 100+ languages'),
    ('Marketplace Certified Agents', '500+ in Year 1, 2,000+ by Year 3'),
    ('Developer Ecosystem Growth', '3x within 18 months'),
    ('Enterprise Renewal Rate', '85% (driven by agent + VIBE stickiness)'),
    ('Incremental Collaboration ARR', '+$2.1 billion by FY2029'),
    ('Marketplace Commission Revenue', '$50M annually by FY2029'),
    ('Productivity Savings per Worker', '$4,200 per knowledge worker per year'),
]

for metric, value in metrics:
    pdf.cell(c1, LH, metric, border=1)
    pdf.cell(c2, LH, value, border=1)
    pdf.ln()

pdf.ln(3)
source_note(pdf, 'Sources: IDC UC&C Market Tracker 2024; MarketsandMarkets Agentic AI Report; Cisco FY2024 10-K; Microsoft Work Trend Index 2024; McKinsey Future of Work Report 2024.')

# ============================================================
# REFERENCES
# ============================================================
pdf.add_page()
heading(pdf, 'References')
pdf.ln(1)

refs = [
    'Cisco Systems. (2024). Annual Report (Form 10-K), Fiscal Year 2024. SEC Filing.',
    'Microsoft Corporation. (2024). Annual Report (Form 10-K), Fiscal Year 2024. SEC Filing.',
    'Zoom Video Communications. (2025). Annual Report (Form 10-K), Fiscal Year 2025. SEC Filing.',
    'IDC. (2024). Worldwide Unified Communications & Collaboration Market Tracker.',
    'Gartner. (2024). Future of Work Survey: Hybrid Work Trends.',
    'McKinsey & Company. (2024). Future of Work Report: Meeting Productivity and Knowledge Worker Efficiency.',
    'MarketsandMarkets. (2024). Agentic AI Market Report: Global Forecast to 2030.',
    'Microsoft. (2024). Work Trend Index: Annual Report on Workplace Trends and Meeting Culture.',
    'Otter.ai. (2024). Workplace Productivity Report: Meeting Follow-Up and Action Item Completion Rates.',
    'Cisco Webex. (2025). Webex AI Assistant and AI Codec Technical Documentation.',
    'Microsoft. (2025). Microsoft 365 Copilot Product Documentation.',
    'Zoom. (2025). Zoom AI Companion 2.0 Product Documentation.',
    'G2. (2025). Video Conferencing Software Reviews and Ratings.',
    'Salesforce. (2024). AppExchange Marketplace Economics and Developer Revenue Sharing Model.',
    'Gartner. (2024). DEI in Technology Procurement Report.',
]

for i, ref in enumerate(refs):
    pdf.set_font('Times', '', 12)
    pdf.multi_cell(0, LH, f'{i+1}. {ref}')
    pdf.ln(1)

pdf.output('cisco_case/Cisco_Problems_Solutions.pdf')
print("PDF generated: cisco_case/Cisco_Problems_Solutions.pdf")

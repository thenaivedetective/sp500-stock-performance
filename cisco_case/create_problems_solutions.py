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
    ax.text(cx, cy, text, ha='center', va='center', fontsize=fs, fontweight='bold', color=tc)

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

# ============================================================
# FLOWCHART 1: Enhanced Agentic AI - Prepare-Perceive-Reason-Act-Follow-Up
# ============================================================
fig, ax = plt.subplots(figsize=(22, 42))
ax.set_xlim(0, 22)
ax.set_ylim(0, 42)
ax.axis('off')

ax.text(11, 41.3, 'Solution 1: Webex AI Meeting Prep & Workflow Orchestrator',
        ha='center', fontsize=21, fontweight='bold', color='#002060')
ax.text(11, 40.7, 'Prepare \u2192 Perceive \u2192 Reason \u2192 Act \u2192 Follow-Up  |  Full Meeting Lifecycle AI',
        ha='center', fontsize=13, color='#555555')

lane_colors = ['#E8F4FD', '#FFF3E0', '#F3E5F5']
lane_labels = ['WEBEX CLOUD', 'CISCO SECURE DATA FABRIC', 'THIRD-PARTY APPS']
lane_sublabels = ['(AI Codec + NLP + Agent Runtime)', '(Splunk + Zero-Trust Identity)', '(Jira, Salesforce, SAP, etc.)']
lane_xs = [(0.3, 7.0), (7.5, 14.5), (15.0, 21.7)]

for i, ((x1, x2), color, label, sublabel) in enumerate(zip(lane_xs, lane_colors, lane_labels, lane_sublabels)):
    rect = mpatches.FancyBboxPatch((x1, 1.0), x2 - x1, 38.5, boxstyle="round,pad=0.1",
                                    facecolor=color, edgecolor='#999999', linewidth=1.5, alpha=0.5)
    ax.add_patch(rect)
    ax.text((x1 + x2) / 2, 39.2, label, ha='center', fontsize=13, fontweight='bold', color='#002060')
    ax.text((x1 + x2) / 2, 38.8, sublabel, ha='center', fontsize=9, color='#666666')

WX = 3.65
DF = 11.0
TP = 18.35

draw_oval(ax, WX, 38.0, 4.5, 1.0, 'START\nMeeting Scheduled', '#002060', 'white', 11)
arrow(ax, WX, 37.45, WX, 36.8)

draw_dashed_box(ax, 0.5, 32.5, 6.3, 4.0, 'PREPARE: AI Meeting Prep', '#0050A0')

draw_rect(ax, WX, 36.2, 5.5, 1.0,
          'Context Ingestion\nIngest title, participants, docs,\nCRM records, past transcripts', '#1A5276', 'white', 9)
arrow(ax, WX, 35.65, WX, 35.0)

draw_rect(ax, WX, 34.4, 5.5, 1.0,
          'AI Generates Agenda + Insights\nPrep checklist, key metrics,\npredicted Q&A for presenter', '#1A5276', 'white', 9)
arrow(ax, WX, 33.85, WX, 33.2)

draw_rect(ax, WX, 32.6, 5.5, 1.0,
          'Auto-Slide Generation\nFirst-draft deck from CRM data,\nJira issues, financial metrics', '#0070C0', 'white', 9)

arrow(ax, WX + 2.8, 36.2, TP - 2.5, 36.2, '#333333')
draw_para(ax, TP, 36.2, 5.0, 1.0,
          'PULL CONTEXT\nCRM pipeline, Jira backlog,\nCalendar history', '#D35400', 'white', 9)

arrow(ax, WX + 2.8, 34.4, DF - 2.5, 34.4, '#333333')
draw_cyl(ax, DF, 34.4, 5.0, 1.2,
         'Cisco Secure Data Fabric\nZero-Trust data retrieval\nSplunk audit logging', '#8E44AD', 'white', 9)

arrow(ax, WX, 32.05, WX, 31.3)

draw_oval(ax, WX, 30.7, 4.5, 1.0, 'Meeting\nBegins Live', '#27AE60', 'white', 11)
arrow(ax, WX, 30.15, WX, 29.5)

draw_dashed_box(ax, 0.5, 23.5, 6.3, 5.8, 'PERCEIVE: AI Codec ML Pipeline', '#0050A0')

draw_para(ax, WX, 28.9, 5.2, 0.9,
          'Raw Audio/Video Input\nMicrophone + Camera streams', '#2C3E50', 'white', 9)
arrow(ax, WX, 28.4, WX, 27.8)

draw_rect(ax, WX, 27.2, 5.5, 1.0,
          'Deep Neural Network (DNN)\nBackground Noise Removal\n150+ noise types in real-time', '#1A5276', 'white', 9)
arrow(ax, WX, 26.65, WX, 26.0)

draw_rect(ax, WX, 25.4, 5.5, 1.0,
          'AI Codec: Neural Speech Synthesis\nCompresses audio to ~1 kbps\n(vs 32 kbps traditional codecs)', '#1A5276', 'white', 9)
arrow(ax, WX, 24.85, WX, 24.2)

draw_rect(ax, WX, 23.6, 5.5, 1.0,
          'NLP Engine: Speech-to-Text\nReal-time transcription + translation\nTask intent + decision detection', '#0070C0', 'white', 9)
arrow(ax, WX, 23.05, WX, 22.3)

draw_diamond(ax, WX, 21.3, 2.0, 'NLP detects\nTask Intent?', '#F39C12', 'black', 10)

ax.text(1.0, 21.3, 'NO', fontsize=12, fontweight='bold', color='#E74C3C', ha='center')
arrow(ax, WX - 1.0, 21.3, 1.5, 21.3, '#E74C3C', 2)
arrow(ax, 1.0, 21.3, 1.0, 28.9, '#E74C3C', 2)
arrow(ax, 1.0, 28.9, WX - 2.8, 28.9, '#E74C3C', 2)
ax.text(1.0, 25.0, 'Continue\nMonitoring', fontsize=9, fontweight='bold', color='#E74C3C', ha='center',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#E74C3C', alpha=0.9))

ax.text(WX + 1.7, 22.0, 'YES', fontsize=12, fontweight='bold', color='#27AE60', ha='center')
arrow(ax, WX + 1.0, 21.3, DF - 2.5, 21.3, '#27AE60', 2.5)

draw_para(ax, DF, 21.3, 5.0, 1.1,
          'REASON: Fetch Context\nA2A Protocol retrieves\nproject data from systems', '#27AE60', 'white', 10)

arrow(ax, DF + 2.8, 21.3, TP - 2.2, 21.3, '#333333')

draw_para(ax, TP, 21.3, 5.0, 1.1,
          'EXTERNAL SYSTEMS\nJira / Salesforce / SAP\nServiceNow / GitHub', '#D35400', 'white', 9)

arrow(ax, DF, 20.65, DF, 19.5)

draw_cyl(ax, DF, 18.7, 5.0, 1.5,
         'CISCO SECURE DATA FABRIC\nSplunk Observability\nZero-Trust Identity Layer', '#8E44AD', 'white', 9)

arrow(ax, DF, 17.85, DF, 16.8)

draw_rect(ax, DF, 16.1, 5.0, 1.2,
          'ACT: DRAFT\nAI Agent generates task draft\nusing retrieved context\n+ LLM-based planning', '#0070C0', 'white', 10)

arrow(ax, DF - 2.8, 16.1, WX + 1.5, 14.5, '#333333')

draw_diamond(ax, WX, 13.5, 2.0, 'Human-in-Loop\nApprove?', '#F39C12', 'black', 10)

ax.text(WX + 1.7, 12.5, 'REJECT', fontsize=11, fontweight='bold', color='#E74C3C', ha='center')
arrow(ax, WX + 1.0, 13.5, DF - 2.8, 15.5, '#E74C3C', 2)

ax.text(WX + 1.7, 14.3, 'APPROVE', fontsize=11, fontweight='bold', color='#27AE60', ha='center')
arrow(ax, WX + 1.0, 13.5, TP - 2.5, 13.5, '#27AE60', 2.5)

draw_rect(ax, TP, 13.5, 5.0, 1.2,
          'EXECUTE\nAgent pushes data via\nsecure API to external app', '#E74C3C', 'white', 10)

arrow(ax, TP, 12.85, TP, 12.0)

draw_rect(ax, DF, 11.3, 5.5, 1.0,
          'Splunk Logs Execution\nPerformance metrics + audit trail\nAnomaly detection on agent actions', '#8E44AD', 'white', 9)
arrow(ax, TP, 11.3, DF + 2.8, 11.3, '#333333')

arrow(ax, DF - 2.8, 11.3, WX + 2.0, 11.3, '#333333')

draw_rect(ax, DF, 9.8, 5.5, 1.0,
          'CONFIRM\nStatus posted to Webex Chat:\n"Task created successfully"', '#0070C0', 'white', 9)
arrow(ax, DF, 10.7, DF, 10.35)

arrow(ax, DF, 9.25, DF, 8.5)

draw_dashed_box(ax, 0.5, 3.5, 6.3, 4.8, 'FOLLOW-UP: Post-Meeting AI', '#0050A0')

draw_oval(ax, WX, 7.8, 4.5, 1.0, 'Meeting\nEnds', '#27AE60', 'white', 11)
arrow(ax, DF - 2.8, 7.8, WX + 2.5, 7.8, '#333333')
arrow(ax, WX, 7.25, WX, 6.6)

draw_rect(ax, WX, 6.0, 5.5, 1.0,
          'Unanswered Q Detection\nIdentify deferred questions\nfrom transcript + predicted Q&A', '#1A5276', 'white', 9)
arrow(ax, WX, 5.45, WX, 4.8)

draw_rect(ax, WX, 4.2, 5.5, 1.0,
          'AI Drafts Follow-Up Answers\nOwner reviews, edits, approves\nMulti-channel delivery', '#0070C0', 'white', 9)

arrow(ax, WX + 2.8, 6.0, DF - 2.5, 6.0, '#333333')
draw_rect(ax, DF, 6.0, 5.0, 1.0,
          'Q&A Tracker Dashboard\nStatus, deadlines, SLA tracking\nWeekly digest to participants', '#8E44AD', 'white', 9)

arrow(ax, WX + 2.8, 4.2, TP - 2.5, 4.2, '#333333')
draw_rect(ax, TP, 4.2, 5.0, 1.0,
          'Deliver Answers via\nWebex Spaces / Email /\nIntegrated Chat Tools', '#D35400', 'white', 9)

arrow(ax, WX, 3.65, WX, 3.0)
draw_oval(ax, WX, 2.5, 4.5, 0.9, 'END\nAll Loops Closed')

mr = mpatches.FancyBboxPatch((0.3, 1.2), 21.4, 0.8, boxstyle='round,pad=0.1',
                               facecolor='#002060', edgecolor='black', linewidth=2)
ax.add_patch(mr)
ax.text(11, 1.6, 'IMPACT: 15 min saved/meeting  |  25% meeting-to-action  |  '
        '40% workflow automation  |  85% task accuracy  |  Q&A resolution rate 90%+',
        ha='center', va='center', fontsize=10, fontweight='bold', color='white')

lx = 15.5; ly = 38.5
ax.text(lx, ly, 'LEGEND:', fontsize=11, fontweight='bold', color='#002060')
draw_oval(ax, lx+0.9, ly-0.7, 1.2, 0.45, 'Start/End', '#002060', 'white', 7)
ax.text(lx+2.1, ly-0.7, '= Terminator', fontsize=8, va='center', color='#333333')
draw_rect(ax, lx+0.9, ly-1.4, 1.2, 0.4, 'Process', '#0070C0', 'white', 7)
ax.text(lx+2.1, ly-1.4, '= Action/ML Step', fontsize=8, va='center', color='#333333')
draw_diamond(ax, lx+0.9, ly-2.1, 0.6, 'Dec.', '#F39C12', 'black', 6)
ax.text(lx+2.1, ly-2.1, '= Decision Point', fontsize=8, va='center', color='#333333')
draw_para(ax, lx+0.9, ly-2.7, 1.2, 0.35, 'I/O', '#27AE60', 'white', 7)
ax.text(lx+2.1, ly-2.7, '= Data I/O', fontsize=8, va='center', color='#333333')
draw_cyl(ax, lx+0.9, ly-3.4, 1.2, 0.55, 'DB', '#8E44AD', 'white', 7)
ax.text(lx+2.1, ly-3.4, '= Database/Store', fontsize=8, va='center', color='#333333')

plt.tight_layout()
plt.savefig('cisco_case/figures/flowchart_1_agentic_ai.png', dpi=200, bbox_inches='tight')
plt.close()
print("Flowchart 1 (Enhanced Prepare-Perceive-Reason-Act-Follow-Up) created")

# ============================================================
# FLOWCHART 2: VIBE / VEL - Voice & Language Intelligence Layer
# ============================================================
fig, ax = plt.subplots(figsize=(22, 44))
ax.set_xlim(0, 22)
ax.set_ylim(0, 44)
ax.axis('off')

ax.text(11, 43.3, 'Solution 2: VIBE - Voice & Language Intelligence Layer',
        ha='center', fontsize=21, fontweight='bold', color='#002060')
ax.text(11, 42.7, 'Voice Boost | Live Translation | Type-to-Speak | Simple Mode  |  Real-Time In-Meeting AI',
        ha='center', fontsize=13, color='#555555')

draw_oval(ax, 11, 41.8, 6.0, 0.9, 'START: User Joins Webex Meeting', '#002060', 'white', 12)
arrow(ax, 11, 41.3, 11, 40.7)

p_onb = mpatches.FancyBboxPatch((0.3, 36.5), 21.4, 4.0, boxstyle="round,pad=0.15",
                                  facecolor='#1A5276', edgecolor='#1A5276', linewidth=2, alpha=0.08)
ax.add_patch(p_onb)
ax.text(1.0, 40.1, 'A: USER ONBOARDING', fontsize=13, fontweight='bold', color='#1A5276')

draw_rect(ax, 11, 40.1, 8.0, 1.0,
          'User Enables VIBE in Meeting Controls\nToggle appears in controls bar - zero configuration required', '#1A5276', 'white', 11)
arrow(ax, 11, 39.55, 11, 38.9)

draw_rect(ax, 11, 38.3, 8.0, 1.0,
          'Select Active Modes\nVoice Boost | Live Translation | Type-to-Speak | Simple Mode\nOne or more modes active simultaneously', '#1A5276', 'white', 11)
arrow(ax, 11, 37.75, 11, 37.1)

draw_rect(ax, 11, 36.5, 8.0, 1.0,
          'Select Language & Voice Profile\nNative Language (100+ supported) | Tech Level | Voice Preset\nClear / Loud / Warm / Broadcast-style', '#0070C0', 'white', 11)
arrow(ax, 11, 35.95, 11, 35.3)

draw_diamond(ax, 11, 34.3, 2.5, 'User is\nSpeaking or\nTyping?', '#F39C12', 'black', 11)

ax.text(5.0, 34.3, 'SPEAKING', fontsize=12, fontweight='bold', color='#27AE60', ha='center')
arrow(ax, 11 - 1.25, 34.3, 4.5, 34.3, '#27AE60', 2.5)
arrow(ax, 4.5, 34.3, 4.5, 33.2)

ax.text(17.0, 34.3, 'TYPING', fontsize=12, fontweight='bold', color='#0070C0', ha='center')
arrow(ax, 11 + 1.25, 34.3, 17.5, 34.3, '#0070C0', 2.5)
arrow(ax, 17.5, 34.3, 17.5, 33.2)

p_speak = mpatches.FancyBboxPatch((0.3, 24.0), 10.0, 9.0, boxstyle="round,pad=0.15",
                                    facecolor='#27AE60', edgecolor='#27AE60', linewidth=2, alpha=0.08)
ax.add_patch(p_speak)
ax.text(1.0, 32.6, 'B: LIVE SPEAK PATH', fontsize=13, fontweight='bold', color='#27AE60')

draw_para(ax, 4.5, 32.5, 5.5, 0.9,
          'Microphone Audio Captured\nPer-speaker separation via AI Codec', '#2C3E50', 'white', 9)
arrow(ax, 4.5, 32.0, 4.5, 31.3)

draw_rect(ax, 4.5, 30.7, 5.5, 1.0,
          'DNN Noise Removal\n150+ noise types (cafe, keyboard,\nHVAC) + Echo Cancellation', '#27AE60', 'white', 9)
arrow(ax, 4.5, 30.15, 4.5, 29.5)

draw_rect(ax, 4.5, 28.9, 5.5, 1.0,
          'Voice Boost & EQ Engine\nApply preset (Clear/Loud/Warm)\nAdaptive to environment', '#27AE60', 'white', 9)
arrow(ax, 4.5, 28.35, 4.5, 27.7)

draw_rect(ax, 4.5, 27.1, 5.5, 1.0,
          'Speech-to-Text (ASR)\nReal-time transcription + diarization\nFiller word removal (um/uh/like)', '#0070C0', 'white', 9)
arrow(ax, 4.5, 26.55, 4.5, 25.9)

draw_rect(ax, 4.5, 25.3, 5.5, 1.0,
          'NLP: Conditional Processing\nSimple Mode: jargon to plain language\nTranslation: native to English/target', '#0070C0', 'white', 9)
arrow(ax, 4.5, 24.75, 4.5, 24.1)

draw_rect(ax, 4.5, 23.5, 5.5, 1.0,
          'Text-to-Speech: VIBE Voice\nNeural TTS with user persona\nEmotional tone matching', '#27AE60', 'white', 9)
arrow(ax, 4.5, 22.95, 4.5, 22.3)

draw_para(ax, 4.5, 21.7, 5.5, 1.0,
          'Delivered to All Participants\nCleaned + boosted + translated voice\nPer-user captions in their language', '#2C3E50', 'white', 9)

p_type = mpatches.FancyBboxPatch((11.7, 26.0), 10.0, 7.0, boxstyle="round,pad=0.15",
                                   facecolor='#0070C0', edgecolor='#0070C0', linewidth=2, alpha=0.08)
ax.add_patch(p_type)
ax.text(12.5, 32.6, 'C: TYPE-TO-SPEAK PATH', fontsize=13, fontweight='bold', color='#0070C0')

draw_rect(ax, 17.5, 32.5, 5.5, 0.9,
          'User Switches to Type-to-Speak\nTrigger: muted / noisy / speech difficulty', '#0070C0', 'white', 9)
arrow(ax, 17.5, 32.0, 17.5, 31.3)

draw_rect(ax, 17.5, 30.7, 5.5, 1.0,
          'User Types in VIBE Panel\nAny language - can paste code/data\nDraft visible only to user before send', '#0070C0', 'white', 9)
arrow(ax, 17.5, 30.15, 17.5, 29.5)

draw_rect(ax, 17.5, 28.9, 5.5, 1.0,
          'NLP Processing\nDetect language + intent\nSimplify or translate to meeting lang\nPolish mode: draft to fluent speech', '#1A5276', 'white', 9)
arrow(ax, 17.5, 28.35, 17.5, 27.7)

draw_rect(ax, 17.5, 27.1, 5.5, 1.0,
          'VIBE Agent Speaks for User\nNeural TTS speaks typed message\nLabel: "Spoken by VIBE for [User]"', '#27AE60', 'white', 9)
arrow(ax, 17.5, 26.55, 17.5, 25.9)

draw_rect(ax, 17.5, 25.3, 5.5, 1.0,
          'Caption & Chat Sync\n"from [User] via VIBE" tag\nTranscript logs typed + spoken', '#0070C0', 'white', 9)

arrow(ax, 4.5, 21.15, 4.5, 20.3)
arrow(ax, 17.5, 24.75, 17.5, 20.3)
arrow(ax, 17.5, 20.3, 11.5, 20.3, '#333333')
arrow(ax, 4.5, 20.3, 10.5, 20.3, '#333333')

p_qa = mpatches.FancyBboxPatch((0.3, 14.0), 21.4, 6.0, boxstyle="round,pad=0.15",
                                 facecolor='#8E44AD', edgecolor='#8E44AD', linewidth=2, alpha=0.08)
ax.add_patch(p_qa)
ax.text(1.0, 19.6, 'D: Q&A CLOSE-LOOP (NON-NATIVE / NON-TECH USERS)', fontsize=13, fontweight='bold', color='#8E44AD')

draw_rect(ax, 5.0, 19.5, 5.5, 0.9,
          'User Asks in Own Language\nVoice or Type-to-Speak - any language', '#8E44AD', 'white', 10)
arrow(ax, 5.0, 19.0, 5.0, 18.2)

draw_rect(ax, 5.0, 17.6, 5.5, 1.0,
          'ASR + Translation to English\nPresenter sees translated question\nwith speaker attribution', '#8E44AD', 'white', 9)
arrow(ax, 7.8, 17.6, 11.0, 17.6, '#333333')

draw_rect(ax, 13.5, 17.6, 5.0, 1.0,
          'Presenter Answers in English\nVIBE captures answer in real-time\nCan tag as "Simplified answer"', '#0070C0', 'white', 9)
arrow(ax, 13.5, 17.05, 13.5, 16.2)

draw_rect(ax, 11, 15.5, 7.0, 1.2,
          'Translation + Simplification Back to User\nEnglish answer translated to native language\nSimple Mode adds analogy + concrete example', '#8E44AD', 'white', 10)
arrow(ax, 11, 14.85, 11, 14.2)

draw_rect(ax, 5.0, 13.5, 4.5, 1.0,
          'Audio Output\nAnswer spoken in native\nlanguage via VIBE voice', '#27AE60', 'white', 9)
draw_rect(ax, 17.0, 13.5, 4.5, 1.0,
          'Text Output\nSimplified text + analogy\nin user caption pane', '#0070C0', 'white', 9)
arrow(ax, 11 - 2.0, 14.2, 5.0, 14.05, '#333333')
arrow(ax, 11 + 2.0, 14.2, 17.0, 14.05, '#333333')

arrow(ax, 5.0, 12.95, 5.0, 12.0)
arrow(ax, 17.0, 12.95, 17.0, 12.0)
arrow(ax, 5.0, 12.0, 10.5, 12.0, '#333333')
arrow(ax, 17.0, 12.0, 11.5, 12.0, '#333333')

p_end = mpatches.FancyBboxPatch((0.3, 5.5), 21.4, 6.2, boxstyle="round,pad=0.15",
                                  facecolor='#D35400', edgecolor='#D35400', linewidth=2, alpha=0.08)
ax.add_patch(p_end)
ax.text(1.0, 11.3, 'E: END & LOGGING', fontsize=13, fontweight='bold', color='#D35400')

draw_oval(ax, 11, 11.3, 5.0, 0.9, 'MEETING ENDS', '#D35400', 'white', 12)
arrow(ax, 11, 10.8, 11, 10.2)

draw_rect(ax, 4.5, 9.5, 5.0, 1.2,
          'VIBE Transcript\nOriginal language layer\nEnglish translation layer\nSimplified text layer\nSpeaker IDs + timestamps', '#D35400', 'white', 9)

draw_rect(ax, 11, 9.5, 5.0, 1.2,
          'VIBE Summary Pack\nKey Q&A in native language\nSimple explanations + examples\nDownloadable per-user\nShareable via Webex/email', '#D35400', 'white', 9)

draw_rect(ax, 17.5, 9.5, 5.0, 1.2,
          'Session Analytics\nVoice clarity score trend\nTranslation accuracy log\nQ&A resolution rate\nVIBE usage breakdown', '#D35400', 'white', 9)

arrow(ax, 11, 10.2, 4.5, 10.15, '#333333')
arrow(ax, 11, 10.2, 17.5, 10.15, '#333333')

arrow(ax, 4.5, 8.85, 4.5, 8.0)
arrow(ax, 11, 8.85, 11, 8.0)
arrow(ax, 17.5, 8.85, 17.5, 8.0)
arrow(ax, 4.5, 8.0, 10.5, 7.5, '#333333')
arrow(ax, 17.5, 8.0, 11.5, 7.5, '#333333')

draw_cyl(ax, 11, 6.8, 7.0, 1.5,
         'Privacy Guarantee: Transparency & Trust Layer\nEvery VIBE voice labeled "Spoken by VIBE for [User]"\nFull audit trail | Zero data retention option | No deepfakes', '#002060', 'white', 9)

arrow(ax, 11, 5.95, 11, 5.3)
draw_oval(ax, 11, 4.8, 6.0, 0.9, 'END: VIBE Session Complete', '#002060', 'white', 12)

tech_box = mpatches.FancyBboxPatch((0.3, 1.5), 21.4, 2.8, boxstyle='round,pad=0.1',
                                     facecolor='#002060', edgecolor='black', linewidth=2)
ax.add_patch(tech_box)
ax.text(11, 3.8, 'TECH STACK', ha='center', fontsize=11, fontweight='bold', color='#FFD700')
ax.text(11, 3.2, 'ASR: Whisper / Cisco AI  |  NLP: Custom LLM + Rules  |  TTS: Neural Voice Synthesis',
        ha='center', fontsize=10, fontweight='bold', color='white')
ax.text(11, 2.6, 'MT: Neural Machine Translation (100+ languages)  |  DSP: DNN Noise + EQ  |  Codec: Webex AI Codec',
        ha='center', fontsize=10, fontweight='bold', color='white')
ax.text(11, 2.0, 'KPIs: Noise reduction 95%+ | ASR accuracy 98% | Translation latency <1s | TTS naturalness 4.5/5 | Type-to-speak <2s',
        ha='center', fontsize=9, fontweight='bold', color='#FFD700')

plt.tight_layout()
plt.savefig('cisco_case/figures/flowchart_2_vibe.png', dpi=200, bbox_inches='tight')
plt.close()
print("Flowchart 2 (VIBE - Voice & Language Intelligence Layer) created")

# ============================================================
# FLOWCHART 3: Secure AI Agent Marketplace Ecosystem
# (Enhanced - kept same structure with minor updates)
# ============================================================
fig, ax = plt.subplots(figsize=(18, 38))
ax.set_xlim(0, 18)
ax.set_ylim(0, 38)
ax.axis('off')

ax.text(9, 37.4, 'Solution 3: Secure AI Agent Marketplace', ha='center',
        fontsize=24, fontweight='bold', color='#002060')
ax.text(9, 36.8, 'Build -> Certify -> Deploy -> Monitor Lifecycle  |  100s of Third-Party Integrations', ha='center',
        fontsize=14, color='#555555')

CX = 9.0

draw_oval(ax, CX, 36.0, 6.0, 0.9, 'START\nDeveloper Registers on Platform', '#002060', 'white', 12)
arrow(ax, CX, 35.5, CX, 34.9)

p1 = mpatches.FancyBboxPatch((0.5, 29.5), 17.0, 5.2, boxstyle="round,pad=0.15",
                               facecolor='#1A5276', edgecolor='#1A5276', linewidth=2, alpha=0.08)
ax.add_patch(p1)
ax.text(1.2, 34.3, 'PHASE 1: BUILD', fontsize=14, fontweight='bold', color='#1A5276')

draw_rect(ax, CX, 34.3, 8.0, 1.0,
          'Download Agent SDK (Python / JavaScript)\nTemplates, API docs, A2A protocol reference', '#1A5276', 'white', 11)
arrow(ax, CX, 33.75, CX, 33.1)

draw_rect(ax, CX, 32.5, 8.0, 1.0,
          'Developer Builds Custom Agent\nDefine triggers, actions, data scope, permissions', '#1A5276', 'white', 11)
arrow(ax, CX, 31.95, CX, 31.3)

draw_rect(ax, CX, 30.7, 8.0, 1.0,
          'Test in Sandbox Environment\nSimulates real meetings, API calls, edge cases\nNo production access required', '#1A5276', 'white', 11)
arrow(ax, CX, 30.15, CX, 29.3)

draw_diamond(ax, CX, 28.3, 2.0, 'Tests\nPass?', '#F39C12', 'black', 11)

ax.text(CX - 3.0, 28.3, 'NO', fontsize=12, fontweight='bold', color='#E74C3C')
arrow(ax, CX - 1.0, 28.3, CX - 3.8, 28.3, '#E74C3C', 2)
arrow(ax, CX - 3.8, 28.3, CX - 3.8, 32.5, '#E74C3C', 2)
arrow(ax, CX - 3.8, 32.5, CX - 4.2, 32.5, '#E74C3C', 2)
ax.text(CX - 3.8, 30.3, 'Fix &\nRetry', fontsize=9, fontweight='bold', color='#E74C3C', ha='center',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#E74C3C', alpha=0.9))

ax.text(CX + 2.0, 28.3, 'YES', fontsize=12, fontweight='bold', color='#27AE60')
arrow(ax, CX, 27.3, CX, 26.7)

draw_rect(ax, CX, 26.1, 8.0, 1.0,
          'Submit Agent to Cisco Marketplace Portal\nUpload manifest, documentation, permission declaration', '#1A5276', 'white', 11)
arrow(ax, CX, 25.55, CX, 24.9)

p2 = mpatches.FancyBboxPatch((0.5, 20.0), 17.0, 4.7, boxstyle="round,pad=0.15",
                               facecolor='#27AE60', edgecolor='#27AE60', linewidth=2, alpha=0.08)
ax.add_patch(p2)
ax.text(1.2, 24.3, 'PHASE 2: CERTIFY (Cisco Security Pipeline)', fontsize=14, fontweight='bold', color='#27AE60')

draw_rect(ax, CX, 24.3, 8.0, 1.0,
          'Security Scan: Static code analysis, vulnerability detection,\ndata access audit, compliance check (SOC2 / HIPAA / FedRAMP)', '#27AE60', 'white', 11)
arrow(ax, CX, 23.75, CX, 23.1)

draw_rect(ax, CX, 22.5, 8.0, 1.0,
          'Permission Review: Zero-trust policy enforcement,\nminimum-privilege validation, PII handling assessment', '#27AE60', 'white', 11)
arrow(ax, CX, 21.95, CX, 21.3)

draw_rect(ax, CX, 20.7, 8.0, 1.0,
          'Performance Testing: Latency benchmarks (< 200ms),\nload testing (1000+ concurrent users), failure recovery', '#27AE60', 'white', 11)
arrow(ax, CX, 20.15, CX, 19.3)

draw_diamond(ax, CX, 18.3, 2.2, 'Cisco\nCertified?', '#F39C12', 'black', 11)

ax.text(CX - 3.2, 18.3, 'FAIL', fontsize=12, fontweight='bold', color='#E74C3C')
arrow(ax, CX - 1.1, 18.3, CX - 4.0, 18.3, '#E74C3C', 2)
draw_rect(ax, CX - 5.5, 18.3, 3.0, 0.8,
          'Return to developer\nwith feedback report', '#E74C3C', 'white', 9)

ax.text(CX + 2.2, 18.3, 'PASS', fontsize=12, fontweight='bold', color='#27AE60')
arrow(ax, CX, 17.2, CX, 16.6)

draw_rect(ax, CX, 16.0, 8.0, 1.0,
          'Cisco Trust Badge Issued: "Cisco Verified Agent"\nListed in Marketplace catalog with security rating', '#27AE60', 'white', 11)
arrow(ax, CX, 15.45, CX, 14.8)

p3 = mpatches.FancyBboxPatch((0.5, 11.5), 17.0, 3.1, boxstyle="round,pad=0.15",
                               facecolor='#0070C0', edgecolor='#0070C0', linewidth=2, alpha=0.08)
ax.add_patch(p3)
ax.text(1.2, 14.2, 'PHASE 3: DEPLOY', fontsize=14, fontweight='bold', color='#0070C0')

draw_rect(ax, CX, 14.2, 8.0, 1.0,
          'Enterprise Admin browses marketplace, selects agent,\nconfigures team access, permissions, and usage limits', '#0070C0', 'white', 11)
arrow(ax, CX, 13.65, CX, 13.0)

draw_diamond(ax, CX, 12.0, 2.0, 'Admin\nApproves?', '#F39C12', 'black', 11)

ax.text(CX - 2.8, 12.0, 'NO', fontsize=12, fontweight='bold', color='#E74C3C')
arrow(ax, CX - 1.0, 12.0, CX - 2.2, 12.0, '#E74C3C', 2)

ax.text(CX + 2.0, 12.0, 'YES', fontsize=12, fontweight='bold', color='#27AE60')
arrow(ax, CX, 11.0, CX, 10.4)

draw_rect(ax, CX, 9.8, 8.0, 1.0,
          'Agent deployed in sandboxed container (Webex Cloud)\nIsolated execution, strict network policies, resource limits', '#0070C0', 'white', 11)
arrow(ax, CX, 9.25, CX, 8.6)

p4 = mpatches.FancyBboxPatch((0.5, 4.5), 17.0, 4.3, boxstyle="round,pad=0.15",
                               facecolor='#8E44AD', edgecolor='#8E44AD', linewidth=2, alpha=0.08)
ax.add_patch(p4)
ax.text(1.2, 8.4, 'PHASE 4: MONITOR (Splunk-Powered)', fontsize=14, fontweight='bold', color='#8E44AD')

draw_rect(ax, CX, 8.0, 8.0, 1.0,
          'Splunk monitors: agent performance, error rates, anomalies\nUsage analytics, ROI dashboards, automated alerts', '#8E44AD', 'white', 11)
arrow(ax, CX, 7.45, CX, 6.6)

draw_diamond(ax, CX, 5.6, 2.0, 'Alert\nTriggered?', '#F39C12', 'black', 11)

ax.text(CX + 2.8, 5.6, 'YES: Kill Switch\n(auto-disable agent)', fontsize=10, fontweight='bold', color='#E74C3C',
        ha='left', va='center',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#FADBD8', edgecolor='#E74C3C', linewidth=1.5))
arrow(ax, CX + 1.0, 5.6, CX + 2.3, 5.6, '#E74C3C', 2)

ax.text(CX - 2.8, 5.6, 'NO: Continue\nmonitoring', fontsize=10, fontweight='bold', color='#27AE60',
        ha='right', va='center',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#D5F5E3', edgecolor='#27AE60', linewidth=1.5))
arrow(ax, CX - 1.0, 5.6, CX - 2.0, 5.6, '#27AE60', 2)

arrow(ax, CX, 4.6, CX, 3.8)

draw_oval(ax, CX, 3.2, 8.0, 0.9, 'Billing & Revenue Share (70/30 developer split)\nAgent runs continuously in Webex', '#002060', 'white', 10)

mr = mpatches.FancyBboxPatch((0.5, 1.5), 17.0, 0.8, boxstyle='round,pad=0.1',
                               facecolor='#002060', edgecolor='black', linewidth=2)
ax.add_patch(mr)
ax.text(9, 1.9, 'IMPACT: 500+ certified agents Year 1  |  $150M GMV by FY2028  |  '
        '3x ecosystem growth  |  85% renewal rate',
        ha='center', va='center', fontsize=11, fontweight='bold', color='white')

plt.tight_layout()
plt.savefig('cisco_case/figures/flowchart_3_marketplace.png', dpi=200, bbox_inches='tight')
plt.close()
print("Flowchart 3 (Marketplace Ecosystem) created")


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
    pdf.set_left_margin(25.4)
    pdf.set_x(25.4 + INDENT)
    pdf.set_left_margin(25.4 + INDENT)
    pdf.multi_cell(0, LH, f'- {text}')
    pdf.set_left_margin(25.4)

def sub_bullet(pdf, text):
    pdf.set_font('Times', '', 12)
    pdf.set_left_margin(25.4)
    pdf.set_x(25.4 + INDENT * 2)
    pdf.set_left_margin(25.4 + INDENT * 2)
    pdf.multi_cell(0, LH, f'- {text}')
    pdf.set_left_margin(25.4)

def source_note(pdf, text):
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
bullet(pdf, 'Auto-Slide Generation: If the presenter opts in, Webex AI generates a first-draft slide deck using meeting context and enterprise data (CRM pipeline, Jira issues, financial metrics), organized into the proposed agenda. The presenter can edit and finalize this deck inside Webex or a connected slides tool.')
bullet(pdf, 'Predicted Q&A: The AI predicts likely questions based on role, history, and topic (e.g., "What is the impact on ACME\'s renewal?"), and suggests draft answers the presenter can review, refine, or reject. This seeds the system to recognize and handle these questions during the live meeting.')
pdf.ln(1)

body_bold(pdf, 'PERCEIVE Phase: Webex AI Codec ML Pipeline')
body(pdf, 'During the live meeting, the existing Webex AI Codec serves as the perception layer. Raw audio and video streams pass through a multi-stage ML pipeline:')
bullet(pdf, 'Deep Neural Network (DNN) Noise Removal: Real-time models remove background noise (keyboards, dogs, construction, etc.), isolating clean speech.')
bullet(pdf, 'Neural Speech Synthesis Codec: Cleaned audio is compressed using a neural codec to maintain high quality even on low bandwidth, ensuring both human participants and AI models receive clear signals.')
bullet(pdf, 'Real-Time Media Models (RMM): AI upscales low-resolution video, separates individual speakers, and detects gestures/reactions to better understand who is speaking and when emphasis or agreement occurs.')
bullet(pdf, 'NLP Engine: Speech is converted to text with real-time transcription and translation. The NLP layer identifies task-related statements, decisions, commitments, and live occurrences of the predicted questions generated during the PREPARE phase.')
pdf.ln(1)

body_bold(pdf, 'REASON Phase: Context Retrieval and Task Planning')
body(pdf, 'When the NLP engine detects a potential task intent or a recognized predicted question, the reasoning phase is activated:')
bullet(pdf, 'Context Retrieval via Agent-to-Agent (A2A) Protocols: Webex AI communicates with external system agents (Jira, Salesforce, GitHub, ServiceNow) through standardized protocols to retrieve relevant context: project details, customer records, previous tickets, or sprint information.')
bullet(pdf, 'Cisco Secure Data Fabric & Observability: All retrieval passes through Cisco\'s zero-trust identity and access layer. Every call is monitored via Splunk observability tools to detect anomalies, unauthorized access patterns, and performance issues.')
bullet(pdf, 'LLM-Based Task and Answer Planning: A large language model synthesizes live meeting context, retrieved system data, and organizational policies to generate either a complete task draft (Jira ticket, CRM update, follow-up email) or a suggested answer and follow-up plan for a question the presenter could not answer live.')
pdf.ln(1)

body_bold(pdf, 'ACT Phase: In-Meeting Human Verification and Execution')
body(pdf, 'Before anything is committed externally, Webex keeps a human firmly in the loop:')
bullet(pdf, 'In-Meeting Draft Cards: The user sees a non-disruptive overlay in the Webex interface showing the fully drafted task artifact (Jira ticket, ServiceNow incident, Salesforce update, etc.) or a draft follow-up response.')
bullet(pdf, 'Approve / Edit / Reject Controls: The user can approve to execute as-is, edit to modify fields (title, description, assignee, due date), or reject to discard the draft.')
bullet(pdf, 'Secure Execution & Logging: On approval, the agent executes through authenticated API calls. Every step from detection to execution is logged for auditing and compliance, including who approved which change and when.')
bullet(pdf, 'Meeting Chat Confirmation: Webex posts a concise confirmation back into the meeting chat (e.g., "Jira ticket WEBAPP-2026-347 created and assigned to Sarah Chen; Priority: High").')
pdf.ln(1)

body_bold(pdf, 'FOLLOW-UP Phase: Structured Q&A and Post-Meeting Delivery')
body(pdf, 'After the meeting ends, Webex AI ensures that open loops are closed:')
bullet(pdf, 'Unanswered Question Detection: Using the transcript and the predicted Q&A patterns from the PREPARE phase, the system identifies questions that were asked but not answered or explicitly deferred.')
bullet(pdf, 'Q&A Follow-Up Drafts: For each unanswered question, the AI drafts a suggested response based on the same enterprise context used in the REASON phase and presents it to the owner for approval/edit.')
bullet(pdf, 'Multi-Channel Delivery: Once approved, Webex automatically sends answers to the relevant participants via their preferred channels (Webex spaces, email, or other integrated systems), optionally simplifying the language for non-technical or non-native speakers.')
bullet(pdf, 'Visibility & Observability: All follow-up actions are logged and visible to admins through observability dashboards, enabling organizations to measure completion rates for post-meeting Q&A and follow-up quality.')
pdf.ln(1)

subheading(pdf, 'Why This Enhanced Solution Wins')
body(pdf, 'This enhanced solution addresses two critical gaps simultaneously. First, it brings Webex from a passive summarization tool to an agentic AI system that can help users prepare more effectively (auto-decks, predicted Q&A, checklists), execute tasks in third-party systems from live conversation with human-in-the-loop, and close the loop with structured post-meeting answers. Second, it does so in a way that aligns with Cisco\'s strengths: enterprise-grade security, compliance, and observability for task execution; AI codec and media models that already enhance audio/video quality; and a runway to integrate tightly with the AI agent marketplace and Splunk-powered monitoring.')

body(pdf, 'Where Microsoft Copilot and Zoom AI Companion focus primarily on content generation and partial task execution inside their own ecosystems, Webex can differentiate by owning the full Prepare-Perceive-Reason-Act-Follow-Up loop with strong guardrails and regulated-industry readiness.')

subheading(pdf, 'Expected Impact')
bullet(pdf, 'Reduces manual post-meeting data entry by 15 minutes per meeting')
bullet(pdf, '25% meeting-to-action conversion rate (vs. current ~5% industry average)')
bullet(pdf, '40% workflow automation rate within 12 months of deployment')
bullet(pdf, '85% task completion accuracy with human-in-the-loop verification')
bullet(pdf, '35% increase in daily active Webex usage as the platform becomes a productivity hub')
bullet(pdf, '90%+ Q&A resolution rate through structured post-meeting follow-up')
pdf.ln(2)
source_note(pdf, 'Sources: Cisco FY2024 10-K; Webex AI Codec documentation; MarketsandMarkets Agentic AI Market Report 2024; Microsoft Copilot & Zoom AI Companion product documentation.')

subheading(pdf, 'Solution 1 Flowchart: Prepare-Perceive-Reason-Act-Follow-Up')
body(pdf, 'The following flowchart details the complete five-phase architecture, including pre-meeting AI prep, the Webex AI Codec ML pipeline, data fabric integration, human-in-the-loop verification, cross-platform task execution, and post-meeting Q&A follow-up.')
pdf.ln(2)

img_w = W
pdf.image('cisco_case/figures/flowchart_1_agentic_ai.png', x=pdf.l_margin, w=img_w)

# ============================================================
# PROBLEM 2: VIBE
# ============================================================
pdf.add_page()
heading(pdf, 'Problem 2: Webex Meetings Exclude Non-Native and Non-Technical Participants')

subheading(pdf, 'Problem Definition')
body(pdf, 'Hybrid and global workforces are now the norm. Enterprises routinely run meetings with participants spread across countries, languages, and technical backgrounds. Yet collaboration platforms, including Webex, treat meetings as though everyone speaks fluent English, understands technical jargon, has a quiet environment, and can always speak aloud. This assumption creates systemic exclusion:')

bullet(pdf, 'Language barriers: Non-native English speakers struggle to follow fast-paced discussions, miss nuances, and hesitate to ask questions. Even with basic translation features, the experience is fragmented: captions lag, context is lost, and speakers must slow down or repeat themselves.')
bullet(pdf, 'Technical jargon: In cross-functional meetings (engineering + sales + leadership), technical terminology alienates non-technical participants. When an engineer says "the API rate limiter is throttling at the gateway," a sales leader hears noise, not information.')
bullet(pdf, 'Poor audio quality: Users in noisy environments (cafes, open offices, public transit) produce audio that degrades the experience for all participants. Background noise, echo, and low volume make it difficult to understand speakers and impossible for AI transcription to work accurately.')
bullet(pdf, 'Inability to speak: Some participants cannot speak aloud due to noise, broken microphones, speech difficulties, or social anxiety in large meetings. These users are effectively silenced, reducing meeting participation and diversity of input.')

body(pdf, 'The combined effect is that a significant portion of meeting participants are passive observers rather than active contributors. This reduces the quality of decisions, lowers engagement, and creates an uneven playing field that undermines the value of bringing diverse, global teams together.')

subheading(pdf, 'Competitive Gap Analysis')
body(pdf, 'Microsoft Teams offers live captions and basic translation, but these are read-only text overlays that do not address voice quality, jargon simplification, or the inability to speak. Zoom provides similar caption-based translation features. Neither platform offers a comprehensive voice intelligence layer that cleans, boosts, translates, simplifies, and speaks on behalf of users in real-time. The market opportunity is an integrated, in-meeting voice and language AI layer that makes every participant equally capable, regardless of language, technical background, or environment.')

subheading(pdf, 'Business Impact of the Problem')
bullet(pdf, 'Reduced meeting ROI: When 30-40% of participants cannot fully engage due to language or audio barriers, meetings produce lower-quality decisions and require follow-up conversations to clarify what was discussed.')
bullet(pdf, 'Global team friction: Multinational enterprises report that language barriers are the number one obstacle to effective cross-border collaboration, ahead of time zones and cultural differences.')
bullet(pdf, 'Accessibility gaps: Users with speech difficulties, hearing impairments, or social anxiety are systematically excluded from verbal participation, reducing inclusion and diversity of input.')
bullet(pdf, 'Competitive vulnerability: As enterprises prioritize DEI (Diversity, Equity, and Inclusion) in technology procurement, platforms that do not actively solve participation barriers will lose to those that do.')
pdf.ln(2)

subheading(pdf, 'Solution 2: VIBE - Voice & Language Intelligence Layer')

body(pdf, 'VIBE (Voice & Language Intelligence Layer) is a real-time, in-meeting voice and language AI layer that boosts and cleans voice quality, translates between native and English in both speech and text, simplifies technical jargon for non-technical users, and enables type-to-speak so VIBE speaks on the user\'s behalf. All inside Webex. No deepfake risk. Every action is auditable and transparent.')

body_bold(pdf, 'A: User Entry & Onboarding')
body(pdf, 'When a user joins a Webex meeting, VIBE activation is simple and instant:')
bullet(pdf, 'Toggle Activation: A VIBE toggle appears in the meeting controls bar. Zero configuration is required to activate.')
bullet(pdf, 'Mode Selection: Users select one or more active modes simultaneously: Voice Boost, Live Translation, Type-to-Speak, and/or Simple Mode (non-technical jargon simplification).')
bullet(pdf, 'Language & Profile: Users select their native language (Hindi, Spanish, Mandarin, French, Arabic, Portuguese, Japanese, Korean, and 90+ more via neural machine translation), their tech level (Technical or Non-Technical), and a voice preset (Clear, Loud, Warm, or Broadcast-style).')
pdf.ln(1)

body_bold(pdf, 'B: Live Audio Path - When User Speaks')
body(pdf, 'When the user speaks, VIBE processes the audio through a full intelligence pipeline:')
bullet(pdf, 'Microphone Audio Captured: Raw PCM stream with per-speaker separation via Webex AI Codec and real-time buffer pipeline.')
bullet(pdf, 'Audio Intelligence Front-End: DNN noise removal for 150+ noise types (cafe, keyboard, HVAC, crowd), echo cancellation and auto gain control, audio tuned to VIBE mode with optimized EQ profile per preset, and smart room detection with reverb and acoustic fingerprint adjustment.')
bullet(pdf, 'Voice Boost & EQ Engine: Applies the selected preset (Clear, Loud, Warm, Broadcast-style), adapts to environment (noisy cafe vs. quiet office vs. conference room), normalizes waveform for consistent output level to all participants.')
bullet(pdf, 'Speech-to-Text (ASR): Real-time transcription in user\'s native language with multi-accent support, per-speaker diarization (who said what, timestamped), and filler word detection that removes "um," "uh," and "like" from the clean transcript.')
bullet(pdf, 'NLP Layer - Conditional Processing: Detects language, intent, domain, tech level, and sentiment. Simple Mode rewrites jargon to plain language with real-world analogies (e.g., "API" becomes "a waiter between kitchen and table"). Translation converts native language to English or any target language. Always-active features include intent and domain tagging, clarity scoring, and real-time caption preparation.')
bullet(pdf, 'Text-to-Speech Output - VIBE Voice: Converts processed/translated text to natural neural speech with a consistent VIBE persona voice identity per user across the session. Emotional tone matching ensures excited text is delivered with energy.')
bullet(pdf, 'Delivered to All Participants: Participants hear cleaned, boosted, and translated VIBE voice. Per-user captions appear in their own selected language. Each attendee independently controls their own caption language.')
pdf.ln(1)

body_bold(pdf, 'C: Type-to-Speak Path - When User Cannot Speak')
body(pdf, 'For users who are muted, in noisy environments, have a broken microphone, experience speech difficulties, or feel shy in large meetings:')
bullet(pdf, 'Mode Activation: User switches to Type-to-Speak manually, or VIBE auto-suggests the mode switch when it detects prolonged silence combined with high ambient noise.')
bullet(pdf, 'Text Input: User types in the VIBE panel or chat in any language. They can paste code, data, or tables. Drafts are visible only to the user before sending.')
bullet(pdf, 'NLP Processing: VIBE detects language and intent, simplifies or professionalizes based on active mode, translates to the meeting language (English by default), and applies "Polish mode" to convert quick drafts into fluent spoken-style language.')
bullet(pdf, 'VIBE Agent Speaks: Neural TTS voice speaks the typed message aloud in the meeting. On-screen label always displays "Spoken by VIBE for [UserName]," ensuring full transparency with no deception. Users select from three VIBE voice personas per session.')
bullet(pdf, 'Caption & Chat Sync: Captions display "from [UserName] via VIBE" with the source tag auto-appended to the meeting transcript. Chat thread logs typed input and spoken output side-by-side.')
pdf.ln(1)

body_bold(pdf, 'D: Q&A Close-Loop for Non-Native / Non-Technical Users')
body(pdf, 'VIBE enables seamless cross-language Q&A during meetings:')
bullet(pdf, 'User Asks in Own Language: A user asks a question using voice or Type-to-Speak in any language (e.g., "API integration kaise kaam karti hai?" in Hindi or "Cuanto cuesta el plan?" in Spanish).')
bullet(pdf, 'ASR + Translation to English: The native speech is converted to English text and displayed as a caption to the presenter (e.g., "[Priya] asked (translated): How does the API integration work?").')
bullet(pdf, 'Presenter Answers in English: The presenter responds normally. VIBE captures the answer in real-time. The presenter can tag the response as "Simplified answer" to trigger extra NLP treatment.')
bullet(pdf, 'Translation + Simplification Back to User: The English answer is translated to the user\'s native language. Simple Mode adds an analogy and concrete example (e.g., "Think of an API like a power outlet - your device does not need to know how electricity is generated"). Audio output delivers the answer spoken in native language via VIBE voice (private to user), and text output shows simplified text and analogy in the user\'s caption pane, bookmarkable for the VIBE summary.')
pdf.ln(1)

body_bold(pdf, 'E: End & Logging')
body(pdf, 'When the meeting ends, VIBE generates comprehensive session outputs:')
bullet(pdf, 'VIBE Transcript: Multi-layer transcript including original language layer, English translation layer, simplified text layer, timestamps and speaker IDs, and Type-to-Speak logs clearly marked.')
bullet(pdf, 'VIBE Summary Pack: Key Q&A in native language with simple explanations and examples, downloadable by each user, shareable via Webex or email.')
bullet(pdf, 'Session Analytics: Voice clarity score trend, translation accuracy log, Q&A resolution rate, and VIBE usage breakdown per participant.')
pdf.ln(1)

body_bold(pdf, 'Privacy Guarantee: Transparency & Trust Layer')
body(pdf, 'VIBE operates with complete transparency and trust:')
bullet(pdf, 'Every VIBE-synthesized voice is labeled on-screen: "Spoken by VIBE for [User]." There is no hidden AI speech.')
bullet(pdf, 'Full audit trail: every VIBE action (boost, translate, TTS) is logged with user consent timestamps.')
bullet(pdf, 'Zero data retention option: transcript is deleted on meeting end if user opts out of VIBE Summary.')
bullet(pdf, 'VIBE never impersonates: the voice persona is distinct from the user\'s actual recorded voice.')
pdf.ln(1)

subheading(pdf, 'Why This Solution Wins')
body(pdf, 'No collaboration platform today offers a unified, real-time voice and language intelligence layer. Teams and Zoom provide basic captions and translation as passive overlays. VIBE goes far beyond by actively improving voice quality, translating in real-time with TTS delivery, simplifying jargon with analogies, and enabling silent users to speak through AI. The Type-to-Speak feature alone addresses an unmet need that no competitor has solved. Combined with Cisco\'s AI Codec technology for noise removal and voice processing, VIBE creates a participation experience that makes every meeting truly inclusive, regardless of language, technical background, or environment.')

subheading(pdf, 'Expected Impact')
bullet(pdf, 'Noise reduction effectiveness: 95%+ across 150+ noise types')
bullet(pdf, 'ASR accuracy: 98% real-time transcription accuracy')
bullet(pdf, 'Translation latency: <1 second end-to-end')
bullet(pdf, 'TTS naturalness: 4.5/5 user rating target')
bullet(pdf, 'Type-to-speak delivery: <2 seconds from send to spoken output')
bullet(pdf, '40% increase in non-native speaker participation rates')
bullet(pdf, '35% reduction in "please repeat that" requests during multilingual meetings')
pdf.ln(2)
source_note(pdf, 'Sources: Cisco Webex AI Codec documentation; Microsoft Work Trend Index 2024 (global workforce statistics); Gartner DEI in Technology Procurement Report 2024.')

subheading(pdf, 'Solution 2 Flowchart: VIBE - Voice & Language Intelligence Layer')
body(pdf, 'The following flowchart details the complete VIBE architecture, including user onboarding, the live audio speak path, type-to-speak path, cross-language Q&A close-loop, session logging, and the privacy and trust layer.')
pdf.ln(2)

pdf.image('cisco_case/figures/flowchart_2_vibe.png', x=pdf.l_margin, w=img_w)

# ============================================================
# PROBLEM 3
# ============================================================
pdf.add_page()
heading(pdf, 'Problem 3: Webex Has a Weaker, Less Strategic Developer Ecosystem')

subheading(pdf, 'Problem Definition')
body(pdf, 'Integration ecosystems are the hidden engines of collaboration platforms. Microsoft Teams offers over 2,000 integrations through its App Marketplace; Zoom supports over 2,500 third-party integrations. These platforms have become "glue layers" that connect nearly every SaaS tool an enterprise uses. Webex, while improving its integration catalog, still lags in scale, depth, and strategic positioning.')

body(pdf, 'Beyond raw connector count, there is a second, more critical gap: intelligence. Today\'s integrations are mostly static, one-off connectors (e.g., "post a Slack message when a Jira ticket is updated") that perform simple, predefined actions. They do not understand meeting context, make decisions, or orchestrate multi-step workflows. The next competitive frontier is AI-driven agents: intelligent, multi-step integrations that can observe, reason, and act autonomously inside a meeting. Yet no platform has launched a dedicated, enterprise-grade AI agent marketplace.')

body(pdf, 'For Webex, this uneven ecosystem creates several problems:')
bullet(pdf, 'Reduced daily utility: Many users treat Webex as a "meetings-only" layer, reserving tasks, CRM updates, and automation for other tools. This reduces stickiness and weakens Webex\'s position in RFPs.')
bullet(pdf, 'Developer disinterest: Developers gravitate toward platforms with large, engaged user bases and clear monetization. Without a compelling differentiator, Webex struggles to attract high-quality AI builders.')
bullet(pdf, 'Procurement friction: Enterprise IT teams evaluate collaboration platforms partly on integration breadth and governance potential. A smaller, less strategic ecosystem makes Webex an easier "tie-breaking loss" when compared to Teams or Zoom.')
bullet(pdf, 'Limited new revenue streams: Webex still relies predominantly on per-seat licensing, with no material marketplace-style revenue from integrations or AI-powered services. As AI becomes commoditized, this model caps growth and margin upside.')

body(pdf, 'The market is ripe for a leapfrog innovation: not more point-to-point connectors, but a new category of AI agents that live inside meetings, act with intelligence, and still obey strict enterprise governance.')

subheading(pdf, 'Competitive Landscape and Market Context')
bullet(pdf, 'Microsoft Teams: Large app catalog built on the Microsoft 365 stack. Copilot operates tightly inside Office apps but does not yet offer a formal AI agent marketplace with third-party AI agents. Integrations are powerful but still largely static and workflow-constrained.')
bullet(pdf, 'Zoom: Strong app marketplace with deep connector coverage. AI Companion provides early agentic behaviors (drafts, action items, CRM sync), but not a fully open, certified AI agent ecosystem. No coherent security governance layer for autonomous agents in regulated industries.')
bullet(pdf, 'Webex: Growing but smaller integration footprint, with strong security and AI coding capabilities, but no dedicated AI agent platform. Remains mostly a "backend-for-video" with AI support rather than a developer-centric AI-agent hub.')

body(pdf, 'Across the market, the next-generation expectation is clear: platforms should not just host apps; they should host intelligent agents that can observe meetings, understand intent, execute multi-step workflows, and operate within a governed, auditable environment. No vendor has yet built a marketplace-like layer that lets developers safely, visibly, and profitably deploy AI agents at scale. This is where Webex can change the game.')

subheading(pdf, 'Business Impact of the Problem')
bullet(pdf, 'Reduced daily utility: Users who cannot connect their daily tools to Webex treat it as a "meetings-only" platform, reducing engagement and stickiness.')
bullet(pdf, 'Developer disinterest: Without a compelling differentiator, developer investment flows to Teams and Zoom.')
bullet(pdf, 'Enterprise adoption friction: A smaller ecosystem creates friction in enterprise procurement decisions.')
bullet(pdf, 'Revenue limitation: Without marketplace revenue, Webex relies solely on seat-based licensing, which limits growth potential.')
pdf.ln(2)

subheading(pdf, 'Solution 3: Webex Secure AI Agent Marketplace')

body(pdf, 'Cisco will launch the Webex Secure AI Agent Marketplace, the industry\'s first enterprise-grade AI agent marketplace that lets developers build, certify, deploy, and monetize AI agents that run inside Webex, while respecting strict security, compliance, and governance boundaries. Unlike traditional app stores, this is not just a catalog of connectors. It is a governed AI operating layer for Webex that provides an SDK and development environment for intelligent agents, enforces a unified security and policy model, and opens a new revenue and ecosystem for Cisco and independent developers. The marketplace operates on a four-stage lifecycle: Build, Certify, Deploy, Monitor.')

body_bold(pdf, 'Stage 1: BUILD - AI Agent SDK & Developer Environment')
body(pdf, 'Developers build agents using a Webex AI Agent SDK that abstracts the complexity of Webex\'s media and AI infrastructure:')
bullet(pdf, 'Agent SDK (Python / JavaScript): Pre-built components for common patterns: "Meeting listener," "Task executor," "Data retriever," "Notification sender." Developers can create AI agents that react to meeting context in hours, not weeks.')
bullet(pdf, 'Agent Templates: Ready-to-customize templates for common scenarios (CRM updater, ticket creator, document generator, calendar scheduler). Templates reduce development time by up to 60% and standardize best practices.')
bullet(pdf, 'Sandbox Environment: A cloud-based testing environment that simulates real Webex meetings, API calls, and data flows. Developers can test their agents against realistic conversation data and edge cases without touching production.')
bullet(pdf, 'API & A2A Reference: Clear documentation for meeting lifecycle, real-time transcription feeds, user-context APIs, and Agent-to-Agent (A2A) protocols for cross-tool orchestration. Ensures agents can interact with external systems (Jira, Salesforce, Slack, etc.) in a controlled manner.')
pdf.ln(1)

body_bold(pdf, 'Stage 2: CERTIFY - Cisco Security & Compliance Pipeline')
body(pdf, 'This is the strategic differentiator. Every agent must pass a Cisco Security Certification Pipeline before appearing in the marketplace:')
bullet(pdf, 'Static Code Analysis: Automated scanning for vulnerabilities, backdoors, data-exfiltration patterns, and insecure API usage. Ensures agents do not silently leak data or execute unauthorized commands.')
bullet(pdf, 'Permission & Scope Validation: Reviews what data the agent declares it needs and verifies that it matches actual code behavior. Cisco\'s zero-trust data fabric enforces minimum-privilege principles: agents can only access data and systems explicitly authorized.')
bullet(pdf, 'Performance & Reliability Testing: Latency benchmarks (<200 ms response time), load testing (1,000+ concurrent users), CPU/memory profiling, and failure-recovery validation. Ensures agents do not destabilize Webex or external systems.')
bullet(pdf, 'Compliance Checks: Automated checks against SOC 2, HIPAA, FedRAMP, GDPR, and other regulatory standards based on the agent\'s declared data-handling practices. Agents handling sensitive data are flagged for stricter review.')
bullet(pdf, 'Cisco Trust Badge: Agents that pass all certification stages receive the "Cisco Verified Agent" badge, signaling to enterprises that they meet Cisco\'s security and compliance bar.')
pdf.ln(1)

body_bold(pdf, 'Stage 3: DEPLOY - Enterprise-Grade Management & Deployment')
body(pdf, 'Enterprise IT administrators control how and where agents run:')
bullet(pdf, 'Marketplace Discovery & Curation: Admins browse agents by industry vertical (healthcare, finance, government, manufacturing), use case (sales, support, HR, engineering), and security level (e.g., "no PII access," "customer-facing compliant"). A "Cisco Verified" filter highlights fully certified agents.')
bullet(pdf, 'Configuration & Scoping: Admins define which teams or orgs can use each agent, what data and systems an agent can access, approval workflows (e.g., "high-risk actions require manager approval"), and usage limits and budgets.')
bullet(pdf, 'Sandboxed, Isolated Execution: Deployed agents run in isolated containers inside Webex Cloud, with strict resource and network policies. Agents cannot directly access unapproved systems or data, preventing lateral-move attacks.')
bullet(pdf, 'Gradual Rollout & A/B Testing: Admins can deploy agents to pilot groups first, compare productivity metrics, and then expand across the organization. This reduces change-management risk and provides data for ROI calculations.')
pdf.ln(1)

body_bold(pdf, 'Stage 4: MONITOR - Splunk-Powered Observability & Governance')
body(pdf, 'Once agents are deployed, Cisco provides continuous observability:')
bullet(pdf, 'Real-Time Dashboards: Metrics per agent (response time, success rate, error rate, CPU/memory/API usage) and aggregated usage analytics (active users, invocations per day, top-used agents).')
bullet(pdf, 'Anomaly Detection & Alerting: Machine-learning-based anomaly detection flags unexpected data-access patterns, performance degradation, and security-policy violations. Automated alerts notify IT teams instantly.')
bullet(pdf, 'Kill-Switch & Audit Trail: If an agent behaves suspiciously, admins can immediately deactivate it. Full audit trail preserves logs for compliance and forensic review.')
bullet(pdf, 'Usage Analytics & Billing: Granular per-agent usage tracking enables pay-per-use pricing or subscription-based models. Revenue is shared between Cisco and developers (70/30 split favoring developers to stimulate ecosystem growth).')
pdf.ln(1)

subheading(pdf, 'Why This Solution Wins')
body(pdf, 'The Secure AI Agent Marketplace changes the game in three ways:')
bullet(pdf, 'Trust-First AI: Cisco\'s security certifications, zero-trust data fabric, and Splunk-powered observability create a level of enterprise-grade governance that neither Microsoft nor Zoom can match. Regulated industries (government, healthcare, finance) can safely experiment with AI agents inside Webex while satisfying strict compliance requirements.')
bullet(pdf, 'Platform-Level Differentiation: Instead of competing on "who has more connectors?" Webex competes on "who has the most intelligent, safest, and most profitable AI agent ecosystem?" The marketplace instantly becomes a developer magnet, pulling in AI-first builders who want to reach enterprises securely.')
bullet(pdf, 'New Revenue & Network Effects: Webex transitions from pure per-seat licensing to per-seat plus per-agent monetization (commissions, premium agents, usage-based fees). As more agents appear, more enterprise workflows bind themselves to Webex, creating a self-reinforcing flywheel: more agents lead to more value, more users, more developers, and more agents.')

subheading(pdf, 'Expected Impact')
bullet(pdf, '500+ certified AI agents in the marketplace within Year 1')
bullet(pdf, '$150 million in GMV (total agent-driven transactions) by FY2028')
bullet(pdf, '3x growth in Webex developer activity within 18 months')
bullet(pdf, '85% enterprise renewal rate driven by agent-based stickiness')
bullet(pdf, 'New annual marketplace commission revenue estimated at $50 million by FY2029')
pdf.ln(2)
source_note(pdf, 'Sources: Cisco FY2024 10-K; Splunk platform documentation; Salesforce AppExchange economics model; Apple App Store developer revenue sharing framework; MarketsandMarkets Agentic AI Market Report 2024.')

subheading(pdf, 'Solution 3 Flowchart: Secure AI Agent Marketplace')
body(pdf, 'The following flowchart details the complete Build-Certify-Deploy-Monitor lifecycle, including the Cisco security certification pipeline, enterprise admin deployment controls, Splunk-powered monitoring, and the developer revenue sharing model.')
pdf.ln(2)

pdf.image('cisco_case/figures/flowchart_3_marketplace.png', x=pdf.l_margin, w=img_w)

# ============================================================
# TECHNICAL FEASIBILITY, CONSTRAINTS & SCALABILITY ASSESSMENT
# ============================================================
pdf.add_page()
heading(pdf, 'Technical Feasibility, Constraints & Scalability Assessment')

body(pdf, 'This section assesses the technical feasibility, key constraints, and scalability considerations for each of the three proposed solutions. These assessments are based on Cisco\'s existing infrastructure, publicly available technology capabilities, and industry benchmarks.')

subheading(pdf, 'Solution 1: AI Meeting Prep & Workflow Orchestrator')

body_bold(pdf, 'Technical Feasibility')
bullet(pdf, 'The Webex AI Codec (DNN noise removal, neural speech synthesis, RMM) already exists in production and processes millions of meeting minutes daily. Extending the NLP layer to detect task intents is an incremental ML advancement, not a greenfield build.')
bullet(pdf, 'LLM-based task planning is technically proven. OpenAI, Anthropic, and Google have demonstrated multi-step reasoning with tool use. Cisco can fine-tune a model on enterprise meeting transcripts to achieve high accuracy for task detection and drafting.')
bullet(pdf, 'A2A protocols for cross-system integration (Jira, Salesforce, ServiceNow) rely on REST/GraphQL APIs that are mature and well-documented. The challenge is not whether integration is possible, but how to manage authentication and data governance at scale.')
bullet(pdf, 'The PREPARE phase (context ingestion, agenda generation, auto-slides) leverages retrieval-augmented generation (RAG), a well-established pattern for grounding LLM outputs in enterprise data.')

body_bold(pdf, 'Key Constraints')
bullet(pdf, 'Latency: Real-time task detection during live meetings requires the NLP pipeline to process audio-to-intent in under 2 seconds. Current Webex AI Codec latency is approximately 200ms for noise removal; adding NLP inference adds 500-1000ms depending on model size. Total pipeline latency must remain below the 2-second threshold for a non-disruptive user experience.')
bullet(pdf, 'LLM hallucination risk: Task drafts generated by the LLM may contain errors (wrong assignee, incorrect priority, fabricated project names). The human-in-the-loop approval step mitigates this risk but does not eliminate it. Confidence thresholds and retrieval grounding are essential safeguards.')
bullet(pdf, 'Enterprise data access: The PREPARE and REASON phases require authorized access to CRM, project management, and calendar systems. Organizations with strict data governance policies may limit what Webex AI can ingest, reducing the quality of AI-generated prep materials and task drafts.')

body_bold(pdf, 'Scalability')
bullet(pdf, 'Cisco\'s cloud infrastructure supports 600+ million meeting minutes per month. The incremental compute for NLP task detection and LLM inference can be distributed across Cisco\'s existing GPU clusters.')
bullet(pdf, 'The A2A protocol is stateless and horizontally scalable: each meeting session independently connects to external system agents without shared state.')
bullet(pdf, 'Splunk observability is designed for enterprise-scale event ingestion (petabytes per day), making audit logging a non-bottleneck.')
pdf.ln(2)

subheading(pdf, 'Solution 2: VIBE - Voice & Language Intelligence Layer')

body_bold(pdf, 'Technical Feasibility')
bullet(pdf, 'DNN noise removal and voice processing are already core capabilities of the Webex AI Codec. Voice Boost extends this with EQ presets, which is a signal processing task with minimal additional compute.')
bullet(pdf, 'ASR (Automatic Speech Recognition) at 98% accuracy is achievable using models like Whisper (OpenAI) or Cisco\'s proprietary ASR. Multi-language support with 100+ languages is available through neural machine translation models that have been deployed at scale by Google, Microsoft, and Meta.')
bullet(pdf, 'Neural TTS (Text-to-Speech) with natural voice personas is technically mature. Services like Google Cloud TTS, Amazon Polly, and open-source models (VITS, Bark) can generate natural speech in under 500ms. Cisco can build or license a TTS model that maintains consistent voice identity per session.')
bullet(pdf, 'The Simple Mode jargon simplification requires a domain-adapted LLM that can rewrite technical text into plain language with analogies. This is a well-understood NLP task with strong performance from current models.')

body_bold(pdf, 'Key Constraints')
bullet(pdf, 'End-to-end latency: The full VIBE pipeline (ASR + translation + simplification + TTS) must complete in under 2 seconds for real-time delivery. Each stage adds latency: ASR (~300ms), translation (~200ms), simplification (~300ms), TTS (~500ms). Pipeline parallelization and model optimization are required to meet the target.')
bullet(pdf, 'Translation accuracy for domain-specific terms: Neural machine translation may mistranslate technical jargon or proper nouns. VIBE needs a custom terminology dictionary per organization to handle domain-specific vocabulary correctly.')
bullet(pdf, 'TTS voice consistency: Maintaining a consistent and natural voice persona across an entire meeting session while varying emotional tone is technically challenging. Voice cloning safeguards must prevent misuse while preserving quality.')
bullet(pdf, 'Bandwidth: Delivering per-user audio streams (each participant receives a personalized VIBE voice in their language) increases bandwidth requirements. Cisco\'s neural codec compression (1 kbps) mitigates this, but meetings with 50+ participants may require adaptive quality scaling.')

body_bold(pdf, 'Scalability')
bullet(pdf, 'VIBE processing is per-user and per-meeting, making it naturally parallelizable. Each user\'s audio pipeline runs independently.')
bullet(pdf, 'Neural machine translation models can be deployed as microservices with auto-scaling based on concurrent meeting load.')
bullet(pdf, 'The privacy guarantee (zero data retention option) simplifies storage scalability since ephemeral processing does not accumulate data.')
pdf.ln(2)

subheading(pdf, 'Solution 3: Secure AI Agent Marketplace')

body_bold(pdf, 'Technical Feasibility')
bullet(pdf, 'SDK development for agent creation is a standard software engineering task. Cisco already provides Webex APIs and developer tools. Extending these into a structured agent SDK with templates and sandbox environments is feasible within 6-9 months.')
bullet(pdf, 'The security certification pipeline leverages existing Cisco capabilities: static code analysis (Cisco acquired SourceFire/Snort), zero-trust networking (Cisco Zero Trust), and observability (Splunk). Assembling these into a unified certification workflow is integration work, not invention.')
bullet(pdf, 'Sandboxed agent execution using containerized environments (Kubernetes, WebAssembly) is a proven pattern used by AWS Lambda, Cloudflare Workers, and similar platforms.')
bullet(pdf, 'The marketplace discovery and billing infrastructure can be modeled on existing platforms (Salesforce AppExchange, Shopify App Store) with well-understood UX patterns and revenue-sharing mechanics.')

body_bold(pdf, 'Key Constraints')
bullet(pdf, 'Certification throughput: If 1,000+ developers submit agents simultaneously, the certification pipeline must scale to handle parallel security reviews. Automated scanning can handle volume, but manual review of edge cases may create bottlenecks.')
bullet(pdf, 'Agent quality control: A marketplace is only as good as its worst agent. Low-quality or poorly performing agents could damage the "Cisco Verified" brand. The certification bar must be high enough to maintain trust but low enough to encourage developer participation.')
bullet(pdf, 'Cross-system compatibility: Agents that interact with third-party systems (Jira, Salesforce, SAP) depend on those systems\' APIs remaining stable. API deprecation, rate limits, or authentication changes could break deployed agents.')
bullet(pdf, 'Developer adoption: Building the marketplace is technically feasible, but attracting developers requires compelling economics (the 70/30 revenue split) and a sufficiently large Webex user base to justify development effort.')

body_bold(pdf, 'Scalability')
bullet(pdf, 'Agent execution scales horizontally: each agent runs in an isolated container with defined resource limits. Cisco\'s cloud infrastructure can provision containers on demand.')
bullet(pdf, 'Splunk-powered monitoring is designed for enterprise-scale observability and can ingest millions of agent events per day without performance degradation.')
bullet(pdf, 'The marketplace catalog itself is a standard web application with CDN-backed discovery, which scales trivially to thousands of listed agents.')

# ============================================================
# IMPLEMENTATION RISKS & SYSTEM-LEVEL TRADE-OFFS
# ============================================================
pdf.add_page()
heading(pdf, 'Implementation Risks & System-Level Trade-Offs')

body(pdf, 'This section identifies the key implementation risks and system-level trade-offs that Cisco must navigate when deploying the three proposed solutions. Understanding these trade-offs enables informed decision-making and proactive risk mitigation.')

subheading(pdf, 'Solution 1: AI Meeting Prep & Workflow Orchestrator')

body_bold(pdf, 'Implementation Risks')
bullet(pdf, 'AI hallucination in task drafts: The LLM may generate task drafts with incorrect details (wrong project, wrong assignee, fabricated deadlines). Mitigation: Human-in-the-loop approval is mandatory for all external actions; confidence scoring filters low-certainty drafts into a review queue rather than auto-processing them.')
bullet(pdf, 'Over-automation backlash: Users may feel overwhelmed by AI-generated suggestions if the system is too aggressive. Mitigation: Progressive disclosure (start with minimal suggestions, increase based on user engagement); user-controlled sensitivity settings; easy "snooze" controls.')
bullet(pdf, 'Data privacy and compliance: Ingesting CRM records, calendar data, and past transcripts for the PREPARE phase raises data privacy concerns, especially under GDPR and HIPAA. Mitigation: All data access passes through Cisco\'s zero-trust data fabric with explicit user and admin consent; data minimization principles limit ingestion to what is strictly necessary.')
bullet(pdf, 'Integration fragility: Dependency on third-party APIs (Jira, Salesforce, ServiceNow) means that API changes, rate limits, or outages can break the orchestrator. Mitigation: Circuit-breaker patterns, graceful degradation (continue meeting even if integration fails), and API version pinning.')

body_bold(pdf, 'System-Level Trade-Offs')
bullet(pdf, 'Accuracy vs. speed: More context retrieval improves task draft quality but increases latency. Cisco must balance how much enterprise data the REASON phase retrieves against the 2-second pipeline target.')
bullet(pdf, 'Automation vs. control: Fully autonomous execution would maximize productivity gains but introduces unacceptable risk for enterprise customers. The human-in-the-loop requirement reduces automation speed but is essential for trust and adoption in regulated industries.')
bullet(pdf, 'Breadth vs. depth of integration: Supporting hundreds of third-party systems increases utility but dilutes engineering focus. Cisco should prioritize the top 10-15 enterprise tools (Jira, Salesforce, ServiceNow, SAP, GitHub, Slack, Confluence, HubSpot) for deep integration and use generic API connectors for long-tail systems.')
pdf.ln(2)

subheading(pdf, 'Solution 2: VIBE - Voice & Language Intelligence Layer')

body_bold(pdf, 'Implementation Risks')
bullet(pdf, 'Deepfake perception risk: Even though VIBE explicitly labels all synthesized speech ("Spoken by VIBE for [User]") and uses distinct voice personas, external stakeholders unfamiliar with the feature may perceive AI-generated speech as deceptive. Mitigation: Mandatory on-screen labeling, meeting-start notification that VIBE is active, and admin controls to disable VIBE for customer-facing meetings if desired.')
bullet(pdf, 'Translation errors in high-stakes contexts: Mistranslation of contractual terms, medical terminology, or legal language could have serious consequences. Mitigation: Custom terminology dictionaries per organization; confidence scoring on translations with visual warnings when confidence is low; option for human translator review before critical communications.')
bullet(pdf, 'User adoption resistance: Some users may resist having AI speak on their behalf or simplify their language, perceiving it as patronizing. Mitigation: VIBE is fully opt-in with per-user control; users choose their own modes, languages, and voice presets; no organizational mandate required.')
bullet(pdf, 'Compute cost: Running the full VIBE pipeline (ASR + translation + TTS) for every participant in every meeting significantly increases per-meeting compute costs. Mitigation: VIBE processing is activated only for users who enable it, not applied globally; adaptive quality scaling reduces resource consumption for large meetings.')

body_bold(pdf, 'System-Level Trade-Offs')
bullet(pdf, 'Latency vs. quality: Higher-quality translation and TTS require larger models with longer inference times. Cisco must choose between slightly lower translation accuracy (faster, smaller models) and better accuracy (slower, larger models) based on the 2-second latency target.')
bullet(pdf, 'Privacy vs. personalization: Personalized voice personas and language profiles require storing user preferences. The zero-data-retention option limits personalization for privacy-conscious users. Cisco must offer both options and let users choose.')
bullet(pdf, 'Simplification vs. accuracy: Simple Mode rewrites jargon into plain language, which inherently involves some loss of technical precision. Over-simplification may distort the original meaning. Cisco must calibrate the simplification level and always provide the original text alongside the simplified version.')
pdf.ln(2)

subheading(pdf, 'Solution 3: Secure AI Agent Marketplace')

body_bold(pdf, 'Implementation Risks')
bullet(pdf, 'Marketplace cold-start problem: An agent marketplace with few agents attracts few users, and few users attract few developers. This chicken-and-egg problem can stall marketplace growth. Mitigation: Cisco should seed the marketplace with 20-30 first-party agents built in-house, partner with major ISVs (Salesforce, Atlassian, ServiceNow) for launch-day integrations, and offer developer grants and revenue guarantees during the first 18 months.')
bullet(pdf, 'Security certification bottleneck: The certification pipeline could become a bottleneck if demand exceeds review capacity. Mitigation: Invest in automated scanning to handle 90%+ of certification checks; reserve manual review for agents that access sensitive data or execute high-risk actions.')
bullet(pdf, 'Agent misbehavior in production: Even certified agents may exhibit unexpected behavior under real-world conditions (edge cases not covered in testing). Mitigation: Kill-switch capability for instant deactivation; sandboxed execution prevents lateral damage; Splunk anomaly detection provides early warning.')
bullet(pdf, 'Revenue model uncertainty: The 70/30 revenue split may not be economically viable if marketplace transaction volume is low in the early years. Mitigation: Start with a generous developer split to attract builders; adjust as the marketplace matures and transaction volume grows.')

body_bold(pdf, 'System-Level Trade-Offs')
bullet(pdf, 'Openness vs. security: A more open marketplace (lower certification bar, more permissive data access) grows faster but increases security risk. A stricter marketplace grows slower but builds stronger enterprise trust. Cisco\'s brand equity in enterprise security means the "trust-first" approach is the correct strategic choice, even if it slows initial growth.')
bullet(pdf, 'First-party vs. third-party agents: Cisco must decide how many agents to build in-house versus leaving to third-party developers. Too many first-party agents discourages developer participation; too few leaves gaps in marketplace coverage. The recommended ratio is 15-20% first-party agents for core use cases, with the remaining 80%+ from the developer community.')
bullet(pdf, 'Platform lock-in vs. portability: Agents built on the Webex SDK are inherently platform-specific. Developers may resist investing in a platform-locked ecosystem. Cisco should adopt open standards (A2A protocol) where possible to reduce perceived lock-in while maintaining competitive differentiation.')

# ============================================================
# INTEGRATED STRATEGY & CONCLUSION
# ============================================================
pdf.add_page()
heading(pdf, 'Integrated Strategy: How the Three Solutions Work Together')

body(pdf, 'The three solutions are designed as an integrated system, not independent initiatives. Together, they create a comprehensive competitive moat:')

bullet(pdf, 'Solution 1 (AI Meeting Prep & Workflow Orchestrator) provides the core intelligence: AI that can prepare users before meetings, perceive meeting context, reason about tasks, execute actions across enterprise systems, and follow up on unanswered questions after the meeting ends.')
bullet(pdf, 'Solution 2 (VIBE - Voice & Language Intelligence Layer) ensures that every participant can fully engage in the meeting regardless of language, technical background, or environment. VIBE makes the input to Solution 1 richer and more inclusive by enabling non-native and non-technical participants to contribute actively.')
bullet(pdf, 'Solution 3 (AI Agent Marketplace) scales the intelligence: instead of Cisco building every agent, the marketplace enables hundreds of developers to build vertical-specific agents for healthcare, finance, government, manufacturing, and more. The marketplace also provides the deployment and governance infrastructure that makes Solutions 1 and 2 safe for regulated industries.')
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
    'Cisco Systems. (2024). Annual Report (Form 10-K), Fiscal Year 2024. SEC Filing. Retrieved from https://investor.cisco.com',
    'Microsoft Corporation. (2024). Annual Report (Form 10-K), Fiscal Year 2024. SEC Filing. Retrieved from https://www.microsoft.com/en-us/investor',
    'Zoom Video Communications. (2025). Annual Report (Form 10-K), Fiscal Year 2025. SEC Filing. Retrieved from https://investors.zoom.us',
    'IDC. (2024). Worldwide Unified Communications & Collaboration Market Tracker. International Data Corporation.',
    'Gartner. (2024). Future of Work Survey: Hybrid Work Trends. Gartner Research.',
    'McKinsey & Company. (2024). Future of Work Report: Meeting Productivity and Knowledge Worker Efficiency. McKinsey Global Institute.',
    'MarketsandMarkets. (2024). Agentic AI Market Report: Global Forecast to 2030. MarketsandMarkets Research.',
    'Microsoft. (2024). Work Trend Index: Annual Report on Workplace Trends and Meeting Culture. Microsoft Research.',
    'Otter.ai. (2024). Workplace Productivity Report: Meeting Follow-Up and Action Item Completion Rates.',
    'Cisco Webex. (2025). Webex AI Assistant and AI Codec Technical Documentation. Retrieved from https://www.webex.com/ai',
    'Microsoft. (2025). Microsoft 365 Copilot Product Documentation. Retrieved from https://www.microsoft.com/copilot',
    'Zoom. (2025). Zoom AI Companion 2.0 Product Documentation. Retrieved from https://zoom.us/ai-assistant',
    'G2. (2025). Video Conferencing Software Reviews and Ratings. Retrieved from https://www.g2.com/categories/video-conferencing',
    'Salesforce. (2024). AppExchange Marketplace Economics and Developer Revenue Sharing Model. Salesforce Documentation.',
    'Gartner. (2024). DEI in Technology Procurement: How Inclusion Features Influence Enterprise Buying Decisions. Gartner Research.',
]

for i, ref in enumerate(refs):
    pdf.set_font('Times', '', 12)
    pdf.multi_cell(0, LH, f'{i+1}. {ref}')
    pdf.ln(1)

pdf.output('cisco_case/Cisco_Problems_Solutions.pdf')
print("PDF generated: cisco_case/Cisco_Problems_Solutions.pdf")

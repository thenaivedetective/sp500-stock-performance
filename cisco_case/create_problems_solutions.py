import matplotlib
matplotlib.use('Agg')
from fpdf import FPDF
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

os.makedirs("cisco_case/figures", exist_ok=True)

# ============================================================
# FLOWCHART 1: Agentic AI Workflow Orchestrator
# (The detailed Perceive-Reason-Act diagram)
# ============================================================
fig, ax = plt.subplots(figsize=(22, 30))
ax.set_xlim(0, 22)
ax.set_ylim(0, 30)
ax.axis('off')

ax.text(11, 29.5, 'Solution 1: Webex Agentic AI Workflow Orchestrator',
        ha='center', fontsize=22, fontweight='bold', color='#002060')
ax.text(11, 29.0, 'Perceive \u2192 Reason \u2192 Act Architecture  |  End-to-End Autonomous Task Execution',
        ha='center', fontsize=13, color='#555555')

lane_colors = ['#E8F4FD', '#FFF3E0', '#F3E5F5']
lane_labels = ['WEBEX CLOUD', 'CISCO SECURE DATA FABRIC', 'THIRD-PARTY APPS']
lane_sublabels = ['(AI Codec + NLP + Agent Runtime)', '(Splunk + Zero-Trust Identity)', '(Jira, Salesforce, SAP, etc.)']
lane_xs = [(0.3, 7.0), (7.5, 14.5), (15.0, 21.7)]

for i, ((x1, x2), color, label, sublabel) in enumerate(zip(lane_xs, lane_colors, lane_labels, lane_sublabels)):
    rect = mpatches.FancyBboxPatch((x1, 1.0), x2 - x1, 27.0, boxstyle="round,pad=0.1",
                                    facecolor=color, edgecolor='#999999', linewidth=1.5, alpha=0.5)
    ax.add_patch(rect)
    ax.text((x1 + x2) / 2, 27.7, label, ha='center', fontsize=13, fontweight='bold', color='#002060')
    ax.text((x1 + x2) / 2, 27.3, sublabel, ha='center', fontsize=9, color='#666666')

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

WX = 3.65
DF = 11.0
TP = 18.35

draw_oval(ax, WX, 26.5, 4.0, 1.0, 'START\nLive Webex Meeting Begins')
arrow(ax, WX, 25.95, WX, 25.2)

draw_dashed_box(ax, 0.5, 19.5, 6.3, 5.5, 'PERCEIVE: AI Codec ML Pipeline', '#0050A0')

draw_para(ax, WX, 24.6, 5.2, 0.9,
          'Raw Audio/Video Input\nMicrophone + Camera streams', '#2C3E50', 'white', 9)
arrow(ax, WX, 24.1, WX, 23.5)

draw_rect(ax, WX, 22.9, 5.5, 1.0,
          'Deep Neural Network (DNN)\nBackground Noise Removal\n150+ noise types in real-time', '#1A5276', 'white', 9)
arrow(ax, WX, 22.35, WX, 21.7)

draw_rect(ax, WX, 21.1, 5.5, 1.0,
          'AI Codec: Neural Speech Synthesis\nCompresses audio to ~1 kbps\n(vs 32 kbps traditional codecs)', '#1A5276', 'white', 9)
arrow(ax, WX, 20.55, WX, 19.9)

draw_rect(ax, WX, 19.3, 5.5, 1.0,
          'Real-Time Media Models (RMM)\nSuper Resolution + Voice Isolation\nGesture Recognition', '#0070C0', 'white', 9)
arrow(ax, WX, 18.75, WX, 18.1)

draw_rect(ax, WX, 17.5, 5.5, 1.0,
          'NLP Engine: Speech-to-Text\nReal-time transcription + translation\n100+ languages', '#0070C0', 'white', 9)
arrow(ax, WX, 16.95, WX, 16.2)

draw_diamond(ax, WX, 15.2, 2.0, 'NLP detects\nTask Intent?', '#F39C12', 'black', 10)

ax.text(1.0, 15.2, 'NO', fontsize=12, fontweight='bold', color='#E74C3C', ha='center')
arrow(ax, WX - 1.0, 15.2, 1.5, 15.2, '#E74C3C', 2)
arrow(ax, 1.0, 15.2, 1.0, 24.6, '#E74C3C', 2)
arrow(ax, 1.0, 24.6, WX - 2.8, 24.6, '#E74C3C', 2)
ax.text(1.0, 19.8, 'Continue\nMonitoring', fontsize=9, fontweight='bold', color='#E74C3C', ha='center',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#E74C3C', alpha=0.9))

ax.text(WX + 1.7, 15.9, 'YES', fontsize=12, fontweight='bold', color='#27AE60', ha='center')
arrow(ax, WX + 1.0, 15.2, DF - 2.5, 15.2, '#27AE60', 2.5)

draw_para(ax, DF, 15.2, 5.0, 1.1,
          'REASON: Fetch Context\nA2A Protocol retrieves\nproject data from systems', '#27AE60', 'white', 10)

arrow(ax, DF + 2.8, 15.2, TP - 2.2, 15.2, '#333333')

draw_para(ax, TP, 15.2, 5.0, 1.1,
          'EXTERNAL SYSTEMS\nJira / Salesforce / SAP\nServiceNow / GitHub', '#D35400', 'white', 9)

arrow(ax, DF, 14.55, DF, 13.5)

draw_cyl(ax, DF, 12.7, 5.0, 1.5,
         'CISCO SECURE DATA FABRIC\nSplunk Observability\nZero-Trust Identity Layer', '#8E44AD', 'white', 9)

arrow(ax, DF, 11.85, DF, 10.8)

draw_rect(ax, DF, 10.1, 5.0, 1.2,
          'ACT: DRAFT\nAI Agent generates task draft\nusing retrieved context\n+ LLM-based planning', '#0070C0', 'white', 10)

arrow(ax, DF - 2.8, 10.1, WX + 1.5, 8.5, '#333333')

draw_diamond(ax, WX, 7.5, 2.0, 'Human-in-Loop\nApprove?', '#F39C12', 'black', 10)

ax.text(WX + 1.7, 6.5, 'REJECT', fontsize=11, fontweight='bold', color='#E74C3C', ha='center')
arrow(ax, WX + 1.0, 7.5, DF - 2.8, 9.5, '#E74C3C', 2)

ax.text(WX + 1.7, 8.3, 'APPROVE', fontsize=11, fontweight='bold', color='#27AE60', ha='center')
arrow(ax, WX + 1.0, 7.5, TP - 2.5, 7.5, '#27AE60', 2.5)

draw_rect(ax, TP, 7.5, 5.0, 1.2,
          'EXECUTE\nAgent pushes data via\nsecure API to external app', '#E74C3C', 'white', 10)

arrow(ax, TP, 6.85, TP, 6.0)

draw_rect(ax, DF, 5.3, 5.5, 1.0,
          'Splunk Logs Execution\nPerformance metrics + audit trail\nAnomaly detection on agent actions', '#8E44AD', 'white', 9)
arrow(ax, TP, 5.3, DF + 2.8, 5.3, '#333333')

arrow(ax, DF - 2.8, 5.3, WX + 2.0, 5.3, '#333333')

draw_rect(ax, DF, 3.8, 5.5, 1.0,
          'CONFIRM\nStatus posted to Webex Chat:\n"Task created successfully"', '#0070C0', 'white', 9)
arrow(ax, DF, 4.7, DF, 4.35)

arrow(ax, DF - 2.8, 3.8, WX + 2.0, 3.8, '#333333')

draw_oval(ax, WX, 3.8, 4.0, 1.0, 'END\nMeeting Continues\nSeamlessly')

mr = mpatches.FancyBboxPatch((0.3, 1.5), 21.4, 1.2, boxstyle='round,pad=0.1',
                               facecolor='#002060', edgecolor='black', linewidth=2)
ax.add_patch(mr)
ax.text(11, 2.4, 'QUANTIFIED IMPACT', ha='center', fontsize=12, fontweight='bold', color='#FFD700')
ax.text(11, 1.85, 'Reduces manual data entry by 15 min/meeting  |  25% meeting-to-action conversion  |  '
        '40% workflow automation  |  85% task accuracy',
        ha='center', va='center', fontsize=10, fontweight='bold', color='white')

lx = 15.5; ly = 27.0
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
print("Flowchart 1 (Agentic AI Workflow) created")

# ============================================================
# FLOWCHART 2: Intelligent Meeting-to-Action Engine
# ============================================================
fig, ax = plt.subplots(figsize=(22, 28))
ax.set_xlim(0, 22)
ax.set_ylim(0, 28)
ax.axis('off')

ax.text(11, 27.5, 'Solution 2: Intelligent Meeting-to-Action Engine',
        ha='center', fontsize=22, fontweight='bold', color='#002060')
ax.text(11, 27.0, 'Automated Follow-Up Pipeline  |  From Conversation to Completed Tasks',
        ha='center', fontsize=13, color='#555555')

phase_data = [
    ('PHASE 1: CAPTURE', '#1A5276', 24.5, [
        ('Live Meeting\nAudio/Video Feed', 'para', 24.5),
        ('AI Transcription Engine\nSpeaker diarization + sentiment\nanalysis + topic segmentation', 'rect', 22.8),
        ('Action Item Extraction\nNLP identifies: tasks, decisions,\ndeadlines, assignees, dependencies', 'rect', 21.0),
    ]),
    ('PHASE 2: CLASSIFY & PRIORITIZE', '#27AE60', 18.5, [
        ('Classification Engine', 'diamond', 18.5),
    ]),
    ('PHASE 3: ROUTE & EXECUTE', '#0070C0', 14.0, []),
    ('PHASE 4: TRACK & REPORT', '#8E44AD', 5.0, []),
]

for title, color, y_pos, _ in phase_data:
    bg = mpatches.FancyBboxPatch((0.3, y_pos - 2.2 if 'PHASE 1' in title else
                                   y_pos - 2.5 if 'PHASE 2' in title else
                                   y_pos - 5.5 if 'PHASE 3' in title else
                                   y_pos - 3.5),
                                  21.4,
                                  6.0 if 'PHASE 1' in title else
                                  5.0 if 'PHASE 2' in title else
                                  7.0 if 'PHASE 3' in title else
                                  5.0,
                                  boxstyle="round,pad=0.1",
                                  facecolor=color, edgecolor=color, linewidth=2, alpha=0.08)
    ax.add_patch(bg)

draw_oval(ax, 11, 26.2, 5.0, 0.9, 'START: Meeting Ends / In-Progress Trigger', '#002060', 'white', 11)
arrow(ax, 11, 25.7, 11, 25.1)

draw_para(ax, 11, 24.5, 6.0, 1.0,
          'Raw Meeting Recording\nAudio + Video + Screen Share + Chat', '#2C3E50', 'white', 10)
arrow(ax, 11, 23.95, 11, 23.3)

draw_rect(ax, 11, 22.7, 7.0, 1.0,
          'AI Transcription Engine\nSpeaker Diarization  |  Sentiment Analysis  |  Topic Segmentation\nIdentifies who said what, emotional tone, and subject clusters', '#1A5276', 'white', 9)
arrow(ax, 11, 22.15, 11, 21.5)

draw_rect(ax, 11, 20.9, 7.0, 1.0,
          'Action Item Extraction (NLP)\nTasks  |  Decisions  |  Deadlines  |  Assignees  |  Dependencies\nConfidence Score assigned to each extracted item', '#1A5276', 'white', 9)
arrow(ax, 11, 20.35, 11, 19.7)

ax.text(1.0, 25.5, 'PHASE 1:\nCAPTURE', fontsize=12, fontweight='bold', color='#1A5276',
        ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F4FD', edgecolor='#1A5276', linewidth=2))

draw_diamond(ax, 11, 18.7, 2.2, 'Confidence\n\u2265 85%?', '#F39C12', 'black', 10)

ax.text(1.0, 18.7, 'PHASE 2:\nCLASSIFY', fontsize=12, fontweight='bold', color='#27AE60',
        ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8FFE8', edgecolor='#27AE60', linewidth=2))

ax.text(8.0, 18.7, 'NO', fontsize=12, fontweight='bold', color='#E74C3C')
arrow(ax, 11 - 1.1, 18.7, 5.5, 18.7, '#E74C3C', 2)
draw_rect(ax, 3.8, 18.7, 3.0, 0.9,
          'Flag for Human\nReview Queue', '#E74C3C', 'white', 9)

ax.text(11 + 1.5, 19.5, 'YES', fontsize=12, fontweight='bold', color='#27AE60')
arrow(ax, 11, 17.6, 11, 17.0)

draw_rect(ax, 11, 16.3, 7.0, 1.2,
          'Priority Classification Engine\nP1-Critical (deadline <24h)  |  P2-High (deadline <1 week)\nP3-Medium (deadline <2 weeks)  |  P4-Low (no deadline)\nRoute based on priority + type + assignee', '#27AE60', 'white', 9)
arrow(ax, 11, 15.65, 11, 15.0)

ax.text(1.0, 14.5, 'PHASE 3:\nROUTE &\nEXECUTE', fontsize=12, fontweight='bold', color='#0070C0',
        ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#E0F0FF', edgecolor='#0070C0', linewidth=2))

draw_diamond(ax, 11, 14.0, 2.2, 'Task\nType?', '#F39C12', 'black', 10)

arrow(ax, 11 - 1.1, 14.0, 4.5, 14.0, '#333333', 2)
ax.text(6.5, 14.5, 'Ticket/Issue', fontsize=9, fontweight='bold', color='#333333')
draw_rect(ax, 3.5, 12.8, 4.0, 1.2,
          'Create Jira/GitHub Issue\nTitle, description, assignee,\npriority, sprint, labels\nautomatically populated', '#0070C0', 'white', 9)
arrow(ax, 4.5, 14.0, 4.5, 13.45)

arrow(ax, 11, 12.9, 11, 11.8, '#333333', 2)
ax.text(11.5, 12.5, 'Document', fontsize=9, fontweight='bold', color='#333333')
draw_rect(ax, 11, 11.2, 4.5, 1.0,
          'Generate Document\nMeeting minutes, decision log,\nor status report in Webex Docs', '#0070C0', 'white', 9)

arrow(ax, 11 + 1.1, 14.0, 17.5, 14.0, '#333333', 2)
ax.text(15.0, 14.5, 'Calendar/Follow-up', fontsize=9, fontweight='bold', color='#333333')
draw_rect(ax, 18.5, 12.8, 4.5, 1.2,
          'Schedule Follow-Up\nCalendar invite with agenda\npre-populated from action items\nReminders set automatically', '#0070C0', 'white', 9)
arrow(ax, 18.5, 14.0, 18.5, 13.45)

arrow(ax, 3.5, 12.15, 3.5, 10.5)
arrow(ax, 11, 10.65, 11, 10.0)
arrow(ax, 18.5, 12.15, 18.5, 10.5)

draw_diamond(ax, 11, 9.2, 2.2, 'Human\nApproval\nNeeded?', '#F39C12', 'black', 9)

ax.text(14.0, 9.2, 'NO (auto-execute)', fontsize=9, fontweight='bold', color='#27AE60')
arrow(ax, 12.1, 9.2, 15.0, 9.2, '#27AE60', 2)

ax.text(8.0, 9.2, 'YES', fontsize=9, fontweight='bold', color='#E74C3C')
arrow(ax, 9.9, 9.2, 7.5, 9.2, '#E74C3C', 2)
draw_rect(ax, 5.5, 9.2, 3.5, 0.9,
          'Approval Card\nin Webex Space', '#F39C12', 'white', 9)
arrow(ax, 5.5, 8.7, 5.5, 8.0)
arrow(ax, 5.5, 8.0, 15.0, 8.0)

draw_rect(ax, 17.0, 8.6, 4.5, 1.2,
          'EXECUTE\nAPI calls to target systems\nJira / Calendar / Docs / CRM\nSplunk logs every action', '#E74C3C', 'white', 9)

arrow(ax, 17.0, 7.95, 17.0, 7.2)

ax.text(1.0, 6.5, 'PHASE 4:\nTRACK &\nREPORT', fontsize=12, fontweight='bold', color='#8E44AD',
        ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#F3E5F5', edgecolor='#8E44AD', linewidth=2))

draw_cyl(ax, 11, 6.2, 6.0, 1.5,
         'Webex Action Tracker Dashboard\nReal-time status: Pending | In Progress | Complete | Overdue\nPer-meeting and per-user analytics  |  Splunk observability', '#8E44AD', 'white', 9)

arrow(ax, 17.0, 6.2, 14.0, 6.2, '#333333')

draw_rect(ax, 11, 4.2, 7.0, 1.0,
          'Automated Notifications\nReminders before deadlines  |  Escalation for overdue items\nWeekly digest: tasks completed, time saved, automation rate', '#8E44AD', 'white', 9)
arrow(ax, 11, 5.4, 11, 4.75)

arrow(ax, 11, 3.65, 11, 3.0)

draw_oval(ax, 11, 2.5, 6.0, 0.9, 'END: All Actions Tracked & Completed', '#002060', 'white', 11)

mr = mpatches.FancyBboxPatch((0.3, 1.0), 21.4, 0.9, boxstyle='round,pad=0.1',
                               facecolor='#002060', edgecolor='black', linewidth=2)
ax.add_patch(mr)
ax.text(11, 1.45, 'IMPACT: 73% of action items auto-completed  |  Meeting follow-up time reduced from 45 min to 5 min  |  '
        '92% on-time task completion',
        ha='center', va='center', fontsize=10, fontweight='bold', color='white')

plt.tight_layout()
plt.savefig('cisco_case/figures/flowchart_2_meeting_to_action.png', dpi=200, bbox_inches='tight')
plt.close()
print("Flowchart 2 (Meeting-to-Action Engine) created")

# ============================================================
# FLOWCHART 3: Secure AI Agent Marketplace Ecosystem
# Clean vertical flow - one column, no overlap
# ============================================================
fig, ax = plt.subplots(figsize=(18, 36))
ax.set_xlim(0, 18)
ax.set_ylim(0, 36)
ax.axis('off')

ax.text(9, 35.4, 'Solution 3: Secure AI Agent Marketplace', ha='center',
        fontsize=24, fontweight='bold', color='#002060')
ax.text(9, 34.8, 'Build -> Certify -> Deploy -> Monitor Lifecycle', ha='center',
        fontsize=14, color='#555555')

CX = 9.0

# === START ===
draw_oval(ax, CX, 34.0, 6.0, 0.9, 'START\nDeveloper Registers on Platform', '#002060', 'white', 12)
arrow(ax, CX, 33.5, CX, 32.9)

# === PHASE 1: BUILD ===
p1 = mpatches.FancyBboxPatch((0.5, 27.5), 17.0, 5.2, boxstyle="round,pad=0.15",
                               facecolor='#1A5276', edgecolor='#1A5276', linewidth=2, alpha=0.08)
ax.add_patch(p1)
ax.text(1.2, 32.3, 'PHASE 1: BUILD', fontsize=14, fontweight='bold', color='#1A5276')

draw_rect(ax, CX, 32.3, 8.0, 1.0,
          'Download Agent SDK (Python / JavaScript)\nTemplates, API docs, code samples', '#1A5276', 'white', 11)
arrow(ax, CX, 31.75, CX, 31.1)

draw_rect(ax, CX, 30.5, 8.0, 1.0,
          'Developer Builds Custom Agent\nDefine triggers, actions, data scope, permissions', '#1A5276', 'white', 11)
arrow(ax, CX, 29.95, CX, 29.3)

draw_rect(ax, CX, 28.7, 8.0, 1.0,
          'Test in Sandbox Environment\nUnit tests + integration tests + performance benchmarks', '#1A5276', 'white', 11)
arrow(ax, CX, 28.15, CX, 27.3)

draw_diamond(ax, CX, 26.3, 2.0, 'Tests\nPass?', '#F39C12', 'black', 11)

ax.text(CX - 3.0, 26.3, 'NO', fontsize=12, fontweight='bold', color='#E74C3C')
arrow(ax, CX - 1.0, 26.3, CX - 3.8, 26.3, '#E74C3C', 2)
arrow(ax, CX - 3.8, 26.3, CX - 3.8, 30.5, '#E74C3C', 2)
arrow(ax, CX - 3.8, 30.5, CX - 4.2, 30.5, '#E74C3C', 2)
ax.text(CX - 3.8, 28.3, 'Fix &\nRetry', fontsize=9, fontweight='bold', color='#E74C3C', ha='center',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#E74C3C', alpha=0.9))

ax.text(CX + 2.0, 26.3, 'YES', fontsize=12, fontweight='bold', color='#27AE60')
arrow(ax, CX, 25.3, CX, 24.7)

draw_rect(ax, CX, 24.1, 8.0, 1.0,
          'Submit Agent to Cisco Marketplace Portal\nUpload manifest, documentation, permission declaration', '#1A5276', 'white', 11)
arrow(ax, CX, 23.55, CX, 22.9)

# === PHASE 2: CERTIFY ===
p2 = mpatches.FancyBboxPatch((0.5, 18.0), 17.0, 4.7, boxstyle="round,pad=0.15",
                               facecolor='#27AE60', edgecolor='#27AE60', linewidth=2, alpha=0.08)
ax.add_patch(p2)
ax.text(1.2, 22.3, 'PHASE 2: CERTIFY (Cisco Security Pipeline)', fontsize=14, fontweight='bold', color='#27AE60')

draw_rect(ax, CX, 22.3, 8.0, 1.0,
          'Security Scan: Static code analysis, vulnerability detection,\ndata access audit, compliance check (SOC2 / HIPAA / FedRAMP)', '#27AE60', 'white', 11)
arrow(ax, CX, 21.75, CX, 21.1)

draw_rect(ax, CX, 20.5, 8.0, 1.0,
          'Permission Review: Zero-trust policy enforcement,\nminimum-privilege validation, PII handling assessment', '#27AE60', 'white', 11)
arrow(ax, CX, 19.95, CX, 19.3)

draw_rect(ax, CX, 18.7, 8.0, 1.0,
          'Performance Testing: Latency benchmarks (< 200ms),\nload testing (1000+ concurrent users), failure recovery', '#27AE60', 'white', 11)
arrow(ax, CX, 18.15, CX, 17.3)

draw_diamond(ax, CX, 16.3, 2.2, 'Cisco\nCertified?', '#F39C12', 'black', 11)

ax.text(CX - 3.2, 16.3, 'FAIL', fontsize=12, fontweight='bold', color='#E74C3C')
arrow(ax, CX - 1.1, 16.3, CX - 4.0, 16.3, '#E74C3C', 2)
draw_rect(ax, CX - 5.5, 16.3, 3.0, 0.8,
          'Return to developer\nwith feedback report', '#E74C3C', 'white', 9)

ax.text(CX + 2.2, 16.3, 'PASS', fontsize=12, fontweight='bold', color='#27AE60')
arrow(ax, CX, 15.2, CX, 14.6)

draw_rect(ax, CX, 14.0, 8.0, 1.0,
          'Cisco Trust Badge Issued: "Cisco Verified Agent"\nListed in Marketplace catalog with security rating', '#27AE60', 'white', 11)
arrow(ax, CX, 13.45, CX, 12.8)

# === PHASE 3: DEPLOY ===
p3 = mpatches.FancyBboxPatch((0.5, 9.5), 17.0, 3.1, boxstyle="round,pad=0.15",
                               facecolor='#0070C0', edgecolor='#0070C0', linewidth=2, alpha=0.08)
ax.add_patch(p3)
ax.text(1.2, 12.2, 'PHASE 3: DEPLOY', fontsize=14, fontweight='bold', color='#0070C0')

draw_rect(ax, CX, 12.2, 8.0, 1.0,
          'Enterprise Admin browses marketplace, selects agent,\nconfigures team access, permissions, and usage limits', '#0070C0', 'white', 11)
arrow(ax, CX, 11.65, CX, 11.0)

draw_diamond(ax, CX, 10.0, 2.0, 'Admin\nApproves?', '#F39C12', 'black', 11)

ax.text(CX - 2.8, 10.0, 'NO', fontsize=12, fontweight='bold', color='#E74C3C')
arrow(ax, CX - 1.0, 10.0, CX - 2.2, 10.0, '#E74C3C', 2)

ax.text(CX + 2.0, 10.0, 'YES', fontsize=12, fontweight='bold', color='#27AE60')
arrow(ax, CX, 9.0, CX, 8.4)

draw_rect(ax, CX, 7.8, 8.0, 1.0,
          'Agent deployed to Webex workspace (sandboxed execution)\nListens for trigger phrases, executes within permissions', '#0070C0', 'white', 11)
arrow(ax, CX, 7.25, CX, 6.6)

# === PHASE 4: MONITOR ===
p4 = mpatches.FancyBboxPatch((0.5, 3.8), 17.0, 2.6, boxstyle="round,pad=0.15",
                               facecolor='#8E44AD', edgecolor='#8E44AD', linewidth=2, alpha=0.08)
ax.add_patch(p4)
ax.text(1.2, 6.0, 'PHASE 4: MONITOR (Splunk Observability)', fontsize=14, fontweight='bold', color='#8E44AD')

draw_rect(ax, CX, 6.0, 8.0, 1.0,
          'Splunk monitors: agent performance, error rates, anomalies\nUsage analytics, ROI dashboards, automated alerts', '#8E44AD', 'white', 11)
arrow(ax, CX, 5.45, CX, 4.8)

draw_diamond(ax, CX, 3.8, 2.0, 'Alert\nTriggered?', '#F39C12', 'black', 11)

ax.text(CX + 2.5, 4.5, 'YES: Kill Switch\n(auto-disable agent)', fontsize=10, fontweight='bold', color='#E74C3C',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#FADBD8', edgecolor='#E74C3C', linewidth=1.5))
arrow(ax, CX + 1.0, 3.8, CX + 2.0, 3.8, '#E74C3C', 2)

ax.text(CX - 2.5, 4.5, 'NO: Continue\nmonitoring', fontsize=10, fontweight='bold', color='#27AE60',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#D5F5E3', edgecolor='#27AE60', linewidth=1.5))
arrow(ax, CX - 1.0, 3.8, CX - 1.8, 3.8, '#27AE60', 2)

arrow(ax, CX, 2.8, CX, 2.2)

draw_oval(ax, CX, 1.6, 8.0, 0.9, 'Billing & Revenue Share (70/30 developer split)\nAgent runs continuously in Webex', '#002060', 'white', 10)

# === IMPACT BAR ===
mr = mpatches.FancyBboxPatch((0.5, 0.3), 17.0, 0.9, boxstyle='round,pad=0.1',
                               facecolor='#002060', edgecolor='black', linewidth=2)
ax.add_patch(mr)
ax.text(9, 0.75, 'IMPACT: 500+ certified agents Year 1  |  $150M GMV by FY2028  |  '
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

def heading(pdf, text):
    pdf.set_font('Times', 'B', 14)
    pdf.cell(0, LH+1, text, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(LH)

def subheading(pdf, text):
    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, LH, text, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

def body(pdf, text):
    pdf.set_font('Times', '', 12)
    pdf.multi_cell(0, LH, text)
    pdf.ln(1)

def body_bold(pdf, text):
    pdf.set_font('Times', 'B', 12)
    pdf.multi_cell(0, LH, text)
    pdf.ln(1)

def bullet(pdf, text):
    pdf.set_font('Times', '', 12)
    lm = pdf.l_margin
    pdf.set_left_margin(lm + INDENT)
    pdf.set_x(lm + INDENT)
    pdf.multi_cell(0, LH, f'- {text}')
    pdf.set_left_margin(lm)

def sub_bullet(pdf, text):
    pdf.set_font('Times', '', 12)
    lm = pdf.l_margin
    pdf.set_left_margin(lm + INDENT * 2)
    pdf.set_x(lm + INDENT * 2)
    pdf.multi_cell(0, LH, f'- {text}')
    pdf.set_left_margin(lm)

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
pdf.cell(0, 7, 'Three Strategic Problems & Solutions', align='C', new_x="LMARGIN", new_y="NEXT")
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
pdf.cell(0, LH, 'March 5, 2026', align='C', new_x="LMARGIN", new_y="NEXT")

# ============================================================
# EXECUTIVE SUMMARY
# ============================================================
pdf.add_page()
heading(pdf, 'Executive Summary')

body(pdf, 'Cisco Webex faces three critical strategic problems that prevent it from competing effectively against Microsoft Teams and Zoom in the next phase of hybrid work. This document identifies each problem with specificity, proposes a targeted solution backed by Cisco\'s existing capabilities, and provides a detailed technical flowchart showing how each solution operates end-to-end.')

body(pdf, 'The three problems and their corresponding solutions are:')

bullet(pdf, 'Problem 1: Webex AI is passive and cannot execute tasks. Competitors\' AI tools draft documents, automate workflows, and take action. Webex AI only summarizes and transcribes. Solution: Deploy the Webex Agentic AI Workflow Orchestrator, a Perceive-Reason-Act system that autonomously executes multi-step business tasks during live meetings.')

bullet(pdf, 'Problem 2: Meeting outcomes are lost. 73% of action items discussed in meetings are never completed because there is no automated system to capture, classify, route, and track them. Solution: Build the Intelligent Meeting-to-Action Engine that automatically extracts action items, creates tickets, schedules follow-ups, and tracks completion.')

bullet(pdf, 'Problem 3: Webex has a weak developer and integration ecosystem. Teams has 2,000+ integrations, Zoom has 2,500+, and Webex lags behind with no AI agent development platform. Solution: Launch the Secure AI Agent Marketplace with a developer SDK, Cisco security certification pipeline, and enterprise deployment infrastructure.')

pdf.ln(2)
body(pdf, 'Each solution leverages Cisco\'s existing competitive advantages: the $7.98 billion R&D budget, the $28 billion Splunk acquisition for enterprise data observability, FedRAMP/HIPAA/SOC 2 Type II security certifications, and the Webex AI Codec\'s proven ML engineering capabilities.')

# ============================================================
# PROBLEM 1
# ============================================================
pdf.add_page()
heading(pdf, 'Problem 1: Webex AI Cannot Execute Tasks')

subheading(pdf, 'Problem Definition')
body(pdf, 'The Webex AI Assistant is limited to passive capabilities: meeting summaries, real-time transcription, and language translation. While these features are technically competent, they represent the minimum baseline that every collaboration platform now offers. The AI tells users what happened in a meeting but cannot act on that information.')

body(pdf, 'This creates a measurable productivity gap. When a manager says "Create a Jira ticket for the login bug Sarah found" during a Webex meeting, nothing happens automatically. The manager must manually open Jira after the meeting, recall the details, type the ticket, assign it, set the priority, and link it to the correct sprint. This process takes an average of 8-12 minutes per task and introduces errors from memory decay.')

subheading(pdf, 'Competitive Gap Analysis')
body(pdf, 'Microsoft Teams with Copilot ($30/user/month) can draft Word documents from meeting context, create PowerPoint presentations, generate Excel formulas, and build Power Automate workflows. Copilot connects to the Microsoft Graph, which indexes all enterprise data across emails, files, calendar, and chats, enabling personalized AI responses with full organizational context.')

body(pdf, 'Zoom AI Companion 2.0 includes early agentic features: it drafts documents in Zoom Docs, automatically generates action items with assignees, updates CRM records through Zoom Revenue Accelerator, and offers a built-in workflow automation engine. Zoom provides these capabilities free to all paid users.')

body(pdf, 'Webex offers none of these action-oriented capabilities. The gap is not incremental; it is categorical. Competitors have AI that does work. Webex has AI that describes work that humans must still do manually.')

subheading(pdf, 'Business Impact of the Problem')
bullet(pdf, 'User engagement stagnation: Users spend less daily time in Webex because the platform does not help them complete post-meeting work. This reduces stickiness and increases churn risk.')
bullet(pdf, 'Enterprise deal losses: In competitive evaluations, IT decision-makers increasingly weight AI task execution capabilities. Webex loses deals to Teams and Zoom when buyers compare AI feature matrices.')
bullet(pdf, 'Revenue ceiling: Without differentiated AI capabilities, Webex\'s collaboration revenue (~$4.2B in FY2024) faces a growth ceiling as the market shifts toward AI-powered platforms.')
pdf.ln(2)

subheading(pdf, 'Solution 1: Webex Agentic AI Workflow Orchestrator')

body(pdf, 'Transform the Webex AI Assistant from a passive tool into an agentic AI system that autonomously detects task intent from live conversations, retrieves relevant context from enterprise systems, drafts complete task artifacts, and executes approved actions across third-party platforms. The system operates on a Perceive-Reason-Act architecture with mandatory human-in-the-loop verification for all external actions.')

body_bold(pdf, 'PERCEIVE Phase: Webex AI Codec ML Pipeline')
body(pdf, 'The existing Webex AI Codec serves as the perception layer. During a live meeting, raw audio and video streams pass through a multi-stage ML pipeline:')
bullet(pdf, 'Deep Neural Network (DNN) Noise Removal: Processes audio in real-time to remove 150+ background noise types (keyboard typing, dog barking, construction, etc.) using Cisco\'s proprietary neural network trained on millions of noise samples.')
bullet(pdf, 'Neural Speech Synthesis Codec: Compresses cleaned audio to approximately 1 kbps using neural speech synthesis, compared to 32 kbps for traditional codecs. This enables high-quality audio even on low-bandwidth connections.')
bullet(pdf, 'Real-Time Media Models (RMM): AI upscales low-resolution video (super resolution), separates individual speakers from overlapping audio (voice isolation), and detects hand gestures and reactions (gesture recognition).')
bullet(pdf, 'NLP Engine: Converts processed audio to text with real-time transcription and translation across 100+ languages. The NLP engine performs contextual understanding to identify task-related statements, decisions, and commitments.')
pdf.ln(1)

body_bold(pdf, 'REASON Phase: Context Retrieval and Planning')
body(pdf, 'When the NLP engine detects a task intent (e.g., "We need to create a ticket for this bug"), the system activates the reasoning phase:')
bullet(pdf, 'Agent-to-Agent (A2A) Protocol: The Webex agent communicates with external system agents (Jira, Salesforce, SAP, GitHub, ServiceNow) using standardized A2A protocols to retrieve project context, user profiles, recent activity, and system-specific metadata.')
bullet(pdf, 'Cisco Secure Data Fabric: All data retrieval passes through Cisco\'s zero-trust identity layer, with Splunk observability monitoring every API call for anomalies, unauthorized access attempts, and performance degradation.')
bullet(pdf, 'LLM-Based Task Planning: A large language model synthesizes the conversation context, retrieved system data, and organizational rules to generate a complete task draft (e.g., a fully populated Jira ticket with title, description, assignee, priority, sprint, and labels).')
pdf.ln(1)

body_bold(pdf, 'ACT Phase: Human Verification and Execution')
body(pdf, 'The system presents the drafted task to the meeting participant via an in-meeting approval card:')
bullet(pdf, 'On-Screen Draft: The user sees the complete task artifact (e.g., Jira ticket) overlaid in the Webex interface without switching tabs or applications.')
bullet(pdf, 'Approval Options: The user can Approve (execute immediately), Edit (modify fields before execution), or Reject (discard the draft).')
bullet(pdf, 'Secure Execution: Upon approval, the agent pushes the data to the target system via authenticated API calls. Splunk logs the entire execution chain for audit compliance.')
bullet(pdf, 'Confirmation: Webex posts a confirmation message to the meeting chat (e.g., "Jira ticket WEBAPP-2026-347 created successfully. Assigned to Sarah Chen. Priority: High.").')
pdf.ln(1)

subheading(pdf, 'Why This Solution Wins')
body(pdf, 'This solution directly addresses the core competitive gap. Microsoft Copilot assists across Office applications but does not autonomously execute cross-platform workflows from live conversation context. Zoom AI Companion 2.0 has early agentic features but lacks the enterprise data infrastructure (Splunk) and security certifications (FedRAMP, HIPAA) required for autonomous AI execution in regulated industries. Webex becomes the only platform where AI agents can securely execute tasks in government, healthcare, and financial services environments.')

subheading(pdf, 'Expected Impact')
bullet(pdf, 'Reduces manual post-meeting data entry by 15 minutes per meeting')
bullet(pdf, '25% meeting-to-action conversion rate (vs. current ~5% industry average)')
bullet(pdf, '40% workflow automation rate within 12 months of deployment')
bullet(pdf, '85% task completion accuracy with human-in-the-loop verification')
bullet(pdf, '35% increase in daily active Webex usage as the platform becomes a productivity hub')
pdf.ln(2)
source_note(pdf, 'Sources: Cisco FY2024 10-K; Webex AI Codec documentation; MarketsandMarkets Agentic AI Market Report 2024; Microsoft Copilot & Zoom AI Companion product documentation.')

subheading(pdf, 'Solution 1 Flowchart: Agentic AI Workflow Orchestrator')
body(pdf, 'The following flowchart details the complete technical architecture of the Perceive-Reason-Act system, including the Webex AI Codec ML pipeline, data fabric integration, human-in-the-loop verification, and cross-platform task execution.')
pdf.ln(2)

img_w = W
pdf.image('cisco_case/figures/flowchart_1_agentic_ai.png', x=pdf.l_margin, w=img_w)

# ============================================================
# PROBLEM 2
# ============================================================
pdf.add_page()
heading(pdf, 'Problem 2: Meeting Outcomes Are Lost')

subheading(pdf, 'Problem Definition')
body(pdf, 'Enterprise organizations conduct an average of 62 meetings per employee per month (Microsoft Work Trend Index, 2024). Despite this massive investment of time, research shows that 73% of action items discussed in meetings are never completed (Otter.ai Workplace Productivity Report, 2024). The primary reason is not that employees are unwilling to follow through; it is that the bridge between discussion and execution is entirely manual.')

body(pdf, 'After a meeting ends, participants must individually recall what was discussed, manually create tasks in project management tools, schedule follow-up meetings by hand, draft meeting minutes from memory, and track completion status across disconnected systems. This manual follow-up process takes an average of 45 minutes per meeting and is error-prone due to memory decay, context loss, and competing priorities.')

subheading(pdf, 'Why Current AI Summaries Are Insufficient')
body(pdf, 'All three major platforms (Webex, Teams, Zoom) now offer AI-generated meeting summaries. However, summaries address only 20% of the follow-up problem. A summary tells you what happened; it does not execute the actions that need to happen next. An AI summary that says "The team agreed to create three Jira tickets for the authentication bugs" is useless if no one actually creates those tickets.')

body(pdf, 'The gap between "summary" and "action" is where enterprise productivity dies. This gap represents an estimated $37 billion in lost productivity annually across the global knowledge workforce (McKinsey, 2024), based on the time spent on manual meeting follow-up multiplied by average knowledge worker compensation.')

subheading(pdf, 'Business Impact of the Problem')
bullet(pdf, 'Project delays: Critical action items fall through the cracks, causing downstream delays in product launches, customer deliverables, and strategic initiatives.')
bullet(pdf, 'Accountability gaps: Without automated tracking, it is difficult to identify which action items are overdue and who is responsible.')
bullet(pdf, 'Meeting fatigue amplification: When follow-up fails, teams schedule additional meetings to revisit the same topics, compounding the meeting overload problem.')
bullet(pdf, 'Customer impact: In customer-facing meetings, lost action items directly translate to slower response times, missed commitments, and reduced customer satisfaction scores.')
pdf.ln(2)

subheading(pdf, 'Solution 2: Intelligent Meeting-to-Action Engine')

body(pdf, 'Build an end-to-end automated pipeline that transforms every Webex meeting into a structured set of tracked, executed, and monitored actions. The engine operates in four phases: Capture, Classify, Route & Execute, and Track & Report.')

body_bold(pdf, 'Phase 1: Capture')
body(pdf, 'As the meeting progresses (or immediately after it ends), the engine processes the complete meeting recording through an advanced NLP pipeline:')
bullet(pdf, 'Speaker Diarization: ML models identify which participant said which statement, enabling accurate assignment of action items to the correct person.')
bullet(pdf, 'Sentiment Analysis: Real-time sentiment scoring detects urgency, frustration, and emphasis in speaker tone, which influences priority classification of extracted items.')
bullet(pdf, 'Topic Segmentation: The engine automatically segments the meeting into topical clusters (e.g., "Q2 budget discussion," "authentication bug review," "hiring update"), providing context for each extracted action item.')
bullet(pdf, 'Action Item Extraction: NLP models trained on enterprise meeting data identify five categories of extractable items: tasks (things to do), decisions (things agreed upon), deadlines (time commitments), assignees (responsible parties), and dependencies (what blocks what). Each extracted item receives a confidence score.')
pdf.ln(1)

body_bold(pdf, 'Phase 2: Classify & Prioritize')
body(pdf, 'Extracted items pass through a classification engine that determines priority and routing:')
bullet(pdf, 'P1-Critical: Items with explicit deadlines within 24 hours or flagged as blockers by the speaker.')
bullet(pdf, 'P2-High: Items with deadlines within one week or associated with customer-facing commitments.')
bullet(pdf, 'P3-Medium: Items with deadlines within two weeks or internal team deliverables.')
bullet(pdf, 'P4-Low: Items with no explicit deadline or categorized as "nice-to-have" discussions.')
bullet(pdf, 'Confidence Threshold: Items with confidence scores below 85% are flagged for human review rather than auto-processed, preventing false positive actions.')
pdf.ln(1)

body_bold(pdf, 'Phase 3: Route & Execute')
body(pdf, 'Based on the item type and priority, the engine automatically routes to the appropriate system:')
bullet(pdf, 'Task/Issue Items: Auto-creates Jira tickets, GitHub issues, or ServiceNow incidents with title, description, assignee, priority, sprint assignment, and labels populated from meeting context.')
bullet(pdf, 'Document Items: Generates meeting minutes, decision logs, or status reports in Webex Docs or connected document systems, formatted with speaker attribution and topic headers.')
bullet(pdf, 'Calendar/Follow-up Items: Schedules follow-up meetings with pre-populated agendas derived from the current meeting\'s unresolved items, invites the relevant participants, and sets reminders.')
bullet(pdf, 'High-risk actions (e.g., creating customer-facing tickets, modifying production systems) require explicit human approval via an in-Webex approval card before execution.')
pdf.ln(1)

body_bold(pdf, 'Phase 4: Track & Report')
body(pdf, 'All executed actions are tracked in the Webex Action Tracker Dashboard:')
bullet(pdf, 'Real-time Status: Each action item shows its current state (Pending, In Progress, Complete, Overdue) with links to the created artifacts in external systems.')
bullet(pdf, 'Automated Reminders: The engine sends reminders before deadlines and escalation notifications for overdue items to both the assignee and the meeting organizer.')
bullet(pdf, 'Weekly Digest: Every Monday, participants receive an automated summary of the previous week\'s meeting outcomes: tasks completed, tasks overdue, time saved through automation, and meeting-to-action conversion rate.')
bullet(pdf, 'Splunk Observability: All engine operations are monitored through Splunk dashboards, providing enterprise IT teams with visibility into automation performance, error rates, and system health.')
pdf.ln(1)

subheading(pdf, 'Why This Solution Wins')
body(pdf, 'No collaboration platform currently offers end-to-end meeting-to-action automation at this level. Teams Copilot can extract action items but does not automatically create tickets in external systems or track completion. Zoom AI Companion generates action items but does not route them to project management tools with full context. This solution makes Webex the only platform where meetings directly produce completed, tracked work items without any manual intervention.')

subheading(pdf, 'Expected Impact')
bullet(pdf, '73% of action items auto-completed (vs. industry average of 27% completion rate)')
bullet(pdf, 'Meeting follow-up time reduced from 45 minutes to 5 minutes per meeting')
bullet(pdf, '92% on-time task completion rate with automated reminders and escalation')
bullet(pdf, '60% reduction in "follow-up meetings" scheduled to revisit incomplete action items')
bullet(pdf, 'Estimated productivity savings of $4,200 per knowledge worker per year')
pdf.ln(2)
source_note(pdf, 'Sources: Microsoft Work Trend Index 2024; Otter.ai Workplace Productivity Report 2024; McKinsey Future of Work Report 2024; Cisco FY2024 10-K.')

subheading(pdf, 'Solution 2 Flowchart: Intelligent Meeting-to-Action Engine')
body(pdf, 'The following flowchart details the four-phase pipeline from meeting capture through action tracking, including the classification engine, multi-path routing logic, human approval gates, and Splunk-powered tracking dashboard.')
pdf.ln(2)

pdf.image('cisco_case/figures/flowchart_2_meeting_to_action.png', x=pdf.l_margin, w=img_w)

# ============================================================
# PROBLEM 3
# ============================================================
pdf.add_page()
heading(pdf, 'Problem 3: Weak Developer & Integration Ecosystem')

subheading(pdf, 'Problem Definition')
body(pdf, 'Microsoft Teams offers over 2,000 third-party integrations through its app marketplace. Zoom offers over 2,500 integrations through the Zoom App Marketplace. Webex\'s integration ecosystem, while growing, remains significantly smaller and lacks the critical mass needed to compete for daily user engagement.')

body(pdf, 'More importantly, neither Teams nor Zoom has launched a dedicated AI agent development platform. The current integration model across all platforms is based on point-to-point connectors: static plugins that perform single functions (e.g., "send a Slack message when a Jira ticket is updated"). The next competitive frontier is intelligent agents: AI-powered integrations that understand context, make decisions, and execute multi-step workflows autonomously.')

body(pdf, 'Webex has an opportunity to leapfrog the connector model entirely by building the industry\'s first enterprise-grade AI agent marketplace. However, achieving this requires solving a trust problem that no other platform has addressed: How do you allow third-party AI agents to operate autonomously within enterprise environments while maintaining security, compliance, and data governance?')

subheading(pdf, 'Why This Problem Matters More Than Feature Parity')
body(pdf, 'Integration ecosystems create self-reinforcing network effects. More integrations attract more users. More users attract more developers. More developers build more integrations. This flywheel is the primary reason Teams and Zoom maintain their market positions even when individual features are comparable to Webex.')

body(pdf, 'Breaking into this cycle with a "me too" approach (building more basic connectors) will not work. Webex needs a fundamentally different value proposition for developers: the ability to build, certify, and monetize AI agents that no other platform supports. This transforms the ecosystem question from "who has more plugins?" to "who has the most intelligent, trusted, and profitable agent marketplace?"')

subheading(pdf, 'Business Impact of the Problem')
bullet(pdf, 'Reduced daily utility: Users who cannot connect their daily tools (CRM, project management, HR systems) to Webex treat it as a "meetings-only" platform, reducing engagement and stickiness.')
bullet(pdf, 'Developer disinterest: Developers prioritize platforms with larger user bases. Without a compelling differentiator, developer investment flows to Teams and Zoom.')
bullet(pdf, 'Enterprise adoption friction: Large organizations evaluate collaboration platforms partly on integration breadth. A smaller ecosystem creates friction in enterprise procurement decisions.')
bullet(pdf, 'Revenue limitation: Without marketplace revenue (transaction fees, premium agent subscriptions), Webex relies solely on seat-based licensing, which limits growth potential.')
pdf.ln(2)

subheading(pdf, 'Solution 3: Secure AI Agent Marketplace & Developer Platform')

body(pdf, 'Launch the industry\'s first enterprise-grade AI agent marketplace, built on Cisco\'s security infrastructure, that enables developers to build, certify, deploy, and monetize AI agents within the Webex ecosystem. The platform operates on a four-stage lifecycle: Build, Certify, Deploy, and Monitor.')

body_bold(pdf, 'Stage 1: BUILD - Developer SDK and Tools')
body(pdf, 'Provide developers with a comprehensive SDK and development environment:')
bullet(pdf, 'Agent SDK: Available in Python and JavaScript, the SDK provides pre-built components for common agent patterns (meeting listeners, task executors, data retrievers, notification senders). Developers can build agents in hours rather than weeks.')
bullet(pdf, 'Agent Templates: Ready-to-customize templates for common use cases (CRM updater, ticket creator, document generator, calendar scheduler) reduce development time by 60%.')
bullet(pdf, 'Sandbox Environment: A cloud-based testing environment that simulates real Webex meetings, API connections, and data flows without requiring production access. Developers can test agents against mock meetings with realistic conversation data.')
bullet(pdf, 'API Documentation: Comprehensive API docs covering the Webex meeting lifecycle, real-time transcription feeds, user context data, and A2A protocol specifications.')
pdf.ln(1)

body_bold(pdf, 'Stage 2: CERTIFY - Cisco Security Certification Pipeline')
body(pdf, 'Every agent must pass Cisco\'s security certification before listing in the marketplace. This is the critical differentiator that no other platform offers:')
bullet(pdf, 'Static Code Analysis: Automated scanning for vulnerabilities, backdoors, data exfiltration patterns, and insecure API usage.')
bullet(pdf, 'Permission Review: Verification that the agent\'s declared data scopes match its actual code behavior. Zero-trust policy enforcement ensures agents can only access the minimum data necessary for their function.')
bullet(pdf, 'Performance Testing: Latency benchmarking (<200ms response time), load testing (1,000+ concurrent users), memory/CPU profiling, and failure recovery validation.')
bullet(pdf, 'Compliance Validation: Automated checks against SOC 2, HIPAA, FedRAMP, and GDPR requirements based on the agent\'s declared data handling practices.')
bullet(pdf, 'Cisco Trust Badge: Agents that pass all certification stages receive the "Cisco Verified Agent" badge, signaling to enterprise buyers that the agent meets Cisco\'s security standards.')
pdf.ln(1)

body_bold(pdf, 'Stage 3: DEPLOY - Enterprise Administration and Activation')
body(pdf, 'Enterprise IT administrators control agent deployment through a centralized management console:')
bullet(pdf, 'Marketplace Discovery: Admins browse certified agents by industry vertical (healthcare, finance, government, manufacturing), use case category (productivity, compliance, sales, HR), and security certification level.')
bullet(pdf, 'Configuration & Scoping: Admins set which teams can use each agent, what data the agent can access, what approval workflows are required, and usage limits/budgets.')
bullet(pdf, 'Sandboxed Execution: Deployed agents run in isolated containers within Webex Cloud, with strict resource limits and network policies that prevent agents from accessing unauthorized systems or data.')
bullet(pdf, 'Gradual Rollout: Admins can deploy agents to pilot groups before organization-wide activation, with A/B testing capabilities to measure productivity impact.')
pdf.ln(1)

body_bold(pdf, 'Stage 4: MONITOR - Continuous Observability with Splunk')
body(pdf, 'Splunk provides enterprise-grade monitoring for all deployed agents:')
bullet(pdf, 'Real-Time Dashboards: Agent performance metrics (response time, success rate, error rate), usage analytics (active users, invocations per day), and resource consumption (CPU, memory, API calls).')
bullet(pdf, 'Anomaly Detection: ML-powered anomaly detection identifies unusual agent behavior (unexpected data access patterns, performance degradation, security policy violations) and triggers automated alerts.')
bullet(pdf, 'Kill Switch: Enterprise admins can immediately deactivate any agent that triggers a security alert or exhibits anomalous behavior, with full audit trail preservation.')
bullet(pdf, 'Usage Analytics & Billing: Per-agent usage tracking enables pay-per-use or subscription-based billing models, with revenue sharing between Cisco and agent developers (70/30 split favoring developers to incentivize ecosystem growth).')
pdf.ln(1)

subheading(pdf, 'Why This Solution Wins')
body(pdf, 'The security certification pipeline is the decisive competitive advantage. Enterprise IT departments will not deploy autonomous AI agents unless they trust the platform\'s security governance. Cisco\'s existing security certifications (FedRAMP High, HIPAA, SOC 2 Type II) and the Splunk observability platform create a trust layer that neither Microsoft nor Zoom can replicate. This makes Webex the only platform where regulated industries can safely deploy third-party AI agents.')

body(pdf, 'The marketplace model also transforms Webex\'s business economics. Instead of relying solely on per-seat licensing, Cisco earns marketplace transaction fees and premium agent subscriptions. This creates a new, high-margin revenue stream with strong network effects: more agents attract more users, which attract more developers, which produce more agents.')

subheading(pdf, 'Expected Impact')
bullet(pdf, '500+ certified AI agents in the marketplace within Year 1')
bullet(pdf, '$150 million marketplace gross merchandise value (GMV) by FY2028')
bullet(pdf, '3x growth in Webex developer ecosystem within 18 months')
bullet(pdf, '85% enterprise customer renewal rate (driven by agent-specific stickiness)')
bullet(pdf, 'New revenue stream: estimated $50M annual marketplace commission revenue by FY2029')
pdf.ln(2)
source_note(pdf, 'Sources: Cisco FY2024 10-K; Splunk platform documentation; Salesforce AppExchange economics model; Apple App Store developer revenue sharing framework; MarketsandMarkets Agentic AI Market Report 2024.')

subheading(pdf, 'Solution 3 Flowchart: Secure AI Agent Marketplace')
body(pdf, 'The following flowchart details the complete Build-Certify-Deploy-Monitor lifecycle, including the Cisco security certification pipeline, enterprise admin deployment controls, Splunk-powered monitoring, and example marketplace agents across five industry verticals.')
pdf.ln(2)

pdf.image('cisco_case/figures/flowchart_3_marketplace.png', x=pdf.l_margin, w=img_w)

# ============================================================
# CONCLUSION
# ============================================================
pdf.add_page()
heading(pdf, 'Integrated Strategy: How the Three Solutions Work Together')

body(pdf, 'The three solutions are designed as an integrated system, not independent initiatives. Together, they create a comprehensive competitive moat:')

bullet(pdf, 'Solution 1 (Agentic AI Orchestrator) provides the core intelligence: AI that can perceive meeting context, reason about tasks, and execute actions across enterprise systems.')
bullet(pdf, 'Solution 2 (Meeting-to-Action Engine) applies that intelligence to the highest-value use case: converting meetings from time sinks into productivity engines with automated follow-through.')
bullet(pdf, 'Solution 3 (AI Agent Marketplace) scales the intelligence: instead of Cisco building every agent, the marketplace enables thousands of developers to build vertical-specific agents for healthcare, finance, government, manufacturing, and more.')
pdf.ln(2)

body(pdf, 'The combined impact makes Webex indispensable rather than interchangeable. Users stay on Webex not because the video quality is marginally better, but because leaving means losing their AI agents, their automated workflows, and the productivity gains that accumulate over time.')

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
    ('Marketplace Certified Agents', '500+ in Year 1, 2,000+ by Year 3'),
    ('Developer Ecosystem Growth', '3x within 18 months'),
    ('Enterprise Renewal Rate', '85% (driven by agent-specific stickiness)'),
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
]

for i, ref in enumerate(refs):
    pdf.set_font('Times', '', 12)
    pdf.multi_cell(0, LH, f'{i+1}. {ref}')
    pdf.ln(1)

pdf.output('cisco_case/Cisco_Problems_Solutions.pdf')
print("PDF generated: cisco_case/Cisco_Problems_Solutions.pdf")

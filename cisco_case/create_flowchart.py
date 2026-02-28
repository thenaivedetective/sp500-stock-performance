import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

os.makedirs("cisco_case/figures", exist_ok=True)

# ============================================================
# FIGURE 1: ENGINEERING FLOWCHART - Workflow Orchestrator Agent
# Swimlane layout with proper engineering symbols
# Perceive -> Reason -> Act loop
# EXPANDED: Webex AI Codec ML pipeline detail
# ============================================================
fig, ax = plt.subplots(figsize=(26, 38))
ax.set_xlim(0, 26)
ax.set_ylim(0, 38)
ax.axis('off')

ax.text(13, 37.5, 'Webex Workflow Orchestrator Agent: Technical Flowchart',
        ha='center', fontsize=24, fontweight='bold', color='#002060')
ax.text(13, 36.95, 'Perceive \u2192 Reason \u2192 Act Loop  |  Webex AI Codec ML Pipeline  |  Agentic AI Architecture',
        ha='center', fontsize=14, color='#555555')

# --- SWIMLANES ---
lane_colors = ['#E8F4FD', '#FFF3E0', '#F3E5F5']
lane_labels = ['WEBEX CLOUD', 'CISCO SECURE DATA FABRIC', 'THIRD-PARTY APPS']
lane_sublabels = ['(Webex AI Codec + Real-Time Media Models)', '(Splunk Observability + Zero-Trust Identity)', '(Jira, Salesforce, SAP, etc.)']
lane_xs = [(0.5, 8.5), (9.0, 17.0), (17.5, 25.5)]

for i, ((x1, x2), color, label, sublabel) in enumerate(zip(lane_xs, lane_colors, lane_labels, lane_sublabels)):
    rect = mpatches.FancyBboxPatch((x1, 11.2), x2 - x1, 25.0, boxstyle="round,pad=0.1",
                                    facecolor=color, edgecolor='#999999', linewidth=1.5, alpha=0.5)
    ax.add_patch(rect)
    ax.text((x1 + x2) / 2, 36.0, label, ha='center', fontsize=14, fontweight='bold', color='#002060')
    ax.text((x1 + x2) / 2, 35.55, sublabel, ha='center', fontsize=9, color='#666666')

# --- HELPER FUNCTIONS ---
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
    sk = 0.35
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

# ===== FLOW LAYOUT =====
# Shifted up by 10 to make room for example section below
S = 10
WX = 4.5
DF = 13.0
TP = 21.5

# ============================================
# ROW 1: START
# ============================================
draw_oval(ax, WX, 25.0+S, 4.0, 1.0, 'START\nLive Webex Meeting Begins')
arrow(ax, WX, 24.45+S, WX, 23.7+S)

# ============================================
# ROW 2: PERCEIVE - EXPANDED AI CODEC SECTION
# ============================================
draw_dashed_box(ax, 0.8, 18.0+S, 7.4, 5.5, 'PERCEIVE: Webex AI Codec ML Pipeline', '#0050A0')

draw_para(ax, WX, 23.0+S, 5.5, 0.9,
          'Raw Audio/Video Input\nMicrophone + Camera streams', '#2C3E50', 'white', 9)
arrow(ax, WX, 22.5+S, WX, 21.8+S)

draw_rect(ax, WX, 21.2+S, 5.8, 1.0,
          'Deep Neural Network (DNN)\nBackground Noise Removal\nRemoves 150+ noise types in real-time', '#1A5276', 'white', 9)
arrow(ax, WX, 20.65+S, WX, 20.0+S)

draw_rect(ax, WX, 19.4+S, 5.8, 1.0,
          'AI Codec: Neural Speech Synthesis\nCompresses audio to ~1 kbps\n(vs 32 kbps traditional codecs)', '#1A5276', 'white', 9)
arrow(ax, WX, 18.85+S, WX, 18.1+S)

draw_rect(ax, WX, 17.2+S, 5.8, 1.2,
          'Real-Time Media Models (RMM)\n- Super Resolution: AI upscales video\n- Voice Isolation: ML separates speakers\n- Gesture Recognition: detects reactions', '#0070C0', 'white', 9)
arrow(ax, WX, 16.55+S, WX, 15.8+S)

draw_rect(ax, WX, 15.2+S, 5.8, 1.0,
          'NLP Engine: Speech-to-Text\nReal-time transcription + translation\n(100+ languages, contextual understanding)', '#0070C0', 'white', 9)
arrow(ax, WX, 14.65+S, WX, 13.8+S)

# ============================================
# ROW 3: DECISION - Task Intent Detected?
# ============================================
draw_diamond(ax, WX, 12.8+S, 2.0, 'NLP detects\nTask Intent?', '#F39C12', 'black', 10)

ax.text(1.3, 12.8+S, 'NO', fontsize=12, fontweight='bold', color='#E74C3C', ha='center')
arrow(ax, WX - 1.0, 12.8+S, 1.8, 12.8+S, '#E74C3C', 2)
arrow(ax, 1.3, 12.8+S, 1.3, 23.0+S, '#E74C3C', 2)
arrow(ax, 1.3, 23.0+S, WX - 3.1, 23.0+S, '#E74C3C', 2)
ax.text(1.3, 17.8+S, 'Continue\nMonitoring', fontsize=9, fontweight='bold', color='#E74C3C', ha='center',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#E74C3C', alpha=0.9))

ax.text(WX + 1.7, 13.5+S, 'YES', fontsize=12, fontweight='bold', color='#27AE60', ha='center')
arrow(ax, WX + 1.0, 12.8+S, DF - 3.0, 12.8+S, '#27AE60', 2.5)

# ============================================
# ROW 3 in Data Fabric: CONTEXT RETRIEVAL
# ============================================
draw_para(ax, DF, 12.8+S, 5.5, 1.1,
          'REASON: Fetch Context\nA2A Protocol retrieves\nproject data from systems', '#27AE60', 'white', 10)

arrow(ax, DF + 3.1, 12.8+S, TP - 2.5, 12.8+S, '#333333')

draw_para(ax, TP, 12.8+S, 5.0, 1.1,
          'EXTERNAL SYSTEMS\nJira / Salesforce / SAP\nServiceNow / GitHub', '#D35400', 'white', 9)

arrow(ax, DF, 12.15+S, DF, 11.2+S)

# ============================================
# ROW 4: DATABASE
# ============================================
draw_cyl(ax, DF, 10.3+S, 5.5, 1.6,
         'CISCO SECURE DATA FABRIC\nSplunk Observability + AppDynamics\nZero-Trust Identity Layer', '#8E44AD', 'white', 9)

arrow(ax, DF, 9.4+S, DF, 8.5+S)

# ============================================
# ROW 5: DRAFTING
# ============================================
draw_rect(ax, DF, 7.8+S, 5.5, 1.2,
          'ACT: DRAFT\nAI Agent generates task/document\ndraft using retrieved context\n+ LLM-based planning', '#0070C0', 'white', 10)

arrow(ax, DF - 3.0, 7.8+S, WX + 1.5, 6.0+S, '#333333')

# ============================================
# ROW 6: VERIFICATION DECISION
# ============================================
draw_diamond(ax, WX, 5.0+S, 2.0, 'Human-in-Loop\nApprove?', '#F39C12', 'black', 10)

ax.text(WX + 1.7, 4.0+S, 'REJECT', fontsize=11, fontweight='bold', color='#E74C3C', ha='center')
arrow(ax, WX + 1.0, 5.0+S, DF - 3.0, 7.1+S, '#E74C3C', 2)

ax.text(WX + 1.7, 5.8+S, 'APPROVE', fontsize=11, fontweight='bold', color='#27AE60', ha='center')
arrow(ax, WX + 1.0, 5.0+S, TP - 2.7, 5.0+S, '#27AE60', 2.5)

# ============================================
# ROW 6 in 3rd Party: EXECUTION
# ============================================
draw_rect(ax, TP, 5.0+S, 5.0, 1.2,
          'EXECUTE\nAgent pushes data via\nsecure API to external app\n(Jira, Salesforce, SAP)', '#E74C3C', 'white', 10)

arrow(ax, TP, 4.35+S, TP, 3.5+S)

# ============================================
# ROW 7: CONFIRMATION + END
# ============================================
draw_rect(ax, DF, 2.8+S, 5.8, 1.0,
          'CONFIRM\nStatus posted to Webex Chat:\n"Task created successfully in Jira"', '#0070C0', 'white', 9)
arrow(ax, TP, 2.8+S, DF + 3.0, 2.8+S, '#333333')
arrow(ax, DF - 3.0, 2.8+S, WX + 2.1, 2.8+S, '#333333')

draw_oval(ax, WX, 2.8+S, 4.0, 1.0, 'END\nMeeting Continues\nSeamlessly')

# ============================================
# METRICS BOX (between flowchart and example)
# ============================================
mr = mpatches.FancyBboxPatch((0.5, 10.5), 25.0, 0.7, boxstyle='round,pad=0.1',
                               facecolor='#002060', edgecolor='black', linewidth=2)
ax.add_patch(mr)
ax.text(13, 10.85, 'QUANTIFIED IMPACT:  Reduces manual data entry by 15 min/meeting  |  '
        '25% meeting-to-action conversion  |  40% workflow automation rate  |  '
        '85% task completion accuracy',
        ha='center', va='center', fontsize=11, fontweight='bold', color='white')

# ============================================
# LEGEND (top-right of 3rd party lane)
# ============================================
lx = 18.2; ly = 35.0
ax.text(lx, ly, 'LEGEND:', fontsize=12, fontweight='bold', color='#002060')
draw_oval(ax, lx+1.0, ly-0.8, 1.3, 0.5, 'Start/End', '#002060', 'white', 7)
ax.text(lx+2.3, ly-0.8, '= Terminator', fontsize=9, va='center', color='#333333')
draw_rect(ax, lx+1.0, ly-1.6, 1.3, 0.45, 'Process', '#0070C0', 'white', 7)
ax.text(lx+2.3, ly-1.6, '= Action/ML Step', fontsize=9, va='center', color='#333333')
draw_diamond(ax, lx+1.0, ly-2.4, 0.7, 'Dec.', '#F39C12', 'black', 6)
ax.text(lx+2.3, ly-2.4, '= Decision Point', fontsize=9, va='center', color='#333333')
draw_para(ax, lx+1.0, ly-3.1, 1.3, 0.4, 'I/O', '#27AE60', 'white', 7)
ax.text(lx+2.3, ly-3.1, '= Data I/O', fontsize=9, va='center', color='#333333')
draw_cyl(ax, lx+1.0, ly-3.9, 1.3, 0.6, 'DB', '#8E44AD', 'white', 7)
ax.text(lx+2.3, ly-3.9, '= Database/Store', fontsize=9, va='center', color='#333333')

r_leg = mpatches.FancyBboxPatch((lx+0.3, ly-4.7), 1.4, 0.45, boxstyle="round,pad=0.05",
                                 facecolor='white', edgecolor='#0050A0', linewidth=2, linestyle='--')
ax.add_patch(r_leg)
ax.text(lx+1.0, ly-4.5, 'Group', fontsize=7, ha='center', va='center', fontweight='bold', color='#0050A0')
ax.text(lx+2.3, ly-4.5, '= ML Pipeline Group', fontsize=9, va='center', color='#333333')

# ============================================
# WEBEX AI CODEC CALLOUT BOX (right side, below legend)
# ============================================
cb_x = 17.8; cb_y = 27.5; cb_w = 7.2; cb_h = 2.8
cb_rect = mpatches.FancyBboxPatch((cb_x, cb_y), cb_w, cb_h, boxstyle="round,pad=0.15",
                                    facecolor='#F0F7FF', edgecolor='#002060', linewidth=2.5)
ax.add_patch(cb_rect)
ax.text(cb_x + cb_w/2, cb_y + cb_h - 0.35, 'Webex AI Codec: ML Capabilities',
        ha='center', fontsize=12, fontweight='bold', color='#002060')

codec_items = [
    ('Neural Speech Synthesis:', '~1 kbps high-quality audio'),
    ('DNN Noise Removal:', '150+ noise types in real-time'),
    ('Super Resolution:', 'CNN upscales low-res to HD'),
    ('Voice Isolation:', 'ML separates speakers'),
    ('Gesture Recognition:', 'Detects hand raises, reactions'),
    ('Auto-Framing:', 'ML tracks & centers speakers'),
]
for i, (bold_part, regular) in enumerate(codec_items):
    y_pos = cb_y + cb_h - 0.8 - i * 0.32
    ax.text(cb_x + 0.3, y_pos, bold_part, fontsize=8.5, fontweight='bold', color='#1A5276')
    ax.text(cb_x + 0.3 + len(bold_part) * 0.065 + 0.1, y_pos, regular,
            fontsize=8.5, color='#333333')

# ============================================
# EXAMPLE SCENARIO - SEPARATE SECTION BELOW FLOWCHART
# Full width, clean layout, no overlap
# ============================================
ex_bg = mpatches.FancyBboxPatch((0.5, 0.3), 25.0, 9.8, boxstyle="round,pad=0.15",
                                  facecolor='#F0FFF0', edgecolor='#27AE60', linewidth=2.5)
ax.add_patch(ex_bg)

ax.text(13, 9.7, 'APPLIED EXAMPLE: Sprint Planning Meeting for Product Team',
        ha='center', fontsize=16, fontweight='bold', color='#27AE60')
ax.text(13, 9.25, 'How the Webex Workflow Orchestrator Agent works in a real meeting scenario',
        ha='center', fontsize=11, fontstyle='italic', color='#555555')

example_steps = [
    ('1. PERCEIVE', '#1A5276',
     'PM says: "We need to create a Jira ticket for the login\n'
     'bug Sarah found."  AI Codec removes cafe noise (DNN),\n'
     'NLP transcribes speech & detects task intent.'),
    ('2. REASON', '#27AE60',
     'A2A Protocol queries Jira via secure API:\n'
     '- Finds project "WEBAPP-2026"\n'
     '- Pulls Sarah\'s recent bug reports & sprint board context'),
    ('3. ACT: DRAFT', '#0070C0',
     'Agent auto-generates Jira ticket draft:\n'
     'Title: "Login Bug - Auth Timeout"  |  Assignee: Sarah\n'
     'Priority: High  |  Sprint: Current  |  Labels: bug, auth'),
    ('4. HUMAN-IN-LOOP', '#F39C12',
     'Webex shows in-meeting approval card:\n'
     '"Create this Jira ticket?  [ Approve ]  [ Edit ]  [ Reject ]"\n'
     'PM clicks Approve -- no tab switching needed.'),
    ('5. EXECUTE + CONFIRM', '#E74C3C',
     'Ticket WEBAPP-2026-347 created in Jira.\n'
     'Webex posts confirmation to chat: "Jira ticket created\n'
     'successfully. Assigned to Sarah."  Meeting continues.'),
]

step_w = 4.6
gap = 0.25
total_w = 5 * step_w + 4 * gap
start_x = (26 - total_w) / 2

for i, (title, color, desc) in enumerate(example_steps):
    sx = start_x + i * (step_w + gap)
    sy = 1.2

    step_rect = mpatches.FancyBboxPatch((sx, sy), step_w, 7.5, boxstyle="round,pad=0.12",
                                         facecolor='white', edgecolor=color, linewidth=2.5)
    ax.add_patch(step_rect)

    header_rect = mpatches.FancyBboxPatch((sx, sy + 6.3), step_w, 1.2, boxstyle="round,pad=0.08",
                                           facecolor=color, edgecolor=color, linewidth=1)
    ax.add_patch(header_rect)
    ax.text(sx + step_w/2, sy + 6.9, title,
            ha='center', va='center', fontsize=12, fontweight='bold', color='white')

    for j, line in enumerate(desc.split('\n')):
        ax.text(sx + 0.2, sy + 5.8 - j * 0.5, line,
                fontsize=8.5, color='#333333', va='top')

    if i < len(example_steps) - 1:
        arrow(ax, sx + step_w + 0.02, sy + 4.5, sx + step_w + gap - 0.02, sy + 4.5, '#27AE60', 2.5)

plt.tight_layout()
plt.savefig('cisco_case/figures/flowchart.png', dpi=200, bbox_inches='tight')
plt.close()
print("Engineering flowchart created")

# ============================================================
# FIGURE 2: Market Share Comparison
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

platforms = ['Microsoft\nTeams', 'Zoom', 'Cisco\nWebex', 'Google\nMeet', 'Others']
market_shares = [37, 10, 10, 5, 38]
colors = ['#0078D4', '#2D8CFF', '#00BCEB', '#34A853', '#CCCCCC']

wedges, texts, autotexts = axes[0].pie(market_shares, labels=platforms, autopct='%1.0f%%',
    colors=colors, startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'},
    explode=[0, 0, 0.08, 0, 0])
axes[0].set_title('UC&C Market Share 2024\n(Source: IDC Worldwide UC&C Tracker)',
                   fontsize=12, fontweight='bold')

mau_platforms = ['Microsoft\nTeams', 'Zoom\n(peak daily)', 'Cisco\nWebex']
mau_values = [320, 300, 150]
colors_mau = ['#0078D4', '#2D8CFF', '#00BCEB']
bars = axes[1].bar(mau_platforms, mau_values, color=colors_mau, edgecolor='black',
                   linewidth=0.8, width=0.5)
for bar, val in zip(bars, mau_values):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                 f'{val}M', ha='center', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Users (Millions)', fontsize=12, fontweight='bold')
axes[1].set_title('Monthly Active Users Comparison\n(Source: Company Earnings Reports 2024)',
                   fontsize=12, fontweight='bold')
axes[1].set_ylim(0, 400)
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('cisco_case/figures/market_share.png', dpi=200, bbox_inches='tight')
plt.close()
print("Market share created")

# ============================================================
# FIGURE 3: AI Feature Comparison - WHY Teams & Zoom Win
# ============================================================
fig, ax = plt.subplots(figsize=(16, 10))
ax.axis('off')

features = [
    'Meeting Summaries',
    'Real-time Transcription',
    'Language Translation',
    'Action Item Extraction',
    'Draft Documents from Meetings',
    'Create Presentations (AI)',
    'Generate Spreadsheet Formulas',
    'Workflow Automation Engine',
    'Agentic Task Execution',
    'Custom AI Agents / Plugins',
    'Cross-App AI Orchestration',
    'Developer Agent SDK',
    'Third-Party Integrations',
    'AI Pricing Model',
]
webex_vals = ['Yes', 'Yes', '100+ langs', 'Yes', 'No', 'No', 'No', 'No', 'No', 'No', 'No', 'Limited', '~500', 'Included']
teams_vals = ['Yes', 'Yes', '40+ langs', 'Yes', 'Yes (Word)', 'Yes (PPT)', 'Yes (Excel)', 'Power Automate', 'Copilot Agents', 'Yes', 'Microsoft Graph', 'Yes', '2,000+', '$30/user/mo']
zoom_vals = ['Yes', 'Yes', '36 langs', 'Yes', 'Yes (Zoom Docs)', 'No', 'No', 'Zoom Workflow', 'AI Companion 2.0', 'Zoom Apps', 'Limited', 'Yes', '2,500+', 'Free (paid plans)']

cell_text = []
cell_colors = []
for i in range(len(features)):
    wv = webex_vals[i]
    tv = teams_vals[i]
    zv = zoom_vals[i]
    def get_color(val):
        if val.startswith('Yes') or val.startswith('100') or val == 'Included':
            return '#D5F5E3'
        elif val.startswith('No'):
            return '#FADBD8'
        else:
            return '#FEF9E7'
    row_colors = ['#F5F5F5', get_color(wv), get_color(tv), get_color(zv)]
    cell_text.append([features[i], wv, tv, zv])
    cell_colors.append(row_colors)

table = ax.table(cellText=cell_text,
                 colLabels=['AI Capability', 'Cisco Webex AI', 'Microsoft Teams\n+ Copilot', 'Zoom AI\nCompanion 2.0'],
                 cellColours=cell_colors,
                 loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.7)

for (i, j), cell in table.get_celld().items():
    if i == 0:
        cell.set_facecolor('#002060')
        cell.set_text_props(color='white', fontweight='bold', fontsize=11)
    cell.set_edgecolor('#CCCCCC')

ax.set_title('Competitive AI Feature Comparison: Why Teams & Zoom Lead\n'
             'Green = Available | Yellow = Partial | Red = Missing\n'
             'Sources: webex.com/ai, microsoft.com/copilot, zoom.us/ai-assistant',
             fontsize=13, fontweight='bold', pad=25)
plt.tight_layout()
plt.savefig('cisco_case/figures/ai_comparison.png', dpi=200, bbox_inches='tight')
plt.close()
print("AI comparison created")

# ============================================================
# FIGURE 4: WHY Teams and Zoom are more popular
# ============================================================
fig, ax = plt.subplots(figsize=(18, 9))
ax.set_xlim(0, 18)
ax.set_ylim(0, 9)
ax.axis('off')

ax.text(9, 8.6, 'Why Microsoft Teams & Zoom Outperform Webex Today',
        ha='center', fontsize=18, fontweight='bold', color='#002060')

def info_box(ax, x, y, w, h, title, items, title_color, bg_color):
    rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                                    facecolor=bg_color, edgecolor=title_color, linewidth=2.5)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h - 0.35, title, ha='center', va='center',
            fontsize=13, fontweight='bold', color=title_color)
    for i, item in enumerate(items):
        ax.text(x + 0.3, y + h - 0.8 - i * 0.45, item, fontsize=9, color='#333333')

info_box(ax, 0.3, 4.3, 5.5, 4.0,
         'MICROSOFT TEAMS',
         ['Bundled FREE with Microsoft 365',
          '320M MAU - automatic install base',
          'Copilot works across Word/Excel/PPT',
          'AI drafts docs FROM meeting context',
          'Microsoft Graph connects all data',
          'Custom AI Agents in production',
          '2,000+ third-party integrations'],
         '#0078D4', '#E8F0FE')

info_box(ax, 6.3, 4.3, 5.5, 4.0,
         'ZOOM',
         ['Simple UX - "just works" design',
          'Free tier: 40-min, 100 participants',
          'AI Companion FREE for all paid users',
          'AI Companion 2.0 = early agentic',
          'Zoom Docs for AI-assisted drafting',
          'Workflow Automation engine built-in',
          '2,500+ app marketplace integrations'],
         '#2D8CFF', '#E8F4FD')

info_box(ax, 12.3, 4.3, 5.5, 4.0,
         'CISCO WEBEX (Current Gaps)',
         ['Not bundled - separate purchase',
          '150M users - 2.1x gap vs Teams',
          'AI only summarizes & transcribes',
          'No task execution capability',
          'No cross-app AI orchestration',
          'No developer agent SDK/marketplace',
          'Smaller integration ecosystem'],
         '#E74C3C', '#FFF5F5')

ax.text(9, 3.5, 'HOW WEBEX CAN LEAPFROG BOTH:', ha='center', fontsize=14,
        fontweight='bold', color='#002060')

info_box(ax, 0.3, 0.3, 17.4, 2.8,
         'WEBEX AGENTIC AI ADVANTAGE: The Security-First Agentic Platform',
         ['1. AGENTIC EXECUTION: Go beyond Copilot/Companion - AI that autonomously executes multi-step workflows across enterprise tools',
          '2. SECURITY MOAT: FedRAMP High + HIPAA + SOC 2 Type II - only platform trusted for government & healthcare agentic AI',
          '3. CISCO DATA FABRIC: Splunk ($28B) + AppDynamics + ThousandEyes = unmatched enterprise observability for AI agents',
          '4. PERCEIVE-REASON-ACT: Full agentic loop vs competitors\' assist-only model - from "here are your action items" to "done"'],
         '#27AE60', '#F0FFF0')

plt.tight_layout()
plt.savefig('cisco_case/figures/competitive_advantage.png', dpi=200, bbox_inches='tight')
plt.close()
print("Competitive advantage created")

# ============================================================
# FIGURE 5: Financial Overview
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

years = ['FY2022', 'FY2023', 'FY2024']
cisco_rev = [51.56, 57.0, 53.8]
axes[0].bar(years, cisco_rev, color=['#00BCEB', '#049FD9', '#002060'],
            edgecolor='black', linewidth=0.8, width=0.5)
for i, v in enumerate(cisco_rev):
    axes[0].text(i, v + 0.5, f'${v}B', ha='center', fontsize=12, fontweight='bold')
axes[0].set_title('Cisco Total Revenue\n(Source: Cisco 10-K SEC Filings)', fontsize=11, fontweight='bold')
axes[0].set_ylabel('Revenue ($B)', fontsize=11)
axes[0].set_ylim(0, 65)
axes[0].grid(True, alpha=0.3, axis='y')

rd_spend = [7.34, 7.59, 7.98]
axes[1].plot(years, rd_spend, 'o-', color='#002060', linewidth=2.5, markersize=10)
for i, v in enumerate(rd_spend):
    axes[1].text(i, v + 0.1, f'${v}B', ha='center', fontsize=11, fontweight='bold')
axes[1].set_title('Cisco R&D Spending\n(Source: Cisco 10-K)', fontsize=11, fontweight='bold')
axes[1].set_ylabel('R&D ($B)', fontsize=11)
axes[1].set_ylim(6.5, 8.5)
axes[1].grid(True, alpha=0.3, axis='y')

companies = ['Cisco', 'Microsoft', 'Zoom']
revenues = [53.8, 245.1, 4.6]
colors_fin = ['#00BCEB', '#0078D4', '#2D8CFF']
bars = axes[2].bar(companies, revenues, color=colors_fin, edgecolor='black', linewidth=0.8, width=0.4)
for bar, v in zip(bars, revenues):
    axes[2].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
                 f'${v}B', ha='center', fontsize=12, fontweight='bold')
axes[2].set_title('Total Revenue Comparison FY2024\n(Source: SEC 10-K Filings)', fontsize=11, fontweight='bold')
axes[2].set_ylabel('Revenue ($B)', fontsize=11)
axes[2].set_ylim(0, 280)
axes[2].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('cisco_case/figures/financials.png', dpi=200, bbox_inches='tight')
plt.close()
print("Financials created")

# ============================================================
# FIGURE 6: Agentic AI Evolution Diagram
# ============================================================
fig, ax = plt.subplots(figsize=(18, 7))
ax.set_xlim(0, 18)
ax.set_ylim(0, 7)
ax.axis('off')

ax.text(9, 6.5, 'Evolution: From AI Assistant to Agentic AI in Webex',
        ha='center', fontsize=16, fontweight='bold', color='#002060')

def draw_box(ax, x, y, w, h, text, color, text_color='white', fontsize=9, bold=True):
    rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                                    facecolor=color, edgecolor='black', linewidth=1.5)
    ax.add_patch(rect)
    weight = 'bold' if bold else 'normal'
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=fontsize,
            fontweight=weight, color=text_color)

draw_box(ax, 0.5, 2.8, 5.0, 3.0,
         'CURRENT: WEBEX\nAssistant-Led AI\n\n- Summarizes meetings\n- Transcribes audio\n- Translates 100+ langs\n- Lists action items\n\nUser must execute\neverything manually',
         '#E74C3C', fontsize=9)

draw_box(ax, 6.5, 2.8, 5.0, 3.0,
         'COMPETITORS TODAY\nCopilot / Companion\n\n- Drafts docs (Word/Zoom Docs)\n- Creates presentations\n- Generates formulas\n- Workflow automation\n\nSemi-autonomous but\nstill app-specific',
         '#F39C12', fontsize=9)

draw_box(ax, 12.5, 2.8, 5.0, 3.0,
         'WEBEX 2026+\nAgentic AI\n\n- Perceive-Reason-Act loop\n- Executes tasks end-to-end\n- Cross-platform orchestration\n- A2A agent protocols\n\nAI DOES the work\nnot just describes it',
         '#27AE60', fontsize=9)

def draw_arrow_simple(ax, x1, y1, x2, y2, color='#333333'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=3))

draw_arrow_simple(ax, 5.5, 4.3, 6.5, 4.3)
draw_arrow_simple(ax, 11.5, 4.3, 12.5, 4.3)

ax.text(3.0, 2.3, 'Webex Today', ha='center', fontsize=12, fontweight='bold', color='#E74C3C')
ax.text(9.0, 2.3, 'Teams Copilot / Zoom AI', ha='center', fontsize=12, fontweight='bold', color='#F39C12')
ax.text(15.0, 2.3, 'Webex Future (Leapfrog)', ha='center', fontsize=12, fontweight='bold', color='#27AE60')

ax.annotate('', xy=(16, 1.8), xytext=(2, 1.8),
            arrowprops=dict(arrowstyle='->', color='#002060', lw=3))
ax.text(9, 1.3, 'Increasing AI Autonomy & Business Value', ha='center',
        fontsize=13, fontweight='bold', color='#002060')
ax.text(9, 0.8, 'Key Differentiator: Cisco\'s Security Moat (FedRAMP/HIPAA/SOC2) + Splunk Data Fabric',
        ha='center', fontsize=10, color='#888888')

plt.tight_layout()
plt.savefig('cisco_case/figures/agentic_evolution.png', dpi=200, bbox_inches='tight')
plt.close()
print("Agentic evolution created")

# ============================================================
# FIGURE 7: Implementation Timeline
# ============================================================
fig, ax = plt.subplots(figsize=(16, 7))
ax.set_xlim(0, 13)
ax.set_ylim(-0.5, 8)
ax.axis('off')

ax.text(6.5, 7.5, 'Implementation Timeline: 18-Month Roadmap',
        ha='center', fontsize=16, fontweight='bold', color='#002060')

quarters = ['Q3 2026', 'Q4 2026', 'Q1 2027', 'Q2 2027', 'Q3 2027', 'Q4 2027']
for i, q in enumerate(quarters):
    x = 1 + i * 2
    ax.text(x + 0.5, 7.0, q, ha='center', fontsize=10, fontweight='bold', color='#002060')
    ax.axvline(x=x-0.3, ymin=0.05, ymax=0.85, color='#DDDDDD', linestyle='-', linewidth=0.5)

phases = [
    ('Sol. 1: Agentic AI', '#27AE60', [
        (0, 2, 'Core agent framework\n+ Perceive-Reason-Act'),
        (2, 2, 'Beta with 50 partners\n+ Human-in-the-Loop'),
        (4, 2, 'GA launch + Splunk\nobservability integration'),
    ]),
    ('Sol. 2: Agent SDK', '#2E86C1', [
        (1, 2, 'SDK design + A2A\nprotocol framework'),
        (3, 2, 'Developer preview\n+ university hackathons'),
        (5, 1, 'Agent Marketplace\nlaunch'),
    ]),
    ('Sol. 3: Workflow Engine', '#E67E22', [
        (0, 1, 'API connector\nframework'),
        (1, 2, 'Top 50 SaaS\nconnectors'),
        (3, 3, '200+ integrations\n+ AI orchestration DAGs'),
    ]),
]

for row_idx, (label, color, blocks) in enumerate(phases):
    y = 5.0 - row_idx * 2.2
    ax.text(0.3, y + 0.3, label, fontsize=11, fontweight='bold', color=color)
    for start, duration, text in blocks:
        x = 1 + start * 2
        w = duration * 2 - 0.2
        rect = mpatches.FancyBboxPatch((x, y - 0.4), w, 0.8,
               boxstyle="round,pad=0.1", facecolor=color, alpha=0.3,
               edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        ax.text(x + w/2, y, text, ha='center', va='center', fontsize=8, color='black')

plt.tight_layout()
plt.savefig('cisco_case/figures/timeline.png', dpi=200, bbox_inches='tight')
plt.close()
print("Timeline created")

# ============================================================
# FIGURE 8: Hybrid Work Statistics
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

work_modes = ['Hybrid\n(48%)', 'Fully\nOn-site\n(42%)', 'Fully\nRemote\n(10%)']
work_pcts = [48, 42, 10]
colors_work = ['#002060', '#00BCEB', '#AAAAAA']
axes[0].pie(work_pcts, labels=work_modes, autopct='%1.0f%%', colors=colors_work,
            startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'},
            explode=[0.05, 0, 0])
axes[0].set_title('Knowledge Worker Distribution 2024\n(Source: Gartner, 2024)',
                   fontsize=12, fontweight='bold')

ai_adoption = ['Already\nUsing AI', 'Plan to Adopt\nby 2026', 'No Plans\nYet']
ai_pcts = [28, 37, 35]
colors_ai = ['#27AE60', '#F39C12', '#E74C3C']
bars = axes[1].bar(ai_adoption, ai_pcts, color=colors_ai, edgecolor='black',
                   linewidth=0.8, width=0.5)
for bar, v in zip(bars, ai_pcts):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                 f'{v}%', ha='center', fontsize=14, fontweight='bold')
axes[1].set_title('Enterprise AI Collaboration Tool Adoption\n(Source: Gartner, 2024 - 65% plan by 2026)',
                   fontsize=12, fontweight='bold')
axes[1].set_ylabel('% of Enterprises', fontsize=11)
axes[1].set_ylim(0, 50)
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('cisco_case/figures/hybrid_work.png', dpi=200, bbox_inches='tight')
plt.close()
print("Hybrid work stats created")

# ============================================================
# FIGURE 9: Projected Revenue Impact
# ============================================================
fig, ax = plt.subplots(figsize=(12, 6))
years_proj = ['FY2025', 'FY2026', 'FY2027', 'FY2028', 'FY2029']
webex_base = [4.5, 4.6, 4.7, 4.8, 4.9]
webex_ai = [4.5, 4.8, 5.4, 6.1, 6.6]

ax.plot(years_proj, webex_base, 'o--', color='#AAAAAA', linewidth=2, markersize=8, label='Webex (No Agentic AI)')
ax.plot(years_proj, webex_ai, 's-', color='#002060', linewidth=3, markersize=10, label='Webex (With Agentic AI)')
ax.fill_between(years_proj, webex_base, webex_ai, alpha=0.2, color='#00BCEB')

for i in range(len(years_proj)):
    if webex_ai[i] != webex_base[i]:
        diff = webex_ai[i] - webex_base[i]
        ax.text(i, (webex_ai[i] + webex_base[i])/2, f'+${diff:.1f}B',
                ha='center', fontsize=10, fontweight='bold', color='#002060')

ax.set_ylabel('Collaboration Revenue ($B)', fontsize=12, fontweight='bold')
ax.set_title('Projected Webex Revenue Impact: Agentic AI Strategy\n(Based on IDC UC&C market growth rate of 8.4% CAGR + market share gains)',
             fontsize=13, fontweight='bold')
ax.legend(fontsize=11, loc='upper left')
ax.grid(True, alpha=0.3)
ax.set_ylim(3.5, 7.5)
plt.tight_layout()
plt.savefig('cisco_case/figures/revenue_projection.png', dpi=200, bbox_inches='tight')
plt.close()
print("Revenue projection created")

# ============================================================
# FIGURE 10: Agentic AI Market Growth
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))
years_m = ['2024', '2025', '2026', '2027', '2028', '2029', '2030']
market_size = [5.1, 8.2, 13.2, 20.5, 30.1, 39.0, 47.0]
ax.bar(years_m, market_size, color=['#00BCEB' if y in ['2024','2025'] else '#002060' for y in years_m],
       edgecolor='black', linewidth=0.8, width=0.5)
ax.plot(years_m, market_size, 'o-', linewidth=2, markersize=8, color='#E74C3C')
for i, v in enumerate(market_size):
    ax.text(i, v + 0.8, f'${v}B', ha='center', fontsize=10, fontweight='bold')
ax.set_ylabel('Market Size ($B)', fontsize=12, fontweight='bold')
ax.set_title('Global Agentic AI Market Size Projection\n(Source: MarketsandMarkets, 2024 - CAGR 44.8%)',
             fontsize=13, fontweight='bold')
ax.set_ylim(0, 55)
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('cisco_case/figures/agentic_market.png', dpi=200, bbox_inches='tight')
plt.close()
print("Agentic market created")

# ============================================================
# FIGURE 11: G2 Ratings
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))
platforms_g2 = ['Zoom', 'Microsoft\nTeams', 'Cisco\nWebex']
ratings = [4.5, 4.3, 4.2]
colors_g2 = ['#2D8CFF', '#0078D4', '#00BCEB']
bars = ax.barh(platforms_g2, ratings, color=colors_g2, edgecolor='black', linewidth=0.8, height=0.4)
for bar, v in zip(bars, ratings):
    ax.text(bar.get_width() + 0.03, bar.get_y() + bar.get_height()/2,
            f'{v}/5.0', va='center', fontsize=14, fontweight='bold')
ax.axvline(x=4.0, color='red', linestyle='--', linewidth=1.5, label='Strong threshold (4.0)')
ax.set_xlabel('G2 Rating (out of 5.0)', fontsize=12, fontweight='bold')
ax.set_title('User Satisfaction Ratings: G2 Peer Reviews 2024\n(Source: g2.com/categories/video-conferencing)',
             fontsize=13, fontweight='bold')
ax.set_xlim(3.5, 5.0)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('cisco_case/figures/g2_ratings.png', dpi=200, bbox_inches='tight')
plt.close()
print("G2 ratings created")

print("\nAll 11 figures generated successfully!")

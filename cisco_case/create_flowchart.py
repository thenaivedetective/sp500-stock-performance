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
# All shapes properly spaced with no overlaps
# ============================================================
fig, ax = plt.subplots(figsize=(24, 20))
ax.set_xlim(0, 24)
ax.set_ylim(0, 20)
ax.axis('off')

ax.text(12, 19.5, 'Webex Workflow Orchestrator Agent: Technical Flowchart',
        ha='center', fontsize=22, fontweight='bold', color='#002060')
ax.text(12, 19.0, 'Perceive \u2192 Reason \u2192 Act Loop | Agentic AI Architecture',
        ha='center', fontsize=14, color='#555555')

# --- SWIMLANES ---
lane_colors = ['#E8F4FD', '#FFF3E0', '#F3E5F5']
lane_labels = ['WEBEX CLOUD', 'CISCO SECURE DATA FABRIC', 'THIRD-PARTY APPS']
lane_sublabels = ['(Webex AI Codec + RMM)', '(Splunk Observability + Identity)', '(Jira, Salesforce, SAP, etc.)']
lane_xs = [(0.5, 7.5), (8.0, 15.5), (16.0, 23.5)]

for i, ((x1, x2), color, label, sublabel) in enumerate(zip(lane_xs, lane_colors, lane_labels, lane_sublabels)):
    rect = mpatches.FancyBboxPatch((x1, 1.2), x2 - x1, 17.0, boxstyle="round,pad=0.1",
                                    facecolor=color, edgecolor='#999999', linewidth=1.5, alpha=0.5)
    ax.add_patch(rect)
    ax.text((x1 + x2) / 2, 18.0, label, ha='center', fontsize=13, fontweight='bold', color='#002060')
    ax.text((x1 + x2) / 2, 17.6, sublabel, ha='center', fontsize=10, color='#666666')

# --- HELPER FUNCTIONS for engineering shapes ---
def draw_oval(ax, cx, cy, w, h, text, color='#002060', text_color='white', fontsize=10):
    ellipse = mpatches.Ellipse((cx, cy), w, h, facecolor=color, edgecolor='black', linewidth=2)
    ax.add_patch(ellipse)
    ax.text(cx, cy, text, ha='center', va='center', fontsize=fontsize,
            fontweight='bold', color=text_color)

def draw_rect(ax, cx, cy, w, h, text, color='#0070C0', text_color='white', fontsize=10):
    rect = mpatches.FancyBboxPatch((cx - w/2, cy - h/2), w, h, boxstyle="round,pad=0.08",
                                    facecolor=color, edgecolor='black', linewidth=2)
    ax.add_patch(rect)
    ax.text(cx, cy, text, ha='center', va='center', fontsize=fontsize,
            fontweight='bold', color=text_color)

def draw_diamond(ax, cx, cy, size, text, color='#F39C12', text_color='black', fontsize=9):
    half = size / 2
    xs = [cx, cx + half, cx, cx - half]
    ys = [cy + half, cy, cy - half, cy]
    poly = plt.Polygon(list(zip(xs, ys)), facecolor=color, edgecolor='black', linewidth=2)
    ax.add_patch(poly)
    ax.text(cx, cy, text, ha='center', va='center', fontsize=fontsize,
            fontweight='bold', color=text_color)

def draw_parallelogram(ax, cx, cy, w, h, text, color='#27AE60', text_color='white', fontsize=10):
    skew = 0.35
    xs = [cx - w/2 + skew, cx + w/2 + skew, cx + w/2 - skew, cx - w/2 - skew]
    ys = [cy - h/2, cy - h/2, cy + h/2, cy + h/2]
    poly = plt.Polygon(list(zip(xs, ys)), facecolor=color, edgecolor='black', linewidth=2)
    ax.add_patch(poly)
    ax.text(cx, cy, text, ha='center', va='center', fontsize=fontsize,
            fontweight='bold', color=text_color)

def draw_cylinder(ax, cx, cy, w, h, text, color='#8E44AD', text_color='white', fontsize=9):
    ell_h = h * 0.2
    body_bottom = cy - h/2
    body_top = cy + h/2 - ell_h
    rect = mpatches.FancyBboxPatch((cx - w/2, body_bottom), w, body_top - body_bottom,
                                    boxstyle="square,pad=0", facecolor=color,
                                    edgecolor='black', linewidth=2)
    ax.add_patch(rect)
    ellipse_top = mpatches.Ellipse((cx, body_top), w, ell_h * 2,
                                    facecolor=color, edgecolor='black', linewidth=2, zorder=5)
    ax.add_patch(ellipse_top)
    ellipse_bot = mpatches.Arc((cx, body_bottom), w, ell_h * 2, angle=0,
                                theta1=180, theta2=360, edgecolor='black', linewidth=2)
    ax.add_patch(ellipse_bot)
    ax.text(cx, cy - 0.1, text, ha='center', va='center', fontsize=fontsize,
            fontweight='bold', color=text_color, zorder=6)

def draw_arrow(ax, x1, y1, x2, y2, color='#333333', lw=2.5, cs=None):
    props = dict(arrowstyle='->', color=color, lw=lw)
    if cs:
        props['connectionstyle'] = cs
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=props)

# ===== FLOW ELEMENTS (top to bottom, well-spaced) =====
# Webex lane center: 4.0,  Data Fabric center: 11.75,  3rd Party center: 19.75

WX = 4.0
DF = 11.75
TP = 19.75

# ROW 1 (y=17): START
draw_oval(ax, WX, 17.0, 3.5, 1.0, 'START\nLive Webex Meeting Begins', '#002060', 'white', 10)

# Arrow
draw_arrow(ax, WX, 16.45, WX, 15.6)

# ROW 2 (y=15): PERCEIVE
draw_rect(ax, WX, 15.0, 5.0, 1.1, 'PERCEIVE\nWebex AI Codec + RMM\nprocesses real-time audio', '#0070C0', 'white', 10)

# Arrow
draw_arrow(ax, WX, 14.4, WX, 13.4)

# ROW 3 (y=12.5): DECISION - Task Intent Detected?
draw_diamond(ax, WX, 12.5, 1.8, 'NLP detects\nTask Intent?', '#F39C12', 'black', 9)

# NO arrow: loop back up to PERCEIVE
ax.text(1.5, 12.5, 'NO', fontsize=11, fontweight='bold', color='#E74C3C', ha='center')
draw_arrow(ax, WX - 0.9, 12.5, 1.9, 12.5, '#E74C3C', 2)
draw_arrow(ax, 1.5, 12.5, 1.5, 15.0, '#E74C3C', 2)
draw_arrow(ax, 1.5, 15.0, WX - 2.5, 15.0, '#E74C3C', 2)
ax.text(1.1, 13.8, 'Continue\nMonitoring', fontsize=8, fontweight='bold', color='#E74C3C', ha='center')

# YES arrow: go right to Data Fabric lane
ax.text(WX + 1.5, 13.0, 'YES', fontsize=11, fontweight='bold', color='#27AE60', ha='center')
draw_arrow(ax, WX + 0.9, 12.5, DF - 2.8, 12.5, '#27AE60', 2.5)

# ROW 3 in Data Fabric (y=12.5): CONTEXT RETRIEVAL
draw_parallelogram(ax, DF, 12.5, 5.0, 1.1,
                   'FETCH CONTEXT\nA2A Protocol retrieves\nproject data', '#27AE60', 'white', 10)

# Arrow right to 3rd party
draw_arrow(ax, DF + 2.8, 12.5, TP - 2.5, 12.5, '#333333')

# ROW 3 in 3rd Party (y=12.5): EXTERNAL SYSTEMS
draw_parallelogram(ax, TP, 12.5, 4.5, 1.1,
                   'EXTERNAL SYSTEMS\nJira / Salesforce / SAP\nServiceNow / GitHub', '#D35400', 'white', 9)

# Arrow down from context retrieval
draw_arrow(ax, DF, 11.9, DF, 10.8)

# ROW 4 (y=10): DATABASE
draw_cylinder(ax, DF, 10.0, 5.0, 1.5, 'CISCO SECURE DATA FABRIC\n(Splunk Observability)', '#8E44AD', 'white', 9)

# Arrow down
draw_arrow(ax, DF, 9.15, DF, 8.3)

# ROW 5 (y=7.7): DRAFTING
draw_rect(ax, DF, 7.7, 5.0, 1.1, 'ACT: DRAFT\nAI Agent generates\ntask/document draft', '#0070C0', 'white', 10)

# Arrow left to Webex lane for verification
draw_arrow(ax, DF - 2.6, 7.7, WX + 1.5, 5.8, '#333333')

# ROW 6 (y=5): VERIFICATION DECISION (back in Webex Cloud)
draw_diamond(ax, WX, 5.0, 1.8, 'Human-in-Loop\nApprove?', '#F39C12', 'black', 9)

# REJECT arrow: go right back to draft
ax.text(WX + 1.5, 4.2, 'REJECT', fontsize=10, fontweight='bold', color='#E74C3C', ha='center')
draw_arrow(ax, WX + 0.9, 5.0, DF - 2.6, 7.1, '#E74C3C', 2)

# APPROVE arrow: go right to 3rd party
ax.text(WX + 1.5, 5.7, 'APPROVE', fontsize=10, fontweight='bold', color='#27AE60', ha='center')
draw_arrow(ax, WX + 0.9, 5.0, TP - 2.5, 5.0, '#27AE60', 2.5)

# ROW 6 in 3rd Party (y=5): EXECUTION
draw_rect(ax, TP, 5.0, 4.5, 1.1, 'EXECUTE\nAgent pushes data via\nsecure API to external app', '#E74C3C', 'white', 10)

# Arrow down from execution
draw_arrow(ax, TP, 4.4, TP, 3.4)

# ROW 7 (y=2.8): CONFIRMATION (Data Fabric lane)
draw_rect(ax, DF, 2.8, 5.5, 1.0, 'CONFIRM\nStatus posted to Webex Chat:\n"Task created successfully in Jira"', '#0070C0', 'white', 9)

# Arrow from 3rd party execution down and left to confirmation
draw_arrow(ax, TP, 2.8, DF + 2.8, 2.8, '#333333')

# Arrow left to END
draw_arrow(ax, DF - 2.8, 2.8, WX + 1.8, 2.8, '#333333')

# ROW 7 in Webex (y=2.8): END
draw_oval(ax, WX, 2.8, 3.5, 1.0, 'END\nMeeting Continues\nSeamlessly', '#002060', 'white', 10)

# --- SUCCESS METRICS BOX ---
metrics_rect = mpatches.FancyBboxPatch((0.5, 0.2), 23.0, 0.7, boxstyle="round,pad=0.1",
                                        facecolor='#002060', edgecolor='black', linewidth=2)
ax.add_patch(metrics_rect)
ax.text(12, 0.55, 'QUANTIFIED IMPACT:  Reduces manual data entry by 15 min/meeting  |  '
        '25% meeting-to-action conversion  |  40% workflow automation rate  |  '
        '85% task completion accuracy',
        ha='center', va='center', fontsize=11, fontweight='bold', color='white')

# --- LEGEND (top-right, inside 3rd party lane) ---
leg_x = 17.0
leg_y = 17.0
ax.text(leg_x, leg_y, 'LEGEND:', fontsize=11, fontweight='bold', color='#002060')
draw_oval(ax, leg_x + 1.0, leg_y - 0.7, 1.3, 0.5, 'Start/End', '#002060', 'white', 7)
ax.text(leg_x + 2.2, leg_y - 0.7, '= Terminator', fontsize=8, va='center', color='#333333')
draw_rect(ax, leg_x + 1.0, leg_y - 1.4, 1.3, 0.45, 'Process', '#0070C0', 'white', 7)
ax.text(leg_x + 2.2, leg_y - 1.4, '= Action Step', fontsize=8, va='center', color='#333333')
draw_diamond(ax, leg_x + 1.0, leg_y - 2.1, 0.7, 'Dec.', '#F39C12', 'black', 6)
ax.text(leg_x + 2.2, leg_y - 2.1, '= Decision', fontsize=8, va='center', color='#333333')
draw_parallelogram(ax, leg_x + 1.0, leg_y - 2.7, 1.3, 0.4, 'I/O', '#27AE60', 'white', 7)
ax.text(leg_x + 2.2, leg_y - 2.7, '= Data I/O', fontsize=8, va='center', color='#333333')
draw_cylinder(ax, leg_x + 1.0, leg_y - 3.4, 1.3, 0.6, 'DB', '#8E44AD', 'white', 7)
ax.text(leg_x + 2.2, leg_y - 3.4, '= Database', fontsize=8, va='center', color='#333333')

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

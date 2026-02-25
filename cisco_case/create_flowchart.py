import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

os.makedirs("cisco_case/figures", exist_ok=True)

# ============================================================
# FIGURE 1: Problem-Solution Flowchart (Main Deliverable)
# ============================================================
fig, ax = plt.subplots(figsize=(20, 14))
ax.set_xlim(0, 20)
ax.set_ylim(0, 14)
ax.axis('off')

def draw_box(ax, x, y, w, h, text, color, text_color='white', fontsize=10, bold=True):
    rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                                    facecolor=color, edgecolor='black', linewidth=1.5)
    ax.add_patch(rect)
    weight = 'bold' if bold else 'normal'
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=fontsize,
            fontweight=weight, color=text_color, wrap=True,
            bbox=dict(boxstyle='round,pad=0', facecolor='none', edgecolor='none'))

def draw_arrow(ax, x1, y1, x2, y2, color='#333333'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=2.5))

ax.text(10, 13.5, 'Cisco Webex AI: From Assistant-Led to Agentic Work',
        ha='center', va='center', fontsize=18, fontweight='bold', color='#002060')
ax.text(10, 13.0, 'Problem-Solution Flowchart | Watson College of Engineering',
        ha='center', va='center', fontsize=12, fontweight='normal', color='#555555')

draw_box(ax, 7.5, 11.5, 5, 1.0,
         'ROOT CAUSE\nWebex AI Assistant = Passive Tool\n(Summarizes, but does not ACT)',
         '#C0392B', fontsize=10)

draw_arrow(ax, 3.5, 11.5, 3.5, 10.8)
draw_arrow(ax, 10, 11.5, 10, 10.8)
draw_arrow(ax, 16.5, 11.5, 16.5, 10.8)

draw_box(ax, 1.0, 9.5, 5, 1.2,
         'PROBLEM 1\nLow User Engagement Gap\nWebex ~150M vs Teams 320M MAU\n(Market Share: ~10% vs ~37%)',
         '#E74C3C', fontsize=9)
draw_box(ax, 7.5, 9.5, 5, 1.2,
         'PROBLEM 2\nAI Limited to Passive Assistance\nOnly summarizes & transcribes\nvs. Copilot executes in Office 365',
         '#E74C3C', fontsize=9)
draw_box(ax, 14.0, 9.5, 5, 1.2,
         'PROBLEM 3\nWeak Ecosystem Integration\nLimited 3rd-party app marketplace\nvs. Teams 2,000+ integrations',
         '#E74C3C', fontsize=9)

draw_arrow(ax, 3.5, 9.5, 3.5, 8.6)
draw_arrow(ax, 10, 9.5, 10, 8.6)
draw_arrow(ax, 16.5, 9.5, 16.5, 8.6)

draw_box(ax, 1.0, 7.5, 5, 1.0,
         '5 WHYS: Why low engagement?\nUI complexity > Poor onboarding >\nNo killer AI feature > No agentic tasks',
         '#F39C12', text_color='black', fontsize=8, bold=False)
draw_box(ax, 7.5, 7.5, 5, 1.0,
         '5 WHYS: Why passive AI?\nAssistant-only model > No task execution >\nNo workflow engine > No agent framework',
         '#F39C12', text_color='black', fontsize=8, bold=False)
draw_box(ax, 14.0, 7.5, 5, 1.0,
         '5 WHYS: Why weak ecosystem?\nClosed platform > No dev SDK >\nLimited APIs > No agent marketplace',
         '#F39C12', text_color='black', fontsize=8, bold=False)

draw_arrow(ax, 3.5, 7.5, 3.5, 6.6)
draw_arrow(ax, 10, 7.5, 10, 6.6)
draw_arrow(ax, 16.5, 7.5, 16.5, 6.6)

draw_box(ax, 1.0, 5.3, 5, 1.2,
         'SOLUTION 1\nAgentic AI Transformation\nAI executes tasks autonomously:\nschedule, draft, assign, follow up',
         '#27AE60', fontsize=9)
draw_box(ax, 7.5, 5.3, 5, 1.2,
         'SOLUTION 2\nWebex AI Agent Platform (SDK)\nOpen developer framework for\nvertical-specific AI agents',
         '#27AE60', fontsize=9)
draw_box(ax, 14.0, 5.3, 5, 1.2,
         'SOLUTION 3\nIntelligent Workflow Engine\n200+ enterprise integrations\nAI-powered cross-platform automation',
         '#27AE60', fontsize=9)

draw_arrow(ax, 3.5, 5.3, 3.5, 4.6)
draw_arrow(ax, 10, 5.3, 10, 4.6)
draw_arrow(ax, 16.5, 5.3, 16.5, 4.6)

draw_box(ax, 1.0, 3.3, 5, 1.2,
         'KPIs\n+35% daily active usage\n+25% meeting-to-action conversion\nNPS improvement: 4.2 to 4.5+',
         '#2E86C1', fontsize=9)
draw_box(ax, 7.5, 3.3, 5, 1.2,
         'KPIs\n500+ agents in marketplace Y1\n10,000+ developers onboarded\n3 vertical solutions launched',
         '#2E86C1', fontsize=9)
draw_box(ax, 14.0, 3.3, 5, 1.2,
         'KPIs\n200+ integrations live\n40% workflow automation rate\n50% reduction in app switching',
         '#2E86C1', fontsize=9)

draw_arrow(ax, 3.5, 3.3, 6.5, 2.3)
draw_arrow(ax, 10, 3.3, 10, 2.3)
draw_arrow(ax, 16.5, 3.3, 13.5, 2.3)

draw_box(ax, 6.0, 1.0, 8, 1.2,
         'OUTCOME: Webex becomes the first Agentic\nCollaboration Platform - AI that WORKS, not just ASSISTS\nProjected: +$2.1B incremental ARR by 2029',
         '#002060', fontsize=11)

draw_box(ax, 0.2, 0.1, 4.5, 0.7,
         'Data: Cisco 10-K FY2024, Microsoft\nFY2024 Earnings, Zoom FY2025 10-K',
         '#EEEEEE', text_color='#666666', fontsize=7, bold=False)

plt.tight_layout()
plt.savefig('cisco_case/figures/flowchart.png', dpi=200, bbox_inches='tight')
plt.close()
print("Flowchart created")

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
# FIGURE 3: AI Feature Comparison Matrix
# ============================================================
fig, ax = plt.subplots(figsize=(14, 8))
ax.axis('off')

features = [
    'Meeting Summaries',
    'Real-time Transcription',
    'Language Translation',
    'Action Item Extraction',
    'Smart Scheduling',
    'Document Generation',
    'Workflow Automation',
    'Agentic Task Execution',
    'Developer SDK/API',
    'Third-party Integrations'
]
webex_scores = [1, 1, 1, 1, 0.5, 0, 0, 0, 0.5, 0.5]
teams_scores = [1, 1, 0.5, 1, 1, 1, 1, 0.5, 1, 1]
zoom_scores =  [1, 1, 0.5, 1, 0.5, 0.5, 0.5, 0, 0.5, 0.5]

cell_colors = []
cell_text = []
for i in range(len(features)):
    row_colors = ['#F5F5F5']
    row_text = [features[i]]
    for score in [webex_scores[i], teams_scores[i], zoom_scores[i]]:
        if score == 1:
            row_colors.append('#27AE60')
            row_text.append('\u2713 Full')
        elif score == 0.5:
            row_colors.append('#F39C12')
            row_text.append('~ Partial')
        else:
            row_colors.append('#E74C3C')
            row_text.append('\u2717 Missing')
    cell_colors.append(row_colors)
    cell_text.append(row_text)

table = ax.table(cellText=cell_text,
                 colLabels=['AI Feature', 'Cisco Webex', 'Microsoft Teams', 'Zoom'],
                 cellColours=cell_colors,
                 loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 1.8)

for (i, j), cell in table.get_celld().items():
    if i == 0:
        cell.set_facecolor('#002060')
        cell.set_text_props(color='white', fontweight='bold', fontsize=12)
    cell.set_edgecolor('#DDDDDD')

ax.set_title('AI Feature Comparison: Webex vs. Competitors (2025)\nSource: Product documentation & analyst reviews',
             fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('cisco_case/figures/ai_comparison.png', dpi=200, bbox_inches='tight')
plt.close()
print("AI comparison created")

# ============================================================
# FIGURE 4: Financial Overview
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
# FIGURE 5: Agentic AI Evolution Diagram
# ============================================================
fig, ax = plt.subplots(figsize=(16, 6))
ax.set_xlim(0, 16)
ax.set_ylim(0, 6)
ax.axis('off')

ax.text(8, 5.5, 'Evolution: From AI Assistant to Agentic AI in Webex',
        ha='center', fontsize=16, fontweight='bold', color='#002060')

draw_box(ax, 0.5, 2.5, 4.5, 2.5,
         'CURRENT STATE\nAssistant-Led AI\n\n\u2022 Summarizes meetings\n\u2022 Transcribes audio\n\u2022 Suggests actions\n\u2022 User must execute',
         '#E74C3C', fontsize=9)

draw_box(ax, 5.8, 2.5, 4.5, 2.5,
         'TRANSITION\nCopilot-Level AI\n\n\u2022 Drafts documents\n\u2022 Creates agendas\n\u2022 Pre-fills templates\n\u2022 Semi-autonomous',
         '#F39C12', fontsize=9)

draw_box(ax, 11.0, 2.5, 4.5, 2.5,
         'FUTURE STATE\nAgentic AI\n\n\u2022 Executes tasks end-to-end\n\u2022 Schedules & coordinates\n\u2022 Manages workflows\n\u2022 Learns & adapts',
         '#27AE60', fontsize=9)

draw_arrow(ax, 5.0, 3.75, 5.8, 3.75, '#333333')
draw_arrow(ax, 10.3, 3.75, 11.0, 3.75, '#333333')

ax.text(2.75, 2.0, 'Webex Today', ha='center', fontsize=11, fontweight='bold', color='#E74C3C')
ax.text(8.05, 2.0, 'Teams Copilot / Zoom', ha='center', fontsize=11, fontweight='bold', color='#F39C12')
ax.text(13.25, 2.0, 'Webex 2026+', ha='center', fontsize=11, fontweight='bold', color='#27AE60')

ax.annotate('', xy=(14, 1.5), xytext=(2, 1.5),
            arrowprops=dict(arrowstyle='->', color='#002060', lw=3))
ax.text(8, 1.1, 'Increasing AI Autonomy & Business Value', ha='center',
        fontsize=12, fontweight='bold', color='#002060')
ax.text(8, 0.6, 'Source: Gartner Agentic AI Framework, 2024; MarketsandMarkets Agentic AI Report',
        ha='center', fontsize=8, color='#888888')

plt.tight_layout()
plt.savefig('cisco_case/figures/agentic_evolution.png', dpi=200, bbox_inches='tight')
plt.close()
print("Agentic evolution created")

# ============================================================
# FIGURE 6: Implementation Timeline
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
        (0, 2, 'Core agent framework\ndevelopment'),
        (2, 2, 'Beta testing with\n50 enterprise partners'),
        (4, 2, 'GA launch + iteration'),
    ]),
    ('Sol. 2: Agent SDK', '#2E86C1', [
        (1, 2, 'SDK design &\ndocumentation'),
        (3, 2, 'Developer preview\n& hackathons'),
        (5, 1, 'Marketplace\nlaunch'),
    ]),
    ('Sol. 3: Workflow Engine', '#E67E22', [
        (0, 1, 'API\nconnectors'),
        (1, 2, 'Integration with\ntop 50 SaaS tools'),
        (3, 3, 'Scale to 200+ integrations\n+ AI orchestration'),
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
# FIGURE 7: Hybrid Work Statistics
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
# FIGURE 8: G2 Ratings Comparison
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

# ============================================================
# FIGURE 9: Projected Revenue Impact
# ============================================================
fig, ax = plt.subplots(figsize=(12, 6))
years_proj = ['FY2025', 'FY2026', 'FY2027', 'FY2028', 'FY2029']
webex_base = [4.5, 4.6, 4.7, 4.8, 4.9]
webex_ai = [4.5, 4.8, 5.4, 6.1, 6.6]

ax.plot(years_proj, webex_base, 'o--', color='#AAAAAA', linewidth=2, markersize=8, label='Webex (No AI Agentic)')
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
ax.plot(years_m, market_size, 'ro-', linewidth=2, markersize=8, color='#E74C3C')
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

print("\nAll 10 figures generated successfully!")

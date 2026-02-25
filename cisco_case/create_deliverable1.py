import matplotlib
matplotlib.use('Agg')
from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        pass
    def footer(self):
        self.set_y(-15)
        self.set_font('Times', 'I', 10)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

pdf = PDF('P', 'mm', 'Letter')
pdf.set_auto_page_break(auto=True, margin=25)
pdf.set_left_margin(25)
pdf.set_right_margin(25)

def heading(pdf, text, size=14):
    pdf.set_font('Times', 'B', size)
    pdf.cell(0, 7, text, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

def subheading(pdf, text):
    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, 6, text, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)

def body(pdf, text):
    pdf.set_font('Times', '', 12)
    pdf.multi_cell(0, 5.5, text)
    pdf.ln(1)

def body_bold(pdf, text):
    pdf.set_font('Times', 'B', 12)
    pdf.multi_cell(0, 5.5, text)
    pdf.ln(1)

def bullet(pdf, text):
    pdf.set_font('Times', '', 12)
    pdf.set_x(30)
    pdf.multi_cell(0, 5.5, f'- {text}')

def source_note(pdf, text):
    pdf.set_font('Times', 'I', 10)
    pdf.multi_cell(0, 4.5, text)
    pdf.ln(1)

# ============================================================
# COVER PAGE
# ============================================================
pdf.add_page()
pdf.ln(30)
pdf.set_font('Times', 'B', 20)
pdf.cell(0, 10, 'Cisco Webex AI: From Assistant-Led to Agentic Work', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)
pdf.set_font('Times', 'B', 16)
pdf.cell(0, 8, 'Spring 2026 Cisco x WiB x SWE Case Competition', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(3)
pdf.set_font('Times', '', 14)
pdf.cell(0, 8, 'Deliverable 1', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(15)
pdf.set_font('Times', 'B', 14)
pdf.cell(0, 8, 'Lana Jalal Gidan', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(3)
pdf.set_font('Times', '', 12)
pdf.cell(0, 7, 'Watson College of Engineering and Applied Science', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 7, 'Binghamton University', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)
pdf.cell(0, 7, 'March 1, 2026', align='C', new_x="LMARGIN", new_y="NEXT")

# ============================================================
# EXECUTIVE SUMMARY
# ============================================================
pdf.add_page()
heading(pdf, 'Executive Summary')
body(pdf, 'Cisco Webex is a trusted enterprise collaboration platform recognized for security, reliability, and enterprise-grade infrastructure. However, in the rapidly evolving hybrid work landscape, Webex trails Microsoft Teams (320 million monthly active users) and Zoom (300 million daily meeting participants at peak) with approximately 150 million users. Webex holds roughly 10-12% of the $55 billion Unified Communications & Collaboration (UC&C) market, compared to Microsoft\'s dominant 35-40% share.')
body(pdf, 'This report identifies three root-cause problems limiting Webex\'s competitiveness and proposes three technically feasible, data-driven solutions centered on evolving Webex\'s AI Assistant from a passive, assistant-led tool into a fully agentic AI platform that autonomously performs tasks, manages workflows, and integrates deeply into enterprise operations.')
body(pdf, 'The core insight is that the next competitive battleground in collaboration is not features -- it is agency. While Microsoft Copilot and Zoom AI Companion assist users, neither has achieved true agentic capability where AI independently executes multi-step business processes. With Cisco\'s $7.98 billion R&D investment (FY2024), $28 billion Splunk acquisition for observability data, and existing enterprise security certifications (FedRAMP, HIPAA, SOC 2 Type II), Webex is uniquely positioned to become the first truly agentic collaboration platform.')
source_note(pdf, 'Sources: Cisco 10-K FY2024, Microsoft FY2024 Earnings, Zoom FY2025 10-K, IDC Worldwide UC&C Tracker 2024.')

# ============================================================
# INDUSTRY OVERVIEW
# ============================================================
heading(pdf, 'Industry Overview')
subheading(pdf, 'The Hybrid Work Landscape')
body(pdf, 'According to Gartner (2024), 48% of knowledge workers now operate in a hybrid model, 42% are fully on-site, and 10% are fully remote. This structural shift has made collaboration platforms essential infrastructure rather than optional tools. The global UC&C market reached approximately $55 billion in 2024 (IDC), growing at a CAGR of 8.4%.')
body(pdf, 'McKinsey (2024) reports that 58% of Americans have the opportunity to work in a hybrid arrangement. This means the addressable market for intelligent collaboration tools continues to expand as organizations seek platforms that can bridge the gap between in-office and remote workers effectively.')

subheading(pdf, 'Competitive Landscape')
body(pdf, 'The collaboration platform market is dominated by three major players:')
bullet(pdf, 'Microsoft Teams: 320M+ monthly active users, deeply integrated with Office 365 and Microsoft 365 Copilot ($30/user/month). Microsoft\'s total Intelligent Cloud + Productivity revenue exceeded $150B in FY2024.')
bullet(pdf, 'Zoom: ~$4.6B annual revenue (FY2025), 3,900+ enterprise customers contributing >$100K ARR. Zoom AI Companion launched September 2023 and is free for all paid users.')
bullet(pdf, 'Cisco Webex: ~150M+ users, part of Cisco\'s $53.8B total revenue (FY2024). Strong in government and regulated industries due to superior security certifications.')
pdf.ln(2)
source_note(pdf, 'Sources: Microsoft FY2024 10-K (https://www.microsoft.com/en-us/investor), Zoom FY2025 10-K (https://investors.zoom.us), Cisco FY2024 10-K (https://investor.cisco.com), IDC UC&C Market Tracker 2024, Gartner Future of Work Research 2024, McKinsey American Opportunity Survey 2024.')

subheading(pdf, 'The Rise of Agentic AI')
body(pdf, 'The global agentic AI market is projected to grow from $5.1 billion (2024) to $47 billion by 2030, representing a CAGR of 44.8% (MarketsandMarkets, 2024). This represents the shift from AI that assists (generating summaries, answering questions) to AI that acts (executing tasks, managing workflows, making decisions within defined guardrails).')
body(pdf, 'Gartner predicts that 65% of enterprises will deploy AI-powered collaboration tools by 2026. However, most current implementations remain at the "assistant" level -- generating text, summarizing meetings, and providing suggestions. The competitive opportunity lies in advancing to agentic AI, where the platform autonomously performs multi-step business processes.')
source_note(pdf, 'Sources: MarketsandMarkets Agentic AI Market Report 2024 (https://www.marketsandmarkets.com/Market-Reports/agentic-ai-market), Gartner "Predicts 2025: AI and Collaboration" Report.')

# ============================================================
# THREE PROBLEMS
# ============================================================
pdf.add_page()
heading(pdf, 'Problem Identification')
body(pdf, 'Using the 5 Whys root-cause analysis framework, we identified three interconnected problems that limit Webex\'s ability to compete in the next phase of hybrid work:')

subheading(pdf, 'Problem 1: Low User Engagement and Adoption Gap')
body(pdf, 'Webex has approximately 150 million users compared to Microsoft Teams\' 320 million MAU, representing a 2.1x gap in user engagement. In the UC&C market, Cisco holds approximately 10-12% market share versus Microsoft\'s 35-40%. G2 peer review ratings show Webex at 4.2/5.0 compared to Zoom (4.5/5.0) and Teams (4.3/5.0).')
body_bold(pdf, '5 Whys Root-Cause Analysis:')
bullet(pdf, 'Why low engagement? Users find the platform less intuitive than competitors.')
bullet(pdf, 'Why less intuitive? The user experience lacks differentiated value beyond security.')
bullet(pdf, 'Why no differentiation? AI features remain basic (summarization, transcription only).')
bullet(pdf, 'Why basic AI? The AI Assistant operates in a passive, assistant-only mode.')
bullet(pdf, 'ROOT CAUSE: Webex AI does not perform tasks -- it only describes what happened.')
pdf.ln(1)
source_note(pdf, 'Data: Microsoft Q2 FY2024 Earnings Call (Jan 2024) -- 320M MAU; Cisco Webex press releases -- 150M users; G2.com video conferencing category ratings (https://www.g2.com/categories/video-conferencing).')

subheading(pdf, 'Problem 2: AI Assistant Limited to Passive Role')
body(pdf, 'The current Webex AI Assistant provides meeting summaries, real-time transcription, and translation (100+ languages), but it does not execute tasks. By contrast, Microsoft Copilot can draft documents in Word, create presentations in PowerPoint, and build spreadsheets in Excel -- directly acting within the productivity suite. Zoom AI Companion, while also primarily assistant-level, is offered free to all paid users, creating a lower barrier to adoption.')
body_bold(pdf, '5 Whys Root-Cause Analysis:')
bullet(pdf, 'Why is AI passive? It was designed as a summarization engine, not a task executor.')
bullet(pdf, 'Why only summarization? No underlying workflow engine exists to route AI decisions.')
bullet(pdf, 'Why no workflow engine? Platform architecture separates AI from business logic.')
bullet(pdf, 'Why separated? No agent framework allows AI to interact with external systems.')
bullet(pdf, 'ROOT CAUSE: Webex lacks an agentic AI architecture that enables autonomous task execution.')
pdf.ln(1)
source_note(pdf, 'Data: Cisco Webex AI Assistant feature documentation (webex.com/ai); Microsoft Copilot for M365 capabilities (microsoft.com/copilot); Zoom AI Companion announcement Sept 2023 (zoom.us/ai-assistant).')

pdf.add_page()
subheading(pdf, 'Problem 3: Weak Ecosystem Integration and Developer Platform')
body(pdf, 'Microsoft Teams offers 2,000+ third-party app integrations through its marketplace and a mature developer SDK (Microsoft Graph API). Zoom has an active app marketplace with 2,500+ integrations. Webex\'s integration ecosystem, while growing, remains significantly smaller with limited developer tooling for AI-native applications.')
body(pdf, 'This ecosystem gap creates a self-reinforcing disadvantage: fewer integrations lead to lower platform stickiness, which leads to fewer developers building for Webex, which leads to even fewer integrations. Breaking this cycle requires a compelling developer platform centered on AI agents.')
body_bold(pdf, '5 Whys Root-Cause Analysis:')
bullet(pdf, 'Why weak ecosystem? Limited third-party integrations reduce daily utility.')
bullet(pdf, 'Why limited integrations? Developer adoption of Webex APIs is low.')
bullet(pdf, 'Why low developer adoption? No compelling platform differentiator for building on Webex.')
bullet(pdf, 'Why no differentiator? No agent SDK allows developers to create intelligent automations.')
bullet(pdf, 'ROOT CAUSE: Webex lacks an open AI agent platform that incentivizes ecosystem development.')
pdf.ln(1)
source_note(pdf, 'Data: Microsoft Teams App Store (appsource.microsoft.com) -- 2,000+ integrations; Zoom App Marketplace (marketplace.zoom.us) -- 2,500+ integrations; Webex App Hub (apphub.webex.com).')

# ============================================================
# THREE SOLUTIONS
# ============================================================
pdf.add_page()
heading(pdf, 'Recommended Solutions')
body(pdf, 'Our three solutions are designed to transform Webex from an assistant-led platform into the industry\'s first agentic collaboration ecosystem. Each solution addresses a root cause identified above and is grounded in technical feasibility, leveraging Cisco\'s existing infrastructure and R&D capabilities.')

subheading(pdf, 'Solution 1: Agentic AI Transformation -- AI That Works, Not Just Assists')
body_bold(pdf, 'Problem Addressed: Low User Engagement (Problem 1) and Passive AI (Problem 2)')
body(pdf, 'Transform the Webex AI Assistant from a passive summarization tool into an agentic AI system that autonomously executes tasks end-to-end. Rather than telling users "Here are your action items," the agentic AI would execute them: scheduling follow-up meetings, drafting and sending recap emails, creating project tasks in integrated tools, and triggering workflow automations.')
body_bold(pdf, 'Technical Architecture:')
bullet(pdf, 'Task Decomposition Engine: Uses LLM-based planning to break complex requests into executable sub-tasks (e.g., "organize quarterly review" becomes: schedule meeting, invite participants, create agenda template, prepare data summary from integrated sources).')
bullet(pdf, 'Execution Layer: Secure API connectors to enterprise tools (Salesforce, Jira, ServiceNow, SAP) enabling the AI to execute actions, not just suggest them.')
bullet(pdf, 'Human-in-the-Loop Guardrails: Configurable approval workflows where high-stakes actions require user confirmation while routine tasks execute autonomously. This addresses enterprise security concerns.')
bullet(pdf, 'Learning Loop: Reinforcement learning from user feedback to improve task completion accuracy over time, leveraging Cisco\'s Splunk observability data ($28B acquisition) for pattern recognition.')
pdf.ln(1)
body_bold(pdf, 'Technical Feasibility:')
body(pdf, 'Cisco\'s $7.98B R&D budget (FY2024) and existing AI infrastructure (Webex AI already handles real-time transcription at scale for 150M+ users) provide the foundation. The Splunk acquisition provides enterprise data observability capabilities essential for agentic decision-making. The agentic framework builds on existing LLM capabilities (meeting summaries, NLP) and extends them with a task execution layer.')
body_bold(pdf, 'Scalability:')
body(pdf, 'The architecture uses a microservices-based agent framework, allowing horizontal scaling. Each agent type (scheduling agent, document agent, workflow agent) operates as an independent service, enabling deployment across Cisco\'s global cloud infrastructure. Cisco\'s existing data center footprint (estimated 40+ global locations) supports low-latency agent execution worldwide.')
source_note(pdf, 'Data: Cisco FY2024 10-K -- $7.98B R&D; Splunk acquisition -- $28B (completed March 2024); Webex AI feature set (webex.com/ai).')

pdf.add_page()
subheading(pdf, 'Solution 2: Webex AI Agent Platform (Open Developer SDK)')
body_bold(pdf, 'Problem Addressed: Weak Ecosystem Integration (Problem 3)')
body(pdf, 'Launch an open AI Agent SDK that enables third-party developers and enterprise IT teams to build, deploy, and monetize custom AI agents within the Webex ecosystem. This creates a new "Webex Agent Marketplace" similar to how app stores transformed mobile platforms.')
body_bold(pdf, 'Technical Architecture:')
bullet(pdf, 'Agent SDK: Python and JavaScript SDKs with pre-built templates for common agent types (meeting coordinator, project manager, customer support, HR onboarding).')
bullet(pdf, 'Agent Runtime: Sandboxed execution environment within Webex Cloud, ensuring enterprise-grade security and data isolation. Each agent runs in its own container with defined permission scopes.')
bullet(pdf, 'Agent Marketplace: Discovery, deployment, and monetization platform where developers can publish agents and enterprises can subscribe to vertical-specific solutions.')
bullet(pdf, 'Vertical Agent Templates: Pre-built agents for healthcare (HIPAA-compliant patient coordination), financial services (compliance-aware document routing), and government (FedRAMP-certified task automation).')
pdf.ln(1)
body_bold(pdf, 'Technical Feasibility:')
body(pdf, 'Cisco already operates the Webex Developer Portal with APIs for meetings, messaging, and devices. The Agent SDK extends this infrastructure with agent lifecycle management (create, deploy, monitor, update). Cisco\'s ThousandEyes acquisition provides the network intelligence layer for monitoring agent performance across distributed environments. The sandboxed container approach leverages standard Kubernetes orchestration, which Cisco already operates at scale.')
body_bold(pdf, 'Implementation Risk:')
body(pdf, 'Primary risk is developer adoption velocity. Mitigation: launch with a $10M developer incentive fund (similar to Salesforce\'s Trailhead model), host hackathons at 50+ universities, and partner with 3 major systems integrators (Accenture, Deloitte, Wipro) for initial vertical agents.')
source_note(pdf, 'Data: Webex Developer Portal (developer.webex.com); ThousandEyes acquisition by Cisco (2020); Salesforce Trailhead developer ecosystem model as benchmark.')

subheading(pdf, 'Solution 3: Intelligent Workflow Engine with Cross-Platform Integration')
body_bold(pdf, 'Problem Addressed: All Three Problems (Engagement, AI Capability, Ecosystem)')
body(pdf, 'Build an AI-powered workflow automation engine that connects Webex to 200+ enterprise SaaS tools, making Webex the central orchestration hub for agentic work. Unlike point-to-point integrations (e.g., "connect Webex to Salesforce"), the Workflow Engine uses AI to understand user intent and automatically orchestrate multi-tool workflows.')
body_bold(pdf, 'Technical Architecture:')
bullet(pdf, 'Intent Recognition Layer: Natural language understanding that converts user requests into executable workflow DAGs (Directed Acyclic Graphs). Example: "After every customer call, update the CRM, create a follow-up task, and schedule a review if the deal is >$50K."')
bullet(pdf, 'Connector Framework: Pre-built connectors for top 50 enterprise SaaS tools (Salesforce, HubSpot, Jira, ServiceNow, SAP, Workday, Slack, GitHub, etc.) with an open connector SDK for custom integrations.')
bullet(pdf, 'AI Orchestration Engine: Coordinates multi-agent workflows across tools, handling error recovery, retry logic, and conflict resolution autonomously.')
bullet(pdf, 'Analytics Dashboard: Real-time visibility into workflow execution, time savings, and automation ROI -- powered by Splunk observability data.')
pdf.ln(1)
body_bold(pdf, 'Technical Feasibility:')
body(pdf, 'Cisco\'s AppDynamics and Splunk acquisitions provide deep application and infrastructure monitoring capabilities. The workflow engine builds on Cisco\'s existing integration with ServiceNow and Salesforce. The connector framework uses standard REST/GraphQL APIs available from all major SaaS platforms. Estimated development timeline: 12-18 months to production readiness with the first 50 connectors.')
source_note(pdf, 'Data: Cisco acquisitions -- AppDynamics ($3.7B, 2017), Splunk ($28B, 2024); SaaS integration market size $15.6B by 2027 (MarketsandMarkets).')

# ============================================================
# TECHNICAL FEASIBILITY & RISKS
# ============================================================
pdf.add_page()
heading(pdf, 'Technical Feasibility Assessment')
body(pdf, 'As Watson College of Engineering students, we assess the technical feasibility across four dimensions:')

subheading(pdf, '1. Infrastructure Readiness')
body(pdf, 'Cisco operates one of the world\'s largest networking infrastructures with 40+ global data centers. Webex already processes billions of meeting minutes annually with real-time AI transcription. The agentic AI layer adds computational overhead estimated at 15-25% above current workloads, well within Cisco\'s elastic cloud scaling capabilities. The Splunk acquisition ($28B) provides the observability infrastructure needed for monitoring agentic AI decision-making in real time.')

subheading(pdf, '2. Security & Compliance')
body(pdf, 'Cisco\'s existing security certifications (FedRAMP High, HIPAA, SOC 2 Type II, ISO 27001) provide the compliance foundation that competitors lack in regulated industries. The agentic AI system implements a "zero-trust agent" architecture where every AI action is authenticated, authorized, and audited. This is a significant competitive advantage over Teams and Zoom in government, healthcare, and financial services verticals.')

subheading(pdf, '3. Constraints')
bullet(pdf, 'Latency: Agentic task execution must complete within 2-5 seconds for user satisfaction. Multi-tool workflows may exceed this threshold. Mitigation: Asynchronous execution with real-time status updates.')
bullet(pdf, 'Data Privacy: AI agents accessing enterprise data must comply with regional data sovereignty regulations (GDPR, CCPA). Mitigation: Cisco\'s existing regional data residency options for Webex.')
bullet(pdf, 'Model Accuracy: LLM-based task decomposition may produce incorrect action plans. Mitigation: Human-in-the-loop approval for high-stakes actions; confidence scoring on all agent outputs.')
pdf.ln(1)

subheading(pdf, '4. System-Level Trade-offs')
bullet(pdf, 'Autonomy vs. Control: More agentic capability increases productivity but raises risk of unintended actions. Trade-off managed through configurable autonomy levels (low/medium/high).')
bullet(pdf, 'Open Platform vs. Security: An open Agent SDK increases ecosystem growth but expands the attack surface. Trade-off managed through sandboxed execution and mandatory security review for marketplace agents.')
bullet(pdf, 'Build vs. Buy: Building the workflow engine in-house ensures deep integration but takes longer than acquiring an existing iPaaS provider. Recommendation: Hybrid approach -- build the AI orchestration layer, acquire or partner for the connector framework.')

# ============================================================
# KPIs
# ============================================================
pdf.add_page()
heading(pdf, 'Key Performance Indicators')
body(pdf, 'We propose the following measurable KPIs to track success over an 18-month implementation period:')

subheading(pdf, 'Solution 1: Agentic AI Transformation')
bullet(pdf, 'Daily Active Usage: +35% increase within 12 months of launch')
bullet(pdf, 'Meeting-to-Action Conversion Rate: 25% of meetings generate auto-executed follow-ups')
bullet(pdf, 'User Satisfaction (NPS): Improve from current 4.2 to 4.5+ on G2 ratings')
bullet(pdf, 'Task Completion Rate: 85%+ autonomous task completion accuracy')
pdf.ln(1)

subheading(pdf, 'Solution 2: AI Agent Platform')
bullet(pdf, 'Developer Onboarding: 10,000+ developers registered within 12 months')
bullet(pdf, 'Agent Marketplace: 500+ published agents within 12 months')
bullet(pdf, 'Vertical Solutions: 3+ industry-specific agent suites (healthcare, finance, government)')
bullet(pdf, 'Enterprise Adoption: 200+ enterprise customers deploying custom agents')
pdf.ln(1)

subheading(pdf, 'Solution 3: Workflow Engine')
bullet(pdf, 'Integration Coverage: 200+ enterprise SaaS connectors within 18 months')
bullet(pdf, 'Workflow Automation Rate: 40% of post-meeting actions automated')
bullet(pdf, 'App Switching Reduction: 50% decrease in context-switching for Webex users')
bullet(pdf, 'Revenue Impact: +$2.1B incremental collaboration ARR by FY2029')
pdf.ln(1)
source_note(pdf, 'KPI benchmarks based on: Salesforce Einstein AI adoption metrics (+34% productivity); Microsoft Copilot early adoption data ($30/user/month premium); Zoom AI Companion engagement rates (Zoom FY2025 10-K). Revenue projection based on IDC UC&C market CAGR of 8.4% + estimated market share gains from agentic differentiation.')

# ============================================================
# DATA SOURCES TABLE
# ============================================================
heading(pdf, 'Data Sources and References')
body(pdf, 'All findings in this report are grounded in the following publicly available data sources:')
pdf.ln(1)

sources = [
    ('1. Cisco FY2024 Annual Report (10-K)', 'https://investor.cisco.com/financial-information/sec-filings', 'Revenue: $53.8B, R&D: $7.98B, Splunk acquisition: $28B'),
    ('2. Microsoft FY2024 Annual Report', 'https://www.microsoft.com/en-us/investor', 'Teams MAU: 320M, Copilot pricing: $30/user/month'),
    ('3. Zoom FY2025 Annual Report (10-K)', 'https://investors.zoom.us/financial-information/sec-filings', 'Revenue: $4.6B, Enterprise customers: 3,900+'),
    ('4. IDC Worldwide UC&C Market Tracker', 'https://www.idc.com/tracker/showproductinfo.jsp?containerId=IDC_P44218', 'Market size: ~$55B, CAGR: 8.4%'),
    ('5. Gartner Future of Work Survey 2024', 'https://www.gartner.com/en/newsroom', '48% hybrid, 10% remote, 42% on-site'),
    ('6. McKinsey American Opportunity Survey', 'https://www.mckinsey.com/industries/real-estate/our-insights', '58% have opportunity for hybrid work'),
    ('7. MarketsandMarkets Agentic AI Report', 'https://www.marketsandmarkets.com/Market-Reports/agentic-ai-market', '$5.1B (2024) to $47B (2030), CAGR 44.8%'),
    ('8. G2 Video Conferencing Reviews', 'https://www.g2.com/categories/video-conferencing', 'Zoom: 4.5/5, Teams: 4.3/5, Webex: 4.2/5'),
    ('9. Webex AI Assistant Documentation', 'https://www.webex.com/ai', 'Features: summaries, transcription, 100+ languages'),
    ('10. Cisco Webex Developer Portal', 'https://developer.webex.com', 'APIs, SDKs, integration documentation'),
]

for title, url, notes in sources:
    pdf.set_font('Times', 'B', 11)
    pdf.set_x(25)
    pdf.cell(0, 5, title, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('Times', '', 10)
    pdf.set_x(28)
    pdf.set_text_color(0, 0, 200)
    pdf.cell(0, 5, f'URL: {url}', new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.set_x(28)
    pdf.cell(0, 5, f'Key Data: {notes}', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

pdf.output('cisco_case/Deliverable1_Lana_Jalal_Gidan.pdf')
print("Deliverable 1 PDF generated: cisco_case/Deliverable1_Lana_Jalal_Gidan.pdf")

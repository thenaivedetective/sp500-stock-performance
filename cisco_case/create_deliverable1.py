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

W = 215.9 - 25 - 25

LH = 5

def heading(pdf, text, size=12):
    pdf.set_font('Times', 'B', 12)
    pdf.cell(0, LH, text, new_x="LMARGIN", new_y="NEXT")
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
    x = pdf.get_x()
    pdf.set_x(x + 5)
    pdf.multi_cell(W - 5, LH, f'- {text}')

def source_note(pdf, text):
    pdf.set_font('Times', 'I', 12)
    pdf.multi_cell(0, LH, text)
    pdf.ln(1)

pdf.add_page()
pdf.ln(35)
pdf.set_font('Times', 'B', 12)
pdf.cell(0, LH, 'Repositioning Cisco Webex for the Next Phase of Hybrid Work', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(LH)
pdf.set_font('Times', 'B', 12)
pdf.cell(0, LH, 'Spring 2026 Cisco x WiB x SWE Case Competition', align='C', new_x="LMARGIN", new_y="NEXT")
pdf.ln(LH)
pdf.set_font('Times', '', 12)
pdf.cell(0, LH, 'Deliverable 1: Written Analysis', align='C', new_x="LMARGIN", new_y="NEXT")
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
pdf.cell(0, LH, 'March 1, 2026', align='C', new_x="LMARGIN", new_y="NEXT")

pdf.add_page()
heading(pdf, '1. Industry Analysis')

subheading(pdf, '1.1 The Unified Communications & Collaboration Market')
body(pdf, 'The global Unified Communications and Collaboration (UC&C) market reached approximately $55 billion in 2024, growing at a compound annual growth rate (CAGR) of 8.4% (IDC Worldwide UC&C Market Tracker, 2024). This growth is driven by a fundamental structural shift in how knowledge work is performed: according to Gartner (2024), 48% of knowledge workers now operate in a hybrid model, 42% are fully on-site, and 10% are fully remote. McKinsey (2024) reports that 58% of Americans have the opportunity to work in a hybrid arrangement, meaning the addressable market for intelligent collaboration tools continues to expand.')
body(pdf, 'Collaboration platforms have evolved from optional video conferencing tools into essential enterprise infrastructure. Organizations now evaluate these platforms not just on audio and video quality, but on their ability to integrate with business workflows, support asynchronous collaboration, and leverage artificial intelligence to improve productivity. The COVID-19 pandemic accelerated adoption by several years, and the resulting changes in work patterns have proven permanent.')

subheading(pdf, '1.2 The Rise of AI in Collaboration')
body(pdf, 'The integration of AI into collaboration platforms represents the most significant competitive shift since the pandemic. Every major platform has introduced AI capabilities: Microsoft launched Copilot for Microsoft 365 at $30 per user per month, Zoom introduced AI Companion for free to all paid users, and Cisco launched the Webex AI Assistant. However, all current implementations remain at the "assistant" level, generating summaries, transcribing meetings, and providing suggestions rather than taking autonomous action.')
body(pdf, 'The global agentic AI market is projected to grow from $5.1 billion in 2024 to $47 billion by 2030, a CAGR of 44.8% (MarketsandMarkets, 2024). Agentic AI represents the shift from AI that assists to AI that acts: executing tasks, managing workflows, and making decisions within defined guardrails. Gartner predicts that 65% of enterprises will deploy AI-powered collaboration tools by 2026. The competitive opportunity lies in being the first platform to advance beyond assistant-level AI into truly agentic capabilities.')

subheading(pdf, '1.3 Market Sizing')
body(pdf, 'The UC&C market is projected to reach approximately $85 billion by 2030 at the current 8.4% CAGR. However, the AI-enhanced collaboration segment is growing significantly faster. IDC estimates that AI-enabled collaboration features will influence over $30 billion in platform spending by 2028. The intersection of agentic AI and collaboration creates a new market category with substantial first-mover advantages for the platform that establishes this capability first.')
source_note(pdf, 'Sources: IDC Worldwide UC&C Market Tracker 2024; Gartner Future of Work Survey 2024; McKinsey American Opportunity Survey 2024; MarketsandMarkets Agentic AI Market Report 2024.')

pdf.add_page()
heading(pdf, '2. Business Overview')

subheading(pdf, '2.1 Cisco Systems: Corporate Profile')
body(pdf, 'Cisco Systems is a global technology leader headquartered in San Jose, California. In fiscal year 2024, Cisco reported total revenue of $53.8 billion with a net income of approximately $10.3 billion. The company invested $7.98 billion in research and development, representing approximately 14.8% of total revenue. Cisco employs over 84,000 people worldwide and operates in more than 175 countries.')
body(pdf, 'Cisco is primarily known for its networking infrastructure (switches, routers, firewalls), but the company has been strategically transitioning toward software and subscription-based revenue. In FY2024, software and subscription revenue represented a growing share of total revenue, driven by acquisitions and organic product development. Key strategic acquisitions include AppDynamics ($3.7 billion, 2017), ThousandEyes (2020), and most significantly, Splunk ($28 billion, completed March 2024), which added enterprise-grade data observability capabilities to Cisco\'s portfolio.')

subheading(pdf, '2.2 Webex: Product Overview')
body(pdf, 'Webex is Cisco\'s cloud-based collaboration platform, serving approximately 150 million users globally. The platform includes video conferencing (Webex Meetings), team messaging (Webex Messaging), cloud calling (Webex Calling), and hardware endpoints (Webex Devices). Webex is particularly strong in enterprise and government segments due to Cisco\'s industry-leading security certifications.')
body(pdf, 'The Webex AI Assistant, launched in 2023, provides real-time meeting transcription, automated meeting summaries, and translation in 100+ languages. Webex also features proprietary audio technology including the Webex AI Codec, which uses deep neural networks for background noise removal (150+ noise types) and neural speech synthesis that compresses audio to approximately 1 kbps while maintaining quality. These AI capabilities demonstrate Cisco\'s technical competence but remain limited to passive assistance rather than active task execution.')

subheading(pdf, '2.3 Revenue Context')
body(pdf, 'Cisco does not break out Webex revenue separately in its financial disclosures. Webex falls within the broader Collaboration segment, which generated approximately $4.2 billion in FY2024 revenue. While this is substantial in absolute terms, it represents less than 8% of Cisco\'s total revenue and has shown slower growth compared to the Security and Observability segments. This positions Webex as a platform with significant upside potential if Cisco can differentiate it effectively in the market.')
source_note(pdf, 'Sources: Cisco FY2024 Annual Report (10-K), SEC Filing; Cisco Investor Relations (investor.cisco.com); Webex product documentation (webex.com/ai).')

pdf.add_page()
heading(pdf, '3. Competitive Landscape')

subheading(pdf, '3.1 Microsoft Teams')
body(pdf, 'Microsoft Teams is the dominant player in the UC&C market with over 320 million monthly active users. Teams\' primary competitive advantage is its bundled distribution: it is included at no additional cost with Microsoft 365, which has over 400 million paid seats. This gives Teams an automatic install base that competitors cannot match through product quality alone.')
body(pdf, 'Microsoft\'s AI strategy centers on Copilot for Microsoft 365, priced at $30 per user per month. Copilot\'s strength is cross-application intelligence: it can draft documents in Word from meeting context, generate formulas in Excel, create presentations in PowerPoint, and summarize email threads in Outlook. The Microsoft Graph connects all enterprise data (emails, files, calendar, chats), enabling Copilot to personalize responses with full organizational context. Microsoft has also launched custom AI agents and offers over 2,000 third-party integrations in the Teams app marketplace.')
body(pdf, 'Weaknesses: Teams\' AI capabilities, while broad, remain assistant-level. Copilot suggests and drafts but does not autonomously execute multi-step workflows. Teams is also tightly coupled to the Microsoft ecosystem, which can be a disadvantage for organizations using diverse tool stacks. The platform has also faced user experience criticism for complexity and slow performance in large organizations.')

subheading(pdf, '3.2 Zoom')
body(pdf, 'Zoom generated approximately $4.6 billion in annual revenue in FY2025, with over 3,900 enterprise customers each contributing more than $100,000 in annual recurring revenue. Zoom\'s competitive advantage lies in its simplicity and user experience: one click to join, no account needed for guests, and an interface that "just works."')
body(pdf, 'Zoom AI Companion, launched in September 2023 and offered free to all paid users, has been rapidly expanding capabilities. AI Companion 2.0 includes early agentic features: it drafts documents in Zoom Docs, automatically generates action items, updates CRM through Zoom Revenue Accelerator, and includes a built-in workflow automation engine. Zoom also offers over 2,500 integrations in its app marketplace.')
body(pdf, 'Weaknesses: Zoom lacks the enterprise data fabric that Cisco has through Splunk. It does not have the security certifications required for government and highly regulated industries. Its revenue growth has slowed significantly from pandemic peaks, and its brand is still primarily associated with video conferencing rather than a full enterprise platform.')

subheading(pdf, '3.3 Comparative Summary')
body(pdf, 'The table below summarizes key competitive metrics across the three platforms:')
pdf.set_font('Times', 'B', 12)
cols = [('Metric', 42), ('Microsoft Teams', 36), ('Zoom', 36), ('Cisco Webex', 36)]
for label, w in cols:
    pdf.cell(w, LH, label, border=1, align='C')
pdf.ln()
pdf.set_font('Times', '', 12)
rows = [
    ('Users / MAU', '320M+ MAU', '~300M peak', '~150M users'),
    ('AI Feature', 'Copilot ($30/mo)', 'AI Comp. (free)', 'AI Assistant'),
    ('AI Level', 'Assistant', 'Early Agentic', 'Assistant'),
    ('Integrations', '2,000+', '2,500+', 'Growing'),
    ('G2 Rating', '4.3 / 5.0', '4.5 / 5.0', '4.2 / 5.0'),
    ('Security Certs', 'Standard', 'Standard', 'FedRAMP, HIPAA'),
    ('Parent Revenue', '$236B (FY24)', '$4.6B (FY25)', '$53.8B (FY24)'),
]
for metric, teams, zoom, webex in rows:
    pdf.cell(42, LH, metric, border=1)
    pdf.cell(36, LH, teams, border=1, align='C')
    pdf.cell(36, LH, zoom, border=1, align='C')
    pdf.cell(36, LH, webex, border=1, align='C')
    pdf.ln()
pdf.ln(2)
source_note(pdf, 'Sources: Microsoft FY2024 10-K; Zoom FY2025 10-K; Cisco FY2024 10-K; G2.com Video Conferencing Category Reviews; respective product documentation.')

pdf.add_page()
heading(pdf, '4. Company Strengths and Weaknesses')

subheading(pdf, '4.1 Strengths')

body_bold(pdf, 'Enterprise Security and Compliance Leadership')
body(pdf, 'Cisco\'s most significant competitive advantage is its security infrastructure. Webex holds FedRAMP High authorization, HIPAA compliance, SOC 2 Type II certification, and ISO 27001 certification. Neither Microsoft Teams nor Zoom can match this breadth of security certifications, particularly for U.S. federal government use cases. This positions Webex as the only viable platform for agentic AI deployment in regulated industries, because autonomous AI agents handling sensitive data require a level of trust that only Cisco can currently provide.')

body_bold(pdf, 'Massive R&D Investment and Technical Infrastructure')
body(pdf, 'Cisco\'s $7.98 billion R&D budget (FY2024) provides the resources necessary to develop advanced AI capabilities. Webex already processes billions of meeting minutes annually with real-time AI transcription, demonstrating the scalability of its AI infrastructure. The company operates 40+ global data centers, providing the compute and network infrastructure needed for low-latency agentic AI execution worldwide.')

body_bold(pdf, 'Splunk Acquisition and Data Observability')
body(pdf, 'The $28 billion Splunk acquisition (completed March 2024) gives Cisco an enterprise data observability platform that no other collaboration vendor possesses. Splunk\'s capabilities in real-time data analytics, security information and event management (SIEM), and application performance monitoring create the foundation for monitoring and optimizing autonomous AI agent behavior at enterprise scale.')

body_bold(pdf, 'Proprietary AI Audio Technology')
body(pdf, 'The Webex AI Codec is a genuine technical differentiator. It uses deep neural networks to remove 150+ background noise types in real time and compresses audio to approximately 1 kbps using neural speech synthesis (compared to 32 kbps for traditional codecs). This technology, combined with Real-Time Media Models for super resolution, voice isolation, and gesture recognition, demonstrates that Cisco has significant AI/ML engineering capability that can be extended into agentic applications.')

subheading(pdf, '4.2 Weaknesses')

body_bold(pdf, 'No Bundled Distribution Channel')
body(pdf, 'Unlike Microsoft Teams, which is included with Microsoft 365 at no additional cost, Webex requires a separate purchase decision. This is the single largest structural disadvantage Webex faces. Microsoft\'s 400+ million paid Microsoft 365 seats give Teams an automatic install base that no amount of product improvement can overcome through feature competition alone.')

body_bold(pdf, 'AI Limited to Passive Assistance')
body(pdf, 'The current Webex AI Assistant provides meeting summaries, transcription, and translation but does not execute tasks. It tells users what happened in a meeting but does not act on that information. By contrast, Microsoft Copilot can draft documents, create presentations, and build spreadsheets across the Microsoft suite. Webex AI lacks the ability to create documents, execute workflows, or interact with external business systems autonomously.')

body_bold(pdf, 'Smaller Integration Ecosystem')
body(pdf, 'Microsoft Teams offers 2,000+ third-party integrations and Zoom offers 2,500+. Webex\'s integration ecosystem, while growing, remains significantly smaller. This creates a self-reinforcing disadvantage: fewer integrations reduce daily utility, which reduces user engagement, which reduces developer interest in building for the platform.')

body_bold(pdf, 'Brand Perception')
body(pdf, 'Webex is often perceived as an "enterprise-only" or "legacy" platform compared to the more consumer-friendly brands of Teams and Zoom. While Webex\'s security strength is valued in government and regulated industries, it can be a liability in broader market segments where ease of use and brand appeal drive adoption decisions.')
source_note(pdf, 'Sources: Cisco FY2024 10-K; Webex product documentation; competitive feature analysis from G2.com and TrustRadius reviews.')

pdf.add_page()
heading(pdf, '5. Key Challenges and Opportunities')

subheading(pdf, '5.1 Key Challenges')

body_bold(pdf, 'Challenge 1: Closing the User Engagement Gap')
body(pdf, 'Webex\'s approximately 150 million users represent a 2.1x gap compared to Microsoft Teams\' 320 million MAU. This gap is primarily driven by Teams\' bundled distribution rather than product quality. Closing this gap requires Webex to offer capabilities so differentiated that organizations choose it despite the additional cost. Incremental feature improvements will not be sufficient; a category-defining capability is needed.')

body_bold(pdf, 'Challenge 2: Competing Against Free AI')
body(pdf, 'Zoom AI Companion is free for all paid Zoom users, and Microsoft Copilot, while priced at $30 per user per month, benefits from Microsoft\'s massive distribution. Webex must demonstrate that its AI capabilities deliver measurably higher value than competitors\' AI features to justify enterprise investment. The value proposition must be clear and quantifiable.')

body_bold(pdf, 'Challenge 3: Developer Ecosystem Growth')
body(pdf, 'Building a competitive integration ecosystem requires attracting developers to the platform. Currently, developers prioritize Teams and Zoom due to their larger user bases. Webex needs a compelling platform differentiator, such as an AI agent development framework, that gives developers a reason to build for Webex that they cannot get elsewhere.')

subheading(pdf, '5.2 Opportunities')

body_bold(pdf, 'Opportunity 1: First-Mover Advantage in Agentic AI for Collaboration')
body(pdf, 'No collaboration platform has yet achieved true agentic AI capability where the AI independently executes multi-step business processes end-to-end. Microsoft Copilot assists across Office apps but does not autonomously manage workflows. Zoom AI Companion has early agentic features but lacks the enterprise data infrastructure for complex task execution. Webex, with Cisco\'s Splunk data platform, security certifications, and $7.98 billion R&D budget, is uniquely positioned to be the first truly agentic collaboration platform.')

body_bold(pdf, 'Opportunity 2: Regulated Industries as a Beachhead')
body(pdf, 'Government agencies, healthcare organizations, and financial services firms require security certifications that only Webex currently provides (FedRAMP High, HIPAA). These industries are also among the most eager to adopt AI for productivity gains but are constrained by compliance requirements. Webex can establish agentic AI in these regulated segments first, building a track record of secure autonomous AI execution before expanding to broader markets.')

body_bold(pdf, 'Opportunity 3: The Splunk Data Advantage')
body(pdf, 'The $28 billion Splunk acquisition gives Cisco a data observability platform that no other collaboration vendor possesses. This creates the foundation for AI agents that can monitor, learn from, and optimize enterprise workflows using real-time operational data. Integrating Splunk\'s analytics with Webex\'s collaboration capabilities creates a unique value proposition: the only platform where AI agents have full visibility into both communication data and operational system performance.')

body_bold(pdf, 'Opportunity 4: Open Agent Platform Economics')
body(pdf, 'Launching an open AI agent development platform (SDK, marketplace, developer incentives) could transform Webex\'s ecosystem disadvantage into a strength. If Webex becomes the platform where developers build and monetize AI agents for enterprise collaboration, it creates network effects similar to those that made the iPhone App Store and Salesforce AppExchange successful. This would generate new revenue streams and increase platform stickiness.')
source_note(pdf, 'Sources: MarketsandMarkets Agentic AI Market Report 2024; Cisco FY2024 10-K; Gartner "Predicts 2025: AI and Collaboration" Report; IDC UC&C Market Tracker 2024.')

pdf.add_page()
heading(pdf, '6. Preliminary Recommendation')

body(pdf, 'In response to the case prompt -- "What product and/or platform improvement can Cisco implement to Webex (powered by an AI assistant) to outperform Zoom and Microsoft Teams in the next phase of hybrid work?" -- we recommend that Cisco transform Webex from an assistant-led platform into the industry\'s first agentic collaboration platform through three integrated initiatives:')

subheading(pdf, '6.1 Agentic AI Transformation: From AI That Assists to AI That Works')
body(pdf, 'Transform the Webex AI Assistant from a passive summarization tool into an agentic AI system that autonomously executes tasks. The system follows a Perceive-Reason-Act architecture:')
bullet(pdf, 'PERCEIVE: The Webex AI Codec and NLP engine process real-time audio/video, identify task intents from conversation (e.g., "Create a Jira ticket for the login bug Sarah found"), and extract structured context.')
bullet(pdf, 'REASON: Using Agent-to-Agent (A2A) protocols, the AI retrieves relevant project data from integrated systems (Jira, Salesforce, SAP) and generates a complete task draft using the retrieved context plus LLM-based planning.')
bullet(pdf, 'ACT: A human-in-the-loop verification step shows the user the draft on-screen. Upon approval, the agent executes the action via secure API and confirms completion in Webex chat.')
pdf.ln(1)
body(pdf, 'This approach directly addresses the core competitive gap: while Teams Copilot assists across Office apps and Zoom AI Companion offers early automation, neither platform provides end-to-end autonomous task execution with enterprise-grade security. Cisco\'s existing security certifications (FedRAMP, HIPAA, SOC 2 Type II) enable agentic AI deployment in regulated industries where competitors cannot follow.')

subheading(pdf, '6.2 Open AI Agent Platform (Developer SDK and Marketplace)')
body(pdf, 'Launch an open Agent SDK (Python and JavaScript) that enables third-party developers and enterprise IT teams to build, deploy, and monetize custom AI agents within the Webex ecosystem. This includes:')
bullet(pdf, 'Agent Runtime: A sandboxed execution environment within Webex Cloud with defined permission scopes and enterprise-grade data isolation.')
bullet(pdf, 'Agent Marketplace: A discovery and deployment platform for vertical-specific solutions (healthcare coordination, financial compliance, government task automation).')
bullet(pdf, 'Developer Incentives: A $10 million developer fund, university hackathon partnerships, and systems integrator collaborations to bootstrap ecosystem growth.')
pdf.ln(1)
body(pdf, 'This initiative transforms Webex\'s smaller integration ecosystem from a weakness into an opportunity. Rather than competing on the number of point-to-point integrations (where Teams and Zoom lead), Webex competes on the intelligence of its integrations by enabling AI agents that orchestrate multi-tool workflows.')

subheading(pdf, '6.3 Intelligent Workflow Engine with Cross-Platform Integration')
body(pdf, 'Build an AI-powered workflow automation engine that connects Webex to 200+ enterprise SaaS tools, making Webex the central orchestration hub for work that originates in meetings. Key capabilities include:')
bullet(pdf, 'Intent Recognition: Natural language understanding that converts user requests into executable workflow plans (e.g., "After every customer call, update the CRM, create a follow-up task, and schedule a review if the deal exceeds $50K").')
bullet(pdf, 'Pre-Built Connectors: Top 50 enterprise SaaS tools (Salesforce, Jira, ServiceNow, SAP, Workday, GitHub) with an open connector SDK for custom integrations.')
bullet(pdf, 'Analytics Dashboard: Real-time visibility into workflow execution, time savings, and automation ROI, powered by Splunk observability data.')
pdf.ln(1)

subheading(pdf, '6.4 Why This Recommendation Wins')
body(pdf, 'This three-part strategy is grounded in Cisco\'s existing competitive advantages rather than requiring capabilities the company does not possess. The $7.98 billion R&D budget provides development resources. The Splunk acquisition provides the data infrastructure for intelligent agent decision-making. The security certifications provide the trust layer that enables agentic AI in regulated industries. And the Webex AI Codec demonstrates the engineering capability to build sophisticated AI/ML systems at scale.')
body(pdf, 'The expected impact includes: 35% increase in daily active usage within 12 months, 25% meeting-to-action conversion rate, 40% workflow automation rate, 85% task completion accuracy, and an estimated $2.1 billion in incremental collaboration ARR by FY2029.')
source_note(pdf, 'Sources: Cisco FY2024 10-K; Splunk acquisition details; IDC UC&C Market Tracker 2024; MarketsandMarkets Agentic AI Report; competitive analysis of Microsoft Copilot, Zoom AI Companion, and Webex AI Assistant capabilities.')

heading(pdf, 'References')
pdf.ln(1)

refs = [
    'Cisco Systems. (2024). Annual Report (Form 10-K), Fiscal Year 2024. SEC Filing. Retrieved from https://investor.cisco.com',
    'Microsoft Corporation. (2024). Annual Report (Form 10-K), Fiscal Year 2024. SEC Filing. Retrieved from https://www.microsoft.com/en-us/investor',
    'Zoom Video Communications. (2025). Annual Report (Form 10-K), Fiscal Year 2025. SEC Filing. Retrieved from https://investors.zoom.us',
    'IDC. (2024). Worldwide Unified Communications & Collaboration Market Tracker. International Data Corporation.',
    'Gartner. (2024). Future of Work Survey: Hybrid Work Trends. Gartner Research.',
    'Gartner. (2025). Predicts 2025: AI and Collaboration. Gartner Research.',
    'McKinsey & Company. (2024). American Opportunity Survey: Hybrid Work Patterns. McKinsey Global Institute.',
    'MarketsandMarkets. (2024). Agentic AI Market Report: Global Forecast to 2030. MarketsandMarkets Research.',
    'G2. (2025). Video Conferencing Software Reviews and Ratings. Retrieved from https://www.g2.com/categories/video-conferencing',
    'Cisco Webex. (2025). Webex AI Assistant Features and Documentation. Retrieved from https://www.webex.com/ai',
    'Microsoft. (2025). Microsoft 365 Copilot Product Documentation. Retrieved from https://www.microsoft.com/copilot',
    'Zoom. (2025). Zoom AI Companion Product Documentation. Retrieved from https://zoom.us/ai-assistant',
]

for i, ref in enumerate(refs):
    pdf.set_font('Times', '', 12)
    pdf.multi_cell(0, LH, f'{i+1}. {ref}')
    pdf.ln(1)

pdf.output('cisco_case/Deliverable1_Lana_Jalal_Gidan.pdf')
print("Deliverable 1 PDF generated: cisco_case/Deliverable1_Lana_Jalal_Gidan.pdf")

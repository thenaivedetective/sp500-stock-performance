# SSIE605 Project Repository

## Overview
Academic project repository for SSIE-605 (Applied Multivariate Data Analysis) at Binghamton University.

**Current Status:** Three Factor Analysis presentations completed

## Presentation 1: Toothpaste Consumer Preferences
- **Topic:** Factor Analysis in Marketing / Consumer Analytics
- **Application Area:** Toothpaste Consumer Preferences (Malhotra, 2010)
- **Format:** PowerPoint presentation (23 slides, 8 visualizations)
- **Output File:** Factor_Analysis_Presentation.pptx
- **Script:** create_presentation.py
- **Figures Directory:** figures/ (8 PNG visualization files)
- **Status:** Complete

### Research Papers Referenced (Presentation 1)
1. Shrestha, N. (2021). "Factor Analysis as a Tool for Survey Analysis." DOI: 10.12691/ajams-9-1-2
2. Hadi, N.U. et al. (2016). "An Easy Approach to Exploratory Factor Analysis." DOI: 10.5901/jesr.2016.v6n1p215
3. Malhotra, N.K. (2010). Marketing Research: An Applied Orientation. 6th Ed., Pearson.

### Key Results (Presentation 1)
- KMO = 0.813, Bartlett's Chi-sq = 637.65, p < 0.0001
- 2 factors extracted, 82.49% total variance explained
- Eigenvalues: Factor 1 = 2.731, Factor 2 = 2.218

## Presentation 2: Employee Job Satisfaction in Healthcare Organizations
- **Topic:** Factor Analysis in Marketing Analytics / Employee Satisfaction
- **Application Area:** Employee Job Satisfaction using EFA + CFA
- **Primary Study:** Karaferis, D., Aletras, V. & Niakas, D. (2022) — BMC Psychology
- **Format:** PowerPoint presentation (27 slides, 11 visualizations)
- **Output File:** Factor_Analysis_JobSatisfaction_Presentation.pptx
- **Script:** create_presentation2.py
- **Figures Directory:** figures2/ (11 PNG visualization files)
- **Status:** Complete

### Research Papers Referenced (Presentation 2)
1. Karaferis, D., Aletras, V. & Niakas, D. (2022). "Determining Dimensions of Job Satisfaction in Healthcare Using Factor Analysis." BMC Psychology, 10, Article 240. DOI: 10.1186/s40359-022-00941-2
2. Spector, P.E. (1985). "Measurement of Human Service Staff Satisfaction: Development of the Job Satisfaction Survey." American Journal of Community Psychology, 13, 693-713. DOI: 10.1007/BF00929796
3. Dziuba, S.T. et al. (2020). "Employees' Job Satisfaction and Their Work Performance." CzOTO, 2(1), 18-25. DOI: 10.2478/czoto-2020-0003

### Key Results (Presentation 2) — All from published tables
- **Sample:** n = 3,278 healthcare employees from 13 Greek hospitals (81.95% response rate)
- **KMO = 0.912** (Superb), Bartlett's p = 0.000
- **6 factors extracted** from 20 retained items (reduced from original 36-item JSS):
  - Benefits & Salary, Management's Attitude, Supervision, Communication, Nature of Work, Colleagues' Support
- **Eigenvalues (Table 6):** 6.18, 3.00, 1.73, 1.64, 1.09, 1.00 — Total variance: 56.23%
- **Factor Loadings (Table 7):** 20 items across 6 factors, range 0.54–0.83
- **Cronbach's Alpha (Table 8):** Overall = 0.81, range by factor: 0.60–0.81
- **CFA Model Fit:** SRMR = 0.050, RMSEA = 0.055, IFI = 0.906, CFI = 0.906
- **JSS 9-dimension reliability (Table 1):** Range 0.41–0.81 in present study vs. 0.60–0.82 in Spector (1985)

## Presentation 3: Financial Performance Evaluation of Real Estate Companies
- **Topic:** Factor Analysis in Financial Performance Evaluation
- **Application Area:** Financial performance of 100 listed Chinese real estate companies
- **Primary Study:** Wang, Y. & Song, X. (2025) — Academic Journal of Business & Management
- **Format:** PowerPoint presentation (27 slides, 10 visualizations)
- **Output File:** Factor_Analysis_Financial_Performance_Presentation.pptx
- **Script:** create_presentation3.py
- **Figures Directory:** figures3/ (10 PNG visualization files)
- **Status:** Complete

### Research Papers Referenced (Presentation 3)
1. Wang, Y. & Song, X. (2025). "Research on the Financial Performance Evaluation of Listed Companies in the Real Estate Industry Based on Factor Analysis Method." AJBM, 7(5), 78-84. DOI: 10.25236/AJBM.2025.070510
2. Kaiser, H.F. (1974). "An Index of Factorial Simplicity." Psychometrika, 39, 31-36.
3. Shrestha, N. (2021). "Factor Analysis as a Tool for Survey Analysis." DOI: 10.12691/ajams-9-1-2

### Key Results (Presentation 3) — All from published tables
- **Sample:** 100 listed real estate companies, 2023 financial data
- **KMO = 0.706** (Meritorious), Bartlett's Chi-sq = 573.599, df = 36, p = 0.000
- **3 factors extracted** from 9 financial indicators:
  - F1: Solvency Factor, F2: Profitability Factor, F3: Operational Development Capability
- **Eigenvalues (Table 3, before rotation):** 3.262, 2.057, 1.300 — Total variance: 73.55%
- **Eigenvalues (Table 3, after rotation):** 2.733, 2.522, 1.364
- **Factor Loadings (Table 4):** 9 variables x 3 factors, range 0.732–0.956 for primary loadings
- **Score Coefficients (Table 5):** Used to build comprehensive scoring equations
- **Score Ranges (Table 6):** Solvency: -24.85 to 46.09, Profitability: -0.32 to 66.24, Oper. Dev.: -156.91 to 947.95

## User Preferences
- Preferred communication style: Simple, everyday language
- Appreciates step-by-step explanations with concrete examples
- Wants simple approaches (not complicated)
- Does NOT want other brands/companies mentioned in presentations - focus only on the topic
- Author attribution: "Lana Jalal Gidan"
- Institution: Binghamton University
- Course: SSIE-605, Professor Susan Lu

## System Architecture
- **Language**: Python 3.11
- **Development Environment**: Replit-based development
- **Project Type**: Academic presentations and data analysis
- **Key Dependencies**: python-pptx, matplotlib, seaborn, numpy, scipy, pandas

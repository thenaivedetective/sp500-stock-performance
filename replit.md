# SSIE605 Project Repository

## Overview
Academic project repository for SSIE-605 (Applied Multivariate Data Analysis) at Binghamton University.

**Current Status:** Two Factor Analysis presentations completed

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

## Presentation 2: Employee Job Satisfaction in Corporate Organizations
- **Topic:** Factor Analysis in Marketing Analytics / Employee Satisfaction
- **Application Area:** Employee Job Satisfaction using EFA + CFA
- **Format:** PowerPoint presentation (24 slides, 8 visualizations)
- **Output File:** Factor_Analysis_JobSatisfaction_Presentation.pptx
- **Script:** create_presentation2.py
- **Figures Directory:** figures2/ (8 PNG visualization files)
- **Status:** Complete

### Research Papers Referenced (Presentation 2)
1. Tsounis, A. & Sarafis, P. (2022). "Determining Dimensions of Job Satisfaction in Healthcare Using Factor Analysis." BMC Psychology, 10, Article 240. DOI: 10.1186/s40359-022-00941-2
2. Spector, P.E. (1985). "Measurement of Human Service Staff Satisfaction: Development of the Job Satisfaction Survey." American Journal of Community Psychology, 13, 693-713. DOI: 10.1007/BF00929796
3. Dziuba, S.T. et al. (2020). "Employees' Job Satisfaction and Their Work Performance." CzOTO, 2(1), 18-25. DOI: 10.2478/czoto-2020-0003

### Key Results (Presentation 2)
- KMO = 0.912 (Superb), Bartlett's Chi-sq = 31,831.572, p = 0.000
- 6 factors extracted: Benefits & Salary, Management's Attitude, Supervision, Communication, Nature of Work, Colleagues' Support
- Overall Cronbach's Alpha = 0.81, dimension range: 0.61-0.81
- CFA Model Fit: SRMR = 0.050, RMSEA = 0.055, IFI = 0.906, CFI = 0.906
- Spector JSS: 36 items, 9 dimensions, validated across 30+ countries

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

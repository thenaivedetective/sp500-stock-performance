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

## Presentation 2: Disney Brand Equity (Entertainment Industry)
- **Topic:** Factor Analysis in Entertainment Industry Brand Equity
- **Application Area:** Disney Brand Equity using CFA/SEM
- **Format:** PowerPoint presentation (24 slides, 8 visualizations)
- **Output File:** Factor_Analysis_Disney_Presentation.pptx
- **Script:** create_presentation2.py
- **Figures Directory:** figures2/ (8 PNG visualization files)
- **Status:** Complete

### Research Papers Referenced (Presentation 2)
1. Gilitwala, B. & Nag, A.K. (2022). "Understanding Effective Factors Affecting Brand Equity." DOI: 10.1080/23311975.2022.2104431
2. Sama, R. (2019). "Impact of Media Advertisements on Consumer Behaviour." DOI: 10.1177/0973258618822624
3. Shrestha, N. (2021). "Factor Analysis as a Tool for Survey Analysis." DOI: 10.12691/ajams-9-1-2

### Key Results (Presentation 2)
- 5 factors: Brand Awareness, Brand Image, Perceived Quality, Brand Association, Brand Loyalty
- CFA: All factor loadings > 0.70, AVE > 0.50, CR > 0.70
- Model Fit: CMIN/df = 2.975, CFI = 0.970, RMSEA = 0.070
- Brand Image is strongest predictor (β = +0.412)
- Brand Awareness has negative effect (β = -0.086)
- Cronbach's Alpha: BA=0.909, BI=0.711, PQ=0.889, BAs=0.943, BL=0.912, BE=0.897

## User Preferences
- Preferred communication style: Simple, everyday language
- Appreciates step-by-step explanations with concrete examples
- Wants simple approaches (not complicated)
- Author attribution: "Lana Jalal Gidan"
- Institution: Binghamton University
- Course: SSIE-605, Professor Susan Lu

## System Architecture
- **Language**: Python 3.11
- **Development Environment**: Replit-based development
- **Project Type**: Academic presentations and data analysis
- **Key Dependencies**: python-pptx, matplotlib, seaborn, numpy, scipy, pandas

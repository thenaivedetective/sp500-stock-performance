# SSIE500 Project Repository

## Overview
Academic project repository for SSIE500 course.

**Current Status:** ✅ Research Question #1 COMPLETED - Ready for submission!

## User Preferences
- Preferred communication style: Simple, everyday language
- Appreciates step-by-step explanations with concrete examples
- Wants simple approaches (not complicated)
- Author attribution: "Group 2" (not individual name)
- Institution: Binghamton University

## Current Project: Daily Routine Regularity and Health Outcomes

### Research Question
Does the Shannon entropy of daily activity patterns predict health outcomes?

### Methodology
- **Data Source**: Fitbit minute-by-minute METs data from two participants (FS1987, FS2116)
- **Approach**: Calculate Shannon entropy for each day's activity distribution
- **Activity Levels**: 4 discrete levels (Resting ≤10, Light 10-15, Moderate 15-30, Vigorous >30 METs)
- **Entropy Formula**: H(X) = -Σ p(x)log₂(p(x))
- **Interpretation**: Lower entropy = less varied activities (sedentary); Higher entropy = more varied (balanced)

### Key Findings (Last Updated: Nov 18, 2025)
- **FS1987**: Average entropy = 0.786 bits (low variety, potentially sedentary lifestyle)
- **FS2116**: Average entropy = 0.991 bits (moderate variety, more balanced)
- **Difference**: 26% higher entropy in FS2116
- **Health Implication**: FS2116 shows healthier activity patterns with more varied daily activities

## System Architecture
- **Language**: Python 3
- **Development Environment**: Replit-based development
- **Project Type**: Data analysis and computational research project

## Available Tools
- Python 3 with scientific computing packages (numpy, pandas, scipy, matplotlib, seaborn, requests)
- LaTeX for report generation

## Project Files

### Code
- `daily_routine_entropy_analysis.py` - Main analysis script

### Data Files (Generated)
- `FS1987_daily_entropy.csv` - Daily entropy values for participant FS1987
- `FS2116_daily_entropy.csv` - Daily entropy values for participant FS2116
- `entropy_summary.csv` - Summary statistics for both participants

### Visualizations
- `daily_entropy_timeseries.png` - Daily entropy over time for both participants
- `entropy_comparison.png` - Bar chart comparing average entropy
- `entropy_distribution.png` - Histogram distribution of daily entropy values

### Report
- `Final_Project_Report.tex` - LaTeX source
- `Final_Project_Report.pdf` - Complete 9-page PDF report (584KB)

### Raw Data (Input)
- `FS1987-intraday.csv` - Fitbit data for participant FS1987
- `FS2116-intraday.csv` - Fitbit data for participant FS2116

## Next Steps
- Research Question #1: ✅ COMPLETE
- Research Question #2: Available for development
- Research Question #3: Available for development

## Technical Notes
- Data has significant null values (~92% missing in FS1987)
- METs values heavily skewed (77% at baseline METs=10)
- Discretization adjusted to actual Fitbit data range
- Final implementation passed architect review

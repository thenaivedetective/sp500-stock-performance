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

## Current Project: Routine Regularity and Health Outcomes

### Research Question
Does the average Shannon entropy of activity patterns across time slots predict health outcomes (sleep quality, mood stability) in individuals monitored via wearable devices?

### Methodology
- **Data Source**: Fitbit minute-by-minute METs data from two participants (FS1987, FS2116)
- **Approach**: Temporal entropy analysis - for each minute of the day (0-1439), calculate Shannon entropy across all days
- **Activity Levels**: 4 discrete levels (Resting ≤10, Light 10-15, Moderate 15-30, Vigorous >30 METs)
- **Entropy Formula**: H(t) = -Σ p_t(x)log₂(p_t(x)) for each time slot t, then average across all 1440 minutes
- **Interpretation**: Lower temporal entropy = regular routine (same activity at same time daily); Higher temporal entropy = chaotic schedule (unpredictable patterns)

### Key Findings (Last Updated: Nov 18, 2025)
- **FS1987**: Average temporal entropy = 0.9985 bits (Moderately Regular Routine, Good health prediction)
- **FS2116**: Average temporal entropy = 1.1741 bits (Somewhat Irregular Routine, Fair health prediction)
- **Difference**: 15% lower entropy in FS1987
- **Health Implication**: FS1987 maintains more regular daily routine, associated with better sleep quality, mood stability, and metabolic health

## System Architecture
- **Language**: Python 3
- **Development Environment**: Replit-based development
- **Project Type**: Data analysis and computational research project

## Available Tools
- Python 3 with scientific computing packages (numpy, pandas, scipy, matplotlib, seaborn, requests)
- LaTeX for report generation

## Project Files

### Code
- `temporal_entropy_analysis.py` - Main temporal entropy analysis script

### Data Files (Generated)
- `FS1987_temporal_entropy.csv` - Entropy for all 1440 time slots (FS1987)
- `FS2116_temporal_entropy.csv` - Entropy for all 1440 time slots (FS2116)
- `temporal_entropy_summary.csv` - Summary statistics for both participants

### Visualizations
- `temporal_entropy_profile.png` - 24-hour entropy profile for both participants
- `temporal_entropy_comparison.png` - Bar chart comparing average temporal entropy
- `temporal_entropy_by_hour.png` - Hourly average temporal entropy

### Report
- `Final_Project_Report.tex` - LaTeX source
- `Final_Project_Report.pdf` - Complete 9-page PDF report (1.3MB)

### Raw Data (Input)
- `FS1987-intraday.csv` - Fitbit data for participant FS1987
- `FS2116-intraday.csv` - Fitbit data for participant FS2116

## Next Steps
- Research Question #1: ✅ COMPLETE (Temporal Entropy - Routine Regularity)
- Research Question #2: Available for development
- Research Question #3: Available for development

## Technical Notes
- Temporal entropy measures routine regularity across days, not daily activity variety
- Single-observation time slots treated as 0 entropy (perfect regularity)
- All 1440 minutes of day included in average calculation
- Final implementation passed architect review after critical fix

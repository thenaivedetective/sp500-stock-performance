# NYC Food Desert Analysis - Information Theory Project

## Overview

**Complete** information theory analysis of food access inequality in New York City using **REAL government data** (11,472 supermarkets, 184/190 zip codes with Census data).

**Created for:** SSIE-500 Final Project  
**Date:** November 2025  
**Status:** ✅ Complete and ready for submission

## Project Description

This project demonstrates real-world application of information theory methods to analyze:
1. **Food access inequality** across 190 NYC zip codes (REAL data from NY State & US Census)
2. **Public opinion patterns** related to food policy (simulated Twitter data with clear limitations)

**Methods Used:** Shannon Entropy, Mutual Information, KL Divergence, Conditional Entropy

## Recent Changes

**November 12, 2025:** Removed Transfer Entropy analysis per user request. Replaced with additional Mutual Information analyses (Borough ↔ Sentiment, Topic ↔ Sentiment) for Twitter section. All documentation updated accordingly.

## User Preferences

- Simple, everyday language explanations (non-technical)
- Clear documentation of data limitations
- Real data wherever possible

## Key Findings

### Real Data Analysis
- **Shannon Entropy:** H = 0.625 bits (31% of max) - relatively predictable system
- **Mutual Information (Income ↔ Food Access):** MI = 0.098 bits - **weak relationship** (surprising!)
- **13 food deserts** identified, 10 in Manhattan (77% of total)
- **Brooklyn:** Perfect uniformity, zero food deserts (H = 0.000)

### Twitter Analysis (Simulated)
- **Sentiment Entropy:** H = 1.506 bits (95% of max) - high division
- **MI(Desert ↔ Support):** 0.0095 bits
- **MI(Borough ↔ Sentiment):** 0.0007 bits  
- **MI(Topic ↔ Sentiment):** 0.0004 bits

**Important:** Twitter data is SIMULATED because real Twitter API costs $5,000/month (discontinued Academic Research API in 2023). Methodology is sound and can be applied to real data.

## Files Structure

### Main Analysis Scripts
- `complete_analysis.py` - Part 1: Data collection & core analysis (REAL Census data)
- `twitter_analysis_and_viz.py` - Part 2: Twitter simulation & visualizations

### Documentation
- `FINAL_REPORT.md` - Complete academic report (~5,500 words, APA references)
- `README.md` - Project overview, usage instructions, explanations
- `replit.md` - This file (project memory/architecture)

### Data Files (Generated)
- `final_dataset.csv` - Main dataset (190 zip codes, 11 variables, REAL data)
- `simulated_twitter_data.csv` - Simulated tweets (25,552 records)
- `analysis_results.json` - Core information theory results
- `twitter_analysis_results.json` - Twitter analysis metrics
- `borough_entropy.csv` - Shannon entropy by borough
- `kl_divergence.csv` - Borough divergence values
- `complete_analysis_visualizations.png` - 7-panel comprehensive visualization

### Raw Data
- `data_raw_stores.json` - Raw supermarket data from NY State API

## Data Sources

### ✅ REAL DATA
1. **NYC Supermarkets:** NY State Dept of Agriculture & Markets (11,472 stores)
2. **Population:** US Census Bureau ACS 2021 (184/190 zip codes)
3. **Median Income:** US Census Bureau ACS 2021 (178/190 zip codes)

### ⚠️ SIMULATED DATA
- **Twitter/X:** Simulated (25,552 tweets) due to API cost ($5,000/month)

## Technical Architecture

### Application Type
Standalone Python analysis scripts - no web interface, no database, no deployment needed.

### Core Dependencies
- pandas, numpy, scipy (data analysis)
- matplotlib, seaborn (visualization)
- requests (API data collection)

### No External Services
- No database connections
- No authentication systems
- No cloud services
- Self-contained local analysis

## Project Status

✅ **Complete and Publication-Ready**
- All real data collected successfully
- All information theory measures calculated correctly
- Comprehensive visualizations generated
- Academic report with proper citations complete
- All documentation updated
- Ready for SSIE-500 submission

## Notes for Future Sessions

- Census API requires individual zip code queries (bulk state filter causes 400 errors)
- Twitter Academic Research API discontinued March 2023
- Project uses 4 information theory measures (Shannon, MI, KL, Conditional)
- Transfer Entropy removed per user request (November 12, 2025)

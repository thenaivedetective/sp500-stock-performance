# S&P 500 Stock Outperformer Prediction

Predicts whether an S&P 500 stock will outperform the index in the next quarter using logistic regression, PCA, and gradient boosting — trained on 15 years of WRDS financial data (Q1 2010 – Q4 2024).

Based on the methodology of **Ananthakumar & Sarkar (2017)**: *Using Logistic Regression to Determine U.S. Equity Performance.*

---

## Overview

The model takes quarterly fundamental ratios (profitability, leverage, growth, valuation) and macroeconomic indicators as inputs and outputs a binary prediction: will this stock beat the S&P 500 next quarter?

Key design decisions:
- **VIF screening** (cutoff 2.5) removes multicollinear predictors before modeling
- **PCA** reduces the 12 retained predictors to 8 components explaining ≥80% of variance
- **Logistic regression** (statsmodels) is the primary interpretable model
- **Gradient Boosting** (sklearn) is the secondary model for comparison
- Models are trained and validated **separately by market cap tier** (Large, Mid, Small)

---

## Results

| Segment   | AUC   | Accuracy |
|-----------|-------|----------|
| Large Cap | 0.71  | 65.3%    |
| Mid Cap   | 0.68  | 63.1%    |
| Small Cap | 0.66  | 61.8%    |

2025 forward validation (Q1–Q4) shows consistent outperformance vs. a random baseline.

---

## Data Sources

All data pulled via **WRDS (Wharton Research Data Services)**:

| File | Source | Contents |
|------|--------|----------|
| `wrds_compustat_quarterly.csv` | Compustat | Quarterly fundamentals (ROA, ROE, margins, ratios) |
| `wrds_crsp_quarterly.csv` | CRSP | Monthly stock returns, market cap |
| `wrds_fred_macro.csv` | FRED via WRDS | GDP growth, CPI inflation |
| `wrds_gics_sectors.csv` | Compustat | GICS sector classifications |
| `wrds_sp500_history.csv` | CRSP | Historical S&P 500 constituent list |

---

## Project Structure

```
├── app.py                        # Main pipeline runner (Steps 1–7)
│
├── Data Pull
│   ├── pull_sp500_history.py     # Step 1 — S&P 500 constituents
│   ├── pull_compustat.py         # Step 2 — Compustat financials
│   ├── pull_crsp.py              # Step 3 — CRSP returns
│   ├── pull_fred_macro.py        # Step 4 — FRED macro data
│   └── pull_gics.py              # Step 5 — GICS sector codes
│
├── Analysis
│   ├── preliminary_analysis.py   # Step 6 — Global logistic regression
│   ├── market_cap_analysis.py    # Step 7 — By market cap segment
│   ├── advanced_analysis.py      # VIF + PCA + full model pipeline
│   ├── delta_analysis.py         # Quarter-over-quarter delta features
│   └── sector_model_portfolio_2025.py  # Sector-level 2025 predictions
│
├── Validation
│   ├── validation_global_model.py
│   ├── validation_wrds_delta.py
│   ├── validation_yfinance.py
│   └── validation_edgar.py
│
├── Outputs
│   ├── viz/                      # Charts (ROC, PCA scree, confusion matrix, etc.)
│   ├── results_advanced.txt      # Full model output log
│   ├── predictions_2025.csv      # 2025 stock predictions
│   └── SP500_Outperformer_Prediction.pdf  # Full written report
│
└── Presentation
    ├── Final_Presentation_Fixed.pptx
    └── Final_Presentation_Video.mp4
```

---

## Predictors Used

After VIF screening (12 of 14 retained):

| Category | Predictors |
|---|---|
| Profitability | Return on Assets (ROA), Gross Profit Margin, Operating Margin |
| Efficiency | Asset Turnover |
| Liquidity | Current Ratio |
| Leverage | Debt-to-Equity |
| Growth | Revenue Growth (QoQ), Net Income Growth (QoQ) |
| Valuation | P/E Ratio, Book-to-Market |
| Macro | GDP Growth (Quarterly), CPI Inflation (Quarterly) |

Removed due to multicollinearity (VIF > 2.5): Return on Equity (ROE), Net Profit Margin.

---

## Setup

### Requirements

```bash
pip install pandas numpy scikit-learn statsmodels tabulate reportlab python-docx
```

### WRDS Credentials

Set these environment variables before running:

```
WRDS_USERNAME=your_username
WRDS_PASSWORD=your_password
```

### Run

```bash
python app.py
```

This runs the full pipeline: data pull → cleaning → modeling → output.

---

## Paper

Full academic paper: [`SP500_Technical_Report_LanaGidan.docx`](SP500_Technical_Report_LanaGidan.docx)

Reference: Ananthakumar, U., & Sarkar, S. (2017). *Using Logistic Regression to Determine U.S. Equity Performance.* Journal of Accounting and Finance.

---



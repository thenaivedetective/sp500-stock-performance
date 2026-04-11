"""
Pull quarterly financial data for S&P 500 companies from SEC EDGAR.
Source: https://data.sec.gov  (no API key required — public government data)

What this script does:
  1. Downloads the SEC master ticker → CIK mapping
  2. Gets the current S&P 500 constituent list from Wikipedia
  3. For each company, calls SEC EDGAR's XBRL company-facts API
  4. Extracts quarterly Income Statement, Balance Sheet, and Cash Flow items
  5. Saves a clean CSV of quarterly financial data

Output: sp500_quarterly_financials.csv
"""

import requests, time, json, re
import pandas as pd
import numpy as np
from datetime import datetime

# ── headers (SEC requires a User-Agent identifying your app) ──────
HEADERS = {
    "User-Agent": "BinghamtonUniversity SSIE lana.gidan@binghamton.edu",
    "Accept-Encoding": "gzip, deflate",
    "Host": "data.sec.gov",
}

# ─────────────────────────────────────────────────────────────────
# STEP 1: Download SEC ticker → CIK mapping
# ─────────────────────────────────────────────────────────────────
print("Step 1: Downloading SEC ticker → CIK mapping...")
url = "https://www.sec.gov/files/company_tickers.json"
resp = requests.get(url, headers={
    "User-Agent": "BinghamtonUniversity SSIE lana.gidan@binghamton.edu"
})
tickers_json = resp.json()

# Build a ticker → CIK dict (CIK padded to 10 digits)
ticker_to_cik = {}
for entry in tickers_json.values():
    tk  = entry["ticker"].upper()
    cik = str(entry["cik_str"]).zfill(10)
    ticker_to_cik[tk] = cik
print(f"  Loaded {len(ticker_to_cik):,} SEC-registered tickers.")

# ─────────────────────────────────────────────────────────────────
# STEP 2: Load S&P 500 tickers from existing CSV (already collected)
# ─────────────────────────────────────────────────────────────────
print("\nStep 2: Loading S&P 500 tickers from sp500_financial_data.csv...")
existing = pd.read_csv("sp500_financial_data.csv")
sp500_tickers = existing["ticker"].tolist()
sp500_sectors = dict(zip(existing["ticker"], existing["sector"]))
sp500_names   = dict(zip(existing["ticker"], existing["ticker"]))
print(f"  Loaded {len(sp500_tickers)} tickers.")

# ─────────────────────────────────────────────────────────────────
# STEP 3: Define the financial concepts to extract
#         SEC XBRL uses US-GAAP concept names — we list fallbacks
#         because different companies report under slightly different names
# ─────────────────────────────────────────────────────────────────

CONCEPTS = {
    # ── Income Statement ──────────────────────────────────────────
    "Revenue": [
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "Revenues",
        "SalesRevenueNet",
        "RevenueFromContractWithCustomerIncludingAssessedTax",
        "SalesRevenueGoodsNet",
        "RevenueFromRelatedParties",
    ],
    "NetIncome": [
        "NetIncomeLoss",
        "NetIncomeLossAvailableToCommonStockholdersBasic",
        "ProfitLoss",
    ],
    "OperatingIncome": [
        "OperatingIncomeLoss",
    ],
    "EBITDA_proxy": [
        "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
    ],
    "EPS_Basic": [
        "EarningsPerShareBasic",
    ],
    "EPS_Diluted": [
        "EarningsPerShareDiluted",
    ],
    "GrossProfit": [
        "GrossProfit",
    ],
    "CostOfRevenue": [
        "CostOfRevenue",
        "CostOfGoodsAndServicesSold",
        "CostOfGoodsSold",
    ],
    "OperatingExpenses": [
        "OperatingExpenses",
    ],
    "InterestExpense": [
        "InterestExpense",
        "InterestExpenseDebt",
    ],
    "IncomeTax": [
        "IncomeTaxExpenseBenefit",
    ],
    # ── Balance Sheet ─────────────────────────────────────────────
    "TotalAssets": [
        "Assets",
    ],
    "TotalLiabilities": [
        "Liabilities",
    ],
    "StockholdersEquity": [
        "StockholdersEquity",
        "StockholdersEquityAttributableToParent",
    ],
    "CurrentAssets": [
        "AssetsCurrent",
    ],
    "CurrentLiabilities": [
        "LiabilitiesCurrent",
    ],
    "CashAndEquivalents": [
        "CashAndCashEquivalentsAtCarryingValue",
        "CashCashEquivalentsAndShortTermInvestments",
    ],
    "LongTermDebt": [
        "LongTermDebt",
        "LongTermDebtNoncurrent",
        "LongTermDebtAndCapitalLeaseObligations",
    ],
    "ShortTermDebt": [
        "ShortTermBorrowings",
        "DebtCurrent",
    ],
    "Inventory": [
        "InventoryNet",
    ],
    "AccountsReceivable": [
        "AccountsReceivableNetCurrent",
    ],
    "Goodwill": [
        "Goodwill",
    ],
    "SharesOutstanding": [
        "CommonStockSharesOutstanding",
    ],
    # ── Cash Flow ─────────────────────────────────────────────────
    "OperatingCashFlow": [
        "NetCashProvidedByUsedInOperatingActivities",
    ],
    "CapEx": [
        "PaymentsToAcquirePropertyPlantAndEquipment",
        "CapitalExpendituresIncurredButNotYetPaid",
    ],
    "FreeCashFlow_proxy": [
        "NetCashProvidedByUsedInOperatingActivities",  # will subtract CapEx later
    ],
    "DividendsPaid": [
        "PaymentsOfDividendsCommonStock",
        "PaymentsOfDividends",
    ],
    "ShareRepurchases": [
        "PaymentsForRepurchaseOfCommonStock",
    ],
}

# ─────────────────────────────────────────────────────────────────
# STEP 4: Helper — extract a single concept from company facts JSON
# ─────────────────────────────────────────────────────────────────
def extract_concept(facts_json, concept_list, start_date="2018-01-01"):
    """
    Try each concept name in order; return a DataFrame with columns:
    [end, val, form] for quarterly (10-Q) and annual (10-K) filings.
    """
    us_gaap = facts_json.get("facts", {}).get("us-gaap", {})
    for concept in concept_list:
        if concept in us_gaap:
            units = us_gaap[concept].get("units", {})
            # look for USD or shares
            for unit_type in ["USD", "shares", "USD/shares"]:
                if unit_type in units:
                    records = units[unit_type]
                    rows = []
                    for rec in records:
                        form = rec.get("form", "")
                        if form not in ("10-Q", "10-K"):
                            continue
                        end = rec.get("end", "")
                        if end < start_date:
                            continue
                        val = rec.get("val", np.nan)
                        fp  = rec.get("fp", "")   # Q1/Q2/Q3/Q4/FY
                        rows.append({
                            "end":    end,
                            "val":    val,
                            "form":   form,
                            "fp":     fp,
                            "concept": concept,
                        })
                    if rows:
                        df = pd.DataFrame(rows)
                        df["end"] = pd.to_datetime(df["end"])
                        df = df.sort_values("end").drop_duplicates(
                            subset=["end", "fp"], keep="last"
                        )
                        return df
    return pd.DataFrame()

# ─────────────────────────────────────────────────────────────────
# STEP 5: Pull data for each S&P 500 company
# ─────────────────────────────────────────────────────────────────
print(f"\nStep 3: Pulling quarterly data from SEC EDGAR for S&P 500 companies...")
print("  (this will take several minutes — SEC rate limit: 10 req/sec)\n")

START_DATE = "2019-01-01"   # pull from Q1 2019 onward
all_records = []
failed = []

for idx, ticker in enumerate(sp500_tickers):
    cik = ticker_to_cik.get(ticker)
    if cik is None:
        # try without hyphen (e.g., BRK-B → BRKB)
        alt = ticker.replace("-", "")
        cik = ticker_to_cik.get(alt)
    if cik is None:
        failed.append((ticker, "CIK not found"))
        continue

    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code != 200:
            failed.append((ticker, f"HTTP {r.status_code}"))
            time.sleep(0.2)
            continue
        facts = r.json()
    except Exception as e:
        failed.append((ticker, str(e)))
        time.sleep(0.5)
        continue

    # Extract each concept
    company_dfs = {}
    for col_name, concept_list in CONCEPTS.items():
        df_concept = extract_concept(facts, concept_list, start_date=START_DATE)
        if not df_concept.empty:
            # Keep only quarterly rows (10-Q) for quarterly analysis
            # Also keep 10-K Q4 data
            df_q = df_concept[df_concept["form"].isin(["10-Q", "10-K"])].copy()
            df_q = df_q[["end", "val"]].rename(columns={"val": col_name})
            df_q = df_q.drop_duplicates(subset="end", keep="last")
            company_dfs[col_name] = df_q

    if not company_dfs:
        failed.append((ticker, "No financial data found"))
        time.sleep(0.15)
        continue

    # Merge all concepts on the 'end' date (quarter end date)
    merged = None
    for col_name, df_c in company_dfs.items():
        if merged is None:
            merged = df_c
        else:
            merged = pd.merge(merged, df_c, on="end", how="outer")

    if merged is not None and not merged.empty:
        merged["ticker"]   = ticker
        merged["company"]  = sp500_names.get(ticker, ticker)
        merged["sector"]   = sp500_sectors.get(ticker, "Unknown")
        merged["cik"]      = cik
        # Extract year and quarter from end date
        merged["year"]     = merged["end"].dt.year
        merged["month"]    = merged["end"].dt.month
        merged["quarter"]  = merged["end"].dt.quarter
        merged["period"]   = merged["end"].dt.to_period("Q").astype(str)
        all_records.append(merged)

    # Progress update every 25 companies
    if (idx + 1) % 25 == 0:
        print(f"  Processed {idx+1}/{len(sp500_tickers)} companies "
              f"({len(all_records)} with data, {len(failed)} failed)...")

    # Respect SEC rate limit (max 10 requests/second)
    time.sleep(0.12)

# ─────────────────────────────────────────────────────────────────
# STEP 6: Combine and clean
# ─────────────────────────────────────────────────────────────────
print(f"\nStep 4: Combining data from {len(all_records)} companies...")
if not all_records:
    print("ERROR: No data was retrieved. Check internet connection.")
    exit(1)

df_all = pd.concat(all_records, ignore_index=True)

# Filter to 2019 onward
df_all = df_all[df_all["year"] >= 2019].copy()

# Sort
df_all = df_all.sort_values(["ticker", "end"]).reset_index(drop=True)

# Compute derived ratios (where base data exists)
# Current Ratio = CurrentAssets / CurrentLiabilities
if "CurrentAssets" in df_all.columns and "CurrentLiabilities" in df_all.columns:
    df_all["CurrentRatio"] = df_all["CurrentAssets"] / df_all["CurrentLiabilities"].replace(0, np.nan)

# Debt-to-Equity = (LongTermDebt + ShortTermDebt) / StockholdersEquity
if all(c in df_all.columns for c in ["LongTermDebt","ShortTermDebt","StockholdersEquity"]):
    df_all["TotalDebt"] = df_all["LongTermDebt"].fillna(0) + df_all["ShortTermDebt"].fillna(0)
    df_all["DebtToEquity"] = df_all["TotalDebt"] / df_all["StockholdersEquity"].replace(0, np.nan)

# Profit Margin = NetIncome / Revenue
if "NetIncome" in df_all.columns and "Revenue" in df_all.columns:
    df_all["ProfitMargin"] = df_all["NetIncome"] / df_all["Revenue"].replace(0, np.nan)

# Gross Margin = GrossProfit / Revenue
if "GrossProfit" in df_all.columns and "Revenue" in df_all.columns:
    df_all["GrossMargin"] = df_all["GrossProfit"] / df_all["Revenue"].replace(0, np.nan)

# Operating Margin = OperatingIncome / Revenue
if "OperatingIncome" in df_all.columns and "Revenue" in df_all.columns:
    df_all["OperatingMargin"] = df_all["OperatingIncome"] / df_all["Revenue"].replace(0, np.nan)

# ROA = NetIncome / TotalAssets
if "NetIncome" in df_all.columns and "TotalAssets" in df_all.columns:
    df_all["ROA"] = df_all["NetIncome"] / df_all["TotalAssets"].replace(0, np.nan)

# ROE = NetIncome / StockholdersEquity
if "NetIncome" in df_all.columns and "StockholdersEquity" in df_all.columns:
    df_all["ROE"] = df_all["NetIncome"] / df_all["StockholdersEquity"].replace(0, np.nan)

# Debt Ratio = TotalLiabilities / TotalAssets
if "TotalLiabilities" in df_all.columns and "TotalAssets" in df_all.columns:
    df_all["DebtRatio"] = df_all["TotalLiabilities"] / df_all["TotalAssets"].replace(0, np.nan)

# Free Cash Flow = OperatingCashFlow - CapEx
if "OperatingCashFlow" in df_all.columns and "CapEx" in df_all.columns:
    df_all["FreeCashFlow"] = df_all["OperatingCashFlow"] - df_all["CapEx"].fillna(0)

# Reorder columns — identifiers first
id_cols  = ["ticker","company","sector","cik","period","year","quarter","month","end"]
fin_cols = [c for c in df_all.columns if c not in id_cols]
df_all   = df_all[id_cols + fin_cols]

# ─────────────────────────────────────────────────────────────────
# STEP 7: Save
# ─────────────────────────────────────────────────────────────────
out_file = "sp500_quarterly_financials.csv"
df_all.to_csv(out_file, index=False)

print(f"\n{'='*60}")
print(f"DONE — Saved: {out_file}")
print(f"{'='*60}")
print(f"  Rows (company-quarters): {len(df_all):,}")
print(f"  Unique companies:        {df_all['ticker'].nunique()}")
print(f"  Columns:                 {len(df_all.columns)}")
print(f"  Date range:              {df_all['end'].min().date()} → {df_all['end'].max().date()}")
print(f"  Companies failed:        {len(failed)}")
if failed[:5]:
    print(f"  Sample failures:         {failed[:5]}")
print(f"\nColumn list:")
for c in df_all.columns:
    non_null = df_all[c].notna().sum()
    print(f"  {c:<30} {non_null:>6} non-null values")

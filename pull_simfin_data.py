"""
Pull quarterly financial data for S&P 500 companies from SimFin.
Pulls: Income Statements, Balance Sheets, Cash Flow Statements (quarterly)
Output: simfin_quarterly_financials.csv
"""

import simfin as sf
from simfin.names import *
import pandas as pd
import numpy as np
import os, warnings
warnings.filterwarnings("ignore")

# ── Setup ─────────────────────────────────────────────────────────
API_KEY = os.environ.get("SIMFIN_API_KEY", "")
if not API_KEY:
    raise ValueError("SIMFIN_API_KEY secret not found.")

sf.set_api_key(API_KEY)
sf.set_data_dir("simfin_data")

print("=" * 60)
print("SimFin Quarterly Data Pull — S&P 500")
print("=" * 60)

# ── Step 1: Load company list ─────────────────────────────────────
print("\nStep 1: Loading company list...")
companies = sf.load_companies(market="us")
print(f"  Total US companies in SimFin: {len(companies):,}")

# ── Step 2: Load S&P 500 tickers from existing CSV ────────────────
print("\nStep 2: Loading S&P 500 tickers from existing data...")
existing = pd.read_csv("sp500_financial_data.csv")
sp500_tickers = existing["ticker"].tolist()
sp500_sectors = dict(zip(existing["ticker"], existing["sector"]))
print(f"  S&P 500 tickers to fetch: {len(sp500_tickers)}")

# ── Step 3: Pull quarterly financials ─────────────────────────────
print("\nStep 3: Downloading quarterly financial statements from SimFin...")
print("  (Income Statement, Balance Sheet, Cash Flow — this may take a minute)\n")

# Income Statement — quarterly
print("  Fetching Income Statements (quarterly)...")
income = sf.load_income(variant="quarterly", market="us")
print(f"    Rows: {len(income):,}")

# Balance Sheet — quarterly
print("  Fetching Balance Sheets (quarterly)...")
balance = sf.load_balance(variant="quarterly", market="us")
print(f"    Rows: {len(balance):,}")

# Cash Flow — quarterly
print("  Fetching Cash Flow Statements (quarterly)...")
cashflow = sf.load_cashflow(variant="quarterly", market="us")
print(f"    Rows: {len(cashflow):,}")

# Share prices for return calculation
print("  Fetching Share Prices (for return calculation)...")
prices = sf.load_shareprices(variant="daily", market="us")
print(f"    Rows: {len(prices):,}")

# ── Step 4: Filter to S&P 500 tickers ────────────────────────────
print("\nStep 4: Filtering to S&P 500 tickers...")

def filter_sp500(df, tickers):
    if df.index.names[0] == "Ticker":
        return df[df.index.get_level_values("Ticker").isin(tickers)]
    elif "Ticker" in df.columns:
        return df[df["Ticker"].isin(tickers)]
    return df

income_sp  = filter_sp500(income,   sp500_tickers)
balance_sp = filter_sp500(balance,  sp500_tickers)
cashflow_sp= filter_sp500(cashflow, sp500_tickers)
prices_sp  = filter_sp500(prices,   sp500_tickers)

print(f"  Income rows (S&P 500):   {len(income_sp):,}")
print(f"  Balance rows (S&P 500):  {len(balance_sp):,}")
print(f"  CashFlow rows (S&P 500): {len(cashflow_sp):,}")
print(f"  Price rows (S&P 500):    {len(prices_sp):,}")

# ── Step 5: Reset index and standardize ───────────────────────────
print("\nStep 5: Standardizing and merging statements...")

def reset_and_clean(df, prefix=""):
    df = df.reset_index()
    # Rename columns: strip whitespace
    df.columns = [c.strip() for c in df.columns]
    # Keep key identifier columns + financial columns
    id_cols = ["Ticker","SimFinId","Currency","Fiscal Year","Fiscal Period",
                "Report Date","Publish Date","Restated Date"]
    id_cols = [c for c in id_cols if c in df.columns]
    fin_cols = [c for c in df.columns if c not in id_cols]
    # Add prefix to financial columns to avoid clashes
    if prefix:
        df = df.rename(columns={c: f"{prefix}_{c}" for c in fin_cols})
    return df, id_cols

income_df,  _ = reset_and_clean(income_sp,   "IS")
balance_df, _ = reset_and_clean(balance_sp,  "BS")
cashflow_df,_ = reset_and_clean(cashflow_sp, "CF")

# Merge on Ticker + Fiscal Year + Fiscal Period
merge_keys = ["Ticker", "Fiscal Year", "Fiscal Period"]

# Keep only merge keys + financial columns
def keep_cols(df, prefix):
    keep = [c for c in df.columns
            if c in merge_keys or c.startswith(prefix)]
    return df[keep]

income_m   = keep_cols(income_df,   "IS")
balance_m  = keep_cols(balance_df,  "BS")
cashflow_m = keep_cols(cashflow_df, "CF")

# Also keep Report Date from income statement
if "Report Date" in income_df.columns:
    income_m = income_df[
        [c for c in income_df.columns
         if c in merge_keys or c.startswith("IS") or c == "Report Date"]
    ]

merged = income_m.merge(balance_m,  on=merge_keys, how="outer")
merged = merged.merge(cashflow_m,   on=merge_keys, how="outer")

print(f"  Merged rows: {len(merged):,}  |  Columns: {len(merged.columns)}")

# ── Step 6: Filter to 2019 onward ────────────────────────────────
merged["Fiscal Year"] = pd.to_numeric(merged["Fiscal Year"], errors="coerce")
merged = merged[merged["Fiscal Year"] >= 2019].copy()
print(f"  After 2019 filter: {len(merged):,} rows")

# ── Step 7: Compute quarterly stock returns ───────────────────────
print("\nStep 6: Computing quarterly stock returns from price data...")

prices_df = prices_sp.reset_index(drop=False)
# Drop duplicate columns before stripping names
prices_df = prices_df.loc[:, ~prices_df.columns.duplicated()]
prices_df.columns = [c.strip() for c in prices_df.columns]
prices_df = prices_df.loc[:, ~prices_df.columns.duplicated()]

# Use Adjusted Close (accounts for dividends/splits)
close_col = "Adj. Close" if "Adj. Close" in prices_df.columns else "Close"
if "Date" not in prices_df.columns:
    prices_df = prices_df.reset_index()
prices_df["Date"] = pd.to_datetime(prices_df["Date"])
prices_df = prices_df[["Ticker", "Date", close_col]].dropna()
prices_df = prices_df.sort_values(["Ticker", "Date"])

# Get last price of each quarter — add a named period column first
prices_df["qperiod"] = prices_df["Date"].dt.to_period("Q")
# Take last date per (Ticker, quarter)
quarterly_prices = (
    prices_df.groupby(["Ticker", "qperiod"], as_index=False)
    .last()[["Ticker", "qperiod", "Date", close_col]]
    .rename(columns={"Date": "price_date", close_col: "price_close",
                     "qperiod": "period_str"})
)
quarterly_prices["period_str"] = quarterly_prices["period_str"].astype(str)

# Quarterly return = (price_t - price_{t-1}) / price_{t-1}
quarterly_prices = quarterly_prices.sort_values(["Ticker","price_date"])
quarterly_prices["quarterly_return"] = (
    quarterly_prices.groupby("Ticker")["price_close"].pct_change()
)

# Also compute 4-quarter (annual) return for the outperformer label
quarterly_prices["annual_return"] = (
    quarterly_prices.groupby("Ticker")["price_close"].pct_change(4)
)

print(f"  Quarterly price records: {len(quarterly_prices):,}")

# ── Step 8: Get SPY benchmark returns ────────────────────────────
print("  Fetching SPY benchmark returns...")
try:
    import yfinance as yf
    spy_raw = yf.download("SPY", start="2019-01-01", end="2026-01-01",
                          auto_adjust=True, progress=False)
    # Handle both single and multi-level column DataFrames
    if isinstance(spy_raw.columns, pd.MultiIndex):
        spy_raw.columns = spy_raw.columns.get_level_values(0)
    spy = spy_raw["Close"].squeeze()   # ensure Series
    spy.index = pd.to_datetime(spy.index)

    # Quarterly return
    spy_q = spy.resample("Q").last().pct_change().dropna()
    spy_q_dict = {str(pd.Period(d, "Q")): float(v)
                  for d, v in spy_q.items()}
    quarterly_prices["spy_quarterly_return"] = (
        quarterly_prices["period_str"].map(spy_q_dict)
    )
    quarterly_prices["outperformer_quarterly"] = (
        quarterly_prices["quarterly_return"] >
        quarterly_prices["spy_quarterly_return"]
    ).astype(int)

    # Annual (4-quarter) return
    spy_a = spy.resample("Q").last().pct_change(4).dropna()
    spy_a_dict = {str(pd.Period(d, "Q")): float(v)
                  for d, v in spy_a.items()}
    quarterly_prices["spy_annual_return"] = (
        quarterly_prices["period_str"].map(spy_a_dict)
    )
    quarterly_prices["outperformer_annual"] = (
        quarterly_prices["annual_return"] >
        quarterly_prices["spy_annual_return"]
    ).astype(int)
    print("  SPY benchmark returns computed.")
except Exception as e:
    print(f"  SPY fetch failed: {e} — adding empty benchmark columns")
    for col in ["spy_quarterly_return","spy_annual_return",
                "outperformer_quarterly","outperformer_annual"]:
        quarterly_prices[col] = np.nan

# ── Step 9: Merge financials with returns ────────────────────────
print("\nStep 7: Merging financials with quarterly returns...")

# Map fiscal period to calendar quarter
fp_map = {"Q1":"Q1","Q2":"Q2","Q3":"Q3","Q4":"Q4"}
merged["fp_label"] = merged["Fiscal Period"].map(fp_map)
merged["period_str"] = (
    merged["Fiscal Year"].astype(str) + "Q" +
    merged["fp_label"].str.replace("Q","")
)

ret_cols = ["Ticker","period_str","price_close","quarterly_return","annual_return",
            "spy_quarterly_return","spy_annual_return",
            "outperformer_quarterly","outperformer_annual"]
ret_cols = [c for c in ret_cols if c in quarterly_prices.columns]
final = merged.merge(
    quarterly_prices[ret_cols],
    on=["Ticker","period_str"],
    how="left"
)

# Add sector
final["Sector"] = final["Ticker"].map(sp500_sectors)

# ── Step 10: Clean column names ───────────────────────────────────
# Remove prefix for readability
def clean_col(c):
    for prefix in ["IS_","BS_","CF_"]:
        if c.startswith(prefix):
            return c[len(prefix):]
    return c

final.columns = [clean_col(c) for c in final.columns]

# Remove duplicate columns
final = final.loc[:, ~final.columns.duplicated()]

# Sort
final = final.sort_values(["Ticker","Fiscal Year","Fiscal Period"]).reset_index(drop=True)

# ── Step 11: Save ─────────────────────────────────────────────────
out = "simfin_quarterly_financials.csv"
final.to_csv(out, index=False)

print(f"\n{'='*60}")
print(f"SAVED: {out}")
print(f"{'='*60}")
print(f"  Rows (company-quarters): {len(final):,}")
print(f"  Unique tickers:          {final['Ticker'].nunique()}")
print(f"  Columns:                 {len(final.columns)}")
print(f"  Fiscal years covered:    {sorted(final['Fiscal Year'].dropna().unique().astype(int).tolist())}")
if "outperformer_quarterly" in final.columns:
    vc = final["outperformer_quarterly"].value_counts()
    print(f"  Outperformers (quarterly): {vc.get(1,0):,}  |  Underperformers: {vc.get(0,0):,}")
print(f"\nColumn list:")
for c in final.columns:
    nn = final[c].notna().sum()
    print(f"  {c:<45} {nn:>5} non-null")

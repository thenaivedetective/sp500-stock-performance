 

import yfinance as yf
import pandas as pd
import numpy as np
import json
import warnings
warnings.filterwarnings("ignore")


UNIVERSE = {
    "Information Technology": [
        "AAPL","MSFT","NVDA","AVGO","ORCL","CRM","AMD","INTC","QCOM","TXN"],
    "Health Care": [
        "UNH","JNJ","LLY","ABBV","MRK","TMO","ABT","DHR","BMY","AMGN"],
    "Financials": [
        "BRK-B","JPM","V","MA","BAC","WFC","GS","MS","BLK","AXP"],
    "Consumer Discretionary": [
        "AMZN","TSLA","HD","MCD","NKE","LOW","SBUX","TGT","BKNG","CMG"],
    "Communication Services": [
        "GOOGL","META","NFLX","DIS","CMCSA","T","VZ","TMUS","ATVI","EA"],
    "Industrials": [
        "CAT","DE","UPS","HON","RTX","LMT","GE","MMM","FDX","BA"],
    "Consumer Staples": [
        "PG","KO","PEP","WMT","COST","PM","MO","CL","GIS","K"],
    "Energy": [
        "XOM","CVX","COP","SLB","EOG","PSX","VLO","MPC","OXY","HAL"],
    "Utilities": [
        "NEE","DUK","SO","D","AEP","EXC","SRE","XEL","ED","WEC"],
    "Real Estate": [
        "PLD","AMT","EQIX","CCI","SPG","O","PSA","WELL","AVB","EQR"],
    "Materials": [
        "LIN","APD","SHW","FCX","NEM","NUE","DOW","PPG","VMC","MLM"],
}

all_tickers = []
sectors = {}
for sector, tickers in UNIVERSE.items():
    for t in tickers:
        all_tickers.append(t)
        sectors[t] = sector

sample_tickers = all_tickers  
print(f"Universe: {len(sample_tickers)} tickers across {len(UNIVERSE)} sectors")


RATIO_FIELDS = {
    
    "pe_ratio":           "trailingPE",
    "forward_pe":         "forwardPE",
    "price_to_book":      "priceToBook",
    "price_to_sales":     "priceToSalesTrailing12Months",
    "ev_to_ebitda":       "enterpriseToEbitda",
    
    "roe":                "returnOnEquity",
    "roa":                "returnOnAssets",
    "gross_margin":       "grossMargins",
    "operating_margin":   "operatingMargins",
    "net_margin":         "profitMargins",
    
    "debt_to_equity":     "debtToEquity",
    "total_debt":         "totalDebt",
    
    "current_ratio":      "currentRatio",
    "quick_ratio":        "quickRatio",
    
    "revenue_growth":     "revenueGrowth",
    "earnings_growth":    "earningsGrowth",
    
    "eps_trailing":       "trailingEps",
    "eps_forward":        "forwardEps",
    "market_cap":         "marketCap",
    "beta":               "beta",
    
    "dividend_yield":     "dividendYield",
}

print(f"\nFetching fundamentals + 1-year prices for {len(sample_tickers)} tickers...")
print("(This takes ~60 seconds)\n")

rows = []
for i, ticker in enumerate(sample_tickers, 1):
    try:
        t    = yf.Ticker(ticker)
        info = t.info

        row = {"ticker": ticker, "sector": sectors.get(ticker, "Unknown")}

        
        for col, key in RATIO_FIELDS.items():
            val = info.get(key)
            row[col] = round(float(val), 4) if val is not None else np.nan

        
        row["name"] = info.get("shortName", ticker)

        rows.append(row)
        print(f"  [{i:3d}/{len(sample_tickers)}] {ticker:8s}  PE={row.get('pe_ratio','—')}"
              f"  ROE={row.get('roe','—')}  Mkt Cap={row.get('market_cap','—')}")

    except Exception as e:
        print(f"  [{i:3d}/{len(sample_tickers)}] {ticker:8s}  SKIP ({e})")

df = pd.DataFrame(rows)


print("\nFetching 1-year price history for return calculation...")


spy  = yf.download("SPY", period="1y", progress=False)
spy_ret = float((spy["Close"].iloc[-1] / spy["Close"].iloc[0]) - 1)
print(f"  SPY (index) 1-year return: {spy_ret*100:.2f}%")

returns = {}
valid_tickers = df["ticker"].tolist()

prices = yf.download(valid_tickers, period="1y",
                     auto_adjust=True, progress=False)["Close"]

for ticker in valid_tickers:
    if ticker in prices.columns:
        series = prices[ticker].dropna()
        if len(series) >= 2:
            r = (series.iloc[-1] / series.iloc[0]) - 1
            returns[ticker] = round(float(r), 4)

df["return_1y"]   = df["ticker"].map(returns)
df["spy_return"]  = spy_ret

df["outperformer"] = (df["return_1y"] > spy_ret).astype(int)


out_csv  = "sp500_financial_data.csv"
out_json = "sp500_fetch_summary.json"

df.to_csv(out_csv, index=False)

summary = {
    "tickers_attempted":   len(sample_tickers),
    "tickers_with_data":   int(df["ticker"].count()),
    "tickers_with_return": int(df["return_1y"].notna().sum()),
    "outperformers":       int(df["outperformer"].sum()),
    "underperformers":     int((df["outperformer"] == 0).sum()),
    "spy_return_1y_pct":   round(spy_ret * 100, 2),
    "columns":             df.columns.tolist(),
    "sectors":             df["sector"].value_counts().to_dict(),
}
with open(out_json, "w") as f:
    json.dump(summary, f, indent=2)

print("\n" + "="*65)
print("DATA PULL COMPLETE")
print("="*65)
print(f"  Saved:          {out_csv}")
print(f"  Rows:           {len(df)}")
print(f"  Columns:        {len(df.columns)}  ({', '.join(df.columns[:6])}, ...)")
print(f"  Outperformers:  {summary['outperformers']}  (beat SPY {spy_ret*100:.1f}%)")
print(f"  Underperformers:{summary['underperformers']}")
print(f"\nMissing data % per column:")
miss = (df.isnull().sum() / len(df) * 100).round(1)
print(miss[miss > 0].to_string())
print("\nSample rows:")
print(df[["ticker","sector","pe_ratio","roe","debt_to_equity",
          "return_1y","outperformer"]].head(20).to_string(index=False))

import os
import sys
import subprocess

STEPS = [
    ("STEP 1 — S&P 500 Historical Constituents",  "pull_sp500_history.py",   "wrds_sp500_history.csv"),
    ("STEP 2 — Compustat Quarterly Financials",    "pull_compustat.py",       "wrds_compustat_quarterly.csv"),
    ("STEP 3 — CRSP Monthly Returns",              "pull_crsp.py",            "wrds_crsp_quarterly.csv"),
    ("STEP 4 — FRED Macro Data (GDP + CPI)",       "pull_fred_macro.py",      "wrds_fred_macro.csv"),
    ("STEP 5 — GICS Sector Codes",                 "pull_gics.py",            "wrds_gics_sectors.csv"),
]

ANALYSES = [
    ("STEP 6 — Preliminary Global Analysis",       "preliminary_analysis.py"),
    ("STEP 7 — Market Cap Segmentation Analysis",  "market_cap_analysis.py"),
]

def banner(title):
    print("\n" + "="*65)
    print(f"  {title}")
    print("="*65)

def run_script(script):
    result = subprocess.run(
        [sys.executable, script],
        capture_output=False,
        text=True
    )
    if result.returncode != 0:
        print(f"\n  ERROR: {script} failed with exit code {result.returncode}")
        sys.exit(1)

print("\n" + "="*65)
print("  S&P 500 STOCK OUTPERFORMER PREDICTION")
print("  Multivariate Financial Analysis | Q1 2010 – Q4 2024")
print("  WRDS Account: lanagidan9790")
print("  Reference: Ananthakumar & Sarkar (2017)")
print("="*65)

print("\n── DATA PULL STATUS ──────────────────────────────────────────")
for label, script, csv in STEPS:
    if os.path.exists(csv):
        size = os.path.getsize(csv)
        print(f"  ✓ {label.split('—')[1].strip():<40} (cached: {csv}, {size/1024:.0f} KB)")
    else:
        print(f"  ✗ {label.split('—')[1].strip():<40} (will pull from WRDS)")

for label, script, csv in STEPS:
    banner(label)
    if os.path.exists(csv):
        print(f"  CSV already exists — skipping pull.")
        print(f"  To re-pull fresh data, delete '{csv}' and re-run.")
    else:
        print(f"  Connecting to WRDS and pulling data...")
        run_script(script)

for label, script in ANALYSES:
    banner(label)
    run_script(script)

print("\n" + "="*65)
print("  PIPELINE COMPLETE")
print("="*65 + "\n")

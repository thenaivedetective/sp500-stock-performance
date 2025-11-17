import pandas as pd
import numpy as np
from datetime import datetime

print("="*70)
print("FITBIT DATA EXPLORATION")
print("="*70)

fs1987 = pd.read_csv('FS1987-intraday.csv')
fs2116 = pd.read_csv('FS2116-intraday.csv')

print("\n📊 FS1987 DATA:")
print(f"  Rows: {len(fs1987):,}")
print(f"  Columns: {list(fs1987.columns)}")
print(f"  Date range: {fs1987['fitbit_start_date'].iloc[0]} to {fs1987['fitbit_end_date'].iloc[0]}")
print(f"\n  Sample statistics:")
print(f"    Calories (mean): {fs1987['activities_calories'].mean():.3f}")
print(f"    Calories (std): {fs1987['activities_calories'].std():.3f}")
print(f"    METs (mean): {fs1987['activities_calories_mets'].mean():.3f}")
print(f"    Activity levels: {sorted(fs1987['activities_calories_level'].unique())}")

print("\n📊 FS2116 DATA:")
print(f"  Rows: {len(fs2116):,}")
print(f"  Columns: {list(fs2116.columns)}")
print(f"  Date range: {fs2116['fitbit_start_date'].iloc[0]} to {fs2116['fitbit_end_date'].iloc[0]}")
print(f"\n  Sample statistics:")
print(f"    Calories (mean): {fs2116['activities_calories'].mean():.3f}")
print(f"    Calories (std): {fs2116['activities_calories'].std():.3f}")
print(f"    METs (mean): {fs2116['activities_calories_mets'].mean():.3f}")
print(f"    Activity levels: {sorted(fs2116['activities_calories_level'].unique())}")

print("\n" + "="*70)
print("KEY DATA FEATURES:")
print("="*70)
print("✓ Minute-by-minute calorie expenditure data")
print("✓ METs values (metabolic equivalent)")
print("✓ Activity levels (0 = sedentary, higher = more active)")
print("✓ Two participants over 2+ consecutive weeks")
print("✓ Time series data with temporal patterns")
print("\n" + "="*70)

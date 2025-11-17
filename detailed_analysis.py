import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Load data
fs1987 = pd.read_csv('FS1987-intraday.csv')

# Convert to datetime
fs1987['activity_date'] = pd.to_datetime(fs1987['activity_date'])

# Show detailed structure
print("="*80)
print("DETAILED DATA EXPLANATION")
print("="*80)

print("\n1. DATA STRUCTURE:")
print("-" * 80)
print(fs1987.head(10).to_string())

print("\n\n2. WHAT EACH COLUMN MEANS:")
print("-" * 80)
print("  • participant_id: Unique ID for the person (FS1987 or FS2116)")
print("  • fitbit_start_date: When the study started for this person")
print("  • fitbit_end_date: When the study ended")
print("  • status: Data completeness (all show 'complete')")
print("  • activity_date: EXACT timestamp for this minute")
print("  • activities_calories: Calories burned in THIS MINUTE")
print("  • activities_calories_mets: METs value (metabolic equivalent)")
print("  • activities_calories_level: Activity intensity (0=rest, 1=light, 2=moderate, 3=vigorous)")

print("\n\n3. TIME SERIES STRUCTURE:")
print("-" * 80)
print(f"  Total minutes of data: {len(fs1987):,}")
print(f"  Start: {fs1987['activity_date'].min()}")
print(f"  End: {fs1987['activity_date'].max()}")
print(f"  Duration: {(fs1987['activity_date'].max() - fs1987['activity_date'].min()).days} days")

print("\n\n4. WHAT IS METs?")
print("-" * 80)
print("  METs = Metabolic Equivalent of Task")
print("  • 1 MET = resting metabolism")
print("  • 10 METs = sleeping/resting")
print("  • 15-20 METs = light activity (sitting, standing)")
print("  • 30+ METs = moderate activity (walking)")
print("  • 50+ METs = vigorous activity (running)")
print(f"\n  FS1987 METs range: {fs1987['activities_calories_mets'].min():.1f} to {fs1987['activities_calories_mets'].max():.1f}")

print("\n\n5. ACTIVITY PATTERNS:")
print("-" * 80)
# Group by hour to see patterns
fs1987['hour'] = fs1987['activity_date'].dt.hour
hourly_avg = fs1987.groupby('hour')['activities_calories_mets'].mean()
print("  Average METs by hour of day:")
for hour, mets in hourly_avg.items():
    bar = "█" * int(mets / 2)
    print(f"    {hour:02d}:00 - {mets:5.1f} {bar}")

print("\n\n6. WHAT MAKES THIS TIME SERIES SPECIAL:")
print("-" * 80)
print("  ✓ MINUTE-by-MINUTE resolution (very high granularity)")
print("  ✓ Captures daily rhythms (sleep/wake cycles)")
print("  ✓ Shows activity bursts and rest periods")
print("  ✓ Reflects behavioral patterns over weeks")
print("  ✓ Can be linked to health outcomes (sleep, mood, BMI, etc.)")

print("\n" + "="*80)

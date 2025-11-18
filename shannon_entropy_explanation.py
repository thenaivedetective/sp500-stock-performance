"""
Simple Explanation: How Shannon Entropy Works
Group 2 - SSIE-500 Final Project
"""

import pandas as pd
import math
from collections import Counter

print("="*70)
print("HOW SHANNON ENTROPY WORKS - SIMPLE EXPLANATION")
print("="*70)

# Load one day of real data
df = pd.read_csv('FS1987-intraday.csv')
df['date'] = pd.to_datetime(df['activity_date']).dt.date

# Pick one example day
example_date = df['date'].unique()[10]  # Day 11
day_data = df[df['date'] == example_date].copy()

print(f"\nExample: {example_date}")
print(f"Total minutes in this day: {len(day_data)}")

# STEP 1: Convert METs to Activity Levels
print("\n" + "="*70)
print("STEP 1: Convert METs to Activity Levels")
print("="*70)

def mets_to_level(mets):
    if pd.isna(mets):
        return None
    if mets <= 10:
        return "Resting"
    elif mets <= 15:
        return "Light"
    elif mets <= 30:
        return "Moderate"
    else:
        return "Vigorous"

day_data['activity_level'] = day_data['activities_calories_mets'].apply(mets_to_level)

# Show first 10 minutes
print("\nFirst 10 minutes of this day:")
print("-" * 70)
for i in range(min(10, len(day_data))):
    row = day_data.iloc[i]
    mets = row['activities_calories_mets']
    level = row['activity_level']
    print(f"  Minute {i+1}: METs = {mets:6.2f} → {level}")

# STEP 2: Count how many minutes in each activity level
print("\n" + "="*70)
print("STEP 2: Count Minutes in Each Activity Level")
print("="*70)

activities = [a for a in day_data['activity_level'] if a is not None]
counts = Counter(activities)
total_minutes = len(activities)

print(f"\nTotal valid minutes: {total_minutes}")
print("\nBreakdown:")
for activity in ["Resting", "Light", "Moderate", "Vigorous"]:
    count = counts.get(activity, 0)
    percentage = (count / total_minutes * 100) if total_minutes > 0 else 0
    print(f"  {activity:12s}: {count:5d} minutes ({percentage:5.1f}%)")

# STEP 3: Calculate probability for each activity level
print("\n" + "="*70)
print("STEP 3: Calculate Probabilities")
print("="*70)

probabilities = {}
for activity in ["Resting", "Light", "Moderate", "Vigorous"]:
    count = counts.get(activity, 0)
    p = count / total_minutes if total_minutes > 0 else 0
    probabilities[activity] = p
    print(f"  p({activity:12s}) = {count:5d} / {total_minutes} = {p:.4f}")

# STEP 4: Calculate Shannon Entropy
print("\n" + "="*70)
print("STEP 4: Calculate Shannon Entropy")
print("="*70)

print("\nFormula: H(X) = -Σ p(x) × log₂(p(x))")
print("\nCalculation:")

entropy = 0
for activity in ["Resting", "Light", "Moderate", "Vigorous"]:
    p = probabilities[activity]
    if p > 0:
        term = -p * math.log2(p)
        entropy += term
        print(f"  {activity:12s}: -{p:.4f} × log₂({p:.4f}) = {term:.4f}")
    else:
        print(f"  {activity:12s}: (skipped, p=0)")

print(f"\nTotal Entropy = {entropy:.4f} bits")

# STEP 5: Interpretation
print("\n" + "="*70)
print("STEP 5: What Does This Mean?")
print("="*70)

print(f"\nEntropy = {entropy:.4f} bits")
print(f"Maximum possible = 2.0 bits (all 4 activities equally common)")
print(f"Minimum possible = 0.0 bits (only 1 activity all day)")

if entropy < 0.8:
    interpretation = "LOW variety - Person mostly doing one thing (e.g., sitting all day)"
elif entropy < 1.2:
    interpretation = "MODERATE variety - Some balance between activities"
else:
    interpretation = "HIGH variety - Well-balanced activities throughout the day"

print(f"\n→ {interpretation}")

# Show the actual average for this participant
print("\n" + "="*70)
print("ACTUAL RESULTS FROM YOUR DATA")
print("="*70)

summary = pd.read_csv('entropy_summary.csv')
print(f"\n{summary.to_string(index=False)}")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print("""
Shannon entropy measures how VARIED or MIXED activities are:

- If someone sits all day → only "Resting" → LOW entropy (close to 0)
- If someone does all 4 activities equally → HIGH entropy (close to 2)
- More variety in activities = Higher entropy = Healthier lifestyle

We calculated this for EVERY day, then averaged across all days.
""")

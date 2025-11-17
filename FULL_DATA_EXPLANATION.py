import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

print("="*90)
print("COMPLETE DETAILED EXPLANATION OF YOUR FITBIT DATA")
print("="*90)

# Load both datasets
fs1987 = pd.read_csv('FS1987-intraday.csv')
fs2116 = pd.read_csv('FS2116-intraday.csv')

print("\n" + "="*90)
print("PART 1: WHAT IS THIS DATA? (THE BIG PICTURE)")
print("="*90)

print("""
This data comes from a research study where people wore Fitbit devices 24/7 for several weeks.
The Fitbit tracked their physical activity EVERY SINGLE MINUTE of the day and night.

Think of it like this:
- You wake up at 7am → Fitbit records your activity at 7:00, 7:01, 7:02, etc.
- You walk to breakfast at 7:30 → Fitbit sees increased activity
- You sit at your desk at 9am → Fitbit sees low activity
- You go for a run at 5pm → Fitbit sees high activity
- You sleep at 11pm → Fitbit sees almost no activity

This happens EVERY MINUTE for 2-3 WEEKS STRAIGHT.

Why is this valuable?
- It captures your ENTIRE lifestyle pattern
- It shows when you're active vs inactive
- It reveals your daily routines (or lack of routine)
- It can be linked to health outcomes like sleep quality, mood, BMI, etc.
""")

print("\n" + "="*90)
print("PART 2: THE TWO PARTICIPANTS")
print("="*90)

print(f"""
PARTICIPANT FS1987:
- Total data points: {len(fs1987):,} minutes
- This equals: {len(fs1987)/(60*24):.1f} days of continuous monitoring
- Date range: {fs1987['activity_date'].min()} to {fs1987['activity_date'].max()}

PARTICIPANT FS2116:
- Total data points: {len(fs2116):,} minutes  
- This equals: {len(fs2116)/(60*24):.1f} days of continuous monitoring
- Date range: {fs2116['activity_date'].min()} to {fs2116['activity_date'].max()}

These are TWO DIFFERENT PEOPLE being monitored.
Each person has their own unique activity patterns, lifestyle, and health profile.
""")

print("\n" + "="*90)
print("PART 3: WHAT EACH COLUMN MEANS (IN DETAIL)")
print("="*90)

print("\nLet me show you the actual data structure:")
print(fs1987.head(15).to_string())

print("""

Now let me explain EVERY column:

1. "Unnamed: 0" 
   - Just a row number, ignore this

2. "participant_id" 
   - Which person this data belongs to (FS1987 or FS2116)
   - Each person is a unique individual in the study

3. "fitbit_start_date" and "fitbit_end_date"
   - The overall study period for this participant
   - Shows when they started and stopped wearing the Fitbit

4. "status"
   - Whether the data collection was successful
   - All say "complete" = good quality data

5. "activity_date" ⭐ MOST IMPORTANT
   - The EXACT timestamp for this specific minute
   - Format: 2024-12-19 17:24:00 means Dec 19, 2024 at 5:24 PM
   - Each row = one minute of this person's life

6. "activities_calories" ⭐ KEY MEASUREMENT
   - How many calories this person burned in THIS SPECIFIC MINUTE
   - Example: 0.9087 calories = very low (sleeping/resting)
   - Example: 5.0 calories = high (walking/exercising)
   - This is REAL energy expenditure

7. "activities_calories_mets" ⭐ KEY MEASUREMENT
   - METs = Metabolic Equivalent of Task
   - This is a standardized way to measure activity intensity
   
   What METs mean:
   - 10 METs = sleeping, completely at rest
   - 15-20 METs = sitting, very light activity (watching TV, desk work)
   - 25-35 METs = light activity (slow walking, cooking)
   - 40-60 METs = moderate activity (brisk walking, light exercise)
   - 70+ METs = vigorous activity (running, intense workout)
   
   Higher METs = more intense activity = more energy being used

8. "activities_calories_level" ⭐ KEY MEASUREMENT
   - A simplified category of activity intensity
   - 0 = sedentary/resting
   - 1 = light activity
   - 2 = moderate activity  
   - 3 = vigorous activity
   - Some values are NaN (missing) = Fitbit wasn't sure
""")

print("\n" + "="*90)
print("PART 4: WHAT DO THE NUMBERS ACTUALLY LOOK LIKE?")
print("="*90)

# Show statistics
print(f"\nFS1987 ACTIVITY STATISTICS:")
print(f"  Calories per minute:")
print(f"    Average: {fs1987['activities_calories'].mean():.3f}")
print(f"    Minimum: {fs1987['activities_calories'].min():.3f} (deeply asleep)")
print(f"    Maximum: {fs1987['activities_calories'].max():.3f} (intense activity)")
print(f"    Standard deviation: {fs1987['activities_calories'].std():.3f}")

print(f"\n  METs (activity intensity):")
print(f"    Average: {fs1987['activities_calories_mets'].mean():.1f}")
print(f"    Minimum: {fs1987['activities_calories_mets'].min():.1f}")
print(f"    Maximum: {fs1987['activities_calories_mets'].max():.1f}")

print(f"\n  Activity levels distribution:")
for level in sorted(fs1987['activities_calories_level'].dropna().unique()):
    count = (fs1987['activities_calories_level'] == level).sum()
    pct = count / len(fs1987) * 100
    print(f"    Level {int(level)}: {count:,} minutes ({pct:.1f}%)")

print(f"\n\nFS2116 ACTIVITY STATISTICS:")
print(f"  Calories per minute:")
print(f"    Average: {fs2116['activities_calories'].mean():.3f}")
print(f"    Minimum: {fs2116['activities_calories'].min():.3f}")
print(f"    Maximum: {fs2116['activities_calories'].max():.3f}")
print(f"    Standard deviation: {fs2116['activities_calories'].std():.3f}")

print(f"\n  METs (activity intensity):")
print(f"    Average: {fs2116['activities_calories_mets'].mean():.1f}")
print(f"    Minimum: {fs2116['activities_calories_mets'].min():.1f}")
print(f"    Maximum: {fs2116['activities_calories_mets'].max():.1f}")

print(f"\n  Activity levels distribution:")
for level in sorted(fs2116['activities_calories_level'].dropna().unique()):
    count = (fs2116['activities_calories_level'] == level).sum()
    pct = count / len(fs2116) * 100
    print(f"    Level {int(level)}: {count:,} minutes ({pct:.1f}%)")

print("\n" + "="*90)
print("PART 5: WHAT PATTERNS CAN WE SEE?")
print("="*90)

# Analyze by hour of day
fs1987['activity_date'] = pd.to_datetime(fs1987['activity_date'])
fs1987['hour'] = fs1987['activity_date'].dt.hour

hourly_pattern = fs1987.groupby('hour')['activities_calories_mets'].mean()

print("\nFS1987 - AVERAGE ACTIVITY BY HOUR OF DAY:")
print("(This shows what this person typically does at each hour)")
print()

for hour, mets in hourly_pattern.items():
    # Create visual bar
    bar_length = int(mets / 2)
    bar = "█" * bar_length
    
    # Interpret the activity
    if mets < 12:
        activity = "SLEEPING"
    elif mets < 18:
        activity = "Resting/Light"
    elif mets < 25:
        activity = "Moderate activity"
    else:
        activity = "ACTIVE"
    
    time_label = f"{hour:02d}:00"
    print(f"  {time_label} | {mets:5.1f} METs | {bar:20s} | {activity}")

print("""

WHAT THIS REVEALS:
- You can SEE when this person sleeps (low METs in early morning hours)
- You can SEE when they're active (higher METs during waking hours)
- You can SEE their daily routine pattern
""")

print("\n" + "="*90)
print("PART 6: THE HEALTH CONNECTION (THE KEY CONTEXT)")
print("="*90)

print("""
According to your professor, each participant has ADDITIONAL DATA available:

✓ Sleep quality scores
✓ Mood and anxiety levels  
✓ Physical activity assessments
✓ BMI (Body Mass Index)
✓ Glucose levels
✓ Lipid levels (cholesterol)
✓ Cardiovascular health markers

THIS IS CRUCIAL because it means:
- We can analyze their Fitbit activity patterns (what we have now)
- We can correlate those patterns with their health outcomes (what we could get)
- We can discover: "Do certain activity patterns predict better/worse health?"

Example research questions this enables:
- Do people with more regular daily routines have better sleep?
- Does activity pattern complexity correlate with anxiety levels?
- Can we predict cardiovascular risk from activity patterns?
- Do morning activity patterns differ between healthy vs at-risk individuals?
""")

print("\n" + "="*90)
print("PART 7: WHY THIS DATA IS SPECIAL FOR INFORMATION THEORY")
print("="*90)

print("""
This data is PERFECT for information theory analysis because:

1. IT'S A SEQUENCE (like text in Huffman coding)
   - Instead of letters: we have activity levels
   - Instead of words: we have activity patterns
   - We can measure entropy, compress it, find patterns

2. IT HAS TEMPORAL STRUCTURE
   - Things happen in order (you can't run before you wake up)
   - Patterns repeat daily (circadian rhythms)
   - We can measure predictability and complexity

3. IT'S CONTINUOUS OVER TIME
   - Unlike surveys (one data point), this is thousands of data points
   - We can see long-term patterns and short-term variations
   - We can measure consistency vs chaos

4. IT CONNECTS TO REAL OUTCOMES
   - Not just abstract data analysis
   - Links to actual health and wellbeing
   - Has practical implications for healthcare

INFORMATION THEORY TOOLS WE CAN APPLY:
- Shannon Entropy: Measure unpredictability in daily patterns
- Huffman Coding: Compress activity sequences, measure compressibility  
- Entropy Rate: Measure predictability of transitions
- Mutual Information: How much does morning activity tell us about evening activity?
- Complexity Measures: Quantify lifestyle regularity vs chaos
""")

print("\n" + "="*90)
print("SUMMARY: WHAT YOU HAVE")
print("="*90)

print(f"""
✓ TWO PEOPLE (FS1987 and FS2116)
✓ MINUTE-BY-MINUTE activity data over 2-3 weeks
✓ {len(fs1987) + len(fs2116):,} total data points
✓ Measurements: calories, METs, activity levels
✓ Clear daily/nightly patterns visible
✓ Potential to link to health outcomes
✓ Rich enough for sophisticated information theory analysis

This is HIGH-QUALITY research data perfect for your final project!
""")

print("="*90)

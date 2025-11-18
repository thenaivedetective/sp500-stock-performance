"""
Temporal Entropy Analysis of Daily Routines
SSIE-500 Final Project - Group 2
Binghamton University

Research Question:
Does the average Shannon entropy of activity patterns across time slots 
predict health outcomes (sleep quality, mood stability) in individuals 
monitored via wearable devices?

Methodology:
For each minute of the day (e.g., 7:00 AM), collect activity levels across 
all days, calculate Shannon entropy H = -Σ p(x)log₂p(x) for that minute.
Repeat for all 1440 minutes, then average these entropies.

Interpretation:
- Lower entropy = Regular routine (same activity at same time daily)
- Higher entropy = Chaotic schedule (unpredictable activity timing)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import math

# Set plotting style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

print("="*80)
print("TEMPORAL ENTROPY ANALYSIS - ROUTINE REGULARITY")
print("Group 2 - SSIE-500 Final Project")
print("="*80)

# ============================================================================
# STEP 1: LOAD DATA
# ============================================================================
print("\nSTEP 1: Loading Fitbit Data")
print("-"*80)

df1 = pd.read_csv('FS1987-intraday.csv')
df2 = pd.read_csv('FS2116-intraday.csv')

print(f"Participant FS1987: {len(df1):,} minutes")
print(f"Participant FS2116: {len(df2):,} minutes")

# ============================================================================
# STEP 2: DISCRETIZE ACTIVITY LEVELS
# ============================================================================
print("\nSTEP 2: Converting METs to Activity Levels")
print("-"*80)

def mets_to_level(mets):
    """Convert METs to activity level (0-3)"""
    if pd.isna(mets):
        return np.nan
    if mets <= 10:
        return 0  # Resting
    elif mets <= 15:
        return 1  # Light
    elif mets <= 30:
        return 2  # Moderate
    else:
        return 3  # Vigorous

df1['activity_level'] = df1['activities_calories_mets'].apply(mets_to_level)
df2['activity_level'] = df2['activities_calories_mets'].apply(mets_to_level)

print("Activity Levels:")
print("  0 = Resting   (METs ≤ 10)")
print("  1 = Light     (10 < METs ≤ 15)")
print("  2 = Moderate  (15 < METs ≤ 30)")
print("  3 = Vigorous  (METs > 30)")

# ============================================================================
# STEP 3: EXTRACT TIME OF DAY
# ============================================================================
print("\nSTEP 3: Extracting Time of Day from Timestamps")
print("-"*80)

# Extract minute of day (0-1439)
df1['timestamp'] = pd.to_datetime(df1['activity_date'])
df1['minute_of_day'] = df1['timestamp'].dt.hour * 60 + df1['timestamp'].dt.minute

df2['timestamp'] = pd.to_datetime(df2['activity_date'])
df2['minute_of_day'] = df2['timestamp'].dt.hour * 60 + df2['timestamp'].dt.minute

print(f"FS1987: Successfully extracted time for {df1['minute_of_day'].notna().sum():,} records")
print(f"FS2116: Successfully extracted time for {df2['minute_of_day'].notna().sum():,} records")

# ============================================================================
# STEP 4: CALCULATE TEMPORAL ENTROPY FOR EACH MINUTE OF DAY
# ============================================================================
print("\nSTEP 4: Calculating Temporal Entropy for Each Minute of Day")
print("-"*80)

def calculate_entropy(activity_series):
    """Calculate Shannon entropy for a series of activities"""
    # Remove NaN values
    activities = activity_series.dropna()
    
    # No data for this time slot
    if len(activities) == 0:
        return np.nan
    
    # Only one observation = always the same activity = perfect regularity = 0 entropy
    if len(activities) == 1:
        return 0.0
    
    # Count occurrences
    counts = activities.value_counts()
    total = len(activities)
    
    # Calculate entropy
    entropy = 0
    for count in counts:
        if count > 0:
            p = count / total
            entropy -= p * np.log2(p)
    
    return entropy

print("Processing FS1987...")
# Group by minute_of_day and calculate entropy for each
df_temporal_1987 = df1.groupby('minute_of_day')['activity_level'].apply(
    calculate_entropy
).reset_index()
df_temporal_1987.columns = ['minute_of_day', 'entropy']
df_temporal_1987['hour'] = df_temporal_1987['minute_of_day'] // 60
df_temporal_1987['minute'] = df_temporal_1987['minute_of_day'] % 60

print("Processing FS2116...")
df_temporal_2116 = df2.groupby('minute_of_day')['activity_level'].apply(
    calculate_entropy
).reset_index()
df_temporal_2116.columns = ['minute_of_day', 'entropy']
df_temporal_2116['hour'] = df_temporal_2116['minute_of_day'] // 60
df_temporal_2116['minute'] = df_temporal_2116['minute_of_day'] % 60

print(f"✓ Calculated entropy for {len(df_temporal_1987)} time slots (FS1987)")
print(f"✓ Calculated entropy for {len(df_temporal_2116)} time slots (FS2116)")

# ============================================================================
# STEP 5: CALCULATE AVERAGE TEMPORAL ENTROPY
# ============================================================================
print("\nSTEP 5: RESULTS - Average Temporal Entropy")
print("="*80)

avg_1987 = df_temporal_1987['entropy'].mean()
std_1987 = df_temporal_1987['entropy'].std()
valid_1987 = df_temporal_1987['entropy'].notna().sum()

avg_2116 = df_temporal_2116['entropy'].mean()
std_2116 = df_temporal_2116['entropy'].std()
valid_2116 = df_temporal_2116['entropy'].notna().sum()

print(f"\nParticipant FS1987:")
print(f"  Average Temporal Entropy: {avg_1987:.4f} bits")
print(f"  Std Deviation:            {std_1987:.4f} bits")
print(f"  Valid time slots:         {valid_1987}")

print(f"\nParticipant FS2116:")
print(f"  Average Temporal Entropy: {avg_2116:.4f} bits")
print(f"  Std Deviation:            {std_2116:.4f} bits")
print(f"  Valid time slots:         {valid_2116}")

difference = abs(avg_1987 - avg_2116)
pct_diff = difference / max(avg_1987, avg_2116) * 100

print(f"\nDifference: {difference:.4f} bits ({pct_diff:.1f}%)")

if avg_1987 < avg_2116:
    print("→ FS1987 has LOWER entropy = MORE REGULAR routine")
    print("→ FS2116 has HIGHER entropy = MORE CHAOTIC schedule")
else:
    print("→ FS2116 has LOWER entropy = MORE REGULAR routine")
    print("→ FS1987 has HIGHER entropy = MORE CHAOTIC schedule")

# ============================================================================
# STEP 6: INTERPRETATION
# ============================================================================
print("\nSTEP 6: HEALTH INTERPRETATION")
print("="*80)

def interpret_temporal(avg_entropy):
    """Interpret temporal entropy"""
    if avg_entropy < 0.7:
        return "Very Regular Routine", "Excellent"
    elif avg_entropy < 1.0:
        return "Moderately Regular Routine", "Good"
    elif avg_entropy < 1.3:
        return "Somewhat Irregular Routine", "Fair"
    else:
        return "Chaotic Schedule", "Poor"

classification_1987, health_1987 = interpret_temporal(avg_1987)
classification_2116, health_2116 = interpret_temporal(avg_2116)

print(f"\nFS1987:")
print(f"  Classification: {classification_1987}")
print(f"  Health Prediction: {health_1987}")
print(f"  → {'Consistent daily routine' if avg_1987 < 1.0 else 'Irregular schedule'}")

print(f"\nFS2116:")
print(f"  Classification: {classification_2116}")
print(f"  Health Prediction: {health_2116}")
print(f"  → {'Consistent daily routine' if avg_2116 < 1.0 else 'Irregular schedule'}")

# ============================================================================
# STEP 7: SAVE RESULTS
# ============================================================================
print("\nSTEP 7: Saving Results")
print("-"*80)

# Save temporal entropy profiles
df_temporal_1987.to_csv('FS1987_temporal_entropy.csv', index=False)
df_temporal_2116.to_csv('FS2116_temporal_entropy.csv', index=False)

# Save summary
summary = pd.DataFrame({
    'Participant': ['FS1987', 'FS2116'],
    'Average_Temporal_Entropy': [avg_1987, avg_2116],
    'Std_Dev': [std_1987, std_2116],
    'Classification': [classification_1987, classification_2116],
    'Health_Prediction': [health_1987, health_2116]
})
summary.to_csv('temporal_entropy_summary.csv', index=False)

print(f"✓ FS1987_temporal_entropy.csv ({len(df_temporal_1987)} time slots)")
print(f"✓ FS2116_temporal_entropy.csv ({len(df_temporal_2116)} time slots)")
print("✓ temporal_entropy_summary.csv")

# ============================================================================
# STEP 8: VISUALIZATIONS
# ============================================================================
print("\nSTEP 8: Creating Visualizations")
print("-"*80)

# Figure 1: 24-hour temporal entropy profile
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8))

# FS1987
hours = df_temporal_1987['minute_of_day'] / 60
ax1.plot(hours, df_temporal_1987['entropy'], color='#2E86AB', linewidth=1.5, alpha=0.7)
ax1.axhline(avg_1987, color='red', linestyle='--', linewidth=2, 
            label=f'Average: {avg_1987:.4f} bits')
ax1.set_ylabel('Temporal Entropy (bits)', fontsize=11, fontweight='bold')
ax1.set_title('FS1987 - Temporal Entropy Profile (Routine Regularity)', 
              fontsize=13, fontweight='bold')
ax1.set_xlim(0, 24)
ax1.set_xticks(range(0, 25, 2))
ax1.legend()
ax1.grid(alpha=0.3)

# FS2116
hours = df_temporal_2116['minute_of_day'] / 60
ax2.plot(hours, df_temporal_2116['entropy'], color='#A23B72', linewidth=1.5, alpha=0.7)
ax2.axhline(avg_2116, color='red', linestyle='--', linewidth=2, 
            label=f'Average: {avg_2116:.4f} bits')
ax2.set_xlabel('Hour of Day', fontsize=11, fontweight='bold')
ax2.set_ylabel('Temporal Entropy (bits)', fontsize=11, fontweight='bold')
ax2.set_title('FS2116 - Temporal Entropy Profile (Routine Regularity)', 
              fontsize=13, fontweight='bold')
ax2.set_xlim(0, 24)
ax2.set_xticks(range(0, 25, 2))
ax2.legend()
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('temporal_entropy_profile.png', dpi=300, bbox_inches='tight')
print("✓ temporal_entropy_profile.png")

# Figure 2: Comparison
fig, ax = plt.subplots(figsize=(8, 6))

bars = ax.bar(['FS1987', 'FS2116'], [avg_1987, avg_2116], 
              color=['#2E86AB', '#A23B72'], alpha=0.8, edgecolor='black', linewidth=2)

for bar, val in zip(bars, [avg_1987, avg_2116]):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{val:.4f}',
            ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_ylabel('Average Temporal Entropy (bits)', fontsize=12, fontweight='bold')
ax.set_title('Routine Regularity Comparison\n(Lower = More Regular)', 
             fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('temporal_entropy_comparison.png', dpi=300, bbox_inches='tight')
print("✓ temporal_entropy_comparison.png")

# Figure 3: Hourly averages
fig, ax = plt.subplots(figsize=(12, 6))

hourly_1987 = df_temporal_1987.groupby('hour')['entropy'].mean()
hourly_2116 = df_temporal_2116.groupby('hour')['entropy'].mean()

ax.plot(hourly_1987.index, hourly_1987.values, marker='o', linewidth=2.5, 
        markersize=6, color='#2E86AB', label='FS1987')
ax.plot(hourly_2116.index, hourly_2116.values, marker='s', linewidth=2.5, 
        markersize=6, color='#A23B72', label='FS2116')

ax.set_xlabel('Hour of Day', fontsize=12, fontweight='bold')
ax.set_ylabel('Average Temporal Entropy (bits)', fontsize=12, fontweight='bold')
ax.set_title('Routine Regularity by Time of Day', fontsize=14, fontweight='bold')
ax.set_xticks(range(0, 24, 2))
ax.legend(fontsize=11)
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('temporal_entropy_by_hour.png', dpi=300, bbox_inches='tight')
print("✓ temporal_entropy_by_hour.png")

print("\n" + "="*80)
print("ANALYSIS COMPLETE!")
print("="*80)
print(f"""
SUMMARY:
- FS1987: Temporal entropy = {avg_1987:.4f} bits ({classification_1987})
- FS2116: Temporal entropy = {avg_2116:.4f} bits ({classification_2116})

Lower entropy = More predictable routine = Better health outcomes
Higher entropy = More chaotic schedule = Potential health issues
""")

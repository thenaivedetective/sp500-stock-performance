"""
RESEARCH QUESTION 1: Temporal Entropy Analysis (CORRECTED VERSION)
===================================================================

CRITICAL FIX: Updated METs discretization to match actual Fitbit data distribution.
Previous version used incorrect thresholds (10-15, 15-25, 25-40, 40+) which didn't
match the Fitbit METs scale. This version uses data-driven bins based on actual distribution.

Research Question:
"Does the average Shannon entropy of activity patterns across time slots 
predict health outcomes (sleep quality, mood stability) in individuals 
monitored via wearable devices?"

Author: Lana Jalal Gidan
Course: SSIE-500 Final Project
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import math
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style for professional plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("="*80)
print("RESEARCH QUESTION 1: TEMPORAL ENTROPY ANALYSIS (CORRECTED)")
print("="*80)

# ============================================================================
# PART 1: DATA LOADING AND PREPROCESSING
# ============================================================================

print("\n" + "="*80)
print("PART 1: DATA LOADING AND PREPROCESSING")
print("="*80)

# Load data for both participants
df_1987 = pd.read_csv('FS1987-intraday.csv')
df_2116 = pd.read_csv('FS2116-intraday.csv')

print(f"\nParticipant FS1987:")
print(f"  Total data points: {len(df_1987):,} minutes")
print(f"  Valid METs values: {df_1987['activities_calories_mets'].notna().sum():,}")

print(f"\nParticipant FS2116:")
print(f"  Total data points: {len(df_2116):,} minutes")
print(f"  Valid METs values: {df_2116['activities_calories_mets'].notna().sum():,}")

# Analyze METs distribution
print("\n" + "="*80)
print("METs DISTRIBUTION ANALYSIS")
print("="*80)

mets_1987 = df_1987['activities_calories_mets'].dropna()
mets_2116 = df_2116['activities_calories_mets'].dropna()

print("\nFS1987 METs statistics:")
print(f"  Mean: {mets_1987.mean():.2f}")
print(f"  Median: {mets_1987.median():.2f}")
print(f"  Min: {mets_1987.min():.2f}")
print(f"  Max: {mets_1987.max():.2f}")
print(f"  25th percentile: {mets_1987.quantile(0.25):.2f}")
print(f"  75th percentile: {mets_1987.quantile(0.75):.2f}")

print("\nFS2116 METs statistics:")
print(f"  Mean: {mets_2116.mean():.2f}")
print(f"  Median: {mets_2116.median():.2f}")
print(f"  Min: {mets_2116.min():.2f}")
print(f"  Max: {mets_2116.max():.2f}")
print(f"  25th percentile: {mets_2116.quantile(0.25):.2f}")
print(f"  75th percentile: {mets_2116.quantile(0.75):.2f}")

# Convert timestamps to datetime
df_1987['activity_date'] = pd.to_datetime(df_1987['activity_date'])
df_2116['activity_date'] = pd.to_datetime(df_2116['activity_date'])

# CORRECTED: Data-driven discretization based on actual METs distribution
def mets_to_level_corrected(mets):
    """
    Convert METs to discrete activity level using DATA-DRIVEN thresholds
    Based on actual Fitbit data distribution where:
    - Most data is at METs=10 (baseline/resting)
    - Mean is around 13-14
    - Values range from 10 to 113+
    """
    if pd.isna(mets):
        return np.nan
    if mets <= 10:
        return 0  # Resting (baseline Fitbit value)
    elif mets <= 15:
        return 1  # Light activity
    elif mets <= 30:
        return 2  # Moderate activity
    else:
        return 3  # Vigorous activity (>30)

df_1987['activity_level'] = df_1987['activities_calories_mets'].apply(mets_to_level_corrected)
df_2116['activity_level'] = df_2116['activities_calories_mets'].apply(mets_to_level_corrected)

print("\n" + "="*80)
print("CORRECTED Activity Level Discretization:")
print("="*80)
print("  Level 0: METs <= 10    (Resting - Fitbit baseline)")
print("  Level 1: 10 < METs <= 15  (Light activity)")
print("  Level 2: 15 < METs <= 30  (Moderate activity)")
print("  Level 3: METs > 30     (Vigorous activity)")

# Verify distribution
print("\nActivity level distribution:")
print("\nFS1987:")
for level in range(4):
    count = (df_1987['activity_level'] == level).sum()
    total_valid = df_1987['activity_level'].notna().sum()
    pct = (count / total_valid * 100) if total_valid > 0 else 0
    print(f"  Level {level}: {count:6,} ({pct:5.1f}%)")

print("\nFS2116:")
for level in range(4):
    count = (df_2116['activity_level'] == level).sum()
    total_valid = df_2116['activity_level'].notna().sum()
    pct = (count / total_valid * 100) if total_valid > 0 else 0
    print(f"  Level {level}: {count:6,} ({pct:5.1f}%)")

# Extract time features
df_1987['hour'] = df_1987['activity_date'].dt.hour
df_1987['minute'] = df_1987['activity_date'].dt.minute
df_1987['minute_of_day'] = df_1987['hour'] * 60 + df_1987['minute']
df_1987['date'] = df_1987['activity_date'].dt.date

df_2116['hour'] = df_2116['activity_date'].dt.hour
df_2116['minute'] = df_2116['activity_date'].dt.minute
df_2116['minute_of_day'] = df_2116['hour'] * 60 + df_2116['minute']
df_2116['date'] = df_2116['activity_date'].dt.date

# ============================================================================
# PART 2: TEMPORAL ENTROPY CALCULATION
# ============================================================================

print("\n" + "="*80)
print("PART 2: TEMPORAL ENTROPY CALCULATION")
print("="*80)

def calculate_shannon_entropy(sequence):
    """
    Calculate Shannon entropy of a sequence
    H(X) = -Σ p(x) log₂ p(x)
    """
    # Remove NaN values
    sequence = [x for x in sequence if not pd.isna(x)]
    
    if len(sequence) == 0:
        return np.nan
    
    # Count frequencies
    counts = Counter(sequence)
    total = len(sequence)
    
    # Calculate entropy
    entropy = 0
    for count in counts.values():
        if count > 0:
            p = count / total
            entropy -= p * math.log2(p)
    
    return entropy

def calculate_temporal_entropy_profile(df, participant_id):
    """
    Calculate entropy for each minute-of-day across all days
    Returns entropy profile for all 1440 minutes
    """
    print(f"\nCalculating temporal entropy for {participant_id}...")
    
    # Get unique days
    unique_days = df['date'].unique()
    num_days = len(unique_days)
    print(f"  Number of days: {num_days}")
    
    # Calculate entropy for each minute of day
    temporal_entropies = []
    
    for minute in range(1440):  # 0 to 1439 (24 hours * 60 minutes)
        # Get all activity levels at this minute across all days
        activities_at_minute = df[df['minute_of_day'] == minute]['activity_level'].values
        
        if len(activities_at_minute) > 0:
            entropy = calculate_shannon_entropy(activities_at_minute)
            temporal_entropies.append({
                'minute_of_day': minute,
                'hour': minute // 60,
                'minute': minute % 60,
                'entropy': entropy,
                'n_observations': len([x for x in activities_at_minute if not pd.isna(x)])
            })
    
    return pd.DataFrame(temporal_entropies)

# Calculate for both participants
entropy_profile_1987 = calculate_temporal_entropy_profile(df_1987, "FS1987")
entropy_profile_2116 = calculate_temporal_entropy_profile(df_2116, "FS2116")

print(f"\nFS1987 temporal entropy profile calculated:")
print(f"  Total time slots analyzed: {len(entropy_profile_1987)}")
print(f"  Valid entropy values: {entropy_profile_1987['entropy'].notna().sum()}")

print(f"\nFS2116 temporal entropy profile calculated:")
print(f"  Total time slots analyzed: {len(entropy_profile_2116)}")
print(f"  Valid entropy values: {entropy_profile_2116['entropy'].notna().sum()}")

# ============================================================================
# PART 3: CALCULATE AVERAGE TEMPORAL ENTROPY (KEY METRIC)
# ============================================================================

print("\n" + "="*80)
print("PART 3: AVERAGE TEMPORAL ENTROPY (PRIMARY RESULT)")
print("="*80)

avg_entropy_1987 = entropy_profile_1987['entropy'].mean()
std_entropy_1987 = entropy_profile_1987['entropy'].std()

avg_entropy_2116 = entropy_profile_2116['entropy'].mean()
std_entropy_2116 = entropy_profile_2116['entropy'].std()

print(f"\nParticipant FS1987:")
print(f"  Average temporal entropy: {avg_entropy_1987:.4f} bits")
print(f"  Standard deviation:       {std_entropy_1987:.4f} bits")
print(f"  Min entropy:              {entropy_profile_1987['entropy'].min():.4f} bits")
print(f"  Max entropy:              {entropy_profile_1987['entropy'].max():.4f} bits")

print(f"\nParticipant FS2116:")
print(f"  Average temporal entropy: {avg_entropy_2116:.4f} bits")
print(f"  Standard deviation:       {std_entropy_2116:.4f} bits")
print(f"  Min entropy:              {entropy_profile_2116['entropy'].min():.4f} bits")
print(f"  Max entropy:              {entropy_profile_2116['entropy'].max():.4f} bits")

print(f"\nComparison:")
print(f"  Difference in average entropy: {abs(avg_entropy_1987 - avg_entropy_2116):.4f} bits")
if avg_entropy_1987 < avg_entropy_2116:
    print(f"  FS1987 has LOWER entropy (more regular routine)")
else:
    print(f"  FS2116 has LOWER entropy (more regular routine)")

# ============================================================================
# PART 4: DETAILED ANALYSIS BY TIME OF DAY
# ============================================================================

print("\n" + "="*80)
print("PART 4: ANALYSIS BY TIME OF DAY")
print("="*80)

# Define time windows
time_windows = {
    'Night (12am-6am)': (0, 6),
    'Morning (6am-12pm)': (6, 12),
    'Afternoon (12pm-6pm)': (12, 18),
    'Evening (6pm-12am)': (18, 24)
}

def analyze_by_time_window(entropy_df, time_windows):
    """Calculate average entropy for each time window"""
    results = {}
    for window_name, (start_hour, end_hour) in time_windows.items():
        window_data = entropy_df[
            (entropy_df['hour'] >= start_hour) & 
            (entropy_df['hour'] < end_hour)
        ]
        avg_entropy = window_data['entropy'].mean()
        results[window_name] = avg_entropy
    return results

window_results_1987 = analyze_by_time_window(entropy_profile_1987, time_windows)
window_results_2116 = analyze_by_time_window(entropy_profile_2116, time_windows)

print("\nFS1987 - Entropy by time of day:")
for window, entropy in window_results_1987.items():
    print(f"  {window:25s}: {entropy:.4f} bits")

print("\nFS2116 - Entropy by time of day:")
for window, entropy in window_results_2116.items():
    print(f"  {window:25s}: {entropy:.4f} bits")

# ============================================================================
# PART 5: VISUALIZATION
# ============================================================================

print("\n" + "="*80)
print("PART 5: GENERATING VISUALIZATIONS")
print("="*80)

# Figure 1: Temporal Entropy Profile (24-hour)
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# FS1987
axes[0].plot(entropy_profile_1987['minute_of_day'] / 60, 
             entropy_profile_1987['entropy'], 
             linewidth=2, color='#2E86AB', alpha=0.8)
axes[0].fill_between(entropy_profile_1987['minute_of_day'] / 60, 
                       entropy_profile_1987['entropy'], 
                       alpha=0.3, color='#2E86AB')
axes[0].axhline(y=avg_entropy_1987, color='red', linestyle='--', 
                linewidth=2, label=f'Mean: {avg_entropy_1987:.3f} bits')
axes[0].set_xlabel('Hour of Day', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Entropy (bits)', fontsize=12, fontweight='bold')
axes[0].set_title('FS1987 - Temporal Entropy Profile Across 24 Hours (CORRECTED)', 
                  fontsize=14, fontweight='bold')
axes[0].set_xlim(0, 24)
axes[0].set_xticks(range(0, 25, 2))
axes[0].grid(True, alpha=0.3)
axes[0].legend(fontsize=11)

# FS2116
axes[1].plot(entropy_profile_2116['minute_of_day'] / 60, 
             entropy_profile_2116['entropy'], 
             linewidth=2, color='#A23B72', alpha=0.8)
axes[1].fill_between(entropy_profile_2116['minute_of_day'] / 60, 
                       entropy_profile_2116['entropy'], 
                       alpha=0.3, color='#A23B72')
axes[1].axhline(y=avg_entropy_2116, color='red', linestyle='--', 
                linewidth=2, label=f'Mean: {avg_entropy_2116:.3f} bits')
axes[1].set_xlabel('Hour of Day', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Entropy (bits)', fontsize=12, fontweight='bold')
axes[1].set_title('FS2116 - Temporal Entropy Profile Across 24 Hours (CORRECTED)', 
                  fontsize=14, fontweight='bold')
axes[1].set_xlim(0, 24)
axes[1].set_xticks(range(0, 25, 2))
axes[1].grid(True, alpha=0.3)
axes[1].legend(fontsize=11)

plt.tight_layout()
plt.savefig('temporal_entropy_profiles_CORRECTED.png', dpi=300, bbox_inches='tight')
print("✓ Saved: temporal_entropy_profiles_CORRECTED.png")

# Figure 2: Comparison Bar Chart
fig, ax = plt.subplots(figsize=(10, 6))

participants = ['FS1987', 'FS2116']
avg_entropies = [avg_entropy_1987, avg_entropy_2116]
colors = ['#2E86AB', '#A23B72']

bars = ax.bar(participants, avg_entropies, color=colors, alpha=0.8, edgecolor='black', linewidth=2)

# Add value labels on bars
for i, (bar, val) in enumerate(zip(bars, avg_entropies)):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{val:.4f} bits',
            ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_ylabel('Average Temporal Entropy (bits)', fontsize=12, fontweight='bold')
ax.set_title('Comparison of Average Temporal Entropy Between Participants (CORRECTED)', 
             fontsize=14, fontweight='bold')
ax.set_ylim(0, max(avg_entropies) * 1.2)
ax.grid(True, axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('entropy_comparison_CORRECTED.png', dpi=300, bbox_inches='tight')
print("✓ Saved: entropy_comparison_CORRECTED.png")

# Figure 3: Time-of-Day Comparison
fig, ax = plt.subplots(figsize=(12, 6))

window_names = list(time_windows.keys())
entropy_1987_vals = [window_results_1987[w] for w in window_names]
entropy_2116_vals = [window_results_2116[w] for w in window_names]

x = np.arange(len(window_names))
width = 0.35

bars1 = ax.bar(x - width/2, entropy_1987_vals, width, label='FS1987', 
               color='#2E86AB', alpha=0.8, edgecolor='black')
bars2 = ax.bar(x + width/2, entropy_2116_vals, width, label='FS2116', 
               color='#A23B72', alpha=0.8, edgecolor='black')

ax.set_xlabel('Time of Day', fontsize=12, fontweight='bold')
ax.set_ylabel('Average Entropy (bits)', fontsize=12, fontweight='bold')
ax.set_title('Temporal Entropy by Time of Day - Participant Comparison (CORRECTED)', 
             fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(window_names, rotation=15, ha='right')
ax.legend(fontsize=11)
ax.grid(True, axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('entropy_by_timeofday_CORRECTED.png', dpi=300, bbox_inches='tight')
print("✓ Saved: entropy_by_timeofday_CORRECTED.png")

# ============================================================================
# PART 6: INTERPRETATION AND HEALTH PREDICTIONS
# ============================================================================

print("\n" + "="*80)
print("PART 6: INTERPRETATION AND HEALTH PREDICTIONS")
print("="*80)

def interpret_entropy(avg_entropy):
    """Interpret average temporal entropy for health prediction"""
    if avg_entropy < 0.5:
        return "Very Regular Routine", "Excellent", "Highly predictable daily patterns"
    elif avg_entropy < 0.8:
        return "Regular Routine", "Good", "Consistent daily patterns with good structure"
    elif avg_entropy < 1.2:
        return "Moderately Regular", "Fair", "Some routine structure but with variability"
    elif avg_entropy < 1.5:
        return "Irregular Routine", "Poor", "Inconsistent daily patterns"
    else:
        return "Chaotic Routine", "Very Poor", "Highly unpredictable, minimal structure"

routine_1987, health_1987, desc_1987 = interpret_entropy(avg_entropy_1987)
routine_2116, health_2116, desc_2116 = interpret_entropy(avg_entropy_2116)

print(f"\nParticipant FS1987:")
print(f"  Average Entropy:    {avg_entropy_1987:.4f} bits")
print(f"  Routine Assessment: {routine_1987}")
print(f"  Health Prediction:  {health_1987}")
print(f"  Description:        {desc_1987}")

print(f"\nParticipant FS2116:")
print(f"  Average Entropy:    {avg_entropy_2116:.4f} bits")
print(f"  Routine Assessment: {routine_2116}")
print(f"  Health Prediction:  {health_2116}")
print(f"  Description:        {desc_2116}")

# ============================================================================
# PART 7: SAVE RESULTS TO CSV
# ============================================================================

print("\n" + "="*80)
print("PART 7: SAVING RESULTS")
print("="*80)

# Save full entropy profiles
entropy_profile_1987.to_csv('FS1987_entropy_profile_CORRECTED.csv', index=False)
entropy_profile_2116.to_csv('FS2116_entropy_profile_CORRECTED.csv', index=False)
print("✓ Saved: FS1987_entropy_profile_CORRECTED.csv")
print("✓ Saved: FS2116_entropy_profile_CORRECTED.csv")

# Save summary results
summary_results = pd.DataFrame({
    'Participant': ['FS1987', 'FS2116'],
    'Average_Temporal_Entropy': [avg_entropy_1987, avg_entropy_2116],
    'Std_Dev': [std_entropy_1987, std_entropy_2116],
    'Min_Entropy': [entropy_profile_1987['entropy'].min(), 
                    entropy_profile_2116['entropy'].min()],
    'Max_Entropy': [entropy_profile_1987['entropy'].max(), 
                    entropy_profile_2116['entropy'].max()],
    'Routine_Assessment': [routine_1987, routine_2116],
    'Health_Prediction': [health_1987, health_2116]
})

summary_results.to_csv('temporal_entropy_summary_CORRECTED.csv', index=False)
print("✓ Saved: temporal_entropy_summary_CORRECTED.csv")

print("\n" + "="*80)
print("ANALYSIS COMPLETE!")
print("="*80)
print("\nGenerated files:")
print("  1. temporal_entropy_profiles_CORRECTED.png - 24-hour entropy profiles")
print("  2. entropy_comparison_CORRECTED.png - Overall comparison")
print("  3. entropy_by_timeofday_CORRECTED.png - Time-of-day analysis")
print("  4. FS1987_entropy_profile_CORRECTED.csv - Detailed data for FS1987")
print("  5. FS2116_entropy_profile_CORRECTED.csv - Detailed data for FS2116")
print("  6. temporal_entropy_summary_CORRECTED.csv - Summary statistics")
print("="*80)

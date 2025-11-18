"""
Daily Routine Regularity Analysis Using Shannon Entropy
SSIE-500 Final Project - Group 2
Binghamton University

Research Question:
Does the Shannon entropy of daily activity patterns predict health outcomes?

Methodology:
For each day, calculate Shannon entropy of activity distribution.
Lower entropy = less varied activities (potentially sedentary or routine)
Higher entropy = more varied activities (balanced lifestyle)
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

print("="*70)
print("DAILY ROUTINE ENTROPY ANALYSIS")
print("Group 2 - SSIE-500 Final Project")
print("="*70)

# ============================================================================
# STEP 1: LOAD DATA
# ============================================================================
print("\nSTEP 1: Loading Fitbit Data")
print("-"*70)

df1 = pd.read_csv('FS1987-intraday.csv')
df2 = pd.read_csv('FS2116-intraday.csv')

print(f"Participant FS1987: {len(df1):,} minutes")
print(f"Participant FS2116: {len(df2):,} minutes")

# ============================================================================
# STEP 2: DISCRETIZE ACTIVITY LEVELS
# ============================================================================
print("\nSTEP 2: Converting METs to Activity Levels")
print("-"*70)

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
# STEP 3: CALCULATE SHANNON ENTROPY FOR EACH DAY
# ============================================================================
print("\nSTEP 3: Calculating Shannon Entropy for Each Day")
print("-"*70)

def shannon_entropy(activities):
    """Calculate Shannon entropy H(X) = -Σ p(x)log₂(p(x))"""
    activities = [a for a in activities if not pd.isna(a)]
    if len(activities) == 0:
        return np.nan
    
    counts = Counter(activities)
    total = len(activities)
    
    entropy = 0
    for count in counts.values():
        if count > 0:
            p = count / total
            entropy -= p * math.log2(p)
    
    return entropy

# Extract date from timestamp
df1['date'] = pd.to_datetime(df1['activity_date']).dt.date
df2['date'] = pd.to_datetime(df2['activity_date']).dt.date

# Calculate entropy for each day
daily_entropy_1987 = []
for date in df1['date'].unique():
    day_data = df1[df1['date'] == date]['activity_level']
    entropy = shannon_entropy(day_data)
    daily_entropy_1987.append({'date': date, 'entropy': entropy})

daily_entropy_2116 = []
for date in df2['date'].unique():
    day_data = df2[df2['date'] == date]['activity_level']
    entropy = shannon_entropy(day_data)
    daily_entropy_2116.append({'date': date, 'entropy': entropy})

df_entropy_1987 = pd.DataFrame(daily_entropy_1987)
df_entropy_2116 = pd.DataFrame(daily_entropy_2116)

print(f"\nFS1987: Calculated entropy for {len(df_entropy_1987)} days")
print(f"FS2116: Calculated entropy for {len(df_entropy_2116)} days")

# ============================================================================
# STEP 4: RESULTS
# ============================================================================
print("\nSTEP 4: RESULTS")
print("="*70)

avg_1987 = df_entropy_1987['entropy'].mean()
std_1987 = df_entropy_1987['entropy'].std()
min_1987 = df_entropy_1987['entropy'].min()
max_1987 = df_entropy_1987['entropy'].max()

avg_2116 = df_entropy_2116['entropy'].mean()
std_2116 = df_entropy_2116['entropy'].std()
min_2116 = df_entropy_2116['entropy'].min()
max_2116 = df_entropy_2116['entropy'].max()

print(f"\nParticipant FS1987:")
print(f"  Average Entropy: {avg_1987:.3f} bits")
print(f"  Std Deviation:   {std_1987:.3f} bits")
print(f"  Range:           {min_1987:.3f} - {max_1987:.3f} bits")

print(f"\nParticipant FS2116:")
print(f"  Average Entropy: {avg_2116:.3f} bits")
print(f"  Std Deviation:   {std_2116:.3f} bits")
print(f"  Range:           {min_2116:.3f} - {max_2116:.3f} bits")

print(f"\nDifference: {abs(avg_1987 - avg_2116):.3f} bits")
if avg_1987 < avg_2116:
    print("→ FS1987 has lower entropy (less activity variety)")
else:
    print("→ FS2116 has lower entropy (less activity variety)")

# ============================================================================
# STEP 5: INTERPRETATION
# ============================================================================
print("\nSTEP 5: HEALTH INTERPRETATION")
print("="*70)

def interpret(avg_entropy):
    if avg_entropy < 0.8:
        return "Low variety (may indicate sedentary lifestyle)"
    elif avg_entropy < 1.2:
        return "Moderate variety (some balance)"
    else:
        return "High variety (balanced activities)"

print(f"\nFS1987: {interpret(avg_1987)}")
print(f"FS2116: {interpret(avg_2116)}")

# ============================================================================
# STEP 6: SAVE RESULTS
# ============================================================================
print("\nSTEP 6: Saving Results")
print("-"*70)

# Save daily entropy values
df_entropy_1987.to_csv('FS1987_daily_entropy.csv', index=False)
df_entropy_2116.to_csv('FS2116_daily_entropy.csv', index=False)

# Save summary
summary = pd.DataFrame({
    'Participant': ['FS1987', 'FS2116'],
    'Average_Entropy': [avg_1987, avg_2116],
    'Std_Dev': [std_1987, std_2116],
    'Min': [min_1987, min_2116],
    'Max': [max_1987, max_2116],
    'Interpretation': [interpret(avg_1987), interpret(avg_2116)]
})
summary.to_csv('entropy_summary.csv', index=False)

print("✓ FS1987_daily_entropy.csv")
print("✓ FS2116_daily_entropy.csv")
print("✓ entropy_summary.csv")

# ============================================================================
# STEP 7: VISUALIZATIONS
# ============================================================================
print("\nSTEP 7: Creating Visualizations")
print("-"*70)

# Figure 1: Daily entropy over time
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

ax1.plot(range(len(df_entropy_1987)), df_entropy_1987['entropy'], 
         marker='o', color='#2E86AB', linewidth=2, markersize=4)
ax1.axhline(avg_1987, color='red', linestyle='--', linewidth=2, 
            label=f'Average: {avg_1987:.3f} bits')
ax1.set_ylabel('Entropy (bits)', fontsize=11, fontweight='bold')
ax1.set_title('FS1987 - Daily Activity Entropy', fontsize=13, fontweight='bold')
ax1.legend()
ax1.grid(alpha=0.3)

ax2.plot(range(len(df_entropy_2116)), df_entropy_2116['entropy'], 
         marker='o', color='#A23B72', linewidth=2, markersize=4)
ax2.axhline(avg_2116, color='red', linestyle='--', linewidth=2, 
            label=f'Average: {avg_2116:.3f} bits')
ax2.set_xlabel('Day Number', fontsize=11, fontweight='bold')
ax2.set_ylabel('Entropy (bits)', fontsize=11, fontweight='bold')
ax2.set_title('FS2116 - Daily Activity Entropy', fontsize=13, fontweight='bold')
ax2.legend()
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('daily_entropy_timeseries.png', dpi=300, bbox_inches='tight')
print("✓ daily_entropy_timeseries.png")

# Figure 2: Comparison
fig, ax = plt.subplots(figsize=(8, 6))

bars = ax.bar(['FS1987', 'FS2116'], [avg_1987, avg_2116], 
              color=['#2E86AB', '#A23B72'], alpha=0.8, edgecolor='black', linewidth=2)

for bar, val in zip(bars, [avg_1987, avg_2116]):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{val:.3f}',
            ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_ylabel('Average Daily Entropy (bits)', fontsize=12, fontweight='bold')
ax.set_title('Comparison of Daily Activity Entropy', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('entropy_comparison.png', dpi=300, bbox_inches='tight')
print("✓ entropy_comparison.png")

# Figure 3: Distribution
fig, ax = plt.subplots(figsize=(10, 6))

ax.hist(df_entropy_1987['entropy'], bins=15, alpha=0.6, color='#2E86AB', 
        label='FS1987', edgecolor='black')
ax.hist(df_entropy_2116['entropy'], bins=15, alpha=0.6, color='#A23B72', 
        label='FS2116', edgecolor='black')

ax.axvline(avg_1987, color='#2E86AB', linestyle='--', linewidth=2, 
           label=f'FS1987 mean: {avg_1987:.3f}')
ax.axvline(avg_2116, color='#A23B72', linestyle='--', linewidth=2, 
           label=f'FS2116 mean: {avg_2116:.3f}')

ax.set_xlabel('Daily Entropy (bits)', fontsize=12, fontweight='bold')
ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
ax.set_title('Distribution of Daily Activity Entropy', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('entropy_distribution.png', dpi=300, bbox_inches='tight')
print("✓ entropy_distribution.png")

print("\n" + "="*70)
print("ANALYSIS COMPLETE!")
print("="*70)

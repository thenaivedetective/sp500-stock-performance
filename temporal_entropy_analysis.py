import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

# Set plotting style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

print("="*90)
print("TEMPORAL ENTROPY ANALYSIS - ROUTINE REGULARITY")
print("Group 2 - SSIE-500 Final Project")
print("="*90)

# ============================================================================
# STEP 1: LOAD DATA
# ============================================================================
print("\nSTEP 1: Loading Fitbit Data")
print("-"*90)

df1 = pd.read_csv('FS1987-intraday.csv')
df2 = pd.read_csv('FS2116-intraday.csv')

print(f"Participant FS1987: {len(df1):,} minute-level observations")
print(f"Participant FS2116: {len(df2):,} minute-level observations")

# ============================================================================
# STEP 2: USE FITBIT'S OFFICIAL ACTIVITY LEVEL COLUMN
# ============================================================================
print("\nSTEP 2: Using Fitbit Activity Levels (0–3)")
print("-"*90)

# Use the real Fitbit activity level column
df1['activity_level'] = df1['activities_calories_level']
df2['activity_level'] = df2['activities_calories_level']

print("Activity Levels (Provided by Fitbit):")
print("  0 = Sedentary")
print("  1 = Light Activity")
print("  2 = Moderate Activity")
print("  3 = Vigorous Activity")

# ============================================================================
# STEP 3: EXTRACT TIME OF DAY
# ============================================================================
print("\nSTEP 3: Extracting Time of Day (0–1439 minutes)")
print("-"*90)

df1['timestamp'] = pd.to_datetime(df1['activity_date'])
df1['minute_of_day'] = df1['timestamp'].dt.hour * 60 + df1['timestamp'].dt.minute

df2['timestamp'] = pd.to_datetime(df2['activity_date'])
df2['minute_of_day'] = df2['timestamp'].dt.hour * 60 + df2['timestamp'].dt.minute

print(f"FS1987 time extraction OK → {df1['minute_of_day'].notna().sum():,} rows")
print(f"FS2116 time extraction OK → {df2['minute_of_day'].notna().sum():,} rows")

# ============================================================================
# STEP 4: CALCULATE TEMPORAL ENTROPY FOR EACH MINUTE OF DAY
# ============================================================================
print("\nSTEP 4: Calculating Shannon Entropy for Each Minute")
print("-"*90)

def calculate_entropy(series):
    """Compute Shannon entropy of a series of categorical activity levels."""
    values = series.dropna()

    if len(values) == 0:
        return np.nan  # no data for this minute

    counts = values.value_counts()
    total = len(values)

    entropy = 0
    for count in counts:
        p = count / total
        entropy -= p * np.log2(p)

    return entropy

print("Processing FS1987...")
df_entropy_1987 = df1.groupby('minute_of_day')['activity_level'].apply(calculate_entropy).reset_index()
df_entropy_1987.columns = ['minute_of_day', 'entropy']
df_entropy_1987['hour'] = df_entropy_1987['minute_of_day'] // 60

print("Processing FS2116...")
df_entropy_2116 = df2.groupby('minute_of_day')['activity_level'].apply(calculate_entropy).reset_index()
df_entropy_2116.columns = ['minute_of_day', 'entropy']
df_entropy_2116['hour'] = df_entropy_2116['minute_of_day'] // 60

print("✓ Entropy calculated for all 1440 minutes where data exists")

# ============================================================================
# STEP 5: CALCULATE AVERAGE ENTROPY
# ============================================================================
print("\nSTEP 5: RESULTS - Average Temporal Entropy")
print("="*90)

avg_1987 = df_entropy_1987['entropy'].mean()
std_1987 = df_entropy_1987['entropy'].std()

avg_2116 = df_entropy_2116['entropy'].mean()
std_2116 = df_entropy_2116['entropy'].std()

print(f"\nParticipant FS1987:")
print(f"  Average Temporal Entropy: {avg_1987:.4f} bits")
print(f"  Standard Deviation:       {std_1987:.4f} bits")

print(f"\nParticipant FS2116:")
print(f"  Average Temporal Entropy: {avg_2116:.4f} bits")
print(f"  Standard Deviation:       {std_2116:.4f} bits")

difference = avg_1987 - avg_2116
print(f"\nEntropy Difference (FS1987 - FS2116): {difference:.4f} bits")

if avg_1987 < avg_2116:
    print("→ FS1987 shows LOWER entropy (more predictable routine)")
    print("→ FS2116 shows HIGHER entropy (more variable routine)")
else:
    print("→ FS2116 shows LOWER entropy (more predictable routine)")
    print("→ FS1987 shows HIGHER entropy (more variable routine)")

# ============================================================================
# STEP 6: INTERPRETATION (VALID)
# ============================================================================
print("\nSTEP 6: INTERPRETATION")
print("="*90)

print("INTERPRETATION OF ENTROPY VALUES:")
print("  • Lower entropy → more routine regularity and predictable daily structure")
print("  • Higher entropy → more behavioral variability across days")
print("  • Comparison of average entropy quantifies how structured each participant's routine is")

# ============================================================================
# STEP 7: SAVE RESULTS
# ============================================================================
print("\nSTEP 7: Saving Results to CSV files")
print("-"*90)

df_entropy_1987.to_csv('FS1987_temporal_entropy.csv', index=False)
df_entropy_2116.to_csv('FS2116_temporal_entropy.csv', index=False)

summary = pd.DataFrame({
    'Participant': ['FS1987', 'FS2116'],
    'Average_Entropy': [avg_1987, avg_2116],
    'Std_Dev': [std_1987, std_2116]
})
summary.to_csv('temporal_entropy_summary.csv', index=False)

print("✓ Saved: FS1987_temporal_entropy.csv")
print("✓ Saved: FS2116_temporal_entropy.csv")
print("✓ Saved: temporal_entropy_summary.csv")

# ============================================================================
# STEP 8: VISUALIZATIONS
# ============================================================================
print("\nSTEP 8: Creating Visualizations")
print("-"*90)

# Figure 1 — Temporal entropy profiles
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8))

# FS1987
hours_1987 = df_entropy_1987['minute_of_day'] / 60
ax1.plot(hours_1987, df_entropy_1987['entropy'], color='#2E86AB', linewidth=1.4)
ax1.axhline(avg_1987, color='red', linestyle='--', linewidth=2,
            label=f'Avg: {avg_1987:.4f} bits')
ax1.set_title('FS1987 — Minute-Level Temporal Entropy', fontsize=13)
ax1.set_ylabel('Entropy (bits)')
ax1.legend()

# FS2116
hours_2116 = df_entropy_2116['minute_of_day'] / 60
ax2.plot(hours_2116, df_entropy_2116['entropy'], color='#A23B72', linewidth=1.4)
ax2.axhline(avg_2116, color='red', linestyle='--', linewidth=2,
            label=f'Avg: {avg_2116:.4f} bits')
ax2.set_title('FS2116 — Minute-Level Temporal Entropy', fontsize=13)
ax2.set_ylabel('Entropy (bits)')
ax2.set_xlabel('Hour of Day')
ax2.legend()

plt.tight_layout()
plt.savefig('temporal_entropy_profile.png', dpi=300)
print("✓ Saved: temporal_entropy_profile.png")

# Figure 2 — Average Entropy Comparison
fig, ax = plt.subplots(figsize=(7, 6))
bars = ax.bar(['FS1987', 'FS2116'], [avg_1987, avg_2116],
              color=['#2E86AB', '#A23B72'], edgecolor='black')

for bar, val in zip(bars, [avg_1987, avg_2116]):
    ax.text(bar.get_x() + bar.get_width()/2., val, f'{val:.4f}',
            ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_title('Comparison of Routine Regularity (Entropy)', fontsize=14)
ax.set_ylabel('Average Entropy (bits)')
plt.tight_layout()
plt.savefig('entropy_comparison.png', dpi=300)
print("✓ Saved: entropy_comparison.png")

# ============================================================================
print("\n" + "="*90)
print("ANALYSIS COMPLETE — RESULTS READY FOR PAPER & PRESENTATION")
print("="*90)
print("\n")
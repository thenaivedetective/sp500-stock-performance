"""
NYC Food Desert Project - Phase 2: Information Theory Analysis
==============================================================

This script calculates information theory measures on the NYC food access data:
- Shannon Entropy (uncertainty/randomness)
- KL Divergence (differences between boroughs)
- Normalized Entropy (interpretability)
- Statistical summaries

Data Input: Files from Phase 1 (food_access_categories.csv)
Output: Entropy calculations, visualizations, and analysis

Author: Created for SSIE-500 Final Project
Date: November 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import entropy
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("NYC FOOD DESERT PROJECT - PHASE 2: INFORMATION THEORY ANALYSIS")
print("="*80)
print()

# ============================================================================
# STEP 1: LOAD DATA FROM PHASE 1
# ============================================================================

print("STEP 1: Loading Data from Phase 1")
print("-" * 80)

try:
    df = pd.read_csv('food_access_categories.csv')
    print(f"✓ Loaded data: {len(df)} zip codes")
    print(f"  Columns: {', '.join(df.columns.tolist())}")
    print()
except FileNotFoundError:
    print("✗ Error: food_access_categories.csv not found!")
    print("  Please run Phase 1 first (phase1_data_collection.py)")
    exit(1)

# ============================================================================
# STEP 2: CALCULATE SHANNON ENTROPY FOR OVERALL NYC
# ============================================================================

print("STEP 2: Calculating Shannon Entropy for Overall NYC")
print("-" * 80)

# Count zip codes in each category
category_counts = df['access_category'].value_counts()
total_zips = len(df)

# Convert to probabilities
probabilities = category_counts / total_zips

print("Food Access Distribution (Probabilities):")
print("-" * 40)
for category in ['Desert', 'Limited', 'Adequate', 'Abundant']:
    if category in probabilities:
        prob = probabilities[category]
        count = category_counts[category]
        print(f"  {category:12} p = {prob:.4f} ({count:3} zip codes, {prob*100:5.1f}%)")
print()

# Calculate Shannon Entropy (base 2 for bits)
H_nyc = entropy(probabilities.values, base=2)

# Maximum possible entropy with 4 categories
H_max = np.log2(4)

# Normalized entropy (as percentage)
H_normalized = (H_nyc / H_max) * 100

print("Shannon Entropy Results:")
print("-" * 40)
print(f"  H(NYC) = {H_nyc:.4f} bits")
print(f"  H_max  = {H_max:.4f} bits (with 4 categories)")
print(f"  Normalized = {H_normalized:.2f}%")
print()

# Interpretation
print("Interpretation:")
print("-" * 40)
if H_normalized < 30:
    interpretation = "Very Low - Highly predictable (strong dominant category)"
elif H_normalized < 50:
    interpretation = "Low-Medium - Moderately predictable (one category dominates)"
elif H_normalized < 70:
    interpretation = "Medium-High - Balanced with variation"
else:
    interpretation = "High - Nearly random (all categories roughly equal)"

print(f"  {interpretation}")
print()

# ============================================================================
# STEP 3: CALCULATE SHANNON ENTROPY BY BOROUGH
# ============================================================================

print("STEP 3: Calculating Shannon Entropy by Borough")
print("-" * 80)

borough_entropy = []

for borough in ['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island']:
    # Filter data for this borough
    borough_data = df[df['borough'] == borough]
    
    if len(borough_data) == 0:
        continue
    
    # Count categories
    borough_counts = borough_data['access_category'].value_counts()
    borough_probs = borough_counts / len(borough_data)
    
    # Calculate entropy
    H_borough = entropy(borough_probs.values, base=2)
    H_norm_borough = (H_borough / H_max) * 100
    
    borough_entropy.append({
        'borough': borough,
        'zip_codes': len(borough_data),
        'entropy_bits': H_borough,
        'normalized_pct': H_norm_borough,
        'dominant_category': borough_probs.idxmax(),
        'dominant_pct': borough_probs.max() * 100
    })
    
    print(f"{borough:15} H = {H_borough:.4f} bits ({H_norm_borough:5.1f}%) | "
          f"{len(borough_data):2} zips | "
          f"Dominant: {borough_probs.idxmax()} ({borough_probs.max()*100:.1f}%)")

print()

# Create DataFrame
df_borough_entropy = pd.DataFrame(borough_entropy)
df_borough_entropy = df_borough_entropy.sort_values('entropy_bits', ascending=False)

# ============================================================================
# STEP 4: CALCULATE KL DIVERGENCE (COMPARE BOROUGHS)
# ============================================================================

print("STEP 4: Calculating KL Divergence (Borough Comparisons)")
print("-" * 80)

# NYC overall distribution as reference
nyc_probs = probabilities.copy()

# Make sure we have all 4 categories (add tiny probability if missing)
all_categories = ['Desert', 'Limited', 'Adequate', 'Abundant']
for cat in all_categories:
    if cat not in nyc_probs:
        nyc_probs[cat] = 1e-10

nyc_probs = nyc_probs[all_categories]  # Order consistently

print("Comparing each borough to NYC average:")
print("-" * 40)

kl_divergences = []

for borough in ['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island']:
    borough_data = df[df['borough'] == borough]
    
    if len(borough_data) == 0:
        continue
    
    # Get borough distribution
    borough_counts = borough_data['access_category'].value_counts()
    borough_probs = borough_counts / len(borough_data)
    
    # Add missing categories with tiny probability
    for cat in all_categories:
        if cat not in borough_probs:
            borough_probs[cat] = 1e-10
    
    borough_probs = borough_probs[all_categories]  # Order consistently
    
    # Calculate KL divergence: KL(Borough || NYC)
    kl_div = np.sum(borough_probs * np.log2(borough_probs / nyc_probs))
    
    kl_divergences.append({
        'borough': borough,
        'kl_divergence': kl_div
    })
    
    # Interpretation
    if kl_div < 0.1:
        diff_level = "Very similar to NYC average"
    elif kl_div < 0.3:
        diff_level = "Slightly different from NYC average"
    elif kl_div < 0.7:
        diff_level = "Moderately different from NYC average"
    else:
        diff_level = "Very different from NYC average"
    
    print(f"  {borough:15} KL = {kl_div:.4f} bits | {diff_level}")

print()

df_kl = pd.DataFrame(kl_divergences).sort_values('kl_divergence', ascending=False)

# ============================================================================
# STEP 5: DETAILED STATISTICS BY BOROUGH
# ============================================================================

print("STEP 5: Detailed Borough Statistics")
print("-" * 80)

borough_details = []

for borough in ['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island']:
    borough_data = df[df['borough'] == borough]
    
    if len(borough_data) == 0:
        continue
    
    category_dist = borough_data['access_category'].value_counts()
    
    details = {
        'Borough': borough,
        'Total_Zips': len(borough_data),
        'Total_Stores': int(borough_data['store_count'].sum()),
        'Avg_Stores_per_Zip': borough_data['store_count'].mean(),
        'Desert_Zips': category_dist.get('Desert', 0),
        'Limited_Zips': category_dist.get('Limited', 0),
        'Adequate_Zips': category_dist.get('Adequate', 0),
        'Abundant_Zips': category_dist.get('Abundant', 0),
        'Desert_Pct': (category_dist.get('Desert', 0) / len(borough_data)) * 100,
        'Abundant_Pct': (category_dist.get('Abundant', 0) / len(borough_data)) * 100
    }
    
    borough_details.append(details)

df_details = pd.DataFrame(borough_details)

print(df_details.to_string(index=False))
print()

# ============================================================================
# STEP 6: CREATE VISUALIZATIONS
# ============================================================================

print("STEP 6: Creating Visualizations")
print("-" * 80)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 12)

# Create figure with subplots
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('NYC Food Desert Information Theory Analysis', fontsize=16, fontweight='bold')

# Plot 1: Overall NYC Distribution
ax1 = axes[0, 0]
categories = ['Desert', 'Limited', 'Adequate', 'Abundant']
colors = ['#d32f2f', '#ff6f00', '#fbc02d', '#388e3c']
counts = [category_counts.get(cat, 0) for cat in categories]

bars1 = ax1.bar(categories, counts, color=colors, edgecolor='black', linewidth=1.5)
ax1.set_title(f'NYC Food Access Distribution\nH = {H_nyc:.3f} bits ({H_normalized:.1f}% of max)', 
              fontsize=12, fontweight='bold')
ax1.set_ylabel('Number of Zip Codes', fontsize=11)
ax1.set_xlabel('Access Category', fontsize=11)

# Add count labels on bars
for bar, count in zip(bars1, counts):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(count)}\n({count/total_zips*100:.1f}%)',
             ha='center', va='bottom', fontsize=10, fontweight='bold')

# Plot 2: Entropy by Borough
ax2 = axes[0, 1]
boroughs = df_borough_entropy['borough'].tolist()
entropies = df_borough_entropy['entropy_bits'].tolist()

bars2 = ax2.barh(boroughs, entropies, color='steelblue', edgecolor='black', linewidth=1.5)
ax2.set_title('Shannon Entropy by Borough', fontsize=12, fontweight='bold')
ax2.set_xlabel('Entropy (bits)', fontsize=11)
ax2.axvline(H_nyc, color='red', linestyle='--', linewidth=2, label=f'NYC Average ({H_nyc:.3f})')
ax2.legend()

# Add value labels
for bar, ent, norm_pct in zip(bars2, entropies, df_borough_entropy['normalized_pct']):
    width = bar.get_width()
    ax2.text(width, bar.get_y() + bar.get_height()/2.,
             f' {ent:.3f} ({norm_pct:.1f}%)',
             ha='left', va='center', fontsize=10, fontweight='bold')

# Plot 3: KL Divergence
ax3 = axes[1, 0]
kl_boroughs = df_kl['borough'].tolist()
kl_values = df_kl['kl_divergence'].tolist()

bars3 = ax3.barh(kl_boroughs, kl_values, color='coral', edgecolor='black', linewidth=1.5)
ax3.set_title('KL Divergence from NYC Average\n(Higher = More Different)', 
              fontsize=12, fontweight='bold')
ax3.set_xlabel('KL Divergence (bits)', fontsize=11)

# Add value labels
for bar, kl in zip(bars3, kl_values):
    width = bar.get_width()
    ax3.text(width, bar.get_y() + bar.get_height()/2.,
             f' {kl:.4f}',
             ha='left', va='center', fontsize=10, fontweight='bold')

# Plot 4: Borough Distribution Comparison
ax4 = axes[1, 1]
borough_names = df_details['Borough'].tolist()
desert_pcts = df_details['Desert_Pct'].tolist()
abundant_pcts = df_details['Abundant_Pct'].tolist()

x = np.arange(len(borough_names))
width = 0.35

bars_desert = ax4.bar(x - width/2, desert_pcts, width, label='Desert %', 
                       color='#d32f2f', edgecolor='black', linewidth=1)
bars_abundant = ax4.bar(x + width/2, abundant_pcts, width, label='Abundant %', 
                         color='#388e3c', edgecolor='black', linewidth=1)

ax4.set_title('Desert vs Abundant by Borough', fontsize=12, fontweight='bold')
ax4.set_ylabel('Percentage of Zip Codes', fontsize=11)
ax4.set_xticks(x)
ax4.set_xticklabels(borough_names, rotation=45, ha='right')
ax4.legend()
ax4.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('entropy_visualizations.png', dpi=300, bbox_inches='tight')
print("✓ Saved visualization to 'entropy_visualizations.png'")
print()

# ============================================================================
# STEP 7: SAVE RESULTS
# ============================================================================

print("STEP 7: Saving Results")
print("-" * 80)

# Save entropy results
entropy_results = pd.DataFrame([{
    'metric': 'NYC Overall Shannon Entropy',
    'value_bits': H_nyc,
    'normalized_pct': H_normalized,
    'interpretation': interpretation
}])

df_borough_entropy.to_csv('shannon_entropy_by_borough.csv', index=False)
print("✓ Saved 'shannon_entropy_by_borough.csv'")

df_kl.to_csv('kl_divergence_results.csv', index=False)
print("✓ Saved 'kl_divergence_results.csv'")

df_details.to_csv('borough_detailed_statistics.csv', index=False)
print("✓ Saved 'borough_detailed_statistics.csv'")

# ============================================================================
# STEP 8: GENERATE COMPREHENSIVE SUMMARY
# ============================================================================

print()
print("STEP 8: Generating Comprehensive Summary")
print("-" * 80)

summary = f"""
{'='*80}
NYC FOOD DESERT INFORMATION THEORY ANALYSIS - PHASE 2 RESULTS
{'='*80}

ANALYSIS COMPLETED: November 2025
Data Source: Phase 1 Collection (11,472 food stores, 190 zip codes)
Methods: Shannon Entropy, KL Divergence, Information Theory

{'='*80}
OVERALL NYC SHANNON ENTROPY
{'='*80}

Shannon Entropy: H = {H_nyc:.4f} bits
Maximum Entropy: H_max = {H_max:.4f} bits (4 categories)
Normalized Entropy: {H_normalized:.2f}% of maximum

Interpretation: {interpretation}

Food Access Distribution:
"""

for category in ['Desert', 'Limited', 'Adequate', 'Abundant']:
    if category in category_counts:
        count = category_counts[category]
        pct = (count / total_zips) * 100
        summary += f"  {category:12} {count:3} zip codes ({pct:5.1f}%)\n"

summary += f"""
{'='*80}
SHANNON ENTROPY BY BOROUGH
{'='*80}

"""

for _, row in df_borough_entropy.iterrows():
    summary += f"{row['borough']:15} H = {row['entropy_bits']:.4f} bits ({row['normalized_pct']:5.1f}%)\n"
    summary += f"                Dominant: {row['dominant_category']} ({row['dominant_pct']:.1f}%)\n"
    summary += f"                Zip codes: {int(row['zip_codes'])}\n\n"

summary += f"""
{'='*80}
KL DIVERGENCE ANALYSIS (Comparison to NYC Average)
{'='*80}

"""

for _, row in df_kl.iterrows():
    summary += f"{row['borough']:15} KL = {row['kl_divergence']:.4f} bits\n"

summary += f"""
Interpretation:
- Higher KL divergence = More different from NYC average
- Lower KL divergence = More similar to NYC average

{'='*80}
KEY FINDINGS
{'='*80}

1. OVERALL NYC ENTROPY ({H_normalized:.1f}%):
   - Indicates {"low-medium" if H_normalized < 50 else "medium-high" if H_normalized < 70 else "high"} uncertainty in food access
   - System is {"relatively organized" if H_normalized < 50 else "moderately varied" if H_normalized < 70 else "highly chaotic"}
   - {category_counts.get('Abundant', 0)} out of {total_zips} zip codes ({category_counts.get('Abundant', 0)/total_zips*100:.1f}%) have abundant access

2. BOROUGH VARIATION:
   - Highest entropy: {df_borough_entropy.iloc[0]['borough']} ({df_borough_entropy.iloc[0]['entropy_bits']:.3f} bits)
     → Most internal variation/unpredictability
   - Lowest entropy: {df_borough_entropy.iloc[-1]['borough']} ({df_borough_entropy.iloc[-1]['entropy_bits']:.3f} bits)
     → Most uniform/predictable

3. KL DIVERGENCE (Outlier Detection):
   - Most different from NYC average: {df_kl.iloc[0]['borough']} (KL = {df_kl.iloc[0]['kl_divergence']:.3f})
   - Most similar to NYC average: {df_kl.iloc[-1]['borough']} (KL = {df_kl.iloc[-1]['kl_divergence']:.3f})

4. FOOD DESERTS:
   - Total: {category_counts.get('Desert', 0)} zip codes ({category_counts.get('Desert', 0)/total_zips*100:.1f}%)
   - Concentrated in specific boroughs (see detailed statistics)

{'='*80}
WHAT THESE NUMBERS MEAN
{'='*80}

Shannon Entropy (H = {H_nyc:.3f} bits, {H_normalized:.1f}%):
→ At {H_normalized:.1f}% of maximum, NYC food access is {"more predictable than random" if H_normalized < 50 else "moderately varied"}
→ If you pick a random zip code, you can guess "{probabilities.idxmax()}" with {probabilities.max()*100:.1f}% accuracy
→ This {"low-medium" if H_normalized < 50 else "medium-high"} entropy suggests {"systematic patterns exist" if H_normalized < 50 else "significant variation exists"}

KL Divergence:
→ Shows which boroughs have DIFFERENT food access patterns
→ High KL = Need borough-specific policies
→ Low KL = Similar to city average, general policies work

{'='*80}
POLICY IMPLICATIONS
{'='*80}

1. Target the {category_counts.get('Desert', 0)} food desert zip codes for intervention
2. {df_kl.iloc[0]['borough']} requires different approach (highest KL divergence)
3. {df_borough_entropy.iloc[0]['borough']} has highest internal variation (H = {df_borough_entropy.iloc[0]['entropy_bits']:.3f})
   - May need multiple sub-borough strategies
4. {df_borough_entropy.iloc[-1]['borough']} is most uniform (H = {df_borough_entropy.iloc[-1]['entropy_bits']:.3f})
   - One-size-fits-all policy likely effective

{'='*80}
FILES CREATED IN PHASE 2
{'='*80}

1. entropy_visualizations.png - Comprehensive visual analysis
2. shannon_entropy_by_borough.csv - Entropy calculations
3. kl_divergence_results.csv - Borough comparisons
4. borough_detailed_statistics.csv - Detailed breakdowns
5. information_theory_summary.txt - This summary

{'='*80}
NEXT STEPS
{'='*80}

→ Phase 3: Add demographic data (income, race, etc.)
→ Calculate Mutual Information (income ↔ food access)
→ Analyze Mamdani election data (food policy ↔ voting)
→ Create geographic visualizations (maps)

{'='*80}
Phase 2: Information Theory Analysis - COMPLETE ✓
{'='*80}
"""

with open('information_theory_summary.txt', 'w') as f:
    f.write(summary)

print(summary)

print("="*80)
print("PHASE 2 COMPLETE! All analysis and visualizations have been created.")
print("="*80)

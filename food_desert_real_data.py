import pandas as pd
import numpy as np
import requests
from scipy.stats import entropy
import matplotlib.pyplot as plt
import seaborn as sns
import json
import time

print("=" * 70)
print("NYC FOOD DESERT ANALYSIS - SHANNON ENTROPY (REAL DATA)")
print("=" * 70)
print()

print("STEP 1: Fetching REAL NYC Supermarket Data from NY State API...")
print("-" * 70)

# Correct county names in ALL CAPS
nyc_counties = ['BRONX', 'KINGS', 'NEW YORK', 'QUEENS', 'RICHMOND']

supermarket_url = "https://data.ny.gov/resource/9a8c-vfzj.json"

all_stores = []

print("Fetching data for NYC boroughs...")
for county in nyc_counties:
    print(f"  Fetching {county} county...", end=" ")
    try:
        params = {
            "county": county,
            "$limit": 5000
        }
        
        response = requests.get(supermarket_url, params=params, timeout=30)
        response.raise_for_status()
        
        county_stores = response.json()
        all_stores.extend(county_stores)
        print(f"✓ {len(county_stores)} stores")
        
        time.sleep(0.5)
        
    except Exception as e:
        print(f"✗ Error: {e}")

print()
print(f"✓ Total stores fetched: {len(all_stores)}")
print()

if len(all_stores) == 0:
    print("ERROR: Failed to fetch any data from the API.")
    print("Please check internet connection or API availability.")
    exit(1)

df_stores = pd.DataFrame(all_stores)

print("Sample of REAL data:")
print(df_stores.head(10))
print()
print(f"Columns available: {list(df_stores.columns)}")
print()
print(f"Total records: {len(df_stores)}")
print()

with open('raw_supermarket_data.json', 'w') as f:
    json.dump(all_stores, f, indent=2)
print("✓ Raw data saved to: raw_supermarket_data.json")
print()

print("=" * 70)
print("STEP 2: Data Cleaning")
print("-" * 70)

print(f"Initial records: {len(df_stores)}")

df_stores_clean = df_stores.copy()

if 'county' in df_stores_clean.columns:
    print(f"\nStores by county:")
    print(df_stores_clean['county'].value_counts())
    print()

borough_mapping = {
    'NEW YORK': 'Manhattan',
    'KINGS': 'Brooklyn',
    'QUEENS': 'Queens',
    'BRONX': 'Bronx',
    'RICHMOND': 'Staten Island'
}

if 'county' in df_stores_clean.columns:
    df_stores_clean['borough'] = df_stores_clean['county'].map(borough_mapping)
else:
    df_stores_clean['borough'] = 'Unknown'

if 'establishment_type' in df_stores_clean.columns:
    print(f"Establishment types:")
    print(df_stores_clean['establishment_type'].value_counts().head(10))
    print()

if 'zip_code' in df_stores_clean.columns:
    df_stores_clean = df_stores_clean[df_stores_clean['zip_code'].notna()]
    df_stores_clean['zip_code'] = df_stores_clean['zip_code'].astype(str).str[:5]
    print(f"After cleaning zip codes: {len(df_stores_clean)} stores")
else:
    print("ERROR: No zip_code field in data")
    exit(1)

print(f"\nFinal cleaned dataset: {len(df_stores_clean)} stores")
print(f"Number of unique zip codes: {df_stores_clean['zip_code'].nunique()}")
print()

print("Stores by borough:")
print(df_stores_clean['borough'].value_counts())
print()

df_stores_clean.to_csv('cleaned_supermarket_data.csv', index=False)
print("✓ Cleaned data saved to: cleaned_supermarket_data.csv")
print()

print("=" * 70)
print("STEP 3: SHANNON ENTROPY CALCULATION")
print("=" * 70)
print()

print("3A. Calculating stores per zip code...")
print("-" * 70)

stores_per_zip = df_stores_clean['zip_code'].value_counts().sort_index()

print(f"\nTotal zip codes analyzed: {len(stores_per_zip)}")
print()
print(f"Top 10 zip codes with most stores:")
print(stores_per_zip.head(10))
print()
print(f"Bottom 10 zip codes with fewest stores:")
print(stores_per_zip.tail(10))
print()

stores_per_zip.to_csv('stores_per_zipcode.csv', header=['store_count'])
print("✓ Saved to: stores_per_zipcode.csv")
print()

print("3B. Categorizing Food Access Levels...")
print("-" * 70)

population_avg = 30000

stores_per_10k = (stores_per_zip / population_avg) * 10000

print(f"Using estimated average population per zip: {population_avg:,}")
print(f"(Note: Actual zip code populations vary significantly)")
print()

def categorize_access(stores_per_10k_pop):
    """
    Categorize food access based on store density
    Based on USDA food desert criteria adapted for urban areas
    """
    if stores_per_10k_pop >= 5:
        return 'abundant'
    elif stores_per_10k_pop >= 3:
        return 'adequate'
    elif stores_per_10k_pop >= 1:
        return 'limited'
    else:
        return 'desert'

access_categories = stores_per_10k.apply(categorize_access)

category_counts = access_categories.value_counts()
print("Food Access Categories (REAL NYC DATA):")
print(category_counts)
print()

category_distribution = category_counts / len(access_categories)
print("Distribution (proportions):")
for cat in ['desert', 'limited', 'adequate', 'abundant']:
    if cat in category_distribution:
        prop = category_distribution[cat]
        print(f"  {cat:10s}: {prop:.3f} ({prop*100:5.1f}%)")
print()

print("3C. SHANNON ENTROPY CALCULATION")
print("-" * 70)

probabilities = category_distribution.values

H = entropy(probabilities, base=2)

print(f"\n{'='*70}")
print(f"🎯 SHANNON ENTROPY (H): {H:.4f} bits")
print(f"   (Calculated from REAL NYC supermarket data)")
print(f"{'='*70}")
print()

max_entropy = np.log2(len(probabilities))
normalized_entropy = H / max_entropy

print(f"Maximum possible entropy (with {len(probabilities)} categories): {max_entropy:.4f} bits")
print(f"Normalized entropy: {normalized_entropy:.2%}")
print()

summary_stats = {
    'Shannon Entropy (bits)': H,
    'Maximum Entropy (bits)': max_entropy,
    'Normalized Entropy (%)': normalized_entropy * 100,
    'Number of Categories': len(probabilities),
    'Total Zip Codes': len(access_categories),
    'Total Stores': len(df_stores_clean)
}

summary_df = pd.DataFrame([summary_stats])
summary_df.to_csv('entropy_summary.csv', index=False)
print("✓ Summary statistics saved to: entropy_summary.csv")
print()

print("=" * 70)
print("INTERPRETATION OF REAL DATA")
print("=" * 70)
print()
print("What does this entropy value mean?")
print()
print(f"• Entropy = {H:.4f} bits")
print(f"• Maximum = {max_entropy:.4f} bits (perfect disorder)")
print(f"• Minimum = 0.00 bits (perfect order)")
print(f"• Normalized = {normalized_entropy:.1%} of maximum")
print()

if normalized_entropy > 0.8:
    interpretation = "HIGH ENTROPY - Very chaotic/unpredictable distribution"
    detail = "Zip codes are spread relatively evenly across all access categories."
    implication = "Significant INEQUALITY - some areas have great access, others have terrible access, with high variation."
elif normalized_entropy > 0.5:
    interpretation = "MEDIUM ENTROPY - Moderate variation"
    detail = "Some concentration in certain categories, but still substantial variation."
    implication = "Mixed food access across NYC with noticeable differences between neighborhoods."
else:
    interpretation = "LOW ENTROPY - More uniform distribution"
    detail = "Most zip codes fall into one or two categories."
    implication = "More predictable access (either consistently good or consistently bad)."

print(f"📊 CLASSIFICATION: {interpretation}")
print()
print(f"   WHAT IT MEANS: {detail}")
print()
print(f"   SOCIAL IMPLICATION: {implication}")
print()

print("=" * 70)
print("BONUS: Entropy by Borough (REAL DATA)")
print("=" * 70)
print()

if 'borough' in df_stores_clean.columns:
    
    borough_entropy = {}
    borough_details = {}
    
    for borough in sorted(df_stores_clean['borough'].unique()):
        if pd.notna(borough) and borough != 'Unknown':
            borough_stores = df_stores_clean[df_stores_clean['borough'] == borough]
            borough_zip_counts = borough_stores['zip_code'].value_counts()
            
            if len(borough_zip_counts) >= 2:
                borough_stores_per_10k = (borough_zip_counts / population_avg) * 10000
                borough_categories = borough_stores_per_10k.apply(categorize_access)
                borough_dist = borough_categories.value_counts(normalize=True)
                
                if len(borough_dist) > 1:
                    H_borough = entropy(borough_dist.values, base=2)
                    max_H_borough = np.log2(len(borough_dist))
                    
                    borough_entropy[borough] = H_borough
                    
                    print(f"{borough}:")
                    print(f"  Entropy: {H_borough:.4f} bits ({H_borough/max_H_borough:.1%} of max)")
                    print(f"  Zip codes: {len(borough_zip_counts)}")
                    print(f"  Total stores: {len(borough_stores)}")
                    print(f"  Distribution: {dict(borough_categories.value_counts())}")
                    print()
                    
                    borough_details[borough] = {
                        'entropy': H_borough,
                        'zip_codes': len(borough_zip_counts),
                        'total_stores': len(borough_stores),
                        'categories': dict(borough_categories.value_counts())
                    }
    
    if borough_entropy:
        borough_df = pd.DataFrame([
            {'Borough': k, 'Entropy': v} for k, v in borough_entropy.items()
        ])
        borough_df = borough_df.sort_values('Entropy', ascending=False)
        borough_df.to_csv('borough_entropy.csv', index=False)
        print("✓ Borough entropy saved to: borough_entropy.csv")
        print()

print("=" * 70)
print("VISUALIZATIONS")
print("=" * 70)

fig = plt.figure(figsize=(16, 5))

ax1 = plt.subplot(1, 3, 1)
colors_bar = {'desert': 'red', 'limited': 'orange', 'adequate': 'yellow', 'abundant': 'green'}
ordered_categories = ['desert', 'limited', 'adequate', 'abundant']
counts_ordered = [category_counts.get(cat, 0) for cat in ordered_categories]
colors_list = [colors_bar[cat] for cat in ordered_categories]

ax1.bar(ordered_categories, counts_ordered, color=colors_list, edgecolor='black', linewidth=1.5)
ax1.set_title('Food Access Distribution - REAL NYC DATA', fontsize=12, fontweight='bold')
ax1.set_xlabel('Access Category', fontsize=11)
ax1.set_ylabel('Number of Zip Codes', fontsize=11)
ax1.grid(axis='y', alpha=0.3)

ax2 = plt.subplot(1, 3, 2)
pie_data = [category_counts.get(cat, 0) for cat in ordered_categories]
ax2.pie(pie_data, labels=ordered_categories, autopct='%1.1f%%', 
        colors=colors_list, startangle=90, textprops={'fontsize': 10})
ax2.set_title(f'Food Access Categories\n(Entropy = {H:.4f} bits)', fontsize=12, fontweight='bold')

ax3 = plt.subplot(1, 3, 3)
ax3.barh(['Current\nEntropy', 'Maximum\nEntropy'], [H, max_entropy], 
         color=['steelblue', 'lightgray'], edgecolor='black', linewidth=1.5)
ax3.set_xlim(0, max_entropy * 1.1)
ax3.set_xlabel('Entropy (bits)', fontsize=11)
ax3.set_title(f'Entropy: {normalized_entropy:.1%} of Maximum', fontsize=12, fontweight='bold')
ax3.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('shannon_entropy_results.png', dpi=300, bbox_inches='tight')
print("✓ Visualization saved to: shannon_entropy_results.png")
print()

print("=" * 70)
print("ANALYSIS COMPLETE - USING REAL NYC DATA!")
print("=" * 70)
print()
print("Files created:")
print("  1. raw_supermarket_data.json - REAL data from NY State API")
print("  2. cleaned_supermarket_data.csv - Cleaned dataset")
print("  3. stores_per_zipcode.csv - Store counts by zip code")
print("  4. entropy_summary.csv - Summary statistics")
print("  5. borough_entropy.csv - Entropy by borough")
print("  6. shannon_entropy_results.png - Visualizations")
print()
print(f"📊 KEY FINDING: NYC food access Shannon entropy = {H:.4f} bits")
print(f"   Based on {len(df_stores_clean)} REAL supermarket locations")
print(f"   Across {len(access_categories)} zip codes")
print(f"   Normalized entropy: {normalized_entropy:.1%} of maximum")
print()
print("=" * 70)
print("DATA SOURCE:")
print("NY State Open Data - Retail Food Stores")
print("https://data.ny.gov/Economic-Development/Retail-Food-Stores/9a8c-vfzj")
print("=" * 70)

import pandas as pd
import numpy as np
import requests
from scipy.stats import entropy
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import json

print("=" * 70)
print("NYC FOOD DESERT ANALYSIS - SHANNON ENTROPY CALCULATION")
print("=" * 70)
print()

print("STEP 1: Fetching NYC Supermarket Data...")
print("-" * 70)

try:
    # Try simpler approach - fetch more records without complex WHERE clause
    supermarket_url = "https://data.ny.gov/resource/9a8c-vfzj.json"
    
    print("Fetching data from NY State Open Data API...")
    
    params = {
        "$limit": 50000  # Increase limit
    }
    
    response = requests.get(supermarket_url, params=params, timeout=30)
    response.raise_for_status()
    
    all_stores = response.json()
    
    print(f"✓ Fetched {len(all_stores)} stores from NY State")
    
    # Filter for NYC counties
    nyc_counties = ['Bronx', 'Kings', 'New York', 'Queens', 'Richmond']
    supermarkets_data = [store for store in all_stores if store.get('county') in nyc_counties]
    
    print(f"✓ Filtered to {len(supermarkets_data)} stores in NYC counties")
    print()
    
except Exception as e:
    print(f"✗ Error fetching data: {e}")
    print("This might be due to API rate limits or connectivity issues.")
    print()
    supermarkets_data = []

if len(supermarkets_data) == 0:
    print("⚠ WARNING: No data fetched from API")
    print("Creating sample data for demonstration purposes...")
    print()
    
    # Create realistic sample data based on NYC patterns
    np.random.seed(42)
    
    zip_codes_manhattan = [10001, 10002, 10003, 10004, 10005, 10006, 10007, 10009, 10010, 10011, 
                           10012, 10013, 10014, 10016, 10017, 10018, 10019, 10020, 10021, 10022]
    zip_codes_bronx = [10451, 10452, 10453, 10454, 10455, 10456, 10457, 10458, 10459, 10460,
                       10461, 10462, 10463, 10464, 10465, 10466, 10467, 10468, 10469, 10470]
    zip_codes_brooklyn = [11201, 11202, 11203, 11204, 11205, 11206, 11207, 11208, 11209, 11210,
                          11211, 11212, 11213, 11214, 11215, 11216, 11217, 11218, 11219, 11220]
    zip_codes_queens = [11101, 11102, 11103, 11104, 11105, 11106, 11354, 11355, 11356, 11357,
                        11358, 11359, 11360, 11361, 11362, 11363, 11364, 11365, 11366, 11367]
    zip_codes_si = [10301, 10302, 10303, 10304, 10305, 10306, 10307, 10308, 10309, 10310]
    
    all_zips = zip_codes_manhattan + zip_codes_bronx + zip_codes_brooklyn + zip_codes_queens + zip_codes_si
    
    sample_stores = []
    store_id = 1
    
    for zip_code in all_zips:
        # Manhattan gets more stores (wealthy area)
        if zip_code in zip_codes_manhattan:
            num_stores = np.random.randint(8, 20)
        # Bronx gets fewer stores (food desert pattern)
        elif zip_code in zip_codes_bronx:
            num_stores = np.random.randint(1, 8)
        # Brooklyn mixed
        elif zip_code in zip_codes_brooklyn:
            num_stores = np.random.randint(3, 12)
        # Queens mixed
        elif zip_code in zip_codes_queens:
            num_stores = np.random.randint(2, 10)
        # Staten Island fewer
        else:
            num_stores = np.random.randint(2, 7)
        
        for _ in range(num_stores):
            sample_stores.append({
                'entity_name': f'Store {store_id}',
                'zip_code': str(zip_code),
                'county': 'Manhattan' if zip_code in zip_codes_manhattan else
                         'Bronx' if zip_code in zip_codes_bronx else
                         'Brooklyn' if zip_code in zip_codes_brooklyn else
                         'Queens' if zip_code in zip_codes_queens else 'Staten Island'
            })
            store_id += 1
    
    supermarkets_data = sample_stores
    print(f"✓ Created {len(supermarkets_data)} sample stores across {len(all_zips)} NYC zip codes")
    print("  (Note: This is simulated data based on typical NYC food desert patterns)")
    print()

df_stores = pd.DataFrame(supermarkets_data)

print("Sample of data:")
print(df_stores.head(10))
print()
print(f"Columns available: {list(df_stores.columns)}")
print()

with open('raw_supermarket_data.json', 'w') as f:
    json.dump(supermarkets_data, f, indent=2)
print("✓ Raw data saved to: raw_supermarket_data.json")
print()

print("=" * 70)
print("STEP 2: Data Cleaning")
print("-" * 70)

print(f"Initial records: {len(df_stores)}")

df_stores_clean = df_stores.copy()

if 'county' in df_stores_clean.columns:
    print(f"\nStores by borough (county):")
    print(df_stores_clean['county'].value_counts())
    print()

df_stores_clean['borough'] = df_stores_clean['county'] if 'county' in df_stores_clean.columns else 'Unknown'

borough_mapping = {
    'New York': 'Manhattan',
    'Kings': 'Brooklyn',
    'Queens': 'Queens',
    'Bronx': 'Bronx',
    'Richmond': 'Staten Island'
}
df_stores_clean['borough'] = df_stores_clean['borough'].map(borough_mapping).fillna(df_stores_clean['borough'])

if 'zip_code' in df_stores_clean.columns:
    df_stores_clean = df_stores_clean[df_stores_clean['zip_code'].notna()]
    print(f"After removing missing zip codes: {len(df_stores_clean)} stores")

print(f"\nFinal cleaned dataset: {len(df_stores_clean)} stores")
print(f"Number of unique zip codes: {df_stores_clean['zip_code'].nunique() if 'zip_code' in df_stores_clean.columns else 'N/A'}")
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

if 'zip_code' not in df_stores_clean.columns or len(df_stores_clean) == 0:
    print("ERROR: No zip code data available")
    exit(1)

stores_per_zip = df_stores_clean['zip_code'].value_counts().sort_index()

print(f"\nTotal zip codes analyzed: {len(stores_per_zip)}")
print(f"\nZip codes with most stores:")
print(stores_per_zip.head(10))
print()

print(f"Zip codes with fewest stores:")
print(stores_per_zip.tail(10))
print()

stores_per_zip.to_csv('stores_per_zipcode.csv', header=['store_count'])
print("✓ Saved to: stores_per_zipcode.csv")
print()

print("3B. Categorizing Food Access Levels...")
print("-" * 70)

# Estimate: average NYC zip code has ~30,000 people
# We'll calculate stores per 10,000 population
population_avg = 30000

stores_per_10k = (stores_per_zip / population_avg) * 10000

print(f"Using estimated average population per zip: {population_avg:,}")
print()

def categorize_access(stores_per_10k_pop):
    """
    Categorize food access based on store density
    - desert: < 1 store per 10k people
    - limited: 1-3 stores per 10k
    - adequate: 3-5 stores per 10k  
    - abundant: 5+ stores per 10k
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
print("Food Access Categories:")
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

# Get probabilities in a consistent order
probabilities = category_distribution.values

# Calculate Shannon Entropy
H = entropy(probabilities, base=2)

print(f"\n{'='*70}")
print(f"🎯 SHANNON ENTROPY (H): {H:.4f} bits")
print(f"{'='*70}")
print()

# Calculate maximum possible entropy
max_entropy = np.log2(len(probabilities))
normalized_entropy = H / max_entropy

print(f"Maximum possible entropy (with {len(probabilities)} categories): {max_entropy:.4f} bits")
print(f"Normalized entropy: {normalized_entropy:.2%}")
print()

# Create summary statistics
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
print("INTERPRETATION")
print("=" * 70)
print()
print("What does this entropy value mean?")
print()
print(f"• Entropy = {H:.4f} bits")
print(f"• Maximum = {max_entropy:.4f} bits (perfect disorder - all categories equally likely)")
print(f"• Minimum = 0.00 bits (perfect order - all in one category)")
print(f"• Normalized = {normalized_entropy:.1%} of maximum")
print()

if normalized_entropy > 0.8:
    interpretation = "HIGH ENTROPY - Very chaotic/unpredictable distribution"
    detail = "Zip codes are spread relatively evenly across all access categories."
    implication = "This suggests significant INEQUALITY - some areas have great access, others have terrible access, with high variation."
elif normalized_entropy > 0.5:
    interpretation = "MEDIUM ENTROPY - Moderate variation"
    detail = "Some concentration in certain categories, but still substantial variation."
    implication = "Mixed food access across NYC with noticeable differences between neighborhoods."
else:
    interpretation = "LOW ENTROPY - More uniform distribution"
    detail = "Most zip codes fall into one or two categories."
    implication = "More predictable access (either consistently good or consistently bad across most areas)."

print(f"📊 CLASSIFICATION: {interpretation}")
print()
print(f"   WHAT IT MEANS: {detail}")
print()
print(f"   SOCIAL IMPLICATION: {implication}")
print()

print("=" * 70)
print("BONUS: Entropy by Borough")
print("=" * 70)
print()

if 'borough' in df_stores_clean.columns:
    
    borough_entropy = {}
    
    for borough in sorted(df_stores_clean['borough'].unique()):
        if pd.notna(borough) and borough != 'Unknown':
            borough_stores = df_stores_clean[df_stores_clean['borough'] == borough]
            borough_zip_counts = borough_stores['zip_code'].value_counts()
            
            if len(borough_zip_counts) >= 2:  # Need at least 2 zip codes
                borough_stores_per_10k = (borough_zip_counts / population_avg) * 10000
                borough_categories = borough_stores_per_10k.apply(categorize_access)
                borough_dist = borough_categories.value_counts(normalize=True)
                
                if len(borough_dist) > 1:  # Need variation to have entropy
                    H_borough = entropy(borough_dist.values, base=2)
                    max_H_borough = np.log2(len(borough_dist))
                    
                    borough_entropy[borough] = H_borough
                    
                    print(f"{borough}:")
                    print(f"  Entropy: {H_borough:.4f} bits ({H_borough/max_H_borough:.1%} of max)")
                    print(f"  Zip codes: {len(borough_zip_counts)}")
                    print(f"  Distribution: {dict(borough_categories.value_counts())}")
                    print()
    
    # Save borough entropy
    if borough_entropy:
        borough_df = pd.DataFrame([
            {'Borough': k, 'Entropy': v} for k, v in borough_entropy.items()
        ])
        borough_df.to_csv('borough_entropy.csv', index=False)
        print("✓ Borough entropy saved to: borough_entropy.csv")
        print()

print("=" * 70)
print("VISUALIZATIONS")
print("=" * 70)

fig = plt.figure(figsize=(15, 5))

# Plot 1: Bar chart
ax1 = plt.subplot(1, 3, 1)
colors_bar = {'desert': 'red', 'limited': 'orange', 'adequate': 'yellow', 'abundant': 'green'}
ordered_categories = ['desert', 'limited', 'adequate', 'abundant']
counts_ordered = [category_counts.get(cat, 0) for cat in ordered_categories]
colors_list = [colors_bar[cat] for cat in ordered_categories]

ax1.bar(ordered_categories, counts_ordered, color=colors_list, edgecolor='black', linewidth=1.5)
ax1.set_title('Food Access Distribution Across NYC Zip Codes', fontsize=12, fontweight='bold')
ax1.set_xlabel('Access Category', fontsize=11)
ax1.set_ylabel('Number of Zip Codes', fontsize=11)
ax1.grid(axis='y', alpha=0.3)

# Plot 2: Pie chart
ax2 = plt.subplot(1, 3, 2)
pie_data = [category_counts.get(cat, 0) for cat in ordered_categories]
ax2.pie(pie_data, labels=ordered_categories, autopct='%1.1f%%', 
        colors=colors_list, startangle=90, textprops={'fontsize': 10})
ax2.set_title(f'Food Access Categories\n(Entropy = {H:.4f} bits)', fontsize=12, fontweight='bold')

# Plot 3: Entropy visualization
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
print("ANALYSIS COMPLETE!")
print("=" * 70)
print()
print("Files created:")
print("  1. raw_supermarket_data.json - Original/sample data")
print("  2. cleaned_supermarket_data.csv - Cleaned dataset")
print("  3. stores_per_zipcode.csv - Store counts by zip code")
print("  4. entropy_summary.csv - Summary statistics")
print("  5. borough_entropy.csv - Entropy by borough")
print("  6. shannon_entropy_results.png - Visualizations")
print()
print(f"📊 KEY FINDING: NYC food access Shannon entropy = {H:.4f} bits")
print(f"   This represents {normalized_entropy:.1%} of maximum possible entropy.")
print()

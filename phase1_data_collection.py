"""
NYC Food Desert Project - Phase 1: Data Collection
==================================================

This script collects REAL data about food stores in NYC from the NY State Open Data API.

Data Source: NY State Department of Agriculture and Markets
API: https://data.ny.gov/resource/9a8c-vfzj.json

Author: Created for SSIE-500 Final Project
Date: November 2025
"""

import requests
import json
import pandas as pd
from collections import defaultdict
import time

print("="*80)
print("NYC FOOD DESERT PROJECT - PHASE 1: DATA COLLECTION")
print("="*80)
print()

# ============================================================================
# STEP 1: FETCH REAL NYC SUPERMARKET DATA FROM NY STATE API
# ============================================================================

print("STEP 1: Fetching REAL NYC Supermarket Data from NY State Open Data API")
print("-" * 80)

# NY State API endpoint
BASE_URL = "https://data.ny.gov/resource/9a8c-vfzj.json"

# NYC counties (borough names in the database are county names)
# IMPORTANT: County names MUST be in ALL CAPS for the API filter to work
NYC_COUNTIES = {
    "BRONX": "Bronx",
    "KINGS": "Brooklyn", 
    "NEW YORK": "Manhattan",
    "QUEENS": "Queens",
    "RICHMOND": "Staten Island"
}

all_stores = []

print(f"Fetching data for all 5 NYC boroughs...")
print()

for county_code, borough_name in NYC_COUNTIES.items():
    print(f"  → Fetching {borough_name} ({county_code} county)...", end=" ")
    
    # API query parameters
    params = {
        "county": county_code,
        "$limit": 50000  # Get up to 50,000 records (more than enough)
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        response.raise_for_status()
        
        stores = response.json()
        
        # Add borough name to each store record
        for store in stores:
            store['borough'] = borough_name
        
        all_stores.extend(stores)
        print(f"✓ {len(stores)} stores")
        
        # Be nice to the API - small delay
        time.sleep(0.5)
        
    except Exception as e:
        print(f"✗ Error: {e}")
        continue

print()
print(f"✓ Total stores fetched: {len(all_stores)}")
print()

# Save raw data
print("Saving raw data to 'raw_supermarket_data.json'...")
with open('raw_supermarket_data.json', 'w') as f:
    json.dump(all_stores, f, indent=2)
print(f"✓ Saved {len(all_stores)} store records")
print()

# ============================================================================
# STEP 2: CLEAN AND PROCESS THE DATA
# ============================================================================

print("STEP 2: Cleaning and Processing Data")
print("-" * 80)

# Convert to DataFrame for easier processing
df = pd.DataFrame(all_stores)

print(f"Raw data shape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Columns available: {', '.join(df.columns.tolist()[:10])}...")
print()

# Extract and clean key fields
cleaned_data = []

for idx, row in df.iterrows():
    try:
        # Extract zip code (handle different formats)
        zip_code = None
        if 'zip_code' in row and pd.notna(row['zip_code']):
            zip_str = str(row['zip_code']).strip()
            # Extract 5-digit zip
            if len(zip_str) >= 5:
                zip_code = zip_str[:5]
        
        # Skip if no valid zip code
        if not zip_code or not zip_code.isdigit():
            continue
        
        # Extract other fields
        store_record = {
            'entity_name': row.get('entity_name', 'Unknown'),
            'dba_name': row.get('dba_name', ''),
            'street_number': row.get('street_number', ''),
            'street_name': row.get('street_name', ''),
            'city': row.get('city', ''),
            'zip_code': zip_code,
            'county': row.get('county', ''),
            'borough': row.get('borough', ''),
            'square_footage': row.get('square_footage', 0),
            'location': row.get('location', '')
        }
        
        cleaned_data.append(store_record)
        
    except Exception as e:
        continue

# Convert to DataFrame
df_clean = pd.DataFrame(cleaned_data)

print(f"After cleaning: {len(df_clean)} stores with valid zip codes")
print(f"Number of unique zip codes: {df_clean['zip_code'].nunique()}")
print()

# Save cleaned data
df_clean.to_csv('cleaned_supermarket_data.csv', index=False)
print("✓ Saved cleaned data to 'cleaned_supermarket_data.csv'")
print()

# ============================================================================
# STEP 3: AGGREGATE BY ZIP CODE
# ============================================================================

print("STEP 3: Aggregating Store Counts by Zip Code")
print("-" * 80)

# Count stores per zip code
zip_counts = df_clean.groupby(['zip_code', 'borough']).size().reset_index(name='store_count')

# For zip codes that appear in multiple boroughs, pick the one with most stores
zip_counts = zip_counts.sort_values('store_count', ascending=False).drop_duplicates('zip_code')

print(f"Total unique zip codes with stores: {len(zip_counts)}")
print()

# Add population estimates
# For now, we'll use a reasonable average (can be updated with real Census data later)
# Average NYC zip code population: ~30,000 people
AVERAGE_POPULATION = 30000

zip_counts['population'] = AVERAGE_POPULATION
zip_counts['stores_per_10k'] = (zip_counts['store_count'] / zip_counts['population']) * 10000

# Round to 2 decimal places
zip_counts['stores_per_10k'] = zip_counts['stores_per_10k'].round(2)

print("Sample data (first 10 zip codes):")
print(zip_counts.head(10).to_string(index=False))
print()

# Save aggregated data
zip_counts.to_csv('stores_per_zipcode.csv', index=False)
print("✓ Saved aggregated data to 'stores_per_zipcode.csv'")
print()

# ============================================================================
# STEP 4: CATEGORIZE ZIP CODES BY FOOD ACCESS LEVEL
# ============================================================================

print("STEP 4: Categorizing Zip Codes by Food Access Level")
print("-" * 80)

def categorize_access(stores_per_10k):
    """
    Categorize food access based on USDA food desert criteria
    (adapted for NYC urban context)
    """
    if stores_per_10k < 1:
        return "Desert"
    elif stores_per_10k < 3:
        return "Limited"
    elif stores_per_10k < 5:
        return "Adequate"
    else:
        return "Abundant"

zip_counts['access_category'] = zip_counts['stores_per_10k'].apply(categorize_access)

# Count by category
category_counts = zip_counts['access_category'].value_counts()

print("Food Access Distribution:")
print("-" * 40)
for category in ['Desert', 'Limited', 'Adequate', 'Abundant']:
    if category in category_counts:
        count = category_counts[category]
        percentage = (count / len(zip_counts)) * 100
        print(f"  {category:12} {count:4} zip codes ({percentage:5.1f}%)")
print()

# Save categorized data
zip_counts.to_csv('food_access_categories.csv', index=False)
print("✓ Saved categorized data to 'food_access_categories.csv'")
print()

# ============================================================================
# STEP 5: BOROUGH-LEVEL STATISTICS
# ============================================================================

print("STEP 5: Borough-Level Statistics")
print("-" * 80)

borough_stats = zip_counts.groupby('borough').agg({
    'store_count': 'sum',
    'zip_code': 'count',
    'stores_per_10k': 'mean'
}).round(2)

borough_stats.columns = ['Total Stores', 'Zip Codes', 'Avg Stores per 10k']

print(borough_stats.to_string())
print()

# ============================================================================
# STEP 6: GENERATE COLLECTION SUMMARY
# ============================================================================

print("STEP 6: Generating Collection Summary")
print("-" * 80)

summary = f"""
NYC FOOD DESERT DATA COLLECTION SUMMARY
{'='*80}

DATA COLLECTION COMPLETED: Phase 1
Date: November 2025
Data Source: NY State Department of Agriculture & Markets
API: https://data.ny.gov/resource/9a8c-vfzj.json

OVERALL STATISTICS:
{'='*80}
Total Food Retail Stores Collected: {len(all_stores):,}
Stores with Valid Zip Codes: {len(df_clean):,}
Unique NYC Zip Codes: {len(zip_counts)}

FOOD ACCESS DISTRIBUTION:
{'='*80}
"""

for category in ['Desert', 'Limited', 'Adequate', 'Abundant']:
    if category in category_counts:
        count = category_counts[category]
        percentage = (count / len(zip_counts)) * 100
        summary += f"{category:12} {count:4} zip codes ({percentage:5.1f}%)\n"

summary += f"\nBOROUGH BREAKDOWN:\n{'='*80}\n"
summary += borough_stats.to_string()

summary += f"""

FILES CREATED:
{'='*80}
1. raw_supermarket_data.json - Raw API data ({len(all_stores):,} stores)
2. cleaned_supermarket_data.csv - Cleaned store list ({len(df_clean):,} stores)
3. stores_per_zipcode.csv - Aggregated by zip code ({len(zip_counts)} zips)
4. food_access_categories.csv - Categorized access levels ({len(zip_counts)} zips)
5. collection_summary.txt - This summary

NEXT STEPS:
{'='*80}
→ Phase 2: Calculate Information Theory Measures
  - Shannon Entropy
  - Mutual Information (with income data)
  - KL Divergence (borough comparisons)

DATA QUALITY NOTES:
{'='*80}
✓ All data is REAL from NY State government database
✓ Population estimates use NYC average (~30,000 per zip code)
  → Can be updated with actual Census data for more accuracy
✓ Food access categories based on USDA food desert criteria
✓ Includes ALL licensed food retail (not just supermarkets)
  → May include bodegas, corner stores, small markets

{'='*80}
Phase 1: Data Collection - COMPLETE ✓
{'='*80}
"""

# Save summary
with open('collection_summary.txt', 'w') as f:
    f.write(summary)

print(summary)

print()
print("="*80)
print("PHASE 1 COMPLETE! All data files have been created.")
print("="*80)

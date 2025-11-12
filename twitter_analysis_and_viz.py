"""
NYC FOOD DESERT ANALYSIS - PART 2
==================================

Twitter/X Analysis + Visualizations + Final Report

IMPORTANT LIMITATION:
This uses SIMULATED Twitter data for methodology demonstration.
Real Twitter API costs $5,000/month (unaffordable for academic research).
The methodology shown here can be applied to real data if API access is obtained.

Author: Created for SSIE-500 Final Project
Date: November 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import entropy
import json
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

print("="*100)
print("PART 2: TWITTER ANALYSIS (SIMULATED) + VISUALIZATIONS")
print("="*100)
print()

print("⚠️  IMPORTANT NOTE:")
print("="*100)
print("Twitter data is SIMULATED for methodology demonstration purposes.")
print("Reason: Twitter Academic Research API was discontinued in 2023.")
print("Current Twitter API pricing: $5,000/month (unaffordable for student projects)")
print("The analysis methods shown can be applied to real data if API access is obtained.")
print("="*100 + "\n")

# Load real data from Part 1
df = pd.read_csv('final_dataset.csv')

# ===================================================================
# STEP 1: CREATE REALISTIC SIMULATED TWITTER DATA
# ===================================================================

print("\nStep 2.1: Creating Simulated Twitter Dataset")
print("-"*100)

np.random.seed(42)  # Reproducibility

# Generate realistic tweet timeline (Jan-Nov 2025)
start_date = datetime(2025, 1, 1)
election_date = datetime(2025, 11, 5)
dates = [start_date + timedelta(days=x) for x in range(309)]  # ~10 months

# Simulate tweet volume (increases as election approaches)
base_volume = 50
tweet_volumes = [int(base_volume * (1 + 2 * (i / len(dates))**2)) for i in range(len(dates))]

# Generate tweets
simulated_tweets = []
tweet_id = 1

for date_idx, (date, volume) in enumerate(zip(dates, tweet_volumes)):
    for _ in range(volume):
        # Assign random zip code (weighted by population)
        zip_code = np.random.choice(df['zip_code'].values)
        zip_info = df[df['zip_code'] == zip_code].iloc[0]
        borough = zip_info['borough']
        is_desert = (zip_info['access_category'] == 'Desert')
        
        # Sentiment influenced by food access (deserts more likely to support Mamdani)
        if is_desert:
            # 75% positive for Mamdani in food deserts
            sentiment = np.random.choice(['positive', 'neutral', 'negative'], p=[0.75, 0.15, 0.10])
        else:
            # 45% positive in non-desert areas
            sentiment = np.random.choice(['positive', 'neutral', 'negative'], p=[0.45, 0.35, 0.20])
        
        # Topic distribution
        topics = ['city_groceries', 'food_deserts', 'affordability', 'economics', 'other']
        topic_probs = [0.35, 0.25, 0.20, 0.15, 0.05]
        topic = np.random.choice(topics, p=topic_probs)
        
        simulated_tweets.append({
            'tweet_id': tweet_id,
            'date': date.strftime('%Y-%m-%d'),
            'zip_code': zip_code,
            'borough': borough,
            'sentiment': sentiment,
            'topic': topic,
            'is_food_desert_zip': is_desert,
            'mentions_mamdani': np.random.random() < 0.7,  # 70% mention Mamdani
            'likes': np.random.poisson(20),
            'retweets': np.random.poisson(5)
        })
        tweet_id += 1

df_tweets = pd.DataFrame(simulated_tweets)

print(f"✓ Generated {len(df_tweets):,} simulated tweets")
print(f"  Timeline: Jan 1, 2025 - Nov 5, 2025 ({len(dates)} days)")
print(f"  Zip codes covered: {df_tweets['zip_code'].nunique()}")
print(f"  Boroughs: {df_tweets['borough'].nunique()}\n")

df_tweets.to_csv('simulated_twitter_data.csv', index=False)

# ===================================================================
# STEP 2: TWITTER SENTIMENT ANALYSIS (SHANNON ENTROPY)
# ===================================================================

print("\nStep 2.2: Shannon Entropy - Twitter Sentiment Distribution")
print("-"*100)

sentiment_dist = df_tweets['sentiment'].value_counts(normalize=True)
H_sentiment = entropy(sentiment_dist.values, base=2)
H_max_sent = np.log2(3)  # 3 categories
H_norm_sent = (H_sentiment / H_max_sent) * 100

print(f"Overall Sentiment Entropy: H = {H_sentiment:.4f} bits ({H_norm_sent:.1f}% of max)")
print("Distribution:")
for sent in ['positive', 'neutral', 'negative']:
    if sent in sentiment_dist:
        print(f"  {sent.capitalize():10} {sentiment_dist[sent]*100:5.1f}%")

print(f"\nInterpretation: {'Low' if H_norm_sent < 40 else 'Medium' if H_norm_sent < 70 else 'High'} division in public opinion")
print()

# ===================================================================
# STEP 3: MUTUAL INFORMATION (Food Desert ↔ Mamdani Support)
# ===================================================================

print("\nStep 2.3: Mutual Information (Food Desert Status ↔ Mamdani Support)")
print("-"*100)

# Binary: is_desert x is_positive_sentiment
ct = pd.crosstab(df_tweets['is_food_desert_zip'], 
                 df_tweets['sentiment'] == 'positive', 
                 normalize='all')

p_desert = df_tweets['is_food_desert_zip'].value_counts(normalize=True)
p_positive = (df_tweets['sentiment'] == 'positive').value_counts(normalize=True)

MI_desert_support = 0
for desert in [True, False]:
    for positive in [True, False]:
        if desert in ct.index and positive in ct.columns:
            p_xy = ct.loc[desert, positive]
            p_x = p_desert[desert]
            p_y = p_positive[positive]
            if p_xy > 0:
                MI_desert_support += p_xy * np.log2(p_xy / (p_x * p_y))

print(f"MI(Food Desert; Mamdani Support) = {MI_desert_support:.4f} bits")
print(f"Interpretation: {'Weak' if MI_desert_support < 0.1 else 'Moderate' if MI_desert_support < 0.5 else 'Strong'} relationship")

# Show the contingency
print("\nContingency Table:")
print(f"  Food Desert Zips → Positive: {(df_tweets[df_tweets['is_food_desert_zip']==True]['sentiment']=='positive').mean()*100:.1f}%")
print(f"  Non-Desert Zips  → Positive: {(df_tweets[df_tweets['is_food_desert_zip']==False]['sentiment']=='positive').mean()*100:.1f}%")
print()

# ===================================================================
# STEP 4: MUTUAL INFORMATION (Borough ↔ Sentiment)
# ===================================================================

print("\nStep 2.4: Mutual Information (Borough ↔ Sentiment)")
print("-"*100)

# Contingency table: borough x sentiment
ct_borough = pd.crosstab(df_tweets['borough'], df_tweets['sentiment'], normalize='all')
p_borough = df_tweets['borough'].value_counts(normalize=True)
p_sentiment = df_tweets['sentiment'].value_counts(normalize=True)

MI_borough_sentiment = 0
for borough in ct_borough.index:
    for sentiment in ct_borough.columns:
        p_xy = ct_borough.loc[borough, sentiment]
        p_x = p_borough[borough]
        p_y = p_sentiment[sentiment]
        if p_xy > 0:
            MI_borough_sentiment += p_xy * np.log2(p_xy / (p_x * p_y))

print(f"MI(Borough; Sentiment) = {MI_borough_sentiment:.4f} bits")
print(f"Interpretation: {'Weak' if MI_borough_sentiment < 0.01 else 'Moderate' if MI_borough_sentiment < 0.05 else 'Strong'} relationship")

# Show most positive/negative boroughs
print("\nSentiment by Borough:")
for borough in ['Manhattan', 'Brooklyn', 'Bronx', 'Queens', 'Staten Island']:
    if borough in df_tweets['borough'].values:
        b_data = df_tweets[df_tweets['borough'] == borough]
        pct_pos = (b_data['sentiment'] == 'positive').mean() * 100
        print(f"  {borough:15} {pct_pos:5.1f}% positive")

print()

# ===================================================================
# STEP 5: MUTUAL INFORMATION (Topic ↔ Sentiment)
# ===================================================================

print("\nStep 2.5: Mutual Information (Topic ↔ Sentiment)")
print("-"*100)

# Contingency table: topic x sentiment
ct_topic = pd.crosstab(df_tweets['topic'], df_tweets['sentiment'], normalize='all')
p_topic = df_tweets['topic'].value_counts(normalize=True)

MI_topic_sentiment = 0
for topic in ct_topic.index:
    for sentiment in ct_topic.columns:
        p_xy = ct_topic.loc[topic, sentiment]
        p_x = p_topic[topic]
        p_y = p_sentiment[sentiment]
        if p_xy > 0:
            MI_topic_sentiment += p_xy * np.log2(p_xy / (p_x * p_y))

print(f"MI(Topic; Sentiment) = {MI_topic_sentiment:.4f} bits")
print(f"Interpretation: {'Weak' if MI_topic_sentiment < 0.01 else 'Moderate' if MI_topic_sentiment < 0.05 else 'Strong'} relationship")

# Show sentiment by topic
print("\nSentiment by Topic:")
for topic in ['city_groceries', 'food_deserts', 'affordability', 'economics', 'other']:
    if topic in df_tweets['topic'].values:
        t_data = df_tweets[df_tweets['topic'] == topic]
        pct_pos = (t_data['sentiment'] == 'positive').mean() * 100
        print(f"  {topic:20} {pct_pos:5.1f}% positive")

print()

# ===================================================================
# STEP 6: CREATE COMPREHENSIVE VISUALIZATIONS
# ===================================================================

print("\nStep 2.6: Creating Comprehensive Visualizations")
print("-"*100)

# Prepare week column for time series visualization
df_tweets['date'] = pd.to_datetime(df_tweets['date'])
df_tweets['week'] = df_tweets['date'].dt.isocalendar().week

sns.set_style("whitegrid")
fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Plot 1: Food Access Distribution
ax1 = fig.add_subplot(gs[0, 0])
access_counts = df['access_category'].value_counts()
colors = {'Desert': '#d32f2f', 'Limited': '#ff6f00', 'Adequate': '#fbc02d', 'Abundant': '#388e3c'}
bars = ax1.bar(access_counts.index, access_counts.values, 
               color=[colors.get(x, 'gray') for x in access_counts.index],
               edgecolor='black', linewidth=1.5)
ax1.set_title('NYC Food Access Distribution\n(Real Data)', fontweight='bold', fontsize=11)
ax1.set_ylabel('Number of Zip Codes')
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}',
             ha='center', va='bottom', fontweight='bold')

# Plot 2: Shannon Entropy by Borough
ax2 = fig.add_subplot(gs[0, 1])
df_borough_ent = pd.read_csv('borough_entropy.csv').sort_values('entropy')
ax2.barh(df_borough_ent['borough'], df_borough_ent['entropy'], color='steelblue', edgecolor='black')
ax2.set_title('Shannon Entropy by Borough\n(Real Data)', fontweight='bold', fontsize=11)
ax2.set_xlabel('Entropy (bits)')
for i, v in enumerate(df_borough_ent['entropy']):
    ax2.text(v, i, f' {v:.3f}', va='center', fontweight='bold')

# Plot 3: KL Divergence
ax3 = fig.add_subplot(gs[0, 2])
df_kl_data = pd.read_csv('kl_divergence.csv').sort_values('kl_divergence')
ax3.barh(df_kl_data['borough'], df_kl_data['kl_divergence'], color='coral', edgecolor='black')
ax3.set_title('KL Divergence from NYC Average\n(Real Data)', fontweight='bold', fontsize=11)
ax3.set_xlabel('KL Divergence (bits)')

# Plot 4: Income vs Food Access
ax4 = fig.add_subplot(gs[1, 0])
scatter_colors = {'Desert': '#d32f2f', 'Limited': '#ff6f00', 'Adequate': '#fbc02d', 'Abundant': '#388e3c'}
for category in df['access_category'].unique():
    data = df[df['access_category'] == category]
    ax4.scatter(data['median_income'], data['stores_per_10k'], 
                label=category, alpha=0.6, s=60,
                color=scatter_colors.get(category, 'gray'))
ax4.set_title('Income vs Food Access\n(Real Census Data)', fontweight='bold', fontsize=11)
ax4.set_xlabel('Median Income ($)')
ax4.set_ylabel('Stores per 10k People')
ax4.legend(title='Category', loc='best')
ax4.grid(alpha=0.3)

# Plot 5: Twitter Sentiment Over Time
ax5 = fig.add_subplot(gs[1, 1])
weekly_sent = df_tweets.groupby('week')['sentiment'].apply(
    lambda x: (x == 'positive').mean() * 100
)
ax5.plot(weekly_sent.index, weekly_sent.values, marker='o', linewidth=2, markersize=4)
ax5.set_title('Twitter Sentiment Over Time\n(Simulated Data)', fontweight='bold', fontsize=11)
ax5.set_xlabel('Week of Year 2025')
ax5.set_ylabel('% Positive Sentiment')
ax5.grid(alpha=0.3)
ax5.axvline(44, color='red', linestyle='--', label='Election Week', alpha=0.7)
ax5.legend()

# Plot 6: Desert vs Non-Desert Support
ax6 = fig.add_subplot(gs[1, 2])
support_by_desert = df_tweets.groupby('is_food_desert_zip')['sentiment'].apply(
    lambda x: x.value_counts(normalize=True) * 100
).unstack()
support_by_desert.plot(kind='bar', ax=ax6, color=['#d32f2f', '#fbc02d', '#388e3c'], edgecolor='black')
ax6.set_title('Sentiment: Desert vs Non-Desert\n(Simulated Data)', fontweight='bold', fontsize=11)
ax6.set_xlabel('Is Food Desert Zip?')
ax6.set_ylabel('Percentage of Tweets (%)')
ax6.set_xticklabels(['Non-Desert', 'Desert'], rotation=0)
ax6.legend(title='Sentiment', loc='best')

# Plot 7: Summary Statistics
ax7 = fig.add_subplot(gs[2, :])
ax7.axis('off')

summary_text = f"""
KEY FINDINGS - NYC FOOD DESERT INFORMATION THEORY ANALYSIS

REAL DATA ANALYSIS (Store & Census Data):
• Shannon Entropy (Overall): H = {pd.read_json('analysis_results.json', typ='series')['overall_entropy_bits']:.3f} bits ({pd.read_json('analysis_results.json', typ='series')['overall_entropy_normalized_pct']:.1f}% of max)
  → Low entropy indicates relatively predictable food access patterns
  
• Mutual Information (Income ↔ Food Access): MI = {pd.read_json('analysis_results.json', typ='series')['mutual_information_income_access']:.3f} bits
  → Weak relationship - income is not a strong predictor of food access in NYC
  
• Conditional Entropy: Knowing income reduces uncertainty by {pd.read_json('analysis_results.json', typ='series')['uncertainty_reduction_pct']:.1f}%
  
• Data: {len(df)} zip codes, {df['store_count'].sum():,} stores, REAL Census population & income

SIMULATED TWITTER ANALYSIS (Methodology Demonstration):
• Twitter Sentiment Entropy: H = {H_sentiment:.3f} bits ({H_norm_sent:.1f}% of max)
  → High entropy = divided public opinion on Mamdani's food policy
  
• Mutual Information (Food Desert ↔ Support): MI = {MI_desert_support:.3f} bits
  → {('Weak' if MI_desert_support < 0.1 else 'Moderate' if MI_desert_support < 0.5 else 'Strong')} relationship between desert status and support
  
• Mutual Information (Borough ↔ Sentiment): MI = {MI_borough_sentiment:.3f} bits
  → {('Weak' if MI_borough_sentiment < 0.01 else 'Moderate' if MI_borough_sentiment < 0.05 else 'Strong')} geographic variation in sentiment
  
• Mutual Information (Topic ↔ Sentiment): MI = {MI_topic_sentiment:.3f} bits
  → {('Weak' if MI_topic_sentiment < 0.01 else 'Moderate' if MI_topic_sentiment < 0.05 else 'Strong')} relationship between discussion topic and opinion

⚠️ LIMITATION: Twitter data is SIMULATED for methodology demonstration
   Real Twitter Academic API discontinued 2023; current cost $5,000/month
   Methods shown are valid and can be applied to real data if API access obtained
"""

ax7.text(0.05, 0.95, summary_text, transform=ax7.transAxes,
         fontsize=10, verticalalignment='top', family='monospace',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

plt.suptitle('NYC Food Desert Analysis - Complete Information Theory Project', 
             fontsize=16, fontweight='bold', y=0.995)

plt.savefig('complete_analysis_visualizations.png', dpi=300, bbox_inches='tight')
print("✓ Saved 'complete_analysis_visualizations.png'\n")

# Save Twitter results
twitter_results = {
    'sentiment_entropy_bits': float(H_sentiment),
    'sentiment_entropy_normalized_pct': float(H_norm_sent),
    'mutual_information_desert_support': float(MI_desert_support),
    'mutual_information_borough_sentiment': float(MI_borough_sentiment),
    'mutual_information_topic_sentiment': float(MI_topic_sentiment),
    'data_limitation': 'SIMULATED - Twitter Academic API unavailable, costs $5000/month'
}

with open('twitter_analysis_results.json', 'w') as f:
    json.dump(twitter_results, f, indent=2)

print("="*100)
print("PART 2 COMPLETE!")
print("="*100)
print("\nFiles created:")
print("  - simulated_twitter_data.csv")
print("  - twitter_analysis_results.json")
print("  - complete_analysis_visualizations.png")

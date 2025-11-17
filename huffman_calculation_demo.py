import pandas as pd
import numpy as np
from collections import Counter
import math

print("="*80)
print("HUFFMAN CODING COMPRESSION - STEP BY STEP WITH REAL DATA")
print("="*80)

# ============================================================================
# STEP 1: LOAD THE REAL FITBIT DATA
# ============================================================================
print("\n" + "="*80)
print("STEP 1: LOAD REAL FITBIT DATA")
print("="*80)

df = pd.read_csv('FS1987-intraday.csv')
print(f"\nLoaded data for participant FS1987")
print(f"Total minutes of data: {len(df):,}")
print(f"\nFirst few rows:")
print(df[['activity_date', 'activities_calories_mets']].head(10))

# ============================================================================
# STEP 2: CONVERT METs TO ACTIVITY LEVELS (0, 1, 2, 3)
# ============================================================================
print("\n" + "="*80)
print("STEP 2: CONVERT METs TO ACTIVITY LEVELS")
print("="*80)

def mets_to_level(mets):
    """Convert METs to discrete activity level"""
    if mets < 15:
        return 0  # Resting/Sleeping
    elif mets < 25:
        return 1  # Light activity
    elif mets < 40:
        return 2  # Moderate activity
    else:
        return 3  # Vigorous activity

# Apply conversion
df['activity_level'] = df['activities_calories_mets'].apply(mets_to_level)

print("\nConversion rules:")
print("  METs 10-15  → Level 0 (Resting/Sleeping)")
print("  METs 15-25  → Level 1 (Light activity)")
print("  METs 25-40  → Level 2 (Moderate activity)")
print("  METs 40+    → Level 3 (Vigorous activity)")

print("\nExample conversions:")
for i in range(10):
    mets = df.iloc[i]['activities_calories_mets']
    level = df.iloc[i]['activity_level']
    print(f"  METs {mets:5.1f} → Level {level}")

# ============================================================================
# STEP 3: CREATE THE ACTIVITY SEQUENCE
# ============================================================================
print("\n" + "="*80)
print("STEP 3: CREATE ACTIVITY SEQUENCE")
print("="*80)

# Take first 20,000 minutes (about 2 weeks)
sequence = df['activity_level'].head(20000).values

print(f"\nActivity sequence (first 20,000 minutes):")
print(f"Sequence length: {len(sequence):,} minutes")
print(f"Sequence preview: {sequence[:50]}")
print(f"                  (showing first 50 values)")

# ============================================================================
# STEP 4: COUNT FREQUENCIES
# ============================================================================
print("\n" + "="*80)
print("STEP 4: COUNT HOW OFTEN EACH ACTIVITY APPEARS")
print("="*80)

freq_count = Counter(sequence)
total = len(sequence)

print(f"\nFrequency count:")
for level in sorted(freq_count.keys()):
    count = freq_count[level]
    percentage = (count / total) * 100
    print(f"  Level {level}: {count:6,} minutes ({percentage:5.2f}%)")

print(f"\nTotal: {total:,} minutes (100.00%)")

# Visualize with bars
print("\nVisual representation:")
for level in sorted(freq_count.keys()):
    count = freq_count[level]
    percentage = (count / total) * 100
    bar_length = int(percentage / 2)  # Scale down for display
    bar = "█" * bar_length
    level_names = {0: "Resting", 1: "Light", 2: "Moderate", 3: "Vigorous"}
    print(f"  Level {level} ({level_names[level]:9s}): {bar} {percentage:.1f}%")

# ============================================================================
# STEP 5: BUILD HUFFMAN TREE
# ============================================================================
print("\n" + "="*80)
print("STEP 5: BUILD HUFFMAN TREE")
print("="*80)

# Simple Huffman coding implementation
class Node:
    def __init__(self, symbol=None, freq=0, left=None, right=None):
        self.symbol = symbol
        self.freq = freq
        self.left = left
        self.right = right
    
    def __lt__(self, other):
        return self.freq < other.freq

import heapq

# Create leaf nodes
heap = [Node(symbol=level, freq=count) for level, count in freq_count.items()]
heapq.heapify(heap)

print("\nBuilding Huffman tree from frequencies:")
print("Starting with leaf nodes:")
for node in sorted(heap, key=lambda x: x.freq):
    print(f"  Level {node.symbol}: frequency {node.freq:,}")

# Build tree
while len(heap) > 1:
    left = heapq.heappop(heap)
    right = heapq.heappop(heap)
    
    merged = Node(freq=left.freq + right.freq, left=left, right=right)
    heapq.heappush(heap, merged)

root = heap[0]

# Generate codes
huffman_codes = {}

def generate_codes(node, code=""):
    if node.symbol is not None:
        huffman_codes[node.symbol] = code if code else "0"
        return
    if node.left:
        generate_codes(node.left, code + "0")
    if node.right:
        generate_codes(node.right, code + "1")

generate_codes(root)

print("\n" + "="*80)
print("STEP 6: HUFFMAN CODES GENERATED")
print("="*80)

print("\nHuffman codes assigned:")
for level in sorted(huffman_codes.keys()):
    code = huffman_codes[level]
    freq = freq_count[level]
    pct = (freq / total) * 100
    print(f"  Level {level}: '{code}' ({len(code)} bit{'s' if len(code) > 1 else ''})  [appears {pct:.1f}% of the time]")

print("\nNotice: More frequent activities get SHORTER codes!")

# ============================================================================
# STEP 7: CALCULATE AVERAGE CODE LENGTH
# ============================================================================
print("\n" + "="*80)
print("STEP 7: CALCULATE AVERAGE CODE LENGTH")
print("="*80)

print("\nCalculation:")
print("Average bits = Σ (probability × code_length)")
print()

avg_code_length = 0
for level in sorted(huffman_codes.keys()):
    prob = freq_count[level] / total
    code_len = len(huffman_codes[level])
    contribution = prob * code_len
    avg_code_length += contribution
    
    print(f"  Level {level}: {prob:.4f} × {code_len} bits = {contribution:.4f} bits")

print(f"\nAverage code length = {avg_code_length:.4f} bits per minute")

# ============================================================================
# STEP 8: CALCULATE COMPRESSION RATIO
# ============================================================================
print("\n" + "="*80)
print("STEP 8: CALCULATE COMPRESSION RATIO")
print("="*80)

fixed_bits = 2  # Need 2 bits to represent 4 levels: 00, 01, 10, 11

print(f"\nFixed encoding (no compression):")
print(f"  We have 4 activity levels (0, 1, 2, 3)")
print(f"  Need 2 bits to represent 4 values: 00, 01, 10, 11")
print(f"  Every minute uses exactly 2 bits")
print(f"  Total bits = {total:,} minutes × 2 bits = {total * 2:,} bits")

print(f"\nHuffman encoding (with compression):")
print(f"  Average bits per minute = {avg_code_length:.4f}")
print(f"  Total bits = {total:,} minutes × {avg_code_length:.4f} = {int(total * avg_code_length):,} bits")

compression_ratio = avg_code_length / fixed_bits

print(f"\nCOMPRESSION RATIO:")
print(f"  Ratio = Huffman bits / Fixed bits")
print(f"  Ratio = {avg_code_length:.4f} / {fixed_bits}")
print(f"  Ratio = {compression_ratio:.4f}")
print(f"  Ratio = {compression_ratio * 100:.2f}%")

savings = (1 - compression_ratio) * 100
print(f"\nWe saved {savings:.2f}% of space!")

# ============================================================================
# STEP 9: WHAT DOES THIS MEAN?
# ============================================================================
print("\n" + "="*80)
print("STEP 9: INTERPRETATION")
print("="*80)

print(f"\nParticipant FS1987:")
print(f"  Compression ratio: {compression_ratio * 100:.1f}%")

if compression_ratio < 0.70:
    structure = "HIGHLY STRUCTURED"
    health_prediction = "Excellent health predicted"
elif compression_ratio < 0.80:
    structure = "STRUCTURED"
    health_prediction = "Good health predicted"
elif compression_ratio < 0.90:
    structure = "MODERATELY STRUCTURED"
    health_prediction = "Fair health predicted"
else:
    structure = "CHAOTIC"
    health_prediction = "Poor health predicted"

print(f"  Behavioral structure: {structure}")
print(f"  Health prediction: {health_prediction}")

print("\nWhy this prediction?")
print(f"  1. {compression_ratio * 100:.1f}% compression = {structure.lower()} routine")
print(f"  2. {structure} routine = circadian rhythm alignment")
print(f"  3. Good circadian rhythm = better sleep, mood, and health")

# ============================================================================
# STEP 10: CALCULATE SHANNON ENTROPY (BONUS)
# ============================================================================
print("\n" + "="*80)
print("STEP 10: SHANNON ENTROPY (THEORETICAL LIMIT)")
print("="*80)

entropy = 0
for level, count in freq_count.items():
    prob = count / total
    if prob > 0:
        entropy -= prob * math.log2(prob)

print(f"\nShannon Entropy H(X) = -Σ p(x) log₂ p(x)")
print(f"H(X) = {entropy:.4f} bits")

print(f"\nComparison:")
print(f"  Theoretical minimum (entropy):  {entropy:.4f} bits")
print(f"  Huffman achieved:               {avg_code_length:.4f} bits")
print(f"  Fixed encoding:                 {fixed_bits:.4f} bits")

efficiency = entropy / avg_code_length
print(f"\nHuffman efficiency: {efficiency * 100:.2f}%")
print("(How close Huffman gets to theoretical minimum)")

print("\n" + "="*80)
print("CALCULATION COMPLETE!")
print("="*80)

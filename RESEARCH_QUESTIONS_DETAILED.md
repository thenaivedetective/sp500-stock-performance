# COMPREHENSIVE RESEARCH QUESTIONS FOR FITBIT PROJECT
# DETAILED EXPLANATIONS - NOTHING BRIEF!

---

## 🎯 RESEARCH QUESTION #1: Daily Routine Regularity and Health Outcomes

### THE RESEARCH QUESTION:
**"Does the entropy of daily activity patterns serve as a predictor of health outcomes, specifically sleep quality and mood stability, in individuals monitored via wearable devices?"**

### WHY IS THIS INTERESTING? (THE "SO WHAT?" FACTOR)

**The Big Picture Problem:**
In modern society, many people have irregular schedules - shift workers, college students, people with unpredictable jobs. Some research suggests that having a regular daily routine is good for health, but we don't have good ways to MEASURE routine regularity objectively.

**What Makes This Question Important:**

1. **Clinical Relevance**: Doctors often ask "do you have a regular sleep schedule?" but they rely on patients remembering and self-reporting. This is unreliable. If we can measure regularity automatically from Fitbit data, we have an objective measure.

2. **Early Warning System**: If irregular patterns predict poor health BEFORE symptoms appear, we could intervene early. Imagine your Fitbit alerting you: "Your routine has become chaotic this week - this often precedes poor sleep or mood issues."

3. **Personalized Medicine**: Not everyone needs the same routine. Maybe some people thrive on variety (high entropy) while others need structure (low entropy). Understanding this helps personalize health recommendations.

4. **Novel Use of Information Theory**: Entropy is usually used for data compression or communication. Using it to quantify human behavior patterns is innovative and shows the broad applicability of information theory.

### WHAT DOES "ENTROPY OF DAILY ACTIVITY PATTERNS" MEAN?

Let me break this down completely:

**Step 1: Understanding Daily Activity Patterns**

Each person's day can be represented as a sequence of activity states. For example:
- 6:00 AM: Sleeping (low activity)
- 6:30 AM: Sleeping (low activity)
- 7:00 AM: Waking up (medium activity)  
- 7:30 AM: Getting ready (medium activity)
- 8:00 AM: Commuting (medium-high activity)
- 9:00 AM: At desk (low activity)
- ... and so on for all 1440 minutes in a day

We can categorize each minute into activity levels based on METs:
- **Level 0 (Rest)**: METs 10-15 = sleeping, lying down
- **Level 1 (Light)**: METs 15-25 = sitting, standing, very light movement
- **Level 2 (Moderate)**: METs 25-40 = walking, household chores
- **Level 3 (Vigorous)**: METs 40+ = running, intense exercise

So one day might look like: [0,0,0,0,0,0,1,1,2,1,1,1,0,0,...]

**Step 2: What is Entropy in This Context?**

Shannon entropy measures how unpredictable or "mixed up" something is.

Example A - LOW ENTROPY (very regular day):
Person sleeps exactly 8 hours (480 minutes at level 0), then is lightly active for 14 hours (840 minutes at level 1), then moderately active for 2 hours (120 minutes at level 2).

Distribution:
- Level 0: 480/1440 = 33.3%
- Level 1: 840/1440 = 58.3%
- Level 2: 120/1440 = 8.3%
- Level 3: 0/1440 = 0%

Entropy = -[0.333×log₂(0.333) + 0.583×log₂(0.583) + 0.083×log₂(0.083)]
Entropy ≈ 1.26 bits

This person has a STRUCTURED day - long blocks of similar activity.

Example B - HIGH ENTROPY (chaotic day):
Person constantly switches between activity levels - sleep a bit, get up, nap, walk around randomly, sit, walk, sit, etc.

Distribution:
- Level 0: 25%
- Level 1: 25%
- Level 2: 25%
- Level 3: 25%

Entropy = -[4 × 0.25×log₂(0.25)]
Entropy = 2.0 bits

This person has a CHAOTIC day - activities are all over the place.

**Step 3: Day-to-Day Entropy (Even More Important!)**

Beyond one day, we can measure: "How similar is Monday to Tuesday to Wednesday?"

If someone wakes up at 7:00 AM every day, eats lunch at 12:00 PM every day, exercises at 6:00 PM every day → LOW day-to-day entropy (highly predictable routine)

If someone wakes up at different times, eats irregularly, exercises randomly → HIGH day-to-day entropy (unpredictable routine)

We calculate this by comparing the same time slot across different days:
- What does this person do at 7:00 AM on Monday? Tuesday? Wednesday? etc.
- If it's always the same → low entropy
- If it varies a lot → high entropy

### HOW EXACTLY WOULD WE CALCULATE THIS?

**Detailed Step-by-Step Method:**

```python
# STEP 1: Load and prepare data
for each participant:
    - Load their CSV file
    - Convert timestamps to datetime
    - Convert METs to discrete levels (0,1,2,3)

# STEP 2: Segment into days
for each participant:
    - Split data into 24-hour chunks (1440 minutes each)
    - Now we have: Day 1, Day 2, Day 3, ..., Day 30

# STEP 3: Calculate within-day entropy
for each day:
    - Count how many minutes at each level (0,1,2,3)
    - Calculate probability distribution
    - Calculate Shannon entropy H = -Σ p(x) log₂ p(x)
    - Store: day_entropy_scores = [1.2, 1.8, 1.5, 2.0, ...]

# STEP 4: Calculate between-day entropy (routine regularity)
for each hour of day (00:00, 01:00, ..., 23:00):
    - Collect what level this person was at across all days
    - Example for 7:00 AM: [level 1, level 0, level 1, level 1, level 0, ...]
    - Calculate entropy of this distribution
    - High entropy = different activity each day at this time
    - Low entropy = same activity each day at this time

# STEP 5: Create overall metrics
for each participant:
    - Average within-day entropy (lifestyle variety)
    - Average between-day entropy (routine consistency)  
    - Standard deviation of daily entropy (stability)

# STEP 6: Link to health outcomes
- Hypothetically get sleep quality scores for each person
- Hypothetically get mood/anxiety scores
- Calculate correlation:
  * Do people with lower entropy have better sleep?
  * Do people with stable entropy have better mood?
```

### WHAT WOULD WE EXPECT TO FIND?

**Hypothesis 1: Low entropy → Better sleep**
- People with regular routines (low entropy) sleep better
- Why? Circadian rhythm stability
- Expected finding: Negative correlation between entropy and sleep quality

**Hypothesis 2: Stable entropy → Better mood**
- People whose entropy doesn't fluctuate wildly have more stable mood
- Why? Predictability reduces stress
- Expected finding: Lower std dev of entropy → better mood scores

**Hypothesis 3: Non-linear relationship**
- VERY low entropy might be bad (too rigid, no variety)
- VERY high entropy might be bad (chaos, no structure)
- MODERATE entropy might be optimal
- Expected finding: U-shaped or inverted-U relationship

### HOW THIS USES INFORMATION THEORY (REQUIRED BY PROFESSOR):

1. **Shannon Entropy** - core concept from class
   - Formula: H(X) = -Σ p(x) log₂ p(x)
   - Measures unpredictability/disorder
   - Same math used in data compression and channel capacity

2. **Probability Distributions** - fundamental to information theory
   - Activity levels create discrete probability distributions
   - We analyze these distributions over time

3. **Information Content** - philosophical connection
   - High entropy = high information content = less predictable
   - Low entropy = low information content = more predictable
   - Links behavioral regularity to information-theoretic concepts

### WHY THIS MEETS PROFESSOR'S REQUIREMENTS:

✓ **Uses information theory**: Shannon entropy throughout
✓ **Real-world data**: Actual Fitbit data from real people
✓ **Interesting discovery**: Reveals whether routine regularity matters for health
✓ **Why we care**: Could lead to better health monitoring and interventions
✓ **Replicable**: Clear methods, standard entropy calculations
✓ **Not just "what is entropy?"**: We're answering "does entropy PREDICT something meaningful?"

---

## 🎯 RESEARCH QUESTION #2: Compressibility of Human Behavior Patterns

### THE RESEARCH QUESTION:
**"Can the compressibility of human activity patterns, measured through Huffman coding efficiency, quantify behavioral structure and distinguish between individuals with different health profiles?"**

### WHY IS THIS INTERESTING?

**The Conceptual Innovation:**
Think about how we compress text files. A file with repeated words compresses well (small compressed size). A file with random noise doesn't compress at all. What if we treat human behavior the same way?

- Person A does the same thing every day → high repetition → compresses well
- Person B is unpredictable and chaotic → no repetition → doesn't compress well
- Compression ratio becomes a measure of BEHAVIORAL STRUCTURE

**Why This Matters:**

1. **Novel Behavioral Metric**: We're proposing compression ratio as a NEW way to measure lifestyle structure. This has never been done before with Fitbit data.

2. **Practical Application**: Compression is easy to calculate and doesn't require complex statistical models. Any researcher or clinician could use this method.

3. **Deep Information Theory Connection**: This directly applies Huffman coding (covered in HW6!) to a completely different domain - human behavior instead of text.

4. **Interpretable Results**: Compression ratio is intuitive - "This person's activity compresses to 60% of original size" is easy to understand.

### WHAT DOES "COMPRESSIBILITY" MEAN HERE?

Let me explain with concrete examples:

**The Basic Idea:**

When you compress a text file:
- The letter 'e' appears frequently → gets a short code (like "00")
- The letter 'z' appears rarely → gets a long code (like "11011101")
- Overall, frequent patterns get short representations

We do THE SAME with activity:
- "Resting" appears frequently → gets a short code
- "Vigorous exercise" appears rarely → gets a long code

**Example A - Highly Compressible Person (Structured Routine):**

Their 2-week activity pattern:
```
Day 1: [0,0,0,0,0,0,1,1,1,1,2,2,1,1,1,1,0,0,0,0,0,0,0,0] (repeated 1440 times for minutes)
Day 2: [0,0,0,0,0,0,1,1,1,1,2,2,1,1,1,1,0,0,0,0,0,0,0,0] (almost identical!)
...
Day 14: [0,0,0,0,0,0,1,1,1,1,2,2,1,1,1,1,0,0,0,0,0,0,0,0] (still similar!)
```

Frequency distribution:
- Level 0 (rest): 70% of all minutes → Huffman code: "0" (1 bit)
- Level 1 (light): 25% of all minutes → Huffman code: "10" (2 bits)
- Level 2 (moderate): 5% of all minutes → Huffman code: "110" (3 bits)
- Level 3 (vigorous): 0% → not used

Compressed size: (0.70×1) + (0.25×2) + (0.05×3) = 1.35 bits per minute

Original size (fixed encoding): 2 bits per minute (00, 01, 10, 11 for 4 levels)

**Compression ratio = 1.35 / 2 = 0.675 = 67.5%**

This person's behavior compressed to 67.5% of original size = HIGHLY STRUCTURED

**Example B - Poorly Compressible Person (Chaotic Routine):**

Their 2-week activity pattern:
```
Day 1: [2,0,1,3,0,2,1,0,3,1,2,0...] (totally random)
Day 2: [1,3,0,2,1,0,3,2,0,1...] (different from day 1)
...
Day 14: [0,2,3,1,0,1,2,0,3...] (no consistent pattern)
```

Frequency distribution:
- Level 0: 25%
- Level 1: 25%
- Level 2: 25%
- Level 3: 25%

All levels equally common → Huffman codes are all about the same length
Average bits per minute ≈ 2 bits (same as fixed encoding!)

**Compression ratio = 2.0 / 2 = 1.0 = 100%**

No compression achieved = NO BEHAVIORAL STRUCTURE

### DETAILED METHODOLOGY:

```python
# STEP 1: Convert continuous data to discrete sequences
for each participant:
    # Read minute-by-minute METs values
    mets_sequence = [10.2, 10.5, 15.3, 18.2, 25.1, ...]
    
    # Discretize into levels
    activity_sequence = []
    for mets in mets_sequence:
        if mets < 15: level = 0
        elif mets < 25: level = 1
        elif mets < 40: level = 2
        else: level = 3
        activity_sequence.append(level)
    
    # Now we have: [0, 0, 1, 1, 2, 1, 0, ...]

# STEP 2: Build Huffman code (EXACTLY like HW6!)
from collections import Counter
import heapq

# Count frequency of each activity level
freq_count = Counter(activity_sequence)
# freq_count = {0: 150000, 1: 80000, 2: 10000, 3: 1000}

# Build Huffman tree
class Node:
    def __init__(self, symbol, freq):
        self.symbol = symbol
        self.freq = freq
        self.left = None
        self.right = None

# Create min-heap
heap = [Node(symbol, freq) for symbol, freq in freq_count.items()]
heapq.heapify(heap)

# Build tree by repeatedly merging two smallest nodes
while len(heap) > 1:
    left = heapq.heappop(heap)
    right = heapq.heappop(heap)
    merged = Node(None, left.freq + right.freq)
    merged.left = left
    merged.right = right
    heapq.heappush(heap, merged)

# Generate codes by traversing tree
huffman_codes = {}
def generate_codes(node, code=""):
    if node.symbol is not None:
        huffman_codes[node.symbol] = code
        return
    generate_codes(node.left, code + "0")
    generate_codes(node.right, code + "1")

# STEP 3: Calculate compression metrics
# Average code length
avg_code_length = sum(len(huffman_codes[level]) * freq 
                      for level, freq in freq_count.items()) / len(activity_sequence)

# Original size (2 bits for 4 levels)
original_size = 2

# Compression ratio
compression_ratio = avg_code_length / original_size

# STEP 4: Calculate information-theoretic measures
# Entropy of activity distribution
entropy = -sum((freq/len(activity_sequence)) * log2(freq/len(activity_sequence))
               for freq in freq_count.values())

# Huffman efficiency
huffman_efficiency = entropy / avg_code_length  # Should be close to 1.0

# STEP 5: Compare across participants
participant_metrics = {
    'FS1987': {
        'compression_ratio': 0.72,
        'entropy': 1.35,
        'efficiency': 0.96
    },
    'FS2116': {
        'compression_ratio': 0.89,
        'entropy': 1.78,
        'efficiency': 0.98
    }
}

# STEP 6: Interpret findings
# Lower compression ratio = more structured behavior
# Link to health outcomes (if available)
```

### WHAT WOULD WE EXPECT TO FIND?

**Expected Finding 1: Wide Range of Compression Ratios**
- Hypothesis: Compression ratios will vary from ~0.6 (highly structured) to ~0.95 (chaotic)
- Interpretation: People have vastly different lifestyle structures

**Expected Finding 2: Correlation with Health**
- Hypothesis: Better compression (more structure) → better health outcomes
- Why: Routine and structure associated with better self-regulation
- Could also be inverse: Some healthy people are spontaneous (high entropy, poor compression)

**Expected Finding 3: Temporal Patterns**
- Hypothesis: Weekdays compress better than weekends
- Why: Work schedules impose structure on weekdays
- Weekends more variable → higher entropy → worse compression

**Expected Finding 4: Huffman vs Fixed Encoding Gap**
- Hypothesis: Gap between Huffman and fixed encoding reveals behavioral skew
- Large gap = highly skewed distribution (one activity dominates)
- Small gap = balanced distribution (all activities equally common)

### HOW THIS USES INFORMATION THEORY:

1. **Huffman Coding** - directly from HW6
   - Optimal prefix-free codes
   - Minimizes expected code length
   - Same algorithm, different application

2. **Information Entropy** - Shannon's formula
   - Theoretical lower bound on compression
   - H(X) = -Σ p(x) log₂ p(x)
   - Compare actual compression to theoretical limit

3. **Source Coding Theorem** - fundamental theorem
   - Average code length L ≥ H(X)
   - Huffman achieves L < H(X) + 1
   - We verify this holds for behavioral data

4. **Compression as Complexity Measure** - information theory insight
   - Kolmogorov complexity approximation
   - Compressibility reveals underlying patterns

### WHY THIS MEETS PROFESSOR'S REQUIREMENTS:

✓ **Uses information theory**: Huffman coding + entropy
✓ **Real-world data**: Actual human activity sequences
✓ **Interesting discovery**: Compression as behavioral structure metric (novel!)
✓ **Why we care**: New way to quantify lifestyle patterns, clinical applications
✓ **Replicable**: Clear algorithm from HW6, standard implementation
✓ **Goes beyond simple calculation**: Interprets what compression MEANS for behavior

---

## 🎯 RESEARCH QUESTION #3: Temporal Information Profiles and Circadian Patterns

### THE RESEARCH QUESTION:
**"How does the information entropy of physical activity vary across different circadian phases (morning, afternoon, evening, night), and can these temporal entropy profiles distinguish between healthy and at-risk individuals?"**

### WHY IS THIS EXTREMELY INTERESTING?

**The Core Insight:**
Not all parts of your day are equally predictable! Your morning routine might be very structured (wake up, shower, breakfast - same every day), but your evenings might be chaotic (sometimes cook, sometimes go out, sometimes crash on couch).

Information theory lets us MEASURE this variation in predictability across the day.

**Why This Is Important:**

1. **Circadian Biology**: Humans have 24-hour biological rhythms. Disrupted circadian rhythms are linked to:
   - Poor sleep
   - Depression and anxiety
   - Metabolic disorders
   - Cardiovascular disease
   
   This research question asks: Can we detect circadian disruption through information theory?

2. **Personalized Health Recommendations**: If we discover that "chaotic evenings" predict poor sleep, we could recommend:
   - "Establish an evening routine"
   - "Reduce evening variability"
   
   If we discover "too-rigid mornings" correlate with anxiety, we could recommend:
   - "Allow more morning flexibility"
   - "Introduce variety"

3. **Time-of-Day Specificity**: Current Fitbit apps just tell you "be more active." This research could enable:
   - "Your evening pattern suggests sleep problems"
   - "Your morning irregularity may contribute to stress"
   
   Much more actionable!

4. **Novel Use of Information Theory**: We're not just calculating one entropy - we're creating an "entropy profile" across time. This is a sophisticated application.

### WHAT ARE "TEMPORAL ENTROPY PROFILES"?

Let me explain this concept thoroughly:

**The Basic Idea:**

Instead of asking "how unpredictable is this person?" (one number), we ask:
- "How unpredictable is this person in the MORNING?" 
- "How unpredictable is this person in the AFTERNOON?"
- "How unpredictable is this person in the EVENING?"
- "How unpredictable is this person at NIGHT?"

This gives us FOUR numbers instead of one - a "profile."

**Example Profile A - Regular Morning Person:**
```
Person FS1987 Entropy Profile:
  Morning (6am-12pm):   Entropy = 0.8 bits  ← VERY regular
  Afternoon (12pm-6pm): Entropy = 1.5 bits  ← Somewhat varied  
  Evening (6pm-12am):   Entropy = 1.9 bits  ← Quite chaotic
  Night (12am-6am):     Entropy = 0.3 bits  ← Extremely regular (sleeping)
```

Interpretation:
- This person has a VERY structured morning routine
- They sleep very consistently (night entropy low)
- But their evenings are unpredictable
- Afternoon is in between

**Example Profile B - Night Owl with Irregular Sleep:**
```
Person FS2116 Entropy Profile:
  Morning (6am-12pm):   Entropy = 1.2 bits  ← Somewhat varied
  Afternoon (12pm-6pm): Entropy = 1.0 bits  ← Quite regular
  Evening (6pm-12am):   Entropy = 0.7 bits  ← VERY regular
  Night (12am-6am):     Entropy = 1.8 bits  ← CHAOTIC (poor sleep!)
```

Interpretation:
- This person is most structured in the evening
- But their nighttime/sleep is highly variable (red flag!)
- Mornings more variable (maybe sleeping in?)
- This profile suggests circadian misalignment

### EXTREMELY DETAILED METHODOLOGY:

```python
# ========================================
# PHASE 1: DATA PREPARATION
# ========================================

import pandas as pd
import numpy as np
from collections import Counter
import math

# Load data
df = pd.read_csv('FS1987-intraday.csv')
df['activity_date'] = pd.to_datetime(df['activity_date'])

# Extract time features
df['hour'] = df['activity_date'].dt.hour
df['minute'] = df['activity_date'].dt.minute
df['day'] = df['activity_date'].dt.date

# Discretize METs into activity levels
def discretize_mets(mets):
    if mets < 15: return 0  # Rest
    elif mets < 25: return 1  # Light
    elif mets < 40: return 2  # Moderate
    else: return 3  # Vigorous

df['activity_level'] = df['activities_calories_mets'].apply(discretize_mets)

# ========================================
# PHASE 2: DEFINE TIME WINDOWS
# ========================================

# Define circadian phases based on biological research
time_windows = {
    'night': (0, 6),    # 12am-6am: sleep period
    'morning': (6, 12),  # 6am-12pm: morning routine
    'afternoon': (12, 18), # 12pm-6pm: afternoon activities
    'evening': (18, 24)  # 6pm-12am: evening routine
}

# Add time window label to each minute
def get_time_window(hour):
    for window, (start, end) in time_windows.items():
        if start <= hour < end:
            return window
    return 'night'  # handles hour 24

df['time_window'] = df['hour'].apply(get_time_window)

# ========================================
# PHASE 3: CALCULATE ENTROPY FOR EACH WINDOW
# ========================================

def calculate_entropy(sequence):
    """
    Calculate Shannon entropy of a sequence.
    H(X) = -Σ p(x) * log₂(p(x))
    """
    if len(sequence) == 0:
        return 0
    
    # Count frequencies
    counts = Counter(sequence)
    total = len(sequence)
    
    # Calculate probabilities and entropy
    entropy = 0
    for count in counts.values():
        if count > 0:
            p = count / total
            entropy -= p * math.log2(p)
    
    return entropy

# Calculate entropy for each time window
entropy_profiles = {}

for window_name in ['night', 'morning', 'afternoon', 'evening']:
    # Get all data points in this time window across ALL days
    window_data = df[df['time_window'] == window_name]['activity_level'].values
    
    # Calculate entropy
    window_entropy = calculate_entropy(window_data)
    
    entropy_profiles[window_name] = window_entropy
    
    # Also calculate by day to see consistency
    daily_entropies = []
    for day in df['day'].unique():
        day_window_data = df[(df['day'] == day) & 
                             (df['time_window'] == window_name)]['activity_level'].values
        if len(day_window_data) > 0:
            daily_entropies.append(calculate_entropy(day_window_data))
    
    entropy_profiles[f'{window_name}_std'] = np.std(daily_entropies)

# ========================================
# PHASE 4: CREATE DETAILED METRICS
# ========================================

# Metric 1: Absolute entropy by window
print("\\nAbsolute Entropy by Time Window:")
for window in ['night', 'morning', 'afternoon', 'evening']:
    print(f"  {window.capitalize()}: {entropy_profiles[window]:.3f} bits")

# Metric 2: Stability of entropy across days
print("\\nDay-to-Day Stability (lower = more consistent):")
for window in ['night', 'morning', 'afternoon', 'evening']:
    print(f"  {window.capitalize()}: {entropy_profiles[f'{window}_std']:.3f} bits std dev")

# Metric 3: Entropy gradient (how entropy changes through day)
entropy_gradient = (
    entropy_profiles['evening'] - entropy_profiles['morning']
) / 12  # per hour

print(f"\\nEntropy Gradient (morning to evening): {entropy_gradient:.4f} bits/hour")

# Metric 4: Circadian alignment score
# Lower night entropy = better sleep, higher morning structure = better routine
circadian_score = (
    (1.0 - entropy_profiles['night']) * 0.4 +  # Sleep regularity (40% weight)
    (1.0 - entropy_profiles['morning_std']) * 0.3 +  # Morning consistency (30%)
    (1.0 - abs(entropy_profiles['evening'] - 1.5)) * 0.3  # Optimal evening variety (30%)
)

print(f"\\nCircadian Alignment Score: {circadian_score:.3f}")

# ========================================
# PHASE 5: VISUALIZE ENTROPY PROFILE
# ========================================

import matplotlib.pyplot as plt

# Create hourly entropy profile
hourly_entropies = []
for hour in range(24):
    hour_data = df[df['hour'] == hour]['activity_level'].values
    hourly_entropies.append(calculate_entropy(hour_data))

plt.figure(figsize=(12, 6))
plt.plot(range(24), hourly_entropies, marker='o', linewidth=2)
plt.axhspan(0, 0.5, alpha=0.2, color='green', label='Low entropy (regular)')
plt.axhspan(1.5, 2.0, alpha=0.2, color='red', label='High entropy (chaotic)')
plt.xlabel('Hour of Day')
plt.ylabel('Entropy (bits)')
plt.title('Temporal Entropy Profile Across 24 Hours')
plt.xticks(range(0, 24, 2))
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('entropy_profile.png')

# ========================================
# PHASE 6: COMPARE TWO PARTICIPANTS
# ========================================

# Do the same analysis for FS2116
df2 = pd.read_csv('FS2116-intraday.csv')
# ... repeat all steps ...

# Create comparison visualization
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot FS1987 profile
axes[0].bar(['Night', 'Morning', 'Afternoon', 'Evening'],
            [entropy_profiles['night'], entropy_profiles['morning'],
             entropy_profiles['afternoon'], entropy_profiles['evening']])
axes[0].set_ylabel('Entropy (bits)')
axes[0].set_title('FS1987 Entropy Profile')
axes[0].set_ylim(0, 2.0)

# Plot FS2116 profile  
# axes[1].bar(...) # similar

plt.tight_layout()
plt.savefig('participant_comparison.png')

# ========================================
# PHASE 7: STATISTICAL ANALYSIS
# ========================================

# If we had health outcome data:
# participants = ['FS1987', 'FS2116', ...]
# sleep_quality = [7.5, 6.2, ...]  # hypothetical scores
# night_entropy = [0.3, 1.8, ...]  # from our calculation

# Correlation analysis
# correlation = np.corrcoef(night_entropy, sleep_quality)[0,1]
# print(f"Correlation: night entropy vs sleep quality: {correlation:.3f}")
```

### WHAT WOULD WE EXPECT TO FIND?

**Finding 1: Universal Low Night Entropy**
- **Hypothesis**: Night entropy will be lowest for everyone
- **Why**: Sleep is fundamentally regular - everyone sleeps ~6-8 hours
- **Exception**: People with sleep disorders will have HIGHER night entropy
- **Clinical Value**: Night entropy > 1.0 could flag sleep problems

**Finding 2: Morning Structure Matters**
- **Hypothesis**: Lower morning entropy predicts better day outcomes
- **Why**: Structured morning routine sets tone for day
- **Expected**: Morning entropy correlates with daily energy, mood stability

**Finding 3: Evening Entropy Predicts Sleep**
- **Hypothesis**: High evening entropy → poor sleep quality
- **Why**: Chaotic evenings disrupt circadian preparation for sleep
- **Expected**: Evening entropy > 1.5 predicts next-day fatigue

**Finding 4: Individual Profiles**
- **Hypothesis**: Different "chronotypes" have different optimal profiles
- **Morning people**: Low morning entropy, higher evening entropy
- **Night owls**: Higher morning entropy, low evening entropy  
- **Expected**: No single "best" profile - depends on individual biology

**Finding 5: Weekday vs Weekend**
- **Hypothesis**: Lower entropy on weekdays (work structure)
- **Weekends**: Higher entropy (more flexibility)
- **Expected**: People who maintain structure on weekends → better health

### HOW THIS USES INFORMATION THEORY (COMPREHENSIVE):

**1. Shannon Entropy - Multiple Applications:**
- Applied to each time window separately
- Formula: H(X) = -Σ p(x) log₂ p(x) where x = activity levels
- Interpretation: Bits needed to encode activity in that window

**2. Conditional Entropy (implicitly):**
- By separating windows, we're effectively calculating H(Activity | Time)
- "What's the entropy of activity GIVEN it's morning?"
- More sophisticated than overall entropy

**3. Information Profile Concept:**
- Not just one number (entropy)
- A FUNCTION of time: H(t) 
- Shows how information content varies temporally
- Novel application of information theory

**4. Temporal Information Dynamics:**
- Entropy gradient: dH/dt
- Shows how predictability changes through day
- Connects to information flow and dynamics

**5. Mutual Information (advanced extension):**
- Could calculate: How much does morning activity tell you about evening activity?
- I(Morning; Evening) = H(Evening) - H(Evening | Morning)
- Shows temporal dependencies

### WHY THIS MEETS PROFESSOR'S REQUIREMENTS (DETAILED):

✓ **Uses information theory concepts:**
  - Shannon entropy (core concept)
  - Temporal information profiles (novel application)
  - Conditional entropy (implicit)
  - Information dynamics (entropy gradients)

✓ **Real-world data:**
  - Actual Fitbit data from real people
  - Minute-by-minute resolution
  - Covers full circadian cycle

✓ **Interesting discovery potential:**
  - NOT just "what is entropy?" 
  - Reveals WHEN people are predictable
  - Links to circadian biology
  - Has clinical implications

✓ **Why we should care:**
  - Circadian disruption is major health issue
  - Could detect problems early
  - Personalized health recommendations
  - Bridges information theory and biology

✓ **Replicable:**
  - Clear time window definitions
  - Standard entropy calculations
  - Detailed methodology provided
  - Code can be shared

✓ **Goes beyond simple calculation:**
  - Creates profiles, not just numbers
  - Compares across participants
  - Links to theoretical biology (circadian rhythms)
  - Proposes novel "circadian alignment score"

---

## 🎯 MY RECOMMENDATION FOR YOU:

Based on the professor's requirements and your data, I recommend:

**#1 CHOICE: Research Question #3 (Temporal Entropy Profiles)**

**Why:**
1. **Most interesting story** - "When are you predictable?" is more engaging than "How predictable are you?"
2. **Best visualizations** - Entropy profiles across 24 hours make beautiful, interpretable graphs
3. **Strong information theory** - Uses entropy in sophisticated way (temporal profiles, not just single values)
4. **Clear health connection** - Circadian rhythms are well-studied, you can cite biology literature
5. **Novel contribution** - No one has done temporal entropy profiles of Fitbit data before

**#2 CHOICE: Research Question #2 (Compression/Huffman)**

**Why:**
1. **Direct HW6 connection** - Easier to explain because you already did Huffman coding
2. **Intuitive metric** - Compression ratio is easy to understand
3. **Solid information theory** - Uses source coding theorem, Huffman algorithm
4. **Clear methodology** - Build Huffman tree, calculate ratio, compare participants

Want me to develop either of these in even more detail? Or do you want to combine elements from multiple questions?

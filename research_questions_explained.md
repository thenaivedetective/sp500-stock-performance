# RESEARCH QUESTION OPTIONS - DETAILED EXPLANATIONS

## OPTION 1: Behavioral Regularity & Health
**Research Question:**
*"Does the entropy/complexity of daily activity patterns predict sleep quality, mood, or health risk indicators?"*

### What This Means:
Some people have very regular daily routines (wake up same time, eat at same times, exercise at same times), while others have chaotic schedules. We want to see if regularity relates to health.

### How to Calculate:

**Step 1: Divide data into days**
- Split each participant's data into 24-hour periods
- Each day = 1440 minutes (24 hours × 60 minutes)

**Step 2: Create "activity patterns" for each day**
- For each minute, discretize the METs into categories:
  - METs 10-15 = "sleeping/resting" (code: 0)
  - METs 15-25 = "light activity" (code: 1)  
  - METs 25-40 = "moderate activity" (code: 2)
  - METs 40+ = "vigorous activity" (code: 3)
- Each day becomes a sequence like: [0,0,0,0,1,1,2,1,0,0,...]

**Step 3: Calculate Shannon Entropy for each day**
```python
from collections import Counter
import math

def calculate_entropy(sequence):
    # Count frequency of each activity level
    counts = Counter(sequence)
    total = len(sequence)
    
    # Calculate probability for each level
    entropy = 0
    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)
    
    return entropy
```

**Step 4: Calculate "day-to-day" entropy**
- Compare the same hour across different days
- Example: How different is your 9am on Monday vs Tuesday vs Wednesday?
- Higher entropy = more irregular routine

**Step 5: Correlate with health outcomes**
- Average the entropy across all days for each participant
- Compare to their ground truth labels (sleep quality, mood, BMI, etc.)
- Hypothesis: Lower entropy (more regular) → better sleep/mood?

---

## OPTION 2: Activity Pattern Compression
**Research Question:**
*"How compressible are human activity patterns, and what does compression efficiency reveal about behavioral complexity?"*

### What This Means:
If someone does the exact same thing every day, their data compresses really well (like a repeating pattern). If they're unpredictable, it won't compress much. Compression ratio = measure of behavioral structure.

### How to Calculate:

**Step 1: Create activity sequences**
- Convert METs to discrete levels (0,1,2,3) as above
- Create one long sequence for entire 2-week period

**Step 2: Build Huffman Code (like HW6!)**
```python
from collections import Counter
import heapq

# Same Huffman code you built for HW6
# Build tree, generate codes for each activity level
# More frequent activities get shorter codes
```

**Step 3: Encode the sequence**
```python
# Encode the entire activity sequence
encoded = huffman.encode_text(activity_sequence)
bits_needed = len(encoded)
```

**Step 4: Calculate compression ratio**
```python
# Original size (if we used fixed-length encoding)
original_bits = len(sequence) * 2  # 2 bits for 4 levels (00,01,10,11)

# Compression ratio
compression_ratio = bits_needed / original_bits

# Lower ratio = more compressible = more structured behavior
```

**Step 5: Compare participants**
- Person A: compression ratio = 0.65 (more structured)
- Person B: compression ratio = 0.92 (more random)
- Check if compression ratio correlates with health metrics

---

## OPTION 3: Temporal Information Content
**Research Question:**
*"How does the information content (entropy) of activity patterns vary across different times of day, and can this distinguish between individuals with different health profiles?"*

### What This Means:
Maybe your morning routine is very predictable (same breakfast time, same commute), but your evenings are chaotic. We measure entropy for different time windows.

### How to Calculate:

**Step 1: Divide day into time windows**
- Morning: 6am-12pm
- Afternoon: 12pm-6pm  
- Evening: 6pm-12am
- Night: 12am-6am

**Step 2: Extract all "mornings" across all days**
```python
# Get all minutes between 6am-12pm from all days
morning_data = []
for day in all_days:
    morning_minutes = day[360:720]  # minutes 360-720 = 6am-12pm
    morning_data.extend(morning_minutes)
```

**Step 3: Calculate entropy for each time window**
```python
morning_entropy = calculate_entropy(morning_data)
afternoon_entropy = calculate_entropy(afternoon_data)
evening_entropy = calculate_entropy(evening_data)
night_entropy = calculate_entropy(night_data)
```

**Step 4: Create "entropy profile" for each person**
```
Person FS1987:
  Morning entropy: 1.2 (very regular)
  Afternoon entropy: 1.8 (somewhat varied)
  Evening entropy: 2.1 (more chaotic)
  Night entropy: 0.5 (very regular - sleeping)
```

**Step 5: Compare profiles between participants**
- Does someone with high evening entropy have worse sleep?
- Does someone with irregular mornings have higher anxiety?

---

## OPTION 4: Predictability as Digital Biomarker
**Research Question:**
*"Can the predictability (measured by entropy rate) of minute-by-minute activity patterns serve as a digital biomarker for health outcomes?"*

### What This Means:
Entropy rate measures: "Given what you did in the past hour, how predictable is the next minute?" It's about temporal patterns and transitions.

### How to Calculate:

**Step 1: Create transition sequences**
- Look at consecutive minutes
- Track: what activity level → what activity level
```
Minute 1: level 0 (resting)
Minute 2: level 0 (still resting)  ← transition: 0→0
Minute 3: level 1 (light activity) ← transition: 0→1
Minute 4: level 1 (still light)    ← transition: 1→1
```

**Step 2: Count all transitions**
```python
transitions = Counter()
for i in range(len(sequence)-1):
    current = sequence[i]
    next = sequence[i+1]
    transitions[(current, next)] += 1

# Example counts:
# (0,0): 15000 times  ← very common (staying at rest)
# (0,1): 500 times    ← occasional (rest to light)
# (2,3): 50 times     ← rare (moderate to vigorous)
```

**Step 3: Calculate conditional entropy (entropy rate)**
```python
# For each current state, calculate entropy of next states
entropy_rate = 0

for current_state in [0,1,2,3]:
    # Get all transitions FROM this state
    next_states = [transitions[(current_state, next)] 
                   for next in [0,1,2,3]]
    total = sum(next_states)
    
    if total > 0:
        # Calculate entropy of next state distribution
        state_entropy = 0
        for count in next_states:
            if count > 0:
                p = count / total
                state_entropy -= p * math.log2(p)
        
        # Weight by how often we're in this state
        weight = total / len(sequence)
        entropy_rate += weight * state_entropy
```

**Step 4: Interpret results**
- **Low entropy rate** (< 0.5): Very predictable transitions
  - Example: If resting, almost always stay resting
  - Suggests rigid, routine behavior
  
- **High entropy rate** (> 1.5): Unpredictable transitions  
  - Example: Constantly switching between activity levels
  - Suggests irregular, chaotic behavior

**Step 5: Link to health**
- Calculate entropy rate for each participant
- Correlate with health labels:
  - Does high entropy rate → poor sleep quality?
  - Does low entropy rate → better cardiovascular health?
  - Can we predict BMI category from entropy rate?

---

## WHICH ONE SHOULD YOU CHOOSE?

**Easiest to implement:** Option 1 (Behavioral Regularity)
- Simple entropy calculation
- Clear interpretation
- Direct health connection

**Most interesting findings:** Option 3 (Temporal Information)
- Shows WHEN patterns differ
- Reveals lifestyle structure
- Nice visualizations possible

**Most sophisticated:** Option 4 (Entropy Rate)
- Uses advanced information theory (conditional entropy)
- Captures temporal dependencies
- Novel "digital biomarker" concept

**Best compression connection:** Option 2 (Huffman Coding)
- Directly uses HW6 concepts
- Easy to explain to class
- Clear compression metrics

Let me know which direction appeals to you most!

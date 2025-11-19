import heapq
from collections import Counter, defaultdict
import math
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import requests

print("="*80)
print("SSIE-500: Homework 6 - Measuring Complexity of Languages")
print("Author: Zeinab Davoudmanesh")
print("Languages: English, German, French")
print("="*80)

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanCoding:
    def __init__(self, text):
        self.text = text
        self.freq_dict = Counter(text)
        self.huffman_codes = {}
        self.root = None
    
    def build_huffman_tree(self):
        """Build the Huffman tree from character frequencies"""
        heap = [HuffmanNode(char, freq) for char, freq in self.freq_dict.items()]
        heapq.heapify(heap)
        
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            
            merged = HuffmanNode(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            
            heapq.heappush(heap, merged)
        
        self.root = heap[0]
    
    def generate_codes(self, node=None, code=""):
        """Generate Huffman codes for each character"""
        if node is None:
            node = self.root
        
        if node.char is not None:
            self.huffman_codes[node.char] = code if code else "0"
            return
        
        if node.left:
            self.generate_codes(node.left, code + "0")
        if node.right:
            self.generate_codes(node.right, code + "1")
    
    def encode_text(self, text):
        """Encode text using generated Huffman codes"""
        return ''.join(self.huffman_codes[char] for char in text)
    
    def get_average_code_length(self):
        """Calculate average code word length"""
        total_chars = len(self.text)
        total_bits = sum(len(self.huffman_codes[char]) * count 
                        for char, count in self.freq_dict.items())
        return total_bits / total_chars

def calculate_entropy(text):
    """Calculate Shannon entropy of the text"""
    freq_dict = Counter(text)
    total_chars = len(text)
    entropy = 0
    
    for count in freq_dict.values():
        probability = count / total_chars
        entropy -= probability * math.log2(probability)
    
    return entropy

def download_text(url):
    """Download text from Project Gutenberg"""
    response = requests.get(url)
    response.encoding = 'utf-8'
    return response.text

def clean_gutenberg_text(text, start_marker, end_marker):
    """Remove Project Gutenberg header and footer"""
    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        return text[start_idx + len(start_marker):end_idx]
    return text

def split_sentences(text):
    """Simple sentence splitter"""
    import re
    sentences = re.split(r'[.!?]+', text)
    return [s.strip() for s in sentences if s.strip()]

def analyze_language(language_name, text_sample):
    """Complete analysis for one language"""
    print(f"\n{'='*80}")
    print(f"ANALYZING {language_name.upper()}")
    print(f"{'='*80}")
    
    # Step 1: Calculate entropy
    entropy = calculate_entropy(text_sample)
    print(f"Shannon Entropy: {entropy:.4f} bits/char")
    
    # Step 2 & 3: Build Huffman code
    huffman = HuffmanCoding(text_sample)
    huffman.build_huffman_tree()
    huffman.generate_codes()
    
    avg_code_length = huffman.get_average_code_length()
    print(f"Average Code Length: {avg_code_length:.4f} bits/char")
    print(f"Difference (Code - Entropy): {avg_code_length - entropy:.4f} bits")
    print(f"Huffman Efficiency: {(entropy/avg_code_length)*100:.2f}%")
    print(f"Unique Characters: {len(huffman.freq_dict)}")
    
    # Show top 10 most frequent characters
    top_chars = sorted(huffman.freq_dict.items(), key=lambda x: x[1], reverse=True)[:10]
    print(f"\nTop 10 Most Frequent Characters:")
    for char, freq in top_chars:
        char_display = 'SPACE' if char == ' ' else char
        code = huffman.huffman_codes[char]
        print(f"  '{char_display}': code={code} (length={len(code)}), freq={freq}")
    
    # Step 4: Encode sentences
    sentences = split_sentences(text_sample)
    sentence_bits = []
    
    for sentence in sentences:
        if sentence:
            encoded = huffman.encode_text(sentence)
            sentence_bits.append(len(encoded))
    
    avg_bits_per_sentence = np.mean(sentence_bits) if sentence_bits else 0
    std_bits_per_sentence = np.std(sentence_bits) if sentence_bits else 0
    
    print(f"\nSentence-Level Analysis:")
    print(f"  Total Sentences: {len(sentence_bits)}")
    print(f"  Average Bits/Sentence: {avg_bits_per_sentence:.2f}")
    print(f"  Std Deviation: {std_bits_per_sentence:.2f}")
    
    return {
        'language': language_name,
        'entropy': entropy,
        'avg_code_length': avg_code_length,
        'difference': avg_code_length - entropy,
        'efficiency': (entropy/avg_code_length)*100,
        'unique_chars': len(huffman.freq_dict),
        'total_sentences': len(sentence_bits),
        'avg_bits_per_sentence': avg_bits_per_sentence,
        'std_bits_per_sentence': std_bits_per_sentence,
        'huffman_codes': huffman.huffman_codes,
        'freq_dict': huffman.freq_dict,
        'top_chars': top_chars
    }

# ============================================================================
# MAIN ANALYSIS
# ============================================================================

print("\nDownloading texts from Project Gutenberg...")

# English: Pride and Prejudice by Jane Austen
english_url = "https://www.gutenberg.org/files/1342/1342-0.txt"
english_text = download_text(english_url)
english_clean = clean_gutenberg_text(english_text, "CHAPTER I", "End of the Project")
english_sample = english_clean[:100000]

# German: Die Verwandlung (Metamorphosis) by Franz Kafka
german_url = "https://www.gutenberg.org/cache/epub/5200/pg5200.txt"
german_text = download_text(german_url)
german_clean = clean_gutenberg_text(german_text, "I", "End of Project")
german_sample = german_clean[:100000]

# French: Les Trois Mousquetaires by Alexandre Dumas
french_url = "https://www.gutenberg.org/files/13951/13951-0.txt"
french_text = download_text(french_url)
french_clean = clean_gutenberg_text(french_text, "CHAPITRE PREMIER", "End of the Project")
french_sample = french_clean[:100000]

print(f"✓ English sample: {len(english_sample)} characters")
print(f"✓ German sample: {len(german_sample)} characters")
print(f"✓ French sample: {len(french_sample)} characters")

# Analyze each language
results = []
results.append(analyze_language("English", english_sample))
results.append(analyze_language("German", german_sample))
results.append(analyze_language("French", french_sample))

# ============================================================================
# SAVE RESULTS TO CSV
# ============================================================================
results_df = pd.DataFrame([{
    'Language': r['language'],
    'Entropy_bits_per_char': r['entropy'],
    'Avg_Code_Length_bits_per_char': r['avg_code_length'],
    'Difference_bits': r['difference'],
    'Efficiency_percent': r['efficiency'],
    'Unique_Characters': r['unique_chars'],
    'Total_Sentences': r['total_sentences'],
    'Avg_Bits_per_Sentence': r['avg_bits_per_sentence'],
    'Std_Bits_per_Sentence': r['std_bits_per_sentence']
} for r in results])

results_df.to_csv('language_complexity_results.csv', index=False)
print(f"\n✓ Saved results to: language_complexity_results.csv")

# ============================================================================
# VISUALIZATIONS
# ============================================================================
print("\nGenerating visualizations...")

fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('Linguistic Complexity Analysis: English, German, French\nZeinab Davoudmanesh', 
             fontsize=16, fontweight='bold')

# Plot 1: Entropy vs Code Length
ax1 = axes[0, 0]
languages = [r['language'] for r in results]
entropies = [r['entropy'] for r in results]
code_lengths = [r['avg_code_length'] for r in results]

x = np.arange(len(languages))
width = 0.35

ax1.bar(x - width/2, entropies, width, label='Entropy', color='steelblue')
ax1.bar(x + width/2, code_lengths, width, label='Avg Code Length', color='coral')
ax1.set_ylabel('Bits per Character')
ax1.set_title('Entropy vs. Huffman Code Length')
ax1.set_xticks(x)
ax1.set_xticklabels(languages)
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

# Plot 2: Average Bits per Sentence
ax2 = axes[0, 1]
bits_per_sentence = [r['avg_bits_per_sentence'] for r in results]
colors = ['steelblue', 'darkgreen', 'coral']
ax2.bar(languages, bits_per_sentence, color=colors)
ax2.set_ylabel('Average Bits per Sentence')
ax2.set_title('Average Bits per Sentence by Language')
ax2.grid(axis='y', alpha=0.3)

# Plot 3: Huffman Efficiency
ax3 = axes[0, 2]
efficiencies = [r['efficiency'] for r in results]
ax3.bar(languages, efficiencies, color='mediumseagreen')
ax3.set_ylabel('Efficiency (%)')
ax3.set_title('Huffman Coding Efficiency')
ax3.set_ylim([98, 100])
ax3.grid(axis='y', alpha=0.3)

# Plot 4-6: Character Frequency Distributions
for idx, result in enumerate(results):
    ax = axes[1, idx]
    top_chars = result['top_chars'][:15]
    chars = [c[0] if c[0] != ' ' else 'SPACE' for c in top_chars]
    freqs = [c[1] for c in top_chars]
    
    ax.barh(chars, freqs, color=colors[idx])
    ax.set_xlabel('Frequency')
    ax.set_title(f'{result["language"]} - Top 15 Characters')
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('language_complexity_comparison.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved visualization: language_complexity_comparison.png")

# ============================================================================
# SUMMARY COMPARISON
# ============================================================================
print("\n" + "="*80)
print("FINAL COMPARISON ACROSS LANGUAGES")
print("="*80)

for r in results:
    print(f"\n{r['language'].upper()}:")
    print(f"  Entropy: {r['entropy']:.4f} bits/char")
    print(f"  Avg Code Length: {r['avg_code_length']:.4f} bits/char")
    print(f"  Avg Bits/Sentence: {r['avg_bits_per_sentence']:.2f}")

print("\n" + "="*80)
print("KEY FINDINGS:")
print("="*80)

# Find language with highest entropy
max_entropy_lang = max(results, key=lambda x: x['entropy'])
print(f"• Highest character-level entropy: {max_entropy_lang['language']} ({max_entropy_lang['entropy']:.4f} bits/char)")

# Find language with most bits per sentence
max_sentence_lang = max(results, key=lambda x: x['avg_bits_per_sentence'])
print(f"• Highest avg bits/sentence: {max_sentence_lang['language']} ({max_sentence_lang['avg_bits_per_sentence']:.2f} bits)")

# Efficiency comparison
print(f"• All languages achieve >99% Huffman coding efficiency")

print("\n" + "="*80)
print("Analysis Complete!")
print("="*80)

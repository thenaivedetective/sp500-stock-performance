import heapq
from collections import Counter, defaultdict
import math
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import requests

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
        """Calculate average code word length in bits per character"""
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

def analyze_sentences(text, huffman_coding):
    """Analyze individual sentences and calculate average bits per sentence"""
    sentences = [s.strip() for s in text.replace('!', '.').replace('?', '.').split('.') if s.strip()]
    
    sentence_bits = []
    for sentence in sentences:
        try:
            encoded = huffman_coding.encode_text(sentence)
            sentence_bits.append(len(encoded))
        except KeyError:
            continue
    
    return {
        'total_sentences': len(sentences),
        'analyzed_sentences': len(sentence_bits),
        'average_bits_per_sentence': np.mean(sentence_bits) if sentence_bits else 0,
        'std_bits_per_sentence': np.std(sentence_bits) if sentence_bits else 0,
        'min_bits': min(sentence_bits) if sentence_bits else 0,
        'max_bits': max(sentence_bits) if sentence_bits else 0
    }

def download_texts():
    """Download real-world texts from Project Gutenberg"""
    texts = {
        'English': 'https://www.gutenberg.org/cache/epub/1342/pg1342.txt',
        'French': 'https://www.gutenberg.org/cache/epub/13951/pg13951.txt',
        'Spanish': 'https://www.gutenberg.org/cache/epub/2000/pg2000.txt'
    }
    
    downloaded_texts = {}
    for lang, url in texts.items():
        print(f"Downloading {lang} text...")
        response = requests.get(url)
        downloaded_texts[lang] = response.text
        print(f"✓ Downloaded {len(response.text)} characters for {lang}")
    
    return downloaded_texts

def clean_text(text):
    """Clean text by removing Project Gutenberg headers/footers"""
    start_markers = ['*** START OF', '***START OF']
    end_markers = ['*** END OF', '***END OF']
    
    start_idx = 0
    for marker in start_markers:
        idx = text.find(marker)
        if idx != -1:
            start_idx = text.find('\n', idx) + 1
            break
    
    end_idx = len(text)
    for marker in end_markers:
        idx = text.find(marker)
        if idx != -1:
            end_idx = idx
            break
    
    cleaned = text[start_idx:end_idx]
    return cleaned

def analyze_language(language_name, text):
    """Perform complete analysis for a language"""
    print(f"\n{'='*70}")
    print(f"ANALYZING {language_name.upper()}")
    print(f"{'='*70}")
    
    text = clean_text(text)
    
    if len(text) > 100000:
        text = text[:100000]
    
    print(f"Text length: {len(text)} characters")
    print(f"Unique characters: {len(set(text))}")
    
    entropy = calculate_entropy(text)
    print(f"\nInformation Entropy: {entropy:.4f} bits/character")
    
    print("\nBuilding Huffman code...")
    huffman = HuffmanCoding(text)
    huffman.build_huffman_tree()
    huffman.generate_codes()
    
    avg_code_length = huffman.get_average_code_length()
    print(f"Average Huffman code length: {avg_code_length:.4f} bits/character")
    print(f"Difference (Code - Entropy): {avg_code_length - entropy:.4f} bits")
    
    print("\nSample Huffman codes:")
    sample_chars = sorted(huffman.freq_dict.items(), key=lambda x: x[1], reverse=True)[:10]
    for char, freq in sample_chars:
        display_char = repr(char) if char in ['\n', '\t', ' '] else char
        print(f"  {display_char:5s}: {huffman.huffman_codes[char]:15s} (freq: {freq})")
    
    print("\nAnalyzing sentences...")
    sentence_analysis = analyze_sentences(text, huffman)
    print(f"Total sentences: {sentence_analysis['total_sentences']}")
    print(f"Average bits per sentence: {sentence_analysis['average_bits_per_sentence']:.2f}")
    print(f"Standard deviation: {sentence_analysis['std_bits_per_sentence']:.2f}")
    print(f"Min/Max bits: {sentence_analysis['min_bits']:.0f} / {sentence_analysis['max_bits']:.0f}")
    
    return {
        'language': language_name,
        'text_length': len(text),
        'unique_chars': len(set(text)),
        'entropy': entropy,
        'avg_code_length': avg_code_length,
        'compression_efficiency': entropy / avg_code_length if avg_code_length > 0 else 0,
        'sentence_stats': sentence_analysis,
        'huffman': huffman
    }

def create_visualizations(results):
    """Create comprehensive visualizations comparing all languages"""
    sns.set_style("whitegrid")
    fig = plt.figure(figsize=(16, 12))
    
    languages = [r['language'] for r in results]
    entropies = [r['entropy'] for r in results]
    avg_code_lengths = [r['avg_code_length'] for r in results]
    avg_bits_per_sentence = [r['sentence_stats']['average_bits_per_sentence'] for r in results]
    
    ax1 = plt.subplot(2, 3, 1)
    x = np.arange(len(languages))
    width = 0.35
    ax1.bar(x - width/2, entropies, width, label='Entropy', alpha=0.8)
    ax1.bar(x + width/2, avg_code_lengths, width, label='Avg Code Length', alpha=0.8)
    ax1.set_xlabel('Language')
    ax1.set_ylabel('Bits per Character')
    ax1.set_title('Entropy vs Huffman Code Length')
    ax1.set_xticks(x)
    ax1.set_xticklabels(languages)
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    ax2 = plt.subplot(2, 3, 2)
    colors = sns.color_palette("husl", len(languages))
    ax2.bar(languages, avg_bits_per_sentence, color=colors, alpha=0.8)
    ax2.set_xlabel('Language')
    ax2.set_ylabel('Bits per Sentence')
    ax2.set_title('Average Bits per Sentence (Huffman Encoded)')
    ax2.grid(axis='y', alpha=0.3)
    
    ax3 = plt.subplot(2, 3, 3)
    efficiency = [r['compression_efficiency'] * 100 for r in results]
    ax3.bar(languages, efficiency, color=colors, alpha=0.8)
    ax3.set_xlabel('Language')
    ax3.set_ylabel('Efficiency (%)')
    ax3.set_title('Huffman Coding Efficiency\n(Entropy / Code Length × 100)')
    ax3.axhline(y=100, color='r', linestyle='--', linewidth=1, alpha=0.5)
    ax3.grid(axis='y', alpha=0.3)
    
    for idx, result in enumerate(results):
        ax = plt.subplot(2, 3, 4 + idx)
        freq_dict = result['huffman'].freq_dict
        top_chars = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)[:15]
        chars = [repr(c) if c in ['\n', '\t', ' '] else c for c, _ in top_chars]
        freqs = [f for _, f in top_chars]
        
        ax.barh(chars, freqs, color=colors[idx], alpha=0.8)
        ax.set_xlabel('Frequency')
        ax.set_title(f'Top 15 Characters - {result["language"]}')
        ax.invert_yaxis()
    
    plt.tight_layout()
    plt.savefig('language_complexity_analysis.png', dpi=300, bbox_inches='tight')
    print("\n✓ Saved visualization to 'language_complexity_analysis.png'")
    
    return fig

def print_comparison_table(results):
    """Print a comprehensive comparison table"""
    print("\n" + "="*90)
    print("COMPARATIVE ANALYSIS ACROSS LANGUAGES")
    print("="*90)
    
    data = {
        'Language': [r['language'] for r in results],
        'Entropy (bits/char)': [f"{r['entropy']:.4f}" for r in results],
        'Avg Code Length (bits/char)': [f"{r['avg_code_length']:.4f}" for r in results],
        'Difference': [f"{r['avg_code_length'] - r['entropy']:.4f}" for r in results],
        'Avg Bits/Sentence': [f"{r['sentence_stats']['average_bits_per_sentence']:.2f}" for r in results],
        'Unique Chars': [r['unique_chars'] for r in results]
    }
    
    df = pd.DataFrame(data)
    print(df.to_string(index=False))
    print("="*90)

def generate_report(results):
    """Generate findings and discussion"""
    print("\n" + "="*90)
    print("FINDINGS AND DISCUSSION")
    print("="*90)
    
    sorted_results = sorted(results, key=lambda x: x['sentence_stats']['average_bits_per_sentence'])
    
    print("\n1. INFORMATION ENTROPY:")
    print("   Information entropy measures the average information content per character.")
    print("   Higher entropy indicates more unpredictability and complexity.")
    entropy_sorted = sorted(results, key=lambda x: x['entropy'], reverse=True)
    for i, r in enumerate(entropy_sorted, 1):
        print(f"   {i}. {r['language']}: {r['entropy']:.4f} bits/character")
    
    print("\n2. HUFFMAN CODING EFFICIENCY:")
    print("   Huffman coding achieves near-optimal compression.")
    print("   The difference between code length and entropy should be minimal (<0.1 bits).")
    for r in results:
        diff = r['avg_code_length'] - r['entropy']
        print(f"   {r['language']}: Difference = {diff:.4f} bits (Efficiency: {r['compression_efficiency']*100:.2f}%)")
    
    print("\n3. AVERAGE BITS PER SENTENCE:")
    print("   This metric reflects both sentence structure and character complexity.")
    for i, r in enumerate(sorted_results, 1):
        avg_bits = r['sentence_stats']['average_bits_per_sentence']
        std_bits = r['sentence_stats']['std_bits_per_sentence']
        print(f"   {i}. {r['language']}: {avg_bits:.2f} ± {std_bits:.2f} bits")
    
    print("\n4. COMPARATIVE INSIGHTS:")
    
    most_complex = max(results, key=lambda x: x['entropy'])
    least_complex = min(results, key=lambda x: x['entropy'])
    
    print(f"   • {most_complex['language']} has the highest character-level entropy ({most_complex['entropy']:.4f} bits),")
    print(f"     indicating more diverse character usage.")
    
    print(f"   • {least_complex['language']} has the lowest character-level entropy ({least_complex['entropy']:.4f} bits),")
    print(f"     suggesting more predictable character patterns.")
    
    longest_sentences = max(results, key=lambda x: x['sentence_stats']['average_bits_per_sentence'])
    shortest_sentences = min(results, key=lambda x: x['sentence_stats']['average_bits_per_sentence'])
    
    print(f"\n   • {longest_sentences['language']} has the longest encoded sentences on average")
    print(f"     ({longest_sentences['sentence_stats']['average_bits_per_sentence']:.2f} bits),")
    print(f"     which may indicate longer sentence structures or richer vocabulary.")
    
    print(f"   • {shortest_sentences['language']} has the shortest encoded sentences")
    print(f"     ({shortest_sentences['sentence_stats']['average_bits_per_sentence']:.2f} bits).")
    
    print("\n5. LINGUISTIC IMPLICATIONS:")
    print("   • Character entropy reflects the diversity of the alphabet and letter frequencies.")
    print("   • Romance languages (French, Spanish) share similar character sets (with accents).")
    print("   • Huffman coding efficiently compresses text by assigning shorter codes to")
    print("     frequent characters, demonstrating information theory's practical applications.")
    print("   • Average bits per sentence captures both character-level and sentence-level")
    print("     complexity, offering insights into linguistic structure.")
    
    print("\n" + "="*90)

def main():
    print("="*90)
    print("HOMEWORK 6: MEASURING COMPLEXITY OF LANGUAGES")
    print("Information Entropy and Huffman Coding Analysis")
    print("="*90)
    
    print("\n[STEP 1] Downloading real-world texts from Project Gutenberg...")
    texts = download_texts()
    
    results = []
    for language in ['English', 'French', 'Spanish']:
        result = analyze_language(language, texts[language])
        results.append(result)
    
    print_comparison_table(results)
    generate_report(results)
    
    print("\n[VISUALIZATION] Creating comparative plots...")
    create_visualizations(results)
    
    print("\n" + "="*90)
    print("ANALYSIS COMPLETE!")
    print("="*90)
    print("\nGenerated files:")
    print("  • language_complexity_analysis.png - Comparative visualizations")
    print("\nNext steps for your report:")
    print("  1. Copy the printed results and tables")
    print("  2. Include the generated visualization")
    print("  3. Add this code to your LaTeX appendix")
    print("  4. Expand the discussion section with your own insights")
    print("="*90)

if __name__ == "__main__":
    main()

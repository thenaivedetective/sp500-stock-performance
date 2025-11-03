import math
from collections import Counter, defaultdict
import os

def calculate_entropy(text):
    """
    Calculate information entropy of the frequency distribution of symbols.
    H(X) = -Σ p(x) * log2(p(x))
    """
    if not text:
        return 0.0
    
    # Count frequency of each symbol
    symbol_counts = Counter(text)
    total_symbols = len(text)
    
    # Calculate entropy
    entropy = 0.0
    for count in symbol_counts.values():
        probability = count / total_symbols
        entropy -= probability * math.log2(probability)
    
    return entropy

def calculate_mutual_information(text):
    """
    Calculate mutual information between two consecutive symbols.
    MI(X;Y) = Σ p(x,y) * log2(p(x,y) / (p(x) * p(y)))
    """
    if len(text) < 2:
        return 0.0
    
    # Count single symbols
    single_counts = Counter(text)
    total_symbols = len(text)
    
    # Count consecutive symbol pairs
    pair_counts = defaultdict(int)
    for i in range(len(text) - 1):
        pair = (text[i], text[i + 1])
        pair_counts[pair] += 1
    
    total_pairs = len(text) - 1
    
    # Calculate mutual information
    mutual_info = 0.0
    for pair, pair_count in pair_counts.items():
        p_xy = pair_count / total_pairs  # Joint probability
        p_x = single_counts[pair[0]] / total_symbols  # Marginal probability of first symbol
        p_y = single_counts[pair[1]] / total_symbols  # Marginal probability of second symbol
        
        mutual_info += p_xy * math.log2(p_xy / (p_x * p_y))
    
    return mutual_info

def analyze_language(file_path, language_name):
    """
    Analyze a text file and calculate entropy and mutual information.
    """
    try:
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        text = None
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    text = f.read()
                break
            except UnicodeDecodeError:
                continue
        
        if text is None:
            print(f"Error: Could not read {file_path} with any encoding")
            return None
        
        # Calculate metrics
        entropy = calculate_entropy(text)
        mutual_info = calculate_mutual_information(text)
        
        # Count statistics
        total_chars = len(text)
        unique_symbols = len(set(text))
        
        result = {
            'language': language_name,
            'file': file_path,
            'total_characters': total_chars,
            'unique_symbols': unique_symbols,
            'entropy': entropy,
            'mutual_information': mutual_info
        }
        
        return result
        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        return None
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return None

def print_results(results):
    """
    Print analysis results in a formatted way.
    """
    print("\n" + "="*80)
    print("LANGUAGE COMPLEXITY ANALYSIS RESULTS")
    print("="*80 + "\n")
    
    for result in results:
        if result:
            print(f"Language: {result['language']}")
            print(f"File: {result['file']}")
            print(f"Total Characters: {result['total_characters']:,}")
            print(f"Unique Symbols: {result['unique_symbols']}")
            print(f"Information Entropy: {result['entropy']:.6f} bits")
            print(f"Mutual Information: {result['mutual_information']:.6f} bits")
            print("-" * 80 + "\n")
    
    # Comparison section
    if len(results) >= 2:
        print("\n" + "="*80)
        print("COMPARISON")
        print("="*80 + "\n")
        
        # Sort by entropy
        sorted_by_entropy = sorted([r for r in results if r], 
                                   key=lambda x: x['entropy'], reverse=True)
        print("Languages ranked by Entropy (highest to lowest):")
        for i, result in enumerate(sorted_by_entropy, 1):
            print(f"{i}. {result['language']}: {result['entropy']:.6f} bits")
        
        print("\nLanguages ranked by Mutual Information (highest to lowest):")
        sorted_by_mi = sorted([r for r in results if r], 
                             key=lambda x: x['mutual_information'], reverse=True)
        for i, result in enumerate(sorted_by_mi, 1):
            print(f"{i}. {result['language']}: {result['mutual_information']:.6f} bits")
        
        print("\n" + "="*80)

def main():
    """
    Main function to analyze text files for different languages.
    """
    print("Language Complexity Analysis")
    print("SSIE-500: Homework 5\n")
    
    # Define the text files for each language
    # Update these paths with your actual text file names
    languages = [
        ('english.txt', 'English'),
        ('french.txt', 'French'),
        ('arabic.txt', 'Arabic')
    ]
    
    results = []
    
    print("Analyzing text files...\n")
    for file_path, language_name in languages:
        if os.path.exists(file_path):
            print(f"Processing {language_name}...")
            result = analyze_language(file_path, language_name)
            results.append(result)
        else:
            print(f"Warning: {file_path} not found. Please add this file to continue.")
            results.append(None)
    
    print_results(results)
    
    print("\nNote: Please place your text files (english.txt, french.txt, arabic.txt)")
    print("in the same directory as this script and run again.")

if __name__ == "__main__":
    main()

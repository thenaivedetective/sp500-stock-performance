SSIE-500 Homework 5 - Language Complexity Analysis
================================================

This program calculates:
1. Information Entropy: H(X) = -Σ p(x) * log2(p(x))
2. Mutual Information: MI(X;Y) = Σ p(x,y) * log2(p(x,y) / (p(x) * p(y)))

SETUP:
------
1. Place your text files in this directory with these names:
   - english.txt (English text)
   - french.txt (French text)
   - arabic.txt (Arabic text)

2. Run the program:
   python main.py

The program will analyze all three languages and provide:
- Total character count
- Number of unique symbols
- Information entropy (in bits)
- Mutual information between consecutive symbols (in bits)
- Comparative ranking

You can then use these results for your LaTeX report.

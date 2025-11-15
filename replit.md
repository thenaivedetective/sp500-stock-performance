# SSIE500 Homework 6

## Overview
Academic project for SSIE500 course implementing information entropy analysis and Huffman coding to measure and compare complexity across three human languages.

**Current Status:** Complete implementation with real-world text analysis

## Project Description
This project analyzes linguistic complexity by:
1. Calculating Shannon information entropy for character distributions
2. Implementing Huffman coding algorithm for optimal text compression
3. Comparing English, French, and Spanish texts from classic literature
4. Analyzing sentence-level compression metrics across languages

## Data Sources
Real-world texts from Project Gutenberg:
- **English**: Pride and Prejudice by Jane Austen
- **French**: Les Trois Mousquetaires by Alexandre Dumas
- **Spanish**: Don Quijote by Miguel de Cervantes

## Key Findings
- **French** has the highest character-level entropy (4.68 bits/char)
- **Spanish** has the longest average sentences when encoded (1191 bits/sentence)
- Huffman coding achieves 99%+ efficiency across all languages
- Character entropy differences reflect alphabet diversity and letter frequency patterns

## User Preferences
- Preferred communication style: Simple, everyday language
- Appreciates step-by-step explanations with concrete examples

## System Architecture
- **Language**: Python 3
- **Development Environment**: Replit-based development
- **Project Type**: Data analysis and computational research project
- **Key Libraries**: 
  - numpy, pandas for data processing
  - matplotlib, seaborn for visualization
  - requests for downloading real-world texts
  - heapq, collections for Huffman tree implementation

## Generated Outputs
- `language_complexity_analysis.png`: Comprehensive 6-panel visualization showing:
  - Entropy vs code length comparison
  - Average bits per sentence
  - Huffman coding efficiency
  - Character frequency distributions for each language

## Implementation Details
- Complete Huffman tree construction using heap-based algorithm
- Shannon entropy calculation with proper logarithmic formulas
- Sentence-level analysis with statistical metrics
- Clean text preprocessing to remove Project Gutenberg headers/footers
- 100,000 character samples from each text for practical computation

## Recent Changes (November 15, 2025)
- Implemented complete Huffman coding algorithm with binary encoding
- Added information entropy calculation
- Created multi-language analysis pipeline
- Generated comparative visualizations
- Completed findings and discussion section with linguistic insights

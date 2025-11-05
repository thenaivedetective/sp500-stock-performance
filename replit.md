# Language Complexity Analysis Tool

## Overview

This is an educational Python application designed for SSIE-500 Homework 5 (for Zeinab) that performs linguistic analysis on text files. The program calculates information-theoretic measures to compare the complexity of different languages:

- **Information Entropy**: Measures the average information content per symbol using Shannon entropy
- **Mutual Information**: Quantifies the statistical dependency between consecutive symbols in text

The application analyzes text samples from three languages (English, Spanish, and Arabic) and provides comparative rankings based on information-theoretic metrics.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Application Type
**Standalone Command-Line Script** - Single-file Python program (`main.py`) that performs batch text analysis without a web interface, database, or persistent storage.

### Core Components

**Text Processing Pipeline**:
- Reads text files from the local filesystem
- Expected input files: `english.txt`, `spanish.txt`, `arabic.txt`
- Processes raw text character-by-character without preprocessing

**Statistical Analysis Engine**:
- **Entropy Calculator**: Implements Shannon entropy formula H(X) = -Σ p(x) * log2(p(x))
  - Uses `collections.Counter` for frequency distribution
  - Calculates probability distributions from symbol counts
  - Returns entropy in bits
  
- **Mutual Information Calculator**: Implements MI(X;Y) = Σ p(x,y) * log2(p(x,y) / (p(x) * p(y)))
  - Analyzes bigram (consecutive symbol pair) statistics
  - Computes joint and marginal probabilities
  - Measures statistical dependency between adjacent characters
  - Fully implemented and functional

**Output Generation**:
- Provides statistics for each language including:
  - Total character count
  - Number of unique symbols
  - Information entropy (bits)
  - Mutual information (bits)
- Generates comparative rankings across languages
- Results intended for inclusion in LaTeX academic reports

### Design Patterns

**Functional Programming Approach**: Pure functions for calculations (`calculate_entropy`, `calculate_mutual_information`) that take text input and return numerical metrics without side effects.

**File-Based I/O**: Simple file reading pattern without streaming or chunking, suitable for academic text samples of moderate size.

### Data Structures

- `Counter` (from collections): Frequency distribution of individual symbols
- `defaultdict(int)`: Efficient storage of bigram counts
- Tuples: Represent consecutive symbol pairs for mutual information calculation

### Project Status

The project is complete and fully functional. All analysis functions are implemented correctly and tested.

## External Dependencies

### Python Standard Library
- `math`: Logarithmic calculations (log2 for information theory)
- `collections.Counter`: Symbol frequency counting
- `collections.defaultdict`: Bigram frequency storage
- `os`: File system operations (imported but may not be actively used)

### No External Services
This is a self-contained local analysis tool with no:
- Database connections
- Web APIs
- Cloud services
- Authentication systems
- Network dependencies

### Input Files
Text corpus files present in the repository root:
- `english.txt` - Pride and Prejudice by Jane Austen (3,483 characters)
- `spanish.txt` - Don Quijote by Miguel de Cervantes (1,386 characters)
- `arabic.txt` - Kalila wa-Dimna classical Arabic text (5,634 characters)

### Output Files
- `report_template.tex` - LaTeX template for academic report (includes Zeinab's name as author)
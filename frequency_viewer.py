#!/usr/bin/env python3
"""
lukin e nimi kon - Simple Frequency Viewer

A standalone tool for visualizing letter frequency analysis and comparing text patterns
with English and French language frequencies.

Author: GitHub Community
License: MIT
Version: 1.0.0
"""

import matplotlib.pyplot as plt
import string
from collections import Counter
import argparse
import sys

# Expected letter frequencies in English (percentages)
ENGLISH_FREQ = {
    'e': 12.7, 't': 9.1, 'a': 8.2, 'o': 7.5, 'i': 7.0, 'n': 6.7, 's': 6.3, 'h': 6.1,
    'r': 6.0, 'd': 4.3, 'l': 4.0, 'c': 2.8, 'u': 2.8, 'm': 2.4, 'w': 2.4, 'f': 2.2,
    'g': 2.0, 'y': 2.0, 'p': 1.9, 'b': 1.3, 'v': 1.0, 'k': 0.8, 'j': 0.15, 'x': 0.15,
    'q': 0.10, 'z': 0.07
}

# Expected letter frequencies in French (percentages)
FRENCH_FREQ = {
    'e': 14.7, 'a': 7.6, 'i': 7.5, 't': 7.2, 'n': 7.1, 'r': 6.6, 's': 6.5, 'u': 6.3,
    'l': 5.5, 'o': 5.4, 'm': 3.0, 'd': 3.7, 'c': 3.3, 'p': 3.0, 'h': 0.9, 'g': 1.1,
    'b': 0.9, 'v': 1.6, 'j': 0.5, 'f': 1.1, 'q': 1.4, 'z': 0.3, 'x': 0.4, 'w': 0.1,
    'y': 0.2, 'k': 0.05
}

def analyze_letter_frequency(text):
    """Analyze the frequency of each letter in the given text."""
    letters_only = ''.join(char.lower() for char in text if char.isalpha())
    letter_counts = Counter(letters_only)
    total_letters = len(letters_only)
    
    frequencies = {}
    for letter in string.ascii_lowercase:
        count = letter_counts.get(letter, 0)
        percentage = (count / total_letters * 100) if total_letters > 0 else 0
        frequencies[letter] = {'count': count, 'percentage': percentage}
    
    return frequencies, total_letters

def print_frequency_table(frequencies, total_letters):
    """Print a detailed frequency table."""
    print(f"\n📊 FREQUENCY ANALYSIS")
    print("=" * 60)
    print(f"Total letters analyzed: {total_letters}")
    print()
    
    # Sort by frequency for display
    sorted_freq = sorted(frequencies.items(), key=lambda x: x[1]['percentage'], reverse=True)
    
    print("Letter | Count | Percentage | English Expected | French Expected")
    print("-" * 60)
    
    for letter, data in sorted_freq:
        if data['count'] > 0:  # Only show letters that appear
            eng_exp = ENGLISH_FREQ[letter]
            fr_exp = FRENCH_FREQ[letter]
            print(f"  {letter}    |  {data['count']:3d}  |   {data['percentage']:5.1f}%    |      {eng_exp:5.1f}%      |     {fr_exp:5.1f}%")

def create_comparison_graph(frequencies, title="Letter Frequency Comparison"):
    """Create a comparison graph showing text vs English vs French frequencies."""
    letters = list(string.ascii_lowercase)
    text_freqs = [frequencies[letter]['percentage'] for letter in letters]
    english_freqs = [ENGLISH_FREQ[letter] for letter in letters]
    french_freqs = [FRENCH_FREQ[letter] for letter in letters]
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(15, 8))
    
    x = range(len(letters))
    width = 0.25
    
    # Create bars
    bars1 = ax.bar([i - width for i in x], text_freqs, width, label='Text', color='lightblue', alpha=0.8)
    bars2 = ax.bar(x, english_freqs, width, label='English Expected', color='lightgreen', alpha=0.8)
    bars3 = ax.bar([i + width for i in x], french_freqs, width, label='French Expected', color='lightcoral', alpha=0.8)
    
    # Customize the plot
    ax.set_xlabel('Letters')
    ax.set_ylabel('Frequency (%)')
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(letters)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars for text frequencies (only non-zero)
    for bar, freq in zip(bars1, text_freqs):
        if freq > 0:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                   f'{freq:.1f}', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.show()

def calculate_language_similarity(frequencies):
    """Calculate similarity scores to English and French."""
    english_score = 0
    french_score = 0
    
    for letter in string.ascii_lowercase:
        observed_freq = frequencies[letter]['percentage']
        english_expected = ENGLISH_FREQ[letter]
        french_expected = FRENCH_FREQ[letter]
        
        # Use negative squared difference (closer to 0 is better)
        english_score -= (observed_freq - english_expected) ** 2
        french_score -= (observed_freq - french_expected) ** 2
    
    return english_score, french_score

def analyze_text_frequency(text, show_graph=True, show_table=True):
    """Main function to analyze text frequency."""
    print("🔍 LUKIN E NIMI KON - Frequency Viewer")
    print("=" * 50)
    print(f"Analyzing: {text[:80]}{'...' if len(text) > 80 else ''}")
    
    # Analyze frequencies
    frequencies, total_letters = analyze_letter_frequency(text)
    
    if total_letters == 0:
        print("❌ No letters found to analyze!")
        return
    
    # Show frequency table if requested
    if show_table:
        print_frequency_table(frequencies, total_letters)
    
    # Calculate language similarity
    english_score, french_score = calculate_language_similarity(frequencies)
    
    print(f"\n🎯 LANGUAGE SIMILARITY SCORES")
    print("=" * 30)
    print(f"English similarity: {english_score:.1f}")
    print(f"French similarity:  {french_score:.1f}")
    
    if french_score > english_score:
        print("→ Text appears more similar to French patterns")
    elif english_score > french_score:
        print("→ Text appears more similar to English patterns")
    else:
        print("→ Text similarity is ambiguous")
    
    # Show top 5 most frequent letters
    sorted_freq = sorted(frequencies.items(), key=lambda x: x[1]['count'], reverse=True)
    print(f"\n📈 TOP 5 MOST FREQUENT LETTERS")
    print("=" * 35)
    for i, (letter, data) in enumerate(sorted_freq[:5], 1):
        if data['count'] > 0:
            print(f"  {i}. '{letter}': {data['count']} times ({data['percentage']:.1f}%)")
    
    # Show comparison graph if requested
    if show_graph:
        create_comparison_graph(frequencies, f"Frequency Analysis: {text[:30]}{'...' if len(text) > 30 else ''}")

def main():
    """Main function with command line support."""
    parser = argparse.ArgumentParser(
        description='lukin e nimi kon - Frequency Viewer v1.0.0\nVisualize letter frequencies and compare with language patterns',
        epilog='Examples:\n  python frequency_viewer.py "sample text here"\n  python frequency_viewer.py -f textfile.txt\n  python frequency_viewer.py "text" --no-graph --no-table',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('text', nargs='?', help='Text to analyze (or use --file)')
    parser.add_argument('-f', '--file', help='Read text from file')
    parser.add_argument('--no-graph', action='store_true', help='Skip showing the comparison graph')
    parser.add_argument('--no-table', action='store_true', help='Skip showing the frequency table')
    parser.add_argument('--version', action='version', version='lukin e nimi kon - Frequency Viewer v1.0.0')
    
    args = parser.parse_args()
    
    # Get input text
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read().strip()
        except FileNotFoundError:
            print(f"❌ Error: File '{args.file}' not found.")
            return 1
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return 1
    elif args.text:
        text = args.text
    else:
        print("🔍 LUKIN E NIMI KON - Frequency Viewer")
        print("Enter text to analyze (or use -h for help):")
        text = input("> ").strip()
        if not text:
            print("❌ No text provided!")
            return 1
    
    if not text:
        print("❌ No text provided!")
        return 1
    
    # Analyze the text
    try:
        analyze_text_frequency(
            text, 
            show_graph=not args.no_graph, 
            show_table=not args.no_table
        )
        return 0
    except KeyboardInterrupt:
        print("\n\n👋 Analysis interrupted by user.")
        return 0
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 
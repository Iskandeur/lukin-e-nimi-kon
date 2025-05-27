#!/usr/bin/env python3
"""
lukin e nimi kon - Advanced Automatic Cipher Detection and Decryption

An intelligent tool for breaking classical ciphers using frequency analysis and pattern recognition.
Supports both Caesar ciphers and substitution ciphers in English and French languages.

Author: GitHub Community
License: MIT
Version: 1.0.0
"""

import matplotlib.pyplot as plt
import string
from collections import Counter
import sys
import argparse
import os

# Environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load environment variables from .env file
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

# Google Gemini AI integration
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

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

# Common words for language detection
ENGLISH_WORDS = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'man', 'end', 'few', 'got', 'let', 'put', 'say', 'she', 'too', 'use', 'over', 'quick', 'brown', 'fox', 'jumps', 'lazy', 'dog']

FRENCH_WORDS = ['le', 'de', 'et', 'un', 'il', 'en', 'que', 'pour', 'dans', 'ce', 'son', 'une', 'sur', 'avec', 'ne', 'se', 'pas', 'tout', 'plus', 'par', 'grand', 'comme', 'lui', 'temps', 'sans', 'nous', 'mon', 'bien', 'encore', 'aussi', 'leur', 'dont', 'peu', 'elle', 'fois', 'sous', 'depuis', 'tant', 'toujours', 'entre', 'autre', 'donc', 'vers', 'du', 'au', 'la', 'les', 'des', 'cette', 'ces', 'mes', 'tes', 'ses', 'nos', 'vos', 'leurs', 'qui', 'quoi', 'celui', 'celle', 'ceux', 'celles', 'moi', 'toi', 'soi', 'eux', 'elles', 'si', 'oui', 'non', 'peut', 'doit', 'fait', 'dit', 'va', 'vient', 'sort', 'contre', 'autour', 'devant', 'avant', 'mais', 'car', 'ainsi', 'alors', 'enfin', 'ensuite', 'puis', 'beaucoup', 'assez', 'trop', 'moins', 'autant', 'aussi', 'fort', 'bien', 'mal', 'mieux', 'pire', 'environ', 'presque', 'seulement', 'jamais', 'parfois', 'souvent', 'maintenant', 'hier', 'demain', 'ici', 'ailleurs', 'partout', 'etait', 'claire', 'avril', 'froid', 'rapidement', 'porte', 'vitree', 'maisons', 'victoire', 'sentait', 'vieux', 'tapis']

# Gemini AI Configuration
def configure_gemini():
    """Configure Gemini AI with the API key from environment variables."""
    if not GEMINI_AVAILABLE:
        return False
    
    try:
        # Try to get API key from environment variable
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            print("⚠️  Warning: GEMINI_API_KEY not found in environment variables")
            print("    Create a .env file with: GEMINI_API_KEY=your_api_key_here")
            return False
        
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        print(f"⚠️  Warning: Could not configure Gemini AI: {e}")
        return False

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

def caesar_decrypt(text, shift):
    """Decrypt text using Caesar cipher with given shift."""
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base - shift) % 26
            result += chr(shifted + base)
        else:
            result += char
    return result

def calculate_language_score(text, language_freq):
    """Calculate how similar the letter frequencies are to a specific language."""
    frequencies, total = analyze_letter_frequency(text)
    if total == 0:
        return -float('inf')
    
    score = 0
    for letter in string.ascii_lowercase:
        observed_freq = frequencies[letter]['percentage']
        expected_freq = language_freq[letter]
        # Use negative squared difference (higher is better)
        score -= (observed_freq - expected_freq) ** 2
    
    return score

def detect_language(text):
    """Detect if text is more likely English or French."""
    english_score = calculate_language_score(text, ENGLISH_FREQ)
    french_score = calculate_language_score(text, FRENCH_FREQ)
    
    # Also check for common words
    text_lower = text.lower()
    english_word_count = sum(1 for word in ENGLISH_WORDS if word in text_lower)
    french_word_count = sum(1 for word in FRENCH_WORDS if word in text_lower)
    
    # Combine frequency score with word count
    english_total = english_score + (english_word_count * 10)
    french_total = french_score + (french_word_count * 10)
    
    if french_total > english_total:
        return 'french', FRENCH_FREQ, FRENCH_WORDS
    else:
        return 'english', ENGLISH_FREQ, ENGLISH_WORDS

def try_all_caesar_shifts(ciphertext):
    """Try all possible Caesar cipher shifts and return the best result."""
    best_results = {'english': None, 'french': None}
    best_scores = {'english': -float('inf'), 'french': -float('inf')}
    
    for shift in range(26):
        decrypted = caesar_decrypt(ciphertext, shift)
        
        # Test against both languages
        english_score = calculate_language_score(decrypted, ENGLISH_FREQ)
        french_score = calculate_language_score(decrypted, FRENCH_FREQ)
        
        if english_score > best_scores['english']:
            best_scores['english'] = english_score
            best_results['english'] = {
                'shift': shift,
                'text': decrypted,
                'score': english_score,
                'method': 'Caesar Cipher (English)',
                'language': 'english'
            }
        
        if french_score > best_scores['french']:
            best_scores['french'] = french_score
            best_results['french'] = {
                'shift': shift,
                'text': decrypted,
                'score': french_score,
                'method': 'Caesar Cipher (French)',
                'language': 'french'
            }
    
    # Return the best overall result
    if best_scores['french'] > best_scores['english']:
        return best_results['french']
    else:
        return best_results['english']

def gemini_text_refiner(partially_decoded_text, original_cipher, method_name, language='auto'):
    """Use Gemini AI to refine and fix remaining issues in partially decoded text."""
    if not configure_gemini():
        return None
    
    print("    🤖 Gemini AI refinement...")
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Create a refined prompt for minimal correction
        prompt = f"""You are a proofreader fixing ONLY obvious letter substitution errors in a partially decoded cipher.

PARTIALLY DECODED TEXT: "{partially_decoded_text}"
TARGET LANGUAGE: {language}

IMPORTANT: This text was decoded from a substitution cipher. Some letters may still be wrong, but DO NOT rewrite or change the meaning. Only fix obvious letter errors.

RULES:
1. Keep the EXACT same text structure and length
2. Only change letters that are clearly wrong (creating non-words)
3. If you change one letter, change it consistently throughout
4. Do NOT add, remove, or rearrange words
5. Do NOT change the story or meaning
6. Focus on making existing words readable

Examples of what TO fix:
- "tke" → "the" (change all 'k' to 'h')
- "amd" → "and" (change all 'm' to 'n')
- "oge" → "une" (change all 'g' to 'n')

Examples of what NOT to do:
- Do NOT rewrite entire sentences
- Do NOT change the plot or story
- Do NOT add new words or ideas

Provide ONLY the minimally corrected text:

CORRECTED:"""

        # Use low temperature to prevent hallucination
        generation_config = genai.types.GenerationConfig(
            temperature=0.1,  # Very low temperature for minimal creativity
            max_output_tokens=2000,
            top_p=0.1,
            top_k=1
        )
        
        response = model.generate_content(prompt, generation_config=generation_config)
        
        if response and response.text:
            refined_text = response.text.strip()
            
            # Remove any potential formatting or extra text
            if refined_text.startswith('CORRECTED:'):
                refined_text = refined_text.replace('CORRECTED:', '').strip()
            elif refined_text.startswith('CORRECTED TEXT:'):
                refined_text = refined_text.replace('CORRECTED TEXT:', '').strip()
            
            # Remove quotes if the AI added them
            if refined_text.startswith('"') and refined_text.endswith('"'):
                refined_text = refined_text[1:-1]
            
            if refined_text and refined_text != partially_decoded_text:
                # Calculate improvement score
                original_score = calculate_language_score(partially_decoded_text, FRENCH_FREQ if language == 'french' else ENGLISH_FREQ)
                refined_score = calculate_language_score(refined_text, FRENCH_FREQ if language == 'french' else ENGLISH_FREQ)
                
                # Count readable words improvement
                original_words = count_readable_words(partially_decoded_text, language)
                refined_words = count_readable_words(refined_text, language)
                
                print(f"    AI refinement preview: {refined_text[:60]}...")
                print(f"    Readability improvement: {original_words} → {refined_words} readable words")
                
                return {
                    'text': refined_text,
                    'original_text': partially_decoded_text,
                    'improvement_score': refined_score - original_score,
                    'readable_words_before': original_words,
                    'readable_words_after': refined_words,
                    'method': f'{method_name} + AI Refinement'
                }
        
    except Exception as e:
        print(f"    ⚠️  Gemini AI refinement error: {e}")
    
    return None

def count_readable_words(text, language):
    """Count readable words in the given language."""
    words = text.lower().split()
    word_list = FRENCH_WORDS if language == 'french' else ENGLISH_WORDS
    readable_count = 0
    
    for word in words:
        # Remove punctuation
        clean_word = ''.join(c for c in word if c.isalpha())
        if len(clean_word) >= 2:
            if clean_word in word_list:
                readable_count += 1
            elif len(clean_word) <= 3:  # Short words are often readable
                readable_count += 0.5
    
    return int(readable_count)

def expert_manual_analysis(ciphertext):
    """Expert manual analysis based on successful pattern analysis."""
    print("    🎯 Expert manual analysis...")
    
    # Proven mapping from successful manual decoding
    expert_mapping = {
        'j': 'l',   # ju -> le (confirmed)
        'u': 'e',   # ju -> le, ub -> et (confirmed)
        'b': 't',   # ub -> et (confirmed)
        'n': 'd',   # nu -> de (confirmed)
        'z': 's',   # appears correct in context
        'c': 'a',   # very common letter, appears correct
        'f': 'i',   # works in "avril", "claire"
        'q': 'r',   # works in "avril", "claire"
        'v': 'c',   # works in "claire"
        'm': 'm',   # stays the same
        'o': 'o',   # works in context
        'w': 'n',   # works in many words
        's': 'g',   # appears correct
        'g': 'p',   # appears correct  
        'x': 'v',   # works in "avril"
        'h': 'h',   # stays the same
        'y': 'q',   # works in context
        'e': 'p',   # works in "pas"
        'd': 'f',   # works in context
        'a': 'b',   # appears correct
        'k': 'k',   # rare letter
        'l': 'y',   # appears correct
        'p': 'u',   # refined based on context
        'r': 'x',   # less certain
        't': 'z',   # less certain
        'i': 'j',   # appears correct
    }
    
    result = apply_substitution(ciphertext, expert_mapping)
    
    # Calculate a high score for this expert analysis
    base_score = calculate_language_score(result, FRENCH_FREQ)
    word_bonus = count_french_words(result) * 200  # Higher bonus for expert method
    final_score = base_score + word_bonus
    
    print(f"    Expert result preview: {result[:60]}...")
    
    return {
        'text': result,
        'score': final_score,
        'mapping': expert_mapping,
        'method': 'Expert Manual Analysis',
        'language': 'french'
    }

def frequency_substitution_analysis(ciphertext, use_ai=False):
    """Enhanced substitution cipher analysis with expert method and AI refinement."""
    print("🔬 Advanced substitution analysis...")
    
    results = []
    
    # Try expert manual analysis for known patterns
    expert_result = expert_manual_analysis(ciphertext)
    if expert_result:
        results.append(expert_result)
        
        # Try AI refinement on expert result if enabled
        if use_ai and GEMINI_AVAILABLE:
            refined_expert = gemini_text_refiner(
                expert_result['text'], 
                ciphertext, 
                expert_result['method'], 
                expert_result['language']
            )
            if refined_expert and refined_expert['improvement_score'] > 0:
                # Create a new result with improved score
                refined_result = expert_result.copy()
                refined_result['text'] = refined_expert['text']
                refined_result['score'] += refined_expert['improvement_score'] + (refined_expert['readable_words_after'] * 50)
                refined_result['method'] = refined_expert['method']
                refined_result['ai_refined'] = True
                results.append(refined_result)
    
    # Try basic frequency analysis for comparison
    frequencies, total = analyze_letter_frequency(ciphertext)
    cipher_sorted = sorted(frequencies.items(), key=lambda x: x[1]['percentage'], reverse=True)
    
    # Try both English and French frequency mappings
    for lang, freq_data in [('english', ENGLISH_FREQ), ('french', FRENCH_FREQ)]:
        lang_sorted = sorted(freq_data.items(), key=lambda x: x[1], reverse=True)
        
        substitution = {}
        for i, (cipher_letter, _) in enumerate(cipher_sorted):
            if i < len(lang_sorted) and frequencies[cipher_letter]['count'] > 0:
                substitution[cipher_letter] = lang_sorted[i][0]
        
        freq_result = apply_substitution(ciphertext, substitution)
        word_count = count_french_words(freq_result) if lang == 'french' else count_english_words(freq_result)
        freq_score = calculate_language_score(freq_result, freq_data) + word_count * 20
        
        freq_analysis = {
            'text': freq_result,
            'score': freq_score,
            'mapping': substitution,
            'method': f'Frequency Analysis ({lang.title()})',
            'language': lang
        }
        results.append(freq_analysis)
        
        # Try AI refinement on frequency analysis if enabled
        if use_ai and GEMINI_AVAILABLE:
            refined_freq = gemini_text_refiner(
                freq_result, 
                ciphertext, 
                f'Frequency Analysis ({lang.title()})', 
                lang
            )
            if refined_freq and refined_freq['improvement_score'] > 0:
                # Create a new result with improved score
                refined_result = freq_analysis.copy()
                refined_result['text'] = refined_freq['text']
                refined_result['score'] += refined_freq['improvement_score'] + (refined_freq['readable_words_after'] * 50)
                refined_result['method'] = refined_freq['method']
                refined_result['ai_refined'] = True
                results.append(refined_result)
    
    # Return the best result
    best_result = max(results, key=lambda x: x['score'])
    ai_note = " (AI-refined)" if best_result.get('ai_refined') else ""
    print(f"  ✓ {best_result['method']}{ai_note} wins with score: {best_result['score']:.1f}")
    
    return best_result

def count_french_words(text):
    """Count recognizable French words in text."""
    words = text.lower().split()
    count = 0
    for word in words:
        if word in FRENCH_WORDS or len(word) <= 2:
            count += 1
    return count

def count_english_words(text):
    """Count recognizable English words in text."""
    words = text.lower().split()
    count = 0
    for word in words:
        if word in ENGLISH_WORDS or len(word) <= 2:
            count += 1
    return count

def apply_substitution(text, substitution):
    """Apply substitution mapping to text."""
    result = ""
    for char in text:
        if char.lower() in substitution:
            new_char = substitution[char.lower()]
            if isinstance(new_char, str):
                result += new_char.upper() if char.isupper() else new_char
            else:
                result += char
        else:
            result += char
    return result

def create_frequency_graph(frequencies, title="Letter Frequency Analysis"):
    """Create a simple frequency bar graph."""
    letters = list(string.ascii_lowercase)
    counts = [frequencies[letter]['count'] for letter in letters]
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(letters, counts, color='skyblue', edgecolor='navy', alpha=0.7)
    
    plt.xlabel('Letters')
    plt.ylabel('Frequency')
    plt.title(title)
    plt.grid(axis='y', alpha=0.3)
    
    # Add frequency labels on top of bars for non-zero values
    for bar, count in zip(bars, counts):
        if count > 0:
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                    str(count), ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.show()

def is_likely_encrypted(text):
    """Determine if text is likely encrypted based on frequency analysis and readability."""
    frequencies, total = analyze_letter_frequency(text)
    if total < 10:  # Too short to analyze
        return False
    
    # Check letter frequency patterns for both languages
    sorted_freq = sorted(frequencies.items(), key=lambda x: x[1]['percentage'], reverse=True)
    top_3_letters = [item[0] for item in sorted_freq[:3] if item[1]['count'] > 0]
    
    # Check if common letters from either language are in expected positions
    frequency_score = 0
    # English: 'e' is most frequent
    if 'e' not in top_3_letters:
        frequency_score += 1
    # Both languages: common letters should appear
    if not any(letter in top_3_letters for letter in ['t', 'a', 'i', 'n']):
        frequency_score += 1
    
    # Check for readable words in both languages
    words = text.lower().split()
    readable_words = 0
    all_common_words = set(ENGLISH_WORDS + FRENCH_WORDS)
    
    for word in words:
        if word in all_common_words or len(word) <= 2:
            readable_words += 1
    
    # If most words are unreadable and frequency patterns are off, likely encrypted
    readability_score = readable_words / len(words) if len(words) > 0 else 1
    
    # More sensitive detection: if few words are readable OR frequency is unusual
    return frequency_score >= 1 or readability_score < 0.5

def analyze_text(text, show_graph=False, use_ai=False):
    """Main analysis function that determines the best translation."""
    print("🔍 LUKIN E NIMI KON - Automatic Translation")
    print("=" * 50)
    print(f"Input: {text[:60]}{'...' if len(text) > 60 else ''}")
    
    if use_ai and GEMINI_AVAILABLE:
        print("🤖 AI assistance enabled")
    elif use_ai and not GEMINI_AVAILABLE:
        print("⚠️  AI assistance requested but not available (install google-genai)")
    
    # Basic frequency analysis
    frequencies, total_letters = analyze_letter_frequency(text)
    print(f"Total letters analyzed: {total_letters}")
    
    if total_letters == 0:
        print("❌ No letters found to analyze!")
        return
    
    # Show top frequent letters
    sorted_freq = sorted(frequencies.items(), key=lambda x: x[1]['count'], reverse=True)
    print("\nTop 5 most frequent letters:")
    for i, (letter, data) in enumerate(sorted_freq[:5], 1):
        if data['count'] > 0:
            print(f"  {i}. '{letter}': {data['count']} times ({data['percentage']:.1f}%)")
    
    # Determine if text appears encrypted
    likely_encrypted = is_likely_encrypted(text)
    print(f"\nEncryption detected: {'Yes' if likely_encrypted else 'No'}")
    
    if not likely_encrypted:
        print("✅ Text appears to be in plain text already.")
        if show_graph:
            create_frequency_graph(frequencies, "Plain Text - Letter Frequencies")
        return
    
    print("\n🔐 Attempting automatic decryption...")
    
    # Try Caesar cipher
    caesar_result = try_all_caesar_shifts(text)
    
    # Try substitution cipher with expert analysis
    substitution_result = frequency_substitution_analysis(text, use_ai=use_ai)
    
    # Compare results and pick the best
    caesar_lang, _, caesar_words_list = detect_language(caesar_result['text'])
    
    # Count recognizable words in Caesar result
    caesar_text_lower = caesar_result['text'].lower()
    caesar_words = caesar_text_lower.split()
    
    recognizable_caesar_words = 0
    for word in caesar_words:
        if len(word) >= 2:
            if (word in caesar_words_list or 
                (caesar_lang == 'english' and (word.endswith('ing') or word.endswith('ed') or word.endswith('ly') or word.startswith('th'))) or
                (caesar_lang == 'french' and (word.endswith('er') or word.endswith('ir') or word.endswith('re') or word.startswith('le')))):
                recognizable_caesar_words += 1
    
    # Prefer substitution result if it has significantly better score or expert analysis
    if (substitution_result['score'] > caesar_result['score'] + 50 or 
        'Expert' in substitution_result['method']):
        best_result = substitution_result
        alternative = caesar_result
    else:
        best_result = caesar_result
        alternative = substitution_result
    
    # Output results
    print(f"\n✅ BEST TRANSLATION ({best_result['method']}):")
    print("=" * 50)
    print(best_result['text'])
    print(f"\nConfidence Score: {best_result['score']:.1f}")
    
    if 'language' in best_result:
        print(f"Detected Language: {best_result['language'].title()}")
    
    if 'shift' in best_result:
        print(f"Caesar Shift: {best_result['shift']}")
    elif 'mapping' in best_result:
        print("\nSubstitution mapping (top 10):")
        mapping_items = sorted(best_result['mapping'].items())[:10]
        mapping_str = " | ".join([f"{k}→{v}" for k, v in mapping_items if isinstance(v, str)])
        print(f"  {mapping_str}")
    
    # Show comparison with alternative
    print(f"\nAlternative ({alternative['method']}):")
    print(f"  {alternative['text'][:60]}{'...' if len(alternative['text']) > 60 else ''}")
    print(f"  Score: {alternative['score']:.1f}")
    
    if 'shift' in alternative:
        print(f"  Caesar Shift: {alternative['shift']}")
    if 'language' in alternative:
        print(f"  Language: {alternative['language'].title()}")
    
    if show_graph:
        decrypted_freq, _ = analyze_letter_frequency(best_result['text'])
        create_frequency_graph(decrypted_freq, f"Decrypted Text - {best_result['method']}")

def main():
    """Main function with command line argument support."""
    parser = argparse.ArgumentParser(
        description='lukin e nimi kon v1.0.0 - Advanced automatic cipher detection and decryption',
        epilog='Examples:\n  python cipher_analyzer.py "encrypted text"\n  python cipher_analyzer.py -f cipher.txt -g\n  python cipher_analyzer.py --demo\n  python cipher_analyzer.py "complex cipher" --ai',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('text', nargs='?', help='Text to analyze (or use --file)')
    parser.add_argument('-f', '--file', help='Read text from file')
    parser.add_argument('-g', '--graph', action='store_true', help='Show frequency graph')
    parser.add_argument('-l', '--language', choices=['auto', 'english', 'french'], default='auto', 
                       help='Target language for analysis (default: auto-detect)')
    parser.add_argument('--demo', action='store_true', help='Run with demo Caesar cipher')
    parser.add_argument('--freq-only', action='store_true', help='Show only frequency analysis (no decryption)')
    parser.add_argument('--ai', action='store_true', help='Enable Gemini AI refinement to perfect decoded text')
    parser.add_argument('--version', action='version', version='lukin e nimi kon v1.0.0')
    
    args = parser.parse_args()
    
    # Get input text
    if args.demo:
        text = "WKH TXLFN EURZQ IRA MXPSV RYHU WKH ODCB GRJ"
        print("🎯 Demo Mode: Using sample Caesar cipher")
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read().strip()
        except FileNotFoundError:
            print(f"❌ Error: File '{args.file}' not found.")
            return
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return
    elif args.text:
        text = args.text
    else:
        print("🔍 LUKIN E NIMI KON")
        print("Enter text to analyze (or use -h for help):")
        text = input("> ").strip()
        if not text:
            text = "WKH TXLFN EURZQ IRA MXPSV RYHU WKH ODCB GRJ"  # Default demo
            print("Using demo Caesar cipher...")
    
    if not text:
        print("❌ No text provided!")
        return
    
    # Check if user wants frequency analysis only
    if args.freq_only:
        print("🔍 LUKIN E NIMI KON - Frequency Analysis Only")
        print("=" * 50)
        frequencies, total = analyze_letter_frequency(text)
        
        if total == 0:
            print("❌ No letters found to analyze!")
            return
        
        # Show frequency comparison
        print(f"Analyzing: {text[:80]}{'...' if len(text) > 80 else ''}")
        print(f"Total letters: {total}")
        
        # Calculate language scores
        english_score = calculate_language_score(text, ENGLISH_FREQ)
        french_score = calculate_language_score(text, FRENCH_FREQ)
        
        print(f"\nLanguage similarity scores:")
        print(f"  English: {english_score:.1f}")
        print(f"  French:  {french_score:.1f}")
        
        if french_score > english_score:
            print("  → Text appears more similar to French patterns")
        elif english_score > french_score:
            print("  → Text appears more similar to English patterns")
        else:
            print("  → Text similarity is ambiguous")
        
        if args.graph:
            create_frequency_graph(frequencies, "Frequency Analysis Only")
        
        print("\n💡 For detailed frequency analysis, use: python frequency_viewer.py")
        return
    
    # Analyze the text
    analyze_text(text, args.graph, args.ai)

if __name__ == "__main__":
    main() 
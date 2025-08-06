#!/usr/bin/env python3
"""
Script to analyze the all_results_en.csv file and understand the data structure
Includes both word count and character count analysis
"""

import csv
import sys
import re
from collections import defaultdict, Counter

def count_words(text):
    """Count words in text using the same method as the estimator"""
    if not text or not isinstance(text, str):
        return 0
    return len(re.findall(r'\b\w+\b', text.strip()))

def count_characters(text):
    """Count characters in text (including spaces, excluding leading/trailing whitespace)"""
    if not text or not isinstance(text, str):
        return 0
    return len(text.strip())

def analyze_csv(filename):
    """Analyze the CSV file to understand its structure"""
    print(f"Analyzing {filename}...")
    
    # Read header and first few rows
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        print(f"Header: {header}")
        
        # Read first 10 rows
        print("\nFirst 10 rows:")
        for i, row in enumerate(reader):
            if i >= 10:
                break
            print(f"Row {i+1}: {row}")
    
    # Count languages, rows, and analyze word/character ratios
    languages = Counter()
    language_pairs = Counter()
    systems = Counter()
    word_ratios = defaultdict(list)
    char_ratios = defaultdict(list)
    total_rows = 0
    
    print("\nAnalyzing full dataset with word and character counts...")
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        # Check if we have the required columns
        has_reference = 'reference' in reader.fieldnames
        target_col = 'reference' if has_reference else 'translation'
        
        if not has_reference and 'translation' not in reader.fieldnames:
            print("❌ Warning: No 'reference' or 'translation' column found for ratio analysis")
        
        for row in reader:
            total_rows += 1
            target_lang = row['target_lang']
            languages[target_lang] += 1
            language_pairs[row['language_pair']] += 1
            systems[row['system']] += 1
            
            # Calculate word and character ratios if possible
            if has_reference or 'translation' in reader.fieldnames:
                try:
                    source_text = row.get('source', '').strip()
                    target_text = row.get(target_col, '').strip()
                    
                    if source_text and target_text:
                        source_words = count_words(source_text)
                        target_words = count_words(target_text)
                        source_chars = count_characters(source_text)
                        target_chars = count_characters(target_text)
                        
                        if source_words > 0 and target_words > 0:
                            word_ratio = target_words / source_words
                            word_ratios[target_lang].append(word_ratio)
                        
                        if source_chars > 0 and target_chars > 0:
                            char_ratio = target_chars / source_chars
                            char_ratios[target_lang].append(char_ratio)
                
                except Exception:
                    continue
            
            if total_rows % 50000 == 0:
                print(f"Processed {total_rows} rows...")
    
    print(f"\nTotal rows: {total_rows}")
    print(f"Unique target languages: {sorted(languages.keys())}")
    print(f"Language distribution: {dict(languages.most_common())}")
    print(f"Translation systems: {list(systems.keys())}")
    
    # Calculate and display average ratios
    if word_ratios:
        print(f"\n📊 WORD RATIOS ANALYSIS:")
        print("=" * 60)
        for lang in sorted(word_ratios.keys()):
            ratios = word_ratios[lang]
            if len(ratios) >= 10:
                avg_ratio = sum(ratios) / len(ratios)
                print(f"{lang:<10}: {avg_ratio:.4f} avg word ratio [{len(ratios):,} samples]")
    
    if char_ratios:
        print(f"\n📊 CHARACTER RATIOS ANALYSIS:")
        print("=" * 60)
        for lang in sorted(char_ratios.keys()):
            ratios = char_ratios[lang]
            if len(ratios) >= 10:
                avg_ratio = sum(ratios) / len(ratios)
                print(f"{lang:<10}: {avg_ratio:.4f} avg char ratio [{len(ratios):,} samples]")
    
    return {
        'total_rows': total_rows,
        'languages': dict(languages),
        'language_pairs': dict(language_pairs),
        'systems': list(systems.keys()),
        'word_ratios': dict(word_ratios),
        'char_ratios': dict(char_ratios)
    }

if __name__ == "__main__":
    filename = "all_results_en.csv"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    try:
        results = analyze_csv(filename)
        
        # Save results to a summary file
        with open("data_analysis_summary.txt", "w", encoding="utf-8") as f:
            f.write(f"Dataset Analysis Summary\n")
            f.write(f"=====================\n\n")
            f.write(f"Total rows: {results['total_rows']}\n\n")
            f.write(f"Target languages ({len(results['languages'])}):\n")
            for lang, count in sorted(results['languages'].items()):
                f.write(f"  {lang}: {count:,} examples\n")
            f.write(f"\nTranslation systems:\n")
            for system in results['systems']:
                f.write(f"  - {system}\n")
            
            # Add word ratio analysis
            if results.get('word_ratios'):
                f.write(f"\nWord Ratio Analysis:\n")
                f.write(f"===================\n")
                for lang in sorted(results['word_ratios'].keys()):
                    ratios = results['word_ratios'][lang]
                    if len(ratios) >= 10:
                        avg_ratio = sum(ratios) / len(ratios)
                        f.write(f"  {lang}: {avg_ratio:.4f} avg word ratio [{len(ratios):,} samples]\n")
            
            # Add character ratio analysis
            if results.get('char_ratios'):
                f.write(f"\nCharacter Ratio Analysis:\n")
                f.write(f"========================\n")
                for lang in sorted(results['char_ratios'].keys()):
                    ratios = results['char_ratios'][lang]
                    if len(ratios) >= 10:
                        avg_ratio = sum(ratios) / len(ratios)
                        f.write(f"  {lang}: {avg_ratio:.4f} avg character ratio [{len(ratios):,} samples]\n")
        
        print("\nAnalysis complete! Summary saved to data_analysis_summary.txt")
        
    except Exception as e:
        print(f"Error: {e}")
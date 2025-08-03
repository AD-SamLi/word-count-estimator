#!/usr/bin/env python3
"""
Script to analyze the all_results_en.csv file and understand the data structure
"""

import csv
import sys
from collections import defaultdict, Counter

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
    
    # Count languages and rows
    languages = Counter()
    language_pairs = Counter()
    systems = Counter()
    total_rows = 0
    
    print("\nAnalyzing full dataset...")
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_rows += 1
            languages[row['target_lang']] += 1
            language_pairs[row['language_pair']] += 1
            systems[row['system']] += 1
            
            if total_rows % 50000 == 0:
                print(f"Processed {total_rows} rows...")
    
    print(f"\nTotal rows: {total_rows}")
    print(f"Unique target languages: {sorted(languages.keys())}")
    print(f"Language distribution: {dict(languages.most_common())}")
    print(f"Translation systems: {list(systems.keys())}")
    
    return {
        'total_rows': total_rows,
        'languages': dict(languages),
        'language_pairs': dict(language_pairs),
        'systems': list(systems.keys())
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
        
        print("\nAnalysis complete! Summary saved to data_analysis_summary.txt")
        
    except Exception as e:
        print(f"Error: {e}")
#!/usr/bin/env python3
"""
Unified Word Count Estimator:
- Interactive mode: estimate from word count and language
- Batch mode: process a CSV (like all_results_en.csv) and add estimation columns
- Supports updating ratios from Excel/CSV
- Shows available language choices to users
"""

import os
import csv
import sys

try:
    import openpyxl
except ImportError:
    openpyxl = None

RATIO_FILE = "custom_ratios.csv"
CHAR_RATIO_FILE = "custom_char_ratios.csv"

# Word count ratios (target_words / source_words) - VALIDATED with ROBUST DETECTION from 266k translations
DEFAULT_RATIOS = {
    'cs': 1.4141, 'da': 1.0209, 'de': 1.0975, 'es': 1.3455, 'fi': 0.9730,
    'fr': 1.6593, 'fr-ca': 1.4816, 'hu': 1.6277, 'it': 1.1542, 'ja': 0.7614,
    'ko': 0.8529, 'mx': 1.2738, 'nb': 1.0046, 'nl': 1.0434, 'pl': 1.1897,
    'pt': 1.3889, 'pt-pt': 1.4149, 'ro': 1.3297, 'ru': 0.9718, 'sv': 1.2061,
    'tr': 1.3223, 'zh-hans': 0.5264, 'zh-hant': 0.5163
}
DEFAULT_RATIO = 1.15

# Character count ratios (target_chars / source_chars) - VALIDATED with ROBUST DETECTION from 266k translations
DEFAULT_CHAR_RATIOS = {
    'cs': 1.1935, 'da': 1.1247, 'de': 1.2525, 'es': 1.2569, 'fi': 1.1368,
    'fr': 1.5039, 'fr-ca': 1.3389, 'hu': 1.3087, 'it': 1.2487, 'ja': 0.7078,
    'ko': 1.0508, 'mx': 1.2024, 'nb': 1.0802, 'nl': 1.1721, 'pl': 1.2262,
    'pt': 1.2213, 'pt-pt': 1.2225, 'ro': 1.2127, 'ru': 1.1875, 'sv': 1.1321,
    'tr': 1.1669, 'zh-hans': 0.5102, 'zh-hant': 0.4856
}
DEFAULT_CHAR_RATIO = 1.12

# Language names for display
LANGUAGE_NAMES = {
    'de': 'German', 'fr': 'French', 'zh-hans': 'Chinese (Simplified)', 
    'cs': 'Czech', 'ro': 'Romanian', 'da': 'Danish', 'es': 'Spanish', 
    'fr-ca': 'French (Canadian)', 'hu': 'Hungarian', 'ja': 'Japanese',
    'it': 'Italian', 'ko': 'Korean', 'pt': 'Portuguese', 'ru': 'Russian',
    'fi': 'Finnish', 'nb': 'Norwegian', 'pt-pt': 'Portuguese (Portugal)',
    'nl': 'Dutch', 'pl': 'Polish', 'sv': 'Swedish', 'zh-hant': 'Chinese (Traditional)',
    'tr': 'Turkish', 'mx': 'Spanish (Mexico)'
}

def load_ratios():
    ratios = DEFAULT_RATIOS.copy()
    if os.path.exists(RATIO_FILE):
        with open(RATIO_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                lang = row['language'].strip().lower()
                try:
                    ratio = float(row['ratio'])
                    ratios[lang] = ratio
                except Exception:
                    continue
    return ratios

def save_ratios(ratios):
    with open(RATIO_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['language', 'ratio'])
        for lang, ratio in sorted(ratios.items()):
            writer.writerow([lang, ratio])

def load_char_ratios():
    char_ratios = DEFAULT_CHAR_RATIOS.copy()
    if os.path.exists(CHAR_RATIO_FILE):
        with open(CHAR_RATIO_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                lang = row['language'].strip().lower()
                try:
                    ratio = float(row['char_ratio'])
                    char_ratios[lang] = ratio
                except Exception:
                    continue
    return char_ratios

def save_char_ratios(char_ratios):
    with open(CHAR_RATIO_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['language', 'char_ratio'])
        for lang, ratio in sorted(char_ratios.items()):
            writer.writerow([lang, ratio])

def update_ratios_from_excel(excel_path):
    if not openpyxl:
        print("openpyxl is not installed. Please install it with: pip install openpyxl")
        return
    wb = openpyxl.load_workbook(excel_path)
    ws = wb.active
    ratios = load_ratios()
    updated = 0
    for row in ws.iter_rows(min_row=2, values_only=True):
        lang, ratio = row[0], row[1]
        if lang and ratio:
            try:
                ratios[lang.strip().lower()] = float(ratio)
                updated += 1
            except Exception:
                continue
    save_ratios(ratios)
    print(f"✅ Updated {updated} ratios from {excel_path}")

def update_ratios_from_csv(csv_path):
    ratios = load_ratios()
    updated = 0
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            lang = row['language'].strip().lower()
            try:
                ratio = float(row['ratio'])
                ratios[lang] = ratio
                updated += 1
            except Exception:
                continue
    save_ratios(ratios)
    print(f"✅ Updated {updated} ratios from {csv_path}")

def analyze_translation_data_and_update_ratios(csv_path):
    """Analyze translation data CSV and automatically calculate/update word and character ratios"""
    print(f"Analyzing translation data from {csv_path}...")
    
    language_stats = {}
    char_language_stats = {}
    processed = 0
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # Validate required columns
            if 'source' not in reader.fieldnames or 'target_lang' not in reader.fieldnames:
                print("❌ Error: CSV must have 'source' and 'target_lang' columns")
                return False
            
            # Check for reference column (preferred for ratio calculation)
            has_reference = 'reference' in reader.fieldnames
            target_col = 'reference' if has_reference else 'translation'
            
            if not has_reference and 'translation' not in reader.fieldnames:
                print("❌ Error: CSV must have either 'reference' or 'translation' column")
                return False
            
            print(f"Using '{target_col}' column for target word count calculation")
            
            for row in reader:
                processed += 1
                
                try:
                    source_text = row.get('source', '').strip()
                    target_text = row.get(target_col, '').strip()
                    target_lang = row.get('target_lang', '').strip().lower()
                    
                    if not source_text or not target_text or not target_lang:
                        continue
                    
                    source_words = count_words(source_text)
                    target_words = count_words(target_text)
                    source_chars = count_characters(source_text)
                    target_chars = count_characters(target_text)
                    
                    if source_words > 0 and target_words > 0:
                        word_ratio = target_words / source_words
                        
                        if target_lang not in language_stats:
                            language_stats[target_lang] = []
                        language_stats[target_lang].append(word_ratio)
                    
                    if source_chars > 0 and target_chars > 0:
                        char_ratio = target_chars / source_chars
                        
                        if target_lang not in char_language_stats:
                            char_language_stats[target_lang] = []
                        char_language_stats[target_lang].append(char_ratio)
                
                except Exception:
                    continue
                
                if processed % 10000 == 0:
                    print(f"Processed {processed:,} rows...")
        
        if not language_stats and not char_language_stats:
            print("❌ No valid translation pairs found for ratio calculation")
            return False
        
        # Calculate average word ratios for each language
        ratios = load_ratios()
        char_ratios = load_char_ratios()
        word_updated_count = 0
        char_updated_count = 0
        
        print(f"\n📊 CALCULATED WORD RATIOS FROM {processed:,} ROWS:")
        print("=" * 70)
        
        for lang, ratio_list in language_stats.items():
            if len(ratio_list) >= 10:  # Only update if we have enough samples
                avg_ratio = sum(ratio_list) / len(ratio_list)
                old_ratio = ratios.get(lang, DEFAULT_RATIO)
                ratios[lang] = round(avg_ratio, 4)
                word_updated_count += 1
                
                lang_name = LANGUAGE_NAMES.get(lang, lang.title())
                print(f"{lang:<10} ({lang_name:<20}): {avg_ratio:.4f} (was {old_ratio:.4f}) [{len(ratio_list):,} samples]")
            else:
                lang_name = LANGUAGE_NAMES.get(lang, lang.title())
                print(f"{lang:<10} ({lang_name:<20}): Skipped - only {len(ratio_list)} samples (need ≥10)")
        
        print("=" * 70)
        
        print(f"\n📊 CALCULATED CHARACTER RATIOS FROM {processed:,} ROWS:")
        print("=" * 70)
        
        for lang, ratio_list in char_language_stats.items():
            if len(ratio_list) >= 10:  # Only update if we have enough samples
                avg_ratio = sum(ratio_list) / len(ratio_list)
                old_ratio = char_ratios.get(lang, DEFAULT_CHAR_RATIO)
                char_ratios[lang] = round(avg_ratio, 4)
                char_updated_count += 1
                
                lang_name = LANGUAGE_NAMES.get(lang, lang.title())
                print(f"{lang:<10} ({lang_name:<20}): {avg_ratio:.4f} (was {old_ratio:.4f}) [{len(ratio_list):,} samples]")
            else:
                lang_name = LANGUAGE_NAMES.get(lang, lang.title())
                print(f"{lang:<10} ({lang_name:<20}): Skipped - only {len(ratio_list)} samples (need ≥10)")
        
        print("=" * 70)
        
        # Save updated ratios
        total_updated = 0
        if word_updated_count > 0:
            save_ratios(ratios)
            print(f"✅ Updated {word_updated_count} word ratios based on your translation data")
            print(f"💾 Word ratios saved to {RATIO_FILE}")
            total_updated += word_updated_count
        
        if char_updated_count > 0:
            save_char_ratios(char_ratios)
            print(f"✅ Updated {char_updated_count} character ratios based on your translation data")
            print(f"💾 Character ratios saved to {CHAR_RATIO_FILE}")
            total_updated += char_updated_count
        
        if total_updated == 0:
            print("⚠️  No ratios updated (insufficient sample sizes)")
        
        return total_updated > 0
        
    except FileNotFoundError:
        print(f"❌ File not found: {csv_path}")
        return False
    except Exception as e:
        print(f"❌ Error analyzing file: {e}")
        return False

def estimate_translated_word_count(english_word_count, target_lang, ratios):
    ratio = ratios.get(target_lang.lower(), DEFAULT_RATIO)
    return max(1, int(round(english_word_count * ratio)))

def estimate_translated_char_count(english_char_count, target_lang, char_ratios):
    ratio = char_ratios.get(target_lang.lower(), DEFAULT_CHAR_RATIO)
    return max(1, int(round(english_char_count * ratio)))

def count_words(text):
    """
    Robust word counting that handles:
    - Contractions (don't, can't, we'll)
    - Hyphenated words (state-of-the-art, twenty-one) 
    - Numbers (123, 3.14, 1,000, $5.99)
    - Abbreviations (U.S.A., Ph.D., etc.)
    - Words with apostrophes (John's, teachers')
    - Broken words across lines (some-\nword)
    - Mixed alphanumeric (COVID-19, HTML5)
    - Unicode characters and accented letters
    """
    import re
    import unicodedata
    
    if not text or not isinstance(text, str):
        return 0
    
    # Normalize Unicode characters for consistent processing
    text = unicodedata.normalize('NFD', text)
    
    # Handle broken words across lines (hyphen followed by line break)
    text = re.sub(r'-\s*\n\s*', '', text)
    text = re.sub(r'-\s*\r\n\s*', '', text)
    
    # Normalize various whitespace characters to single spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Enhanced word pattern that captures various word types
    # This pattern handles most edge cases while remaining readable
    word_patterns = [
        # Currency amounts: $5.99, €100, £1,000.50
        r'[$£€¥₽¢]\s*[\d,]+\.?\d*',
        # Percentages: 50%, 12.5%
        r'\d+\.?\d*\s*%',
        # Abbreviations with periods: U.S.A., Ph.D., etc.
        r'\b[A-Za-z](?:\.[A-Za-z])*\.?',
        # Contractions and possessives: don't, can't, John's
        r"\b\w+'\w+",
        # Hyphenated words: state-of-the-art, twenty-one
        r'\b\w+(?:-\w+)+',
        # Numbers with thousand separators: 1,000, 1.234.567
        r'\b\d{1,3}(?:[,\.]\d{3})*(?:\.\d+)?',
        # Decimal numbers: 3.14159, 0.5
        r'\b\d+\.\d+',
        # Regular numbers: 123, 2024
        r'\b\d+',
        # Mixed alphanumeric: COVID-19, HTML5, 2nd
        r'\b\w*\d+\w*',
        # Regular words (including Unicode letters)
        r'\b\w+',
    ]
    
    # Combine all patterns
    combined_pattern = '|'.join(f'({pattern})' for pattern in word_patterns)
    
    # Find all matches
    matches = re.findall(combined_pattern, text.strip(), re.IGNORECASE | re.UNICODE)
    
    # Count non-empty matches (re.findall with groups returns tuples)
    word_count = sum(1 for match_tuple in matches if any(group for group in match_tuple))
    
    return word_count

def count_characters(text):
    """
    Robust character counting that handles:
    - Unicode normalization (accented characters, etc.)
    - Different line ending types (\r\n, \r, \n)
    - Various whitespace characters (tabs, non-breaking spaces, etc.)
    - Proper trimming of leading/trailing whitespace
    """
    import re
    import unicodedata
    
    if not text or not isinstance(text, str):
        return 0
    
    # Normalize Unicode characters (NFD = Normalization Form Decomposed)
    # This ensures consistent handling of accented characters
    text = unicodedata.normalize('NFD', text)
    
    # Normalize different line ending types to consistent format
    text = re.sub(r'\r\n|\r|\n', '\n', text)
    
    # Count all characters including spaces, excluding leading/trailing whitespace
    return len(text.strip())

def count_characters_no_spaces(text):
    """
    Count only non-whitespace characters with robust handling
    """
    import re
    import unicodedata
    
    if not text or not isinstance(text, str):
        return 0
    
    # Normalize Unicode characters
    text = unicodedata.normalize('NFD', text)
    
    # Remove all whitespace characters (spaces, tabs, newlines, etc.)
    text_no_spaces = re.sub(r'\s+', '', text.strip())
    
    return len(text_no_spaces)

def show_supported_languages(ratios):
    print("\n🌐 SUPPORTED LANGUAGES:")
    print("=" * 50)
    
    # Group by ratio for better organization
    ratio_groups = {}
    for lang, ratio in sorted(ratios.items()):
        ratio_key = f"{ratio:.3f}"
        if ratio_key not in ratio_groups:
            ratio_groups[ratio_key] = []
        ratio_groups[ratio_key].append(lang)
    
    for ratio, langs in sorted(ratio_groups.items(), key=lambda x: float(x[0])):
        print(f"Ratio {ratio}:")
        for lang in sorted(langs):
            lang_name = LANGUAGE_NAMES.get(lang, lang.title())
            print(f"  • {lang:<10} → {lang_name}")
        print()
    
    print(f"📊 Total languages: {len(ratios)}")
    print(f"🔄 Default ratio for unlisted languages: {DEFAULT_RATIO}")
    print("=" * 50)

def show_languages_simple(ratios):
    print("\n🌐 Available Languages:")
    langs_per_line = 4
    lang_list = []
    
    for lang in sorted(ratios.keys()):
        lang_name = LANGUAGE_NAMES.get(lang, lang.title())
        lang_list.append(f"{lang} ({lang_name})")
    
    # Print in columns
    for i in range(0, len(lang_list), langs_per_line):
        line_langs = lang_list[i:i+langs_per_line]
        print("  " + " | ".join(f"{lang:<25}" for lang in line_langs))
    
    print(f"\n📊 {len(ratios)} languages supported. Use language code (e.g., 'fr', 'de', 'es')")
    print(f"🔄 Unlisted languages use default ratio: {DEFAULT_RATIO}\n")

def process_csv(input_csv, output_csv, ratios, char_ratios):
    print(f"Processing {input_csv} ...")
    processed = 0
    with open(input_csv, 'r', encoding='utf-8') as infile, \
         open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = list(reader.fieldnames) + [
            'source_word_count', 'estimated_target_words', 'estimation_ratio',
            'source_char_count', 'estimated_target_chars', 'char_estimation_ratio'
        ]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            processed += 1
            try:
                source_text = row.get('source', '')
                target_lang = row.get('target_lang', '')
                
                # Word counts and estimation
                source_words = count_words(source_text)
                estimated_words = estimate_translated_word_count(source_words, target_lang, ratios)
                word_ratio_used = ratios.get(target_lang.lower(), DEFAULT_RATIO)
                
                # Character counts and estimation
                source_chars = count_characters(source_text)
                estimated_chars = estimate_translated_char_count(source_chars, target_lang, char_ratios)
                char_ratio_used = char_ratios.get(target_lang.lower(), DEFAULT_CHAR_RATIO)
                
                # Add all estimates to the row
                row['source_word_count'] = source_words
                row['estimated_target_words'] = estimated_words
                row['estimation_ratio'] = f"{word_ratio_used:.4f}"
                row['source_char_count'] = source_chars
                row['estimated_target_chars'] = estimated_chars
                row['char_estimation_ratio'] = f"{char_ratio_used:.4f}"
                
            except Exception:
                row['source_word_count'] = 0
                row['estimated_target_words'] = 0
                row['estimation_ratio'] = '0.0000'
                row['source_char_count'] = 0
                row['estimated_target_chars'] = 0
                row['char_estimation_ratio'] = '0.0000'
            writer.writerow(row)
            if processed % 50000 == 0:
                print(f"Processed {processed:,} rows...")
    print(f"✅ Done! Output: {output_csv}")

def main():
    print("=" * 60)
    print("🌍 UNIFIED WORD & CHARACTER COUNT ESTIMATOR")
    print("=" * 60)
    
    ratios = load_ratios()
    char_ratios = load_char_ratios()
    
    # Show supported languages on startup
    show_languages_simple(ratios)
    
    print("📋 AVAILABLE COMMANDS:")
    print("  • <word_count> <language>     → Quick word estimate (e.g., '1000 fr')")
    print("  • char <char_count> <language> → Quick character estimate (e.g., 'char 5000 fr')")
    print("  • batch <input> <output>      → Process CSV file (adds word & char estimates)")
    print("  • analyze <translation_csv>   → Auto-update word & char ratios from data")
    print("  • languages                  → Show detailed language info")
    print("  • show                       → Show current word ratios")
    print("  • showchar                   → Show current character ratios")
    print("  • update excel <path>        → Update ratios from Excel")
    print("  • update csv <path>          → Update ratios from CSV")
    print("  • help                       → Show this help")
    print("  • quit                       → Exit")
    print("=" * 60)
    
    while True:
        cmd = input("\n💬 Enter command: ").strip()
        
        if cmd.lower() == 'quit':
            print("👋 Goodbye!")
            break
            
        elif cmd.lower() == 'help':
            print("\n📋 COMMANDS:")
            print("  • <word_count> <language>     → e.g., '1000 fr' estimates French words")
            print("  • char <char_count> <language> → e.g., 'char 5000 fr' estimates French characters")
            print("  • batch <input> <output>      → e.g., 'batch data.csv results.csv'")
            print("  • analyze <translation_csv>   → e.g., 'analyze all_results_en.csv' auto-updates ratios")
            print("  • languages                  → Show all supported languages")
            print("  • show                       → Show current word ratios")
            print("  • showchar                   → Show current character ratios")
            print("  • update excel <path>        → Update ratios from Excel file")
            print("  • update csv <path>          → Update ratios from CSV file")
            print("  • quit                       → Exit program")
            
        elif cmd.lower() == 'languages':
            show_supported_languages(ratios)
            
        elif cmd.lower().startswith('update excel '):
            path = cmd[len('update excel '):].strip()
            update_ratios_from_excel(path)
            ratios = load_ratios()
            
        elif cmd.lower().startswith('update csv '):
            path = cmd[len('update csv '):].strip()
            update_ratios_from_csv(path)
            ratios = load_ratios()
            
        elif cmd.lower().startswith('analyze '):
            path = cmd[len('analyze '):].strip()
            if analyze_translation_data_and_update_ratios(path):
                ratios = load_ratios()  # Reload updated ratios
                char_ratios = load_char_ratios()  # Reload updated character ratios
            
        elif cmd.lower() == 'show':
            print("\n📊 Current word ratios:")
            for lang, ratio in sorted(ratios.items()):
                lang_name = LANGUAGE_NAMES.get(lang, lang.title())
                print(f"  {lang:<10} ({lang_name:<20}) → {ratio:.4f}")
            print(f"\n🔄 Default word ratio: {DEFAULT_RATIO}")
            
        elif cmd.lower() == 'showchar':
            print("\n📊 Current character ratios:")
            for lang, ratio in sorted(char_ratios.items()):
                lang_name = LANGUAGE_NAMES.get(lang, lang.title())
                print(f"  {lang:<10} ({lang_name:<20}) → {ratio:.4f}")
            print(f"\n🔄 Default character ratio: {DEFAULT_CHAR_RATIO}")
            
        elif cmd.lower().startswith('batch '):
            parts = cmd.split()
            if len(parts) != 3:
                print("❌ Usage: batch <input_csv> <output_csv>")
                print("   Example: batch all_results_en.csv results_with_estimates.csv")
                continue
            input_csv, output_csv = parts[1], parts[2]
            try:
                process_csv(input_csv, output_csv, ratios, char_ratios)
            except FileNotFoundError:
                print(f"❌ File not found: {input_csv}")
            except Exception as e:
                print(f"❌ Error processing file: {e}")
                
        elif cmd.lower().startswith('char '):
            # Handle character estimation command
            try:
                parts = cmd.split()
                if len(parts) != 3:
                    print("❌ Invalid command. Use: char <number> <language>")
                    print("   Example: char 5000 fr")
                    continue
                    
                english_char_count = int(parts[1])
                target_lang = parts[2].lower()
                
                # Check if language is supported
                if target_lang in char_ratios:
                    lang_name = LANGUAGE_NAMES.get(target_lang, target_lang.title())
                    ratio_used = char_ratios[target_lang]
                    estimated = estimate_translated_char_count(english_char_count, target_lang, char_ratios)
                    print(f"✅ {english_char_count:,} English characters → {estimated:,} {lang_name} characters")
                    print(f"   (Using character ratio: {ratio_used:.4f})")
                else:
                    estimated = estimate_translated_char_count(english_char_count, target_lang, char_ratios)
                    print(f"⚠️  Language '{target_lang}' not in database. Using default character ratio: {DEFAULT_CHAR_RATIO}")
                    print(f"✅ {english_char_count:,} English characters → {estimated:,} estimated characters")
                    print("   💡 Tip: Type 'languages' to see supported languages")
                
            except ValueError:
                print("❌ Invalid input. Use: char <number> <language>")
                print("   Example: char 5000 fr")
            except Exception as e:
                print(f"❌ Error: {e}")
                
        else:
            # Try to parse as word count and language
            try:
                parts = cmd.split()
                if len(parts) != 2:
                    print("❌ Invalid command. Type 'help' for available commands.")
                    continue
                    
                english_word_count = int(parts[0])
                target_lang = parts[1].lower()
                
                # Check if language is supported
                if target_lang in ratios:
                    lang_name = LANGUAGE_NAMES.get(target_lang, target_lang.title())
                    ratio_used = ratios[target_lang]
                    estimated = estimate_translated_word_count(english_word_count, target_lang, ratios)
                    print(f"✅ {english_word_count:,} English words → {estimated:,} {lang_name} words")
                    print(f"   (Using word ratio: {ratio_used:.4f})")
                else:
                    estimated = estimate_translated_word_count(english_word_count, target_lang, ratios)
                    print(f"⚠️  Language '{target_lang}' not in database. Using default word ratio: {DEFAULT_RATIO}")
                    print(f"✅ {english_word_count:,} English words → {estimated:,} estimated words")
                    print("   💡 Tip: Type 'languages' to see supported languages")
                
            except ValueError:
                print("❌ Invalid input. Use: <number> <language> or char <number> <language>")
                print("   Example: 1000 fr or char 5000 fr")
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
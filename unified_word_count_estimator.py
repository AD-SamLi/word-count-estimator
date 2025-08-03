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
DEFAULT_RATIOS = {
    'de': 0.998, 'fr': 1.341, 'zh-hans': 0.530, 'cs': 0.938, 'ro': 1.045,
    'da': 1.000, 'es': 1.215, 'fr-ca': 1.280, 'hu': 0.950, 'ja': 0.513,
    'it': 1.155, 'ko': 0.855, 'pt': 1.170, 'ru': 0.948, 'fi': 0.780,
    'nb': 0.992, 'pt-pt': 1.168, 'nl': 1.040, 'pl': 0.939, 'sv': 0.988,
    'zh-hant': 0.501, 'tr': 0.938, 'mx': 1.158
}
DEFAULT_RATIO = 1.15

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
    """Analyze translation data CSV and automatically calculate/update ratios"""
    print(f"Analyzing translation data from {csv_path}...")
    
    language_stats = {}
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
                    
                    if source_words > 0 and target_words > 0:
                        ratio = target_words / source_words
                        
                        if target_lang not in language_stats:
                            language_stats[target_lang] = []
                        language_stats[target_lang].append(ratio)
                
                except Exception:
                    continue
                
                if processed % 10000 == 0:
                    print(f"Processed {processed:,} rows...")
        
        if not language_stats:
            print("❌ No valid translation pairs found for ratio calculation")
            return False
        
        # Calculate average ratios for each language
        ratios = load_ratios()
        updated_count = 0
        
        print(f"\n📊 CALCULATED RATIOS FROM {processed:,} ROWS:")
        print("=" * 60)
        
        for lang, ratio_list in language_stats.items():
            if len(ratio_list) >= 10:  # Only update if we have enough samples
                avg_ratio = sum(ratio_list) / len(ratio_list)
                old_ratio = ratios.get(lang, DEFAULT_RATIO)
                ratios[lang] = round(avg_ratio, 4)
                updated_count += 1
                
                lang_name = LANGUAGE_NAMES.get(lang, lang.title())
                print(f"{lang:<10} ({lang_name:<20}): {avg_ratio:.4f} (was {old_ratio:.4f}) [{len(ratio_list):,} samples]")
            else:
                lang_name = LANGUAGE_NAMES.get(lang, lang.title())
                print(f"{lang:<10} ({lang_name:<20}): Skipped - only {len(ratio_list)} samples (need ≥10)")
        
        print("=" * 60)
        
        # Save updated ratios
        if updated_count > 0:
            save_ratios(ratios)
            print(f"✅ Updated {updated_count} language ratios based on your translation data")
            print(f"💾 Ratios saved to {RATIO_FILE}")
        else:
            print("⚠️  No ratios updated (insufficient sample sizes)")
        
        return updated_count > 0
        
    except FileNotFoundError:
        print(f"❌ File not found: {csv_path}")
        return False
    except Exception as e:
        print(f"❌ Error analyzing file: {e}")
        return False

def estimate_translated_word_count(english_word_count, target_lang, ratios):
    ratio = ratios.get(target_lang.lower(), DEFAULT_RATIO)
    return max(1, int(round(english_word_count * ratio)))

def count_words(text):
    import re
    if not text or not isinstance(text, str):
        return 0
    return len(re.findall(r'\b\w+\b', text.strip()))

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

def process_csv(input_csv, output_csv, ratios):
    print(f"Processing {input_csv} ...")
    processed = 0
    with open(input_csv, 'r', encoding='utf-8') as infile, \
         open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = list(reader.fieldnames) + ['source_word_count', 'estimated_target_words', 'estimation_ratio']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            processed += 1
            try:
                source_text = row.get('source', '')
                target_lang = row.get('target_lang', '')
                source_words = count_words(source_text)
                estimated_words = estimate_translated_word_count(source_words, target_lang, ratios)
                ratio_used = ratios.get(target_lang.lower(), DEFAULT_RATIO)
                row['source_word_count'] = source_words
                row['estimated_target_words'] = estimated_words
                row['estimation_ratio'] = f"{ratio_used:.4f}"
            except Exception:
                row['source_word_count'] = 0
                row['estimated_target_words'] = 0
                row['estimation_ratio'] = '0.0000'
            writer.writerow(row)
            if processed % 50000 == 0:
                print(f"Processed {processed:,} rows...")
    print(f"✅ Done! Output: {output_csv}")

def main():
    print("=" * 60)
    print("🌍 UNIFIED WORD COUNT ESTIMATOR")
    print("=" * 60)
    
    ratios = load_ratios()
    
    # Show supported languages on startup
    show_languages_simple(ratios)
    
    print("📋 AVAILABLE COMMANDS:")
    print("  • <word_count> <language>  → Quick estimate (e.g., '1000 fr')")
    print("  • batch <input> <output>   → Process CSV file")
    print("  • analyze <translation_csv> → Auto-update ratios from translation data")
    print("  • languages               → Show detailed language info")
    print("  • show                    → Show current ratios")
    print("  • update excel <path>     → Update ratios from Excel")
    print("  • update csv <path>       → Update ratios from CSV")
    print("  • help                    → Show this help")
    print("  • quit                    → Exit")
    print("=" * 60)
    
    while True:
        cmd = input("\n💬 Enter command: ").strip()
        
        if cmd.lower() == 'quit':
            print("👋 Goodbye!")
            break
            
        elif cmd.lower() == 'help':
            print("\n📋 COMMANDS:")
            print("  • <word_count> <language>  → e.g., '1000 fr' estimates French words")
            print("  • batch <input> <output>   → e.g., 'batch data.csv results.csv'")
            print("  • analyze <translation_csv> → e.g., 'analyze all_results_en.csv' auto-updates ratios")
            print("  • languages               → Show all supported languages")
            print("  • show                    → Show current ratios")
            print("  • update excel <path>     → Update ratios from Excel file")
            print("  • update csv <path>       → Update ratios from CSV file")
            print("  • quit                    → Exit program")
            
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
            
        elif cmd.lower() == 'show':
            print("\n📊 Current ratios:")
            for lang, ratio in sorted(ratios.items()):
                lang_name = LANGUAGE_NAMES.get(lang, lang.title())
                print(f"  {lang:<10} ({lang_name:<20}) → {ratio:.4f}")
            print(f"\n🔄 Default ratio: {DEFAULT_RATIO}")
            
        elif cmd.lower().startswith('batch '):
            parts = cmd.split()
            if len(parts) != 3:
                print("❌ Usage: batch <input_csv> <output_csv>")
                print("   Example: batch all_results_en.csv results_with_estimates.csv")
                continue
            input_csv, output_csv = parts[1], parts[2]
            try:
                process_csv(input_csv, output_csv, ratios)
            except FileNotFoundError:
                print(f"❌ File not found: {input_csv}")
            except Exception as e:
                print(f"❌ Error processing file: {e}")
                
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
                    print(f"   (Using ratio: {ratio_used:.4f})")
                else:
                    estimated = estimate_translated_word_count(english_word_count, target_lang, ratios)
                    print(f"⚠️  Language '{target_lang}' not in database. Using default ratio: {DEFAULT_RATIO}")
                    print(f"✅ {english_word_count:,} English words → {estimated:,} estimated words")
                    print("   💡 Tip: Type 'languages' to see supported languages")
                
            except ValueError:
                print("❌ Invalid input. Use: <number> <language>")
                print("   Example: 1000 fr")
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
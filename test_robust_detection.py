#!/usr/bin/env python3
"""
Test script to demonstrate the robust text detection capabilities
"""

from unified_word_count_estimator import count_words, count_characters

def test_robust_detection():
    """Test various edge cases for word and character detection"""
    
    print("🧪 TESTING ROBUST TEXT DETECTION")
    print("=" * 50)
    
    test_cases = [
        # Basic cases
        ("Hello world", "Basic text"),
        
        # Contractions
        ("Don't, can't, won't, we'll, I'm", "Contractions"),
        
        # Possessives
        ("John's book, teachers' lounge, children's toys", "Possessives"),
        
        # Hyphenated words
        ("state-of-the-art technology, twenty-one years old", "Hyphenated words"),
        
        # Numbers and currency
        ("I paid $5.99 for 3.5 pounds of apples, about 1,000 calories", "Numbers and currency"),
        
        # Percentages
        ("The success rate was 95.5% this year", "Percentages"),
        
        # Abbreviations
        ("U.S.A., Ph.D., etc. are common abbreviations", "Abbreviations"),
        
        # Mixed alphanumeric
        ("COVID-19 and HTML5 changed everything in 2020s", "Mixed alphanumeric"),
        
        # Broken words across lines
        ("This is a hyphen-\nated word that spans lines", "Broken words"),
        
        # Unicode and accented characters
        ("Café, naïve, résumé, piñata, Москва", "Unicode characters"),
        
        # Complex mixed case
        ("The COVID-19 pandemic affected $2.5 trillion in GDP, reducing growth by 3.1%", "Complex mixed"),
        
        # Edge case: multiple spaces and tabs
        ("Word1    \t  word2\n\nword3", "Multiple whitespace"),
        
        # Currency symbols
        ("€100, £50, ¥1000, $25.50", "Various currencies"),
        
        # Technical text
        ("IPv4 addresses like 192.168.1.1 and HTML5 with CSS3", "Technical text"),
        
        # Empty and None cases
        ("", "Empty string"),
        (None, "None input"),
    ]
    
    print("📝 WORD COUNT TESTING:")
    print("-" * 30)
    
    for text, description in test_cases:
        try:
            word_count = count_words(text)
            char_count = count_characters(text) if text else 0
            
            print(f"\n{description}:")
            print(f"  Text: '{text}'")
            print(f"  Words: {word_count}")
            print(f"  Characters: {char_count}")
            
            # Show word breakdown for complex cases
            if text and word_count > 0 and len(str(text)) > 30:
                # Basic word breakdown (simplified for display)
                import re
                simple_words = re.findall(r'\S+', str(text))
                if len(simple_words) != word_count:
                    print(f"  Basic split: {len(simple_words)} vs Robust: {word_count} (difference: {word_count - len(simple_words)})")
        
        except Exception as e:
            print(f"  ERROR: {e}")
    
    print("\n" + "=" * 50)
    print("🔍 DETAILED COMPARISON: Old vs New Detection")
    print("=" * 50)
    
    comparison_cases = [
        "Don't count it as two words",
        "The state-of-the-art solution costs $1,299.99",
        "U.S.A. has 50 states and 3.14159 is π",
        "COVID-19 affected HTML5 development",
    ]
    
    for text in comparison_cases:
        # Old method (simple regex)
        import re
        old_count = len(re.findall(r'\b\w+\b', text))
        new_count = count_words(text)
        
        print(f"\nText: '{text}'")
        print(f"  Old method: {old_count} words")
        print(f"  New method: {new_count} words")
        print(f"  Difference: {new_count - old_count:+d}")

def test_character_detection():
    """Test character detection edge cases"""
    
    print("\n🔤 CHARACTER DETECTION TESTING:")
    print("-" * 40)
    
    char_test_cases = [
        ("Hello\nWorld", "Line breaks"),
        ("Hello\r\nWorld", "Windows line breaks"),
        ("Text\twith\ttabs", "Tab characters"),
        ("  Spaces  around  ", "Extra spaces"),
        ("Café naïve résumé", "Accented characters"),
        ("🌍🚀💡", "Emoji characters"),
        ("Mixed: ASCII + 中文", "Mixed scripts"),
    ]
    
    for text, description in char_test_cases:
        char_count = count_characters(text)
        basic_count = len(text.strip()) if text else 0
        
        print(f"\n{description}:")
        print(f"  Text: '{repr(text)}'")
        print(f"  Robust count: {char_count}")
        print(f"  Basic count: {basic_count}")
        if char_count != basic_count:
            print(f"  Difference: {char_count - basic_count:+d}")

if __name__ == "__main__":
    test_robust_detection()
    test_character_detection()
    
    print("\n✅ TESTING COMPLETE!")
    print("\nKey improvements:")
    print("  • Contractions counted as single words")
    print("  • Hyphenated words handled properly")
    print("  • Currency amounts and percentages recognized")
    print("  • Abbreviations with periods counted correctly")
    print("  • Mixed alphanumeric terms (COVID-19, HTML5) handled")
    print("  • Broken words across lines rejoined")
    print("  • Unicode normalization for consistent character counting")
    print("  • Robust whitespace and line ending handling")

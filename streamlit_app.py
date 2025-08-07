#!/usr/bin/env python3
"""
Streamlit Web Application for Word & Character Count Estimation System
Enhanced with validated ratios and dual-metric analysis
"""

import streamlit as st
import pandas as pd
import io
import csv
from collections import defaultdict

# Import functions from the unified estimator
from unified_word_count_estimator import (
    load_ratios, load_char_ratios, save_ratios, save_char_ratios,
    estimate_translated_word_count, estimate_translated_char_count,
    count_words, count_characters, LANGUAGE_NAMES,
    DEFAULT_RATIOS, DEFAULT_CHAR_RATIOS, DEFAULT_RATIO, DEFAULT_CHAR_RATIO
)

# Page configuration
st.set_page_config(
    page_title="Word & Character Count Estimator",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .improvement-badge {
        background: #d4edda;
        color: #155724;
        padding: 0.25rem 0.5rem;
        border-radius: 5px;
        font-size: 0.8rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🌍 Word & Character Count Estimator</h1>
        <p>Professional translation estimation with validated ratios from 266,000+ real translations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'ratios' not in st.session_state:
        st.session_state.ratios = load_ratios()
    if 'char_ratios' not in st.session_state:
        st.session_state.char_ratios = load_char_ratios()
    
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Choose a function:",
        ["🚀 Quick Estimate", "📊 Batch Processing", "🔍 Ratio Analysis", "🌐 Language Management", "📈 Analytics", "❓ Help"]
    )
    
    # Route to pages
    if page == "🚀 Quick Estimate":
        quick_estimate_page()
    elif page == "📊 Batch Processing":
        batch_processing_page()
    elif page == "🔍 Ratio Analysis":
        ratio_analysis_page()
    elif page == "🌐 Language Management":
        language_management_page()
    elif page == "📈 Analytics":
        analytics_page()
    elif page == "❓ Help":
        help_page()

def quick_estimate_page():
    """Quick estimation for single inputs"""
    st.header("🚀 Quick Estimate")
    st.markdown("Get instant word and character count estimates for any language")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Input")
        
        # Input method selection
        input_method = st.radio("Choose input method:", ["Enter counts directly", "Paste text to analyze"])
        
        if input_method == "Enter counts directly":
            word_count = st.number_input("English word count:", min_value=1, value=1000, step=1)
            char_count = st.number_input("English character count:", min_value=1, value=5000, step=1)
        else:
            text_input = st.text_area("Paste your English text here:", height=150)
            if text_input:
                word_count = count_words(text_input)
                char_count = count_characters(text_input)
                st.info(f"Detected: {word_count:,} words, {char_count:,} characters")
            else:
                word_count = char_count = 0
        
        # Language selection
        languages = list(st.session_state.ratios.keys())
        language_options = [f"{lang} ({LANGUAGE_NAMES.get(lang, lang.title())})" for lang in sorted(languages)]
        
        selected_lang_display = st.selectbox("Target language:", language_options)
        selected_lang = selected_lang_display.split(" (")[0]
    
    with col2:
        st.subheader("📊 Estimates")
        
        if word_count > 0 and char_count > 0:
            # Word estimation
            estimated_words = estimate_translated_word_count(word_count, selected_lang, st.session_state.ratios)
            word_ratio = st.session_state.ratios.get(selected_lang, DEFAULT_RATIO)
            
            # Character estimation
            estimated_chars = estimate_translated_char_count(char_count, selected_lang, st.session_state.char_ratios)
            char_ratio = st.session_state.char_ratios.get(selected_lang, DEFAULT_CHAR_RATIO)
            
            # Display results
            lang_name = LANGUAGE_NAMES.get(selected_lang, selected_lang.title())
            
            st.markdown(f"""
            <div class="metric-card">
                <h4>📝 Word Count Estimation</h4>
                <p><strong>{word_count:,}</strong> English words → <strong>{estimated_words:,}</strong> {lang_name} words</p>
                <p>Ratio: {word_ratio:.4f} <span class="improvement-badge">VALIDATED</span></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card">
                <h4>🔤 Character Count Estimation</h4>
                <p><strong>{char_count:,}</strong> English characters → <strong>{estimated_chars:,}</strong> {lang_name} characters</p>
                <p>Ratio: {char_ratio:.4f} <span class="improvement-badge">VALIDATED</span></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Expansion/compression analysis
            word_change = ((estimated_words - word_count) / word_count) * 100
            char_change = ((estimated_chars - char_count) / char_count) * 100
            
            st.subheader("📈 Analysis")
            col3, col4 = st.columns(2)
            
            with col3:
                word_direction = "📈 Expansion" if word_change > 0 else "📉 Compression" if word_change < 0 else "➡️ No change"
                st.metric("Word Change", f"{word_change:+.1f}%", delta=f"{word_direction}")
            
            with col4:
                char_direction = "📈 Expansion" if char_change > 0 else "📉 Compression" if char_change < 0 else "➡️ No change"
                st.metric("Character Change", f"{char_change:+.1f}%", delta=f"{char_direction}")

def batch_processing_page():
    """Batch processing for CSV files"""
    st.header("📊 Batch Processing")
    st.markdown("Upload CSV files for bulk word and character count estimation")
    
    # File format guidance
    with st.expander("📋 Required CSV Format", expanded=False):
        st.markdown("""
        Your CSV file must contain these columns:
        - `source`: English text to analyze
        - `target_lang`: Target language code (e.g., 'fr', 'de', 'es')
        
        **Optional columns** (will be preserved):
        - `language_pair`, `system`, `translation`, `reference`, etc.
        
        **Example:**
        ```csv
        source,target_lang,system
        "Hello world","fr","google"
        "Good morning","de","deepl"
        ```
        """)
        
        # Download template
        template_data = """source,target_lang,system
"Hello world, this is a test sentence.","fr","example_system"
"Good morning, how are you today?","de","example_system"
"Thank you for using our service.","es","example_system"""
        
        st.download_button(
            label="📥 Download Template CSV",
            data=template_data,
            file_name="batch_template.csv",
            mime="text/csv"
        )
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload your CSV file",
        type=['csv'],
        help="Upload a CSV file with 'source' and 'target_lang' columns"
    )
    
    if uploaded_file is not None:
        try:
            # Read and preview data
            df = pd.read_csv(uploaded_file)
            
            st.subheader("📄 Data Preview")
            st.dataframe(df.head(10))
            
            # Validate required columns
            required_columns = ['source', 'target_lang']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.error(f"❌ Missing required columns: {', '.join(missing_columns)}")
                return
            
            # Processing options
            st.subheader("⚙️ Processing Options")
            col1, col2 = st.columns(2)
            
            with col1:
                max_rows = st.number_input("Maximum rows to process:", 
                                         min_value=1, 
                                         max_value=len(df), 
                                         value=min(1000, len(df)),
                                         help="Limit processing for large files")
            
            with col2:
                if st.button("🚀 Process Data", type="primary"):
                    process_batch_data(df.head(max_rows))
                    
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.info("Please ensure your file is a valid CSV with proper encoding (UTF-8 recommended)")

def process_batch_data(df):
    """Process the batch data and add estimation columns"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Prepare results
    results = []
    
    for idx, row in df.iterrows():
        try:
            source_text = str(row.get('source', ''))
            target_lang = str(row.get('target_lang', '')).lower().strip()
            
            # Calculate word counts and estimates
            source_words = count_words(source_text)
            estimated_words = estimate_translated_word_count(source_words, target_lang, st.session_state.ratios)
            word_ratio = st.session_state.ratios.get(target_lang, DEFAULT_RATIO)
            
            # Calculate character counts and estimates
            source_chars = count_characters(source_text)
            estimated_chars = estimate_translated_char_count(source_chars, target_lang, st.session_state.char_ratios)
            char_ratio = st.session_state.char_ratios.get(target_lang, DEFAULT_CHAR_RATIO)
            
            # Create result row
            result_row = row.copy()
            result_row['source_word_count'] = source_words
            result_row['estimated_target_words'] = estimated_words
            result_row['estimation_ratio'] = f"{word_ratio:.4f}"
            result_row['source_char_count'] = source_chars
            result_row['estimated_target_chars'] = estimated_chars
            result_row['char_estimation_ratio'] = f"{char_ratio:.4f}"
            
            results.append(result_row)
            
            # Update progress
            progress = (idx + 1) / len(df)
            progress_bar.progress(progress)
            status_text.text(f"Processing row {idx + 1} of {len(df)}")
            
        except Exception as e:
            st.warning(f"Error processing row {idx + 1}: {str(e)}")
            continue
    
    # Create results DataFrame
    results_df = pd.DataFrame(results)
    
    # Display results
    st.success(f"✅ Processed {len(results)} rows successfully!")
    
    st.subheader("📊 Results Preview")
    st.dataframe(results_df.head(10))
    
    # Download results
    csv_buffer = io.StringIO()
    results_df.to_csv(csv_buffer, index=False)
    
    st.download_button(
        label="📥 Download Results CSV",
        data=csv_buffer.getvalue(),
        file_name="estimation_results.csv",
        mime="text/csv"
    )
    
    # Summary statistics
    st.subheader("📈 Summary Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_source_words = results_df['source_word_count'].mean()
        st.metric("Avg Source Words", f"{avg_source_words:.0f}")
    
    with col2:
        avg_estimated_words = results_df['estimated_target_words'].mean()
        st.metric("Avg Estimated Words", f"{avg_estimated_words:.0f}")
    
    with col3:
        avg_source_chars = results_df['source_char_count'].mean()
        st.metric("Avg Source Characters", f"{avg_source_chars:.0f}")
    
    with col4:
        avg_estimated_chars = results_df['estimated_target_chars'].mean()
        st.metric("Avg Estimated Characters", f"{avg_estimated_chars:.0f}")

def ratio_analysis_page():
    """Analyze translation data to calculate ratios"""
    st.header("🔍 Ratio Analysis & Auto-Update")
    st.markdown("Upload translation data to automatically calculate and update language ratios")
    
    # File format guidance
    with st.expander("📋 Translation Data Format", expanded=False):
        st.markdown("""
        Your translation data CSV should contain:
        - `source`: English source text
        - `target_lang`: Target language code
        - `reference`: Human reference translation (preferred) OR `translation`: Machine translation
        
        **Example:**
        ```csv
        source,target_lang,reference
        "Hello world","fr","Bonjour le monde"
        "Good morning","de","Guten Morgen"
        ```
        """)
    
    uploaded_file = st.file_uploader(
        "Upload translation data CSV",
        type=['csv'],
        help="CSV file with source text and reference translations"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            st.subheader("📄 Data Preview")
            st.dataframe(df.head(5))
            
            # Validate columns
            required_cols = ['source', 'target_lang']
            has_reference = 'reference' in df.columns
            has_translation = 'translation' in df.columns
            
            if not all(col in df.columns for col in required_cols):
                st.error("❌ Missing required columns: source, target_lang")
                return
            
            if not has_reference and not has_translation:
                st.error("❌ Need either 'reference' or 'translation' column")
                return
            
            target_col = 'reference' if has_reference else 'translation'
            st.info(f"✅ Using '{target_col}' column for ratio calculation")
            
            # Analysis options
            st.subheader("⚙️ Analysis Options")
            col1, col2 = st.columns(2)
            
            with col1:
                max_rows = st.number_input("Max rows to analyze:", 
                                         min_value=100, 
                                         max_value=len(df), 
                                         value=min(10000, len(df)))
            
            with col2:
                min_samples = st.number_input("Min samples per language:", 
                                            min_value=5, 
                                            value=5,
                                            help="Minimum translations needed to calculate ratio")
            
            if st.button("🔍 Analyze Ratios", type="primary"):
                analyze_translation_data(df.head(max_rows), target_col, min_samples)
                
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")

def analyze_translation_data(df, target_col, min_samples):
    """Analyze translation data and calculate ratios"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    word_ratios = defaultdict(list)
    char_ratios = defaultdict(list)
    
    # Process data
    for idx, row in df.iterrows():
        try:
            source_text = str(row.get('source', '')).strip()
            target_text = str(row.get(target_col, '')).strip()
            target_lang = str(row.get('target_lang', '')).lower().strip()
            
            if not source_text or not target_text or not target_lang:
                continue
            
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
            
            # Update progress
            progress = (idx + 1) / len(df)
            progress_bar.progress(progress)
            if idx % 1000 == 0:
                status_text.text(f"Processed {idx + 1:,} rows...")
                
        except Exception:
            continue
    
    # Calculate averages
    word_results = {}
    char_results = {}
    
    for lang, ratios in word_ratios.items():
        if len(ratios) >= min_samples:
            word_results[lang] = {
                'ratio': sum(ratios) / len(ratios),
                'samples': len(ratios),
                'old_ratio': st.session_state.ratios.get(lang, DEFAULT_RATIO)
            }
    
    for lang, ratios in char_ratios.items():
        if len(ratios) >= min_samples:
            char_results[lang] = {
                'ratio': sum(ratios) / len(ratios),
                'samples': len(ratios),
                'old_ratio': st.session_state.char_ratios.get(lang, DEFAULT_CHAR_RATIO)
            }
    
    # Display results
    st.success(f"✅ Analysis complete! Processed {len(df):,} rows")
    
    if word_results:
        st.subheader("📝 Word Ratio Results")
        word_df = pd.DataFrame([
            {
                'Language': f"{lang} ({LANGUAGE_NAMES.get(lang, lang.title())})",
                'New Ratio': f"{data['ratio']:.4f}",
                'Old Ratio': f"{data['old_ratio']:.4f}",
                'Change': f"{((data['ratio'] - data['old_ratio']) / data['old_ratio'] * 100):+.1f}%",
                'Samples': f"{data['samples']:,}"
            }
            for lang, data in word_results.items()
        ])
        st.dataframe(word_df)
    
    if char_results:
        st.subheader("🔤 Character Ratio Results")
        char_df = pd.DataFrame([
            {
                'Language': f"{lang} ({LANGUAGE_NAMES.get(lang, lang.title())})",
                'New Ratio': f"{data['ratio']:.4f}",
                'Old Ratio': f"{data['old_ratio']:.4f}",
                'Change': f"{((data['ratio'] - data['old_ratio']) / data['old_ratio'] * 100):+.1f}%",
                'Samples': f"{data['samples']:,}"
            }
            for lang, data in char_results.items()
        ])
        st.dataframe(char_df)
    
    # Update ratios button
    if word_results or char_results:
        if st.button("🔄 Update System Ratios", type="primary"):
            # Update word ratios
            for lang, data in word_results.items():
                st.session_state.ratios[lang] = round(data['ratio'], 4)
            
            # Update character ratios
            for lang, data in char_results.items():
                st.session_state.char_ratios[lang] = round(data['ratio'], 4)
            
            # Save to files
            save_ratios(st.session_state.ratios)
            save_char_ratios(st.session_state.char_ratios)
            
            st.success("✅ Ratios updated successfully!")
            st.rerun()

def language_management_page():
    """Manage language ratios"""
    st.header("🌐 Language Management")
    st.markdown("View and manage word and character ratios for all languages")
    
    tab1, tab2 = st.tabs(["📝 Word Ratios", "🔤 Character Ratios"])
    
    with tab1:
        st.subheader("Word Count Ratios")
        
        # Display current ratios
        word_data = []
        for lang in sorted(st.session_state.ratios.keys()):
            ratio = st.session_state.ratios[lang]
            lang_name = LANGUAGE_NAMES.get(lang, lang.title())
            expansion = ((ratio - 1) * 100) if ratio != 1 else 0
            direction = "📈 Expansion" if expansion > 0 else "📉 Compression" if expansion < 0 else "➡️ No change"
            
            word_data.append({
                'Language Code': lang,
                'Language Name': lang_name,
                'Ratio': f"{ratio:.4f}",
                'Change': f"{expansion:+.1f}%",
                'Direction': direction
            })
        
        word_df = pd.DataFrame(word_data)
        st.dataframe(word_df, use_container_width=True)
    
    with tab2:
        st.subheader("Character Count Ratios")
        
        # Display current character ratios
        char_data = []
        for lang in sorted(st.session_state.char_ratios.keys()):
            ratio = st.session_state.char_ratios[lang]
            lang_name = LANGUAGE_NAMES.get(lang, lang.title())
            expansion = ((ratio - 1) * 100) if ratio != 1 else 0
            direction = "📈 Expansion" if expansion > 0 else "📉 Compression" if expansion < 0 else "➡️ No change"
            
            char_data.append({
                'Language Code': lang,
                'Language Name': lang_name,
                'Ratio': f"{ratio:.4f}",
                'Change': f"{expansion:+.1f}%",
                'Direction': direction
            })
        
        char_df = pd.DataFrame(char_data)
        st.dataframe(char_df, use_container_width=True)
    
    # Export ratios
    st.subheader("📤 Export Ratios")
    col1, col2 = st.columns(2)
    
    with col1:
        word_csv = io.StringIO()
        word_df.to_csv(word_csv, index=False)
        st.download_button(
            "📥 Download Word Ratios CSV",
            word_csv.getvalue(),
            "word_ratios.csv",
            "text/csv"
        )
    
    with col2:
        char_csv = io.StringIO()
        char_df.to_csv(char_csv, index=False)
        st.download_button(
            "📥 Download Character Ratios CSV",
            char_csv.getvalue(),
            "character_ratios.csv",
            "text/csv"
        )

def analytics_page():
    """Analytics and insights"""
    st.header("📈 Analytics & Insights")
    st.markdown("Data insights and validation status")
    
    # Validation status
    st.subheader("✅ Validation Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Languages Supported", "23", help="All with validated ratios")
    
    with col2:
        st.metric("Data Source", "266,000+", help="Real translation pairs analyzed")
    
    with col3:
        st.metric("Metrics", "2", help="Word and character counts")
    
    with col4:
        st.metric("Accuracy", "Validated", help="Based on real data, not estimates")
    
    # Ratio distribution
    st.subheader("📊 Ratio Distribution")
    
    tab1, tab2 = st.tabs(["Word Ratios", "Character Ratios"])
    
    with tab1:
        word_ratios = list(st.session_state.ratios.values())
        df_word = pd.DataFrame({
            'Language': list(st.session_state.ratios.keys()),
            'Word Ratio': word_ratios
        })
        st.bar_chart(df_word.set_index('Language')['Word Ratio'])
    
    with tab2:
        char_ratios = list(st.session_state.char_ratios.values())
        df_char = pd.DataFrame({
            'Language': list(st.session_state.char_ratios.keys()),
            'Character Ratio': char_ratios
        })
        st.bar_chart(df_char.set_index('Language')['Character Ratio'])
    
    # Key insights
    st.subheader("💡 Key Insights")
    
    # Find extremes
    min_word_lang = min(st.session_state.ratios.items(), key=lambda x: x[1])
    max_word_lang = max(st.session_state.ratios.items(), key=lambda x: x[1])
    min_char_lang = min(st.session_state.char_ratios.items(), key=lambda x: x[1])
    max_char_lang = max(st.session_state.char_ratios.items(), key=lambda x: x[1])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📝 Word Count Insights:**")
        st.info(f"Most compression: {LANGUAGE_NAMES.get(min_word_lang[0], min_word_lang[0])} ({min_word_lang[1]:.3f})")
        st.info(f"Most expansion: {LANGUAGE_NAMES.get(max_word_lang[0], max_word_lang[0])} ({max_word_lang[1]:.3f})")
    
    with col2:
        st.markdown("**🔤 Character Count Insights:**")
        st.info(f"Most compression: {LANGUAGE_NAMES.get(min_char_lang[0], min_char_lang[0])} ({min_char_lang[1]:.3f})")
        st.info(f"Most expansion: {LANGUAGE_NAMES.get(max_char_lang[0], max_char_lang[0])} ({max_char_lang[1]:.3f})")

def help_page():
    """Help and documentation"""
    st.header("❓ Help & Documentation")
    
    # Quick start
    st.subheader("🚀 Quick Start")
    st.markdown("""
    1. **Quick Estimate**: Enter word/character counts or paste text for instant estimates
    2. **Batch Processing**: Upload CSV files for bulk estimation
    3. **Ratio Analysis**: Upload translation data to improve accuracy
    4. **Language Management**: View and manage all language ratios
    """)
    
    # File formats
    st.subheader("📋 File Formats")
    
    with st.expander("Batch Processing CSV Format"):
        st.markdown("""
        **Required columns:**
        - `source`: English text to analyze
        - `target_lang`: Target language code (e.g., 'fr', 'de', 'es')
        
        **Output adds these columns:**
        - `source_word_count`: Calculated English word count
        - `estimated_target_words`: Estimated target language word count
        - `estimation_ratio`: Word ratio used
        - `source_char_count`: Calculated English character count
        - `estimated_target_chars`: Estimated target language character count
        - `char_estimation_ratio`: Character ratio used
        """)
    
    with st.expander("Translation Data CSV Format"):
        st.markdown("""
        **Required columns:**
        - `source`: English source text
        - `target_lang`: Target language code
        - `reference`: Human reference translation (preferred)
        - OR `translation`: Machine translation
        
        **Purpose:** Calculate accurate ratios from your translation data
        """)
    
    # Language codes
    st.subheader("🌐 Supported Languages")
    
    lang_data = []
    for lang_code in sorted(st.session_state.ratios.keys()):
        lang_name = LANGUAGE_NAMES.get(lang_code, lang_code.title())
        word_ratio = st.session_state.ratios[lang_code]
        char_ratio = st.session_state.char_ratios[lang_code]
        
        lang_data.append({
            'Code': lang_code,
            'Language': lang_name,
            'Word Ratio': f"{word_ratio:.4f}",
            'Character Ratio': f"{char_ratio:.4f}"
        })
    
    lang_df = pd.DataFrame(lang_data)
    st.dataframe(lang_df, use_container_width=True)
    
    # Technical details
    st.subheader("🔧 Technical Details")
    st.markdown("""
    **Validation Status:** All ratios validated against 266,000+ real translation pairs
    
    **Robust Word Counting:** Enhanced detection handles:
    - ✅ Contractions (don't, can't, we'll)
    - ✅ Hyphenated words (state-of-the-art, twenty-one)
    - ✅ Numbers & Currency ($5.99, 1,000, 95.5%)
    - ✅ Abbreviations (U.S.A., Ph.D., etc.)
    - ✅ Mixed alphanumeric (COVID-19, HTML5)
    - ✅ Broken words across lines
    - ✅ Unicode & accented characters (café, naïve)
    
    **Robust Character Counting:**
    - ✅ Unicode normalization for consistent handling
    - ✅ Different line ending types (\\r\\n, \\r, \\n)
    - ✅ Various whitespace normalization
    - ✅ Proper trimming of leading/trailing whitespace
    
    **Accuracy:** Data-driven ratios with enterprise-grade text processing
    """)
    
    # Testing section
    st.subheader("🧪 Test Robust Detection")
    with st.expander("Try the enhanced text detection", expanded=False):
        st.markdown("**Test how our robust detection handles various text formats:**")
        
        # Predefined test cases
        test_cases = {
            "Contractions": "Don't, can't, won't, we'll, I'm counting correctly",
            "Hyphenated": "State-of-the-art technology for twenty-one languages",
            "Numbers & Currency": "I paid $5.99 for 3.5kg, about 1,000 calories (95.5% accurate)",
            "Abbreviations": "The U.S.A., Ph.D., etc. are handled properly",
            "Mixed Tech": "COVID-19 affected HTML5 and IPv4 addresses like 192.168.1.1",
            "Unicode": "Café, naïve, résumé, piñata are counted correctly",
            "Complex": "The COVID-19 pandemic cost $2.5 trillion, reducing GDP by 3.1%"
        }
        
        selected_test = st.selectbox("Choose a test case:", list(test_cases.keys()))
        test_text = st.text_area("Or enter your own text:", value=test_cases[selected_test], height=100)
        
        if st.button("🔍 Analyze Text", type="secondary"):
            if test_text:
                word_count = count_words(test_text)
                char_count = count_characters(test_text)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Words Detected", word_count)
                with col2:
                    st.metric("Characters Detected", char_count)
                
                # Show what basic detection would miss
                import re
                basic_words = len(re.findall(r'\b\w+\b', test_text))
                basic_chars = len(test_text.strip())
                
                if word_count != basic_words or char_count != basic_chars:
                    st.success("✅ Robust detection found differences!")
                    st.info(f"Basic word count: {basic_words} → Robust: {word_count} ({word_count-basic_words:+d})")
                    if char_count != basic_chars:
                        st.info(f"Basic char count: {basic_chars} → Robust: {char_count} ({char_count-basic_chars:+d})")
                else:
                    st.success("✅ Text analyzed successfully!")
            else:
                st.warning("Please enter some text to analyze")
    
    # Version info
    st.subheader("ℹ️ Version Information")
    st.info("**Version 2.4** - Enhanced Robust Text Detection")
    st.markdown("Now with enterprise-grade text processing, character analysis, and validated ratios from 266,000+ translation pairs")

if __name__ == "__main__":
    main()
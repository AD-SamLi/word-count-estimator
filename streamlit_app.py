#!/usr/bin/env python3
"""
Streamlit Web Application for Word Count Estimation System
Provides a user-friendly web interface for all estimation functions
"""

import streamlit as st
import pandas as pd
import csv
import io
import os
import re
from collections import defaultdict
import zipfile

try:
    import openpyxl
    EXCEL_SUPPORT = True
except ImportError:
    EXCEL_SUPPORT = False

# Configuration
RATIO_FILE = "custom_ratios.csv"
DEFAULT_RATIOS = {
    'de': 0.998, 'fr': 1.341, 'zh-hans': 0.530, 'cs': 0.938, 'ro': 1.045,
    'da': 1.000, 'es': 1.215, 'fr-ca': 1.280, 'hu': 0.950, 'ja': 0.513,
    'it': 1.155, 'ko': 0.855, 'pt': 1.170, 'ru': 0.948, 'fi': 0.780,
    'nb': 0.992, 'pt-pt': 1.168, 'nl': 1.040, 'pl': 0.939, 'sv': 0.988,
    'zh-hant': 0.501, 'tr': 0.938, 'mx': 1.158
}
DEFAULT_RATIO = 1.15

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
    """Load language ratios from file or use defaults"""
    ratios = DEFAULT_RATIOS.copy()
    if os.path.exists(RATIO_FILE):
        try:
            with open(RATIO_FILE, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    lang = row['language'].strip().lower()
                    try:
                        ratio = float(row['ratio'])
                        ratios[lang] = ratio
                    except Exception:
                        continue
        except Exception:
            pass
    return ratios

def save_ratios(ratios):
    """Save ratios to file"""
    try:
        with open(RATIO_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['language', 'ratio'])
            for lang, ratio in sorted(ratios.items()):
                writer.writerow([lang, ratio])
        return True
    except Exception:
        return False

def count_words(text):
    """Count words in text using regex"""
    if not text or not isinstance(text, str):
        return 0
    return len(re.findall(r'\b\w+\b', text.strip()))

def estimate_translated_word_count(english_word_count, target_lang, ratios):
    """Estimate translated word count"""
    ratio = ratios.get(target_lang.lower(), DEFAULT_RATIO)
    return max(1, int(round(english_word_count * ratio)))

def process_csv_data(df, ratios):
    """Process CSV data and add estimation columns"""
    results = []
    for _, row in df.iterrows():
        source_text = str(row.get('source', ''))
        target_lang = str(row.get('target_lang', '')).lower()
        
        source_words = count_words(source_text)
        estimated_words = estimate_translated_word_count(source_words, target_lang, ratios)
        ratio_used = ratios.get(target_lang, DEFAULT_RATIO)
        
        # Create new row with additional columns
        new_row = row.to_dict()
        new_row['source_word_count'] = source_words
        new_row['estimated_target_words'] = estimated_words
        new_row['estimation_ratio'] = f"{ratio_used:.4f}"
        
        results.append(new_row)
    
    return pd.DataFrame(results)

def analyze_translation_data_and_calculate_ratios(df):
    """Analyze translation data and calculate ratios automatically"""
    
    # Validate required columns
    required_cols = ['source', 'target_lang']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        return None, f"Missing required columns: {', '.join(missing_cols)}"
    
    # Check for reference or translation column
    has_reference = 'reference' in df.columns
    has_translation = 'translation' in df.columns
    
    if not has_reference and not has_translation:
        return None, "CSV must have either 'reference' or 'translation' column for ratio calculation"
    
    target_col = 'reference' if has_reference else 'translation'
    
    language_stats = {}
    processed = 0
    
    for _, row in df.iterrows():
        processed += 1
        
        try:
            source_text = str(row.get('source', '')).strip()
            target_text = str(row.get(target_col, '')).strip()
            target_lang = str(row.get('target_lang', '')).strip().lower()
            
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
    
    if not language_stats:
        return None, "No valid translation pairs found for ratio calculation"
    
    # Calculate average ratios
    calculated_ratios = {}
    analysis_results = []
    
    for lang, ratio_list in language_stats.items():
        if len(ratio_list) >= 5:  # Lower threshold for web interface
            avg_ratio = sum(ratio_list) / len(ratio_list)
            calculated_ratios[lang] = round(avg_ratio, 4)
            
            lang_name = LANGUAGE_NAMES.get(lang, lang.title())
            analysis_results.append({
                'Language Code': lang,
                'Language Name': lang_name,
                'Calculated Ratio': round(avg_ratio, 4),
                'Sample Count': len(ratio_list),
                'Min Ratio': round(min(ratio_list), 4),
                'Max Ratio': round(max(ratio_list), 4),
                'Status': '✅ Updated' if len(ratio_list) >= 10 else '⚠️ Low samples'
            })
        else:
            lang_name = LANGUAGE_NAMES.get(lang, lang.title())
            analysis_results.append({
                'Language Code': lang,
                'Language Name': lang_name,
                'Calculated Ratio': 'N/A',
                'Sample Count': len(ratio_list),
                'Min Ratio': 'N/A',
                'Max Ratio': 'N/A',
                'Status': '❌ Insufficient data'
            })
    
    results_df = pd.DataFrame(analysis_results)
    
    return {
        'ratios': calculated_ratios,
        'analysis': results_df,
        'target_column': target_col,
        'total_processed': processed
    }, None

def main():
    st.set_page_config(
        page_title="Word Count Estimation System",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    if 'ratios' not in st.session_state:
        st.session_state.ratios = load_ratios()
    
    # Header
    st.title("🌍 Word Count Estimation System")
    st.markdown("**Estimate translated word counts from English to various target languages**")
    
    # Sidebar for navigation
    st.sidebar.title("🎛️ Navigation")
    page = st.sidebar.selectbox(
        "Choose a function:",
        ["🚀 Quick Estimate", "📊 Batch Processing", "🔍 Ratio Analysis", "🌐 Language Management", "📈 Analytics", "❓ Help"]
    )
    
    # Display current language support
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🌐 Supported Languages")
    st.sidebar.markdown(f"**{len(st.session_state.ratios)} languages** currently supported")
    
    # Quick language reference
    with st.sidebar.expander("View Languages"):
        for lang, ratio in sorted(st.session_state.ratios.items()):
            lang_name = LANGUAGE_NAMES.get(lang, lang.title())
            st.write(f"**{lang}**: {lang_name} ({ratio:.3f})")
    
    # Main content based on selected page
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
    else:
        help_page()

def quick_estimate_page():
    """Quick estimation interface"""
    st.header("🚀 Quick Word Count Estimation")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Input")
        english_words = st.number_input(
            "English Word Count:",
            min_value=1,
            max_value=100000,
            value=1000,
            step=1,
            help="Enter the number of English words to estimate"
        )
        
        # Language selection with search
        lang_options = {}
        for lang, ratio in sorted(st.session_state.ratios.items()):
            lang_name = LANGUAGE_NAMES.get(lang, lang.title())
            lang_options[f"{lang} - {lang_name}"] = lang
        
        selected_lang_display = st.selectbox(
            "Target Language:",
            options=list(lang_options.keys()),
            help="Select the target language for estimation"
        )
        
        target_lang = lang_options[selected_lang_display]
        
        # Custom ratio option
        use_custom_ratio = st.checkbox("Use custom ratio", help="Override the default ratio for this calculation")
        
        if use_custom_ratio:
            custom_ratio = st.number_input(
                "Custom Ratio:",
                min_value=0.1,
                max_value=5.0,
                value=st.session_state.ratios.get(target_lang, DEFAULT_RATIO),
                step=0.01,
                format="%.3f"
            )
            ratio_to_use = custom_ratio
        else:
            ratio_to_use = st.session_state.ratios.get(target_lang, DEFAULT_RATIO)
    
    with col2:
        st.subheader("Results")
        
        if st.button("Calculate Estimate", type="primary"):
            estimated_words = max(1, int(round(english_words * ratio_to_use)))
            
            # Display results
            st.success("✅ Estimation Complete!")
            
            # Metrics
            col_metric1, col_metric2, col_metric3 = st.columns(3)
            
            with col_metric1:
                st.metric("English Words", f"{english_words:,}")
            
            with col_metric2:
                st.metric("Estimated Words", f"{estimated_words:,}")
            
            with col_metric3:
                change_pct = ((estimated_words - english_words) / english_words) * 100
                st.metric("Change", f"{change_pct:+.1f}%")
            
            # Additional info
            st.info(f"**Language**: {LANGUAGE_NAMES.get(target_lang, target_lang.title())}")
            st.info(f"**Ratio Used**: {ratio_to_use:.4f}")
            
            if change_pct > 0:
                st.warning(f"📈 Text expansion expected: +{change_pct:.1f}%")
            elif change_pct < 0:
                st.warning(f"📉 Text compression expected: {change_pct:.1f}%")
            else:
                st.info("📊 No significant change expected")

def batch_processing_page():
    """Batch processing interface"""
    st.header("📊 Batch Processing")
    st.markdown("Upload a CSV file to process multiple translations at once")
    
    # Show required format
    with st.expander("📋 Required CSV Format", expanded=False):
        st.markdown("""
        **Required Columns:**
        - `source`: English source text
        - `target_lang`: Target language code (e.g., 'fr', 'de', 'es')
        
        **Optional Columns:**
        - `language_pair`: Language pair identifier
        - `source_lang`: Source language (usually 'en')
        - `system`: Translation system identifier
        - `translation`: Machine translation output
        - `reference`: Human reference translation
        
        **Example CSV:**
        ```csv
        source,target_lang,translation,reference
        "Hello world","fr","Bonjour le monde","Bonjour le monde"
        "Good morning","de","Guten Morgen","Guten Morgen"
        "How are you?","es","¿Cómo estás?","¿Cómo estás?"
        ```
        
        **Output:** Your CSV will get 3 new columns:
        - `source_word_count`: Calculated English word count
        - `estimated_target_words`: Estimated target language word count
        - `estimation_ratio`: Ratio used for estimation
        """)
        
        # Download template
        if os.path.exists('sample_batch_template.csv'):
            with open('sample_batch_template.csv', 'r', encoding='utf-8') as f:
                template_data = f.read()
            st.download_button(
                "📥 Download Template CSV",
                data=template_data,
                file_name="batch_template.csv",
                mime="text/csv",
                help="Download a sample CSV file with the correct format"
            )
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose CSV file",
        type=['csv'],
        help="Upload a CSV file with the format shown above"
    )
    
    if uploaded_file is not None:
        try:
            # Read CSV
            df = pd.read_csv(uploaded_file)
            
            st.success(f"✅ File uploaded successfully! Found {len(df):,} rows")
            
            # Validate required columns
            required_cols = ['source', 'target_lang']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
                st.info("Required columns: 'source' (English text), 'target_lang' (language code)")
                return
            
            # Show preview
            st.subheader("📋 Data Preview")
            st.dataframe(df.head(10))
            
            # Processing options
            st.subheader("⚙️ Processing Options")
            
            col1, col2 = st.columns(2)
            
            with col1:
                process_all = st.checkbox("Process all rows", value=True)
                if not process_all:
                    max_rows = st.number_input(
                        "Maximum rows to process:",
                        min_value=1,
                        max_value=len(df),
                        value=min(1000, len(df))
                    )
                else:
                    max_rows = len(df)
            
            with col2:
                include_analytics = st.checkbox("Include analytics", value=True)
            
            # Process button
            if st.button("🚀 Process Data", type="primary"):
                with st.spinner("Processing data..."):
                    # Limit rows if needed
                    df_to_process = df.head(max_rows) if not process_all else df
                    
                    # Process the data
                    result_df = process_csv_data(df_to_process, st.session_state.ratios)
                    
                    st.success(f"✅ Processed {len(result_df):,} rows successfully!")
                    
                    # Show results preview
                    st.subheader("📊 Results Preview")
                    st.dataframe(result_df.head(10))
                    
                    # Analytics
                    if include_analytics:
                        st.subheader("📈 Processing Analytics")
                        
                        # Language breakdown
                        lang_stats = result_df.groupby('target_lang').agg({
                            'source_word_count': ['count', 'mean', 'sum'],
                            'estimated_target_words': ['mean', 'sum']
                        }).round(1)
                        
                        lang_stats.columns = ['Rows', 'Avg Source', 'Total Source', 'Avg Estimated', 'Total Estimated']
                        lang_stats['Effective Ratio'] = (lang_stats['Total Estimated'] / lang_stats['Total Source']).round(3)
                        
                        st.dataframe(lang_stats)
                    
                    # Download options
                    st.subheader("💾 Download Results")
                    
                    # Convert to CSV
                    csv_buffer = io.StringIO()
                    result_df.to_csv(csv_buffer, index=False)
                    csv_data = csv_buffer.getvalue()
                    
                    # Download button
                    st.download_button(
                        label="📥 Download CSV Results",
                        data=csv_data,
                        file_name=f"word_count_estimates_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                    
                    # Excel download (if supported)
                    if EXCEL_SUPPORT:
                        excel_buffer = io.BytesIO()
                        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                            result_df.to_excel(writer, sheet_name='Estimates', index=False)
                            if include_analytics:
                                lang_stats.to_excel(writer, sheet_name='Analytics')
                        
                        st.download_button(
                            label="📥 Download Excel Results",
                            data=excel_buffer.getvalue(),
                            file_name=f"word_count_estimates_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
        
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")

def ratio_analysis_page():
    """Ratio analysis and automatic updating from translation data"""
    st.header("🔍 Ratio Analysis & Auto-Update")
    st.markdown("Upload translation data to automatically calculate and update language ratios")
    
    # Show required format
    with st.expander("📋 Required CSV Format for Ratio Analysis", expanded=False):
        st.markdown("""
        **Required Columns:**
        - `source`: English source text
        - `target_lang`: Target language code (e.g., 'fr', 'de', 'es')
        - `reference` OR `translation`: Target language text
        
        **Optional Columns:**
        - `language_pair`: Language pair identifier
        - `source_lang`: Source language (usually 'en')
        - `system`: Translation system identifier
        
        **Example CSV:**
        ```csv
        source,target_lang,reference,translation
        "Hello world","fr","Bonjour le monde","Bonjour le monde"
        "Good morning","de","Guten Morgen","Guten Morgen"
        "How are you?","es","¿Cómo estás?","¿Cómo estás?"
        ```
        
        **Note:** The system will use `reference` column if available (preferred for accuracy), otherwise `translation` column.
        """)
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose translation data CSV file",
        type=['csv'],
        help="Upload a CSV file with translation data to analyze ratios"
    )
    
    if uploaded_file is not None:
        try:
            # Read CSV
            df = pd.read_csv(uploaded_file)
            
            st.success(f"✅ File uploaded successfully! Found {len(df):,} rows")
            
            # Show preview
            st.subheader("📋 Data Preview")
            st.dataframe(df.head(10))
            
            # Analysis options
            st.subheader("⚙️ Analysis Options")
            
            col1, col2 = st.columns(2)
            
            with col1:
                analyze_all = st.checkbox("Analyze all rows", value=True)
                if not analyze_all:
                    max_rows = st.number_input(
                        "Maximum rows to analyze:",
                        min_value=100,
                        max_value=len(df),
                        value=min(10000, len(df))
                    )
                else:
                    max_rows = len(df)
            
            with col2:
                min_samples = st.number_input(
                    "Minimum samples per language:",
                    min_value=5,
                    max_value=100,
                    value=10,
                    help="Languages with fewer samples won't be updated"
                )
            
            # Analyze button
            if st.button("🔍 Analyze Translation Data", type="primary"):
                with st.spinner("Analyzing translation data..."):
                    # Limit rows if needed
                    df_to_analyze = df.head(max_rows) if not analyze_all else df
                    
                    # Analyze the data
                    result, error = analyze_translation_data_and_calculate_ratios(df_to_analyze)
                    
                    if error:
                        st.error(f"❌ {error}")
                        return
                    
                    st.success(f"✅ Analyzed {result['total_processed']:,} rows successfully!")
                    
                    # Show analysis results
                    st.subheader("📊 Ratio Analysis Results")
                    st.info(f"**Using column:** {result['target_column']} (for target word count)")
                    
                    # Display analysis table
                    st.dataframe(result['analysis'], use_container_width=True)
                    
                    # Update ratios section
                    st.subheader("🔄 Update System Ratios")
                    
                    # Filter ratios that meet minimum sample requirement
                    valid_ratios = {lang: ratio for lang, ratio in result['ratios'].items() 
                                  if any(row['Language Code'] == lang and row['Sample Count'] >= min_samples 
                                        for _, row in result['analysis'].iterrows())}
                    
                    if valid_ratios:
                        st.info(f"**{len(valid_ratios)} languages** meet the minimum sample requirement ({min_samples} samples)")
                        
                        # Show what will be updated
                        update_preview = []
                        for lang, new_ratio in valid_ratios.items():
                            old_ratio = st.session_state.ratios.get(lang, DEFAULT_RATIO)
                            lang_name = LANGUAGE_NAMES.get(lang, lang.title())
                            change_pct = ((new_ratio - old_ratio) / old_ratio) * 100
                            
                            update_preview.append({
                                'Language': f"{lang} ({lang_name})",
                                'Current Ratio': f"{old_ratio:.4f}",
                                'New Ratio': f"{new_ratio:.4f}",
                                'Change': f"{change_pct:+.1f}%"
                            })
                        
                        st.dataframe(pd.DataFrame(update_preview), use_container_width=True)
                        
                        # Update button
                        if st.button("✅ Update System Ratios", type="primary"):
                            # Update ratios in session state
                            for lang, ratio in valid_ratios.items():
                                st.session_state.ratios[lang] = ratio
                            
                            # Save to file
                            if save_ratios(st.session_state.ratios):
                                st.success(f"🎉 Successfully updated {len(valid_ratios)} language ratios!")
                                st.balloons()
                                
                                # Show updated ratios
                                st.subheader("📈 Updated Ratios Summary")
                                for lang, ratio in valid_ratios.items():
                                    lang_name = LANGUAGE_NAMES.get(lang, lang.title())
                                    st.write(f"**{lang}** ({lang_name}): {ratio:.4f}")
                                
                                st.rerun()
                            else:
                                st.error("❌ Failed to save updated ratios")
                    else:
                        st.warning(f"⚠️ No languages meet the minimum sample requirement ({min_samples} samples)")
                        st.info("💡 Try reducing the minimum samples threshold or upload more translation data")
                    
                    # Export analysis results
                    st.subheader("💾 Export Analysis Results")
                    
                    # CSV export
                    csv_buffer = io.StringIO()
                    result['analysis'].to_csv(csv_buffer, index=False)
                    csv_data = csv_buffer.getvalue()
                    
                    st.download_button(
                        label="📥 Download Analysis Report (CSV)",
                        data=csv_data,
                        file_name=f"ratio_analysis_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
        
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")

def language_management_page():
    """Language and ratio management interface"""
    st.header("🌐 Language Management")
    
    tab1, tab2, tab3 = st.tabs(["📊 Current Ratios", "➕ Add/Update", "📥 Import/Export"])
    
    with tab1:
        st.subheader("Current Language Ratios")
        
        # Create DataFrame for display
        ratio_data = []
        for lang, ratio in sorted(st.session_state.ratios.items()):
            lang_name = LANGUAGE_NAMES.get(lang, lang.title())
            expansion = ((ratio - 1) * 100)
            ratio_data.append({
                'Code': lang,
                'Language': lang_name,
                'Ratio': ratio,
                'Expansion %': f"{expansion:+.1f}%"
            })
        
        ratio_df = pd.DataFrame(ratio_data)
        st.dataframe(ratio_df, use_container_width=True)
        
        # Summary stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Languages", len(st.session_state.ratios))
        with col2:
            avg_ratio = sum(st.session_state.ratios.values()) / len(st.session_state.ratios)
            st.metric("Average Ratio", f"{avg_ratio:.3f}")
        with col3:
            st.metric("Default Ratio", f"{DEFAULT_RATIO:.3f}")
    
    with tab2:
        st.subheader("Add or Update Language Ratios")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Add new language
            st.markdown("#### Add New Language")
            new_lang_code = st.text_input("Language Code", placeholder="e.g., 'pt-br'")
            new_lang_name = st.text_input("Language Name", placeholder="e.g., 'Portuguese (Brazil)'")
            new_ratio = st.number_input("Ratio", min_value=0.1, max_value=5.0, value=1.0, step=0.01)
            
            if st.button("➕ Add Language"):
                if new_lang_code and new_ratio:
                    st.session_state.ratios[new_lang_code.lower()] = new_ratio
                    if new_lang_name:
                        LANGUAGE_NAMES[new_lang_code.lower()] = new_lang_name
                    
                    if save_ratios(st.session_state.ratios):
                        st.success(f"✅ Added {new_lang_code} with ratio {new_ratio}")
                        st.rerun()
                    else:
                        st.error("❌ Failed to save ratios")
                else:
                    st.error("❌ Please provide language code and ratio")
        
        with col2:
            # Update existing language
            st.markdown("#### Update Existing Language")
            
            lang_to_update = st.selectbox(
                "Select Language to Update:",
                options=list(st.session_state.ratios.keys()),
                format_func=lambda x: f"{x} - {LANGUAGE_NAMES.get(x, x.title())}"
            )
            
            current_ratio = st.session_state.ratios.get(lang_to_update, 1.0)
            updated_ratio = st.number_input(
                "New Ratio",
                min_value=0.1,
                max_value=5.0,
                value=current_ratio,
                step=0.01,
                key="update_ratio"
            )
            
            col_update, col_delete = st.columns(2)
            
            with col_update:
                if st.button("🔄 Update Ratio"):
                    st.session_state.ratios[lang_to_update] = updated_ratio
                    if save_ratios(st.session_state.ratios):
                        st.success(f"✅ Updated {lang_to_update} to {updated_ratio}")
                        st.rerun()
                    else:
                        st.error("❌ Failed to save ratios")
            
            with col_delete:
                if st.button("🗑️ Delete Language", type="secondary"):
                    if lang_to_update not in DEFAULT_RATIOS:
                        del st.session_state.ratios[lang_to_update]
                        if save_ratios(st.session_state.ratios):
                            st.success(f"✅ Deleted {lang_to_update}")
                            st.rerun()
                        else:
                            st.error("❌ Failed to save ratios")
                    else:
                        st.error("❌ Cannot delete default language")
    
    with tab3:
        st.subheader("Import/Export Ratios")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Import Ratios")
            
            # Show file format requirements
            with st.expander("📋 Required File Format", expanded=True):
                st.markdown("""
                **CSV Format:**
                ```csv
                language,ratio
                fr,1.341
                de,0.998
                es,1.215
                ja,0.513
                ```
                
                **Excel Format:**
                - Column A: language (e.g., 'fr', 'de', 'es')
                - Column B: ratio (e.g., 1.341, 0.998, 1.215)
                - Row 1: Headers ('language', 'ratio')
                - Row 2+: Data
                
                **Requirements:**
                - Language codes must be lowercase
                - Ratios must be positive numbers
                - Use decimal point (not comma) for ratios
                """)
            
            # Download template
            if os.path.exists('sample_ratios_template.csv'):
                with open('sample_ratios_template.csv', 'r', encoding='utf-8') as f:
                    template_data = f.read()
                st.download_button(
                    "📥 Download Ratios Template",
                    data=template_data,
                    file_name="ratios_template.csv",
                    mime="text/csv",
                    help="Download a sample ratios file with the correct format"
                )
            
            uploaded_ratios = st.file_uploader(
                "Upload ratios file",
                type=['csv', 'xlsx'],
                help="Upload a CSV or Excel file with the format shown above"
            )
            
            if uploaded_ratios is not None:
                try:
                    if uploaded_ratios.name.endswith('.csv'):
                        ratios_df = pd.read_csv(uploaded_ratios)
                    else:
                        ratios_df = pd.read_excel(uploaded_ratios)
                    
                    if 'language' in ratios_df.columns and 'ratio' in ratios_df.columns:
                        st.dataframe(ratios_df.head())
                        
                        if st.button("📥 Import Ratios"):
                            imported_count = 0
                            for _, row in ratios_df.iterrows():
                                lang = str(row['language']).strip().lower()
                                try:
                                    ratio = float(row['ratio'])
                                    st.session_state.ratios[lang] = ratio
                                    imported_count += 1
                                except Exception:
                                    continue
                            
                            if save_ratios(st.session_state.ratios):
                                st.success(f"✅ Imported {imported_count} ratios")
                                st.rerun()
                            else:
                                st.error("❌ Failed to save ratios")
                    else:
                        st.error("❌ File must have 'language' and 'ratio' columns")
                
                except Exception as e:
                    st.error(f"❌ Error reading file: {str(e)}")
        
        with col2:
            st.markdown("#### Export Ratios")
            
            # Create export DataFrame
            export_data = []
            for lang, ratio in sorted(st.session_state.ratios.items()):
                export_data.append({
                    'language': lang,
                    'ratio': ratio,
                    'language_name': LANGUAGE_NAMES.get(lang, lang.title())
                })
            
            export_df = pd.DataFrame(export_data)
            
            # CSV export
            csv_export = export_df[['language', 'ratio']].to_csv(index=False)
            st.download_button(
                "📤 Export as CSV",
                data=csv_export,
                file_name=f"language_ratios_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
            
            # Excel export (if supported)
            if EXCEL_SUPPORT:
                excel_buffer = io.BytesIO()
                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                    export_df.to_excel(writer, sheet_name='Ratios', index=False)
                
                st.download_button(
                    "📤 Export as Excel",
                    data=excel_buffer.getvalue(),
                    file_name=f"language_ratios_{pd.Timestamp.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

def analytics_page():
    """Analytics and insights page"""
    st.header("📈 System Analytics")
    
    # Ratio analysis
    st.subheader("🔍 Ratio Analysis")
    
    ratios = list(st.session_state.ratios.values())
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Languages", len(ratios))
    with col2:
        st.metric("Avg Ratio", f"{sum(ratios)/len(ratios):.3f}")
    with col3:
        st.metric("Min Ratio", f"{min(ratios):.3f}")
    with col4:
        st.metric("Max Ratio", f"{max(ratios):.3f}")
    
    # Ratio distribution chart
    st.subheader("📊 Ratio Distribution")
    
    # Create bins for ratio ranges
    ratio_ranges = {
        "High Compression (< 0.7)": [lang for lang, ratio in st.session_state.ratios.items() if ratio < 0.7],
        "Moderate Compression (0.7-0.9)": [lang for lang, ratio in st.session_state.ratios.items() if 0.7 <= ratio < 0.9],
        "Neutral (0.9-1.1)": [lang for lang, ratio in st.session_state.ratios.items() if 0.9 <= ratio < 1.1],
        "Moderate Expansion (1.1-1.3)": [lang for lang, ratio in st.session_state.ratios.items() if 1.1 <= ratio < 1.3],
        "High Expansion (≥ 1.3)": [lang for lang, ratio in st.session_state.ratios.items() if ratio >= 1.3]
    }
    
    for range_name, languages in ratio_ranges.items():
        if languages:
            st.write(f"**{range_name}**: {len(languages)} languages")
            lang_display = ", ".join([f"{lang} ({st.session_state.ratios[lang]:.3f})" for lang in languages[:5]])
            if len(languages) > 5:
                lang_display += f" ... and {len(languages)-5} more"
            st.write(lang_display)
    
    # Language families analysis
    st.subheader("🌍 Language Families")
    
    language_families = {
        "Germanic": ['de', 'nl', 'da', 'nb', 'sv'],
        "Romance": ['fr', 'fr-ca', 'es', 'mx', 'it', 'pt', 'pt-pt', 'ro'],
        "Slavic": ['cs', 'pl', 'ru'],
        "East Asian": ['zh-hans', 'zh-hant', 'ja', 'ko'],
        "Finno-Ugric": ['fi', 'hu'],
        "Turkic": ['tr']
    }
    
    for family, languages in language_families.items():
        family_ratios = [st.session_state.ratios.get(lang) for lang in languages if lang in st.session_state.ratios]
        if family_ratios:
            avg_ratio = sum(family_ratios) / len(family_ratios)
            st.write(f"**{family}**: {len(family_ratios)} languages, avg ratio: {avg_ratio:.3f}")

def help_page():
    """Help and documentation page"""
    st.header("❓ Help & Documentation")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🚀 Quick Start", "📊 File Formats", "🔧 Troubleshooting", "📖 About"])
    
    with tab1:
        st.subheader("Quick Start Guide")
        
        st.markdown("""
        ### 🎯 Getting Started
        
        1. **Quick Estimate**: Use the "Quick Estimate" page for single calculations
        2. **Batch Processing**: Upload CSV files for bulk processing
        3. **Language Management**: Add, update, or remove language ratios
        4. **Analytics**: View system statistics and insights
        
        ### 💡 Tips
        - Language codes should be lowercase (e.g., 'fr', 'de', 'zh-hans')
        - Ratios > 1.0 indicate text expansion, < 1.0 indicate compression
        - Use custom ratios for specific projects or clients
        - Export your ratios regularly as backup
        """)
    
    with tab2:
        st.subheader("File Formats")
        
        st.markdown("""
        ### 📁 CSV Format for Batch Processing
        
        **Required columns:**
        - `source`: English source text (in quotes if contains commas)
        - `target_lang`: Target language code (lowercase, e.g., 'fr', 'de', 'es')
        
        **Optional columns:**
        - `language_pair`: Language pair identifier (e.g., 'en-fr')
        - `source_lang`: Source language (usually 'en')
        - `system`: Translation system identifier
        - `translation`: Machine translation output
        - `reference`: Human reference translation
        
        **Example:**
        ```csv
        source,target_lang,translation,reference
        "Hello world","fr","Bonjour le monde","Bonjour le monde"
        "Good morning","de","Guten Morgen","Guten Morgen"
        "How are you today?","es","¿Cómo estás hoy?","¿Cómo estás hoy?"
        ```
        
        **Important Notes:**
        - Use UTF-8 encoding for special characters
        - Put text in quotes if it contains commas
        - Language codes must be lowercase
        - Empty cells are handled gracefully
        
        ### 📊 Ratio Import Format
        
        **CSV format:**
        ```csv
        language,ratio
        fr,1.341
        de,0.998
        es,1.215
        ja,0.513
        zh-hans,0.530
        ```
        
        **Excel format:**
        - Column A: language codes (fr, de, es, etc.)
        - Column B: ratio values (1.341, 0.998, 1.215, etc.)
        - Row 1: Headers ('language', 'ratio')
        - Rows 2+: Data
        
        **Ratio Guidelines:**
        - Values > 1.0 = text expansion (target longer than source)
        - Values < 1.0 = text compression (target shorter than source)
        - Values = 1.0 = neutral (same length)
        - Typical range: 0.5 to 2.0
        - Use decimal point (.) not comma (,)
        """)
    
    with tab3:
        st.subheader("Troubleshooting")
        
        st.markdown("""
        ### ⚠️ Common Issues
        
        **File Upload Problems:**
        - Ensure CSV files are UTF-8 encoded
        - Check that required columns exist
        - File size limit may apply for very large files
        
        **Ratio Issues:**
        - Language codes must be lowercase
        - Ratios should be positive numbers
        - Changes are saved automatically
        
        **Processing Errors:**
        - Check for empty or invalid data in source column
        - Ensure target_lang column contains valid language codes
        - Try processing smaller batches for large files
        
        ### 🔧 Reset Options
        - Language ratios can be reset to defaults in Language Management
        - Clear browser cache if interface issues persist
        """)
    
    with tab4:
        st.subheader("About This System")
        
        st.markdown("""
        ### 🌍 Word Count Estimation System
        
        **Version:** 2.0  
        **Languages Supported:** 23  
        **Data Source:** 266,000+ translation pairs
        
        ### 🎯 Purpose
        This system provides accurate word count estimations for translation projects by analyzing actual translation data and applying learned language-specific expansion/compression ratios.
        
        ### 📊 Features
        - Interactive web interface
        - Batch processing capabilities
        - Custom ratio management
        - Real-time analytics
        - Export functionality
        
        ### 🔬 Methodology
        Ratios are derived from analyzing real translation data, providing more accurate estimates than traditional rule-of-thumb approaches.
        
        ### 💾 Data Privacy
        - All processing happens locally
        - No data is sent to external servers
        - Files are processed in memory only
        """)

if __name__ == "__main__":
    main()
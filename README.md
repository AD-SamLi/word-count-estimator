# Word Count Estimation System

A comprehensive system for estimating translated word counts from English to various target languages using data-driven ratios derived from real translation data.

## 🌐 **Live Web Application**

**🚀 Try it now:** https://mt-word-count-estimator.streamlit.app/

**Features available online:**
- ⚡ **Quick Estimates** - Get instant word count estimates for any language
- 📊 **Batch Processing** - Upload CSV files for bulk estimation  
- 🔧 **Ratio Management** - View and update language expansion ratios
- 📈 **Translation Analysis** - Automatically calculate ratios from your translation data
- 📱 **Mobile Friendly** - Works on any device, no installation required

*No installation required - works directly in your browser!*

## 🎯 Overview

This system provides accurate word count estimations for translation projects by analyzing actual translation data and applying learned language-specific expansion/compression ratios. It supports both interactive single estimates and batch processing of large CSV datasets.

## 📁 Project Structure

```
word_estimation/
├── README.md                           # This documentation
├── requirements.txt                    # Python dependencies
├── streamlit_app.py                    # Web interface with ratio analysis
├── launch_webapp.bat                   # Windows launcher script
├── unified_word_count_estimator.py     # CLI with auto-ratio updating
├── analyze_data.py                     # Data analysis utility
├── sample_batch_template.csv           # Template for batch processing
├── sample_ratios_template.csv          # Template for ratio updates
├── all_results_en.csv                  # Sample translation dataset (70MB)
├── all_results_estimation.csv          # Processed results with estimates (76MB)
├── Python Translation Word Count Estimation_.docx  # Reference documentation
└── .env                                # Environment configuration
```

## 🚀 Quick Start

### Option 1: Use Online (Recommended)
**Simply visit:** https://mt-word-count-estimator.streamlit.app/
- No installation required
- Works on any device
- Always up-to-date
- Free to use

### Option 2: Run Locally

#### Prerequisites
- Python 3.7+
- Required: `streamlit`, `pandas` for web interface
- Optional: `openpyxl` for Excel file support

#### Installation
```bash
pip install -r requirements.txt
```

#### Running the System

##### 🌐 Web Interface (Recommended)
```bash
streamlit run streamlit_app.py
```
Or double-click `launch_webapp.bat` on Windows

#### 💻 Command Line Interface
```bash
python unified_word_count_estimator.py
```

## 💡 Features

### 🌐 Web Interface (New!)
- **User-friendly web dashboard** with intuitive navigation
- **Drag-and-drop file uploads** for batch processing
- **Automatic ratio analysis** from translation data (NEW!)
- **Real-time analytics** and visualizations
- **Interactive language management** with live updates
- **Export functionality** (CSV, Excel) with one-click downloads

### ✅ Interactive Mode
- Quick word count estimates for any language
- Real-time language support display
- User-friendly command interface

### ✅ Batch Processing Mode
- Process large CSV files with translation data
- Add estimation columns to existing datasets
- Progress tracking for large files
- **Web-based progress monitoring**

### ✅ Dynamic Ratio Management
- **Automatic ratio calculation** from translation data (NEW!)
- Update ratios from Excel/CSV files
- Persistent custom ratio storage
- Data-driven optimization
- **Visual ratio management interface**

### ✅ Multi-Language Support
Currently supports **23 languages** with optimized ratios:
- **Asian Languages**: Chinese (Simplified/Traditional), Japanese, Korean
- **European Languages**: German, French, Spanish, Italian, Portuguese, Dutch, etc.
- **Nordic Languages**: Danish, Norwegian, Swedish, Finnish
- **Slavic Languages**: Czech, Polish, Russian
- **Others**: Turkish, Romanian, Hungarian

## 📊 Input File Formats

### 1. Translation Dataset CSV Format

For batch processing, your CSV file must contain these **required columns**:

```csv
language_pair,source_lang,target_lang,system,source,translation,reference
en-fr,en,fr,system1,"Hello world","Bonjour le monde","Bonjour le monde"
en-de,en,de,system2,"Good morning","Guten Morgen","Guten Morgen"
```

#### Required Columns:
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `source` | String | English source text | `"Hello world"` |
| `target_lang` | String | Target language code | `"fr"`, `"de"`, `"es"` |

#### Optional Columns:
| Column | Type | Description |
|--------|------|-------------|
| `language_pair` | String | Language pair identifier |
| `source_lang` | String | Source language (typically "en") |
| `system` | String | Translation system identifier |
| `translation` | String | Machine translation output |
| `reference` | String | Human reference translation |

#### Output Format:
The system adds three new columns to your CSV:
- `source_word_count`: Calculated English word count
- `estimated_target_words`: Estimated target language word count
- `estimation_ratio`: Ratio used for estimation

### 2. Custom Ratios CSV Format

To update language ratios, use this format:

```csv
language,ratio
fr,1.341
de,0.998
es,1.215
ja,0.513
```

#### Columns:
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `language` | String | Language code | `"fr"`, `"de"` |
| `ratio` | Float | Expansion/compression ratio | `1.341`, `0.998` |

### 3. Excel Ratios Format

For Excel files (.xlsx), use the same structure:
- **Column A**: Language codes
- **Column B**: Ratios
- **Row 1**: Headers (`language`, `ratio`)
- **Row 2+**: Data

## 🎮 Usage Examples

### 🌐 Web Interface Usage

1. **Start the web app:**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Quick Estimates:**
   - Navigate to "Quick Estimate" page
   - Enter English word count and select target language
   - Get instant results with expansion/compression analysis

3. **Batch Processing:**
   - Go to "Batch Processing" page
   - Upload CSV file with drag-and-drop
   - Download results with added estimation columns

4. **Ratio Analysis (NEW!):**
   - Upload translation data CSV to automatically calculate ratios
   - Analyze your own translation data for better accuracy
   - One-click ratio updates with validation

5. **Language Management:**
   - Use "Language Management" to view, add, or update ratios
   - Import/export ratio configurations  
   - Real-time ratio validation

### 💻 Command Line Usage

```bash
# Start the CLI system
python unified_word_count_estimator.py

# Quick estimates
💬 Enter command: 1000 fr
✅ 1,000 English words → 1,341 French words

💬 Enter command: 500 ja  
✅ 500 English words → 257 Japanese words

# Show available languages
💬 Enter command: languages

# Show current ratios
💬 Enter command: show
```

### Batch Processing (CLI)

```bash
# Process a CSV file
💬 Enter command: batch input_data.csv output_with_estimates.csv
Processing input_data.csv ...
Processed 50,000 rows...
✅ Done! Output: output_with_estimates.csv
```

### Automatic Ratio Analysis (CLI) - NEW!

```bash
# Analyze translation data and auto-update ratios
💬 Enter command: analyze all_results_en.csv
Analyzing translation data from all_results_en.csv...
📊 CALCULATED RATIOS FROM 266,000 ROWS:
fr         (French             ): 1.3410 (was 1.3410) [19,000 samples]
de         (German             ): 0.9980 (was 0.9980) [24,000 samples]
✅ Updated 23 language ratios based on your translation data
```

### Update Ratios (CLI)

```bash
# From CSV file
💬 Enter command: update csv new_ratios.csv
✅ Updated 15 ratios from new_ratios.csv

# From Excel file  
💬 Enter command: update excel ratios.xlsx
✅ Updated 20 ratios from ratios.xlsx
```

## 📋 Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `<number> <lang>` | Quick estimate | `1000 fr` |
| `batch <input> <output>` | Process CSV | `batch data.csv results.csv` |
| `analyze <translation_csv>` | Auto-update ratios from data | `analyze all_results_en.csv` |
| `languages` | Show detailed language info | |
| `show` | Display current ratios | |
| `update csv <path>` | Update from CSV | `update csv ratios.csv` |
| `update excel <path>` | Update from Excel | `update excel ratios.xlsx` |
| `help` | Show help | |
| `quit` | Exit program | |

## 🔧 Data Analysis Utility

Use `analyze_data.py` to explore your translation datasets:

```bash
python analyze_data.py [csv_file]
```

This utility provides:
- Dataset structure analysis
- Language distribution statistics
- Translation system breakdown
- Data quality insights

## 📈 Language Ratios

The system uses optimized ratios derived from analyzing 266,000+ real translation examples:

| Language | Code | Ratio | Expansion/Compression |
|----------|------|-------|---------------------|
| Chinese (Traditional) | zh-hant | 0.501 | 50% compression |
| Japanese | ja | 0.513 | 49% compression |
| Chinese (Simplified) | zh-hans | 0.530 | 47% compression |
| Finnish | fi | 0.780 | 22% compression |
| Korean | ko | 0.855 | 15% compression |
| German | de | 0.998 | 0% change |
| Danish | da | 1.000 | No change |
| Spanish | es | 1.215 | 22% expansion |
| French | fr | 1.341 | 34% expansion |

## ⚙️ Configuration

### Environment Variables (.env)
```env
# Optional configuration
DEFAULT_RATIO=1.15
RATIO_FILE=custom_ratios.csv
```

### Custom Ratios File
The system automatically creates and maintains `custom_ratios.csv` for persistent ratio storage.

## 🔍 Technical Details

### Word Counting Algorithm
- Uses regex pattern: `\b\w+\b`
- Handles Unicode text properly
- Counts hyphenated words as single units
- Ignores punctuation and whitespace

### Ratio Calculation
```
Estimated Target Words = English Word Count × Language Ratio
```

### Error Handling
- Graceful handling of missing languages (uses default ratio)
- Robust CSV parsing with encoding detection
- Progress tracking for large file processing
- Input validation and user feedback

## 📊 Performance

- **Processing Speed**: ~50,000 rows per minute
- **Memory Usage**: Efficient streaming for large files
- **File Size Support**: Tested with 70MB+ CSV files
- **Accuracy**: Based on 266,000+ real translation pairs

## 🤝 Contributing

To add new languages or improve ratios:

1. Prepare translation data in the required CSV format
2. Use the batch processing mode to analyze your data
3. Update ratios using the `update csv` or `update excel` commands
4. The system will automatically save and use your custom ratios

## 🌐 Deployment

### Live Application
The system is deployed and accessible at: **https://mt-word-count-estimator.streamlit.app/**

### Technical Details
- **Platform**: Streamlit Cloud
- **Repository**: https://github.com/AD-SamLi/word-count-estimator
- **Deployment**: Automatic updates from main branch
- **Availability**: 24/7 free hosting
- **Requirements**: Public GitHub repository

### For Developers
To deploy your own instance:
1. Fork the repository
2. Create a Streamlit Cloud account
3. Connect your GitHub repository
4. Deploy with `streamlit_app.py` as the main file

## 📄 License

This project is provided as-is for translation estimation purposes.

## 🆘 Support

For issues or questions:
1. **Try the live app first**: https://mt-word-count-estimator.streamlit.app/
2. Check the command reference above
3. Use the `help` command within the system
4. Verify your input file format matches the specifications
5. Ensure all required columns are present in your CSV files

---

**Last Updated**: January 2025  
**Version**: 2.1 - Live Deployment  
**Languages Supported**: 23  
**Data Source**: 266,000+ translation pairs  
**Live App**: https://mt-word-count-estimator.streamlit.app/
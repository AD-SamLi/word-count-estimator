# Word & Character Count Estimation System

A comprehensive system for estimating translated word AND character counts from English to various target languages using data-driven ratios derived from real translation data.

## 🌐 **Live Web Application**

**🚀 Try it now:** https://mt-word-count-estimator.streamlit.app/

**Features available online:**
- ⚡ **Quick Estimates** - Get instant word AND character count estimates for any language
- 📊 **Batch Processing** - Upload CSV files for bulk estimation (adds both word & character columns)
- 🔧 **Ratio Management** - View and update language expansion ratios for words & characters
- 📈 **Translation Analysis** - Automatically calculate word & character ratios from your translation data
- 📱 **Mobile Friendly** - Works on any device, no installation required

*No installation required - works directly in your browser!*

## 🎯 Overview

This system provides accurate **word and character count estimations** for translation projects by analyzing actual translation data and applying learned language-specific expansion/compression ratios. It supports both interactive single estimates and batch processing of large CSV datasets with dual counting methodologies.

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
- **Automatic word & character ratio analysis** from translation data (NEW!)
- **Real-time analytics** and visualizations for both metrics
- **Interactive language management** with live updates
- **Export functionality** (CSV, Excel) with one-click downloads

### ✅ Dual Estimation Mode (NEW!)
- **Quick word count estimates** for any language
- **Quick character count estimates** for any language
- **Side-by-side comparison** of word vs character ratios
- Real-time language support display
- User-friendly command interface

### ✅ Enhanced Batch Processing Mode
- Process large CSV files with translation data
- Add **both word AND character estimation columns** to existing datasets
- Progress tracking for large files
- **Web-based progress monitoring**
- **Dual-metric analysis** for comprehensive estimation

### ✅ Advanced Ratio Management
- **Automatic word & character ratio calculation** from translation data (NEW!)
- **Dual ratio system** - separate optimization for words and characters
- Update ratios from Excel/CSV files
- Persistent custom ratio storage for both metrics
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
The system adds six new columns to your CSV:
- `source_word_count`: Calculated English word count
- `estimated_target_words`: Estimated target language word count
- `estimation_ratio`: Word ratio used for estimation
- `source_char_count`: Calculated English character count (NEW!)
- `estimated_target_chars`: Estimated target language character count (NEW!)
- `char_estimation_ratio`: Character ratio used for estimation (NEW!)

### 2. Custom Word Ratios CSV Format

To update word language ratios, use this format:

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
| `ratio` | Float | Word expansion/compression ratio | `1.341`, `0.998` |

### 3. Custom Character Ratios CSV Format (NEW!)

To update character language ratios, use this format:

```csv
language,char_ratio
fr,1.245
de,1.089
es,1.198
ja,0.892
```

#### Columns:
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `language` | String | Language code | `"fr"`, `"de"` |
| `char_ratio` | Float | Character expansion/compression ratio | `1.245`, `1.089` |

### 4. Excel Ratios Format

For Excel files (.xlsx), use the same structure as CSV:
- **Word Ratios**: Column A = Language codes, Column B = Word ratios
- **Character Ratios**: Column A = Language codes, Column B = Character ratios  
- **Row 1**: Headers (`language`, `ratio` or `language`, `char_ratio`)
- **Row 2+**: Data

*Note: The system automatically detects whether you're updating word or character ratios based on the column headers.*

## 🎮 Usage Examples

### 🌐 Web Interface Usage

1. **Start the web app:**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Quick Estimates:**
   - Navigate to "Quick Estimate" page
   - Enter English word OR character count and select target language
   - Get instant results with expansion/compression analysis for both metrics

3. **Batch Processing:**
   - Go to "Batch Processing" page
   - Upload CSV file with drag-and-drop
   - Download results with added word AND character estimation columns

4. **Ratio Analysis (NEW!):**
   - Upload translation data CSV to automatically calculate word & character ratios
   - Analyze your own translation data for better accuracy in both metrics
   - One-click ratio updates with validation for both ratio types

5. **Language Management:**
   - Use "Language Management" to view, add, or update word & character ratios
   - Import/export ratio configurations for both metrics
   - Real-time ratio validation

### 💻 Command Line Usage

```bash
# Start the CLI system
python unified_word_count_estimator.py

# Quick word estimates
💬 Enter command: 1000 fr
✅ 1,000 English words → 1,341 French words

# Quick character estimates (NEW!)
💬 Enter command: char 5000 fr
✅ 5,000 English characters → 6,225 French characters

💬 Enter command: 500 ja  
✅ 500 English words → 257 Japanese words

# Show available languages
💬 Enter command: languages

# Show current word ratios
💬 Enter command: show

# Show current character ratios (NEW!)
💬 Enter command: showchar
```

### Batch Processing (CLI)

```bash
# Process a CSV file (adds both word & character estimates)
💬 Enter command: batch input_data.csv output_with_estimates.csv
Processing input_data.csv ...
Processed 50,000 rows...
✅ Done! Output: output_with_estimates.csv
```

### Automatic Ratio Analysis (CLI) - Enhanced!

```bash
# Analyze translation data and auto-update both word & character ratios
💬 Enter command: analyze all_results_en.csv
Analyzing translation data from all_results_en.csv...

📊 CALCULATED WORD RATIOS FROM 266,000 ROWS:
fr         (French             ): 1.3410 (was 1.3410) [19,000 samples]
de         (German             ): 0.9980 (was 0.9980) [24,000 samples]

📊 CALCULATED CHARACTER RATIOS FROM 266,000 ROWS:
fr         (French             ): 1.2450 (was 1.2450) [19,000 samples]
de         (German             ): 1.0890 (was 1.0890) [24,000 samples]

✅ Updated 23 word ratios based on your translation data
✅ Updated 23 character ratios based on your translation data
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
| `<number> <lang>` | Quick word estimate | `1000 fr` |
| `char <number> <lang>` | Quick character estimate (NEW!) | `char 5000 fr` |
| `batch <input> <output>` | Process CSV (adds word & char estimates) | `batch data.csv results.csv` |
| `analyze <translation_csv>` | Auto-update word & char ratios from data | `analyze all_results_en.csv` |
| `languages` | Show detailed language info | |
| `show` | Display current word ratios | |
| `showchar` | Display current character ratios (NEW!) | |
| `update csv <path>` | Update from CSV | `update csv ratios.csv` |
| `update excel <path>` | Update from Excel | `update excel ratios.xlsx` |
| `help` | Show help | |
| `quit` | Exit program | |

## 🔧 Enhanced Data Analysis Utility

Use `analyze_data.py` to explore your translation datasets with comprehensive metrics:

```bash
python analyze_data.py [csv_file]
```

This utility provides:
- Dataset structure analysis
- Language distribution statistics
- Translation system breakdown
- **Word ratio analysis** for all languages (NEW!)
- **Character ratio analysis** for all languages (NEW!)
- Data quality insights with dual metrics
- Comprehensive summary export

## 📈 Dual Language Ratios

The system uses optimized ratios derived from analyzing 266,000+ real translation examples:

### Word Count Ratios (VALIDATED!)
| Language | Code | Word Ratio | Word Expansion/Compression |
|----------|------|------------|----------------------------|
| Chinese (Traditional) | zh-hant | **0.5177** | **48% word compression** |
| Japanese | ja | **0.5307** | **47% word compression** |
| Chinese (Simplified) | zh-hans | **0.5271** | **47% word compression** |
| Finnish | fi | **0.7774** | **22% word compression** |
| Korean | ko | **0.8529** | **15% word compression** |
| German | de | **0.9979** | **0% word change** |
| Danish | da | **1.0006** | **No word change** |
| Spanish | es | **1.2168** | **22% word expansion** |
| French | fr | **1.4429** | **44% word expansion** |

### Character Count Ratios (VALIDATED!)
| Language | Code | Char Ratio | Character Expansion/Compression |
|----------|------|------------|--------------------------------|
| Chinese (Traditional) | zh-hant | **0.4856** | **51% character compression** |
| Chinese (Simplified) | zh-hans | **0.5102** | **49% character compression** |
| Korean | ko | **0.5709** | **43% character compression** |
| Japanese | ja | **0.6638** | **34% character compression** |
| Finnish | fi | **1.0939** | **9% character expansion** |
| Norwegian | nb | **1.0714** | **7% character expansion** |
| Danish | da | **1.1168** | **12% character expansion** |
| German | de | **1.2359** | **24% character expansion** |
| Spanish | es | **1.236** | **24% character expansion** |
| French | fr | **1.4617** | **46% character expansion** |

## ⚙️ Configuration

### Environment Variables (.env)
```env
# Optional configuration
DEFAULT_RATIO=1.15
DEFAULT_CHAR_RATIO=1.12
RATIO_FILE=custom_ratios.csv
CHAR_RATIO_FILE=custom_char_ratios.csv
```

### Custom Ratios Files
The system automatically creates and maintains:
- `custom_ratios.csv` for persistent word ratio storage
- `custom_char_ratios.csv` for persistent character ratio storage (NEW!)

## 🔍 Technical Details

### Word Counting Algorithm
- Uses regex pattern: `\b\w+\b`
- Handles Unicode text properly
- Counts hyphenated words as single units
- Ignores punctuation and whitespace

### Character Counting Algorithm (NEW!)
- Counts all characters including spaces
- Excludes leading/trailing whitespace
- Handles Unicode text properly
- Preserves text formatting context

### Dual Ratio Calculation
```
Estimated Target Words = English Word Count × Word Language Ratio
Estimated Target Characters = English Character Count × Character Language Ratio
```

### Error Handling
- Graceful handling of missing languages (uses default ratios for both metrics)
- Robust CSV parsing with encoding detection
- Progress tracking for large file processing
- Input validation and user feedback
- Dual-metric validation and fallback handling

## 📊 Performance

- **Processing Speed**: ~50,000 rows per minute (dual calculations)
- **Memory Usage**: Efficient streaming for large files
- **File Size Support**: Tested with 70MB+ CSV files
- **Accuracy**: Based on 266,000+ real translation pairs
- **Dual Metrics**: Simultaneous word and character analysis

## 🤝 Contributing

To add new languages or improve ratios:

1. Prepare translation data in the required CSV format
2. Use the batch processing mode to analyze your data
3. Use `analyze` command to automatically calculate both word & character ratios
4. Manually update ratios using the `update csv` or `update excel` commands
5. The system will automatically save and use your custom ratios for both metrics

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
**Version**: 2.3 - Validated Ratios from Real Data  
**Languages Supported**: 23 (with validated dual ratios)  
**Data Source**: 266,000+ translation pairs (ANALYZED & VALIDATED)  
**Metrics**: Word & Character Count Estimation  
**Live App**: https://mt-word-count-estimator.streamlit.app/
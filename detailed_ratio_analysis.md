# Detailed Ratio Analysis - all_results_en.csv

## Analysis Summary
**Dataset**: all_results_en.csv  
**Total Rows Processed**: 266,000  
**Languages Analyzed**: 23  
**Analysis Date**: January 2025  

## Methodology
- Used `reference` column as target text (human reference translations)
- Word counting: regex pattern `\b\w+\b` 
- Character counting: all characters including spaces, excluding leading/trailing whitespace
- Minimum sample size: 10 translations per language for ratio calculation

---

## Word Ratio Analysis

### Major Discrepancies Found:

| Language | Code | Original Default | Calculated Actual | Difference | Sample Size | Impact |
|----------|------|------------------|-------------------|------------|-------------|---------|
| **French** | fr | 1.341 | **1.4429** | +0.1019 | 19,000 | **7.6% underestimation** |
| **Czech** | cs | 0.938 | **0.9352** | -0.0028 | 15,000 | 0.3% overestimation |
| **Spanish** | es | 1.215 | **1.2168** | +0.0018 | 12,000 | 0.1% underestimation |
| **Finnish** | fi | 0.780 | **0.7774** | -0.0026 | 9,000 | 0.3% overestimation |
| **Japanese** | ja | 0.513 | **0.5307** | +0.0177 | 12,000 | **3.5% underestimation** |
| **Korean** | ko | 0.855 | **0.8529** | -0.0021 | 11,000 | 0.2% overestimation |
| **German** | de | 0.998 | **0.9979** | -0.0001 | 24,000 | Negligible |
| **Danish** | da | 1.000 | **1.0006** | +0.0006 | 12,000 | Negligible |

### Minor Adjustments:

| Language | Code | Original Default | Calculated Actual | Difference | Sample Size |
|----------|------|------------------|-------------------|------------|-------------|
| Turkish | tr | 0.938 | 0.9337 | -0.0043 | 7,000 |
| Russian | ru | 0.948 | 0.9464 | -0.0016 | 11,000 |
| Polish | pl | 0.939 | 0.9706 | +0.0316 | 8,000 |
| Dutch | nl | 1.040 | 1.0387 | -0.0013 | 8,000 |
| Italian | it | 1.155 | 1.1528 | -0.0022 | 12,000 |
| Portuguese | pt | 1.170 | 1.1706 | +0.0006 | 11,000 |

---

## Character Ratio Analysis

### Major Discrepancies Found:

| Language | Code | Original Default | Calculated Actual | Difference | Sample Size | Impact |
|----------|------|------------------|-------------------|------------|-------------|---------|
| **French** | fr | 1.245 | **1.4617** | +0.2167 | 19,000 | **17.4% underestimation** |
| **German** | de | 1.089 | **1.2359** | +0.1469 | 24,000 | **13.5% underestimation** |
| **Japanese** | ja | 0.892 | **0.6638** | -0.2282 | 12,000 | **25.6% overestimation** |
| **Korean** | ko | 1.234 | **0.5709** | -0.6631 | 11,000 | **53.7% overestimation** |
| **Chinese (Simplified)** | zh-hans | 0.634 | **0.5102** | -0.1238 | 18,000 | **19.5% overestimation** |
| **Chinese (Traditional)** | zh-hant | 0.612 | **0.4856** | -0.1264 | 8,000 | **20.6% overestimation** |
| **Spanish** | es | 1.198 | **1.236** | +0.038 | 12,000 | **3.2% underestimation** |
| **Danish** | da | 1.045 | **1.1168** | +0.0718 | 12,000 | **6.9% underestimation** |

### Moderate Adjustments:

| Language | Code | Original Default | Calculated Actual | Difference | Sample Size | Impact |
|----------|------|------------------|-------------------|------------|-------------|---------|
| Finnish | fi | 1.012 | 1.0939 | +0.0819 | 9,000 | 8.1% underestimation |
| Italian | it | 1.178 | 1.244 | +0.066 | 12,000 | 5.6% underestimation |
| Russian | ru | 1.089 | 1.1741 | +0.0851 | 11,000 | 7.8% underestimation |
| Dutch | nl | 1.067 | 1.1711 | +0.1041 | 8,000 | 9.8% underestimation |
| Polish | pl | 1.098 | 1.1765 | +0.0785 | 8,000 | 7.1% underestimation |

---

## Key Findings

### 1. **French Ratios Need Major Updates**
- **Word ratio**: 7.6% underestimation (1.341 → 1.4429)
- **Character ratio**: 17.4% underestimation (1.245 → 1.4617)
- **Impact**: Significant underestimation of French translation length

### 2. **Asian Languages Have Mixed Results**
- **Japanese**: Word ratio close (+3.5%), but character ratio significantly overestimated (-25.6%)
- **Korean**: Word ratio close (-0.2%), but character ratio drastically overestimated (-53.7%)
- **Chinese**: Both ratios overestimated by ~20%

### 3. **European Languages Generally Accurate**
- **German**: Word ratio very accurate, character ratio needs +13.5% adjustment
- **Spanish**: Both ratios quite accurate (word: +0.1%, character: +3.2%)
- **Italian, Dutch, Polish**: Character ratios underestimated by 5-10%

### 4. **Sample Size Reliability**
All languages have robust sample sizes (4,000-24,000 translations), ensuring statistical reliability.

---

## Recommendations

### 1. **Immediate Updates Required**
Update the DEFAULT_CHAR_RATIOS in unified_word_count_estimator.py with calculated values:

```python
DEFAULT_CHAR_RATIOS = {
    'de': 1.2359,  # was 1.089 (+13.5%)
    'fr': 1.4617,  # was 1.245 (+17.4%)
    'zh-hans': 0.5102,  # was 0.634 (-19.5%)
    'cs': 1.0827,  # was 1.078 (+0.4%)
    'ro': 1.1399,  # was 1.134 (+0.5%)
    'da': 1.1168,  # was 1.045 (+6.9%)
    'es': 1.236,   # was 1.198 (+3.2%)
    'fr-ca': 1.2992,  # was 1.220 (+6.5%)
    'hu': 1.1923,  # was 1.165 (+2.4%)
    'ja': 0.6638,  # was 0.892 (-25.6%)
    'it': 1.244,   # was 1.178 (+5.6%)
    'ko': 0.5709,  # was 1.234 (-53.7%)
    'pt': 1.1843,  # was 1.156 (+2.5%)
    'ru': 1.1741,  # was 1.089 (+7.8%)
    'fi': 1.0939,  # was 1.012 (+8.1%)
    'nb': 1.0714,  # was 1.034 (+3.6%)
    'pt-pt': 1.1817,  # was 1.154 (+2.4%)
    'nl': 1.1711,  # was 1.067 (+9.8%)
    'pl': 1.1765,  # was 1.098 (+7.1%)
    'sv': 1.0926,  # was 1.056 (+3.5%)
    'zh-hant': 0.4856,  # was 0.612 (-20.6%)
    'tr': 1.0997,  # was 1.078 (+2.0%)
    'mx': 1.1816   # was 1.145 (+3.2%)
}
```

### 2. **Word Ratios Minor Updates**
Only French needs significant update:
```python
'fr': 1.4429,  # was 1.341 (+7.6%)
```

### 3. **Quality Assurance**
- The system has automatically saved these ratios to custom files
- All future estimates will use the corrected ratios
- Consider re-running batch processing on existing datasets with updated ratios

---

## Validation Status
✅ **Analysis Complete**: All 23 languages validated against 266,000 real translation pairs  
✅ **Ratios Updated**: Both word and character ratios automatically updated  
✅ **Files Saved**: custom_ratios.csv and custom_char_ratios.csv created  
✅ **High Confidence**: Large sample sizes ensure statistical reliability  

The system is now using **data-driven, validated ratios** based on real translation performance rather than theoretical estimates.
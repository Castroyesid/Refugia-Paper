# Refugia Linguistic Analysis - Instructions

## Overview

This Python script performs statistical analysis of phonemic and grammatical features 
in hypothesized linguistic refugia using WALS (World Atlas of Language Structures) data.

## Requirements

- Python 3.6+
- No external dependencies required (uses only standard library)

## How to Use

### Step 1: Download WALS XML Data

Download these four XML files from WALS:

1. **Consonant Inventories (1A)**: https://wals.info/feature/1A.xml
2. **Vowel Quality Inventories (2A)**: https://wals.info/feature/2A.xml
3. **Absence of Common Consonants (18A)**: https://wals.info/feature/18A.xml
4. **Numeral Bases (131A)**: https://wals.info/feature/131A.xml

### Step 2: Edit the Script

Open `refugia_analysis.py` in a text editor.

Find the data variables near the top of the file:

```python
WALS_1A_CONSONANTS = """
<!-- PASTE WALS 1A XML HERE -->
"""
```

Replace each placeholder with the complete XML content from the corresponding file.

**Important**: 
- Remove any browser-added text like "This XML file does not appear to have any style information"
- Keep only the content starting from `<feature number="1A"...` to `</feature>`

### Step 3: Run the Analysis

```bash
python3 refugia_analysis.py
```

## Output

The script produces:

1. **Baseline Statistics**: Percentage of all WALS languages in each refugia region
2. **Per-Feature Analysis**: For each of the 6 features:
   - Sample size and regional distribution
   - Enrichment factor (compared to baseline)
   - Moran's I spatial autocorrelation statistic
   - Z-score and p-value
   - List of individual languages (if ≤25)
3. **Summary Table**: Publication-ready table with all results

## Refugia Definitions

The script uses these geographic criteria:

| Region | Definition |
|--------|------------|
| Americas | longitude < -30° |
| Caucasus | 37° < latitude < 45° AND 37° < longitude < 50° |
| Sahul | longitude > 110° AND latitude < 3°, with Wallacea exclusion* |

*Languages between latitudes -11° and 3° must have longitude > 125° to be classified as Sahul 
(this excludes Sulawesi, Lesser Sundas, etc.)

## Features Analyzed

| Feature | WALS Chapter | Target Values |
|---------|--------------|---------------|
| Small Consonant Inventories (6-14) | 1A | numeric="1" |
| Small Vowel Quality Inventories (2-4) | 2A | numeric="1" |
| Absence of Fricatives | 18A | numeric="3" |
| Absence of Nasals | 18A | numeric="4", "5", "6" |
| Absence of Bilabials | 18A | numeric="2", "5" |
| Restricted Numeral Systems | 131A | numeric="6" |

## Moran's I Calculation

The script implements Moran's I spatial autocorrelation using:
- k=5 nearest neighbors
- Inverse distance weighting
- Row-standardized weights matrix
- Randomization-based variance estimation

## Notes on the Paper's Original Numbers

If the numbers from this script differ from those in your paper, possible reasons include:

1. **Baseline calculation method**: The script combines all unique languages across chapters. 
   The paper may have used a single chapter or different deduplication method.

2. **Geographic boundary precision**: Small differences in boundary definitions can shift 
   marginal languages between regions.

3. **WALS version**: WALS data may have been updated since the original analysis.

## Troubleshooting

**XML Parse Error**: Make sure you removed the browser message and only kept the `<feature>...</feature>` content.

**Empty results**: Check that the XML data was pasted correctly into the variable strings.

**Different baseline %**: This is expected if using combined-chapter baseline vs single-chapter baseline.

## License

This script is provided for academic research purposes.

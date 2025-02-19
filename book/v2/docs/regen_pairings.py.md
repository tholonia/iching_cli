# regen_pairings.py

## I Ching Pair-Path Analysis Generator

### Description
This script analyzes pairs of I Ching hexagrams that are inversions of each other, representing ascending and descending aspects of a pair-path. It processes hexagram data and uses AI to generate pair-path analysis.

### Usage
```
./regen_pairings.py <hex1> <hex2> <pair_number>
Example: ./regen_pairings.py 1 2 1
```

### Process
1. Loads data for both hexagrams from JSON files
2. Analyzes their relationship as a pair-path
3. Generates analysis using AI:
   - Title for the pair-path
   - Description of relationship
   - Image prompt for visualization
4. Updates both hexagram JSON files with pair-path data
5. Determines path stability (dynamic/stable)
6. Assigns pair-path number (1-32)

### Arguments
- `hex1`: First hexagram number (1-64)
- `hex2`: Second hexagram number (1-64)
- `pair_number`: Pair-path number (1-32)
- `--save`: Save changes back to JSON files

### Output
- Updates to hexagram JSON files with pair-path analysis
- Console output of generated analysis
- Status messages for process steps

### Pair-Path Features
- Identifies ascending/descending relationships
- Generates meaningful titles
- Creates descriptive analysis
- Provides image generation prompts
- Determines path stability
- Assigns canonical path numbers

### Dependencies
- Python 3.x
- openai
- json
- colorama

*Last Updated:* 03-21-2024 HH:MM

---


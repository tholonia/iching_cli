# Unicode Hexagram Character Converter

## This script processes JSON files containing I Ching hexagram data and updates their hexagram codes with the corresponding Unicode characters. It uses a mapping of hexagram IDs (1-64) to their respective Unicode characters (U+4DC0 to U+4DFF).

### The script:
1. Reads all JSON files in the `../regen` directory
2. For each file, extracts the 'id' field
3. Looks up the corresponding Unicode hexagram character
4. Updates the 'hexagram_code' field with the Unicode character
5. Saves the modified JSON file

### Each hexagram entry contains:
- bin: Binary representation (e.g., "111111")
- hex: Unicode hexagram character (e.g., "䷀")
- unicode: Unicode code point (e.g., "\u4DC0")

### Usage:
```bash
python unicode2char.py
```

### Requirements:
- Python 3.x
- JSON files must contain 'id' and 'hexagram_code' fields.

*Last Updated:* MM-DD-YYYY HH:MM

---


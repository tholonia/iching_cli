# print_fields.py

## I Ching Hexagram Field Extractor

### Description
This script extracts and displays specific fields from hexagram JSON files. It focuses on the "lines_in_transition" data, showing the first four words of each line's description for quick reference and verification.

### Usage
```bash
./print_fields.py
```

### Process
1. Scans `../_v2` directory for JSON files
2. For each hexagram file:
   - Extracts "lines_in_transition" data
   - Shows first four words for lines 1-6
   - Displays in order by hexagram number

### Dependencies
- Python 3.x
- Required modules: `json`, `os`

### File Structure
**Input:**
- `../_v2/*.json`: Hexagram JSON files

**Output Format:**
```
--- filename.json ---
[first four words of line 6]
[first four words of line 5]
...etc
```

**Author:** JW  
*Last Updated:* 10-19-2023 15:24

---


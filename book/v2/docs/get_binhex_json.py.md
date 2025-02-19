# get_binhex_json.py

## Hexagram JSON Data Extractor

### Description
Reads all JSON files from the `../regen` directory and extracts specific values including hexagram ID, code, name, and binary sequence.

### Usage
```bash
python get_binhex_json.py
```

### Input Files
- All JSON files in `../regen` directory with structure:
  ```json
  {
      "id": int,
      "hexagram_code": str,
      "name": str,
      "binary_sequence": int
  }
  ```

### Output
Pretty prints sorted array of hexagram data:  
`[id, hexagram_code, binary_sequence, name]`

### Functions
- `read_hexagram_info(file_path)`
  - Reads JSON file and extracts hexagram information
  - Handles file not found and JSON parsing errors
  - Returns formatted output of hexagram data

### Dependencies
- `json`: JSON file parsing
- `os`: File system operations
- `pathlib`: Path handling
- `pprint`: Pretty printing of data structures

*Author:* JW  
*Last Updated:* 10-15-2024 12:34

---


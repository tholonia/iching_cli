# line_types.py

## I Ching Line Type Generator

### Description
This script processes hexagram JSON files to create or update line_type values based on binary sequences. It converts 6-digit binary numbers into an array of yin/yang symbols (⚊/⚋) for each hexagram.

### Usage
```bash
./line_types.py <json_file> [--save]
```

### Arguments
- `json_file`: Path to the hexagram JSON file to process
- `--save`: Optional flag to save changes back to the JSON file

### Examples
```bash
./line_types.py hexagram.json         # Display output only
./line_types.py hexagram.json --save  # Update JSON file
```

### Process
1. Reads `binary_sequence` from input JSON file.
2. Converts to 6-digit binary string with zero padding.
3. Maps binary digits to yin/yang symbols (1->⚊, 0->⚋).
4. Updates `line_type` array in JSON.
5. Optionally saves back to file.

### Dependencies
- Python 3.x
- Required modules: `json`, `argparse`, `sys`

### File Structure
- Input/Output: JSON file containing:
  - `binary_sequence`: Integer (0-63)
  - `line_type`: Array of 6 symbols

*Author: JW*

*Last Updated:* 09-29-2023 14:00

---


# Hexbin Binary Value Extractor

## hexbinvals.py

### Description
This script extracts and displays hexagram binary sequences and their corresponding hex values from JSON files. It processes one or more hexagram numbers provided as command-line arguments.

### Usage
```bash
python hexbinvals.py num1,num2,num3,...
```
Example: 
```bash
python hexbinvals.py 1,2,3
```

### Arguments
- **numbers**: Comma-separated list of hexagram numbers to process  
  Numbers will be zero-padded to two digits (1 -> "01")

### Process
1. Accepts comma-separated hexagram numbers from command line
2. Converts numbers to zero-padded two-digit strings
3. Loads corresponding JSON files from regen directory
4. Extracts hex ID and binary sequence for each hexagram
5. Displays results in format: "Hex X = binary_sequence"

### Dependencies
- **json**: JSON file parsing
- **pathlib**: Cross-platform path handling
- **sys**: Command line argument processing

### File Structure
**Input:**  
- `../regen/XX.json`: Hexagram data files where XX is hexagram number  
  Each JSON file contains:
  - **id**: Hexagram identifier
  - **binary_sequence**: Binary representation of hexagram

**Output Format:**  
`Hex <id> = <binary_sequence>`  
Example: `"Hex 01 = 111111"`

### Error Handling
- Validates command line arguments
- Checks for file existence
- Verifies JSON structure
- Reports specific error messages for each failure case

*Author: JW*  
*Last Updated:* 10-24-2024 12:00

---


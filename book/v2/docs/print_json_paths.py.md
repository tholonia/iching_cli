# print_json_paths.py

## JSON Path Structure Analyzer

### Description
This script processes a JSON file and prints all paths to each value in the JSON structure. It helps visualize and analyze the hierarchical structure of JSON data by showing complete paths to all values.

### Usage
```bash
./print_json_paths.py <file_path>
```

### Arguments
- `file_path`: Full path to the JSON file to analyze

### Process
1. Reads the specified JSON file
2. Recursively traverses the JSON structure
3. For each element encountered:
   - Builds the complete path using dot notation
   - Handles both objects and arrays
   - Prints each unique path

### Dependencies
- Python 3.x
- Required modules: `json`, `argparse`, `pathlib`

### Output Format
```
Paths for example.json:
key1
key1.subkey1
key1.array[0]
key1.array[1]
...etc
```

*Author:* JW  
*Last Updated:* 10-10-2023 09:58

---


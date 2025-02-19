# JSON Schema Generator for I Ching Data

## gen_schema.py

### Description
This script generates a JSON schema from an input JSON file, specifically designed for I Ching data structures. It analyzes the structure and data types of the input JSON and creates a corresponding schema that describes the format and validation rules for hexagram data files.

### Usage
```bash
./gen_schema.py <input_json_file>
```
Example:
```bash
./gen_schema.py ../regen/01.json
```

### Process
1. Reads input JSON file (typically a hexagram data file)
2. Analyzes structure recursively:
   - Determines data types for all fields
   - Identifies required fields (non-null values)
   - Handles arrays and nested objects
   - Processes special I Ching specific structures
3. Generates schema with:
   - Property definitions for hexagram data
   - Type information for all fields
   - Required field lists
   - Validation rules for I Ching specific data
4. Saves schema to `schema.json`

### Arguments
- `input_json_file`: Path to the input JSON file to analyze (typically a hexagram JSON file from `../regen/`)

### Output
- `schema.json`: Generated JSON schema file that describes the hexagram data format and validation rules

### Schema Features
- Validates hexagram structure
- Enforces required fields
- Type checking for all properties
- Handles nested objects (trigrams, lines, etc.)
- Array validation for line data
- Special handling for I Ching specific fields

### Dependencies
- Python 3.x
- `json` (standard library)
- `typing`

*Last Updated:* 03-21-2024 14:56

---


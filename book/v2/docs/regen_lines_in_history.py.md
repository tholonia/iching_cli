# regen_lines_in_history.py

## I Ching Line History Generator

### Description
This script generates the six stages of change for a specific hexagram's history section using the OpenAI API. It processes a JSON file containing hexagram data and updates it with generated line-by-line interpretations.

### Usage
```bash
./regen_lines_in_history.py <source_dir> <hexagram_number>
```

### Arguments
- **source_dir**: Directory containing hexagram JSON files
- **hexagram_number**: Number of hexagram to process (1-64)

### Process
1. Validates input arguments and file existence
2. Loads hexagram JSON data
3. Extracts history section
4. Uses OpenAI API to generate line interpretations
5. Updates JSON with new line data:
   - **name**: Concept name for the line
   - **meaning**: Line interpretation
   - **changing**: Meaning when line changes

### Dependencies
- Python 3.x
- Required packages: openai, colorama
- OpenAI API key in environment

### File Structure
- Input/Output: `<source_dir>/<hexagram_number>.json`

### Environment
OPENAI_API_KEY: OpenAI API authentication key

*Last Updated:* 10-13-2023 11:23

---


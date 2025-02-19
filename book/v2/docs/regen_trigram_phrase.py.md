# Regen Lines in Trans

## I Ching Line Transition Generator

### Description
This script generates line transition interpretations for I Ching hexagrams using the OpenAI API. It processes JSON files containing hexagram data and updates them with new line-by-line transition meanings. For each line, it generates a name, meaning, and changing line interpretation based on the hexagram's context.

### Usage
```bash
./regen_lines_in_trans.py <source_dir> <dest_dir>
```

### Arguments
- **source_dir**: Directory containing source hexagram JSON files
- **dest_dir**: Directory to write updated JSON files

### Process
1. Validates input/output directories
2. Loads hexagram JSON data
3. For each hexagram (1-64):
   - Extracts hexagram context and data
   - Uses OpenAI API to generate line transitions
   - For each line (1-6):
     * Generates name capturing transition concept
     * Generates meaning interpretation
     * Generates changing line interpretation
4. Updates JSON with new line data
5. Saves to destination directory

### Dependencies
- Python 3.x
- Required packages: openai, colorama
- OpenAI API key in environment

### File Structure
- Input: `<source_dir>/<hexagram>.json`
- Output: `<dest_dir>/<hexagram>.json`

### Environment
- **OPENAI_API_KEY**: OpenAI API authentication key

### Error Handling
- Validates directory paths
- Ensures valid JSON formatting
- Handles API errors gracefully

*Last Updated:* 10-05-2024 15:43

---


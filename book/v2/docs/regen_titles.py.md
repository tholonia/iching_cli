# regen_titles.py

## I Ching Hexagram Title Generator

### Description
This script uses the OpenAI API to generate a concise one- or two-word title that best expresses the core concept of a specific I Ching hexagram. It processes a JSON file containing hexagram data and updates the title based on the hexagram's meaning and context.

### Usage
```bash
./regen_titles.py <source_dir> <hexagram_number>
```

### Arguments
- **source_dir**: Directory containing hexagram JSON files
- **hexagram_number**: Number of hexagram to process (1-64)

### Process
1. Validates input arguments and file existence
2. Loads hexagram JSON data
3. Extracts current hexagram name
4. Uses OpenAI API to generate new concise title
5. Updates JSON with new title

### Dependencies
- Python 3.x
- Required packages: openai, colorama
- OpenAI API key in environment

### File Structure
- Input/Output: `<source_dir>/<hexagram_number>.json`

### Environment
- `OPENAI_API_KEY`: OpenAI API authentication key

*Last Updated:* 10-15-2023 12:00

---


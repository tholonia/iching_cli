# regen_lines_in_context.py

## Generate six stages of change for a specific story in I Ching Hexagrams using OpenAI API

### Usage
```
./regen_lines_in_context.py <source_dir> <hexagram_number> <story_index>
```

### Required Arguments
- **source_dir**: The directory containing the source JSON files
- **hexagram_number**: The number of the hexagram to process (1-64)
- **story_index**: The index of the story to process (0-based index)

### Example
```
./regen_lines_in_context.py ../regen 01 0
```

### Process
1. Validates input arguments and file paths
2. Loads hexagram data from JSON file
3. Extracts specified story by index
4. Generates six stages of change using OpenAI API
5. Updates JSON with new line data:
   - **name**: Concept title for the stage
   - **meaning**: Description of the stage
   - **changing**: Interpretation when line changes

### Dependencies
- **OpenAI Python package** (v1.0.0 or later)
- **colorama**: Terminal output formatting
- Required files:
  - `../includes/iching_primer.md`
  - `../includes/tholonic_primer.md`

### Environment Variables
- **OPENAI_API_KEY**: Your OpenAI API key (required)

### File Structure
**Input:**
- `<source_dir>/<hexagram_number>.json`
- `../includes/iching_primer.md`
- `../includes/tholonic_primer.md`

**Output:**
- Updated JSON file with new `lines_in_context` data

*Last Updated:* MM-DD-YYYY HH:MM

---


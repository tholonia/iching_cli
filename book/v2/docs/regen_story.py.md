# regen_story.py

## I Ching Story Regenerator

### Description
This script regenerates stories for I Ching hexagrams using various AI providers. It takes a JSON file containing story data and an entry index as input, then updates the specified story with new AI-generated content while preserving the existing structure.

### Usage
```bash
./regen_story.py -f <input_json_file> -i <entry_index> -p <provider> [-s]
```

### Arguments
- `-f, --filename`: Path to JSON file containing stories data
- `-i, --index`: Integer specifying which story entry to update (0-based index)
- `-p, --provider`: AI provider to use (e.g., openai, grok, anthropic)
- `-s, --save`: Save the modified data back to the input file (optional)

### Example
```bash
./regen_story.py -f ../regen/01.json -i 0 -p openai -s
./regen_story.py --filename ../regen/01.json --index 0 --provider grok
```

### Process
1. Reads and validates input JSON file against schema
2. Makes API request to specified AI provider for new story content
3. Updates specified story entry with new content:
   - title
   - theme
   - short_story
   - lines_in_context (name, meaning, changing for each line)
4. Optionally saves changes back to input file
5. Prints complete JSON output in red

### Environment Variables
- `OPENAI_API_KEY`: Required for OpenAI API access
- Other provider-specific keys as needed

### Dependencies
- OpenAI Python package
- jsonschema
- colorama
- regen_story_lib.py (local library)
- funcs_lib.py (local library)

### Output
- Prints formatted story to stdout
- Returns updated stories data structure
- Optionally saves modified JSON back to input file

*Author:* Assistant  
*Last Updated:* 10-04-2023 12:34

---


# regen_story.py

## I Ching Story Generator

### Description
This script generates new stories for I Ching hexagrams using OpenAI's GPT API. It takes a JSON file containing story data and an entry index as input, then updates the specified story with new AI-generated content.

### Usage
```bash
./regen_story.py --filename <input_json_file> --index <entry_index>
./regen_story.py -f <input_json_file> -i <entry_index>
```

### Arguments
- `-f`, `--filename` : Path to JSON file containing stories data
- `-i`, `--index`    : Integer specifying which story entry to update (0-based index)
- `-s`, `--save`     : Save the modified data back to the input file

### Example
```bash
./regen_story.py --filename ../regen/01.json --index 0
./regen_story.py -f ../regen/01.json -i 0
```

### Environment Variables
- `OPENAI_API_KEY`: Required OpenAI API key for making requests

### Process
1. Reads and validates input JSON file against schema
2. Makes API request to OpenAI for new story content
3. Updates specified story entry with new content:
   - title
   - theme
   - short_story
   - lines_in_context (name, meaning, changing for each line)
4. Prints updated story and returns modified data structure

### Dependencies
- OpenAI Python package
- jsonschema
- colorama
- regen_story_lib.py (local library)

### Output
- Prints formatted story to stdout
- Returns updated stories data structure
- Prints complete JSON output in red

*Last Updated:* 10-15-2023 03:45

---


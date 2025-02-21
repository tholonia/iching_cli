# regen_history.py

## I Ching Historical Context Generator

### Description
Generates historical context and interpretations for I Ching hexagrams using various AI APIs. Takes a hexagram JSON file as input and generates new historical perspectives and line interpretations.

### Usage
```shell
./regen_history.py -f <input_json_file> -p <provider> [-s]
```

### Arguments
- `-f, --filename` : Path to hexagram JSON file (e.g., ../regen/01.json)
- `-p, --provider` : AI provider to use (openai, grok, anthropic, google)
- `-s, --save`     : Save the modified data back to the input file

### Environment Variables
- `OPENAI_API_KEY`  : For OpenAI API access
- `GROK_API_KEY`    : For Grok API access
- `ANTHROPIC_KEY`   : For Anthropic API access
- `GOOGLE_API_KEY`  : For Google API access

### Process
1. Reads hexagram data from JSON file
2. Generates new historical context using specified AI provider
3. Updates:
   - Title and subtitle
   - Historical source reference
   - Historical context and interpretation
   - Line-by-line historical meanings and changes

### Output
- Prints formatted historical context
- Outputs complete JSON if not saving
- Updates input file if `--save` specified

### Dependencies
- requests
- jsonschema
- colorama
- funcs_lib.py

*Author:* Assistant  
*Last Updated:* 03-04-2024 00:00

---


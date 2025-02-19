# regen_trigrams_phrase_general.py

## I Ching Trigram Phrase Generator

### Description
This script generates a general trigram phrase for an I Ching hexagram by combining multiple philosophical perspectives (Jungian, Platonic, Taoist, Tholonic, and Thermodynamic) into a single comprehensive description. It processes a single JSON file containing hexagram data and can either display or save the generated phrase.

### Usage
```bash
./regen_trigrams_phrase_general.py <filename> [--save]
Example: ./regen_trigrams_phrase_general.py 01.json --save
```

### Arguments
- `filename`: JSON file to process (e.g., 01.json)
- `--save`: Optional flag to save updates to the JSON file

### Process
1. Loads specified hexagram JSON file
2. Extracts existing trigram phrases from different perspectives
3. Uses OpenAI API to generate a combined general phrase
4. Either displays the result or saves it back to the file
5. Updates JSON with new 'general' field under 'trigram_phrase'

### Dependencies
- Python 3.x
- Required packages: openai, colorama
- OpenAI API key in environment

### File Structure
**Input JSON format:**
```json
{
  "trigram_phrase": {
    "Jungian": "...",
    "Platonic": "...",
    "Taoist": "...",
    "Tholonic": "...",
    "Thermodynamics": "..."
  }
}
```

### Environment
- `OPENAI_API_KEY`: OpenAI API authentication key

### Error Handling
- Validates file existence
- Ensures valid JSON formatting
- Handles API errors gracefully
- Reports errors in color-coded output

*Author: JW*

*Last Updated:* 10-10-2023 10:00

---

